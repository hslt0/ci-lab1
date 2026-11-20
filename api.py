import math
import random

from fastapi import FastAPI, Response
from pydantic import BaseModel, ConfigDict, Field


app = FastAPI(
    title="Echo sounder API",
    version="1.0.0",
)


class EchoConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    total_steps: int = Field(..., gt=0, description="Кількість точок зондування")
    sample_rate: float = Field(..., gt=0, description="Частота дискретизації АЦП, Гц")
    sound_speed: float = Field(..., gt=0, description="Швидкість поширення звуку, м/с")
    carrier_freq: float = Field(..., gt=0, description="Несуча частота імпульсу, Гц")


ECHOSOUNDER_CONFIG = EchoConfig(
    total_steps=1000,
    sample_rate=44100.0,
    sound_speed=1500.0,
    carrier_freq=10000.0,
)

# Duration of the tone pulse is set independently of the route configuration.
PULSE_DURATION_SECONDS = 1e-3


def generate_pulse() -> list[float]:
    """Generate a finite-tone burst using one sample per ADC period."""
    sample_count = round(ECHOSOUNDER_CONFIG.sample_rate * PULSE_DURATION_SECONDS)
    return [
        math.sin(
            2 * math.pi
            * ECHOSOUNDER_CONFIG.carrier_freq
            * index
            / ECHOSOUNDER_CONFIG.sample_rate
        )
        for index in range(sample_count)
    ]


PULSE = generate_pulse()

SIGNAL_LENGTH = 512


@app.get(
    "/api/signal/{step}",
    response_model=list[float],
    summary="Отримати зашумлений сигнал для точки маршруту",
)
async def get_signal(step: int, response: Response) -> list[float]:
    if step < 0 or step >= ECHOSOUNDER_CONFIG.total_steps:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Крок маршруту поза допустимим діапазоном")

    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"

    true_shift = 80 + (step * 7 % 240)
    rng = random.Random(10_000 + step)
    signal = [rng.uniform(-0.08, 0.08) for _ in range(SIGNAL_LENGTH)]

    for pulse_index, pulse_sample in enumerate(PULSE):
        signal_index = true_shift + pulse_index
        if signal_index < SIGNAL_LENGTH:
            signal[signal_index] += pulse_sample

    return signal


@app.get(
    "/api/config",
    response_model=EchoConfig,
    summary="Отримати конфігурацію ехолота",
)
async def get_config(response: Response) -> EchoConfig:
    response.headers["Cache-Control"] = "public, max-age=60"
    return ECHOSOUNDER_CONFIG


@app.get(
    "/api/pulse",
    response_model=list[float],
    summary="Отримати еталонний тонально-імпульсний сигнал",
)
async def get_pulse(response: Response) -> list[float]:
    response.headers["Cache-Control"] = "public, max-age=60"
    return PULSE
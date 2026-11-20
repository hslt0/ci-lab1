import json
import math
import urllib.request

from models import EchoConfig


class EchoSounderClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def get_json(self, path: str) -> object:
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            headers={"Accept": "application/json"},
            method="GET",
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status != 200:
                raise RuntimeError(f"HTTP {response.status} для {path}")
            return json.loads(response.read().decode("utf-8"))

    def get_config(self) -> EchoConfig:
        data = self.get_json("/api/config")
        if not isinstance(data, dict):
            raise RuntimeError("Відповідь /api/config повинна бути JSON-object")

        try:
            config = EchoConfig(
                total_steps=int(data["total_steps"]),
                sample_rate=float(data["sample_rate"]),
                sound_speed=float(data["sound_speed"]),
                carrier_freq=float(data["carrier_freq"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError("Некоректна конфігурація сервера ехолота") from exc

        if (
            config.total_steps <= 0
            or config.sample_rate <= 0
            or config.sound_speed <= 0
            or config.carrier_freq <= 0
        ):
            raise RuntimeError("Параметри конфігурації повинні бути додатними")
        return config

    def get_pulse(self) -> list[float]:
        return validate_samples(self.get_json("/api/pulse"), "/api/pulse")

    def get_signal(self, step: int) -> list[float]:
        path = f"/api/signal/{step}"
        return validate_samples(self.get_json(path), path)


def validate_samples(data: object, source: str) -> list[float]:
    if not isinstance(data, list) or not data:
        raise RuntimeError(f"{source} повинен повернути непорожній JSON-масив")

    samples: list[float] = []
    for value in data:
        if isinstance(value, bool):
            raise RuntimeError(f"{source} містить булеве значення замість числа")
        try:
            sample = float(value)
        except (TypeError, ValueError) as exc:
            raise RuntimeError(f"{source} містить некоректний відлік") from exc
        if not math.isfinite(sample):
            raise RuntimeError(f"{source} містить нечисловий або нескінченний відлік")
        samples.append(sample)
    return samples

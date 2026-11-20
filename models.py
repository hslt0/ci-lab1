from dataclasses import dataclass


@dataclass(frozen=True)
class EchoConfig:
    total_steps: int
    sample_rate: float
    sound_speed: float
    carrier_freq: float


@dataclass(frozen=True)
class RouteDepth:
    step: int
    shift: int
    depth_m: float
    accumulated_shift: int
    accumulated_depth_m: float

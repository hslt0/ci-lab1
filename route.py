from api_client import EchoSounderClient
from correlation import average_samples, cross_correlation, find_best_shift
from models import EchoConfig, RouteDepth


def shift_to_depth_m(
    shift: int,
    sample_rate: float,
    sound_speed: float,
) -> float:
    both_way_time_s = shift / sample_rate
    return sound_speed * both_way_time_s / 2


def maximum_depth_m(
    signal_length: int,
    pulse_length: int,
    sample_rate: float,
    sound_speed: float,
) -> float:
    maximum_shift = max(0, signal_length - pulse_length)
    return shift_to_depth_m(maximum_shift, sample_rate, sound_speed)


def process_route(
    client: EchoSounderClient,
    config: EchoConfig,
    pulse: list[float],
    repeat_count: int,
    max_steps: int | None = None,
) -> tuple[list[RouteDepth], float]:
    route_depths: list[RouteDepth] = []
    signal_length: int | None = None
    step_count = config.total_steps
    if max_steps is not None:
        step_count = min(step_count, max_steps)

    for step in range(step_count):
        first_signal = client.get_signal(step)
        signal_length = len(first_signal)

        first_shift = find_best_shift(cross_correlation(first_signal, pulse))

        accumulated_signals = [first_signal]
        for _ in range(repeat_count - 1):
            accumulated_signals.append(client.get_signal(step))
        averaged_signal = average_samples(accumulated_signals)
        accumulated_shift = find_best_shift(
            cross_correlation(averaged_signal, pulse)
        )

        route_depth = RouteDepth(
            step=step,
            shift=first_shift,
            depth_m=shift_to_depth_m(
                first_shift,
                config.sample_rate,
                config.sound_speed,
            ),
            accumulated_shift=accumulated_shift,
            accumulated_depth_m=shift_to_depth_m(
                accumulated_shift,
                config.sample_rate,
                config.sound_speed,
            ),
        )
        route_depths.append(route_depth)

        print(
            f"{step:5d}: depth={route_depth.depth_m:9.3f} m "
            f"(k={first_shift:4d}); "
            f"averaged={route_depth.accumulated_depth_m:9.3f} m "
            f"(k={accumulated_shift:4d})"
        )

    if signal_length is None:
        return route_depths, 0.0

    max_depth = maximum_depth_m(
        signal_length,
        len(pulse),
        config.sample_rate,
        config.sound_speed,
    )
    return route_depths, max_depth

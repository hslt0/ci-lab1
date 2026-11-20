def cross_correlation(signal: list[float], pulse: list[float]) -> list[float]:
    """Самостійна дискретна взаємна кореляція: O(N*M) без NumPy."""
    if len(pulse) > len(signal):
        raise ValueError("Еталонний імпульс довший за прийнятий сигнал")

    correlations: list[float] = []
    for shift in range(len(signal) - len(pulse) + 1):
        value = 0.0
        for pulse_index, pulse_sample in enumerate(pulse):
            value += signal[shift + pulse_index] * pulse_sample
        correlations.append(value)
    return correlations


def find_best_shift(correlation: list[float]) -> int:
    if not correlation:
        raise ValueError("Не можна знайти максимум порожньої кореляції")

    best_shift = 0
    best_value = correlation[0]
    for shift in range(1, len(correlation)):
        if correlation[shift] > best_value:
            best_value = correlation[shift]
            best_shift = shift
    return best_shift


def average_samples(signals: list[list[float]]) -> list[float]:
    if not signals:
        raise ValueError("Немає сигналів для усереднення")

    length = len(signals[0])
    if any(len(signal) != length for signal in signals):
        raise ValueError("Сигнали для усереднення мають різну довжину")

    averaged = [0.0] * length
    for signal in signals:
        for index, sample in enumerate(signal):
            averaged[index] += sample
    return [sample / len(signals) for sample in averaged]

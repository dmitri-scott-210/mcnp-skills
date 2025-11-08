"""
Time-Weighted Averaging Utilities
For collapsing operational history into representative configurations
"""

import numpy as np


def time_weighted_average(values, time_intervals):
    """
    Calculate time-weighted average.

    Args:
        values: Array of parameter values at each timestep
        time_intervals: Array of time duration for each timestep (same length as values)

    Returns:
        Time-weighted average value

    Example:
        >>> power = np.array([23.5, 24.1, 23.8])
        >>> time = np.array([24.0, 18.5, 30.0])  # hours
        >>> time_weighted_average(power, time)
        23.79... MW
    """
    if len(values) != len(time_intervals):
        raise ValueError("Values and time_intervals must have same length")

    if np.sum(time_intervals) == 0:
        raise ValueError("Total time interval is zero")

    return np.sum(values * time_intervals) / np.sum(time_intervals)


def snap_to_discrete(value, discrete_values):
    """
    Snap continuous value to nearest discrete option.

    Useful for control drum angles, rod positions with predefined detents.

    Args:
        value: Continuous value (e.g., 82.3 degrees)
        discrete_values: List of allowed values (e.g., [0, 25, 40, 50, ...])

    Returns:
        Nearest discrete value

    Example:
        >>> angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100]
        >>> snap_to_discrete(82.3, angles)
        80
    """
    discrete_array = np.array(discrete_values)
    differences = np.abs(discrete_array - value)
    idx = np.argmin(differences)
    return discrete_values[idx]


def round_binary(value):
    """
    Round to binary state (0 or 1).

    Useful for control rod insertion states after time-averaging.

    Args:
        value: Continuous value between 0 and 1 (e.g., 0.73 = mostly inserted)

    Returns:
        0 or 1

    Example:
        >>> round_binary(0.23)  # Mostly withdrawn
        0
        >>> round_binary(0.78)  # Mostly inserted
        1
    """
    return int(np.rint(value))


def cycle_average(data, cycle_column, time_column, value_column):
    """
    Calculate time-weighted average for each cycle in a DataFrame.

    Args:
        data: Pandas DataFrame
        cycle_column: Name of cycle identifier column
        time_column: Name of time interval column
        value_column: Name of value column to average

    Returns:
        Dict mapping cycle -> average value

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'Cycle': ['138B', '138B', '139A', '139A'],
        ...     'Time_hrs': [24, 20, 18, 22],
        ...     'Power_MW': [23.5, 24.1, 24.3, 24.0]
        ... })
        >>> cycle_average(df, 'Cycle', 'Time_hrs', 'Power_MW')
        {'138B': 23.77..., '139A': 24.14...}
    """
    averages = {}

    for cycle in data[cycle_column].unique():
        cycle_data = data[data[cycle_column] == cycle]
        values = cycle_data[value_column].values
        times = cycle_data[time_column].values

        averages[cycle] = time_weighted_average(values, times)

    return averages


def validate_time_data(time_intervals):
    """
    Validate time interval data.

    Checks:
    - All positive
    - No NaN/Inf
    - Total > 0

    Args:
        time_intervals: Array of time durations

    Raises:
        ValueError: If validation fails
    """
    if np.any(time_intervals < 0):
        raise ValueError("Time intervals must be positive")

    if np.any(np.isnan(time_intervals)) or np.any(np.isinf(time_intervals)):
        raise ValueError("Time intervals contain NaN or Inf")

    if np.sum(time_intervals) == 0:
        raise ValueError("Total time is zero")


# Example usage and tests
if __name__ == "__main__":
    print("=" * 60)
    print("Time-Weighted Averaging Utilities - Examples")
    print("=" * 60)

    # Example 1: Simple time-weighted average
    print("\nExample 1: Time-Weighted Average")
    power = np.array([23.5, 24.1, 23.8, 24.0])
    time = np.array([24.0, 18.5, 30.0, 20.0])  # hours
    ave = time_weighted_average(power, time)
    print(f"  Power values: {power}")
    print(f"  Time intervals: {time} hrs")
    print(f"  Time-weighted average: {ave:.2f} MW")
    print(f"  (Compare to simple mean: {power.mean():.2f} MW)")

    # Example 2: Snap to discrete values
    print("\nExample 2: Snap to Discrete Values")
    angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
    continuous_angle = 82.3
    closest = snap_to_discrete(continuous_angle, angles)
    print(f"  Continuous angle: {continuous_angle}°")
    print(f"  Discrete options: {angles}")
    print(f"  Closest discrete: {closest}°")

    # Example 3: Round binary
    print("\nExample 3: Round Binary State")
    insertion_states = np.array([1, 1, 0, 1, 1, 0])  # Binary: in/out
    time_intervals = np.array([10, 15, 5, 20, 18, 12])  # hours
    ave_insertion = time_weighted_average(insertion_states, time_intervals)
    representative_state = round_binary(ave_insertion)
    print(f"  States over time: {insertion_states}")
    print(f"  Time intervals: {time_intervals} hrs")
    print(f"  Time-weighted average: {ave_insertion:.2f}")
    print(f"  Representative state: {representative_state} ({'inserted' if representative_state else 'withdrawn'})")

    # Example 4: Cycle averaging
    print("\nExample 4: Cycle Averaging from DataFrame")
    import pandas as pd
    df = pd.DataFrame({
        'Cycle': ['138B', '138B', '138B', '139A', '139A', '139A'],
        'Timestep': [1, 2, 3, 1, 2, 3],
        'Time_hrs': [24, 20, 18, 22, 25, 19],
        'Power_MW': [23.5, 24.1, 23.8, 24.3, 24.0, 24.2]
    })
    print("  Input DataFrame:")
    print(df.to_string(index=False))

    averages = cycle_average(df, 'Cycle', 'Time_hrs', 'Power_MW')
    print("\n  Cycle-averaged power:")
    for cycle, ave_power in averages.items():
        print(f"    {cycle}: {ave_power:.2f} MW")

    print("\n" + "=" * 60)

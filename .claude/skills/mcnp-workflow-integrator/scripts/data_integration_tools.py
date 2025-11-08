"""
Data Integration Tools for MCNP Workflows

Tools for processing external data (CSV, Excel) into MCNP-compatible formats.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any

def time_weighted_average(values: np.ndarray, times: np.ndarray) -> float:
    """
    Calculate time-weighted average of parameter values.

    Used to convert continuous operational data to discrete MCNP configuration.

    Args:
        values: Array of parameter values
        times: Array of timestamps (must be same length as values)

    Returns:
        Time-weighted average

    Example:
        Power varies from 100 MW to 150 MW over 10 days.
        Average for MCNP = time_weighted_average([100, 150], [0, 10])
    """
    if len(values) != len(times):
        raise ValueError("Values and times must have same length")

    if len(values) == 0:
        raise ValueError("Cannot average empty array")

    if len(values) == 1:
        return float(values[0])

    # Calculate time intervals
    intervals = np.diff(times, prepend=0)

    # Time-weighted sum
    weighted_sum = (values * intervals).sum()
    total_time = intervals.sum()

    if total_time == 0:
        raise ValueError("Total time is zero")

    return weighted_sum / total_time


def find_closest_value(allowed_values: List[float], target: float) -> float:
    """
    Find closest allowed value to target.

    Used when MCNP model has discrete options (e.g., control drum angles).

    Args:
        allowed_values: List of permitted values
        target: Desired value (may not be in list)

    Returns:
        Closest value from allowed_values

    Example:
        Allowed angles: [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
        Target: 73.5 → returns 75
    """
    allowed = np.array(allowed_values)
    differences = np.abs(allowed - target)
    closest_index = np.argmin(differences)
    return float(allowed[closest_index])


def process_power_history(csv_file: str, cycle_name: str) -> Dict[str, float]:
    """
    Process power history CSV into MCNP-compatible parameters.

    Args:
        csv_file: Path to power.csv
        cycle_name: Cycle identifier (e.g., '138B')

    Returns:
        Dictionary with averaged parameters

    CSV Format:
        Cycle, Time_h, Power_MW, Lobe_NE, Lobe_NW, Lobe_SE, Lobe_SW
    """
    df = pd.read_csv(csv_file)

    # Filter to this cycle
    cycle_data = df[df['Cycle'] == cycle_name]

    if len(cycle_data) == 0:
        raise ValueError(f"No data found for cycle {cycle_name}")

    # Time-weighted averaging
    result = {
        'cycle': cycle_name,
        'duration_days': (cycle_data['Time_h'].max() - cycle_data['Time_h'].min()) / 24,
        'avg_power_MW': time_weighted_average(
            cycle_data['Power_MW'].values,
            cycle_data['Time_h'].values
        )
    }

    # Lobe-specific if available
    for lobe in ['NE', 'NW', 'SE', 'SW']:
        col = f'Lobe_{lobe}'
        if col in cycle_data.columns:
            result[f'avg_power_{lobe}_MW'] = time_weighted_average(
                cycle_data[col].values,
                cycle_data['Time_h'].values
            )

    return result


def process_control_positions(csv_file: str, cycle_name: str,
                              allowed_angles: List[float]) -> Dict[str, float]:
    """
    Process control drum position history.

    Args:
        csv_file: Path to oscc.csv (outer safety control cylinder)
        cycle_name: Cycle identifier
        allowed_angles: Discrete angles modeled in MCNP

    Returns:
        Dictionary with selected angle

    CSV Format:
        Cycle, Time_h, Angle_deg
    """
    df = pd.read_csv(csv_file)
    cycle_data = df[df['Cycle'] == cycle_name]

    if len(cycle_data) == 0:
        raise ValueError(f"No data found for cycle {cycle_name}")

    # Time-weighted average of continuous angle
    avg_angle = time_weighted_average(
        cycle_data['Angle_deg'].values,
        cycle_data['Time_h'].values
    )

    # Find closest allowed angle
    selected_angle = find_closest_value(allowed_angles, avg_angle)

    return {
        'cycle': cycle_name,
        'avg_angle_continuous': avg_angle,
        'selected_angle_discrete': selected_angle,
        'difference': abs(avg_angle - selected_angle)
    }


def process_binary_state(csv_file: str, cycle_name: str,
                        state_materials: Dict[int, Tuple[int, float]]) -> Dict[str, Any]:
    """
    Process binary state data (inserted/withdrawn).

    Args:
        csv_file: Path to state data CSV
        cycle_name: Cycle identifier
        state_materials: Mapping of state → (material_number, density)
                        Example: {0: (10, 1.00276e-1), 1: (71, 4.55926e-2)}
                        0 = withdrawn (water), 1 = inserted (hafnium)

    Returns:
        Dictionary with selected state and material

    CSV Format:
        Cycle, Time_h, State (0 or 1)
    """
    df = pd.read_csv(csv_file)
    cycle_data = df[df['Cycle'] == cycle_name]

    if len(cycle_data) == 0:
        raise ValueError(f"No data found for cycle {cycle_name}")

    # Time-weighted average of state
    avg_state = time_weighted_average(
        cycle_data['State'].values,
        cycle_data['Time_h'].values
    )

    # Round to nearest integer (0 or 1)
    selected_state = int(np.rint(avg_state))

    # Get material for this state
    material_num, density = state_materials[selected_state]

    return {
        'cycle': cycle_name,
        'avg_state_continuous': avg_state,
        'selected_state': selected_state,
        'material_number': material_num,
        'density': density,
        'state_description': 'inserted' if selected_state == 1 else 'withdrawn'
    }


def validate_csv_data(csv_file: str, required_columns: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate CSV file structure.

    Args:
        csv_file: Path to CSV
        required_columns: List of required column names

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        return False, [f"File not found: {csv_file}"]
    except pd.errors.EmptyDataError:
        return False, [f"File is empty: {csv_file}"]
    except Exception as e:
        return False, [f"Error reading file: {e}"]

    # Check columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        issues.append(f"Missing columns: {missing_cols}")

    # Check for empty data
    if len(df) == 0:
        issues.append("No data rows in file")

    # Check for NaN values in required columns
    for col in required_columns:
        if col in df.columns:
            nan_count = df[col].isna().sum()
            if nan_count > 0:
                issues.append(f"Column '{col}' has {nan_count} NaN values")

    return len(issues) == 0, issues


# Example usage
if __name__ == "__main__":
    # Example: Process AGR-1 cycle 138B data

    print("Processing power history...")
    power_params = process_power_history('data/power.csv', '138B')
    print(f"  Average power: {power_params['avg_power_MW']:.2f} MW")
    print(f"  Duration: {power_params['duration_days']:.1f} days")

    print("\nProcessing control positions...")
    allowed_angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
    control_params = process_control_positions('data/oscc.csv', '138B', allowed_angles)
    print(f"  Continuous average: {control_params['avg_angle_continuous']:.2f}°")
    print(f"  Selected discrete: {control_params['selected_angle_discrete']:.0f}°")
    print(f"  Difference: {control_params['difference']:.2f}°")

    print("\nProcessing neck shim state...")
    state_materials = {
        0: (10, 1.00276e-1),  # Withdrawn: water
        1: (71, 4.55926e-2)   # Inserted: hafnium
    }
    shim_params = process_binary_state('data/neck_shim.csv', '138B', state_materials)
    print(f"  State: {shim_params['state_description']}")
    print(f"  Material: m{shim_params['material_number']}, density={shim_params['density']:.5e}")

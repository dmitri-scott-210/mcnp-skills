# Time-Weighted Averaging Algorithms
## Collapsing Operational History into Representative Configurations

This reference covers time-weighted averaging methods for MCNP template generation.

## The Core Algorithm

### Basic Time-Weighted Average

**Formula**:
```
Average = Σ(value_i × duration_i) / Σ(duration_i)
```

**Python implementation**:
```python
import numpy as np

def time_weighted_average(values, time_intervals):
    """
    Calculate time-weighted average.
    
    Args:
        values: Array of parameter values at each timestep
        time_intervals: Array of time duration for each timestep
        
    Returns:
        Time-weighted average value
    """
    return np.sum(values * time_intervals) / np.sum(time_intervals)
```

**Example**:
```python
# Power varies over 3 timesteps
power = np.array([23.5, 24.1, 23.8])  # MW
time = np.array([24.0, 18.5, 30.0])   # hours

ave_power = time_weighted_average(power, time)
# Result: 23.79 MW (vs simple mean of 23.8 MW)
```

## Parameter-Specific Methods

### 1. Continuous Parameters (Power, Temperature, Angles)

**Use**: Direct time-weighted average

```python
# Control drum angle
angles = np.array([80, 82, 85, 83, 81])  # degrees
time_intervals = np.array([24, 20, 18, 22, 16])  # hours

ave_angle = time_weighted_average(angles, time_intervals)
# Result: 82.2 degrees
```

**Snap to discrete values** (if only certain positions allowed):
```python
def snap_to_discrete(value, discrete_values):
    """Find nearest allowed value."""
    discrete_array = np.array(discrete_values)
    idx = np.argmin(np.abs(discrete_array - value))
    return discrete_values[idx]

# Predefined drum positions
allowed_angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
closest_angle = snap_to_discrete(ave_angle, allowed_angles)
# Result: 85 degrees (closest to 82.2)
```

### 2. Binary Parameters (Inserted/Withdrawn, On/Off)

**Use**: Time-weighted average, then round

```python
def round_binary(value):
    """Round to 0 or 1."""
    return int(np.rint(value))

# Shim rod states (0=withdrawn, 1=inserted)
states = np.array([1, 1, 0, 1, 1, 0])
time_intervals = np.array([10, 15, 5, 20, 18, 12])  # hours

ave_state = time_weighted_average(states, time_intervals)
# Result: 0.725 (rod inserted 72.5% of time)

representative_state = round_binary(ave_state)
# Result: 1 (inserted)
```

**Interpretation**:
- ave_state > 0.5 → rod inserted for majority of cycle
- ave_state ≤ 0.5 → rod withdrawn for majority of cycle

### 3. Categorical Parameters (Material Types, Configurations)

**Use**: Mode (most common) or custom logic

```python
def categorical_mode(values, time_intervals):
    """Find most-used category weighted by time."""
    categories = np.unique(values)
    time_by_category = {}
    
    for cat in categories:
        mask = (values == cat)
        time_by_category[cat] = np.sum(time_intervals[mask])
    
    return max(time_by_category, key=time_by_category.get)

# Material types
materials = np.array(['water', 'water', 'hafnium', 'water', 'hafnium'])
time_intervals = np.array([10, 15, 5, 20, 30])  # hours

representative_material = categorical_mode(materials, time_intervals)
# Result: 'water' (used 45/80 hrs = 56%)
```

## Multi-Parameter Averaging

### Group by Cycle

**Pandas-based workflow** for large datasets:

```python
import pandas as pd

def cycle_averages(data, cycle_col, time_col, value_cols):
    """
    Calculate time-weighted averages for multiple parameters by cycle.
    
    Args:
        data: DataFrame with operational data
        cycle_col: Name of cycle identifier column
        time_col: Name of time interval column
        value_cols: List of parameter columns to average
        
    Returns:
        Dictionary {cycle: {param: average}}
    """
    results = {}
    
    for cycle in data[cycle_col].unique():
        cycle_data = data[data[cycle_col] == cycle]
        time_intervals = cycle_data[time_col].values
        
        cycle_results = {}
        for col in value_cols:
            values = cycle_data[col].values
            cycle_results[col] = time_weighted_average(values, time_intervals)
        
        results[cycle] = cycle_results
    
    return results
```

**Example**:
```python
# Multi-lobe power data
data = pd.DataFrame({
    'Cycle': ['138B', '138B', '138B', '139A', '139A'],
    'Time_hrs': [24, 20, 18, 22, 25],
    'NE_Power': [7.8, 8.1, 7.9, 8.0, 8.2],
    'SE_Power': [7.9, 8.2, 8.0, 8.1, 8.3],
    'C_Power': [7.8, 8.0, 7.8, 7.9, 8.1]
})

averages = cycle_averages(data, 'Cycle', 'Time_hrs', 
                         ['NE_Power', 'SE_Power', 'C_Power'])

# Result:
# {
#   '138B': {'NE_Power': 7.93, 'SE_Power': 8.03, 'C_Power': 7.87},
#   '139A': {'NE_Power': 8.11, 'SE_Power': 8.21, 'C_Power': 8.00}
# }
```

## Edge Cases and Validation

### Zero Time Intervals

```python
def time_weighted_average_safe(values, time_intervals):
    """Safe version with validation."""
    if len(values) != len(time_intervals):
        raise ValueError("Values and time_intervals must have same length")
    
    total_time = np.sum(time_intervals)
    if total_time == 0:
        raise ValueError("Total time interval is zero")
    
    if np.any(time_intervals < 0):
        raise ValueError("Negative time intervals not allowed")
    
    return np.sum(values * time_intervals) / total_time
```

### Missing Data

```python
# Handle NaN values
def time_weighted_average_with_nan(values, time_intervals):
    """Average excluding NaN values."""
    mask = ~np.isnan(values)
    return time_weighted_average(values[mask], time_intervals[mask])
```

### Outlier Detection

```python
def detect_outliers_iqr(values, time_intervals):
    """Detect outliers using IQR method."""
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers = (values < lower_bound) | (values > upper_bound)
    
    if np.any(outliers):
        print(f"Warning: {np.sum(outliers)} outliers detected")
        print(f"Outlier values: {values[outliers]}")
    
    # Average excluding outliers
    return time_weighted_average(values[~outliers], time_intervals[~outliers])
```

## Visualization for QA

```python
import matplotlib.pyplot as plt

def plot_averaging_qa(values, time_intervals, average, cycle):
    """Visualize time-weighted averaging."""
    cumulative_time = np.cumsum(time_intervals)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Step plot of values over time
    times = np.insert(cumulative_time, 0, 0)
    values_extended = np.repeat(values, 2)
    times_extended = np.repeat(times[:-1], 2)
    times_extended = np.append(times_extended, times[-1])
    
    ax.plot(times_extended, values_extended, 'b-', linewidth=2, label='Actual values')
    
    # Time-weighted average line
    ax.axhline(average, color='r', linestyle='--', linewidth=2, 
               label=f'Time-weighted average: {average:.2f}')
    
    # Simple mean for comparison
    simple_mean = np.mean(values)
    ax.axhline(simple_mean, color='orange', linestyle=':', linewidth=2,
               label=f'Simple mean: {simple_mean:.2f}')
    
    ax.set_xlabel('Cumulative Time (hrs)')
    ax.set_ylabel('Parameter Value')
    ax.set_title(f'Time-Weighted Averaging QA - Cycle {cycle}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.savefig(f'averaging_qa_{cycle}.png', dpi=150, bbox_inches='tight')
```

## Complete AGR-1 Example

```python
# Process neck shim data (binary states)
def process_neck_shims(data, cycles):
    """Process neck shim insertion states."""
    shim_results = {}
    
    for cycle in cycles:
        cycle_data = data[data['Cycle'] == cycle]
        time_intervals = cycle_data['Time_Interval_hrs'].values
        
        # Process each shim rod
        cycle_shims = {}
        for rod in ['NE_1', 'NE_2', 'NE_3', 'SE_1', 'SE_2', 'SE_3']:
            states = cycle_data[rod].values  # 0 or 1
            ave_state = time_weighted_average(states, time_intervals)
            representative_state = round_binary(ave_state)
            cycle_shims[rod] = representative_state
        
        shim_results[cycle] = cycle_shims
    
    return shim_results
```

## Performance Optimization

For large datasets (>10000 timesteps):

```python
# Use NumPy broadcasting
def batch_time_weighted_average(data_matrix, time_intervals):
    """
    Vectorized averaging for multiple parameters.
    
    Args:
        data_matrix: 2D array (timesteps × parameters)
        time_intervals: 1D array (timesteps)
        
    Returns:
        1D array of averages (one per parameter)
    """
    return np.sum(data_matrix * time_intervals[:, np.newaxis], axis=0) / np.sum(time_intervals)
```

## Summary

**Key Principles**:
1. Always weight by time duration (not simple mean)
2. Validate time intervals (positive, sum > 0)
3. Handle parameter types appropriately (continuous vs binary vs categorical)
4. Visualize results for QA
5. Document averaging methodology in output files

**See Also**:
- `scripts/time_averaging.py` - Complete utility functions
- `example_inputs/agr1_burnup_workflow.py` - Real-world application

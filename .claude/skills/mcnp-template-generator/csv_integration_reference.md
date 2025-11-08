# CSV Integration Reference
## Designing Data Files for Template Rendering

This reference covers best practices for CSV data file design and integration with Jinja2 templates.

## CSV Schema Design Principles

### 1. Include Identifier Columns

Always include columns that identify the scenario/cycle:

```csv
Cycle, Timestep, Time_Interval_hrs, Parameter1, Parameter2
138B, 1, 24.0, 80.5, 23.4
138B, 2, 20.0, 82.3, 24.1
139A, 1, 22.0, 75.0, 22.8
```

**Required columns**:
- Scenario/Cycle identifier (text or numeric)
- Timestep number (for ordering)
- Time interval (for weighted averaging)

### 2. Use Clear Column Names with Units

**Good**:
```csv
Power_MW, Temperature_K, ControlAngle_deg, Density_g_cm3
```

**Bad**:
```csv
P, T, A, D
```

### 3. Consistent Data Types

Ensure Pandas can parse correctly:

```python
# Specify dtypes when reading
data = pd.read_csv('params.csv', dtype={
    'Cycle': str,
    'Timestep': int,
    'Time_Interval_hrs': float,
    'Power_MW': float
})
```

### 4. Handle Missing Data

Use explicit markers:
```csv
Cycle, Power_MW, Temperature_K
138B, 23.5, N/A
139A, 24.1, 600.0
```

Or in Python:
```python
data = pd.read_csv('params.csv', na_values=['N/A', 'NULL'])
data.fillna(method='ffill', inplace=True)  # Forward fill
```

## Common CSV Patterns

### Pattern 1: Time-Series Data

**Use case**: Operational parameters varying over time

```csv
Cycle, Timestep, Time_Interval_hrs, NE_Power_MW, SE_Power_MW, C_Power_MW
138B, 1, 24.0, 7.8, 7.9, 7.8
138B, 2, 20.0, 8.1, 8.2, 8.0
138B, 3, 18.5, 7.9, 8.0, 7.8
```

**Processing**:
```python
for cycle in cycles:
    cycle_data = data[data['Cycle'] == cycle]
    ave_power = (cycle_data['NE_Power_MW'] * cycle_data['Time_Interval_hrs']).sum() / \
                cycle_data['Time_Interval_hrs'].sum()
```

### Pattern 2: Discrete States

**Use case**: Binary or categorical parameters

```csv
Cycle, Rod1_State, Rod2_State, Rod3_State
138B, inserted, withdrawn, inserted
139A, withdrawn, withdrawn, inserted
```

**Processing**:
```python
# Map to numeric
state_map = {'withdrawn': 0, 'inserted': 1}
data['Rod1_Numeric'] = data['Rod1_State'].map(state_map)
```

### Pattern 3: Multi-Parameter Sensitivity

**Use case**: Parameter sweep studies

```csv
Case, Enrichment_pct, Density_g_cm3, Temperature_K
1, 3.0, 10.5, 900
2, 3.5, 10.5, 900
3, 4.0, 10.5, 900
4, 3.0, 10.0, 900
```

**Processing**:
```python
for _, row in data.iterrows():
    params = {
        'enrichment': row['Enrichment_pct'],
        'density': row['Density_g_cm3'],
        'temp': row['Temperature_K']
    }
    # Generate material card
    # Render template
```

## Validation Best Practices

### Check Completeness

```python
def validate_csv_completeness(data, expected_cycles):
    """Ensure all expected cycles present."""
    actual_cycles = set(data['Cycle'].unique())
    missing = set(expected_cycles) - actual_cycles
    extra = actual_cycles - set(expected_cycles)
    
    if missing:
        raise ValueError(f"Missing cycles: {missing}")
    if extra:
        print(f"Warning: Extra cycles found: {extra}")
```

### Check Data Ranges

```python
def validate_ranges(data):
    """Check physical reasonableness."""
    if (data['Power_MW'] < 0).any():
        raise ValueError("Negative power values found")
    
    if (data['Temperature_K'] < 0).any():
        raise ValueError("Negative temperature values found")
    
    if (data['ControlAngle_deg'] < 0).any() or (data['ControlAngle_deg'] > 180).any():
        raise ValueError("Control angle out of range [0, 180]")
```

### Visualize Data

```python
import matplotlib.pyplot as plt

def plot_qa_diagnostics(data):
    """Create QA plots for data validation."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Power vs time
    for cycle in data['Cycle'].unique():
        cycle_data = data[data['Cycle'] == cycle]
        axes[0, 0].plot(cycle_data['Timestep'], cycle_data['Power_MW'], 
                       marker='o', label=cycle)
    axes[0, 0].set_xlabel('Timestep')
    axes[0, 0].set_ylabel('Power (MW)')
    axes[0, 0].legend()
    
    # Add more plots...
    plt.tight_layout()
    plt.savefig('data_qa.png', dpi=150)
```

## Integration with Template Rendering

### Complete Workflow

```python
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Read CSV
data = pd.read_csv('operational_params.csv')

# Validate
validate_csv_completeness(data, expected_cycles)
validate_ranges(data)

# Create QA plots
plot_qa_diagnostics(data)

# Process by cycle
env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('base.template')

for cycle in expected_cycles:
    cycle_data = data[data['Cycle'] == cycle]
    
    # Calculate averages
    ave_power = time_weighted_average(
        cycle_data['Power_MW'].values,
        cycle_data['Time_Interval_hrs'].values
    )
    
    # Render template
    output = template.render(power=ave_power, cycle=cycle)
    
    # Write output
    with open(f'mcnp/input_{cycle}.i', 'w') as f:
        f.write(output)
```

## Common Issues and Solutions

### Issue: CSV encoding problems

**Solution**: Specify encoding explicitly
```python
data = pd.read_csv('params.csv', encoding='utf-8')
```

### Issue: Leading/trailing whitespace in columns

**Solution**: Strip whitespace
```python
data.columns = data.columns.str.strip()
data['Cycle'] = data['Cycle'].str.strip()
```

### Issue: Inconsistent cycle naming

**Solution**: Normalize identifiers
```python
data['Cycle'] = data['Cycle'].str.upper().str.strip()
```

## Example CSV Files

See `example_inputs/` for:
- `power.csv` - Multi-lobe power vs time
- `oscc.csv` - Control drum angles vs time
- `neck_shim.csv` - Binary insertion states vs time
- `enrichment_study.csv` - Enrichment parameter sweep
- `control_rod_positions.csv` - Discrete rod positions

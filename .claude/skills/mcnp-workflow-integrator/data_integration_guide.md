# Data Integration Guide

How to integrate external data sources into MCNP workflows.

## Overview

Real-world reactor analysis requires integrating data from multiple sources:
- Experimental measurements
- Operational records
- Material property databases
- Benchmark specifications

This guide shows how to process external data into MCNP-compatible formats.

---

## CSV Data Processing

### Power Histories

**Problem**: Reactor power varies continuously during operation. MCNP models require discrete power levels.

**Solution**: Time-weighted averaging

**CSV Format** (`power.csv`):
```csv
Cycle,Time_h,Power_MW,Lobe_NE,Lobe_NW,Lobe_SE,Lobe_SW
138B,0.0,110.0,27.5,27.5,27.5,27.5
138B,24.0,115.0,28.75,28.75,28.75,28.75
138B,48.0,112.0,28.0,28.0,28.0,28.0
138B,72.0,108.0,27.0,27.0,27.0,27.0
139A,0.0,105.0,26.25,26.25,26.25,26.25
139A,24.0,110.0,27.5,27.5,27.5,27.5
```

**Processing Script**:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def time_weighted_average(values, times):
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
    # First interval assumed to start at 0
    intervals = np.diff(times, prepend=0)

    # Time-weighted sum
    weighted_sum = (values * intervals).sum()
    total_time = intervals.sum()

    if total_time == 0:
        raise ValueError("Total time is zero")

    return weighted_sum / total_time


def process_power_history(csv_file, cycle_name):
    """
    Process power history CSV into MCNP-compatible parameters.

    Args:
        csv_file: Path to power.csv
        cycle_name: Cycle identifier (e.g., '138B')

    Returns:
        Dictionary with averaged parameters
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


def visualize_power_history(csv_file, cycle_name, output_file):
    """
    Create diagnostic plot of power history.

    Shows time-dependent power and time-weighted average.
    """
    df = pd.read_csv(csv_file)
    cycle_data = df[df['Cycle'] == cycle_name]

    params = process_power_history(csv_file, cycle_name)

    plt.figure(figsize=(10, 6))

    # Plot time-dependent power
    plt.step(cycle_data['Time_h'], cycle_data['Power_MW'],
             where='post', label='Actual Power', linewidth=2)

    # Plot time-weighted average
    plt.axhline(params['avg_power_MW'], color='r', linestyle='--',
                linewidth=2, label=f"Time-Weighted Average ({params['avg_power_MW']:.1f} MW)")

    plt.xlabel('Time (hours)', fontsize=12)
    plt.ylabel('Power (MW)', fontsize=12)
    plt.title(f'Power History - Cycle {cycle_name}', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Saved: {output_file}")


# Example usage
if __name__ == "__main__":
    params = process_power_history('data/power.csv', '138B')
    print(f"Cycle {params['cycle']}:")
    print(f"  Duration: {params['duration_days']:.1f} days")
    print(f"  Average Power: {params['avg_power_MW']:.2f} MW")

    if 'avg_power_NE_MW' in params:
        print(f"  NE Lobe: {params['avg_power_NE_MW']:.2f} MW")

    # Create diagnostic plot
    visualize_power_history('data/power.csv', '138B', 'power_cycle_138B.png')
```

---

### Control Position Data

**Problem**: Control rods/drums rotate continuously. MCNP model has discrete angle options.

**Solution**: Time-weighted average → find closest discrete angle

**CSV Format** (`oscc.csv`):
```csv
Cycle,Time_h,Angle_deg
138B,0.0,65.0
138B,24.0,67.5
138B,48.0,70.0
138B,72.0,72.5
139A,0.0,75.0
139A,24.0,73.0
```

**Processing Script**:

```python
def find_closest_value(allowed_values, target):
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


def process_control_positions(csv_file, cycle_name, allowed_angles):
    """
    Process control drum position history.

    Args:
        csv_file: Path to oscc.csv (outer safety control cylinder)
        cycle_name: Cycle identifier
        allowed_angles: Discrete angles modeled in MCNP

    Returns:
        Dictionary with selected angle and metadata
    """
    df = pd.read_csv(csv_file)
    cycle_data = df[df['Cycle'] == cycle_name]

    if len(cycle_data) == 0:
        raise ValueError(f"No data found for cycle {cycle_name}")

    # Time-weighted average of continuous angle
    ave_angle = time_weighted_average(
        cycle_data['Angle_deg'].values,
        cycle_data['Time_h'].values
    )

    # Find closest allowed angle
    selected_angle = find_closest_value(allowed_angles, ave_angle)

    return {
        'cycle': cycle_name,
        'avg_angle_continuous': ave_angle,
        'selected_angle_discrete': selected_angle,
        'difference': abs(ave_angle - selected_angle),
        'allowed_angles': allowed_angles
    }


# Example usage
allowed_angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
control_params = process_control_positions('data/oscc.csv', '138B', allowed_angles)

print(f"Cycle {control_params['cycle']}:")
print(f"  Continuous average: {control_params['avg_angle_continuous']:.2f}°")
print(f"  Selected discrete:  {control_params['selected_angle_discrete']:.0f}°")
print(f"  Difference:         {control_params['difference']:.2f}°")
```

---

### Binary State Data (Inserted/Withdrawn)

**Problem**: Component has two states (e.g., shim rod inserted or withdrawn). State changes during cycle.

**Solution**: Time-weighted average → round to nearest state

**CSV Format** (`neck_shim.csv`):
```csv
Cycle,Time_h,State
138B,0.0,0
138B,24.0,0
138B,48.0,1
138B,72.0,1
139A,0.0,1
139A,24.0,1
```

Where: `0 = withdrawn`, `1 = inserted`

**Processing Script**:

```python
def process_binary_state(csv_file, cycle_name, state_materials):
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
    """
    df = pd.read_csv(csv_file)
    cycle_data = df[df['Cycle'] == cycle_name]

    if len(cycle_data) == 0:
        raise ValueError(f"No data found for cycle {cycle_name}")

    # Time-weighted average of state
    ave_state = time_weighted_average(
        cycle_data['State'].values,
        cycle_data['Time_h'].values
    )

    # Round to nearest integer (0 or 1)
    selected_state = int(np.rint(ave_state))

    # Get material for this state
    material_num, density = state_materials[selected_state]

    return {
        'cycle': cycle_name,
        'avg_state_continuous': ave_state,
        'selected_state': selected_state,
        'material_number': material_num,
        'density': density,
        'state_description': 'inserted' if selected_state == 1 else 'withdrawn',
        'fraction_time_inserted': ave_state  # If ave_state=0.75, inserted 75% of time
    }


# Example usage
state_materials = {
    0: (10, 1.00276e-1),  # Withdrawn: water (m10, density)
    1: (71, 4.55926e-2)   # Inserted: hafnium (m71, density)
}

shim_params = process_binary_state('data/neck_shim.csv', '138B', state_materials)

print(f"Cycle {shim_params['cycle']}:")
print(f"  State: {shim_params['state_description']}")
print(f"  Inserted {shim_params['fraction_time_inserted']*100:.0f}% of time")
print(f"  Material: m{shim_params['material_number']}, density={shim_params['density']:.5e}")
```

---

### Material Properties Database

**Problem**: Need material compositions and densities for many materials.

**Solution**: Database lookup with temperature interpolation

**CSV Format** (`materials.csv`):
```csv
Material,Temperature_K,Density_g/cm3,Element,Fraction_Type,Fraction
Graphite,300,1.85,C,atom,1.0
Graphite,600,1.85,C,atom,1.0
Stainless_Steel_304,300,7.92,Fe,weight,0.695
Stainless_Steel_304,300,7.92,Cr,weight,0.190
Stainless_Steel_304,300,7.92,Ni,weight,0.095
Stainless_Steel_304,300,7.92,Mn,weight,0.020
```

**Processing Script**:

```python
def load_material_database(csv_file):
    """Load material properties from CSV."""
    df = pd.read_csv(csv_file)

    materials = {}

    for material in df['Material'].unique():
        mat_data = df[df['Material'] == material]

        # Group by temperature
        for temp in mat_data['Temperature_K'].unique():
            temp_data = mat_data[mat_data['Temperature_K'] == temp]

            key = f"{material}_{int(temp)}K"

            materials[key] = {
                'material': material,
                'temperature_K': temp,
                'density_g/cm3': temp_data['Density_g/cm3'].iloc[0],
                'composition': []
            }

            for _, row in temp_data.iterrows():
                materials[key]['composition'].append({
                    'element': row['Element'],
                    'fraction_type': row['Fraction_Type'],
                    'fraction': row['Fraction']
                })

    return materials


def get_material(database, material_name, temperature_K):
    """
    Get material properties at specified temperature.

    Interpolates if exact temperature not in database.
    """
    # Find available temperatures for this material
    available = [k for k in database.keys() if k.startswith(material_name)]

    if not available:
        raise ValueError(f"Material {material_name} not in database")

    # Extract temperatures
    temps = [int(k.split('_')[-1][:-1]) for k in available]

    # Find closest temperature
    closest_temp = min(temps, key=lambda t: abs(t - temperature_K))

    if abs(closest_temp - temperature_K) > 100:
        print(f"WARNING: Using {closest_temp}K data for {temperature_K}K request")

    return database[f"{material_name}_{closest_temp}K"]


# Example usage
materials_db = load_material_database('data/materials.csv')

# Get stainless steel at 400K (will use 300K data with warning)
ss304 = get_material(materials_db, 'Stainless_Steel_304', 400)

print(f"Material: {ss304['material']}")
print(f"Temperature: {ss304['temperature_K']} K")
print(f"Density: {ss304['density_g/cm3']} g/cm³")
print("Composition:")
for comp in ss304['composition']:
    print(f"  {comp['element']}: {comp['fraction']} ({comp['fraction_type']})")
```

---

## Excel Integration

**When to Use**: Excel files with multiple sheets, complex formatting

**Library**: `openpyxl` for .xlsx, `xlrd` for .xls

**Example**:

```python
import openpyxl

def read_benchmark_data(excel_file):
    """
    Read benchmark data from Excel workbook.

    Assumes structure:
    - Sheet 'Geometry': geometric parameters
    - Sheet 'Materials': compositions
    - Sheet 'Results': expected keff values
    """
    wb = openpyxl.load_workbook(excel_file)

    # Read geometry parameters
    geom_sheet = wb['Geometry']
    geometry = {}
    for row in geom_sheet.iter_rows(min_row=2, values_only=True):
        param_name, value, unit = row[0], row[1], row[2]
        geometry[param_name] = {'value': value, 'unit': unit}

    # Read expected results
    results_sheet = wb['Results']
    expected_keff = {}
    for row in results_sheet.iter_rows(min_row=2, values_only=True):
        case_name, keff, uncertainty = row[0], row[1], row[2]
        expected_keff[case_name] = {'keff': keff, 'uncertainty': uncertainty}

    return {
        'geometry': geometry,
        'expected_keff': expected_keff
    }


# Example usage
benchmark = read_benchmark_data('data/benchmark.xlsx')

print("Geometry Parameters:")
for param, data in benchmark['geometry'].items():
    print(f"  {param}: {data['value']} {data['unit']}")

print("\nExpected keff:")
for case, result in benchmark['expected_keff'].items():
    print(f"  {case}: {result['keff']:.5f} ± {result['uncertainty']:.5f}")
```

---

## Database Queries (SQLite)

**When to Use**: Large datasets, complex queries, relational data

**Example**: Cross-section library database

```python
import sqlite3
import pandas as pd

def create_xsdir_database(xsdir_file, db_file):
    """
    Parse XSDIR file and create searchable SQLite database.

    XSDIR format (simplified):
    ZAID  filename  atomic_weight  temperature
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cross_sections (
            zaid TEXT PRIMARY KEY,
            filename TEXT,
            atomic_weight REAL,
            temperature_K REAL,
            library TEXT,
            particle TEXT
        )
    ''')

    # Parse XSDIR and populate
    with open(xsdir_file, 'r') as f:
        for line in f:
            if line.startswith('  '):  # Data lines indented
                parts = line.split()
                zaid = parts[0]
                filename = parts[1]
                atomic_weight = float(parts[2])
                # ... parse rest

                cursor.execute('''
                    INSERT OR REPLACE INTO cross_sections
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (zaid, filename, atomic_weight, temperature, library, particle))

    conn.commit()
    conn.close()


def query_cross_sections(db_file, element=None, temperature=None, library=None):
    """
    Query cross-section database.

    Args:
        element: Element symbol (e.g., 'U', 'Pu')
        temperature: Temperature in K (finds nearest)
        library: Library name (e.g., '00c', '71c')

    Returns:
        DataFrame of matching cross sections
    """
    conn = sqlite3.connect(db_file)

    query = "SELECT * FROM cross_sections WHERE 1=1"
    params = []

    if element:
        # Convert element to Z (atomic number)
        Z = element_to_Z(element)
        query += " AND CAST(SUBSTR(zaid, 1, INSTR(zaid, '.')-1) AS INTEGER) / 1000 = ?"
        params.append(Z)

    if temperature:
        query += " AND ABS(temperature_K - ?) < 50"
        params.append(temperature)

    if library:
        query += " AND library = ?"
        params.append(library)

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    return df


# Example usage
# Create database (one-time)
create_xsdir_database('/path/to/xsdir', 'xslib.db')

# Query for uranium cross sections at 600K
u_xs = query_cross_sections('xslib.db', element='U', temperature=600)
print(u_xs)
```

---

## Validation of External Data

**Always validate data before using in MCNP!**

```python
def validate_csv_data(csv_file, required_columns, value_ranges=None):
    """
    Validate CSV file structure and data ranges.

    Args:
        csv_file: Path to CSV
        required_columns: List of required column names
        value_ranges: Dict of {column: (min, max)} for range checking

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

    # Check value ranges
    if value_ranges:
        for col, (min_val, max_val) in value_ranges.items():
            if col in df.columns:
                out_of_range = ((df[col] < min_val) | (df[col] > max_val)).sum()
                if out_of_range > 0:
                    issues.append(
                        f"Column '{col}': {out_of_range} values outside "
                        f"range [{min_val}, {max_val}]"
                    )

    return len(issues) == 0, issues


# Example usage
is_valid, issues = validate_csv_data(
    'data/power.csv',
    required_columns=['Cycle', 'Time_h', 'Power_MW'],
    value_ranges={'Power_MW': (0, 200), 'Time_h': (0, 10000)}
)

if not is_valid:
    print("Validation failed:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("Data validated successfully!")
```

---

## Complete Example: AGR-1 Data Integration

**Bringing it all together**:

```python
import pandas as pd
import numpy as np

class AGR1DataProcessor:
    """Process AGR-1 experimental data for MCNP input generation."""

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.power_df = pd.read_csv(f'{data_dir}/power.csv')
        self.oscc_df = pd.read_csv(f'{data_dir}/oscc.csv')
        self.neck_shim_df = pd.read_csv(f'{data_dir}/neck_shim.csv')

        # MCNP model constraints
        self.allowed_oscc_angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
        self.neck_shim_materials = {
            0: (10, 1.00276e-1),  # Water
            1: (71, 4.55926e-2)   # Hafnium
        }

    def process_cycle(self, cycle_name):
        """
        Process all data for one cycle.

        Returns:
            Dictionary with all parameters for MCNP input generation
        """
        print(f"\nProcessing cycle {cycle_name}...")

        # Power history
        power_data = self._process_power(cycle_name)
        print(f"  Average power: {power_data['avg_power_MW']:.2f} MW")

        # OSCC positions
        oscc_data = self._process_oscc(cycle_name)
        print(f"  OSCC angle: {oscc_data['selected_angle']:.0f}°")

        # Neck shim state
        neck_data = self._process_neck_shim(cycle_name)
        print(f"  Neck shim: {neck_data['state_description']}")

        # Combine all parameters
        return {
            'cycle': cycle_name,
            **power_data,
            **oscc_data,
            **neck_data
        }

    def _process_power(self, cycle_name):
        """Process power history for cycle."""
        cycle_data = self.power_df[self.power_df['Cycle'] == cycle_name]

        return {
            'avg_power_MW': time_weighted_average(
                cycle_data['Power_MW'].values,
                cycle_data['Time_h'].values
            ),
            'duration_days': (cycle_data['Time_h'].max() - cycle_data['Time_h'].min()) / 24
        }

    def _process_oscc(self, cycle_name):
        """Process OSCC angles for cycle."""
        cycle_data = self.oscc_df[self.oscc_df['Cycle'] == cycle_name]

        ave_angle = time_weighted_average(
            cycle_data['Angle_deg'].values,
            cycle_data['Time_h'].values
        )

        selected_angle = find_closest_value(self.allowed_oscc_angles, ave_angle)

        return {
            'selected_angle': selected_angle,
            'oscc_surfaces': self._generate_oscc_surfaces(selected_angle)
        }

    def _process_neck_shim(self, cycle_name):
        """Process neck shim state for cycle."""
        cycle_data = self.neck_shim_df[self.neck_shim_df['Cycle'] == cycle_name]

        ave_state = time_weighted_average(
            cycle_data['State'].values,
            cycle_data['Time_h'].values
        )

        selected_state = int(np.rint(ave_state))
        material_num, density = self.neck_shim_materials[selected_state]

        return {
            'neck_shim_state': selected_state,
            'neck_shim_material': material_num,
            'neck_shim_density': density,
            'state_description': 'inserted' if selected_state == 1 else 'withdrawn'
        }

    def _generate_oscc_surfaces(self, angle):
        """Generate OSCC surface definitions for given angle."""
        # Generate rotated surface cards
        # (Simplified - actual implementation more complex)
        return f"c OSCC rotated to {angle} degrees\n"


# Example usage
processor = AGR1DataProcessor('data')

cycles = ['138B', '139A', '139B', '140A', '140B',
          '141A', '142A', '142B', '143A', '143B',
          '144A', '144B', '145A']

all_cycle_params = {}
for cycle in cycles:
    all_cycle_params[cycle] = processor.process_cycle(cycle)

# Save processed parameters
import json
with open('processed_cycle_data.json', 'w') as f:
    json.dump(all_cycle_params, f, indent=2)

print("\nProcessed data saved to: processed_cycle_data.json")
```

---

## Summary

**Key Principles**:

1. **Time-Weighted Averaging**: Convert continuous → discrete
2. **Closest-Value Selection**: Match continuous to allowed discrete values
3. **Validation First**: Always validate external data before use
4. **Visualization**: Plot data to catch errors visually
5. **Provenance Tracking**: Document data sources

**Tools**:
- **pandas**: CSV/Excel processing
- **numpy**: Numerical operations
- **sqlite3**: Database queries
- **openpyxl**: Excel file handling

**Next Steps**:
- Adapt examples to your data format
- Implement validation appropriate to your application
- Create diagnostic visualizations
- Document data provenance

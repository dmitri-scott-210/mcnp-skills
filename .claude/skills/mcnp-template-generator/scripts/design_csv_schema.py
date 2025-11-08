"""
Design CSV Schema for Template Data
Generate template CSV file for data collection
"""

import argparse
import pandas as pd


def create_csv_template(cycles, parameters, output_file, with_timesteps=False):
    """
    Create CSV template for data collection.
    
    Args:
        cycles: List of cycle identifiers
        parameters: List of parameter names
        output_file: Output CSV file path
        with_timesteps: Include timestep columns
    """
    # Build column structure
    columns = ['Cycle']
    
    if with_timesteps:
        columns.extend(['Timestep', 'Time_Interval_hrs'])
    
    columns.extend(parameters)
    
    # Create example data
    rows = []
    
    for cycle in cycles:
        if with_timesteps:
            # Create 3 timesteps per cycle as example
            for ts in range(1, 4):
                row = {
                    'Cycle': cycle,
                    'Timestep': ts,
                    'Time_Interval_hrs': 24.0,
                }
                # Add parameter placeholders
                for param in parameters:
                    row[param] = 0.0
                
                rows.append(row)
        else:
            row = {'Cycle': cycle}
            for param in parameters:
                row[param] = 0.0
            rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=columns)
    
    # Write CSV
    df.to_csv(output_file, index=False)
    
    print(f"✓ CSV template created: {output_file}")
    print(f"  Cycles: {len(cycles)}")
    print(f"  Parameters: {len(parameters)}")
    print(f"  Columns: {', '.join(columns)}")
    print(f"  Rows: {len(rows)}")
    print(f"\nNext steps:")
    print(f"  1. Open {output_file} in spreadsheet editor")
    print(f"  2. Fill in parameter values for each cycle/timestep")
    print(f"  3. Use with render_template.py to generate MCNP inputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate CSV template for data collection'
    )
    parser.add_argument('--cycles', '-c', required=True, nargs='+',
                       help='Cycle identifiers (e.g., 138B 139A 140A)')
    parser.add_argument('--parameters', '-p', required=True, nargs='+',
                       help='Parameter names (e.g., Power_MW Temperature_K)')
    parser.add_argument('--output', '-o', default='data_template.csv',
                       help='Output CSV file (default: data_template.csv)')
    parser.add_argument('--with-timesteps', '-t', action='store_true',
                       help='Include timestep columns (for time-series data)')
    
    args = parser.parse_args()
    
    create_csv_template(
        cycles=args.cycles,
        parameters=args.parameters,
        output_file=args.output,
        with_timesteps=args.with_timesteps
    )

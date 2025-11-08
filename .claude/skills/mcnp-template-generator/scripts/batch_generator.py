"""
Batch Template Generator
Generate multiple MCNP inputs from template and data files
"""

import argparse
import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
import os
import sys


def time_weighted_average(values, time_intervals):
    """Calculate time-weighted average."""
    return np.sum(values * time_intervals) / np.sum(time_intervals)


def process_cycle_data(data, cycle, time_column, value_columns):
    """
    Process data for a single cycle.
    
    Args:
        data: DataFrame with cycle data
        cycle: Cycle identifier
        time_column: Name of time interval column
        value_columns: List of parameter columns to average
        
    Returns:
        Dictionary of averaged values
    """
    cycle_data = data[data['Cycle'] == cycle]
    
    if len(cycle_data) == 0:
        raise ValueError(f"No data found for cycle {cycle}")
    
    result = {'Cycle': cycle}
    
    # Check if time-weighted averaging needed
    if time_column and time_column in cycle_data.columns:
        time_intervals = cycle_data[time_column].values
        
        for col in value_columns:
            if col in cycle_data.columns:
                values = cycle_data[col].values
                result[col] = time_weighted_average(values, time_intervals)
    else:
        # Simple average or single value
        for col in value_columns:
            if col in cycle_data.columns:
                result[col] = cycle_data[col].mean()
    
    return result


def batch_generate(template_path, data_path, output_dir, time_column=None, 
                   value_columns=None, validate=True):
    """
    Generate multiple MCNP inputs from template and CSV data.
    
    Args:
        template_path: Path to .template file
        data_path: Path to CSV data file
        output_dir: Directory for generated inputs
        time_column: Name of time interval column (for averaging)
        value_columns: List of value columns to process
        validate: Check for unreplaced variables
    """
    print("=" * 70)
    print("BATCH TEMPLATE GENERATION")
    print("=" * 70)
    
    # Load data
    print(f"\n📊 Loading data from {data_path}...")
    data = pd.read_csv(data_path)
    
    if 'Cycle' not in data.columns:
        raise ValueError("CSV must have 'Cycle' column")
    
    cycles = data['Cycle'].unique()
    print(f"  Found {len(cycles)} cycles: {', '.join(map(str, cycles))}")
    
    # Auto-detect value columns if not specified
    if value_columns is None:
        excluded = ['Cycle', 'Timestep', time_column] if time_column else ['Cycle', 'Timestep']
        value_columns = [col for col in data.columns if col not in excluded]
        print(f"  Auto-detected parameters: {', '.join(value_columns)}")
    
    # Setup template
    print(f"\n📄 Loading template from {template_path}...")
    template_dir = os.path.dirname(template_path) or '.'
    template_name = os.path.basename(template_path)
    
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate inputs for each cycle
    print(f"\n🔧 Generating MCNP inputs...")
    print("-" * 70)
    
    for cycle in cycles:
        # Process cycle data
        cycle_params = process_cycle_data(data, cycle, time_column, value_columns)
        
        # Render template
        output = template.render(**cycle_params)
        
        # Validate
        if validate and ('{{' in output or '}}' in output):
            print(f"⚠ Warning: Unreplaced variables in cycle {cycle}")
        
        # Write file
        base_name = os.path.splitext(template_name)[0]
        output_file = os.path.join(output_dir, f'{base_name}_{cycle}.i')
        
        with open(output_file, 'w') as f:
            f.write(output)
        
        # Report
        print(f"✓ {cycle:10s}: {len(output):7d} bytes → {output_file}")
    
    print("-" * 70)
    print(f"\n✓ Generated {len(cycles)} MCNP inputs in {output_dir}/")
    print("\nNext steps:")
    print(f"  1. Validate inputs: ls -lh {output_dir}/")
    print(f"  2. Test one input: mcnp6 inp={output_dir}/{os.listdir(output_dir)[0] if os.listdir(output_dir) else 'file.i'}")
    print(f"  3. Run batch: for f in {output_dir}/*.i; do mcnp6 inp=$f; done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Batch generate MCNP inputs from template and CSV data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple generation (one value per cycle)
  python batch_generator.py template.i data.csv -o mcnp/
  
  # With time-weighted averaging
  python batch_generator.py template.i data.csv -o mcnp/ --time-column Time_Interval_hrs
  
  # Specify value columns
  python batch_generator.py template.i data.csv -o mcnp/ --values Power_MW Temperature_K
        """
    )
    
    parser.add_argument('template', help='Template file (.template)')
    parser.add_argument('data', help='CSV data file')
    parser.add_argument('--output-dir', '-o', default='output',
                       help='Output directory (default: output/)')
    parser.add_argument('--time-column', '-t',
                       help='Time interval column for weighted averaging')
    parser.add_argument('--values', '-v', nargs='+',
                       help='Value columns to process (default: auto-detect)')
    parser.add_argument('--no-validate', action='store_true',
                       help='Skip validation of rendered output')
    
    args = parser.parse_args()
    
    try:
        batch_generate(
            template_path=args.template,
            data_path=args.data,
            output_dir=args.output_dir,
            time_column=args.time_column,
            value_columns=args.values,
            validate=not args.no_validate
        )
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

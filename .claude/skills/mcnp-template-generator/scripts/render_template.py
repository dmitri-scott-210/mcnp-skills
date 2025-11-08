"""
Render Jinja2 Template with Data
Apply CSV data or Python dict to MCNP template
"""

import argparse
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
import sys


def render_from_dict(template_path, data_dict, output_path):
    """
    Render template with Python dictionary.
    
    Args:
        template_path: Path to .template file
        data_dict: Dictionary of template variables
        output_path: Where to write rendered output
    """
    template_dir = os.path.dirname(template_path) or '.'
    template_name = os.path.basename(template_path)
    
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    
    # Render
    output = template.render(**data_dict)
    
    # Validate
    if '{{' in output or '}}' in output:
        print(f"⚠ Warning: Unreplaced variables found in {output_path}")
        import re
        unreplaced = re.findall(r'\{\{([^}]+)\}\}', output)
        print(f"  Unreplaced: {unreplaced}")
    
    # Write
    with open(output_path, 'w') as f:
        f.write(output)
    
    print(f"✓ Rendered: {output_path} ({len(output)} bytes)")


def render_from_csv(template_path, csv_path, output_dir, cycle_column='Cycle'):
    """
    Render template for each cycle in CSV file.
    
    Args:
        template_path: Path to .template file
        csv_path: Path to CSV data file
        output_dir: Directory to write rendered files
        cycle_column: Name of cycle identifier column
    """
    # Read CSV
    data = pd.read_csv(csv_path)
    
    if cycle_column not in data.columns:
        raise ValueError(f"Column '{cycle_column}' not found in CSV")
    
    cycles = data[cycle_column].unique()
    
    print(f"Found {len(cycles)} cycles in {csv_path}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Setup template
    template_dir = os.path.dirname(template_path) or '.'
    template_name = os.path.basename(template_path)
    
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    
    # Render for each cycle
    for cycle in cycles:
        cycle_data = data[data[cycle_column] == cycle].iloc[0]  # First row for cycle
        
        # Convert to dict
        data_dict = cycle_data.to_dict()
        
        # Render
        output = template.render(**data_dict)
        
        # Write
        base_name = os.path.splitext(template_name)[0]
        output_path = os.path.join(output_dir, f'{base_name}_{cycle}.i')
        
        with open(output_path, 'w') as f:
            f.write(output)
        
        print(f"✓ {cycle}: {output_path}")
    
    print(f"\n✓ Rendered {len(cycles)} inputs in {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Render Jinja2 template with data'
    )
    parser.add_argument('template', help='Template file (.template)')
    parser.add_argument('--data', '-d', help='CSV data file')
    parser.add_argument('--output-dir', '-o', default='output',
                       help='Output directory (default: output/)')
    parser.add_argument('--cycle-column', '-c', default='Cycle',
                       help='Cycle identifier column name (default: Cycle)')
    
    args = parser.parse_args()
    
    if args.data:
        render_from_csv(args.template, args.data, args.output_dir, args.cycle_column)
    else:
        print("Error: --data required")
        parser.print_help()
        sys.exit(1)

"""
Create Jinja2 Template from MCNP Input
Converts MCNP input to template by replacing specified sections with variables
"""

import argparse
import re


def create_template(input_file, output_file, variables):
    """
    Convert MCNP input to Jinja2 template.
    
    Args:
        input_file: Path to MCNP input file
        output_file: Path to output template file
        variables: List of (placeholder_name, start_line, end_line) tuples
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Sort variables by start_line in reverse to avoid index shifting
    variables_sorted = sorted(variables, key=lambda x: x[1], reverse=True)
    
    # Replace sections with template variables
    for var_name, start, end in variables_sorted:
        # Replace lines [start:end] with {{var_name}}
        template_var = f"{{{{{var_name}}}}}\n"
        lines[start:end] = [template_var]
    
    # Write template
    with open(output_file, 'w') as f:
        f.writelines(lines)
    
    print(f"✓ Template created: {output_file}")
    print(f"  Replaced {len(variables)} sections with template variables")
    for var_name, start, end in variables:
        print(f"    - {{{{{var_name}}}}}: lines {start}-{end}")


def interactive_mode(input_file, output_file):
    """
    Interactive mode to select sections for templating.
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    print(f"\nMCNP Input: {input_file} ({len(lines)} lines)")
    print("=" * 70)
    
    # Show file structure
    print("\nFile preview:")
    for i, line in enumerate(lines[:20], 1):
        print(f"  {i:4d}: {line.rstrip()}")
    print(f"  ... ({len(lines) - 20} more lines)")
    
    # Collect variables
    variables = []
    
    print("\n" + "=" * 70)
    print("Define template variables (press Enter to finish)")
    print("=" * 70)
    
    while True:
        print("\nNew template variable:")
        var_name = input("  Variable name (e.g., 'oscc_surfaces'): ").strip()
        
        if not var_name:
            break
        
        start = input("  Start line number: ").strip()
        end = input("  End line number: ").strip()
        
        try:
            start = int(start) - 1  # Convert to 0-indexed
            end = int(end)
            
            if start < 0 or end > len(lines) or start >= end:
                print("  ✗ Invalid line range")
                continue
            
            variables.append((var_name, start, end))
            print(f"  ✓ Added {{{{{var_name}}}}} (lines {start+1}-{end})")
            
        except ValueError:
            print("  ✗ Invalid line numbers")
            continue
    
    if not variables:
        print("\nNo variables defined. Exiting.")
        return
    
    # Create template
    create_template(input_file, output_file, variables)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert MCNP input to Jinja2 template'
    )
    parser.add_argument('input_file', help='MCNP input file')
    parser.add_argument('--output', '-o', default='template.i',
                       help='Output template file (default: template.i)')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive mode to select sections')
    parser.add_argument('--variables', '-v', nargs='+',
                       help='Variable definitions: name:start:end (e.g., oscc:100:150)')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode(args.input_file, args.output)
    elif args.variables:
        # Parse variable definitions
        variables = []
        for var_def in args.variables:
            parts = var_def.split(':')
            if len(parts) != 3:
                print(f"✗ Invalid variable definition: {var_def}")
                print("  Expected format: name:start:end")
                continue
            
            name, start, end = parts
            variables.append((name, int(start)-1, int(end)))
        
        create_template(args.input_file, args.output, variables)
    else:
        print("Error: Specify --interactive or --variables")
        parser.print_help()

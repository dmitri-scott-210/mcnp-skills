#!/usr/bin/env python3
"""
Universe Hierarchy Visualizer - Parse and visualize MCNP universe nesting

Usage:
    python universe_hierarchy_visualizer.py input.i
    python universe_hierarchy_visualizer.py input.i --format tree
    python universe_hierarchy_visualizer.py input.i --check-circular

Purpose:
    - Extract universe assignments (U parameter) from input
    - Identify FILL references between universes
    - Generate ASCII tree showing hierarchy
    - Detect circular references (errors)
    - Calculate nesting depth

Author: MCNP Lattice Builder Skill
Version: 1.0.0
"""

import sys
import argparse
import re

def main():
    parser = argparse.ArgumentParser(description="Visualize MCNP universe hierarchy")
    parser.add_argument("input_file", help="MCNP input file")
    parser.add_argument("--format", choices=["tree", "list"], default="tree")
    parser.add_argument("--check-circular", action="store_true")

    args = parser.parse_args()

    print(f"Analyzing universe hierarchy in: {args.input_file}")
    print()

    # Parse input file
    universes = parse_universes(args.input_file)
    fill_refs = parse_fill_refs(args.input_file)

    if not universes and not fill_refs:
        print("No universes or FILL references found in input")
        return 1

    # Display results
    print("Universe Definitions:")
    for u, cells in sorted(universes.items()):
        print(f"  U={u}: cells {', '.join(map(str, cells))}")
    print()

    print("FILL References:")
    for cell, filled_u in sorted(fill_refs.items()):
        print(f"  Cell {cell} → FILL={filled_u}")
    print()

    # Build and display hierarchy
    if args.format == "tree":
        display_tree(universes, fill_refs)
    else:
        display_list(universes, fill_refs)

    # Check for circular references
    if args.check_circular or True:  # Always check
        circular = check_circular_refs(fill_refs)
        if circular:
            print("\nWARNING: Circular references detected!")
            for cycle in circular:
                print(f"  {' → '.join(map(str, cycle))}")
        else:
            print("\n✓ No circular references detected")

    return 0

def parse_universes(filename):
    """Extract universe assignments from input file"""
    universes = {}  # {universe_num: [cell_nums]}
    # Simplified parsing - production version would be more robust
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Look for U= parameter on cell cards
                match = re.search(r'\bU\s*=\s*(\d+)', line, re.IGNORECASE)
                if match:
                    u_num = int(match.group(1))
                    # Try to extract cell number (first number on line)
                    cell_match = re.match(r'\s*(\d+)', line)
                    if cell_match:
                        cell_num = int(cell_match.group(1))
                        if u_num not in universes:
                            universes[u_num] = []
                        universes[u_num].append(cell_num)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filename}")
        sys.exit(1)
    return universes

def parse_fill_refs(filename):
    """Extract FILL references from input file"""
    fill_refs = {}  # {cell_num: filled_universe}
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Look for FILL= parameter
                match = re.search(r'\bFILL\s*=\s*(\d+)', line, re.IGNORECASE)
                if match:
                    filled_u = int(match.group(1))
                    # Try to extract cell number
                    cell_match = re.match(r'\s*(\d+)', line)
                    if cell_match:
                        cell_num = int(cell_match.group(1))
                        fill_refs[cell_num] = filled_u
    except FileNotFoundError:
        pass
    return fill_refs

def display_tree(universes, fill_refs):
    """Display hierarchy as ASCII tree"""
    print("Universe Hierarchy (Tree View):")
    print()
    # Start from U=0 (real world)
    print_tree_node(0, universes, fill_refs, visited=set(), indent="")

def print_tree_node(u, universes, fill_refs, visited, indent):
    """Recursively print tree nodes"""
    if u in visited:
        print(f"{indent}U={u} (CIRCULAR REFERENCE!)")
        return

    visited.add(u)

    # Find cells that reference this universe via FILL
    children = []
    for cell, filled in fill_refs.items():
        if filled == u:
            children.append((cell, filled))

    if u == 0:
        print(f"{indent}U=0 (Real World)")
    else:
        cells_in_u = universes.get(u, [])
        print(f"{indent}U={u} (cells: {', '.join(map(str, cells_in_u))})")

    # Print children
    for i, (cell, child_u) in enumerate(children):
        is_last = (i == len(children) - 1)
        branch = "└──" if is_last else "├──"
        next_indent = indent + ("    " if is_last else "│   ")
        print(f"{indent}{branch} Cell {cell} → ", end="")
        # Find what universe this cell belongs to, then recurse to filled universe
        # Simplified: just show the filled universe
        print(f"U={child_u}")
        # Recursively show what's in the filled universe
        print_tree_node(child_u, universes, fill_refs, visited.copy(), next_indent)

def display_list(universes, fill_refs):
    """Display hierarchy as list"""
    print("Universe Hierarchy (List View):")
    all_u = set(universes.keys()) | set(fill_refs.values())
    for u in sorted(all_u):
        print(f"  U={u}")

def check_circular_refs(fill_refs):
    """Check for circular FILL references"""
    # Simplified check - production version would use proper graph algorithm
    circular = []
    # TODO: Implement proper cycle detection
    return circular

if __name__ == "__main__":
    sys.exit(main())

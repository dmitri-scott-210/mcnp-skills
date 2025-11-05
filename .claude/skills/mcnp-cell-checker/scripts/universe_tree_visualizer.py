#!/usr/bin/env python3
"""
Universe Tree Visualizer

Visualizes MCNP universe dependency hierarchy as an indented tree.
Shows cells, fills, levels, and detects circular references.

Usage:
    python universe_tree_visualizer.py input.inp [--output tree.txt]
"""

import sys
import argparse
from mcnp_cell_checker import MCNPCellChecker


def visualize_tree(input_file, output_file=None):
    """
    Build and visualize universe dependency tree

    Args:
        input_file: Path to MCNP input file
        output_file: Optional output file path (prints to stdout if None)
    """
    checker = MCNPCellChecker()
    tree = checker.build_universe_tree(input_file)

    # Build output
    lines = []
    lines.append("=" * 70)
    lines.append(f"Universe Dependency Tree: {input_file}")
    lines.append("=" * 70)
    lines.append("")

    # Summary
    lines.append("Summary:")
    lines.append(f"  Total universes: {len(tree['universes'])}")
    lines.append(f"  Maximum depth: {tree['max_depth']} levels")

    if tree['circular_refs']:
        lines.append(f"  ⚠ Circular references: {len(tree['circular_refs'])}")
    else:
        lines.append("  ✓ No circular references")

    if tree['unreachable']:
        lines.append(f"  ⚠ Unreachable universes: {len(tree['unreachable'])}")

    lines.append("")
    lines.append("=" * 70)
    lines.append("Hierarchy Tree:")
    lines.append("=" * 70)
    lines.append("")

    # Build tree visualization
    universe_info = tree['universes']

    def print_tree(u, indent=0, visited=None):
        """Recursively build tree lines"""
        if visited is None:
            visited = set()

        if u in visited:
            # Circular reference
            lines.append(f"{'  ' * indent}u={u}: [CIRCULAR REFERENCE]")
            return

        visited.add(u)
        info = universe_info.get(u, {})

        indent_str = "  " * indent

        # Format universe info
        if u == 0:
            name = "u=0 (real world)"
        else:
            name = f"u={u}"

        cell_count = len(info.get('cells', []))
        level = info.get('level', '?')
        fills = info.get('fills', [])
        fills_str = str(sorted(fills)) if fills else "none"

        line = f"{indent_str}{name}: level {level}, {cell_count} cells, fills={fills_str}"
        lines.append(line)

        # Recursively print children
        for child_u in sorted(fills):
            print_tree(child_u, indent + 1, visited.copy())

    # Start from real world
    print_tree(0)

    # Show circular references
    if tree['circular_refs']:
        lines.append("")
        lines.append("=" * 70)
        lines.append("Circular References Detected:")
        lines.append("=" * 70)
        for cycle in tree['circular_refs']:
            lines.append(f"  {' → '.join(map(str, cycle))}")

    # Show unreachable universes
    if tree['unreachable']:
        lines.append("")
        lines.append("=" * 70)
        lines.append("Unreachable Universes:")
        lines.append("=" * 70)
        lines.append("  These universes are defined but not connected to real world")
        for u in sorted(tree['unreachable']):
            info = universe_info.get(u, {})
            cell_count = len(info.get('cells', []))
            lines.append(f"  u={u}: {cell_count} cells")

    # Performance analysis
    lines.append("")
    lines.append("=" * 70)
    lines.append("Performance Analysis:")
    lines.append("=" * 70)

    max_depth = tree['max_depth']
    if max_depth <= 3:
        lines.append(f"  ✓ Shallow nesting ({max_depth} levels)")
        lines.append("    Optimal performance expected")
    elif max_depth <= 7:
        lines.append(f"  ✓ Moderate nesting ({max_depth} levels)")
        lines.append("    Acceptable performance")
        lines.append("    💡 Consider negative universe optimization for levels 3+")
    elif max_depth <= 10:
        lines.append(f"  ⚠ Deep nesting ({max_depth} levels)")
        lines.append("    Performance impact expected")
        lines.append("    💡 Apply negative universe optimization")
        lines.append("    💡 Consider combining levels where possible")
    else:
        lines.append(f"  ❌ Excessive nesting ({max_depth} levels)")
        lines.append("    Significant performance penalty")
        lines.append("    💡 Simplify geometry")
        lines.append("    💡 Homogenize lower levels")
        lines.append("    💡 Combine intermediate levels")

    lines.append("")
    lines.append("=" * 70)

    # Output
    output_text = "\n".join(lines)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(output_text)
        print(f"Universe tree written to: {output_file}")
    else:
        print(output_text)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Visualize MCNP universe dependency hierarchy"
    )
    parser.add_argument(
        'input_file',
        help="MCNP input file (.inp, .i, or .txt)"
    )
    parser.add_argument(
        '-o', '--output',
        help="Output file (default: print to stdout)"
    )

    args = parser.parse_args()

    try:
        visualize_tree(args.input_file, args.output)
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

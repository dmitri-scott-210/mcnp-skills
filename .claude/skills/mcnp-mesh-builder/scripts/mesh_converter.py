#!/usr/bin/env python3
"""
Mesh Format Converter for MCNP6

Purpose: Convert between mesh file formats (GMSH, ABAQUS, VTK, CGAL).
Author: MCNP Skills Project
Version: 1.0.0

Usage:
    python mesh_converter.py input.msh --output output.vtk
    python mesh_converter.py input.vtk --format gmsh --output output.msh

Requires: meshio (pip install meshio)
"""

import argparse
import sys
from pathlib import Path

try:
    import meshio
    HAS_MESHIO = True
except ImportError:
    HAS_MESHIO = False
    print("Error: meshio not installed.")
    print("Install with: pip install meshio")
    sys.exit(1)


def detect_format(filename: str) -> str:
    """
    Detect mesh format from file extension.

    Args:
        filename: Input file path

    Returns:
        Format string for meshio
    """
    suffix = Path(filename).suffix.lower()

    format_map = {
        '.msh': 'gmsh',
        '.inp': 'abaqus',
        '.vtk': 'vtk',
        '.vtu': 'vtu',
        '.mesh': 'medit',
        '.stl': 'stl',
        '.obj': 'obj'
    }

    if suffix not in format_map:
        raise ValueError(f"Unknown file format: {suffix}")

    return format_map[suffix]


def convert_mesh(input_file: str, output_file: str,
                 input_format: str = None, output_format: str = None):
    """
    Convert mesh between formats.

    Args:
        input_file: Input mesh file path
        output_file: Output mesh file path
        input_format: Input format (if None, auto-detect from extension)
        output_format: Output format (if None, auto-detect from extension)
    """
    # Auto-detect formats if not specified
    if input_format is None:
        input_format = detect_format(input_file)

    if output_format is None:
        output_format = detect_format(output_file)

    print(f"Converting {input_file} ({input_format}) → {output_file} ({output_format})")

    # Read input mesh
    try:
        mesh = meshio.read(input_file, file_format=input_format)
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        sys.exit(1)

    # Print mesh info
    print(f"\nMesh statistics:")
    print(f"  Vertices: {len(mesh.points):,}")

    total_cells = 0
    for cell_type, cells in mesh.cells:
        print(f"  {cell_type}: {len(cells):,} elements")
        total_cells += len(cells)

    print(f"  Total elements: {total_cells:,}")

    # Write output mesh
    try:
        meshio.write(output_file, mesh, file_format=output_format)
        print(f"\nSuccessfully wrote {output_file}")
    except Exception as e:
        print(f"Error writing {output_file}: {e}")
        sys.exit(1)


def validate_mesh(filename: str):
    """
    Validate mesh file (check for errors, print summary).

    Args:
        filename: Mesh file path
    """
    fmt = detect_format(filename)

    try:
        mesh = meshio.read(filename, file_format=fmt)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"MESH VALIDATION: {filename}")
    print(f"{'='*60}")

    # Basic info
    print(f"\nFormat: {fmt}")
    print(f"Vertices: {len(mesh.points):,}")

    # Element types
    print(f"\nElement types:")
    for cell_type, cells in mesh.cells:
        print(f"  {cell_type}: {len(cells):,} elements")

    # Bounding box
    points = mesh.points
    print(f"\nBounding box:")
    print(f"  X: [{points[:, 0].min():.3f}, {points[:, 0].max():.3f}]")
    print(f"  Y: [{points[:, 1].min():.3f}, {points[:, 1].max():.3f}]")
    print(f"  Z: [{points[:, 2].min():.3f}, {points[:, 2].max():.3f}]")

    # Check for common issues
    print(f"\nValidation checks:")

    # Check 1: Duplicate vertices
    unique_points = set(map(tuple, points))
    if len(unique_points) < len(points):
        duplicates = len(points) - len(unique_points)
        print(f"  ⚠️  Warning: {duplicates} duplicate vertices found")
    else:
        print(f"  ✅ No duplicate vertices")

    # Check 2: Element types supported by MCNP
    supported_types = {'tetra', 'hexahedron', 'wedge', 'pyramid'}
    unsupported = []
    for cell_type, cells in mesh.cells:
        if cell_type not in supported_types:
            unsupported.append(cell_type)

    if unsupported:
        print(f"  ⚠️  Warning: Unsupported element types for MCNP: {unsupported}")
        print(f"      MCNP supports: {supported_types}")
    else:
        print(f"  ✅ All element types supported by MCNP")

    # Check 3: Quadratic elements (not supported by MCNP)
    quadratic_types = {'tetra10', 'hexahedron20', 'wedge15', 'pyramid13'}
    has_quadratic = False
    for cell_type, cells in mesh.cells:
        if cell_type in quadratic_types:
            has_quadratic = True
            print(f"  ⚠️  Warning: Quadratic elements ({cell_type}) not supported by MCNP")
            print(f"      Use linear elements only (tetra, hexahedron, wedge, pyramid)")

    if not has_quadratic:
        print(f"  ✅ No quadratic elements")

    print(f"\n{'='*60}\n")


def list_supported_formats():
    """Print list of supported mesh formats."""
    print("\nSupported mesh formats:\n")

    formats = [
        ("GMSH", ".msh", "gmsh", "Open-source mesh generator"),
        ("ABAQUS", ".inp", "abaqus", "Abaqus FEA input"),
        ("VTK Legacy", ".vtk", "vtk", "VTK legacy ASCII format"),
        ("VTK XML", ".vtu", "vtu", "VTK XML unstructured grid"),
        ("CGAL/Medit", ".mesh", "medit", "CGAL mesh format"),
        ("STL", ".stl", "stl", "Stereolithography (surface only)"),
        ("OBJ", ".obj", "obj", "Wavefront OBJ (surface only)")
    ]

    print(f"{'Format':<15} {'Extension':<12} {'meshio ID':<12} {'Description':<30}")
    print("-" * 75)
    for name, ext, meshio_id, desc in formats:
        print(f"{name:<15} {ext:<12} {meshio_id:<12} {desc:<30}")

    print("\nNote: MCNP supports tetrahedra, hexahedra, wedges, and pyramids only.")
    print("      Use GMSH or ABAQUS formats for best MCNP compatibility.\n")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Convert between mesh file formats for MCNP6',
        epilog='Example: python mesh_converter.py input.msh --output output.vtk'
    )

    parser.add_argument('input', nargs='?', type=str,
                        help='Input mesh file')
    parser.add_argument('-o', '--output', type=str,
                        help='Output mesh file')
    parser.add_argument('-f', '--format', type=str,
                        help='Output format (gmsh, abaqus, vtk, etc.)')
    parser.add_argument('-v', '--validate', action='store_true',
                        help='Validate mesh file (print summary)')
    parser.add_argument('-l', '--list-formats', action='store_true',
                        help='List supported formats')

    args = parser.parse_args()

    if args.list_formats:
        list_supported_formats()
        sys.exit(0)

    if not args.input:
        parser.print_help()
        sys.exit(1)

    if args.validate:
        validate_mesh(args.input)
        sys.exit(0)

    if not args.output:
        print("Error: Output file required (use -o/--output)")
        parser.print_help()
        sys.exit(1)

    # Convert
    convert_mesh(args.input, args.output, output_format=args.format)


if __name__ == '__main__':
    main()

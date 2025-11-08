#!/usr/bin/env python3
"""
Concentric Geometry Generator for MCNP
Generate nested sphere or cylinder cell/surface cards

Usage:
    python concentric_geometry_generator.py --type sphere --radii 0.025 0.035 0.039 --materials 1 2 3 --densities -10.8 -0.98 -1.85
    python concentric_geometry_generator.py --type cylinder --radii 0.41 0.42 0.48 --height 366 --materials 1 0 2 --densities -10.5 0 -6.5

Author: MCNP Geometry Builder Skill
Version: 1.0.0
Date: 2025-11-08
"""

import argparse
import sys
import math


def generate_concentric_spheres(radii, materials, densities, universe=None, start_cell=1, start_surf=1):
    """
    Generate MCNP cell and surface cards for concentric spheres

    Args:
        radii: List of radii (cm), increasing order
        materials: List of material numbers (length = len(radii) + 1 for exterior)
        densities: List of densities (negative for g/cm³, length = len(radii) + 1)
        universe: Universe number (optional)
        start_cell: Starting cell number (default 1)
        start_surf: Starting surface number (default 1)

    Returns:
        tuple: (cell_cards, surface_cards)
    """

    # Validate inputs
    if len(materials) != len(radii) + 1:
        raise ValueError(f"materials must have length {len(radii) + 1} (radii + 1 for exterior)")

    if len(densities) != len(radii) + 1:
        raise ValueError(f"densities must have length {len(radii) + 1} (radii + 1 for exterior)")

    if radii != sorted(radii):
        raise ValueError("radii must be in increasing order")

    n = len(radii)
    cell_cards = []
    surface_cards = []

    # Generate cells
    u_spec = f"  u={universe}" if universe else ""

    # Inner sphere
    mat = materials[0]
    dens = densities[0]
    if mat == 0:
        cell_cards.append(f"{start_cell}    0  -{start_surf}{u_spec}  $ Core (void)")
    else:
        cell_cards.append(f"{start_cell}    {mat}  {dens:.3f}  -{start_surf}{u_spec}  $ Core")

    # Intermediate shells
    for i in range(1, n):
        cell_num = start_cell + i
        surf_inner = start_surf + i - 1
        surf_outer = start_surf + i
        mat = materials[i]
        dens = densities[i]

        if mat == 0:
            cell_cards.append(f"{cell_num}    0  {surf_inner} -{surf_outer}{u_spec}  $ Layer {i} (void)")
        else:
            cell_cards.append(f"{cell_num}    {mat}  {dens:.3f}  {surf_inner} -{surf_outer}{u_spec}  $ Layer {i}")

    # Exterior cell
    cell_num = start_cell + n
    surf = start_surf + n - 1
    mat = materials[n]
    dens = densities[n]

    if universe:
        # In universe, exterior cell has material
        if mat == 0:
            cell_cards.append(f"{cell_num}    0  {surf}{u_spec}  $ Exterior (void)")
        else:
            cell_cards.append(f"{cell_num}    {mat}  {dens:.3f}  {surf}{u_spec}  $ Exterior")
    else:
        # Global geometry, exterior is graveyard
        cell_cards.append(f"{cell_num}    0  {surf}  imp:n=0  $ Graveyard")

    # Generate surfaces
    for i, r in enumerate(radii):
        surf_num = start_surf + i
        r_um = r * 10000  # Convert cm to μm
        surface_cards.append(f"{surf_num}    so  {r:.6f}    $ R = {r_um:.1f} μm = {r*10:.3f} mm")

    cells = "\n".join(cell_cards)
    surfaces = "\n".join(surface_cards)

    return cells, surfaces


def generate_concentric_cylinders(radii, height, materials, densities,
                                  center=(0, 0), universe=None, z_planes=None,
                                  start_cell=1, start_surf=1):
    """
    Generate MCNP cell and surface cards for concentric cylinders

    Args:
        radii: List of radii (cm), increasing order
        height: Cylinder height (cm) or (z_min, z_max) tuple
        materials: List of material numbers (length = len(radii) + 1)
        densities: List of densities (length = len(radii) + 1)
        center: (x, y) center coordinates (default origin)
        universe: Universe number (optional)
        z_planes: (z_min_surf, z_max_surf) surface numbers (optional)
        start_cell: Starting cell number (default 1)
        start_surf: Starting surface number (default 1)

    Returns:
        tuple: (cell_cards, surface_cards)
    """

    # Validate inputs
    if len(materials) != len(radii) + 1:
        raise ValueError(f"materials must have length {len(radii) + 1}")

    if len(densities) != len(radii) + 1:
        raise ValueError(f"densities must have length {len(radii) + 1}")

    if radii != sorted(radii):
        raise ValueError("radii must be in increasing order")

    # Parse height
    if isinstance(height, tuple):
        z_min, z_max = height
    else:
        z_min, z_max = 0, height

    # Parse z-planes
    if z_planes:
        z_min_surf, z_max_surf = z_planes
        z_spec = f"  -{z_min_surf} {z_max_surf}"
        add_z_surfaces = False
    else:
        # Assign surface numbers for Z planes
        z_min_surf = start_surf + len(radii)
        z_max_surf = start_surf + len(radii) + 1
        z_spec = f"  -{z_min_surf} {z_max_surf}"
        add_z_surfaces = True

    n = len(radii)
    cell_cards = []
    surface_cards = []

    cx, cy = center
    u_spec = f"  u={universe}" if universe else ""

    # Determine surface type
    if abs(cx) < 1e-10 and abs(cy) < 1e-10:
        surf_type = "cz"
        surf_params = lambda r: f"{r:.4f}"
        center_note = "(on Z-axis)"
    else:
        surf_type = "c/z"
        surf_params = lambda r: f"{cx:.6f}  {cy:.6f}  {r:.4f}"
        center_note = f"(center: {cx:.3f}, {cy:.3f})"

    # Generate cells
    # Inner cylinder
    mat = materials[0]
    dens = densities[0]
    if mat == 0:
        cell_cards.append(f"{start_cell}    0  -{start_surf}{z_spec}{u_spec}  $ Core (void)")
    else:
        cell_cards.append(f"{start_cell}    {mat}  {dens:.3f}  -{start_surf}{z_spec}{u_spec}  $ Core")

    # Intermediate shells
    for i in range(1, n):
        cell_num = start_cell + i
        surf_inner = start_surf + i - 1
        surf_outer = start_surf + i
        mat = materials[i]
        dens = densities[i]

        if mat == 0:
            cell_cards.append(f"{cell_num}    0  {surf_inner} -{surf_outer}{z_spec}{u_spec}  $ Layer {i} (void)")
        else:
            cell_cards.append(f"{cell_num}    {mat}  {dens:.3f}  {surf_inner} -{surf_outer}{z_spec}{u_spec}  $ Layer {i}")

    # Exterior
    cell_num = start_cell + n
    surf = start_surf + n - 1
    mat = materials[n]
    dens = densities[n]

    if universe:
        if mat == 0:
            cell_cards.append(f"{cell_num}    0  {surf}{z_spec}{u_spec}  $ Exterior (void)")
        else:
            cell_cards.append(f"{cell_num}    {mat}  {dens:.3f}  {surf}{z_spec}{u_spec}  $ Exterior")
    else:
        cell_cards.append(f"{cell_num}    0  {surf}{z_spec}  imp:n=0  $ Graveyard")

    # Generate radial surfaces
    for i, r in enumerate(radii):
        surf_num = start_surf + i
        r_mm = r * 10
        surface_cards.append(f"{surf_num}    {surf_type}  {surf_params(r)}    $ R = {r_mm:.1f} mm {center_note}")

    # Generate z-plane surfaces if not provided
    if add_z_surfaces:
        surface_cards.append(f"{z_min_surf}    pz  {z_min:.4f}    $ Bottom")
        surface_cards.append(f"{z_max_surf}    pz  {z_max:.4f}    $ Top")

    cells = "\n".join(cell_cards)
    surfaces = "\n".join(surface_cards)

    return cells, surfaces


def main():
    parser = argparse.ArgumentParser(
        description='Generate MCNP concentric geometry cards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # TRISO particle (5-layer sphere)
  python concentric_geometry_generator.py \\
    --type sphere \\
    --radii 0.025 0.035 0.039 0.0425 0.0465 \\
    --materials 1 2 3 4 5 6 \\
    --densities -10.8 -0.98 -1.85 -3.20 -1.86 -1.75 \\
    --universe 100

  # PWR fuel pin (concentric cylinders)
  python concentric_geometry_generator.py \\
    --type cylinder \\
    --radii 0.4095 0.4178 0.4750 \\
    --height 366 \\
    --materials 1 0 2 3 \\
    --densities -10.5 0 -6.5 -1.0 \\
    --universe 10

  # Off-axis capsule (7 layers)
  python concentric_geometry_generator.py \\
    --type cylinder \\
    --radii 0.635 0.641 1.519 1.588 1.622 1.647 1.786 \\
    --height 0 129.54 \\
    --materials 1 0 2 0 3 4 3 5 \\
    --densities -10.9 0 -1.75 0 -8.0 -13.3 -8.0 -1.2e-3 \\
    --center 25.337 -25.337
        """
    )

    parser.add_argument('--type', required=True, choices=['sphere', 'cylinder'],
                        help='Geometry type (sphere or cylinder)')

    parser.add_argument('--radii', required=True, nargs='+', type=float,
                        help='Radii in cm (space-separated, increasing order)')

    parser.add_argument('--materials', required=True, nargs='+', type=int,
                        help='Material numbers (length = len(radii) + 1 for exterior)')

    parser.add_argument('--densities', required=True, nargs='+', type=float,
                        help='Densities in g/cm³ (negative) or atoms/b-cm (positive)')

    parser.add_argument('--height', nargs='+', type=float,
                        help='Cylinder height (single value or z_min z_max)')

    parser.add_argument('--center', nargs=2, type=float, default=[0, 0],
                        help='Cylinder center (x y) in cm (default: 0 0)')

    parser.add_argument('--universe', type=int,
                        help='Universe number (optional)')

    parser.add_argument('--start-cell', type=int, default=1,
                        help='Starting cell number (default: 1)')

    parser.add_argument('--start-surf', type=int, default=1,
                        help='Starting surface number (default: 1)')

    parser.add_argument('--output', type=str,
                        help='Output file (default: print to stdout)')

    args = parser.parse_args()

    # Validate inputs
    if args.type == 'sphere':
        if args.height:
            print("Warning: --height ignored for sphere geometry", file=sys.stderr)
        if args.center != [0, 0]:
            print("Warning: --center ignored for sphere geometry", file=sys.stderr)

        try:
            cells, surfaces = generate_concentric_spheres(
                args.radii, args.materials, args.densities,
                universe=args.universe,
                start_cell=args.start_cell,
                start_surf=args.start_surf
            )
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.type == 'cylinder':
        if not args.height:
            print("Error: --height required for cylinder geometry", file=sys.stderr)
            sys.exit(1)

        if len(args.height) == 1:
            height = args.height[0]
        elif len(args.height) == 2:
            height = tuple(args.height)
        else:
            print("Error: --height must be single value or z_min z_max", file=sys.stderr)
            sys.exit(1)

        try:
            cells, surfaces = generate_concentric_cylinders(
                args.radii, height, args.materials, args.densities,
                center=tuple(args.center),
                universe=args.universe,
                start_cell=args.start_cell,
                start_surf=args.start_surf
            )
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Format output
    output = []
    output.append("c " + "=" * 60)
    output.append(f"c CONCENTRIC {args.type.upper()} GEOMETRY")
    output.append("c Generated by concentric_geometry_generator.py")
    output.append("c " + "=" * 60)
    output.append("")
    output.append("c Cell Cards")
    output.append(cells)
    output.append("")
    output.append("c Surface Cards")
    output.append(surfaces)
    output.append("")

    # Write or print
    if args.output:
        with open(args.output, 'w') as f:
            f.write('\n'.join(output))
        print(f"Generated {args.type} geometry written to {args.output}")
    else:
        print('\n'.join(output))


if __name__ == "__main__":
    main()

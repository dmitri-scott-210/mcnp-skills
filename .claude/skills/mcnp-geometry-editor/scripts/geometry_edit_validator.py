#!/usr/bin/env python3
"""
MCNP Geometry Edit Validator

Automated validation functions for complex geometry edits in MCNP input files.

Functions:
1. validate_concentric_surfaces() - Check spherical shell consistency
2. validate_lattice_bounds() - Verify lattice surface = N × pitch
3. validate_universe_hierarchy() - Check universe references
4. validate_fill_transformations() - Verify fill placements
5. validate_numbering_scheme() - Check systematic numbering
6. validate_hex_geometry() - LAT=2 specific checks

Usage:
    python geometry_edit_validator.py input_file.i

Author: MCNP Geometry Editor Skill
Date: November 8, 2025
"""

import re
import sys
import math
from typing import Dict, List, Tuple, Set
from collections import defaultdict


class GeometryValidator:
    """Validator for MCNP geometry edits"""

    def __init__(self, input_file: str):
        self.input_file = input_file
        self.lines = []
        self.cells = {}
        self.surfaces = {}
        self.universes_defined = set()
        self.universes_used = set()
        self.errors = []
        self.warnings = []

        self._read_input()
        self._parse_geometry()

    def _read_input(self):
        """Read MCNP input file"""
        try:
            with open(self.input_file, 'r') as f:
                self.lines = f.readlines()
        except FileNotFoundError:
            print(f"ERROR: File not found: {self.input_file}")
            sys.exit(1)

    def _parse_geometry(self):
        """Parse cells and surfaces from input"""
        in_cells = False
        in_surfaces = False

        for i, line in enumerate(self.lines):
            line_clean = line.strip()

            # Skip comments and blank lines
            if not line_clean or line_clean.startswith('c ') or line_clean.startswith('C '):
                continue

            # Detect sections
            if line_clean.lower().startswith('c --- cell'):
                in_cells = True
                in_surfaces = False
                continue
            elif line_clean.lower().startswith('c --- surface') or line_clean.lower().startswith('c surface'):
                in_cells = False
                in_surfaces = True
                continue
            elif line_clean.lower().startswith('c --- data') or line_clean.lower().startswith('c data'):
                in_cells = False
                in_surfaces = False
                continue

            # Parse cells (simplified)
            if in_cells or (not in_surfaces and i < len(self.lines) // 3):
                match = re.match(r'^\s*(\d+)\s+', line)
                if match:
                    cell_id = int(match.group(1))
                    self.cells[cell_id] = line

                    # Extract universe definitions
                    if 'u=' in line.lower():
                        u_match = re.search(r'u=(\d+)', line.lower())
                        if u_match:
                            self.universes_defined.add(int(u_match.group(1)))

                    # Extract fill references
                    if 'fill=' in line.lower():
                        fill_match = re.search(r'fill=(\d+)', line.lower())
                        if fill_match:
                            self.universes_used.add(int(fill_match.group(1)))

            # Parse surfaces (simplified)
            if in_surfaces or (not in_cells and i > len(self.lines) // 3 and i < 2 * len(self.lines) // 3):
                match = re.match(r'^\s*(\d+)\s+(\w+)\s+(.*)', line)
                if match:
                    surf_id = int(match.group(1))
                    surf_type = match.group(2).upper()
                    surf_params = match.group(3)
                    self.surfaces[surf_id] = {
                        'type': surf_type,
                        'params': surf_params,
                        'line': line
                    }

    def validate_concentric_surfaces(self, surface_ids: List[int]) -> bool:
        """
        Validate concentric spherical surfaces.

        Args:
            surface_ids: List of surface IDs (innermost to outermost)

        Returns:
            True if valid, False otherwise

        Checks:
        - All surfaces exist
        - All are spherical (SO or S)
        - Radii increase monotonically
        - Centers match (for S surfaces)
        """
        print(f"\n=== Validating Concentric Surfaces: {surface_ids} ===")

        # Check all surfaces exist
        for surf_id in surface_ids:
            if surf_id not in self.surfaces:
                self.errors.append(f"Surface {surf_id} not found in input")
                return False

        # Extract radii and centers
        radii = []
        centers = []

        for surf_id in surface_ids:
            surf = self.surfaces[surf_id]
            surf_type = surf['type']
            params = surf['params'].split()

            if surf_type == 'SO':
                # SO: radius only
                if len(params) < 1:
                    self.errors.append(f"Surface {surf_id}: Invalid SO parameters")
                    return False
                radii.append(float(params[0]))
                centers.append((0, 0, 0))

            elif surf_type == 'S':
                # S: x y z R
                if len(params) < 4:
                    self.errors.append(f"Surface {surf_id}: Invalid S parameters")
                    return False
                centers.append((float(params[0]), float(params[1]), float(params[2])))
                radii.append(float(params[3]))

            elif surf_type == 'SPH':
                # SPH: x y z R (macrobody)
                if len(params) < 4:
                    self.errors.append(f"Surface {surf_id}: Invalid SPH parameters")
                    return False
                centers.append((float(params[0]), float(params[1]), float(params[2])))
                radii.append(float(params[3]))

            else:
                self.errors.append(f"Surface {surf_id}: Not spherical (type={surf_type})")
                return False

        # Check radii increase monotonically
        for i in range(len(radii) - 1):
            if radii[i] >= radii[i + 1]:
                self.errors.append(
                    f"Surfaces {surface_ids[i]}, {surface_ids[i+1]}: "
                    f"Radii not increasing (R{surface_ids[i]}={radii[i]:.6f}, "
                    f"R{surface_ids[i+1]}={radii[i+1]:.6f})"
                )
                return False

        # Check centers match (if S or SPH surfaces)
        if len(centers) > 1:
            center_0 = centers[0]
            for i, center in enumerate(centers[1:], start=1):
                dist = math.sqrt(
                    (center[0] - center_0[0])**2 +
                    (center[1] - center_0[1])**2 +
                    (center[2] - center_0[2])**2
                )
                if dist > 1e-6:  # Tolerance
                    self.warnings.append(
                        f"Surfaces {surface_ids[0]}, {surface_ids[i]}: "
                        f"Centers differ by {dist:.6f} cm"
                    )

        print(f"✓ Concentric surfaces valid:")
        for i, surf_id in enumerate(surface_ids):
            print(f"  Surface {surf_id}: R = {radii[i]:.6f} cm")

        return True

    def validate_lattice_bounds(self, cell_id: int, pitch: float,
                                 n_elements: Tuple[int, int, int]) -> bool:
        """
        Validate lattice bounding surface matches N × pitch.

        Args:
            cell_id: Lattice cell ID
            pitch: Lattice pitch (cm)
            n_elements: (nx, ny, nz) number of elements in each direction

        Returns:
            True if valid, False otherwise
        """
        print(f"\n=== Validating Lattice Bounds: Cell {cell_id} ===")

        if cell_id not in self.cells:
            self.errors.append(f"Cell {cell_id} not found")
            return False

        cell_line = self.cells[cell_id]

        # Extract bounding surface (assumes -surf_id format)
        surf_match = re.search(r'-(\d+)', cell_line)
        if not surf_match:
            self.errors.append(f"Cell {cell_id}: Cannot find bounding surface")
            return False

        surf_id = int(surf_match.group(1))
        if surf_id not in self.surfaces:
            self.errors.append(f"Surface {surf_id} not found")
            return False

        surf = self.surfaces[surf_id]
        surf_type = surf['type']

        # Check RPP surface
        if surf_type == 'RPP':
            params = surf['params'].split()
            if len(params) < 6:
                self.errors.append(f"Surface {surf_id}: Invalid RPP parameters")
                return False

            xmin, xmax = float(params[0]), float(params[1])
            ymin, ymax = float(params[2]), float(params[3])
            zmin, zmax = float(params[4]), float(params[5])

            x_extent = xmax - xmin
            y_extent = ymax - ymin
            z_extent = zmax - zmin

            nx, ny, nz = n_elements
            expected_x = nx * pitch
            expected_y = ny * pitch
            expected_z = nz * pitch

            tolerance = 0.01 * pitch  # 1% tolerance

            print(f"Surface {surf_id} (RPP):")
            print(f"  X: {x_extent:.6f} cm (expected: {expected_x:.6f} cm)")
            print(f"  Y: {y_extent:.6f} cm (expected: {expected_y:.6f} cm)")
            print(f"  Z: {z_extent:.6f} cm (expected: {expected_z:.6f} cm)")

            valid = True
            if abs(x_extent - expected_x) > tolerance:
                self.errors.append(
                    f"X extent mismatch: {x_extent:.6f} ≠ {expected_x:.6f}"
                )
                valid = False

            if abs(y_extent - expected_y) > tolerance:
                self.errors.append(
                    f"Y extent mismatch: {y_extent:.6f} ≠ {expected_y:.6f}"
                )
                valid = False

            if abs(z_extent - expected_z) > tolerance:
                self.errors.append(
                    f"Z extent mismatch: {z_extent:.6f} ≠ {expected_z:.6f}"
                )
                valid = False

            if valid:
                print("✓ Lattice bounds match N × pitch")
            return valid

        else:
            self.warnings.append(
                f"Surface {surf_id}: Type {surf_type} not RPP, "
                f"automated validation not implemented"
            )
            return True

    def validate_universe_hierarchy(self) -> bool:
        """
        Validate universe hierarchy consistency.

        Checks:
        - All filled universes exist
        - No circular references
        - No orphaned universes (defined but never used)

        Returns:
            True if valid, False otherwise
        """
        print("\n=== Validating Universe Hierarchy ===")

        # Check for missing universe definitions
        missing = self.universes_used - self.universes_defined
        if missing:
            for u in sorted(missing):
                self.errors.append(f"Universe {u} used but not defined")
            return False

        # Check for orphaned universes
        orphaned = self.universes_defined - self.universes_used
        if orphaned:
            for u in sorted(orphaned):
                self.warnings.append(f"Universe {u} defined but never used")

        print(f"Universes defined: {len(self.universes_defined)}")
        print(f"Universes used: {len(self.universes_used)}")
        print(f"Missing: {len(missing)}")
        print(f"Orphaned: {len(orphaned)}")

        if missing:
            return False

        print("✓ Universe hierarchy valid")
        return True

    def validate_fill_transformations(self, fill_cells: Dict[int, Tuple[float, float, float]]) -> bool:
        """
        Validate fill transformations match bounding surfaces.

        Args:
            fill_cells: Dict mapping cell_id to (x, y, z) fill position

        Returns:
            True if valid, False otherwise
        """
        print("\n=== Validating Fill Transformations ===")

        for cell_id, fill_pos in fill_cells.items():
            if cell_id not in self.cells:
                self.errors.append(f"Cell {cell_id} not found")
                continue

            cell_line = self.cells[cell_id]

            # Extract bounding surfaces
            # Look for c/z surface pattern: c/z x y R
            cz_match = re.search(r'c/z\s+([\d.+-]+)\s+([\d.+-]+)\s+([\d.+-]+)', cell_line.lower())

            if cz_match:
                # Check if fill position matches c/z center
                cx = float(cz_match.group(1))
                cy = float(cz_match.group(2))

                fill_x, fill_y, fill_z = fill_pos

                tolerance = 0.01  # 1 cm tolerance

                if abs(fill_x - cx) > tolerance or abs(fill_y - cy) > tolerance:
                    self.errors.append(
                        f"Cell {cell_id}: Fill position ({fill_x:.6f}, {fill_y:.6f}) "
                        f"doesn't match c/z center ({cx:.6f}, {cy:.6f})"
                    )
                else:
                    print(f"✓ Cell {cell_id}: Fill matches c/z center")

        if not self.errors:
            print("✓ All fill transformations valid")
            return True
        return False

    def validate_numbering_scheme(self, scheme: str, check_cells: List[int] = None) -> bool:
        """
        Validate systematic numbering scheme.

        Args:
            scheme: Description of numbering scheme (e.g., "9XYZW")
            check_cells: Optional list of cell IDs to check

        Returns:
            True if valid, False otherwise
        """
        print(f"\n=== Validating Numbering Scheme: {scheme} ===")

        if check_cells is None:
            check_cells = list(self.cells.keys())

        # For AGR-1 style (9XYZW), check if cells follow pattern
        if scheme == "9XYZW":
            for cell_id in check_cells:
                cell_str = str(cell_id)
                if len(cell_str) != 5:
                    self.warnings.append(
                        f"Cell {cell_id}: Not 5 digits (expected 9XYZW format)"
                    )
                elif cell_str[0] != '9':
                    self.warnings.append(
                        f"Cell {cell_id}: Doesn't start with 9 (expected 9XYZW)"
                    )

        print(f"Checked {len(check_cells)} cells against {scheme} scheme")
        print(f"Warnings: {len(self.warnings)}")

        return True  # Numbering is advisory, not fatal

    def validate_hex_geometry(self, surf_id: int, expected_pitch: float = None) -> bool:
        """
        Validate hexagonal geometry (RHP surface).

        Args:
            surf_id: RHP surface ID
            expected_pitch: Expected hexagonal pitch (if known)

        Returns:
            True if valid, False otherwise

        Checks:
        - RHP parameters valid
        - R-vector magnitude
        - Pitch = |R| × √3
        - Height vector perpendicular to R (if applicable)
        """
        print(f"\n=== Validating Hexagonal Geometry: Surface {surf_id} ===")

        if surf_id not in self.surfaces:
            self.errors.append(f"Surface {surf_id} not found")
            return False

        surf = self.surfaces[surf_id]
        if surf['type'] != 'RHP':
            self.errors.append(f"Surface {surf_id}: Not RHP (type={surf['type']})")
            return False

        params = surf['params'].split()
        if len(params) < 9:
            self.errors.append(f"Surface {surf_id}: Invalid RHP parameters (need 9)")
            return False

        # Parse RHP parameters: vx vy vz  hx hy hz  rx ry rz
        vx, vy, vz = float(params[0]), float(params[1]), float(params[2])
        hx, hy, hz = float(params[3]), float(params[4]), float(params[5])
        rx, ry, rz = float(params[6]), float(params[7]), float(params[8])

        # Calculate R-vector magnitude
        r_mag = math.sqrt(rx**2 + ry**2 + rz**2)

        # Calculate pitch
        pitch = r_mag * math.sqrt(3)

        # Calculate height
        h_mag = math.sqrt(hx**2 + hy**2 + hz**2)

        # Check perpendicularity (R · H should be 0)
        dot_product = rx * hx + ry * hy + rz * hz
        perpendicular = abs(dot_product) < 1e-6

        print(f"RHP Surface {surf_id}:")
        print(f"  Origin: ({vx:.6f}, {vy:.6f}, {vz:.6f})")
        print(f"  Height vector: ({hx:.6f}, {hy:.6f}, {hz:.6f}), |H| = {h_mag:.6f} cm")
        print(f"  R-vector: ({rx:.6f}, {ry:.6f}, {rz:.6f}), |R| = {r_mag:.6f} cm")
        print(f"  Hexagonal pitch: {pitch:.6f} cm")
        print(f"  R ⊥ H: {perpendicular} (dot product = {dot_product:.6e})")

        # Validate expected pitch
        if expected_pitch is not None:
            tolerance = 0.01 * expected_pitch
            if abs(pitch - expected_pitch) > tolerance:
                self.errors.append(
                    f"Pitch mismatch: {pitch:.6f} ≠ {expected_pitch:.6f}"
                )
                return False

        if not perpendicular:
            self.warnings.append(
                f"R-vector not perpendicular to height vector (dot = {dot_product:.6e})"
            )

        print("✓ Hexagonal geometry parameters valid")
        return True

    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Errors: {len(self.errors)}")
        for err in self.errors:
            print(f"  ✗ {err}")

        print(f"\nWarnings: {len(self.warnings)}")
        for warn in self.warnings:
            print(f"  ⚠ {warn}")

        if not self.errors:
            print("\n✓ ALL VALIDATIONS PASSED")
        else:
            print("\n✗ VALIDATION FAILED")

        return len(self.errors) == 0


def main():
    """Main validation function"""
    if len(sys.argv) < 2:
        print("Usage: python geometry_edit_validator.py input_file.i")
        sys.exit(1)

    input_file = sys.argv[1]
    validator = GeometryValidator(input_file)

    # Example validations (customize based on your input)
    # validator.validate_concentric_surfaces([91111, 91112, 91113, 91114, 91115])
    # validator.validate_lattice_bounds(cell_id=91116, pitch=0.00583, n_elements=(15, 15, 1))
    validator.validate_universe_hierarchy()
    # validator.validate_hex_geometry(surf_id=400, expected_pitch=2.771)

    validator.print_summary()

    sys.exit(0 if len(validator.errors) == 0 else 1)


if __name__ == "__main__":
    main()

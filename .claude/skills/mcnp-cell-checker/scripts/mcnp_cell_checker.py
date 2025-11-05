#!/usr/bin/env python3
"""
MCNP Cell Card Checker

Validates MCNP cell cards for universe, lattice, and fill correctness.
Checks U/FILL references, LAT specifications, fill array dimensions,
nesting hierarchy, and boundary surfaces.

Usage:
    from mcnp_cell_checker import MCNPCellChecker
    checker = MCNPCellChecker()
    results = checker.check_cells('input.inp')
"""

import re
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple, Any


class MCNPCellChecker:
    """Main cell card validation class"""

    def __init__(self):
        """Initialize cell checker"""
        self.cells = []
        self.surfaces = {}
        self.input_file = None

    def validate_universes(self, input_file: str) -> Dict[str, Any]:
        """
        Validate that all fill= references have corresponding u= definitions

        Args:
            input_file: Path to MCNP input file

        Returns:
            Dictionary with keys:
                'defined': List of defined universe numbers
                'used': List of used universe numbers
                'undefined': List of undefined universes
                'valid': True if all references defined
        """
        self.input_file = input_file
        self._parse_input()

        defined_universes = set()
        used_universes = set()

        # Collect defined universes
        for cell in self.cells:
            if 'u' in cell:
                u_val = cell['u']
                # Negative universes define |u|
                defined_universes.add(abs(u_val))

        # Collect used universes
        for cell in self.cells:
            if 'fill' in cell:
                fill_val = cell['fill']

                if isinstance(fill_val, int):
                    # Simple fill
                    used_universes.add(fill_val)
                elif isinstance(fill_val, dict):
                    # Array fill
                    for u in fill_val['array_values']:
                        if u != 0:  # 0 means void element
                            used_universes.add(u)

        # Find undefined references
        undefined = used_universes - defined_universes

        return {
            'defined': sorted(list(defined_universes)),
            'used': sorted(list(used_universes)),
            'undefined': sorted(list(undefined)),
            'valid': len(undefined) == 0
        }

    def validate_lattices(self, input_file: str) -> Dict[int, Dict[str, Any]]:
        """
        Validate lattice type specifications

        Args:
            input_file: Path to MCNP input file

        Returns:
            Dictionary mapping cell numbers to validation results
        """
        self.input_file = input_file
        self._parse_input()

        results = {}

        for cell in self.cells:
            if 'lat' in cell:
                cell_num = cell['number']
                lat_value = cell['lat']

                errors = []
                warnings = []

                # Check valid LAT values
                if lat_value not in [1, 2]:
                    errors.append(
                        f"Invalid LAT={lat_value} (must be 1 or 2)"
                    )

                # Check FILL requirement
                has_fill = 'fill' in cell
                if not has_fill:
                    errors.append(
                        "LAT specified without FILL (lattice requires fill)"
                    )

                # Check material
                material_ok = (cell.get('material', 0) == 0)
                if not material_ok:
                    errors.append(
                        f"Lattice cell has material {cell['material']} "
                        "(must be void: material 0)"
                    )

                # Count surfaces
                surf_count = len(cell.get('surfaces', []))

                # Check surface count
                if lat_value == 1 and surf_count < 6:
                    warnings.append(
                        f"LAT=1 typically needs 6 surfaces (found {surf_count})"
                    )
                elif lat_value == 2 and surf_count < 8:
                    warnings.append(
                        f"LAT=2 typically needs 8 surfaces (found {surf_count})"
                    )

                results[cell_num] = {
                    'lat_type': lat_value,
                    'has_fill': has_fill,
                    'fill_valid': has_fill,
                    'material_ok': material_ok,
                    'surface_count': surf_count,
                    'errors': errors,
                    'warnings': warnings
                }

        return results

    def check_fill_dimensions(self, input_file: str) -> Dict[int, Dict[str, Any]]:
        """
        Validate fill array dimensions match lattice declarations

        Args:
            input_file: Path to MCNP input file

        Returns:
            Dictionary mapping cell numbers to dimension results
        """
        self.input_file = input_file
        self._parse_input()

        results = {}

        for cell in self.cells:
            if 'fill' in cell and isinstance(cell['fill'], dict):
                cell_num = cell['number']
                fill_data = cell['fill']

                i_range = fill_data['i_range']
                j_range = fill_data['j_range']
                k_range = fill_data['k_range']

                # Calculate expected size
                i_size = i_range[1] - i_range[0] + 1
                j_size = j_range[1] - j_range[0] + 1
                k_size = k_range[1] - k_range[0] + 1
                expected_size = i_size * j_size * k_size

                # Get actual size
                array_values = fill_data['array_values']
                actual_size = len(array_values)

                # Format declaration string
                declaration = (
                    f"fill= {i_range[0]}:{i_range[1]} "
                    f"{j_range[0]}:{j_range[1]} "
                    f"{k_range[0]}:{k_range[1]}"
                )

                results[cell_num] = {
                    'declaration': declaration,
                    'i_range': i_range,
                    'j_range': j_range,
                    'k_range': k_range,
                    'dimensions': (i_size, j_size, k_size),
                    'expected_size': expected_size,
                    'actual_size': actual_size,
                    'array_values': array_values,
                    'valid': expected_size == actual_size
                }

        return results

    def build_universe_tree(self, input_file: str) -> Dict[str, Any]:
        """
        Build complete universe dependency hierarchy

        Args:
            input_file: Path to MCNP input file

        Returns:
            Dictionary with universe hierarchy information
        """
        self.input_file = input_file
        self._parse_input()

        # Initialize universe info
        universe_info = defaultdict(lambda: {
            'cells': [],
            'fills': [],
            'filled_by': [],
            'level': None
        })

        # Build relationships
        for cell in self.cells:
            u_num = abs(cell.get('u', 0))
            universe_info[u_num]['cells'].append(cell['number'])

            if 'fill' in cell:
                fill_val = cell['fill']

                if isinstance(fill_val, int):
                    universe_info[u_num]['fills'].append(fill_val)
                    universe_info[fill_val]['filled_by'].append(u_num)
                elif isinstance(fill_val, dict):
                    unique_fills = set(fill_val['array_values']) - {0}
                    for f_u in unique_fills:
                        if f_u not in universe_info[u_num]['fills']:
                            universe_info[u_num]['fills'].append(f_u)
                        if u_num not in universe_info[f_u]['filled_by']:
                            universe_info[f_u]['filled_by'].append(u_num)

        # Calculate levels using BFS
        queue = deque([(0, 0)])
        visited = {0}
        universe_info[0]['level'] = 0

        while queue:
            u, level = queue.popleft()
            universe_info[u]['level'] = level

            for filled_u in universe_info[u]['fills']:
                if filled_u not in visited:
                    visited.add(filled_u)
                    queue.append((filled_u, level + 1))

        # Find max depth
        max_depth = max(
            (info['level'] for info in universe_info.values()
             if info['level'] is not None),
            default=0
        )

        # Detect circular references
        circular_refs = self._detect_cycles(universe_info)

        # Find unreachable universes
        all_universes = set(universe_info.keys())
        reachable = set(u for u in all_universes
                       if universe_info[u]['level'] is not None)
        unreachable = list((all_universes - reachable) - {0})

        return {
            'universes': dict(universe_info),
            'max_depth': max_depth,
            'circular_refs': circular_refs,
            'unreachable': sorted(unreachable)
        }

    def check_lattice_boundaries(self, input_file: str) -> Dict[int, Dict[str, Any]]:
        """
        Check lattice boundary surface types

        Args:
            input_file: Path to MCNP input file

        Returns:
            Dictionary mapping cell numbers to boundary analysis
        """
        self.input_file = input_file
        self._parse_input()

        results = {}

        for cell in self.cells:
            if 'lat' in cell:
                cell_num = cell['number']
                lat_type = cell['lat']
                surfaces = cell.get('surfaces', [])

                # Get surface types
                surface_types = [
                    self._get_surface_type(s) for s in surfaces
                ]

                # Check if appropriate
                appropriate = False
                recommendations = []

                if lat_type == 1:
                    # Cubic: RPP or 6 planes
                    has_rpp = 'RPP' in surface_types
                    has_box = 'BOX' in surface_types
                    plane_count = sum(
                        1 for st in surface_types
                        if st in ['P', 'PX', 'PY', 'PZ']
                    )

                    if has_rpp or has_box or plane_count >= 6:
                        appropriate = True
                    else:
                        recommendations.append(
                            "Use RPP macrobody or 6 planar surfaces"
                        )

                elif lat_type == 2:
                    # Hexagonal: RHP or 6 P + 2 PZ
                    has_hex = 'HEX' in surface_types
                    has_rhp = 'RHP' in surface_types
                    p_count = surface_types.count('P')
                    pz_count = surface_types.count('PZ')

                    if has_hex or has_rhp or (p_count >= 6 and pz_count >= 2):
                        appropriate = True
                    else:
                        recommendations.append(
                            "Use RHP macrobody or 6 P-planes + 2 PZ-planes"
                        )

                results[cell_num] = {
                    'lat_type': lat_type,
                    'surfaces': surfaces,
                    'surface_types': surface_types,
                    'appropriate': appropriate,
                    'recommendations': recommendations
                }

        return results

    def check_cells(self, input_file: str) -> Dict[str, Any]:
        """
        Run all validations

        Args:
            input_file: Path to MCNP input file

        Returns:
            Dictionary with comprehensive results
        """
        errors = []
        warnings = []
        info = []

        # Universe validation
        universe_check = self.validate_universes(input_file)
        if universe_check['undefined']:
            for u in universe_check['undefined']:
                errors.append(
                    f"Universe {u} referenced in FILL but not defined"
                )
        else:
            info.append(
                f"{len(universe_check['used'])} universe references valid"
            )

        # Lattice validation
        lattice_check = self.validate_lattices(input_file)
        for cell_num, result in lattice_check.items():
            errors.extend(result['errors'])
            warnings.extend(result['warnings'])

        if lattice_check and not any(r['errors'] for r in lattice_check.values()):
            info.append(f"{len(lattice_check)} lattice cells valid")

        # Fill dimension validation
        fill_check = self.check_fill_dimensions(input_file)
        for cell_num, result in fill_check.items():
            if not result['valid']:
                diff = result['actual_size'] - result['expected_size']
                errors.append(
                    f"Cell {cell_num}: Fill array size mismatch "
                    f"(expected {result['expected_size']}, "
                    f"found {result['actual_size']}, {diff:+d})"
                )

        if fill_check and all(r['valid'] for r in fill_check.values()):
            info.append("All fill array dimensions correct")

        # Universe tree
        tree = self.build_universe_tree(input_file)
        if tree['circular_refs']:
            for cycle in tree['circular_refs']:
                errors.append(
                    f"Circular universe reference: "
                    f"{' → '.join(map(str, cycle))}"
                )
        else:
            info.append(f"No circular references (depth: {tree['max_depth']})")

        if tree['max_depth'] > 10:
            warnings.append(
                f"Deep nesting ({tree['max_depth']} levels) "
                "may impact performance"
            )

        # Boundary check
        boundary_check = self.check_lattice_boundaries(input_file)
        for cell_num, result in boundary_check.items():
            if not result['appropriate']:
                warnings.extend(result['recommendations'])

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'info': info,
            'universe_check': universe_check,
            'lattice_check': lattice_check,
            'fill_check': fill_check,
            'tree': tree,
            'boundary_check': boundary_check
        }

    # Private methods

    def _parse_input(self):
        """Parse MCNP input file (simplified parser)"""
        self.cells = []

        with open(self.input_file, 'r') as f:
            content = f.read()

        # Simple cell card extraction (simplified)
        # In real implementation, would use full MCNP parser
        lines = content.split('\n')
        in_cells = False
        cell_buffer = []

        for line in lines:
            # Skip comments
            if line.strip().startswith('c ') or line.strip().startswith('C '):
                continue

            # Detect cell block (simplified)
            if not in_cells and line.strip() and line.strip()[0].isdigit():
                in_cells = True

            if in_cells:
                if line.strip() == '':
                    # End of cell block
                    break

                # Parse cell card (very simplified)
                cell_data = self._parse_cell_line(line)
                if cell_data:
                    self.cells.append(cell_data)

    def _parse_cell_line(self, line: str) -> Dict[str, Any]:
        """Parse a cell card line (simplified)"""
        # This is a simplified parser for demonstration
        # Real implementation would handle continuation lines,
        # parentheses, complex geometries, etc.

        tokens = line.split()
        if not tokens:
            return None

        try:
            cell_num = int(tokens[0])
        except ValueError:
            return None

        cell = {'number': cell_num}

        # Extract parameters (simplified)
        for token in tokens[1:]:
            if token.startswith('u='):
                cell['u'] = int(token[2:])
            elif token.startswith('lat='):
                cell['lat'] = int(token[4:])
            elif token.startswith('fill='):
                # Simplified fill parsing
                cell['fill'] = int(token[5:])

        return cell

    def _detect_cycles(self, universe_info: Dict) -> List[List[int]]:
        """Detect circular universe references using DFS"""
        cycles = []

        def dfs(u, visited, rec_stack, path):
            visited.add(u)
            rec_stack.add(u)
            path.append(u)

            for filled_u in universe_info[u]['fills']:
                if filled_u not in visited:
                    dfs(filled_u, visited, rec_stack, path)
                elif filled_u in rec_stack:
                    # Found cycle
                    cycle_start = path.index(filled_u)
                    cycle = path[cycle_start:] + [filled_u]
                    cycles.append(cycle)

            rec_stack.remove(u)
            path.pop()

        dfs(0, set(), set(), [])
        return cycles

    def _get_surface_type(self, surf_num: int) -> str:
        """Get surface type (simplified)"""
        # In real implementation, would parse surface cards
        # This is a placeholder
        return "UNKNOWN"


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python mcnp_cell_checker.py input.inp")
        sys.exit(1)

    input_file = sys.argv[1]
    checker = MCNPCellChecker()
    results = checker.check_cells(input_file)

    # Display results
    if results['errors']:
        print("\n❌ FATAL ERRORS:")
        for err in results['errors']:
            print(f"  • {err}")

    if results['warnings']:
        print("\n⚠ WARNINGS:")
        for warn in results['warnings']:
            print(f"  • {warn}")

    if results['info']:
        print("\n📝 INFORMATION:")
        for info in results['info']:
            print(f"  • {info}")

    # Overall status
    print("\n" + "=" * 70)
    if results['valid']:
        print("✓ CELL VALIDATION PASSED")
    else:
        print("✗ CELL VALIDATION FAILED")
    print("=" * 70)

    sys.exit(0 if results['valid'] else 1)

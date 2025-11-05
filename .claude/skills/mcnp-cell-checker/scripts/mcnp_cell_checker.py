"""MCNP Cell Checker - Validates universe, lattice, and fill specifications

This module provides comprehensive validation of MCNP cell card features:
- Universe definitions and references (U and FILL parameters)
- Lattice type specifications (LAT=1 or LAT=2)
- Fill array dimension matching
- Universe nesting hierarchy and circular reference detection
- Lattice boundary surface validation

Based on MCNP6 Manual Chapter 5.2 (Cell Cards) and 5.5.5 (Repeated Structures)
"""

import sys
from pathlib import Path
# Add project root to path (go up 3 levels: mcnp-cell-checker -> skills -> .claude -> project root)
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from parsers.input_parser import MCNPInputParser
from utils.geometry_evaluator import GeometryEvaluator
from collections import deque
import re


class MCNPCellChecker:
    """Validates MCNP cell cards for universe/lattice/fill correctness"""

    def __init__(self):
        self.parser = MCNPInputParser()
        self.parsed = None
        self.errors = []
        self.warnings = []
        self.info = []

    def check_cells(self, filepath: str) -> dict:
        """Comprehensive cell card validation

        Returns:
            dict: {
                'valid': bool,
                'errors': [str],
                'warnings': [str],
                'info': [str]
            }
        """
        self.errors = []
        self.warnings = []
        self.info = []

        # Parse input file
        try:
            self.parsed = self.parser.parse_file(filepath)
        except Exception as e:
            self.errors.append(f"Failed to parse input file: {str(e)}")
            return self._build_results()

        # Run all validation checks
        self._validate_universe_references()
        self._validate_lattice_types()
        self._validate_fill_dimensions()
        self._detect_circular_references()
        self._check_lattice_boundaries()
        self._check_nesting_depth()

        return self._build_results()

    def validate_universes(self, filepath: str) -> dict:
        """Check universe definitions and references

        Returns:
            dict: {
                'defined': [int],       # Universe numbers defined with u=
                'used': [int],          # Universe numbers referenced in fill=
                'undefined': [int]      # Used but not defined
            }
        """
        if not self.parsed or filepath:
            self.parsed = self.parser.parse_file(filepath)

        defined = set()
        used = set()

        for cell in self.parsed['cells']:
            # Collect universe definitions
            if hasattr(cell, 'parameters') and cell.parameters:
                if 'U' in cell.parameters:
                    u_num = abs(cell.parameters['U'])  # Strip negative sign
                    if u_num == 0:
                        # Universe 0 is implicit real world, shouldn't be explicit
                        pass
                    else:
                        defined.add(u_num)

                # Collect universe references
                if 'FILL' in cell.parameters:
                    fill_value = cell.parameters['FILL']

                    if isinstance(fill_value, int):
                        # Simple fill: fill=5
                        if fill_value != 0:
                            used.add(fill_value)

                    elif isinstance(fill_value, dict) and 'array_values' in fill_value:
                        # Array fill: extract universe IDs
                        for u in fill_value['array_values']:
                            if u != 0:
                                used.add(u)

        undefined = used - defined

        return {
            'defined': sorted(list(defined)),
            'used': sorted(list(used)),
            'undefined': sorted(list(undefined))
        }

    def validate_lattices(self, filepath: str) -> dict:
        """Validate lattice specifications (LAT parameter)

        Returns:
            dict: {
                cell_num: {
                    'lat_type': int (1 or 2),
                    'has_fill': bool,
                    'fill_valid': bool,
                    'errors': [str]
                }
            }
        """
        if not self.parsed or filepath:
            self.parsed = self.parser.parse_file(filepath)

        results = {}

        for cell in self.parsed['cells']:
            if not (hasattr(cell, 'parameters') and cell.parameters):
                continue

            if 'LAT' in cell.parameters:
                lat_type = cell.parameters['LAT']
                errors = []

                # Check valid LAT values (1 or 2 only)
                if lat_type not in [1, 2]:
                    errors.append(f"Invalid LAT={lat_type} (must be 1 or 2)")

                # Check FILL requirement
                has_fill = 'FILL' in cell.parameters
                if not has_fill:
                    errors.append("LAT specified without FILL (lattice requires fill)")

                # Check material (should be void)
                if cell.material != 0:
                    errors.append(f"Lattice cell has material {cell.material} "
                                "(should be void)")

                # Check surface count
                geom_eval = GeometryEvaluator()
                surfaces = geom_eval.get_all_surfaces(cell.geometry)

                if lat_type == 1 and len(surfaces) < 6:
                    errors.append(f"LAT=1 (cubic) typically needs 6 surfaces, "
                                f"found {len(surfaces)}")
                elif lat_type == 2 and len(surfaces) < 8:
                    errors.append(f"LAT=2 (hexagonal) typically needs 8 surfaces, "
                                f"found {len(surfaces)}")

                results[cell.number] = {
                    'lat_type': lat_type,
                    'has_fill': has_fill,
                    'fill_valid': len(errors) == 0,
                    'errors': errors
                }

        return results

    def check_fill_dimensions(self, filepath: str) -> dict:
        """Validate fill array dimensions match lattice declarations

        Returns:
            dict: {
                cell_num: {
                    'declaration': str,
                    'expected_size': int,
                    'actual_size': int
                }
            }
        """
        if not self.parsed or filepath:
            self.parsed = self.parser.parse_file(filepath)

        results = {}

        for cell in self.parsed['cells']:
            if not (hasattr(cell, 'parameters') and cell.parameters):
                continue

            if 'LAT' in cell.parameters and 'FILL' in cell.parameters:
                fill_value = cell.parameters['FILL']

                if isinstance(fill_value, dict):
                    # Array fill with range
                    i_range = fill_value.get('i_range', (0, 0))
                    j_range = fill_value.get('j_range', (0, 0))
                    k_range = fill_value.get('k_range', (0, 0))

                    # Calculate expected size
                    i_size = i_range[1] - i_range[0] + 1
                    j_size = j_range[1] - j_range[0] + 1
                    k_size = k_range[1] - k_range[0] + 1
                    expected_size = i_size * j_size * k_size

                    # Count actual values
                    actual_values = fill_value.get('array_values', [])
                    actual_size = len(actual_values)

                    # Format declaration string
                    declaration = (f"fill= {i_range[0]}:{i_range[1]} "
                                 f"{j_range[0]}:{j_range[1]} "
                                 f"{k_range[0]}:{k_range[1]}")

                    results[cell.number] = {
                        'declaration': declaration,
                        'expected_size': expected_size,
                        'actual_size': actual_size
                    }

        return results

    def build_universe_tree(self, filepath: str) -> dict:
        """Build complete universe dependency hierarchy

        Returns:
            dict: {
                'universes': {
                    u_num: {
                        'cells': [cell_nums],
                        'fills': [universe_nums],
                        'level': int
                    }
                },
                'max_depth': int,
                'circular_refs': [[universe_cycle]]
            }
        """
        if not self.parsed or filepath:
            self.parsed = self.parser.parse_file(filepath)

        # Initialize universe info
        universe_info = {}

        # Collect all universe numbers
        all_universes = {0}  # Start with real world
        for cell in self.parsed['cells']:
            if hasattr(cell, 'parameters') and cell.parameters:
                if 'U' in cell.parameters:
                    all_universes.add(abs(cell.parameters['U']))
                if 'FILL' in cell.parameters:
                    fill = cell.parameters['FILL']
                    if isinstance(fill, int):
                        all_universes.add(fill)
                    elif isinstance(fill, dict) and 'array_values' in fill:
                        all_universes.update(fill['array_values'])

        # Initialize all universes
        for u in all_universes:
            universe_info[u] = {
                'cells': [],
                'fills': [],
                'filled_by': [],
                'level': None
            }

        # Build relationships
        for cell in self.parsed['cells']:
            u_num = 0  # Default to real world
            if hasattr(cell, 'parameters') and cell.parameters:
                u_num = abs(cell.parameters.get('U', 0))

            universe_info[u_num]['cells'].append(cell.number)

            # Track what this universe fills
            if hasattr(cell, 'parameters') and cell.parameters:
                if 'FILL' in cell.parameters:
                    fill = cell.parameters['FILL']

                    if isinstance(fill, int):
                        if fill not in universe_info:
                            universe_info[fill] = {
                                'cells': [], 'fills': [], 'filled_by': [], 'level': None
                            }
                        universe_info[u_num]['fills'].append(fill)
                        universe_info[fill]['filled_by'].append(u_num)

                    elif isinstance(fill, dict) and 'array_values' in fill:
                        unique_fills = set(fill['array_values'])
                        for f_u in unique_fills:
                            if f_u not in universe_info:
                                universe_info[f_u] = {
                                    'cells': [], 'fills': [], 'filled_by': [], 'level': None
                                }
                            if f_u not in universe_info[u_num]['fills']:
                                universe_info[u_num]['fills'].append(f_u)
                            if u_num not in universe_info[f_u]['filled_by']:
                                universe_info[f_u]['filled_by'].append(u_num)

        # Calculate hierarchy levels (BFS from real world)
        queue = deque([(0, 0)])  # (universe_num, level)
        visited = {0}

        while queue:
            u, level = queue.popleft()
            universe_info[u]['level'] = level

            for filled_u in universe_info[u]['fills']:
                if filled_u not in visited:
                    visited.add(filled_u)
                    queue.append((filled_u, level + 1))

        # Find max depth
        max_depth = max((info['level'] for info in universe_info.values()
                        if info['level'] is not None), default=0)

        # Detect circular references
        circular_refs = self._find_circular_refs(universe_info)

        return {
            'universes': universe_info,
            'max_depth': max_depth,
            'circular_refs': circular_refs
        }

    def check_lattice_boundaries(self, filepath: str) -> dict:
        """Check lattice cells have appropriate boundary surfaces

        Returns:
            dict: {
                cell_num: {
                    'lat_type': int,
                    'surfaces': [surf_nums],
                    'appropriate': bool,
                    'recommendations': [str]
                }
            }
        """
        if not self.parsed or filepath:
            self.parsed = self.parser.parse_file(filepath)

        results = {}
        geom_eval = GeometryEvaluator()

        for cell in self.parsed['cells']:
            if not (hasattr(cell, 'parameters') and cell.parameters):
                continue

            if 'LAT' in cell.parameters:
                lat_type = cell.parameters['LAT']
                surfaces = geom_eval.get_all_surfaces(cell.geometry)

                # Simplified check based on surface count
                appropriate = False
                recommendations = []
                surf_count = len(surfaces)

                if lat_type == 1:
                    # Cubic lattice - typically 6 surfaces
                    if surf_count >= 6:
                        appropriate = True
                    else:
                        recommendations.append(
                            f"LAT=1 (cubic) typically needs 6 surfaces, found {surf_count}"
                        )

                elif lat_type == 2:
                    # Hexagonal lattice - typically 8 surfaces
                    if surf_count >= 8:
                        appropriate = True
                    else:
                        recommendations.append(
                            f"LAT=2 (hexagonal) typically needs 8 surfaces, found {surf_count}"
                        )

                results[cell.number] = {
                    'lat_type': lat_type,
                    'surfaces': surfaces,
                    'appropriate': appropriate,
                    'recommendations': recommendations
                }

        return results

    # Private helper methods

    def _validate_universe_references(self):
        """Check all FILL references have corresponding U definitions"""
        universe_check = self.validate_universes('')

        # Check for undefined references
        for u in universe_check['undefined']:
            self.errors.append(f"Universe {u} referenced in FILL but not defined "
                             f"with u={u}")

        # Warn about unused definitions
        unused = set(universe_check['defined']) - set(universe_check['used'])
        if unused:
            self.warnings.append(f"Unused universe definitions: {sorted(list(unused))}")

        # Check for universe 0 misuse
        for cell in self.parsed['cells']:
            if hasattr(cell, 'parameters') and cell.parameters:
                if cell.parameters.get('U') == 0:
                    self.errors.append(
                        f"Cell {cell.number}: Universe 0 cannot be explicitly defined "
                        "(it is the default real world)"
                    )

        # Info: report universe counts
        if universe_check['defined']:
            self.info.append(
                f"Found {len(universe_check['defined'])} universe definitions: "
                f"{universe_check['defined']}"
            )
            self.info.append(
                f"Found {len(universe_check['used'])} universe references: "
                f"{universe_check['used']}"
            )

    def _validate_lattice_types(self):
        """Validate LAT parameter values"""
        lattice_results = self.validate_lattices('')

        for cell_num, result in lattice_results.items():
            for error in result['errors']:
                self.errors.append(f"Cell {cell_num}: {error}")

        if lattice_results:
            self.info.append(f"Found {len(lattice_results)} lattice cells")

    def _validate_fill_dimensions(self):
        """Check fill array sizes match declarations"""
        fill_check = self.check_fill_dimensions('')

        for cell_num, result in fill_check.items():
            expected = result['expected_size']
            actual = result['actual_size']

            if expected != actual:
                self.errors.append(
                    f"Cell {cell_num}: Fill array size mismatch\n"
                    f"  {result['declaration']}\n"
                    f"  Expected: {expected} values\n"
                    f"  Actual: {actual} values\n"
                    f"  Difference: {actual - expected:+d}"
                )
            else:
                self.info.append(
                    f"Cell {cell_num}: Fill array size correct ({actual} values)"
                )

    def _detect_circular_references(self):
        """Detect circular universe dependencies"""
        tree = self.build_universe_tree('')

        if tree['circular_refs']:
            for cycle in tree['circular_refs']:
                cycle_str = ' → '.join(map(str, cycle))
                self.errors.append(
                    f"Circular universe reference detected: {cycle_str} → "
                    "(creates infinite loop)"
                )
        else:
            self.info.append("No circular universe references detected")

    def _check_lattice_boundaries(self):
        """Validate lattice boundary surfaces"""
        boundary_check = self.check_lattice_boundaries('')

        for cell_num, result in boundary_check.items():
            if not result['appropriate']:
                for rec in result['recommendations']:
                    self.warnings.append(f"Cell {cell_num}: {rec}")

    def _check_nesting_depth(self):
        """Check universe nesting depth"""
        tree = self.build_universe_tree('')

        max_depth = tree['max_depth']

        if max_depth > 10:
            self.warnings.append(
                f"Deep universe nesting detected: {max_depth} levels\n"
                "  This may impact performance\n"
                "  Consider: (1) simplification, (2) negative universe optimization, "
                "(3) homogenization"
            )
        elif max_depth > 7:
            self.warnings.append(
                f"Moderate universe nesting: {max_depth} levels\n"
                "  Consider using negative u= for fully enclosed cells to improve "
                "performance"
            )
        else:
            self.info.append(f"Universe nesting depth: {max_depth} levels (acceptable)")

    def _find_circular_refs(self, universe_info: dict) -> list:
        """Find circular references in universe dependency graph using DFS

        Returns:
            list: List of cycles, each cycle is a list of universe numbers
        """
        cycles = []

        def dfs(u, visited, rec_stack, path):
            visited.add(u)
            rec_stack.add(u)
            path.append(u)

            for filled_u in universe_info[u]['fills']:
                if filled_u not in visited:
                    if dfs(filled_u, visited, rec_stack, path):
                        return True
                elif filled_u in rec_stack:
                    # Found cycle
                    cycle_start = path.index(filled_u)
                    cycle = path[cycle_start:] + [filled_u]
                    cycles.append(cycle)
                    return True

            rec_stack.remove(u)
            path.pop()
            return False

        # Check for cycles starting from each universe
        for u in universe_info.keys():
            if universe_info[u]['level'] is None:
                # Unreachable from real world, might be in isolated cycle
                visited = set()
                rec_stack = set()
                path = []
                dfs(u, visited, rec_stack, path)

        return cycles

    def _build_results(self) -> dict:
        """Build validation results dictionary"""
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info
        }


def main():
    """Command-line interface for cell checker"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python mcnp_cell_checker.py <input_file>")
        print("\nValidates MCNP cell cards for universe/lattice/fill correctness")
        sys.exit(1)

    input_file = sys.argv[1]

    print(f"MCNP Cell Checker - Validating: {input_file}")
    print("=" * 70)

    checker = MCNPCellChecker()
    results = checker.check_cells(input_file)

    # Print errors
    if results['errors']:
        print("\n[X] FATAL ERRORS:")
        for i, err in enumerate(results['errors'], 1):
            print(f"\n{i}. {err}")

    # Print warnings
    if results['warnings']:
        print("\n[!] WARNINGS:")
        for warn in results['warnings']:
            print(f"  - {warn}")

    # Print info
    if results['info']:
        print("\n[i] INFORMATION:")
        for info in results['info']:
            print(f"  - {info}")

    # Summary
    print("\n" + "=" * 70)
    if results['valid']:
        print("[PASS] CELL VALIDATION PASSED")
        print(f"  - {len(results['errors'])} errors")
        print(f"  - {len(results['warnings'])} warnings")
        print(f"  - {len(results['info'])} info messages")
        sys.exit(0)
    else:
        print("[FAIL] CELL VALIDATION FAILED")
        print(f"  - {len(results['errors'])} errors (must fix)")
        print(f"  - {len(results['warnings'])} warnings")
        sys.exit(1)


if __name__ == "__main__":
    main()

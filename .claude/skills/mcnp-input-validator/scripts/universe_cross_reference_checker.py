"""
MCNP Universe Cross-Reference Validator
Validates universe hierarchy to prevent circular references and undefined universes

Checks:
1. All filled universes are defined
2. No circular dependencies (A→B, B→A or longer cycles)
3. Universe 0 never explicitly defined
4. Reasonable hierarchy depth (<10 levels)
"""

import re
from typing import Dict, List, Set, Tuple


class UniverseCrossRefValidator:
    """Validates universe cross-references and hierarchy"""

    def __init__(self, input_file: str):
        """
        Initialize validator with MCNP input file

        Args:
            input_file: Path to MCNP input file
        """
        self.input_file = input_file
        self.universe_definitions = {}  # universe_id: list of cell_ids defining it
        self.universe_fills = {}  # universe_id: set of filled universe_ids
        self.errors = []
        self.warnings = []

        self._parse_input()

    def _parse_input(self):
        """Parse MCNP input to extract universe definitions and fill references"""
        with open(self.input_file, 'r') as f:
            content = f.read()

        # Parse each cell card
        cell_buffer = []
        in_cells = False

        for line in content.split('\n'):
            # Skip full-line comments
            if line.strip().startswith('c ') or line.strip().startswith('C '):
                continue

            if not line.strip():
                continue

            # Detect surfaces block (exit cells section)
            if re.match(r'^\s*\d+\s+(p[xyz]|c[xyz]|s[ox]|rpp|rhp|rcc)', line, re.IGNORECASE):
                in_cells = False

            # Check if in cells section
            if re.match(r'^\d+\s+\d+', line):
                in_cells = True

            if in_cells:
                # Handle line continuation
                if line.startswith('     '):
                    if cell_buffer:
                        cell_buffer[-1] += ' ' + line.strip()
                else:
                    if cell_buffer:
                        self._parse_cell_for_universes(cell_buffer[-1])
                    cell_buffer.append(line.strip())

        # Parse last cell
        if cell_buffer and in_cells:
            self._parse_cell_for_universes(cell_buffer[-1])

    def _parse_cell_for_universes(self, cell_line: str):
        """
        Parse cell card to extract universe definitions and fill references

        Args:
            cell_line: Complete cell card line
        """
        # Extract cell ID
        cell_id_match = re.match(r'^(\d+)', cell_line.strip())
        if not cell_id_match:
            return
        cell_id = int(cell_id_match.group(1))

        # Look for universe definition (u=XXX)
        u_match = re.search(r'u=(\d+)', cell_line, re.IGNORECASE)
        if u_match:
            universe_id = int(u_match.group(1))

            if universe_id not in self.universe_definitions:
                self.universe_definitions[universe_id] = []
            self.universe_definitions[universe_id].append(cell_id)

        # Look for simple fill directive (fill=XXX)
        fill_simple_match = re.search(r'fill=(\d+)(?:\s|$)', cell_line, re.IGNORECASE)
        if fill_simple_match:
            filled_universe = int(fill_simple_match.group(1))

            # Determine which universe this cell belongs to
            if u_match:
                parent_universe = int(u_match.group(1))
            else:
                parent_universe = 0  # Global universe

            if parent_universe not in self.universe_fills:
                self.universe_fills[parent_universe] = set()
            self.universe_fills[parent_universe].add(filled_universe)

        # Look for lattice fill arrays (fill=i:i j:j k:k ...)
        lat_fill_match = re.search(r'lat=[12].*fill=[\d\-:]+\s+[\d\-:]+\s+[\d\-:]+\s+([\d\s\$RrCc]+)',
                                    cell_line, re.IGNORECASE)
        if lat_fill_match:
            fill_array_str = lat_fill_match.group(1).split('$')[0]  # Remove comments

            # Extract universe numbers from fill array
            # Handle repeat notation: "100 2R 200" → [100, 100, 100, 200]
            tokens = fill_array_str.split()
            filled_universes = set()

            for token in tokens:
                if token.upper().endswith('R'):
                    continue  # Skip repeat notation markers
                try:
                    universe_num = int(token)
                    filled_universes.add(universe_num)
                except ValueError:
                    continue

            # Determine parent universe
            if u_match:
                parent_universe = int(u_match.group(1))
            else:
                parent_universe = 0

            if parent_universe not in self.universe_fills:
                self.universe_fills[parent_universe] = set()
            self.universe_fills[parent_universe].update(filled_universes)

    def find_undefined_universes(self) -> Set[int]:
        """
        Find all universe IDs that are filled but never defined

        Returns:
            Set of undefined universe IDs
        """
        # Collect all filled universes
        all_filled = set()
        for filled_set in self.universe_fills.values():
            all_filled.update(filled_set)

        # Remove universe 0 (always valid, never defined explicitly)
        all_filled.discard(0)

        # Find undefined universes
        undefined = all_filled - set(self.universe_definitions.keys())

        return undefined

    def find_circular_references(self) -> List[List[int]]:
        """
        Find circular universe references using depth-first search

        Returns:
            List of circular reference chains (each is a list of universe IDs)
        """
        circular_chains = []
        visited_global = set()

        def dfs(universe: int, path: List[int], visited_path: Set[int]):
            """Depth-first search to detect cycles"""
            if universe in visited_path:
                # Found a cycle
                cycle_start = path.index(universe)
                cycle = path[cycle_start:] + [universe]
                # Only add unique cycles
                if cycle not in circular_chains:
                    circular_chains.append(cycle)
                return

            if universe in visited_global:
                return

            visited_path_new = visited_path.copy()
            visited_path_new.add(universe)
            path_new = path + [universe]

            # Explore filled universes
            if universe in self.universe_fills:
                for filled_u in self.universe_fills[universe]:
                    dfs(filled_u, path_new, visited_path_new)

            visited_global.add(universe)

        # Start DFS from global universe (0) and all root universes
        all_universes = set(self.universe_definitions.keys()) | {0}
        for u in all_universes:
            if u not in visited_global:
                dfs(u, [], set())

        return circular_chains

    def calculate_hierarchy_depth(self, universe: int = 0, visited: Set[int] = None) -> int:
        """
        Calculate maximum hierarchy depth starting from a universe

        Args:
            universe: Starting universe ID (default 0 = global)
            visited: Set of already visited universes (prevents infinite loops)

        Returns:
            Maximum depth from this universe
        """
        if visited is None:
            visited = set()

        if universe in visited:
            return 0

        visited.add(universe)

        if universe not in self.universe_fills or not self.universe_fills[universe]:
            return 1  # Leaf node

        max_depth = 0
        for filled_u in self.universe_fills[universe]:
            depth = self.calculate_hierarchy_depth(filled_u, visited.copy())
            max_depth = max(max_depth, depth)

        return max_depth + 1

    def check_universe_zero_definition(self) -> bool:
        """
        Check if universe 0 is explicitly defined (it shouldn't be)

        Returns:
            True if error detected, False otherwise
        """
        return 0 in self.universe_definitions

    def validate(self) -> Dict[str, List[str]]:
        """
        Run all universe cross-reference validations

        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        # Check 1: Undefined universes
        undefined = self.find_undefined_universes()
        if undefined:
            self.errors.append(
                f"Undefined universes referenced: {sorted(undefined)}\n"
                f"  These universes are filled but never defined with u=XXX"
            )

        # Check 2: Circular references
        circular = self.find_circular_references()
        if circular:
            for chain in circular:
                chain_str = " → ".join(map(str, chain))
                self.errors.append(
                    f"Circular universe reference detected: {chain_str}\n"
                    f"  Universe {chain[0]} fills {chain[1]}, which eventually fills {chain[0]} again"
                )

        # Check 3: Universe 0 explicitly defined
        if self.check_universe_zero_definition():
            self.errors.append(
                "Universe 0 explicitly defined\n"
                "  Universe 0 is the global universe and should never be defined with u=0"
            )

        # Check 4: Hierarchy depth
        max_depth = self.calculate_hierarchy_depth(0)
        if max_depth > 10:
            self.warnings.append(
                f"Universe hierarchy depth is {max_depth} levels\n"
                f"  Recommendation: Keep hierarchy depth <10 for clarity and performance"
            )
        elif max_depth > 6:
            self.warnings.append(
                f"Universe hierarchy depth is {max_depth} levels (acceptable but deep)"
            )

        return {
            'errors': self.errors,
            'warnings': self.warnings
        }

    def print_report(self):
        """Print validation report to console"""
        results = self.validate()

        print("=" * 70)
        print("UNIVERSE CROSS-REFERENCE VALIDATION REPORT")
        print(f"File: {self.input_file}")
        print("=" * 70)

        print(f"\nUniverses defined: {len(self.universe_definitions)}")
        print(f"Universe fill relationships: {len(self.universe_fills)}")
        print(f"Maximum hierarchy depth: {self.calculate_hierarchy_depth(0)} levels")

        if results['errors']:
            print(f"\n❌ CRITICAL ERRORS ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"\n{error}")
        else:
            print("\n✓ No universe cross-reference errors detected")

        if results['warnings']:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"\n{warning}")

        # Print hierarchy summary
        if self.universe_fills:
            print("\nUniverse Hierarchy Summary:")
            for universe, filled_set in sorted(self.universe_fills.items()):
                if filled_set:
                    print(f"  u={universe} → fills with: {sorted(filled_set)}")

        print("\n" + "=" * 70)


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python universe_cross_reference_checker.py <input_file>")
        sys.exit(1)

    validator = UniverseCrossRefValidator(sys.argv[1])
    validator.print_report()

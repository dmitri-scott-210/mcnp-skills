"""
MCNP Cell Parser
================

Parses MCNP cell cards into structured data for validation.

Handles:
- Simple cells with material and geometry
- Universe assignments (u=XXXX)
- Lattice specifications (lat=1/2)
- Fill arrays with repeat notation
- Fill with translations
- Surface references
- Cross-references to materials

Based on analysis of AGR-1 model with complex lattice hierarchies.

Author: MCNP Cell Checker Skill
Date: 2025-11-08
"""

import re
from typing import List, Optional, Tuple
from cell_validator import (
    CellDefinition, SurfaceDefinition, MaterialDefinition,
    UniverseDefinition, MCNPInputRegistry, LatticeType, SurfaceType
)


class MCNPCellParser:
    """
    Parse MCNP cell cards into structured data

    This parser handles the full complexity of MCNP cell cards including:
    - Multi-line continuation (via & or line breaks)
    - Comment removal
    - Repeat notation in FILL arrays (NR syntax)
    - Translation vectors for FILL
    - All cell card parameters
    """

    def __init__(self):
        self.registry = MCNPInputRegistry()
        self.current_cell_lines = []  # Buffer for multi-line cells
        self.last_fill_element = None  # For repeat notation

    def parse_input_file(self, filename: str) -> MCNPInputRegistry:
        """
        Parse complete MCNP input file

        Returns populated registry with all cells, surfaces, materials parsed.
        """
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.registry.add_error(
                "ERROR", "PARSE",
                f"Input file not found: {filename}"
            )
            return self.registry

        self.registry.total_lines = len(lines)
        in_cells_block = True  # MCNP starts with cells block
        in_surfaces_block = False
        in_materials_block = False

        for line_num, line in enumerate(lines, start=1):
            # Strip trailing whitespace but preserve leading spaces
            line = line.rstrip()

            # Skip blank lines
            if not line.strip():
                # Blank line indicates block transition
                if in_cells_block:
                    in_cells_block = False
                    in_surfaces_block = True
                elif in_surfaces_block:
                    in_surfaces_block = False
                    in_materials_block = True
                continue

            # Skip comment lines (start with 'c' or 'C')
            if line.strip().lower().startswith('c'):
                continue

            # Parse based on current block
            if in_cells_block:
                self._parse_cell_line(line, line_num)
            elif in_surfaces_block:
                self._parse_surface_line(line, line_num)
            elif in_materials_block:
                self._parse_material_line(line, line_num)

        # Parse any remaining accumulated cell lines at end of file
        if self.current_cell_lines:
            self._parse_complete_cell(' '.join(self.current_cell_lines), len(lines))

        return self.registry

    def _parse_cell_line(self, line: str, line_number: int):
        """Parse a single cell card line"""
        # Remove inline comments
        if '$' in line:
            line = line.split('$')[0]

        # Check for continuation (starts with space after line 1)
        if line and line[0] == ' ' and self.current_cell_lines:
            # Continuation line
            self.current_cell_lines.append(line.strip())
            return

        # If we have accumulated lines, parse them as a complete cell
        if self.current_cell_lines:
            self._parse_complete_cell(' '.join(self.current_cell_lines), line_number - len(self.current_cell_lines))

        # Start new cell
        self.current_cell_lines = [line.strip()]

    def _parse_complete_cell(self, cell_line: str, line_number: int):
        """Parse a complete cell card (may span multiple lines)"""
        tokens = cell_line.split()
        if len(tokens) < 2:
            return  # Not a valid cell card

        try:
            cell_id = int(tokens[0])
        except ValueError:
            return  # Not a cell number

        # Parse material ID
        try:
            material_id = int(tokens[1])
            token_idx = 2
        except ValueError:
            self.registry.add_error(
                "ERROR", "PARSE",
                f"Invalid material ID in cell {cell_id}",
                line_number=line_number,
                cell_id=cell_id
            )
            return

        # Parse density (optional for void cells with fill)
        density = None
        if len(tokens) > token_idx:
            try:
                density = float(tokens[token_idx])
                token_idx += 1
            except ValueError:
                # No density specified (might be void with fill)
                pass

        # Parse remaining parameters
        surfaces = []
        universe = None
        lattice_type = LatticeType.NONE
        fill_simple = None
        fill_translation = None
        fill_array_bounds = None
        fill_array_elements = []
        volume = None
        importance = None

        # Reset repeat notation state
        self.last_fill_element = None

        while token_idx < len(tokens):
            token = tokens[token_idx]

            # Universe assignment
            if token.lower().startswith('u='):
                try:
                    universe = int(token.split('=')[1])
                except (ValueError, IndexError):
                    self.registry.add_error(
                        "ERROR", "PARSE",
                        f"Invalid universe specification: {token}",
                        line_number=line_number,
                        cell_id=cell_id
                    )

            # Lattice type
            elif token.lower().startswith('lat='):
                try:
                    lat_value = int(token.split('=')[1])
                    if lat_value == 1:
                        lattice_type = LatticeType.RECTANGULAR
                    elif lat_value == 2:
                        lattice_type = LatticeType.HEXAGONAL
                    else:
                        self.registry.add_error(
                            "ERROR", "LATTICE",
                            f"Invalid LAT value: {lat_value} (must be 1 or 2)",
                            line_number=line_number,
                            cell_id=cell_id
                        )
                except (ValueError, IndexError):
                    self.registry.add_error(
                        "ERROR", "PARSE",
                        f"Invalid lattice specification: {token}",
                        line_number=line_number,
                        cell_id=cell_id
                    )

            # Fill directive
            elif token.lower().startswith('fill='):
                fill_spec = token.split('=')[1]
                if ':' in fill_spec:
                    # Array fill: fill=imin:imax jmin:jmax kmin:kmax
                    fill_array_bounds, next_idx = self._parse_fill_array_bounds(tokens, token_idx)
                    token_idx = next_idx
                    # Parse fill array elements
                    while token_idx < len(tokens) and not self._is_keyword(tokens[token_idx]):
                        elements = self._parse_fill_element(tokens[token_idx])
                        fill_array_elements.extend(elements)
                        token_idx += 1
                    token_idx -= 1  # Back up since loop will increment
                else:
                    # Simple fill: fill=UNIV or fill=UNIV (x y z)
                    try:
                        fill_simple = int(fill_spec)
                    except ValueError:
                        self.registry.add_error(
                            "ERROR", "PARSE",
                            f"Invalid fill universe: {fill_spec}",
                            line_number=line_number,
                            cell_id=cell_id
                        )
                    # Check for translation
                    if token_idx + 1 < len(tokens) and tokens[token_idx + 1].startswith('('):
                        fill_translation, next_idx = self._parse_translation(tokens, token_idx + 1)
                        token_idx = next_idx

            # Volume
            elif token.lower().startswith('vol='):
                try:
                    volume = float(token.split('=')[1])
                except (ValueError, IndexError):
                    pass

            # Importance
            elif token.lower().startswith('imp:'):
                try:
                    importance = float(token.split('=')[1])
                except (ValueError, IndexError):
                    pass

            # Surface number (including negative)
            elif self._is_surface_number(token):
                try:
                    surfaces.append(int(token))
                except ValueError:
                    pass

            token_idx += 1

        # Create cell definition
        cell = CellDefinition(
            cell_id=cell_id,
            material_id=material_id,
            density=density,
            surfaces=surfaces,
            universe=universe,
            lattice_type=lattice_type,
            fill_simple=fill_simple,
            fill_translation=fill_translation,
            fill_array_bounds=fill_array_bounds,
            fill_array_elements=fill_array_elements,
            volume=volume,
            importance=importance,
            line_number=line_number,
            raw_line=cell_line
        )

        self.registry.cells[cell_id] = cell
        self.registry.cells_parsed += 1

        # Register universe if specified
        if universe is not None:
            if universe not in self.registry.universes:
                self.registry.universes[universe] = UniverseDefinition(
                    universe_id=universe,
                    is_lattice=(lattice_type != LatticeType.NONE),
                    lattice_type=lattice_type,
                    defined_at_line=line_number
                )
            self.registry.universes[universe].cells.append(cell_id)

    def _parse_fill_array_bounds(self, tokens: List[str], start_idx: int) -> Tuple[Tuple[int, int, int, int, int, int], int]:
        """
        Parse fill array bounds: fill=imin:imax jmin:jmax kmin:kmax

        Returns: ((imin, imax, jmin, jmax, kmin, kmax), next_token_index)
        """
        bounds_str = tokens[start_idx].split('=')[1]
        idx = start_idx + 1

        # Parse three range pairs
        ranges = []

        # First range is in bounds_str
        if ':' in bounds_str:
            parts = bounds_str.split(':')
            ranges.extend([int(parts[0]), int(parts[1])])

        # Next two ranges
        for _ in range(2):
            if idx < len(tokens) and ':' in tokens[idx] and not self._is_keyword(tokens[idx]):
                parts = tokens[idx].split(':')
                ranges.extend([int(parts[0]), int(parts[1])])
                idx += 1
            else:
                break

        if len(ranges) != 6:
            raise ValueError(f"Invalid fill array bounds: expected 3 ranges, got {len(ranges)//2}")

        return (tuple(ranges), idx)

    def _parse_fill_element(self, token: str) -> List[int]:
        """
        Parse fill array element with repeat notation

        Examples:
          "100" → [100]
          "2R" → [self.last_fill_element] * 3 (if last was 100: [100, 100, 100])

        Returns list of universe IDs
        """
        token = token.strip()

        # Check for repeat notation: NR or Nr
        if re.match(r'^\d+[Rr]$', token):
            n_repeats = int(token[:-1])
            if self.last_fill_element is None:
                return []  # Error: repeat without previous element
            # NR means N additional repeats (total N, not N+1 - MCNP convention)
            return [self.last_fill_element] * n_repeats

        # Simple universe number
        try:
            universe_id = int(token)
            self.last_fill_element = universe_id
            return [universe_id]
        except ValueError:
            return []

    def _parse_translation(self, tokens: List[str], start_idx: int) -> Tuple[Optional[Tuple[float, float, float]], int]:
        """
        Parse translation vector: (x y z) or (x, y, z)

        Returns: ((x, y, z), next_token_index)
        """
        # Combine tokens until we find closing paren
        trans_str = ""
        idx = start_idx
        while idx < len(tokens):
            trans_str += tokens[idx] + " "
            if ')' in tokens[idx]:
                idx += 1
                break
            idx += 1

        # Extract numbers
        trans_str = trans_str.replace('(', '').replace(')', '').replace(',', ' ')
        try:
            coords = [float(x) for x in trans_str.split()]
            if len(coords) == 3:
                return ((coords[0], coords[1], coords[2]), idx)
        except ValueError:
            pass

        return (None, idx)

    def _parse_surface_line(self, line: str, line_number: int):
        """Parse a surface card"""
        # Remove inline comments
        if '$' in line:
            line = line.split('$')[0]

        tokens = line.strip().split()
        if len(tokens) < 2:
            return

        try:
            surface_id = int(tokens[0])
        except ValueError:
            return

        # Get surface type
        surf_type_str = tokens[1].lower()
        try:
            surface_type = SurfaceType(surf_type_str)
        except ValueError:
            surface_type = SurfaceType.UNKNOWN

        # Parse parameters
        params = []
        for token in tokens[2:]:
            try:
                params.append(float(token))
            except ValueError:
                break

        surface = SurfaceDefinition(
            surface_id=surface_id,
            surface_type=surface_type,
            parameters=params,
            line_number=line_number,
            raw_line=line
        )

        self.registry.surfaces[surface_id] = surface
        self.registry.surfaces_parsed += 1

    def _parse_material_line(self, line: str, line_number: int):
        """Parse a material card (basic tracking)"""
        # Remove inline comments
        if '$' in line:
            line = line.split('$')[0]

        tokens = line.strip().split()
        if len(tokens) < 1:
            return

        # Material card starts with 'm' or 'M' followed by number
        if tokens[0].lower().startswith('m'):
            try:
                material_id = int(tokens[0][1:])
                if material_id not in self.registry.materials:
                    self.registry.materials[material_id] = MaterialDefinition(
                        material_id=material_id,
                        line_number=line_number
                    )
                    self.registry.materials_parsed += 1
            except ValueError:
                pass

    def _is_keyword(self, token: str) -> bool:
        """Check if token is a cell card keyword"""
        keywords = ['u=', 'lat=', 'fill=', 'vol=', 'imp:', 'trcl=', '*']
        return any(token.lower().startswith(kw) for kw in keywords)

    def _is_surface_number(self, token: str) -> bool:
        """Check if token is a surface number (including negative)"""
        try:
            int(token)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        parser = MCNPCellParser()
        registry = parser.parse_input_file(sys.argv[1])
        print(registry.generate_summary_report())
    else:
        print("Usage: python cell_parser.py <input_file>")
        print("\nExample test:")

        # Create test input
        test_input = """Test MCNP Input
c Cell block
100 1 -10.0 -1 u=10 imp:n=1
200 0 -2 u=20 lat=1 fill=0:1 0:1 0:0
    10 10
    10 10
300 0 -3 fill=20 (0 0 0) imp:n=1

c Surface block
1 so 1.0
2 rpp -1 1 -1 1 -1 1
3 rpp -2 2 -2 2 -2 2

c Material block
m1 92235.70c 1.0
"""
        # Write to temp file
        with open('/tmp/test_mcnp.i', 'w') as f:
            f.write(test_input)

        parser = MCNPCellParser()
        registry = parser.parse_input_file('/tmp/test_mcnp.i')
        print(registry.generate_summary_report())

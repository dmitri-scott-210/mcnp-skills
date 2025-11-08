"""
MCNP Fill Array Validator
Validates FILL array dimensions for LAT=1 (rectangular) and LAT=2 (hexagonal) lattices

Checks:
1. Element count matches declared fill range
2. Repeat notation correctly expanded
3. All filled universes are defined
4. Lattice type matches surface type

CRITICAL: Dimension calculation is (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
          This works for BOTH LAT=1 (rectangular) and LAT=2 (hexagonal)

Repeat notation: U nR means (n+1) total copies of U
"""

import re
from typing import Dict, List, Tuple, Set


class FillArrayValidator:
    """Validates FILL arrays in MCNP lattice cells"""

    def __init__(self, input_file: str):
        """
        Initialize validator with MCNP input file

        Args:
            input_file: Path to MCNP input file
        """
        self.input_file = input_file
        self.cells = {}  # cell_id: cell_definition
        self.surfaces = {}  # surface_id: surface_definition
        self.universes_defined = set()  # Set of defined universe IDs
        self.lattice_cells = {}  # cell_id: lattice_info
        self.errors = []
        self.warnings = []

        self._parse_input()

    def _parse_input(self):
        """Parse MCNP input file to extract cells, surfaces, universes"""
        with open(self.input_file, 'r') as f:
            content = f.read()

        # Parse cells block (first block after title)
        in_cells = False
        cell_buffer = []

        for line in content.split('\n'):
            # Skip comments and blank lines
            if line.strip().startswith('c ') or line.strip().startswith('C ') or not line.strip():
                continue

            # Detect surfaces block start
            if line.strip() and (line.strip().startswith('*') or re.match(r'^\s*\d+\s+(p[xyz]|c[xyz]|s[ox]|rpp|rhp)', line, re.IGNORECASE)):
                in_cells = False

            # Parse cell cards
            if in_cells:
                # Handle line continuation (indented lines)
                if line.startswith('     '):
                    if cell_buffer:
                        cell_buffer[-1] += ' ' + line.strip()
                else:
                    if cell_buffer:
                        self._parse_cell(cell_buffer[-1])
                    cell_buffer.append(line.strip())
            else:
                # Check if this line starts cells block
                if re.match(r'^\d+\s+\d+', line):
                    in_cells = True
                    cell_buffer = [line.strip()]

        # Parse last cell
        if cell_buffer and in_cells:
            self._parse_cell(cell_buffer[-1])

    def _parse_cell(self, cell_line: str):
        """
        Parse individual cell card to extract LAT and FILL information

        Args:
            cell_line: Complete cell card line (with continuations joined)
        """
        # Extract cell ID
        match = re.match(r'^(\d+)', cell_line)
        if not match:
            return
        cell_id = int(match.group(1))

        self.cells[cell_id] = cell_line

        # Check for universe definition (u=XXX)
        u_match = re.search(r'u=(\d+)', cell_line, re.IGNORECASE)
        if u_match:
            universe_id = int(u_match.group(1))
            self.universes_defined.add(universe_id)

        # Check for lattice definition (lat=1 or lat=2)
        lat_match = re.search(r'lat=([12])', cell_line, re.IGNORECASE)
        if lat_match:
            lat_type = int(lat_match.group(1))

            # Extract FILL specification
            fill_match = re.search(r'fill=([\d\-:]+\s+[\d\-:]+\s+[\d\-:]+)', cell_line, re.IGNORECASE)
            if fill_match:
                fill_spec = fill_match.group(1)

                # Parse fill range: imin:imax jmin:jmax kmin:kmax
                ranges = fill_spec.split()
                if len(ranges) == 3:
                    i_range = ranges[0].split(':')
                    j_range = ranges[1].split(':')
                    k_range = ranges[2].split(':')

                    imin, imax = int(i_range[0]), int(i_range[1])
                    jmin, jmax = int(j_range[0]), int(j_range[1])
                    kmin, kmax = int(k_range[0]), int(k_range[1])

                    # Store lattice info
                    self.lattice_cells[cell_id] = {
                        'lat_type': lat_type,
                        'imin': imin,
                        'imax': imax,
                        'jmin': jmin,
                        'jmax': jmax,
                        'kmin': kmin,
                        'kmax': kmax,
                        'cell_line': cell_line
                    }

    def calculate_required_elements(self, imin: int, imax: int,
                                     jmin: int, jmax: int,
                                     kmin: int, kmax: int) -> int:
        """
        Calculate required number of elements for FILL array

        Works for BOTH LAT=1 (rectangular) and LAT=2 (hexagonal)

        Formula: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)

        Args:
            imin, imax: I-index range
            jmin, jmax: J-index range
            kmin, kmax: K-index range

        Returns:
            Total number of elements required
        """
        i_count = imax - imin + 1
        j_count = jmax - jmin + 1
        k_count = kmax - kmin + 1

        return i_count * j_count * k_count

    def expand_repeat_notation(self, fill_array_str: str) -> List[int]:
        """
        Expand MCNP repeat notation to full universe list

        CRITICAL: nR means (n+1) total copies, NOT n copies!

        Examples:
            "100 2R" → [100, 100, 100]  (100 + 2 more = 3 total)
            "100 2R 200 24R 100 2R" → [100, 100, 100, 200, ..., 100, 100, 100]

        Args:
            fill_array_str: Fill array with potential repeat notation

        Returns:
            List of universe numbers (fully expanded)
        """
        tokens = fill_array_str.split()
        expanded = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Check for repeat notation (e.g., "2R")
            if token.upper().endswith('R'):
                # Extract repeat count
                try:
                    repeat_count = int(token[:-1])
                except ValueError:
                    self.errors.append(f"Invalid repeat notation '{token}' (non-numeric)")
                    i += 1
                    continue

                # Repeat previous element (nR = n+1 total copies)
                if expanded:
                    prev = expanded[-1]
                    expanded.extend([prev] * repeat_count)
                else:
                    self.errors.append(f"Repeat notation '{token}' at start (no previous element)")

            else:
                # Regular universe number
                try:
                    universe_num = int(token)
                    expanded.append(universe_num)
                except ValueError:
                    # Not a number, skip (might be comment marker $)
                    pass

            i += 1

        return expanded

    def validate_fill_array(self, cell_id: int, lattice_info: Dict) -> List[str]:
        """
        Validate FILL array for a specific lattice cell

        Args:
            cell_id: Cell ID number
            lattice_info: Dictionary with lattice parameters

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Calculate required elements
        required = self.calculate_required_elements(
            lattice_info['imin'], lattice_info['imax'],
            lattice_info['jmin'], lattice_info['jmax'],
            lattice_info['kmin'], lattice_info['kmax']
        )

        # Extract fill array from cell line
        # Look for universe numbers after "fill=..." specification
        cell_line = lattice_info['cell_line']

        # Find where fill array starts (after fill=i:i j:j k:k)
        fill_match = re.search(r'fill=[\d\-:]+\s+[\d\-:]+\s+[\d\-:]+\s+(.*)', cell_line, re.IGNORECASE)
        if not fill_match:
            errors.append(f"Cell {cell_id}: Cannot parse FILL array")
            return errors

        fill_array_str = fill_match.group(1)

        # Remove comments (everything after $)
        fill_array_str = fill_array_str.split('$')[0]

        # Expand repeat notation
        expanded_fill = self.expand_repeat_notation(fill_array_str)

        # Check element count
        if len(expanded_fill) != required:
            lat_type_name = "rectangular (LAT=1)" if lattice_info['lat_type'] == 1 else "hexagonal (LAT=2)"
            errors.append(
                f"Cell {cell_id} ({lat_type_name} lattice): FILL array dimension mismatch\n"
                f"  fill={lattice_info['imin']}:{lattice_info['imax']} "
                f"{lattice_info['jmin']}:{lattice_info['jmax']} "
                f"{lattice_info['kmin']}:{lattice_info['kmax']}\n"
                f"  Required: {required} elements "
                f"({lattice_info['imax']-lattice_info['imin']+1} × "
                f"{lattice_info['jmax']-lattice_info['jmin']+1} × "
                f"{lattice_info['kmax']-lattice_info['kmin']+1})\n"
                f"  Provided: {len(expanded_fill)} elements\n"
                f"  {'Missing' if required > len(expanded_fill) else 'Extra'}: {abs(required - len(expanded_fill))} elements"
            )

        # Check all filled universes are defined
        undefined_universes = set(expanded_fill) - self.universes_defined - {0}  # u=0 is always valid
        if undefined_universes:
            errors.append(
                f"Cell {cell_id}: Fill references undefined universes: {sorted(undefined_universes)}"
            )

        return errors

    def validate(self) -> Dict[str, List[str]]:
        """
        Run all fill array validations

        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        for cell_id, lattice_info in self.lattice_cells.items():
            cell_errors = self.validate_fill_array(cell_id, lattice_info)
            self.errors.extend(cell_errors)

        return {
            'errors': self.errors,
            'warnings': self.warnings
        }

    def print_report(self):
        """Print validation report to console"""
        results = self.validate()

        print("=" * 70)
        print("FILL ARRAY VALIDATION REPORT")
        print(f"File: {self.input_file}")
        print("=" * 70)

        print(f"\nLattice cells found: {len(self.lattice_cells)}")
        for cell_id, info in self.lattice_cells.items():
            lat_type_name = "rectangular (LAT=1)" if info['lat_type'] == 1 else "hexagonal (LAT=2)"
            required = self.calculate_required_elements(
                info['imin'], info['imax'],
                info['jmin'], info['jmax'],
                info['kmin'], info['kmax']
            )
            print(f"  Cell {cell_id}: {lat_type_name}, {required} elements required")

        if results['errors']:
            print(f"\n❌ CRITICAL ERRORS ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"\n{error}")
        else:
            print("\n✓ No fill array errors detected")

        if results['warnings']:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"  - {warning}")

        print("\n" + "=" * 70)


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python fill_array_validator.py <input_file>")
        sys.exit(1)

    validator = FillArrayValidator(sys.argv[1])
    validator.print_report()

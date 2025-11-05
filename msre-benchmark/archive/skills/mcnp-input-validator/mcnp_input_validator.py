"""MCNP Input Validator (Skill 12) - Pre-run syntax checking"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.input_parser import MCNPInputParser
from utils.geometry_evaluator import GeometryEvaluator

class MCNPInputValidator:
    def __init__(self):
        self.parser = MCNPInputParser()
        self.parsed = None
        self.errors = []
        self.warnings = []

    def validate_file(self, filepath: str) -> dict:
        """Validate MCNP input file (based on Chapters 3 & 4)"""
        self.errors = []
        self.warnings = []
        self.filepath = filepath

        # Try to parse the file - catch parsing errors
        try:
            self.parsed = self.parser.parse_file(filepath)
        except ValueError as e:
            # Parsing failed - add error and return invalid
            self.errors.append(f"PARSE ERROR: {str(e)}")
            return {
                'errors': self.errors,
                'warnings': self.warnings,
                'recommendations': [],
                'valid': False
            }
        except Exception as e:
            # Unexpected error
            self.errors.append(f"ERROR: {str(e)}")
            return {
                'errors': self.errors,
                'warnings': self.warnings,
                'recommendations': [],
                'valid': False
            }

        # Run all validation checks
        self._check_block_structure()
        self._check_continuation_formatting()
        self._check_cross_references()
        self._check_importance()
        self._check_materials()
        self._check_tallies()

        # Add recommendations
        recommendations = []
        if len(self.parsed['cells']) > 10:
            recommendations.append("RECOMMENDATION: Use geometry plotting to verify complex geometry")
        if not any(name.startswith('void') for name in self.parsed['data_cards'].keys()):
            recommendations.append("RECOMMENDATION: Test geometry with VOID card before production runs")

        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'recommendations': recommendations,
            'valid': len(self.errors) == 0
        }

    def _check_block_structure(self):
        """Check that required blocks exist"""
        if not self.parsed['cells']:
            self.errors.append("FATAL: No cell cards found")
        if not self.parsed['surfaces']:
            self.errors.append("FATAL: No surface cards found")
        if not self.parsed['data_cards']:
            self.warnings.append("No data cards found - using all defaults")

    def _check_continuation_formatting(self):
        """Check that continuation lines have proper indentation (5+ leading spaces)"""
        # Read raw file to check line-by-line formatting
        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except:
            return  # Skip check if file can't be read

        in_data_block = False
        blank_count = 0
        current_card_name = None

        for line_num, line in enumerate(lines, 1):
            # Remove inline comments for analysis
            if '$' in line:
                line_content = line[:line.index('$')]
            else:
                line_content = line

            # Track blank lines to identify data block (3rd block)
            if not line.strip():
                blank_count += 1
                current_card_name = None
                continue

            # Data block starts after 2nd blank line delimiter
            if blank_count >= 2:
                in_data_block = True

            if not in_data_block:
                continue

            # Skip comment lines
            if line.lstrip().startswith('c') or line.lstrip().startswith('C'):
                # Check if it's actually a comment (not just starts with 'c')
                stripped = line.lstrip()
                if len(stripped) > 1 and not stripped[1].isalnum():
                    continue

            # Check if this is a card name line or continuation
            if not line[0].isspace():
                # This is a new card (starts in column 1)
                # Extract card name for tracking
                card_name = line_content.split()[0] if line_content.split() else ""
                current_card_name = card_name.lower()
            else:
                # This is a continuation line (starts with spaces)
                # Count leading spaces
                leading_spaces = len(line) - len(line.lstrip())

                # Continuation lines MUST have at least 5 leading spaces (start at column 6)
                if leading_spaces < 5:
                    # Identify the card type for better error message
                    card_type = "data card"
                    if current_card_name:
                        if current_card_name.startswith('m') and current_card_name[1:].replace(':','').isdigit():
                            card_type = f"material card {current_card_name.upper()}"
                        elif current_card_name.startswith('f') and any(c.isdigit() for c in current_card_name):
                            card_type = f"tally card {current_card_name.upper()}"
                        elif current_card_name in ['sdef', 'kcode', 'ksrc', 'si', 'sp']:
                            card_type = f"{current_card_name.upper()} card"

                    self.errors.append(
                        f"FATAL: Line {line_num} ({card_type}): Continuation line has only "
                        f"{leading_spaces} leading spaces (need 5+, starting at column 6)"
                    )

    def _check_cross_references(self):
        """Check all surfaces referenced in cells exist"""
        geom_eval = GeometryEvaluator()
        defined_surfs = {s.number for s in self.parsed['surfaces']}
        for cell in self.parsed['cells']:
            # For lattice cells with fill arrays, extract only the geometry boundary
            # to avoid false positives from universe IDs in fill arrays
            geometry_to_check = self._extract_geometry_boundary(cell)

            referenced = geom_eval.get_all_surfaces(geometry_to_check)
            for surf in referenced:
                if surf not in defined_surfs:
                    self.errors.append(f"FATAL: Cell {cell.number} references undefined surface {surf}")

    def _extract_geometry_boundary(self, cell) -> str:
        """Extract geometry boundary from cell, excluding fill arrays for lattice cells"""
        # Check if this is a lattice cell (has LAT parameter)
        if hasattr(cell, 'parameters') and cell.parameters:
            is_lattice = 'LAT' in cell.parameters or 'lat' in {k.lower() for k in cell.parameters.keys()}
            has_fill = 'FILL' in cell.parameters or 'fill' in {k.lower() for k in cell.parameters.keys()}

            if is_lattice and has_fill:
                # This is a lattice cell with fill array
                # The geometry string contains: <boundary_surfaces> <fill_range> <universe_array>
                # We only want the boundary surfaces part

                # For lattice cells, geometry is typically simple (e.g., "-200")
                # followed by fill range (e.g., "-7:7 -7:7 0:0")
                # Split and take tokens that look like surface references

                import re
                tokens = cell.geometry.split()

                # Surface references: optional sign + digits (e.g., "-200", "100", "+50")
                # Fill range: digit:digit or -digit:digit (e.g., "-7:7", "0:0")
                # Universe IDs: just digits (e.g., "40", "50")

                boundary_tokens = []
                for token in tokens:
                    # Check if it's a surface reference (has + or - prefix, or is first token)
                    if ':' in token:
                        # This is fill range start (e.g., "-7:7") - stop here
                        break
                    elif token.startswith('-') or token.startswith('+'):
                        # Surface reference with sign
                        boundary_tokens.append(token)
                    elif not boundary_tokens:
                        # First token might be surface without sign
                        boundary_tokens.append(token)
                    elif re.match(r'^[a-zA-Z#]', token):
                        # Alphabetic token (like U=, IMP=, etc.) or # operator
                        boundary_tokens.append(token)
                    else:
                        # Bare number - could be fill range or universe ID
                        # If we've seen surface refs and now see bare numbers, stop
                        if boundary_tokens:
                            break

                return ' '.join(boundary_tokens)

        # Not a lattice with fill, or no parameters - return entire geometry
        return cell.geometry

    def _check_importance(self):
        """Check importance cards (Chapter 3 requirement)"""
        imp_cards = [name for name in self.parsed['data_cards'].keys() if name.startswith('imp')]
        if not imp_cards:
            self.warnings.append("No importance cards found - particles may get trapped")

        # Check for zero importance without escape
        for card_name, card in self.parsed['data_cards'].items():
            if card_name.startswith('imp'):
                has_zero = '0' in card.entries or 0 in card.entries
                if has_zero:
                    self.warnings.append(f"Zero importance found in {card_name} - ensure particles can escape")

    def _check_materials(self):
        """Check material specifications (Chapter 4)"""
        # Get all material numbers used in cells
        used_materials = {cell.material for cell in self.parsed['cells'] if cell.material > 0}

        # Get defined materials
        defined_materials = {int(name[1:]) for name in self.parsed['data_cards'].keys() if name.startswith('m') and name[1:].isdigit()}

        # Check for undefined materials
        undefined = used_materials - defined_materials
        for mat in undefined:
            self.errors.append(f"FATAL: Cell uses undefined material {mat}")

    def _check_tallies(self):
        """Check tally specifications (Chapter 4)"""
        tally_numbers = {}
        for card_name in self.parsed['data_cards'].keys():
            if card_name[0] == 'f' and card_name[1:].split(':')[0].isdigit():
                # Extract tally number and particle
                parts = card_name.split(':')
                tally_num = int(parts[0][1:])
                particle = parts[1] if len(parts) > 1 else ''

                # Check for conflicting tally numbers (F1:N and F1:P not allowed)
                if tally_num in tally_numbers:
                    self.errors.append(f"FATAL: Tally {tally_num} defined for multiple particles - not allowed")
                else:
                    tally_numbers[tally_num] = particle

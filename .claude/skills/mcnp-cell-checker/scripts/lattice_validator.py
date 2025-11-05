#!/usr/bin/env python3
"""
Lattice Validator

Validates lattice (lat=) specifications and fill array dimensions.
"""

import re


class LatticeValidator:
    """Validates lattice cells and fill arrays"""

    def validate_lattices(self, input_file):
        """
        Validate all lattice type specifications

        Args:
            input_file: Path to MCNP input file

        Returns:
            dict mapping cell_num to result dict with keys:
                - 'lat_type': 1 or 2
                - 'has_fill': bool
                - 'errors': list of error messages
        """
        results = {}

        with open(input_file, 'r') as f:
            lines = f.readlines()

        # Parse cell cards
        cell_cards = self._parse_cells(lines)

        for cell_num, cell_line in cell_cards.items():
            # Check for lat= parameter
            lat_match = re.search(r'\blat=(\d+)', cell_line, re.IGNORECASE)
            if not lat_match:
                continue

            lat_value = int(lat_match.group(1))
            errors = []

            # Validate LAT value (must be 1 or 2)
            if lat_value not in [1, 2]:
                errors.append(
                    f"Cell {cell_num}: Invalid LAT={lat_value} (must be 1 or 2)"
                )

            # Check for FILL parameter
            has_fill = bool(re.search(r'\bfill=', cell_line, re.IGNORECASE))
            if not has_fill:
                errors.append(
                    f"Cell {cell_num}: LAT specified without FILL "
                    "(lattice requires fill)"
                )

            # Check material (should be void)
            # Pattern: cell_num material density geometry...
            parts = cell_line.split()
            if len(parts) >= 2:
                try:
                    material = int(parts[1])
                    if material != 0:
                        errors.append(
                            f"Cell {cell_num}: Lattice cell must be void "
                            f"(has material {material})"
                        )
                except ValueError:
                    pass

            results[cell_num] = {
                'lat_type': lat_value,
                'has_fill': has_fill,
                'errors': errors
            }

        return results

    def check_fill_dimensions(self, input_file):
        """
        Validate fill array dimensions match lattice declaration

        Args:
            input_file: Path to MCNP input file

        Returns:
            dict mapping cell_num to result dict with keys:
                - 'declaration': str (fill= range specification)
                - 'expected_size': int
                - 'actual_size': int
        """
        results = {}

        with open(input_file, 'r') as f:
            lines = f.readlines()

        cell_cards = self._parse_cells(lines)

        for cell_num, cell_line in cell_cards.items():
            # Look for array fill pattern
            fill_match = re.search(
                r'fill=\s*(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)\s+([\d\s]+)',
                cell_line,
                re.IGNORECASE
            )

            if not fill_match:
                continue

            # Extract range
            i1, i2 = int(fill_match.group(1)), int(fill_match.group(2))
            j1, j2 = int(fill_match.group(3)), int(fill_match.group(4))
            k1, k2 = int(fill_match.group(5)), int(fill_match.group(6))

            # Calculate expected size
            i_size = i2 - i1 + 1
            j_size = j2 - j1 + 1
            k_size = k2 - k1 + 1
            expected_size = i_size * j_size * k_size

            # Count actual values
            universe_ids = fill_match.group(7).split()
            actual_size = len(universe_ids)

            results[cell_num] = {
                'declaration': f"fill= {i1}:{i2} {j1}:{j2} {k1}:{k2}",
                'expected_size': expected_size,
                'actual_size': actual_size
            }

        return results

    def check_lattice_boundaries(self, input_file):
        """
        Check lattice cells have appropriate boundary surfaces

        Args:
            input_file: Path to MCNP input file

        Returns:
            dict mapping cell_num to result dict with keys:
                - 'lat_type': 1 or 2
                - 'surfaces': list of surface numbers
                - 'appropriate': bool
                - 'recommendations': list of recommendation messages
        """
        results = {}

        with open(input_file, 'r') as f:
            lines = f.readlines()

        cell_cards = self._parse_cells(lines)

        for cell_num, cell_line in cell_cards.items():
            # Check for lat= parameter
            lat_match = re.search(r'\blat=(\d+)', cell_line, re.IGNORECASE)
            if not lat_match:
                continue

            lat_value = int(lat_match.group(1))

            # Extract surfaces (numbers between material/density and parameters)
            # Pattern: cell_num mat density [-]surf1 [-]surf2 ... params
            parts = cell_line.split()
            surfaces = []

            # Skip cell_num, material, density
            for part in parts[3:]:
                # Stop at first parameter (contains =)
                if '=' in part:
                    break
                # Extract surface number (with or without -)
                s_match = re.match(r'-?(\d+)', part)
                if s_match:
                    surfaces.append(int(s_match.group(1)))

            surface_count = len(surfaces)
            appropriate = False
            recommendations = []

            if lat_value == 1:
                # Cubic lattice: recommend 6 surfaces
                if surface_count >= 6:
                    appropriate = True
                else:
                    recommendations.append(
                        f"Cell {cell_num} (LAT=1): Recommend RPP macrobody or 6 planes "
                        f"(found {surface_count} surfaces)"
                    )

            elif lat_value == 2:
                # Hexagonal lattice: recommend 8 surfaces
                if surface_count >= 8:
                    appropriate = True
                else:
                    recommendations.append(
                        f"Cell {cell_num} (LAT=2): Recommend HEX macrobody or 8 surfaces "
                        f"(6 hex sides + 2 bases, found {surface_count} surfaces)"
                    )

            results[cell_num] = {
                'lat_type': lat_value,
                'surfaces': surfaces,
                'appropriate': appropriate,
                'recommendations': recommendations
            }

        return results

    def _parse_cells(self, lines):
        """Parse cell cards from input file lines"""
        cell_cards = {}

        # Find cell cards block
        in_cells = False
        cell_lines = []
        blank_count = 0

        for i, line in enumerate(lines):
            if i == 0:  # Skip title
                continue

            # Count blank lines
            if line.strip() == '':
                blank_count += 1
                if blank_count >= 1:  # End of cells block
                    break
                continue

            # In cells block
            in_cells = True
            cell_lines.append(line)

        # Parse cell cards
        current_cell = ""
        for line in cell_lines:
            # Skip comments
            if line.strip().startswith('c '):
                continue

            # Handle continuation
            if line.strip().endswith('&'):
                current_cell += line.strip()[:-1] + " "
                continue
            else:
                current_cell += line.strip()

            # Process complete cell card
            if current_cell:
                parts = current_cell.split()
                if parts:
                    try:
                        cell_num = int(parts[0])
                        cell_cards[cell_num] = current_cell
                    except ValueError:
                        pass
                current_cell = ""

        return cell_cards

#!/usr/bin/env python3
"""
Universe Validator

Validates universe definitions and references in MCNP cell cards.
"""

import re
from collections import defaultdict


class UniverseValidator:
    """Validates universe (u=) and fill (fill=) parameters"""

    def __init__(self):
        self.defined_universes = set()
        self.used_universes = set()

    def validate_universes(self, input_file):
        """
        Check all universe references are defined

        Args:
            input_file: Path to MCNP input file

        Returns:
            dict with keys:
                - 'defined': set of universe numbers with u= parameter
                - 'used': set of universe numbers referenced in fill=
                - 'undefined': set of used but not defined universe numbers
        """
        self.defined_universes = set()
        self.used_universes = set()

        with open(input_file, 'r') as f:
            lines = f.readlines()

        # Find cell cards block (between title and first blank line)
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
                self._parse_cell_card(current_cell)
                current_cell = ""

        # Check for undefined references
        undefined = self.used_universes - self.defined_universes

        return {
            'defined': self.defined_universes,
            'used': self.used_universes,
            'undefined': undefined
        }

    def _parse_cell_card(self, cell_line):
        """Extract universe information from cell card"""
        # Look for u= parameter
        u_match = re.search(r'\bu=(\d+)', cell_line, re.IGNORECASE)
        if u_match:
            u_num = int(u_match.group(1))
            self.defined_universes.add(u_num)

        # Look for fill= parameter
        fill_match = re.search(r'\bfill=([^\s]+)', cell_line, re.IGNORECASE)
        if fill_match:
            fill_str = fill_match.group(1)

            # Simple fill (single number)
            if fill_str.isdigit():
                self.used_universes.add(int(fill_str))
            else:
                # Array fill - extract all universe numbers after range spec
                # Pattern: fill= -7:7 -7:7 0:0 [universe IDs...]
                array_match = re.search(
                    r'fill=\s*-?\d+:-?\d+\s+-?\d+:-?\d+\s+-?\d+:-?\d+\s+([\d\s]+)',
                    cell_line,
                    re.IGNORECASE
                )
                if array_match:
                    universe_ids = array_match.group(1).split()
                    for uid in universe_ids:
                        if uid.isdigit():
                            self.used_universes.add(int(uid))

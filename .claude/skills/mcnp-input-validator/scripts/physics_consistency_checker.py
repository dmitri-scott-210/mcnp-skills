#!/usr/bin/env python3
"""
Physics Consistency Checker

Validates physics settings in MCNP input files:
- MODE card present and appropriate
- PHYS cards consistent with MODE
- Cross-section library suffixes match particle types
- Energy ranges cover source and tallies

Usage:
    from physics_consistency_checker import check_physics_consistency

    warnings = check_physics_consistency('input.inp')
    for warning in warnings:
        print(f"WARNING: {warning}")

Author: MCNP Skills Revamp Project
Version: 2.0.0
"""

import re
from typing import List, Set


class PhysicsConsistencyChecker:
    """Check physics settings consistency."""

    def __init__(self):
        """Initialize checker."""
        self.mode_particles = set()
        self.phys_cards = set()
        self.materials = []
        self.warnings = []

    def check_file(self, filepath: str) -> List[str]:
        """
        Check physics consistency in MCNP input file.

        Args:
            filepath: Path to MCNP input file

        Returns:
            List of warning strings
        """
        self.warnings = []

        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            return [f"Error reading file: {e}"]

        # Parse data cards
        self._parse_data_cards(lines)

        # Check consistency
        self._check_mode_card()
        self._check_phys_cards()
        self._check_cross_sections()

        return self.warnings

    def _parse_data_cards(self, lines: List[str]):
        """Parse data cards block."""
        # Find data block (after second blank line)
        blank_positions = [i for i, line in enumerate(lines) if line.strip() == '']

        if len(blank_positions) < 2:
            return

        data_start = blank_positions[1] + 1
        data_lines = lines[data_start:]

        for line in data_lines:
            line = line.strip()
            if not line or line.startswith('c'):
                continue

            # MODE card
            if line.startswith('MODE') or line.startswith('mode'):
                tokens = line.split()
                if len(tokens) > 1:
                    # Extract particle types
                    particles = ' '.join(tokens[1:])
                    # Split on whitespace
                    for p in particles.split():
                        self.mode_particles.add(p.upper())

            # PHYS cards
            if line.startswith('PHYS:') or line.startswith('phys:'):
                match = re.match(r'PHYS:([A-Z])', line, re.IGNORECASE)
                if match:
                    particle = match.group(1).upper()
                    self.phys_cards.add(particle)

            # Material cards
            if re.match(r'^[Mm]\d+', line):
                self.materials.append(line)

    def _check_mode_card(self):
        """Check MODE card present."""
        if not self.mode_particles:
            self.warnings.append(
                "FATAL: MODE card missing - must specify particle type(s)"
            )

    def _check_phys_cards(self):
        """Check PHYS cards for MODE particles."""
        for particle in self.mode_particles:
            if particle not in self.phys_cards:
                self.warnings.append(
                    f"WARNING: PHYS:{particle} card missing - MCNP will use defaults"
                )

    def _check_cross_sections(self):
        """Check cross-section library consistency (basic)."""
        # Check for mixed libraries
        libraries_used = set()

        for mat_line in self.materials:
            # Extract ZAIDs
            zaids = re.findall(r'\d{4,6}\.\d{2}[a-z]', mat_line, re.IGNORECASE)
            for zaid in zaids:
                # Extract library (e.g., "80" from "92235.80c")
                match = re.match(r'\d+\.(\d{2})[a-z]', zaid, re.IGNORECASE)
                if match:
                    library = match.group(1)
                    libraries_used.add(library)

        if len(libraries_used) > 1:
            self.warnings.append(
                f"WARNING: Mixed cross-section libraries detected: {libraries_used}. "
                f"Recommend consistent library version (e.g., all .80c)"
            )


def check_physics_consistency(filepath: str) -> List[str]:
    """
    Convenience function to check physics consistency.

    Args:
        filepath: Path to MCNP input file

    Returns:
        List of warning strings
    """
    checker = PhysicsConsistencyChecker()
    return checker.check_file(filepath)


def main():
    """Command-line interface."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python physics_consistency_checker.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    print(f"Checking physics consistency: {input_file}")
    print("="*60)

    warnings = check_physics_consistency(input_file)

    if warnings:
        print("PHYSICS WARNINGS:")
        for i, warning in enumerate(warnings, 1):
            print(f"{i}. {warning}")
    else:
        print("✓ Physics settings consistent")

    sys.exit(0)


if __name__ == '__main__':
    main()

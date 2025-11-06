#!/usr/bin/env python3
"""
MCNP Unit Checker - Validate unit consistency in MCNP input files

Scans MCNP input files to identify potential unit errors and inconsistencies.
Checks material densities, source energies, geometry dimensions, and other parameters
for proper unit conventions.

Usage:
    python mcnp_unit_checker.py input.i                   # Check single file
    python mcnp_unit_checker.py input.i --fix             # Suggest fixes
    python mcnp_unit_checker.py input.i --report=report.txt  # Save report

Author: MCNP Skills Project
License: MIT
"""

import sys
import argparse
import re
from pathlib import Path

class MCNPUnitChecker:
    """Check MCNP input files for unit consistency"""

    def __init__(self, filename):
        self.filename = filename
        self.issues = []
        self.warnings = []
        self.suggestions = []
        self.line_number = 0

        # Expected unit ranges
        self.ranges = {
            'density_g_cm3': (0.001, 25.0),      # g/cm³ (air to osmium)
            'density_atom_b_cm': (0.0001, 0.15), # atom/b-cm
            'energy_MeV': (1e-11, 100.0),        # MeV (thermal to high energy)
            'length_cm': (1e-10, 1e6),           # cm (Angstrom to km)
            'temperature_K': (0.1, 10000),       # Kelvin
            'activity_Bq': (1e-10, 1e15),        # Becquerel
        }

    def check_file(self):
        """Main checking routine"""
        print(f"\nChecking MCNP input file: {self.filename}")
        print("=" * 70)

        if not Path(self.filename).exists():
            print(f"ERROR: File not found: {self.filename}")
            return False

        try:
            with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"ERROR: Could not read file: {e}")
            return False

        # Parse file by blocks
        cell_block, surface_block, data_block = self._split_blocks(lines)

        # Check each block
        self._check_cell_cards(cell_block)
        self._check_data_cards(data_block)

        # Print results
        self._print_results()

        return len(self.issues) == 0

    def _split_blocks(self, lines):
        """Split MCNP input into cell, surface, and data blocks"""
        cell_block = []
        surface_block = []
        data_block = []

        current_block = 'cell'
        blank_count = 0

        for line_num, line in enumerate(lines, 1):
            # Skip title card (first line)
            if line_num == 1:
                continue

            # Remove comments
            if '$' in line:
                line = line.split('$')[0]

            # Check for blank line (block separator)
            if line.strip() == '':
                blank_count += 1
                if blank_count == 1:
                    current_block = 'surface'
                elif blank_count == 2:
                    current_block = 'data'
                continue

            # Store line with line number
            if current_block == 'cell':
                cell_block.append((line_num, line))
            elif current_block == 'surface':
                surface_block.append((line_num, line))
            elif current_block == 'data':
                data_block.append((line_num, line))

        return cell_block, surface_block, data_block

    def _check_cell_cards(self, cell_block):
        """Check cell cards for density issues"""
        for line_num, line in cell_block:
            self.line_number = line_num

            # Skip comment lines
            if line.strip().startswith('c ') or line.strip().startswith('C '):
                continue

            # Parse cell card: cell_num mat_num density geom
            parts = line.split()
            if len(parts) < 3:
                continue

            try:
                cell_num = int(parts[0])
                mat_num = int(parts[1])
                density = float(parts[2])
            except ValueError:
                continue

            # Check density
            if mat_num > 0:  # Not void
                if density > 0:
                    # Positive density → atom/b-cm
                    self._check_atomic_density(density, line_num)
                elif density < 0:
                    # Negative density → g/cm³
                    self._check_mass_density(-density, line_num)

    def _check_atomic_density(self, density, line_num):
        """Check atomic density (atom/b-cm) for reasonableness"""
        min_val, max_val = self.ranges['density_atom_b_cm']

        if density < min_val:
            self.warnings.append({
                'line': line_num,
                'type': 'Low atomic density',
                'value': density,
                'message': f'Atomic density {density:.6f} atom/b-cm is very low (< {min_val}). Verify units.'
            })

        if density > max_val:
            self.issues.append({
                'line': line_num,
                'type': 'High atomic density',
                'value': density,
                'message': f'Atomic density {density:.6f} atom/b-cm is too high (> {max_val}). Possible unit error?',
                'suggestion': f'If you meant {density:.2f} g/cm³, use negative sign: -{density:.2f}'
            })

    def _check_mass_density(self, density, line_num):
        """Check mass density (g/cm³) for reasonableness"""
        min_val, max_val = self.ranges['density_g_cm3']

        if density < min_val:
            self.warnings.append({
                'line': line_num,
                'type': 'Low mass density',
                'value': density,
                'message': f'Mass density {density:.6f} g/cm³ is very low (< {min_val}). Verify material.'
            })

        if density > max_val:
            self.issues.append({
                'line': line_num,
                'type': 'High mass density',
                'value': density,
                'message': f'Mass density {density:.2f} g/cm³ exceeds osmium density (~22.6). Possible error.',
                'suggestion': 'Check if density should be in kg/m³ (divide by 1000) or atom/b-cm (use positive)'
            })

    def _check_data_cards(self, data_block):
        """Check data cards for energy, temperature, and other unit issues"""
        current_card = None
        card_lines = []

        for line_num, line in data_block:
            self.line_number = line_num

            # Check if this starts a new card
            line_stripped = line.strip()
            if line_stripped and not line[0].isspace():
                # Process previous card if exists
                if current_card:
                    self._check_card(current_card, card_lines)

                # Start new card
                current_card = line_stripped.split()[0].upper()
                card_lines = [(line_num, line)]
            else:
                # Continuation of current card
                if current_card:
                    card_lines.append((line_num, line))

        # Process last card
        if current_card:
            self._check_card(current_card, card_lines)

    def _check_card(self, card_name, card_lines):
        """Check specific card types"""
        # Material cards
        if card_name.startswith('M') and card_name[1:].isdigit():
            self._check_material_card(card_name, card_lines)

        # Source cards
        elif card_name == 'SDEF':
            self._check_sdef_card(card_lines)

        # Energy distribution cards
        elif card_name.startswith('SI') or card_name.startswith('SP'):
            self._check_energy_distribution(card_lines)

        # Temperature card
        elif card_name == 'TMP':
            self._check_tmp_card(card_lines)

        # Time binning
        elif card_name.startswith('T') and len(card_name) > 1:
            self._check_time_bins(card_lines)

        # Energy binning
        elif card_name.startswith('E') and len(card_name) > 1:
            self._check_energy_bins(card_lines)

    def _check_material_card(self, card_name, card_lines):
        """Check material card format"""
        # Combine continuation lines
        full_text = ' '.join([line for _, line in card_lines])

        # Extract ZAIDs and fractions
        # Format: ZAID fraction ZAID fraction ...
        tokens = full_text.split()
        if len(tokens) < 3:  # card name + at least one ZAID + fraction
            return

        # Check fractions
        i = 1
        while i < len(tokens) - 1:
            try:
                zaid = tokens[i]
                fraction = float(tokens[i + 1])

                # Check if fraction is reasonable
                if fraction > 0:
                    # Atom fraction
                    if fraction > 1.0:
                        self.warnings.append({
                            'line': card_lines[0][0],
                            'type': 'Large atom fraction',
                            'value': fraction,
                            'message': f'{card_name}: Atom fraction {fraction:.3f} for {zaid} is > 1.0'
                        })
                elif fraction < 0:
                    # Weight fraction
                    if fraction < -1.0:
                        self.warnings.append({
                            'line': card_lines[0][0],
                            'type': 'Large weight fraction',
                            'value': fraction,
                            'message': f'{card_name}: Weight fraction {fraction:.3f} for {zaid} has magnitude > 1.0'
                        })

                i += 2
            except (ValueError, IndexError):
                break

    def _check_sdef_card(self, card_lines):
        """Check SDEF card for energy units"""
        full_text = ' '.join([line for _, line in card_lines])
        line_num = card_lines[0][0]

        # Check for ERG parameter
        erg_match = re.search(r'ERG\s*=\s*([\d.Ee+-]+)', full_text, re.IGNORECASE)
        if erg_match:
            energy = float(erg_match.group(1))

            # Check if energy is in reasonable MeV range
            min_energy, max_energy = self.ranges['energy_MeV']

            if energy < min_energy:
                self.issues.append({
                    'line': line_num,
                    'type': 'Very low energy',
                    'value': energy,
                    'message': f'SDEF ERG={energy:.2e} MeV is very low. Check units.',
                    'suggestion': f'If energy is in eV, convert: ERG={energy * 1e-6:.6g} (MeV)'
                })

            if energy > max_energy:
                self.warnings.append({
                    'line': line_num,
                    'type': 'Very high energy',
                    'value': energy,
                    'message': f'SDEF ERG={energy:.2f} MeV is very high. Verify.'
                })

            # Check for common keV error
            if 1 < energy < 1000 and energy % 1 > 0.01:
                self.suggestions.append({
                    'line': line_num,
                    'type': 'Possible keV units',
                    'value': energy,
                    'message': f'SDEF ERG={energy:.3f} might be in keV? If so: ERG={energy/1000:.6g}'
                })

    def _check_energy_distribution(self, card_lines):
        """Check energy distribution for unit consistency"""
        full_text = ' '.join([line for _, line in card_lines])
        line_num = card_lines[0][0]

        # Extract numbers from distribution
        numbers = re.findall(r'[\d.Ee+-]+', full_text)
        if len(numbers) < 2:
            return

        energies = [float(n) for n in numbers[1:]]  # Skip card number

        # Check range
        for energy in energies:
            if energy > 1000:
                self.suggestions.append({
                    'line': line_num,
                    'type': 'Large energy value',
                    'value': energy,
                    'message': f'Energy {energy:.1f} in distribution. If in keV, divide by 1000.'
                })
                break  # Only warn once per card

    def _check_tmp_card(self, card_lines):
        """Check TMP card for temperature units"""
        full_text = ' '.join([line for _, line in card_lines])
        line_num = card_lines[0][0]

        # Extract temperature values
        numbers = re.findall(r'[\d.Ee+-]+', full_text)
        if not numbers:
            return

        for temp_str in numbers:
            temp = float(temp_str)

            # TMP accepts both K and MeV
            # Kelvin: typically 1-10000
            # MeV: typically 1e-11 to 1e-6

            if temp > 10000:
                self.issues.append({
                    'line': line_num,
                    'type': 'Very high temperature',
                    'value': temp,
                    'message': f'TMP={temp:.2e} is very high. If in Celsius, convert to Kelvin (+273.15).'
                })

            elif temp < 1e-15:
                self.warnings.append({
                    'line': line_num,
                    'type': 'Very low temperature',
                    'value': temp,
                    'message': f'TMP={temp:.2e} is very low. Verify units.'
                })

    def _check_time_bins(self, card_lines):
        """Check time bins (might be in wrong units)"""
        card_name = card_lines[0][1].split()[0].upper()
        full_text = ' '.join([line for _, line in card_lines])
        line_num = card_lines[0][0]

        # Extract time values
        numbers = re.findall(r'[\d.Ee+-]+', full_text)
        if len(numbers) < 2:
            return

        times = [float(n) for n in numbers]

        # MCNP expects shakes (1e-8 s)
        # Check if user might have used seconds
        max_time = max(times)
        if max_time < 1.0:
            self.suggestions.append({
                'line': line_num,
                'type': 'Possible time unit error',
                'value': max_time,
                'message': f'{card_name}: Max time {max_time:.3e} shakes is < 1 shake. If in seconds, multiply by 1e8.'
            })

    def _check_energy_bins(self, card_lines):
        """Check energy bins for unit errors"""
        card_name = card_lines[0][1].split()[0].upper()
        full_text = ' '.join([line for _, line in card_lines])
        line_num = card_lines[0][0]

        # Extract energy values
        numbers = re.findall(r'[\d.Ee+-]+', full_text)
        if len(numbers) < 2:
            return

        # Skip card number
        energies = [float(n) for n in numbers if float(n) > 0.001]

        if not energies:
            return

        # Check for keV instead of MeV
        max_energy = max(energies)
        if 10 < max_energy < 10000:
            self.suggestions.append({
                'line': line_num,
                'type': 'Possible keV units',
                'value': max_energy,
                'message': f'{card_name}: Max energy {max_energy:.1f}. If in keV, divide by 1000 for MeV.'
            })

    def _print_results(self):
        """Print all issues, warnings, and suggestions"""
        print()

        # Issues (errors)
        if self.issues:
            print("ISSUES (likely errors):")
            print("-" * 70)
            for issue in self.issues:
                print(f"  Line {issue['line']}: {issue['type']}")
                print(f"    {issue['message']}")
                if 'suggestion' in issue:
                    print(f"    → Suggestion: {issue['suggestion']}")
                print()
        else:
            print("✓ No critical issues found")

        # Warnings
        if self.warnings:
            print("\nWARNINGS (verify these):")
            print("-" * 70)
            for warning in self.warnings:
                print(f"  Line {warning['line']}: {warning['type']}")
                print(f"    {warning['message']}")
                print()

        # Suggestions
        if self.suggestions:
            print("\nSUGGESTIONS (potential improvements):")
            print("-" * 70)
            for suggestion in self.suggestions:
                print(f"  Line {suggestion['line']}: {suggestion['type']}")
                print(f"    {suggestion['message']}")
                print()

        # Summary
        print("=" * 70)
        print(f"Summary: {len(self.issues)} issues, {len(self.warnings)} warnings, {len(self.suggestions)} suggestions")
        print("=" * 70)

    def save_report(self, report_file):
        """Save checking results to file"""
        with open(report_file, 'w') as f:
            f.write(f"MCNP Unit Checker Report\n")
            f.write(f"File: {self.filename}\n")
            f.write("=" * 70 + "\n\n")

            if self.issues:
                f.write("ISSUES:\n")
                for issue in self.issues:
                    f.write(f"  Line {issue['line']}: {issue['type']}\n")
                    f.write(f"    {issue['message']}\n")
                    if 'suggestion' in issue:
                        f.write(f"    → {issue['suggestion']}\n")
                    f.write("\n")

            if self.warnings:
                f.write("\nWARNINGS:\n")
                for warning in self.warnings:
                    f.write(f"  Line {warning['line']}: {warning['type']}\n")
                    f.write(f"    {warning['message']}\n\n")

            if self.suggestions:
                f.write("\nSUGGESTIONS:\n")
                for suggestion in self.suggestions:
                    f.write(f"  Line {suggestion['line']}: {suggestion['type']}\n")
                    f.write(f"    {suggestion['message']}\n\n")

            f.write("=" * 70 + "\n")
            f.write(f"Summary: {len(self.issues)} issues, {len(self.warnings)} warnings, {len(self.suggestions)} suggestions\n")

        print(f"\nReport saved to: {report_file}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='MCNP Unit Checker - Validate unit consistency in MCNP input files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python mcnp_unit_checker.py input.i                      # Check file
    python mcnp_unit_checker.py input.i --report=report.txt  # Save report
    python mcnp_unit_checker.py *.i                          # Check multiple files

Common issues detected:
    - Density in wrong units (kg/m³ instead of g/cm³)
    - Energy in keV instead of MeV
    - Temperature in Celsius instead of Kelvin
    - Time in seconds instead of shakes
    - Material fractions > 1.0

For MCNP unit conventions, see SKILL.md
        """
    )

    parser.add_argument('files', nargs='+', help='MCNP input file(s) to check')
    parser.add_argument('--report', help='Save report to file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    all_passed = True

    for filename in args.files:
        checker = MCNPUnitChecker(filename)
        passed = checker.check_file()

        if args.report:
            report_name = args.report if len(args.files) == 1 else f"{Path(filename).stem}_report.txt"
            checker.save_report(report_name)

        if not passed:
            all_passed = False

        if len(args.files) > 1:
            print()  # Blank line between files

    # Exit code
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()

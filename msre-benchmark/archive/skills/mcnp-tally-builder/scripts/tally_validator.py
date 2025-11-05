#!/usr/bin/env python3
"""
MCNP Tally Validator

Validates tally card specifications in MCNP input files to catch common errors
before running expensive simulations.

Usage:
    python tally_validator.py input.i
    python tally_validator.py input.i --verbose

Author: MCNP Skills Project
License: MIT
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set


class TallyValidator:
    """Validates MCNP tally specifications."""
    
    def __init__(self, input_file: str):
        self.input_file = Path(input_file)
        self.errors = []
        self.warnings = []
        self.cells = set()
        self.surfaces = set()
        self.materials = {}
        self.tallies = {}
        
    def validate(self) -> bool:
        """Run all validation checks. Returns True if no errors found."""
        if not self.input_file.exists():
            self.errors.append(f"Input file not found: {self.input_file}")
            return False
            
        try:
            self._parse_input()
            self._validate_tally_references()
            self._validate_energy_bins()
            self._validate_fm_cards()
            self._validate_dedf_cards()
            self._validate_fs_sd_cards()
            self._validate_tally_numbers()
            return len(self.errors) == 0
        except Exception as e:
            self.errors.append(f"Validation error: {str(e)}")
            return False
    
    def _parse_input(self):
        """Parse MCNP input file to extract cells, surfaces, materials, tallies."""
        content = self.input_file.read_text()
        lines = content.split('\n')
        
        # Find block boundaries
        blank_count = 0
        cell_block = []
        surface_block = []
        data_block = []
        current_block = cell_block
        
        for i, line in enumerate(lines[1:], start=2):  # Skip title
            if line.strip() == '':
                blank_count += 1
                if blank_count == 1:
                    current_block = surface_block
                elif blank_count == 2:
                    current_block = data_block
                continue
            current_block.append((i, line))
        
        # Parse cells
        for line_num, line in cell_block:
            if line.strip().startswith('c'):
                continue
            match = re.match(r'^\s*(\d+)', line)
            if match:
                self.cells.add(int(match.group(1)))
        
        # Parse surfaces
        for line_num, line in surface_block:
            if line.strip().startswith('c'):
                continue
            match = re.match(r'^\s*\*?(\d+)', line)
            if match:
                self.surfaces.add(int(match.group(1)))
        
        # Parse data cards
        current_card = None
        for line_num, line in data_block:
            stripped = line.strip()
            if not stripped or stripped.startswith('c'):
                continue
                
            # Check if new card (starts with letter or special character)
            if re.match(r'^[a-zA-Z*+]', stripped):
                # Material cards
                if re.match(r'^m(\d+)', stripped, re.IGNORECASE):
                    match = re.match(r'^m(\d+)', stripped, re.IGNORECASE)
                    mat_num = int(match.group(1))
                    self.materials[mat_num] = line_num
                
                # Tally cards (F, E, T, C, FM, etc.)
                elif re.match(r'^[*+]?f(\d+):', stripped, re.IGNORECASE):
                    match = re.match(r'^([*+]?)f(\d+):([npe])', stripped, re.IGNORECASE)
                    if match:
                        flag = match.group(1)
                        tally_num = int(match.group(2))
                        particle = match.group(3).lower()
                        self.tallies[tally_num] = {
                            'line': line_num,
                            'flag': flag,
                            'particle': particle,
                            'content': stripped
                        }
                        current_card = ('F', tally_num)
                
                elif re.match(r'^e(\d+)', stripped, re.IGNORECASE):
                    match = re.match(r'^e(\d+)', stripped, re.IGNORECASE)
                    tally_num = int(match.group(1))
                    if tally_num in self.tallies:
                        self.tallies[tally_num]['E_card'] = (line_num, stripped)
                
                elif re.match(r'^fm(\d+)', stripped, re.IGNORECASE):
                    match = re.match(r'^fm(\d+)', stripped, re.IGNORECASE)
                    tally_num = int(match.group(1))
                    if tally_num in self.tallies:
                        self.tallies[tally_num]['FM_card'] = (line_num, stripped)
                
                elif re.match(r'^de(\d+)', stripped, re.IGNORECASE):
                    match = re.match(r'^de(\d+)', stripped, re.IGNORECASE)
                    tally_num = int(match.group(1))
                    if tally_num in self.tallies:
                        self.tallies[tally_num]['DE_card'] = (line_num, stripped)
                
                elif re.match(r'^df(\d+)', stripped, re.IGNORECASE):
                    match = re.match(r'^df(\d+)', stripped, re.IGNORECASE)
                    tally_num = int(match.group(1))
                    if tally_num in self.tallies:
                        self.tallies[tally_num]['DF_card'] = (line_num, stripped)
                
                elif re.match(r'^fs(\d+)', stripped, re.IGNORECASE):
                    match = re.match(r'^fs(\d+)', stripped, re.IGNORECASE)
                    tally_num = int(match.group(1))
                    if tally_num in self.tallies:
                        self.tallies[tally_num]['FS_card'] = (line_num, stripped)
                
                elif re.match(r'^sd(\d+)', stripped, re.IGNORECASE):
                    match = re.match(r'^sd(\d+)', stripped, re.IGNORECASE)
                    tally_num = int(match.group(1))
                    if tally_num in self.tallies:
                        self.tallies[tally_num]['SD_card'] = (line_num, stripped)
    
    def _validate_tally_references(self):
        """Check that tallies reference valid cells/surfaces."""
        for tally_num, info in self.tallies.items():
            content = info['content']
            tally_type = tally_num % 10
            
            # Extract cell/surface numbers from tally specification
            parts = content.split()
            if len(parts) < 2:
                continue
                
            # Parse cell/surface list (after particle type)
            references = []
            for part in parts[1:]:
                if re.match(r'^-?\d+$', part):
                    references.append(int(part))
            
            # Validate based on tally type
            if tally_type in [1, 2]:  # Surface tallies
                for surf_num in references:
                    abs_surf = abs(surf_num)
                    if abs_surf not in self.surfaces:
                        self.errors.append(
                            f"Line {info['line']}: F{tally_num} references "
                            f"non-existent surface {surf_num}"
                        )
            elif tally_type in [4, 6, 7]:  # Cell tallies
                for cell_num in references:
                    if cell_num not in self.cells and cell_num > 0:
                        self.errors.append(
                            f"Line {info['line']}: F{tally_num} references "
                            f"non-existent cell {cell_num}"
                        )
    
    def _validate_energy_bins(self):
        """Check that energy bins are monotonically increasing."""
        for tally_num, info in self.tallies.items():
            if 'E_card' not in info:
                continue
                
            line_num, content = info['E_card']
            parts = content.split()[1:]  # Skip E# label
            
            energies = []
            for part in parts:
                if part.upper() in ['NT', 'C']:
                    continue
                try:
                    energies.append(float(part))
                except ValueError:
                    continue
            
            # Check monotonically increasing
            for i in range(1, len(energies)):
                if energies[i] <= energies[i-1]:
                    self.errors.append(
                        f"Line {line_num}: E{tally_num} energy bins not "
                        f"monotonically increasing: {energies[i-1]} >= {energies[i]}"
                    )
                    break
    
    def _validate_fm_cards(self):
        """Check that FM multiplier cards reference valid materials."""
        for tally_num, info in self.tallies.items():
            if 'FM_card' not in info:
                continue
                
            line_num, content = info['FM_card']
            parts = content.split()[1:]  # Skip FM# label
            
            # FM format: (multiplier material_num reaction_num) repeating
            i = 0
            while i < len(parts):
                if i + 1 >= len(parts):
                    break
                try:
                    mat_num = int(float(parts[i+1]))
                    if mat_num > 0 and mat_num not in self.materials:
                        self.warnings.append(
                            f"Line {line_num}: FM{tally_num} references "
                            f"material M{mat_num} which is not defined"
                        )
                except (ValueError, IndexError):
                    pass
                i += 3  # Skip to next triplet
    
    def _validate_dedf_cards(self):
        """Check that DE and DF cards have matching entry counts."""
        for tally_num, info in self.tallies.items():
            has_de = 'DE_card' in info
            has_df = 'DF_card' in info
            
            if has_de and not has_df:
                self.warnings.append(
                    f"Tally F{tally_num}: Has DE{tally_num} but no DF{tally_num}"
                )
            elif has_df and not has_de:
                self.warnings.append(
                    f"Tally F{tally_num}: Has DF{tally_num} but no DE{tally_num}"
                )
            elif has_de and has_df:
                de_line, de_content = info['DE_card']
                df_line, df_content = info['DF_card']
                
                de_entries = len([p for p in de_content.split()[1:] 
                                 if p.upper() not in ['LIN', 'LOG']])
                df_entries = len([p for p in df_content.split()[1:] 
                                 if p.upper() not in ['LIN', 'LOG']])
                
                if de_entries != df_entries:
                    self.errors.append(
                        f"Tally F{tally_num}: DE{tally_num} has {de_entries} entries "
                        f"but DF{tally_num} has {df_entries} entries (must match)"
                    )
    
    def _validate_fs_sd_cards(self):
        """Check that FS and SD cards have compatible entry counts."""
        for tally_num, info in self.tallies.items():
            if 'FS_card' in info and 'SD_card' in info:
                fs_line, fs_content = info['FS_card']
                sd_line, sd_content = info['SD_card']
                
                # Count segments in FS (surfaces listed)
                fs_parts = fs_content.split()[1:]
                fs_segments = len([p for p in fs_parts if re.match(r'^-?\d+$', p)])
                
                # Count divisors in SD
                sd_parts = sd_content.split()[1:]
                sd_divisors = len([p for p in sd_parts if p != '1'])
                
                # SD should have segments+1 entries (one per segment plus total)
                expected = fs_segments + 1
                if len(sd_parts) != expected:
                    self.warnings.append(
                        f"Tally F{tally_num}: FS{tally_num} creates {fs_segments} segments "
                        f"but SD{tally_num} has {len(sd_parts)} entries (expected {expected})"
                    )
    
    def _validate_tally_numbers(self):
        """Check tally numbering conventions."""
        for tally_num in self.tallies.keys():
            if tally_num > 99999999:
                self.errors.append(
                    f"Tally F{tally_num} exceeds maximum tally number (99,999,999)"
                )
            
            # Check increment of 10 warning
            if tally_num % 10 == 0:
                self.warnings.append(
                    f"Tally F{tally_num} uses tally number ending in 0 "
                    f"(MCNP uses last digit for tally type)"
                )
    
    def report(self, verbose: bool = False):
        """Print validation report."""
        print(f"\n{'='*70}")
        print(f"MCNP Tally Validation Report: {self.input_file.name}")
        print(f"{'='*70}\n")
        
        print(f"Parsed: {len(self.cells)} cells, {len(self.surfaces)} surfaces, "
              f"{len(self.materials)} materials, {len(self.tallies)} tallies\n")
        
        if verbose:
            print(f"Tallies found: {', '.join(f'F{n}' for n in sorted(self.tallies.keys()))}\n")
        
        if self.errors:
            print(f"ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  ❌ {error}")
            print()
        else:
            print("✅ No errors found\n")
        
        if self.warnings:
            print(f"WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")
            print()
        
        if not self.errors and not self.warnings:
            print("✅ All tally validations passed!")
        
        print(f"{'='*70}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python tally_validator.py input.i [--verbose]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    verbose = '--verbose' in sys.argv
    
    validator = TallyValidator(input_file)
    success = validator.validate()
    validator.report(verbose=verbose)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

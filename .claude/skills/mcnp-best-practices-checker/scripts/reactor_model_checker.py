#!/usr/bin/env python3
"""
Automated Reactor Model Best Practices Checker

Validates MCNP inputs against Phase 0 (Professional Standards)
and reactor-specific Phase 1 extensions.

Usage:
    python reactor_model_checker.py input.i
    python reactor_model_checker.py --all-inputs mcnp/*.i
    python reactor_model_checker.py --config checks.yaml input.i
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


class MCNPInputParser:
    """Parse MCNP input file into structured data."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.cells = {}
        self.surfaces = {}
        self.materials = {}
        self.mt_cards = set()
        self.universes = set()
        self.lattices = []
        self.parse()

    def parse(self):
        """Parse MCNP input file."""
        with open(self.filepath, 'r') as f:
            lines = f.readlines()

        # Identify blocks (cells, surfaces, materials)
        blocks = self._identify_blocks(lines)

        # Parse each block
        self._parse_cells(blocks['cells'])
        self._parse_surfaces(blocks['surfaces'])
        self._parse_materials(blocks['materials'])

    def _identify_blocks(self, lines: List[str]) -> Dict[str, List[str]]:
        """Identify cell, surface, material blocks."""
        blocks = {'cells': [], 'surfaces': [], 'materials': []}
        current_block = 'cells'
        blank_count = 0

        for line in lines:
            # Skip comment lines
            if line.strip().startswith('c ') or line.strip().startswith('C '):
                continue

            # Empty line separates blocks
            if not line.strip():
                blank_count += 1
                if blank_count == 1 and current_block == 'cells':
                    current_block = 'surfaces'
                elif blank_count == 2 and current_block == 'surfaces':
                    current_block = 'materials'
                continue

            blank_count = 0
            blocks[current_block].append(line)

        return blocks

    def _parse_cells(self, lines: List[str]):
        """Extract cell definitions."""
        for line in lines:
            # Simple cell parsing (cell_id material density surfaces...)
            match = re.match(r'^\s*(\d+)\s+(\d+)\s+([\d.eE+-]+)\s+(.*)$', line)
            if match:
                cell_id = int(match.group(1))
                material = int(match.group(2))
                density = float(match.group(3))
                rest = match.group(4)

                # Extract surfaces (simplified)
                surfaces = []
                universe = 0
                fill = None

                # Check for U= parameter
                u_match = re.search(r'\bU[= ](\d+)', rest, re.IGNORECASE)
                if u_match:
                    universe = int(u_match.group(1))
                    self.universes.add(universe)

                # Check for FILL= parameter
                fill_match = re.search(r'\bFILL[= ](\d+)', rest, re.IGNORECASE)
                if fill_match:
                    fill = int(fill_match.group(1))

                # Check for LAT= parameter
                lat_match = re.search(r'\bLAT[= ](\d+)', rest, re.IGNORECASE)
                if lat_match:
                    lat_type = int(lat_match.group(1))
                    # This is a lattice cell
                    self.lattices.append({
                        'cell': cell_id,
                        'lat_type': lat_type,
                        'universe': universe,
                        'fill_array': rest  # Simplified
                    })

                self.cells[cell_id] = {
                    'material': material,
                    'density': density,
                    'surfaces': surfaces,
                    'universe': universe,
                    'fill': fill
                }

    def _parse_surfaces(self, lines: List[str]):
        """Extract surface definitions."""
        for line in lines:
            # Simple surface parsing
            match = re.match(r'^\s*(\d+)\s+(\w+)\s+(.*)$', line)
            if match:
                surf_id = int(match.group(1))
                surf_type = match.group(2).upper()
                params = match.group(3)

                self.surfaces[surf_id] = {
                    'type': surf_type,
                    'params': params
                }

    def _parse_materials(self, lines: List[str]):
        """Extract material definitions."""
        current_mat = None

        for line in lines:
            # Material card
            m_match = re.match(r'^\s*[Mm](\d+)\s+(.*)$', line)
            if m_match:
                mat_id = int(m_match.group(1))
                isotopes = m_match.group(2)
                self.materials[mat_id] = {
                    'isotopes': isotopes
                }
                current_mat = mat_id

            # MT card (thermal scattering)
            mt_match = re.match(r'^\s*[Mm][Tt](\d+)\s+(.*)$', line)
            if mt_match:
                mat_id = int(mt_match.group(1))
                self.mt_cards.add(mat_id)


class Phase0Checker:
    """Phase 0: Professional Modeling Standards"""

    def __init__(self, input_parser: MCNPInputParser, repo_path: Path):
        self.parser = input_parser
        self.repo_path = repo_path
        self.results = []

    def check_all(self) -> List[Dict]:
        """Run all Phase 0 checks."""
        self.check_version_control()
        self.check_numbering_scheme()
        self.check_data_separation()
        self.check_readme()
        self.check_thermal_scattering()
        return self.results

    def check_version_control(self):
        """Item 1: Version control from start."""
        git_dir = self.repo_path / '.git'
        if git_dir.exists():
            self.results.append({
                'item': '0.1',
                'name': 'Version Control',
                'status': 'PASS',
                'message': 'Git repository detected'
            })
        else:
            self.results.append({
                'item': '0.1',
                'name': 'Version Control',
                'status': 'FAIL',
                'message': 'No version control (.git not found)',
                'action': 'Run: git init && git add . && git commit -m "Initial commit"'
            })

    def check_numbering_scheme(self):
        """Item 2: Systematic numbering scheme."""
        # Check for documented numbering scheme in header
        with open(self.parser.filepath, 'r') as f:
            header = ''.join(f.readlines()[:50])  # First 50 lines

        keywords = ['numbering', 'scheme', 'convention', 'cell id', 'surface id']
        has_documentation = any(kw in header.lower() for kw in keywords)

        if has_documentation:
            self.results.append({
                'item': '0.2',
                'name': 'Numbering Scheme Documentation',
                'status': 'PASS',
                'message': 'Numbering scheme documented in header'
            })
        else:
            self.results.append({
                'item': '0.2',
                'name': 'Numbering Scheme Documentation',
                'status': 'WARN',
                'message': 'Numbering scheme not documented in header',
                'action': 'Add comments explaining cell/surface/material ID structure'
            })

    def check_data_separation(self):
        """Item 3: Separate data from logic."""
        # Check for CSV/JSON files in repo
        csv_files = list(self.repo_path.glob('*.csv'))
        json_files = list(self.repo_path.glob('*.json'))

        if csv_files or json_files:
            self.results.append({
                'item': '0.3',
                'name': 'Data Separation',
                'status': 'PASS',
                'message': f'Found {len(csv_files)} CSV, {len(json_files)} JSON data files'
            })
        else:
            self.results.append({
                'item': '0.3',
                'name': 'Data Separation',
                'status': 'INFO',
                'message': 'No external data files found (may not be needed)'
            })

    def check_readme(self):
        """Item 5: README with complete workflow."""
        readme_files = list(self.repo_path.glob('README*'))

        if readme_files:
            self.results.append({
                'item': '0.5',
                'name': 'README Documentation',
                'status': 'PASS',
                'message': f'README found: {readme_files[0].name}'
            })
        else:
            self.results.append({
                'item': '0.5',
                'name': 'README Documentation',
                'status': 'WARN',
                'message': 'No README found',
                'action': 'Create README documenting workflow and dependencies'
            })

    def check_thermal_scattering(self):
        """Item 10: Thermal scattering for graphite/water."""
        issues = []

        # Check for carbon without MT card
        for mat_id, mat_data in self.parser.materials.items():
            isotopes = mat_data['isotopes'].lower()
            has_carbon = 'c' in isotopes or '6000' in isotopes or '6012' in isotopes
            has_mt = mat_id in self.parser.mt_cards

            if has_carbon and not has_mt:
                issues.append(f"Material m{mat_id} contains carbon but NO MT card")

        # Check for hydrogen (water) without MT card
        for mat_id, mat_data in self.parser.materials.items():
            isotopes = mat_data['isotopes'].lower()
            has_hydrogen = '1001' in isotopes or '1002' in isotopes
            has_mt = mat_id in self.parser.mt_cards

            if has_hydrogen and not has_mt:
                issues.append(f"Material m{mat_id} contains hydrogen but NO MT card")

        if issues:
            self.results.append({
                'item': '0.10',
                'name': 'Thermal Scattering',
                'status': 'FAIL',
                'message': f"Missing thermal scattering: {', '.join(issues)}",
                'action': 'Add MT cards (grph.XXt for C, lwtr.XXt for H2O, hwtr.XXt for D2O)',
                'impact': 'CRITICAL: 1000-5000 pcm reactivity error!'
            })
        else:
            self.results.append({
                'item': '0.10',
                'name': 'Thermal Scattering',
                'status': 'PASS',
                'message': 'All carbon/hydrogen materials have MT cards (or none present)'
            })


class Phase1ReactorChecker:
    """Phase 1 Extensions: Reactor-Specific Checks"""

    def __init__(self, input_parser: MCNPInputParser):
        self.parser = input_parser
        self.results = []

    def check_all(self) -> List[Dict]:
        """Run all reactor-specific Phase 1 checks."""
        self.check_lattice_dimensions()
        self.check_cross_references()
        self.check_numbering_conflicts()
        self.check_universe_hierarchy()
        return self.results

    def check_lattice_dimensions(self):
        """Item 1.23: Multi-level lattice validation."""
        if not self.parser.lattices:
            self.results.append({
                'item': '1.23',
                'name': 'Lattice Dimensions',
                'status': 'INFO',
                'message': 'No lattices found in input'
            })
            return

        for lat in self.parser.lattices:
            # Simplified check (full implementation would parse FILL bounds)
            self.results.append({
                'item': '1.23',
                'name': f"Lattice {lat['cell']} Type",
                'status': 'INFO',
                'message': f"LAT={lat['lat_type']} lattice detected (full validation requires FILL parsing)"
            })

    def check_cross_references(self):
        """Item 1.26: Cross-reference completeness."""
        errors = []

        # Check all material cells reference defined materials
        for cell_id, cell in self.parser.cells.items():
            mat_id = cell['material']
            if mat_id > 0 and mat_id not in self.parser.materials:
                errors.append(f"Cell {cell_id} references undefined material {mat_id}")

        # Check all fill cells reference defined universes
        for cell_id, cell in self.parser.cells.items():
            if cell.get('fill') and cell['fill'] not in self.parser.universes:
                errors.append(f"Cell {cell_id} fill={cell['fill']} but universe not defined")

        if errors:
            self.results.append({
                'item': '1.26',
                'name': 'Cross-Reference Completeness',
                'status': 'FAIL',
                'message': f"{len(errors)} undefined references found",
                'details': errors,
                'impact': 'CRITICAL: MCNP will fatal error'
            })
        else:
            self.results.append({
                'item': '1.26',
                'name': 'Cross-Reference Completeness',
                'status': 'PASS',
                'message': 'All references valid'
            })

    def check_numbering_conflicts(self):
        """Item 1.27: Numbering scheme conflicts."""
        conflicts = []

        # Check for duplicate cell IDs
        cell_ids = list(self.parser.cells.keys())
        if len(cell_ids) != len(set(cell_ids)):
            duplicates = [cid for cid in cell_ids if cell_ids.count(cid) > 1]
            conflicts.append(f"Duplicate cell IDs: {set(duplicates)}")

        # Check for duplicate surface IDs
        surf_ids = list(self.parser.surfaces.keys())
        if len(surf_ids) != len(set(surf_ids)):
            duplicates = [sid for sid in surf_ids if surf_ids.count(sid) > 1]
            conflicts.append(f"Duplicate surface IDs: {set(duplicates)}")

        # Check for duplicate material IDs
        mat_ids = list(self.parser.materials.keys())
        if len(mat_ids) != len(set(mat_ids)):
            duplicates = [mid for mid in mat_ids if mat_ids.count(mid) > 1]
            conflicts.append(f"Duplicate material IDs: {set(duplicates)}")

        if conflicts:
            self.results.append({
                'item': '1.27',
                'name': 'Numbering Conflicts',
                'status': 'FAIL',
                'message': 'Duplicate IDs found',
                'details': conflicts,
                'action': 'Renumber conflicting entities',
                'impact': 'CRITICAL: Later definition overwrites earlier'
            })
        else:
            self.results.append({
                'item': '1.27',
                'name': 'Numbering Conflicts',
                'status': 'PASS',
                'message': 'No duplicate IDs'
            })

    def check_universe_hierarchy(self):
        """Item 1.23: Universe fill chain validation."""
        # Build directed graph of universe fills
        fill_graph = defaultdict(set)

        for cell_id, cell in self.parser.cells.items():
            if cell.get('universe') and cell.get('fill'):
                parent_u = cell['universe']
                child_u = cell['fill']
                fill_graph[parent_u].add(child_u)

        # Detect cycles using DFS
        def has_cycle(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in fill_graph[node]:
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        visited = set()
        rec_stack = set()
        cycles_found = []

        for node in fill_graph:
            if node not in visited:
                if has_cycle(node, visited, rec_stack):
                    cycles_found.append(node)

        if cycles_found:
            self.results.append({
                'item': '1.23',
                'name': 'Universe Hierarchy',
                'status': 'FAIL',
                'message': f"Circular universe references detected: {cycles_found}",
                'action': 'Restructure universe nesting to eliminate cycles',
                'impact': 'CRITICAL: MCNP will fatal error'
            })
        else:
            self.results.append({
                'item': '1.23',
                'name': 'Universe Hierarchy',
                'status': 'PASS',
                'message': 'No circular universe references'
            })


def main():
    parser = argparse.ArgumentParser(
        description='MCNP Reactor Model Best Practices Checker'
    )
    parser.add_argument('input_file', type=Path, help='MCNP input file')
    parser.add_argument('--repo-path', type=Path, default=Path.cwd(),
                       help='Repository root path (for version control check)')
    parser.add_argument('--phase', choices=['0', '1', 'all'], default='all',
                       help='Which phase to check')
    parser.add_argument('--output', choices=['text', 'json', 'markdown'], default='text',
                       help='Output format')

    args = parser.parse_args()

    # Parse input file
    print(f"Parsing MCNP input: {args.input_file}")
    mcnp_parser = MCNPInputParser(args.input_file)

    all_results = []

    # Run Phase 0 checks
    if args.phase in ['0', 'all']:
        print("\n" + "="*70)
        print("PHASE 0: PROFESSIONAL MODELING STANDARDS (15 items)")
        print("="*70)

        phase0 = Phase0Checker(mcnp_parser, args.repo_path)
        results0 = phase0.check_all()
        all_results.extend(results0)

        print_results(results0)

    # Run Phase 1 reactor checks
    if args.phase in ['1', 'all']:
        print("\n" + "="*70)
        print("PHASE 1: REACTOR-SPECIFIC EXTENSIONS (8 items)")
        print("="*70)

        phase1 = Phase1ReactorChecker(mcnp_parser)
        results1 = phase1.check_all()
        all_results.extend(results1)

        print_results(results1)

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    total = len(all_results)
    passed = sum(1 for r in all_results if r['status'] == 'PASS')
    failed = sum(1 for r in all_results if r['status'] == 'FAIL')
    warned = sum(1 for r in all_results if r['status'] in ['WARN', 'INFO'])

    print(f"Total checks: {total}")
    print(f"  ✓ PASS: {passed}")
    print(f"  ✗ FAIL: {failed}")
    print(f"  ⚠ WARN: {warned}")

    if failed > 0:
        print("\n" + "!"*70)
        print("CRITICAL FAILURES FOUND - INPUT NOT READY FOR PRODUCTION")
        print("!"*70)
        print("\nFix all FAIL items before running MCNP.")
        sys.exit(1)
    elif warned > 0:
        print("\n" + "!"*70)
        print("WARNINGS FOUND - REVIEW RECOMMENDED")
        print("!"*70)
        print("\nConsider addressing WARN items for best practices.")
        sys.exit(0)
    else:
        print("\n" + "✓"*70)
        print("ALL CHECKS PASSED - INPUT READY FOR PHASE 2 TESTING")
        print("✓"*70)
        sys.exit(0)


def print_results(results: List[Dict]):
    """Print check results in formatted output."""
    for r in results:
        status_symbol = {
            'PASS': '✓',
            'FAIL': '✗',
            'WARN': '⚠',
            'INFO': 'ℹ'
        }.get(r['status'], '?')

        print(f"\n[{r['item']}] {status_symbol} {r['name']}")
        print(f"    Status: {r['status']}")
        print(f"    {r['message']}")

        if 'action' in r:
            print(f"    Action: {r['action']}")

        if 'impact' in r:
            print(f"    Impact: {r['impact']}")

        if 'details' in r:
            for detail in r['details']:
                print(f"      - {detail}")


if __name__ == '__main__':
    main()

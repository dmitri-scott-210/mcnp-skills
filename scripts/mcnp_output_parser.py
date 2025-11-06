#!/usr/bin/env python
"""
MCNP Output File (OUTP) Parser

Purpose: Parse MCNP text output files for warnings, errors, tallies, and statistics
Usage: See --help for command-line interface

This script extracts key information from MCNP output files including:
- Problem termination status
- Fatal errors and warnings
- Tally results with statistical checks
- keff and criticality information
- Run statistics

Example:
    python mcnp_output_parser.py output.txt --check-termination
    python mcnp_output_parser.py output.txt --extract-tally 14
"""

import argparse
import re
import sys
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


def check_termination(filepath: str) -> Tuple[bool, str]:
    """
    Check if MCNP run terminated normally

    Parameters:
        filepath: Path to OUTP file

    Returns:
        (success: bool, message: str)
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Check for normal termination
    if 'run terminated when' in content.lower():
        # Extract termination reason
        match = re.search(r'run terminated when\s+(.+?)\.', content, re.IGNORECASE)
        if match:
            reason = match.group(1).strip()
            return True, f"Normal termination: {reason}"
        return True, "Normal termination"

    # Check for fatal errors
    if 'fatal error' in content.lower():
        return False, "Fatal error encountered"

    # Check for bad trouble
    if 'bad trouble' in content.lower():
        return False, "BAD TROUBLE encountered"

    return False, "Termination status unclear"


def extract_warnings(filepath: str) -> List[Dict[str, str]]:
    """
    Extract all warning messages from OUTP file

    Parameters:
        filepath: Path to OUTP file

    Returns:
        List of dictionaries with 'type', 'message', 'line_number'
    """
    warnings = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            line_lower = line.lower()

            if 'warning' in line_lower:
                warnings.append({
                    'type': 'warning',
                    'message': line.strip(),
                    'line_number': line_num
                })

            elif 'caution' in line_lower:
                warnings.append({
                    'type': 'caution',
                    'message': line.strip(),
                    'line_number': line_num
                })

    return warnings


def extract_errors(filepath: str) -> List[Dict[str, str]]:
    """
    Extract fatal error messages

    Parameters:
        filepath: Path to OUTP file

    Returns:
        List of dictionaries with 'type', 'message', 'line_number'
    """
    errors = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            line_lower = line.lower()

            if 'fatal error' in line_lower or 'bad trouble' in line_lower:
                errors.append({
                    'type': 'fatal',
                    'message': line.strip(),
                    'line_number': line_num
                })

    return errors


def extract_tally(filepath: str, tally_num: int) -> Optional[Dict]:
    """
    Extract specific tally results

    Parameters:
        filepath: Path to OUTP file
        tally_num: Tally number to extract

    Returns:
        Dictionary with tally data or None if not found
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find tally section
    tally_pattern = rf'1tally\s+{tally_num}\s+.*?(?=1tally|\Z)'
    match = re.search(tally_pattern, content, re.DOTALL | re.IGNORECASE)

    if not match:
        return None

    tally_section = match.group(0)

    result = {
        'tally_number': tally_num,
        'tally_type': None,
        'particle_type': None,
        'cells': [],
        'results': [],
        'statistical_checks': None
    }

    # Extract tally type (F1, F2, etc.)
    type_match = re.search(r'tally\s+(\d+).*?nps.*?(f\d+|\w+)', tally_section, re.IGNORECASE)
    if type_match:
        result['tally_type'] = type_match.group(2)

    # Extract particle type
    particle_match = re.search(r'particle[s]?:?\s*(\w+)', tally_section, re.IGNORECASE)
    if particle_match:
        result['particle_type'] = particle_match.group(1)

    # Extract results table
    # Look for typical tally result pattern: cell  value  error
    result_pattern = r'^\s*(\d+)\s+([\d.E+-]+)\s+([\d.E+-]+)'
    for line in tally_section.split('\n'):
        match = re.match(result_pattern, line)
        if match:
            cell, value, error = match.groups()
            result['results'].append({
                'cell': int(cell),
                'value': float(value),
                'relative_error': float(error)
            })

    return result if result['results'] else None


def get_statistical_checks(filepath: str, tally_num: int) -> Optional[Dict]:
    """
    Extract 10 statistical checks for specific tally

    Parameters:
        filepath: Path to OUTP file
        tally_num: Tally number

    Returns:
        Dictionary with check results (passed/not passed)
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find tally statistical checks section
    checks_pattern = rf'tally\s+{tally_num}.*?results of 10 statistical checks.*?(?=tally|\Z)'
    match = re.search(checks_pattern, content, re.DOTALL | re.IGNORECASE)

    if not match:
        return None

    checks_section = match.group(0)

    result = {
        'tally_number': tally_num,
        'checks': {}
    }

    # Parse 10 checks
    check_names = [
        'mean_behavior',
        'relative_error',
        'relative_error_decrease',
        'relative_error_decrease_rate',
        'vov',
        'vov_decrease',
        'vov_decrease_rate',
        'figure_of_merit',
        'figure_of_merit_behavior',
        'pdf_slope'
    ]

    # Look for "passed" or "not passed" for each check
    lines = checks_section.split('\n')
    for i, check_name in enumerate(check_names, 1):
        # Pattern: check number followed by status
        pattern = rf'{i}\s+.*?(passed|not passed|missed)'
        match = re.search(pattern, checks_section, re.IGNORECASE)
        if match:
            result['checks'][check_name] = match.group(1).lower()

    return result if result['checks'] else None


def extract_keff(filepath: str) -> Optional[Dict]:
    """
    Extract keff results from criticality calculation

    Parameters:
        filepath: Path to OUTP file

    Returns:
        Dictionary with keff, std dev, and confidence intervals
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Look for keff (criticality) section
    keff_pattern = r'final result.*?keff.*?=\s*([\d.]+)\s*\+\-\s*([\d.]+)'
    match = re.search(keff_pattern, content, re.DOTALL | re.IGNORECASE)

    if not match:
        return None

    keff_value = float(match.group(1))
    keff_uncertainty = float(match.group(2))

    result = {
        'keff': keff_value,
        'uncertainty': keff_uncertainty,
        '95_conf_interval': (keff_value - 1.96*keff_uncertainty,
                             keff_value + 1.96*keff_uncertainty)
    }

    return result


def parse_output(filepath: str) -> Dict:
    """
    Parse OUTP file and extract comprehensive information

    Parameters:
        filepath: Path to OUTP file

    Returns:
        Dictionary with all extracted information
    """
    result = {
        'filepath': filepath,
        'termination': {},
        'warnings': [],
        'errors': [],
        'tallies': defaultdict(dict),
        'keff': None,
        'statistics': {}
    }

    # Check termination
    success, message = check_termination(filepath)
    result['termination'] = {
        'success': success,
        'message': message
    }

    # Extract warnings and errors
    result['warnings'] = extract_warnings(filepath)
    result['errors'] = extract_errors(filepath)

    # Extract keff if present
    result['keff'] = extract_keff(filepath)

    return result


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Parse MCNP output files for key information",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('outpfile', help='MCNP output file to parse')

    parser.add_argument('--check-termination', '-t', action='store_true',
                        help='Check if run terminated normally')
    parser.add_argument('--extract-warnings', '-w', action='store_true',
                        help='Extract all warnings')
    parser.add_argument('--extract-errors', '-e', action='store_true',
                        help='Extract fatal errors')
    parser.add_argument('--extract-tally', '-f', type=int, metavar='NUM',
                        help='Extract specific tally number')
    parser.add_argument('--statistical-checks', '-s', type=int, metavar='NUM',
                        help='Get statistical checks for tally number')
    parser.add_argument('--extract-keff', '-k', action='store_true',
                        help='Extract keff from criticality calculation')
    parser.add_argument('--full-parse', '-a', action='store_true',
                        help='Perform full parse (all information)')

    args = parser.parse_args()

    try:
        if args.check_termination:
            success, message = check_termination(args.outpfile)
            print(f"Termination status: {message}")
            sys.exit(0 if success else 1)

        elif args.extract_warnings:
            warnings = extract_warnings(args.outpfile)
            print(f"Found {len(warnings)} warnings:")
            for w in warnings:
                print(f"  Line {w['line_number']}: [{w['type']}] {w['message']}")

        elif args.extract_errors:
            errors = extract_errors(args.outpfile)
            if errors:
                print(f"Found {len(errors)} fatal errors:")
                for e in errors:
                    print(f"  Line {e['line_number']}: {e['message']}")
            else:
                print("No fatal errors found")

        elif args.extract_tally:
            tally = extract_tally(args.outpfile, args.extract_tally)
            if tally:
                print(f"Tally {args.extract_tally}:")
                print(f"  Type: {tally['tally_type']}")
                print(f"  Particle: {tally['particle_type']}")
                print(f"  Results ({len(tally['results'])} cells):")
                for r in tally['results']:
                    print(f"    Cell {r['cell']}: {r['value']:.6E} ± {r['relative_error']:.4f}")
            else:
                print(f"Tally {args.extract_tally} not found")

        elif args.statistical_checks:
            checks = get_statistical_checks(args.outpfile, args.statistical_checks)
            if checks:
                print(f"Statistical checks for tally {args.statistical_checks}:")
                for name, status in checks['checks'].items():
                    symbol = "✓" if status == "passed" else "✗"
                    print(f"  {symbol} {name}: {status}")
            else:
                print(f"Statistical checks for tally {args.statistical_checks} not found")

        elif args.extract_keff:
            keff = extract_keff(args.outpfile)
            if keff:
                print(f"keff = {keff['keff']:.5f} ± {keff['uncertainty']:.5f}")
                print(f"95% confidence interval: [{keff['95_conf_interval'][0]:.5f}, "
                      f"{keff['95_conf_interval'][1]:.5f}]")
            else:
                print("No keff results found (not a criticality calculation?)")

        elif args.full_parse:
            data = parse_output(args.outpfile)
            print("="*60)
            print(f"MCNP Output Parse Results: {args.outpfile}")
            print("="*60)
            print(f"\nTermination: {data['termination']['message']}")
            print(f"Warnings: {len(data['warnings'])}")
            print(f"Errors: {len(data['errors'])}")
            if data['keff']:
                print(f"\nkeff: {data['keff']['keff']:.5f} ± {data['keff']['uncertainty']:.5f}")

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

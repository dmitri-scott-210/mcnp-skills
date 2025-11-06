#!/usr/bin/env python
"""
MCNP MCTAL Basic Parser

Purpose: Basic MCTAL file parsing for data extraction (read-only)
Note: For advanced processing (merging, export, conversion), see mcnp-mctal-processor skill

Usage: See --help for command-line interface

Provides lightweight parsing of MCTAL files for:
- Header information extraction
- Tally value/error reading
- Tally listing

Example:
    python mctal_basic_parser.py mctal --list-tallies
    python mctal_basic_parser.py mctal --extract-tally 14
"""

import argparse
import numpy as np
import sys
from typing import Dict, List, Optional, Tuple


def parse_mctal_header(mctal_file: str) -> Dict:
    """
    Parse MCTAL file header

    Parameters:
        mctal_file: Path to MCTAL file

    Returns:
        Dictionary with header information
    """
    with open(mctal_file, 'r') as f:
        # Line 1: kod, ver, probid, knod, nps, rnr
        line1 = f.readline().strip()
        parts = line1.split()

        header = {
            'code': parts[0] if len(parts) > 0 else None,
            'version': parts[1] if len(parts) > 1 else None,
            'problem_id': ' '.join(parts[2:-3]) if len(parts) > 5 else None,
            'dump_number': int(parts[-3]) if len(parts) > 2 else None,
            'nps': int(parts[-2]) if len(parts) > 1 else None,
            'rnr': int(parts[-1]) if len(parts) > 0 else None,
        }

        # Line 2: Comment line (problem title)
        header['title'] = f.readline().strip()

        # Line 3: ntal, ntally numbers
        line3 = f.readline().strip().split()
        ntal = int(line3[0])
        tally_numbers = [int(x) for x in line3[1:ntal+1]]
        header['n_tallies'] = ntal
        header['tally_numbers'] = tally_numbers

    return header


def list_tallies(mctal_file: str) -> List[int]:
    """
    List all tally numbers in MCTAL file

    Parameters:
        mctal_file: Path to MCTAL file

    Returns:
        List of tally numbers
    """
    header = parse_mctal_header(mctal_file)
    return header['tally_numbers']


def extract_tally_basic(mctal_file: str, tally_num: int) -> Optional[Dict]:
    """
    Extract basic tally data (values and errors only)

    Parameters:
        mctal_file: Path to MCTAL file
        tally_num: Tally number to extract

    Returns:
        Dictionary with values, errors, and basic metadata
    """
    with open(mctal_file, 'r') as f:
        content = f.read()

    # Find tally section
    # MCTAL format: "tally N" line starts each tally
    tally_marker = f"tally {tally_num:8d}"
    if tally_marker not in content:
        # Try without padding
        tally_marker = f"tally {tally_num}"
        if tally_marker not in content:
            return None

    # Split into lines and find tally start
    lines = content.split('\n')
    tally_start = None
    for i, line in enumerate(lines):
        if f"tally" in line.lower() and str(tally_num) in line:
            tally_start = i
            break

    if tally_start is None:
        return None

    # Parse tally header line
    # Format: tally  n  particle_type
    tally_line = lines[tally_start].split()
    result = {
        'tally_number': tally_num,
        'particle_type': tally_line[2] if len(tally_line) > 2 else None,
    }

    # Next line typically has tally comment/type
    # Then f, d, u, s, m, c, e, t bins

    # Find "vals" section - this marks start of data
    vals_start = None
    for i in range(tally_start, min(tally_start + 100, len(lines))):
        if 'vals' in lines[i].lower():
            vals_start = i + 1
            break

    if vals_start is None:
        return None

    # Read values and errors
    # MCTAL format: alternating value, error on same or consecutive lines
    values = []
    errors = []

    for i in range(vals_start, len(lines)):
        line = lines[i].strip()

        # Check if we've hit next tally or end
        if 'tally' in line.lower() or not line:
            if len(values) > 10:  # Likely finished reading data
                break
            continue

        # Parse numbers
        parts = line.split()
        if parts:
            try:
                nums = [float(x) for x in parts]
                # MCTAL typically has value, error pairs
                for j in range(0, len(nums), 2):
                    if j + 1 < len(nums):
                        values.append(nums[j])
                        errors.append(nums[j+1])
                    else:
                        values.append(nums[j])
            except ValueError:
                continue

    result['values'] = np.array(values)
    result['errors'] = np.array(errors) if errors else None

    return result


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Basic MCTAL file parser for data extraction",
        epilog="For advanced MCTAL processing (merging, export), see mcnp-mctal-processor skill",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('mctal_file', help='MCTAL file to parse')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list-tallies', '-l', action='store_true',
                       help='List all tally numbers')
    group.add_argument('--extract-tally', '-t', type=int, metavar='NUM',
                       help='Extract tally number NUM')
    group.add_argument('--header', '-H', action='store_true',
                       help='Parse and display header information')

    parser.add_argument('--output', '-o', help='Output file (NPZ format for arrays)')

    args = parser.parse_args()

    try:
        if args.list_tallies:
            tallies = list_tallies(args.mctal_file)
            print(f"\nTallies in {args.mctal_file}:")
            print(f"  Total: {len(tallies)}")
            print(f"  Numbers: {', '.join(map(str, tallies))}")

        elif args.header:
            header = parse_mctal_header(args.mctal_file)
            print(f"\nMCTAL Header Information:")
            print(f"  Code: {header['code']}")
            print(f"  Version: {header['version']}")
            print(f"  Title: {header['title']}")
            print(f"  Dump: {header['dump_number']}")
            print(f"  NPS: {header['nps']}")
            print(f"  Random number: {header['rnr']}")
            print(f"  Number of tallies: {header['n_tallies']}")
            print(f"  Tally numbers: {', '.join(map(str, header['tally_numbers']))}")

        elif args.extract_tally:
            data = extract_tally_basic(args.mctal_file, args.extract_tally)
            if data:
                print(f"\nTally {args.extract_tally}:")
                print(f"  Particle type: {data['particle_type']}")
                print(f"  Number of bins: {len(data['values'])}")
                print(f"  Value range: [{np.min(data['values']):.6E}, {np.max(data['values']):.6E}]")
                if data['errors'] is not None:
                    print(f"  Error range: [{np.min(data['errors']):.6E}, {np.max(data['errors']):.6E}]")

                    # Print first few values
                    print(f"\n  First 5 bins:")
                    for i in range(min(5, len(data['values']))):
                        print(f"    {i+1}: {data['values'][i]:.6E} ± {data['errors'][i]:.6E}")

                if args.output:
                    np.savez(args.output, **data)
                    print(f"\nSaved to {args.output}")
            else:
                print(f"Tally {args.extract_tally} not found")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""
MCNP PTRAC Parser

Purpose: Parse PTRAC (Particle Track) files in HDF5 or ASCII format
Usage: See --help for command-line interface

Parses MCNP6 particle track data including positions, energies, events,
and history information.

Example:
    python ptrac_parser.py ptrac.h5 --particle 1
    python ptrac_parser.py ptrac.h5 --filter-event SRC
"""

import argparse
import h5py
import numpy as np
import sys
from typing import Dict, List, Optional


# PTRAC event type codes
EVENT_TYPES = {
    1000: 'SRC',   # Source
    2000: 'BNK',   # Bank
    3000: 'SUR',   # Surface crossing
    4000: 'COL',   # Collision
    5000: 'TER',   # Termination
}


def parse_ptrac_hdf5(h5_file: str, particle_num: int = 1) -> Dict[str, np.ndarray]:
    """
    Parse PTRAC HDF5 file

    Parameters:
        h5_file: Path to PTRAC HDF5 file
        particle_num: Particle type (1=neutron, 2=photon, etc.)

    Returns:
        Dictionary with trajectory data arrays
    """
    with h5py.File(h5_file, 'r') as f:
        # Find particle group
        possible_paths = [
            f'/particle_{particle_num}',
            f'/ptrac/particle_{particle_num}',
            f'/tracks/particle_{particle_num}',
        ]

        ptrac_group = None
        for path in possible_paths:
            if path in f:
                ptrac_group = f[path]
                break

        if ptrac_group is None:
            raise ValueError(f"PTRAC data for particle {particle_num} not found")

        result = {}

        # Common PTRAC datasets
        datasets = ['x', 'y', 'z', 'u', 'v', 'w', 'energy', 'time',
                   'cell', 'surface', 'event_type', 'history', 'weight']

        for name in datasets:
            if name in ptrac_group:
                result[name] = ptrac_group[name][:]
            else:
                result[name] = None

        # Metadata
        result['metadata'] = dict(ptrac_group.attrs.items())

        return result


def filter_by_event(ptrac_data: Dict[str, np.ndarray], event_type: str) -> Dict[str, np.ndarray]:
    """
    Filter PTRAC data by event type

    Parameters:
        ptrac_data: Dictionary from parse_ptrac_hdf5
        event_type: Event type string ('SRC', 'COL', 'SUR', 'TER', 'BNK')

    Returns:
        Filtered dictionary with only specified event type
    """
    event_codes = {v: k for k, v in EVENT_TYPES.items()}
    if event_type.upper() not in event_codes:
        raise ValueError(f"Unknown event type: {event_type}")

    code = event_codes[event_type.upper()]

    if ptrac_data['event_type'] is None:
        raise ValueError("No event_type data in PTRAC file")

    mask = ptrac_data['event_type'] == code

    filtered = {}
    for key, value in ptrac_data.items():
        if key != 'metadata' and value is not None:
            filtered[key] = value[mask]
        else:
            filtered[key] = value

    return filtered


def get_trajectory(ptrac_data: Dict[str, np.ndarray], history_num: int) -> Dict[str, np.ndarray]:
    """
    Extract single particle history trajectory

    Parameters:
        ptrac_data: Dictionary from parse_ptrac_hdf5
        history_num: History number to extract

    Returns:
        Dictionary with trajectory for single history
    """
    if ptrac_data['history'] is None:
        raise ValueError("No history data in PTRAC file")

    mask = ptrac_data['history'] == history_num

    trajectory = {}
    for key, value in ptrac_data.items():
        if key != 'metadata' and value is not None:
            trajectory[key] = value[mask]
        else:
            trajectory[key] = value

    return trajectory


def export_to_csv(ptrac_data: Dict[str, np.ndarray], output_file: str) -> None:
    """
    Export PTRAC data to CSV format

    Parameters:
        ptrac_data: Dictionary from parse_ptrac_hdf5
        output_file: Output CSV filename
    """
    import csv

    # Determine which fields are present
    fields = [k for k, v in ptrac_data.items()
              if k != 'metadata' and v is not None]

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

        # Get length from first field
        n_points = len(ptrac_data[fields[0]])

        for i in range(n_points):
            row = [ptrac_data[field][i] for field in fields]
            writer.writerow(row)


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Parse MCNP PTRAC particle track files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('ptrac_file', help='PTRAC HDF5 file')
    parser.add_argument('--particle', '-p', type=int, default=1,
                        help='Particle type number (default: 1=neutron)')
    parser.add_argument('--filter-event', '-e', choices=['SRC', 'COL', 'SUR', 'TER', 'BNK'],
                        help='Filter by event type')
    parser.add_argument('--history', '-n', type=int,
                        help='Extract specific history number')
    parser.add_argument('--output', '-o', help='Output file (CSV format)')
    parser.add_argument('--summary', '-s', action='store_true',
                        help='Print summary statistics')

    args = parser.parse_args()

    try:
        # Parse PTRAC file
        data = parse_ptrac_hdf5(args.ptrac_file, args.particle)

        # Apply filters
        if args.filter_event:
            data = filter_by_event(data, args.filter_event)

        if args.history:
            data = get_trajectory(data, args.history)

        # Print summary
        if args.summary or (not args.output and not args.history):
            print(f"\nPTRAC Summary for particle type {args.particle}:")
            for key, value in data.items():
                if key != 'metadata' and value is not None:
                    print(f"  {key:12s}: {len(value):10d} points")

            if 'history' in data and data['history'] is not None:
                n_histories = len(np.unique(data['history']))
                print(f"  Unique histories: {n_histories}")

            if 'event_type' in data and data['event_type'] is not None:
                unique_events = np.unique(data['event_type'])
                print(f"\n  Event types present:")
                for event_code in unique_events:
                    event_name = EVENT_TYPES.get(event_code, f"Unknown ({event_code})")
                    count = np.sum(data['event_type'] == event_code)
                    print(f"    {event_name:10s}: {count:10d}")

        # Export to CSV
        if args.output:
            export_to_csv(data, args.output)
            print(f"\nExported to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

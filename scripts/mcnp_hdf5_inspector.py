#!/usr/bin/env python
"""
MCNP HDF5 Inspector

Purpose: Inspect and extract data from MCNP HDF5 output files (RUNTPE.H5, mesh HDF5)
Usage: See --help for command-line interface

This script provides utilities for navigating and extracting data from MCNP6.3+
HDF5 output files, including mesh tallies, PTRAC data, and fission matrices.

Example:
    python mcnp_hdf5_inspector.py runtpe.h5 --list-structure
    python mcnp_hdf5_inspector.py runtpe.h5 --extract-mesh 14
"""

import argparse
import h5py
import numpy as np
import sys
from typing import Dict, List, Tuple, Optional


def list_structure(h5_file: str, group: str = "/", max_depth: Optional[int] = None) -> None:
    """
    List hierarchical structure of HDF5 file

    Parameters:
        h5_file: Path to HDF5 file
        group: Starting group path (default: root)
        max_depth: Maximum depth to display (None = unlimited)
    """
    def print_structure(name, obj, depth=0):
        if max_depth is not None and depth > max_depth:
            return

        indent = "  " * depth
        if isinstance(obj, h5py.Group):
            print(f"{indent}📁 {name}/ (group)")
        elif isinstance(obj, h5py.Dataset):
            print(f"{indent}📄 {name} (dataset, shape: {obj.shape}, dtype: {obj.dtype})")

        # Print attributes
        for attr_name, attr_value in obj.attrs.items():
            print(f"{indent}  🏷️  @{attr_name} = {attr_value}")

    with h5py.File(h5_file, 'r') as f:
        start_group = f.get(group)
        if start_group is None:
            print(f"Error: Group '{group}' not found")
            return

        print(f"\nStructure of {h5_file} starting at '{group}':\n")
        print_structure(group, start_group)
        start_group.visititems(lambda n, o: print_structure(n, o, n.count('/') + 1))


def extract_mesh_tally(h5_file: str, tally_num: int) -> Dict[str, np.ndarray]:
    """
    Extract mesh tally data from HDF5 file

    Parameters:
        h5_file: Path to HDF5 file
        tally_num: Tally number (e.g., 14 for FMESH14)

    Returns:
        Dictionary with 'values', 'errors', 'metadata'
    """
    with h5py.File(h5_file, 'r') as f:
        # Try different path patterns
        possible_paths = [
            f'/results/mesh_tally_{tally_num}',
            f'/mesh_tally_{tally_num}',
            f'/tallies/fmesh_{tally_num}',
        ]

        mesh_group = None
        for path in possible_paths:
            if path in f:
                mesh_group = f[path]
                break

        if mesh_group is None:
            raise ValueError(f"Mesh tally {tally_num} not found in {h5_file}")

        result = {}

        # Extract values (navigate energy_total/time_total or similar)
        def find_values(group):
            """Recursively find 'values' and 'errors' datasets"""
            if 'values' in group:
                return group['values'][:], group.get('errors', np.array([]))[:]
            for key in group.keys():
                subgroup = group[key]
                if isinstance(subgroup, h5py.Group):
                    vals, errs = find_values(subgroup)
                    if vals is not None:
                        return vals, errs
            return None, None

        values, errors = find_values(mesh_group)

        if values is None:
            raise ValueError(f"No 'values' dataset found in tally {tally_num}")

        result['values'] = values
        result['errors'] = errors if errors.size > 0 else None

        # Extract metadata
        metadata = {}
        for attr_name, attr_value in mesh_group.attrs.items():
            metadata[attr_name] = attr_value

        result['metadata'] = metadata

        return result


def extract_ptrac(h5_file: str, particle_num: int = 1) -> Dict[str, np.ndarray]:
    """
    Extract PTRAC particle track data from HDF5 file

    Parameters:
        h5_file: Path to HDF5 file
        particle_num: Particle type number (1=neutron, 2=photon, etc.)

    Returns:
        Dictionary with trajectory data
    """
    with h5py.File(h5_file, 'r') as f:
        # PTRAC paths vary by MCNP version
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
        dataset_names = ['x', 'y', 'z', 'u', 'v', 'w', 'energy', 'time',
                         'cell', 'surface', 'event_type', 'history']

        for name in dataset_names:
            if name in ptrac_group:
                result[name] = ptrac_group[name][:]

        # Extract metadata
        result['metadata'] = dict(ptrac_group.attrs.items())

        return result


def extract_fission_matrix(h5_file: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Extract fission matrix in CSR (Compressed Sparse Row) format

    Parameters:
        h5_file: Path to HDF5 file

    Returns:
        Tuple of (values, column_indices, row_pointers)
    """
    with h5py.File(h5_file, 'r') as f:
        # Fission matrix typically in /fission_matrix or /results/fission_matrix
        possible_paths = [
            '/fission_matrix',
            '/results/fission_matrix',
            '/tallies/fission_matrix',
        ]

        fm_group = None
        for path in possible_paths:
            if path in f:
                fm_group = f[path]
                break

        if fm_group is None:
            raise ValueError("Fission matrix not found in HDF5 file")

        # CSR format: values, column_indices, row_pointers
        values = fm_group['values'][:]
        column_indices = fm_group['column_indices'][:]
        row_pointers = fm_group['row_pointers'][:]

        return values, column_indices, row_pointers


def get_attributes(h5_file: str, path: str) -> Dict:
    """
    Get all attributes for a specific HDF5 object

    Parameters:
        h5_file: Path to HDF5 file
        path: Path to object in HDF5 file

    Returns:
        Dictionary of attributes
    """
    with h5py.File(h5_file, 'r') as f:
        obj = f.get(path)
        if obj is None:
            raise ValueError(f"Path '{path}' not found in {h5_file}")

        return dict(obj.attrs.items())


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Inspect and extract data from MCNP HDF5 output files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('h5file', help='HDF5 file to inspect')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list-structure', '-l', action='store_true',
                       help='List hierarchical structure')
    group.add_argument('--extract-mesh', '-m', type=int, metavar='NUM',
                       help='Extract mesh tally number NUM')
    group.add_argument('--extract-ptrac', '-p', type=int, metavar='NUM', nargs='?',
                       const=1, default=None,
                       help='Extract PTRAC data (default particle: 1=neutron)')
    group.add_argument('--extract-fmtx', '-f', action='store_true',
                       help='Extract fission matrix')

    parser.add_argument('--group', '-g', default='/',
                        help='Starting group for structure listing (default: /)')
    parser.add_argument('--max-depth', '-d', type=int,
                        help='Maximum depth for structure listing')
    parser.add_argument('--output', '-o', help='Output file for extracted data (NPZ format)')

    args = parser.parse_args()

    try:
        if args.list_structure:
            list_structure(args.h5file, args.group, args.max_depth)

        elif args.extract_mesh is not None:
            data = extract_mesh_tally(args.h5file, args.extract_mesh)
            print(f"\nExtracted mesh tally {args.extract_mesh}:")
            print(f"  Values shape: {data['values'].shape}")
            if data['errors'] is not None:
                print(f"  Errors shape: {data['errors'].shape}")
            print(f"  Metadata: {data['metadata']}")

            if args.output:
                np.savez(args.output, **data)
                print(f"\nSaved to {args.output}")

        elif args.extract_ptrac is not None:
            data = extract_ptrac(args.h5file, args.extract_ptrac)
            print(f"\nExtracted PTRAC data for particle {args.extract_ptrac}:")
            for key, value in data.items():
                if key != 'metadata' and isinstance(value, np.ndarray):
                    print(f"  {key}: shape {value.shape}")
            print(f"  Metadata: {data['metadata']}")

            if args.output:
                np.savez(args.output, **data)
                print(f"\nSaved to {args.output}")

        elif args.extract_fmtx:
            values, cols, rows = extract_fission_matrix(args.h5file)
            print(f"\nExtracted fission matrix (CSR format):")
            print(f"  Values: {len(values)} non-zero entries")
            print(f"  Matrix size: {len(rows)-1} rows")
            print(f"  Sparsity: {len(values)/(len(rows)-1)**2*100:.2f}%")

            if args.output:
                np.savez(args.output, values=values, column_indices=cols,
                         row_pointers=rows)
                print(f"\nSaved to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Cell Selector for MCNP Burnup Calculations

Purpose: Automatically select cells for depletion tracking based on flux magnitude
         and material type, following AGR-1 production methodology.

Usage:
    python cell_selector.py --mcnp-output output.o --threshold 1e12 --output cells.txt

    OR

    python cell_selector.py --flux-file flux_data.csv --threshold 1e12 --output cells.txt

Author: MCNP Burnup Builder Skill
Based on: AGR-1 cell selection strategy (150 cells from 1600 total)
"""

import argparse
import re
import sys
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np


class CellSelector:
    """Select cells for burnup tracking based on flux and material type"""

    # Flux thresholds (n/cm²/s)
    FLUX_FUEL_MIN = 1e13        # Minimum for fuel cells
    FLUX_ABSORBER_MIN = 1e12    # Minimum for burnable absorbers
    FLUX_STRUCTURAL_MIN = 1e11  # Minimum for structural (activation)
    FLUX_IGNORE = 1e10          # Below this: ignore

    def __init__(self, flux_data: pd.DataFrame):
        """
        Initialize cell selector

        Args:
            flux_data: DataFrame with columns ['cell_id', 'flux', 'uncertainty', 'material_id', 'volume']
        """
        self.flux_data = flux_data
        self.selected_cells = []

    def classify_material_type(self, material_id: int) -> str:
        """
        Classify material type based on material ID convention

        Assumes material numbering convention:
        - 1-99: Fuel materials
        - 100-199: Burnable absorbers (Gd, B, Hf)
        - 200-299: Structural materials
        - 300+: Moderator/coolant

        Returns:
            'fuel', 'absorber', 'structural', or 'other'
        """
        if 1 <= material_id < 100:
            return 'fuel'
        elif 100 <= material_id < 200:
            return 'absorber'
        elif 200 <= material_id < 300:
            return 'structural'
        else:
            return 'other'

    def select_cells(self, max_cells: int = 200) -> pd.DataFrame:
        """
        Select cells for burnup tracking

        Strategy:
        1. ALL fuel cells with flux > 1E13
        2. ALL absorber cells with flux > 1E12
        3. Structural cells with flux > 1E11 (up to limit)
        4. Ignore cells with flux < 1E10

        Args:
            max_cells: Maximum number of cells to track (default: 200)

        Returns:
            DataFrame of selected cells
        """
        # Classify all cells
        self.flux_data['material_type'] = self.flux_data['material_id'].apply(
            self.classify_material_type
        )

        selected = []

        # Priority 1: Fuel cells (HIGH flux)
        fuel_cells = self.flux_data[
            (self.flux_data['material_type'] == 'fuel') &
            (self.flux_data['flux'] > self.FLUX_FUEL_MIN)
        ].copy()
        fuel_cells['priority'] = 1
        selected.append(fuel_cells)

        print(f"Selected {len(fuel_cells)} fuel cells (φ > {self.FLUX_FUEL_MIN:.0e})")

        # Priority 2: Burnable absorbers (MEDIUM flux)
        absorber_cells = self.flux_data[
            (self.flux_data['material_type'] == 'absorber') &
            (self.flux_data['flux'] > self.FLUX_ABSORBER_MIN)
        ].copy()
        absorber_cells['priority'] = 2
        selected.append(absorber_cells)

        print(f"Selected {len(absorber_cells)} absorber cells (φ > {self.FLUX_ABSORBER_MIN:.0e})")

        # Priority 3: Structural materials (activation tracking)
        structural_cells = self.flux_data[
            (self.flux_data['material_type'] == 'structural') &
            (self.flux_data['flux'] > self.FLUX_STRUCTURAL_MIN)
        ].copy()
        structural_cells['priority'] = 3
        selected.append(structural_cells)

        print(f"Selected {len(structural_cells)} structural cells (φ > {self.FLUX_STRUCTURAL_MIN:.0e})")

        # Combine all selected cells
        selected_df = pd.concat(selected, ignore_index=True)

        # Sort by priority, then flux (descending)
        selected_df = selected_df.sort_values(['priority', 'flux'], ascending=[True, False])

        # Limit to max_cells
        if len(selected_df) > max_cells:
            print(f"\nWARNING: {len(selected_df)} cells selected, limiting to {max_cells}")
            selected_df = selected_df.head(max_cells)

        # Calculate statistics
        total_cells = len(self.flux_data)
        tracked_cells = len(selected_df)
        percentage = tracked_cells / total_cells * 100

        print(f"\n=== CELL SELECTION SUMMARY ===")
        print(f"Total cells in model: {total_cells}")
        print(f"Cells tracked: {tracked_cells}")
        print(f"Percentage tracked: {percentage:.1f}%")
        print(f"Target: ~10% (production reactors), ~50% (test reactors)")

        return selected_df

    def group_similar_cells(self, selected_df: pd.DataFrame,
                           flux_tolerance: float = 0.1) -> pd.DataFrame:
        """
        Group cells with similar flux spectra to reduce tracked cell count

        Args:
            selected_df: DataFrame of selected cells
            flux_tolerance: Fractional flux difference for grouping (default: 0.1 = 10%)

        Returns:
            DataFrame with 'group_id' column added
        """
        # Simple grouping by flux magnitude (production version would use spectrum)
        selected_df = selected_df.copy()
        selected_df['group_id'] = 0

        groups = []
        ungrouped = selected_df.copy()

        group_id = 1
        while len(ungrouped) > 0:
            # Take first cell as group representative
            rep_flux = ungrouped.iloc[0]['flux']

            # Find cells within tolerance
            mask = (np.abs(ungrouped['flux'] - rep_flux) / rep_flux < flux_tolerance)
            group = ungrouped[mask].copy()
            group['group_id'] = group_id

            groups.append(group)
            ungrouped = ungrouped[~mask]
            group_id += 1

        grouped_df = pd.concat(groups, ignore_index=True)

        print(f"\n=== CELL GROUPING ===")
        print(f"Original cells: {len(selected_df)}")
        print(f"Groups formed: {group_id - 1}")
        print(f"Reduction factor: {len(selected_df) / (group_id - 1):.1f}×")

        return grouped_df


def parse_mcnp_output(filepath: str) -> pd.DataFrame:
    """
    Parse MCNP output file to extract flux tally data

    Assumes F4:n tallies were run on cells of interest

    Args:
        filepath: Path to MCNP output file

    Returns:
        DataFrame with flux data
    """
    print(f"Parsing MCNP output: {filepath}")

    with open(filepath, 'r') as f:
        content = f.read()

    # Simple regex to find F4 tally results (cell flux)
    # Format: cell <id> <flux> <uncertainty>
    pattern = r'cell\s+(\d+)\s+([\d.E+-]+)\s+([\d.E+-]+)'

    matches = re.findall(pattern, content, re.IGNORECASE)

    if not matches:
        raise ValueError("No F4 tally results found in MCNP output. "
                        "Ensure F4:n tallies were included in input.")

    data = []
    for cell_id, flux, unc in matches:
        data.append({
            'cell_id': int(cell_id),
            'flux': float(flux),
            'uncertainty': float(unc),
            'material_id': 1,  # Placeholder, would need to parse from input
            'volume': 1.0      # Placeholder
        })

    df = pd.DataFrame(data)
    print(f"Found {len(df)} cells with flux tallies")

    return df


def read_flux_csv(filepath: str) -> pd.DataFrame:
    """
    Read flux data from CSV file

    Expected columns: cell_id, flux, uncertainty, material_id, volume

    Args:
        filepath: Path to CSV file

    Returns:
        DataFrame with flux data
    """
    print(f"Reading flux data from CSV: {filepath}")
    df = pd.read_csv(filepath)

    required_cols = ['cell_id', 'flux', 'material_id']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns in CSV: {missing_cols}")

    # Fill optional columns
    if 'uncertainty' not in df.columns:
        df['uncertainty'] = 0.01
    if 'volume' not in df.columns:
        df['volume'] = 1.0

    print(f"Loaded {len(df)} cells from CSV")

    return df


def write_selected_cells(selected_df: pd.DataFrame, output_file: str):
    """
    Write selected cells to output file

    Format compatible with MCNP BURN card MAT= keyword

    Args:
        selected_df: DataFrame of selected cells
        output_file: Output file path
    """
    with open(output_file, 'w') as f:
        f.write("c ================================================================\n")
        f.write("c MCNP BURN Card Material Selection\n")
        f.write(f"c Generated by cell_selector.py\n")
        f.write(f"c Total cells selected: {len(selected_df)}\n")
        f.write("c ================================================================\n\n")

        # Group by priority
        for priority in sorted(selected_df['priority'].unique()):
            priority_name = {1: 'FUEL', 2: 'ABSORBERS', 3: 'STRUCTURAL'}
            cells = selected_df[selected_df['priority'] == priority]

            f.write(f"c --- {priority_name.get(priority, 'OTHER')} CELLS ({len(cells)} total) ---\n")

            # Write material IDs (assuming cell_id = material_id for simplicity)
            mat_ids = cells['material_id'].unique()
            f.write("MAT=" + " ".join(map(str, mat_ids)) + "\n\n")

        # Write detailed table
        f.write("\nc ================================================================\n")
        f.write("c DETAILED CELL INFORMATION\n")
        f.write("c ================================================================\n")
        f.write("c Cell_ID  Material  Flux(n/cm2/s)  Uncertainty  Priority  Type\n")
        f.write("c ----------------------------------------------------------------\n")

        for _, row in selected_df.iterrows():
            f.write(f"c {row['cell_id']:6d}  {row['material_id']:8d}  "
                   f"{row['flux']:13.6E}  {row['uncertainty']:11.4f}  "
                   f"{row['priority']:8d}  {row['material_type']:12s}\n")

    print(f"\nSelected cells written to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Select cells for MCNP burnup tracking based on flux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From MCNP output file
  python cell_selector.py --mcnp-output run.o --output selected_cells.txt

  # From CSV flux data
  python cell_selector.py --flux-file flux.csv --max-cells 150 --output selected_cells.txt

  # With cell grouping
  python cell_selector.py --flux-file flux.csv --group --tolerance 0.1
        """
    )

    parser.add_argument('--mcnp-output', type=str,
                       help='MCNP output file (contains F4 tally results)')
    parser.add_argument('--flux-file', type=str,
                       help='CSV file with flux data (cell_id, flux, material_id, ...)')
    parser.add_argument('--max-cells', type=int, default=200,
                       help='Maximum number of cells to track (default: 200)')
    parser.add_argument('--group', action='store_true',
                       help='Group similar cells to reduce count')
    parser.add_argument('--tolerance', type=float, default=0.1,
                       help='Flux tolerance for grouping (default: 0.1 = 10%%)')
    parser.add_argument('--output', type=str, default='selected_cells.txt',
                       help='Output file for selected cells')

    args = parser.parse_args()

    # Validate input
    if not args.mcnp_output and not args.flux_file:
        parser.error("Must specify either --mcnp-output or --flux-file")

    # Load flux data
    if args.mcnp_output:
        flux_data = parse_mcnp_output(args.mcnp_output)
    else:
        flux_data = read_flux_csv(args.flux_file)

    # Select cells
    selector = CellSelector(flux_data)
    selected_df = selector.select_cells(max_cells=args.max_cells)

    # Optional grouping
    if args.group:
        selected_df = selector.group_similar_cells(selected_df, flux_tolerance=args.tolerance)

    # Write output
    write_selected_cells(selected_df, args.output)

    print("\n=== CELL SELECTION COMPLETE ===")
    return 0


if __name__ == '__main__':
    sys.exit(main())

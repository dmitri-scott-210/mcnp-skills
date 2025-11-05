#!/usr/bin/env python3
"""
MCNP FOM Tracker

Extracts and tracks Figure of Merit (FOM) values from MCNP output files
across multiple iterations to monitor variance reduction convergence.

Usage:
    python fom_tracker.py output1.o output2.o output3.o
    python fom_tracker.py --tally 5 --plot out*.o

Author: MCNP Variance Reducer Skill
Version: 1.0.0
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional


class TallyFOM:
    """Container for tally FOM data"""
    def __init__(self, tally_num: int, nps: int, mean: float, error: float, fom: float):
        self.tally_num = tally_num
        self.nps = nps
        self.mean = mean
        self.error = error
        self.fom = fom

    def __repr__(self):
        return f"TallyFOM(tally={self.tally_num}, nps={self.nps}, error={self.error:.4f}, fom={self.fom:.1f})"


def extract_fom_from_output(filepath: Path, tally_num: Optional[int] = None) -> Dict[int, TallyFOM]:
    """
    Extract FOM values from MCNP output file.

    Args:
        filepath: Path to MCNP output file
        tally_num: Specific tally number to extract (None = all tallies)

    Returns:
        Dictionary mapping tally number to TallyFOM object
    """
    fom_data = {}

    try:
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read()

        # Pattern for tally results (final table)
        # Matches: tally  5
        #                nps    mean       error      vov      slope    fom
        #          1000000000  1.2345E-04  0.0123   0.0001   ...  12345.6

        pattern = r'tally\s+(\d+)\s+.*?nps\s+mean\s+error.*?\n\s+(\d+)\s+([\d.E+-]+)\s+([\d.]+)\s+[\d.E+-]+\s+[\d.]+\s+([\d.]+)'

        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            tal_num = int(match.group(1))

            if tally_num is not None and tal_num != tally_num:
                continue

            nps = int(match.group(2))
            mean = float(match.group(3))
            error = float(match.group(4))
            fom = float(match.group(5))

            fom_data[tal_num] = TallyFOM(tal_num, nps, mean, error, fom)

    except Exception as e:
        print(f"Warning: Error reading {filepath}: {e}", file=sys.stderr)

    return fom_data


def calculate_fom_improvement(fom_baseline: float, fom_vr: float) -> float:
    """
    Calculate FOM improvement factor.

    Args:
        fom_baseline: Baseline FOM (analog or previous iteration)
        fom_vr: VR FOM (current iteration)

    Returns:
        Improvement factor (e.g., 50.0 = 50× improvement)
    """
    if fom_baseline <= 0:
        return 0.0
    return fom_vr / fom_baseline


def check_fom_convergence(fom_values: List[float], threshold: float = 0.20) -> Tuple[bool, float]:
    """
    Check if FOM has converged across iterations.

    Args:
        fom_values: List of FOM values (oldest to newest)
        threshold: Convergence threshold (default 0.20 = 20% change)

    Returns:
        Tuple of (converged: bool, change_ratio: float)
    """
    if len(fom_values) < 2:
        return False, 0.0

    fom_prev = fom_values[-2]
    fom_curr = fom_values[-1]

    if fom_prev <= 0:
        return False, 0.0

    change_ratio = abs(fom_curr - fom_prev) / fom_prev
    converged = change_ratio < threshold

    return converged, change_ratio


def format_fom_table(results: List[Tuple[str, Dict[int, TallyFOM]]], tally_num: int) -> str:
    """
    Format FOM tracking results as ASCII table.

    Args:
        results: List of (filename, fom_data) tuples
        tally_num: Tally number to display

    Returns:
        Formatted table string
    """
    lines = []
    lines.append(f"FOM Tracking for Tally {tally_num}")
    lines.append("=" * 80)
    lines.append(f"{'File':<25} {'NPS':>12} {'Mean':>12} {'Error':>8} {'FOM':>12} {'Ratio':>8}")
    lines.append("-" * 80)

    baseline_fom = None

    for filename, fom_data in results:
        if tally_num not in fom_data:
            lines.append(f"{filename:<25} {'N/A':>12}")
            continue

        fom_obj = fom_data[tally_num]

        # Calculate ratio to baseline
        if baseline_fom is None:
            baseline_fom = fom_obj.fom
            ratio_str = "1.0×"
        else:
            ratio = fom_obj.fom / baseline_fom
            ratio_str = f"{ratio:.1f}×"

        lines.append(
            f"{filename:<25} {fom_obj.nps:>12d} {fom_obj.mean:>12.4e} "
            f"{fom_obj.error:>8.4f} {fom_obj.fom:>12.1f} {ratio_str:>8}"
        )

    # Convergence check
    fom_values = [fom_data[tally_num].fom for _, fom_data in results if tally_num in fom_data]
    if len(fom_values) >= 2:
        converged, change = check_fom_convergence(fom_values)
        lines.append("-" * 80)
        lines.append(f"Convergence: {'✓ CONVERGED' if converged else '✗ NOT CONVERGED'} "
                     f"(last change: {change*100:.1f}%)")

    return "\n".join(lines)


def plot_fom_trend(results: List[Tuple[str, Dict[int, TallyFOM]]], tally_num: int):
    """
    Create simple ASCII plot of FOM trend.

    Args:
        results: List of (filename, fom_data) tuples
        tally_num: Tally number to plot
    """
    fom_values = []
    labels = []

    for i, (filename, fom_data) in enumerate(results):
        if tally_num in fom_data:
            fom_values.append(fom_data[tally_num].fom)
            labels.append(f"Run {i+1}")

    if not fom_values:
        print(f"No data for tally {tally_num}")
        return

    # Normalize to 60-character width
    max_fom = max(fom_values)
    scale = 60.0 / max_fom

    print(f"\nFOM Trend (Tally {tally_num}):")
    print("=" * 70)

    for label, fom in zip(labels, fom_values):
        bar_length = int(fom * scale)
        bar = "█" * bar_length
        print(f"{label:<8} {fom:>10.1f} {bar}")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Track FOM values across MCNP runs for variance reduction optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Track all tallies in multiple output files
  python fom_tracker.py out1.o out2.o out3.o

  # Track specific tally with plot
  python fom_tracker.py --tally 5 --plot out_iter*.o

  # Check convergence
  python fom_tracker.py --tally 5 --convergence-threshold 0.15 out*.o
        """
    )

    parser.add_argument('files', nargs='+', help='MCNP output files')
    parser.add_argument('--tally', type=int, help='Specific tally number to track')
    parser.add_argument('--plot', action='store_true', help='Display ASCII plot of FOM trend')
    parser.add_argument('--convergence-threshold', type=float, default=0.20,
                        help='Convergence threshold (default: 0.20 = 20%%)')

    args = parser.parse_args()

    # Process files
    results = []
    for filepath in args.files:
        path = Path(filepath)
        if not path.exists():
            print(f"Warning: File not found: {filepath}", file=sys.stderr)
            continue

        fom_data = extract_fom_from_output(path, args.tally)
        results.append((path.name, fom_data))

    if not results:
        print("Error: No valid output files found", file=sys.stderr)
        sys.exit(1)

    # Display results
    if args.tally:
        # Single tally tracking
        print(format_fom_table(results, args.tally))

        if args.plot:
            plot_fom_trend(results, args.tally)
    else:
        # All tallies
        all_tallies = set()
        for _, fom_data in results:
            all_tallies.update(fom_data.keys())

        for tally_num in sorted(all_tallies):
            print(format_fom_table(results, tally_num))
            print()


if __name__ == "__main__":
    main()

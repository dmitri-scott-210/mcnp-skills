#!/usr/bin/env python3
"""
MCNP Statistical Convergence Plotter

Purpose: Extract and visualize Tally Fluctuation Chart (TFC) data from MCNP output files.
Author: MCNP Skills Project
Version: 1.0.0

Usage:
    python plot_convergence.py output.o --tally 4
    python plot_convergence.py output.o --tally 14 --output convergence_f14.png
"""

import argparse
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def parse_tfc(output_file, tally_num):
    """
    Extract Tally Fluctuation Chart data from MCNP output file.

    Args:
        output_file: Path to MCNP output file (.o or .out)
        tally_num: Tally number to extract

    Returns:
        Dictionary with keys: nps, mean, error, vov, slope, fom
    """
    try:
        with open(output_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {output_file}")
        return None

    # Find TFC section for specified tally
    pattern = rf'tally\s+{tally_num}\s*\n.*?nps.*?mean.*?error.*?vov.*?slope.*?fom\s*\n(.*?)(?=tally|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    if not match:
        print(f"Error: Tally {tally_num} not found in output file")
        return None

    lines = match.group(1).strip().split('\n')
    nps, mean, error, vov, slope, fom = [], [], [], [], [], []

    for line in lines:
        parts = line.split()
        if len(parts) >= 6:
            try:
                nps.append(float(parts[0]))
                mean.append(float(parts[1]))
                error.append(float(parts[2]))
                vov.append(float(parts[3]))
                slope.append(float(parts[4]))
                fom.append(float(parts[5]))
            except ValueError:
                continue  # Skip non-numeric lines

    if not nps:
        print(f"Error: No TFC data found for tally {tally_num}")
        return None

    return {
        'nps': np.array(nps),
        'mean': np.array(mean),
        'error': np.array(error),
        'vov': np.array(vov),
        'slope': np.array(slope),
        'fom': np.array(fom)
    }


def plot_convergence(tfc_data, tally_num, save_path='convergence.png'):
    """
    Create 4-panel convergence plot.

    Args:
        tfc_data: Dictionary from parse_tfc()
        tally_num: Tally number (for title)
        save_path: Output file path
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    nps = tfc_data['nps']
    mean = tfc_data['mean']
    error = tfc_data['error']
    vov = tfc_data['vov']
    fom = tfc_data['fom']

    # Panel 1: Mean vs NPS
    ax1.plot(nps, mean, 'b-o', markersize=4)
    ax1.axhline(mean[-1], color='k', linestyle='--', alpha=0.5, label=f'Final: {mean[-1]:.4e}')
    ax1.set_xlabel('Number of Histories', fontsize=11)
    ax1.set_ylabel('Tally Mean', fontsize=11)
    ax1.set_title(f'Tally {tally_num}: Mean Convergence', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=9)

    # Panel 2: Relative Error vs NPS (log-log)
    ax2.loglog(nps, error, 'r-o', markersize=4, label='Actual error')
    # Theoretical 1/√N line
    theory = error[0] * np.sqrt(nps[0] / nps)
    ax2.loglog(nps, theory, 'k--', alpha=0.7, label='1/√N theory')
    ax2.axhline(0.10, color='orange', linestyle=':', alpha=0.5, label='10% target')
    ax2.set_xlabel('Number of Histories', fontsize=11)
    ax2.set_ylabel('Relative Error', fontsize=11)
    ax2.set_title('Error Convergence', fontsize=12, fontweight='bold')
    ax2.grid(True, which='both', alpha=0.3)
    ax2.legend(fontsize=9)

    # Panel 3: VOV vs NPS
    ax3.semilogy(nps, vov, 'g-o', markersize=4)
    ax3.axhline(0.1, color='r', linestyle='--', alpha=0.5, label='VOV=0.1 limit')
    ax3.set_xlabel('Number of Histories', fontsize=11)
    ax3.set_ylabel('Variance of Variance (VOV)', fontsize=11)
    ax3.set_title('VOV Convergence', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=9)

    # Panel 4: FOM vs NPS
    ax4.plot(nps, fom, 'm-o', markersize=4)
    ax4.axhline(fom[-1], color='k', linestyle='--', alpha=0.5, label=f'Final FOM: {fom[-1]:.2e}')
    ax4.set_xlabel('Number of Histories', fontsize=11)
    ax4.set_ylabel('Figure of Merit (FOM)', fontsize=11)
    ax4.set_title('FOM Stability', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Convergence plot saved to {save_path}")

    return fig


def print_summary(tfc_data, tally_num):
    """Print statistical summary."""
    print(f"\n{'='*60}")
    print(f"CONVERGENCE SUMMARY - Tally {tally_num}")
    print(f"{'='*60}")

    nps = tfc_data['nps']
    mean = tfc_data['mean']
    error = tfc_data['error']
    vov = tfc_data['vov']
    fom = tfc_data['fom']

    print(f"\nFinal Statistics:")
    print(f"  NPS:          {nps[-1]:.2e}")
    print(f"  Mean:         {mean[-1]:.6e}")
    print(f"  Rel. Error:   {error[-1]:.4f} ({error[-1]*100:.2f}%)")
    print(f"  VOV:          {vov[-1]:.4f}")
    print(f"  FOM:          {fom[-1]:.2e}")

    print(f"\nConvergence Assessment:")

    # Check mean stability (last 3 points within 5%)
    mean_stable = np.std(mean[-3:]) / np.mean(mean[-3:]) < 0.05
    print(f"  Mean stable:     {'✓ YES' if mean_stable else '✗ NO (still drifting)'}")

    # Check error target
    error_good = error[-1] < 0.10
    print(f"  Error < 10%:     {'✓ YES' if error_good else '✗ NO'}")

    # Check VOV
    vov_good = vov[-1] < 0.10
    print(f"  VOV < 0.1:       {'✓ YES' if vov_good else '✗ NO'}")

    # Check FOM stability (last 3 points within 20%)
    fom_stable = np.std(fom[-3:]) / np.mean(fom[-3:]) < 0.20
    print(f"  FOM stable:      {'✓ YES' if fom_stable else '✗ NO (degrading)'}")

    overall_pass = mean_stable and error_good and vov_good and fom_stable
    print(f"\nOverall: {'✓ CONVERGED' if overall_pass else '✗ NEEDS MORE HISTORIES'}")
    print(f"{'='*60}\n")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Plot MCNP tally convergence from output file',
        epilog='Example: python plot_convergence.py output.o --tally 4'
    )

    parser.add_argument('output_file', type=str,
                        help='MCNP output file (.o or .out)')
    parser.add_argument('--tally', '-t', type=int, required=True,
                        help='Tally number to plot')
    parser.add_argument('--output', '-o', type=str, default='convergence.png',
                        help='Output plot file (default: convergence.png)')
    parser.add_argument('--summary', '-s', action='store_true',
                        help='Print summary only (no plot)')

    args = parser.parse_args()

    # Parse TFC data
    print(f"Parsing tally {args.tally} from {args.output_file}...")
    tfc_data = parse_tfc(args.output_file, args.tally)

    if tfc_data is None:
        sys.exit(1)

    print(f"✓ Found {len(tfc_data['nps'])} data points")

    # Print summary
    print_summary(tfc_data, args.tally)

    # Create plot
    if not args.summary:
        plot_convergence(tfc_data, args.tally, args.output)


if __name__ == '__main__':
    main()

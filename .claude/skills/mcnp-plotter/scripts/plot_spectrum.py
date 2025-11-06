#!/usr/bin/env python3
"""
MCNP Energy Spectrum Plotter

Purpose: Create publication-quality energy spectrum plots from MCNP tally data.
Author: MCNP Skills Project
Version: 1.0.0

Usage:
    python plot_spectrum.py --energy 1e-10 1e-6 0.1 1 14 --flux 1.2e-4 5.6e-5 3.4e-5 1.8e-5 8.2e-6 --error 0.05 0.08 0.10 0.12 0.15
    python plot_spectrum.py --file spectrum_data.txt
"""

import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt


def plot_energy_spectrum(energy_bins, flux, errors, particle='neutron',
                         title=None, save_path='spectrum.png'):
    """
    Create publication-quality energy spectrum plot.

    Args:
        energy_bins: Array of energy bin edges (MeV)
        flux: Array of flux values (length = len(energy_bins) - 1)
        errors: Array of relative errors (same length as flux)
        particle: Particle type ('neutron', 'photon', etc.)
        title: Plot title (if None, auto-generated)
        save_path: Output file path
    """
    # Validate inputs
    if len(flux) != len(energy_bins) - 1:
        raise ValueError(f"Flux array length ({len(flux)}) must be one less than energy bins ({len(energy_bins)})")

    if len(errors) != len(flux):
        raise ValueError(f"Errors array length ({len(errors)}) must match flux array ({len(flux)})")

    fig, ax = plt.subplots(figsize=(10, 7))

    # Calculate bin centers (geometric mean for log scale)
    e_centers = np.sqrt(energy_bins[:-1] * energy_bins[1:])

    # Calculate absolute uncertainties
    abs_errors = flux * errors

    # Plot with error bars
    ax.errorbar(e_centers, flux, yerr=abs_errors,
                fmt='o-', markersize=6, capsize=3, capthick=1.5,
                color='#0173B2', ecolor='gray', label='MCNP Calculation',
                linewidth=2)

    # Formatting
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Energy (MeV)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Flux (particles/cm² per source particle)', fontsize=13, fontweight='bold')

    if title is None:
        title = f'{particle.capitalize()} Energy Spectrum'
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add reference lines for neutrons
    if particle.lower() == 'neutron':
        ax.axvline(1e-6, color='b', linestyle='--', alpha=0.4, linewidth=1.5, label='Thermal (1 eV)')
        ax.axvline(1e-3, color='g', linestyle='--', alpha=0.4, linewidth=1.5, label='Epithermal (1 keV)')
        ax.axvline(1.0, color='r', linestyle='--', alpha=0.4, linewidth=1.5, label='Fast (1 MeV)')

    ax.grid(True, which='both', alpha=0.3, linestyle=':')
    ax.legend(fontsize=11, loc='best', framealpha=0.9)

    # Adjust limits to show all data
    ax.set_xlim(energy_bins[0] * 0.8, energy_bins[-1] * 1.2)
    y_min = np.min(flux[flux > 0]) * 0.5 if np.any(flux > 0) else 1e-10
    y_max = np.max(flux) * 2.0
    ax.set_ylim(y_min, y_max)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.savefig(save_path.replace('.png', '.pdf'), bbox_inches='tight')
    print(f"\n✓ Spectrum plots saved:")
    print(f"  {save_path}")
    print(f"  {save_path.replace('.png', '.pdf')}")

    return fig


def load_spectrum_file(filepath):
    """
    Load spectrum data from file.

    Expected format (space or comma separated):
    # Energy (MeV)  Flux  RelError
    1e-10  1.23e-4  0.05
    1e-6   5.67e-5  0.08
    ...
    """
    try:
        data = np.loadtxt(filepath)
    except Exception as e:
        print(f"Error loading file {filepath}: {e}")
        sys.exit(1)

    if data.shape[1] < 3:
        print(f"Error: File must have at least 3 columns (energy, flux, error)")
        sys.exit(1)

    # Assume first column is energy bin edges or centers
    # If N rows, interpret as bin centers and reconstruct edges
    energy_centers = data[:, 0]
    flux = data[:, 1]
    errors = data[:, 2]

    # Reconstruct bin edges from centers (geometric)
    ratios = energy_centers[1:] / energy_centers[:-1]
    avg_ratio = np.mean(ratios)

    energy_bins = np.zeros(len(energy_centers) + 1)
    energy_bins[0] = energy_centers[0] / np.sqrt(avg_ratio)
    for i in range(len(energy_centers)):
        energy_bins[i+1] = energy_bins[i] * avg_ratio

    return energy_bins, flux, errors


def print_spectrum_summary(energy_bins, flux, errors):
    """Print spectrum statistics."""
    print(f"\n{'='*60}")
    print(f"ENERGY SPECTRUM SUMMARY")
    print(f"{'='*60}")

    print(f"\nEnergy Bins: {len(flux)}")
    print(f"Energy Range: {energy_bins[0]:.2e} - {energy_bins[-1]:.2e} MeV")

    e_centers = np.sqrt(energy_bins[:-1] * energy_bins[1:])

    print(f"\nBin-by-Bin Data:")
    print(f"{'E_low (MeV)':<15} {'E_high (MeV)':<15} {'Flux':<15} {'Error (%)':<10}")
    print("-" * 60)
    for i in range(len(flux)):
        print(f"{energy_bins[i]:<15.3e} {energy_bins[i+1]:<15.3e} {flux[i]:<15.3e} {errors[i]*100:<10.2f}")

    print(f"\nTotal Integrated Flux: {np.sum(flux):.3e}")
    print(f"Mean Relative Error: {np.mean(errors):.4f} ({np.mean(errors)*100:.2f}%)")
    print(f"Max Relative Error: {np.max(errors):.4f} ({np.max(errors)*100:.2f}%)")

    print(f"{'='*60}\n")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Plot MCNP energy spectrum',
        epilog='Example: python plot_spectrum.py --energy 1e-10 1e-6 0.1 1 14 --flux 1.2e-4 5.6e-5 --error 0.05 0.08'
    )

    parser.add_argument('--energy', '-e', nargs='+', type=float,
                        help='Energy bin edges (MeV)')
    parser.add_argument('--flux', '-f', nargs='+', type=float,
                        help='Flux values (one per bin)')
    parser.add_argument('--error', '-r', nargs='+', type=float,
                        help='Relative errors (one per bin)')
    parser.add_argument('--file', type=str,
                        help='Load data from file (3 columns: energy, flux, error)')
    parser.add_argument('--particle', '-p', type=str, default='neutron',
                        help='Particle type (neutron, photon, etc.)')
    parser.add_argument('--title', '-t', type=str,
                        help='Plot title (default: auto-generated)')
    parser.add_argument('--output', '-o', type=str, default='spectrum.png',
                        help='Output plot file (default: spectrum.png)')
    parser.add_argument('--summary', '-s', action='store_true',
                        help='Print summary only (no plot)')

    args = parser.parse_args()

    # Load data
    if args.file:
        print(f"Loading spectrum from {args.file}...")
        energy_bins, flux, errors = load_spectrum_file(args.file)
    elif args.energy and args.flux and args.error:
        energy_bins = np.array(args.energy)
        flux = np.array(args.flux)
        errors = np.array(args.error)

        if len(flux) != len(energy_bins) - 1:
            print(f"Error: Flux array length ({len(flux)}) must be one less than energy bins ({len(energy_bins)})")
            sys.exit(1)
    else:
        print("Error: Must provide either --file OR (--energy + --flux + --error)")
        parser.print_help()
        sys.exit(1)

    # Print summary
    print_spectrum_summary(energy_bins, flux, errors)

    # Create plot
    if not args.summary:
        plot_energy_spectrum(energy_bins, flux, errors,
                           particle=args.particle,
                           title=args.title,
                           save_path=args.output)


if __name__ == '__main__':
    main()

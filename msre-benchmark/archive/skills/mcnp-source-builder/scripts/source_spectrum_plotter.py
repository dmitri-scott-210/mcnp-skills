"""
MCNP Source Spectrum Plotter

Plots energy and angular distributions for MCNP source definitions.
Supports Watt spectrum, Maxwellian, Gaussian, discrete lines, and histogram distributions.

Usage:
    python source_spectrum_plotter.py --type watt --param1 0.988 --param2 2.249
    python source_spectrum_plotter.py --type maxwell --param1 1.29
    python source_spectrum_plotter.py --type gaussian --param1 2.5 --param2 0.1
    python source_spectrum_plotter.py --type discrete --energies 0.662 1.173 1.332 --intensities 0.85 1.0 1.0

Author: Claude (Anthropic)
Created: 2025-11-03
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple


def watt_spectrum(E: np.ndarray, a: float, b: float) -> np.ndarray:
    """
    Calculate Watt fission spectrum: p(E) ∝ exp(-E/a) * sinh(√(bE))

    Args:
        E: Energy array (MeV)
        a: Parameter 'a' (typically ~0.988 for U-235 thermal)
        b: Parameter 'b' (typically ~2.249 for U-235 thermal)

    Returns:
        Probability density array (normalized)
    """
    p = np.exp(-E / a) * np.sinh(np.sqrt(b * E))
    return p / np.trapz(p, E)


def maxwell_spectrum(E: np.ndarray, T: float) -> np.ndarray:
    """
    Calculate Maxwellian spectrum: p(E) ∝ √E * exp(-E/T)

    Args:
        E: Energy array (MeV)
        T: Temperature parameter (MeV)

    Returns:
        Probability density array (normalized)
    """
    p = np.sqrt(E) * np.exp(-E / T)
    return p / np.trapz(p, E)


def gaussian_spectrum(E: np.ndarray, E0: float, sigma: float) -> np.ndarray:
    """
    Calculate Gaussian spectrum: p(E) ∝ exp(-(E-E0)²/(2σ²))

    Args:
        E: Energy array (MeV)
        E0: Mean energy (MeV)
        sigma: Standard deviation (MeV)

    Returns:
        Probability density array (normalized)
    """
    p = np.exp(-((E - E0)**2) / (2 * sigma**2))
    return p / np.trapz(p, E)


def exponential_spectrum(E: np.ndarray, lambda_param: float) -> np.ndarray:
    """
    Calculate exponential spectrum: p(E) ∝ exp(-λE)

    Args:
        E: Energy array (MeV)
        lambda_param: Decay constant (1/MeV)

    Returns:
        Probability density array (normalized)
    """
    p = np.exp(-lambda_param * E)
    return p / np.trapz(p, E)


def plot_watt_spectrum(a: float, b: float, output: str = None):
    """Plot Watt fission spectrum"""
    E = np.linspace(0.01, 20, 1000)
    p = watt_spectrum(E, a, b)

    plt.figure(figsize=(10, 6))
    plt.plot(E, p, 'b-', linewidth=2)
    plt.xlabel('Energy (MeV)', fontsize=12)
    plt.ylabel('Probability Density (MeV⁻¹)', fontsize=12)
    plt.title(f'Watt Fission Spectrum (a={a:.3f}, b={b:.3f})', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 20)

    # Add statistics
    E_avg = np.trapz(E * p, E)
    E_mode = E[np.argmax(p)]
    plt.axvline(E_avg, color='r', linestyle='--', label=f'Mean: {E_avg:.3f} MeV')
    plt.axvline(E_mode, color='g', linestyle='--', label=f'Mode: {E_mode:.3f} MeV')
    plt.legend()

    if output:
        plt.savefig(output, dpi=300, bbox_inches='tight')
        print(f"Saved to {output}")
    else:
        plt.show()


def plot_maxwell_spectrum(T: float, output: str = None):
    """Plot Maxwellian spectrum"""
    E = np.linspace(0.001, 10 * T, 1000)
    p = maxwell_spectrum(E, T)

    plt.figure(figsize=(10, 6))
    plt.plot(E, p, 'r-', linewidth=2)
    plt.xlabel('Energy (MeV)', fontsize=12)
    plt.ylabel('Probability Density (MeV⁻¹)', fontsize=12)
    plt.title(f'Maxwellian Spectrum (T={T:.3f} MeV)', fontsize=14)
    plt.grid(True, alpha=0.3)

    # Add statistics
    E_avg = np.trapz(E * p, E)
    E_mode = E[np.argmax(p)]
    plt.axvline(E_avg, color='b', linestyle='--', label=f'Mean: {E_avg:.3f} MeV')
    plt.axvline(E_mode, color='g', linestyle='--', label=f'Mode: {E_mode:.3f} MeV')
    plt.legend()

    if output:
        plt.savefig(output, dpi=300, bbox_inches='tight')
        print(f"Saved to {output}")
    else:
        plt.show()


def plot_gaussian_spectrum(E0: float, sigma: float, output: str = None):
    """Plot Gaussian spectrum"""
    E = np.linspace(max(0, E0 - 5*sigma), E0 + 5*sigma, 1000)
    p = gaussian_spectrum(E, E0, sigma)

    plt.figure(figsize=(10, 6))
    plt.plot(E, p, 'g-', linewidth=2)
    plt.xlabel('Energy (MeV)', fontsize=12)
    plt.ylabel('Probability Density (MeV⁻¹)', fontsize=12)
    plt.title(f'Gaussian Spectrum (E₀={E0:.3f} MeV, σ={sigma:.3f} MeV)', fontsize=14)
    plt.grid(True, alpha=0.3)

    # Add statistics
    plt.axvline(E0, color='r', linestyle='--', label=f'Mean: {E0:.3f} MeV')
    plt.axvline(E0 - sigma, color='k', linestyle=':', alpha=0.5, label=f'±1σ')
    plt.axvline(E0 + sigma, color='k', linestyle=':', alpha=0.5)
    plt.legend()

    if output:
        plt.savefig(output, dpi=300, bbox_inches='tight')
        print(f"Saved to {output}")
    else:
        plt.show()


def plot_discrete_spectrum(energies: List[float], intensities: List[float], output: str = None):
    """Plot discrete line spectrum"""
    # Normalize intensities
    intensities = np.array(intensities)
    intensities = intensities / np.sum(intensities)

    plt.figure(figsize=(10, 6))
    plt.stem(energies, intensities, basefmt=' ', linefmt='b-', markerfmt='bo')
    plt.xlabel('Energy (MeV)', fontsize=12)
    plt.ylabel('Relative Intensity', fontsize=12)
    plt.title('Discrete Gamma-Ray Spectrum', fontsize=14)
    plt.grid(True, alpha=0.3, axis='y')

    # Annotate lines
    for E, I in zip(energies, intensities):
        plt.text(E, I * 1.05, f'{E:.3f} MeV\n({I:.2%})',
                ha='center', va='bottom', fontsize=9)

    if output:
        plt.savefig(output, dpi=300, bbox_inches='tight')
        print(f"Saved to {output}")
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='Plot MCNP source energy spectra',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Watt spectrum (U-235 thermal fission)
  python source_spectrum_plotter.py --type watt --param1 0.988 --param2 2.249

  # Maxwellian (1.29 MeV temperature)
  python source_spectrum_plotter.py --type maxwell --param1 1.29

  # Gaussian (2.5 MeV mean, 0.1 MeV std dev)
  python source_spectrum_plotter.py --type gaussian --param1 2.5 --param2 0.1

  # Discrete gamma lines (Co-60)
  python source_spectrum_plotter.py --type discrete --energies 1.173 1.332 --intensities 1.0 1.0

  # Save to file
  python source_spectrum_plotter.py --type watt --param1 0.988 --param2 2.249 --output watt.png
        """
    )

    parser.add_argument('--type', required=True,
                       choices=['watt', 'maxwell', 'gaussian', 'discrete', 'exponential'],
                       help='Spectrum type')
    parser.add_argument('--param1', type=float, help='First parameter (a for Watt, T for Maxwell, E0 for Gaussian, λ for exponential)')
    parser.add_argument('--param2', type=float, help='Second parameter (b for Watt, σ for Gaussian)')
    parser.add_argument('--energies', type=float, nargs='+', help='Energy values for discrete spectrum (MeV)')
    parser.add_argument('--intensities', type=float, nargs='+', help='Intensity values for discrete spectrum')
    parser.add_argument('--output', '-o', help='Output file path (PNG, PDF, etc.)')

    args = parser.parse_args()

    if args.type == 'watt':
        if args.param1 is None or args.param2 is None:
            parser.error("Watt spectrum requires --param1 (a) and --param2 (b)")
        plot_watt_spectrum(args.param1, args.param2, args.output)

    elif args.type == 'maxwell':
        if args.param1 is None:
            parser.error("Maxwellian spectrum requires --param1 (T)")
        plot_maxwell_spectrum(args.param1, args.output)

    elif args.type == 'gaussian':
        if args.param1 is None or args.param2 is None:
            parser.error("Gaussian spectrum requires --param1 (E0) and --param2 (sigma)")
        plot_gaussian_spectrum(args.param1, args.param2, args.output)

    elif args.type == 'discrete':
        if args.energies is None or args.intensities is None:
            parser.error("Discrete spectrum requires --energies and --intensities")
        if len(args.energies) != len(args.intensities):
            parser.error("Number of energies and intensities must match")
        plot_discrete_spectrum(args.energies, args.intensities, args.output)

    elif args.type == 'exponential':
        if args.param1 is None:
            parser.error("Exponential spectrum requires --param1 (lambda)")
        E = np.linspace(0.01, 10, 1000)
        p = exponential_spectrum(E, args.param1)
        plt.figure(figsize=(10, 6))
        plt.plot(E, p, 'm-', linewidth=2)
        plt.xlabel('Energy (MeV)', fontsize=12)
        plt.ylabel('Probability Density (MeV⁻¹)', fontsize=12)
        plt.title(f'Exponential Spectrum (λ={args.param1:.3f} MeV⁻¹)', fontsize=14)
        plt.grid(True, alpha=0.3)
        if args.output:
            plt.savefig(args.output, dpi=300, bbox_inches='tight')
            print(f"Saved to {args.output}")
        else:
            plt.show()


if __name__ == '__main__':
    main()

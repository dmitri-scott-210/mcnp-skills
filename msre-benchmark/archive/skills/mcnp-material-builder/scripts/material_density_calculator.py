#!/usr/bin/env python3
"""
MCNP Material Density Calculator

Purpose: Calculate atomic densities, weight fractions, and temperature conversions
         for MCNP material definitions.

Features:
  - Mass density → atomic density conversion
  - Atomic fractions → weight fractions conversion
  - Weight fractions → atomic fractions conversion
  - Composition normalization
  - Temperature conversion (K ↔ MeV)

Usage:
  python material_density_calculator.py

Or import as module:
  from material_density_calculator import *

Author: MCNP Material Builder Skill
Version: 1.0
Date: 2025-11-03
"""

import sys
from typing import Dict, List, Tuple

# Physical constants
AVOGADRO = 0.6022  # 10^24 atoms/mol (for MCNP atomic density units)
BOLTZMANN_MEV_PER_K = 8.617e-11  # MeV/K

# Common atomic masses (g/mol) - extend as needed
ATOMIC_MASSES = {
    1: 1.008,      # H
    2: 4.003,      # He
    6: 12.011,     # C
    7: 14.007,     # N
    8: 15.999,     # O
    11: 22.990,    # Na
    12: 24.305,    # Mg
    13: 26.982,    # Al
    14: 28.085,    # Si
    20: 40.078,    # Ca
    24: 51.996,    # Cr
    26: 55.845,    # Fe
    28: 58.693,    # Ni
    40: 91.224,    # Zr
    50: 118.710,   # Sn
    82: 207.2,     # Pb
    92: 238.029,   # U
}


def mass_density_to_atomic_density(mass_density_g_cm3: float,
                                   molecular_weight_g_mol: float,
                                   atoms_per_molecule: int = 1) -> float:
    """
    Convert mass density to atomic density for MCNP input.

    Formula: ρ_atomic [atoms/b-cm] = ρ_mass [g/cm³] × N_A [atoms/mol] / M [g/mol] × 10⁻²⁴
                                    = ρ_mass × 0.6022 / M

    Args:
        mass_density_g_cm3: Mass density in g/cm³
        molecular_weight_g_mol: Molecular weight in g/mol
        atoms_per_molecule: Number of atoms per molecule (for compound)

    Returns:
        Atomic density in atoms/b-cm (negative sign NOT included)

    Example:
        >>> mass_density_to_atomic_density(1.0, 18, 3)  # H₂O
        0.1003
    """
    atomic_density = (mass_density_g_cm3 * AVOGADRO / molecular_weight_g_mol) * atoms_per_molecule
    return atomic_density


def atomic_fractions_to_weight_fractions(atomic_fractions: Dict[int, float]) -> Dict[int, float]:
    """
    Convert atomic fractions to weight fractions.

    Args:
        atomic_fractions: Dictionary {Z: atomic_fraction} or {Z: atom_count}

    Returns:
        Dictionary {Z: weight_fraction} (negative values for MCNP)

    Example:
        >>> atomic_fractions_to_weight_fractions({1: 2, 8: 1})  # H₂O
        {1: -0.1119, 8: -0.8881}
    """
    # Calculate total mass
    total_mass = sum(count * ATOMIC_MASSES.get(Z, 0) for Z, count in atomic_fractions.items())

    if total_mass == 0:
        raise ValueError("Total mass is zero. Check atomic numbers.")

    # Calculate weight fractions (negative for MCNP)
    weight_fractions = {Z: -(count * ATOMIC_MASSES.get(Z, 0) / total_mass)
                        for Z, count in atomic_fractions.items()}

    return weight_fractions


def weight_fractions_to_atomic_fractions(weight_fractions: Dict[int, float]) -> Dict[int, float]:
    """
    Convert weight fractions to atomic fractions (normalized).

    Args:
        weight_fractions: Dictionary {Z: weight_fraction} (negative values)

    Returns:
        Dictionary {Z: atomic_fraction} (positive, normalized)

    Example:
        >>> weight_fractions_to_atomic_fractions({1: -0.1119, 8: -0.8881})
        {1: 0.6667, 8: 0.3333}
    """
    # Convert weight fractions to atomic counts
    atomic_counts = {Z: abs(wf) / ATOMIC_MASSES.get(Z, 1)
                     for Z, wf in weight_fractions.items()}

    # Normalize
    total = sum(atomic_counts.values())
    atomic_fractions = {Z: count / total for Z, count in atomic_counts.items()}

    return atomic_fractions


def normalize_fractions(fractions: Dict[int, float], target_sum: float = 1.0) -> Dict[int, float]:
    """
    Normalize fractions to sum to target value.

    Args:
        fractions: Dictionary {Z: fraction}
        target_sum: Target sum (1.0 for atomic, -1.0 for weight)

    Returns:
        Normalized dictionary {Z: fraction}

    Example:
        >>> normalize_fractions({1: 2, 8: 1})
        {1: 0.6667, 8: 0.3333}
    """
    current_sum = sum(fractions.values())

    if current_sum == 0:
        raise ValueError("Cannot normalize: sum is zero.")

    factor = target_sum / current_sum
    normalized = {Z: frac * factor for Z, frac in fractions.items()}

    return normalized


def temperature_K_to_MeV(temperature_K: float) -> float:
    """
    Convert temperature from Kelvin to MeV for MCNP TMP card.

    Formula: T [MeV] = T [K] × 8.617×10⁻¹¹

    Args:
        temperature_K: Temperature in Kelvin

    Returns:
        Temperature in MeV

    Example:
        >>> temperature_K_to_MeV(293.6)
        2.53e-08
    """
    return temperature_K * BOLTZMANN_MEV_PER_K


def temperature_MeV_to_K(temperature_MeV: float) -> float:
    """
    Convert temperature from MeV to Kelvin.

    Formula: T [K] = T [MeV] / 8.617×10⁻¹¹

    Args:
        temperature_MeV: Temperature in MeV

    Returns:
        Temperature in Kelvin

    Example:
        >>> temperature_MeV_to_K(2.53e-08)
        293.6
    """
    return temperature_MeV / BOLTZMANN_MEV_PER_K


def calculate_compound_molecular_weight(composition: Dict[int, int]) -> float:
    """
    Calculate molecular weight of compound from atomic composition.

    Args:
        composition: Dictionary {Z: atom_count}

    Returns:
        Molecular weight in g/mol

    Example:
        >>> calculate_compound_molecular_weight({1: 2, 8: 1})  # H₂O
        18.015
    """
    molecular_weight = sum(count * ATOMIC_MASSES.get(Z, 0)
                          for Z, count in composition.items())
    return molecular_weight


def generate_material_card(material_num: int,
                          composition: Dict[int, float],
                          density: float,
                          use_atomic: bool = True,
                          library_suffix: str = "80c",
                          comment: str = "") -> str:
    """
    Generate MCNP M card text from composition.

    Args:
        material_num: Material number
        composition: Dictionary {Z: fraction}
        density: Density value (sign determined by use_atomic)
        use_atomic: True for atomic fractions, False for weight
        library_suffix: Library identifier (e.g., "80c")
        comment: Optional comment

    Returns:
        String containing M card

    Example:
        >>> generate_material_card(1, {1: 2, 8: 1}, 0.1003, True, "80c", "H2O")
        M1   1001.80c  2  8016.80c  1          $ H2O
    """
    # Format density with correct sign
    density_str = f"{-density if use_atomic else density:.6g}"

    # Build M card
    zaids = []
    for Z, fraction in composition.items():
        zaid = f"{Z:03d}000" if Z < 100 else f"{Z:04d}00"
        if Z == 1:
            zaid = "1001"  # H-1
        fraction_str = f"{fraction:.6g}" if use_atomic else f"{fraction:.6g}"
        zaids.append(f"{zaid}.{library_suffix}  {fraction_str}")

    m_card = f"M{material_num}   " + "  ".join(zaids)
    if comment:
        m_card += f"          $ {comment}"

    return m_card


# Interactive mode
def interactive_mode():
    """
    Interactive calculator for material properties.
    """
    print("=" * 70)
    print("MCNP Material Density Calculator")
    print("=" * 70)
    print()
    print("Select operation:")
    print("  1. Mass density → Atomic density")
    print("  2. Atomic fractions → Weight fractions")
    print("  3. Weight fractions → Atomic fractions")
    print("  4. Normalize fractions")
    print("  5. Temperature K → MeV")
    print("  6. Temperature MeV → K")
    print("  7. Calculate molecular weight")
    print("  8. Generate M card")
    print("  0. Exit")
    print()

    while True:
        try:
            choice = input("Enter choice (0-8): ").strip()

            if choice == "0":
                print("Exiting.")
                break

            elif choice == "1":
                mass_dens = float(input("Mass density (g/cm³): "))
                mol_weight = float(input("Molecular weight (g/mol): "))
                atoms_per_mol = int(input("Atoms per molecule: "))
                result = mass_density_to_atomic_density(mass_dens, mol_weight, atoms_per_mol)
                print(f"Atomic density: {result:.6f} atoms/b-cm")
                print(f"MCNP cell card density: -{result:.6f}")
                print()

            elif choice == "2":
                print("Enter atomic composition (e.g., H2O: Z=1,count=2; Z=8,count=1)")
                composition = {}
                while True:
                    z_input = input("  Atomic number Z (enter to finish): ").strip()
                    if not z_input:
                        break
                    Z = int(z_input)
                    count = float(input(f"  Count for Z={Z}: "))
                    composition[Z] = count

                weight_frac = atomic_fractions_to_weight_fractions(composition)
                print("Weight fractions:")
                for Z, wf in weight_frac.items():
                    print(f"  Z={Z}: {wf:.6f}")
                print(f"Sum: {sum(weight_frac.values()):.6f} (should be -1.0)")
                print()

            elif choice == "3":
                print("Enter weight fractions (negative values)")
                composition = {}
                while True:
                    z_input = input("  Atomic number Z (enter to finish): ").strip()
                    if not z_input:
                        break
                    Z = int(z_input)
                    wf = float(input(f"  Weight fraction for Z={Z}: "))
                    composition[Z] = wf

                atomic_frac = weight_fractions_to_atomic_fractions(composition)
                print("Atomic fractions:")
                for Z, af in atomic_frac.items():
                    print(f"  Z={Z}: {af:.6f}")
                print(f"Sum: {sum(atomic_frac.values()):.6f} (should be 1.0)")
                print()

            elif choice == "4":
                print("Enter fractions to normalize")
                composition = {}
                while True:
                    z_input = input("  Atomic number Z (enter to finish): ").strip()
                    if not z_input:
                        break
                    Z = int(z_input)
                    frac = float(input(f"  Fraction for Z={Z}: "))
                    composition[Z] = frac

                target = float(input("Target sum (1.0 or -1.0): "))
                normalized = normalize_fractions(composition, target)
                print("Normalized fractions:")
                for Z, nf in normalized.items():
                    print(f"  Z={Z}: {nf:.6f}")
                print(f"Sum: {sum(normalized.values()):.6f}")
                print()

            elif choice == "5":
                temp_K = float(input("Temperature (K): "))
                temp_MeV = temperature_K_to_MeV(temp_K)
                print(f"Temperature: {temp_MeV:.6e} MeV")
                print(f"MCNP TMP card: TMP{input('Material number: ')}  {temp_MeV:.6e}")
                print()

            elif choice == "6":
                temp_MeV = float(input("Temperature (MeV): "))
                temp_K = temperature_MeV_to_K(temp_MeV)
                print(f"Temperature: {temp_K:.2f} K ({temp_K-273.15:.2f} °C)")
                print()

            elif choice == "7":
                print("Enter atomic composition")
                composition = {}
                while True:
                    z_input = input("  Atomic number Z (enter to finish): ").strip()
                    if not z_input:
                        break
                    Z = int(z_input)
                    count = int(input(f"  Count for Z={Z}: "))
                    composition[Z] = count

                mol_weight = calculate_compound_molecular_weight(composition)
                print(f"Molecular weight: {mol_weight:.3f} g/mol")
                print()

            elif choice == "8":
                mat_num = int(input("Material number: "))
                print("Enter composition")
                composition = {}
                while True:
                    z_input = input("  Atomic number Z (enter to finish): ").strip()
                    if not z_input:
                        break
                    Z = int(z_input)
                    frac = float(input(f"  Fraction for Z={Z}: "))
                    composition[Z] = frac

                density = float(input("Density value: "))
                use_atomic = input("Use atomic fractions? (y/n): ").strip().lower() == 'y'
                lib_suffix = input("Library suffix (default 80c): ").strip() or "80c"
                comment = input("Comment (optional): ").strip()

                m_card = generate_material_card(mat_num, composition, density,
                                               use_atomic, lib_suffix, comment)
                print("\nM card:")
                print(m_card)
                print()

            else:
                print("Invalid choice. Try again.")
                print()

        except ValueError as e:
            print(f"Error: {e}")
            print()
        except KeyboardInterrupt:
            print("\nExiting.")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(__doc__)
        sys.exit(0)

    interactive_mode()

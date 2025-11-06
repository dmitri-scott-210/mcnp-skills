#!/usr/bin/env python3
"""
MCNP Unit-Aware Calculator

Scientific calculator with automatic unit handling for MCNP physics calculations.
Performs common calculations using physical constants with proper unit tracking.

Usage:
    Interactive mode:
        python unit_aware_calculator.py

    Command-line mode:
        python unit_aware_calculator.py --calc "atom_density" --density 7.85 --mass 55.845
        python unit_aware_calculator.py --calc "thermal_energy" --temperature 600
        python unit_aware_calculator.py --calc "neutron_speed" --energy 0.0253 --energy-unit eV

Dependencies:
    None (pure stdlib)

Author: MCNP Skills Project
Date: 2025-11-06
Version: 2.0.0
"""

import argparse
import math
import sys
from typing import Dict, Tuple, Optional, Any


class PhysicalConstants:
    """Physical constants for calculations."""

    # CODATA 2018 values
    c = 2.99792458e10  # cm/s
    h = 6.62607015e-34  # J·s
    hbar = 1.054571817e-34  # J·s
    k_B_J = 1.380649e-23  # J/K
    k_B_eV = 8.617333262e-5  # eV/K
    k_B_MeV = 8.617333262e-11  # MeV/K
    e = 1.602176634e-19  # C
    N_A = 6.02214076e23  # 1/mol
    amu_to_MeV = 931.49410242  # MeV/c²
    eV_to_J = 1.602176634e-19  # J

    # Particle masses
    m_e_kg = 9.1093837015e-31  # kg
    m_e_MeV = 0.51099895000  # MeV/c²
    m_p_kg = 1.67262192369e-27  # kg
    m_p_MeV = 938.27208816  # MeV/c²
    m_n_kg = 1.67492749804e-27  # kg
    m_n_MeV = 939.56542052  # MeV/c²
    m_n_amu = 1.00866491595  # amu

    # Useful constants
    barn = 1.0e-24  # cm²


class UnitConverter:
    """Unit conversion utilities."""

    @staticmethod
    def energy_to_joules(value: float, unit: str) -> float:
        """Convert energy to joules."""
        conversions = {
            "J": 1.0,
            "eV": PhysicalConstants.eV_to_J,
            "keV": 1e3 * PhysicalConstants.eV_to_J,
            "MeV": 1e6 * PhysicalConstants.eV_to_J,
            "GeV": 1e9 * PhysicalConstants.eV_to_J,
        }
        if unit not in conversions:
            raise ValueError(f"Unknown energy unit: {unit}")
        return value * conversions[unit]

    @staticmethod
    def energy_to_mev(value: float, unit: str) -> float:
        """Convert energy to MeV."""
        j_value = UnitConverter.energy_to_joules(value, unit)
        return j_value / PhysicalConstants.eV_to_J / 1e6

    @staticmethod
    def temperature_to_kelvin(value: float, unit: str) -> float:
        """Convert temperature to Kelvin."""
        conversions = {
            "K": lambda x: x,
            "C": lambda x: x + 273.15,
            "F": lambda x: (x - 32) * 5/9 + 273.15,
        }
        if unit not in conversions:
            raise ValueError(f"Unknown temperature unit: {unit}")
        return conversions[unit](value)


class MCNPCalculator:
    """Calculator for common MCNP physics calculations."""

    def __init__(self):
        """Initialize calculator."""
        self.constants = PhysicalConstants()
        self.converter = UnitConverter()

    def atom_density(self, mass_density: float, atomic_mass: float) -> Dict[str, Any]:
        """
        Calculate atom density from mass density.

        Args:
            mass_density: Mass density in g/cm³
            atomic_mass: Atomic mass in g/mol (or amu)

        Returns:
            Dict with results
        """
        # N = (ρ × N_A) / A
        N_atoms_per_cm3 = (mass_density * self.constants.N_A) / atomic_mass
        N_atoms_per_barn_cm = N_atoms_per_cm3 / 1e24

        return {
            "atom_density_atoms_per_cm3": N_atoms_per_cm3,
            "atom_density_atoms_per_barn_cm": N_atoms_per_barn_cm,
            "mass_density_g_per_cm3": mass_density,
            "atomic_mass_g_per_mol": atomic_mass,
        }

    def thermal_energy(self, temperature: float, temp_unit: str = "K") -> Dict[str, Any]:
        """
        Calculate thermal energy from temperature.

        Args:
            temperature: Temperature value
            temp_unit: Temperature unit (K, C, F)

        Returns:
            Dict with results
        """
        T_kelvin = self.converter.temperature_to_kelvin(temperature, temp_unit)

        E_J = self.constants.k_B_J * T_kelvin
        E_eV = self.constants.k_B_eV * T_kelvin
        E_MeV = self.constants.k_B_MeV * T_kelvin

        return {
            "temperature_K": T_kelvin,
            "thermal_energy_J": E_J,
            "thermal_energy_eV": E_eV,
            "thermal_energy_MeV": E_MeV,
        }

    def neutron_speed(self, energy: float, energy_unit: str = "MeV") -> Dict[str, Any]:
        """
        Calculate neutron speed from kinetic energy (non-relativistic).

        Args:
            energy: Kinetic energy value
            energy_unit: Energy unit (J, eV, keV, MeV, GeV)

        Returns:
            Dict with results
        """
        E_J = self.converter.energy_to_joules(energy, energy_unit)
        E_MeV = self.converter.energy_to_mev(energy, energy_unit)

        # v = sqrt(2E/m) (non-relativistic)
        v_m_per_s = math.sqrt(2 * E_J / self.constants.m_n_kg)
        v_cm_per_s = v_m_per_s * 100

        # De Broglie wavelength
        lambda_m = self.constants.h / (self.constants.m_n_kg * v_m_per_s)
        lambda_angstrom = lambda_m * 1e10

        # Check if relativistic correction needed (v > 0.1c)
        relativistic = v_m_per_s > (0.1 * self.constants.c / 100)

        return {
            "energy_MeV": E_MeV,
            "speed_m_per_s": v_m_per_s,
            "speed_cm_per_s": v_cm_per_s,
            "wavelength_angstrom": lambda_angstrom,
            "relativistic_warning": relativistic,
        }

    def q_value(self, reactant_masses: list, product_masses: list) -> Dict[str, Any]:
        """
        Calculate Q-value for nuclear reaction.

        Args:
            reactant_masses: List of reactant masses in amu
            product_masses: List of product masses in amu

        Returns:
            Dict with results
        """
        total_reactant = sum(reactant_masses)
        total_product = sum(product_masses)
        mass_defect = total_reactant - total_product

        Q_MeV = mass_defect * self.constants.amu_to_MeV

        reaction_type = "exothermic" if Q_MeV > 0 else "endothermic"

        return {
            "Q_value_MeV": Q_MeV,
            "mass_defect_amu": mass_defect,
            "reaction_type": reaction_type,
            "reactants_total_amu": total_reactant,
            "products_total_amu": total_product,
        }

    def binding_energy(self, Z: int, N: int, nuclear_mass: float) -> Dict[str, Any]:
        """
        Calculate nuclear binding energy.

        Args:
            Z: Number of protons
            N: Number of neutrons
            nuclear_mass: Actual nuclear mass in amu

        Returns:
            Dict with results
        """
        # Calculate mass of constituents
        m_p_amu = self.constants.m_p_MeV / self.constants.amu_to_MeV
        m_n_amu = self.constants.m_n_amu

        constituent_mass = Z * m_p_amu + N * m_n_amu
        mass_defect = constituent_mass - nuclear_mass

        E_B = mass_defect * self.constants.amu_to_MeV
        A = Z + N
        E_B_per_nucleon = E_B / A if A > 0 else 0

        return {
            "binding_energy_MeV": E_B,
            "binding_energy_per_nucleon_MeV": E_B_per_nucleon,
            "mass_defect_amu": mass_defect,
            "mass_number_A": A,
            "constituent_mass_amu": constituent_mass,
            "actual_mass_amu": nuclear_mass,
        }

    def fission_rate_from_power(self, power_watts: float, energy_per_fission: float = 200.0) -> Dict[str, Any]:
        """
        Calculate fission rate from thermal power.

        Args:
            power_watts: Thermal power in watts
            energy_per_fission: Energy released per fission in MeV (default 200 MeV)

        Returns:
            Dict with results
        """
        # Convert power to MeV/s
        power_MeV_per_s = power_watts / (self.constants.eV_to_J * 1e6)

        # Fission rate
        fissions_per_second = power_MeV_per_s / energy_per_fission

        # Fuel consumption (U-235)
        mass_u235_per_mol = 235.0  # g/mol
        mass_consumed_g_per_s = (fissions_per_second * mass_u235_per_mol) / self.constants.N_A
        mass_consumed_g_per_day = mass_consumed_g_per_s * 86400

        return {
            "power_watts": power_watts,
            "power_MW": power_watts / 1e6,
            "fissions_per_second": fissions_per_second,
            "energy_per_fission_MeV": energy_per_fission,
            "fuel_consumption_g_per_day": mass_consumed_g_per_day,
        }

    def decay_constant(self, half_life: float, time_unit: str = "s") -> Dict[str, Any]:
        """
        Calculate decay constant from half-life.

        Args:
            half_life: Half-life value
            time_unit: Time unit (s, min, h, d, y)

        Returns:
            Dict with results
        """
        # Convert to seconds
        time_conversions = {
            "s": 1.0,
            "min": 60.0,
            "h": 3600.0,
            "d": 86400.0,
            "y": 365.25 * 86400.0,
        }

        if time_unit not in time_conversions:
            raise ValueError(f"Unknown time unit: {time_unit}")

        half_life_s = half_life * time_conversions[time_unit]

        # λ = ln(2) / t_1/2
        lambda_per_s = math.log(2) / half_life_s
        mean_lifetime_s = 1.0 / lambda_per_s

        return {
            "half_life_s": half_life_s,
            "decay_constant_per_s": lambda_per_s,
            "mean_lifetime_s": mean_lifetime_s,
            "half_life_input": half_life,
            "time_unit_input": time_unit,
        }

    def specific_activity(self, atomic_mass: float, half_life_s: float) -> Dict[str, Any]:
        """
        Calculate specific activity.

        Args:
            atomic_mass: Atomic mass in g/mol
            half_life_s: Half-life in seconds

        Returns:
            Dict with results
        """
        # A_specific = (ln(2) × N_A) / (t_1/2 × A)
        lambda_decay = math.log(2) / half_life_s
        A_specific_Bq_per_g = (lambda_decay * self.constants.N_A) / atomic_mass
        A_specific_Ci_per_g = A_specific_Bq_per_g / 3.7e10

        return {
            "specific_activity_Bq_per_g": A_specific_Bq_per_g,
            "specific_activity_Ci_per_g": A_specific_Ci_per_g,
            "half_life_s": half_life_s,
            "atomic_mass_g_per_mol": atomic_mass,
        }

    def interactive_mode(self):
        """Run interactive calculator."""
        print("\n" + "="*70)
        print("MCNP UNIT-AWARE CALCULATOR")
        print("="*70)
        print("\nAvailable calculations:")
        print("  1. Atom density (from mass density)")
        print("  2. Thermal energy (from temperature)")
        print("  3. Neutron speed (from energy)")
        print("  4. Q-value (nuclear reaction)")
        print("  5. Binding energy")
        print("  6. Fission rate (from power)")
        print("  7. Decay constant (from half-life)")
        print("  8. Specific activity")
        print("\nType 'help' for detailed instructions, 'quit' to exit.")
        print("="*70 + "\n")

        while True:
            try:
                choice = input("Select calculation (1-8) or command> ").strip()

                if choice.lower() in ["quit", "exit", "q"]:
                    print("Exiting...")
                    break

                elif choice.lower() == "help":
                    print("\nEnter the number (1-8) for the calculation you want to perform.")
                    print("The calculator will prompt you for the required inputs.")
                    continue

                elif choice == "1":
                    self._calc_atom_density()
                elif choice == "2":
                    self._calc_thermal_energy()
                elif choice == "3":
                    self._calc_neutron_speed()
                elif choice == "4":
                    self._calc_q_value()
                elif choice == "5":
                    self._calc_binding_energy()
                elif choice == "6":
                    self._calc_fission_rate()
                elif choice == "7":
                    self._calc_decay_constant()
                elif choice == "8":
                    self._calc_specific_activity()
                else:
                    print("Invalid choice. Enter 1-8, 'help', or 'quit'.")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

    def _calc_atom_density(self):
        """Interactive atom density calculation."""
        print("\n--- Atom Density Calculation ---")
        density = float(input("Mass density (g/cm³): "))
        mass = float(input("Atomic mass (g/mol): "))

        result = self.atom_density(density, mass)
        print(f"\nResults:")
        print(f"  Atom density: {result['atom_density_atoms_per_cm3']:.4e} atoms/cm³")
        print(f"  Atom density: {result['atom_density_atoms_per_barn_cm']:.6f} atoms/b-cm")
        print(f"\nMCNP material card (atom density):")
        print(f"  M#  ZZZAAA.##c  {result['atom_density_atoms_per_barn_cm']:.6f}\n")

    def _calc_thermal_energy(self):
        """Interactive thermal energy calculation."""
        print("\n--- Thermal Energy Calculation ---")
        temp = float(input("Temperature: "))
        unit = input("Unit (K/C/F) [K]: ").strip() or "K"

        result = self.thermal_energy(temp, unit)
        print(f"\nResults:")
        print(f"  Temperature: {result['temperature_K']:.2f} K")
        print(f"  Thermal energy: {result['thermal_energy_eV']:.4e} eV")
        print(f"  Thermal energy: {result['thermal_energy_MeV']:.4e} MeV")
        print(f"\nMCNP TMP card:")
        print(f"  TMP  {result['temperature_K']:.2f}    $ Temperature in Kelvin\n")

    def _calc_neutron_speed(self):
        """Interactive neutron speed calculation."""
        print("\n--- Neutron Speed Calculation ---")
        energy = float(input("Energy: "))
        unit = input("Unit (eV/keV/MeV) [MeV]: ").strip() or "MeV"

        result = self.neutron_speed(energy, unit)
        print(f"\nResults:")
        print(f"  Energy: {result['energy_MeV']:.6f} MeV")
        print(f"  Speed: {result['speed_m_per_s']:.4e} m/s")
        print(f"  Wavelength: {result['wavelength_angstrom']:.4e} Å")
        if result['relativistic_warning']:
            print(f"  WARNING: Relativistic correction may be needed (v > 0.1c)\n")
        else:
            print()

    def _calc_q_value(self):
        """Interactive Q-value calculation."""
        print("\n--- Q-Value Calculation ---")
        print("Enter reactant masses (amu), one per line. Empty line to finish:")
        reactants = []
        while True:
            mass_str = input(f"  Reactant {len(reactants)+1}: ").strip()
            if not mass_str:
                break
            reactants.append(float(mass_str))

        print("Enter product masses (amu), one per line. Empty line to finish:")
        products = []
        while True:
            mass_str = input(f"  Product {len(products)+1}: ").strip()
            if not mass_str:
                break
            products.append(float(mass_str))

        result = self.q_value(reactants, products)
        print(f"\nResults:")
        print(f"  Q-value: {result['Q_value_MeV']:.4f} MeV ({result['reaction_type']})")
        print(f"  Mass defect: {result['mass_defect_amu']:.6f} amu\n")

    def _calc_binding_energy(self):
        """Interactive binding energy calculation."""
        print("\n--- Binding Energy Calculation ---")
        Z = int(input("Number of protons (Z): "))
        N = int(input("Number of neutrons (N): "))
        mass = float(input("Nuclear mass (amu): "))

        result = self.binding_energy(Z, N, mass)
        print(f"\nResults:")
        print(f"  Binding energy: {result['binding_energy_MeV']:.4f} MeV")
        print(f"  B.E. per nucleon: {result['binding_energy_per_nucleon_MeV']:.4f} MeV/nucleon")
        print(f"  Mass defect: {result['mass_defect_amu']:.6f} amu\n")

    def _calc_fission_rate(self):
        """Interactive fission rate calculation."""
        print("\n--- Fission Rate from Power ---")
        power = float(input("Thermal power (watts): "))
        energy = float(input("Energy per fission (MeV) [200]: ").strip() or "200")

        result = self.fission_rate_from_power(power, energy)
        print(f"\nResults:")
        print(f"  Power: {result['power_MW']:.4f} MW")
        print(f"  Fission rate: {result['fissions_per_second']:.4e} fissions/s")
        print(f"  Fuel consumption: {result['fuel_consumption_g_per_day']:.4f} g/day\n")

    def _calc_decay_constant(self):
        """Interactive decay constant calculation."""
        print("\n--- Decay Constant from Half-Life ---")
        half_life = float(input("Half-life: "))
        unit = input("Unit (s/min/h/d/y): ").strip()

        result = self.decay_constant(half_life, unit)
        print(f"\nResults:")
        print(f"  Half-life: {result['half_life_s']:.4e} s")
        print(f"  Decay constant: {result['decay_constant_per_s']:.4e} /s")
        print(f"  Mean lifetime: {result['mean_lifetime_s']:.4e} s\n")

    def _calc_specific_activity(self):
        """Interactive specific activity calculation."""
        print("\n--- Specific Activity ---")
        mass = float(input("Atomic mass (g/mol): "))
        half_life = float(input("Half-life (seconds): "))

        result = self.specific_activity(mass, half_life)
        print(f"\nResults:")
        print(f"  Specific activity: {result['specific_activity_Bq_per_g']:.4e} Bq/g")
        print(f"  Specific activity: {result['specific_activity_Ci_per_g']:.4e} Ci/g\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MCNP Unit-Aware Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python unit_aware_calculator.py

  Atom density:
    python unit_aware_calculator.py --calc atom_density --density 7.85 --mass 55.845

  Thermal energy:
    python unit_aware_calculator.py --calc thermal_energy --temperature 600

  Neutron speed:
    python unit_aware_calculator.py --calc neutron_speed --energy 0.0253 --energy-unit eV
        """
    )

    parser.add_argument(
        "--calc", "-c",
        choices=["atom_density", "thermal_energy", "neutron_speed"],
        help="Calculation type"
    )
    parser.add_argument("--density", type=float, help="Mass density (g/cm³)")
    parser.add_argument("--mass", type=float, help="Atomic mass (g/mol)")
    parser.add_argument("--temperature", type=float, help="Temperature")
    parser.add_argument("--temp-unit", default="K", help="Temperature unit (K/C/F)")
    parser.add_argument("--energy", type=float, help="Energy")
    parser.add_argument("--energy-unit", default="MeV", help="Energy unit (eV/keV/MeV)")

    args = parser.parse_args()

    calc = MCNPCalculator()

    if args.calc:
        # Command-line mode
        if args.calc == "atom_density":
            if not (args.density and args.mass):
                print("Error: --density and --mass required for atom_density")
                sys.exit(1)
            result = calc.atom_density(args.density, args.mass)
            print(f"Atom density: {result['atom_density_atoms_per_barn_cm']:.6f} atoms/b-cm")

        elif args.calc == "thermal_energy":
            if not args.temperature:
                print("Error: --temperature required for thermal_energy")
                sys.exit(1)
            result = calc.thermal_energy(args.temperature, args.temp_unit)
            print(f"Thermal energy: {result['thermal_energy_MeV']:.6e} MeV")

        elif args.calc == "neutron_speed":
            if not args.energy:
                print("Error: --energy required for neutron_speed")
                sys.exit(1)
            result = calc.neutron_speed(args.energy, args.energy_unit)
            print(f"Neutron speed: {result['speed_m_per_s']:.4e} m/s")
    else:
        # Interactive mode
        calc.interactive_mode()


if __name__ == "__main__":
    main()

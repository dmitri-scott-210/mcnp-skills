#!/usr/bin/env python3
"""
MCNP Physical Constants Lookup Tool

Interactive and command-line tool for searching and retrieving fundamental
physical constants, particle properties, and nuclear data used in MCNP calculations.

Based on CODATA 2018 recommended values and Particle Data Group (PDG) 2020 values.

Usage:
    Interactive mode:
        python constants_lookup.py

    Command-line mode:
        python constants_lookup.py --search "avogadro"
        python constants_lookup.py --constant "speed_of_light"
        python constants_lookup.py --particle "neutron"
        python constants_lookup.py --list

    Examples:
        python constants_lookup.py --search "planck"
        python constants_lookup.py --particle "electron" --property "mass"
        python constants_lookup.py --constant "boltzmann_constant" --unit "eV/K"

Dependencies:
    None (pure stdlib)

Author: MCNP Skills Project
Date: 2025-11-06
Version: 2.0.0
"""

import argparse
import sys
import re
from typing import Dict, List, Tuple, Optional, Any


class PhysicalConstants:
    """Database of fundamental physical constants (CODATA 2018)."""

    def __init__(self):
        """Initialize constants database."""
        self.constants = {
            # Universal constants
            "speed_of_light": {
                "symbol": "c",
                "value": 2.99792458e10,
                "unit": "cm/s",
                "uncertainty": 0.0,  # Exact by definition
                "alt_values": {
                    "m/s": 2.99792458e8,
                },
                "description": "Speed of light in vacuum (exact by definition)"
            },
            "planck_constant": {
                "symbol": "h",
                "value": 6.62607015e-34,
                "unit": "J·s",
                "uncertainty": 0.0,  # Exact by definition
                "alt_values": {
                    "eV·s": 4.135667696e-15,
                },
                "description": "Planck constant (exact by definition since 2019)"
            },
            "reduced_planck_constant": {
                "symbol": "ℏ",
                "value": 1.054571817e-34,
                "unit": "J·s",
                "uncertainty": 0.0,
                "alt_values": {
                    "eV·s": 6.582119569e-16,
                    "MeV·fm": 197.3269804,
                },
                "description": "Reduced Planck constant (h-bar = h/2π)"
            },
            "boltzmann_constant": {
                "symbol": "k_B",
                "value": 1.380649e-23,
                "unit": "J/K",
                "uncertainty": 0.0,  # Exact by definition
                "alt_values": {
                    "eV/K": 8.617333262e-5,
                    "MeV/K": 8.617333262e-11,
                },
                "description": "Boltzmann constant (exact by definition since 2019)"
            },
            "elementary_charge": {
                "symbol": "e",
                "value": 1.602176634e-19,
                "unit": "C",
                "uncertainty": 0.0,  # Exact by definition
                "description": "Elementary charge (exact by definition since 2019)"
            },
            "avogadro_constant": {
                "symbol": "N_A",
                "value": 6.02214076e23,
                "unit": "1/mol",
                "uncertainty": 0.0,  # Exact by definition
                "description": "Avogadro constant (exact by definition since 2019)"
            },
            # Gravitational constant
            "gravitational_constant": {
                "symbol": "G",
                "value": 6.67430e-11,
                "unit": "m³/(kg·s²)",
                "uncertainty": 1.5e-15,
                "alt_values": {
                    "cm³/(g·s²)": 6.67430e-8,
                },
                "description": "Newtonian gravitational constant"
            },
            # Electromagnetic constants
            "permittivity_vacuum": {
                "symbol": "ε₀",
                "value": 8.8541878128e-12,
                "unit": "F/m",
                "uncertainty": 1.3e-21,
                "description": "Permittivity of free space (electric constant)"
            },
            "permeability_vacuum": {
                "symbol": "μ₀",
                "value": 1.25663706212e-6,
                "unit": "N/A²",
                "uncertainty": 1.9e-16,
                "description": "Permeability of free space (magnetic constant)"
            },
            "fine_structure_constant": {
                "symbol": "α",
                "value": 7.2973525693e-3,
                "unit": "dimensionless",
                "uncertainty": 1.1e-12,
                "alt_values": {
                    "inverse": 137.035999084,
                },
                "description": "Fine structure constant (≈ 1/137)"
            },
            # Energy conversion
            "atomic_mass_unit": {
                "symbol": "u (amu)",
                "value": 1.66053906660e-27,
                "unit": "kg",
                "uncertainty": 5.0e-37,
                "alt_values": {
                    "g": 1.66053906660e-24,
                    "MeV/c²": 931.49410242,
                },
                "description": "Atomic mass unit (unified, 1/12 of C-12 mass)"
            },
            "electron_volt": {
                "symbol": "eV",
                "value": 1.602176634e-19,
                "unit": "J",
                "uncertainty": 0.0,  # Exact (same as elementary charge)
                "description": "Electron volt in joules"
            },
        }

    def search(self, query: str) -> List[str]:
        """
        Search for constants matching query.

        Args:
            query: Search string (case-insensitive)

        Returns:
            List of matching constant names
        """
        query_lower = query.lower()
        matches = []

        for name, data in self.constants.items():
            # Search in name
            if query_lower in name.lower():
                matches.append(name)
                continue

            # Search in description
            if query_lower in data.get("description", "").lower():
                matches.append(name)
                continue

            # Search in symbol
            if query_lower in data.get("symbol", "").lower():
                matches.append(name)

        return matches

    def get(self, name: str, unit: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get constant data.

        Args:
            name: Constant name
            unit: Optional unit (returns value in this unit if available)

        Returns:
            Dictionary with constant data, or None if not found
        """
        if name not in self.constants:
            return None

        data = self.constants[name].copy()

        # If specific unit requested, convert
        if unit and unit != data["unit"]:
            alt_values = data.get("alt_values", {})
            if unit in alt_values:
                data["value"] = alt_values[unit]
                data["unit"] = unit

        return data

    def list_all(self) -> List[str]:
        """Return list of all constant names."""
        return sorted(self.constants.keys())


class ParticleProperties:
    """Database of particle masses and properties."""

    def __init__(self):
        """Initialize particle properties database."""
        self.particles = {
            # Leptons
            "electron": {
                "symbol": "e⁻",
                "mass_kg": 9.1093837015e-31,
                "mass_amu": 5.48579909065e-4,
                "mass_MeV": 0.51099895000,
                "charge": -1,
                "spin": 0.5,
                "description": "Electron (stable lepton)"
            },
            "positron": {
                "symbol": "e⁺",
                "mass_kg": 9.1093837015e-31,
                "mass_amu": 5.48579909065e-4,
                "mass_MeV": 0.51099895000,
                "charge": +1,
                "spin": 0.5,
                "description": "Positron (antielectron)"
            },
            "muon": {
                "symbol": "μ⁻",
                "mass_kg": 1.883531627e-28,
                "mass_amu": 0.1134289259,
                "mass_MeV": 105.6583755,
                "charge": -1,
                "spin": 0.5,
                "half_life_s": 2.1969811e-6,
                "description": "Muon (unstable lepton, mean life 2.2 μs)"
            },
            # Nucleons
            "proton": {
                "symbol": "p",
                "mass_kg": 1.67262192369e-27,
                "mass_amu": 1.007276466621,
                "mass_MeV": 938.27208816,
                "charge": +1,
                "spin": 0.5,
                "description": "Proton (stable nucleon)"
            },
            "neutron": {
                "symbol": "n",
                "mass_kg": 1.67492749804e-27,
                "mass_amu": 1.00866491595,
                "mass_MeV": 939.56542052,
                "charge": 0,
                "spin": 0.5,
                "half_life_s": 879.4,
                "description": "Neutron (unstable when free, t_1/2 = 879.4 s)"
            },
            # Light nuclei
            "deuteron": {
                "symbol": "d (²H)",
                "mass_kg": 3.3435837724e-27,
                "mass_amu": 2.013553212745,
                "mass_MeV": 1875.61294257,
                "charge": +1,
                "spin": 1,
                "description": "Deuteron (deuterium nucleus, stable)"
            },
            "triton": {
                "symbol": "t (³H)",
                "mass_kg": 5.0073567446e-27,
                "mass_amu": 3.01604927912,
                "mass_MeV": 2808.92113662,
                "charge": +1,
                "spin": 0.5,
                "half_life_s": 3.888e8,  # 12.32 years
                "description": "Triton (tritium nucleus, radioactive)"
            },
            "helium3": {
                "symbol": "³He",
                "mass_kg": 5.0064127862e-27,
                "mass_amu": 3.0160293201,
                "mass_MeV": 2808.39160743,
                "charge": +2,
                "spin": 0.5,
                "description": "Helium-3 nucleus (stable, rare)"
            },
            "alpha": {
                "symbol": "α (⁴He)",
                "mass_kg": 6.6446573357e-27,
                "mass_amu": 4.001506179129,
                "mass_MeV": 3727.3794066,
                "charge": +2,
                "spin": 0,
                "description": "Alpha particle (helium-4 nucleus, stable)"
            },
        }

    def search(self, query: str) -> List[str]:
        """Search for particles matching query."""
        query_lower = query.lower()
        matches = []

        for name, data in self.particles.items():
            if query_lower in name.lower():
                matches.append(name)
                continue
            if query_lower in data.get("description", "").lower():
                matches.append(name)
                continue
            if query_lower in data.get("symbol", "").lower():
                matches.append(name)

        return matches

    def get(self, name: str, property_name: Optional[str] = None) -> Optional[Any]:
        """
        Get particle properties.

        Args:
            name: Particle name
            property_name: Optional specific property (mass_MeV, charge, etc.)

        Returns:
            Full particle data dict, or specific property, or None
        """
        if name not in self.particles:
            return None

        data = self.particles[name]

        if property_name:
            return data.get(property_name)

        return data

    def list_all(self) -> List[str]:
        """Return list of all particle names."""
        return sorted(self.particles.keys())


class ConstantsLookup:
    """Main lookup interface combining constants and particles."""

    def __init__(self):
        """Initialize lookup tool."""
        self.constants = PhysicalConstants()
        self.particles = ParticleProperties()

    def search(self, query: str) -> Dict[str, List[str]]:
        """
        Search both constants and particles.

        Args:
            query: Search string

        Returns:
            Dict with 'constants' and 'particles' keys containing matches
        """
        return {
            "constants": self.constants.search(query),
            "particles": self.particles.search(query)
        }

    def display_constant(self, name: str, unit: Optional[str] = None):
        """Display constant information."""
        data = self.constants.get(name, unit)
        if not data:
            print(f"Constant '{name}' not found.")
            return

        print(f"\n{'='*70}")
        print(f"CONSTANT: {name}")
        print(f"{'='*70}")
        print(f"Symbol:      {data['symbol']}")
        print(f"Value:       {data['value']:.10e} {data['unit']}")
        if data['uncertainty'] > 0:
            print(f"Uncertainty: {data['uncertainty']:.2e}")
        else:
            print(f"Uncertainty: Exact (by definition)")
        print(f"Description: {data['description']}")

        # Show alternative units if available
        if "alt_values" in data and data["alt_values"]:
            print(f"\nAlternative units:")
            for alt_unit, alt_value in data["alt_values"].items():
                print(f"  {alt_value:.10e} {alt_unit}")
        print(f"{'='*70}\n")

    def display_particle(self, name: str):
        """Display particle information."""
        data = self.particles.get(name)
        if not data:
            print(f"Particle '{name}' not found.")
            return

        print(f"\n{'='*70}")
        print(f"PARTICLE: {name}")
        print(f"{'='*70}")
        print(f"Symbol:      {data['symbol']}")
        print(f"Mass (kg):   {data['mass_kg']:.10e} kg")
        print(f"Mass (amu):  {data['mass_amu']:.12f} amu")
        print(f"Mass (MeV):  {data['mass_MeV']:.9f} MeV/c²")
        print(f"Charge:      {data['charge']:+d} e")
        print(f"Spin:        {data['spin']}")
        if "half_life_s" in data:
            print(f"Half-life:   {data['half_life_s']:.6e} s")
        print(f"Description: {data['description']}")
        print(f"{'='*70}\n")

    def display_search_results(self, results: Dict[str, List[str]]):
        """Display search results."""
        print(f"\n{'='*70}")
        print("SEARCH RESULTS")
        print(f"{'='*70}")

        if results["constants"]:
            print(f"\nCONSTANTS ({len(results['constants'])} matches):")
            for i, name in enumerate(results["constants"], 1):
                print(f"  {i}. {name}")

        if results["particles"]:
            print(f"\nPARTICLES ({len(results['particles'])} matches):")
            for i, name in enumerate(results["particles"], 1):
                print(f"  {i}. {name}")

        if not results["constants"] and not results["particles"]:
            print("No matches found.")

        print(f"{'='*70}\n")

    def interactive_mode(self):
        """Run interactive lookup session."""
        print("\n" + "="*70)
        print("MCNP PHYSICAL CONSTANTS LOOKUP TOOL")
        print("="*70)
        print("\nCommands:")
        print("  search <query>       - Search constants and particles")
        print("  constant <name>      - Display constant information")
        print("  particle <name>      - Display particle information")
        print("  list constants       - List all constants")
        print("  list particles       - List all particles")
        print("  help                 - Show this help")
        print("  quit / exit          - Exit program")
        print("="*70 + "\n")

        while True:
            try:
                user_input = input("lookup> ").strip()

                if not user_input:
                    continue

                # Parse command
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()

                # Handle commands
                if command in ["quit", "exit", "q"]:
                    print("Exiting...")
                    break

                elif command == "help":
                    print("\nCommands:")
                    print("  search <query>       - Search constants and particles")
                    print("  constant <name>      - Display constant information")
                    print("  particle <name>      - Display particle information")
                    print("  list constants       - List all constants")
                    print("  list particles       - List all particles")
                    print("  help                 - Show this help")
                    print("  quit / exit          - Exit program\n")

                elif command == "search":
                    if len(parts) < 2:
                        print("Usage: search <query>")
                        continue
                    query = parts[1]
                    results = self.search(query)
                    self.display_search_results(results)

                elif command == "constant":
                    if len(parts) < 2:
                        print("Usage: constant <name>")
                        continue
                    name = parts[1]
                    self.display_constant(name)

                elif command == "particle":
                    if len(parts) < 2:
                        print("Usage: particle <name>")
                        continue
                    name = parts[1]
                    self.display_particle(name)

                elif command == "list":
                    if len(parts) < 2:
                        print("Usage: list [constants|particles]")
                        continue
                    list_type = parts[1].lower()
                    if list_type == "constants":
                        names = self.constants.list_all()
                        print(f"\nALL CONSTANTS ({len(names)}):")
                        for i, name in enumerate(names, 1):
                            print(f"  {i}. {name}")
                        print()
                    elif list_type == "particles":
                        names = self.particles.list_all()
                        print(f"\nALL PARTICLES ({len(names)}):")
                        for i, name in enumerate(names, 1):
                            print(f"  {i}. {name}")
                        print()
                    else:
                        print("Usage: list [constants|particles]")

                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MCNP Physical Constants Lookup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python constants_lookup.py

  Search for constants:
    python constants_lookup.py --search "avogadro"
    python constants_lookup.py --search "planck"

  Display specific constant:
    python constants_lookup.py --constant "speed_of_light"
    python constants_lookup.py --constant "boltzmann_constant" --unit "eV/K"

  Display particle properties:
    python constants_lookup.py --particle "neutron"
    python constants_lookup.py --particle "electron"

  List all:
    python constants_lookup.py --list
        """
    )

    parser.add_argument(
        "--search", "-s",
        metavar="QUERY",
        help="Search for constants/particles matching query"
    )
    parser.add_argument(
        "--constant", "-c",
        metavar="NAME",
        help="Display specific constant"
    )
    parser.add_argument(
        "--particle", "-p",
        metavar="NAME",
        help="Display specific particle"
    )
    parser.add_argument(
        "--unit", "-u",
        metavar="UNIT",
        help="Unit for constant value (if available)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all constants and particles"
    )
    parser.add_argument(
        "--property",
        metavar="PROP",
        help="Specific particle property to retrieve (mass_MeV, charge, etc.)"
    )

    args = parser.parse_args()

    lookup = ConstantsLookup()

    # Command-line mode
    if args.search:
        results = lookup.search(args.search)
        lookup.display_search_results(results)

    elif args.constant:
        lookup.display_constant(args.constant, args.unit)

    elif args.particle:
        if args.property:
            value = lookup.particles.get(args.particle, args.property)
            if value is not None:
                print(f"{args.particle}.{args.property} = {value}")
            else:
                print(f"Particle '{args.particle}' or property '{args.property}' not found.")
        else:
            lookup.display_particle(args.particle)

    elif args.list:
        print(f"\nALL CONSTANTS ({len(lookup.constants.list_all())}):")
        for i, name in enumerate(lookup.constants.list_all(), 1):
            print(f"  {i}. {name}")

        print(f"\nALL PARTICLES ({len(lookup.particles.list_all())}):")
        for i, name in enumerate(lookup.particles.list_all(), 1):
            print(f"  {i}. {name}")
        print()

    else:
        # Interactive mode (default)
        lookup.interactive_mode()


if __name__ == "__main__":
    main()

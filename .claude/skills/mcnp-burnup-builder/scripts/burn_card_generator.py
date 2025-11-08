#!/usr/bin/env python3
"""
BURN Card Generator for MCNP Burnup Calculations

Purpose: Automatically generate MCNP BURN cards with adaptive time stepping,
         multi-cycle support, and shutdown periods

Usage:
    python burn_card_generator.py --cycles 3 --days 540 --power 3400 --output burn.txt
    python burn_card_generator.py --config burnup_config.json --output burn.txt

Author: MCNP Burnup Builder Skill
Based on: AGR-1/production reactor burnup methodology
"""

import argparse
import json
import sys
from typing import List, Dict, Tuple
import numpy as np


class BurnCardGenerator:
    """Generate MCNP BURN cards with adaptive time stepping"""

    def __init__(self):
        self.burn_cards = []
        self.cumulative_time = 0.0

    def add_irradiation_period(self,
                               duration_days: float,
                               power_mw: float,
                               materials: List[int],
                               volumes: List[float],
                               time_steps: List[float] = None,
                               fp_tier: int = -1,
                               omit_isotopes: List[int] = None) -> None:
        """
        Add irradiation period (power > 0)

        Args:
            duration_days: Total irradiation time (days)
            power_mw: Total reactor power (MW)
            materials: List of material IDs to burn
            volumes: List of material volumes (cm³), same order as materials
            time_steps: Custom time steps (days), if None uses adaptive
            fp_tier: Fission product tier (-1 to -4, default: -1)
            omit_isotopes: List of isotope ZAIDs to omit
        """
        if time_steps is None:
            time_steps = self._generate_adaptive_steps(duration_days)

        # Convert to cumulative time
        cumulative_steps = [self.cumulative_time + t for t in time_steps]

        # Create BURN card
        burn_card = {
            'type': 'irradiation',
            'time_steps': cumulative_steps,
            'power': power_mw,
            'pfrac': 1.0,
            'materials': materials,
            'volumes': volumes,
            'fp_tier': fp_tier,
            'omit_isotopes': omit_isotopes or self._default_omit_list()
        }

        self.burn_cards.append(burn_card)
        self.cumulative_time = cumulative_steps[-1]

    def add_decay_period(self,
                        duration_days: float,
                        materials: List[int],
                        volumes: List[float],
                        time_steps: List[float] = None,
                        fp_tier: int = -1,
                        omit_isotopes: List[int] = None) -> None:
        """
        Add decay period (power = 0)

        Args:
            duration_days: Decay time (days)
            materials: List of material IDs (same as irradiation)
            volumes: List of material volumes
            time_steps: Custom time steps for decay, if None uses single step
            fp_tier: Fission product tier
            omit_isotopes: List of isotope ZAIDs to omit
        """
        if time_steps is None:
            # Single decay step
            time_steps = [duration_days]

        # Convert to cumulative time
        cumulative_steps = [self.cumulative_time + t for t in time_steps]

        # Create BURN card
        burn_card = {
            'type': 'decay',
            'time_steps': cumulative_steps,
            'power': 0.0,
            'pfrac': 0.0,
            'materials': materials,
            'volumes': volumes,
            'fp_tier': fp_tier,
            'omit_isotopes': omit_isotopes or self._default_omit_list()
        }

        self.burn_cards.append(burn_card)
        self.cumulative_time = cumulative_steps[-1]

    def _generate_adaptive_steps(self, duration_days: float) -> List[float]:
        """
        Generate adaptive time steps for irradiation

        Strategy:
        - BOL (0-100 days): 20-day steps (rapid Pu buildup)
        - Mid-life (100-400 days): 50-day steps
        - EOL (400-end): 100-day steps (approaching equilibrium)

        Args:
            duration_days: Total duration

        Returns:
            List of cumulative time steps
        """
        steps = []

        # BOL: Fine steps (0-100 days)
        bol_end = min(100, duration_days)
        steps.extend(np.arange(20, bol_end + 1, 20).tolist())

        # Mid-life: Medium steps (100-400 days)
        if duration_days > 100:
            mid_end = min(400, duration_days)
            steps.extend(np.arange(150, mid_end + 1, 50).tolist())

        # EOL: Coarse steps (400-end)
        if duration_days > 400:
            steps.extend(np.arange(500, duration_days + 1, 100).tolist())

        # Ensure final time is included
        if steps[-1] < duration_days:
            steps.append(duration_days)

        return steps

    def _default_omit_list(self) -> List[int]:
        """
        Default isotope omit list (no cross-section data)

        Returns:
            List of ZAIDs to omit
        """
        return [6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244]

    def format_mcnp_burn_cards(self) -> str:
        """
        Format all BURN cards as MCNP input

        Returns:
            String with MCNP BURN card format
        """
        lines = []
        lines.append("c ================================================================")
        lines.append("c BURN CARDS - Generated by burn_card_generator.py")
        lines.append("c ================================================================")
        lines.append("")

        for i, card in enumerate(self.burn_cards, 1):
            card_type = card['type'].upper()
            time_range = f"{card['time_steps'][0]:.0f}-{card['time_steps'][-1]:.0f} days"

            lines.append(f"c --- BURN Card {i}: {card_type} ({time_range}) ---")

            # Format TIME
            time_str = " ".join(f"{t:.1f}" for t in card['time_steps'])
            # Split into multiple lines if too long
            if len(time_str) > 60:
                time_parts = time_str.split()
                time_lines = []
                current_line = "BURN  TIME="
                for part in time_parts:
                    if len(current_line) + len(part) + 1 > 78:
                        time_lines.append(current_line)
                        current_line = "           " + part
                    else:
                        current_line += part + " "
                time_lines.append(current_line)
                lines.extend(time_lines)
            else:
                lines.append(f"BURN  TIME={time_str}")

            # Format POWER
            lines.append(f"      POWER={card['power']:.2f}")

            # Format PFRAC
            lines.append(f"      PFRAC={card['pfrac']:.1f}")

            # Format MAT
            mat_str = " ".join(str(m) for m in card['materials'])
            lines.append(f"      MAT={mat_str}")

            # Format MATVOL
            vol_str = " ".join(f"{v:.1f}" for v in card['volumes'])
            # Split if too long
            if len(vol_str) > 60:
                vol_parts = vol_str.split()
                vol_lines = []
                current_line = "      MATVOL="
                for part in vol_parts:
                    if len(current_line) + len(part) + 1 > 78:
                        vol_lines.append(current_line)
                        current_line = "             " + part
                    else:
                        current_line += part + " "
                vol_lines.append(current_line)
                lines.extend(vol_lines)
            else:
                lines.append(f"      MATVOL={vol_str}")

            # Format BOPT
            lines.append(f"      BOPT=1.0, {card['fp_tier']}, 1")

            lines.append("")

        # Add OMIT cards
        lines.append("c ================================================================")
        lines.append("c OMIT CARDS (Isotopes without cross-section data)")
        lines.append("c ================================================================")
        lines.append("")

        # Get unique material list
        all_materials = set()
        for card in self.burn_cards:
            all_materials.update(card['materials'])

        # Get omit list from first card (assuming same for all)
        omit_list = self.burn_cards[0]['omit_isotopes']
        omit_str = ", ".join(str(z) for z in omit_list)

        for mat in sorted(all_materials):
            lines.append(f"OMIT  {mat}, 8, {omit_str}")

        lines.append("")
        lines.append("c ================================================================")

        return '\n'.join(lines)

    def get_summary(self) -> str:
        """
        Get summary of burnup schedule

        Returns:
            Formatted summary string
        """
        lines = []
        lines.append("=" * 70)
        lines.append("BURNUP SCHEDULE SUMMARY")
        lines.append("=" * 70)
        lines.append(f"{'Period':<10} {'Type':<12} {'Duration':<12} {'Power (MW)':<12} {'Steps':<6}")
        lines.append("-" * 70)

        for i, card in enumerate(self.burn_cards, 1):
            duration = card['time_steps'][-1] - (card['time_steps'][0] if i == 1 else self.burn_cards[i-2]['time_steps'][-1])
            period_type = card['type'].capitalize()
            power = f"{card['power']:.1f}" if card['power'] > 0 else "Decay"
            n_steps = len(card['time_steps'])

            lines.append(f"{i:<10} {period_type:<12} {duration:<12.1f} {power:<12} {n_steps:<6}")

        lines.append("-" * 70)
        lines.append(f"Total time: {self.cumulative_time:.1f} days")
        lines.append(f"Total BURN cards: {len(self.burn_cards)}")
        lines.append("=" * 70)

        return '\n'.join(lines)


def load_config_file(filepath: str) -> Dict:
    """
    Load burnup configuration from JSON file

    Expected format:
    {
        "cycles": [
            {"duration_days": 540, "power_mw": 3400, "shutdown_days": 60},
            {"duration_days": 540, "power_mw": 3400, "shutdown_days": 60},
            ...
        ],
        "materials": [1, 2, 3],
        "volumes": [500.0, 800.0, 1200.0],
        "fp_tier": -1
    }

    Args:
        filepath: Path to JSON config file

    Returns:
        Configuration dictionary
    """
    with open(filepath, 'r') as f:
        config = json.load(f)

    return config


def main():
    parser = argparse.ArgumentParser(
        description="Generate MCNP BURN cards with adaptive time stepping",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single cycle (540 days, 3400 MW)
  python burn_card_generator.py --cycles 1 --days 540 --power 3400 \\
                                 --materials 1 2 3 --volumes 500 800 1200

  # Three cycles with shutdowns
  python burn_card_generator.py --cycles 3 --days 540 --power 3400 \\
                                 --shutdown 60 --materials 1 --volumes 193

  # From configuration file
  python burn_card_generator.py --config burnup_schedule.json --output burn.txt

  # Custom time steps
  python burn_card_generator.py --days 540 --power 3400 --materials 1 \\
                                 --volumes 193 --steps 100 200 300 400 500 540
        """
    )

    parser.add_argument('--cycles', type=int, default=1,
                       help='Number of irradiation cycles (default: 1)')
    parser.add_argument('--days', type=float, default=540,
                       help='Duration per cycle (days, default: 540)')
    parser.add_argument('--power', type=float, default=1.0,
                       help='Total reactor power (MW, default: 1.0)')
    parser.add_argument('--shutdown', type=float, default=0,
                       help='Shutdown duration between cycles (days, default: 0)')
    parser.add_argument('--materials', type=int, nargs='+', default=[1],
                       help='Material IDs to burn (default: 1)')
    parser.add_argument('--volumes', type=float, nargs='+', default=[1.0],
                       help='Material volumes (cm³, default: 1.0)')
    parser.add_argument('--steps', type=float, nargs='*',
                       help='Custom time steps (days), if not specified uses adaptive')
    parser.add_argument('--fp-tier', type=int, choices=[1, 2, 3, 4], default=1,
                       help='Fission product tier (default: 1)')
    parser.add_argument('--config', type=str,
                       help='JSON configuration file')
    parser.add_argument('--output', type=str,
                       help='Output file (default: stdout)')

    args = parser.parse_args()

    # Validate materials and volumes
    if len(args.materials) != len(args.volumes):
        parser.error(f"Number of materials ({len(args.materials)}) must match "
                    f"number of volumes ({len(args.volumes)})")

    # Create generator
    generator = BurnCardGenerator()

    # Load from config file or command line
    if args.config:
        config = load_config_file(args.config)
        for cycle in config['cycles']:
            # Irradiation
            generator.add_irradiation_period(
                duration_days=cycle['duration_days'],
                power_mw=cycle['power_mw'],
                materials=config['materials'],
                volumes=config['volumes'],
                fp_tier=config.get('fp_tier', -1)
            )
            # Shutdown (if specified)
            if cycle.get('shutdown_days', 0) > 0:
                generator.add_decay_period(
                    duration_days=cycle['shutdown_days'],
                    materials=config['materials'],
                    volumes=config['volumes'],
                    fp_tier=config.get('fp_tier', -1)
                )
    else:
        # Generate from command line arguments
        fp_tier_map = {1: -1, 2: -2, 3: -3, 4: -4}
        fp_tier_value = fp_tier_map[args.fp_tier]

        for cycle in range(args.cycles):
            # Irradiation
            generator.add_irradiation_period(
                duration_days=args.days,
                power_mw=args.power,
                materials=args.materials,
                volumes=args.volumes,
                time_steps=args.steps,
                fp_tier=fp_tier_value
            )

            # Shutdown (if not last cycle and shutdown > 0)
            if cycle < args.cycles - 1 and args.shutdown > 0:
                generator.add_decay_period(
                    duration_days=args.shutdown,
                    materials=args.materials,
                    volumes=args.volumes,
                    fp_tier=fp_tier_value
                )

    # Generate output
    burn_cards = generator.format_mcnp_burn_cards()
    summary = generator.get_summary()

    # Write to file or stdout
    if args.output:
        with open(args.output, 'w') as f:
            f.write(burn_cards)
        print(f"BURN cards written to: {args.output}", file=sys.stderr)
        print("\n" + summary, file=sys.stderr)
    else:
        print(burn_cards)
        print("\n" + summary, file=sys.stderr)

    return 0


if __name__ == '__main__':
    sys.exit(main())

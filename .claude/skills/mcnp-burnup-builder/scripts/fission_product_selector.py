#!/usr/bin/env python3
"""
Fission Product Selector for MCNP Burnup Calculations

Purpose: Generate fission product lists for MCNP material cards based on
         4-tier importance system (reactivity, decay heat, dose rates)

Usage:
    python fission_product_selector.py --tier 1 --output fp_list.txt
    python fission_product_selector.py --tier 2 --format mcnp --output material_fp.txt

Author: MCNP Burnup Builder Skill
Based on: AGR-1 fission product selection strategy
"""

import argparse
import sys
from typing import List, Dict, Tuple


# Fission Product Database (ZAID, name, cross-section, purpose)
FISSION_PRODUCTS = {
    # TIER 1: ALWAYS Include (Strong Absorbers)
    1: [
        (54135, 'Xe-135', 2.65e6, 'Peak ~9 hr after shutdown, 3.5 Mbarn'),
        (62149, 'Sm-149', 40140, 'Stable, builds up over time, 40 kbarn'),
        (62151, 'Sm-151', 15000, 'Long-lived (90 yr), 15 kbarn'),
        (64155, 'Gd-155', 60900, 'From Eu-155 decay, 61 kbarn'),
        (64157, 'Gd-157', 254000, 'STRONGEST absorber, 254 kbarn'),
        (61147, 'Pm-147', 168, 'Decays to Sm-147, precursor'),
        (61149, 'Pm-149', 2000, 'Decays to Sm-149, CRITICAL precursor'),
    ],

    # TIER 2: SHOULD Include (Significant Absorbers)
    2: [
        (48113, 'Cd-113', 20600, 'Strong absorber, 20.6 kbarn'),
        (63153, 'Eu-153', 312, 'Moderate absorber'),
        (63155, 'Eu-155', 3760, 'Decays to Gd-155, 3.76 kbarn'),
        (45103, 'Rh-103', 150, 'Resonance absorber'),
        (43099, 'Tc-99', 20, 'Long-lived, high yield'),
        (55133, 'Cs-133', 30, 'Stable, high yield'),
    ],

    # TIER 3: MAY Include (Decay Heat/Dose Sources)
    3: [
        (55137, 'Cs-137', 0.25, 'MAJOR γ source (661 keV), 30 yr'),
        (38090, 'Sr-90', 0.8, 'MAJOR β source, 29 yr'),
        (56140, 'Ba-140', 5, 'γ source, short-lived'),
        (57140, 'La-140', 3, 'γ source, 1.7 day'),
        (58141, 'Ce-141', 2, 'γ source, 32 day'),
        (59143, 'Pr-143', 1, 'β source, 13.6 day'),
        (53131, 'I-131', 7, 'Medical/environmental, 8 day'),
        (44106, 'Ru-106', 2, 'β/γ source, 1.02 yr'),
    ],

    # TIER 4: Optional (Completeness)
    4: [
        (36083, 'Kr-83', 0.2, 'Stable noble gas'),
        (54131, 'Xe-131', 0.1, 'Stable'),
        (54133, 'Xe-133', 0.3, 'Dose important, 5.2 day'),
        (42095, 'Mo-95', 0.5, 'Stable, 6.5% yield'),
        (44101, 'Ru-101', 0.4, 'Stable, 5.1% yield'),
        (60143, 'Nd-143', 0.3, 'Stable, burnup monitor'),
        (60145, 'Nd-145', 0.2, 'Stable, 3.9% yield'),
        (40093, 'Zr-93', 0.1, 'Very long-lived, 1.5 Myr'),
    ]
}


class FissionProductSelector:
    """Select fission products for MCNP material cards"""

    def __init__(self, tier: int = 1, library_suffix: str = '70c'):
        """
        Initialize FP selector

        Args:
            tier: Maximum tier to include (1-4)
            library_suffix: MCNP cross-section library suffix (default: 70c)
        """
        self.tier = tier
        self.library_suffix = library_suffix
        self.selected_fps = []

    def select_fps(self) -> List[Tuple[int, str, float, str]]:
        """
        Select fission products up to specified tier

        Returns:
            List of (ZAID, name, cross-section, notes)
        """
        selected = []

        for t in range(1, self.tier + 1):
            if t in FISSION_PRODUCTS:
                selected.extend(FISSION_PRODUCTS[t])

        self.selected_fps = selected
        return selected

    def format_mcnp_material(self, densities: Dict[int, float] = None) -> str:
        """
        Format as MCNP material card lines

        Args:
            densities: Optional dict of ZAID → atom density
                      If None, uses placeholder '<?>'

        Returns:
            String with MCNP material card format
        """
        lines = []
        lines.append("c Fission Products (Tier 1-{})".format(self.tier))

        # Group by tier
        for t in range(1, self.tier + 1):
            if t not in FISSION_PRODUCTS:
                continue

            tier_name = {
                1: 'TIER 1: Strong Absorbers',
                2: 'TIER 2: Significant Absorbers',
                3: 'TIER 3: Decay Heat/Dose Sources',
                4: 'TIER 4: Completeness'
            }

            lines.append(f"c {tier_name[t]}")

            for zaid, name, xsec, notes in FISSION_PRODUCTS[t]:
                density = densities.get(zaid, '<?>')if densities else '<?>'
                zaid_lib = f"{zaid}.{self.library_suffix}"
                comment = f"$ {name} ({notes})"

                if isinstance(density, str):
                    line = f"   {zaid_lib:12s}  {density:12s}  {comment}"
                else:
                    line = f"   {zaid_lib:12s}  {density:12.6E}  {comment}"

                lines.append(line)

        return '\n'.join(lines)

    def format_zaid_list(self) -> str:
        """
        Format as simple ZAID list (for OMIT cards or tallies)

        Returns:
            Space-separated string of ZAIDs
        """
        zaids = [str(zaid) for zaid, _, _, _ in self.selected_fps]
        return ' '.join(zaids)

    def format_summary_table(self) -> str:
        """
        Format as summary table

        Returns:
            Formatted table string
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"FISSION PRODUCT SELECTION SUMMARY (Tier 1-{self.tier})")
        lines.append("=" * 80)
        lines.append(f"{'ZAID':<8} {'Name':<10} {'σ_thermal (barn)':<18} {'Purpose/Notes':<42}")
        lines.append("-" * 80)

        for zaid, name, xsec, notes in self.selected_fps:
            xsec_str = f"{xsec:.2e}" if xsec >= 1000 else f"{xsec:.1f}"
            lines.append(f"{zaid:<8} {name:<10} {xsec_str:<18} {notes:<42}")

        lines.append("-" * 80)
        lines.append(f"Total isotopes selected: {len(self.selected_fps)}")
        lines.append("=" * 80)

        return '\n'.join(lines)

    def get_statistics(self) -> Dict[str, int]:
        """
        Get selection statistics

        Returns:
            Dict with counts by tier and type
        """
        stats = {
            'total': len(self.selected_fps),
            'tier_1': len(FISSION_PRODUCTS.get(1, [])) if self.tier >= 1 else 0,
            'tier_2': len(FISSION_PRODUCTS.get(2, [])) if self.tier >= 2 else 0,
            'tier_3': len(FISSION_PRODUCTS.get(3, [])) if self.tier >= 3 else 0,
            'tier_4': len(FISSION_PRODUCTS.get(4, [])) if self.tier >= 4 else 0,
        }

        # Count absorbers (σ > 100 barn)
        stats['strong_absorbers'] = sum(1 for _, _, xsec, _ in self.selected_fps if xsec > 100)
        stats['dose_sources'] = sum(1 for _, name, _, _ in self.selected_fps if 'Cs-137' in name or 'Sr-90' in name)

        return stats


def main():
    parser = argparse.ArgumentParser(
        description="Select fission products for MCNP burnup calculations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Tier Descriptions:
  1 - Strong absorbers (Xe-135, Sm-149, Gd-157): ALWAYS include
  2 - Significant absorbers (Cd-113, Eu-155, Rh-103): Standard calculations
  3 - Decay heat/dose sources (Cs-137, Sr-90): Add for dose calculations
  4 - Completeness (stable FPs, burnup monitors): Research/benchmarking

Examples:
  # Minimum set (Tier 1 only): 7 isotopes
  python fission_product_selector.py --tier 1 --output fp_tier1.txt

  # Standard set (Tiers 1-2): 13 isotopes
  python fission_product_selector.py --tier 2 --format mcnp --output fp_material.txt

  # Comprehensive (Tiers 1-3): 21 isotopes, for dose calculations
  python fission_product_selector.py --tier 3 --format mcnp

  # Full set (All tiers): 29 isotopes, for benchmarking
  python fission_product_selector.py --tier 4 --format table
        """
    )

    parser.add_argument('--tier', type=int, choices=[1, 2, 3, 4], default=1,
                       help='Maximum tier to include (default: 1)')
    parser.add_argument('--format', choices=['mcnp', 'zaid', 'table'], default='mcnp',
                       help='Output format (default: mcnp)')
    parser.add_argument('--library', type=str, default='70c',
                       help='MCNP cross-section library suffix (default: 70c)')
    parser.add_argument('--output', type=str,
                       help='Output file (default: stdout)')

    args = parser.parse_args()

    # Create selector
    selector = FissionProductSelector(tier=args.tier, library_suffix=args.library)
    selector.select_fps()

    # Generate output
    if args.format == 'mcnp':
        output = selector.format_mcnp_material()
    elif args.format == 'zaid':
        output = selector.format_zaid_list()
    elif args.format == 'table':
        output = selector.format_summary_table()
    else:
        output = selector.format_summary_table()

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output + '\n')
        print(f"Fission product selection written to: {args.output}", file=sys.stderr)

        # Print statistics to stderr
        stats = selector.get_statistics()
        print(f"\nStatistics:", file=sys.stderr)
        print(f"  Total isotopes: {stats['total']}", file=sys.stderr)
        print(f"  Strong absorbers: {stats['strong_absorbers']}", file=sys.stderr)
        print(f"  Dose sources: {stats['dose_sources']}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == '__main__':
    sys.exit(main())

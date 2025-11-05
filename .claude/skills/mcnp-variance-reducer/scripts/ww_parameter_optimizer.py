#!/usr/bin/env python3
"""
MCNP Weight Window Parameter Optimizer

Suggests optimal WWP card parameters (wupn, wsurvn, mxspln) based on
weight distribution statistics and splitting/roulette counts.

Usage:
    python ww_parameter_optimizer.py output.o
    python ww_parameter_optimizer.py --suggest-target output.o

Author: MCNP Variance Reducer Skill
Version: 1.0.0
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class WeightStats:
    """Weight window statistics"""
    min_weight: float
    max_weight: float
    avg_weight: float
    splits: int
    roulettes: int
    kills: int

    @property
    def weight_ratio(self) -> float:
        """Max/min weight ratio"""
        if self.min_weight > 0:
            return self.max_weight / self.min_weight
        return 0.0


@dataclass
class WWPParameters:
    """Weight window parameters"""
    wupn: float  # Upper bound multiplier
    wsurvn: float  # Survival weight multiplier
    mxspln: int  # Maximum splits

    def format_card(self, particle: str = "N") -> str:
        """Format as MCNP WWP card"""
        return f"WWP:{particle}  {self.wupn:.0f}  {self.wsurvn:.0f}  {self.mxspln}  0  -1"


def extract_weight_stats(filepath: Path) -> Optional[WeightStats]:
    """
    Extract weight window statistics from MCNP output.

    Args:
        filepath: Path to MCNP output file

    Returns:
        WeightStats object or None if not found
    """
    try:
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read()

        # Extract weight statistics
        # Pattern: minimum weight = 1.2345E-03
        min_match = re.search(r'minimum\s+weight\s*[=:]\s*([\d.E+-]+)', content, re.IGNORECASE)
        max_match = re.search(r'maximum\s+weight\s*[=:]\s*([\d.E+-]+)', content, re.IGNORECASE)
        avg_match = re.search(r'average\s+weight\s*[=:]\s*([\d.E+-]+)', content, re.IGNORECASE)

        # Extract splitting/roulette counts
        splits_match = re.search(r'number\s+of\s+splits.*?[=:]\s*(\d+)', content, re.IGNORECASE)
        roulette_match = re.search(r'number.*?roulette.*?[=:]\s*(\d+)', content, re.IGNORECASE)
        kills_match = re.search(r'killed.*?weight.*?window.*?[=:]\s*(\d+)', content, re.IGNORECASE)

        if not (min_match and max_match and avg_match):
            return None

        return WeightStats(
            min_weight=float(min_match.group(1)),
            max_weight=float(max_match.group(1)),
            avg_weight=float(avg_match.group(1)),
            splits=int(splits_match.group(1)) if splits_match else 0,
            roulettes=int(roulette_match.group(1)) if roulette_match else 0,
            kills=int(kills_match.group(1)) if kills_match else 0
        )

    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None


def suggest_wupn(weight_stats: WeightStats, current_wupn: float = 5.0) -> Tuple[float, str]:
    """
    Suggest wupn value based on weight distribution.

    Args:
        weight_stats: Weight statistics from output
        current_wupn: Current wupn value

    Returns:
        Tuple of (suggested_wupn, reason)
    """
    ratio = weight_stats.weight_ratio

    if ratio > 100:
        return 20.0, f"Weight ratio ({ratio:.1f}) very large - widen window significantly"
    elif ratio > 50:
        return 10.0, f"Weight ratio ({ratio:.1f}) large - widen window"
    elif ratio > 20:
        return max(current_wupn * 1.5, 7.0), f"Weight ratio ({ratio:.1f}) moderate-high"
    elif ratio < 5:
        return min(current_wupn * 0.7, 3.0), f"Weight ratio ({ratio:.1f}) small - can narrow window"
    else:
        return current_wupn, f"Weight ratio ({ratio:.1f}) acceptable"


def suggest_wsurvn(wupn: float) -> Tuple[float, str]:
    """
    Suggest wsurvn based on wupn.

    Args:
        wupn: Upper bound multiplier

    Returns:
        Tuple of (suggested_wsurvn, reason)
    """
    # Rule: wsurvn should be between wupn/3 and wupn/2
    wsurvn = wupn / 2.0

    # Round to reasonable value
    if wsurvn < 2.0:
        wsurvn = 2.0
        reason = f"Minimum wsurvn (must be > 1.0)"
    elif wsurvn > wupn - 1:
        wsurvn = wupn - 1
        reason = f"Must be < wupn ({wupn})"
    else:
        reason = f"Half of wupn (standard practice)"

    return wsurvn, reason


def suggest_mxspln(weight_stats: WeightStats, current_mxspln: int = 5) -> Tuple[int, str]:
    """
    Suggest mxspln based on splitting statistics.

    Args:
        weight_stats: Weight statistics from output
        current_mxspln: Current mxspln value

    Returns:
        Tuple of (suggested_mxspln, reason)
    """
    if weight_stats.splits == 0:
        return current_mxspln, "No splitting data available"

    # Check if splits are being limited
    # High ratio of splits to particles suggests limiting
    splits_per_1000 = weight_stats.splits / 1000.0

    if splits_per_1000 > 100:
        return min(current_mxspln + 5, 20), f"High split rate ({splits_per_1000:.0f}/1000) - may need more splits"
    elif splits_per_1000 < 10:
        return max(current_mxspln - 2, 2), f"Low split rate ({splits_per_1000:.0f}/1000) - can reduce limit"
    else:
        return current_mxspln, f"Split rate ({splits_per_1000:.0f}/1000) acceptable"


def suggest_target_weight(weight_stats: WeightStats) -> Tuple[float, str]:
    """
    Suggest WWG target weight parameter.

    Args:
        weight_stats: Weight statistics from output

    Returns:
        Tuple of (suggested_target, reason)
    """
    avg = weight_stats.avg_weight

    # Heuristic: target should be close to average weight
    # Round to 1 significant figure
    magnitude = 10 ** int(str(f"{avg:.0e}").split('e')[1])
    target = round(avg / magnitude) * magnitude

    if target == 0:
        target = 1.0
        reason = "Default target (average weight too small)"
    elif avg > 10:
        reason = f"Many particles (avg weight {avg:.1f}) - increase target"
    elif avg < 0.1:
        reason = f"Few particles (avg weight {avg:.3f}) - decrease target"
    else:
        reason = f"Match average weight ({avg:.2f})"

    return target, reason


def analyze_performance(weight_stats: WeightStats) -> List[str]:
    """
    Analyze weight window performance and provide recommendations.

    Args:
        weight_stats: Weight statistics from output

    Returns:
        List of recommendation strings
    """
    recommendations = []

    # Check weight ratio
    if weight_stats.weight_ratio > 100:
        recommendations.append(
            "⚠️  CRITICAL: Weight ratio >100 - weight windows may be too aggressive"
        )
    elif weight_stats.weight_ratio > 50:
        recommendations.append(
            "⚠️  WARNING: Weight ratio >50 - consider widening weight windows"
        )

    # Check kill rate
    total_events = weight_stats.splits + weight_stats.roulettes
    if total_events > 0:
        kill_rate = weight_stats.kills / total_events
        if kill_rate > 0.5:
            recommendations.append(
                f"⚠️  WARNING: High kill rate ({kill_rate*100:.1f}%) - weight windows may be too restrictive"
            )

    # Check split/roulette balance
    if weight_stats.splits > 0 and weight_stats.roulettes > 0:
        split_roulette_ratio = weight_stats.splits / weight_stats.roulettes
        if split_roulette_ratio > 10:
            recommendations.append(
                f"ℹ️  INFO: Many more splits than roulettes (ratio {split_roulette_ratio:.1f}) - importance may be increasing too fast"
            )
        elif split_roulette_ratio < 0.1:
            recommendations.append(
                f"ℹ️  INFO: Many more roulettes than splits (ratio {split_roulette_ratio:.3f}) - importance may be decreasing"
            )

    if not recommendations:
        recommendations.append("✓ Weight window performance appears good")

    return recommendations


def main():
    parser = argparse.ArgumentParser(
        description="Optimize MCNP weight window parameters based on simulation statistics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze weight window performance
  python ww_parameter_optimizer.py output.o

  # Suggest WWG target weight
  python ww_parameter_optimizer.py --suggest-target output.o

  # Provide current parameters for comparison
  python ww_parameter_optimizer.py --current-wupn 5 --current-wsurvn 3 output.o
        """
    )

    parser.add_argument('file', help='MCNP output file')
    parser.add_argument('--current-wupn', type=float, default=5.0,
                        help='Current wupn value (default: 5.0)')
    parser.add_argument('--current-wsurvn', type=float, default=3.0,
                        help='Current wsurvn value (default: 3.0)')
    parser.add_argument('--current-mxspln', type=int, default=5,
                        help='Current mxspln value (default: 5)')
    parser.add_argument('--suggest-target', action='store_true',
                        help='Suggest WWG target weight parameter')
    parser.add_argument('--particle', type=str, default='N',
                        help='Particle type for WWP card (default: N)')

    args = parser.parse_args()

    # Read output file
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    weight_stats = extract_weight_stats(filepath)
    if not weight_stats:
        print(f"Error: Could not extract weight statistics from {args.file}", file=sys.stderr)
        sys.exit(1)

    # Display statistics
    print("Weight Window Statistics:")
    print("=" * 60)
    print(f"Minimum weight:    {weight_stats.min_weight:.6e}")
    print(f"Maximum weight:    {weight_stats.max_weight:.6e}")
    print(f"Average weight:    {weight_stats.avg_weight:.6e}")
    print(f"Weight ratio:      {weight_stats.weight_ratio:.2f} (max/min)")
    print(f"Splits:            {weight_stats.splits:,}")
    print(f"Roulettes:         {weight_stats.roulettes:,}")
    print(f"Particles killed:  {weight_stats.kills:,}")
    print()

    # Performance analysis
    print("Performance Analysis:")
    print("=" * 60)
    for rec in analyze_performance(weight_stats):
        print(rec)
    print()

    # Parameter suggestions
    print("Parameter Suggestions:")
    print("=" * 60)

    # Current parameters
    current_params = WWPParameters(args.current_wupn, args.current_wsurvn, args.current_mxspln)
    print(f"Current:  {current_params.format_card(args.particle)}")

    # Suggest new parameters
    new_wupn, wupn_reason = suggest_wupn(weight_stats, args.current_wupn)
    new_wsurvn, wsurvn_reason = suggest_wsurvn(new_wupn)
    new_mxspln, mxspln_reason = suggest_mxspln(weight_stats, args.current_mxspln)

    suggested_params = WWPParameters(new_wupn, new_wsurvn, new_mxspln)
    print(f"Suggested: {suggested_params.format_card(args.particle)}")
    print()

    print("Reasoning:")
    print(f"  wupn:    {wupn_reason}")
    print(f"  wsurvn:  {wsurvn_reason}")
    print(f"  mxspln:  {mxspln_reason}")

    # WWG target suggestion
    if args.suggest_target:
        print()
        print("WWG Target Weight Suggestion:")
        print("=" * 60)
        target, target_reason = suggest_target_weight(weight_stats)
        print(f"Target:  {target:.2f}")
        print(f"Reason:  {target_reason}")
        print(f"\nWWG card: WWG  <tally>  <mesh>  {target:.1f}")


if __name__ == "__main__":
    main()

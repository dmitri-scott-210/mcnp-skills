#!/usr/bin/env python3
"""
MCNP Checkpoint Interval Calculator

Calculate optimal checkpoint (PRDMP) intervals based on run time and overhead.

Usage:
    python checkpoint_calculator.py --runtime 48 --dump-overhead 120
    python checkpoint_calculator.py  # Interactive mode
"""

import sys
import argparse
import math

def calculate_optimal_interval(runtime_hours, dump_overhead_seconds, mtbf_hours=100):
    """
    Calculate optimal checkpoint interval
    
    Formula: optimal = sqrt(2 × checkpoint_overhead × MTBF)
    
    Args:
        runtime_hours: Expected run time (hours)
        dump_overhead_seconds: Time to write dump (seconds)
        mtbf_hours: Mean time between failures (hours)
    
    Returns:
        Optimal interval in minutes
    """
    optimal_seconds = math.sqrt(2 * dump_overhead_seconds * mtbf_hours * 3600)
    optimal_minutes = optimal_seconds / 60
    return optimal_minutes

def recommend_interval(runtime_hours, optimal_minutes):
    """Recommend practical interval based on optimal"""
    
    if runtime_hours < 4:
        return None, "Optional (run < 4 hours)"
    
    # Round to nice values
    if optimal_minutes < 30:
        interval = 30
    elif optimal_minutes < 45:
        interval = 30
    elif optimal_minutes < 75:
        interval = 60
    elif optimal_minutes < 105:
        interval = 90
    elif optimal_minutes < 150:
        interval = 120
    elif optimal_minutes < 210:
        interval = 180
    else:
        interval = 240
    
    return interval, "Recommended"

def interactive_mode():
    """Interactive calculator"""
    print("=" * 60)
    print("MCNP Checkpoint Interval Calculator")
    print("=" * 60)
    
    try:
        runtime = float(input("Expected run time (hours): ").strip())
        dump_overhead = float(input("Dump write time (seconds) [120]: ").strip() or "120")
        mtbf = float(input("Mean time between failures (hours) [100]: ").strip() or "100")
    except ValueError as e:
        print(f"ERROR: Invalid number: {e}")
        return
    
    optimal = calculate_optimal_interval(runtime, dump_overhead, mtbf)
    recommended, reason = recommend_interval(runtime, optimal)
    
    print("\n" + "=" * 60)
    print("Results:")
    print("=" * 60)
    print(f"Optimal interval: {optimal:.1f} minutes")
    
    if recommended:
        print(f"Recommended:     {recommended} minutes")
        print(f"PRDMP card:       PRDMP  {recommended}")
    else:
        print(f"Recommendation:   {reason}")
    
    num_dumps = (runtime * 60) / (recommended if recommended else 60)
    print(f"\nExpected dumps: {num_dumps:.1f}")
    
    if recommended:
        ctme = runtime * 60 - 30
        print(f"Suggested CTME: {int(ctme)} (leaves 30-min buffer)")

def main():
    parser = argparse.ArgumentParser(
        description='Calculate optimal MCNP checkpoint interval'
    )
    
    parser.add_argument('--runtime', type=float, help='Expected run time (hours)')
    parser.add_argument('--dump-overhead', type=float, default=120, help='Dump write time (seconds)')
    parser.add_argument('--mtbf', type=float, default=100, help='Mean time between failures (hours)')
    
    args = parser.parse_args()
    
    if not args.runtime:
        interactive_mode()
    else:
        optimal = calculate_optimal_interval(args.runtime, args.dump_overhead, args.mtbf)
        recommended, reason = recommend_interval(args.runtime, optimal)
        
        print(f"Optimal interval: {optimal:.1f} minutes")
        if recommended:
            print(f"Recommended: {recommended} minutes")
            print(f"PRDMP card: PRDMP  {recommended}")
        else:
            print(f"Recommendation: {reason}")

if __name__ == '__main__':
    main()

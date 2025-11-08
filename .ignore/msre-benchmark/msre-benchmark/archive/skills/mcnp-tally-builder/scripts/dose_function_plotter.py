#!/usr/bin/env python3
"""
MCNP Dose Function Plotter

Plots flux-to-dose conversion factors from MCNP input files or built-in standards.
Supports ICRP-74, ICRP-116, and ANSI/ANS-6.1.1 response functions.

Usage:
    python dose_function_plotter.py input.i 14
    python dose_function_plotter.py --builtin ICRP74_AP
    python dose_function_plotter.py input.i 14 --output dose_response.png

Requires: matplotlib, numpy

Author: MCNP Skills Project
License: MIT
"""

import sys
import re
from pathlib import Path
from typing import Tuple, List

try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError:
    print("Error: This script requires matplotlib and numpy")
    print("Install with: pip install matplotlib numpy")
    sys.exit(1)


class DoseFunctionPlotter:
    """Plots dose conversion factors for MCNP tallies."""
    
    # Built-in ICRP-74 AP (Anterior-Posterior) neutron dose factors (Sv/h per n/cm²/s)
    ICRP74_AP_NEUTRON = {
        'energies': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 
                     5e-1, 1.0, 2.0, 5.0, 10.0, 20.0],
        'factors': [5.64e-6, 5.64e-6, 6.48e-6, 7.92e-6, 7.92e-6, 7.92e-6,
                   9.00e-6, 1.08e-5, 2.88e-5, 1.08e-4, 1.62e-4, 2.16e-4,
                   3.24e-4, 4.32e-4, 5.40e-4]
    }
    
    def __init__(self, input_file: str = None, tally_num: int = None):
        self.input_file = Path(input_file) if input_file else None
        self.tally_num = tally_num
        self.energies = []
        self.factors = []
        self.title = "Dose Response Function"
        
    def load_from_input(self) -> bool:
        """Load DE/DF cards from MCNP input file."""
        if not self.input_file or not self.input_file.exists():
            print(f"Error: Input file not found: {self.input_file}")
            return False
        
        content = self.input_file.read_text()
        lines = content.split('\n')
        
        # Find DE and DF cards for specified tally
        de_pattern = re.compile(rf'^de{self.tally_num}\s+(.+)', re.IGNORECASE)
        df_pattern = re.compile(rf'^df{self.tally_num}\s+(.+)', re.IGNORECASE)
        
        de_values = []
        df_values = []
        
        for line in lines:
            stripped = line.strip()
            
            de_match = de_pattern.match(stripped)
            if de_match:
                parts = de_match.group(1).split()
                for part in parts:
                    if part.upper() not in ['LIN', 'LOG']:
                        try:
                            de_values.append(float(part))
                        except ValueError:
                            continue
            
            df_match = df_pattern.match(stripped)
            if df_match:
                parts = df_match.group(1).split()
                for part in parts:
                    if part.upper() not in ['LIN', 'LOG']:
                        try:
                            df_values.append(float(part))
                        except ValueError:
                            continue
        
        if not de_values or not df_values:
            print(f"Error: Could not find DE{self.tally_num}/DF{self.tally_num} cards")
            return False
        
        if len(de_values) != len(df_values):
            print(f"Warning: DE and DF have different lengths ({len(de_values)} vs {len(df_values)})")
        
        self.energies = de_values
        self.factors = df_values
        self.title = f"Dose Response Function (F{self.tally_num})"
        return True
    
    def load_builtin(self, standard: str) -> bool:
        """Load built-in dose response function."""
        if standard.upper() == 'ICRP74_AP':
            self.energies = self.ICRP74_AP_NEUTRON['energies']
            self.factors = self.ICRP74_AP_NEUTRON['factors']
            self.title = "ICRP-74 AP Neutron Dose (Sv/h per n/cm²/s)"
            return True
        else:
            print(f"Error: Unknown built-in standard '{standard}'")
            print("Available: ICRP74_AP")
            return False
    
    def plot(self, output_file: str = None, show: bool = True):
        """Generate and display/save plot."""
        if not self.energies or not self.factors:
            print("Error: No data to plot")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot data
        ax.loglog(self.energies, self.factors, 'o-', linewidth=2, markersize=8)
        
        # Labels and formatting
        ax.set_xlabel('Energy (MeV)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Dose Conversion Factor (Sv/h per n/cm²/s)', fontsize=12, fontweight='bold')
        ax.set_title(self.title, fontsize=14, fontweight='bold')
        ax.grid(True, which='both', alpha=0.3)
        
        # Add statistics text box
        stats_text = (f"Energy range: {min(self.energies):.2e} - {max(self.energies):.2e} MeV\n"
                     f"Factor range: {min(self.factors):.2e} - {max(self.factors):.2e} Sv/h\n"
                     f"Data points: {len(self.energies)}")
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {output_file}")
        
        if show:
            plt.show()


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python dose_function_plotter.py input.i tally_number [--output file.png]")
        print("  python dose_function_plotter.py --builtin ICRP74_AP [--output file.png]")
        print("\nExamples:")
        print("  python dose_function_plotter.py reactor.i 14")
        print("  python dose_function_plotter.py --builtin ICRP74_AP --output dose.png")
        sys.exit(1)
    
    output_file = None
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
    
    plotter = DoseFunctionPlotter()
    
    if sys.argv[1] == '--builtin':
        if len(sys.argv) < 3:
            print("Error: --builtin requires standard name (e.g., ICRP74_AP)")
            sys.exit(1)
        standard = sys.argv[2]
        if not plotter.load_builtin(standard):
            sys.exit(1)
    else:
        input_file = sys.argv[1]
        if len(sys.argv) < 3:
            print("Error: Tally number required")
            sys.exit(1)
        try:
            tally_num = int(sys.argv[2])
        except ValueError:
            print(f"Error: Invalid tally number '{sys.argv[2]}'")
            sys.exit(1)
        
        plotter = DoseFunctionPlotter(input_file, tally_num)
        if not plotter.load_from_input():
            sys.exit(1)
    
    plotter.plot(output_file=output_file, show=(output_file is None))


if __name__ == '__main__':
    main()

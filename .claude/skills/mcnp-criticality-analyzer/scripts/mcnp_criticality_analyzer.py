"""MCNP Criticality Analyzer (Skill 19) - Analyze KCODE results

KCODE format (Chapter 5):
- nsrck: Particles per cycle
- rkk: Initial k-effective guess
- ikz: Cycles to skip before tallying (inactive)
- kct: Total cycles to run (inactive + active)

Convergence criteria:
- σ(k_eff) < 0.005 for well-converged
- σ(k_eff) < 0.001 for publication quality
- Monitor k_eff trend over cycles
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.output_parser import MCNPOutputParser

class MCNPCriticalityAnalyzer:
    """Analyze KCODE criticality calculations"""

    def __init__(self):
        self.parser = MCNPOutputParser()
        
    def analyze_kcode(self, output_file: str) -> dict:
        results = self.parser.parse_file(output_file)
        if not results['kcode']:
            return {'has_kcode': False}
        
        kcode = results['kcode']
        keff, sigma = kcode.k_combined
        
        analysis = {
            'has_kcode': True,
            'k_effective': keff,
            'uncertainty': sigma,
            'total_cycles': kcode.cycles,
            'active_cycles': kcode.active_cycles,
            'inactive_cycles': kcode.inactive_cycles,
            'converged': sigma < 0.005
        }
        return analysis
    
    def get_cycle_history(self, output_file: str) -> list:
        results = self.parser.parse_file(output_file)
        if results['kcode']:
            return results['kcode'].cycle_values
        return []
    
    def check_convergence(self, output_file: str) -> dict:
        analysis = self.analyze_kcode(output_file)
        if not analysis['has_kcode']:
            return {'converged': False, 'reason': 'No KCODE data'}
        
        converged = analysis['uncertainty'] < 0.005
        return {
            'converged': converged,
            'k_eff': analysis['k_effective'],
            'sigma': analysis['uncertainty'],
            'recommendation': 'Good' if converged else 'Run more cycles'
        }

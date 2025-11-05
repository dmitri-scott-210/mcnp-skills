"""MCNP Statistics Checker (Skill 20) - Verify 10 statistical checks

Based on MCNP6.3 Chapter 3 requirements:
1. Mean stable in final half
2. Relative error < 0.10 (ideally < 0.05)
3. Variance of variance (VOV) < 0.10
4. Figure of merit (FOM) relatively constant
5. PDF slope in range 3-10 for last half
6. All 10 bins passed
7. No oscillatory behavior
8. Confidence intervals overlap
9. Largest tally < 5% of total
10. Relative error decreases as 1/√N
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.output_parser import MCNPOutputParser

class MCNPStatisticsChecker:
    """Check MCNP tally statistics against 10 statistical checks"""

    def __init__(self):
        self.parser = MCNPOutputParser()

    def check_all_tallies(self, output_file: str) -> dict:
        """Check all tallies in output file

        Returns dict with tally number -> check results
        """
        results = self.parser.parse_file(output_file)
        tally_checks = {}
        
        for tally_num, tally in results['tallies'].items():
            checks = tally.statistical_checks
            all_passed = all(checks.values()) if checks else False
            tally_checks[tally_num] = {
                'all_passed': all_passed,
                'checks': checks,
                'fom': tally.figure_of_merit
            }
        
        return tally_checks
    
    def get_failed_checks(self, output_file: str) -> dict:
        self.parser.parse_file(output_file)
        return self.parser.get_failed_statistical_checks()
    
    def recommend_improvements(self, output_file: str) -> list:
        """Recommend improvements based on failed checks (Chapter 3)

        Common fixes:
        - Increase NPS
        - Improve variance reduction (importance, weight windows)
        - Check geometry for lost particles
        - Verify source definition
        - Use mesh tallies to visualize source
        """
        failed = self.get_failed_checks(output_file)
        recommendations = []

        for tally_num, checks in failed.items():
            if checks:
                # Specific recommendations based on which checks failed
                suggestions = []
                if 'relative_error' in checks:
                    suggestions.append('Increase NPS to reduce relative error')
                if 'vov' in checks:
                    suggestions.append('Improve variance reduction (IMP, WWN cards)')
                if 'fom_stability' in checks:
                    suggestions.append('Check for systematic errors in geometry or source')

                recommendations.append({
                    'tally': tally_num,
                    'issue': f"Failed {len(checks)} statistical checks",
                    'suggestions': suggestions if suggestions else ['Increase NPS or improve variance reduction']
                })

        return recommendations

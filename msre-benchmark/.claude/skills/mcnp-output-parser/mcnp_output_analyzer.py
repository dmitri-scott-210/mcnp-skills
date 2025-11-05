"""MCNP Output Analyzer (Skill 17) - Parse complete OUTP file

Analyzes main MCNP output file (OUTP) format:
- Problem summary
- Cross-section tables
- Cell/surface/material information
- Tally results with 10 statistical checks
- Figure of merit (FOM = 1/(R²×T))
- Tally fluctuation charts
- Warnings and errors (Chapter 3)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.output_parser import MCNPOutputParser

class MCNPOutputAnalyzer:
    """Parse and analyze MCNP main output file"""

    def __init__(self):
        self.parser = MCNPOutputParser()
        
    def analyze_output(self, filepath: str) -> dict:
        results = self.parser.parse_file(filepath)
        summary = {
            'terminated_normally': results['terminated_normally'],
            'n_warnings': len(results['warnings']),
            'n_errors': len(results['errors']),
            'n_tallies': len(results['tallies']),
            'has_kcode': results['kcode'] is not None,
            'computer_time': results['computer_time']
        }
        return {'summary': summary, 'details': results}
    
    def extract_warnings(self, filepath: str) -> list:
        results = self.parser.parse_file(filepath)
        return results['warnings']
    
    def extract_errors(self, filepath: str) -> list:
        results = self.parser.parse_file(filepath)
        return results['errors']
    
    def generate_report(self, filepath: str) -> str:
        analysis = self.analyze_output(filepath)
        lines = ["MCNP Output Analysis Report", "="*50]
        lines.append(f"Terminated normally: {analysis['summary']['terminated_normally']}")
        lines.append(f"Warnings: {analysis['summary']['n_warnings']}")
        lines.append(f"Errors: {analysis['summary']['n_errors']}")
        lines.append(f"Tallies: {analysis['summary']['n_tallies']}")
        return "\n".join(lines)

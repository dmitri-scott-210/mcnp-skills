"""MCNP Tally Analyzer (Skill 18) - Extract and analyze tally results

Tally types (Chapter 5):
- F1: Surface current
- F2: Surface flux
- F4: Cell flux
- F5: Point detector
- F6: Energy deposition
- F7: Fission energy
- F8: Pulse height

Analysis includes:
- Energy/time bins
- Relative errors
- Statistical checks
- Figure of merit
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.output_parser import MCNPOutputParser

class MCNPTallyAnalyzer:
    """Extract and analyze tally results from output"""

    def __init__(self):
        self.parser = MCNPOutputParser()
        
    def extract_tally_results(self, output_file: str) -> dict:
        results = self.parser.parse_file(output_file)
        return results['tallies']
    
    def get_tally_by_number(self, output_file: str, tally_num: int) -> dict:
        results = self.parser.parse_file(output_file)
        return results['tallies'].get(tally_num)
    
    def get_worst_error(self, output_file: str) -> tuple:
        self.parser.parse_file(output_file)
        return self.parser.get_worst_tally_error()
    
    def export_to_csv(self, tally_data: dict, output_file: str):
        """Export tally to CSV format"""
        import csv
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Bin', 'Value', 'Error'])
            for i, (val, err) in enumerate(zip(tally_data['values'], tally_data['errors'])):
                writer.writerow([i, val, err])

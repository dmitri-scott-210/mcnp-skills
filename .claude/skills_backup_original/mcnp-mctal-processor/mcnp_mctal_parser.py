"""MCNP MCTAL Parser (Skill 21) - Parse MCTAL tally files

MCTAL file format (ASCII):
- Header: Problem ID, NPS, particle types
- Tally blocks: Fn, particle, bins, values, errors
- Energy/time/angle bins
- Total/direct/flagged contributions

For HDF5 mesh tallies, see Appendix D.4:
- Use .xdmf files for visualization in ParaView/VisIt
- HDF5 structure: /results/mesh_tally_N/energy_bin_M/
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.output_parser import MCTALParser

class MCNPMCTALParser:
    """Parse MCTAL tally output files"""

    def __init__(self):
        self.parser = MCTALParser()
        
    def parse_mctal(self, mctal_file: str) -> dict:
        return self.parser.parse_file(mctal_file)
    
    def extract_tally(self, mctal_file: str, tally_num: int) -> dict:
        data = self.parser.parse_file(mctal_file)
        return data['tallies'].get(tally_num)
    
    def export_to_json(self, mctal_file: str, output_file: str):
        """Export MCTAL to JSON"""
        import json
        data = self.parser.parse_file(mctal_file)
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def list_tallies(self, mctal_file: str) -> list:
        data = self.parser.parse_file(mctal_file)
        return list(data['tallies'].keys())

"""MCNP Geometry Editor (Skill 8) - Modify cell/surface definitions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.input_parser import MCNPInputParser, SurfaceCard
from utils.geometry_evaluator import GeometryEvaluator

class MCNPGeometryEditor:
    def __init__(self):
        self.parser = MCNPInputParser()
        self.geom_eval = GeometryEvaluator()
        self.parsed = None

    def load_file(self, filepath: str):
        """Load and parse MCNP input file"""
        self.parsed = self.parser.parse_file(filepath)
        return self.parsed

    def modify_cell_parameter(self, cell_num: int, param: str, value):
        """Modify a parameter on a cell card"""
        if not self.parsed:
            return
        for cell in self.parsed['cells']:
            if cell.number == cell_num:
                cell.parameters[param] = value
                break

    def replace_surface_in_cells(self, old_surf: int, new_surf: int):
        """Replace surface number in all cell geometries"""
        if not self.parsed:
            return
        old_str = str(old_surf)
        new_str = str(new_surf)
        for cell in self.parsed['cells']:
            cell.geometry = self.geom_eval.substitute_surface(cell.geometry, old_str, new_str)

    def add_surface(self, surf_type: str, params: list) -> int:
        """Add a new surface card"""
        if not self.parsed:
            return -1
        surf_num = max([s.number for s in self.parsed['surfaces']], default=0) + 1
        surf = SurfaceCard(
            number=surf_num,
            mnemonic=surf_type.upper(),
            parameters=params,
            transformation=None,
            reflecting=False,
            white_boundary=False,
            raw=f"{surf_num} {surf_type.upper()} {' '.join(map(str, params))}"
        )
        self.parsed['surfaces'].append(surf)
        return surf_num

    def remove_surface(self, surf_num: int):
        """Remove a surface card"""
        if not self.parsed:
            return
        self.parsed['surfaces'] = [s for s in self.parsed['surfaces'] if s.number != surf_num]

    def save_file(self, filepath: str):
        """Save modified input to file"""
        if not self.parsed:
            return
        with open(filepath, 'w') as f:
            f.write(self.parser.to_string(self.parsed))

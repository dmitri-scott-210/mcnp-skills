"""MCNP Transform Editor (Skill 9) - Create/modify TR cards"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.transformations import TransformationMatrix
from parsers.input_parser import MCNPInputParser, DataCard

class MCNPTransformEditor:
    def __init__(self):
        self.parser = MCNPInputParser()
        self.transformations = {}
        self.parsed = None

    def load_file(self, filepath: str):
        """Load and parse MCNP input file"""
        self.parsed = self.parser.parse_file(filepath)
        return self.parsed

    def create_translation(self, tr_num: int, dx: float, dy: float, dz: float) -> str:
        """Create translation transformation"""
        trans = TransformationMatrix(tr_num)
        trans.translation = [dx, dy, dz]
        self.transformations[tr_num] = trans
        return trans.to_tr_card()

    def create_rotation(self, tr_num: int, axis: str, angle_deg: float) -> str:
        """Create rotation transformation"""
        trans = TransformationMatrix(tr_num)
        if axis.lower() == 'x':
            from utils.transformations import rotation_matrix_x
            trans.rotation = rotation_matrix_x(angle_deg)
        elif axis.lower() == 'y':
            from utils.transformations import rotation_matrix_y
            trans.rotation = rotation_matrix_y(angle_deg)
        else:
            from utils.transformations import rotation_matrix_z
            trans.rotation = rotation_matrix_z(angle_deg)
        self.transformations[tr_num] = trans
        return trans.to_tr_card()

    def apply_to_cell(self, cell_num: int, tr_num: int):
        """Apply transformation to a cell"""
        if not self.parsed:
            return
        for cell in self.parsed['cells']:
            if cell.number == cell_num:
                cell.parameters['trcl'] = tr_num
                break

    def generate_tr_cards(self) -> list:
        """Generate all TR data cards"""
        cards = []
        for tr_num, trans in sorted(self.transformations.items()):
            tr_card = trans.to_tr_card()
            cards.append(tr_card)
        return cards

    def save_file(self, filepath: str):
        """Save modified input to file"""
        if not self.parsed:
            return
        with open(filepath, 'w') as f:
            f.write(self.parser.to_string(self.parsed))

    def generate_plot_command(self, origin: tuple, basis: str, extent: tuple) -> str:
        """Generate MCNP plot command"""
        return f"plot origin={origin[0]} {origin[1]} {origin[2]} basis={basis} extent={extent[0]} {extent[1]}"

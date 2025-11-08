"""MCNP Geometry Checker (Skill 13) - Validate geometry definitions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.input_parser import MCNPInputParser
from utils.geometry_evaluator import GeometryEvaluator

class MCNPGeometryChecker:
    def __init__(self):
        self.parser = MCNPInputParser()
        self.geom_eval = GeometryEvaluator()
        self.parsed = None
        self.issues = []

    def check_geometry(self, filepath: str) -> list:
        """Check geometry for issues (based on Chapters 3 & 4)"""
        self.issues = []
        self.parsed = self.parser.parse_file(filepath)
        self._check_surface_usage()
        self._check_cell_definitions()
        self._check_voids()
        self._check_boolean_operators()
        self._check_geometry_recommendations()
        return self.issues

    def _check_surface_usage(self):
        """Check for unused surfaces"""
        defined = {s.number for s in self.parsed['surfaces']}
        used = set()
        for cell in self.parsed['cells']:
            used.update(self.geom_eval.get_all_surfaces(cell.geometry))
        unused = defined - used
        for surf in unused:
            self.issues.append({'type':'warning','message':f'Surface {surf} defined but not used'})

    def _check_cell_definitions(self):
        """Validate cell geometry definitions"""
        for cell in self.parsed['cells']:
            valid, msg = self.geom_eval.is_valid_geometry(cell.geometry)
            if not valid:
                self.issues.append({'type':'error','message':f'Cell {cell.number}: {msg}'})

    def _check_voids(self):
        """Check for void cells"""
        void_cells = [c for c in self.parsed['cells'] if c.material==0]
        if not void_cells:
            self.issues.append({'type':'info','message':'No void cells defined'})
    
    def _check_boolean_operators(self):
        """Check for common Boolean operator errors (Chapter 4)"""
        for cell in self.parsed['cells']:
            geom = cell.geometry
            # Check for excessive complement operators
            if geom.count('#') > 3:
                self.issues.append({
                    'type': 'warning',
                    'message': f'Cell {cell.number}: Excessive use of complement operator (#) - may indicate geometry error'
                })

            # Check for potentially incorrect precedence
            if ':' in geom and '(' not in geom:
                self.issues.append({
                    'type': 'info',
                    'message': f'Cell {cell.number}: Union operator (:) without parentheses - verify operator precedence'
                })

    def _check_geometry_recommendations(self):
        """Add geometry checking recommendations (Chapter 3)"""
        self.issues.append({
            'type': 'recommendation',
            'message': 'ALWAYS plot geometry from multiple directions before production runs'
        })
        self.issues.append({
            'type': 'recommendation',
            'message': 'Use VOID card to flood geometry and detect overlaps/gaps quickly'
        })
        self.issues.append({
            'type': 'recommendation',
            'message': 'Watch for dashed lines in plots - indicate geometry errors'
        })

    def generate_plot_commands(self) -> list:
        """Generate PLOT commands for visualization (Chapter 3)"""
        return [
            "plot origin=0 0 0 basis=xy extent=50 50",
            "plot origin=0 0 0 basis=xz extent=50 50",
            "plot origin=0 0 0 basis=yz extent=50 50"
        ]

    def generate_void_test_input(self) -> str:
        """Generate VOID card test setup (Chapter 3)"""
        return """c VOID CARD GEOMETRY TEST
c Add this to your input for geometry validation:
void
c Run with high NPS (e.g., nps 1000000) to flood geometry
c Remove VOID card once geometry is verified"""

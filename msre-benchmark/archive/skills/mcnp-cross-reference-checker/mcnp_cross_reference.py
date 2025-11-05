"""MCNP Cross Reference Checker (Skill 16) - Check all references"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.input_parser import MCNPInputParser
from utils.geometry_evaluator import GeometryEvaluator

class MCNPCrossReferenceChecker:
    def __init__(self):
        self.parser = MCNPInputParser()
        self.geom_eval = GeometryEvaluator()
        self.parsed = None

    def build_dependency_graph(self, filepath: str) -> dict:
        """Build dependency graph of all references"""
        self.parsed = self.parser.parse_file(filepath)

        graph = {
            'cells_to_surfaces': {},
            'cells_to_materials': {},
            'tallies_to_cells': {},
            'unused_surfaces': [],
            'unused_materials': []
        }

        # Build cell->surface mapping
        for cell in self.parsed['cells']:
            surfs = self.geom_eval.get_all_surfaces(cell.geometry)
            graph['cells_to_surfaces'][cell.number] = list(surfs)
            if cell.material > 0:
                graph['cells_to_materials'][cell.number] = cell.material

        # Check unused
        defined_surfs = {s.number for s in self.parsed['surfaces']}
        used_surfs = set()
        for surfs in graph['cells_to_surfaces'].values():
            used_surfs.update(surfs)
        graph['unused_surfaces'] = list(defined_surfs - used_surfs)

        return graph

    def find_broken_references(self, filepath: str) -> list:
        """Find all broken cross-references"""
        graph = self.build_dependency_graph(filepath)
        broken = []

        defined_surfs = {s.number for s in self.parsed['surfaces']}
        for cell_num, surfs in graph['cells_to_surfaces'].items():
            for surf in surfs:
                if surf not in defined_surfs:
                    broken.append({'cell': cell_num, 'missing_surface': surf})

        return broken

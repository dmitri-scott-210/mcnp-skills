"""MCNP Example Finder (Skill 31) - Search example database"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from knowledge_base.example_finder import ExampleFinder

class MCNPExampleFinderSkill:
    def __init__(self, examples_root: str = None):
        if not examples_root:
            examples_root = str(Path(__file__).parent.parent.parent / 'example_files')
        self.finder = ExampleFinder(examples_root)
        self.finder.index_all()
    
    def search(self, keyword: str, max_results: int = 10) -> list:
        """Search examples by keyword"""
        examples = self.finder.search(keyword, max_results)
        return [{'file': ex.filename, 'category': ex.category, 'description': ex.description} for ex in examples]
    
    def get_simple_examples(self, count: int = 5) -> list:
        """Get simplest examples for beginners"""
        examples = self.finder.get_simple_examples(count)
        return [{'file': ex.filename, 'path': ex.file_path, 'description': ex.description} for ex in examples]
    
    def find_by_feature(self, criticality=False, tallies=False, variance_reduction=False) -> list:
        """Find examples with specific features"""
        examples = self.finder.get_by_feature(criticality, tallies, variance_reduction)
        return [{'file': ex.filename, 'category': ex.category} for ex in examples]
    
    def get_category_summary(self) -> dict:
        """Get count of examples by category"""
        return {cat: len(exs) for cat, exs in self.finder.category_index.items()}

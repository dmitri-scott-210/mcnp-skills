"""
Example Finder
Search and retrieve MCNP example files
"""

import os
import re
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class MCNPExample:
    """Represents an MCNP example file"""
    file_path: str
    filename: str
    category: str
    description: str = ""
    has_criticality: bool = False
    has_tallies: bool = False
    has_variance_reduction: bool = False
    complexity: str = "basic"  # basic, intermediate, advanced
    

class ExampleFinder:
    """
    Find and categorize MCNP example input files
    
    Searches 1,147+ example files across:
    - Basic examples (100+)
    - Criticality examples
    - Intermediate examples
    - MCNP6 V&V suite (120+ benchmarks)
    - Radiation protection examples
    - Reactor models
    - Safeguards examples
    - Unstructured mesh examples (15+)
    - Variance reduction examples (19)
    """
    
    def __init__(self, examples_root: str):
        """
        Initialize example finder
        
        Args:
            examples_root: Path to example_files directory
        """
        self.examples_root = Path(examples_root)
        self.examples: List[MCNPExample] = []
        self.category_index: Dict[str, List[MCNPExample]] = {}
        
    def index_all(self):
        """Index all MCNP example files"""
        if not self.examples_root.exists():
            print(f"Warning: Examples root not found: {self.examples_root}")
            return
        
        # Find all MCNP input files (.txt, .inp, .i)
        patterns = ['**/*.txt', '**/*.inp', '**/*.i']
        
        for pattern in patterns:
            for file_path in self.examples_root.glob(pattern):
                # Skip output files and data files
                if any(skip in str(file_path).lower() for skip in ['outp', 'mctal', 'meshtal', 'runtpe']):
                    continue
                
                example = self._analyze_example(file_path)
                if example:
                    self.examples.append(example)
                    
                    # Add to category index
                    if example.category not in self.category_index:
                        self.category_index[example.category] = []
                    self.category_index[example.category].append(example)
        
        print(f"Indexed {len(self.examples)} example files across {len(self.category_index)} categories")
    
    def _analyze_example(self, file_path: Path) -> Optional[MCNPExample]:
        """Analyze an example file to extract metadata"""
        try:
            # Determine category from path
            path_str = str(file_path.relative_to(self.examples_root))
            category = self._extract_category(path_str)
            
            # Read first 100 lines to analyze
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [f.readline() for _ in range(100)]
                content = ''.join(lines).lower()
            
            # Extract description (title line)
            description = lines[0].strip() if lines else ""
            
            # Detect features
            has_criticality = 'kcode' in content or 'ksrc' in content
            has_tallies = any(f'f{i}:' in content or f'f{i} ' in content for i in range(1, 9))
            has_variance_reduction = any(term in content for term in ['imp:', 'wwn', 'dxtran', 'ext'])
            
            # Determine complexity
            complexity = self._assess_complexity(content, file_path)
            
            return MCNPExample(
                file_path=str(file_path),
                filename=file_path.name,
                category=category,
                description=description,
                has_criticality=has_criticality,
                has_tallies=has_tallies,
                has_variance_reduction=has_variance_reduction,
                complexity=complexity
            )
            
        except Exception as e:
            return None
    
    def _extract_category(self, path: str) -> str:
        """Extract category from file path"""
        path_lower = path.lower()
        
        if 'basic' in path_lower:
            return 'basic'
        elif 'criticality' in path_lower or 'crit_' in path_lower:
            return 'criticality'
        elif 'intermediate' in path_lower:
            return 'intermediate'
        elif 'vnv' in path_lower or 'validation' in path_lower:
            return 'validation'
        elif 'rad-protection' in path_lower:
            return 'radiation_protection'
        elif 'reactor' in path_lower:
            return 'reactor_model'
        elif 'safeguards' in path_lower:
            return 'safeguards'
        elif 'unstructured' in path_lower or 'mesh' in path_lower:
            return 'unstructured_mesh'
        elif 'variance' in path_lower:
            return 'variance_reduction'
        else:
            return 'other'
    
    def _assess_complexity(self, content: str, file_path: Path) -> str:
        """Assess complexity level of example"""
        # Count various features
        cell_count = content.count('imp:')
        has_lattice = 'lat=' in content or 'fill=' in content
        has_transformations = ' tr' in content or '*tr' in content
        has_universes = ' u=' in content or 'fill=' in content
        has_mesh = 'fmesh' in content or 'embed' in content
        
        # File size as complexity indicator
        try:
            size = os.path.getsize(file_path)
            line_count = size / 50  # Rough estimate
        except:
            line_count = 0
        
        # Complexity scoring
        score = 0
        if cell_count > 50:
            score += 2
        elif cell_count > 20:
            score += 1
        
        if has_lattice:
            score += 1
        if has_transformations:
            score += 1
        if has_universes:
            score += 1
        if has_mesh:
            score += 2
        
        if line_count > 1000:
            score += 2
        elif line_count > 500:
            score += 1
        
        if score >= 5:
            return 'advanced'
        elif score >= 2:
            return 'intermediate'
        else:
            return 'basic'
    
    def search(self, query: str, max_results: int = 10) -> List[MCNPExample]:
        """
        Search examples by keyword
        
        Args:
            query: Search query
            max_results: Maximum results to return
        
        Returns:
            List of matching examples
        """
        query_lower = query.lower()
        results = []
        
        for example in self.examples:
            # Search in filename and description
            if (query_lower in example.filename.lower() or 
                query_lower in example.description.lower() or
                query_lower in example.category.lower()):
                results.append(example)
        
        return results[:max_results]
    
    def get_by_category(self, category: str) -> List[MCNPExample]:
        """Get all examples in a category"""
        return self.category_index.get(category.lower(), [])
    
    def get_by_complexity(self, complexity: str) -> List[MCNPExample]:
        """Get examples by complexity level"""
        return [ex for ex in self.examples if ex.complexity == complexity.lower()]
    
    def get_by_feature(self, criticality: bool = False, tallies: bool = False, 
                       variance_reduction: bool = False) -> List[MCNPExample]:
        """Get examples with specific features"""
        results = []
        for ex in self.examples:
            match = True
            if criticality and not ex.has_criticality:
                match = False
            if tallies and not ex.has_tallies:
                match = False
            if variance_reduction and not ex.has_variance_reduction:
                match = False
            
            if match:
                results.append(ex)
        
        return results
    
    def get_simple_examples(self, count: int = 5) -> List[MCNPExample]:
        """Get simplest examples for beginners"""
        basic_examples = self.get_by_complexity('basic')
        # Sort by filename length (shorter usually simpler)
        basic_examples.sort(key=lambda x: len(x.filename))
        return basic_examples[:count]


if __name__ == "__main__":
    # Test example finder
    examples_root = Path(__file__).parent.parent / "example_files"
    finder = ExampleFinder(str(examples_root))
    finder.index_all()
    
    # Test search
    print("\n=== Category Summary ===")
    for category, examples in finder.category_index.items():
        print(f"{category:25s}: {len(examples):4d} examples")
    
    print("\n=== Simple Examples ===")
    simple = finder.get_simple_examples(5)
    for ex in simple:
        print(f"  {ex.filename:30s} - {ex.description[:50]}")
    
    print("\n=== Criticality Examples ===")
    crit = finder.get_by_feature(criticality=True)
    print(f"  Found {len(crit)} criticality examples")

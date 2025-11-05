"""
Documentation Indexer
Index and search MCNP documentation markdown files
"""

import os
import re
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DocumentSection:
    """Represents a section of documentation"""
    file_path: str
    title: str
    content: str
    section_level: int
    line_number: int
    keywords: List[str]


class DocumentationIndexer:
    """
    Index and search MCNP6 documentation
    
    Handles 72 markdown files across:
    - Theory manual (13 files)
    - User manual (21 files)  
    - Examples (6 files)
    - Primers (6 files)
    - Appendices (25 files)
    """
    
    def __init__(self, docs_root: str):
        """
        Initialize documentation indexer
        
        Args:
            docs_root: Path to markdown_docs directory
        """
        self.docs_root = Path(docs_root)
        self.sections: List[DocumentSection] = []
        self.file_index: Dict[str, List[DocumentSection]] = {}
        self.keyword_index: Dict[str, List[DocumentSection]] = {}
        
    def index_all(self):
        """Index all markdown documentation files"""
        if not self.docs_root.exists():
            print(f"Warning: Documentation root not found: {self.docs_root}")
            return
        
        # Find all markdown files
        md_files = list(self.docs_root.rglob("*.md"))
        
        print(f"Indexing {len(md_files)} documentation files...")
        
        for md_file in md_files:
            if md_file.name != "README.md":  # Skip README
                self._index_file(md_file)
        
        print(f"Indexed {len(self.sections)} sections from {len(self.file_index)} files")
        
    def _index_file(self, file_path: Path):
        """Index a single markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Split into sections based on headers
            sections = self._split_into_sections(content, str(file_path))
            
            for section in sections:
                self.sections.append(section)
                
                # Add to file index
                file_key = str(file_path.relative_to(self.docs_root))
                if file_key not in self.file_index:
                    self.file_index[file_key] = []
                self.file_index[file_key].append(section)
                
                # Add to keyword index
                for keyword in section.keywords:
                    keyword_lower = keyword.lower()
                    if keyword_lower not in self.keyword_index:
                        self.keyword_index[keyword_lower] = []
                    self.keyword_index[keyword_lower].append(section)
                    
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
    
    def _split_into_sections(self, content: str, file_path: str) -> List[DocumentSection]:
        """Split markdown content into sections"""
        sections = []
        lines = content.split('\n')
        
        current_section = []
        current_title = "Introduction"
        current_level = 1
        current_line = 1
        
        for i, line in enumerate(lines, 1):
            # Check for markdown headers
            if line.startswith('#'):
                # Save previous section
                if current_section:
                    section_content = '\n'.join(current_section)
                    keywords = self._extract_keywords(section_content)
                    
                    sections.append(DocumentSection(
                        file_path=file_path,
                        title=current_title,
                        content=section_content,
                        section_level=current_level,
                        line_number=current_line,
                        keywords=keywords
                    ))
                
                # Start new section
                current_level = len(line) - len(line.lstrip('#'))
                current_title = line.lstrip('#').strip()
                current_section = []
                current_line = i
            else:
                current_section.append(line)
        
        # Add final section
        if current_section:
            section_content = '\n'.join(current_section)
            keywords = self._extract_keywords(section_content)
            
            sections.append(DocumentSection(
                file_path=file_path,
                title=current_title,
                content=section_content,
                section_level=current_level,
                line_number=current_line,
                keywords=keywords
            ))
        
        return sections
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Common MCNP terms to index
        mcnp_terms = [
            'cell', 'surface', 'material', 'tally', 'source', 'kcode', 'criticality',
            'geometry', 'transformation', 'lattice', 'universe', 'fill',
            'neutron', 'photon', 'electron', 'particle',
            'energy', 'cross section', 'library', 'xsdir', 'zaid',
            'variance reduction', 'importance', 'weight window', 'dxtran',
            'mesh', 'fmesh', 'tmesh', 'unstructured',
            'burnup', 'depletion', 'activation',
            'error', 'warning', 'fatal', 'lost particle',
            'mode', 'phys', 'cut', 'nps', 'print', 'ptrac'
        ]
        
        keywords = []
        text_lower = text.lower()
        
        # Find MCNP terms
        for term in mcnp_terms:
            if term in text_lower:
                keywords.append(term)
        
        # Find card names (uppercase words followed by optional number)
        card_pattern = r'\b([A-Z]{2,}[0-9]*)\b'
        cards = re.findall(card_pattern, text)
        keywords.extend(cards[:20])  # Limit to 20 cards
        
        return list(set(keywords))  # Remove duplicates
    
    def search(self, query: str, max_results: int = 10) -> List[DocumentSection]:
        """
        Search documentation by keyword or phrase
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
        
        Returns:
            List of matching document sections
        """
        query_lower = query.lower()
        results = []
        
        # Search in keywords first
        for keyword, sections in self.keyword_index.items():
            if query_lower in keyword:
                results.extend(sections)
        
        # Search in titles
        for section in self.sections:
            if query_lower in section.title.lower():
                if section not in results:
                    results.append(section)
        
        # Search in content
        for section in self.sections:
            if query_lower in section.content.lower():
                if section not in results:
                    results.append(section)
        
        # Score and sort results
        scored_results = []
        for section in results:
            score = 0
            # Title match is worth more
            if query_lower in section.title.lower():
                score += 10
            # Keyword match
            if any(query_lower in kw.lower() for kw in section.keywords):
                score += 5
            # Content match (count occurrences)
            score += section.content.lower().count(query_lower)
            
            scored_results.append((score, section))
        
        # Sort by score descending
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        return [section for score, section in scored_results[:max_results]]
    
    def get_by_category(self, category: str) -> List[DocumentSection]:
        """
        Get sections by documentation category
        
        Categories: 'theory', 'user', 'examples', 'primers', 'appendices'
        """
        results = []
        for file_path, sections in self.file_index.items():
            if category.lower() in file_path.lower():
                results.extend(sections)
        return results
    
    def get_card_documentation(self, card_type: str) -> List[DocumentSection]:
        """Get documentation for specific card type (e.g., 'SDEF', 'F4', 'M')"""
        return self.search(card_type, max_results=5)


if __name__ == "__main__":
    # Test indexer
    docs_root = Path(__file__).parent.parent / "markdown_docs"
    indexer = DocumentationIndexer(str(docs_root))
    indexer.index_all()
    
    # Test search
    print("\n=== Testing Search ===")
    results = indexer.search("tally", max_results=3)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.title}")
        print(f"   File: {Path(result.file_path).name}")
        print(f"   Keywords: {', '.join(result.keywords[:5])}")

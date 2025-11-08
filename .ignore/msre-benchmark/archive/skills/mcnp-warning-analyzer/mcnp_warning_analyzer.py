"""MCNP Warning Analyzer (Skill 15) - Analyze and categorize warnings"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from knowledge_base.error_patterns import ErrorPatternDatabase

class MCNPWarningAnalyzer:
    def __init__(self):
        self.error_db = ErrorPatternDatabase()
        
    def analyze_warnings(self, output_file: str) -> dict:
        with open(output_file, 'r', errors='ignore') as f:
            content = f.read()
        
        warnings = {'geometry': [], 'material': [], 'tally': [], 'source': [], 'other': []}
        
        for line in content.split('\n'):
            if 'warning' in line.lower():
                matches = self.error_db.match_error(line)
                category = matches[0].category if matches else 'other'
                if category in warnings:
                    warnings[category].append(line.strip())
                else:
                    warnings['other'].append(line.strip())
        
        return warnings
    
    def prioritize_warnings(self, warnings: dict) -> list:
        """Sort warnings by severity"""
        priority_order = ['geometry', 'material', 'source', 'tally', 'other']
        prioritized = []
        for cat in priority_order:
            for warn in warnings.get(cat, []):
                prioritized.append({'category': cat, 'message': warn})
        return prioritized

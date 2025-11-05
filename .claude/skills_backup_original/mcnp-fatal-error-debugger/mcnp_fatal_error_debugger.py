"""MCNP Fatal Error Debugger (Skill 14) - Diagnose fatal errors"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from knowledge_base.error_patterns import ErrorPatternDatabase

class MCNPFatalErrorDebugger:
    def __init__(self):
        self.error_db = ErrorPatternDatabase()
        
    def diagnose_error(self, output_file: str) -> dict:
        with open(output_file, 'r', errors='ignore') as f:
            content = f.read()
        
        errors_found = []
        for line in content.split('\n'):
            if 'fatal' in line.lower() or 'bad trouble' in line.lower():
                matches = self.error_db.match_error(line)
                if matches:
                    errors_found.append({
                        'message': line,
                        'pattern': matches[0],
                        'fix': matches[0].fix,
                        'example': matches[0].example
                    })
        return {'errors': errors_found, 'count': len(errors_found)}
    
    def suggest_fix(self, error_message: str) -> str:
        suggestion = self.error_db.suggest_fix(error_message)
        return suggestion if suggestion else "No known fix for this error"
    
    def get_common_errors(self) -> list:
        return self.error_db.get_all_fatal_errors()

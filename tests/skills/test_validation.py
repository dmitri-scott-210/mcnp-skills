"""
Test suite for Category C: Validation Skills (5 skills)
"""
import pytest
import sys
from pathlib import Path

# Add project root to path to import from .claude/skills/
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import from new .claude/skills/ structure
from claude.skills.mcnp_input_validator.mcnp_input_validator import MCNPInputValidator
from claude.skills.mcnp_geometry_checker.mcnp_geometry_checker import MCNPGeometryChecker
from claude.skills.mcnp_fatal_error_debugger.mcnp_fatal_error_debugger import MCNPFatalErrorDebugger
from claude.skills.mcnp_warning_analyzer.mcnp_warning_analyzer import MCNPWarningAnalyzer
from claude.skills.mcnp_cross_reference_checker.mcnp_cross_reference import MCNPCrossReferenceChecker

class TestMCNPInputValidator:
    
    def test_validate_simple_input(self, simple_input):
        """Test validation of simple input"""
        validator = MCNPInputValidator()
        result = validator.validate_string(simple_input)
        
        assert result['is_valid'] is True
        assert 'errors' in result
    
    def test_detect_missing_blocks(self):
        """Test detecting missing blocks"""
        incomplete = "test\n1 0 -1 imp:n=1\n"
        
        validator = MCNPInputValidator()
        result = validator.validate_string(incomplete)
        
        # Should detect missing surface block
        assert result['is_valid'] is False
    
    def test_validate_cross_references(self, tal01_input):
        """Test cross-reference validation"""
        validator = MCNPInputValidator()
        result = validator.validate_string(tal01_input)
        
        # Should check that materials reference valid isotopes
        assert 'warnings' in result or 'errors' in result
    
    def test_validate_all_examples(self, all_example_files):
        """Test validation on all example files"""
        validator = MCNPInputValidator()
        valid_count = 0
        total = 0
        
        for filepath in all_example_files:
            total += 1
            if total > 100:  # Sample first 100 files
                break
            
            try:
                result = validator.validate_file(str(filepath))
                if result.get('is_valid'):
                    valid_count += 1
            except:
                pass
        
        print(f"Validated {valid_count}/{total} files successfully")

class TestMCNPGeometryChecker:
    
    def test_check_basic_geometry(self, simple_input):
        """Test basic geometry checking"""
        checker = MCNPGeometryChecker()
        result = checker.check_geometry_string(simple_input)
        
        assert 'surfaces' in result
        assert 'cells' in result
    
    def test_detect_unused_surfaces(self):
        """Test detecting unused surfaces"""
        input_with_unused = """test
1 0 -1 imp:n=1

1 so 1
2 pz 5
3 cz 2

"""
        checker = MCNPGeometryChecker()
        result = checker.check_geometry_string(input_with_unused)
        
        # Should detect surfaces 2 and 3 are unused
        assert 'unused_surfaces' in result
    
    def test_generate_plot_commands(self, tal01_input):
        """Test plot command generation"""
        checker = MCNPGeometryChecker()
        plots = checker.generate_plot_commands(tal01_input)
        
        assert len(plots) > 0
        assert any('px' in p.lower() for p in plots)

class TestMCNPFatalErrorDebugger:
    
    def test_diagnose_sourcc_error(self):
        """Test diagnosing sourcc fatal error"""
        output = """
fatal error.  bad trouble in subroutine sourcc of mcrun
        """
        
        debugger = MCNPFatalErrorDebugger()
        diagnosis = debugger.diagnose_error(output)
        
        assert 'sourcc' in diagnosis.lower()
        assert 'source' in diagnosis.lower()
    
    def test_diagnose_lost_particle(self):
        """Test diagnosing lost particle"""
        output = """
particle  12345678 lost.
   x,y,z coordinates:  1.23456E+01  2.34567E+01  3.45678E+01
        """
        
        debugger = MCNPFatalErrorDebugger()
        diagnosis = debugger.diagnose_error(output)
        
        assert 'lost' in diagnosis.lower()
        assert 'geometry' in diagnosis.lower()
    
    def test_suggest_fix(self):
        """Test fix suggestions"""
        debugger = MCNPFatalErrorDebugger()
        fix = debugger.suggest_fix('bad trouble in subroutine sourcc')
        
        assert len(fix) > 0
        assert 'sdef' in fix.lower() or 'source' in fix.lower()

class TestMCNPWarningAnalyzer:
    
    def test_analyze_warnings(self):
        """Test warning analysis"""
        output = """
warning.  material        1 has been set to a conductor.
warning.  tally        5 needs more than 1000 histories.
warning.  cell      100 is not used.
        """
        
        analyzer = MCNPWarningAnalyzer()
        result = analyzer.analyze_warnings(output)
        
        assert len(result['warnings']) == 3
    
    def test_prioritize_warnings(self):
        """Test warning prioritization"""
        output = """
warning.  tally has not passed all 10 statistical checks.
warning.  cell   50 has importance=0 but volume>0.
        """
        
        analyzer = MCNPWarningAnalyzer()
        result = analyzer.analyze_warnings(output)
        priorities = analyzer.prioritize_warnings(result['warnings'])
        
        # Tally check failures should be high priority
        assert any('tally' in w['message'].lower() for w in priorities if w['priority'] == 'high')

class TestMCNPCrossReferenceChecker:
    
    def test_build_dependency_graph(self, tal01_input):
        """Test building dependency graph"""
        checker = MCNPCrossReferenceChecker()
        graph = checker.build_dependency_graph(tal01_input)
        
        assert 'cells' in graph
        assert 'surfaces' in graph
        assert 'materials' in graph
    
    def test_find_broken_references(self):
        """Test finding broken references"""
        bad_input = """test
1 999 -1.0 -1 imp:n=1

1 so 5

"""
        checker = MCNPCrossReferenceChecker()
        broken = checker.find_broken_references(bad_input)
        
        # Material 999 doesn't exist
        assert len(broken) > 0
        assert any('m999' in str(b).lower() for b in broken)

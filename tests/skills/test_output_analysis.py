"""
Test suite for Category D: Output Analysis Skills (5 skills)
"""
import pytest
import sys
from pathlib import Path

# Add project root to path to import from .claude/skills/
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import from new .claude/skills/ structure
from claude.skills.mcnp_output_parser.mcnp_output_analyzer import MCNPOutputAnalyzer
from claude.skills.mcnp_tally_analyzer.mcnp_tally_analyzer import MCNPTallyAnalyzer
from claude.skills.mcnp_criticality_analyzer.mcnp_criticality_analyzer import MCNPCriticalityAnalyzer
from claude.skills.mcnp_statistics_checker.mcnp_statistics_checker import MCNPStatisticsChecker
from claude.skills.mcnp_mctal_processor.mcnp_mctal_parser import MCNPMctalParser

class TestMCNPOutputAnalyzer:
    
    def test_analyze_output_basic(self):
        """Test basic output analysis"""
        sample_output = """
1mcnp     version 6.3.0  03/01/2023
 
          Code Name & Version = MCNP6.3, 6.3.0
          
 comment.  total nubar used if fissionable isotopes are present.
 comment.  setting up hash tables.
 comment.  loading cross section tables.
 
 problem summary                                                                                                   
                  run terminated when     1000000  particle histories were done.
        """
        
        analyzer = MCNPOutputAnalyzer()
        result = analyzer.analyze_output(sample_output)
        
        assert 'version' in result
        assert 'particles_run' in result
    
    def test_generate_report(self):
        """Test report generation"""
        sample = "1mcnp version 6.3.0\n\nrun terminated when 1000000 particle histories were done."
        
        analyzer = MCNPOutputAnalyzer()
        result = analyzer.analyze_output(sample)
        report = analyzer.generate_report(result)
        
        assert len(report) > 0
        assert 'summary' in report.lower() or 'report' in report.lower()

class TestMCNPTallyAnalyzer:
    
    def test_extract_tally_results(self):
        """Test extracting tally data"""
        sample_output = """
1tally        4        nps =     1000000
           tally type 4    track length estimate of particle flux.      units   1/cm**2   

      cell  10
                                 
 cell  10                                                                                                          
                   1.2345E-02 0.0234
        """
        
        analyzer = MCNPTallyAnalyzer()
        tallies = analyzer.extract_tally_results(sample_output)
        
        assert len(tallies) > 0
        assert tallies[0]['number'] == 4
    
    def test_get_worst_error(self):
        """Test finding worst relative error"""
        sample = """
1tally  1
 cell 10    1.23E-02 0.0150
 cell 20    2.45E-02 0.1200
 cell 30    3.67E-02 0.0500
        """
        
        analyzer = MCNPTallyAnalyzer()
        tallies = analyzer.extract_tally_results(sample)
        worst = analyzer.get_worst_error(tallies)
        
        assert worst['relative_error'] == 0.12
    
    def test_export_to_csv(self):
        """Test CSV export"""
        sample = """
1tally  1
 cell 10    1.23E-02 0.0150
        """
        
        analyzer = MCNPTallyAnalyzer()
        tallies = analyzer.extract_tally_results(sample)
        csv = analyzer.export_to_csv(tallies)
        
        assert 'tally' in csv.lower()
        assert '1.23E-02' in csv or '0.0123' in csv

class TestMCNPCriticalityAnalyzer:
    
    def test_analyze_kcode(self):
        """Test KCODE analysis"""
        sample_output = """
the final estimated combined collision/absorption/track-length keff = 1.00234 with an estimated standard deviation of 0.00123

 the minimum estimated standard deviations in the individual estimators occurred at cycle       85
        """
        
        analyzer = MCNPCriticalityAnalyzer()
        result = analyzer.analyze_kcode(sample_output)
        
        assert abs(result['k_effective'] - 1.00234) < 0.00001
        assert result['k_std_dev'] == 0.00123
    
    def test_check_convergence(self):
        """Test convergence checking"""
        sample = """
the final estimated combined keff = 1.00234 with an estimated standard deviation of 0.00123

the estimated prompt neutron removal lifetime =  1.23E-05 seconds with an estimated standard deviation of 2.34E-07
        """
        
        analyzer = MCNPCriticalityAnalyzer()
        result = analyzer.analyze_kcode(sample)
        convergence = analyzer.check_convergence(result)
        
        assert 'is_converged' in convergence

class TestMCNPStatisticsChecker:
    
    def test_check_all_10_tests(self):
        """Test all 10 statistical checks"""
        tally_data = {
            'number': 4,
            'mean': 1.234e-2,
            'relative_error': 0.05,
            'bins': [
                {'value': 1.23e-2, 'error': 0.05},
                {'value': 2.34e-2, 'error': 0.06}
            ]
        }
        
        checker = MCNPStatisticsChecker()
        results = checker.check_all_tallies([tally_data])
        
        assert len(results) > 0
        assert 'passed_checks' in results[0]
    
    def test_get_failed_checks(self):
        """Test identifying failed checks"""
        bad_tally = {
            'number': 1,
            'mean': 1.234e-2,
            'relative_error': 0.25,  # High error
            'bins': []
        }
        
        checker = MCNPStatisticsChecker()
        results = checker.check_all_tallies([bad_tally])
        failed = checker.get_failed_checks(results)
        
        assert len(failed) > 0
    
    def test_recommend_improvements(self):
        """Test improvement recommendations"""
        checker = MCNPStatisticsChecker()
        recommendations = checker.recommend_improvements(
            {'passed_checks': 7, 'failed_checks': 3}
        )
        
        assert len(recommendations) > 0
        assert 'histories' in recommendations.lower() or 'variance' in recommendations.lower()

class TestMCNPMctalParser:
    
    def test_parse_mctal_header(self):
        """Test parsing MCTAL header"""
        sample_mctal = """mcnp   version 6     ld=03/01/23  probid =  01/15/24 12:00:00
nps =     1000000  nrn =     123456789
        """
        
        parser = MCNPMctalParser()
        result = parser.parse_mctal(sample_mctal)
        
        assert 'nps' in result
        assert result['nps'] == 1000000
    
    def test_extract_tally_from_mctal(self):
        """Test extracting specific tally"""
        sample = """mcnp version 6
tally       4
f       4:n  10
d   0 0 1
u   1 1 1
s   0 0 0
m   0 0 0
c   0 0 0
vals
 1.234E-02 5.678E-04
        """
        
        parser = MCNPMctalParser()
        result = parser.parse_mctal(sample)
        tally4 = parser.extract_tally(result, 4)
        
        assert tally4 is not None
        assert len(tally4['values']) > 0
    
    def test_export_to_json(self):
        """Test JSON export"""
        sample = """mcnp version 6
nps = 1000000
        """
        
        parser = MCNPMctalParser()
        result = parser.parse_mctal(sample)
        json_str = parser.export_to_json(result)
        
        assert 'nps' in json_str
        assert '1000000' in json_str

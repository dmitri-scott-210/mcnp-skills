"""
Test suite for parsers/output_parser.py
"""
import pytest
from parsers.output_parser import MCNPOutputParser, TallyResult, KCODEResult

class TestMCNPOutputParser:
    
    def test_parse_tally_results(self):
        """Test parsing tally results from OUTP"""
        sample_output = """
1tally        1        nps =     1000000
           tally type 1    number of particles crossing a surface.
 
      surface  1
 
 surface 1                                                                                                         
      energy
    1.0000E-02   1.5234E-03 0.0234
    2.0000E-02   2.8976E-03 0.0198
    3.0000E-02   4.1234E-03 0.0156
        """
        
        parser = MCNPOutputParser()
        result = parser.parse_string(sample_output)
        
        assert len(result['tallies']) > 0
        tally1 = result['tallies'][0]
        assert tally1.number == 1
        assert tally1.tally_type == 1
        assert len(tally1.bins) >= 3
    
    def test_parse_kcode_results(self):
        """Test parsing KCODE criticality results"""
        sample_output = """
           the final estimated combined collision/absorption/track-length keff = 1.00234 with an estimated standard deviation of 0.00123
           
 the estimated collision/absorption neutron lifetimes, one standard deviations, and 68, 95, and 99 percent confidence intervals are:

           estimation      value        one standard deviation         68% confidence          95% confidence          99% confidence
           ----------      -----        ----------------------        ---------------         ---------------         ---------------
           collision      1.2345E-04            2.3456E-06         1.2322E-04  1.2368E-04  1.2299E-04  1.2391E-04  1.2283E-04  1.2407E-04
        """
        
        parser = MCNPOutputParser()
        result = parser.parse_string(sample_output)
        
        assert 'kcode' in result
        kcode = result['kcode']
        assert abs(kcode.k_effective - 1.00234) < 0.00001
        assert abs(kcode.k_std_dev - 0.00123) < 0.00001
    
    def test_parse_warnings(self):
        """Test parsing warning messages"""
        sample_output = """
warning.  material        1 has been set to a conductor.
 warning.  tally        5 needs more than 1000 histories for valid statistics.
 bad trouble in subroutine sourcc of mcrun
        """
        
        parser = MCNPOutputParser()
        result = parser.parse_string(sample_output)
        
        assert len(result['warnings']) >= 2
        assert len(result['fatal_errors']) >= 1

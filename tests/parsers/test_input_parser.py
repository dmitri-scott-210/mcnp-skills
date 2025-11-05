"""
Test suite for parsers/input_parser.py
"""
import pytest
from parsers.input_parser import MCNPInputParser, CellCard, SurfaceCard, DataCard

class TestMCNPInputParser:
    
    def test_parse_simple_input(self, simple_input):
        """Test parsing simplest MCNP input"""
        parser = MCNPInputParser()
        result = parser.parse_string(simple_input)
        
        assert result['title'] == 'simple - simplest MCNP input'
        assert len(result['cells']) == 2
        assert len(result['surfaces']) == 1
        assert 'sdef' in result['data_cards']
    
    def test_parse_src1(self, src1_input):
        """Test parsing src1 with energy bins"""
        parser = MCNPInputParser()
        result = parser.parse_string(src1_input)
        
        assert 'mode' in result['data_cards']
        assert 'nps' in result['data_cards']
        assert 'sdef' in result['data_cards']
        assert 'f1' in result['data_cards']
        assert 'e1' in result['data_cards']
    
    def test_parse_tal01_materials(self, tal01_input):
        """Test parsing materials"""
        parser = MCNPInputParser()
        result = parser.parse_string(tal01_input)
        
        assert len(result['cells']) >= 3
        assert 'm100' in result['data_cards']
        assert 'm200' in result['data_cards']
    
    def test_get_cells_by_material(self, tal01_input):
        """Test filtering cells by material"""
        parser = MCNPInputParser()
        result = parser.parse_string(tal01_input)
        
        cells_100 = parser.get_cells_by_material(result, 100)
        assert len(cells_100) == 1
        assert cells_100[0].number == 10
    
    def test_roundtrip_conversion(self, src1_input):
        """Test parse then regenerate input"""
        parser = MCNPInputParser()
        result = parser.parse_string(src1_input)
        regenerated = parser.to_string(result)
        
        # Parse again
        result2 = parser.parse_string(regenerated)
        assert len(result2['cells']) == len(result['cells'])
        assert len(result2['surfaces']) == len(result['surfaces'])
    
    def test_parse_all_examples(self, all_example_files):
        """Test parsing all 1,147+ example files"""
        parser = MCNPInputParser()
        success_count = 0
        fail_count = 0
        
        for filepath in all_example_files:
            try:
                result = parser.parse_file(str(filepath))
                if result:
                    success_count += 1
            except Exception as e:
                fail_count += 1
        
        # Should successfully parse majority of files
        assert success_count > 1000
        print(f"Parsed {success_count} files successfully, {fail_count} failed")

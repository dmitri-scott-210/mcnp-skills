"""
Test CSV Data Integration
"""

import os
import sys
import tempfile
import unittest
import pandas as pd
import numpy as np

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestCSVProcessing(unittest.TestCase):
    """Test CSV data loading and processing."""
    
    def setUp(self):
        """Create test CSV file."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create test CSV
        self.csv_path = os.path.join(self.test_dir, 'test_data.csv')
        
        data = pd.DataFrame({
            'Cycle': ['A', 'A', 'B', 'B'],
            'Timestep': [1, 2, 1, 2],
            'Time_Interval_hrs': [24, 20, 22, 25],
            'Power_MW': [23.5, 24.1, 24.3, 24.0]
        })
        
        data.to_csv(self.csv_path, index=False)
    
    def test_csv_loading(self):
        """Test CSV loading."""
        data = pd.read_csv(self.csv_path)
        
        self.assertEqual(len(data), 4)
        self.assertIn('Cycle', data.columns)
        self.assertIn('Power_MW', data.columns)
    
    def test_cycle_grouping(self):
        """Test grouping by cycle."""
        data = pd.read_csv(self.csv_path)
        cycles = data['Cycle'].unique()
        
        self.assertEqual(len(cycles), 2)
        self.assertIn('A', cycles)
        self.assertIn('B', cycles)
    
    def test_cycle_averaging(self):
        """Test averaging by cycle."""
        from time_averaging import cycle_average
        
        data = pd.read_csv(self.csv_path)
        averages = cycle_average(data, 'Cycle', 'Time_Interval_hrs', 'Power_MW')
        
        # Verify we got averages for both cycles
        self.assertIn('A', averages)
        self.assertIn('B', averages)
        
        # Verify reasonable values
        self.assertGreater(averages['A'], 20.0)
        self.assertLess(averages['A'], 30.0)


class TestBatchGeneration(unittest.TestCase):
    """Test batch generation workflow."""
    
    def setUp(self):
        """Create test files."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create template
        self.template_path = os.path.join(self.test_dir, 'test.template')
        with open(self.template_path, 'w') as f:
            f.write("""c Test Input - Cycle {{Cycle}}
c Power: {{Power_MW}} MW
mode n
nps 1000
""")
        
        # Create CSV
        self.csv_path = os.path.join(self.test_dir, 'test_data.csv')
        data = pd.DataFrame({
            'Cycle': ['A', 'B'],
            'Power_MW': [23.5, 24.1]
        })
        data.to_csv(self.csv_path, index=False)
    
    def test_template_file_exists(self):
        """Test template file creation."""
        self.assertTrue(os.path.exists(self.template_path))
    
    def test_csv_file_exists(self):
        """Test CSV file creation."""
        self.assertTrue(os.path.exists(self.csv_path))


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)

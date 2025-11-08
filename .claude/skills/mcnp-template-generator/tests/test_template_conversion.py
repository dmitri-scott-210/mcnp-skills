"""
Test Template Conversion Functionality
"""

import os
import sys
import tempfile
import unittest

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestTemplateConversion(unittest.TestCase):
    """Test template creation and rendering."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def test_jinja2_basic_rendering(self):
        """Test basic Jinja2 template rendering."""
        from jinja2 import Template
        
        # Create simple template
        template_text = "c Control at {{angle}} degrees\n  100  10  -1.0  -100"
        template = Template(template_text)
        
        # Render with data
        output = template.render(angle=85)
        
        # Verify
        self.assertIn("85 degrees", output)
        self.assertNotIn("{{", output)  # No unreplaced variables
    
    def test_multiline_substitution(self):
        """Test multi-line string substitution."""
        from jinja2 import Template
        
        template_text = """c Cell block
{{cells}}
c End"""
        
        cells = """  1  10  -1.0  -100
  2  20  -2.0  -200"""
        
        template = Template(template_text)
        output = template.render(cells=cells)
        
        self.assertIn("1  10  -1.0", output)
        self.assertIn("2  20  -2.0", output)
    
    def test_unreplaced_variable_detection(self):
        """Test detection of unreplaced template variables."""
        from jinja2 import Template
        
        template_text = "{{var1}} and {{var2}}"
        template = Template(template_text)
        
        # Render with only one variable
        output = template.render(var1="VALUE1")
        
        # Should still have unreplaced var2
        self.assertIn("{{var2}}", output)
        self.assertNotIn("{{var1}}", output)


class TestTimeAveraging(unittest.TestCase):
    """Test time-weighted averaging functions."""
    
    def test_basic_time_average(self):
        """Test basic time-weighted average calculation."""
        import numpy as np
        from time_averaging import time_weighted_average
        
        values = np.array([10, 20, 30])
        times = np.array([1, 1, 1])
        
        result = time_weighted_average(values, times)
        self.assertAlmostEqual(result, 20.0)
    
    def test_weighted_time_average(self):
        """Test time-weighted average with different durations."""
        import numpy as np
        from time_averaging import time_weighted_average
        
        values = np.array([10, 30])
        times = np.array([1, 3])  # 30 weighted 3x more
        
        # Expected: (10*1 + 30*3) / (1+3) = 100/4 = 25
        result = time_weighted_average(values, times)
        self.assertAlmostEqual(result, 25.0)
    
    def test_snap_to_discrete(self):
        """Test snapping to discrete values."""
        from time_averaging import snap_to_discrete
        
        options = [0, 25, 50, 75, 100]
        
        # Test various values
        self.assertEqual(snap_to_discrete(23, options), 25)
        self.assertEqual(snap_to_discrete(27, options), 25)
        self.assertEqual(snap_to_discrete(38, options), 50)
        self.assertEqual(snap_to_discrete(62, options), 50)
    
    def test_round_binary(self):
        """Test binary rounding."""
        from time_averaging import round_binary
        
        self.assertEqual(round_binary(0.2), 0)
        self.assertEqual(round_binary(0.4), 0)
        self.assertEqual(round_binary(0.5), 0)  # Round half down
        self.assertEqual(round_binary(0.6), 1)
        self.assertEqual(round_binary(0.8), 1)


class TestDataValidation(unittest.TestCase):
    """Test CSV data validation."""
    
    def test_time_interval_validation(self):
        """Test time interval validation."""
        import numpy as np
        from time_averaging import validate_time_data
        
        # Valid data
        valid_times = np.array([1, 2, 3])
        validate_time_data(valid_times)  # Should not raise
        
        # Invalid: negative
        with self.assertRaises(ValueError):
            validate_time_data(np.array([1, -2, 3]))
        
        # Invalid: zero sum
        with self.assertRaises(ValueError):
            validate_time_data(np.array([0, 0, 0]))


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)

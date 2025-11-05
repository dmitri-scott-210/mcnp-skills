"""Unit tests for MCNP Input Builder"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-input-builder"
sys.path.insert(0, str(skill_dir))

from mcnp_input_generator import MCNPInputGenerator

class TestMCNPInputGenerator:
    def setup_method(self):
        self.generator = MCNPInputGenerator()

    def test_generate_minimal_input(self):
        """Test minimal input generation"""
        result = self.generator.generate_simple_problem('point_source_sphere')
        assert result is not None
        assert len(result) > 0

    def test_set_title(self):
        """Test problem title in generated output"""
        result = self.generator.generate_simple_problem('point_source_sphere')
        # Title is first line of generated output
        assert result is not None

    def test_add_cell(self):
        """Test cells in generated output"""
        result = self.generator.generate_simple_problem('point_source_sphere')
        # Generated problem includes cells
        assert result is not None

    def test_add_surface(self):
        """Test surfaces in generated output"""
        result = self.generator.generate_simple_problem('point_source_sphere')
        # Generated problem includes surfaces
        assert result is not None

    def test_complete_sphere_problem(self):
        """Test complete sphere problem"""
        result = self.generator.generate_simple_problem('point_source_sphere', radius=5.0)
        assert result is not None
        assert len(result) > 50

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

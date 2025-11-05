"""
Unit tests for MCNP Variance Reducer Skill

Tests variance reduction capabilities:
- Cell importance setting
- Weight window addition
- DXTRAN sphere addition
- Energy cutoff setting
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-variance-reducer"
sys.path.insert(0, str(skill_dir))

from mcnp_variance_reducer import MCNPVarianceReducer


class TestMCNPVarianceReducer:
    """Test suite for MCNP Variance Reducer"""

    def setup_method(self):
        """Setup test fixture"""
        self.reducer = MCNPVarianceReducer()

    # ===== Basic API Tests =====

    def test_reducer_initialization(self):
        """Test reducer initializes correctly"""
        assert self.reducer is not None
        assert self.reducer.parser is not None
        assert self.reducer.parsed is None

    def test_set_cell_importances_interface(self):
        """Test set_cell_importances method exists"""
        assert hasattr(self.reducer, 'set_cell_importances')
        assert callable(self.reducer.set_cell_importances)

    def test_add_weight_windows_interface(self):
        """Test add_weight_windows method exists"""
        assert hasattr(self.reducer, 'add_weight_windows')
        assert callable(self.reducer.add_weight_windows)

    def test_add_dxtran_sphere_interface(self):
        """Test add_dxtran_sphere method exists"""
        assert hasattr(self.reducer, 'add_dxtran_sphere')
        assert callable(self.reducer.add_dxtran_sphere)

    def test_add_energy_cutoffs_interface(self):
        """Test add_energy_cutoffs method exists"""
        assert hasattr(self.reducer, 'add_energy_cutoffs')
        assert callable(self.reducer.add_energy_cutoffs)

    # ===== Cell Importance Tests =====

    def test_set_importances_single_cell(self):
        """Test setting importance for single cell"""
        self.reducer.set_cell_importances('n', {1: 1})
        assert self.reducer.parsed is not None
        assert 'imp:n' in self.reducer.parsed['data_cards']

    def test_set_importances_multiple_cells(self):
        """Test setting importances for multiple cells"""
        importances = {1: 1, 2: 0.5, 3: 0.1, 4: 0}
        self.reducer.set_cell_importances('n', importances)
        assert 'imp:n' in self.reducer.parsed['data_cards']

    def test_set_importances_photon(self):
        """Test setting photon importances"""
        self.reducer.set_cell_importances('p', {1: 1, 2: 0})
        assert 'imp:p' in self.reducer.parsed['data_cards']

    def test_set_importances_geometric_progression(self):
        """Test setting geometric progression importances"""
        importances = {1: 1, 2: 0.5, 3: 0.25, 4: 0.125, 5: 0.0625}
        self.reducer.set_cell_importances('n', importances)
        card = self.reducer.parsed['data_cards']['imp:n']
        assert card is not None

    def test_set_importances_zero_importance(self):
        """Test setting zero importance (void region)"""
        importances = {1: 1, 2: 1, 3: 0}  # Cell 3 is void
        self.reducer.set_cell_importances('n', importances)
        assert self.reducer.parsed is not None

    # ===== Weight Window Tests =====

    def test_add_weight_windows_basic(self):
        """Test adding basic weight windows"""
        self.reducer.add_weight_windows(
            particle='n',
            cells=[1, 2, 3],
            energies=[0.01, 1.0, 10.0],
            bounds=[0.5, 0.3, 0.1]
        )
        assert 'wwn:n' in self.reducer.parsed['data_cards']
        assert 'wwe:n' in self.reducer.parsed['data_cards']

    def test_add_weight_windows_no_energy(self):
        """Test adding weight windows without energy bins"""
        self.reducer.add_weight_windows(
            particle='n',
            cells=[1, 2],
            energies=[],
            bounds=[1.0, 0.5]
        )
        assert 'wwn:n' in self.reducer.parsed['data_cards']
        # WWE should not be added if energies empty
        assert 'wwe:n' not in self.reducer.parsed['data_cards']

    def test_add_weight_windows_photon(self):
        """Test adding photon weight windows"""
        self.reducer.add_weight_windows(
            particle='p',
            cells=[1],
            energies=[0.1, 1.0],
            bounds=[0.5]
        )
        assert 'wwn:p' in self.reducer.parsed['data_cards']

    # ===== DXTRAN Tests =====

    def test_add_dxtran_basic(self):
        """Test adding basic DXTRAN sphere"""
        self.reducer.add_dxtran_sphere(
            position=(100, 0, 0),
            radius=5.0
        )
        assert self.reducer.parsed is not None
        assert 'dxt:n' in self.reducer.parsed['data_cards']

    def test_add_dxtran_custom_contribution(self):
        """Test adding DXTRAN with custom contribution"""
        self.reducer.add_dxtran_sphere(
            position=(50, 50, 0),
            radius=10.0,
            contribution=0.95
        )
        card = self.reducer.parsed['data_cards']['dxt:n']
        assert '0.95' in card.entries

    def test_add_dxtran_negative_coordinates(self):
        """Test DXTRAN with negative coordinates"""
        self.reducer.add_dxtran_sphere(
            position=(-100, -50, -25),
            radius=5.0
        )
        assert 'dxt:n' in self.reducer.parsed['data_cards']

    # ===== Energy Cutoff Tests =====

    def test_add_energy_cutoff_neutron(self):
        """Test adding neutron energy cutoff"""
        self.reducer.add_energy_cutoffs('n', 0.001)
        assert 'cut:n' in self.reducer.parsed['data_cards']

    def test_add_energy_cutoff_photon(self):
        """Test adding photon energy cutoff"""
        self.reducer.add_energy_cutoffs('p', 0.01)
        assert 'cut:p' in self.reducer.parsed['data_cards']

    def test_add_energy_cutoff_electron(self):
        """Test adding electron energy cutoff"""
        self.reducer.add_energy_cutoffs('e', 0.001)
        assert 'cut:e' in self.reducer.parsed['data_cards']

    # ===== File Operations Tests =====

    def test_save_file_with_data(self, tmp_path):
        """Test saving file with variance reduction"""
        self.reducer.set_cell_importances('n', {1: 1, 2: 0.5})
        self.reducer.parser.to_string = Mock(return_value="Test content")

        output_file = tmp_path / "test_vr.inp"
        self.reducer.save_file(str(output_file))
        assert output_file.exists()

    # ===== Integration Tests =====

    def test_complete_variance_reduction_setup(self):
        """Test complete variance reduction setup"""
        # Set importances
        importances = {1: 1, 2: 0.5, 3: 0.25, 4: 0.125, 5: 0}
        self.reducer.set_cell_importances('n', importances)

        # Add weight windows
        self.reducer.add_weight_windows(
            particle='n',
            cells=[1, 2, 3, 4],
            energies=[0.01, 1.0, 10.0],
            bounds=[1.0, 0.5, 0.25, 0.125]
        )

        # Add energy cutoff
        self.reducer.add_energy_cutoffs('n', 0.001)

        assert 'imp:n' in self.reducer.parsed['data_cards']
        assert 'wwn:n' in self.reducer.parsed['data_cards']
        assert 'wwe:n' in self.reducer.parsed['data_cards']
        assert 'cut:n' in self.reducer.parsed['data_cards']

    def test_deep_penetration_shielding_vr(self):
        """Test variance reduction for deep penetration shielding"""
        # Aggressive importance reduction through shield
        importances = {
            1: 1,      # Source region
            2: 0.5,    # First shield layer
            3: 0.1,    # Second shield layer
            4: 0.01,   # Third shield layer
            5: 0.001,  # Detector region
            6: 0       # Outside
        }
        self.reducer.set_cell_importances('n', importances)

        # Add DXTRAN to detector
        self.reducer.add_dxtran_sphere(
            position=(100, 0, 0),
            radius=5.0,
            contribution=0.9
        )

        assert len(self.reducer.parsed['data_cards']) >= 2

    def test_reactor_core_vr(self):
        """Test variance reduction for reactor core"""
        # All core cells have importance 1, outside has 0
        core_cells = list(range(1, 101))  # 100 core cells
        importances = {cell: 1 for cell in core_cells}
        importances[200] = 0  # Outside world

        self.reducer.set_cell_importances('n', importances)
        assert 'imp:n' in self.reducer.parsed['data_cards']

    def test_coupled_particle_vr(self):
        """Test variance reduction for coupled n-p problem"""
        # Set neutron importances
        self.reducer.set_cell_importances('n', {1: 1, 2: 0.5, 3: 0})

        # Set photon importances
        self.reducer.set_cell_importances('p', {1: 1, 2: 0.8, 3: 0})

        assert 'imp:n' in self.reducer.parsed['data_cards']
        assert 'imp:p' in self.reducer.parsed['data_cards']

    def test_api_consistency(self):
        """Test all methods create parsed structure if needed"""
        # All these should create parsed structure if None
        self.reducer.set_cell_importances('n', {1: 1})
        assert self.reducer.parsed is not None

        reducer2 = MCNPVarianceReducer()
        reducer2.add_weight_windows('n', [1], [], [0.5])
        assert reducer2.parsed is not None

        reducer3 = MCNPVarianceReducer()
        reducer3.add_dxtran_sphere((0, 0, 0), 5.0)
        assert reducer3.parsed is not None

        reducer4 = MCNPVarianceReducer()
        reducer4.add_energy_cutoffs('n', 0.001)
        assert reducer4.parsed is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

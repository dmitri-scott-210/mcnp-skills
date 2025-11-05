"""
Unit tests for MCNP Weight Window Optimizer Skill

Tests weight window variance reduction:
- WWG card generation
- WWN bounds specification
- WWE energy bins
- WWP parameters
- Mesh-based weight windows
- Quality assessment
- Optimization workflow
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-ww-optimizer"
sys.path.insert(0, str(skill_dir))

from mcnp_ww_optimizer import MCNPWeightWindowOptimizer


class TestMCNPWeightWindowOptimizer:
    """Test suite for MCNP Weight Window Optimizer"""

    def setup_method(self):
        """Setup test fixture"""
        self.optimizer = MCNPWeightWindowOptimizer()

    # ===== WWG Setup Tests =====

    def test_setup_wwg_basic(self):
        """Test basic WWG setup"""
        result = self.optimizer.setup_wwg(tally_num=4, particle='n')
        assert result is not None
        assert 'wwg:n' in result
        assert '4' in result

    def test_setup_wwg_photon(self):
        """Test WWG for photons"""
        result = self.optimizer.setup_wwg(tally_num=14, particle='p')
        assert 'wwg:p' in result

    def test_setup_wwg_custom_update_factor(self):
        """Test WWG with custom update factor"""
        result = self.optimizer.setup_wwg(
            tally_num=4,
            particle='n',
            update_factor=0.7
        )
        assert '0.7' in result

    def test_setup_wwg_custom_softening(self):
        """Test WWG with custom softening"""
        result = self.optimizer.setup_wwg(
            tally_num=4,
            particle='n',
            softening=0.3
        )
        assert '0.3' in result

    def test_setup_wwg_with_ratios(self):
        """Test WWG with min/max ratios"""
        result = self.optimizer.setup_wwg(
            tally_num=4,
            particle='n',
            min_ratio=0.1,
            max_ratio=10.0
        )
        assert result is not None
        assert '0.1' in result
        assert '10.0' in result

    # ===== WWN Bounds Tests =====

    def test_add_wwn_bounds_single(self):
        """Test WWN with single cell"""
        result = self.optimizer.add_wwn_bounds(
            particle='n',
            lower_bounds=[0.5]
        )
        assert result is not None
        assert 'wwn:n' in result
        assert '0.5' in result

    def test_add_wwn_bounds_multiple(self):
        """Test WWN with multiple cells"""
        result = self.optimizer.add_wwn_bounds(
            particle='n',
            lower_bounds=[0.5, 0.3, 0.1, 0.01]
        )
        assert 'wwn:n' in result
        assert '0.5' in result
        assert '0.01' in result

    def test_add_wwn_bounds_photon(self):
        """Test WWN for photons"""
        result = self.optimizer.add_wwn_bounds(
            particle='p',
            lower_bounds=[1.0, 0.5, 0.1]
        )
        assert 'wwn:p' in result

    # ===== WWE Energy Bins Tests =====

    def test_add_wwe_energy_bins_basic(self):
        """Test WWE with basic energy bins"""
        result = self.optimizer.add_wwe_energy_bins(
            particle='n',
            energy_bins=[0.01, 1.0, 10.0]
        )
        assert result is not None
        assert 'wwe:n' in result
        assert '0.01' in result

    def test_add_wwe_energy_bins_fine(self):
        """Test WWE with fine energy binning"""
        energy_bins = [1e-8, 1e-6, 1e-4, 0.01, 1.0, 10.0, 100.0]
        result = self.optimizer.add_wwe_energy_bins(
            particle='n',
            energy_bins=energy_bins
        )
        assert 'wwe:n' in result
        assert len(result.split()) >= len(energy_bins)

    # ===== WWP Parameters Tests =====

    def test_add_wwp_default(self):
        """Test WWP with default parameters"""
        result = self.optimizer.add_wwp_parameters(particle='n')
        assert result is not None
        assert 'wwp:n' in result
        assert '0.25' in result  # Default cutoff
        assert '0.5' in result   # Default survival

    def test_add_wwp_custom_cutoff(self):
        """Test WWP with custom weight cutoff"""
        result = self.optimizer.add_wwp_parameters(
            particle='n',
            weight_cutoff=0.1
        )
        assert '0.1' in result

    def test_add_wwp_custom_survival(self):
        """Test WWP with custom survival weight"""
        result = self.optimizer.add_wwp_parameters(
            particle='n',
            weight_survival=0.75
        )
        assert '0.75' in result

    def test_add_wwp_custom_max_split(self):
        """Test WWP with custom max split"""
        result = self.optimizer.add_wwp_parameters(
            particle='n',
            max_split=10
        )
        assert '10' in result

    def test_add_wwp_stores_params(self):
        """Test WWP parameters are stored"""
        self.optimizer.add_wwp_parameters(
            particle='n',
            weight_cutoff=0.2,
            weight_survival=0.6
        )
        assert 'n' in self.optimizer.wwp_params
        assert self.optimizer.wwp_params['n']['cutoff'] == 0.2
        assert self.optimizer.wwp_params['n']['survival'] == 0.6

    # ===== Mesh for WW Tests =====

    def test_add_mesh_rectangular(self):
        """Test rectangular mesh for WW"""
        result = self.optimizer.add_mesh_for_ww(
            particle='n',
            mesh_type='xyz',
            origin=(0, 0, 0),
            imesh=[10, 20], jmesh=[10], kmesh=[10],
            iints=[5, 5], jints=[5], kints=[5]
        )
        assert result is not None
        assert 'mesh' in result
        assert 'geom=xyz' in result

    def test_add_mesh_cylindrical(self):
        """Test cylindrical mesh for WW"""
        result = self.optimizer.add_mesh_for_ww(
            particle='n',
            mesh_type='cyl',
            origin=(0, 0, 0),
            imesh=[5, 10], jmesh=[180, 360], kmesh=[0, 100],
            iints=[5, 5], jints=[6, 6], kints=[10]
        )
        assert 'geom=cyl' in result

    def test_add_mesh_sets_flag(self):
        """Test mesh addition sets mesh_defined flag"""
        assert self.optimizer.mesh_defined == False
        self.optimizer.add_mesh_for_ww(
            particle='n',
            mesh_type='xyz',
            origin=(0, 0, 0),
            imesh=[10], jmesh=[10], kmesh=[10],
            iints=[5], jints=[5], kints=[5]
        )
        assert self.optimizer.mesh_defined == True

    # ===== Optimization Workflow Tests =====

    def test_generate_optimization_workflow_default(self):
        """Test optimization workflow with default parameters"""
        result = self.optimizer.generate_optimization_workflow()
        assert result is not None
        assert 'Iteration' in result
        assert 'WWINP' in result

    def test_generate_optimization_workflow_custom_iterations(self):
        """Test optimization workflow with custom iterations"""
        result = self.optimizer.generate_optimization_workflow(
            n_iterations=5,
            particles_per_iteration=5000000
        )
        assert '5' in result or 'Iterations 2-5' in result
        assert '5000000' in result or '5,000,000' in result

    def test_optimization_workflow_has_convergence(self):
        """Test workflow includes convergence criteria"""
        result = self.optimizer.generate_optimization_workflow()
        assert 'Convergence' in result or 'FOM' in result

    def test_optimization_workflow_has_steps(self):
        """Test workflow includes step-by-step instructions"""
        result = self.optimizer.generate_optimization_workflow()
        assert 'WWG' in result
        assert 'Generate' in result or 'Refine' in result

    # ===== WW Quality Check Tests =====

    def test_check_ww_quality_good(self):
        """Test WW quality check with good ratios"""
        result = self.optimizer.check_ww_quality([2.0, 3.0, 5.0, 8.0])
        assert result is not None
        assert result['status'] == 'good'
        assert result['max_ratio'] == 8.0

    def test_check_ww_quality_acceptable(self):
        """Test WW quality check with acceptable ratios"""
        result = self.optimizer.check_ww_quality([10.0, 20.0, 50.0, 80.0])
        assert result['status'] == 'acceptable'

    def test_check_ww_quality_poor(self):
        """Test WW quality check with poor ratios"""
        result = self.optimizer.check_ww_quality([50.0, 100.0, 200.0])
        assert result['status'] == 'poor'

    def test_check_ww_quality_average(self):
        """Test WW quality calculates average ratio"""
        result = self.optimizer.check_ww_quality([2.0, 4.0, 6.0, 8.0])
        assert result['avg_ratio'] == 5.0

    def test_check_ww_quality_has_recommendation(self):
        """Test WW quality provides recommendation"""
        result = self.optimizer.check_ww_quality([5.0, 10.0, 15.0])
        assert 'recommendation' in result
        assert len(result['recommendation']) > 0

    # ===== Card Tracking Tests =====

    def test_ww_cards_empty_initially(self):
        """Test WW cards list is empty initially"""
        assert len(self.optimizer.ww_cards) == 0

    def test_ww_cards_tracks_additions(self):
        """Test WW cards are tracked"""
        self.optimizer.setup_wwg(tally_num=4, particle='n')
        self.optimizer.add_wwn_bounds(particle='n', lower_bounds=[0.5])
        self.optimizer.add_wwe_energy_bins(particle='n', energy_bins=[0.01, 1.0])
        assert len(self.optimizer.ww_cards) == 3

    # ===== Integration Tests =====

    def test_complete_ww_setup(self):
        """Test complete weight window setup"""
        # Setup WWG from tally
        wwg = self.optimizer.setup_wwg(tally_num=4, particle='n')
        # Add WWP parameters
        wwp = self.optimizer.add_wwp_parameters(
            particle='n',
            weight_cutoff=0.25,
            weight_survival=0.5,
            max_split=5
        )
        # Add energy bins
        wwe = self.optimizer.add_wwe_energy_bins(
            particle='n',
            energy_bins=[1e-8, 1e-6, 1e-4, 0.01, 1.0, 10.0]
        )
        assert wwg is not None
        assert wwp is not None
        assert wwe is not None
        assert len(self.optimizer.ww_cards) == 3

    def test_mesh_based_ww_setup(self):
        """Test mesh-based weight window setup"""
        # Add mesh for WW
        mesh = self.optimizer.add_mesh_for_ww(
            particle='n',
            mesh_type='xyz',
            origin=(0, 0, 0),
            imesh=[10, 20, 30],
            jmesh=[10, 20, 30],
            kmesh=[10, 20, 30],
            iints=[5, 5, 5],
            jints=[5, 5, 5],
            kints=[5, 5, 5]
        )
        # Setup WWG
        wwg = self.optimizer.setup_wwg(tally_num=4, particle='n')
        assert mesh is not None
        assert wwg is not None
        assert self.optimizer.mesh_defined

    def test_deep_penetration_shielding_ww(self):
        """Test WW setup for deep penetration shielding"""
        # This is challenging - need aggressive variance reduction
        wwg = self.optimizer.setup_wwg(
            tally_num=4,
            particle='n',
            update_factor=0.5,
            softening=0.5
        )
        wwp = self.optimizer.add_wwp_parameters(
            particle='n',
            weight_cutoff=0.1,
            weight_survival=0.3,
            max_split=10
        )
        workflow = self.optimizer.generate_optimization_workflow(
            n_iterations=5,
            particles_per_iteration=10000000
        )
        assert wwg is not None
        assert wwp is not None
        assert workflow is not None

    def test_complete_optimization_cycle(self):
        """Test complete WW optimization cycle"""
        # Setup
        self.optimizer.setup_wwg(tally_num=4, particle='n')
        self.optimizer.add_wwp_parameters(particle='n')
        # Generate workflow
        workflow = self.optimizer.generate_optimization_workflow(n_iterations=3)
        # Check quality (simulate)
        quality = self.optimizer.check_ww_quality([2.0, 5.0, 10.0, 15.0])

        assert workflow is not None
        assert quality['status'] in ['good', 'acceptable']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

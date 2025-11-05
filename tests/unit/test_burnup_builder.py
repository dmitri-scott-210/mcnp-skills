"""
Unit tests for MCNP Burnup Builder Skill

Tests burnup/depletion construction capabilities:
- BURN card specification
- Power level setting
- Burnup step configuration
- Burnup calculations
- Runtime estimation
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-burnup-builder"
sys.path.insert(0, str(skill_dir))

from mcnp_burnup_builder import MCNPBurnupBuilder


class TestMCNPBurnupBuilder:
    """Test suite for MCNP Burnup Builder"""

    def setup_method(self):
        """Setup test fixture"""
        self.builder = MCNPBurnupBuilder()

    # ===== BURN Specification Tests =====

    def test_add_burn_basic(self):
        """Test basic BURN specification"""
        result = self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 100, 200, 300]
        )
        assert result is not None
        assert 'burn' in result.lower()
        assert 'mat=1' in result

    def test_add_burn_custom_power(self):
        """Test BURN with custom power level"""
        result = self.builder.add_burn_specification(
            material=1,
            power_mw=3000,  # 3 GW reactor
            burnup_steps=[0, 365, 730]
        )
        assert 'power=3000' in result

    def test_add_burn_days_units(self):
        """Test BURN with days time units"""
        result = self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 30, 60, 90],
            units='days'
        )
        assert 'days' in result

    def test_add_burn_years_units(self):
        """Test BURN with years time units"""
        result = self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 1, 2, 3],
            units='years'
        )
        assert 'years' in result

    def test_add_burn_seconds_units(self):
        """Test BURN with seconds time units"""
        result = self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 86400, 172800],
            units='seconds'
        )
        assert 'seconds' in result

    def test_add_burn_multiple_materials(self):
        """Test BURN for multiple materials"""
        result1 = self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 100, 200]
        )
        result2 = self.builder.add_burn_specification(
            material=2,
            power_mw=50,
            burnup_steps=[0, 100, 200]
        )
        assert result1 is not None
        assert result2 is not None
        assert len(self.builder.burn_cards) == 2

    # ===== Depletion Cell Tests =====

    def test_set_depletion_cells_single(self):
        """Test setting single depletion cell"""
        self.builder.set_depletion_cells([10])
        assert self.builder.depletion_cells == [10]

    def test_set_depletion_cells_multiple(self):
        """Test setting multiple depletion cells"""
        self.builder.set_depletion_cells([10, 20, 30, 40])
        assert len(self.builder.depletion_cells) == 4

    # ===== Burnup Calculation Tests =====

    def test_calculate_burnup_simple(self):
        """Test burnup calculation"""
        burnup = self.builder.calculate_burnup_mwd_kghm(
            power_mw=100,
            mass_kghm=1000,
            time_days=100
        )
        assert burnup == 10.0  # 100*100/1000

    def test_calculate_burnup_pwr_typical(self):
        """Test burnup for typical PWR fuel"""
        # 100 tons fuel, 3000 MW, 500 days
        burnup = self.builder.calculate_burnup_mwd_kghm(
            power_mw=3000,
            mass_kghm=100000,
            time_days=500
        )
        assert 10 < burnup < 20  # Typical PWR discharge ~15 MWd/kgHM

    def test_calculate_burnup_zero_mass_error(self):
        """Test burnup calculation with zero mass"""
        with pytest.raises(ZeroDivisionError):
            self.builder.calculate_burnup_mwd_kghm(
                power_mw=100,
                mass_kghm=0,
                time_days=100
            )

    def test_calculate_burnup_high_burnup(self):
        """Test high burnup calculation"""
        burnup = self.builder.calculate_burnup_mwd_kghm(
            power_mw=100,
            mass_kghm=100,
            time_days=6000
        )
        assert burnup == 6000  # High burnup fuel

    # ===== Runtime Estimation Tests =====

    def test_estimate_runtime_simple(self):
        """Test runtime estimation for simple case"""
        result = self.builder.estimate_depletion_runtime(
            n_steps=10,
            particles_per_step=10000,
            step_time_sec=60
        )
        assert result is not None
        assert 'total_steps' in result
        assert result['total_steps'] == 10

    def test_estimate_runtime_particles(self):
        """Test runtime estimation particle count"""
        result = self.builder.estimate_depletion_runtime(
            n_steps=20,
            particles_per_step=100000,
            step_time_sec=60
        )
        assert result['total_particles'] == 2000000

    def test_estimate_runtime_hours(self):
        """Test runtime estimation in hours"""
        result = self.builder.estimate_depletion_runtime(
            n_steps=100,
            particles_per_step=10000,
            step_time_sec=36  # 36 sec/step = 1 hour total
        )
        assert result['estimated_hours'] == 1.0

    def test_estimate_runtime_long_calculation(self):
        """Test runtime estimation for long calculation"""
        result = self.builder.estimate_depletion_runtime(
            n_steps=1000,
            particles_per_step=1000000,
            step_time_sec=120
        )
        assert result['estimated_hours'] > 30  # Should be significant

    def test_estimate_runtime_has_recommendation(self):
        """Test runtime estimation provides recommendation"""
        result = self.builder.estimate_depletion_runtime(
            n_steps=50,
            particles_per_step=50000
        )
        assert 'recommendation' in result
        assert 'Burnup' in result['recommendation']

    # ===== Depletion Info Tests =====

    def test_generate_depletion_info_empty(self):
        """Test depletion info with no materials"""
        result = self.builder.generate_depletion_info()
        assert result is not None
        assert 'Configuration' in result

    def test_generate_depletion_info_single_material(self):
        """Test depletion info with single material"""
        self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 100, 200]
        )
        result = self.builder.generate_depletion_info()
        assert 'Material 1' in result
        assert '100 MW' in result

    def test_generate_depletion_info_multiple_materials(self):
        """Test depletion info with multiple materials"""
        self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 100, 200]
        )
        self.builder.add_burn_specification(
            material=2,
            power_mw=50,
            burnup_steps=[0, 100, 200]
        )
        result = self.builder.generate_depletion_info()
        assert 'Material 1' in result
        assert 'Material 2' in result

    def test_generate_depletion_info_with_cells(self):
        """Test depletion info includes cell information"""
        self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 100, 200]
        )
        self.builder.set_depletion_cells([10, 20, 30])
        result = self.builder.generate_depletion_info()
        assert 'Depletion cells' in result

    def test_generate_depletion_info_has_warning(self):
        """Test depletion info includes format warning"""
        result = self.builder.generate_depletion_info()
        assert 'NOTE' in result or 'Verify' in result

    # ===== Card Generation Tests =====

    def test_generate_cards_empty(self):
        """Test generate_cards with no BURN cards"""
        result = self.builder.generate_cards()
        assert result is not None
        assert 'No burnup' in result

    def test_generate_cards_single_burn(self):
        """Test generate_cards with one BURN card"""
        self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 100, 200]
        )
        result = self.builder.generate_cards()
        assert 'burn' in result.lower()
        assert 'mat=1' in result

    def test_generate_cards_multiple_burns(self):
        """Test generate_cards with multiple BURN cards"""
        self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 100, 200]
        )
        self.builder.add_burn_specification(
            material=2,
            power_mw=50,
            burnup_steps=[0, 100, 200]
        )
        result = self.builder.generate_cards()
        assert result.lower().count('burn') >= 2

    def test_generate_cards_has_warning(self):
        """Test generate_cards includes format warning"""
        self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 100, 200]
        )
        result = self.builder.generate_cards()
        assert 'NOTE' in result or 'Verify' in result

    # ===== Integration Tests =====

    def test_pwr_fuel_depletion(self):
        """Test realistic PWR fuel depletion"""
        # 100 tons fuel, 3000 MW, 18-month cycle
        self.builder.add_burn_specification(
            material=1,
            power_mw=3000,
            burnup_steps=[0, 180, 365, 545],  # 18-month cycle
            units='days'
        )
        burnup = self.builder.calculate_burnup_mwd_kghm(
            power_mw=3000,
            mass_kghm=100000,
            time_days=545
        )
        assert 15 < burnup < 20  # Typical discharge burnup

    def test_complete_burnup_workflow(self):
        """Test complete burnup specification workflow"""
        # Add BURN specification
        self.builder.add_burn_specification(
            material=1,
            power_mw=100,
            burnup_steps=[0, 100, 200, 300]
        )
        # Set depletion cells
        self.builder.set_depletion_cells([10, 20, 30])
        # Calculate burnup
        burnup = self.builder.calculate_burnup_mwd_kghm(100, 1000, 300)
        # Estimate runtime
        runtime = self.builder.estimate_depletion_runtime(3, 10000)
        # Generate info
        info = self.builder.generate_depletion_info()
        # Generate cards
        cards = self.builder.generate_cards()

        assert burnup == 30.0
        assert runtime is not None
        assert info is not None
        assert cards is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

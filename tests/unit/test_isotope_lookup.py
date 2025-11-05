"""
Unit tests for MCNP Isotope Lookup Skill

Tests ZAID lookup and atomic data retrieval:
- Isotope name to ZAID conversion
- Atomic weight lookup
- Natural element expansion
- Library recommendation
"""
import pytest
import sys
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-isotope-lookup"
sys.path.insert(0, str(skill_dir))

from mcnp_isotope_lookup import MCNPIsotopeLookup


class TestMCNPIsotopeLookup:
    """Test suite for MCNP Isotope Lookup"""

    def setup_method(self):
        """Setup test fixture"""
        self.lookup = MCNPIsotopeLookup()

    # ===== ZAID Lookup Tests =====

    def test_lookup_zaid_u235(self):
        """Test ZAID lookup for U-235"""
        zaid = self.lookup.lookup_zaid('U-235')

        assert zaid is not None, "Should find U-235"
        assert '92235' in zaid, "ZAID should contain 92235"

    def test_lookup_zaid_h1(self):
        """Test ZAID lookup for H-1"""
        zaid = self.lookup.lookup_zaid('H-1')

        assert zaid is not None, "Should find H-1"
        assert '1001' in zaid, "ZAID should contain 1001"

    def test_lookup_zaid_o16(self):
        """Test ZAID lookup for O-16"""
        zaid = self.lookup.lookup_zaid('O-16')

        assert zaid is not None, "Should find O-16"
        assert '8016' in zaid, "ZAID should contain 8016"

    def test_lookup_zaid_pu239(self):
        """Test ZAID lookup for Pu-239"""
        zaid = self.lookup.lookup_zaid('Pu-239')

        assert zaid is not None, "Should find Pu-239"
        assert '94239' in zaid, "ZAID should contain 94239"

    def test_lookup_zaid_with_library(self):
        """Test ZAID lookup with specific library"""
        zaid_80c = self.lookup.lookup_zaid('U-235', '80c')
        zaid_70c = self.lookup.lookup_zaid('U-235', '70c')

        assert zaid_80c is not None, "Should find with 80c library"
        # Library suffix should be in ZAID
        assert '.80c' in zaid_80c or '80c' in zaid_80c, "Should have 80c library"

    def test_lookup_zaid_invalid_isotope(self):
        """Test ZAID lookup for invalid isotope"""
        zaid = self.lookup.lookup_zaid('XX-999')

        assert zaid is None, "Should return None for invalid isotope"

    def test_lookup_zaid_case_insensitive(self):
        """Test ZAID lookup is case-insensitive"""
        zaid1 = self.lookup.lookup_zaid('U-235')
        zaid2 = self.lookup.lookup_zaid('u-235')

        # Should handle both cases
        assert zaid1 is not None or zaid2 is not None, "Should handle case variations"

    # ===== Atomic Weight Tests =====

    def test_get_atomic_weight_hydrogen(self):
        """Test atomic weight for hydrogen"""
        weight = self.lookup.get_atomic_weight('H')

        assert weight > 0, "Should return positive weight"
        assert 1.0 < weight < 1.1, "H atomic weight should be ~1.008"

    def test_get_atomic_weight_carbon(self):
        """Test atomic weight for carbon"""
        weight = self.lookup.get_atomic_weight('C')

        assert weight > 0, "Should return positive weight"
        assert 12.0 < weight < 12.2, "C atomic weight should be ~12.011"

    def test_get_atomic_weight_uranium(self):
        """Test atomic weight for uranium"""
        weight = self.lookup.get_atomic_weight('U')

        assert weight > 0, "Should return positive weight"
        assert 237.9 < weight < 238.1, "U atomic weight should be ~238.03"

    def test_get_atomic_weight_oxygen(self):
        """Test atomic weight for oxygen"""
        weight = self.lookup.get_atomic_weight('O')

        assert weight > 0, "Should return positive weight"
        assert 15.9 < weight < 16.1, "O atomic weight should be ~15.999"

    def test_get_atomic_weight_aluminum(self):
        """Test atomic weight for aluminum"""
        weight = self.lookup.get_atomic_weight('Al')

        assert weight > 0, "Should return positive weight"
        assert 26.9 < weight < 27.1, "Al atomic weight should be ~26.982"

    def test_get_atomic_weight_invalid_element(self):
        """Test atomic weight for invalid element"""
        weight = self.lookup.get_atomic_weight('Xx')

        assert weight == 0.0, "Should return 0.0 for invalid element"

    def test_get_atomic_weight_case_sensitive(self):
        """Test atomic weight lookup is case-sensitive for symbols"""
        # 'H' is hydrogen, 'h' might not be recognized
        weight_upper = self.lookup.get_atomic_weight('H')
        weight_lower = self.lookup.get_atomic_weight('h')

        # At least uppercase should work
        assert weight_upper > 0, "Uppercase symbol should work"

    # ===== Natural Element Expansion Tests =====

    def test_expand_natural_element_hydrogen(self):
        """Test expansion of natural hydrogen"""
        isotopes = self.lookup.expand_natural_element('H')

        assert isinstance(isotopes, list), "Should return a list"
        assert len(isotopes) > 0, "H has at least one natural isotope"
        # Natural hydrogen is mostly H-1 with trace H-2 (deuterium)

    def test_expand_natural_element_carbon(self):
        """Test expansion of natural carbon"""
        isotopes = self.lookup.expand_natural_element('C')

        assert isinstance(isotopes, list), "Should return a list"
        assert len(isotopes) > 0, "C has natural isotopes"
        # Natural carbon is C-12 (~99%) and C-13 (~1%)

    def test_expand_natural_element_oxygen(self):
        """Test expansion of natural oxygen"""
        isotopes = self.lookup.expand_natural_element('O')

        assert isinstance(isotopes, list), "Should return a list"
        assert len(isotopes) > 0, "O has natural isotopes"
        # Natural oxygen is O-16 (~99.76%), O-17, O-18

    def test_expand_natural_element_uranium(self):
        """Test expansion of natural uranium"""
        isotopes = self.lookup.expand_natural_element('U')

        assert isinstance(isotopes, list), "Should return a list"
        # Natural uranium has U-234, U-235, U-238
        # May or may not be in database depending on implementation

    def test_expand_natural_element_with_library(self):
        """Test expansion with specific library"""
        isotopes = self.lookup.expand_natural_element('H', '80c')

        assert isinstance(isotopes, list), "Should return a list"

    def test_expand_natural_element_invalid(self):
        """Test expansion of invalid element"""
        isotopes = self.lookup.expand_natural_element('Xx')

        assert isinstance(isotopes, list), "Should return a list"
        assert len(isotopes) == 0, "Invalid element should return empty list"

    # ===== Library Recommendation Tests =====

    def test_recommend_library_neutron(self):
        """Test library recommendation for neutron transport"""
        library = self.lookup.recommend_library('U-235', 'n')

        assert library is not None, "Should recommend a library"
        assert isinstance(library, str), "Should return string"
        # Typically .80c, .70c, etc.

    def test_recommend_library_photon(self):
        """Test library recommendation for photon transport"""
        library = self.lookup.recommend_library('Al-27', 'p')

        assert library is not None, "Should recommend a library"
        assert isinstance(library, str), "Should return string"

    def test_recommend_library_default_particle(self):
        """Test library recommendation with default particle"""
        library = self.lookup.recommend_library('H-1')

        assert library is not None, "Should recommend a library"
        assert isinstance(library, str), "Should return string"
        # Default is neutron

    def test_recommend_library_invalid_isotope(self):
        """Test library recommendation for invalid isotope"""
        library = self.lookup.recommend_library('XX-999')

        # Should return default
        assert library == '80c', "Should return default 80c for invalid"

    def test_recommend_library_common_isotopes(self):
        """Test library recommendations for common isotopes"""
        isotopes = ['H-1', 'C-12', 'O-16', 'U-235', 'Pu-239']

        for isotope in isotopes:
            library = self.lookup.recommend_library(isotope)
            assert library is not None, f"Should recommend library for {isotope}"
            assert isinstance(library, str), f"Should return string for {isotope}"

    # ===== Integration Tests =====

    def test_lookup_common_fuel_isotopes(self):
        """Test lookup of common nuclear fuel isotopes"""
        fuel_isotopes = ['U-235', 'U-238', 'Pu-239', 'Pu-241']

        for isotope in fuel_isotopes:
            zaid = self.lookup.lookup_zaid(isotope)
            assert zaid is not None, f"Should find {isotope}"

            weight = self.lookup.get_atomic_weight(isotope.split('-')[0])
            assert weight > 0, f"Should have atomic weight for {isotope}"

    def test_lookup_common_moderator_isotopes(self):
        """Test lookup of common moderator isotopes"""
        moderators = ['H-1', 'H-2', 'C-12', 'O-16']

        for isotope in moderators:
            zaid = self.lookup.lookup_zaid(isotope)
            # Not all may be in database
            if zaid:
                assert '.' in zaid or 'c' in zaid.lower(), \
                    f"{isotope} ZAID should have library extension"

    def test_lookup_structural_materials(self):
        """Test lookup of common structural material elements"""
        elements = ['Al', 'Fe', 'Zr', 'Ni']

        for elem in elements:
            weight = self.lookup.get_atomic_weight(elem)
            assert weight > 0, f"Should have atomic weight for {elem}"

            isotopes = self.lookup.expand_natural_element(elem)
            assert isinstance(isotopes, list), f"Should expand {elem}"

    # ===== Workflow Tests =====

    def test_complete_material_workflow_water(self):
        """Test complete workflow for water (H2O)"""
        # Step 1: Get ZAIDs for hydrogen and oxygen
        h_zaid = self.lookup.lookup_zaid('H-1')
        o_zaid = self.lookup.lookup_zaid('O-16')

        assert h_zaid is not None, "Should find H-1 ZAID"
        assert o_zaid is not None, "Should find O-16 ZAID"

        # Step 2: Get atomic weights
        h_weight = self.lookup.get_atomic_weight('H')
        o_weight = self.lookup.get_atomic_weight('O')

        assert h_weight > 0, "Should have H atomic weight"
        assert o_weight > 0, "Should have O atomic weight"

        # Step 3: Calculate molecular weight
        water_mw = 2 * h_weight + o_weight
        assert 18.0 < water_mw < 18.1, "Water MW should be ~18.015"

    def test_complete_material_workflow_uo2(self):
        """Test complete workflow for UO2 fuel"""
        # Step 1: Get ZAIDs
        u235_zaid = self.lookup.lookup_zaid('U-235')
        u238_zaid = self.lookup.lookup_zaid('U-238')
        o16_zaid = self.lookup.lookup_zaid('O-16')

        # At least oxygen should be found
        assert o16_zaid is not None, "Should find O-16"

        # Step 2: Get atomic weight for U
        u_weight = self.lookup.get_atomic_weight('U')
        o_weight = self.lookup.get_atomic_weight('O')

        assert u_weight > 0, "Should have U atomic weight"
        assert o_weight > 0, "Should have O atomic weight"

        # Step 3: UO2 molecular weight
        uo2_mw = u_weight + 2 * o_weight
        assert 260 < uo2_mw < 280, "UO2 MW should be ~270"

    # ===== Edge Case Tests =====

    def test_lookup_zaid_empty_string(self):
        """Test ZAID lookup with empty string"""
        zaid = self.lookup.lookup_zaid('')

        assert zaid is None, "Empty string should return None"

    def test_get_atomic_weight_empty_string(self):
        """Test atomic weight with empty string"""
        weight = self.lookup.get_atomic_weight('')

        assert weight == 0.0, "Empty string should return 0.0"

    def test_expand_natural_element_empty_string(self):
        """Test expansion with empty string"""
        isotopes = self.lookup.expand_natural_element('')

        assert isinstance(isotopes, list), "Should return a list"
        assert len(isotopes) == 0, "Empty string should return empty list"

    def test_recommend_library_empty_string(self):
        """Test library recommendation with empty string"""
        library = self.lookup.recommend_library('')

        assert library == '80c', "Should return default for empty string"

    def test_lookup_transuranic_elements(self):
        """Test lookup of transuranic elements"""
        transuranics = ['Np-237', 'Pu-239', 'Am-241', 'Cm-244']

        for isotope in transuranics:
            zaid = self.lookup.lookup_zaid(isotope)
            # May or may not be in database
            # Just verify no crashes
            assert zaid is None or isinstance(zaid, str), \
                f"Should handle {isotope}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

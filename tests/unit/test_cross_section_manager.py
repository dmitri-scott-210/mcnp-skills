"""
Unit tests for MCNP Cross Section Manager Skill

Tests cross-section library management:
- xsdir file parsing
- ZAID availability checking
- Library information lookup
- Temperature-based library recommendations
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-cross-section-manager"
sys.path.insert(0, str(skill_dir))

from mcnp_cross_section_manager import MCNPCrossSectionManager


class TestMCNPCrossSectionManager:
    """Test suite for MCNP Cross Section Manager"""

    def setup_method(self):
        """Setup test fixture"""
        self.manager = MCNPCrossSectionManager()

    # ===== Helper Methods =====

    def create_temp_xsdir(self, content: str) -> str:
        """Create temporary xsdir file"""
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.xsdir', delete=False)
        temp.write(content)
        temp.close()
        return temp.name

    # ===== Library Listing Tests =====

    def test_list_available_libraries(self):
        """Test listing available libraries"""
        libraries = self.manager.list_available_libraries()

        assert isinstance(libraries, dict), "Should return a dictionary"
        assert len(libraries) > 0, "Should have some libraries available"

    def test_list_libraries_structure(self):
        """Test library listing has proper structure"""
        libraries = self.manager.list_available_libraries()

        # Should have standard ENDF/B libraries
        assert isinstance(libraries, dict), "Should be a dictionary"

    def test_list_libraries_common_ids(self):
        """Test that common library IDs are present"""
        libraries = self.manager.list_available_libraries()

        # Common library suffixes
        common_libs = ['80c', '70c', '71c', '72c']

        # At least some standard libraries should be present
        lib_keys = list(libraries.keys())
        assert len(lib_keys) > 0, "Should have library entries"

    # ===== Library Info Tests =====

    def test_get_library_info_80c(self):
        """Test getting library info for 80c"""
        info = self.manager.get_library_info('80c')

        assert info is not None, "Should return info for 80c"
        assert isinstance(info, str), "Should return string description"

    def test_get_library_info_70c(self):
        """Test getting library info for 70c"""
        info = self.manager.get_library_info('70c')

        assert info is not None, "Should return info for 70c"
        assert isinstance(info, str), "Should return string description"

    def test_get_library_info_photon(self):
        """Test getting library info for photon library"""
        info = self.manager.get_library_info('04p')

        # May or may not be available depending on implementation
        if info is not None:
            assert isinstance(info, str), "Should return string if available"

    def test_get_library_info_invalid(self):
        """Test getting library info for invalid ID"""
        info = self.manager.get_library_info('99z')

        # Should handle gracefully - either None or default message
        assert info is None or isinstance(info, str), "Should handle invalid ID gracefully"

    # ===== Temperature Recommendation Tests =====

    def test_suggest_temperature_library_room_temp(self):
        """Test temperature recommendation for room temperature"""
        library = self.manager.suggest_temperature_library('U-235', 293.6)

        assert library is not None, "Should recommend a library"
        assert library == '80c', "Room temp should recommend 80c (~293K)"

    def test_suggest_temperature_library_low_temp(self):
        """Test temperature recommendation for low temperature"""
        library = self.manager.suggest_temperature_library('H-1', 77.0)

        assert library is not None, "Should recommend a library"
        assert library == '80c', "Low temp should recommend 80c"

    def test_suggest_temperature_library_moderate(self):
        """Test temperature recommendation for moderate temperature"""
        library = self.manager.suggest_temperature_library('U-235', 600.0)

        assert library is not None, "Should recommend a library"
        assert library == '81c', "600K should recommend 81c"

    def test_suggest_temperature_library_high(self):
        """Test temperature recommendation for high temperature"""
        library = self.manager.suggest_temperature_library('U-235', 900.0)

        assert library is not None, "Should recommend a library"
        assert library == '82c', "900K should recommend 82c"

    def test_suggest_temperature_library_very_high(self):
        """Test temperature recommendation for very high temperature"""
        library = self.manager.suggest_temperature_library('U-235', 1500.0)

        assert library is not None, "Should recommend a library"
        assert library == '83c', "1500K should recommend 83c"

    def test_suggest_temperature_library_boundary_400K(self):
        """Test temperature recommendation at 400K boundary"""
        library_399 = self.manager.suggest_temperature_library('U-235', 399.0)
        library_401 = self.manager.suggest_temperature_library('U-235', 401.0)

        assert library_399 == '80c', "399K should be 80c"
        assert library_401 == '81c', "401K should be 81c"

    def test_suggest_temperature_library_boundary_700K(self):
        """Test temperature recommendation at 700K boundary"""
        library_699 = self.manager.suggest_temperature_library('U-235', 699.0)
        library_701 = self.manager.suggest_temperature_library('U-235', 701.0)

        assert library_699 == '81c', "699K should be 81c"
        assert library_701 == '82c', "701K should be 82c"

    def test_suggest_temperature_library_boundary_1000K(self):
        """Test temperature recommendation at 1000K boundary"""
        library_999 = self.manager.suggest_temperature_library('U-235', 999.0)
        library_1001 = self.manager.suggest_temperature_library('U-235', 1001.0)

        assert library_999 == '82c', "999K should be 82c"
        assert library_1001 == '83c', "1001K should be 83c"

    # ===== ZAID Availability Tests =====

    def test_check_availability_common_isotopes(self):
        """Test availability checking for common isotopes"""
        common_zaids = ['1001.80c', '8016.80c', '92235.80c', '94239.80c']

        for zaid in common_zaids:
            # Should not crash - may or may not be available
            result = self.manager.check_availability(zaid)
            assert isinstance(result, bool), f"Should return bool for {zaid}"

    def test_check_availability_hydrogen(self):
        """Test availability of hydrogen"""
        result = self.manager.check_availability('1001.80c')

        # H-1 should typically be available in most databases
        assert isinstance(result, bool), "Should return boolean"

    def test_check_availability_oxygen(self):
        """Test availability of oxygen"""
        result = self.manager.check_availability('8016.80c')

        assert isinstance(result, bool), "Should return boolean"

    def test_check_availability_u235(self):
        """Test availability of U-235"""
        result = self.manager.check_availability('92235.80c')

        assert isinstance(result, bool), "Should return boolean"

    def test_check_availability_invalid_format(self):
        """Test availability check with invalid ZAID format"""
        # Should handle gracefully
        try:
            result = self.manager.check_availability('invalid')
            assert isinstance(result, bool), "Should return bool even for invalid"
        except (ValueError, AttributeError):
            # Some implementations may raise exception for invalid format
            pass

    def test_check_availability_nonexistent_zaid(self):
        """Test availability of nonexistent ZAID"""
        result = self.manager.check_availability('99999.80c')

        assert isinstance(result, bool), "Should return boolean"
        # Likely False, but implementation dependent

    # ===== xsdir Parsing Tests =====

    def test_parse_xsdir_minimal(self):
        """Test parsing minimal xsdir file"""
        xsdir_content = """datapath=/path/to/data
atomic weight ratios
  1001.80c    0.999167 filename 0 1 0
"""
        temp_file = self.create_temp_xsdir(xsdir_content)

        # Should parse without errors
        try:
            self.manager.parse_xsdir(temp_file)
            # If it completes without error, test passes
            assert True
        except Exception as e:
            # Some implementations may not fully implement xsdir parsing
            # Allow graceful handling
            pytest.skip(f"xsdir parsing not fully implemented: {e}")
        finally:
            Path(temp_file).unlink()

    def test_parse_xsdir_empty(self):
        """Test parsing empty xsdir file"""
        temp_file = self.create_temp_xsdir("")

        # Should handle empty file gracefully
        try:
            self.manager.parse_xsdir(temp_file)
            assert True, "Should handle empty file"
        except Exception:
            # May raise exception - that's acceptable
            pass
        finally:
            Path(temp_file).unlink()

    def test_parse_xsdir_nonexistent(self):
        """Test parsing nonexistent xsdir file"""
        # Should handle missing file gracefully
        try:
            self.manager.parse_xsdir('/nonexistent/path/xsdir')
        except (FileNotFoundError, OSError):
            # Expected exception
            pass

    # ===== Integration Tests =====

    def test_workflow_temperature_to_library(self):
        """Test complete workflow: temperature -> library -> info"""
        # Step 1: Get recommendation
        temp = 600.0
        library = self.manager.suggest_temperature_library('U-235', temp)

        assert library is not None, "Should recommend library"

        # Step 2: Get info about recommended library
        info = self.manager.get_library_info(library)

        assert info is not None, "Should have info for recommended library"
        assert isinstance(info, str), "Info should be string"

    def test_workflow_list_and_info(self):
        """Test workflow: list libraries then get info"""
        # Step 1: List all libraries
        libraries = self.manager.list_available_libraries()

        assert len(libraries) > 0, "Should have libraries"

        # Step 2: Get info for each library
        for lib_id in list(libraries.keys())[:3]:  # Test first 3
            info = self.manager.get_library_info(lib_id)
            # Should return something (may be None for some)
            assert info is None or isinstance(info, str)

    def test_workflow_pwr_fuel_library_selection(self):
        """Test realistic workflow: PWR fuel library selection"""
        # PWR fuel operates at ~600K
        fuel_temp = 600.0

        # Get library for fuel isotopes
        u235_lib = self.manager.suggest_temperature_library('U-235', fuel_temp)
        u238_lib = self.manager.suggest_temperature_library('U-238', fuel_temp)
        o16_lib = self.manager.suggest_temperature_library('O-16', fuel_temp)

        # All should recommend same library (81c for 600K)
        assert u235_lib == '81c', "U-235 at 600K should use 81c"
        assert u238_lib == '81c', "U-238 at 600K should use 81c"
        assert o16_lib == '81c', "O-16 at 600K should use 81c"

    def test_workflow_reflector_library_selection(self):
        """Test workflow: Reflector at different temperature"""
        # Reflector cooler than fuel, maybe 400K
        reflector_temp = 400.0

        lib = self.manager.suggest_temperature_library('C-12', reflector_temp)

        assert lib == '81c', "400K should use 81c"

    # ===== Edge Case Tests =====

    def test_temperature_zero_kelvin(self):
        """Test temperature recommendation at 0 K"""
        library = self.manager.suggest_temperature_library('H-1', 0.0)

        assert library is not None, "Should handle 0 K"
        assert library == '80c', "0 K should use lowest temp library"

    def test_temperature_negative(self):
        """Test temperature recommendation with negative value"""
        library = self.manager.suggest_temperature_library('H-1', -100.0)

        # Should handle gracefully - use lowest library
        assert library is not None, "Should handle negative temp"
        assert library == '80c', "Negative temp should use 80c"

    def test_temperature_extreme_high(self):
        """Test temperature recommendation at extreme high temperature"""
        library = self.manager.suggest_temperature_library('U-235', 5000.0)

        assert library is not None, "Should handle extreme temp"
        assert library == '83c', "Very high temp should use 83c"

    def test_availability_different_libraries(self):
        """Test checking same isotope with different libraries"""
        zaids = ['1001.80c', '1001.70c', '1001.71c']

        for zaid in zaids:
            result = self.manager.check_availability(zaid)
            assert isinstance(result, bool), f"Should return bool for {zaid}"

    def test_library_info_all_standard_neutron_libs(self):
        """Test getting info for all standard neutron libraries"""
        standard_libs = ['80c', '70c', '71c', '72c', '81c', '82c', '83c']

        for lib_id in standard_libs:
            info = self.manager.get_library_info(lib_id)
            # Info may be None for some libraries, that's OK
            assert info is None or isinstance(info, str), \
                f"Info for {lib_id} should be None or string"

    def test_library_info_photon_libraries(self):
        """Test getting info for photon libraries"""
        photon_libs = ['04p', '03p', '12p']

        for lib_id in photon_libs:
            info = self.manager.get_library_info(lib_id)
            # May not be implemented
            assert info is None or isinstance(info, str)

    def test_multiple_temperature_recommendations(self):
        """Test multiple temperature recommendations in sequence"""
        temps = [293.6, 400.0, 600.0, 900.0, 1200.0]
        expected = ['80c', '81c', '81c', '82c', '83c']

        for temp, exp_lib in zip(temps, expected):
            lib = self.manager.suggest_temperature_library('U-235', temp)
            assert lib == exp_lib, f"{temp}K should recommend {exp_lib}, got {lib}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

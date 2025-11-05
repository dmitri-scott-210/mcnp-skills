"""
Unit tests for MCNP Mesh Builder Skill

Tests mesh tally construction capabilities:
- Rectangular (xyz) FMESH tallies
- Cylindrical (cyl, rzt) FMESH tallies
- TMESH tallies
- Energy binning
- Mesh size estimation
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-mesh-builder"
sys.path.insert(0, str(skill_dir))

from mcnp_mesh_builder import MCNPMeshBuilder


class TestMCNPMeshBuilder:
    """Test suite for MCNP Mesh Builder"""

    def setup_method(self):
        """Setup test fixture"""
        self.builder = MCNPMeshBuilder()

    # ===== Rectangular Mesh Tests =====

    def test_rectangular_mesh_basic(self):
        """Test basic rectangular mesh"""
        result = self.builder.add_rectangular_mesh(
            tally_num=104,
            particle='n',
            origin=(0, 0, 0),
            imesh=[10], jmesh=[10], kmesh=[10],
            iints=[5], jints=[5], kints=[5]
        )
        assert result is not None
        assert 'fmesh104:n' in result
        assert 'geom=xyz' in result

    def test_rectangular_mesh_custom_origin(self):
        """Test rectangular mesh with custom origin"""
        result = self.builder.add_rectangular_mesh(
            tally_num=104,
            particle='n',
            origin=(-10, -10, 0),
            imesh=[10], jmesh=[10], kmesh=[10],
            iints=[5], jints=[5], kints=[5]
        )
        assert '-10' in result

    def test_rectangular_mesh_multiple_bins(self):
        """Test rectangular mesh with multiple bin boundaries"""
        result = self.builder.add_rectangular_mesh(
            tally_num=104,
            particle='n',
            origin=(0, 0, 0),
            imesh=[10, 20], jmesh=[10], kmesh=[10],
            iints=[5, 10], jints=[5], kints=[5]
        )
        assert '10 20' in result

    def test_rectangular_mesh_photon(self):
        """Test rectangular mesh for photons"""
        result = self.builder.add_rectangular_mesh(
            tally_num=114,
            particle='p',
            origin=(0, 0, 0),
            imesh=[10], jmesh=[10], kmesh=[10],
            iints=[5], jints=[5], kints=[5]
        )
        assert 'fmesh114:p' in result

    def test_rectangular_mesh_with_energy(self):
        """Test rectangular mesh with energy binning"""
        result = self.builder.add_rectangular_mesh(
            tally_num=104,
            particle='n',
            origin=(0, 0, 0),
            imesh=[10], jmesh=[10], kmesh=[10],
            iints=[5], jints=[5], kints=[5],
            emesh=[0.1, 1.0, 10.0],
            eints=[1, 1, 1]
        )
        assert 'emesh=' in result
        assert 'eints=' in result

    def test_rectangular_mesh_xdmf_output(self):
        """Test rectangular mesh with XDMF output"""
        result = self.builder.add_rectangular_mesh(
            tally_num=104,
            particle='n',
            origin=(0, 0, 0),
            imesh=[10], jmesh=[10], kmesh=[10],
            iints=[5], jints=[5], kints=[5],
            out_format='xdmf'
        )
        assert 'out=xdmf' in result

    def test_rectangular_mesh_mismatched_arrays(self):
        """Test rectangular mesh with mismatched array lengths"""
        with pytest.raises(ValueError):
            self.builder.add_rectangular_mesh(
                tally_num=104,
                particle='n',
                origin=(0, 0, 0),
                imesh=[10, 20],  # 2 elements
                jmesh=[10], kmesh=[10],
                iints=[5],  # 1 element - MISMATCH
                jints=[5], kints=[5]
            )

    # ===== Cylindrical Mesh Tests =====

    def test_cylindrical_mesh_basic(self):
        """Test basic cylindrical mesh"""
        result = self.builder.add_cylindrical_mesh(
            tally_num=204,
            particle='n',
            origin=(0, 0, 0),
            axis=(0, 0, 1),
            vec=(1, 0, 0),
            rmesh=[5, 10],
            zmesh=[0, 10, 20],
            rints=[5, 5],
            zints=[5, 5]
        )
        assert result is not None
        assert 'fmesh204:n' in result
        assert 'geom=cyl' in result

    def test_cylindrical_mesh_custom_axis(self):
        """Test cylindrical mesh with custom axis"""
        result = self.builder.add_cylindrical_mesh(
            tally_num=204,
            particle='n',
            origin=(0, 0, 0),
            axis=(1, 0, 0),  # X-axis cylinder
            vec=(0, 1, 0),
            rmesh=[5],
            zmesh=[10],
            rints=[5],
            zints=[5]
        )
        assert 'axs=1 0 0' in result

    def test_cylindrical_mesh_rzt_geometry(self):
        """Test cylindrical mesh with RZT geometry"""
        result = self.builder.add_cylindrical_mesh(
            tally_num=204,
            particle='n',
            origin=(0, 0, 0),
            axis=(0, 0, 1),
            vec=(1, 0, 0),
            rmesh=[5],
            zmesh=[10],
            rints=[5],
            zints=[5],
            geometry='rzt'
        )
        assert 'geom=rzt' in result

    # ===== TMESH Tests =====

    def test_tmesh_rectangular(self):
        """Test TMESH rectangular mesh"""
        result = self.builder.add_tmesh(
            mesh_num=1,
            particle='n',
            mesh_type='rmesh',
            cora=[0, 10, 20],
            corb=[0, 10, 20],
            corc=[0, 10, 20]
        )
        assert result is not None
        assert 'tmesh' in result
        assert 'rmesh1:n' in result

    def test_tmesh_with_energy(self):
        """Test TMESH with energy binning"""
        result = self.builder.add_tmesh(
            mesh_num=1,
            particle='n',
            mesh_type='rmesh',
            cora=[0, 10],
            corb=[0, 10],
            corc=[0, 10],
            ergsh=[0.1, 1.0, 10.0]
        )
        assert 'ergsh1' in result

    def test_tmesh_cylindrical(self):
        """Test TMESH cylindrical mesh"""
        result = self.builder.add_tmesh(
            mesh_num=11,
            particle='n',
            mesh_type='cmesh',
            cora=[0, 5, 10],  # Radial
            corb=[0, 360],    # Theta
            corc=[0, 100]     # Z
        )
        assert 'cmesh11:n' in result

    def test_tmesh_spherical(self):
        """Test TMESH spherical mesh"""
        result = self.builder.add_tmesh(
            mesh_num=21,
            particle='n',
            mesh_type='smesh',
            cora=[0, 5, 10],   # Radial
            corb=[0, 180],     # Theta
            corc=[0, 360]      # Phi
        )
        assert 'smesh21:n' in result

    # ===== Unstructured Mesh Tests =====

    def test_unstructured_mesh(self):
        """Test unstructured mesh embedding"""
        result = self.builder.add_unstructured_mesh(
            mesh_file='reactor.inp',
            background_cell=100
        )
        assert result is not None
        assert 'embed' in result
        assert 'embee' in result

    # ===== Mesh Size Estimation Tests =====

    def test_estimate_mesh_size_small(self):
        """Test mesh size estimation for small mesh"""
        result = self.builder.estimate_mesh_size(10, 10, 10)
        assert result is not None
        assert 'total_bins' in result
        assert result['total_bins'] == 1000

    def test_estimate_mesh_size_with_energy(self):
        """Test mesh size estimation with energy bins"""
        result = self.builder.estimate_mesh_size(10, 10, 10, ne=5)
        assert result['total_bins'] == 5000

    def test_estimate_mesh_size_target_error(self):
        """Test mesh size estimation with custom error target"""
        result = self.builder.estimate_mesh_size(10, 10, 10, stat_target=0.01)
        assert result['particles_per_bin'] == 10000  # (1/0.01)^2

    def test_estimate_mesh_size_has_recommendation(self):
        """Test mesh size estimation provides recommendation"""
        result = self.builder.estimate_mesh_size(10, 10, 10)
        assert 'recommendation' in result
        assert 'particles' in result['recommendation'].lower()

    def test_estimate_mesh_size_large_mesh(self):
        """Test mesh size estimation for large mesh"""
        result = self.builder.estimate_mesh_size(50, 50, 50, ne=10)
        assert result['total_bins'] == 1250000  # 50*50*50*10
        assert result['total_particles_needed'] > 1e6

    # ===== Card Generation Tests =====

    def test_generate_cards_empty(self):
        """Test generate_cards with no meshes"""
        result = self.builder.generate_cards()
        assert result is not None
        assert 'Mesh Tally' in result

    def test_generate_cards_single_mesh(self):
        """Test generate_cards with one mesh"""
        self.builder.add_rectangular_mesh(
            tally_num=104,
            particle='n',
            origin=(0, 0, 0),
            imesh=[10], jmesh=[10], kmesh=[10],
            iints=[5], jints=[5], kints=[5]
        )
        result = self.builder.generate_cards()
        assert 'fmesh104:n' in result

    def test_generate_cards_multiple_meshes(self):
        """Test generate_cards with multiple meshes"""
        self.builder.add_rectangular_mesh(
            tally_num=104,
            particle='n',
            origin=(0, 0, 0),
            imesh=[10], jmesh=[10], kmesh=[10],
            iints=[5], jints=[5], kints=[5]
        )
        self.builder.add_cylindrical_mesh(
            tally_num=204,
            particle='n',
            origin=(0, 0, 0),
            axis=(0, 0, 1),
            vec=(1, 0, 0),
            rmesh=[5],
            zmesh=[10],
            rints=[5],
            zints=[5]
        )
        result = self.builder.generate_cards()
        assert 'fmesh104:n' in result
        assert 'fmesh204:n' in result

    # ===== Integration Tests =====

    def test_pwr_core_mesh(self):
        """Test realistic PWR core mesh"""
        result = self.builder.add_cylindrical_mesh(
            tally_num=304,
            particle='n',
            origin=(0, 0, 0),
            axis=(0, 0, 1),
            vec=(1, 0, 0),
            rmesh=[50, 100, 150],  # Radial zones
            zmesh=[0, 100, 200, 366],  # Core height
            rints=[10, 10, 10],
            zints=[20, 20, 33],
            out_format='xdmf'
        )
        assert result is not None
        assert 'geom=cyl' in result
        assert 'out=xdmf' in result

    def test_reactor_building_mesh(self):
        """Test reactor building mesh"""
        result = self.builder.add_rectangular_mesh(
            tally_num=104,
            particle='n',
            origin=(-500, -500, 0),
            imesh=[500],
            jmesh=[500],
            kmesh=[1000],
            iints=[50],
            jints=[50],
            kints=[50],
            out_format='xdmf'
        )
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

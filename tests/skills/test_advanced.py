"""
Test suite for Category E: Advanced Operations Skills (5 skills)
"""
import pytest
import sys
from pathlib import Path

# Add project root to path to import from .claude/skills/
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import from new .claude/skills/ structure
from claude.skills.mcnp_burnup_builder.mcnp_burnup_builder import MCNPBurnupBuilder
from claude.skills.mcnp_mesh_builder.mcnp_mesh_builder import MCNPMeshBuilder
from claude.skills.mcnp_lattice_builder.mcnp_lattice_builder import MCNPLatticeBuilder
from claude.skills.mcnp_ww_optimizer.mcnp_ww_optimizer import MCNPWeightWindowOptimizer
from claude.skills.mcnp_parallel_configurator.mcnp_parallel_configurator import MCNPParallelConfigurator

class TestMCNPBurnupBuilder:
    
    def test_add_burn_card(self):
        """Test adding BURN card"""
        builder = MCNPBurnupBuilder()
        builder.add_burn_card(
            time_values=[0, 1, 10, 100],
            time_units='days',
            power=100.0
        )
        
        result = builder.generate_cards()
        assert 'burn' in result.lower()
        assert 'time' in result.lower()
    
    def test_set_depletion_cells(self):
        """Test specifying depletion cells"""
        builder = MCNPBurnupBuilder()
        builder.set_depletion_cells([10, 20, 30])
        
        result = builder.generate_cards()
        assert '10' in result and '20' in result and '30' in result
    
    def test_add_fission_products(self):
        """Test including fission products"""
        builder = MCNPBurnupBuilder()
        builder.add_burn_card(time_values=[0, 1], time_units='days')
        builder.add_fission_products()
        
        result = builder.generate_cards()
        # Should reference fission product libraries
        assert 'fp' in result.lower() or 'fission' in result.lower()

class TestMCNPMeshBuilder:
    
    def test_rectangular_mesh(self):
        """Test rectangular mesh tally"""
        builder = MCNPMeshBuilder()
        builder.add_rectangular_mesh(
            tally_number=14,
            particle='n',
            x_bins=[-10, 0, 10],
            y_bins=[-10, 0, 10],
            z_bins=[-10, 0, 10]
        )
        
        result = builder.generate_cards()
        assert 'fmesh14:n' in result.lower()
        assert 'geom=xyz' in result.lower()
    
    def test_cylindrical_mesh(self):
        """Test cylindrical mesh"""
        builder = MCNPMeshBuilder()
        builder.add_cylindrical_mesh(
            tally_number=24,
            particle='n',
            axis='z',
            r_bins=[0, 1, 2, 5],
            z_bins=[-10, 0, 10]
        )
        
        result = builder.generate_cards()
        assert 'fmesh24:n' in result.lower()
        assert 'geom=cyl' in result.lower() or 'geom=rzt' in result.lower()
    
    def test_add_energy_bins(self):
        """Test adding energy bins to mesh"""
        builder = MCNPMeshBuilder()
        builder.add_rectangular_mesh(14, 'n', [-5, 5], [-5, 5], [-5, 5])
        builder.add_energy_bins(14, [0.01, 0.1, 1.0, 10.0])
        
        result = builder.generate_cards()
        assert 'emesh14' in result.lower()

class TestMCNPLatticeBuilder:
    
    def test_hexagonal_lattice(self):
        """Test hexagonal lattice generation"""
        builder = MCNPLatticeBuilder()
        builder.create_hexagonal_lattice(
            universe_number=100,
            pitch=1.26,
            n_rings=3,
            fill_pattern={0: 1, 1: 2}  # Ring 0: universe 1, ring 1: universe 2
        )
        
        result = builder.generate_cards()
        assert 'lat=2' in result.lower()
        assert 'fill' in result.lower()
    
    def test_rectangular_lattice(self):
        """Test rectangular lattice"""
        builder = MCNPLatticeBuilder()
        builder.create_rectangular_lattice(
            universe_number=200,
            nx=3, ny=3, nz=1,
            pitch_x=1.26, pitch_y=1.26, pitch_z=10.0,
            fill_pattern=[1, 2, 1, 2, 3, 2, 1, 2, 1]
        )
        
        result = builder.generate_cards()
        assert 'lat=1' in result.lower()
        assert 'fill' in result.lower()
    
    def test_infinite_lattice(self):
        """Test infinite lattice with single universe"""
        builder = MCNPLatticeBuilder()
        builder.create_rectangular_lattice(
            universe_number=300,
            nx=1, ny=1, nz=1,
            pitch_x=1.26, pitch_y=1.26, pitch_z=10.0,
            fill_pattern=[10]
        )
        
        result = builder.generate_cards()
        assert 'lat=1' in result.lower()

class TestMCNPWeightWindowOptimizer:
    
    def test_setup_wwg(self):
        """Test weight window generator setup"""
        optimizer = MCNPWeightWindowOptimizer()
        optimizer.setup_wwg(
            particle='n',
            target_cells=[100],
            mesh_type='rectangular'
        )
        
        result = optimizer.generate_cards()
        assert 'wwg' in result.lower()
    
    def test_add_mesh_ww(self):
        """Test mesh-based weight windows"""
        optimizer = MCNPWeightWindowOptimizer()
        optimizer.add_mesh_ww(
            particle='n',
            x_bins=[-10, 0, 10],
            y_bins=[-10, 0, 10],
            z_bins=[-10, 0, 10]
        )
        
        result = optimizer.generate_cards()
        assert 'mesh' in result.lower()
    
    def test_iterate_ww(self):
        """Test iterative weight window generation"""
        optimizer = MCNPWeightWindowOptimizer()
        optimizer.setup_wwg('n', [100], 'rectangular')
        
        instructions = optimizer.iterate_ww(n_iterations=3)
        assert '3' in instructions or 'three' in instructions.lower()

class TestMCNPParallelConfigurator:
    
    def test_generate_tasks_card(self):
        """Test TASKS card generation"""
        config = MCNPParallelConfigurator()
        tasks_card = config.generate_tasks_card(n_tasks=8)
        
        assert 'prdmp' in tasks_card.lower() or 'tasks' in tasks_card.lower()
        assert '8' in tasks_card
    
    def test_generate_slurm_script(self):
        """Test SLURM batch script generation"""
        config = MCNPParallelConfigurator()
        script = config.generate_slurm_script(
            job_name='mcnp_test',
            n_nodes=2,
            n_tasks=32,
            time_hours=4,
            input_file='test.i'
        )
        
        assert '#SBATCH' in script
        assert 'srun' in script or 'mpirun' in script
        assert 'mcnp6' in script.lower()
    
    def test_estimate_resources(self):
        """Test resource estimation"""
        config = MCNPParallelConfigurator()
        estimate = config.estimate_resources(
            n_particles=1e8,
            expected_runtime_hours=10.0
        )
        
        assert 'tasks' in estimate or 'cores' in estimate

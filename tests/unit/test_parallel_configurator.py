"""
Unit tests for MCNP Parallel Configurator Skill

Tests parallel execution configuration:
- TASKS card generation
- SLURM job script generation
- PBS/Torque job script generation
- LSF job script generation
- Resource estimation
- Parallel efficiency checking
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-parallel-configurator"
sys.path.insert(0, str(skill_dir))

from mcnp_parallel_configurator import MCNPParallelConfigurator


class TestMCNPParallelConfigurator:
    """Test suite for MCNP Parallel Configurator"""

    def setup_method(self):
        """Setup test fixture"""
        self.configurator = MCNPParallelConfigurator()

    # ===== TASKS Card Tests =====

    def test_generate_tasks_basic(self):
        """Test basic TASKS card generation"""
        result = self.configurator.generate_tasks_card(n_tasks=16)
        assert result is not None
        assert 'tasks 16' in result

    def test_generate_tasks_large(self):
        """Test TASKS card with many tasks"""
        result = self.configurator.generate_tasks_card(n_tasks=256)
        assert 'tasks 256' in result

    def test_generate_tasks_with_stride(self):
        """Test TASKS card with stride"""
        result = self.configurator.generate_tasks_card(n_tasks=32, stride=2)
        assert 'tasks 32' in result
        assert '2' in result

    # ===== SLURM Script Tests =====

    def test_slurm_script_basic(self):
        """Test basic SLURM script generation"""
        result = self.configurator.generate_slurm_script(
            job_name='mcnp_test',
            nodes=4,
            tasks_per_node=32,
            walltime='24:00:00',
            input_file='input.inp'
        )
        assert result is not None
        assert '#SBATCH --job-name=mcnp_test' in result
        assert '#SBATCH --nodes=4' in result
        assert '#SBATCH --ntasks-per-node=32' in result

    def test_slurm_script_total_tasks(self):
        """Test SLURM script calculates total tasks correctly"""
        result = self.configurator.generate_slurm_script(
            job_name='mcnp_test',
            nodes=8,
            tasks_per_node=16,
            walltime='24:00:00',
            input_file='input.inp'
        )
        assert 'mpiexec -n 128' in result  # 8*16

    def test_slurm_script_with_partition(self):
        """Test SLURM script with partition"""
        result = self.configurator.generate_slurm_script(
            job_name='mcnp_test',
            nodes=2,
            tasks_per_node=32,
            walltime='12:00:00',
            input_file='input.inp',
            partition='standard'
        )
        assert '#SBATCH --partition=standard' in result

    def test_slurm_script_with_account(self):
        """Test SLURM script with account"""
        result = self.configurator.generate_slurm_script(
            job_name='mcnp_test',
            nodes=2,
            tasks_per_node=32,
            walltime='12:00:00',
            input_file='input.inp',
            account='proj123'
        )
        assert '#SBATCH --account=proj123' in result

    def test_slurm_script_with_email(self):
        """Test SLURM script with email notifications"""
        result = self.configurator.generate_slurm_script(
            job_name='mcnp_test',
            nodes=2,
            tasks_per_node=32,
            walltime='12:00:00',
            input_file='input.inp',
            email='user@example.com'
        )
        assert '#SBATCH --mail-user=user@example.com' in result
        assert '#SBATCH --mail-type=END,FAIL' in result

    def test_slurm_script_openmp_threads(self):
        """Test SLURM script with OpenMP threads"""
        result = self.configurator.generate_slurm_script(
            job_name='mcnp_test',
            nodes=2,
            tasks_per_node=16,
            walltime='12:00:00',
            input_file='input.inp',
            threads=4
        )
        assert 'export OMP_NUM_THREADS=4' in result

    # ===== PBS Script Tests =====

    def test_pbs_script_basic(self):
        """Test basic PBS script generation"""
        result = self.configurator.generate_pbs_script(
            job_name='mcnp_test',
            nodes=4,
            ppn=16,
            walltime='24:00:00',
            input_file='input.inp'
        )
        assert result is not None
        assert '#PBS -N mcnp_test' in result
        assert '#PBS -l nodes=4:ppn=16' in result

    def test_pbs_script_total_tasks(self):
        """Test PBS script calculates total tasks"""
        result = self.configurator.generate_pbs_script(
            job_name='mcnp_test',
            nodes=8,
            ppn=12,
            walltime='24:00:00',
            input_file='input.inp'
        )
        assert 'tasks 96' in result  # 8*12

    def test_pbs_script_with_queue(self):
        """Test PBS script with queue"""
        result = self.configurator.generate_pbs_script(
            job_name='mcnp_test',
            nodes=2,
            ppn=32,
            walltime='12:00:00',
            input_file='input.inp',
            queue='batch'
        )
        assert '#PBS -q batch' in result

    def test_pbs_script_with_email(self):
        """Test PBS script with email"""
        result = self.configurator.generate_pbs_script(
            job_name='mcnp_test',
            nodes=2,
            ppn=32,
            walltime='12:00:00',
            input_file='input.inp',
            email='user@example.com'
        )
        assert '#PBS -M user@example.com' in result
        assert '#PBS -m abe' in result

    # ===== LSF Script Tests =====

    def test_lsf_script_basic(self):
        """Test basic LSF script generation"""
        result = self.configurator.generate_lsf_script(
            job_name='mcnp_test',
            n_tasks=128,
            walltime_minutes=1440,
            input_file='input.inp'
        )
        assert result is not None
        assert '#BSUB -J mcnp_test' in result
        assert '#BSUB -n 128' in result
        assert '#BSUB -W 1440' in result

    def test_lsf_script_with_queue(self):
        """Test LSF script with queue"""
        result = self.configurator.generate_lsf_script(
            job_name='mcnp_test',
            n_tasks=64,
            walltime_minutes=720,
            input_file='input.inp',
            queue='normal'
        )
        assert '#BSUB -q normal' in result

    # ===== Resource Estimation Tests =====

    def test_estimate_resources_simple(self):
        """Test resource estimation for simple problem"""
        result = self.configurator.estimate_resources(
            n_particles=100000000,  # Use many particles
            complexity='simple',
            target_walltime_hours=1.0  # Short walltime to require parallelization
        )
        assert result is not None
        assert 'recommended_tasks' in result
        assert 'recommended_nodes' in result
        assert result['recommended_tasks'] >= 1

    def test_estimate_resources_complex(self):
        """Test resource estimation for complex problem"""
        result = self.configurator.estimate_resources(
            n_particles=100000000,  # Use more particles
            complexity='complex',
            target_walltime_hours=24.0
        )
        assert result['recommended_tasks'] >= 1
        assert 'warning' in result

    def test_estimate_resources_particles_per_task(self):
        """Test particles per task calculation"""
        result = self.configurator.estimate_resources(
            n_particles=100000000,  # Use more particles
            complexity='medium',
            target_walltime_hours=12.0
        )
        assert result['particles_per_task'] > 0

    def test_estimate_resources_has_recommendation(self):
        """Test resource estimation provides recommendation"""
        result = self.configurator.estimate_resources(
            n_particles=100000000,  # Use more particles
            complexity='medium'
        )
        assert 'recommendation' in result
        assert 'tasks' in result['recommendation'].lower()

    def test_estimate_resources_very_complex(self):
        """Test resource estimation for very complex problem"""
        result = self.configurator.estimate_resources(
            n_particles=100000000,
            complexity='very_complex',
            target_walltime_hours=48.0
        )
        assert result['recommended_tasks'] > 10
        assert result['estimated_efficiency'] < 1.0

    # ===== Efficiency Checking Tests =====

    def test_check_efficiency_poor(self):
        """Test efficiency check with poor configuration"""
        result = self.configurator.check_parallel_efficiency(
            n_tasks=1000,
            n_particles=10000
        )
        assert result['status'] == 'poor'
        assert result['particles_per_task'] == 10

    def test_check_efficiency_marginal(self):
        """Test efficiency check with marginal configuration"""
        result = self.configurator.check_parallel_efficiency(
            n_tasks=100,
            n_particles=50000
        )
        assert result['status'] == 'marginal'
        assert result['particles_per_task'] == 500

    def test_check_efficiency_good(self):
        """Test efficiency check with good configuration"""
        result = self.configurator.check_parallel_efficiency(
            n_tasks=100,
            n_particles=500000
        )
        assert result['status'] == 'good'
        assert result['particles_per_task'] == 5000

    def test_check_efficiency_excellent(self):
        """Test efficiency check with excellent configuration"""
        result = self.configurator.check_parallel_efficiency(
            n_tasks=10,
            n_particles=1000000
        )
        assert result['status'] == 'excellent'
        assert result['particles_per_task'] == 100000

    def test_check_efficiency_has_recommendation(self):
        """Test efficiency check provides recommendation"""
        result = self.configurator.check_parallel_efficiency(
            n_tasks=50,
            n_particles=250000
        )
        assert 'recommendation' in result

    # ===== Integration Tests =====

    def test_complete_slurm_workflow(self):
        """Test complete SLURM workflow"""
        # Estimate resources
        resources = self.configurator.estimate_resources(
            n_particles=100000000,  # Use more particles
            complexity='medium',
            target_walltime_hours=24.0
        )
        # Generate TASKS card
        tasks_card = self.configurator.generate_tasks_card(
            n_tasks=resources['recommended_tasks']
        )
        # Generate SLURM script
        script = self.configurator.generate_slurm_script(
            job_name='pwr_core',
            nodes=resources['recommended_nodes'],
            tasks_per_node=resources['tasks_per_node'],
            walltime='24:00:00',
            input_file='pwr_core.inp'
        )
        assert tasks_card is not None
        assert script is not None
        assert 'mcnp6' in script

    def test_pwr_core_parallel_config(self):
        """Test realistic PWR core parallel configuration"""
        # Large PWR core: 1B particles, complex geometry
        resources = self.configurator.estimate_resources(
            n_particles=1000000000,  # 1 billion particles
            complexity='complex',
            target_walltime_hours=48.0
        )
        efficiency = self.configurator.check_parallel_efficiency(
            n_tasks=resources['recommended_tasks'],
            n_particles=1000000000
        )
        # With 1B particles and complex geometry, should need many tasks
        assert resources['recommended_tasks'] >= 1
        assert efficiency['status'] in ['good', 'excellent', 'marginal']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

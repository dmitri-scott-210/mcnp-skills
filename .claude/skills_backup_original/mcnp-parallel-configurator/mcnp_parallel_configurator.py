"""
MCNP Parallel Configurator (Skill 26) - MPI/OpenMP parallel execution setup

Based on MCNP6 Parallel Execution:
- TASKS card: Specifies number of MPI tasks
- MPI parallelization: Distributes particles across processes
- OpenMP threading: Thread-level parallelism (less efficient than MPI)
- Scaling efficiency: Best up to ~256 tasks, diminishing returns after
- Particles/task: Recommend >1000 particles per task for efficiency

Job Schedulers:
- SLURM: #SBATCH directives
- PBS/Torque: #PBS directives
- LSF: #BSUB directives

References:
- COMPLETE_MCNP6_KNOWLEDGE_BASE.md: ADVANCED OPERATIONS section
- MCNP6 User Manual Chapter 6: Execution Control
- LA-UR-20-20093: MCNP6.2 Parallel Performance
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from typing import Dict, Optional

class MCNPParallelConfigurator:
    """
    Configure MCNP for parallel execution

    Capabilities:
    - TASKS card generation
    - SLURM job script generation
    - PBS/Torque job script generation
    - LSF job script generation
    - Resource estimation
    - Scaling efficiency analysis
    """

    def __init__(self):
        pass

    def generate_tasks_card(self, n_tasks: int, stride: Optional[int] = None) -> str:
        """
        Generate TASKS card for MPI parallelization

        Args:
            n_tasks: Number of MPI tasks
            stride: Optional task stride (advanced usage)

        Returns:
            TASKS card string

        Format: TASKS n [stride]
        """
        card = f"tasks {n_tasks}"
        if stride:
            card += f" {stride}"
        return card

    def generate_slurm_script(self, job_name: str, nodes: int, tasks_per_node: int,
                             walltime: str, input_file: str,
                             partition: Optional[str] = None,
                             account: Optional[str] = None,
                             email: Optional[str] = None,
                             threads: int = 1) -> str:
        """
        Generate SLURM job script for parallel MCNP

        Args:
            job_name: Job name
            nodes: Number of compute nodes
            tasks_per_node: MPI tasks per node
            walltime: Wall clock limit (HH:MM:SS)
            input_file: MCNP input filename
            partition: SLURM partition (optional)
            account: Account/allocation (optional)
            email: Email for notifications (optional)
            threads: OpenMP threads per task (default 1, MPI-only)

        Returns:
            SLURM batch script string
        """
        total_tasks = nodes * tasks_per_node

        script = f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --nodes={nodes}
#SBATCH --ntasks-per-node={tasks_per_node}
#SBATCH --time={walltime}
#SBATCH --output=mcnp_%j.out
#SBATCH --error=mcnp_%j.err
"""

        if partition:
            script += f"#SBATCH --partition={partition}\n"
        if account:
            script += f"#SBATCH --account={account}\n"
        if email:
            script += f"#SBATCH --mail-type=END,FAIL\n"
            script += f"#SBATCH --mail-user={email}\n"

        script += f"""
# Set OpenMP threads (1 = MPI-only, recommended)
export OMP_NUM_THREADS={threads}

# Load modules (adjust for your system)
# module load mcnp/6.3
# module load intel-mpi

# Change to submission directory
cd $SLURM_SUBMIT_DIR

# Run MCNP with MPI
mpiexec -n {total_tasks} mcnp6 i={input_file} tasks {total_tasks}

# Alternative for Intel MPI:
# mpirun -n {total_tasks} mcnp6 i={input_file} tasks {total_tasks}
"""

        return script

    def generate_pbs_script(self, job_name: str, nodes: int, ppn: int,
                           walltime: str, input_file: str,
                           queue: Optional[str] = None,
                           email: Optional[str] = None) -> str:
        """
        Generate PBS/Torque job script

        Args:
            job_name: Job name
            nodes: Number of nodes
            ppn: Processors per node
            walltime: Wall clock limit (HH:MM:SS)
            input_file: MCNP input filename
            queue: Queue name (optional)
            email: Email for notifications (optional)

        Returns:
            PBS batch script string
        """
        total_tasks = nodes * ppn

        script = f"""#!/bin/bash
#PBS -N {job_name}
#PBS -l nodes={nodes}:ppn={ppn}
#PBS -l walltime={walltime}
#PBS -o mcnp_$PBS_JOBID.out
#PBS -e mcnp_$PBS_JOBID.err
"""

        if queue:
            script += f"#PBS -q {queue}\n"
        if email:
            script += f"#PBS -M {email}\n"
            script += f"#PBS -m abe\n"  # a=abort, b=begin, e=end

        script += f"""
# Change to submission directory
cd $PBS_O_WORKDIR

# Set OpenMP threads
export OMP_NUM_THREADS=1

# Run MCNP with MPI
mpiexec mcnp6 i={input_file} tasks {total_tasks}
"""

        return script

    def generate_lsf_script(self, job_name: str, n_tasks: int,
                           walltime_minutes: int, input_file: str,
                           queue: Optional[str] = None) -> str:
        """
        Generate LSF job script

        Args:
            job_name: Job name
            n_tasks: Total number of MPI tasks
            walltime_minutes: Wall clock limit in minutes
            input_file: MCNP input filename
            queue: Queue name (optional)

        Returns:
            LSF batch script string
        """
        script = f"""#!/bin/bash
#BSUB -J {job_name}
#BSUB -n {n_tasks}
#BSUB -W {walltime_minutes}
#BSUB -o mcnp_%J.out
#BSUB -e mcnp_%J.err
"""

        if queue:
            script += f"#BSUB -q {queue}\n"

        script += f"""
# Set OpenMP threads
export OMP_NUM_THREADS=1

# Run MCNP with MPI
mpiexec mcnp6 i={input_file} tasks {n_tasks}
"""

        return script

    def estimate_resources(self, n_particles: int, complexity: str,
                          target_walltime_hours: float = 24.0) -> Dict[str, any]:
        """
        Estimate computational resources for MCNP run

        Args:
            n_particles: Number of particles (NPS)
            complexity: Problem complexity ('simple', 'medium', 'complex', 'very_complex')
            target_walltime_hours: Desired walltime in hours

        Returns:
            Dict with resource recommendations
        """
        # Estimate time per particle (seconds) based on complexity
        time_per_particle = {
            'simple': 0.0001,      # Basic geometry, few tallies
            'medium': 0.001,       # Moderate geometry, several tallies
            'complex': 0.01,       # Complex geometry, many tallies, variance reduction
            'very_complex': 0.1    # Extremely complex, burnup, etc.
        }[complexity]

        # Total serial time
        total_time_sec = n_particles * time_per_particle
        total_time_hours = total_time_sec / 3600.0

        # Calculate tasks needed for target walltime
        # Account for parallel efficiency (~90% at 128 tasks, ~70% at 256 tasks)
        tasks_needed_ideal = total_time_hours / target_walltime_hours

        # Apply efficiency factor
        if tasks_needed_ideal <= 16:
            efficiency = 0.95
            tasks_needed = int(tasks_needed_ideal / efficiency)
        elif tasks_needed_ideal <= 64:
            efficiency = 0.92
            tasks_needed = int(tasks_needed_ideal / efficiency)
        elif tasks_needed_ideal <= 128:
            efficiency = 0.90
            tasks_needed = int(tasks_needed_ideal / efficiency)
        elif tasks_needed_ideal <= 256:
            efficiency = 0.75
            tasks_needed = int(tasks_needed_ideal / efficiency)
        else:
            efficiency = 0.60
            tasks_needed = min(512, int(tasks_needed_ideal / efficiency))

        # Particles per task (recommend >1000 for good statistics)
        particles_per_task = n_particles / tasks_needed

        # Node recommendations (assuming 32-64 cores per node)
        cores_per_node = 32  # Typical
        nodes_needed = (tasks_needed + cores_per_node - 1) // cores_per_node

        return {
            'total_serial_hours': total_time_hours,
            'target_walltime_hours': target_walltime_hours,
            'recommended_tasks': tasks_needed,
            'recommended_nodes': nodes_needed,
            'tasks_per_node': min(tasks_needed, cores_per_node),
            'particles_per_task': int(particles_per_task),
            'estimated_efficiency': efficiency,
            'complexity': complexity,
            'warning': 'Particles per task < 1000 - consider fewer tasks' if particles_per_task < 1000 else None,
            'recommendation': f"Use {tasks_needed} tasks on {nodes_needed} nodes for ~{target_walltime_hours:.1f}h runtime"
        }

    def check_parallel_efficiency(self, n_tasks: int, n_particles: int) -> Dict[str, any]:
        """
        Check if parallelization is efficient

        Args:
            n_tasks: Number of MPI tasks
            n_particles: Number of particles

        Returns:
            Dict with efficiency assessment
        """
        particles_per_task = n_particles / n_tasks

        if particles_per_task < 100:
            status = 'poor'
            recommendation = f"Only {int(particles_per_task)} particles/task - drastically reduce tasks or increase NPS"
        elif particles_per_task < 1000:
            status = 'marginal'
            recommendation = f"{int(particles_per_task)} particles/task - consider reducing tasks for better efficiency"
        elif particles_per_task < 10000:
            status = 'good'
            recommendation = f"{int(particles_per_task)} particles/task - good balance"
        else:
            status = 'excellent'
            recommendation = f"{int(particles_per_task)} particles/task - could potentially use more tasks"

        return {
            'particles_per_task': int(particles_per_task),
            'status': status,
            'recommendation': recommendation
        }

    def generate_cards(self) -> str:
        """Placeholder for consistency with other skills"""
        return "c Parallel execution configured via job script"

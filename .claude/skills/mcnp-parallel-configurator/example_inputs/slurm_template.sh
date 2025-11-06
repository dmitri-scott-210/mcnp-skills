#!/bin/bash
#SBATCH --job-name=JOBNAME
#SBATCH --nodes=NODES
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=CPUS
#SBATCH --time=HOURS:00:00
#SBATCH --partition=normal
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

# Load MCNP module
module load mcnp6

# Set OpenMP threads
export OMP_NUM_THREADS=CPUS

# Run MCNP
mpirun -np NODES mcnp6 inp=INPUTFILE

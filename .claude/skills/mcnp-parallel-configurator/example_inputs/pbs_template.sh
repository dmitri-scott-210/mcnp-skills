#!/bin/bash
#PBS -N JOBNAME
#PBS -l nodes=NODES:ppn=CPUS
#PBS -l walltime=HOURS:00:00
#PBS -j oe
#PBS -o ${PBS_JOBNAME}_${PBS_JOBID}.out

# Change to working directory
cd $PBS_O_WORKDIR

# Load MCNP module
module load mcnp6

# Set OpenMP threads
export OMP_NUM_THREADS=CPUS

# Run MCNP
mpirun -np NODES mcnp6 inp=INPUTFILE

# HPC Job Submission Guide

## SLURM Scheduler

### Basic Hybrid Job
```bash
#!/bin/bash
#SBATCH --job-name=mcnp_job
#SBATCH --nodes=20
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --time=48:00:00
#SBATCH --partition=normal

module load mcnp6
export OMP_NUM_THREADS=16
mpirun -np 20 mcnp6 inp=input.i
```

### With Array Jobs
```bash
#!/bin/bash
#SBATCH --array=1-10
#SBATCH --nodes=5
#SBATCH --time=24:00:00

export OMP_NUM_THREADS=16
mpirun -np 5 mcnp6 inp=input_${SLURM_ARRAY_TASK_ID}.i
```

## PBS Scheduler

### Basic Job
```bash
#!/bin/bash
#PBS -N mcnp_job
#PBS -l nodes=20:ppn=16
#PBS -l walltime=48:00:00

cd $PBS_O_WORKDIR
module load mcnp6
export OMP_NUM_THREADS=16
mpirun -np 20 mcnp6 inp=input.i
```

## LSF Scheduler

### Basic Job
```bash
#!/bin/bash
#BSUB -J mcnp_job
#BSUB -n 320
#BSUB -R "span[ptile=16]"
#BSUB -W 48:00

module load mcnp6
export OMP_NUM_THREADS=16
mpirun mcnp6 inp=input.i
```

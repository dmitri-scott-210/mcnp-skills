#!/usr/bin/env python3
"""
MCNP HPC Job Script Generator

Generate HPC job submission scripts for SLURM, PBS, and LSF schedulers.

Usage:
    python job_script_generator.py --scheduler slurm --nodes 20 --cpus 16 --hours 48
    python job_script_generator.py  # Interactive mode
"""

import sys
import argparse

SLURM_TEMPLATE = """#!/bin/bash
#SBATCH --job-name={jobname}
#SBATCH --nodes={nodes}
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task={cpus}
#SBATCH --time={hours}:00:00
#SBATCH --partition={partition}
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

# Load MCNP module
module load mcnp6

# Set OpenMP threads
export OMP_NUM_THREADS={cpus}

# Run MCNP
mpirun -np {nodes} mcnp6 inp={input_file}
"""

PBS_TEMPLATE = """#!/bin/bash
#PBS -N {jobname}
#PBS -l nodes={nodes}:ppn={cpus}
#PBS -l walltime={hours}:00:00
#PBS -j oe
#PBS -o ${{PBS_JOBNAME}}_${{PBS_JOBID}}.out

# Change to working directory
cd $PBS_O_WORKDIR

# Load MCNP module
module load mcnp6

# Set OpenMP threads
export OMP_NUM_THREADS={cpus}

# Run MCNP
mpirun -np {nodes} mcnp6 inp={input_file}
"""

LSF_TEMPLATE = """#!/bin/bash
#BSUB -J {jobname}
#BSUB -n {total_cores}
#BSUB -R "span[ptile={cpus}]"
#BSUB -W {hours}:00

# Load MCNP module
module load mcnp6

# Set OpenMP threads
export OMP_NUM_THREADS={cpus}

# Run MCNP
mpirun mcnp6 inp={input_file}
"""

def generate_script(scheduler, nodes, cpus, hours, jobname, input_file, partition='normal'):
    """Generate job script"""
    
    total_cores = nodes * cpus
    
    params = {
        'jobname': jobname,
        'nodes': nodes,
        'cpus': cpus,
        'hours': hours,
        'input_file': input_file,
        'partition': partition,
        'total_cores': total_cores
    }
    
    if scheduler == 'slurm':
        return SLURM_TEMPLATE.format(**params)
    elif scheduler == 'pbs':
        return PBS_TEMPLATE.format(**params)
    elif scheduler == 'lsf':
        return LSF_TEMPLATE.format(**params)
    else:
        raise ValueError(f"Unknown scheduler: {scheduler}")

def interactive_mode():
    """Interactive job script generation"""
    print("=" * 60)
    print("MCNP HPC Job Script Generator")
    print("=" * 60)
    
    scheduler = input("Scheduler (slurm/pbs/lsf): ").strip().lower()
    if scheduler not in ['slurm', 'pbs', 'lsf']:
        print(f"ERROR: Unknown scheduler '{scheduler}'")
        return
    
    try:
        nodes = int(input("Number of nodes: ").strip())
        cpus = int(input("CPUs per node: ").strip())
        hours = int(input("Wall time (hours): ").strip())
    except ValueError as e:
        print(f"ERROR: Invalid number: {e}")
        return
    
    jobname = input("Job name [mcnp_job]: ").strip() or "mcnp_job"
    input_file = input("MCNP input file [input.i]: ").strip() or "input.i"
    
    if scheduler == 'slurm':
        partition = input("Partition [normal]: ").strip() or "normal"
    else:
        partition = 'normal'
    
    output_file = input(f"Output script [submit_{scheduler}.sh]: ").strip() or f"submit_{scheduler}.sh"
    
    script = generate_script(scheduler, nodes, cpus, hours, jobname, input_file, partition)
    
    with open(output_file, 'w') as f:
        f.write(script)
    
    print(f"\n✓ Created {output_file}")
    print(f"  Scheduler: {scheduler}")
    print(f"  Resources: {nodes} nodes × {cpus} CPUs = {nodes * cpus} cores")
    print(f"  Wall time: {hours} hours")
    print(f"\nSubmit with: {'sbatch' if scheduler == 'slurm' else 'qsub' if scheduler == 'pbs' else 'bsub'} {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description='Generate HPC job submission scripts for MCNP',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--scheduler', choices=['slurm', 'pbs', 'lsf'], help='Job scheduler')
    parser.add_argument('--nodes', type=int, help='Number of nodes')
    parser.add_argument('--cpus', type=int, help='CPUs per node')
    parser.add_argument('--hours', type=int, help='Wall time (hours)')
    parser.add_argument('--jobname', default='mcnp_job', help='Job name')
    parser.add_argument('--input', dest='input_file', default='input.i', help='MCNP input file')
    parser.add_argument('--partition', default='normal', help='SLURM partition')
    parser.add_argument('--output', help='Output script file')
    
    args = parser.parse_args()
    
    if not all([args.scheduler, args.nodes, args.cpus, args.hours]):
        interactive_mode()
    else:
        output = args.output or f"submit_{args.scheduler}.sh"
        script = generate_script(args.scheduler, args.nodes, args.cpus, args.hours, 
                                args.jobname, args.input_file, args.partition)
        
        with open(output, 'w') as f:
            f.write(script)
        
        print(f"Created {output}")

if __name__ == '__main__':
    main()

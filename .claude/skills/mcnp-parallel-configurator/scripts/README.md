# MCNP Parallel Configurator - Python Tools

## Tools Overview

This directory contains two Python tools for configuring parallel MCNP jobs:

1. **job_script_generator.py** - Generate HPC submission scripts
2. **checkpoint_calculator.py** - Calculate optimal checkpoint intervals

## Requirements

- Python 3.6+
- No external dependencies (pure stdlib)

## 1. job_script_generator.py

Generate HPC job submission scripts for SLURM, PBS, and LSF schedulers.

### Usage

**Interactive Mode**:
```bash
python job_script_generator.py
# Prompts for: scheduler, nodes, CPUs, hours, job name, input file
```

**Command-Line Mode**:
```bash
# Generate SLURM script
python job_script_generator.py --scheduler slurm --nodes 20 --cpus 16 --hours 48

# Generate PBS script
python job_script_generator.py --scheduler pbs --nodes 10 --cpus 16 --hours 24

# Custom output file
python job_script_generator.py --scheduler slurm --nodes 50 --cpus 16 --hours 72 --output my_job.sh
```

### Output

Creates a complete job submission script with:
- Scheduler directives
- Module loading
- OpenMP configuration
- MPI execution command

**Example** (SLURM):
```bash
#!/bin/bash
#SBATCH --job-name=mcnp_job
#SBATCH --nodes=20
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --time=48:00:00

module load mcnp6
export OMP_NUM_THREADS=16
mpirun -np 20 mcnp6 inp=input.i
```

## 2. checkpoint_calculator.py

Calculate optimal PRDMP interval based on run time and checkpoint overhead.

### Usage

**Interactive Mode**:
```bash
python checkpoint_calculator.py
# Prompts for: run time, dump overhead, MTBF
```

**Command-Line Mode**:
```bash
# Calculate for 48-hour run
python checkpoint_calculator.py --runtime 48

# With custom dump overhead
python checkpoint_calculator.py --runtime 72 --dump-overhead 180
```

### Algorithm

Uses the formula:
```
optimal_interval = sqrt(2 × checkpoint_overhead × MTBF)
```

Where:
- checkpoint_overhead = Time to write dump (default: 120 seconds)
- MTBF = Mean time between failures (default: 100 hours)

### Output

```
Optimal interval: 155.3 minutes
Recommended: 180 minutes
PRDMP card: PRDMP  180

Expected dumps: 16.0
Suggested CTME: 2850 (leaves 30-min buffer)
```

## Workflow Examples

### Workflow 1: New HPC Job

```bash
# Step 1: Generate job script
python job_script_generator.py --scheduler slurm --nodes 20 --cpus 16 --hours 48
# Creates: submit_slurm.sh

# Step 2: Calculate checkpoint interval
python checkpoint_calculator.py --runtime 48
# Recommends: PRDMP 180

# Step 3: Add to MCNP input
echo "PRDMP  180  J  0  1  1  1  0" >> input.i
echo "NPS  500000000" >> input.i
echo "CTME  2850" >> input.i

# Step 4: Submit job
sbatch submit_slurm.sh
```

### Workflow 2: Optimize Existing Run

```bash
# Calculate optimal interval for 72-hour run with slow I/O
python checkpoint_calculator.py --runtime 72 --dump-overhead 300

# Generates recommendation
# Recommends: PRDMP 240 (4 hours)
```

## Quick Reference

| Run Duration | Recommended Interval | PRDMP Card |
|--------------|---------------------|------------|
| < 4 hours | Optional | - |
| 4-12 hours | 60-90 minutes | `PRDMP 60` or `PRDMP 90` |
| 12-48 hours | 120-180 minutes | `PRDMP 120` or `PRDMP 180` |
| > 48 hours | 180-240 minutes | `PRDMP 180` or `PRDMP 240` |

## Integration

These tools are designed to work together:

1. Use **checkpoint_calculator.py** to determine PRDMP interval
2. Use **job_script_generator.py** to create submission script
3. Add PRDMP card to MCNP input file
4. Submit job

---

**See also**: `../SKILL.md`, `../parallel_execution.md`, `../checkpoint_restart.md`

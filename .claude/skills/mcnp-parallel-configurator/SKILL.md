---
category: E
name: mcnp-parallel-configurator
description: Configure parallel execution, checkpointing, restart, and distributed computing using PRDMP/TASKS/DBCN cards for efficient large-scale simulations
version: 2.0.0
activation_keywords:
  - parallel
  - PRDMP
  - TASKS
  - MPI
  - checkpoint
  - restart
  - distributed
  - problem dump
  - RUNTPE
  - DBCN
---

# MCNP Parallel Configurator Skill

## Purpose

Configure parallel execution (MPI/OpenMP), checkpointing, restart capabilities, and distributed computing for MCNP6 to efficiently run large-scale simulations and enable recovery from interruptions.

## When to Use This Skill

- Setting up parallel execution on HPC clusters (MPI + OpenMP hybrid)
- Implementing checkpointing for long-running simulations (PRDMP card)
- Configuring restart capability after crashes or time limits
- Optimizing load balancing for complex geometries (TASKS card)
- Debugging distributed runs (DBCN card)
- Generating HPC job submission scripts (SLURM, PBS, LSF)

## Prerequisites

- **mcnp-input-builder**: Basic input file structure
- **mcnp-mesh-builder**: Parallel mesh tallies
- **mcnp-statistics-checker**: Restart decisions
- Understanding of HPC cluster architecture (nodes, cores, MPI, OpenMP)
- Familiarity with job schedulers (SLURM, PBS, LSF)

## Core Concepts - Quick Reference

### Parallel Execution Models

| Model | Mechanism | Use Case | Command |
|-------|-----------|----------|---------|
| **OpenMP** | Shared memory (threads) | Single node | `export OMP_NUM_THREADS=16` |
| **MPI** | Distributed memory (processes) | Multi-node cluster | `mpirun -np 20 mcnp6` |
| **Hybrid** | MPI + OpenMP | Large HPC jobs | Both commands |

**Best Practice**: Hybrid (1-2 MPI tasks/node × many threads/task)

**Detailed Reference**: See `parallel_execution.md` for architecture guide.

### PRDMP Card (Checkpointing)

**Basic Syntax**:
```
PRDMP  nd1  nd2  ndm  mct  kcod  notek  prdmtsk
```

**Common Configurations**:
```
PRDMP  60            $ Dump every 60 minutes
PRDMP  60  J  0  1   $ Hourly dumps, mctal at dumps
PRDMP  120 J  0  1  1  1  0   $ 2-hour dumps, master task only (MPI)
```

**Output Files**:
- `runtpe` - Restart file (binary)
- `mctal` - Tally results (machine-readable)
- `srctp` - Source distribution (KCODE only)

**Detailed Reference**: See `checkpoint_restart.md` for complete guide.

### Restart Methods

| Method | Command | When to Use |
|--------|---------|-------------|
| CONTINUE | `mcnp6 inp=input.i continue` | Resume from last dump |
| RUNTPE | `mcnp6 inp=input.i runtpe=runtpe.5` | Restart from specific dump |
| Source File | KCODE with SRCTP | Skip source convergence |

**Detailed Reference**: See `checkpoint_restart.md` sections 4-6.

### TASKS Card (Load Balancing)

```
TASKS  mode  nps_task  rngseed

Modes:
  0 = Automatic (default)
  1 = Static (fixed particles/task)
  2 = Dynamic (load balancing)
```

**Recommendation**: Use `TASKS 2` for complex geometries with load imbalance.

## Python Tools

This skill includes two practical tools for HPC job configuration:

### 1. checkpoint_calculator.py - Optimize Dump Intervals
```bash
# Calculate optimal checkpoint interval
python checkpoint_calculator.py --runtime 48 --dump-overhead 120

# Analyze existing run
python checkpoint_calculator.py --analyze outp

# Interactive mode
python checkpoint_calculator.py
```

### 2. job_script_generator.py - Generate Submission Scripts
```bash
# Generate SLURM script
python job_script_generator.py --scheduler slurm --nodes 20 --hours 48

# Generate PBS script
python job_script_generator.py --scheduler pbs --nodes 10 --cpus 16

# Interactive mode
python job_script_generator.py
```

**Detailed Documentation**: See `scripts/README.md` for complete usage guide.

## Decision Tree: Parallel Configuration

```
START: Configure parallel execution
  |
  +--> What is your computing environment?
  |      ├─> Single workstation (1-64 cores)
  |      │   └─> Use OpenMP only
  |      │       - export OMP_NUM_THREADS=<cores>
  |      │       - No TASKS card needed
  |      │
  |      ├─> Small cluster (2-10 nodes)
  |      │   └─> Use MPI
  |      │       - mpirun -np <nodes> mcnp6
  |      │       - PRDMP with prdmtsk=0
  |      │
  |      └─> Large HPC (>10 nodes)
  |          └─> Use Hybrid (MPI + OpenMP)
  |              - mpirun -np <nodes> + OMP_NUM_THREADS
  |              - TASKS 2 (dynamic load balancing)
  |
  +--> Do you need checkpointing?
  |      ├─> Short run (<4 hours): Optional
  |      ├─> Medium run (4-24 hours): Recommended (PRDMP 60-120)
  |      └─> Long run (>24 hours): Required (PRDMP 60-180)
  |
  +--> Is geometry homogeneous?
  |      ├─> Yes (uniform): TASKS 0 (automatic)
  |      └─> No (complex): TASKS 2 (dynamic)
  |
  └─> Generate job script
         └─> Use job_script_generator.py
```

## Use Cases

### Use Case 1: Basic Checkpointing (Workstation)

**Objective**: Run 12-hour job on single node with hourly checkpoints

**MCNP Input**:
```
c --- Problem setup ---
...

c --- Checkpointing ---
PRDMP  60  J  0  1   $ Dump every 60 min, mctal at dumps

NPS  10000000
CTME  720   $ 12 hours (leave buffer for final dump)
```

**Command**:
```bash
export OMP_NUM_THREADS=16
mcnp6 inp=input.i
```

**To Restart**:
```bash
mcnp6 inp=input.i continue
```

### Use Case 2: MPI Cluster (20 Nodes)

**Objective**: Run on 20 nodes with checkpointing and restart capability

**Job Script** (SLURM):
```bash
#!/bin/bash
#SBATCH --nodes=20
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --time=48:00:00

module load mcnp6

export OMP_NUM_THREADS=16

mpirun -np 20 mcnp6 inp=input.i
```

**MCNP Input**:
```
PRDMP  120  J  0  1  1  1  0   $ 2-hour dumps, master only (prdmtsk=0)
TASKS  2   $ Dynamic load balancing

NPS  500000000
CTME  2850   $ 47.5 hours (buffer for final dump)
```

**To Restart** (resubmit with):
```bash
mpirun -np 20 mcnp6 inp=input.i continue
```

### Use Case 3: Criticality with Source Restart

**Objective**: KCODE run with source file for faster restart

**Initial Run**:
```
KCODE  10000  1.0  50  250   $ Skip 50, run 250 cycles
PRDMP  60  J  0  1  1   $ Creates srctp file

NPS  J
CTME  360
```

**Restart Run** (skip source convergence):
```bash
mcnp6 inp=input.i continue   $ Automatically reads srctp
```

**Or explicitly** (modify input):
```
KCODE  10000  1.0  0  300   $ Skip 0 (source converged), run 300 more
KSRC  SRCTP   $ Read source from srctp file
```

### Use Case 4: Generate Submission Script

**Using Python Tool**:
```bash
# Interactive mode
python job_script_generator.py

# Command-line
python job_script_generator.py \
  --scheduler slurm \
  --nodes 50 \
  --cpus 16 \
  --hours 48 \
  --input reactor.i \
  --output submit_reactor.sh
```

**Output** (`submit_reactor.sh`):
```bash
#!/bin/bash
#SBATCH --job-name=reactor
#SBATCH --nodes=50
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --time=48:00:00

module load mcnp6
export OMP_NUM_THREADS=16
mpirun -np 50 mcnp6 inp=reactor.i
```

## Common Configurations - Quick Reference

### PRDMP Configurations

| Scenario | Configuration | Explanation |
|----------|---------------|-------------|
| Hourly checkpoint | `PRDMP 60` | Dump every 60 minutes |
| 2-hour checkpoint | `PRDMP 120 J 0 1` | Every 120 min, mctal at dumps |
| MPI cluster | `PRDMP 120 J 0 1 1 1 0` | 2-hour, master only (prdmtsk=0) |
| Debugging | `PRDMP 10 J 10 1 1 2` | 10-min dumps, max 10, verbose |
| mctal at end only | `PRDMP 60 J 0 2` | Hourly runtpe, mctal at end |

**Complete Reference**: See `example_inputs/example_prdmp_configs.txt`

### Performance Optimization

**Optimal Thread Count**:
- Use physical cores (not hyperthreads)
- Example: 16-core node → `OMP_NUM_THREADS=16`

**Optimal MPI Task Count**:
- 1-2 tasks/node (rest use OpenMP)
- More tasks → better load balance, more communication
- Fewer tasks → less overhead, more memory/task

**Example** (20 nodes, 16 cores each):
```bash
# Option A: 20 MPI × 16 threads = 320 cores
export OMP_NUM_THREADS=16
mpirun -np 20 mcnp6 inp=input.i

# Option B: 40 MPI × 8 threads = 320 cores (better load balance)
export OMP_NUM_THREADS=8
mpirun -np 40 mcnp6 inp=input.i
```

**Guideline**: Test both, measure speedup.

## Troubleshooting

### Problem: Restart fails ("runtpe incompatible")
**Cause**: Input file changed between runs
**Fix**: Only modify NPS/CTME for restarts; don't change geometry/materials

### Problem: Poor MPI scaling
**Cause**: Communication overhead or load imbalance
**Fix**:
```
TASKS 2   $ Dynamic load balancing
PRDMP 180   $ Reduce dump frequency (3 hours)
```
Reduce MPI tasks, increase OpenMP threads

### Problem: Out of memory on MPI tasks
**Cause**: Each task replicates geometry/cross sections
**Fix**: Fewer tasks/node, more memory/task
```bash
# Before: 16 tasks/node → After: 1 task/node
export OMP_NUM_THREADS=16
mpirun -np 10 mcnp6 inp=input.i  # Instead of -np 160
```

### Problem: Dumps not created
**Cause**: Insufficient time or disk full
**Fix**: Increase CTME buffer, check disk space
```
CTME 2850   $ Leave 2.5-hour buffer for 48-hour job
```

## Integration with Other Skills

- **mcnp-statistics-checker**: Check convergence before restarting
- **mcnp-mesh-builder**: Parallel mesh tallies (`MSHMF=rma_batch`)
- **mcnp-input-validator**: Validate PRDMP/TASKS syntax

## Validation Checklist

- [ ] PRDMP card configured with appropriate dump frequency
- [ ] CTME set with 2-5% buffer (48h job → CTME 2850 min)
- [ ] For MPI: prdmtsk=0 (master only dumps)
- [ ] For complex geometry: TASKS 2 (dynamic load balancing)
- [ ] Tested restart procedure before production run
- [ ] Job script matches cluster requirements (nodes, time limit)
- [ ] OMP_NUM_THREADS set to physical cores (not hyperthreads)
- [ ] MPI task count optimized (1-2 tasks/node recommended)
- [ ] Sufficient disk space for runtpe files
- [ ] CTME less than wall time limit (ensure final dump completes)

## Best Practices

1. **Always use PRDMP** - Hardware fails, even on reliable clusters
2. **Dump frequency**: 1-2 hours for long runs (balance safety vs I/O)
3. **Master-only dumps**: `prdmtsk=0` for MPI (reduces I/O contention)
4. **CTME buffer**: Set 2-5% less than wall time (ensure final dump)
5. **Test restart**: Practice before production runs
6. **Hybrid parallelism**: 1-2 MPI tasks/node, rest OpenMP
7. **Dynamic load balancing**: `TASKS 2` for complex geometries
8. **No modifications**: Don't change geometry/materials between restarts
9. **Archive critical dumps**: Keep runtpe files for important runs
10. **Monitor scaling**: Measure speedup vs cores (diminishing returns)

## Resources and References

### Reference Files (Detailed Guides)
- `parallel_execution.md` - MPI vs OpenMP, hybrid models, architecture guide
- `checkpoint_restart.md` - Complete PRDMP reference, restart procedures
- `hpc_job_submission.md` - Cluster-specific submission scripts and best practices

### Python Tools
- `scripts/checkpoint_calculator.py` - Calculate optimal dump intervals
- `scripts/job_script_generator.py` - Generate HPC submission scripts
- `scripts/README.md` - Complete tool documentation

### Example Data
- `example_inputs/example_prdmp_configs.txt` - Common PRDMP configurations
- `example_inputs/slurm_template.sh` - SLURM submission template
- `example_inputs/pbs_template.sh` - PBS submission template
- `example_inputs/scaling_benchmarks.csv` - Parallel scaling data

### Related MCNP Skills
- **mcnp-input-builder**: Basic input structure
- **mcnp-mesh-builder**: Parallel mesh tallies
- **mcnp-statistics-checker**: Convergence checking for restart decisions

### External Resources
- **MCNP Manual**: Chapter 3.6 (PRDMP), 3.23 (TASKS), 3.1 (DBCN)
- **Getting Started Manual**: Parallel execution guide
- **HPC Center Documentation**: Cluster-specific best practices

---

**Version**: 2.0.0
**Last Updated**: 2025-11-06
**Status**: Production-ready with HPC job generation tools

---

**End of MCNP Parallel Configurator Skill**

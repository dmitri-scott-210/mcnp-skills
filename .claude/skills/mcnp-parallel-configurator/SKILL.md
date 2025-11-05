---
category: E
name: mcnp-parallel-configurator
description: Configure parallel execution, checkpointing, restart, and distributed computing using PRDMP/TASKS/DBCN cards for efficient large-scale simulations
version: 1.0.0
auto_activate: true
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
  - RNDK SRC
  - DBCN
dependencies:
  - mcnp-input-builder
related_skills:
  - mcnp-mesh-builder
  - mcnp-statistics-checker
output_formats:
  - MCNP input cards (PRDMP/TASKS/DBCN)
  - Parallel execution guidance
  - Restart instructions
---

# mcnp-parallel-configurator

**Purpose**: Configure parallel execution, checkpointing, restart capabilities, and distributed computing for MCNP6 to efficiently run large-scale simulations across multiple processors and enable recovery from interruptions.

## Core Concepts

### Parallel Execution in MCNP6

MCNP6 supports two levels of parallelism:

**1. Shared memory (OpenMP)**:
- Multiple threads on single node
- Set with environment variable: `OMP_NUM_THREADS=<n>`
- Typical: 8-64 threads
- **Use case**: Single workstation

**2. Distributed memory (MPI)**:
- Multiple processes across nodes
- Set with MPI launcher: `mpirun -np <n> mcnp6`
- Typical: 10-1000 processes
- **Use case**: HPC clusters

**Hybrid (OpenMP + MPI)**:
- MPI across nodes, OpenMP within nodes
- Example: 10 nodes × 8 threads = 80 total cores
- **Use case**: Large HPC jobs

### Problem Dumps (PRDMP Card)

**Purpose**: Periodically save simulation state to disk for:
- **Restart** after crash/interruption
- **Checkpointing** for long runs
- **Debugging** problem setup

**Output files**:
- `runtpe` = Binary restart file (primary)
- `srctp` = Source file (criticality only)
- `mctal` = Tally file (machine-readable)
- `ptrac` = Particle track file (if PTRAC card present)

## PRDMP Card Syntax

```
PRDMP  nd1  nd2  ndm  mct  kcod  notek  prdmtsk  <options>
```

**Parameters** (all optional):

- **nd1** (default: -1): Dump frequency in minutes
  - Positive: Dump every `nd1` minutes
  - Negative: Dump every `-nd1` minutes AND at end
  - `0`: No time-based dumps
  - `J`: Skip (use default)

- **nd2** (default: 0): NPS intervals between dumps
  - `0`: No NPS-based dumps
  - `n`: Dump every `n` particles

- **ndm** (default: 0): Maximum number of dumps
  - `0`: Unlimited dumps
  - `n`: Stop after `n` dumps

- **mct** (default: 1): MCT AL file creation
  - `0`: No mctal file
  - `1`: Create mctal at dumps
  - `2`: Create mctal only at end
  - `3`: Create mctal at dumps and end

- **kcod** (default: 1): Kcode dumps (criticality only)
  - `0`: No kcode dumps
  - `1`: Dump kcode at intervals
  - `2`: Dump only at end

- **notek** (default: 1): Screen output control
  - `0`: Minimal screen output
  - `1`: Normal screen output
  - `2`: Verbose screen output

- **prdmtsk** (default: -1): Task-level dumps (MPI)
  - `-1`: Each task dumps separately
  - `0`: Master task only dumps
  - `1`: All tasks dump (large files!)

## Decision Tree: Parallel Configuration

```
START: What is your computing environment?
│
├─→ Single workstation (1-64 cores)
│   └─→ Use OpenMP (shared memory)
│       - Set OMP_NUM_THREADS=<cores>
│       - No TASKS card needed
│       - PRDMP for checkpointing
│
├─→ Small cluster (2-10 nodes, 100-500 cores)
│   └─→ Use MPI (distributed memory)
│       - mpirun -np <tasks> mcnp6
│       - Optional: TASKS card for load balancing
│       - PRDMP with prdmtsk=0 (master only)
│
├─→ Large HPC cluster (>10 nodes, >500 cores)
│   └─→ Use Hybrid (MPI + OpenMP)
│       - mpirun -np <nodes> mcnp6
│       - OMP_NUM_THREADS=<cores_per_node>
│       - TASKS card for MPI decomposition
│       - PRDMP with prdmtsk=0
│
└─→ Need restart capability (long runs, unstable systems)
    └─→ Use PRDMP with frequent dumps
        - nd1=60 (dump every 60 minutes)
        - Restart with CONTINUE keyword
```

## Common Use Cases

### Use Case 1: Basic Checkpointing (Single Node)

**Problem**: Run for 12 hours, dump every hour for safety.

```
c ============================================================
c Basic Checkpointing (12-hour run, hourly dumps)
c ============================================================

c --- Geometry, materials, source (standard setup) ---
...

c --- Tally ---
F4:N  1

c --- Problem dump (hourly checkpoints) ---
PRDMP  60  J  0  1  1  1  0   $ Dump every 60 min, mctal at dumps, master only

c --- Run for 12 hours worth of particles ---
NPS  10000000
CTME  720   $ Computer time limit: 720 minutes (12 hours)
```

**Files created**:
- `runtpe` (every 60 minutes): Restart file
- `mctal` (every 60 minutes): Tally results
- `outp` (at end): Main output

**To restart** (if interrupted):
```bash
mcnp6 inp=input.i continue
```

### Use Case 2: Frequent Dumps for Debugging

**Problem**: New problem, want frequent dumps to diagnose issues.

```
PRDMP  10  J  10  1  1  2  0   $ Dump every 10 min, max 10 dumps, verbose output
DBCN  J  J  J  2   $ Debug: check all (cells, surfaces, sources), level 2
```

**Output**: Up to 10 dumps (runtpe.1, runtpe.2, ..., runtpe.10), verbose diagnostics.

### Use Case 3: MPI Parallel on Cluster

**Problem**: Run on 20 MPI tasks (20 nodes × 1 process each).

```bash
# Submit script (SLURM example)
#!/bin/bash
#SBATCH --nodes=20
#SBATCH --ntasks-per-node=1
#SBATCH --time=24:00:00

module load mcnp6

mpirun -np 20 mcnp6 inp=input.i
```

**Input file**:
```
c --- Parallel configuration ---
PRDMP  60  J  0  1  1  1  0   $ Master task only dumps (prdmtsk=0)

c --- Run parameters ---
NPS  100000000   $ Large NPS (distributed across 20 tasks)
CTME  1440       $ 24-hour time limit
```

**Performance**: Each task runs ~5M particles (100M / 20).

### Use Case 4: Hybrid MPI+OpenMP

**Problem**: Run on 10 nodes, 16 cores each (10 MPI tasks × 16 threads = 160 cores).

```bash
#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --time=48:00:00

module load mcnp6

export OMP_NUM_THREADS=16

mpirun -np 10 mcnp6 inp=input.i
```

**Input file**:
```
PRDMP  120  J  0  1  1  1  0   $ Dump every 2 hours

NPS  500000000   $ 500M particles (10 tasks × 50M each × 16 threads)
CTME  2880       $ 48-hour time limit
```

**Speedup**: ~160× (if perfect scaling).

### Use Case 5: Criticality with KCODE

**Problem**: KCODE criticality with checkpointing and source file.

```
c --- Criticality problem ---
KCODE  10000  1.0  50  250   $ 10K/cycle, skip 50, run 250

c --- Problem dump (save source) ---
PRDMP  60  J  0  1  1  1  0   $ kcod=1 → dump kcode source

c --- Run ---
NPS  J   $ Not used (KCODE controls)
CTME  360   $ 6-hour time limit
```

**Output files**:
- `runtpe` (restart file with kcode state)
- `srctp` (source distribution)
- `mctal` (keff and tally results)

**To restart**:
```bash
mcnp6 inp=input.i continue
```

MCNP resumes from last complete kcode cycle.

## TASKS Card (MPI Task Decomposition)

**Purpose**: Control how work is distributed across MPI tasks.

### TASKS Syntax

```
TASKS  <mode>  <nps_task>  <rngseed>
```

**Parameters**:

- **mode** (default: 0): Decomposition mode
  - `0`: Automatic (MCNP decides)
  - `1`: Static (each task runs nps_task particles)
  - `2`: Dynamic (load balancing)

- **nps_task**: Particles per task (mode=1 only)

- **rngseed**: Random number seed control
  - `0`: Each task uses different seed (default)
  - `1`: All tasks use same seed (for reproducibility testing)

### Example: Static Decomposition

**Problem**: Run exactly 1M particles per task on 50 tasks.

```
TASKS  1  1000000  0   $ Static: 1M per task, different seeds

NPS  50000000   $ Total: 50M particles (50 tasks × 1M each)
```

**Use case**: Testing, benchmarking.

### Example: Dynamic Load Balancing

**Problem**: Inhomogeneous geometry (some particles fast, some slow).

```
TASKS  2  J  0   $ Dynamic load balancing

NPS  100000000   $ MCNP distributes work dynamically
```

**Effect**: Tasks with fast particles get more work; tasks with slow particles get less. Overall better load balance.

**Use case**: Complex geometries, deep penetration, variance reduction.

## Restart Methods

### Method 1: CONTINUE Keyword

**Purpose**: Resume from last dump.

```bash
mcnp6 inp=input.i continue
```

**Requirements**:
- `runtpe` file exists
- Input file unchanged (or only NPS/CTME increased)

**Effect**: MCNP resumes from last dump, accumulates additional statistics.

**Example workflow**:
```bash
# Initial run (6 hours)
mcnp6 inp=input.i   # Creates runtpe after 6 hours

# Continue run (6 more hours)
mcnp6 inp=input.i continue   # Resumes from runtpe, runs 6 more hours

# Total: 12 hours of statistics
```

### Method 2: RUNTPE Keyword

**Purpose**: Read specific runtpe file (not default).

```bash
mcnp6 inp=input.i runtpe=runtpe_old
```

**Use case**: Restart from archived dump file.

### Method 3: RNDSRC/SRCTP (Criticality Source)

**Purpose**: Restart KCODE with source distribution from previous run.

**Initial run**:
```
KCODE  10000  1.0  50  250
PRDMP  60  J  0  1  1   $ Creates srctp file
```

**Restart run**:
```bash
mcnp6 inp=input.i continue   # Automatically reads srctp if present
```

or explicitly:
```
KCODE  10000  1.0  0  300   $ Skip 0 cycles (source already converged)
KSRC  SRCTP   $ Read source from srctp file
```

**Effect**: Skip initial source convergence (saves time for large problems).

## Debugging and Diagnostics (DBCN Card)

**Purpose**: Enable detailed checks and debug output.

### DBCN Syntax

```
DBCN  cellchk  surfchk  srcchk  debug  <options>
```

**Parameters**:

- **cellchk** (default: 0): Cell definition checks
  - `0`: No checks
  - `1`: Check cells (lost particle detection)
  - `2`: Detailed cell checks

- **surfchk** (default: 0): Surface definition checks
  - `0`: No checks
  - `1`: Check surfaces
  - `2`: Detailed surface checks

- **srcchk** (default: 0): Source checks
  - `0`: No checks
  - `1`: Check source (sample points, verify in geometry)
  - `2`: Detailed source checks

- **debug** (default: 0): Debug output level
  - `0`: No debug output
  - `1`: Basic debug output
  - `2`: Detailed debug output (WARNING: large files!)

### Example: Validate New Geometry

```
DBCN  2  2  2  1   $ Check all (cells, surfaces, source), basic debug

PRDMP  J  J  1  J  J  2   $ 1 dump only, verbose output (notek=2)

NPS  1000   $ Short run for validation
```

**Output**: Detailed diagnostics on geometry, source, potential lost particle locations.

### Example: Diagnose Lost Particles

```
DBCN  2  J  J  1   $ Detailed cell checks, basic debug

PRDMP  J  J  1  J  J  2  J  $ Verbose output
```

**Output** (if lost particles occur):
```
lost particle in cell ... at position (x, y, z)
surface ... distance ...
```

**Fix**: Adjust geometry (fill gaps, check surface equations).

## Advanced Dump Control

### Selective Tally Output (MCT Card Parameter)

Control when `mctal` is written:

```
PRDMP  60  J  0  2   $ mct=2: mctal only at end (not at dumps)
```

**Use case**: Reduce I/O during run (dump runtpe frequently, mctal only at end).

### Dump File Naming

MCNP creates numbered dumps:
```
runtpe.1  (first dump)
runtpe.2  (second dump)
...
runtpe.n  (nth dump)
```

**Latest dump**: `runtpe` (symlink or copy of last dump)

**To restart from specific dump**:
```bash
mcnp6 inp=input.i runtpe=runtpe.5   # Restart from 5th dump
```

### Dump File Management

**Problem**: Many dumps consume disk space.

**Solution**: Periodic cleanup script:
```bash
#!/bin/bash
# Keep only last 3 dumps
ls -t runtpe.* | tail -n +4 | xargs rm -f
```

**Schedule**: Run hourly via cron during MCNP job.

## Performance Optimization

### Optimal Thread Count (OpenMP)

**Rule of thumb**: `OMP_NUM_THREADS` = physical cores (not hyperthreads).

**Example** (16-core node):
```bash
export OMP_NUM_THREADS=16   # Use 16 physical cores
mcnp6 inp=input.i
```

**Avoid**: Oversubscription (OMP_NUM_THREADS > physical cores) → context switching overhead.

### Optimal MPI Task Count

**Factors**:
- Memory per task (ensure sufficient RAM)
- Communication overhead (more tasks → more communication)
- Load balance (inhomogeneous geometry)

**Typical**: 1-2 MPI tasks per node (rest use OpenMP).

**Example** (20 nodes, 16 cores each):
```bash
# Option A: 20 MPI tasks × 16 threads = 320 cores
export OMP_NUM_THREADS=16
mpirun -np 20 mcnp6 inp=input.i

# Option B: 40 MPI tasks × 8 threads = 320 cores (better load balance)
export OMP_NUM_THREADS=8
mpirun -np 40 mcnp6 inp=input.i
```

**Guideline**: More MPI tasks improve load balance, but increase communication. Test both.

### Minimize Dump I/O

**Problem**: Frequent dumps slow down run (disk I/O bottleneck).

**Solution**: Dump less frequently, or dump to fast storage (SSD, RAM disk).

```
c Dump every 2 hours instead of every 30 minutes
PRDMP  120  J  0  1   $ 120 minutes
```

### Parallel Mesh Tallies (FMESH)

**Problem**: Large mesh tallies on distributed systems.

**Solution**: Use `rma_batch` algorithm (distributed memory).

```
FMESH14:N GEOM=XYZ ...
          MSHMF=rma_batch   $ Distributed mesh tally
```

**Effect**: Each task stores portion of mesh, reduces memory per task.

## Troubleshooting

### Problem: Restart fails ("runtpe file incompatible")

**Causes**:
1. Input file changed (geometry, materials, tallies)
2. MCNP version mismatch
3. Corrupted runtpe file

**Fix**:
- Don't modify input file for restart (only NPS/CTME)
- Use same MCNP version
- Try earlier dump: `runtpe=runtpe.1`

### Problem: MPI job doesn't scale (poor speedup)

**Causes**:
1. Too many MPI tasks (communication overhead)
2. Load imbalance (inhomogeneous geometry)
3. I/O bottleneck (dump files)

**Fix**:
```
c Reduce MPI tasks, increase threads
export OMP_NUM_THREADS=32
mpirun -np 10 mcnp6 inp=input.i   # Instead of -np 320

c Use dynamic load balancing
TASKS  2

c Reduce dump frequency
PRDMP  180   $ 3 hours instead of 1 hour
```

### Problem: Out of memory on MPI tasks

**Cause**: Each task replicates geometry/cross sections.

**Fix**: Reduce tasks per node.
```bash
# Before: 16 tasks/node
mpirun -np 160 mcnp6 inp=input.i   # 10 nodes × 16 = 160 tasks

# After: 1 task/node (more memory per task)
export OMP_NUM_THREADS=16
mpirun -np 10 mcnp6 inp=input.i   # 10 nodes × 1 task × 16 threads
```

### Problem: Lost particles after restart

**Cause**: Geometry changed between dumps.

**Fix**: Don't modify geometry for restarts. If unavoidable, start fresh run.

### Problem: Dumps not created

**Cause**: Insufficient time (CTME too short) or disk full.

**Fix**:
```
CTME  1440   $ Ensure sufficient time (24 hours)

c Check disk space before run
df -h /path/to/rundir
```

## Integration with Other Skills

### With mcnp-statistics-checker

Check convergence before continuing:
```python
from skills.output_analysis.mcnp_statistics_checker import StatisticsChecker

checker = StatisticsChecker('outp')

if checker.all_tests_passed():
    print("Statistics good, no need to continue")
else:
    print("Continue run: mcnp6 inp=input.i continue")
    # Increase NPS in input file, then restart
```

### With mcnp-mesh-builder

Parallel mesh tallies:
```
FMESH14:N GEOM=XYZ ...
          MSHMF=rma_batch   $ Distributed mesh (for MPI)

TASKS  2   $ Dynamic load balancing

PRDMP  120  J  0  1  J  J  0   $ Master dumps only (prdmtsk=0)
```

## Best Practices

1. **Always use PRDMP** - Even on reliable systems (hardware fails)
2. **Dump frequency**: 1-2 hours for long runs (balance safety vs I/O cost)
3. **Master-only dumps**: `prdmtsk=0` for MPI (reduces I/O contention)
4. **CTME buffer**: Set CTME 10% less than wall time (ensure final dump completes)
5. **Test restart**: Practice restart procedure before production runs
6. **Archive dumps**: Keep runtpe files for critical runs
7. **Hybrid parallelism**: 1-2 MPI tasks/node, rest OpenMP (best of both)
8. **Dynamic load balancing**: Use `TASKS 2` for complex geometries
9. **Minimize modifications**: Don't change input file between restarts
10. **Monitor performance**: Check speedup vs number of tasks (diminishing returns)

## Example: Production HPC Job

**Scenario**: Run on 50 nodes (16 cores each) for 48 hours, with restart capability.

```bash
#!/bin/bash
#SBATCH --job-name=mcnp_production
#SBATCH --nodes=50
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --time=48:00:00
#SBATCH --partition=normal

module load mcnp6

export OMP_NUM_THREADS=16

# Run with automatic restart
mpirun -np 50 mcnp6 inp=input.i

# If interrupted, resubmit with continue
# mpirun -np 50 mcnp6 inp=input.i continue
```

**Input file**:
```
c ============================================================
c Production Run: 50 Nodes × 16 Threads = 800 Cores
c ============================================================

c --- Geometry, materials, source ---
...

c --- Tallies ---
F4:N  1
F6:N  2

c --- Parallel configuration ---
PRDMP  120  J  0  1  1  1  0   $ Dump every 2 hours, master only
TASKS  2   $ Dynamic load balancing

c --- Run parameters ---
NPS  1000000000   $ 1 billion particles (50 tasks × 20M each × 16 threads)
CTME  2850        $ 47.5 hours (leave buffer for final dump)
```

**Expected output**:
- `runtpe` files every 2 hours (24 total dumps)
- `mctal` files at each dump
- `outp` at completion
- Speedup: ~600× (75% efficiency on 800 cores)

**Programmatic Parallel Configuration**:
- For automated parallel setup and job submission scripts, see: `mcnp_parallel_configurator.py`
- Useful for HPC job scheduling, resource optimization, and batch parallel execution

## References

- **User Manual**: Chapter 3.6 - PRDMP Card
- **User Manual**: Chapter 3.23 - TASKS Card
- **User Manual**: Chapter 3.1 - DBCN Card
- **Getting Started Manual**: Parallel execution
- **COMPLETE_MCNP6_KNOWLEDGE_BASE.md**: Parallel computing
- **Related skills**: mcnp-mesh-builder, mcnp-statistics-checker

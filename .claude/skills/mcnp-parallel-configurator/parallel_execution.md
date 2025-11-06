# MCNP Parallel Execution Guide

## Parallel Execution Models

### OpenMP (Shared Memory)

**Mechanism**: Multiple threads share same memory space

**Configuration**:
```bash
export OMP_NUM_THREADS=16  # Set thread count
mcnp6 inp=input.i
```

**Best For**:
- Single workstation
- 1-64 cores
- Simple setup

**Advantages**:
- Low communication overhead
- Easy to configure
- Efficient memory use

**Disadvantages**:
- Limited to single node
- Cannot scale beyond one machine

### MPI (Distributed Memory)

**Mechanism**: Multiple processes communicate via message passing

**Configuration**:
```bash
mpirun -np 20 mcnp6 inp=input.i
```

**Best For**:
- Multi-node clusters
- Large-scale simulations
- 10-1000+ cores

**Advantages**:
- Scales across nodes
- Good for large problems
- Better load balancing

**Disadvantages**:
- Higher communication overhead
- Each task replicates geometry/cross sections
- More complex setup

### Hybrid (MPI + OpenMP)

**Mechanism**: MPI across nodes, OpenMP within nodes

**Configuration**:
```bash
export OMP_NUM_THREADS=16
mpirun -np 20 mcnp6 inp=input.i
# 20 nodes × 16 threads = 320 cores total
```

**Best For**:
- Large HPC clusters
- >500 cores
- Production runs

**Advantages**:
- Best of both worlds
- Reduced communication (fewer MPI tasks)
- More memory per task
- Better scaling

**Disadvantages**:
- More complex configuration
- Requires hybrid-aware job scripts

**Recommended Configuration**:
- 1-2 MPI tasks per node
- Rest of cores use OpenMP threads
- Example: 50 nodes → 50 MPI tasks × 16 threads = 800 cores

## Performance Optimization

### Optimal Thread Count

**Rule**: Use physical cores, not hyperthreads

**Example**:
```bash
# 16-core node (32 hyperthreads)
export OMP_NUM_THREADS=16  # CORRECT (physical cores)
# NOT 32 (includes hyperthreads, causes overhead)
```

### Optimal MPI Task Count

**Factors**:
1. Memory per task (more tasks = less memory each)
2. Communication overhead (more tasks = more communication)
3. Load balance (more tasks = better balance for inhomogeneous geometry)

**Guidelines**:
```
Small cluster (2-10 nodes): 1 task/node
Medium cluster (10-50 nodes): 1-2 tasks/node
Large cluster (>50 nodes): 2-4 tasks/node (if geometry is complex)
```

**Example** (20 nodes, 16 cores each = 320 cores total):
```bash
# Option A: 20 MPI × 16 OpenMP = 320 cores
export OMP_NUM_THREADS=16
mpirun -np 20 mcnp6 inp=input.i
# Pros: Low communication, high memory/task
# Cons: May have load imbalance

# Option B: 40 MPI × 8 OpenMP = 320 cores
export OMP_NUM_THREADS=8
mpirun -np 40 mcnp6 inp=input.i
# Pros: Better load balance
# Cons: More communication

# Option C: 80 MPI × 4 OpenMP = 320 cores
export OMP_NUM_THREADS=4
mpirun -np 80 mcnp6 inp=input.i
# Pros: Best load balance for complex geometry
# Cons: Highest communication, lowest memory/task
```

**Recommendation**: Test Options A and B, measure speedup

### Load Balancing

**Problem**: Some particles take longer than others (deep penetration, variance reduction)

**Solution**: Use dynamic load balancing
```
TASKS  2   $ Dynamic mode
```

**Effect**: Fast tasks get more particles, slow tasks get fewer → better overall balance

## Scaling Analysis

### Expected Speedup

**Ideal scaling**: Speedup = Number of cores
- 10 cores → 10× faster
- 100 cores → 100× faster

**Realistic scaling**:
- 10 cores → 9× faster (90% efficiency)
- 100 cores → 70× faster (70% efficiency)
- 1000 cores → 400× faster (40% efficiency)

**Efficiency drops due to**:
- Communication overhead (MPI)
- Load imbalance
- I/O contention (dumps)
- Serial portions of code

### Measuring Speedup

**Method**:
1. Run on 1 core: Time = T₁
2. Run on N cores: Time = Tₙ
3. Speedup = T₁ / Tₙ
4. Efficiency = Speedup / N × 100%

**Example**:
```
1 core:   10 hours
10 cores: 1.2 hours → Speedup = 10/1.2 = 8.3× (83% efficiency)
20 cores: 0.7 hours → Speedup = 10/0.7 = 14.3× (71% efficiency)
```

### When to Stop Scaling

**Diminishing Returns**: Adding more cores gives minimal speedup

**Example**:
```
100 cores → 70× speedup
200 cores → 110× speedup (only 40× improvement for 100 extra cores)
400 cores → 150× speedup (only 40× improvement for 200 extra cores)
```

**Recommendation**: Stop when efficiency < 50% or when speedup improvement < 20% per doubling

## Architecture Considerations

### NUMA (Non-Uniform Memory Access)

**Modern multi-core nodes**: Memory is divided into NUMA domains

**Best Practice**: Pin threads to cores
```bash
export OMP_PROC_BIND=true
export OMP_PLACES=cores
```

### Hyperthreading

**Definition**: 2 virtual cores per physical core

**Recommendation for MCNP**: Do NOT use hyperthreads
```bash
# 16 physical cores (32 hyperthreads)
export OMP_NUM_THREADS=16  # CORRECT
# NOT 32 (no benefit, causes overhead)
```

### Memory Requirements

**Per MPI task**: Full geometry + cross sections replicated
```
Typical MCNP problem: 2-10 GB per task
Large problem: 10-100 GB per task
```

**Example** (40 GB problem, 16 GB RAM/node):
```
BAD:  4 MPI tasks/node → 4 × 40 GB = 160 GB needed (exceeds 16 GB!)
GOOD: 1 MPI task/node → 1 × 40 GB = 40 GB needed (fits with buffer)
```

## HPC Job Configuration

### SLURM Example (Hybrid)
```bash
#!/bin/bash
#SBATCH --nodes=20
#SBATCH --ntasks-per-node=1      # 1 MPI task/node
#SBATCH --cpus-per-task=16       # 16 threads/task
#SBATCH --time=48:00:00

export OMP_NUM_THREADS=16
mpirun -np 20 mcnp6 inp=input.i
```

### PBS Example (Hybrid)
```bash
#!/bin/bash
#PBS -l nodes=20:ppn=16
#PBS -l walltime=48:00:00

export OMP_NUM_THREADS=16
mpirun -np 20 mcnp6 inp=input.i
```

## Troubleshooting Parallel Performance

### Problem: Poor Scaling

**Symptoms**: 10 cores → only 5× faster

**Diagnosis**:
1. Check load balance (MCNP output: task timings)
2. Check communication time (MPI profiling)
3. Check I/O time (dump frequency)

**Fixes**:
```
# Load imbalance
TASKS  2   $ Use dynamic balancing

# Communication overhead
# Reduce MPI tasks, increase threads
export OMP_NUM_THREADS=16
mpirun -np 10 mcnp6 inp=input.i  # Instead of np=160

# I/O contention
PRDMP  180   $ Dump every 3 hours instead of 1
```

### Problem: Out of Memory

**Symptoms**: Job killed, "out of memory" error

**Cause**: Too many MPI tasks per node (geometry replicated)

**Fix**: Fewer tasks/node
```bash
# Before: 4 tasks/node × 40 GB = 160 GB needed
#SBATCH --ntasks-per-node=4

# After: 1 task/node × 40 GB = 40 GB needed
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
export OMP_NUM_THREADS=16
```

---

**See also**: `checkpoint_restart.md`, `hpc_job_submission.md`

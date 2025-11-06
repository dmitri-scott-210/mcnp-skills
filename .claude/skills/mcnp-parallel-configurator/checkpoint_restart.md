# MCNP Checkpoint and Restart Guide

## PRDMP Card Reference

### Complete Syntax
```
PRDMP  nd1  nd2  ndm  mct  kcod  notek  prdmtsk
```

### Parameters

**nd1** (dump frequency in minutes):
- Positive: Dump every nd1 minutes
- Negative: Dump every |nd1| minutes AND at end
- 0: No time-based dumps
- J: Skip (use default -1)

**nd2** (NPS intervals):
- 0: No NPS-based dumps
- n: Dump every n particles

**ndm** (maximum dumps):
- 0: Unlimited
- n: Stop after n dumps

**mct** (mctal file creation):
- 0: No mctal
- 1: mctal at dumps
- 2: mctal only at end
- 3: mctal at dumps and end

**kcod** (KCODE dumps):
- 0: No kcode dumps
- 1: Dump at intervals
- 2: Dump only at end

**notek** (screen output):
- 0: Minimal
- 1: Normal
- 2: Verbose

**prdmtsk** (MPI task dumps):
- -1: Each task dumps separately
- 0: Master task only (RECOMMENDED for MPI)
- 1: All tasks dump (large files!)

## Common Configurations

### Single Node (OpenMP Only)
```
PRDMP  60  J  0  1   $ Hourly, mctal at dumps
```

### MPI Cluster
```
PRDMP  120  J  0  1  1  1  0   $ 2-hour, master only
```

### Debugging
```
PRDMP  10  J  10  1  1  2   $ 10-min, max 10, verbose
```

### mctal at End Only
```
PRDMP  60  J  0  2   $ Hourly runtpe, mctal at end
```

## Output Files

### runtpe (Restart File)
- Binary format
- Contains complete simulation state
- Enables restart from interruption
- Size: Typically 100 MB - 10 GB

### mctal (Tally File)
- Machine-readable tally results
- Created based on mct parameter
- Can be read by post-processing tools

### srctp (Source File, KCODE only)
- Converged source distribution
- Enables restart without source convergence
- Significant time savings for large problems

## Restart Methods

### Method 1: CONTINUE Keyword

**Usage**:
```bash
mcnp6 inp=input.i continue
```

**Requirements**:
- runtpe file exists
- Input file unchanged (or only NPS/CTME modified)

**Effect**: Resumes from last dump, accumulates statistics

**Example Workflow**:
```bash
# Initial run (6 hours, creates runtpe)
mcnp6 inp=input.i

# Continue (6 more hours)
mcnp6 inp=input.i continue

# Total: 12 hours of accumulated statistics
```

### Method 2: Specific RUNTPE File

**Usage**:
```bash
mcnp6 inp=input.i runtpe=runtpe.5
```

**Use Case**: Restart from archived dump (not latest)

### Method 3: KCODE Source Restart

**Initial Run**:
```
KCODE  10000  1.0  50  250   $ Skip 50, run 250
PRDMP  60  J  0  1  1         $ Creates srctp
```

**Restart** (automatic):
```bash
mcnp6 inp=input.i continue   $ Auto-reads srctp
```

**Restart** (explicit):
```
KCODE  10000  1.0  0  300   $ Skip 0, run 300 more
KSRC  SRCTP                  $ Explicit source file
```

**Benefit**: Skip source convergence (~50 cycles saved)

## Dump File Management

### File Naming
```
runtpe    (latest dump, symlink or copy)
runtpe.1  (first dump)
runtpe.2  (second dump)
...
runtpe.n  (nth dump)
```

### Cleanup Script
```bash
#!/bin/bash
# Keep only last 3 dumps
ls -t runtpe.* | tail -n +4 | xargs rm -f
```

**Schedule**: Run hourly via cron during job

### Disk Space Calculation
```
Dump size: ~2 GB (typical)
Frequency: Every 60 minutes
Run time: 48 hours
Total dumps: 48 dumps
Total space: 48 × 2 GB = 96 GB

Recommendation: Ensure 150 GB free space
```

## Checkpoint Interval Optimization

### Formula
```
Optimal interval = sqrt(2 × checkpoint_overhead × MTBF)

Where:
  checkpoint_overhead = Time to write dump (seconds)
  MTBF = Mean time between failures (hours)
```

### Example Calculation
```
checkpoint_overhead = 120 seconds (2 minutes)
MTBF = 100 hours (cluster reliability)

Optimal = sqrt(2 × 120 × 100 × 3600)
        = sqrt(86,400,000)
        = 9,300 seconds
        = 155 minutes
        ≈ 2.5 hours

Recommendation: PRDMP 150 (2.5 hours)
```

### Practical Guidelines

| Run Duration | Dump Frequency | Reasoning |
|--------------|----------------|-----------|
| < 4 hours | Optional | Low failure risk |
| 4-12 hours | 60-120 min | Moderate risk |
| 12-48 hours | 120-180 min | Balance safety/I/O |
| > 48 hours | 180-240 min | Minimize I/O overhead |

## CTME Buffer Calculation

**Rule**: Set CTME 2-5% less than wall time

**Examples**:
```
Wall time: 24 hours (1440 min)
CTME: 1400 min (leaves 40-min buffer = 2.8%)

Wall time: 48 hours (2880 min)
CTME: 2850 min (leaves 30-min buffer = 1%)

Wall time: 72 hours (4320 min)
CTME: 4250 min (leaves 70-min buffer = 1.6%)
```

**Rationale**: Ensure final dump completes before job killed

## Troubleshooting

### Problem: "runtpe incompatible"

**Cause**: Input file changed between runs

**Allowed modifications**:
- NPS (increase)
- CTME (increase)
- PRINT/PRDMP (output control)

**NOT allowed**:
- Geometry changes
- Material changes
- Tally modifications
- KCODE parameters

**Fix**: Use original input file for restart

### Problem: Dumps not created

**Causes**:
1. CTME too short (job ends before first dump)
2. Disk full
3. Write permissions

**Fixes**:
```
1. Increase CTME
2. Check: df -h /path/to/rundir
3. Check: ls -l runtpe
```

### Problem: Lost particles after restart

**Cause**: Geometry modified between runs

**Fix**: Don't modify geometry. If essential, start fresh run.

---

**See also**: `parallel_execution.md`, `hpc_job_submission.md`

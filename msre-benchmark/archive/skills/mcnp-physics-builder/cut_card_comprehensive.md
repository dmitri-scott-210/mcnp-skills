# CUT Card Comprehensive Reference

## Overview

The CUT card provides alternative specification of transport and production cutoffs beyond PHYS card parameters. More flexible than PHYS card cutoffs for complex multi-cell problems.

## Syntax

```
CUT:P j1 j2 j3 c1 c2 c3 c4 ... cJ
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| P | Particle designator (N, P, H, E, /, etc.) |
| j1 | Time cutoff (shakes, 1 shake = 10⁻⁸ s) |
| j2 | Energy cutoff type (MeV) |
| j3 | Weight cutoff |
| c1, c2, ... cJ | Cell-dependent parameters (J = number of cells) |

## vs PHYS Card

**PHYS Card Cutoffs:**
- Global across all cells
- Simple energy cutoff (cutn, cutp, etc.)

**CUT Card Cutoffs:**
- Cell-specific
- More options (time, energy, weight)
- Overrides PHYS card if both specified

## When to Use CUT Card

✅ **Use CUT when:**
- Different cutoffs needed in different cells
- Time-dependent problems (need time cutoff)
- Weight cutoffs for variance reduction
- More control than PHYS card provides

❌ **Use PHYS when:**
- Same cutoffs for all cells (simpler)
- Only energy cutoffs needed

## Examples

### Example 1: Cell-Dependent Energy Cutoffs
```
CUT:N J 5J 0.1 0.01 0.001 10R
```
- No time or weight cutoffs (J entries)
- Cells 1-5: no energy cutoff
- Cell 6: 0.1 MeV
- Cell 7: 0.01 MeV
- Cell 8: 0.001 MeV
- Cells 9-18: 0.001 MeV (10R repeats last value)

### Example 2: Time Cutoff
```
CUT:P 1000 J J
```
- Photons killed at t > 1000 shakes (10 μs)
- No energy or weight cutoffs
- Same for all cells

## Integration

**Related Cards:**
- PHYS:P - Global cutoffs
- TSPLT - Time splitting (use with time cutoffs)
- IMP - Importance (affects weight cutoffs)

**Related Skills:**
- mcnp-physics-builder - Set PHYS card first, CUT for refinement
- mcnp-tally-builder - Ensure tally energies/times above cutoffs

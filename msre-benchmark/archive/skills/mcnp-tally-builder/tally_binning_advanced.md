# Advanced Tally Binning Options

## Overview

This document provides detailed specifications for advanced tally binning options using the E (energy), T (time), and C (cosine/angle) cards in MCNP. These cards subdivide tally results into multiple bins for detailed distribution analysis.

## Energy Binning (E Card)

### Basic Format
```
En   E1  E2  E3  ...  Ek
```
Where:
- `n` = tally number
- `E1, E2, ...` = energy bin boundaries in MeV
- Creates k bins: [0, E1], [E1, E2], ..., [Ek-1, Ek], [Ek, ∞]

### NT Option (Default Energy Structure)

The NT option provides quick access to MCNP's built-in energy structures without manually specifying boundaries:

```
En  NT
```

**Behavior:**
- Uses MCNP's default energy group structure
- Number of bins depends on particle type (MODE card)
- Neutrons: Typically uses ENDF/B-VII.1 or similar structure
- Photons: MCNP photon energy groups
- Electrons: Electron-specific energy structure

**Applications:**
- Quick scoping calculations
- Standardized cross-section group analysis
- Compatibility with legacy calculations

**Limitations:**
- Less control over bin placement
- May not match specific experimental detector response
- Default structure varies with MCNP version

### Custom Energy Binning

**Linear spacing:**
```
E4  0.1  0.5  1.0  2.0  5.0  10.0  20.0
```
Creates 7 bins from 0.1 to 20 MeV with manual boundaries.

**Logarithmic spacing (manual calculation required):**
```
E4  1e-9  1e-8  1e-7  1e-6  1e-5  1e-4  1e-3  1e-2  1e-1  1.0  10.0
```
Covers 10 decades with logarithmic bins.

**Combined strategies:**
- Fine binning in region of interest (e.g., thermal neutron range)
- Coarse binning elsewhere
- Example: Detailed thermal + broad fast neutron coverage

```
E4  1e-9  1e-8  5e-8  1e-7  5e-7  1e-6  0.1  1.0  10.0  20.0
     ^----- Fine thermal bins -----^     ^-- Coarse fast bins --^
```

## Time Binning (T Card)

### Basic Format
```
Tn   T1  T2  T3  ...  Tk
```
Where:
- Time boundaries in shakes (1 shake = 10⁻⁸ seconds)
- Creates time bins analogous to energy bins

### Cyclic Time Binning

For problems with periodic behavior (e.g., pulsed sources, accelerator cycles), use cyclic parameters:

```
Tn   CBEG= CFRQ= COFI= CONI= CSUB= CEND=
```

**Parameter Definitions:**

1. **CBEG** (Cycle Begin Time)
   - Start time of first cycle (shakes)
   - Default: 0

2. **CFRQ** (Cycle Frequency)
   - Period/duration of one complete cycle (shakes)
   - **REQUIRED** for cyclic binning

3. **COFI** (Cycle Offset In)
   - Time offset into cycle when binning begins (shakes)
   - Default: 0
   - Used to skip initial transient

4. **CONI** (Cycle Number In)
   - Which cycle number to start binning
   - Default: 1 (start immediately)
   - Used to skip startup cycles

5. **CSUB** (Cycle Subdivisions)
   - Number of equal-width bins within each cycle
   - **REQUIRED** for cyclic binning
   - All cycles divided into same bin structure

6. **CEND** (Cycle End)
   - Last cycle to include in binning
   - Default: All cycles through problem end time

**Example: Pulsed Neutron Source (1 kHz, 10 cycles)**
```
c Pulsed source at 1 kHz (period = 1e5 shakes)
T4  CFRQ=1e5  CSUB=10  CEND=10
```
Creates 10 time bins per cycle, tracks 10 complete cycles (100 total bins).

**Example: Skip Initial Cycles**
```
c Skip first 5 cycles to reach steady state
T4  CFRQ=1e6  COFI=5e5  CONI=6  CSUB=20  CEND=50
```
- Cycle period: 10⁻² seconds (1e6 shakes)
- Offset: Skip first 5e5 shakes of each cycle
- Start binning at cycle 6
- 20 bins per cycle
- Stop after cycle 50

**Applications:**
- Spallation neutron sources
- Pulsed reactor experiments
- Accelerator-driven systems
- Time-of-flight detectors

## Cosine/Angle Binning (C Card)

### Basic Format (Cosine Binning)
```
Cn   C1  C2  C3  ...  Ck
```
Where:
- Values are cosines of angle relative to surface normal or axis
- Range: -1.0 (backward) to +1.0 (forward)
- Used with F1 (surface current) and F2 (surface flux) tallies

**Example: Forward hemisphere (0° to 90°)**
```
C1  0.0  0.5  0.707  0.866  0.966  1.0
```
Bins: 0°-60°, 60°-45°, 45°-30°, 30°-15°, 15°-0°

### Degrees Format (Special Application)

MCNP also accepts angle bins in **degrees** for certain tallies:

```
Cn   DEGREES   θ1  θ2  θ3  ...  θk
```

Where:
- Angles measured from surface normal or reference axis
- Range: 0° (forward) to 180° (backward)
- Automatically converted to cosines internally

**Example: Forward angles in degrees**
```
C1  DEGREES  0  15  30  45  60  90
```
Equivalent to cosines: 1.0, 0.966, 0.866, 0.707, 0.5, 0.0

**When to Use Degrees:**
- More intuitive for experimentalists
- Aligns with detector specifications
- Easier to specify grazing angles (near 90°)

**Limitations:**
- Only valid for surface tallies (F1, F2)
- Not available for point detector (F5) or track-length estimators

### Combining C Card with FS Card

For angular distributions on specific surfaces:
```
F1:n  (201 202 203)    $ Three detector surfaces
C1    0.0  0.5  0.707  0.866  1.0
FS1   -201  -202  -203  $ Segment by surface
```
Creates 3 surfaces × 4 angle bins = 12 total bins in tally output.

## Multi-Dimensional Binning

Combining E, T, and C cards creates multi-dimensional tally arrays:

```
F4:n  10              $ Cell 10
E4    0.1  1.0  10.0  $ 3 energy bins
T4    1e6  1e7  1e8   $ 3 time bins
```
Total bins: 3 (energy) × 3 (time) = 9 bins

**Bin ordering in output:**
- Innermost loop: Cosine (C)
- Middle loop: Time (T)
- Outer loop: Energy (E)
- Example: E1-T1-C1, E1-T1-C2, ..., E1-T2-C1, ...

**Performance considerations:**
- Each additional dimension multiplies bin count
- Large bin arrays increase memory and output file size
- Use SD card to manage bin hierarchy if needed

## Best Practices

1. **Energy Binning:**
   - Use NT for quick analysis
   - Custom bins for specific applications (resonances, thresholds)
   - Match experimental detector resolution

2. **Time Binning:**
   - Linear bins for steady-state problems
   - Cyclic bins for pulsed/periodic problems
   - Skip initial cycles if transients present

3. **Cosine Binning:**
   - Use degrees format for intuitive specification
   - Denser bins near 0° and 180° for forward/backward peaks
   - Combine with FS card for surface-specific angular distributions

4. **Multi-Dimensional Binning:**
   - Start with fewer bins, refine as needed
   - Consider memory and output size
   - Use FQ card to suppress unwanted print tables

## Common Errors

**Energy binning errors:**
- Bins not in ascending order → FATAL ERROR
- Missing NT keyword when intended → Interpreted as energy values
- Mixing NT with manual bins → FATAL ERROR

**Time binning errors:**
- CFRQ not specified with cyclic parameters → WARNING, cyclic ignored
- CSUB = 0 or negative → FATAL ERROR
- Time bins exceeding problem end time (CTME card) → Bins never filled

**Cosine binning errors:**
- Values outside [-1, 1] range → FATAL ERROR
- DEGREES keyword misspelled → Interpreted as cosine values
- Using C card with F4/F5 tallies → WARNING, C card ignored (only for F1/F2)

## References

- MCNP6 Manual, Volume 2, Chapter 5.09 (E, T, C cards)
- MCNP6 Manual, Section on Cyclic Time Binning
- See also: `tally_segmentation_fs_sd.md` for combining binning with segmentation

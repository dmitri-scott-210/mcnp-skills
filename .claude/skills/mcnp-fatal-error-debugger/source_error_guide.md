# MCNP Source Definition Error Guide

**Purpose:** Comprehensive guide to source specification errors (SDEF, KCODE, SI, SP, DS cards).

**Companion to:** mcnp-fatal-error-debugger SKILL.md

---

## Overview

Source definition errors occur when SDEF, KCODE, or related distribution cards contain invalid specifications, dependencies, or inconsistencies. These errors typically manifest during input processing or early in particle transport.

---

## Source Error Categories

### Category 1: Impossible Variable Dependencies

#### Error Pattern

```
fatal error. impossible source variable dependencies.
```

#### Cause

SDEF includes dependency that is physically impossible or not supported by MCNP.

#### Common Invalid Dependencies

**1. AXS = FPOS (Axis depending on Position)**

```
c WRONG:
SDEF  POS=D1  AXS=FPOS=D2             $ Axis cannot depend on position

c WHY INVALID:
c - AXS defines reference axis for DIR, VEC
c - Cannot change axis for each source position
c - Physically meaningless
```

**Fix Option 1:** Use fixed axis
```
SDEF  POS=D1  AXS=0 0 1               $ Fixed axis (Z-direction)
SI1  L  0 0 0  10 0 0  20 0 0         $ Position distribution
```

**Fix Option 2:** Use different approach
```
SDEF  CEL=D1  AXS=0 0 1               $ Source in specific cells
SI1  L  1  2  3                       $ Cell numbers
SP1     1  1  1                       $ Equal probability
```

**2. SUR = FPOS (Surface depending on Position)**

```
c WRONG:
SDEF  POS=D1  SUR=FPOS=D2             $ Surface cannot depend on position

c WHY INVALID:
c - SUR defines which surface for surface source
c - Cannot change surface based on position
c - Logically inconsistent
```

**Fix:**
```
c Use multiple SDEF definitions (MCNP6 feature)
c OR use single surface with area weighting
SDEF  SUR=1  POS=D1                   $ Position distributed on surface 1
SI1  0  10                            $ Radius distribution on surface
SP1  -21  0                           $ Area weighting (r dr)
```

**3. Other Invalid Dependencies (from Source Primer)**

- RAD = FPOS → Radius depending on position
- EXT = FPOS → Extent depending on position
- CEL = FPOS → Cell depending on position
- Multiple dependent variables depending on same independent variable

#### Diagnosis Steps

1. **Identify SDEF line with error**
2. **Look for FPOS= or FCEL= or similar dependencies**
3. **Check Source Primer Table 5-1 for valid dependencies**
4. **Restructure source without invalid dependency**

#### Valid Dependencies (Examples)

```
c VALID: Energy depends on cell
SDEF  CEL=D1  ERG=FCEL=D2
SI1  L  1  2  3                       $ Cells
SP1     1  1  1
DS2  S  3  4  5                       $ Energy distributions for each cell
SI3  H  0.1  1  10                    $ Energy for cell 1
SP3     1  1  0
SI4  H  0.1  1  10                    $ Energy for cell 2
SP4     0.5  1  0.5
SI5  H  0.1  1  10                    $ Energy for cell 3
SP5     2  1  0

c VALID: Direction depends on position
SDEF  POS=D1  DIR=FPOS=D2
SI1  L  0 0 0  10 0 0
SP1     1  1
DS2  S  3  4                          $ DIR distributions
SI3  H  -1  0  1                      $ Cosine for position 1
SP3     1  0  1
SI4  H  -1  0  1                      $ Cosine for position 2
SP4     0  1  0
```

---

### Category 2: Source Outside Geometry

#### Error Pattern

```
fatal error. source particle not in any cell.
bad trouble in subroutine sourcc of mcrun
  nps =        1
```

#### Cause

Source position is outside defined geometry or in void cell.

#### Example 1: Position Outside Geometry

```
c Geometry:
1  1  -1.0  -1  IMP:N=1                $ Sphere R=10
999  0  1  IMP:N=0                     $ Graveyard

1  SO  10                              $ Sphere radius 10

c Source (WRONG):
SDEF  POS=20 0 0  ERG=14.1            $ Position at (20,0,0)
                                       $ This is OUTSIDE geometry (R=10)!
```

**Fix:**
```
SDEF  POS=0 0 0  ERG=14.1             $ Position at origin (inside sphere)
```

#### Example 2: Position in Void Cell

```
c Cells:
1  1  -1.0  -1  IMP:N=1                $ Inner sphere R=5
2  0        1 -2  IMP:N=1              $ Void shell R=5 to R=10
999  0  2  IMP:N=0                     $ Graveyard

c Source (WRONG):
SDEF  POS=7 0 0  ERG=14.1             $ Position in void cell 2!
```

**Fix Option 1:** Place in non-void cell
```
SDEF  POS=0 0 0  ERG=14.1             $ Position in cell 1 (material)
```

**Fix Option 2:** Use cell source
```
SDEF  CEL=1  ERG=14.1                 $ Source in cell 1
```

#### Example 3: Distributed Source with Some Positions Outside

```
SDEF  POS=D1  ERG=14.1
SI1  L  0 0 0  5 0 0  15 0 0          $ Third position (15,0,0) outside!
SP1     1  1  1

c Geometry: Sphere R=10
1  SO  10
```

**Fix:** Remove positions outside geometry
```
SI1  L  0 0 0  5 0 0                  $ Only positions inside R=10
SP1     1  1
```

#### Diagnosis Steps

1. **Note source position from SDEF**
2. **Plot geometry at that position:**
   ```
   IP  20 0 0                          $ Plot at source position
   ```
3. **Check if position is inside a cell with IMP>0**
4. **If outside geometry:** Move source or extend geometry
5. **If in void cell:** Move source or change cell material

---

### Category 3: Energy Distribution Errors

#### Error 1: Zero Bin Width

```
fatal error. energy distribution has zero bin width.
bad trouble in subroutine source - divide by zero
```

**Cause:** SI histogram has adjacent identical energies

```
c WRONG:
SDEF  ERG=D1
SI1  H  0  0  1                        $ Zero width bin (0 to 0)
SP1     0  1
```

**Fix:**
```
SDEF  ERG=D1
SI1  H  0  0.1  1  10                  $ Non-zero widths
SP1     0  1    1  0                   $ Histogram probabilities
```

#### Error 2: Negative Energy

```
fatal error. negative energy on SI card.
```

**Cause:** Energy value < 0

```
c WRONG:
SI1  L  -1  1  10                      $ Negative energy!

c CORRECT:
SI1  L  0.001  1  10                   $ All positive
```

#### Error 3: Energies Not Increasing

```
fatal error. energies on SI card must be in increasing order.
```

**Cause:** SI energies not monotonically increasing

```
c WRONG:
SI1  H  0  10  1  20                   $ 10 > 1 (wrong order)

c CORRECT:
SI1  H  0  1  10  20                   $ Increasing: 0 < 1 < 10 < 20
```

---

### Category 4: Distribution Card Errors

#### Error 1: SI/SP Count Mismatch

```
fatal error. number of entries on SI and SP cards do not match.
```

**Cause:** SI has N entries, SP has M entries (N ≠ M)

```
c WRONG:
SI1  L  1  2  3  4                     $ 4 entries
SP1     0.1  0.3  0.6                  $ 3 entries (MISMATCH!)

c CORRECT:
SI1  L  1  2  3  4                     $ 4 entries
SP1     0.1  0.2  0.3  0.4             $ 4 entries (match)
```

**Note:** For histograms (H), SP has N-1 entries where SI has N bin boundaries.

#### Error 2: Probabilities Don't Sum to 1

```
warning. probabilities on SP card do not sum to unity.
         probabilities will be renormalized.
```

**Not fatal, but warning.** MCNP will renormalize automatically.

```
c WARNING:
SP1  1  2  3                           $ Sum = 6 (will be normalized to 1/6, 2/6, 3/6)

c BETTER (explicit normalization):
SP1  0.167  0.333  0.5                 $ Sum = 1.0
```

#### Error 3: DS Points to Undefined SI

```
fatal error. DS card references undefined distribution.
```

**Cause:** DS points to SI that doesn't exist

```
c WRONG:
SDEF  CEL=D1  ERG=FCEL=D2
SI1  L  1  2  3                        $ Cells
DS2  S  10  11  12                     $ References SI10, SI11, SI12
c BUT: SI10, SI11, SI12 don't exist!

c CORRECT:
SDEF  CEL=D1  ERG=FCEL=D2
SI1  L  1  2  3
DS2  S  10  11  12
SI10  L  1  14.1                       $ Define SI10
SP10     1  1
SI11  L  1  14.1                       $ Define SI11
SP11     1  1
SI12  L  1  14.1                       $ Define SI12
SP12     1  1
```

---

### Category 5: Surface Source Errors

#### Error 1: Source on Surface Ambiguity

```
fatal error. source position on surface   1 is ambiguous.
```

**Cause:** Point source positioned exactly on surface boundary

```
c WRONG:
SDEF  POS=10 0 0  ERG=14.1            $ Exactly on surface 1 (SO 10)
1  SO  10
```

**Fix Option 1:** Offset slightly
```
SDEF  POS=10.001 0 0  ERG=14.1        $ Just inside or outside
```

**Fix Option 2:** Use explicit surface source
```
SDEF  SUR=1  NRM=-1  ERG=14.1         $ Surface source, inward direction
```

#### Error 2: Surface Source on Wrong Side

**Symptom:** All source particles immediately escape

```
c Geometry:
1  1  -1.0  -1  IMP:N=1                $ Sphere R=10
999  0  1  IMP:N=0                     $ Graveyard

c Source (WRONG):
SDEF  SUR=1  NRM=1  ERG=14.1          $ Outward direction (into graveyard!)
```

**Fix:** Reverse NRM direction
```
SDEF  SUR=1  NRM=-1  ERG=14.1         $ Inward direction (into geometry)
```

**Rule:**
- NRM=-1: Source particles directed into negative sense of surface
- NRM=1: Source particles directed into positive sense of surface

#### Error 3: SUR References Undefined Surface

```
fatal error. surface   5 on SDEF not defined.
```

**Cause:** SUR=5 but surface 5 doesn't exist

**Fix:**
```
c Either define surface 5:
5  PZ  0

c Or use different existing surface:
SDEF  SUR=1  NRM=-1  ERG=14.1
```

---

### Category 6: KCODE Errors (Criticality)

#### Error 1: Invalid KCODE Parameters

```
fatal error. KCODE parameters must be positive integers (except k).
```

**Cause:** KCODE has negative or zero values

```
c WRONG:
KCODE  10000  1.0  50  0               $ Fourth parameter = 0 (invalid!)

c CORRECT:
KCODE  10000  1.0  50  150             $ All positive (except k_eff estimate)
```

**KCODE format:** KCODE  nsrck  k_eff  nskip  nkcode

- nsrck: Source particles per cycle (must be > 0)
- k_eff: Initial guess (can be any positive number, typically ~1.0)
- nskip: Number of cycles to skip (can be 0)
- nkcode: Total number of active cycles (must be > 0)

#### Error 2: KSRC Outside Fissile Material

```
warning. initial source point not in fissile material.
fatal error. no fission source generated.
```

**Cause:** KSRC positions not inside cells with fissile material

```
c Geometry:
1  1  -10.0  -1  IMP:N=1               $ Fuel sphere R=10 (fissile)
2  2  -1.0   1 -2  IMP:N=1             $ Water reflector
999  0  2  IMP:N=0

c KSRC (WRONG):
KSRC  15 0 0                           $ Position in water reflector!

c KSRC (CORRECT):
KSRC  0 0 0  5 0 0  0 5 0              $ Positions inside fuel (cell 1)
```

**Diagnosis:**
1. Plot KSRC positions
2. Verify they are in cells with fissile material (U-235, Pu-239, etc.)
3. Move KSRC into fissile regions

#### Error 3: KCODE Without KSRC

```
fatal error. KCODE specified but no initial source (KSRC).
```

**Cause:** KCODE card exists but no KSRC card

**Fix:**
```
KCODE  10000  1.0  50  150
KSRC  0 0 0  5 0 0  0 5 0  -5 0 0  0 -5 0  0 0 5  $ Initial source points
```

---

### Category 7: Direction and Angle Errors

#### Error 1: DIR and VEC Both Specified

```
warning. both DIR and VEC specified - DIR will be ignored.
```

**Cause:** SDEF has both DIR= and VEC= (only one should be used)

```
c AVOID:
SDEF  POS=0 0 0  DIR=1  VEC=0 0 1  ERG=14.1   $ Both specified

c CORRECT (choose one):
SDEF  POS=0 0 0  DIR=D1  ERG=14.1             $ Use DIR
c OR:
SDEF  POS=0 0 0  VEC=0 0 1  DIR=1  ERG=14.1   $ Use VEC + DIR
```

**Difference:**
- DIR: Cosine of angle from AXS or VEC
- VEC: Reference vector for direction
- If both: VEC overrides, DIR used as cosine from VEC

#### Error 2: Invalid DIR Distribution

```
fatal error. DIR distribution contains values outside [-1, 1].
```

**Cause:** Cosines must be in range -1 ≤ μ ≤ 1

```
c WRONG:
SI1  L  -1  0  1.5                     $ 1.5 > 1 (invalid cosine!)

c CORRECT:
SI1  L  -1  0  1                       $ All in [-1, 1]
SP1     1  1  1
```

---

### Category 8: Transformation Errors with Source

#### Error: Source Transformation Applied Incorrectly

**Symptom:** Source particles appear in wrong locations

```
c Transformation:
TR1  10 0 0                            $ Translation +10 in X

c Source (intending to use transformation):
SDEF  POS=0 0 0  TR=1  ERG=14.1       $ Source at (0,0,0) transformed to (10,0,0)
```

**Common Error:** Forgetting that transformation applies to source coordinates

**Verification:**
```
c Plot source location:
# Should appear at (10,0,0) due to TR1 translation
# If appears at (0,0,0), transformation not applied correctly
```

**Fix if transformation not working:**
```
c Check TR card exists:
TR1  10 0 0

c Check TR=1 on SDEF:
SDEF  POS=0 0 0  TR=1  ERG=14.1

c Verify transformation number matches
```

---

## Systematic Diagnosis Procedure

### Step 1: Read Error Message

Identify error type:
- "impossible source variable dependencies" → Category 1
- "source particle not in any cell" → Category 2
- "zero bin width" or "divide by zero" → Category 3
- "entries do not match" → Category 4
- "source position on surface ambiguous" → Category 5
- "KCODE" related → Category 6

### Step 2: Locate Problematic Cards

```
c Find SDEF line:
SDEF  POS=D1  AXS=FPOS=D2  ERG=D3     $ Error is here (AXS=FPOS invalid)

c Find related SI/SP/DS cards:
SI1  L  0 0 0  10 0 0
DS2  S  10  11                         $ Check if SI10, SI11 exist
SI3  H  0  1  10
SP3     1  1
```

### Step 3: Verify Distributions

```
c Check each distribution:
SI1: Does it exist? Correct format? Values valid?
SP1: Matches SI1 entry count? Positive values?
DS2: Points to existing distributions?
```

### Step 4: Plot Source Locations

```
c For POS=D1:
SI1  L  0 0 0  10 0 0  20 0 0

# Plot at each position:
IP  0 0 0
IP  10 0 0
IP  20 0 0

# Verify each position is inside geometry in non-void cell
```

### Step 5: Test Simplified Source

```
c Replace complex source with simple test:
c SDEF  POS=D1  AXS=FPOS=D2  ERG=FCEL=D3  ...  (complex, failing)

c Simplified test:
SDEF  POS=0 0 0  ERG=14.1                        $ Minimal source

# If works, add complexity incrementally:
SDEF  POS=D1  ERG=14.1                           $ Add position distribution
SDEF  POS=D1  ERG=D2                             $ Add energy distribution
# Test at each stage to isolate error
```

---

## Common Patterns and Best Practices

### Pattern 1: Isotropic Point Source

```
SDEF  POS=0 0 0  ERG=14.1              $ Position, energy (direction isotropic by default)
```

### Pattern 2: Monodirectional Beam

```
SDEF  POS=0 0 0  AXS=0 0 1  DIR=1  ERG=14.1   $ Beam along +Z axis
```

### Pattern 3: Surface Source Inward

```
SDEF  SUR=1  NRM=-1  ERG=14.1          $ On surface 1, inward direction
```

### Pattern 4: Cell Volume Source

```
SDEF  CEL=1  ERG=D1                    $ Uniform in cell 1 volume
SI1  L  1  14.1                        $ Two energies
SP1     0.9  0.1                       $ 90% thermal, 10% 14 MeV
```

### Pattern 5: Energy-Dependent Direction (Valid)

```
SDEF  ERG=D1  DIR=FERG=D2              $ Direction depends on energy (VALID)
SI1  L  0.0253  1  14.1                $ Energies
SP1     1  1  1
DS2  S  10  11  12                     $ DIR for each energy
SI10  -1  1                            $ Isotropic (thermal)
SP10  0  1
SI11  0.5  1                           $ Forward peaked (1 MeV)
SP11  0  1
SI12  0.9  1                           $ Very forward (14 MeV)
SP12  0  1
```

---

## References

- **MCNP Manual Chapter 5.08:** Source Definition
- **Source Primer Chapter 5:** Known Source Errors
- **Source Primer Table 5-1:** Valid Variable Dependencies
- **fatal_error_catalog.md:** Error messages
- **MCNP Manual Chapter 3:** KCODE Criticality

---

**END OF SOURCE ERROR GUIDE**

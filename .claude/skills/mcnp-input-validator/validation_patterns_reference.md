# MCNP Input Validation Patterns Reference

**Created**: November 8, 2025
**Purpose**: Comprehensive reference for MCNP input validation patterns, error examples, and fixes

---

## Table of Contents

1. [FILL Array Validation](#fill-array-validation)
2. [Universe Cross-Reference Validation](#universe-cross-reference-validation)
3. [Thermal Scattering Verification](#thermal-scattering-verification)
4. [Numbering Conflict Detection](#numbering-conflict-detection)
5. [Surface-Cell Consistency](#surface-cell-consistency)

---

## FILL Array Validation

### Pattern: Rectangular Lattice (LAT=1)

**Dimension Calculation:**
```
Required Elements = (IMAX - IMIN + 1) × (JMAX - JMIN + 1) × (KMAX - KMIN + 1)
```

**Example: Valid 3×3×1 Rectangular Lattice**
```mcnp
c 3×3×1 = 9 elements required
200 0 -200 u=200 lat=1 imp:n=1 fill=-1:1 -1:1 0:0
    100 100 100
    100 100 100
    100 100 100
```

**Calculation:**
- I: -1 to 1 → (1-(-1)+1) = 3
- J: -1 to 1 → (1-(-1)+1) = 3
- K: 0 to 0 → (0-0+1) = 1
- Total: 3 × 3 × 1 = **9 elements** ✓

**Common Error: Dimension Mismatch**
```mcnp
c ERROR: Need 9 elements but only provide 8
200 0 -200 u=200 lat=1 imp:n=1 fill=-1:1 -1:1 0:0
    100 100 100
    100 100 100
    100 100         $ ← Missing 1 element!
```

**Error Message:**
```
Cell 200 (rectangular (LAT=1) lattice): FILL array dimension mismatch
  fill=-1:1 -1:1 0:0
  Required: 9 elements (3 × 3 × 1)
  Provided: 8 elements
  Missing: 1 elements
```

---

### Pattern: Hexagonal Lattice (LAT=2)

**CRITICAL: Same dimension calculation as LAT=1!**

**Example: Valid 3×3×1 Hexagonal Lattice**
```mcnp
c 3×3×1 = 9 elements required (same as LAT=1)
200 0 -200 u=200 lat=2 imp:n=1 fill=-1:1 -1:1 0:0
    100 100 100
    100 100 100
    100 100 100
```

**Calculation:**
- I: -1 to 1 → (1-(-1)+1) = 3
- J: -1 to 1 → (1-(-1)+1) = 3
- K: 0 to 0 → (0-0+1) = 1
- Total: 3 × 3 × 1 = **9 elements** ✓

**Note:** The dimension formula is identical for LAT=1 and LAT=2. The difference is only in how MCNP interprets the geometric arrangement.

---

### Pattern: Repeat Notation

**Critical Rule: nR means (n+1) total copies, NOT n copies!**

**Example: Correct Repeat Notation**
```mcnp
c 5×5×1 = 25 elements
200 0 -200 u=200 lat=1 imp:n=1 fill=-2:2 -2:2 0:0
    101 100 100 100 101
    100 100 2R 100
    100 3R 100
    100 100 2R 100
    101 100 100 100 101
```

**Expansion:**
- Row 1: `101 100 100 100 101` = 5 elements
- Row 2: `100 100 2R 100` = `100 100 100 100 100` = 5 elements (100 + 2R adds 2 more 100s)
- Row 3: `100 3R 100` = `100 100 100 100 100` = 5 elements (100 + 3R adds 3 more 100s)
- Row 4: Same as row 2 = 5 elements
- Row 5: Same as row 1 = 5 elements
- **Total: 25 elements** ✓

**Common Error: Off-by-One in Repeat Notation**
```mcnp
c ERROR: Think "2R" means 2 copies instead of 3 total
c Need 25 elements but think we have it
200 0 -200 u=200 lat=1 imp:n=1 fill=-2:2 -2:2 0:0
    101 100 100 100 101
    100 100 1R 100      $ ← Only gives 4 elements (100 + 1 more)
    100 2R 100          $ ← Only gives 4 elements
    100 100 1R 100
    101 100 100 100 101
c Total: 5 + 4 + 4 + 4 + 5 = 22 elements (missing 3!)
```

---

### Pattern: Large Lattices with Negative Indices

**Common Mistake: Forgetting the +1**

**Example: 15×15×1 Lattice**
```mcnp
c fill=-7:7 -7:7 0:0
c Calculation: (7-(-7)+1) × (7-(-7)+1) × (0-0+1)
c           = 15 × 15 × 1 = 225 elements
```

**Common Error:**
```
Wrong thinking: "-7 to 7 is 14 elements"
Correct: -7 to 7 is (-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7) = 15 elements
```

**Mnemonic:** Always use (MAX - MIN + 1), never subtract directly.

---

## Universe Cross-Reference Validation

### Pattern: Valid Hierarchy

**Example: 3-Level Universe Hierarchy**
```mcnp
c Level 3: TRISO particle (u=100)
100 1 -10.2 -100 u=100 imp:n=1  $ Fuel kernel
101 2 -1.9  100 -101 u=100 imp:n=1  $ Buffer layer
102 0 101 u=100 imp:n=1  $ Outside particle

c Level 2: Particle lattice (u=200, fills with u=100)
200 0 -200 u=200 lat=1 fill=-1:1 -1:1 0:0
    100 100 100
    100 100 100
    100 100 100

c Level 1: Global (u=0, fills with u=200)
999 0 -999 fill=200 imp:n=1
1000 0 999 imp:n=0
```

**Hierarchy Summary:**
```
u=0 (global) → fills with u=200
u=200 → fills with u=100
u=100 → no further fills (material cells)
```

**Depth: 3 levels** ✓

---

### Pattern: Circular Reference Error

**Example: Direct Circular Reference**
```mcnp
c ERROR: u=10 fills u=20, u=20 fills u=10
100 0 -1 u=10 fill=20 imp:n=1
200 0 -2 u=20 fill=10 imp:n=1  $ ← CIRCULAR!
```

**Error Message:**
```
Circular universe reference detected: 10 → 20 → 10
  Universe 10 fills 20, which eventually fills 10 again
```

**Example: Indirect Circular Reference**
```mcnp
c ERROR: u=10→u=20→u=30→u=10
100 0 -1 u=10 fill=20 imp:n=1
200 0 -2 u=20 fill=30 imp:n=1
300 0 -3 u=30 fill=10 imp:n=1  $ ← CIRCULAR!
```

**Error Message:**
```
Circular universe reference detected: 10 → 20 → 30 → 10
```

---

### Pattern: Undefined Universe

**Example: Fill References Undefined Universe**
```mcnp
c ERROR: u=200 is never defined
200 0 -200 u=100 lat=1 fill=-1:1 -1:1 0:0
    200 200 200    $ ← u=200 filled but never defined!
    200 200 200
    200 200 200
```

**Error Message:**
```
Undefined universes referenced: [200]
  These universes are filled but never defined with u=XXX
```

**Fix:**
```mcnp
c Define u=200 before using it
200 1 -10.0 -200 u=200 imp:n=1  $ ← Now u=200 is defined

c Now can use u=200 in fill
300 0 -300 u=100 lat=1 fill=-1:1 -1:1 0:0
    200 200 200
    200 200 200
    200 200 200
```

---

### Pattern: Universe 0 Explicit Definition

**Error: u=0 Should Never Be Explicitly Defined**
```mcnp
c ERROR: Universe 0 is global, never define it explicitly
100 0 -1 u=0 imp:n=1  $ ← WRONG! Don't use u=0
```

**Correct:**
```mcnp
c Correct: Cells without u=XXX are implicitly in universe 0
100 0 -1 imp:n=1  $ ← Implicitly in u=0 (global universe)
```

---

## Thermal Scattering Verification

### Pattern: Graphite Materials

**Required: grph.XXt for all carbon-containing materials**

**Example: Valid Graphite Material**
```mcnp
m1  $ Graphite moderator
    6012.00c  0.9890
    6013.00c  0.0110
mt1 grph.18t  $ ← CRITICAL: Must have MT card!
```

**Common Error: Missing MT Card**
```mcnp
m1  $ Graphite moderator - MISSING MT CARD!
    6012.00c  0.9890
    6013.00c  0.0110
c ← ERROR: Missing mt1 grph.XXt
```

**Error Message:**
```
CRITICAL: Material m1 contains carbon but missing grph.XXt S(α,β) library
  ZAIDs: ['6012', '6013']
  Add: mt1 grph.18t  $ or appropriate temperature
  Impact: Wrong thermal spectrum, 1000-5000 pcm reactivity error
```

**Available Graphite Libraries:**
- `grph.10t` → 296K (room temperature)
- `grph.18t` → 600K (HTGR, AGR)
- `grph.22t` → 800K
- `grph.24t` → 1000K (high-temperature reactor)
- `grph.26t` → 1200K
- `grph.28t` → 1600K
- `grph.30t` → 2000K

---

### Pattern: Light Water Materials

**Required: lwtr.XXt for H-1 + O-16 mixtures**

**Example: Valid Light Water Material**
```mcnp
m2  $ Light water
    1001.70c  2.0
    8016.70c  1.0
mt2 lwtr.13t  $ ← CRITICAL: Must have MT card for water!
```

**Common Error: Missing MT Card**
```mcnp
m2  $ Light water - MISSING MT CARD!
    1001.70c  2.0
    8016.70c  1.0
c ← ERROR: Missing mt2 lwtr.XXt
```

**Error Message:**
```
CRITICAL: Material m2 appears to be light water but missing lwtr.XXt library
  ZAIDs: ['1001', '8016']
  Add: mt2 lwtr.13t  $ or appropriate temperature
  Impact: Wrong thermal spectrum, incorrect reactivity
```

**Available Light Water Libraries:**
- `lwtr.10t` → 294K (room temperature)
- `lwtr.11t` → 325K (PWR cold leg)
- `lwtr.13t` → 350K (PWR average)
- `lwtr.14t` → 400K (PWR hot leg)
- `lwtr.16t` → 500K
- `lwtr.20t` → 800K (steam)

---

### Pattern: Heavy Water Materials

**Required: hwtr.XXt for H-2 + O-16 mixtures**

**Example: Valid Heavy Water Material**
```mcnp
m3  $ Heavy water (D2O)
    1002.70c  2.0
    8016.70c  1.0
mt3 hwtr.11t  $ ← CRITICAL: Must have MT card for D2O!
```

**Available Heavy Water Libraries:**
- `hwtr.10t` → 294K (room temperature)
- `hwtr.11t` → 325K (CANDU reactor)

---

### Pattern: Beryllium Materials

**Beryllium Metal: be.XXt**
```mcnp
m4  $ Beryllium metal reflector
    4009.70c  1.0
mt4 be.10t  $ ← Required for Be metal
```

**Beryllium Oxide: beo.XXt**
```mcnp
m5  $ Beryllium oxide (BeO)
    4009.70c  1.0
    8016.70c  1.0
mt5 beo.10t  $ ← Required for BeO
```

---

## Numbering Conflict Detection

### Pattern: Duplicate Cell IDs

**Error: Same Cell ID Used Twice**
```mcnp
c ERROR: Cell 100 defined twice
100 1 -10.0 -1 u=10 imp:n=1  $ First definition
...
100 2 -6.5 -2 u=20 imp:n=1   $ ← Second definition (CONFLICT!)
```

**Error Message:**
```
Duplicate cell ID 100 defined at lines: 5, 127
```

**Fix: Use unique cell IDs**
```mcnp
100 1 -10.0 -1 u=10 imp:n=1
101 2 -6.5 -2 u=20 imp:n=1   $ ← Changed to 101
```

---

### Pattern: Systematic Numbering

**Recommended: Encode Hierarchy in ID Numbers**

**Example: AGR-1 Systematic Numbering**
```python
# Cells: 9XYZW (X=capsule, Y=stack, Z=compact, W=sequence)
cell_id = 90000 + capsule*1000 + stack*100 + compact*20 + sequence

# Example:
91108 = capsule 1, stack 1, compact 0, sequence 8
92315 = capsule 2, stack 3, compact 1, sequence 5

# Surfaces: 9XYZn
surface_id = 9000 + capsule*100 + stack*10 + compact

# Materials: 9XYZ
material_id = 9000 + capsule*100 + stack*10 + compact

# Universes: XYZW
universe_id = capsule*1000 + stack*100 + compact*10 + component
```

**Benefits:**
- Easy to identify component from ID
- Prevents conflicts across subsystems
- Simplifies maintenance and debugging
- Enables programmatic generation

---

## Surface-Cell Consistency

### Pattern: Undefined Surface Reference

**Error: Cell References Undefined Surface**
```mcnp
c ERROR: Surface 1000 is referenced but not defined
100 1 -10.0 -1000 2000 imp:n=1  $ References surfaces 1000, 2000
...
c Surfaces:
100 so 5.0   $ ← Surface 1000 not defined (typo: 100 vs 1000?)
200 pz 10.0  $ ← Surface 2000 not defined
```

**Error Message:**
```
Cell 100: References undefined surface 1000
Cell 100: References undefined surface 2000
```

**Common Cause: Typo**
```mcnp
c Intended: -100 (surface 100)
c Typed: -1000 (surface 1000)
```

**Fix:**
```mcnp
100 1 -10.0 -100 200 imp:n=1  $ ← Fixed: use -100, not -1000
```

---

## Validation Checklist

### Pre-Run Validation Steps

1. **FILL Array Validation**
   - [ ] Calculate required elements: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
   - [ ] Expand repeat notation: nR = (n+1) total copies
   - [ ] Count provided elements
   - [ ] Verify match for LAT=1 and LAT=2

2. **Universe Cross-Reference**
   - [ ] All filled universes are defined
   - [ ] No circular references
   - [ ] Universe 0 not explicitly defined
   - [ ] Hierarchy depth <10 levels

3. **Thermal Scattering**
   - [ ] Graphite materials have grph.XXt
   - [ ] Water materials have lwtr.XXt or hwtr.XXt
   - [ ] Beryllium materials have be.XXt or beo.XXt
   - [ ] Temperature-appropriate library selected

4. **Numbering Conflicts**
   - [ ] No duplicate cell IDs
   - [ ] No duplicate surface IDs
   - [ ] No duplicate material IDs
   - [ ] No duplicate universe IDs

5. **Surface-Cell Consistency**
   - [ ] All referenced surfaces are defined
   - [ ] All referenced materials are defined
   - [ ] No typos in surface/material references

---

## References

- **MCNP6 Manual Chapter 3**: Geometry Specification
- **MCNP6 Manual Chapter 4**: Material Specification
- **MCNP6 Manual Appendix G**: S(α,β) Thermal Scattering Data
- **AGR-1 HTGR Model**: Production example of complex lattice hierarchy
- **mcnp-input-validator Skill**: Automated validation tools

---

**Version**: 2.0.0
**Last Updated**: November 8, 2025

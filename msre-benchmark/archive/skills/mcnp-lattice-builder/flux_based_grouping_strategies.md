# Flux-Based Grouping Strategies for Lattice Depletion

**Reference for:** mcnp-lattice-builder skill
**Source:** AGR-1 verification exercise (Fairhurst-Agosta & Kozlowski, 2024)
**Purpose:** Critical guidance for grouping repeated structures to achieve accurate depletion/activation results

---

## The Fundamental Problem

When modeling repeated structures (fuel assemblies, fuel pins, detector arrays) for depletion or activation calculations, a critical decision must be made:

**How to group structures for independent flux tallying and depletion tracking?**

**Wrong grouping → Significant errors (10-15%)**
**Correct grouping → Acceptable errors (<5%)**

---

## The Verification Exercise

### Experimental Setup

**Geometry:** Simplified LWR-like 8×8 pin array

**Specifications:**
- 64 fuel pins total
- Pin radius: 1.25 cm
- Pin pitch: 4 cm
- Pin height: 80 cm
- Square array in aluminum shroud (2 cm thick)
- Light water reflector (40 cm radius cylindrical tank)

**Objective:** Compare three grouping approaches

### Three Approaches Tested

#### Approach 1: Explicit Cells (Reference)

**Method:** Every pin = unique cell number (no repeated structures)

**MCNP Implementation:**
```
c Pin 1 at position (0,0)
1  1  -10.5  -1  IMP:N=1   $ Fuel pin 1
2  2  -6.5    1 -2  IMP:N=1   $ Clad pin 1
3  3  -1.0    2  IMP:N=1   $ Water around pin 1

c Pin 2 at position (1,0)
11  1  -10.5  -11  IMP:N=1   $ Fuel pin 2
12  2  -6.5    11 -12  IMP:N=1   $ Clad pin 2
13  3  -1.0    12  IMP:N=1   $ Water around pin 2

[... 64 pins × 3 cells each = 192 cells]
```

**Depletion:** Each pin tracked independently with unique material

**Results:**
- Neutron flux: Reference (0% error by definition)
- Photon intensity: Reference
- Delayed gamma heating: Reference

**Disadvantage:** Impractical for large systems (thousands of pins)

#### Approach 2: Whole-Core Single Universe

**Method:** All 64 pins grouped as ONE universe, replicated 64 times

**MCNP Implementation:**
```
c Universe 1: Generic pin (used for all 64 positions)
1  1  -10.5  -1  U=1  IMP:N=1   $ Fuel
2  2  -6.5    1 -2  U=1  IMP:N=1   $ Clad
3  3  -1.0    2  U=1  IMP:N=1   $ Water

c Lattice
100  0  -10  LAT=1  U=10  FILL=0:7  0:7  0:0  IMP:N=1
                            1 1 1 1 1 1 1 1   $ All same universe
                            1 1 1 1 1 1 1 1
                            [...8 rows total]

c Material 1 is SHARED by all 64 pins
```

**Depletion:** Single flux tally averaged over all 64 pins → single burnup calculation

**Results:**
- Neutron flux: <0.1% difference (GOOD)
- Photon intensity: <0.1% difference (GOOD)
- **Delayed gamma heating: 15.6% difference (UNACCEPTABLE)**

**Why it failed:** Flux varies spatially across array. Pins at edge see different flux than pins at center. Averaging loses this spatial variation.

**Impact on depletion:**
- Center pins: Higher flux → more burnup → underpredicted by average
- Edge pins: Lower flux → less burnup → overpredicted by average
- Activation products wrong → gamma source wrong → dose rate wrong

#### Approach 3: Assembly-Level Grouping (4-Pin Groups)

**Method:** Divide 64 pins into 16 groups of 4 adjacent pins each

**MCNP Implementation:**
```
c Universe 1: Pin type for group 1 (positions [0-1, 0-1])
1  1  -10.5  -1  U=1  IMP:N=1   $ Fuel
2  2  -6.5    1 -2  U=1  IMP:N=1   $ Clad
3  3  -1.0    2  U=1  IMP:N=1   $ Water

c Universe 2: Pin type for group 2 (positions [2-3, 0-1])
11  2  -10.5  -1  U=2  IMP:N=1   $ Fuel (different material number)
12  2  -6.5    1 -2  U=2  IMP:N=1   $ Clad
13  3  -1.0    2  U=2  IMP:N=1   $ Water

[... 16 universes total, one per 4-pin group]

c Lattice with different universes
100  0  -10  LAT=1  U=10  FILL=0:7  0:7  0:0  IMP:N=1
                            1  1  2  2  3  3  4  4   $ Grouped in quarters
                            1  1  2  2  3  3  4  4
                            5  5  6  6  7  7  8  8
                            5  5  6  6  7  7  8  8
                            [...pattern continues]
```

**Depletion:** 16 flux tallies → 16 independent burnup calculations

**Results:**
- Neutron flux: <0.1% difference (GOOD)
- Photon intensity: <0.1% difference (GOOD)
- **Delayed gamma heating: 4.3% difference (ACCEPTABLE)**

**Why it succeeded:** 4-pin groups small enough that flux variation within group is small. Spatial variation between groups captured by independent depletion.

---

## The Rule: Group by Flux Zone

### Physical Principle

**Flux spatial variation drives burnup spatial variation:**

```
High flux region  →  High burnup  →  More fission products  →  More activation
Low flux region   →  Low burnup   →  Fewer fission products  →  Less activation
```

**If you average high-flux and low-flux regions:**
- High-flux pins: Burnup underpredicted → Activation underpredicted
- Low-flux pins: Burnup overpredicted → Activation overpredicted
- **Net result: Wrong gamma source distribution → Wrong dose rates**

### The Grouping Rule

**Group structures that experience SIMILAR flux levels**

**DO NOT group based on:**
- ❌ Geometric convenience ("all pins are same → one universe")
- ❌ Modeling simplicity ("easier to manage")
- ❌ Input file size ("fewer materials")

**DO group based on:**
- ✅ Flux spatial variation ("pins with similar flux → one group")
- ✅ Physical regions ("inner assembly vs outer assembly")
- ✅ Depletion similarity ("similar burnup behavior")

---

## Determining Appropriate Group Size

### Step 1: Understand Flux Spatial Distribution

**Run preliminary calculation:**
1. Model entire geometry with single universe (simplest)
2. Add FMESH tally to map flux distribution
3. Identify flux spatial patterns

**Example FMESH:**
```
FMESH4:N  GEOM=XYZ
          ORIGIN=-50  -50  0
          IMESH=50  IINTS=20   $ 5 cm bins
          JMESH=50  JINTS=20
          KMESH=80  KINTS=1    $ Single axial bin
```

**Analysis:** Plot flux map, identify regions with:
- Uniform flux (can group together)
- Strong gradients (need finer grouping)

### Step 2: Define Flux-Based Zones

**Typical reactor patterns:**

**PWR Core:**
- Zone 1: Inner assemblies (highest flux)
- Zone 2: Mid-radius assemblies (medium flux)
- Zone 3: Peripheral assemblies (lowest flux)
- Zone 4: Assemblies near control rod clusters (depressed flux)

**HTGR Core:**
- Zone 1: Central region (high flux)
- Zone 2: Mid-plane assemblies (medium flux)
- Zone 3: Top/bottom assemblies (lower flux, axial gradient)
- Zone 4: Radial reflector region (low flux)

**AGR-1 Experiment:**
- Zone: Each compact (72 total)
- Rationale: Flux varies axially along test train → each compact sees different flux
- Result: 72 independent universes, 72 material definitions

### Step 3: Balance Accuracy vs Computational Cost

**Trade-off:**
- More groups = Better accuracy + Higher cost
- Fewer groups = Lower accuracy + Lower cost

**Typical grouping sizes:**

| System Type | Typical Group Size | Rationale |
|-------------|-------------------|-----------|
| Single assembly | Pin-by-pin or 4-pin groups | High flux gradients within assembly |
| Full core (small) | Assembly-level | Flux relatively uniform within assembly |
| Full core (large) | Region-level (4-9 assemblies/group) | Balance accuracy vs cost |
| Test rigs | Per-sample (like AGR-1) | Strong axial/radial gradients |

**Error tolerance guidance:**
- <5% error: Acceptable for most analyses
- 5-10% error: Acceptable for scoping studies
- >10% error: Generally unacceptable (re-group!)

### Step 4: Verification

**Test your grouping:**

1. **Run with chosen grouping**
2. **Compare to reference case:**
   - Option A: Explicit cells (small problems)
   - Option B: Finer grouping (2× more groups)
3. **Check key parameters:**
   - k-effective (criticality)
   - Peak/average power ratio
   - Activation product inventory
   - Dose rates (if applicable)
4. **Iterate if error >5%**

---

## Implementation in MCNP

### Universe and Material Strategy

**Key principle:** Each flux zone needs:
1. **Unique universe number** (for geometric grouping)
2. **Unique material number** (for depletion tracking)

**Example: 8×8 array with 4-pin grouping (16 groups)**

```
c ===== Universe 1: Group 1 (pins at [0-1, 0-1]) =====
1  1  -10.5  -1  U=1  IMP:N=1   $ Fuel
2  2  -6.5    1 -2  U=1  IMP:N=1   $ Clad
3  3  -1.0    2  U=1  IMP:N=1   $ Coolant

c ===== Universe 2: Group 2 (pins at [2-3, 0-1]) =====
11  11  -10.5  -1  U=2  IMP:N=1   $ Fuel (material 11, different from mat 1)
12  2   -6.5    1 -2  U=2  IMP:N=1   $ Clad (shared)
13  3   -1.0    2  U=2  IMP:N=1   $ Coolant (shared)

[... 16 universes total]

c ===== Lattice with zone assignments =====
100  0  -10  LAT=1  U=10  FILL=0:7  0:7  0:0  IMP:N=1
                            1  1  2  2  3  3  4  4   $ Zone assignments
                            1  1  2  2  3  3  4  4
                            5  5  6  6  7  7  8  8
                            5  5  6  6  7  7  8  8
                            9  9  10 10 11 11 12 12
                            9  9  10 10 11 11 12 12
                            13 13 14 14 15 15 16 16
                            13 13 14 14 15 15 16 16

c ===== Material definitions =====
c All fuel materials start identical but deplete independently
M1   92235.80c  0.04  92238.80c  0.96  8016.80c  2.0   $ Group 1 fuel
M11  92235.80c  0.04  92238.80c  0.96  8016.80c  2.0   $ Group 2 fuel
[... materials 1, 11, 21, 31, ... 151 for 16 fuel groups]

M2   40000.80c  1.0   $ Zircaloy clad (shared by all)
M3   1001.80c   2.0  8016.80c  1.0   $ Water coolant (shared by all)
```

**Depletion tracking:**
- Material 1: Depletes based on flux in zone 1
- Material 11: Depletes based on flux in zone 2
- ... independent depletion for each zone

### AGR-1 Implementation (72 Groups)

**Grouping strategy:** Each of 72 compacts = one group

```
c ===== Compact numbering scheme =====
c Universe format: [Capsule][Stack][Compact]0
c Material format: m9[Capsule][Stack][Compact][Layer]
c
c Example: Capsule 2, Stack 3, Compact 4:
c   Universe: 2340
c   Fuel material: m9234

c ===== Universe 1110: Capsule 1, Stack 1, Compact 1 =====
[TRISO particle universe 1114 with material m9111]
  ↓
[Particle lattice universe 1116]
  ↓
[Compact lattice universe 1110]

c ===== Universe 1120: Capsule 1, Stack 1, Compact 2 =====
[TRISO particle universe 1124 with material m9112]
  ↓
[Particle lattice universe 1126]
  ↓
[Compact lattice universe 1120]

[... 72 total compact universes with 72 unique fuel materials]
```

**Result:** Each compact's TRISO fuel tracked independently → accurate activation → accurate dose rates

---

## When Whole-Core Grouping Fails

### Failure Modes

**Spatial flux gradients:**
- Radial: Center-to-edge flux variation
- Axial: Top-to-bottom flux variation
- Azimuthal: Near control rods vs far from control rods

**Burnup effects:**
- High-burnup assemblies: Depleted fuel → different spectrum
- Fresh assemblies: Higher reactivity → higher local flux
- BOL vs EOL: Flux distribution evolves

**Result:** Whole-core average flux does NOT represent any physical location

### AGR-1 Verification Impact

**If AGR-1 used whole-train grouping (6 capsules as one group):**
- Capsule 1 (bottom): Lower flux → actual dose rate LOW
- Capsule 3 (middle): Medium flux → actual dose rate MEDIUM
- Capsule 6 (top): Higher flux → actual dose rate HIGH
- Average flux → WRONG dose rate everywhere

**Estimated error with whole-train grouping:** >15% (based on verification exercise scaling)

**Actual approach (compact-level grouping):** Within measurement uncertainty

---

## Recommended Grouping by Problem Type

### Small Systems (<100 fuel elements)

**Recommendation:** Pin-by-pin or 4-pin groups

**Rationale:** Computational cost manageable, accuracy maximized

**Implementation:** Each pin or small group = unique universe + material

### Medium Systems (100-1000 fuel elements)

**Recommendation:** Assembly-level or sub-assembly grouping

**Rationale:** Balance between accuracy and cost

**Implementation:** Group pins within assembly → each assembly = unique universe

**Example:**
- 17×17 PWR assembly = 264 pins
- Group as: All pins in assembly share universe
- Different assemblies: Different universes
- Full core with 193 assemblies: 193 groups

### Large Systems (>1000 fuel elements)

**Recommendation:** Region-level grouping (multiple assemblies per group)

**Rationale:** Computational limits require coarser grouping

**Implementation:** Divide core into flux zones (inner/mid/outer, or 3×3 regions, etc.)

**Example:**
- 400-assembly core
- Group into 9 radial zones (5×5 → 25 "supercells" → 9 unique zones)
- Each zone: ~45 assemblies

### Test Rigs / Experiments

**Recommendation:** Per-sample grouping

**Rationale:** Strong spatial gradients, validation against measurement critical

**Implementation:** Each experimental sample = unique universe + material

**Example:** AGR-1 with 72 compacts → 72 groups

---

## Best Practices Summary

1. **NEVER group entire core as single universe** for depletion/activation (except for preliminary scoping)

2. **Run FMESH tally first** to understand flux spatial distribution

3. **Group by flux similarity**, not geometric convenience

4. **Verify grouping** by comparing to finer-resolution case

5. **Target <5% error** in activation/dose parameters

6. **Document grouping rationale** clearly in input file

7. **Unique materials for each group** - critical for independent depletion

8. **Balance accuracy vs cost** - use finest practical grouping

9. **When in doubt, use finer grouping** - easier to coarsen than to discover errors late

10. **Validate against measurement** when available - ultimate test of grouping strategy

---

**END OF FLUX-BASED GROUPING STRATEGIES REFERENCE**

For lattice fundamentals, see lattice_fundamentals.md. For reactor modeling workflow, see reactor_to_mcnp_workflow.md.

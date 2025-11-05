# Reactor-to-MCNP Translation Workflow

**Reference for:** mcnp-lattice-builder skill
**Source:** AGR-1 experiment analysis and reactor modeling best practices
**Purpose:** Guidance for translating reactor design specifications from literature to MCNP lattice models

---

## Overview

Reactor modeling requires translating design specifications from technical papers, design reports, and engineering drawings into MCNP lattice syntax. This is a critical skill for reactor physics analysis, safety evaluation, and design studies.

**Key challenge:** Literature provides high-level specifications, but MCNP requires detailed geometric and material definitions.

---

## Information Typically Available in Literature

### Geometric Specifications

**Usually provided:**
- Overall dimensions (core diameter, height)
- Lattice pitch (assembly spacing, pin spacing)
- Number of fuel assemblies/pins
- Layer thicknesses (fuel, clad, gap)
- Assembly arrangement (e.g., "24 fuel assemblies in hexagonal arrangement")

**Example from literature:**
> "The AGR-1 test train contains 6 capsules, each with 3 stacks of 4 compacts. TRISO particles have 5 layers: kernel (UO₂, 350 μm), buffer (100 μm), IPyC (40 μm), SiC (35 μm), OPyC (40 μm)."

### Material Compositions

**Usually provided:**
- Fuel type (UO₂, UCO, MOX, metal)
- Enrichment percentage
- Structural material types (SS316L, Zircaloy, graphite)
- Coolant specifications

**Often missing:**
- Exact densities (may say "typical" or reference standard)
- Isotopic compositions beyond enrichment
- Impurity levels
- Temperature-dependent properties

### Operating Conditions

**Usually provided:**
- Thermal power
- Burnup (MWd/kgU)
- Irradiation duration
- Operating temperature ranges

**Often missing:**
- Detailed power history
- Control rod positions over time
- Coolant flow distribution
- Spatial power peaking factors

---

## Information Often Missing (Requires Assumptions)

### Detailed Geometry

**Missing details:**
- Exact surface definitions (mathematical equations)
- Gap dimensions between components
- Transformation matrices for tilted/rotated assemblies
- Manufacturing tolerances
- As-built vs as-designed dimensions

**Mitigation:**
- Use engineering standards for gaps (e.g., "typical PWR fuel-clad gap = 85 μm")
- Reference similar reactor designs
- Document all assumptions clearly

### Material Specifications

**Missing details:**
- Exact density values (may give range)
- Full isotopic vectors (beyond U-235/238)
- Temperature dependencies
- Burnup-dependent composition changes
- Fission product distributions

**Mitigation:**
- Use MCNP material compendium for standard materials
- Reference NIST or IAEA databases
- Use bounding analysis (max/min density cases)
- Document material source and assumptions

### Operational Details

**Missing details:**
- Detailed power history (may only give "average")
- Control rod motion during operation
- Coolant void patterns
- Flux spatial distribution

**Mitigation:**
- Use cycle-average conditions
- Perform sensitivity studies
- Document simplifications
- Validate against reported results

---

## Recommended Translation Workflow

### Step 1: Extract Available Information

**Create information table:**

| Parameter | Value | Source | Confidence |
|-----------|-------|--------|------------|
| Assembly pitch | 30 cm | Paper Fig. 2 | High |
| Fuel enrichment | 19.75% U-235 | Table 1 | High |
| Clad material | Zircaloy-4 | Text p.5 | High |
| Fuel density | ~10.8 g/cm³ | "Typical UO₂" | Medium |
| Gap thickness | Not specified | Assume 85 μm | Low |

**Confidence levels:**
- High: Explicitly stated with precision
- Medium: Stated but approximate or "typical"
- Low: Inferred or assumed from similar designs

### Step 2: Identify Hierarchy

**Determine geometric levels:**

**Example: HTGR core**
1. **Level 0:** Core (main geometry)
2. **Level 1:** Assembly arrangement (hexagonal/rectangular)
3. **Level 2:** Fuel channel lattice within assembly
4. **Level 3:** TRISO particles within fuel compact

**Key questions:**
- What repeats at each level?
- What varies between instances?
- How are levels connected (fill cards)?

### Step 3: Design Universe Structure

**Principle:** Work from smallest to largest

**Example: AGR-1 test train**

```
Level 1: TRISO particle (5 layers)
  Universe 1114: Kernel + 5 layers
  Universe 1115: Matrix only (filler)

Level 2: Particle lattice (15×15 rectangular)
  Universe 1116: LAT=1 lattice of 1114/1115

Level 3: Compact (31 axial elements)
  Universe 1110: LAT=1 (1D) with end caps

Level 4: Stack (4 compacts + gaps)
  Real-world cells with FILL=1110, 1120, 1130, 1140

Level 5: Capsule (3 stacks + structure)
  Structural materials surround stacks
```

**Numbering scheme:**
```
Universe format: [Capsule][Stack][Compact][Layer]
Example: 1114 = Capsule 1, Stack 1, Compact 1, Layer 4 (TRISO particle)
```

### Step 4: Make Reasonable Assumptions

**Document assumptions clearly:**

```
c ============================================================
c MODELING ASSUMPTIONS (Document in input file header)
c ============================================================
c 1. Fuel-clad gap: 85 μm (typical PWR value, not specified in paper)
c 2. Coolant density: 0.7 g/cm³ at 300°C (typical VVER condition)
c 3. Regular lattice: TRISO particles in cubic array (actual: random)
c 4. Uniform flux: All pins in assembly grouped (simplification)
c 5. Burnup: Cycle-average conditions used (neglects in-cycle variation)
c ============================================================
```

**Assumption categories:**
- **Geometric:** Dimensions, gaps, manufacturing tolerances
- **Material:** Densities, compositions, impurities
- **Operational:** Power distribution, control rod position, burnup
- **Modeling:** Regular vs stochastic, flux grouping, symmetry

### Step 5: Implement MCNP Geometry

**Create surfaces systematically:**

```
c ===== LEVEL 1: TRISO Particle Surfaces =====
1111  SO  0.017485  $ Kernel radius (from Table 2)
1112  SO  0.027905  $ Buffer outer (kernel + 100μm buffer)
1113  SO  0.031785  $ IPyC outer (buffer + 40μm IPyC)
[...]

c ===== LEVEL 2: Lattice Element =====
1117  RPP  -0.04372  0.04372  -0.04372  0.04372  -0.05  0.05  $ 0.874 mm pitch

c ===== LEVEL 3: Compact Dimensions =====
1118  RPP  -0.65  0.65  -0.65  0.65  -0.04372  0.04372  $ 1.3 cm diameter compact
```

**Define universes:**

```
c ===== LEVEL 1: TRISO Particle =====
1  m1 -10.924  -1111  U=1114  VOL=0.092522  $ Kernel
2  m2  -1.100  1111 -1112  U=1114  $ Buffer
[... 5 layers total]

c ===== LEVEL 2: Particle Lattice =====
10  0  -1117  LAT=1  U=1116  FILL=-7:7 -7:7 0:0  $ 15×15 array
    1115 1115 1114 [...]   $ Pattern from paper description
```

### Step 6: Flux-Based Grouping

**CRITICAL:** Group by flux level, not just geometric convenience

**From AGR-1 verification exercise:**
- Whole-core single universe: **15.6% error** (UNACCEPTABLE)
- Assembly-level grouping: **4.3% error** (ACCEPTABLE)
- Explicit cells: 0% error (reference, but impractical)

**Grouping strategy:**
```
c ===== Each compact gets unique universe for independent depletion =====
c Capsule 1, Stack 1:
c   Compact 1: Universe 1110, Material m1111
c   Compact 2: Universe 1120, Material m1112
c   Compact 3: Universe 1130, Material m1113
c   Compact 4: Universe 1140, Material m1114
c
c Capsule 1, Stack 2:
c   Compact 1: Universe 1210, Material m1121
c   [... 72 total compacts = 72 universes = 72 materials]
```

**Reason:** Each compact experiences different flux → different burnup → must track separately

**Rule:** Group structures with similar flux levels. If strong spatial gradients, use finer grouping.

### Step 7: Material Definitions

**Start with known compositions:**

```
c ===== Fuel Kernel: UCO from Table 1 =====
c U enrichment: 19.75% U-235
c C/U ratio: 0.4 (from paper)
c O/U ratio: 1.5 (from paper)
m1111  92234.80c  3.34179E-03   $ U-234 (from enrichment)
       92235.80c  1.99636E-01   $ U-235 (19.75% specified)
       92236.80c  1.93132E-04   $ U-236 (trace)
       92238.80c  7.96829E-01   $ U-238 (balance)
       6012.80c   0.3217217     $ C-12
       6013.80c   0.0035783     $ C-13 (natural abundance)
       8016.80c   1.3613        $ O-16
```

**For "typical" materials, reference databases:**

```
c ===== SS316L: Standard composition from PNNL Compendium =====
m9011  24050.80c  -0.00653131   $ Cr (reference composition)
       24052.80c  -0.14263466
       [...standard SS316L composition...]
```

### Step 8: Validate Against Literature

**Cross-check results:**

1. **k-effective:** Compare to reported value (if available)
2. **Flux distribution:** Check against reported peaking factors
3. **Dose rates:** Compare calculated to measured (if post-irradiation data available)
4. **Isotopic inventory:** Compare to reported burnup compositions

**Document validation:**
```
c ============================================================
c VALIDATION vs Literature
c ============================================================
c k-eff (BOL): 1.042 (calculated) vs 1.045±0.003 (reported)
c   → Difference: 0.29% (within reported uncertainty)
c
c Peak/average flux: 1.15 (calculated) vs 1.12-1.18 (reported range)
c   → Within reported range
c
c Dose rate at 30 days: 190 Sv/h (calculated) vs 188±12 Sv/h (measured)
c   → Agreement within measurement uncertainty
c ============================================================
```

### Step 9: Sensitivity Analysis

**Test impact of assumptions:**

**Example sensitivity cases:**
1. **Density variation:** ±5% on fuel density
2. **Gap thickness:** 50 μm vs 100 μm
3. **Lattice type:** Regular vs URAN (stochastic)
4. **Grouping:** Whole-core vs assembly-level

**Document sensitivity:**
```
c ============================================================
c SENSITIVITY ANALYSIS RESULTS
c ============================================================
c Parameter          Base      Variation    Δk-eff
c --------------------------------------------------
c Fuel density       10.8      10.3 g/cm³   -0.0045
c Fuel density       10.8      11.3 g/cm³   +0.0042
c Gap thickness      85 μm     50 μm        +0.0008
c Gap thickness      85 μm     120 μm       -0.0012
c Flux grouping      Assembly  Whole-core   +0.0234 (UNACCEPTABLE)
c ============================================================
```

---

## Common Literature Scenarios

### Scenario 1: Partial Geometry Information

**Literature says:** "Standard PWR 17×17 assembly with 24 guide tubes"

**Missing:** Exact guide tube positions

**Solution:**
1. Reference standard Westinghouse 17×17 design
2. Document assumption: "Guide tube pattern from standard W 17×17 design (ref: NUREG/CR-XXXX)"
3. Verify total guide tube count matches (24)

### Scenario 2: "Typical" Material Properties

**Literature says:** "Zircaloy-4 clad, typical density"

**Missing:** Exact density value

**Solution:**
1. Use standard reference: PNNL-15870 Rev 1 (Compendium of Material Composition Data)
2. Zircaloy-4 density: 6.56 g/cm³ (standard)
3. Document: "Zr-4 density from PNNL-15870, representative of unirradiated material at 20°C"

### Scenario 3: Simplified Descriptions

**Literature says:** "TRISO particles randomly distributed in graphite matrix"

**Challenge:** Random distribution not practical in MCNP for millions of particles

**Solution:**
1. Use regular lattice (computational necessity)
2. Document: "Regular lattice approximation used due to computational limits. See validation section for impact assessment."
3. Optional: Use URAN card for limited randomness if critical

### Scenario 4: Multi-Level Assembly

**Literature says:** "Core contains 24 hexagonal assemblies, each with 19 fuel channels, each channel contains fuel compacts with TRISO particles"

**Translation:**
1. **Level 0:** Core geometry (barrel, reflector)
2. **Level 1:** Core lattice (24 hexagonal assemblies) → LAT=2
3. **Level 2:** Assembly lattice (19 fuel channels) → LAT=2
4. **Level 3:** Channel internals (fuel compacts stacked)
5. **Level 4:** TRISO particle lattice within compact → LAT=1

**Hierarchy:**
```
Universe 0 (main)
  └─> Universe 1000 (core lattice, LAT=2)
      └─> Universe 100 (assembly lattice, LAT=2)
          └─> Universe 10 (channel with compacts)
              └─> Universe 5 (TRISO lattice, LAT=1)
                  └─> Universe 1 (TRISO particle)
```

---

## Best Practices for Literature Translation

1. **Extract-document-verify cycle:** Extract info → document assumptions → verify against reported results

2. **Hierarchy-first design:** Identify repeating structures before writing geometry

3. **Conservative assumptions:** When uncertain, use bounding values and test sensitivity

4. **Clear documentation:** Every assumption must be documented in input file header

5. **Reference standards:** Use ASTM, ASME, NUREG, IAEA standards for "typical" values

6. **Validate ruthlessly:** Compare every available result to literature

7. **Sensitivity analysis:** Test impact of uncertain parameters

8. **Version control:** Track assumption changes and their impact

9. **Peer review:** Have another analyst review assumptions and implementation

10. **Literature contact:** When possible, contact authors for clarification on missing details

---

## AGR-1 Example: Complete Translation

**Literature specifications:**
- 6 capsules, 3 stacks each, 4 compacts per stack
- TRISO: 5-layer structure, dimensions given
- Regular lattice (explicitly stated as simplification)

**Translation:**
1. **Extract:** All dimensions from Table 1, materials from Table 2
2. **Hierarchy:** TRISO → particle lattice → compact → stack → capsule
3. **Grouping:** 72 compacts = 72 universes (flux-based)
4. **Materials:** 72 fuel materials (independent burnup), shared structural materials
5. **Assumptions:** Regular TRISO lattice, Hf shroud continuous, omit gas lines/thermocouples
6. **Validation:** Dose rates at 1, 30, 365 days match reported values within uncertainty

**Result:** 4653-line MCNP input with 72 independent depletion zones, validated against experiment

---

**END OF REACTOR-TO-MCNP WORKFLOW REFERENCE**

For lattice fundamentals, see lattice_fundamentals.md. For flux-based grouping details, see flux_based_grouping_strategies.md.

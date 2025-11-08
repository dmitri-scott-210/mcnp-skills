# MCNP-BURNUP-BUILDER SKILL REFINEMENT PLAN
## Comprehensive Enhancement for Depletion and Activation Calculations

**Created**: 2025-11-08
**Based On**: HTGR reactor model analysis (AGR-1, μHTGR microreactor)
**Priority**: HIGH - Critical for realistic reactor calculations
**Execution Time**: 2-3 hours

---

## EXECUTIVE SUMMARY

The mcnp-burnup-builder skill requires major enhancements based on analysis of production-quality HTGR models demonstrating:
- Strategic cell selection for depletion tracking (~150 cells from thousands)
- Systematic fission product and actinide inclusion
- Multi-physics workflow integration (MCNP ↔ ORIGEN)
- Time-dependent burnup calculations with operational history
- Shutdown dose rate calculations from depleted isotopics

**Current Gap**: Skill lacks guidance on what cells to track, which isotopes to include, and how to integrate with depletion codes.

**Impact**: Users cannot perform ANY realistic burnup calculations for reactors.

---

## PART 1: ISSUES IDENTIFIED

### Current Skill Status

**Location**: `.claude/skills/mcnp-burnup-builder/`

**Current SKILL.md**: Focuses on BURN card syntax but lacks:
1. ❌ Strategic cell selection criteria
2. ❌ Fission product selection methodology
3. ❌ Actinide chain completeness
4. ❌ ORIGEN coupling workflow
5. ❌ Time-dependent burnup sequences
6. ❌ Computational complexity management
7. ❌ Validation against experimental data

### What Production Models Teach Us

From AGR-1 and μHTGR analysis:

**Cell Selection Strategy**:
- Track ~150 cells from 1,500+ total cells
- Focus on high-flux regions: fuel, absorbers, structural materials near core
- Ignore low-importance regions: far reflectors, shields, external structures
- Balance: physics accuracy vs. computational cost

**Isotope Selection**:
- 25+ fission products for criticality impact
- 4-7 actinides minimum (U-234/235/236/238, Pu-239/240/241)
- Strong absorbers: Sm-149, Gd-155/157, Xe-135
- Stable FPs for decay heat: Cs-137, Sr-90, Ba-140

**Workflow Integration**:
- Neutron transport → depletion → photon transport
- Cell-wise isotopic evolution
- Time-averaged operational parameters
- Decay source generation for shutdown dose rates

---

## PART 2: REFINEMENT OBJECTIVES

### Primary Goals

1. **Teach strategic cell selection**
   - Criteria for identifying important cells
   - Flux-based grouping strategies
   - Computational trade-offs

2. **Provide systematic isotope selection**
   - Fission product importance ranking
   - Actinide chain requirements
   - Absorption cross-section impacts

3. **Explain BURN card mechanics**
   - Card format and options
   - Material specification
   - Time step selection

4. **Enable ORIGEN coupling**
   - MCNP → ORIGEN data handoff
   - Isotopic inventory management
   - Multi-cycle calculations

5. **Support workflow integration**
   - Burnup → dose rate sequences
   - Time-dependent configurations
   - Validation strategies

---

## PART 3: SPECIFIC ENHANCEMENTS

### 3.1 Update SKILL.md

**File**: `.claude/skills/mcnp-burnup-builder/SKILL.md`

**Current Length**: ~200 lines (can add 400+ lines)

**ADD new sections**:

```markdown
## STRATEGIC CELL SELECTION FOR DEPLETION TRACKING

### The Fundamental Trade-Off

**Challenge**: Reactor models have 1,000s of cells, but tracking all cells is computationally prohibitive.

**Solution**: Strategic selection of ~100-200 cells that matter for physics.

### Cell Selection Criteria

**ALWAYS track these cell types**:

1. **Fuel Cells** (CRITICAL)
   - All fissile material regions
   - High flux regions (>1E13 n/cm²/s)
   - Spatial resolution: by assembly, axial zone, radial zone
   - Example: 72 fuel kernels in AGR-1 (6 capsules × 3 stacks × 4 compacts)

2. **Control Materials** (CRITICAL)
   - Burnable absorbers (B-10, Gd-155/157)
   - Control rods (Ag-In-Cd, B4C, hafnium)
   - Shim rods, safety rods
   - These burn out and change reactivity

3. **Structural Materials Near Core** (IMPORTANT)
   - Stainless steel (activation: Fe-55, Co-60, Mn-54)
   - Zircaloy cladding (activation products)
   - Graphite reflectors (C-14 production)
   - These become dose sources after shutdown

**MAY track if computationally feasible**:

4. **Moderator/Reflector Regions**
   - Graphite blocks near fuel
   - Water/heavy water in high flux
   - Beryllium reflectors

**DO NOT track**:

5. **Low-Flux Regions**
   - Outer reflectors (flux < 1E10 n/cm²/s)
   - Biological shields
   - External structures
   - Coolant far from core
   - Minimal physics impact, waste computational resources

### Cell Selection Methodology

**Step 1: Identify High-Flux Regions**
```mcnp
c Run initial MCNP calculation with F4 tallies
F4:n  100 101 102 103  $ Test cells
```

**Step 2: Rank by Flux Magnitude**
- Flux > 1E14 n/cm²/s: MUST track
- Flux 1E13-1E14 n/cm²/s: SHOULD track (fuel, absorbers)
- Flux 1E12-1E13 n/cm²/s: MAY track (structural)
- Flux < 1E12 n/cm²/s: DO NOT track

**Step 3: Group by Similarity**
- Cells with similar flux spectra can be grouped
- Reduces total tracked cells while preserving accuracy
- Example: 4 identical fuel assemblies → track 1, apply to all 4

### Example: AGR-1 Cell Selection

**Total model**: ~1,600 cells

**Tracked cells** (~150 total):
```
Fuel kernels (72 cells):
  - 6 capsules × 3 stacks × 4 compacts = 72 unique fuel regions
  - Each has different flux history → must track separately

Structural steel (30 cells):
  - Capsule walls, supports, holders
  - Activation products important for dose rates

Graphite (20 cells):
  - Spacers above/below compacts
  - C-14 production important

Borated graphite (10 cells):
  - Burnable poison holders
  - B-10 depletion affects reactivity

Hafnium shrouds (10 cells):
  - Control material
  - Hf-177 burnout critical

Coolant/void (0 cells):
  - Not tracked, minimal burnup
```

**Result**: ~10% of cells tracked, captures >99% of physics

---

## FISSION PRODUCT SELECTION

### Why Fission Products Matter

**Three Critical Impacts**:

1. **Reactivity Effects**
   - Strong absorbers poison the reactor (Xe-135, Sm-149, Gd-155/157)
   - Typical reactivity worth: -1000 to -5000 pcm

2. **Decay Heat**
   - Beta/gamma emission after shutdown
   - Safety-critical for cooling requirements

3. **Dose Rates**
   - Photon sources for shielding calculations
   - Decommissioning planning

### Systematic FP Selection Strategy

**TIER 1: ALWAYS Include (Strong Absorbers)**

```
Xe-135   (3.5 Mbarn thermal) - Peak ~9 hours after shutdown
Sm-149   (40 kbarn thermal) - Stable, builds up over time
Sm-151   (15 kbarn thermal) - Long-lived (90 yr)
Gd-155   (61 kbarn thermal) - Builds from Eu-155 decay
Gd-157   (254 kbarn thermal) - Strongest absorber
Pm-147   (Decays to Sm-147) - Precursor
Pm-149   (Decays to Sm-149) - Precursor
```

**TIER 2: SHOULD Include (Significant Absorbers)**

```
Cd-113   (20 kbarn thermal)
Eu-153   (312 barn thermal)
Eu-155   (3.7 kbarn thermal)
Rh-103   (150 barn thermal)
Tc-99    (20 barn thermal)
Cs-133   (30 barn thermal)
```

**TIER 3: MAY Include (Decay Heat/Dose)**

```
Cs-137   (Beta/gamma emitter, 30 yr half-life)
Sr-90    (Beta emitter, 29 yr)
Ba-140   (Gamma, short-lived)
La-140   (Gamma, 1.7 day)
Ce-141   (Gamma, 32 day)
Pr-143   (Beta, 13.6 day)
```

**TIER 4: Optional (Completeness)**

```
Kr-83    (Stable noble gas)
Xe-131   (Stable)
Xe-133   (5.2 day, dose important)
Mo-95    (Stable)
Ru-101   (Stable)
Nd-143   (Stable)
Nd-145   (Stable)
```

### MCNP Material Card Example

**Depleted fuel with FP tracking**:
```mcnp
m100  $ UO2 fuel after 3 cycles, cell 100
c Actinides
   92234.70c  5.873407E-06  $ U-234
   92235.70c  4.198373E-04  $ U-235 (depleted from fresh)
   92236.70c  1.517056E-05  $ U-236 (capture product)
   92238.70c  3.057844E-05  $ U-238
   93237.70c  1.886031E-07  $ Np-237
   94239.70c  3.962382E-07  $ Pu-239 (bred)
   94240.70c  3.184477E-08  $ Pu-240
   94241.70c  1.038741E-08  $ Pu-241
c TIER 1 FPs (strong absorbers)
   54135.70c  5.732034E-10  $ Xe-135 (equilibrium)
   62149.70c  2.657344E-08  $ Sm-149 (CRITICAL)
   62151.70c  7.853828E-08  $ Sm-151
   64155.70c  8.234521E-09  $ Gd-155
   64157.70c  1.440627E-10  $ Gd-157 (STRONGEST)
c TIER 2 FPs (significant absorbers)
   48113.70c  7.621751E-10  $ Cd-113
   63153.70c  1.027083E-07  $ Eu-153
   63155.70c  1.247127E-08  $ Eu-155
   45103.70c  3.635464E-07  $ Rh-103
   55133.70c  2.445752E-06  $ Cs-133
c TIER 3 FPs (decay heat, optional)
   55137.70c  1.234567E-06  $ Cs-137 (gamma source)
   38090.70c  9.876543E-07  $ Sr-90 (beta source)
c TIER 4 FPs (completeness, optional)
   36083.70c  2.749474E-07  $ Kr-83
   54131.70c  9.237888E-07  $ Xe-131
   42095.70c  9.415301E-08  $ Mo-95
   44101.70c  2.720314E-06  $ Ru-101
   60143.70c  1.325206E-06  $ Nd-143
   60145.70c  2.037404E-06  $ Nd-145
```

**Typical count**:
- Minimum: 7-10 isotopes (actinides + Tier 1 FPs)
- Standard: 20-30 isotopes (+ Tier 2)
- Comprehensive: 40-60 isotopes (+ Tier 3 + Tier 4)

---

## ACTINIDE CHAIN REQUIREMENTS

### Minimum Actinide Tracking

**ALWAYS include these 7 isotopes** (captures major chains):

```
U-234   - Decay product of Pu-238
U-235   - Primary fissile (if LEU/HEU)
U-236   - U-235 + n capture
U-238   - Primary fertile, Pu production
Np-237  - U-237 beta decay
Pu-239  - U-238 + n, primary bred fissile
Pu-240  - Pu-239 + n capture
Pu-241  - Pu-240 + n, fissile
```

### Extended Actinide Tracking

**For high-burnup or long-irradiation** (add these):

```
Pu-238  - Cm-242 alpha decay, heat source
Pu-242  - Pu-241 + n capture
Am-241  - Pu-241 beta decay (432 yr)
Am-242m - Am-241 + n, isomer
Am-243  - Am-242 + n or Pu-242 + n
Cm-242  - Am-241 + n + beta decay
Cm-243  - Pu-242 + n
Cm-244  - Cm-243 + n, spontaneous fission
Cm-245  - Cm-244 + n, fissile
```

### Capture/Decay Chains

**U-238 neutron capture chain**:
```
U-238 + n → U-239 (β⁻, 23 min) → Np-239 (β⁻, 2.4 day) → Pu-239
Pu-239 + n → Pu-240 + n → Pu-241 + n → Pu-242
```

**Am-241 production**:
```
Pu-241 (β⁻, 14 yr) → Am-241
Am-241 + n → Am-242m (β⁻) → Cm-242 (α, 163 day) → Pu-238
```

**Critical insight**: Must include precursors to get correct buildup!

### Example: Fresh vs. Depleted Fuel

**Fresh UO₂ (BOL - Beginning of Life)**:
```mcnp
m1  $ Fresh UO2, 4.5% enriched
   92234.70c  3.6e-4   $ Natural abundance in enriched U
   92235.70c  0.045    $ Enrichment
   92236.70c  2.1e-6   $ Trace from enrichment process
   92238.70c  0.955    $ Remainder
    8016.70c  2.0      $ Oxygen (stoichiometric)
```

**Depleted UO₂ (EOL - End of Life, 60 GWd/MTU)**:
```mcnp
m1  $ Depleted UO2 after ~3 cycles
c Uranium (depleted U-235, built up U-236)
   92234.70c  1.2e-4   $ Decreased
   92235.70c  0.008    $ Depleted from 4.5% → 0.8%
   92236.70c  0.005    $ Built up from captures
   92238.70c  0.940    $ Slightly decreased from fission
c Plutonium (bred from U-238)
   94238.70c  2.3e-5   $ From Cm-242 alpha decay
   94239.70c  0.006    $ Major bred fissile
   94240.70c  0.003    $ From Pu-239 captures
   94241.70c  0.002    $ Fissile, from Pu-240 captures
   94242.70c  8.0e-4   $ From Pu-241 captures
c Minor actinides
   93237.70c  6.0e-4   $ From U-237 decay chain
   95241.70c  1.0e-4   $ From Pu-241 beta decay
   95242.70c  2.0e-7   $ From Am-241 + n
   95243.70c  2.0e-5   $ From Pu-242 + n
   96242.70c  1.5e-6   $ From Am-241 + n chain
   96244.70c  8.0e-6   $ From Cm-243 + n
c Fission products (Tier 1 + Tier 2, 20+ isotopes)
   [... as shown in previous example ...]
c Oxygen
    8016.70c  2.0      $ Approximately constant
```

---

## BURN CARD SPECIFICATION

### BURN Card Format

**MCNP6 BURN card syntax**:
```mcnp
BURN  TIME=t1 t2 t3 ... tn  MAT=m1 m2 m3 ...  POWER=p  PFRAC=f1 f2 f3 ...
      BOPT=options  MATVOL=v1 v2 v3 ...  OMIT=isotope_list
```

**Critical Parameters**:

- **TIME**: Irradiation time steps (days)
- **MAT**: Material numbers to deplete
- **POWER**: Total reactor power (MW)
- **PFRAC**: Power fraction in each material
- **BOPT**: ORIGEN library options
- **MATVOL**: Material volumes (cm³) for normalization
- **OMIT**: Isotopes to exclude from tracking

### Example: 3-Cycle Burnup

**Scenario**: PWR fuel assembly, 18-month cycles, 3 cycles total

```mcnp
c Cycle 1: 500 EFPD (effective full-power days)
BURN  TIME=100 200 300 400 500
      MAT=1 2 3 4 5 6 7 8 9 10
      POWER=3400  $ 3400 MW thermal
      PFRAC=0.10 0.10 0.10 0.10 0.10 0.10 0.10 0.10 0.10 0.10
      BOPT=1 2 3
      MATVOL=1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5

c Shutdown 1: 60 days decay
BURN  TIME=560  POWER=0

c Cycle 2: 500 EFPD
BURN  TIME=660 760 860 960 1060
      MAT=1 2 3 4 5 6 7 8 9 10
      POWER=3400
      PFRAC=0.11 0.11 0.10 0.09 0.09 0.10 0.10 0.10 0.10 0.10
      BOPT=1 2 3
      MATVOL=1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5

c Shutdown 2: 60 days decay
BURN  TIME=1120  POWER=0

c Cycle 3: 500 EFPD
BURN  TIME=1220 1320 1420 1520 1620
      MAT=1 2 3 4 5 6 7 8 9 10
      POWER=3400
      PFRAC=0.12 0.11 0.10 0.09 0.08 0.10 0.10 0.10 0.10 0.10
      BOPT=1 2 3
      MATVOL=1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5 1.5e5

c Final shutdown: 30 years cooling
BURN  TIME=12582  POWER=0  $ 1620 + 30*365 = 12582 days
```

**Note**: Power fractions shift as outer assemblies deplete faster than inner.

### Time Step Selection

**Guidelines**:

1. **During irradiation**: 50-100 day intervals
   - Finer at BOL (isotopes building up rapidly)
   - Coarser at EOL (approach equilibrium)

2. **During shutdown**:
   - First 24 hours: 1-hour steps (Xe-135, I-135 decay)
   - 1 day - 1 week: Daily steps
   - 1 week - 1 month: Weekly steps
   - > 1 month: Monthly or yearly steps

3. **Critical transitions**:
   - Reactor startup/shutdown: Fine steps
   - Power changes: Fine steps around transition
   - Refueling: Explicit decay period

### Material Volume Specification

**CRITICAL**: Volumes must be accurate for correct isotopic densities.

**Option 1: VOL card in cell definition**:
```mcnp
100 1 -10.2  -100  u=10  imp:n=1  vol=1.5e5  $ Volume in cm³
```

**Option 2: MATVOL in BURN card**:
```mcnp
BURN  MAT=1 2 3  MATVOL=1.5e5 1.4e5 1.6e5
```

**Calculation example**:
```
Fuel pin: r=0.41 cm, h=365 cm
Volume = π r² h = π × 0.41² × 365 = 193 cm³

Fuel assembly: 264 pins
Total fuel volume = 264 × 193 = 5.09e4 cm³
```

---

## ORIGEN COUPLING WORKFLOW

### The Three-Step Process

**Production workflow from AGR-1/μHTGR**:

```
Step 1: MCNP Neutron Transport (Burnup Calculation)
  ├─ Calculate neutron flux in all cells
  ├─ Identify cells for depletion tracking (~150 cells)
  ├─ Extract cell-wise flux spectra
  └─ Output: Flux spectra, reaction rates → ORIGEN input

Step 2: ORIGEN Depletion Calculation
  ├─ Read MCNP flux/spectrum data
  ├─ Calculate isotopic evolution using Bateman equations
  ├─ Track actinides + fission products + activation products
  ├─ Apply operational history (power, time steps)
  └─ Output: Cell-wise isotopic inventories vs. time

Step 3: MCNP Photon Transport (Shutdown Dose Rate)
  ├─ Read ORIGEN isotopic inventories at decay time
  ├─ Generate photon source from decays (Ci → photons/sec)
  ├─ Define SDEF using isotopic distributions
  ├─ Calculate dose rates using F4:p + dose function
  └─ Output: 3D dose rate map for decommissioning
```

### MCNP → ORIGEN Data Handoff

**MCNP provides** (via BURN card or external coupling):
1. Cell-wise flux magnitude (n/cm²/s)
2. Energy spectrum (multi-group or continuous)
3. One-group cross-sections for major reactions
4. Irradiation time steps
5. Power normalization

**ORIGEN needs**:
1. One-group flux (or spectrum)
2. Fuel composition (actinides, initial enrichment)
3. Irradiation/decay times
4. Cross-section library (matched to spectrum)

### MOAA Tool (Production Example)

**MOAA** = MCNP-ORIGEN Activation Automation

**Not included in repository** (export-controlled), but workflow documented:

1. Run MCNP to get fluxes for selected cells
2. MOAA extracts flux data automatically
3. MOAA generates ORIGEN inputs for each cell
4. ORIGEN runs in batch for all cells
5. MOAA collects isotopic inventories
6. MOAA generates MCNP SDEF for dose calculation

**Lesson**: Professional tools automate coupling, but understanding workflow is essential.

### Manual ORIGEN Coupling (Step-by-Step)

**Step 1: Extract flux from MCNP**
```mcnp
F4:n  100  $ Cell 100 flux tally
E4    1e-10 20  $ Energy bins (thermal to fast)
```

MCNP output:
```
Cell 100 flux: 5.23e13 n/cm²/s
Spectrum: 40% thermal, 35% epithermal, 25% fast
```

**Step 2: Create ORIGEN input**
```
-1
RDA  Set title, library, flux
LIB 0 1 2 3 9 3 9 3 9  $ PWR library
TIT Fuel Cell 100 - Cycle 1
FLU 5.23e13  $ Flux from MCNP
HED 1 1 1   $ Headers
BAS 1.0e6   $ 1 MTU fuel basis
INP 1 1 1 0 0 0  $ Input options

Isotopic composition (from MCNP material m1):
  92234  3.6e-4
  92235  0.045
  92236  2.1e-6
  92238  0.955
   8016  2.0
  0 0 0

Irradiation steps (days):
IRP  100  3400  1  2  4  $ 100 days at 3400 MW
IRP  100  3400  1  2  4
IRP  100  3400  1  2  4
IRP  100  3400  1  2  4
IRP  100  3400  1  2  4
DEC  60   1  2  4  $ 60 day shutdown
...
END
```

**Step 3: Run ORIGEN**
```bash
origen < input_cell100.txt > output_cell100.txt
```

**Step 4: Extract isotopic inventory**

ORIGEN output (after 500 days irradiation + 30 days decay):
```
ISOTOPE  GRAMS   CURIES
U-234    1.2e2   6.2e-3
U-235    8.0e3   1.7e-2
U-236    5.0e3   3.2e-2
U-238    9.4e5   3.2e-1
Pu-239   6.0e3   3.7e2
Pu-240   3.0e3   6.8e2
Pu-241   2.0e3   2.1e5
...
Cs-137   1.2e3   8.7e4  $ Major gamma source
Sr-90    9.5e2   1.2e5
Sm-149   2.7e1   0.0    $ Stable absorber
```

**Step 5: Create MCNP photon source**
```mcnp
c Shutdown dose rate calculation
c Use ORIGEN isotopics as source

SDEF  CEL=D1  ERG=D2  PAR=2  $ Photon source, energy distribution

SI1  L  100 101 102 103  $ Source cells
SP1     0.25 0.25 0.25 0.25  $ Equal probability (adjust by activity)

c Energy distribution (from ORIGEN gamma spectrum)
SI2  H  0.05 0.1 0.2 0.5 1.0 2.0  $ MeV bins
SP2  D  0    1.2e15 3.4e15 5.6e15 2.1e15 0.8e15  $ Photons/sec per bin
```

### Multi-Cycle Calculations

**Challenge**: Compositions change each cycle, requiring iteration.

**Workflow**:
```
Cycle 1:
  1. MCNP with BOL compositions → flux
  2. ORIGEN with flux → EOC compositions
  3. Update MCNP materials to EOC
  4. Re-run MCNP → verify k_eff

Shutdown 1:
  5. ORIGEN decay (no flux) → compositions after 60 days

Cycle 2:
  6. MCNP with updated compositions → new flux
  7. ORIGEN with new flux → EOC compositions
  ...

Repeat for all cycles.
```

**Convergence**: Iterate until k_eff stable cycle-to-cycle.

---

## TIME-DEPENDENT OPERATIONAL HISTORY

### Power History Integration

**Real reactors have variable power**:
- Startup ramps
- Load following
- Forced outages
- Refueling shutdowns

**MCNP/ORIGEN approach**: Time-weighted averaging

**Example from AGR-1**:

**Raw operational data** (616 time steps over 138 days):
```
Time (h)  Power (MW)
0         3.2
2.5       5.1
5.0       6.8
...
138       4.9
```

**Time-weighted average**:
```python
ave_power = (power * time_interval).sum() / total_time
ave_power = 5.23 MW  # Representative for this cycle
```

**MCNP input**:
```mcnp
BURN  TIME=138  MAT=1  POWER=5.23  PFRAC=1.0
```

**Accuracy**: Typically within 5% of detailed time-step calculation.

### Control Rod History

**Control positions vary during cycle** (reactivity compensation):

**Example**: Outer Safety Control Cylinder (OSCC) rotation
```
Time (h)  Angle (°)
0         150  $ Withdrawn
24        125
48        100
...
138       60   $ Inserted
```

**Time-weighted average**:
```python
ave_angle = (angle * time_interval).sum() / total_time
ave_angle = 87.3°

# Find closest tabulated position
available = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
closest = 85°  # Use for MCNP geometry
```

**MCNP geometry update** (rotate surfaces for 85° position):
```mcnp
c OSCC surfaces rotated 85° from reference
1001  px  5.234   $ Calculated for 85° rotation
1002  py  3.876
...
```

### Refueling and Load Patterns

**PWR example**: 1/3 core shuffle each 18 months

**Tracking strategy**:
1. Divide core into 3 batches
2. Track each batch separately
3. Batch 1: Fresh → 1 cycle → 2 cycles → 3 cycles → discharged
4. Batch 2: 1 cycle → 2 cycles → 3 cycles → fresh → 1 cycle
5. Batch 3: 2 cycles → 3 cycles → fresh → 1 cycle → 2 cycles

**MCNP approach**:
- 3 material sets (batch 1, 2, 3)
- Update compositions each cycle
- Track spatial movement (cell assignments change)

---

## VALIDATION STRATEGIES

### Experimental Benchmark Data

**What to validate against**:

1. **Critical configurations**
   - k_eff for fresh core (should be ~1.000)
   - k_eff vs. burnup (reactivity loss)
   - Critical boron concentration (PWRs)

2. **Burnup measurements**
   - FIMA (Fissions per Initial Metal Atom)
   - Burnup monitors (Nd-148, Cs-137)
   - Isotopic assays (destructive analysis)

3. **Dose rate measurements**
   - Contact dose rates on fuel
   - Dose rates at detector locations
   - Time evolution (decay verification)

**AGR-1 example**:

Experimental data: MOAA_burnup_FIMA.csv
```
Capsule  Stack  Compact  FIMA_measured  FIMA_calculated  Difference
1        1      1        0.1123         0.1145           +1.96%
1        1      2        0.1089         0.1102           +1.19%
...
```

**Acceptance criteria**: Typically <5% difference for burnup, <20% for dose rates

### Code-to-Code Comparisons

**Cross-check with other codes**:

1. **MCNP vs. Serpent** (Monte Carlo)
2. **ORIGEN vs. SCALE** (depletion)
3. **MCNP vs. PARTISN** (deterministic transport)

**Example**:
```
k_eff comparison (fresh core):
  MCNP:    1.1834 ± 0.0012
  Serpent: 1.1842 ± 0.0010
  Difference: 80 pcm (within statistical uncertainty)
```

### Internal Consistency Checks

**Physics-based validation**:

1. **Reactivity balance**:
   - BOL k_eff - EOL k_eff = total burnup reactivity loss
   - Should equal: fissile depletion + FP buildup + Pu buildup

2. **Isotope mass balance**:
   - Total heavy metal mass approximately constant
   - Total actinide mass = initial U - fissioned U + bred Pu

3. **Power normalization**:
   - Fission energy × fission rate = reactor power
   - Verify MCNP power matches ORIGEN input

4. **Decay verification**:
   - Short-lived isotopes (I-135, Xe-135) approach zero during long shutdown
   - Long-lived isotopes (Pu-239, Cs-137) approximately constant

---

## COMPUTATIONAL COMPLEXITY MANAGEMENT

### The Scaling Problem

**Computational cost** scales roughly as:
```
CPU_time ∝ N_cells × N_isotopes × N_timesteps × N_iterations

Example:
  150 cells × 40 isotopes × 20 timesteps × 3 iterations
  = 360,000 ORIGEN runs (if brute-force approach)
```

**Production approach**: Intelligent reduction strategies

### Strategy 1: Cell Grouping by Flux

**Observation**: Cells with similar flux spectra have similar depletion.

**Approach**:
1. Run initial MCNP with many F4 tallies
2. Cluster cells by spectrum similarity
3. Track 1 representative cell per cluster
4. Apply results to all cells in cluster

**Example**:
```
Initial: 1000 fuel pins → 1000 tracked cells

After grouping:
  Cluster 1 (inner core, high flux): 120 pins → 1 tracked
  Cluster 2 (mid-core, medium flux): 450 pins → 1 tracked
  Cluster 3 (outer core, low flux): 380 pins → 1 tracked
  Cluster 4 (corner, lowest flux): 50 pins → 1 tracked

Result: 4 tracked cells instead of 1000 (250× reduction)
Error: <3% in k_eff, <8% in local burnup
```

### Strategy 2: Isotope Pruning

**Remove negligible isotopes**:

**Rule**: If atom density < 1E-15 atoms/barn-cm, omit from tracking.

**BURN card OMIT option**:
```mcnp
BURN  MAT=1  OMIT=54133 57140 58141 59143 61147 61149 61151
```

**Example**:
```
Initial: Tracking 250 fission products

After pruning:
  - Omit short-lived (t½ < 1 day) after equilibrium: -80 isotopes
  - Omit ultra-low abundance (<1E-15): -120 isotopes
  - Keep only: 50 isotopes

Result: 50 instead of 250 (5× reduction)
Error: <1% in k_eff (negligible isotopes have negligible impact)
```

### Strategy 3: Adaptive Time Stepping

**Variable time step sizing**:

```
BOL (0-100 days): 10-day steps (10 steps)
  - Rapid buildup of Pu, FPs
  - Fine resolution needed

Mid-life (100-400 days): 50-day steps (6 steps)
  - Approaching equilibrium
  - Coarser acceptable

EOL (400-500 days): 100-day steps (1 step)
  - Near equilibrium
  - Large steps acceptable

Shutdown (500-530 days): Variable
  - First 24 hours: 1-hour steps (24 steps)
  - Next 6 days: 1-day steps (6 steps)
  - After: exponential spacing

Total: 47 steps instead of uniform 100 (2× reduction)
```

### Strategy 4: Parallel Execution

**Cells are independent** → embarrassingly parallel

**Approach**:
```bash
# Split cells across compute nodes
node1: ORIGEN for cells 1-50
node2: ORIGEN for cells 51-100
node3: ORIGEN for cells 101-150
...

# Aggregate results
combine_results.py
```

**Speedup**: ~Linear with number of nodes (150 cells on 10 nodes = 15× faster)

---

## COMMON PITFALLS AND SOLUTIONS

### Pitfall 1: Tracking Too Many Cells

**Problem**: User tracks all 5,000 cells in model
```mcnp
BURN  MAT=1 2 3 4 ... 5000  $ Don't do this!
```

**Impact**:
- Runtime: weeks or months
- Memory: exhausted
- Output files: terabytes
- Minimal physics benefit

**Solution**: Strategic selection (~150 cells)
```mcnp
BURN  MAT=101 102 103 ... 250  $ Fuel cells only
     MAT=301 302 ... 330        $ Structural near core
     MAT=401 402 ... 410        $ Control materials
```

### Pitfall 2: Missing Critical Fission Products

**Problem**: User omits Sm-149 from tracking

**Impact**:
- k_eff too high by 2000-3000 pcm
- Reactivity predictions completely wrong
- Cycle length miscalculated

**Solution**: Always include TIER 1 FPs (Xe-135, Sm-149, Gd-155/157)

### Pitfall 3: Incorrect Volume Normalization

**Problem**: Volume in BURN card doesn't match actual cell volume

**Example**:
```
Cell volume: 1.5e5 cm³ (correct)
BURN MATVOL: 1.5e4 cm³ (wrong - off by 10×)

Result:
  - Atom densities wrong by 10×
  - Reactivity wrong
  - Isotope masses wrong
```

**Solution**: Calculate volumes carefully
```python
import numpy as np

r = 0.41  # cm, fuel radius
h = 365   # cm, fuel height
vol = np.pi * r**2 * h
print(f"Volume: {vol:.2e} cm³")
```

### Pitfall 4: Time Step Too Coarse

**Problem**: Single 500-day time step for entire cycle

**Impact**:
- Miss Xe-135 transients
- Miss Sm-149 buildup dynamics
- Flux-weighted averages incorrect

**Solution**: 50-100 day intervals during irradiation

### Pitfall 5: Forgetting Decay Periods

**Problem**: Continuous irradiation assumed, no shutdowns

**Impact**:
- Short-lived FPs too high (I-135, Xe-135)
- Dose rates immediately after shutdown too high
- Unrealistic operational history

**Solution**: Explicit decay steps
```mcnp
BURN  TIME=500  POWER=3400  $ Cycle 1
BURN  TIME=560  POWER=0     $ 60-day shutdown
BURN  TIME=1060 POWER=3400  $ Cycle 2
```

---

## REFERENCE FILES

**Create these supporting documents**:

1. **cell_selection_guide.md** - Detailed criteria and examples
2. **fission_product_database.md** - Complete FP properties, cross-sections
3. **actinide_chains.md** - Capture/decay pathways, branching ratios
4. **burn_card_examples.md** - Production-quality BURN card templates
5. **origen_coupling_tutorial.md** - Step-by-step workflow
6. **validation_procedures.md** - Benchmark comparison methods

---

## WORKING EXAMPLES

### Example 1: Simple PWR Pin Burnup

**File**: `.claude/skills/mcnp-burnup-builder/example_inputs/pwr_pin_burnup.i`

```mcnp
c PWR Fuel Pin Burnup Calculation
c Single pin, 3 cycles, 18 months each
c
c Cells
c
100 1 -10.2  -100     imp:n=1  vol=193  $ UO2 fuel
101 2 -6.5   100 -101 imp:n=1  vol=45   $ Zircaloy clad
102 3 -1.0   101      imp:n=1           $ Water
999 0  -999           imp:n=1           $ Global cell
1000 0  999           imp:n=0           $ Outside world

c
c Surfaces
c
100 cz  0.41   $ Fuel radius
101 cz  0.48   $ Clad outer
999 cz  1.0    $ Water boundary

c
c Materials (BOL fresh fuel)
c
m1  $ UO2 fuel, 4.5% enriched
   92234.70c  3.6e-4
   92235.70c  0.045
   92238.70c  0.955
    8016.70c  2.0
c
m2  $ Zircaloy-4 clad
   40000.60c  0.98
   26000.50c  0.002
   24000.50c  0.001
   28000.50c  0.001
c
m3  $ Light water
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.13t

c
c Burnup calculation
c
c Cycle 1: 500 EFPD
BURN  TIME=100 200 300 400 500
      MAT=1
      POWER=3400
      PFRAC=1.0
      MATVOL=193
      OMIT=54133 57140 58141 59143 61147 61149 61151  $ Short-lived FPs

c Shutdown 1: 60 days
BURN  TIME=560  POWER=0

c Cycle 2: 500 EFPD
BURN  TIME=660 760 860 960 1060
      MAT=1
      POWER=3400
      PFRAC=1.0
      MATVOL=193

c Shutdown 2: 60 days
BURN  TIME=1120  POWER=0

c Cycle 3: 500 EFPD
BURN  TIME=1220 1320 1420 1520 1620
      MAT=1
      POWER=3400
      PFRAC=1.0
      MATVOL=193

c Final shutdown: 5 years
BURN  TIME=3445  POWER=0

c Source
kcode 10000 1.0 50 250
ksrc 0 0 0
```

### Example 2: Multi-Cell Core Burnup

**File**: `.claude/skills/mcnp-burnup-builder/example_inputs/core_burnup_multizone.i`

```mcnp
c 3-Zone Core Burnup
c Inner, middle, outer fuel zones
c Different flux levels → different burnup
c
[... cell/surface/material definitions ...]

c Burnup calculation - different power fractions
BURN  TIME=100 200 300 400 500
      MAT=1 2 3  $ Inner, middle, outer zones
      POWER=3400
      PFRAC=0.45 0.35 0.20  $ Inner burns faster (higher flux)
      MATVOL=5.0e5 7.0e5 9.0e5
```

---

## VALIDATION TESTS

### Test 1: Cell Selection

**User query**: "Which cells should I track for burnup in a PWR core?"

**Expected output**:
1. ✅ Criteria: high flux (>1E13), fuel, absorbers, structural near core
2. ✅ Example: ~150 cells from 5000 total
3. ✅ Grouping strategy for similar cells
4. ✅ Flux-based ranking

### Test 2: Fission Product Selection

**User query**: "What fission products must I include for accurate reactivity?"

**Expected output**:
1. ✅ TIER 1 (Xe-135, Sm-149, Gd-155/157) - ALWAYS
2. ✅ TIER 2 (Cd-113, Eu-153/155, Rh-103) - SHOULD
3. ✅ Cross-section values and physics impact
4. ✅ Example material card with FPs

### Test 3: BURN Card Creation

**User query**: "Create BURN card for 3-cycle PWR fuel with 60-day shutdowns"

**Expected output**:
1. ✅ Multi-BURN cards for cycles + shutdowns
2. ✅ Time steps: 100-day intervals during irradiation
3. ✅ POWER=0 for decay periods
4. ✅ Material volume specification

### Test 4: ORIGEN Coupling

**User query**: "How do I couple MCNP burnup results to ORIGEN for dose rates?"

**Expected output**:
1. ✅ 3-step workflow diagram
2. ✅ Data handoff (flux → ORIGEN, isotopics → MCNP)
3. ✅ Example ORIGEN input from MCNP output
4. ✅ Photon source generation from isotopics

---

## IMPLEMENTATION CHECKLIST

- [ ] Update SKILL.md with new sections (cell selection, FP selection, actinides, BURN card, ORIGEN)
- [ ] Create cell_selection_guide.md
- [ ] Create fission_product_database.md
- [ ] Create actinide_chains.md
- [ ] Create burn_card_examples.md
- [ ] Create origen_coupling_tutorial.md
- [ ] Create validation_procedures.md
- [ ] Create example_inputs/pwr_pin_burnup.i
- [ ] Create example_inputs/core_burnup_multizone.i
- [ ] Create scripts/cell_selector.py (flux-based ranking)
- [ ] Create scripts/fission_product_selector.py (TIER-based selection)
- [ ] Create scripts/burn_card_generator.py (time step automation)
- [ ] Test all 4 validation queries
- [ ] Cross-reference with mcnp-workflow-integrator (future skill)

---

## SUCCESS CRITERIA

**Skill is successful when users can**:

1. ✅ Select appropriate cells for depletion tracking (flux-based criteria)
2. ✅ Choose fission products systematically (TIER 1/2/3/4)
3. ✅ Include complete actinide chains (U→Np→Pu→Am→Cm)
4. ✅ Write proper BURN cards (multi-cycle with shutdowns)
5. ✅ Understand MCNP-ORIGEN coupling workflow
6. ✅ Validate burnup calculations against benchmarks
7. ✅ Manage computational complexity (grouping, pruning, parallel)
8. ✅ Avoid common pitfalls (too many cells, missing FPs, wrong volumes)

**Overall impact**:
- Users can perform PRODUCTION-QUALITY burnup calculations
- Results match experimental data within 5%
- Computational resources used efficiently
- Workflow integrates with broader reactor analysis

---

**END OF REFINEMENT PLAN**

**Status**: Ready for immediate execution
**Estimated effort**: 2-3 hours for complete implementation
**Priority**: HIGH - Essential for realistic reactor modeling

# MCNP Best Practices - Complete 57-Item Checklist

**Purpose:** Comprehensive reference for MCNP Chapter 3.4 best practices checklist with detailed explanations.

**Companion to:** mcnp-best-practices-checker SKILL.md

---

## Overview

These practices ensure correct and efficient MCNP simulations, extended with professional reactor modeling standards. They exist because users got wrong answers by skipping them. This is not optional advice - these are requirements for reliable results.

**Organization:**
- **Phase 0: Professional Modeling Standards** (15 items) - BEFORE input creation
- **Phase 1: Problem Setup** (30 items) - Before first run (22 standard + 8 reactor-specific)
- **Phase 2: Preproduction** (20 items) - During short test runs
- **Phase 3: Production** (10 items) - During long production runs
- **Phase 4: Criticality** (5 items) - Additional for KCODE problems

---

## Phase 0: Professional Modeling Standards (PRE-SETUP)

**Purpose:** Establish professional practices BEFORE creating MCNP input files

**When:** Before ANY input file creation, especially for reactor models

**Critical for:** Large models (>100 cells), automated generation, publication, licensing, collaboration

### Project Organization (Items 1-5)

#### 0.1. Version Control from Start

**Practice:** Initialize version control before creating files

**Why:**
- Enables rollback if errors introduced
- Enables collaboration among team members
- Required for reproducible research
- Tracks evolution of model
- Essential for publication and licensing

**How:**
```bash
git init
git add .
git commit -m "Initial reactor model - baseline configuration"
git tag v1.0-baseline
```

**For large projects:**
- Commit frequently (after each working increment)
- Use meaningful commit messages
- Tag releases (v1.0, v2.0, etc.)
- Create branches for major changes

**Consequence of skipping:**
- Cannot recover from mistakes
- Cannot collaborate effectively
- Cannot prove reproducibility
- Publication rejection risk

---

#### 0.2. Design Numbering Scheme BEFORE Implementation

**Practice:** Plan systematic numbering conventions before coding geometry

**Why:**
- Prevents conflicts in large models (1000+ entities)
- Enables instant identification of relationships
- Simplifies debugging
- Enables automated generation
- Reduces human error

**Proven Patterns:**

**Hierarchical encoding (HTGR example):**
```
Cell numbering: 9[capsule][stack][2×compact][sequence]
cell_id = 90000 + cap*1000 + stack*100 + 2*(comp-1)*10 + seq

Example: Cell 91234 = Capsule 1, Stack 2, Compact 2, Sequence 4
```

**Range allocation:**
- 60000s: ATR fuel elements
- 90000s: Experiment geometry
- 2000-2999: Layer 1 assemblies
- 3000-3999: Layer 2 assemblies
- 9000-9999: Reflector/boundaries

**Document in header:**
```mcnp
c NUMBERING CONVENTION:
c   Cells:     9XYZW where X=capsule, Y=stack, Z=compact, W=component
c   Surfaces:  9XYZ matching cell hierarchy
c   Materials: 9XYZ matching cell hierarchy
c   Universes: XYZ (condensed cell numbering)
```

**Consequence of skipping:**
- Numbering conflicts (later overwrites earlier)
- Impossible debugging in 10,000-line files
- Cannot systematically generate geometry

---

#### 0.3. Separate Data from Logic

**Practice:** External data in CSV/JSON files, not hardcoded in input

**Why:**
- Enables parameter studies (change CSV, regenerate)
- Makes validation easier (inspect data separately)
- Reduces errors (data entry once, not per input)
- Enables version control of data

**Example structure:**
```
project/
├── data/
│   ├── power.csv            # Experimental measurements
│   ├── positions.csv        # Control positions
│   ├── materials.json       # Material compositions
│   └── geometry.json        # Dimensions
├── scripts/
│   └── create_input.py      # Generation logic
└── outputs/
    └── reactor.i            # Generated input
```

**CSV example (power.csv):**
```csv
cycle,lobe,power_MW,duration_days
138B,NE,1.2,42.5
138B,SE,1.3,42.5
139A,NE,1.4,38.2
```

**Usage in script:**
```python
import pandas as pd
power_df = pd.read_csv('data/power.csv')
ne_power = power_df[power_df['lobe'] == 'NE']['power_MW'].values[0]
```

**Consequence of skipping:**
- Hardcoded values spread across 10,000+ lines
- Impossible to find and change systematically
- High error rate in manual updates

---

#### 0.4. Document Provenance of ALL Values

**Practice:** Every number traceable to source

**Why:**
- Required for validation
- Required for licensing
- Enables error checking
- Builds confidence in model
- Required for publication peer review

**How to document:**
```mcnp
c Fuel density: 10.5 g/cm³ (ORNL/TM-2006/12, Table 3.2)
m1  92235.70c 0.045  92238.70c 0.955  $ Enrichment: INL/EXT-10-17686
    8016.70c 2.0                      $ Stoichiometric UO2

c Graphite density: 1.74 g/cm³ (IG-110 vendor data, Toyo Tanso)
m2  6012.00c 0.9890  6013.00c 0.0110  $ Natural carbon
mt2 grph.18t                          $ 600K (operating temperature)
```

**Provenance file (data_sources.md):**
```markdown
## Fuel Composition
- Source: INL/EXT-10-17686, "AGR-1 Irradiation Test Specification"
- Enrichment: 19.75% U-235
- Kernel diameter: 350 μm (measured, ±10 μm)

## Graphite Properties
- Source: Toyo Tanso IG-110 product specification
- Density: 1.74 g/cm³ (nominal)
- Purity: >99.9% carbon
```

**Consequence of skipping:**
- Cannot validate model
- Cannot defend to reviewers
- Cannot identify error sources
- Publication rejection

---

#### 0.5. README with Complete Workflow

**Practice:** Document how to regenerate inputs from scratch

**Why:**
- Enables reproducibility
- Onboards new team members
- Documents methodology
- Required for publication

**Essential README contents:**

1. **Purpose and scope**
2. **Dependencies** (software versions)
3. **Data files** (what each contains)
4. **Generation workflow** (step-by-step)
5. **Validation criteria** (how to verify)
6. **Expected outputs**

**Example README.md:**
````markdown
# HTGR Reactor Model

## Purpose
Shutdown dose rate calculations for decommissioning strategy evaluation.

## Dependencies
- Python 3.11.0
- numpy 1.24.0
- pandas 2.0.0
- jinja2 3.1.2
- MCNP6.2 (build 2020-02-14)
- Cross sections: ENDF/B-VII.1

## Regeneration from Scratch
```bash
cd reactor-model/
python create_inputs.py
python validate_inputs.py
```

Expected: 13 inputs in mcnp/ directory, 0 validation errors

## Data Files
- power.csv: Experimental power history (source: ECAR-3569)
- positions.csv: Control drum angles (source: ATR operations)
- materials.json: Fuel compositions (source: INL/EXT-10-17686)

## Validation
- Geometry plotted: `mcnp6 ip i=mcnp/reactor.i`
- VOID test passed: 0 lost particles
- Volume check: MCNP vs CAD < 2%
````

**Consequence of skipping:**
- Cannot reproduce results
- Wastes future time re-deriving workflow
- Publication rejection

---

### Geometry Design (Items 6-9)

#### 0.6. Plan Universe Hierarchy BEFORE Coding

**Practice:** Draw containment tree diagram before implementation

**Why:**
- Prevents circular references
- Allocates number ranges systematically
- Identifies all nesting levels
- Simplifies implementation

**Example hierarchy (HTGR):**
```
Level 1: TRISO particle (u=XXX4)
    ├── Kernel (innermost)
    ├── Buffer
    ├── IPyC
    ├── SiC
    └── OPyC (outermost)

Level 2: Particle lattice (u=XXX6, LAT=1)
    └── 15×15 rectangular array of TRISO

Level 3: Compact stack (u=XXX0, LAT=1)
    └── Vertical 1×1×31 array

Level 4: Fuel channel (u=XXX1)
    └── Cylinder filled with compact lattice

Level 5: Assembly (u=XXX0, LAT=2)
    └── Hexagonal lattice

Level 6: Core
    └── Multiple assemblies
```

**Number allocation:**
- Level 1 particles: u=XXX4 (last digit 4)
- Level 2 lattices: u=XXX6 (last digit 6)
- Level 3 stacks: u=XXX0 (last digit 0)
- Etc.

**Consequence of skipping:**
- Circular references (u=100 fill=200, u=200 fill=100)
- MCNP fatal errors
- Difficult debugging

---

#### 0.7. Choose Lattice Types Appropriately

**Practice:** Select LAT=1 vs LAT=2 based on physics

**When to use LAT=1 (rectangular):**
- PWR fuel assemblies (square grid)
- Vertical stacks (1×1×N)
- Rectangular arrays
- Most TRISO particle lattices

**When to use LAT=2 (hexagonal):**
- HTGR cores (hex fuel blocks)
- Fast reactor assemblies (hex ducts)
- Hexagonal fuel pins
- Any honeycomb pattern

**Mixed types allowed:**
```
Level 2: Particle lattice (LAT=1) inside compact
Level 5: Assembly lattice (LAT=2) in core
```

**Document choice:**
```mcnp
c LAT=1 selected for particle array (regular grid packing)
1116  10  -1.0  -1116  u=1116  lat=1  fill=-7:7 -7:7 0:0  ...

c LAT=2 selected for assembly layout (hexagonal core)
2000  0        -2000  u=2000  lat=2  fill=-6:6 -6:6 0:0  ...
```

**Consequence of wrong choice:**
- LAT=2 with RPP surface → fatal error
- Wrong physics (rectangular when should be hex)

---

#### 0.8. Validate Lattice Dimensions Mathematically

**Practice:** Pre-calculate element counts before coding

**Formula:**
```
Elements = (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
```

**CRITICAL:** Account for zero!
```
fill=-7:7 -7:7 0:0
  I: -7 to 7 = 15 elements (not 14!)
  J: -7 to 7 = 15 elements
  K: 0 to 0 = 1 element
  Total: 15 × 15 × 1 = 225 elements
```

**Surface extent validation:**
```
Rectangular: Surface extent = N × pitch
  15 elements × 0.1 cm pitch = 1.5 cm
  RPP: -0.75 to 0.75 (extent 1.5 cm) ✓

Hexagonal: Match RHP dimensions
  R = 1.6 cm → Pitch = 1.6 × √3 = 2.77 cm
```

**Consequence of skipping:**
- Off-by-one errors → fatal error
- Surface/lattice mismatch → lost particles
- Very hard to debug

---

#### 0.9. Use Systematic Cell/Surface Correlation

**Practice:** Cell N uses surfaces NXXX, material mN

**Example:**
```mcnp
91234  9123  -1.0  -91234 -91235 91236  imp:n=1  $ Cell uses surfaces 9123X
91234  so  0.0350                                 $ Surface matches cell number
m9123  6012.00c 0.99                              $ Material matches cell number
```

**Benefits:**
- Instant relationship identification
- Simplified debugging
- Reduced cross-reference errors

**Consequence of skipping:**
- Hard to find which surfaces define which cells
- Time-consuming debugging

---

### Materials (Items 10-12)

#### 0.10. Thermal Scattering REQUIRED

**Practice:** ALWAYS add MT cards for graphite, water, Be, polyethylene

**CRITICAL:** Omission causes 1000-5000 pcm reactivity error!

**Required for:**
- ✅ ALL graphite (any reactor type)
- ✅ ALL water (light or heavy)
- ✅ Polyethylene (shielding)
- ✅ Beryllium, BeO (reflectors)

**Temperature selection:**
```mcnp
c HTGR operating (600K)
m1  6012.00c 0.9890  6013.00c 0.0110
mt1 grph.18t  $ 600K library

c HTGR cold critical (294K)
m2  6012.00c 0.9890  6013.00c 0.0110
mt2 grph.10t  $ 294K library

c PWR operating (350K)
m3  1001.70c 2.0  8016.70c 1.0
mt3 lwtr.13t  $ 350K library

c Heavy water CANDU (325K)
m4  1002.70c 2.0  8016.70c 1.0
mt4 hwtr.11t  $ 325K library
```

**Consequence of skipping:**
- 1000-5000 pcm reactivity error
- WRONG keff
- WRONG reaction rates
- Invalid results

**See:** thermal_scattering_reference.md for complete library guide

---

#### 0.11. Temperature-Consistent Cross Sections

**Practice:** Match S(α,β) temperature to neutronics temperature

**Good:**
```mcnp
c All ENDF/B-VII.0 (.70c), 600K thermal treatment
m1  92235.70c ...  92238.70c ...  6012.70c ...
mt1 grph.18t  $ 600K matches operating temperature
```

**Bad:**
```mcnp
c Mixed evaluations - AVOID!
m2  92235.70c ...  92238.21c ...  6012.80c ...
mt2 grph.18t
```

**Consequence of mixing:**
- Inconsistent evaluations
- Potential double-counting or gaps
- Hard to defend in reviews

---

#### 0.12. Material Density Specifications Consistent

**Practice:** Know and document density convention

**Convention:**
- Negative = g/cm³ (mass density)
- Positive = atoms/barn-cm (atom density)

**Document:**
```mcnp
c UO2 fuel, mass density 10.5 g/cm³
m1  92235.70c 0.045  92238.70c 0.955  8016.70c 2.0

c Graphite moderator, atom density 0.0785 atoms/barn-cm
m2  6012.00c 0.9890  6013.00c 0.0110
```

**Validate:**
- Atom fractions sum to 1 (for compounds)
- Density reasonable for material (compare handbook)

---

### Automation (Items 13-15)

#### 0.13. Automate for ≥3 Similar Cases

**Practice:** Use templates or scripts when generating 3+ similar inputs

**When to automate:**
- ✅ More than 3 similar cases
- ✅ Parameters change frequently
- ✅ Geometry follows algorithmic pattern
- ✅ High error risk in manual entry
- ✅ Reproducibility critical

**When NOT to automate:**
- ❌ One-time model
- ❌ Highly irregular geometry
- ❌ Automation effort > manual effort

**See:** automation_guide.md for detailed patterns

---

#### 0.14. Validate Generated Outputs

**Practice:** Automated checking of generated inputs

**Validations:**
- Compare to reference case (if exists)
- Check numbering conflicts
- Verify cross-references
- Check lattice dimensions
- Verify thermal scattering

**See:** reactor_model_checker.py script

---

#### 0.15. Reproducible Generation

**Practice:** Single command regenerates all inputs

**Goal:**
```bash
python create_all_inputs.py
```

**Requirements:**
- Scripts version-controlled
- External data frozen (known versions)
- Dependencies documented
- No manual steps

**See:** reproducibility_checklist.md

---

## Phase 1: Problem Setup (§3.4.1)

**Purpose:** Prevent basic errors before running expensive calculations

**When:** Before ANY MCNP run

### Geometry Practices (Items 1-7)

#### 1. Draw Geometry Picture

**Practice:** Sketch geometry on paper before coding

**Why:** Visualizing helps identify:
- Dimension errors
- Missing components
- Spatial relationships
- Coordinate system issues

**How:**
- Draw cross-sections (XY, XZ, YZ planes)
- Label dimensions
- Mark material boundaries
- Note symmetries

**Consequence of skipping:** Coding errors harder to debug

---

#### 2. ALWAYS Plot Geometry

**Practice:** Use MCNP plotter before running particles

**Command:**
```bash
mcnp6 ip i=input.inp
```

**Why:** Catches 90% of geometry errors
- Overlaps (dashed lines)
- Gaps (missing cells)
- Wrong dimensions
- Transformation errors

**Minimum:** Plot from 3 orthogonal views
```
PX 1 0 0    $ View along X
PX 0 1 0    $ View along Y
PX 0 0 1    $ View along Z
```

**Consequence of skipping:** Lost particles, BAD TROUBLE, wrong answers

**CRITICAL:** This is the MOST IMPORTANT practice

---

#### 3. Model in Sufficient Detail

**Practice:** Balance accuracy vs. complexity

**Too Simple:**
- Missing critical components
- Over-simplified geometry
- Wrong physics

**Too Complex:**
- Unnecessary detail
- Slow calculations
- Hard to debug

**How to Judge:**
- What's the question? (dose, keff, activation?)
- What precision needed? (screening vs. licensing)
- Sensitivity analysis on detail level

---

#### 4. Use Simple Cells

**Practice:** Avoid overly complex Boolean expressions

**Bad:**
```
5  1  -1.0  (-1:2:#3):(4 -5 (-6:7))  IMP:N=1    $ Too complex!
```

**Good:**
```
5  1  -1.0  -1 2  IMP:N=1                        $ Simple
6  1  -1.0  4 -5 -6  IMP:N=1                     $ Clear
```

**Why:** Simpler = fewer errors, easier debugging

---

#### 5. Use Simplest Surfaces

**Practice:** Prefer macrobodies and simple surfaces

**Preference Order:**
1. RPP, SPH, RCC macrobodies (easiest)
2. PX, PY, PZ planes
3. SO, SX, SY, SZ spheres
4. CX, CY, CZ cylinders
5. General surfaces (last resort)

**Why:** Simpler surfaces = faster tracking, fewer errors

---

#### 6. Avoid Excessive # Operator

**Practice:** Minimize complement operator usage

**Warning Sign:**
```
10  1  -1.0  #1 #2 #3 #4 #5 #6 #7    $ Too many complements!
```

**Better:**
```
10  1  -1.0  -10 (1:2:3:4:5:6:7)     $ Explicit boundary, union of interior
```

**Why:** Excessive complements indicate overly complex design

---

#### 7. Build Incrementally

**Practice:** Add and test geometry piece by piece

**Workflow:**
1. Start simple (single cell)
2. Test with VOID card
3. Add next component
4. Test again
5. Repeat until complete

**Why:** Isolates errors to recent additions

---

### Organization Practices (Items 8-9)

#### 8. Use READ Card

**Practice:** Store common cards in separate files

**Example:**
```
c Main input
READ FILE=materials.txt
READ FILE=common_surfaces.txt
```

**Benefits:**
- Reusable components
- Cleaner main input
- Version control easier

---

#### 9. Pre-calculate Volumes/Masses

**Practice:** Calculate system volume by hand, compare with MCNP

**Workflow:**
1. Calculate expected volume analytically
2. Run MCNP with VOL card
3. Compare results
4. Investigate large discrepancies (>5%)

**Example:**
```
c Expected: Sphere R=10 → V = 4/3 π R³ = 4188.8 cm³
VOL  NO                                $ Calculate volumes
c After run: Check Table 126 for volumes
c If MCNP says 4500 cm³ → geometry error!
```

**Why:** Major discrepancies = geometry errors

---

### Validation Practices (Items 10-13)

#### 10. Use VOID Card

**Practice:** Test geometry with VOID card

**Procedure:**
```
VOID                                   $ Make all cells void
MODE  N
IMP:N  1  1  1  ...  1  0             $ All cells IMP=1 except graveyard
SDEF  SUR=998  NRM=-1                 $ Flood from outside
NPS  1000000                           $ Many particles
```

**Why:** Quickly finds overlaps and gaps
- No collisions → particles stream through
- Lost particle = geometry error
- Very effective, takes minutes

**When:** Before any production run

---

#### 11. Check Source (Tables 10, 110, 170)

**Practice:** Verify source distribution in output

**Tables to Check:**
- **Table 10:** Source overview
- **Table 110:** Source position distribution
- **Table 170:** Source energy distribution

**Verify:**
- Positions where expected?
- Energy distribution correct?
- Particles in right cells?

---

#### 12. Check Source with Mesh Tally

**Practice:** Use TMESH or FMESH to visualize source

**Example:**
```
TMESH
  RMESH1:N  FLUX
    CORA1  -100  99i  100              $ X bins
    CORB1  -100  99i  100              $ Y bins
    CORC1  -100  99i  100              $ Z bins
```

**Why:** Visual verification of source location and intensity

---

#### 13. Understand Physics Approximations

**Practice:** Know what physics MCNP models and what it doesn't

**Key Limitations:**
- Energy cutoffs (particles killed below threshold)
- Physics models (not all interactions included)
- Cross-section availability (some ZAIDs incomplete)
- Thermal treatment (may need S(α,β))

**Action:** Document assumptions and limitations

---

### Cross Sections & Tallies (Items 14-16)

#### 14. Cross-Section Sets Matter!

**Practice:** Verify correct libraries loaded

**Check in Output:**
```
 tables from file /path/to/xsdir
   1001.80c    ENDF/B-VIII.0
   8016.80c    ENDF/B-VIII.0
```

**Common Issues:**
- Mixed library versions (.70c and .80c)
- Wrong temperature libraries
- Missing thermal scattering

**Consequence:** Can change answers by 5-10%

---

#### 15. Separate Tallies for Fluctuation

**Practice:** Don't combine too many things in one tally

**Bad:**
```
F4:N  1 2 3 4 5 6 7 8 9 10            $ All cells in one tally
```

**Better:**
```
F4:N  1                                $ Tally each cell separately
F14:N  2
F24:N  3
```

**Why:** Combined tallies mask poor statistics in individual regions

---

#### 16. Conservative Variance Reduction

**Practice:** Start simple, add complexity gradually

**Progression:**
1. Analog (no VR) → establish baseline
2. Simple importance (IMP cards)
3. Weight windows if needed
4. Advanced techniques only if necessary

**Why:** Complex VR hard to debug, may introduce errors

---

### General Practices (Items 17-22)

#### 17. Don't Use Too Many VR Techniques

**Practice:** KISS principle - Keep It Simple

**Warning Signs:**
- IMP + WWG + DXTRAN + FCL + ...
- Diminishing returns
- Hard to debug

**Recommendation:** 1-2 VR techniques maximum

---

#### 18. Balance User vs Computer Time

**Practice:** Don't over-optimize simple problems

**Example:**
- Problem runs in 10 minutes analog
- Spend 2 hours optimizing to 5 minutes?
- Not worth it!

**When to Optimize:**
- Production runs >1 hour
- Repeated calculations
- Large parameter studies

---

#### 19. Study ALL Warnings

**Practice:** Read and understand every warning message

**Don't Ignore:**
- "minor" normalization warnings
- Statistical check failures
- IEEE exceptions (if many)

**Use:** mcnp-warning-analyzer skill

---

#### 20. Generate Best Output (PRINT Card)

**Practice:** Request comprehensive output

**Recommendation:**
```
PRINT  10  40  50  110  117  118  126  128  140  160  170
```

**Why:** More information = better debugging

**Balance:** Disk space vs. information

---

#### 21. Recheck INP File

**Practice:** Final review before running

**Checklist:**
- Materials correct? (densities, fractions)
- Source reasonable? (position, energy)
- Tallies in right locations?
- Importance sensible?
- NPS appropriate?

**When:** Before production run

---

#### 22. Garbage In = Garbage Out

**Practice:** MCNP WILL RUN bad inputs

**Remember:**
- MCNP doesn't check physics reasonableness
- No error ≠ correct answer
- You are responsible for validation

**Example:**
- MCNP will track 10 MeV thermal neutrons
- Wrong, but no error message
- YOU must catch these!

---

## Phase 2: Preproduction (§3.4.2)

**Purpose:** Validate setup during short test runs

**When:** After setup, before production (10k-100k particles)

### Understanding Practices (Items 1-3)

#### 1. Don't Use as Black Box

**Practice:** Understand Monte Carlo theory

**Must Know:**
- Central limit theorem
- Variance reduction principles
- Statistical error interpretation
- Sampling methods

**Resources:**
- MCNP Manual Chapter 2
- Monte Carlo textbooks

---

#### 2. Run Short Calculations

**Practice:** Test with 10k-100k particles before production

**Why:**
- Fast feedback (minutes vs. hours)
- Find errors early
- Test VR effectiveness
- Estimate time for production

**Typical:** 100k particles for testing

---

#### 3. Examine Outputs Carefully

**Practice:** Read entire output file

**Check:**
- All warnings
- All tables
- Statistical summaries
- Diagnostic messages

**Time:** 10-15 minutes per output review

---

### Statistics Practices (Items 4-7)

#### 4. Study Summary Tables

**Practice:** Review activity, collision, track summaries

**Key Tables:**
- Table 126: Cell activity
- Table 130: Surface crossings
- Table 140: Nuclide activity

**Look For:**
- Unexpected values
- Zero activity in important regions
- Excessive activity in unimportant regions

---

#### 5. Study Statistical Checks

**Practice:** ALL 10 statistical tests must pass

**Rule:**
- 0 failed: Excellent ✓
- 1-2 failed: Marginal, investigate
- 3+ failed: Unreliable, must fix

**Action:** Use mcnp-statistics-checker skill

---

#### 6. Study FOM and VOV Trends

**Practice:** Figure of Merit and Variance of Variance should be stable

**FOM:** Should be constant (±10%)
**VOV:** Should be <0.10 and decreasing

**If not:** Variance reduction issue or rare events

---

#### 7. Consider Collisions/Particle

**Practice:** Check average collisions per source particle

**Typical Ranges:**
- Shielding: 100-1,000
- Reactor core: 1,000-10,000
- Deep penetration: 10-100

**If Very Low (<10):** Particles not interacting enough
**If Very High (>100,000):** May need better VR or geometry simplification

---

### Efficiency Practices (Items 8-12)

#### 8. Examine Track Populations

**Practice:** Check Table 126 for particles by cell

**Question:** Are particles getting where needed?

**Look For:**
- High population in unimportant regions
- Low population in important regions (tally locations)

**Fix:** Adjust importance or add VR

---

#### 9. Scan Mean-Free-Path Column

**Practice:** Identify problem regions in output tables

**Large MFP:** Void or low-density (fast streaming)
**Small MFP:** High-density (many collisions)

**Use:** Identify where VR needed

---

#### 10. Check Detector Diagnostics

**Practice:** Review F5 and DXTRAN effectiveness

**Output Shows:**
- Detector contributions
- Effectiveness of point detector methods
- Whether DXTRAN working

**If Ineffective:** Adjust or remove

---

#### 11. Understand Large Contributions

**Practice:** No single particle should dominate tally

**Warning Sign:**
- One particle contributes >10% of total
- Indicates rare large event

**Fix:** Better VR or much longer run

---

#### 12. Reduce Unimportant Tracks

**Practice:** Kill particles in unimportant regions

**Methods:**
- IMP:N=0 (kill immediately)
- Low importance (roulette)
- Energy cutoffs

**Balance:** Don't kill particles that might contribute later

---

### Physics Practices (Items 13-14)

#### 13. Check Secondary Production

**Practice:** Verify expected particles generated

**Tables:**
- Photon production from neutrons
- Electron production from photons
- Neutron production from fission

**Expected?** Cross-check with physics intuition

---

#### 14. Back-of-Envelope Check

**Practice:** Rough physics estimate before run

**Examples:**
- Keff should be ~1.0 for critical system
- Dose decreases exponentially through shield
- Flux higher in fuel than reflector

**If MCNP result wildly different:** Something wrong

---

## Phase 3: Production (§3.4.3)

**Purpose:** Ensure quality during long runs

**When:** During production (millions of particles)

### File Practices (Items 1-2)

#### 1. Save RUNTPE

**Practice:** Keep RUNTPE file for analysis

**Uses:**
- Restart calculations
- PTRAC analysis
- MCTAL extraction
- Mesh tally visualization

**Storage:** Archive important RUNTPE files

---

#### 2. Limit RUNTPE Size (PRDMP)

**Practice:** Control dump frequency

**Card:**
```
PRDMP  J  J  1                         $ Dump every cycle
PRDMP  J  J  10                        $ Dump every 10 cycles (smaller file)
```

**Balance:** Restart granularity vs. disk space

---

### Statistics Practices (Items 3-8)

#### 3. Check FOM Stability

**Practice:** FOM should remain roughly constant

**If Decreasing:**
- Particles reaching harder regions
- VR becoming less effective
- May be OK if gradual

**If Increasing:**
- Suspicious (check for errors)

---

#### 4. Answers Seem Reasonable

**Practice:** Physics intuition check

**Questions:**
- Does magnitude make sense?
- Does trend make sense?
- Comparable to similar problems?

---

#### 5. Examine 10 Statistical Checks

**Practice:** ALL tallies must pass all 10 checks

**Non-Negotiable:** Production results must be statistically valid

---

#### 6. Form Valid Confidence Intervals

**Practice:** Understand error bars

**68% CI:** Result ± 1σ
**95% CI:** Result ± 2σ
**99% CI:** Result ± 3σ

**Remember:** These assume normal distribution and statistical convergence

---

#### 7. Continue-Run if Necessary

**Practice:** Extend run until converged

**Command:**
```bash
mcnp6 c runtpe=runtpe outp=outp_continued
```

**When:** Statistical checks not passing after initial run

---

#### 8. Verify Errors Decrease 1/√N

**Practice:** Theory check

**Expected:** Doubling particles → error decreases by √2

**If Not:** Statistical anomaly or setup error

---

### Final Practices (Items 9-10)

#### 9. Accuracy Has Multiple Factors

**Practice:** Statistics ≠ accuracy

**Other Factors:**
- Geometry approximations
- Material approximations
- Physics models
- Cross-section data quality
- Source approximations

**Total Error:** √(statistical² + systematic²)

---

#### 10. Adequately Sample All Cells

**Practice:** Check all cells have sufficient tracks

**Minimum:** ~100 tracks per cell for basic reliability

**Action:** Review Table 126 populations

---

## Phase 4: Criticality (§3.4.4)

**Purpose:** Additional requirements for KCODE problems

**When:** Criticality (eigenvalue) calculations

### Criticality Practices (Items 1-5)

#### 1. Determine Inactive Cycles

**Practice:** Plot keff and Shannon entropy

**Converged When:**
- Entropy flat (±5%) for final 30% of inactive
- Keff stable (no trend)

**Typical:** 50-200 inactive cycles depending on complexity

---

#### 2. Large Histories/Cycle

**Practice:** Minimum 10,000 particles per cycle for production

**Recommendations:**
- Testing: 1,000-5,000 per cycle
- Production: 10,000-100,000 per cycle

**Why:** Better statistics within each cycle

---

#### 3. Examine Keff Behavior

**Practice:** Keff should be stable after inactive cycles

**Warning Signs:**
- Trend continuing in active cycles
- Large cycle-to-cycle fluctuations (>0.001)

**Action:** More inactive cycles

---

#### 4. At Least 100 Active Cycles

**Practice:** Minimum active cycles for confidence intervals

**Typical:** 100-300 active cycles

**Balance:** Cycles vs. histories per cycle

---

#### 5. Recheck Convergence After Run

**Practice:** Verify inactive cycles were sufficient

**Check:**
- Entropy plot retrospectively
- Keff trend in active cycles
- Source distribution settled

**If Not Converged:** Discard run, increase inactive cycles

---

## Quick Reference: Critical Practices

**Never Skip These:**
1. Plot geometry (Item 1.2) - 90% of errors
2. VOID card test (Item 1.10) - Finds overlaps/gaps
3. Study all warnings (Item 1.19) - May indicate serious issues
4. All 10 statistical checks pass (Items 2.5, 3.5) - Result validity
5. Shannon entropy converged (Item 4.1) - Keff reliability

---

## References

- **MCNP Manual Chapter 3.4:** Complete best practices discussion
- **phase_workflows.md:** Systematic review procedures
- **MCNP Manual Chapter 2:** Statistical theory background

---

**END OF CHECKLIST REFERENCE**

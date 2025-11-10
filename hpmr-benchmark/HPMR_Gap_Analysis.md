# Heat Pipe Microreactor (HPMR) Gap Analysis
## Current MCNP Model vs. Reference Plant Specifications

**Current Model:** `/home/user/mcnp-skills/hpcmr-simplified.i`
**Reference:** INL HPMR Reference Plant Model + HPMR_Analysis_Overview.md
**Analysis Date:** 2025-11-08

---

## EXECUTIVE SUMMARY

The current MCNP model (`hpcmr-simplified.i`) implements the **core active region** with fuel assemblies, heat pipes, and radial reflector in a hexagonal lattice configuration. However, it is **incomplete and will not run** due to missing critical components: axial reflectors (top/bottom), control drums, source definition, and physics cards.

**Completeness:** ~40% implemented
**Status:** Model will NOT run as-is
**Priority Gaps:** 7 critical, 5 important, 3 nice-to-have

---

## 1. WHAT'S CURRENTLY IMPLEMENTED

### 1.1 Geometry Components Present ✓

| Component | Status | Details |
|-----------|--------|---------|
| **Fuel Pins** | ✓ Implemented | u=301, u=302 with 2 axial segments (z=20-100, z=100-180) |
| **Heat Pipes** | ✓ Implemented | u=320, homogenized SS316+Na, r=1.07 cm |
| **Pin Lattices** | ✓ Implemented | u=200, u=201 (9×9 hexagonal, LAT=2, pitch=2.782 cm) |
| **Fuel Assemblies** | ✓ Implemented | u=901 (w/ guide), u=902 (no guide), pitch=17.368 cm |
| **Core Lattice** | ✓ Implemented | u=102 (15×15 hexagonal, LAT=2) |
| **Active Core** | ✓ Implemented | Cell 102, z=20-180 cm (160 cm height) |
| **Radial Reflector** | ✓ Implemented | Cell 18, BeO, r=140-146.8 cm |
| **SS316 Shield** | ✓ Implemented | Cell 19, r=146.8-? cm |
| **Guide Tubes** | ✓ Implemented | u=20, r=3.2 cm, helium-filled |

**Geometry Hierarchy:** 4-level nested universe structure correctly implemented
- Level 1: Pin universes (u=301, u=302, u=320, u=20)
- Level 2: Pin lattices (u=200, u=201)
- Level 3: Assembly universes (u=901, u=902)
- Level 4: Core lattice (u=102)

### 1.2 Materials Defined ✓

| Material ID | Description | Density | S(α,β) Status |
|-------------|-------------|---------|---------------|
| **m201** | Graphite monolith (H-451) | -1.803 g/cm³ | ✓ grph.47t |
| **m300** | Helium gap | 2.4×10⁻⁴ atoms/b-cm | - |
| **m301** | Fuel lower segment | atoms/b-cm | ✓ grph.47t |
| **m302** | Fuel upper segment | atoms/b-cm | ✓ grph.47t |
| **m315** | Homogenized heat pipe | atoms/b-cm | - |
| **m401** | BeO radial reflector | -2.86 g/cm³ | ✓ be-beo, o-beo |
| **m411** | SS316 shield | atoms/b-cm | - |

**Material Quality:** Compositions match reference specifications, isotopics correct, temperatures appropriate (900-1200K).

### 1.3 Lattice Structures Present ✓

**Hexagonal Lattices (LAT=2):**
1. **Pin lattice (u=200, u=201):** 9×9 array, correctly filled with fuel (u=301/302) and heat pipes (u=320)
2. **Core lattice (u=102):** 15×15 array, correctly filled with assemblies (u=901, u=902)

**Fill Arrays:** Properly indexed for hexagonal coordinates (-4:4 -4:4 0:0 for pin, -7:7 -7:7 0:0 for core)

### 1.4 Universe Hierarchy ✓

**Nesting Structure:** Correctly implemented with negative universe numbers for filling:
- Fuel pins: u=-301, u=-302
- Heat pipes: u=-320
- Pin lattices: u=200, u=201 (filled into assemblies)
- Assemblies: u=-901, u=-902
- Core lattice: u=102 (filled into cell 102)

---

## 2. MISSING REACTOR COMPONENTS

### 2.1 CRITICAL GAPS (Model Will Not Run Without These)

#### **GAP 1: Bottom Reflector (z = 0-20 cm)** ❌ CRITICAL

**What's Missing:**
- Graphite H-451 reflector below active core
- Heat pipe holes extending through reflector
- Guide tube holes (for assemblies with u=901)
- Lattice structure matching core configuration

**Current Status:** Surfaces commented out (lines 155-156), cells not defined

**Specification from Reference:**
- Material: Graphite H-451 (m201 or m710)
- Thickness: 20 cm
- Axial position: z = 0-20 cm
- Configuration: Hexagonal lattice matching core (15×15 array)
- Heat pipes: Extend through reflector (876 pipes)
- Density: 1.803 g/cm³
- Temperature: ~1045.6 K average

**Required Implementation:**
1. **Create reflector assembly universe (u=701):**
   ```
   c --- Bottom Reflector Assembly ---
   7011  315  1  -4701  u=-701  imp:n=1     $ Heat pipe through reflector
   701   710  1  -7011  u=-701  imp:n=1     $ Graphite H-451 fill

   c --- Bottom Reflector Assembly (with guide tube) ---
   7012  315  1  -4702  u=-702  imp:n=1     $ Heat pipe
   7013  300  1  -9912  u=-702  imp:n=1     $ Guide tube
   702   710  1  -7012:-7013  u=-702  imp:n=1  $ Graphite fill
   ```

2. **Create reflector lattice (u=101):**
   ```
   c --- Bottom Reflector Lattice ---
   1001  710  1  -7001  lat=2  u=101  imp:n=1  fill=-7:7 -7:7 0:0
   [Same fill pattern as core, but with u=701/702 instead of u=901/902]

   101  0  -101  fill=101  imp:n=1     $ Bottom reflector
   ```

3. **Define surfaces:**
   ```
   101   rhp  0 0 0   0 0 20   100.92 0 0    $ Reflector container
   7001  rhp  0 0 0   0 0 20   8.684 0 0     $ Reflector assembly
   4701  rcc  0 0 0   0 0 20   1.070         $ Heat pipe hole
   4702  rcc  0 0 0   0 0 20   1.070         $ Heat pipe hole
   9912  rcc  0 0 0   0 0 20   3.200         $ Guide tube hole
   ```

**Dependencies:** Requires m710 material definition (same as m201)

---

#### **GAP 2: Top Reflector (z = 180-200 cm)** ❌ CRITICAL

**What's Missing:**
- Graphite H-451 reflector above active core
- Heat pipe protrusions through reflector
- Guide tube holes
- Harder neutron spectrum due to reduced graphite content

**Current Status:** Surfaces commented out (lines 162-166), cells not defined

**Specification from Reference:**
- Material: Graphite H-451 (m710)
- Thickness: 20 cm
- Axial position: z = 180-200 cm
- Configuration: Hexagonal lattice matching core
- Heat pipes: Protrude through (876 pipes, evaporator section ends at z=180)
- Special: Lower graphite density due to heat pipe/control rod holes
- Temperature: ~1002.0 K average

**Required Implementation:**
1. **Create top reflector assembly universe (u=801, u=802):**
   ```
   c --- Top Reflector Assembly (with guide tube) ---
   8011  315  1  -4801  u=-801  imp:n=1     $ Heat pipe through reflector
   8012  300  1  -9811  u=-801  imp:n=1     $ Guide tube
   801   710  1  -8011:-8012  u=-801  imp:n=1  $ Graphite fill

   c --- Top Reflector Assembly (no guide tube) ---
   8021  315  1  -4802  u=-802  imp:n=1     $ Heat pipe
   802   710  1  -8021  u=-802  imp:n=1     $ Graphite fill
   ```

2. **Create top reflector lattice (u=104):**
   ```
   c --- Top Reflector Lattice ---
   1004  710  1  -8001  lat=2  u=104  imp:n=1  fill=-7:7 -7:7 0:0
   [Same fill pattern as core: u=801 for guide tube positions, u=802 elsewhere]

   104  0  -104  fill=104  imp:n=1     $ Top reflector
   ```

3. **Define surfaces:**
   ```
   104   rhp  0 0 180  0 0 20   100.92 0 0   $ Reflector container
   8001  rhp  0 0 180  0 0 20   8.684 0 0    $ Reflector assembly
   4801  rcc  0 0 180  0 0 20   1.070        $ Heat pipe hole
   4802  rcc  0 0 180  0 0 20   1.070        $ Heat pipe hole
   9811  rcc  0 0 180  0 0 20   3.200        $ Guide tube hole
   ```

**Dependencies:** Requires m710 material definition

---

#### **GAP 3: Control Drums (12 drums)** ❌ CRITICAL

**What's Missing:**
- 12 control drums positioned around core periphery
- B₄C absorber sections (120° arc, 2.7984 cm thick)
- Graphite sections (240° arc)
- Cylindrical geometry intersecting hexagonal core

**Current Status:** Not implemented at all

**Specification from Reference:**
- Number: 12 drums
- Diameter: 28.1979 cm (radius = 14.09895 cm)
- B₄C thickness: 2.7984 cm (radial)
- B₄C angular coverage: 120° (1/3 circumference)
- Graphite: 240° (2/3 circumference)
- Axial coverage: z = 20-180 cm (active core only)
- Position: Around core periphery at ~110-130 cm radius

**Required Implementation:**
1. **Define control drum surfaces:**
   ```
   c --- Control Drum 1 (example at 0° position) ---
   c Drum center at (x=120, y=0)
   c Outer cylinder
   801  rcc  120 0 20   0 0 160   14.09895     $ Drum 1 outer
   c B4C absorber cylinder (inner)
   802  rcc  120 0 20   0 0 160   11.30055     $ Drum 1 B4C inner
   c Cutting planes for 120° B4C arc (facing inward)
   803  pz  120  $ Plane 1
   804  pz  120  $ Plane 2 (rotated 120°)
   [Repeat for all 12 drums at 30° intervals]
   ```

2. **Define control drum cells:**
   ```
   c --- Drum 1 ---
   8101  800  1  -802  <angular cut>  u=0  imp:n=1  $ B4C absorber
   8102  801  1  -801  802:<angular cut complement>  u=0  imp:n=1  $ Graphite
   [Repeat for all 12 drums]
   ```

3. **Position drums around core:**
   - Drum centers at radius ~120 cm
   - Angular positions: 0°, 30°, 60°, ..., 330° (12 drums)
   - Use TRn cards for rotation if needed

**Dependencies:** Requires m800 (B₄C) and m801 (graphite) materials

---

#### **GAP 4: Source Definition (KCODE + KSRC)** ❌ CRITICAL

**What's Missing:**
- KCODE card for criticality calculation
- KSRC card for initial source distribution
- Source points distributed across fuel regions

**Current Status:** No source cards present

**Required Implementation:**
```
c ============================================================================
c                        SOURCE DEFINITION
c ============================================================================
c
KCODE 10000 1.0 50 250
c     nsrck  keff  nskip  nkcode
c     10000 neutrons per cycle
c     Initial keff guess = 1.0
c     Skip 50 cycles (settle)
c     Run 250 active cycles
c
c --- Initial source points distributed in fuel ---
KSRC  0 0 100        $ Center assembly, mid-height
      30 0 100       $ Radial position 1
      -30 0 100      $ Radial position 2
      0 30 100       $ Radial position 3
      0 -30 100      $ Radial position 4
      60 0 100       $ Radial position 5
      -60 0 100      $ Radial position 6
      30 52 100      $ Radial position 7
      -30 -52 100    $ Radial position 8
      0 0 50         $ Center, lower
      0 0 150        $ Center, upper
      50 0 50        $ Mid-radius, lower
      50 0 150       $ Mid-radius, upper
```

**Notes:**
- Minimum 10-20 source points recommended
- Distribute radially and axially
- Avoid source points in reflector or shield

---

#### **GAP 5: MODE Card** ❌ CRITICAL

**What's Missing:**
- MODE N (neutron transport)

**Current Status:** No MODE card

**Required Implementation:**
```
MODE N
```

---

#### **GAP 6: Material m800 (B₄C Control Drum Absorber)** ❌ CRITICAL

**What's Missing:**
- B₄C material definition for control drums

**Current Status:** Not defined (though referenced in material list)

**Specification:**
- Density: ~2.52 g/cm³ (typical for B₄C)
- Composition: B₄C stoichiometry
- Temperature: ~1000 K

**Required Implementation:**
```
c --- Material 800: B4C Control Drum Absorber (1000 K) ---
m800  5010.02c  1.673E-02      $ B-10 (19.9% natural abundance)
      5011.02c  6.738E-02      $ B-11 (80.1% natural abundance)
      6000.82c  2.103E-02      $ C (graphite)
c Total density: 2.52 g/cm3
c B4C: 4 boron atoms, 1 carbon atom
c Using natural boron enrichment
```

**Alternative (enriched B-10):**
If using enriched boron (e.g., 90% B-10):
```
m800  5010.02c  7.576E-02      $ B-10 (90% enriched)
      5011.02c  8.418E-03      $ B-11 (10%)
      6000.82c  2.103E-02      $ C
```

---

#### **GAP 7: Material m710 (Graphite Reflector)** ❌ CRITICAL

**What's Missing:**
- Separate material for reflector graphite (different temperature than monolith)

**Current Status:** Not defined (can use m201 as workaround, but separate material preferred)

**Required Implementation:**
```
c --- Material 710: Graphite Reflector H-451 (1000-1045 K) ---
m710  6000.83c  -1.0            $ Carbon at 1200K (or .02c at 900K)
mt710 grph.47t                  $ Graphite S(a,b) at 1200K (or .20t at 400K)
c Density: 1.803 g/cm3
```

**Note:** Can use m201 initially if temperature difference acceptable

---

### 2.2 IMPORTANT GAPS (Needed for Accuracy)

#### **GAP 8: PHYS Card for Transport Parameters** ⚠ IMPORTANT

**What's Missing:**
- PHYS:N card for neutron physics parameters
- Energy cutoffs
- Thermal treatment parameters

**Required Implementation:**
```
c --- Neutron physics parameters ---
PHYS:N 40.0 0 0 J J J 1.0E-8 J J J -1.0 J 0.0017
c      emax emin cutoff etc.
c      40 MeV maximum energy
c      1E-8 MeV thermal cutoff (optional)
```

**Recommendation:** Start without PHYS card (use defaults), add if needed for refinement

---

#### **GAP 9: Tally Definitions** ⚠ IMPORTANT

**What's Missing:**
- F4 (flux) tallies for fuel regions
- F7 (fission heating) tallies
- Energy bins for spectral information
- FM cards for reaction rates

**Recommended Implementation:**
```
c --- Core-averaged flux ---
F4:N  (102)           $ Cell 102 (active core)
E4    1E-8  0.625E-6  5.53E-3  0.821  20.0   $ 5-group structure
c
c --- Fission power distribution ---
F7:N  (fuel cells)
c
c --- Assembly-wise power ---
F4:N  (assembly cells with FM multiplier)
FM4   (-1 -6 -8)     $ Fission energy release
```

---

#### **GAP 10: Print and Output Control** ⚠ IMPORTANT

**What's Missing:**
- PRINT card for output control
- PRDMP card for dump cycle control
- Lost particle control

**Recommended Implementation:**
```
c --- Print control ---
PRINT 10 30 38 40 50 110 117 118 126 128 160 161 162 170
c     Reduced output, focus on summary tables
c
c --- Dump cycle control ---
PRDMP J J 1 J J    $ Write RUNTPE every cycle
c
c --- Lost particle handling ---
LOST  10 10        $ Allow 10 lost particles before warning, 10 before fatal
```

---

#### **GAP 11: Axial Segmentation Refinement** ⚠ IMPORTANT

**Current Status:** 2 axial segments (80 cm each)
**Reference Model:** 18 axial segments (10 cm each)

**Impact:**
- Current: Coarse axial flux and power distribution
- Reference: Fine resolution for temperature feedback and depletion

**Trade-off:** Computational cost vs. accuracy

**Recommendation:**
- Start with 2-4 segments for initial testing
- Refine to 8-16 segments for production runs
- Full 18 segments for high-fidelity coupled analysis

---

#### **GAP 12: Temperature-Dependent Cross-Section Sets** ⚠ IMPORTANT

**Current Status:** Single temperature library for each material
**Reference Model:** Multiple state points (600-1400 K fuel, 600-1400 K moderator)

**Gap:**
- No cross-section temperature interpolation
- Single .03c (1200K) library used throughout
- Large temperature gradients (600-1570 K) not captured

**Recommended Enhancement:**
- Define multiple material cards for different temperature zones
- Use TMP card for interpolation (if available)
- Or: Accept single-temperature approximation for initial model

**Implementation (if pursuing):**
```
c --- Fuel at 800K ---
m301a  92235.02c  ...    $ .02c = 900K library
mt301a grph.20t         $ grph at 400K S(a,b)

c --- Fuel at 1200K ---
m301b  92235.03c  ...    $ .03c = 1200K library
mt301b grph.47t         $ grph at 1200K S(a,b)

c --- Assign to cells based on expected temperature ---
```

---

### 2.3 NICE-TO-HAVE ADDITIONS (Model Enhancements)

#### **GAP 13: Detailed Control Drum Positioning** ⭕ ENHANCEMENT

**Gap:** Exact angular positions of 12 drums not specified in reference

**Recommendation:**
- Distribute evenly: 0°, 30°, 60°, ..., 330°
- Or: Use clustering pattern if available from eVinci™ design
- Model drums "facing in" (absorber toward core) for conservative estimate

---

#### **GAP 14: Shutdown Control Rod System** ⭕ ENHANCEMENT

**Gap:** Reference mentions shutdown control rods as future work, not currently modeled

**Recommendation:** Defer to future model refinement

---

#### **GAP 15: Explicit TRISO Particle Modeling** ⭕ ENHANCEMENT

**Current:** Homogenized TRISO in graphite matrix
**Enhancement:** Explicit TRISO particles with lattice

**Impact:**
- More accurate self-shielding
- Better Doppler feedback
- Significantly higher computational cost

**Recommendation:** Start with homogenization, upgrade if needed for validation

---

## 3. DETAILED GAP SPECIFICATIONS

### 3.1 Bottom Reflector Assembly Implementation

**What to Add:** Complete bottom reflector (z = 0-20 cm)

**Where to Add:**

**Cell Block:**
```
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR ASSEMBLY | w/ GUIDE TUBE (u=701)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
7011  315   1  -4701         u=-701  imp:n=1    $ Heat pipe through reflector
7012  300   1  -9701         u=-701  imp:n=1    $ Guide tube helium
701   710  -1.803  -7001  7011:7012  u=-701  fill=701R  imp:n=1  $ Graphite reflector

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR ASSEMBLY | FULL, NO GUIDE TUBE (u=702)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
7021  315   1  -4702         u=-702  imp:n=1    $ Heat pipe through reflector
702   710  -1.803  -7002  7021   u=-702  imp:n=1  $ Graphite reflector

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR LATTICE (u=101)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1001  710  -1.803  -7000  lat=2  u=101  imp:n=1  fill=-7:7 -7:7 0:0
     [Same pattern as core lattice, using u=701/702]

101   0  -101  fill=101  imp:n=1    $ Bottom reflector region
```

**Surface Block:**
```
c --- Bottom Reflector Surfaces ---
101   rhp  0 0  0   0 0  20   100.92 0 0    $ Bottom reflector container
7000  rhp  0 0  0   0 0  20     8.684 0 0    $ Reflector assembly lattice
7001  rhp  0 0  0   0 0  20     8.684 0 0    $ Assembly w/ guide tube
7002  rhp  0 0  0   0 0  20     8.684 0 0    $ Assembly w/o guide tube
4701  rcc  0 0  0   0 0  20     1.070         $ Heat pipe hole (w/ guide)
4702  rcc  0 0  0   0 0  20     1.070         $ Heat pipe hole (no guide)
9701  rcc  0 0  0   0 0  20     3.200         $ Guide tube hole
```

**Material Block:**
```
c --- Material 710: Graphite Reflector (1045 K) ---
m710  6000.83c  -1.0            $ Carbon at 1200K
mt710 grph.47t                  $ Graphite S(a,b) at 1200K
```

**Dimensions:**
- Total thickness: 20 cm
- Axial: z = 0-20 cm
- Radial: Same as core lattice (~100.92 cm hexagon)
- Heat pipe holes: 876 pipes, r = 1.07 cm
- Guide tube holes: 13 locations, r = 3.2 cm

**Dependencies:**
- m710 material
- m315 heat pipe material (already defined)
- m300 helium (already defined)
- Core lattice fill pattern (copy and modify)

---

### 3.2 Top Reflector Assembly Implementation

**What to Add:** Complete top reflector (z = 180-200 cm)

**Where to Add:**

**Cell Block:**
```
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR ASSEMBLY | w/ GUIDE TUBE (u=801)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8011  315   1  -4801         u=-801  imp:n=1    $ Heat pipe through reflector
8012  300   1  -9801         u=-801  imp:n=1    $ Guide tube helium
801   710  -1.803  -8001  8011:8012  u=-801  imp:n=1  $ Graphite reflector

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR ASSEMBLY | FULL, NO GUIDE TUBE (u=802)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8021  315   1  -4802         u=-802  imp:n=1    $ Heat pipe through reflector
802   710  -1.803  -8002  8021   u=-802  imp:n=1  $ Graphite reflector

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR LATTICE (u=104)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1004  710  -1.803  -8000  lat=2  u=104  imp:n=1  fill=-7:7 -7:7 0:0
     [Same pattern as core lattice, using u=801/802]

104   0  -104  fill=104  imp:n=1    $ Top reflector region
```

**Surface Block:**
```
c --- Top Reflector Surfaces ---
104   rhp  0 0 180  0 0  20   100.92 0 0    $ Top reflector container
8000  rhp  0 0 180  0 0  20     8.684 0 0    $ Reflector assembly lattice
8001  rhp  0 0 180  0 0  20     8.684 0 0    $ Assembly w/ guide tube
8002  rhp  0 0 180  0 0  20     8.684 0 0    $ Assembly w/o guide tube
4801  rcc  0 0 180  0 0  20     1.070         $ Heat pipe hole (w/ guide)
4802  rcc  0 0 180  0 0  20     1.070         $ Heat pipe hole (no guide)
9801  rcc  0 0 180  0 0  20     3.200         $ Guide tube hole
```

**Material Block:** (same m710 as bottom reflector)

**Dimensions:**
- Total thickness: 20 cm
- Axial: z = 180-200 cm
- Radial: Same as core lattice (~100.92 cm hexagon)
- Heat pipe protrusions: 876 pipes, r = 1.07 cm
- Guide tube holes: 13 locations, r = 3.2 cm

**Special Note:** Top reflector has slightly harder spectrum due to heat pipe and control rod holes reducing graphite content.

---

### 3.3 Control Drum Implementation

**What to Add:** 12 control drums around core periphery

**Where to Add:**

**Cell Block:**
```
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c CONTROL DRUMS (12 drums at 30° intervals)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Drum 1 (0° position, x-axis) ---
c Center: (120, 0, 0)
c
c B4C absorber sector (120° arc facing inward)
8101  800  -2.52  -8011  8012  8013  8014  imp:n=1  $ Drum 1 B4C
c Graphite sectors (240° arc)
8102  801  -1.803  -8011  8012  ~8013:~8014  imp:n=1  $ Drum 1 graphite

c [Repeat for drums 2-12 with rotated positions]
c Drum 2: 30° (center at r=120, theta=30°)
c Drum 3: 60°
c ...
c Drum 12: 330°
```

**Surface Block:**
```
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c CONTROL DRUM SURFACES
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Drum 1 (0° position) ---
8011  rcc  120 0 20   0 0 160   14.09895      $ Drum 1 outer cylinder
8012  rcc  120 0 20   0 0 160   11.30055      $ Drum 1 B4C inner cylinder
c Cutting planes for 120° B4C sector (±60° from inward direction)
8013  p  1 0 0  120                             $ Plane at 60° from inward
8014  p  1 0 0  120                             $ Plane at -60° from inward
c [Use transformation or direct calculation for plane equations]

c [Repeat for drums 2-12]
```

**Material Block:**
```
c --- Material 800: B4C Control Drum Absorber (1000 K) ---
m800  5010.02c  1.673E-02      $ B-10 at 900K (natural abundance 19.9%)
      5011.02c  6.738E-02      $ B-11 at 900K (natural abundance 80.1%)
      6000.82c  2.103E-02      $ C at 900K
c Density: 2.52 g/cm3
c Stoichiometry: B4C (4 boron, 1 carbon)

c --- Material 801: Control Drum Graphite (1000 K) ---
m801  6000.82c  -1.0            $ Carbon at 900K
mt801 grph.20t                  $ Graphite S(a,b) at 400K (or .47t at 1200K)
c Density: 1.803 g/cm3
```

**Dimensions:**
- Drum outer radius: 14.09895 cm (diameter 28.1979 cm)
- B₄C inner radius: 11.30055 cm (thickness 2.7984 cm)
- B₄C angular coverage: 120° (facing inward)
- Graphite: Remaining 240°
- Axial extent: z = 20-180 cm (active core only)
- Radial positions: 12 drums at ~120 cm radius, 30° intervals

**Complexity Note:**
- Cylindrical drums in hexagonal lattice require careful surface intersections
- May need coordinate transformations (TRn cards)
- Alternative: Use simplified geometry (full B₄C cylinders) for initial model, refine later

---

### 3.4 Source Definition Implementation

**What to Add:** KCODE and KSRC cards

**Where to Add:** After material cards, before end of input

```
c ============================================================================
c                        SOURCE DEFINITION
c ============================================================================
c
c --- Criticality source definition ---
KCODE 10000 1.0 50 250
c     10000 neutrons per cycle
c     Initial keff guess = 1.0
c     Skip 50 cycles for source convergence
c     Run 250 active cycles for statistics
c
c --- Initial source points ---
KSRC  0   0  100      $ Center, mid-height
      0   0   50      $ Center, lower
      0   0  150      $ Center, upper
     30   0  100      $ Ring 1, 0°
     30  52  100      $ Ring 1, 60°
    -15  26  100      $ Ring 1, 120°
    -30   0  100      $ Ring 1, 180°
    -15 -26  100      $ Ring 1, 240°
     15 -26  100      $ Ring 1, 300°
     60   0  100      $ Ring 2, 0°
     60 104  100      $ Ring 2, 60°
    -30  52  100      $ Ring 2, 120°
    -60   0  100      $ Ring 2, 180°
    -30 -52  100      $ Ring 2, 240°
     30 -52  100      $ Ring 2, 300°
     80   0   50      $ Ring 3, lower
     80   0  150      $ Ring 3, upper
      0  80   50      $ Ring 3, 90°, lower
      0  80  150      $ Ring 3, 90°, upper
c
c Total: 20 source points distributed radially and axially in fuel
```

**Notes:**
- Distribute source points across fuel region only
- Avoid placing in reflector, shield, or void
- More source points improve initial convergence
- Source converges during first 50 cycles (monitored via Shannon entropy)

---

## 4. PRIORITY RANKING

### 4.1 CRITICAL GAPS (Must Fix - Model Won't Run)

| Priority | Gap | Impact | Effort |
|----------|-----|--------|--------|
| **1** | MODE card | No particle transport | 1 line |
| **2** | KCODE + KSRC | No criticality calculation | ~25 lines |
| **3** | Bottom reflector | Geometry incomplete, neutron leakage | ~50 lines |
| **4** | Top reflector | Geometry incomplete, neutron leakage | ~50 lines |
| **5** | Material m710 | Reflectors undefined | ~3 lines |
| **6** | Material m800 | Control drums undefined | ~5 lines |
| **7** | Control drums | Reactivity control missing | ~150 lines |

**Estimated Total Effort:** ~284 lines of input + testing

---

### 4.2 IMPORTANT GAPS (Needed for Accurate Results)

| Priority | Gap | Impact | Effort |
|----------|-----|--------|--------|
| **8** | PHYS:N card | Default physics may be non-optimal | ~1 line |
| **9** | Tallies (F4, F7) | No power/flux output | ~20 lines |
| **10** | Print control | Excessive output | ~3 lines |
| **11** | Axial segmentation | Coarse power distribution | ~100 lines |
| **12** | Temperature XS | Single-temperature approximation | ~50 lines |

**Estimated Total Effort:** ~174 lines

---

### 4.3 NICE-TO-HAVE (Model Enhancements)

| Priority | Gap | Impact | Effort |
|----------|-----|--------|--------|
| **13** | Drum positioning detail | Minor reactivity uncertainty | ~10 lines |
| **14** | Shutdown rods | Not in reference model | ~100 lines |
| **15** | Explicit TRISO | Better physics, huge cost | ~500+ lines |

---

## 5. IMPLEMENTATION ROADMAP

### Phase 1: Make Model Runnable (Critical Gaps 1-6)

**Objective:** Model runs and produces keff

**Tasks:**
1. Add MODE N card
2. Add KCODE 10000 1.0 50 250
3. Add KSRC with 10-20 source points in fuel
4. Define m710 (copy m201 with different temperature)
5. Define m800 (B₄C absorber)
6. Uncomment and complete bottom reflector (z=0-20)
7. Uncomment and complete top reflector (z=180-200)

**Test:** Run MCNP and verify:
- Model runs without fatal errors
- keff calculation completes
- Neutron balance reasonable (no excessive leakage)

**Estimated Time:** 2-4 hours

---

### Phase 2: Add Control Drums (Critical Gap 7)

**Objective:** Include reactivity control system

**Tasks:**
1. Define 12 control drum positions (30° intervals at r~120 cm)
2. Create cylindrical surfaces for drum outer and inner boundaries
3. Create cutting planes for B₄C/graphite sectors
4. Define drum cells with m800 (B₄C) and m801 (graphite)
5. Handle intersections with radial reflector

**Test:** Run MCNP and verify:
- Drums are geometrically valid (no overlaps)
- Reactivity decreases with drums facing in
- Flux depression near drums

**Estimated Time:** 4-8 hours (geometry complexity)

---

### Phase 3: Add Output and Refinement (Important Gaps 8-12)

**Objective:** Improve accuracy and usability

**Tasks:**
1. Add PHYS:N card for transport parameters
2. Define F4 flux tallies for core regions
3. Define F7 heating tallies for power distribution
4. Add PRINT card to reduce output
5. Add PRDMP for restart capability
6. (Optional) Refine to 4-8 axial segments
7. (Optional) Add temperature-dependent XS sets

**Test:** Run MCNP and verify:
- Tallies produce reasonable results
- Power distribution matches reference (~2.4 peaking)
- Temperature coefficients reasonable (Doppler ~ -7 pcm/K)

**Estimated Time:** 4-8 hours

---

### Phase 4: Validation (Nice-to-Have)

**Objective:** Compare to reference Serpent/Griffin results

**Tasks:**
1. Compare keff to reference (Serpent: 1.09972 ± 0.00014)
2. Compare power peaking (reference: 2.44)
3. Compare temperature distributions
4. Adjust drum positions if needed
5. Refine geometry/materials as needed

**Estimated Time:** Variable (depends on discrepancies)

---

## 6. VALIDATION TARGETS

### 6.1 Expected Results (From Reference)

| Parameter | Reference Value | Tolerance | Source |
|-----------|----------------|-----------|--------|
| **keff (drums in)** | 1.09972 ± 0.00014 | ±500 pcm | Serpent, Table 10 |
| **keff (drums out)** | ~1.12-1.15 (estimated) | ±1000 pcm | Estimated |
| **Power Peaking** | 2.44 | ±0.5 | Table 19 |
| **Fuel Temp (avg)** | 1155.6 K | Info only | Table 19 |
| **Fuel Temp (max)** | 1570.0 K | Info only | Table 19 |
| **Doppler Coeff** | -6 to -9 pcm/K | ±50% | Tables 11 |
| **Graphite Coeff** | +0.4 to +0.7 pcm/K | Info only | Table 12 |

### 6.2 Acceptance Criteria

**For Initial Model (Phases 1-2):**
- keff within ±1000 pcm of reference
- Model runs without fatal errors
- Neutron balance reasonable (leakage < 30%)
- Control drums produce negative reactivity insertion

**For Refined Model (Phase 3):**
- keff within ±500 pcm of reference
- Power peaking within ±0.5 of reference
- Flux distributions qualitatively similar
- Temperature coefficients correct sign

---

## 7. KNOWN ISSUES AND LIMITATIONS

### 7.1 Current Model Issues

1. **No axial reflectors:** Neutrons leak excessively from top/bottom
2. **No control drums:** Cannot simulate reactivity control
3. **No source:** Model cannot run criticality calculation
4. **Single temperature:** Large temperature gradients not captured
5. **Coarse axial mesh:** 2 segments vs. 18 in reference

### 7.2 Reference Model Approximations

1. **Homogenized TRISO:** Individual particles not modeled
2. **Homogenized heat pipes:** Detailed structure averaged
3. **No Xe/Sm poisons:** keff is ~5000 pcm too high
4. **No depletion:** Fresh fuel only
5. **Fixed cross-sections:** No temperature feedback

### 7.3 Discrepancies to Resolve

1. **Reflector material:** Document says graphite H-451, model uses BeO (m401)
   - **Resolution:** Clarify which is correct, or model both cases

2. **Fuel gap:** Document says no gap between fuel and monolith, model has 0.05 cm gap (r=0.875 fuel, r=0.925 compact)
   - **Resolution:** Verify if gap is modeling artifact or real

3. **Assembly count:** 114 + 13 = 127 assemblies, but 15×15 lattice
   - **Resolution:** Some lattice positions filled with graphite (u=102)

---

## 8. RECOMMENDATIONS

### 8.1 Immediate Actions (Phase 1)

1. **Add MODE N card** - Critical, 5 minutes
2. **Add KCODE and KSRC** - Critical, 30 minutes
3. **Define m710 reflector material** - Critical, 10 minutes
4. **Implement bottom reflector** - Critical, 1-2 hours
5. **Implement top reflector** - Critical, 1-2 hours
6. **Define m800 B₄C material** - Critical, 15 minutes

**Result:** Runnable model with axial reflectors

---

### 8.2 Short-Term Actions (Phase 2)

1. **Implement 12 control drums** - Important, 4-8 hours
2. **Add basic tallies (F4, F7)** - Important, 1 hour
3. **Add print control** - Nice-to-have, 15 minutes
4. **Test and validate keff** - Important, 1-2 hours

**Result:** Functional model with reactivity control

---

### 8.3 Medium-Term Enhancements (Phase 3)

1. **Refine axial segmentation to 8 segments** - Improves accuracy
2. **Add temperature-dependent XS** - Improves physics
3. **Detailed drum positioning** - Minor improvement
4. **Comprehensive tallies** - Better output

**Result:** Production-quality model

---

### 8.4 Long-Term Enhancements (Phase 4)

1. **18 axial segments** - Match reference
2. **Explicit TRISO particles** - High fidelity
3. **Depletion analysis** - Burnup, Xe/Sm
4. **Coupled thermal-neutronics** - Feedback
5. **Shutdown rod system** - Complete control model

**Result:** High-fidelity validation model

---

## 9. SUMMARY

### Current Status
- **Completeness:** ~40%
- **Runnable:** NO (missing critical components)
- **Quality:** Good (what's implemented is correct)

### Top 3 Critical Gaps
1. **Axial reflectors** (top and bottom) - Geometry incomplete
2. **Source definition** (KCODE + KSRC) - Cannot run
3. **Control drums** (12 drums) - Reactivity control missing

### Effort to Make Runnable
- **Phase 1:** ~4-6 hours (add reflectors, source, MODE)
- **Phase 2:** +4-8 hours (add control drums)
- **Total:** ~8-14 hours to functional model

### Recommended Path Forward
1. Complete Phase 1 (make runnable) - **Priority 1**
2. Complete Phase 2 (add drums) - **Priority 2**
3. Test and validate against reference
4. Refine as needed based on results

---

## DOCUMENT METADATA

**Created:** 2025-11-08
**Author:** MCNP Technical Documentation Analyzer
**Model Analyzed:** /home/user/mcnp-skills/hpcmr-simplified.i
**Reference:** INL HPMR Reference Plant Model (April 2024)
**Status:** Complete - Ready for implementation planning
**Next Action:** Implement Phase 1 critical gaps (make model runnable)

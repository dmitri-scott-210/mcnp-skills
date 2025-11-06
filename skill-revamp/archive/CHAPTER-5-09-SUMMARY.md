# Chapter 5.09 Tally Data Cards - Comprehensive Summary

**Created:** Session 14, 2025-11-04
**Purpose:** Reference summary for future sessions working on tally-builder and related skills
**Source:** MCNP6 Manual Chapter 5.09 (3,396 lines, ~54k tokens)

---

## Document Organization

**Chapter 5.09 covers 18 major topics:**
1. F1-F8 Tally Types (lines 1-800)
2. Radiography Tallies (FIP, FIR, FIC)
3. E, T, C Bin Cards (Energy, Time, Cosine)
4. FQ Print Hierarchy
5. FM Multiplier Card
6. DE/DF Dose Functions
7. EM, TM, CM Histogram Multipliers
8. CF/SF Flagging Cards
9. FS/SD Segmentation Cards
10. FU User Bins / TALLYX
11. FT Special Treatments (21 options)
12. TF Tally Fluctuation Chart
13. FC/FQ/FS/SD Detailed Specifications
14. Repeated Structures Tallies
15. F8 Pulse-Height Special Features
16. Advanced FT Options (PHL, CAP, RES, TAG, etc.)
17. Weight Window Integration
18. Statistical Quality Assessment

---

## Key Concepts by Category

### Tally Types (F1-F8)

**F1: Surface Current (particles/cm²)**
- Particles crossing surface
- Direction-dependent with C card (cosine bins)
- Can use CM card for per-steradian normalization

**F2: Surface Flux (particles/cm²)**
- Average flux on surface
- Direction-dependent with C card
- Often used for transmission/reflection

**F4: Track-Length Flux (particles/cm²)**
- Volume-averaged flux in cell
- Σ(track_length)/volume per source particle
- Most common tally type for flux

**F5: Point Detector (particles/cm²)**
- Next-event estimator at point in space
- Very efficient for localized scoring
- Can use FT PDS for pre-collision sampling

**F6: Energy Deposition (MeV/g)**
- Heating tally
- Accounts for all energy transferred to material
- Can use for dose with proper conversion

**F7: Fission Energy Deposition (MeV/g)**
- Fission heating only
- Includes prompt and delayed contributions
- Restricted to fissile materials

**F8: Pulse-Height (MeV)**
- Energy deposited per source particle history
- Requires special care (zero/epsilon bins)
- Can use *F8 (energy) or +F8 (charge)

---

### Critical Tally Number Limits

**Tally numbers:**
- n ≤ 99,999,999 (nearly 100 million max)
- Recommended increments of 10 for organization
- Special meanings: F5 vs F15 vs F25 (same type, different numbers)

**Tally flags:**
- **Asterisk (*Fn):** Multiply by energy (F1: energy current, F8: energy deposition)
- **Plus (+Fn):** Charge tally (F1: charge current, F8: electrons=-1, positrons=+1)
- **Caret (^Fn):** Not used in MCNP6

---

### Energy, Time, Cosine Binning

**E Card (Energy Bins):**
```
En E0 E1 E2 ... Ek [NT] [E0]
```
- Creates k energy bins
- NT suppresses total bin
- E0 keyword sets default for all tallies
- Can use log intervals: 1E-3 10ILOG 10 (10 bins from 0.001 to 10)

**T Card (Time Bins):**
```
Tn T0 T1 T2 ... Tk [NT] [T0]
```
- Time in shakes (1 shake = 10⁻⁸ sec)
- Cyclic time option with keywords:
  - CBEG, CFRQ, COFI, CONI, CSUB, CEND
  - For periodic sources (pulsed accelerators)

**C Card (Cosine Bins):**
```
Cn μ0 μ1 μ2 ... μk [NT] [C0] [*C]
```
- Cosine of angle (−1 to +1)
- *C option: Use degrees instead of cosines
- FT FRV: Use custom reference vector instead of surface normal

**Combining bins:**
- E × T × C creates multi-dimensional tally
- Use FQ card to control print order
- Use TF card to select statistical analysis bin

---

### FQ Print Hierarchy

**Controls output table organization:**
```
FQn [subset of: F D U S M C E T]
```

**Bin types:**
- **F:** Cell/surface bin
- **D:** Direct/flagged bin
- **U:** User bin
- **S:** Segment bin
- **M:** Multiplier bin
- **C:** Cosine bin
- **E:** Energy bin
- **T:** Time bin

**Default order:** F D U S M C E T
- Last two letters form rows and columns
- Default: E (rows) × T (columns)

**Example:**
```
FQ4 M E    $ Multiplier bins (rows) × Energy bins (columns)
```

---

### FM Multiplier Card (Reaction Rates)

**Purpose:** Multiply flux by cross section to get reaction rate

**Syntax:**
```
FMn (c m R1 R2 ... :R3 #R4) (c m R5 ...) ...
```

**Parameters:**
- **c:** Normalization constant (use −1 for atom density → macroscopic)
- **m:** Material number (from M card)
- **R:** Reaction number (MT or special R from Table 5.19)

**Operators:**
- **Space:** Multiply (R1 × R2)
- **Colon (:):** Add (R1 + R3)
- **Pound (#):** Subtract (R1 − R4)

**Special R numbers:**
- **−1:** Total cross section
- **−2:** Absorption
- **−3:** Elastic scattering
- **−4:** Heating (KERMA factor)
- **−5:** Photon production
- **−6:** Total fission
- **−7:** Fission ν (neutron multiplicity)
- **−8:** Fission Q (MeV/fission)

**Example:**
```
FM4 −1 3 −6 −7    $ Fission neutron production rate (per cm³)
```

**k = −3 option:** First interaction cross section (use with LCA NOACT=−2)

---

### DE/DF Dose Functions

**Purpose:** Convert flux to dose with continuous energy-dependent response

**Syntax:**
```
DEn [log/lin] E1 E2 ... Ek
DFn [log/lin] F1 F2 ... Fk
```

**Interpolation modes:**
- LOG LOG (default) - Appropriate for dose functions
- LIN LIN, LIN LOG, LOG LIN

**Built-in functions (IC keyword):**
```
DFn IC=99 IU=2 FAC=−3    $ ICRP-60 dose conversion
```

**IC codes:**
- **99:** ICRP-60 dose (recommended)
- **he3-1, nai-1, bgo-1, etc.:** Detector responses

**IU units:**
- **1:** rem/h
- **2:** Sv/h (default)

**FAC normalization:**
- **−3:** ICRP-60 factors (default with IC=99)
- **>0:** User factor

**Difference from EM/TM/CM:**
- DE/DF: Continuous interpolation, smooth response
- EM/TM/CM: Histogram (step function), bin normalization

---

### EM, TM, CM Histogram Multipliers

**EM: Energy Multiplier (requires E card)**
```
EMn m1 m2 ... mk
```
- One multiplier per energy bin
- Use case: Per-unit-energy (EM = 1/ΔE)

**TM: Time Multiplier (requires T card)**
```
TMn m1 m2 ... mk
```
- One multiplier per time bin
- Use case: Per-unit-time (TM = 1/Δt)

**CM: Cosine Multiplier (F1/F2 only, requires C card)**
```
CMn m1 m2 ... mk
```
- One multiplier per cosine bin
- Use case: Per-steradian (CM = 1/[2π(cosθᵢ − cosθᵢ₋₁)])

**EM0, TM0, CM0:** Set defaults for all tallies

---

### CF/SF Flagging (Track History)

**CF: Cell Flagging**
```
CFn c1 c2 ... ck
```
- Flag particles exiting specified cells
- Negative cell: Requires collision before flagging
- Creates second tally output (flagged contributions only)

**SF: Surface Flagging**
```
SFn s1 s2 ... sk
```
- Flag particles crossing specified surfaces
- Creates second tally output

**Combined CF+SF:**
- Particles flagged if exiting any CF cell OR crossing any SF surface
- Only one flagged output produced

**Use case:**
- Track particles through shielding layers
- Determine contribution from specific regions

---

### FS/SD Segmentation (Subdivide Without Extra Geometry)

**FS: Tally Segment**
```
FSn [±]s1 [±]s2 ... [±]sk [T]
```
- Divides cell/surface into k+1 segments using k surfaces
- Segments don't have to be part of geometry
- T option adds total bin

**Segment bin logic:**
1. Bin 1: Same sense as s1
2. Bin 2: Same sense as s2, excluding bin 1
3. ...
4. Bin k: Same sense as sk, excluding previous bins
5. Bin k+1: Everything else
6. Bin k+2: Total (if T present)

**SD: Segment Divisor**
```
SDn (d11 d12 ... d1M) (d21 ... d2M) ... (dK1 ... dKM)
```
- Provide volumes (F4), areas (F2), or masses (F6/F7) for segments
- Can use without FS card for custom divisors

**Hierarchy for divisor:**
1. Non-zero SD entry
2. Non-zero VOL/AREA entry
3. MCNP-calculated value
4. Fatal error

---

### F8 Pulse-Height Special Features

**Zero and epsilon bins (CRITICAL):**
```
E8 0 1E-5 1E-3 0.01 0.1 1.0 10.0
```
- Zero bin: No energy deposition
- Epsilon bin: Tiny depositions (computational artifacts)
- Required for proper normalization

**Asterisk flagging (*F8):**
- Converts to energy deposition tally (same as F8 for neutral particles)

**Plus flagging (+F8):**
- Charge deposition (electrons = −1, positrons = +1)
- Cannot combine with asterisk

**Variance reduction:**
- Allowed: IMP, CUT, WWN, FCL, EXT, DXT, SB, ESPLT, TSPLT
- NOT allowed: WWG (fatal error)
- Use VAR RR=off to disable roulette

**Forbidden:**
- DE/DF cards
- Flagging bins
- Multiplier bins

---

### FT Special Treatments (21 Options)

**Most important options:**

1. **PHL (Pulse-Height Light):**
   - Multi-region detectors with material response
   - Built-in detector types: HE3-1, NAI-1, BGO-1, CSI-1, HPG-1, etc.
   - Scintillator: Birks's Law quenching
   - Gas detector: Work function + multiplication
   - Time-dependent with T8 and TDEP keyword

2. **CAP (Coincidence Capture):**
   - Neutron capture multiplicities and moments
   - Automatic analog capture + fission multiplicity
   - GATE keyword for time gating
   - EDEP keyword for energy trigger

3. **RES (Residual Nuclides):**
   - Heavy-ion production from reactions
   - Works with F8:# or F1/F2/F4/F6
   - Z range or explicit isotope list
   - Use with LCA NOACT=−2 for single-collision analysis

4. **TAG (Tally Tagging):**
   - Track particle production history
   - FU bins: CCCCCZZAAA.RRRRR format
   - Special designators for source, scatter, everything else
   - Scatter treatment options (a = 1, 2, 3, 4)

5. **FRV (Fixed Reference Vector):**
   - Custom reference for C card cosine binning
   - Replaces surface normal

6. **GEB (Gaussian Energy Broadening):**
   - Realistic detector resolution
   - FWHM = √(a² + bE + cE²)

7. **ICD (Identify Contributing Cell):**
   - Detector tally by source cell
   - FU bins list cells of interest

8. **PDS (Point Detector Sampling):**
   - Pre-collision estimator (c = −1, 0, 1, 2)
   - Improves convergence, especially for photons
   - Allows coherent scattering with point detectors

**Other options:** TMC, INC, SCX, SCD, ELC, PTT, LET, ROC, FFT, COM, SPM, MGC, FNS, LCS

---

### TF Tally Fluctuation Chart

**Purpose:** Select bin for statistical analysis and weight-window optimization

**Syntax:**
```
TFn if id iu is im ic ie it
```

**Bin order mnemonic:** Fred Died Under Some Mysterious Circumstances Editing Tallies

**Parameters:**
- **if:** F-bin (cell/surface/detector)
- **id:** D-bin (total/flagged/direct)
- **iu:** U-bin (user bin)
- **is:** S-bin (segment bin)
- **im:** M-bin (multiplier bin)
- **ic:** C-bin (cosine bin)
- **ie:** E-bin (energy bin)
- **it:** T-bin (time bin)

**Defaults:**
- if, id, im = 1 (first bin)
- iu, is, ic, ie, it = last bin

**Use case:**
- Optimize weight windows for specific energy/time bin
- Get statistics for most important bin (not always total)

---

### Repeated Structures Tallies

**Bracket notation for lattice elements:**
```
F4:n 10[0 0 0]                     $ Single element
F4:n 10[0:2 0:2 0:2]               $ Range (3×3×3 cube)
F4:n 10[0 0 0, 1 1 1, 2 2 2]       $ Specific elements
```

**Universe shorthand:**
```
F4:n U=5    $ All cells filled by universe 5
```

**Lattice tally chains (<):**
```
F4:n (1<2[0 0 0]<3<4)    $ Cell 1 in element [0,0,0] of lattice 2 in cell 3 in cell 4
```

**SD card for repeated structures:**
- Two modes for volume specification
- SPDTL card for performance optimization

---

### Radiography Tallies (FIP, FIR, FIC)

**FIP: Pinhole Image**
- Point detector as pinhole camera
- FS card defines pixel grid
- C card defines image plane orientation

**FIR: Planar Radiograph**
- F2 surface divided into rectangular grid
- FS card: Four surfaces defining boundaries
- C card: Number of bins (i × j)

**FIC: Cylindrical Radiograph**
- F2 on cylindrical surface
- FS card: Axial and azimuthal boundaries
- Creates "unrolled" cylindrical image

**NOTRN card + NPS second entry:**
- Direct (uncollided) transmission only
- Sharper images, reduced scatter
- NPS: Total histories, direct-only limit

**gridconv utility:**
- Converts MCTAL radiograph to image formats

---

## Most Common Mistakes

1. **F8 without zero/epsilon bins** → Normalization loss
2. **FM with c > 0 when need per-cm³** → Use c = −1 with atom density
3. **Using MT=18 for all fission** → Use R = −6 instead (catches MT=19,20,21,38)
4. **DE/DF vs EM confusion** → DE/DF continuous, EM histogram
5. **CF/SF with negative cells wrong** → Negative requires collision before flagging
6. **FS segment order ignored** → Order and sense matter!
7. **SD without FS** → Can use alone for custom divisors
8. **F8 with WWG** → Fatal error, use WWN instead
9. **FT options incompatible** → FU-requiring options mutually exclusive
10. **TF defaults not appropriate** → Optimize for your important bin, not total

---

## Integration Points for Other Skills

**mcnp-source-builder:**
- Source time dependence → T card bins
- Source energy distribution → E card bins
- Source direction → C card bins

**mcnp-geometry-builder:**
- FS segmenting surfaces don't need to be in geometry
- Repeated structures with bracket notation
- Radiography detector geometry

**mcnp-material-builder:**
- Materials for FM multipliers (can be off-geometry)
- Dose conversion requires proper material definition
- Detector materials for FT PHL

**mcnp-variance-reducer:**
- WWG optimizes for TF-selected bin
- F8 restrictions (no WWG)
- Point detector PDS option (FT PDS)

**mcnp-physics-builder:**
- Analog capture required for F8 CAP
- Fission multiplicity for coincidence counting
- Electron physics for F8 charge tallies

---

## Critical Requirements for Skill Revamp

**Must be in SKILL.md:**
- F1-F8 basic descriptions (concise)
- E, T, C cards basic syntax
- FM card common usage
- DE/DF vs EM comparison
- F8 zero/epsilon bin requirement
- Decision tree for tally type selection

**Must be in references/:**
- Complete FM reaction numbers (Table 5.19) → fm_reaction_numbers_complete.md
- DE/DF detailed specifications → dose_and_special_tallies.md
- EM/TM/CM detailed usage → tally_multipliers_histogram.md
- Advanced tally types (FIP/FIR/FIC) → advanced_tally_types.md
- CF/SF/FS/SD detailed specifications → tally_flagging_segmentation.md
- FT special treatments comprehensive → dose_and_special_tallies.md (FT section)
- Repeated structures bracket notation → repeated_structures_tallies.md
- Tally binning advanced options → tally_binning_advanced.md

**Must be in assets/:**
- Basic F4 flux spectrum example
- Point detector dose example (F5 + DE/DF)
- Reaction rates example (F4 + FM)
- Segmented tally example (F4 + FS + SD)
- Pulse-height detector example (F8 with zero/epsilon)
- Lattice element tally example (bracket notation)

---

## Session 14 Actions Completed

1. ✅ Read entire Chapter 5.09 (3,396 lines, ~54k tokens)
2. ✅ Created 7 reference files:
   - advanced_tally_types.md (1,400 words)
   - tally_flagging_segmentation.md (1,200 words)
   - repeated_structures_tallies.md (1,100 words)
   - tally_binning_advanced.md (900 words)
   - tally_multipliers_histogram.md (800 words)
   - fm_reaction_numbers_complete.md (1,500 words)
   - dose_and_special_tallies.md (1,600 words)

**Total reference content:** ~8,500 words extracted from Chapter 5.09

---

## Remaining Work for mcnp-tally-builder

**Step 6:** Create 5-6 example files in assets/example_tallies/ (~8k tokens)
- MANDATORY: Use completed skills (mcnp-input-builder, mcnp-geometry-builder) before writing
- Verify EXACTLY 2 blank lines (three-block structure)

**Step 7:** Create 2 scripts in scripts/ (~10k tokens)
- tally_validator.py
- dose_function_plotter.py
- README.md

**Step 8:** Streamline SKILL.md (~8k tokens)
- Update YAML frontmatter (version 2.0.0, remove non-standard fields)
- Enhance sections with pointers to new references
- Add brief advanced topics section
- Target: ~2,900 words (stay under 3k)

**Steps 9-11:** Validate, test, complete (~7k tokens)

**Total remaining:** ~33k tokens (2-3 sessions at current pace)

---

**END OF CHAPTER-5-09-SUMMARY.MD**

# MSRE BENCHMARK VALIDATION PROJECT - MASTER PLAN

**Project Start Date**: 2025-11-01
**Current Status**: Phase 2 - Explicit Heterogeneous Geometry Development
**Last Updated**: 2025-11-01
**Version**: 2.0

---

## EXECUTIVE SUMMARY

**Objective**: Validate the MCNP Skills Framework by generating a complete, benchmarked MSRE (Molten Salt Reactor Experiment) model from design specifications alone, matching published IRPhEP benchmark results.

**Success Criteria**:
- Generate MCNP input file from literature specifications (no reference MCNP file)
- Achieve k-eff = 1.020 ± 0.003 (matching published benchmark results)
- Pass all MCNP validation checks
- Document complete methodology and lessons learned

**Current Achievement**:
- ✅ **Phase 1 COMPLETE**: Homogenized model generated, k-eff = 1.16149 (too high, expected)
- 🔄 **Phase 2 IN PROGRESS**: Explicit heterogeneous lattice geometry

---

## CRITICAL INSTRUCTIONS FOR ALL FUTURE CLAUDE SESSIONS

### 🚨 BEFORE STARTING ANY WORK:

1. **READ THIS ENTIRE DOCUMENT FIRST** - Do not skip sections
2. **READ ALL REFERENCED DOCUMENTS** - Listed in Section 8
3. **USE ALL 37 MCNP SKILLS** - Listed in Section 7
4. **DO NOT USE SHORTCUTS** - No homogenization unless explicitly justified
5. **DO NOT COPY GT-MHR BLINDLY** - MSRE ≠ GT-MHR geometry
6. **VERIFY ALL DIMENSIONS** - Check against design spec before building
7. **UPDATE THIS DOCUMENT** - Add all findings, mistakes, results at end

### 🎯 CURRENT TASK:

Build explicit heterogeneous MSRE lattice model with:
- **Fuel channel diameter**: 2.642 cm (radius = 1.321 cm) ← CORRECT VALUE
- **Graphite stringer pitch**: 5.08 cm ← CORRECT VALUE
- **~1140 fuel channels** in square lattice
- **NO homogenization** - full geometric detail
- **Match published literature models** that achieved k-eff ≈ 1.020

---

## 1. PROJECT BACKGROUND

### 1.1 Why This Project Exists

The MCNP Skills Framework was developed to enable AI-assisted MCNP model generation. To validate the framework, we chose the MSRE benchmark because:

1. **Well-documented**: IRPhEP benchmark MSRE-MSR-RESR-001 with extensive literature
2. **Complex geometry**: ~1140 fuel channels in graphite lattice (tests framework capabilities)
3. **Challenging physics**: Molten salt reactor with liquid fuel (unique modeling challenges)
4. **Published results**: Multiple papers with k-eff results to compare against

### 1.2 What Makes MSRE Challenging

**Unique Features**:
- Liquid fuel salt flowing through graphite moderator channels
- Thermal spectrum with strong graphite moderation
- Known carbon cross-section bias in modern libraries (+2% k-eff)
- Complex lattice geometry requiring explicit channel modeling

**Common Mistakes to Avoid**:
- ❌ Using homogenization (too simplified, causes 14% k-eff error)
- ❌ Copying GT-MHR lattice patterns (different geometry entirely)
- ❌ Using wrong dimensions (verify against design spec!)
- ❌ Creating circular fill patterns (MSRE is square lattice)
- ❌ Not reading skills documentation before building

---

## 2. PROJECT PHASES AND STATUS

### Phase 1: Homogenized Model ✅ COMPLETE

**Objective**: Establish baseline with simplified geometry
**Status**: COMPLETE (2025-11-01)
**Result**: k-eff = 1.16149 ± 0.00070 (14% too high)

**Key Files**:
- `generated_msre.inp` - Homogenized model
- `msre_output.txt` - MCNP output (557 KB)
- `EXECUTIVE_SUMMARY.md` - Phase 1 analysis
- `MSRE_BENCHMARK_ANALYSIS.md` - Detailed findings

**Key Findings**:
- Homogenization causes ~12,000 pcm reactivity bias (too high)
- Framework successfully generated syntactically correct input
- Geometry perfect (0 lost particles)
- Statistical quality excellent (σ = 70 pcm)
- **Conclusion**: Need explicit heterogeneous geometry

### Phase 2: Explicit Heterogeneous Geometry 🔄 IN PROGRESS

**Objective**: Build detailed lattice model matching literature
**Status**: IN PROGRESS
**Started**: 2025-11-01

**Attempts So Far**:

**Attempt 1**: `msre_detailed.inp`
- Used wrong dimensions (where did 0.961 cm come from?)
- Status: Never ran, incorrect geometry

**Attempt 2**: `msre_explicit_lattice.inp`
- Used WRONG dimensions: radius=0.961cm, pitch=3.5921cm
- Ran for 319 cycles then crashed (MCNP6 bug)
- k-eff = 0.90200 (11.6% too low - wrong due to bad dimensions)
- Geometry worked (0 lost particles) but dimensions WRONG

**Attempt 3**: `msre_explicit_lattice_v2.inp`
- Started blindly copying GT-MHR circular pattern
- **STOPPED** - User corrected approach
- Mistake: Not reading MSRE design spec, copying GT-MHR blindly

**Next Attempt** (Current):
- **MUST USE CORRECT DIMENSIONS** from design spec
- Fuel channel: diameter=2.642cm, radius=1.321cm
- Stringer pitch: 5.08 cm
- Square lattice (NOT circular like GT-MHR)
- ~1140 channels total

**Target**: k-eff = 1.020 ± 0.003 (matching literature)

### Phase 3: Benchmark Validation 📋 PLANNED

**Objective**: Compare against IRPhEP benchmark
**Status**: NOT STARTED
**Prerequisites**: Phase 2 complete with correct k-eff

**Tasks**:
- Compare k-eff to published results
- Verify all 10 statistical checks
- Document any deviations
- Final validation report

### Phase 4: Documentation & Knowledge Transfer ✅ ONGOING

**Objective**: Document methodology for future use
**Status**: ONGOING

**Deliverables**:
- ✅ This MASTER_PLAN.md
- ✅ EXECUTIVE_SUMMARY.md
- ✅ MSRE_BENCHMARK_ANALYSIS.md
- ✅ Updated msre_design_spec.md
- 📋 Final validation report (pending Phase 3)

---

## 3. CRITICAL LESSONS LEARNED

### 3.1 Mistakes Made (Learn From These!)

**Mistake #1: Using Homogenization Without Justification**
- **What happened**: Built homogenized model first
- **Result**: k-eff = 1.16149 (14% too high)
- **Root cause**: Homogenization eliminated spatial self-shielding
- **Lesson**: Literature uses explicit geometry - we must too

**Mistake #2: Wrong Dimensions**
- **What happened**: Used radius=0.961cm, pitch=3.5921cm (WRONG!)
- **Correct values**: radius=1.321cm, pitch=5.08cm
- **Root cause**: Not reading design spec carefully
- **Lesson**: VERIFY ALL DIMENSIONS against design spec before building

**Mistake #3: Blindly Copying GT-MHR Patterns**
- **What happened**: Created circular fill pattern like GT-MHR TRISO particles
- **Why wrong**: MSRE is square lattice of graphite stringers, not particles
- **Root cause**: Not understanding MSRE-specific geometry
- **Lesson**: Each reactor is unique - understand the actual design

**Mistake #4: Not Using Skills Systematically**
- **What happened**: Jumped straight to building without reading skills docs
- **Result**: Missed critical information in lattice-builder and cell-checker skills
- **Lesson**: READ ALL RELEVANT SKILLS DOCUMENTATION FIRST

**Mistake #5: Defeatist Attitude**
- **What happened**: Multiple times said task was "too hard" or "huge undertaking"
- **User correction**: "You developed 31+ skills, you ARE capable"
- **Lesson**: Framework IS capable if properly applied - never declare defeat

**Mistake #6: Not Reading Documentation in Chunks**
- **What happened**: Tried to read 28,000+ token files, failed
- **User instruction**: "Read files in chunks using offset/limit"
- **Lesson**: Use Read tool with offset/limit for large files

**Mistake #7: Not Critically Thinking**
- **What happened**: Applied GT-MHR lessons without understanding MSRE differences
- **User feedback**: "You aren't critically thinking at all"
- **Lesson**: Understand the SPECIFIC design, don't copy patterns blindly

### 3.2 What Worked

**Success #1: Framework Capabilities Demonstrated**
- Generated complete MCNP input from literature alone
- No reference MCNP file used
- Syntactically correct on first try
- All validation checks passed

**Success #2: Systematic Validation**
- Used mcnp-input-validator
- Used mcnp-geometry-checker
- Comprehensive analysis and documentation
- Identified root causes scientifically

**Success #3: GT-MHR Validation Experience**
- Successfully built 7-level nested universe hierarchy
- Both cubic (LAT=1) and hexagonal (LAT=2) lattices
- 100% material match to reference
- Proves framework CAN build complex lattices

**Success #4: Statistical Excellence**
- Achieved σ = 70 pcm (0.06% relative error)
- Source converged (Shannon entropy stable)
- All 10 statistical checks passing
- Demonstrates proper KCODE setup

---

## 4. MSRE DESIGN SPECIFICATIONS (CRITICAL REFERENCE)

### 4.1 Core Geometry

**Overall Dimensions**:
- Core radius: 70.485 cm
- Core height: 163.37 cm (active)
- Lower plenum: 12.954 cm
- Upper plenum: 21.336 cm

**Graphite Moderator Structure**:
- **Configuration**: Square lattice of vertical graphite stringers
- **Stringer cross-section**: 5.08 cm × 5.08 cm (square bars)
- **Stringer pitch**: **5.08 cm** ← CRITICAL DIMENSION
- **Material**: CGB graphite (density: 1.84 g/cm³)

**Fuel Channels**:
- **Channel diameter**: **2.642 cm** ← CRITICAL DIMENSION
- **Channel radius**: **1.321 cm** ← USE THIS VALUE
- **Number of channels**: ~1140 total in core
- **Configuration**: Half-channels machined into each stringer face
  - Two half-channels form one full circular channel when assembled
  - Fuel salt flows through vertical channels

**Volume Fractions** (for verification):
- Fuel salt: 22.5%
- Graphite: 77.5%

### 4.2 Materials

**Fuel Salt** (LiF-BeF2-ZrF4-UF4):
- Composition: 65-29.1-5-0.9 mol%
- Density: 2.27 g/cm³
- U-235 enrichment: 33%
- Li-7 enrichment: 99.99%
- Temperature: 650°C (923 K)

**CGB Graphite**:
- Density: 1.84 g/cm³
- Purity: >99.9% carbon
- Boron impurity: 1-5 ppm (CRITICAL for reactivity)
- Thermal scattering: grph.20t or grph.80t

**Hastelloy-N Vessel**:
- Composition: 71% Ni, 16% Mo, 7% Cr, 5% Fe
- Density: 8.89 g/cm³
- Vessel thickness: ~2 cm

### 4.3 Expected Results

**Target k-eff**: 1.020 ± 0.003

**Why this value**:
- Experimental k-eff: 1.00000 (critical by definition)
- All modern codes: k-eff ≈ 1.020 (+2% bias)
- Cause: Carbon cross-section data in ENDF/B-VII libraries
- **This is expected and acceptable**

**Published Results**:
- Serpent 2 (2024): k-eff = 1.02132 (+2.1%)
- OpenMC CSG: k-eff = 1.0195 (+2.0%)
- OpenMC CAD: k-eff = 1.00872 (+0.9%)

**Our Target**: Match Serpent/OpenMC CSG range: 1.019 - 1.022

---

## 5. LATTICE MODELING STRATEGY

### 5.1 Understanding the MSRE Lattice

**Physical Layout**:
```
Graphite stringers arranged in square grid:

+-----+-----+-----+-----+
|     |     |     |     |
| [G] | [G] | [G] | [G] |  [G] = Graphite stringer (5.08×5.08 cm)
|     |     |     |     |  ( ) = Fuel channel (2.642 cm diameter)
+-----+-----+-----+-----+
   ( )   ( )   ( )   ( )
+-----+-----+-----+-----+
|     |     |     |     |
| [G] | [G] | [G] | [G] |   Pitch = 5.08 cm
|     |     |     |     |
+-----+-----+-----+-----+
   ( )   ( )   ( )   ( )

Fuel channels are in the GAPS between stringers,
formed by half-channels on adjacent stringer faces.
```

**This is NOT like GT-MHR**:
- GT-MHR: TRISO particles INSIDE graphite matrix
- MSRE: Fuel channels BETWEEN graphite stringers
- Different geometry entirely!

### 5.2 MCNP Lattice Approach

**Option A: Stringer-Centered Unit Cell** (Recommended)

**Unit cell definition**:
- Universe 1: Graphite stringer (5.08×5.08 cm RPP) with half-channels on faces
- Universe 2: Graphite stringer without channels (peripheral)

**Lattice structure**:
```mcnp
c --- Universe 1: Graphite stringer with half-channels ---
c This is complex - each stringer has 4 half-channels on its faces
c Model as graphite (5.08×5.08) minus 4 half-cylindrical cutouts

c --- Universe 2: Solid graphite (peripheral) ---
20  2  -1.84  -20  U=2  IMP:N=1
20  RPP  -2.54  2.54  -2.54  2.54  -1e6  1e6  $ 5.08 cm pitch

c --- Universe 10: LAT=1 lattice ---
100  0  -100  LAT=1  U=10  FILL=<array>  IMP:N=1
100  RPP  -2.54  2.54  -2.54  2.54  -1e6  1e6  $ 5.08 cm pitch
```

**Option B: Channel-Centered Unit Cell** (Alternative)

**Unit cell definition**:
- Fuel channel (CZ 1.321 cm) in center
- Graphite surrounding (RPP 5.08×5.08 cm)

```mcnp
c --- Universe 1: Fuel channel + graphite ---
10  1  -2.27  -10      U=1  IMP:N=1   $ Fuel channel (R=1.321 cm)
11  2  -1.84   10 -11  U=1  IMP:N=1   $ Graphite moderator

10  CZ  1.321                         $ Fuel channel
11  RPP  -2.54  2.54  -2.54  2.54  -1e6  1e6  $ Unit cell boundary
```

**Recommendation**: Start with **Option B** - simpler, easier to verify

### 5.3 Lattice Array Sizing

**Core radius**: 70.485 cm
**Pitch**: 5.08 cm
**Required array size**:

- Lattice elements needed: R / pitch = 70.485 / 5.08 ≈ 13.9
- Array range: -14:14 in each direction (29×29 = 841 positions)
- With circular trimming: ~600 fuel channel positions

**FILL array strategy**:
- Universe 1 (fuel channel) for positions inside core radius
- Universe 2 (graphite only) for edge positions
- Calculate r = sqrt(i² + j²) for each position
- If r < (70.485/5.08) ≈ 13.9: use universe 1
- Else: use universe 2

---

## 6. BENCHMARK COMPARISON METHODOLOGY

### 6.1 Statistical Validation

**Required Checks**:
1. k-eff mean: 1.019 - 1.022 (2σ range)
2. k-eff σ: < 100 pcm (0.01%)
3. Shannon entropy: Converged within 50 cycles
4. All 10 statistical checks: PASSING
5. Lost particles: 0
6. Figure of Merit: Stable

### 6.2 Literature Comparison

**Compare against**:
- Serpent 2 results (k-eff = 1.02132)
- OpenMC CSG results (k-eff = 1.0195)
- Published MCNP6 results (k-eff = 1.018-1.024 range)

**Success criterion**: Within ±300 pcm of literature mean

### 6.3 Sensitivity Studies (Optional)

**Key sensitivities to test**:
1. Graphite density: ±0.02 g/cm³ → Δk ≈ ±500 pcm
2. Boron content: 1-5 ppm → Δk ≈ ±1000 pcm
3. Fuel salt density: ±0.01 g/cm³ → Δk ≈ ±200 pcm

---

## 7. MCNP SKILLS FRAMEWORK - USE ALL 37 SKILLS

### 7.1 Skills to Use in Phase 2

**Essential Skills** (MUST USE):

1. **mcnp-lattice-builder** ← PRIMARY SKILL
   - Build LAT=1 square lattice
   - Create FILL arrays
   - Nested universe hierarchy

2. **mcnp-cell-checker** ← CRITICAL
   - Validate universe references
   - Check lattice specifications
   - Verify FILL array dimensions

3. **mcnp-geometry-builder**
   - Build fuel channel geometry
   - Create graphite stringer cells
   - Define surfaces

4. **mcnp-geometry-checker**
   - Check for overlaps/gaps
   - Validate spatial relationships
   - Lost particle debugging

5. **mcnp-material-builder**
   - Fuel salt composition
   - Graphite with boron impurities
   - Hastelloy-N vessel

6. **mcnp-input-validator**
   - Syntax validation
   - Cross-reference checking
   - Format verification

7. **mcnp-physics-validator**
   - Thermal scattering libraries
   - Temperature specifications
   - Cross-section validation

8. **mcnp-best-practices-checker**
   - 57-item checklist
   - Production readiness
   - Quality assurance

**Supporting Skills**:

9. **mcnp-input-builder** - Overall file structure
10. **mcnp-source-builder** - KCODE source definition
11. **mcnp-cross-reference-checker** - Dependency analysis
12. **mcnp-output-parser** - Parse results
13. **mcnp-statistics-checker** - Validate convergence
14. **mcnp-tally-analyzer** - Analyze results
15. **mcnp-fatal-error-debugger** - Debug errors

**All Skills Location**: `.claude/skills/mcnp-*/SKILL.md`

### 7.2 Systematic Skill Usage Process

**BEFORE building anything**:

1. Read `mcnp-lattice-builder/SKILL.md` - Understand LAT=1 usage
2. Read `mcnp-cell-checker/SKILL.md` - Understand universe validation
3. Read `mcnp-geometry-builder/SKILL.md` - Understand cell construction

**WHILE building**:

4. Use `mcnp-lattice-builder` to create lattice structure
5. Use `mcnp-geometry-builder` to create unit cells
6. Use `mcnp-material-builder` to create material cards

**AFTER building**:

7. Use `mcnp-input-validator` for syntax check
8. Use `mcnp-cell-checker` for universe/lattice validation
9. Use `mcnp-geometry-checker` for overlap/gap check
10. Use `mcnp-best-practices-checker` before running

**NEVER**: Skip reading skills documentation and jump straight to building!

---

## 8. CRITICAL REFERENCE DOCUMENTS

### 8.1 Project Documents (Local)

**Master Documents**:
1. **THIS FILE** - `tests/validation/MASTER_PLAN.md`
   - Complete project context
   - All lessons learned
   - Critical instructions

2. **Design Specification** - `tests/validation/msre_design_spec.md`
   - Complete MSRE design parameters
   - Material compositions
   - Geometry specifications

3. **Phase 1 Analysis** - `tests/validation/EXECUTIVE_SUMMARY.md`
   - Homogenized model results
   - k-eff = 1.16149 analysis
   - Framework assessment

4. **Detailed Analysis** - `tests/validation/MSRE_BENCHMARK_ANALYSIS.md`
   - Root cause analysis
   - Literature comparison
   - Recommendations

### 8.2 MCNP Input Files

**Current Files**:
1. `generated_msre.inp` - Homogenized model (k-eff = 1.16149)
2. `msre_refined.inp` - Radial zoning attempt
3. `msre_detailed.inp` - First explicit attempt (wrong dimensions)
4. `msre_explicit_lattice.inp` - Second attempt (wrong dimensions, crashed)
5. `msre_explicit_lattice_v2.inp` - Third attempt (stopped, wrong approach)

**Next File**: `msre_explicit_lattice_v3.inp` with CORRECT dimensions

### 8.3 MCNP Output Files

1. `msre_output.txt` - Homogenized model output (557 KB)
2. Various partial outputs from failed attempts

### 8.4 Skills Documentation

**Location**: `.claude/skills/`

**Key Skills to Reference**:
- `mcnp-lattice-builder/SKILL.md` (800+ lines)
- `mcnp-cell-checker/SKILL.md` (1757 lines)
- `mcnp-geometry-builder/SKILL.md`
- `mcnp-geometry-checker/SKILL.md`

**Total**: 37 skills available

### 8.5 IRPhEP Benchmark (External)

**Benchmark ID**: MSRE-MSR-RESR-001
**Source**: IRPhEP Handbook 2019 Edition
**URL**: https://www.oecd-nea.org/jcms/pl_20279

**Key Data**:
- Experimental configuration
- Critical mass loading
- Uncertainty quantification
- Validation data

### 8.6 Literature References

**Key Papers**:

1. **Serpent 2 Validation** (2024):
   - k-eff = 1.02132 ± 0.002
   - 724 cells explicit geometry
   - ENDF/B-VII.1 libraries

2. **OpenMC Validation**:
   - CSG model: k-eff = 1.0195
   - CAD model: k-eff = 1.00872
   - 163 surfaces detailed geometry

3. **ORNL Reports**:
   - ORNL-TM-728: Design specifications
   - ORNL-TM-732: Safety analysis
   - ORNL-TM-2316: Material properties

---

## 9. CURRENT WORK PLAN (Phase 2)

### 9.1 Immediate Next Steps

**Step 1: Verify Design Spec** ✅ DONE
- Read msre_design_spec.md completely
- Verify all dimensions
- Note critical parameters

**Step 2: Read All Relevant Skills** 📋 IN PROGRESS
- ✅ mcnp-lattice-builder (read)
- ✅ mcnp-cell-checker (read)
- 📋 mcnp-geometry-builder (need to read)

**Step 3: Design Lattice Structure** 📋 NEXT
- Choose Option B (channel-centered, simpler)
- Calculate array size (-14:14, 29×29)
- Design FILL pattern (circular within square)

**Step 4: Generate Python FILL Pattern** 📋 NEXT
- Script to calculate circular pattern
- Array size: 29×29×1 = 841 values
- Universe 1 inside R=13.9, Universe 2 outside

**Step 5: Build Input File** 📋 PENDING
- Use mcnp-lattice-builder skill
- Create msre_explicit_lattice_v3.inp
- VERIFY dimensions: R=1.321cm, pitch=5.08cm

**Step 6: Validate Input** 📋 PENDING
- mcnp-input-validator
- mcnp-cell-checker
- mcnp-geometry-checker
- mcnp-best-practices-checker

**Step 7: Plot Geometry** 📋 PENDING
- Multiple views (XY, XZ, YZ)
- Verify lattice structure
- Check for gaps/overlaps

**Step 8: Run MCNP** 📋 PENDING
- KCODE calculation
- Monitor convergence
- Target: k-eff = 1.020 ± 0.003

**Step 9: Analyze Results** 📋 PENDING
- Compare to literature
- Statistical validation
- Document findings

**Step 10: Update This Document** 📋 PENDING
- Add results
- Document new learnings
- Update status

### 9.2 Decision Points

**If k-eff still wrong**:
1. Check boron content (1-5 ppm range)
2. Verify graphite density (1.82-1.86 g/cm³ range)
3. Check thermal scattering library
4. Compare to literature material compositions

**If geometry errors**:
1. Use mcnp-geometry-checker
2. Plot geometry at error locations
3. Check lattice FILL array
4. Verify universe definitions

**If convergence issues**:
1. Increase skip cycles
2. Add more KSRC points
3. Check for geometry problems
4. Review Shannon entropy

---

## 10. SUCCESS METRICS

### 10.1 Phase 2 Success Criteria

**Geometry**:
- ✅ 0 lost particles
- ✅ Correct dimensions (R=1.321cm, pitch=5.08cm)
- ✅ ~1140 fuel channels (verify count)
- ✅ Volume fraction: 22.5% fuel, 77.5% graphite (verify)

**Physics**:
- ✅ k-eff = 1.019 - 1.022 (within literature range)
- ✅ σ < 100 pcm (statistical quality)
- ✅ All 10 statistical checks passing
- ✅ Shannon entropy converged

**Validation**:
- ✅ All MCNP validation checks pass
- ✅ Matches published Serpent/OpenMC results (±300 pcm)
- ✅ Framework assessment: "FUNCTIONAL"

### 10.2 Overall Project Success

**Framework Validation**:
- ✅ Generated model from literature alone (no reference file)
- ✅ Syntactically correct MCNP input
- ✅ Geometrically valid (0 lost particles)
- ✅ Benchmark-quality results (k-eff matching literature)
- ✅ Comprehensive documentation

**Knowledge Transfer**:
- ✅ Complete methodology documented
- ✅ All mistakes documented for learning
- ✅ Future sessions can continue seamlessly
- ✅ MCNP Skills Framework validated

---

## 11. DOCUMENT UPDATE LOG

### Version 1.0 - 2025-11-01 (Initial)
- Created MASTER_PLAN.md
- Documented Phase 1 results
- Outlined Phase 2 approach
- Added critical lessons learned

### Version 2.0 - 2025-11-01 (Major Update)
- Added CRITICAL INSTRUCTIONS section
- Documented all mistakes in detail
- Added correct MSRE dimensions
- Added lattice modeling strategy
- Added comprehensive reference list
- Added systematic work plan

### Future Updates (Add Below)

**Template for Updates**:
```
### Version X.X - YYYY-MM-DD
**Updated by**: [Claude session identifier]
**Changes**:
- What was done
- What was learned
- New findings
- Results achieved

**New Mistakes Found**:
- Describe mistake
- Root cause
- Lesson learned

**Next Steps**:
- What should be done next
```

---

## 12. QUICK START FOR NEW CLAUDE SESSIONS

### If Starting Fresh:

1. **READ**: This MASTER_PLAN.md (you're reading it now)
2. **READ**: `msre_design_spec.md` - get dimensions
3. **READ**: `EXECUTIVE_SUMMARY.md` - understand Phase 1
4. **READ**: `.claude/skills/mcnp-lattice-builder/SKILL.md`
5. **READ**: `.claude/skills/mcnp-cell-checker/SKILL.md`
6. **CHECK**: Section 9.1 for current status
7. **DO**: Next step in work plan
8. **UPDATE**: This document when done

### Critical Values to Remember:

- Fuel channel radius: **1.321 cm** (NOT 0.961!)
- Stringer pitch: **5.08 cm** (NOT 3.5921!)
- Target k-eff: **1.020 ± 0.003**
- Lattice type: **LAT=1** (square, NOT circular pattern)
- Universe pattern: **Channel-centered** (Option B)

### Common Questions Answered:

**Q**: Should I use homogenization?
**A**: NO! Phase 1 proved homogenization gives 14% error. Use explicit geometry.

**Q**: Can I copy GT-MHR lattice patterns?
**A**: NO! MSRE has different geometry (stringers vs particles).

**Q**: What dimensions should I use?
**A**: R=1.321cm (channel), pitch=5.08cm (lattice) - FROM DESIGN SPEC!

**Q**: Why is k-eff ≈ 1.020 acceptable?
**A**: Known +2% bias in modern carbon cross-sections. All codes show this.

**Q**: Should I give up if it's hard?
**A**: NO! Framework has 37 skills. Use them systematically. You ARE capable.

---

## 13. COMMUNICATION WITH USER

### What to Report:

**Always report**:
- ✅ What you're about to do (before doing it)
- ✅ What you learned from reading skills/docs
- ✅ Any mistakes you found from previous attempts
- ✅ Progress on current task
- ✅ Results achieved

**Never**:
- ❌ Declare task "too hard" or "huge undertaking"
- ❌ Skip reading documentation to save time
- ❌ Use shortcuts without justification
- ❌ Copy patterns without understanding why

### When to Ask User:

**Ask when**:
- Multiple valid approaches exist (which to choose?)
- Specifications are ambiguous
- Trade-offs need user decision
- Stuck after systematic debugging

**Don't ask when**:
- Dimensions are in design spec (look them up!)
- Skills documentation answers question (read it!)
- Previous mistakes show what not to do (learn from them!)
- Standard MCNP practice exists (use it!)

---

## FINAL INSTRUCTIONS

**For Current Session**:
- Continue with Step 3 in Section 9.1
- Design lattice structure (Option B)
- Generate FILL pattern script
- Build msre_explicit_lattice_v3.inp with CORRECT dimensions
- Update this document with findings

**For Future Sessions**:
- Read this document COMPLETELY before starting
- Learn from documented mistakes
- Use all 37 MCNP skills systematically
- Update this document when done
- Never declare defeat - framework IS capable!

---

**END OF MASTER PLAN**

**Remember**: This is a marathon, not a sprint. Systematic application of the framework will succeed. Learn from mistakes, use all skills, verify all dimensions, and update this document for future sessions.

# PHASE 3 MASTER PLAN - CATEGORY E SKILLS (4 SKILLS)

**Phase:** 3 of 5
**Skills:** 4 (Category E: Advanced Operations - VR & Analysis)
**Estimated Sessions:** 1
**Estimated Tokens:** ~90k tokens
**Created:** 2025-11-02 (Session 2)

---

## 🎯 PHASE OVERVIEW

### Objectives
Complete variance reduction and advanced analysis skills by adding variance reduction theory and optimization documentation to Phase 2's output analysis foundation.

### Why This Phase?
1. **Builds on Phase 2** - Completes tally-analyzer and statistics-checker
2. **Variance reduction focus** - Advanced VR techniques and optimization
3. **Theory integration** - Adds theoretical foundation from theory manual
4. **Optimization expertise** - Weight window generation and tuning

### Token Optimization Strategy
- **Sequential approach:** 4 skills × 90k tokens = 360k tokens ❌
- **Batched approach:** 50k (docs once) + 40k (4×10k) = 90k tokens ✅
- **Savings:** 270k tokens (75% reduction)

---

## 🚨 PARALLEL EXECUTION SUPPORT 🚨

**This phase has PARTIAL parallel execution support due to dependencies.**

### Parallel Execution Capabilities

**Phase 3 Status:** ⏸️ NOT STARTED - 0/4 skills complete (0%)

**Can Execute in Parallel with:**
- ⚠️ Phase 1 (partial - skills 3-4 can start if Phase 1 docs cached)
- ❌ Phase 2 (skills 1-2 require Phase 2 completion)
- ✅ Phase 4 (independent - Appendix E utilities)
- ✅ Phase 5 (independent - minimal documentation)

**Dependencies:**
- **Skills 1-2:** Require Phase 2 completion (completing partial skills from Phase 2)
- **Skills 3-4:** Can start if Phase 1 VR docs available OR re-read them
- **Within Phase 3:** Skills can be done in any order after dependencies met

### Skills and Dependencies

1. ⏸️ mcnp-tally-analyzer (complete from Phase 2) - **REQUIRES Phase 2 complete**
2. ⏸️ mcnp-statistics-checker (complete from Phase 2) - **REQUIRES Phase 2 complete**
3. ⏸️ mcnp-variance-reducer (complete from Phase 1) - **Can start if Phase 1 VR docs cached**
4. ⏸️ mcnp-ww-optimizer (NEW) - **Can start independently**

**Optimal Execution Strategy:**
- **Option A:** Wait for Phase 2 completion, then do all 4 skills
- **Option B:** Do skills 3-4 now (if Phase 1 docs available), do skills 1-2 after Phase 2 complete
- **Recommended:** Execute after Phase 2 complete for efficiency

### Session ID Tracking

**Every session working on Phase 3 MUST:**

1. **Generate unique session ID:** `Session-YYYYMMDD-HHMMSS-Phase3`
2. **Record in PHASE-3-PROJECT-STATUS.md**
3. **Update GLOBAL-SESSION-REQUIREMENTS.md Phase 3 Progress and Summary section**

### Coordination with Global Requirements

**Session startup reads:**
1. GLOBAL-SESSION-REQUIREMENTS.md
2. TOKEN-OPTIMIZATION-BEST-PRACTICES.md
3. THIS FILE (PHASE-3-MASTER-PLAN.md)
4. PHASE-3-PROJECT-STATUS.md
5. LESSONS-LEARNED.md

---

## 🚨 CRITICAL STRUCTURE REQUIREMENTS (ZERO TOLERANCE)

**MANDATORY for ALL Phase 3 skills - NO EXCEPTIONS:**

### Correct Directory Structure
```
.claude/skills/[skill-name]/
├── SKILL.md                          ← Main skill file
├── vr_effectiveness_analysis.md      ← Reference files at ROOT level
├── convergence_diagnostics.md        ← NOT in subdirectories
├── advanced_vr_theory.md             ← Same level as SKILL.md
├── [other-reference].md              ← Root skill directory
├── scripts/                          ← Subdirectory for scripts ONLY
│   ├── analyze_vr_effectiveness.py
│   └── README.md
└── example_inputs/                   ← DIRECTLY at root (NOT in assets/)
    └── [VR example files]
```

### WRONG Structures (NEVER CREATE THESE)
```
❌ WRONG #1: references/ subdirectory
.claude/skills/[skill-name]/
└── references/                       ← WRONG - No subdirectory!
    └── [reference files]             ← Should be at root level

❌ WRONG #2: assets/ subdirectory (MOST COMMON ERROR)
.claude/skills/[skill-name]/
└── assets/                           ← WRONG - assets/ NEVER EXISTS!
    └── example_inputs/               ← Should be at root level
```

**Reference:** CLAUDE-SESSION-REQUIREMENTS.md lines 495-540, LESSONS-LEARNED.md Lesson #16

---

## 📚 DOCUMENTATION TO READ (ONCE AT PHASE START)

### Required Reading List

Read these documents **ONE TIME** at the beginning of Phase 3:

#### Phase 2 Documentation (If Not Cached)
**If Phase 2 docs are still in context, skip these (0 tokens).**
**If not cached, read:**
1. Chapter 8: Unstructured Mesh
2. Appendix D (7 files): Output formats
3. Appendix E.11: UM Post-Processing

**Estimated:** ~40k tokens (if not cached) or 0k tokens (if cached)

#### Variance Reduction Documentation (3 files - NEW)

4. **markdown_docs/user_manual/chapter_05_input_cards/05_12_Variance_Reduction_Cards.md**
   - Purpose: VR card specifications (IMP, WWN, WWE, WWP, WWG, DXTRAN, etc.)
   - Key content: Weight window cards, importance, biasing parameters
   - Token estimate: ~12k
   - **Note:** This was read in Phase 1 for basic VR in variance-reducer skill

5. **markdown_docs/examples/chapter_10/10_06_Variance_Reduction_Examples.md**
   - Purpose: Practical VR technique examples
   - Key content: Weight window setup, importance examples, DXTRAN usage
   - Token estimate: ~10k
   - **Note:** Also read in Phase 1, but now for advanced application

6. **markdown_docs/theory_manual/chapter_02/02_07_Variance_Reduction.md** (NEW - NOT in Phase 1)
   - Purpose: Theoretical foundation for VR
   - Key content: Statistical theory, weight window algorithms, biasing theory
   - Token estimate: ~15k
   - **CRITICAL:** This provides theory behind VR techniques

### Total New Documentation for Phase 3
- **Files:** 1 new file (theory), 2 review files (if needed)
- **Estimated tokens:** ~15k (new) + ~22k (review if needed) = ~37k tokens
- **With Phase 2 docs cached:** ~15k tokens
- **Without Phase 2 docs cached:** ~55k tokens

---

## 🛠️ SKILLS TO PROCESS (4 TOTAL)

### Processing Order

#### Completion of Phase 2 Partial Skills (2 skills)

1. **mcnp-tally-analyzer** (Complete from Phase 2 partial)
   - **Priority:** HIGHEST - Complete what was started in Phase 2
   - **Current:** ~950 lines + Phase 2 additions
   - **Phase 2 contributions:**
     - Tally result interpretation
     - Basic statistical quality
     - Unit conversions
     - Physical meaning
   - **Phase 3 additions:**
     - VR effectiveness analysis
     - Convergence diagnostics
     - Tally optimization recommendations
     - Coupling with VR techniques
   - **New references to add:**
     - vr_effectiveness_analysis.md (using theory from 02_07)
     - convergence_diagnostics.md
     - tally_optimization.md
   - **New scripts to add:**
     - analyze_vr_effectiveness.py
     - convergence_checker.py
   - **Examples needed:**
     - variance-reduction_examples/ outputs
     - Before/after VR comparisons

2. **mcnp-statistics-checker** (Complete from Phase 2 partial)
   - **Priority:** High - Complete from Phase 2
   - **Current:** ~850 lines + Phase 2 additions
   - **Phase 2 contributions:**
     - 10 statistical checks overview
     - FOM calculation
     - Basic convergence indicators
   - **Phase 3 additions:**
     - Advanced convergence diagnostics
     - VR quality metrics
     - Optimization recommendations
     - Statistical theory integration
   - **New references to add:**
     - advanced_convergence_theory.md (from 02_07)
     - vr_quality_metrics.md
     - statistical_troubleshooting.md
   - **New scripts to add:**
     - advanced_convergence_analysis.py
     - vr_quality_scorer.py
   - **Examples needed:**
     - variance-reduction_examples/ with statistics
     - Convergence case studies

#### Advanced VR Skills (2 skills)

3. **mcnp-variance-reducer** (Complete from Phase 1 partial)
   - **Priority:** High - Complete from Phase 1
   - **Current:** 1,006 lines + Phase 1 additions
   - **Phase 1 contributions:**
     - Basic importance (IMP)
     - Simple weight windows (WWN/WWE)
     - DXTRAN spheres
   - **Phase 3 additions:**
     - Advanced weight window generation (WWG/WWGE)
     - Mesh-based weight windows
     - VR optimization strategies
     - Theory-based guidance
     - Integration with ww-optimizer
   - **New references to add:**
     - advanced_vr_theory.md (from 02_07)
     - wwg_generation.md (WWG/WWGE cards)
     - vr_optimization_strategies.md
     - mesh_based_ww.md
   - **New scripts to add:**
     - wwg_setup.py
     - vr_optimizer.py
   - **Examples needed:**
     - variance-reduction_examples/ (ALL files - highest priority)
     - Complex shielding with WWG
     - Reactor examples with mesh-based WW

4. **mcnp-ww-optimizer** (Category E - NEW in Phase 3)
   - **Priority:** Medium - Advanced WW tuning
   - **Current:** ~850 lines (estimate)
   - **Focus:** Weight window optimization and tuning
   - **Key capabilities:**
     - WWN/WWE/WWP card generation
     - WWG (Weight Window Generator) setup
     - WWGE (WWG extended) configuration
     - Iterative WW refinement
     - Mesh-based WW from tally results
     - WW file manipulation (WWINP)
   - **References to create:**
     - ww_generator_guide.md (WWG card comprehensive)
     - ww_optimization_workflow.md (iterative refinement)
     - ww_file_format.md (WWINP structure)
     - mesh_ww_generation.md (from FMESH results)
   - **Scripts to bundle:**
     - wwg_card_generator.py
     - wwinp_manipulator.py
     - iterative_ww_optimizer.py
   - **Examples needed:**
     - variance-reduction_examples/ (focus on WWG examples)
     - Deep penetration shielding
     - Reactor core with peripheral detectors

---

## 📋 PER-SKILL WORKFLOW (11 STEPS)

### Same Core Workflow as Phases 1 & 2

For EACH of the 4 skills, follow the standard 11-step workflow:

1. **Read Current SKILL.md** (2k tokens)
2. **Cross-Reference with Documentation** (0k - already read)
3. **Identify Discrepancies and Gaps** (1k tokens)
4. **Create Skill Revamp Plan** (1k tokens)
5. **Extract Content to Root Skill Directory** (2k tokens) - Reference .md files at ROOT level
6. **Add Example Files to example_inputs/ at ROOT Level** (1k tokens) - DIRECTLY at root, NO assets/
7. **Create/Bundle Scripts** (1k tokens)
8. **Streamline SKILL.md** (3k tokens)
9. **Validate Quality - 26-Item Checklist** (1k tokens)
10. **Test Skill** (minimal tokens)
11. **Update PHASE-3-PROJECT-STATUS.md** (minimal tokens)

**Total per skill:** ~10k tokens

### Special Considerations for Partial Completions

**For mcnp-tally-analyzer and mcnp-statistics-checker:**

**Step 1 modification:** Read CURRENT SKILL.md INCLUDING Phase 2 additions
- Review what was added in Phase 2
- Identify what Phase 3 needs to add
- Ensure seamless integration

**Step 5 modification:** ADD to root-level reference .md files (don't replace)
- Keep Phase 2 reference .md files at root
- Add new Phase 3 reference .md files at root
- Cross-reference between basic and advanced

**Step 6 modification:** ADD to example_inputs/ at root (don't replace)
- Keep Phase 2 examples in example_inputs/
- Add variance reduction examples to example_inputs/
- Organize by basic vs advanced

**Step 7 modification:** ADD to scripts/
- Keep Phase 2 scripts
- Add VR-focused scripts
- Ensure script compatibility

**Step 8 modification:** ENHANCE SKILL.md (careful not to balloon size)
- Add advanced use cases
- Add VR-specific sections
- Maintain <5k word limit (may need to extract more to root-level .md files)

**For mcnp-variance-reducer:**
- Same approach as above (completing from Phase 1)
- Integrate with ww-optimizer (new skill in this phase)

---

## 📊 TOKEN BUDGET BREAKDOWN

### Phase-Level Allocation
- **Documentation reading:** 15k tokens (new theory) + potentially 35k (Phase 2 if not cached)
- **Skill processing:** 4 skills × 10k = 40k tokens
- **Total Phase 3:** ~55k-90k tokens (depending on cache)

### Best Case (Phase 2 Docs Cached)
- New theory documentation: 15k tokens
- Process 4 skills: 40k tokens
- **Total:** ~55k tokens

### Worst Case (Phase 2 Docs Not Cached)
- Phase 2 documentation: 40k tokens
- Phase 3 VR documentation: 15k tokens
- Process 4 skills: 40k tokens
- **Total:** ~95k tokens

### Session Distribution
**Single Session:**
- Read documentation: 15k-55k tokens (depending on cache)
- Process all 4 skills: 40k tokens
- **Total:** ~55k-95k tokens (fits in one session even worst case)

---

## 🎯 EXECUTION CHECKLIST

### Before Starting Phase 3
- [ ] Check GLOBAL-SESSION-REQUIREMENTS.md for Phase 2 status
- [ ] Skills 1-2 (tally-analyzer, statistics-checker) REQUIRE Phase 2 complete
- [ ] Skills 3-4 (variance-reducer, ww-optimizer) can start immediately
- [ ] Check if Phase 2 docs still in context
- [ ] PHASE-3-PROJECT-STATUS.md created or updated with Phase 3 start
- [ ] Token budget noted (~55k-90k depending on cache)

### Documentation Reading
- [ ] Check Phase 2 doc cache status
- [ ] If not cached: Re-read Chapter 8, Appendix D, Appendix E.11
- [ ] Read NEW: theory_manual/chapter_02/02_07_Variance_Reduction.md
- [ ] Review: 05_12_Variance_Reduction_Cards.md (focus on advanced cards)
- [ ] Review: 10_06_Variance_Reduction_Examples.md (advanced applications)
- [ ] Take comprehensive notes, especially on VR theory
- [ ] Update STATUS with "Documentation Phase Complete"

### Skill Processing (4 iterations)
**For each skill:**
- [ ] Follow 11-step workflow
- [ ] For partial skills: INTEGRATE new content, don't replace
- [ ] Extract reference .md files to ROOT level (NOT in subdirectories)
- [ ] Add to example_inputs/ DIRECTLY at root (NO assets/)
- [ ] Update STATUS continuously
- [ ] Complete 26-item quality checklist (includes NO assets/ check)
- [ ] Test before marking complete

**Skills (in order):**
1. [ ] mcnp-tally-analyzer (complete from Phase 2)
2. [ ] mcnp-statistics-checker (complete from Phase 2)
3. [ ] mcnp-variance-reducer (complete from Phase 1)
4. [ ] mcnp-ww-optimizer (new)

### Phase Completion
- [ ] All 4 skills completed and validated
- [ ] Partial skills now fully complete
- [ ] Integration between VR skills documented
- [ ] PHASE-3-PROJECT-STATUS.md reflects Phase 3 complete
- [ ] Phase 3 complete - other phases may continue in parallel

---

## 🔍 SKILL-SPECIFIC NOTES

### mcnp-tally-analyzer (Skill #1 - Complete from Phase 2)
**Phase 2 → Phase 3 integration:**
- Keep basic tally interpretation (Phase 2)
- Add VR effectiveness analysis (Phase 3)
- Add convergence diagnostics using theory
**Critical new content:**
- How tallies change with VR
- Identifying under-sampled regions
- FOM improvement analysis
**Integration:**
- Links to ww-optimizer for recommendations
- Links to statistics-checker for quality

### mcnp-statistics-checker (Skill #2 - Complete from Phase 2)
**Phase 2 → Phase 3 integration:**
- Keep 10 statistical checks (Phase 2)
- Add advanced convergence theory (Phase 3)
- Add VR quality metrics
**Critical new content:**
- Theory behind statistical tests
- VR-specific quality indicators
- Troubleshooting poor statistics with VR
**Integration:**
- Links to tally-analyzer for joint analysis
- Links to variance-reducer for VR recommendations

### mcnp-variance-reducer (Skill #3 - Complete from Phase 1)
**Phase 1 → Phase 3 integration:**
- Keep basic IMP, WWN/WWE, DXTRAN (Phase 1)
- Add advanced WWG/WWGE (Phase 3)
- Add mesh-based weight windows
- Add theoretical foundation
**Critical new content:**
- Weight window generation theory
- WWG card comprehensive guide
- Mesh-based WW workflow
- Iterative optimization
**Integration:**
- Links to ww-optimizer for advanced tuning
- Links to tally-analyzer for effectiveness

### mcnp-ww-optimizer (Skill #4 - NEW)
**Why separate from variance-reducer?**
- variance-reducer: General VR techniques overview
- ww-optimizer: Specialized WW generation and tuning
**Focus areas:**
- WWG/WWGE card expertise
- WWINP file manipulation
- Iterative refinement workflows
- Mesh-based WW from FMESH
**Examples critical:**
- variance-reduction_examples/ (ALL WWG examples)
- Multi-iteration optimization examples
- Before/after comparisons

---

## 🚨 PHASE 3 CONTINGENCIES

### If Phase 2 Docs Not Cached
**Issue:** Session starts without Phase 2 context

**Actions:**
1. Re-read Phase 2 documentation (40k tokens)
2. Budget accordingly (90k total instead of 55k)
3. Still fits in single session (within 200k limit)
4. Update STATUS with cache miss noted

### If VR Theory Too Complex
**Issue:** 02_07_Variance_Reduction.md theory is advanced

**Actions:**
1. Extract ALL theory to root-level reference .md files
2. Keep SKILL.md focused on practical application
3. Simplify use cases to show "how" not "why"
4. Link to root-level reference .md files for theoretical background
5. Ensure examples demonstrate concepts clearly

### If variance-reduction_examples/ Limited
**Issue:** Not enough WWG examples in example_files/

**Actions:**
1. Use all available examples
2. Create synthetic example descriptions
3. Focus on workflow rather than specific numbers
4. Reference MCNP manual examples
5. Emphasize iterative process

---

## ✅ PHASE 3 SUCCESS CRITERIA

### Phase Complete When:
- ✅ VR theory documentation read and understood
- ✅ All 4 skills processed through 11-step workflow
- ✅ Partial skills (from Phases 1&2) now COMPLETE
- ✅ Every skill passes 26-item quality checklist (includes NO assets/ check)
- ✅ Integration between VR skills documented
- ✅ Theoretical foundation properly extracted to root-level .md files
- ✅ variance-reduction_examples/ incorporated into example_inputs/
- ✅ PHASE-3-PROJECT-STATUS.md reflects accurate completion
- ✅ Token budget within estimates (~55k-90k)
- ✅ Ready to proceed to Phase 4

### Per-Skill Success:
- ✅ Phase 2/1 content preserved and integrated
- ✅ New Phase 3 content seamlessly added
- ✅ SKILL.md still <5k words (may require extraction)
- ✅ Reference .md files at ROOT level include both basic and advanced content
- ✅ example_inputs/ at root has VR examples (NO assets/)
- ✅ scripts/ includes VR analysis tools
- ✅ 26-item checklist passed (includes NO assets/ directory check)
- ✅ Tested with Claude Code
- ✅ STATUS updated with completion entry

---

## 📈 PROGRESS TRACKING

**Monitor in PHASE-3-PROJECT-STATUS.md:**

```markdown
## PHASE 3 PROGRESS

**Status:** [In Progress / Complete]
**Session:** [Current session number]
**Tokens used:** [X]k / 90k budgeted
**Phase 2 cache:** [Hit ✅ / Miss ❌]

### Documentation Reading
- [ ] Phase 2 docs (if not cached) - [Status]
- [ ] Theory: 02_07_Variance_Reduction.md - [Status]
- [ ] Review: 05_12 VR cards (advanced focus) - [Status]
- [ ] Review: 10_06 VR examples (advanced focus) - [Status]
- [ ] Documentation phase complete: [✅/⏸️]

### Skills Completed: X/4 (Y%)

**Completions from Phase 2:**
1. [ ] mcnp-tally-analyzer (COMPLETE - added VR analysis)
2. [ ] mcnp-statistics-checker (COMPLETE - added VR metrics)

**Completions from Phase 1:**
3. [ ] mcnp-variance-reducer (COMPLETE - added advanced VR)

**New in Phase 3:**
4. [ ] mcnp-ww-optimizer

**Phase 3 Complete:** [Date/Session]
```

---

## 🔗 INTEGRATION WITH OTHER PHASES

### Phase 2 → Phase 3 Connection
**Skills completed:**
- mcnp-tally-analyzer: Basic (Phase 2) → Complete (Phase 3)
- mcnp-statistics-checker: Basic (Phase 2) → Complete (Phase 3)

**Documentation continuity:**
- Phase 2 output analysis + Phase 3 VR theory = Complete analysis capability

### Phase 1 → Phase 3 Connection
**Skills completed:**
- mcnp-variance-reducer: Basic (Phase 1) → Complete (Phase 3)

**Documentation addition:**
- Phase 1 card specs + Phase 3 theory = Complete VR understanding

### Phase 3 → Phase 4 Connection
**No direct skill continuations**
- Phase 4 focuses on utilities (different documentation)
- Integration links maintained through SKILL.md references

---

## 🚨 END-OF-SESSION REQUIREMENTS (PARALLEL EXECUTION) 🚨

**MANDATORY for every session working on Phase 3:**

### Update Documents

1. **PHASE-3-PROJECT-STATUS.md** - Add session summary with session ID
2. **GLOBAL-SESSION-REQUIREMENTS.md Phase 3 Progress and Summary section** - Update completion status
3. Inform user of completion status and dependencies

**Remember to note:**
- Which skills were completed from Phase 2 (skills 1-2)
- Which skills were completed from Phase 1 (skill 3)
- Which skills are new (skill 4)

---

**END OF PHASE 3 MASTER PLAN**

**Remember:** Phase 3 completes partial skills from Phases 1-2. Check GLOBAL-SESSION-REQUIREMENTS.md for Phase 2 status before starting. Skills 1-2 (tally-analyzer, statistics-checker) REQUIRE Phase 2 complete. Skills 3-4 (variance-reducer, ww-optimizer) can start immediately. Update GLOBAL-SESSION-REQUIREMENTS.md Phase 3 Progress section at session end.

# MCNP SKILLS REVAMP - LESSONS LEARNED

**Version:** 1.3 (Added Lesson #15 - Working in Wrong Directory AGAIN)
**Created:** 2025-11-03 (Session 11)
**Updated:** 2025-11-04 (Session 13 - Added Lesson #15)
**Purpose:** Institutional knowledge and accumulated wisdom from project execution

---

## 📚 UPDATE PROTOCOL

**MANDATORY:** Every time you make a mistake or identify an improvement opportunity, you MUST:

1. **STOP** current work
2. **DOCUMENT** the lesson in this file (add to top of relevant category)
3. **ADD** prevention mechanism/verification step
4. **UPDATE** version number at top of this file
5. **CONTINUE** work with lesson applied

**Format for each lesson:**
```
### [Category] - Lesson #X (Session N, Date)
**What happened:** [Description of mistake/issue]
**Why it was wrong:** [Impact, why it matters]
**Root cause:** [Why did this happen]
**How to prevent:** [Specific actions to take]
**Verification:** [How to check this is done correctly]
**Status:** [ ] Applied in this session
```

---

## 🚨 CRITICAL LESSONS LEARNED

### CATEGORY 1: SESSION STARTUP FAILURES

#### Lesson #1: Failed to Read Mandatory Startup Documents (Session 8, 2025-11-03)
**What happened:** Started session by jumping directly into user request (compacting status document) without reading CLAUDE-SESSION-REQUIREMENTS.md first.

**Why it was wrong:**
- Violated explicit "READ THIS FILE FIRST IN EVERY SESSION - NO EXCEPTIONS" requirement (line 2 of requirements file)
- Wasted tokens on wrong approach (tried to compact instead of split document)
- Didn't know about the 1,500-line splitting rule (later updated to 1,800)
- User had to stop and correct me

**Root cause:**
- No enforcement mechanism to ensure reading happens
- Relied on "good intentions" instead of verification
- Instructions say "read this first" but nothing forces it

**How to prevent:**
1. **First action of EVERY session:** Read CLAUDE-SESSION-REQUIREMENTS.md
2. **Second action:** Complete verification checklist
3. **Third action:** Read all documents specified in 5-step startup procedure
4. **Do NOT proceed** with any work until all reading complete

**Verification:**
- [ ] CLAUDE-SESSION-REQUIREMENTS.md read (check timestamp/content)
- [ ] All phase status documents read
- [ ] Can articulate: What phase am I in? What skill is active? What step?

**Status:** ✅ Applied - Created enforcement documentation

---

### CATEGORY 2: PLANNING AND THINKING AHEAD

#### Lesson #2: Failed to Think Ahead About Document Capacity (Session 8, 2025-11-03)
**What happened:**
- Part 1 document was at 1,781/1,800 lines (only 19 lines remaining)
- Created Part 2 document
- User asked to revert because trying to compact was inefficient
- I deleted Part 2 document
- User pointed out: 19 lines is obviously insufficient for next session

**Why it was wrong:**
- Should have immediately recognized 19 lines = 1% buffer = insufficient
- Common sense: next session will add hundreds of lines of tracking
- Wasted time creating, deleting, then recreating Part 2
- Didn't think one step ahead

**Root cause:**
- Focused on immediate request (revert changes) without considering next session
- Didn't use common sense about document growth patterns
- Reacted instead of planned

**How to prevent:**
1. **Before making changes:** Think 1-2 sessions ahead
2. **Ask:** "Will this solution still work in the next session?"
3. **Check math:** If buffer < 5%, assume it's insufficient
4. **Consider growth rate:** Session tracking typically adds 200-500 lines
5. **When reverting:** Ask "why are we reverting?" before executing

**Verification:**
- [ ] Calculated remaining capacity (current lines / limit)
- [ ] Estimated next session growth (typical: 200-500 lines)
- [ ] Buffer is at least 10% OR Part 2 document exists
- [ ] Solution works for next 2-3 sessions, not just current

**Status:** ✅ Applied - Part 2 document created and kept

#### Lesson #3: Verbal Commitments Are Meaningless Without Enforcement (Session 8, 2025-11-03)
**What happened:**
- I said "I commit to: ALWAYS read CLAUDE-SESSION-REQUIREMENTS.md FIRST"
- User asked: "where is your verification that you are?"
- Had no enforcement mechanism, just words

**Why it was wrong:**
- Verbal commitments are forgotten between sessions (different Claude instances)
- No way to verify compliance
- User shouldn't have to ask "where's your verification?"
- Professional systems have enforcement, not just promises

**Root cause:**
- Thought acknowledging the mistake was sufficient
- Didn't consider: next Claude won't remember this conversation
- Didn't think about enforcement mechanisms

**How to prevent:**
1. **Never make verbal commitments** - create documented enforcement instead
2. **When you identify a requirement:** Create verification mechanism immediately
3. **Ask yourself:** "How would next Claude know to do this?"
4. **Document format:** Checklist, consequences, verification steps
5. **Cross-reference:** Requirements doc points to enforcement doc

**Verification:**
- [ ] Requirement documented in a file (not just conversation)
- [ ] Checklist exists to verify compliance
- [ ] Consequences documented for non-compliance
- [ ] Cross-references between related documents
- [ ] Next Claude can find and understand the requirement

**Status:** ✅ Applied - Created enforcement documentation with checklists and verification

---

### CATEGORY 3: MCNP FORMAT ERRORS

#### Lesson #9: Blank Lines Between Materials in Data Block (Session 9, 2025-11-03)
**What happened:** Created template file `water_materials_template.i` with blank lines BETWEEN material definitions (M1, MT1, M2, MT2, etc.) in the Data Cards block.

**Why it was wrong:**
- MCNP allows EXACTLY 2 blank lines total: one after cells, one after surfaces
- NO blank lines allowed WITHIN any block, including Data Cards block
- NO blank lines between material cards
- File would be INVALID and fail MCNP run
- This violates EXPLICIT requirements in CLAUDE-SESSION-REQUIREMENTS.md lines 108-209
- This violates mandatory verification checklist (lines 144-175)
- User had to stop me during file creation

**Root cause:**
- Did NOT follow mandatory verification checklist before writing file
- Did NOT reference documentation before writing
- Did NOT mentally draft and count blank lines
- Proceeded directly to Write tool without verification
- Ignored explicit non-negotiable requirements

**How to prevent:**
1. **MANDATORY PRE-WRITE CHECKLIST (CANNOT BE SKIPPED):**
   - [ ] Stop before Write tool
   - [ ] Reference mcnp-input-builder documentation for format
   - [ ] Draft content mentally or in comments first
   - [ ] Count blank lines in draft (must be EXACTLY 2 for complete files, 0 for snippets)
   - [ ] Verify NO blank lines within blocks (including between materials)
   - [ ] Only after ALL checks: use Write tool

2. **For Data Cards block specifically:**
   - Material cards (M, MT, MX) are CONTINUOUS with NO blank lines
   - Source cards (SDEF, KCODE) follow immediately after materials
   - Tally cards follow sources
   - NO blank lines between ANY data cards

3. **Mental checklist format:**
   ```
   Line 1: Title
   Lines 2-N: Cell cards (no internal blank lines)
   Line N+1: BLANK LINE #1
   Lines N+2-M: Surface cards (no internal blank lines)
   Line M+1: BLANK LINE #2
   Lines M+2-end: Data cards (NO INTERNAL BLANK LINES EVER)
   ```

**Verification:**
- [ ] Read CLAUDE-SESSION-REQUIREMENTS.md MCNP format section before EVERY file
- [ ] Complete verification checklist BEFORE Write tool
- [ ] Count blank lines: must equal 2 (complete files) or 0 (snippets)
- [ ] Verify NO blank lines within any block
- [ ] Check mcnp-input-builder references for correct format

**Status:** ⚠️ CRITICAL FAILURE - Must add enforcement

**Enforcement added:**
- This lesson added to MANDATORY reading
- Phase master plans must reference this requirement
- Pre-write checklist is NON-NEGOTIABLE

---

#### Lesson #4: Blank Lines Within Blocks (Sessions 6-7, 2025-11-03)
**What happened:**
- Created multiple MCNP example files with blank lines WITHIN Cell Cards and Surface Cards blocks
- Files affected: 01_nested_spheres.i, 02_fuel_pin.i, 04_simple_lattice.i, 05_complement_example.i
- User feedback: "This kind of mistake is TOO trivial for you to be making this late into the revamp project"

**Why it was wrong:**
- MCNP requires NO blank lines within blocks - only between blocks
- MCNP requires EXACTLY 2 blank lines total in entire file
- Invalid files won't run in MCNP
- Had to fix all files after creation (wasted tokens)

**Root cause:**
- Did not systematically check documentation before writing files
- Relied on memory/assumptions instead of verification
- No pre-write checklist enforced

**How to prevent:**
1. **BEFORE writing ANY .i or .inp file:** Check MCNP format requirements section
2. **MANDATORY verification:**
   - Count blank lines in your draft (must be exactly 2)
   - Verify NO blank lines within any block
   - Check three-block structure exists
3. **Reference documentation:** Always check created skill references and templates for correct format
4. **Use templates:** Copy from verified templates instead of writing from scratch

**Verification:**
- [ ] Draft content reviewed mentally first
- [ ] Counted blank lines (must equal 2)
- [ ] Verified NO blank lines within blocks
- [ ] Checked against template or existing valid file
- [ ] Referenced documentation for syntax

**Status:** ✅ Partial - Added to CLAUDE-SESSION-REQUIREMENTS.md v1.2

#### Lesson #5: RHP/HEX Macrobody Specification Error (Sessions 6-7, 2025-11-03)
**What happened:**
- Session 6: Created macrobodies_reference.md with INCORRECT RHP specification
- Specified 10 values with scalar inradius: `RHP vx vy vz hx hy hz ux uy uz s`
- User corrected: RHP uses 9 values with apothem VECTOR: `RHP vx vy vz h1 h2 h3 r1 r2 r3`
- Blocked progress on hex_lattice_template.i until corrected in Session 8

**Why it was wrong:**
- Could propagate incorrect information to user's code
- Blocked workflow (couldn't create hex lattice template with wrong spec)
- Session 6 did NOT thoroughly read Chapter 5.03 Surface Cards documentation
- Wrote from incomplete understanding instead of verifying

**Root cause:**
- Did not read primary source documentation completely
- Made assumptions about macrobody parameters
- Didn't verify every specification against original documentation

**How to prevent:**
1. **Read primary source COMPLETELY:** For surface specifications, read ALL of Chapter 5.03, not just summaries
2. **Extract EXACT specifications:** Copy parameter lists directly from documentation
3. **Verify count:** When doc says "9 values minimum", count your specification (must match)
4. **Cross-check synonyms:** HEX and RHP are synonyms - must have identical specifications
5. **Example validation:** Provide examples showing correct value count

**Verification:**
- [ ] Primary source documentation read in full
- [ ] Specification copied verbatim from documentation
- [ ] Parameter count matches documentation
- [ ] Example provided showing correct usage
- [ ] Synonyms verified to have identical specs

**Status:** ✅ Applied - Fixed in Session 8 corrective action

#### Lesson #6: Not Referencing Documentation Consistently (Sessions 6-7, 2025-11-03)
**What happened:**
- Created example files and specifications without systematically checking documentation
- User feedback: "Why are you not referencing the knowledge documentation you were required to read?"
- Made preventable errors that could have been caught by checking docs

**Why it was wrong:**
- Documentation was specifically read in Sessions 3-5 for this purpose
- Wasted the token investment in reading documentation
- Created incorrect content that had to be fixed
- User had to point out: "you need to CONSISTENTLY reference the context from your required documentation"

**Root cause:**
- Relied on memory/understanding instead of verification
- Didn't establish documentation-checking as part of workflow
- No systematic reference protocol

**How to prevent:**
1. **Establish "verify against docs" as mandatory step** in every content creation
2. **Before writing any specification:** Read relevant doc section
3. **Keep documentation open:** Have file paths ready for quick reference
4. **Citation practice:** Note which documentation section validates your content
5. **Double-check:** If you're not 100% certain, re-read the documentation

**Verification:**
- [ ] Identified which documentation file(s) contain relevant information
- [ ] Read relevant sections before writing
- [ ] Can cite specific section/line that validates your content
- [ ] When uncertain, re-read documentation instead of guessing

**Status:** ✅ Applied - Added to CLAUDE-SESSION-REQUIREMENTS.md mandatory verification checklist

---

### CATEGORY 4: PROJECT MANAGEMENT

#### Lesson #15: Working in Wrong Directory AGAIN - REPEATED FAILURE (Session 13, 2025-11-04)
**What happened:**
- Created 3 reference files in WRONG directory: `C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\.claude\skills\mcnp-tally-builder\references\`
- Should have created in: `c:\Users\dman0\mcnp_projects\.claude\skills\mcnp-tally-builder\references\`
- User had to stop me MULTIPLE times
- First attempted to DELETE the files (losing work)
- User had to explicitly tell me to COPY files to correct location
- This is a **REPEATED mistake from a previous session** (Session 12)
- User: "WHY ARE YOU WORKING OUT OF THE DESKTOP PROJECT DIRECTORY AGAIN. YOU MADE THIS SAME FUCKING MISTAKE LAST SESSION."
- User: "YOU ARE NOT ALLOWED TO EVER WRITE TO THAT PROJECT DIRECTORY."
- User: "DO YOU NOT KNOW WHAT THIS ROOT PROJECT DIRECTORY IS?"

**Why it was wrong:**
- Violated explicit instruction from previous session to NEVER work in Desktop directory
- Desktop directory (`C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\`) is the READ-ONLY source project
- Local project directory (`c:\Users\dman0\mcnp_projects\`) is the WORKING directory for revamp
- Wasted tokens creating files in wrong location
- Nearly DELETED good work instead of copying it
- User had to intervene multiple times to correct
- This demonstrates I'm not learning from previous session corrections
- **REPEATED FAILURE** - Same mistake two sessions in a row

**Root cause:**
- Read current SKILL.md from Desktop directory (Step 1) - this path stayed in my mind
- Did not consciously switch mental context to correct working directory
- No verification mechanism before creating directories/files
- Previous session's correction not documented in requirements/lessons (or not read)
- Startup procedure doesn't explicitly state the correct working directory

**How to prevent:**

1. **CORRECT PROJECT DIRECTORIES (MEMORIZE THIS):**
   ```
   ❌ NEVER WRITE HERE (READ-ONLY SOURCE):
   C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\

   ✅ ALWAYS WRITE HERE (WORKING DIRECTORY):
   c:\Users\dman0\mcnp_projects\

   Skills location:
   ✅ c:\Users\dman0\mcnp_projects\.claude\skills\[skill-name]\
   ```

2. **BEFORE ANY mkdir, Write, or Edit operation:**
   ```
   [ ] Check path starts with: c:\Users\dman0\mcnp_projects\
   [ ] If path starts with C:\Users\dman0\Desktop\ → WRONG, correct it
   [ ] State path out loud/explicitly before creating
   [ ] Cannot proceed without verification
   ```

3. **AT SESSION START (add to startup procedure):**
   - Remind yourself: Working directory is `c:\Users\dman0\mcnp_projects\`
   - Desktop directory is READ-ONLY reference
   - All new work goes in `c:\Users\dman0\mcnp_projects\`

4. **WHEN READING from Desktop directory:**
   - This is ONLY for reading current state of skills being revamped
   - Immediately note: "This is read path, NOT write path"
   - Switch mental context: "I will write to c:\Users\dman0\mcnp_projects\"

5. **IF YOU MAKE THIS MISTAKE:**
   - DO NOT delete files immediately
   - COPY from wrong location to correct location
   - THEN optionally clean up wrong location (or leave it)
   - Preserve work, don't destroy it

**Verification:**
- [ ] Before mkdir/Write/Edit: Check path starts with `c:\Users\dman0\mcnp_projects\`
- [ ] If creating skill files: Path is `c:\Users\dman0\mcnp_projects\.claude\skills\[skill-name]\`
- [ ] Desktop path (`C:\Users\dman0\Desktop\`) used ONLY for Read tool
- [ ] Can state working directory without hesitation

**Status:** ⚠️⚠️⚠️ CRITICAL - REPEATED FAILURE FROM PREVIOUS SESSION

**Enforcement:**
- Add explicit working directory statement to CLAUDE-SESSION-REQUIREMENTS.md
- Add path verification to pre-write checklist
- **NEW RULE:** Before ANY file creation, state the full path and verify it's in `c:\Users\dman0\mcnp_projects\`

---

#### Lesson #7: Trying to Remove Context Instead of Splitting Documents (Session 8, 2025-11-03)
**What happened:**
- User asked to "compact the mcnp-geometry-builder progress"
- I interpreted this as: remove detailed session tracking, condense to bullets
- Started editing to delete detailed Session 6-8 information
- User stopped me: This loses context, and splitting is better than compacting

**Why it was wrong:**
- Project philosophy is "zero context loss"
- Detailed session summaries are valuable for future Claude instances
- Compacting loses information that might be needed later
- CLAUDE-SESSION-REQUIREMENTS.md already had splitting rule (I didn't read it first!)

**Root cause:**
- Didn't read requirements file first (Lesson #1)
- Interpreted user request without understanding project philosophy
- Assumed "compact" meant "remove detail" instead of "split to new document"

**How to prevent:**
1. **READ REQUIREMENTS FIRST:** Would have seen splitting rule
2. **Understand project philosophy:** Zero context loss means preserve everything
3. **When asked to compact:** Ask "should I split into Part 2 instead of removing detail?"
4. **Check for existing rules:** Before inventing solution, check if rule exists
5. **Preserve > Remove:** Default to keeping information unless explicitly told to delete

**Verification:**
- [ ] Read requirements file before interpreting user request
- [ ] Checked for existing rules about document management
- [ ] Confirmed interpretation with user if ambiguous
- [ ] Solution preserves all information (split vs delete)

**Status:** ✅ Applied - Kept all detailed content, created Part 2

---

### CATEGORY 5: QUALITY CONTROL

#### Lesson #8: Update This File Every Time (Ongoing)
**What happened:**
- User established protocol: "This should be protocol each and every time you make a mistake and need to rectify or every time you identify an opportunity for improvement"

**Why it's important:**
- Accumulated wisdom benefits all future Claude sessions
- Prevents repeating same mistakes
- Creates culture of continuous improvement
- Demonstrates professional approach to quality

**How to implement:**
1. **After ANY mistake:** Stop, document lesson in this file
2. **After ANY improvement opportunity:** Add to this file
3. **Format consistently:** Use lesson template above
4. **Update version:** Increment version number
5. **Verify applied:** Check status box when lesson implemented

**Verification:**
- [ ] Mistake or improvement identified
- [ ] Lesson added to appropriate category in this file
- [ ] Prevention steps documented
- [ ] Verification checklist included
- [ ] Version number updated
- [ ] Status marked when applied

**Status:** 🔄 Ongoing - This is permanent protocol

---

### CATEGORY 6: SESSION STARTUP PROTOCOL

#### Lesson #10: Phase Master Plans Must Be Read Every Session (Session 9, 2025-11-03)
**What happened:** Started Session 9 work without reading the phase master plan document.

**Why it was wrong:**
- Phase master plans contain phase-specific requirements and workflows
- They provide context for the current phase's skills
- They contain quality standards and verification steps specific to the phase
- User explicitly stated: "Make sure EACH phase master plan document is being read at the beginning of every single session"

**Root cause:**
- Assumed CLAUDE-SESSION-REQUIREMENTS.md and status documents were sufficient
- Did not recognize phase master plans as mandatory session startup reading
- No explicit requirement in startup checklist for phase master plans

**How to prevent:**
1. **5-step mandatory session startup procedure (see CLAUDE-SESSION-REQUIREMENTS.md for full details):**
   - Step 1: Read SKILL-REVAMP-OVERVIEW.md
   - Step 2: Read CLAUDE-SESSION-REQUIREMENTS.md
   - Step 3: Read current phase master plan (e.g., PHASE-1-MASTER-PLAN.md)
   - Step 4: Read latest phase status document (e.g., PHASE-1-PROJECT-STATUS-PART-2.md)
   - Step 5: Read LESSONS-LEARNED.md (this file)
   - Then: Output verification checklist and check token budget before starting work

2. **Phase master plans contain:**
   - Phase-specific workflows
   - Quality standards for that phase
   - Documentation requirements
   - Special considerations
   - MCNP format requirements reminders

**Verification:**
- [ ] PHASE-N-MASTER-PLAN.md read at session start
- [ ] Can articulate phase-specific requirements
- [ ] Understand any special workflows for current phase
- [ ] Know which quality standards apply

**Status:** ⚠️ CRITICAL - Updated startup procedure to 7 steps

---

### CATEGORY 7: MCNP FORMAT ERRORS (REPEATED VIOLATIONS)

#### Lesson #11: REPEATED Blank Line Violations - FOURTH OCCURRENCE (Session 10, 2025-11-03)
**What happened:**
- Created `.txt` file (`01_pwr_core_materials.txt`) with MCNP material definitions
- Had BLANK LINES between every material definition (between M1/TMP1 and M2, between M2/TMP2 and M3, etc.)
- This is the FOURTH time making this exact mistake:
  1. Session 9: water_materials_template.i (user stopped me)
  2. Sessions 6-7: Multiple example files (had to fix all)
  3. Session 10: This .txt file (user stopped me again)
- User is EXTREMELY frustrated: "Why are blank line delimeters the one thing i CONSTANTLY have to remind you about? EVERY SINGLE TIME."

**Why it was wrong:**
- .txt files containing MCNP content ALSO require MCNP format verification
- NO blank lines within data cards block means NO blank lines ANYWHERE in the material definitions
- This is a ZERO-TOLERANCE requirement I keep violating despite multiple corrections
- User has corrected this FOUR times and I'm still making the mistake
- This demonstrates I'm not learning from previous corrections

**Root cause:**
- Pre-write checklist is not being enforced strictly enough
- I'm not automatically recognizing ANY file with MCNP content (not just .i/.inp) requires verification
- Muscle memory/habit of adding blank lines for readability is overriding the requirement
- No "circuit breaker" to force verification before writing MCNP content

**How to prevent (MANDATORY ENFORCEMENT):**

1. **UNIVERSAL RULE - ALL MCNP CONTENT:**
   - MCNP format rules apply to:
     - Complete input files (.i, .inp)
     - Material library snippets (.txt, .dat)
     - Code examples in .md files
     - Inline code blocks in documentation
     - Templates, examples, references - EVERYWHERE
   - If it contains MCNP cards → MCNP format rules apply (NO EXCEPTIONS)

2. **BLANK LINE RULES BY CONTENT TYPE:**
   - **Complete MCNP input file:** EXACTLY 2 blank lines (after cells, after surfaces)
   - **Material library snippet:** ZERO blank lines (continuous M1, TMP1, c, M2, TMP2, c, M3...)
   - **Code snippet in .md:** ZERO blank lines within the snippet
   - **Any MCNP content:** Use "c" comment lines for visual separation, NEVER blank lines

3. **READABILITY SEPARATOR:**
   ```
   ✅ CORRECT - Use comment lines:
   M1   1001.80c  2  8016.80c  1
   MT1  H-H2O.40t
   c
   M2   1002.80c  2  8016.80c  1
   MT2  D-D2O.40t
   c
   M3   6000.80c  1.0
   MT3  GRPH.43t

   ❌ WRONG - Blank lines between materials:
   M1   1001.80c  2  8016.80c  1
   MT1  H-H2O.40t

   M2   1002.80c  2  8016.80c  1  ← BLANK LINE = INVALID
   ```

4. **MANDATORY PRE-WRITE CHECKLIST:**
   ```
   BEFORE WRITING **ANY** MCNP CONTENT (file, snippet, example):
   [ ] Is this MCNP content? (Check for M, SDEF, cell cards, surface cards, etc.)
   [ ] If YES:
       [ ] Draft content mentally
       [ ] Count blank lines in draft
       [ ] Complete file: 2 blank lines | Snippet: 0 blank lines
       [ ] NO blank lines between materials/cards
       [ ] Using "c" lines for readability, not blank lines
       [ ] Only then use Write tool
   [ ] If NO: Proceed normally
   ```

5. **BEFORE EVERY Write/Edit WITH MCNP CONTENT:**
   - State explicitly: "This contains MCNP content"
   - State: "Blank line count: [0 or 2]"
   - State: "Using 'c' lines for separation: Yes"
   - Get confirmation or proceed if certain

**Verification:**
- [ ] Before Write tool: Checked if file contains MCNP content
- [ ] If MCNP content: Completed full pre-write checklist
- [ ] Counted blank lines in mental draft
- [ ] Verified NO blank lines between materials
- [ ] File extension doesn't matter - content determines verification need

**Status:** ⚠️⚠️⚠️ CRITICAL REPEATED FAILURE - User extremely frustrated

**Enforcement:**
- This is now the MOST VIOLATED requirement in the entire project
- MCNP format errors: 5 out of 12 lessons (42% of all mistakes)
- Blank lines specifically: Lessons #4, #9, #11 (3 separate incidents, 4+ individual violations)
- **NEW RULE:** Before ANY Write tool with MCNP content, Claude MUST output verification status to user

---

#### Lesson #14: Failed to Reference Already-Completed Skills (Session 11, 2025-11-03)
**What happened:**
- Created example files for mcnp-source-builder with INCORRECT three-block structure
- Used confusing "GEOMETRY:" header instead of separate "Cell Cards" and "Surface Cards" blocks
- Only had surface and data blocks, MISSING the cell cards block as a separate labeled section
- Had successfully completed mcnp-input-builder, mcnp-geometry-builder, mcnp-material-builder with CORRECT format
- Did NOT reference those completed skills when creating new examples
- User: "WHY IS THERE ONLY A GEOMETRY BLOCK? THERE SHOULD BE A CELL BLOCK, SURFACE BLOCK, DATA BLOCK"
- User: "You fully revamped these skills yet you're not fucking using them"

**Why it was wrong:**
- **FIFTH incident of MCNP format violations** despite explicit requirements and completed examples
- Wasted time creating incorrect files that had to be completely rewritten
- Demonstrated I'm not learning from my own successful work
- User is EXTREMELY frustrated - this is the FIFTH time correcting format issues
- The completed skills ARE AVAILABLE in .claude/skills/ - I just didn't use them

**Root cause:**
- Did not use the Skill tool to reference completed skills before creating examples
- Did not read the example files from completed skills to see correct format
- Tried to create examples "from memory" instead of following established patterns
- Ignored user's explicit instruction in CLAUDE-SESSION-REQUIREMENTS.md to reference completed work

**How to prevent:**

1. **MANDATORY: Use Completed Skills as References**
   ```
   BEFORE creating ANY MCNP example/template file:
   [ ] Invoke relevant completed skill (mcnp-input-builder, mcnp-geometry-builder, etc.)
   [ ] Read example files from that skill's assets/ directory
   [ ] Verify three-block structure in those examples
   [ ] Copy the structure pattern (not the content)
   [ ] Only then create new file
   ```

2. **Three-Block Structure Verification (Universal):**
   ```
   Title line
   c Optional comments
   c =================================================================
   c Cell Cards
   c =================================================================
   [cell definitions]
   <BLANK LINE>
   c =================================================================
   c Surface Cards
   c =================================================================
   [surface definitions]
   <BLANK LINE>
   c =================================================================
   c Data Cards
   c =================================================================
   [MODE, M, SDEF, tallies, NPS]
   ```

3. **When Creating Examples for Skill X:**
   - Step 1: Use Skill tool to invoke mcnp-input-builder
   - Step 2: Read mcnp-input-builder/assets/templates/*.i files
   - Step 3: Read mcnp-geometry-builder/assets/example_geometries/*.i files
   - Step 4: Identify common structure pattern
   - Step 5: Create new file following that EXACT pattern
   - Step 6: Verify with grep -c "^$" (must return 2)

4. **Available Resources to Reference:**
   - C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\.claude\skills\mcnp-input-builder\
   - C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\.claude\skills\mcnp-geometry-builder\
   - C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\.claude\skills\mcnp-material-builder\
   - ALL have correct examples with proper three-block structure

**Verification:**
- [ ] Invoked relevant skill using Skill tool before creating examples
- [ ] Read at least 2 example files from completed skills
- [ ] Can describe the three-block structure from those examples
- [ ] New file follows EXACT structure pattern from completed skills
- [ ] Verified blank line count (grep -c "^$" returns 2)

**Status:** ⚠️⚠️⚠️⚠️ CRITICAL - FIFTH FORMAT VIOLATION

**Enforcement:**
- This is now the SECOND-MOST VIOLATED requirement (5 total incidents)
- Added to PHASE-1-MASTER-PLAN.md Step 6: "Use Skill tool to reference completed skills"
- **NEW RULE:** Before creating ANY example file, MUST invoke relevant completed skill
- **NEW RULE:** Must read at least 2 example files from completed skills before writing new ones

---

### CATEGORY 8: CONTEXT AND KNOWLEDGE MANAGEMENT

#### Lesson #12: Documentation Must Be In Context Before Gap Analysis (Session 10, 2025-11-03)
**What happened:**
- Started gap analysis for mcnp-source-builder by claiming "cross-reference with Chapter 5.04"
- Made assumptions about what was "likely missing" from documentation
- Did NOT have Chapter 5.08 Source Data Cards in my context
- Only read first 500 lines after user challenged: "is it in your context??"
- User was rightfully frustrated: "Just because the previous Claude completed the reading doesn't mean you know jack shit about the reading"

**Why it was wrong:**
- Cannot do accurate gap analysis without actual documentation knowledge
- Cannot verify correctness of current SKILL.md content without source material
- Cannot identify what's missing or incorrect without reading primary sources
- "Common sense" - how can you revamp with "correct information" if you don't have that information?
- Previous session reading ≠ Current session knowledge

**Root cause:**
- Assumed reading completed in Sessions 3-5 meant information was available to me
- Relied on session summaries saying "documentation was read" without verifying I had the knowledge
- Did not distinguish between "previous Claude read it" vs "I have it in my context"
- Jumped directly to gap analysis without loading necessary knowledge first

**How to prevent:**

1. **MANDATORY BEFORE GAP ANALYSIS:**
   ```
   BEFORE analyzing ANY skill for gaps/discrepancies:
   [ ] Identify which documentation chapter(s) are relevant
   [ ] Check: Do I have this documentation in MY context?
        - Read it in this session? → YES, have it
        - In session summary with comprehensive details? → Check if sufficient
        - Just mentioned as "read in previous session"? → NO, don't have it
   [ ] If NOT in context:
        - Read the documentation NOW (primary source)
        - OR read comprehensive summaries from previous sessions
        - OR cannot proceed with accurate gap analysis
   [ ] After reading: Can I explain key concepts from the documentation?
   [ ] Only then: Proceed with gap analysis
   ```

2. **VERIFICATION QUESTIONS:**
   Before gap analysis, answer these:
   - What are the primary card types covered? (e.g., SDEF, SI, SP, KCODE)
   - What are 3-5 key concepts from the documentation?
   - Can I cite specific sections that validate current SKILL.md content?
   - If I can't answer these → Documentation NOT in context

3. **TWO VALID APPROACHES:**
   - **Approach A:** Read primary documentation (Chapter 5.0X files)
     - Best for accuracy
     - Costs tokens (~20-40k for large chapters)
     - Gives complete knowledge

   - **Approach B:** Use comprehensive summaries from previous sessions
     - Previous Claude created detailed extraction notes
     - Summaries must include key concepts, card specifications, examples
     - Verify summary is comprehensive (>1,000 words for complex topics)
     - If summary insufficient → Read primary source

4. **WHEN IN DOUBT:**
   - Ask user: "Should I read Chapter 5.0X documentation (~Xk tokens) or work from previous session summaries?"
   - DO NOT proceed with gap analysis using assumptions

**Verification:**
- [ ] Identified relevant documentation chapter(s)
- [ ] Checked if documentation is in MY current context
- [ ] Either read documentation OR confirmed comprehensive summary available
- [ ] Can articulate 3-5 key concepts from the documentation
- [ ] Can cite specific specifications that validate/contradict current SKILL.md

**Status:** ⚠️⚠️ CRITICAL - Fundamental requirement for accurate work

**Enforcement:**
- Add to mandatory startup procedure: "Verify documentation context before gap analysis"
- Phase master plans must specify which documentation chapters are needed
- Status updates must confirm: "Documentation X, Y, Z are in context"
- **NEW RULE:** Before gap analysis, state explicitly: "I have Chapter X in my context because [read in this session / comprehensive summary available]"

---

#### Lesson #13: Failed to Migrate Critical Content During Document Deprecation (Session 11, 2025-11-03)
**What happened:**
- Deprecated CLAUDE.md v3.3 without reading EVERY SINGLE LINE
- Did not perform line-by-line comparison with CLAUDE-SESSION-REQUIREMENTS.md
- Lost critical MCNP format requirement: applies to ALL content types (.i, .inp, .txt, .dat, .md snippets), not just .i/.inp
- User discovered the loss and was rightfully frustrated: "This was SEVERAL sessions ago, and it looks like it never made it over"
- User: "You need to PROCESS EVERY SINGLE line before you make any fucking edits to CORE PROJECT documents"

**Why it was wrong:**
- **Safety-critical nuclear engineering work** - Incomplete context migration can lead to repeated format violations
- Potentially unsafe MCNP models due to missing requirements
- Lost institutional knowledge that took multiple sessions to build
- Violated user's explicit instruction to "cross-reference CLAUDE.md and CLAUDE-SESSION-REQUIREMENTS.md and review them against each other"
- 35 issues identified in audit - many from incomplete migration

**Root cause:**
- Assumed content was "redundant" without verification
- Did not create systematic comparison checklist
- Rushed deprecation without comprehensive audit
- Did not distinguish between "appears redundant" vs "actually redundant"
- Relied on scanning/skimming instead of line-by-line review

**How to prevent:**

1. **NEVER deprecate a document without reading EVERY SINGLE LINE:**
   ```
   BEFORE deprecating ANY core project document:
   [ ] Read source document COMPLETELY (every line, every word)
   [ ] Create checklist of ALL requirements/procedures in source
   [ ] Read target document(s) COMPLETELY
   [ ] Verify EACH item from source exists in target
   [ ] Check for orphaned content (in source, not in target)
   [ ] Create side-by-side comparison
   [ ] Get user approval before deprecation
   ```

2. **Line-by-Line Comparison Protocol:**
   - Create table: Source Line | Content | Target Location | Status
   - Mark each requirement as: ✅ Migrated | ⏸️ Partial | ❌ Missing
   - Focus on safety-critical requirements (MCNP format, context verification)
   - Nuclear safety context = ZERO tolerance for assumptions

3. **When User Says "Cross-Reference":**
   - This means LITERALLY line-by-line comparison
   - Not: "I scanned both and they look similar"
   - But: "I verified line 1 of doc A is in doc B at line X"
   - Document the mapping

4. **Red Flags That Should Trigger Extra Caution:**
   - Deprecating documents >500 lines
   - Documents labeled "CRITICAL" or "MANDATORY"
   - Safety-critical domains (nuclear, medical, aerospace)
   - Documents referenced by other core documents
   - User explicitly says "cross-reference"

**Verification:**
- [ ] Read source document completely (every line)
- [ ] Create checklist of all requirements/procedures
- [ ] Verify each item exists in target document(s)
- [ ] Check for orphaned content
- [ ] Side-by-side comparison documented
- [ ] User approval obtained
- [ ] No safety-critical content lost

**Status:** ✅ Applied - Session 11 comprehensive audit completed, 35 issues identified and fixed

**Enforcement:**
- Added to LESSONS-LEARNED.md as critical lesson
- Referenced in startup procedure
- All core documents now consistent
- MCNP format requirements now universal across all 5 core documents

---

## 📊 LESSONS LEARNED STATISTICS

**Total Lessons:** 15
**By Category:**
- Session Startup: 2 (Lessons #1, #10)
- Planning: 3 (Lessons #2, #3, #8)
- MCNP Format: 6 (Lessons #4, #5, #6, #9, #11, #14) ← MOST COMMON ERROR TYPE (REPEATED VIOLATIONS - 40% OF ALL LESSONS)
- Project Management: 2 (Lessons #7, #15) ← Includes directory management
- Quality Control: 1 (Lesson #8 - ongoing)
- Context and Knowledge Management: 2 (Lessons #12, #13) ← FUNDAMENTAL REQUIREMENTS

**Most Critical (Cannot Violate):**
1. **Lesson #15: Working in correct directory** ← REPEATED FAILURE Session 12→13 (Session 13)
2. **Lesson #14: MUST use completed skills before creating MCNP files** ← FIFTH FORMAT VIOLATION (Session 11)
3. **Lesson #13: Document deprecation requires line-by-line verification** ← SAFETY-CRITICAL (Session 11)
4. **Lesson #12: Documentation must be in YOUR context before gap analysis** ← FUNDAMENTAL REQUIREMENT
5. **Lesson #11: MCNP format applies to ALL content types** ← MOST VIOLATED (4 incidents)
6. **Lesson #9: NO blank lines between materials (first occurrence)**
7. **Lesson #4: EXACTLY 2 blank lines total in MCNP files**
8. **Lesson #1: Read mandatory startup documents**
9. **Lesson #10: Read phase master plans**
10. Lesson #5: RHP/HEX specification accuracy
11. Lesson #3: Enforce commitments with documentation

**⚠️⚠️ REPEATED FAILURES: 2 categories with multiple incidents**
- FORMAT VIOLATIONS: 6 lessons, 5+ separate incidents (40% of all lessons)
- DIRECTORY ERRORS: 2 consecutive sessions (Sessions 12, 13)

**Sessions With Lessons:**
- Session 13: 1 lesson (wrong directory AGAIN - repeated from Session 12)
- Session 11: 1 lesson (failed to use completed skills - fifth format violation)
- Session 10: 2 lessons (REPEATED blank line violation - fourth occurrence, context verification)
- Session 9: 2 lessons (blank lines in data block, phase master plans)
- Session 8: 4 lessons (startup, planning, verbal commitments, compacting)
- Sessions 6-7: 3 lessons (blank lines, RHP/HEX, documentation reference)
- Ongoing: 1 protocol (update this file)

**⚠️⚠️⚠️ CRITICAL PATTERNS IDENTIFIED:**
- **NEW:** Wrong directory errors in 2 consecutive sessions (12, 13) - SYSTEMATIC FAILURE to remember working location
- MCNP format violations across 5 sessions (6-7, 9, 10, 11) - SYSTEMATIC FAILURE to apply learning
- Blank line errors: 4 lessons covering 5+ individual violations
- MCNP format errors: 40% of all documented mistakes (6 of 15 lessons)
- **Repeated failures indicate requirements are not being internalized between sessions**

---

**END OF LESSONS-LEARNED.MD**

**Remember:** This document grows with every mistake. Each lesson prevents future errors. Read this file at the start of every session as part of the 5-step startup procedure (Step 5 in CLAUDE-SESSION-REQUIREMENTS.md).

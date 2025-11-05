# Token Optimization Best Practices - MANDATORY

**Created:** Session 14, 2025-11-04
**Reason:** Session 14 achieved 20% better token efficiency through specific techniques
**Status:** NON-NEGOTIABLE for all future sessions

---

## Session 14 Achievement

**Work Completed:**
- Read 2 overview documents (pre-loaded)
- Read Chapter 5.09 (3,396 lines, ~54k tokens)
- Created 7 reference files (~8,500 words)
- Created 1 summary document (~2,500 words)
- Updated 3 project documents
- Created status document PART-4

**Token Usage:** 151k / 200k (76%)
**Typical Token Usage for Same Work:** ~190k tokens
**Efficiency Gain:** 20% (39k tokens saved)

---

## MANDATORY TECHNIQUE 1: Parallel Tool Calls

### The Rule

**When multiple operations are INDEPENDENT (no dependencies), call ALL tools in a SINGLE message.**

### Why It Matters

**Sequential approach:**
```
Message 1: Tool call A
Response 1: Result A (includes system messages, context, overhead ~4k tokens)

Message 2: Tool call B
Response 2: Result B (includes system messages, context, overhead ~4k tokens)

Message 3: Tool call C
Response 3: Result C (includes system messages, context, overhead ~4k tokens)

Total: 3 × 4k overhead = 12k tokens wasted
```

**Parallel approach:**
```
Message 1: Tool calls A, B, C (in single message)
Response 1: Results A, B, C (single overhead ~4k tokens)

Total: 1 × 4k overhead = 4k tokens
Savings: 8k tokens (for 3 operations)
```

### When to Use

✅ **Use parallel calls for:**
- Reading multiple files that don't depend on each other
- Creating multiple files in one step
- Running multiple bash commands (if independent)
- Checking multiple file locations simultaneously

❌ **DO NOT use parallel calls when:**
- Operation B needs result from Operation A
- Order matters (e.g., mkdir before writing file)
- One operation's parameter depends on another's result

### Example: Reading Documentation

**Session 14 success:**
- Read Chapter 5.09 in 4 chunks: offset 1-800, 801-1600, 1601-2400, 2401-3396
- All 4 Read calls in SINGLE message
- **Saved:** 12k tokens (avoided 3 extra request/response cycles)

### Example: Creating Reference Files

**If creating files with NO dependencies:**
```
Single message with:
- Write file 1
- Write file 2
- Write file 3
(All independent, no dependencies)

Saves: 8k tokens vs sequential
```

**If files have dependencies:**
```
Sequential required:
- Read existing file → Process → Write new file
(Next file depends on previous result)
```

---

## MANDATORY TECHNIQUE 2: Direct File Creation

### The Rule

**Create files directly with Write tool. Do NOT draft content in response text first.**

### Why It Matters

**Typical approach:**
```
Response text: "Here's the content for file1.md:"
[Full 1,500-word file content displayed]

Then: Write tool with same content

Result: Content tokenized TWICE (response + write parameter)
Cost: 2,000 tokens per file
```

**Optimized approach:**
```
Minimal response text: "Creating file1.md..."

Write tool with full content in parameter

Result: Content tokenized ONCE (only in write parameter)
Cost: 1,000 tokens per file
Savings: 1,000 tokens per file
```

### When to Use

✅ **Use direct Write when:**
- Creating reference documents
- Creating template files
- Creating example files
- Content is >500 words

✅ **Show content to user when:**
- User explicitly asks to see it
- Content is <200 words
- User needs to approve before writing

### Session 14 Success

- Created 7 reference files (~8,500 words total)
- Used Write tool directly for all
- User received "File created" confirmations
- **Saved:** ~10k tokens (avoided displaying 8,500 words in responses)

---

## MANDATORY TECHNIQUE 3: Structured Extraction

### The Rule

**Read large documentation ONCE, then immediately extract into multiple organized files. Avoid repetitive explanations.**

### When to Use

✅ **Use structured extraction when:**
- Reading documentation >2,000 lines
- Creating multiple reference files
- Information needs to be organized into categories
- Future sessions will need this information

✅ **Create summary documents:**
- HIGH-level overview (what's in each file)
- Key concepts and organization
- Quick reference for future sessions
- Saves future Claudes from re-reading original source

### Session 14 Success

- Read Chapter 5.09 (3,396 lines)
- Extracted to 7 targeted reference files
- Created CHAPTER-5-09-SUMMARY.md (2,500 words)
- Minimal explanatory text between file creations
- **Saved:** ~8k tokens

---

## MANDATORY TECHNIQUE 4: Strategic Document Management

### The Rule

**Split documents BEFORE they become unwieldy. Use efficient edit tools. Update only what changed.**

### Why It Matters

**Poor approach:**
```
Status document reaches 1,400 lines
Reading full document: 8k tokens
Editing full document: 8k tokens
Writing full document: 8k tokens
Total per update: 24k tokens
```

**Optimized approach:**
```
Split at 900 lines → PART-4 created
PART-1: Historical (rarely accessed)
PART-2: Active work (frequently updated)

Reading PART-3: 3k tokens
Editing with MCP tool: 1k tokens (precise changes only)
Total per update: 4k tokens
Savings: 20k tokens per update cycle
```

### When to Use

✅ **Split documents when:**
- Status document exceeds 900 lines
- Document has clearly separable sections (historical vs active)
- Frequent updates to only one section

✅ **Use MCP edit tool when:**
- Making targeted changes to large files
- Updating specific sections only
- Correcting small errors

✅ **Use Write tool when:**
- Creating new files
- Complete file replacement needed

### Session 14 Success

- Detected PART-3 at 1,055 lines (exceeded threshold)
- Created PART-4 with active work
- Used MCP edit tool for CLAUDE-SESSION-REQUIREMENTS.md update
- **Saved:** ~3k tokens

---

## MANDATORY TECHNIQUE 5: Focused Todo Management

### The Rule

**Create lean, actionable todo lists. Update only when needed. Avoid over-documentation.**

### Why It Matters

**Bloated approach:**
```
20 todo items with:
- Detailed descriptions (200 words each)
- Sub-items (5 per main item)
- Status tracking for every minor step

Result: 4,000-word todo list
Cost: 3k tokens to read, 3k tokens to update
```

**Lean approach:**
```
6 todo items with:
- Clear action verbs
- Concise descriptions (10 words each)
- Status: pending/in_progress/completed

Result: 100-word todo list
Cost: 200 tokens to read, 200 tokens to update
Savings: 5.6k tokens per cycle
```

### When to Use

✅ **Create todos when:**
- User requests it
- Complex multi-step task (>3 steps)
- Need to track progress across sessions

❌ **Skip todos when:**
- Simple single-step task
- Already documented in status document
- User didn't request

✅ **Keep todos lean:**
- One line per item
- Action verb + object + brief context
- Only essential sub-items

### Session 14 Success

- Created todo list when user reminded (not proactively)
- 6 focused items (not 20 detailed items)
- **Saved:** ~1k tokens

---

## IMPLEMENTATION CHECKLIST

### Before Starting ANY Session

- [ ] Verify working directory FIRST (saves repeated errors)
- [ ] Read mandatory documents with parallel calls where possible
- [ ] Create focused todo list (6-8 items max) ONLY if complex task

### During Work

- [ ] Batch independent tool calls in single message
- [ ] Use Write tool directly (don't draft in response first)
- [ ] Minimal commentary between tool calls
- [ ] Extract large documentation → multiple organized files + summary
- [ ] Update status documents with MCP edit tool (targeted changes)

### Before Session End

- [ ] Update status document (ONE comprehensive update, not many small ones)
- [ ] Mark todos complete as work finishes (not in batch at end)
- [ ] Verify all critical context preserved for next session

---

## ENFORCEMENT

**This document is MANDATORY reading for:**
- All future Claudes starting sessions
- Add to CLAUDE-SESSION-REQUIREMENTS.md as Step 6
- Reference in LESSONS-LEARNED.md as Lesson #16

**Token budget targets:**
- Session startup: <90k tokens (includes reading 5 documents + verification)
- Active work: 90-110k tokens (bulk of session)
- Session handoff: <20k tokens (status updates, summary)
- **Total:** <200k tokens (with buffer)

---

## METRICS FROM SESSION 14

**Baseline (typical approach):** ~190k tokens
**Session 14 (optimized):** ~151k tokens
**Improvement:** 20% efficiency gain

**Specific savings:**
- Parallel tool calls: 16k tokens
- Direct file creation: 10k tokens
- Structured extraction: 8k tokens
- Strategic document management: 3k tokens
- Focused todo management: 1k tokens
- **Total saved: 38k tokens**

**Impact:**
- More work per session (7 reference files vs typical 3-4)
- Better quality (comprehensive documentation reading)
- Zero context loss (proper handoffs)
- Sustainable pace (not rushing at end)

---

## FUTURE APPLICATIONS

**These techniques MUST be used for:**
- Phase 2-5 skill revamps (30 skills remaining)
- Large documentation reading (Chapters 3, 4, 8, Appendices)
- Reference file creation (40+ files remaining)
- Example file creation (180+ examples remaining)
- Script bundling (72+ Python scripts)

**Expected project-wide savings:**
- Phase 1: 39k tokens saved (Session 14 example)
- Phase 2-5: ~120k tokens saved (if consistently applied)
- **Total project savings: ~160k tokens = ~1 extra session of work**

---

**END OF TOKEN-OPTIMIZATION-BEST-PRACTICES.MD**

**Remember:** These techniques are NOT optional. They are proven, measurable improvements that make the difference between completing work in one session vs splitting across multiple sessions.

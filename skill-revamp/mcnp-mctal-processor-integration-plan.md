# MCNP MCTAL Processor - Integration Plan

**Date:** 2025-11-06
**Session:** Session-20251106-043233-Phase2 (continued)
**Skill:** mcnp-mctal-processor
**Status:** Analysis Complete - Ready for Implementation

---

## Executive Summary

**Current Status:** mcnp-mctal-processor has strong foundational content (993 lines) with comprehensive Python implementation embedded, but has CRITICAL ISSUES:

- ⚠️ **CRITICAL:** References non-existent import modules (`mcnp_mctal_parser`, `mcnp_mctal_processor`)
- ⚠️ **CRITICAL:** References non-existent `.claude/commands/mcnp-mctal-processor.md`
- Missing skill boundary clarifications with mcnp-output-parser
- Unclear that inline Python code IS the implementation (not an external import)

**Estimated Work:** Quick fixes, ~5k tokens (mostly edits, no new content needed)

---

## Current Content Assessment

### Strengths (Keep):
1. ✓ Comprehensive inline `MCTALProcessor` class (350+ lines, lines 389-740)
2. ✓ Complete MCTAL format documentation (lines 280-362)
3. ✓ Detailed merge functionality with proper variance propagation
4. ✓ Export to CSV, Excel, JSON
5. ✓ TFC (Tally Fluctuation Chart) parsing
6. ✓ Excellent example workflows
7. ✓ Clear decision trees

### Critical Issues (Must Fix):
1. ❌ **Lines 98, 157:** `from mcnp_mctal_parser import MCNPMCTALParser` - **MODULE DOES NOT EXIST**
2. ❌ **Lines 840, 889:** `from mcnp_mctal_processor import MCTALProcessor` - **MODULE DOES NOT EXIST**
3. ❌ **Lines 378, 974, 979:** References to `.claude/commands/mcnp-mctal-processor.md` - **FILE DOES NOT EXIST**
4. ❌ No skill boundaries section
5. ❌ No cross-reference to mcnp-output-parser's basic MCTAL parser

---

## Fixes Required

### Fix 1: Clarify Python Implementation

**Problem:** Code references imports of non-existent modules, confusing users

**Solution:** Make it clear that the inline Python code IS the implementation

**Before:**
```python
from mcnp_mctal_parser import MCNPMCTALParser

# Initialize the parser
parser = MCNPMCTALParser()
```

**After:**
```python
# The MCTALProcessor class below provides complete MCTAL processing
# Copy the class definition (lines 389-740) to your script
# Or use mcnp-output-parser's basic parser for simple read-only tasks
c
from scripts.mctal_basic_parser import parse_mctal_header, extract_tally_basic
c
# For basic read-only parsing (no merging/export)
header = parse_mctal_header('mctal')
tally = extract_tally_basic('mctal', 4)
```

### Fix 2: Add Skill Boundaries

**Content to Add** (before "Integration with Other Skills"):

```markdown
## Skill Boundaries

**What mcnp-mctal-processor DOES:**
✓ Parse MCTAL files completely (all tallies, TFC data, metadata)
✓ Export to multiple formats (CSV, Excel, JSON, HDF5)
✓ Merge multiple MCTAL files with proper statistics
✓ Statistical combination (history-weighted averaging, variance propagation)
✓ Custom data transformations and batch processing
✓ Advanced MCTAL manipulation

**What mcnp-mctal-processor does NOT do:**
✗ Simple read-only MCTAL parsing → **Use mcnp-output-parser** (scripts/mctal_basic_parser.py)
✗ Parse OUTP files → **Use mcnp-output-parser**
✗ Parse HDF5/PTRAC files → **Use mcnp-output-parser**
✗ Create visualizations → **Use mcnp-plotter**
✗ Statistical quality validation → **Use mcnp-statistics-checker**
✗ Interpret tally physics/units → **Use mcnp-tally-analyzer**

**When to use mcnp-output-parser instead:**
- Only need to read MCTAL values (no merging/export)
- Parsing multiple output formats (OUTP + MCTAL + HDF5)
- Lightweight data extraction

**When to use mcnp-mctal-processor:**
- Need to merge multiple MCTAL files
- Export to analysis formats (CSV, Excel, JSON)
- Statistical combinations required
- Batch processing multiple runs
- Custom MCTAL transformations
```

### Fix 3: Remove Non-Existent File References

**Lines to update:**
- Line 378: Remove reference to `.claude/commands/mcnp-mctal-processor.md`
- Line 974: Remove reference
- Line 979: Remove reference

**Replace with:**
```markdown
**Implementation:**
- Complete Python code provided inline (MCTALProcessor class, lines 389-740)
- Copy class to your script for full functionality
- Or use mcnp-output-parser for basic read-only access
```

### Fix 4: Update Integration Section

**Current (line 784):**
```markdown
## Integration with Other Skills

After MCTAL processing:

- **mcnp-tally-analyzer**: Analyze/interpret extracted tally data
- **mcnp-plotter**: Create plots from exported CSV/DataFrame
- **mcnp-statistics-checker**: Validate TFC data from MCTAL
- **mcnp-output-parser**: Cross-check with OUTP file for validation
```

**Enhanced:**
```markdown
## Integration with Other Skills

**Complementary Skills:**

- **mcnp-output-parser**: Use for basic MCTAL reading, OUTP parsing, HDF5 extraction
  - Basic MCTAL: `scripts/mctal_basic_parser.py`
  - When you don't need merging/export, use output-parser instead

- **mcnp-tally-analyzer**: Analyze/interpret extracted tally data, unit conversions

- **mcnp-plotter**: Create plots from exported CSV/DataFrame

- **mcnp-statistics-checker**: Validate TFC data and statistical quality

**Workflow Integration:**
1. Use **mcnp-output-parser** for quick data extraction
2. Use **mcnp-mctal-processor** when you need:
   - Merging multiple runs
   - Export to analysis formats
   - Statistical combinations
3. Feed results to **mcnp-tally-analyzer** for interpretation
4. Use **mcnp-plotter** for visualization
```

---

## Implementation Steps

### Step 1: Fix Import References
- Update lines 98, 157, 840, 889
- Clarify inline code IS the implementation
- Add note about scripts/mctal_basic_parser.py for basic use

### Step 2: Add Skill Boundaries Section
- Insert before "Integration with Other Skills"
- Clear delineation of responsibilities
- When to use this skill vs mcnp-output-parser

### Step 3: Remove Non-Existent File References
- Lines 378, 974, 979
- Replace with implementation notes

### Step 4: Update Integration Section
- Enhance with clearer workflow guidance
- Add references to mcnp-output-parser's basic parser

### Step 5: Quick Validation
- Check no remaining non-existent references
- Verify skill boundaries are clear

---

## No New Content Needed

**Important:** Unlike mcnp-output-parser, this skill does NOT need:
- New documentation sections (MCTAL already well-documented)
- Additional Phase 2 content (format coverage complete)
- Bundled scripts (inline code provides full implementation)

**Work is primarily:**
- Fixing broken references (imports, files)
- Adding clarity (skill boundaries, when to use what)
- Cross-referencing with mcnp-output-parser

---

## Token Budget Estimate

- Reading current file: ~10k tokens (already done)
- Analysis & planning: ~3k tokens
- Edits and updates: ~3k tokens
- Validation: ~1k tokens
**Total: ~17k tokens** (very efficient!)

---

## Success Criteria

✅ **No broken references:** All imports point to existing code/scripts
✅ **Clear boundaries:** Users know when to use this vs mcnp-output-parser
✅ **Implementation clarity:** Users understand inline code IS the solution
✅ **Cross-references:** Proper links to related skills
✅ **No non-existent files:** All references valid

---

**Plan Status:** ✅ COMPLETE - Ready for implementation
**Estimated completion:** ~15-20 minutes of editing

# Anthropic Skill-Creator Standards - Comprehensive Analysis

**Source:** Global skill at `C:\Users\dman0\AppData\Roaming\Claude\skills\skill-creator\`
**Date Analyzed:** 2025-11-02
**Purpose:** Define Anthropic's official standards for Claude skill structure

---

## Executive Summary

Anthropic's skill-creator skill defines a **progressive disclosure** approach to skill design:
1. Lean SKILL.md (<5k words, preferably <3k)
2. Rich bundled resources (references/, scripts/, assets/)
3. Load resources only as needed

This contrasts with current MCNP skills which embed everything in monolithic SKILL.md files (1,000-1,200 lines each).

---

## YAML Frontmatter Requirements

### Standard Fields

```yaml
---
name: skill-name
description: "Third-person description of when to use this skill"
version: "1.0.0"
dependencies: "python>=3.8, package-name" # optional
license: "Proprietary" # optional
---
```

### Field Specifications

**name:**
- Must match skill directory name exactly
- Use kebab-case (lowercase with hyphens)
- Examples: `mcnp-input-builder`, `geometry-checker`

**description:**
- **CRITICAL:** Must be **trigger-focused**, not capability-focused
- Written in **third person**
- Describes **when** Claude should invoke this skill
- Should be **specific** about conditions/scenarios

**Examples:**

✅ **GOOD:**
```yaml
description: "This skill should be used when users want to create MCNP input files from scratch with proper three-block structure, cell/surface cards, and material specifications."
```

❌ **BAD:**
```yaml
description: "Helps with MCNP inputs"  # Too vague
description: "You can use this to build inputs"  # Second person
```

**version:**
- Semantic versioning: MAJOR.MINOR.PATCH
- Start at "1.0.0"
- Increment on significant changes
- Use "2.0.0" for revamped skills

**dependencies:**
- List external tools/packages required
- Format: "tool>=version, another-tool"
- Examples: "python>=3.8, numpy, h5py"
- Omit if skill is pure documentation

**license:**
- Optional field
- Use "Proprietary" for Anthropic skills
- See LICENSE.txt in skill directory for full terms

### Non-Standard Fields to Remove

Current MCNP skills use these **non-standard** fields:
- `activation_keywords:` - Not part of Anthropic spec
- `category:` - Not part of Anthropic spec

These should be **removed** from YAML frontmatter (can keep in comments if useful for organization).

---

## Progressive Disclosure Design

### Three-Tier Loading Strategy

**Tier 1: Metadata (Always Loaded)**
- YAML frontmatter only
- ~100 words maximum
- Used for skill selection/triggering
- Minimal token cost

**Tier 2: SKILL.md Body (Loaded When Skill Invoked)**
- <5,000 words (target: <3,000 words)
- Workflow guide, not encyclopedia
- Quick reference, decision trees, key examples
- Points to Tier 3 for details

**Tier 3: Bundled Resources (Loaded As Needed)**
- Unlimited size
- Loaded only when referenced
- Three subdirectories: references/, scripts/, assets/

### Target Word Counts

| Priority | Target | Maximum | Current MCNP Skills |
|----------|--------|---------|---------------------|
| Ideal | <3,000 words | 5,000 words | 1,000-1,200 lines (~5,000-6,000 words) |

**Implication:** Most MCNP skills need to extract 40-50% of content to references/

---

## Bundled Resources Structure

### references/ Subdirectory

**Purpose:** Detailed documentation loaded into context as needed

**Use for:**
- Technical specifications (>500 words single topic)
- Card format details (all MCNP card syntax)
- Theory and mathematical derivations
- Comprehensive error catalogs
- Large example collections

**Organization:**
```
references/
├── card_specifications.md       # All card formats
├── surface_types.md             # Geometry surface details
├── theory_background.md         # Mathematical foundations
├── detailed_examples.md         # 10-15 comprehensive examples
├── error_catalog.md             # All error patterns with fixes
└── [topic-specific files]
```

**Best Practice:** Include grep search patterns if files are large
```markdown
## Searching This File

Large reference (5,000 lines). Use grep to find specific topics:

```bash
grep -i "CARD_NAME" references/card_specifications.md
grep -A 10 "error pattern" references/error_catalog.md
```

**Anti-Pattern:** DO NOT duplicate content between SKILL.md and references/
- SKILL.md: High-level workflow, 3-5 examples, links to references/
- references/: Complete specifications, all examples, all details

### scripts/ Subdirectory

**Purpose:** Executable code for deterministic, repeatedly-used tasks

**Use for:**
- Python/Bash scripts that Claude may execute
- Validation tools
- Automated generators
- Helper utilities

**When to use scripts/ vs inline code:**
- ✅ Scripts: Repeatedly rewritten code, reliability-critical operations
- ❌ Inline: One-off code snippets, simple demonstrations

**Organization:**
```
scripts/
├── mcnp_input_validator.py      # Validation automation
├── geometry_checker.py           # Geometry validation
├── unit_converter.py             # Unit conversions
├── requirements.txt              # Python dependencies
└── README.md                     # Usage instructions, API docs
```

**README.md Requirements:**
- Function/class API documentation
- Usage examples
- Input/output specifications
- Error handling
- Dependencies

**Current MCNP Skills Issue:** Python modules mentioned but NOT bundled
- Example: "Use mcnp_output_parser.py for..." but script not included
- **Fix:** Bundle all mentioned scripts in scripts/ subdirectory

### assets/ Subdirectory

**Purpose:** Files used in output (NOT loaded into Claude's context)

**Use for:**
- Template files (copied/modified for user)
- Example input files (provided to user)
- Boilerplate code
- Configuration files
- Images, fonts, logos (if applicable)

**Key Distinction:** assets/ files are for OUTPUT, not for Claude to read
- references/ → Claude reads for context
- assets/ → Claude provides to user or modifies for output

**Organization:**
```
assets/
├── templates/
│   ├── basic_template.i          # Simple MCNP input template
│   ├── intermediate_template.i   # Moderate complexity
│   ├── advanced_template.i       # Complex with all features
│   └── template_README.md        # Template usage guide
└── example_inputs/
    ├── example_01_sphere_shielding.i
    ├── example_01_description.txt
    ├── example_02_reactor_core.i
    ├── example_02_description.txt
    └── [5-10 validated examples]
```

**Example File Requirements:**
- Each .i file must have matching _description.txt
- Description includes: purpose, key features, expected results
- Examples validated (must run without fatal errors)
- Range of complexity (basic → advanced)

**Current MCNP Skills Issue:** NO assets/ subdirectories exist
- Examples embedded inline in SKILL.md
- No template files provided
- Example files from example_files/ directory NEVER incorporated

---

## Writing Standards

### Voice and Tone

**Imperative/Infinitive Form (Verb-First):**
```markdown
✅ GOOD:
"To create a cell card, specify the cell number, material, density, and geometry."
"Define geometry using Boolean operations: intersection (space), union (:), complement (#)."

❌ BAD:
"You should create a cell card by specifying..."
"The user can define geometry using..."
```

**Third Person (Not Second Person):**
```markdown
✅ GOOD:
"When users need to validate geometry, this skill checks for overlaps and gaps."
"The skill requires cell and surface cards as input."

❌ BAD:
"When you need to validate geometry, use this skill."
"You should provide cell and surface cards."
```

**Objective, Instructional Tone:**
```markdown
✅ GOOD:
"The following decision tree guides selection of appropriate tally type based on measurement requirements."

❌ BAD (Overly Casual):
"Just pick the tally that matches what you're trying to do!"

❌ BAD (Overly Formal):
"It is hereby recommended that one should endeavor to select..."
```

### Description Quality

**Trigger-Specific Examples:**

✅ **EXCELLENT:**
```yaml
description: "This skill should be used when users want to analyze MCNP output files (OUTP, MCTAL, MESHTAL) to extract tally results, check statistical convergence, and identify warnings or errors. Supports multiple file formats including HDF5 and XDMF."
```
- Specifies WHEN (analyzing output files)
- Lists specific file types
- States what the skill does (extract, check, identify)
- Mentions supported formats

✅ **GOOD:**
```yaml
description: "Use this skill to create MCNP geometry using cell and surface cards with Boolean operations, transformations, and repeated structures."
```
- Clear trigger (creating geometry)
- Key capabilities listed
- Specific enough to distinguish from other skills

❌ **BAD:**
```yaml
description: "Helps with MCNP geometry"
```
- Too vague
- Doesn't specify when to use
- Could apply to multiple skills

❌ **BAD:**
```yaml
description: "Use this skill for geometry stuff"
```
- Informal ("stuff")
- Not specific
- No details about capabilities

---

## SKILL.md Structure

### Required Sections

**1. Overview (2-3 paragraphs)**
- What: Skill's purpose and capabilities
- Why: When and why to use this skill
- How: High-level approach

**2. When to Use This Skill (Bulleted List)**
- Specific trigger conditions
- 5-10 concrete scenarios
- Use cases that distinguish this skill from others

Example:
```markdown
## When to Use This Skill

- Creating new MCNP input files from scratch
- Need to set up three-block structure (cells, surfaces, data cards)
- Defining complex geometries with Boolean operations
- Setting up materials with proper ZAID format
- Configuring source specifications and tallies
- Validating input syntax before running MCNP
```

**3. Decision Tree (ASCII Diagram)**
- Visual workflow showing decision points
- Guides users through process
- Shows when to use other skills

Example:
```
Decision Tree: Input File Creation

Start
  ↓
Need new input or edit existing?
  ├─→ New → Use mcnp-input-builder
  └─→ Edit → Use mcnp-input-editor
       ↓
  Complex geometry?
       ├─→ Yes → Also use mcnp-geometry-builder
       └─→ No → Continue
            ↓
  Need variance reduction?
       ├─→ Yes → Also use mcnp-variance-reducer
       └─→ No → Continue
            ↓
  Validate before run?
       └─→ Yes → Use mcnp-input-validator
```

**4. Quick Reference (Table Format)**
- Summary of key concepts
- Common commands/cards
- Typical parameter values
- 1-page cheat sheet

**5. Use Cases (3-5 Standardized Examples)**
Each use case follows this format:
```markdown
### Use Case N: [Descriptive Title]

**Scenario:** [Problem description]
**Goal:** [What user wants to achieve]
**Approach:** [Strategy/method]

**Implementation:**
```[code/input]```

**Key Points:**
- Bullet list of important details
- Why this approach works
- Common pitfalls to avoid

**Expected Results:** [What output looks like]
```

**6. Integration with Other Skills**
- Which skills to use before this one
- Which skills to use after
- Which skills provide complementary functionality
- Example workflow chains

Example:
```markdown
## Integration with Other Skills

**Typical Workflow:**
1. mcnp-input-builder → Create basic structure
2. mcnp-geometry-builder → Define complex geometry
3. mcnp-material-builder → Add materials
4. mcnp-source-builder → Configure source
5. mcnp-tally-builder → Set up tallies
6. mcnp-input-validator → Validate before run
7. [Run MCNP]
8. mcnp-output-parser → Analyze results
```

**7. References Section**
- Points to references/ files
- Points to assets/ files
- Points to scripts/ with usage notes
- External documentation references

Example:
```markdown
## References

**Detailed Information:**
- Card specifications: See `references/card_specifications.md`
- Theory background: See `references/theory_background.md`
- Comprehensive examples: See `references/detailed_examples.md`
- Error troubleshooting: See `references/error_catalog.md`

**Templates and Examples:**
- Input templates: See `assets/templates/`
- Validated examples: See `assets/example_inputs/`

**Automation Tools:**
- Python scripts: See `scripts/README.md`

**External Documentation:**
- MCNP6 User Manual: Chapter 5 (Input Cards)
- MCNP6 Primer: Sections 2-4
```

**8. Best Practices (10 Numbered Items)**
- Actionable recommendations
- Based on common pitfalls
- Prioritized by importance

---

## Content Extraction Guidelines

### What to Extract from SKILL.md to references/

**Extract if:**
- ✅ Content >500 words on single topic
- ✅ Comprehensive specifications (all card formats)
- ✅ Theory or mathematical derivations
- ✅ Complete error catalogs with all patterns
- ✅ Collections of >10 detailed examples
- ✅ Step-by-step procedures >1,000 words

**Keep in SKILL.md if:**
- ✅ Workflow overview (<200 words)
- ✅ Quick reference table
- ✅ 3-5 key examples (with links to more in references/)
- ✅ Decision tree diagram
- ✅ Integration points with other skills

### What to Move from SKILL.md to assets/

**Move to assets/ if:**
- ✅ Template files (full input file examples)
- ✅ Example input files from example_files/
- ✅ Boilerplate code/configuration

**Keep in SKILL.md if:**
- ✅ Code snippets demonstrating syntax (5-20 lines)
- ✅ Minimal examples showing specific concept

### What to Bundle in scripts/

**Bundle if:**
- ✅ Python/Bash automation mentioned in SKILL.md
- ✅ Validation or checking tools
- ✅ Repeatedly-used code
- ✅ Complex algorithms better as executable code

---

## Quality Indicators

### Signs of Good Skill Structure

✅ SKILL.md can be read in 5-10 minutes
✅ Decision tree immediately clarifies when to use skill
✅ Quick reference table enables fast lookup
✅ Use cases provide concrete examples
✅ Integration section shows workflow context
✅ References section points to details
✅ No duplication between SKILL.md and references/

### Signs of Poor Skill Structure

❌ SKILL.md takes >15 minutes to read
❌ Unclear when to use this skill vs others
❌ No visual guides (decision trees, tables)
❌ Examples too abstract or incomplete
❌ No mention of related skills
❌ All content inline (no bundled resources)
❌ Same information repeated in multiple places

---

## Application to MCNP Skills

### Current State Assessment

**All 36 MCNP skills share these issues:**
1. No references/ subdirectories
2. No scripts/ subdirectories (Python modules mentioned but not bundled)
3. No assets/ subdirectories
4. YAML frontmatter uses non-standard fields
5. SKILL.md files are borderline too long (1,000-1,200 lines)

**What's working well:**
1. Most have decision trees
2. Integration sections present
3. Good use cases with code
4. Clear "When to Use" sections

### Recommended Extraction Strategy

For typical MCNP skill (1,100 lines):

**Extract to references/ (~500 lines):**
- Card specifications
- Surface type details
- Error catalogs
- 10-15 detailed examples

**Extract to assets/ (~100 lines of examples):**
- 5-10 complete example input files from example_files/
- Template files

**Bundle in scripts/ (if mentioned):**
- Python automation modules
- Validation scripts

**Resulting SKILL.md (~500-600 lines = ~2,500-3,000 words):**
- Overview, decision tree, quick reference
- 3-5 key examples
- Integration, references, best practices

**Target reduction: 50% of SKILL.md content moves to bundled resources**

---

## Examples from Anthropic Skills

### document-skills/docx

**YAML Frontmatter:**
```yaml
---
name: docx
description: "Use for reading, editing, creating, or analyzing Word documents"
---
```

**Structure:**
- SKILL.md: ~2,000 lines (workflows, key examples)
- references/: docx-js.md, ooxml.md (detailed APIs)
- scripts/: document.py, utilities.py
- scripts/templates/: XML templates for comments

**Key Insight:** Separates workflow guidance (SKILL.md) from API details (references/)

### mcp-builder

**YAML Frontmatter:**
```yaml
---
name: mcp-builder
description: "Build high-quality Model Context Protocol servers that enable LLMs to interact with external services"
---
```

**Structure:**
- SKILL.md: ~3,000 words (four-phase workflow)
- references/:
  - mcp_best_practices.md
  - node_mcp_server.md
  - python_mcp_server.md
  - evaluation.md
- scripts/: connections.py, evaluation.py

**Key Insight:** Large reference docs (5,000+ words each) kept separate, SKILL.md stays focused

---

## Conclusion

Anthropic's skill-creator standards emphasize:
1. **Progressive disclosure** - Load only what's needed
2. **Focused SKILL.md** - Workflow guide, not encyclopedia
3. **Rich bundled resources** - Details in references/, examples in assets/, automation in scripts/
4. **Clear triggers** - Description specifies when to invoke
5. **Standard structure** - Consistent YAML, sections, organization

Applying these standards to MCNP skills requires:
- Extracting ~50% of SKILL.md content to references/
- Adding example files from example_files/ to assets/
- Bundling Python modules in scripts/
- Standardizing YAML frontmatter
- Streamlining to <3k words

**Result:** More maintainable, more usable, more efficient skills that follow Anthropic best practices.

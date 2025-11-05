# MCNP Cross-Reference Validation Procedures

**Version:** 2.0.0
**Skill:** mcnp-cross-reference-checker
**Purpose:** Step-by-step procedures for validating cross-references in MCNP inputs

---

## Validation Workflow Overview

```
User Input File
      ↓
Basic Syntax Check (mcnp-input-validator)
      ↓
Cross-Reference Validation (THIS SKILL)
      ├─→ Quick Check Mode (5 min)
      ├─→ Comprehensive Analysis (15 min)
      └─→ Dependency Mapping (30 min)
      ↓
Report Generation
      ↓
User Review & Fixes
      ↓
Re-validate Until Clean
      ↓
Proceed to Geometry Validation
```

---

## Procedure 1: Quick Reference Check

**When to use:** Before every MCNP run, after quick edits
**Time:** ~5 minutes
**Tool:** `cross_reference_validator.py`

### Step 1: Run Quick Validator

```bash
python scripts/cross_reference_validator.py input.inp --mode quick
```

### Step 2: Check for FATAL Errors

```
OUTPUT PRIORITY:
1. FATAL ERRORS (broken references)
   → Must fix before running MCNP
2. WARNINGS (unused entities, count mismatches)
   → Should fix, but MCNP may run
3. INFO (dependency statistics)
   → Informational only
```

### Step 3: Fix FATAL Errors First

**Error order:**
1. Undefined surface references
2. Undefined material references
3. IMP count mismatches (if > cell count)
4. Tally references to undefined cells/surfaces

### Step 4: Re-run Until Clean

```bash
# Fix errors in input.inp
# Re-run validator
python scripts/cross_reference_validator.py input.inp --mode quick

# Repeat until no FATAL errors
```

### Quick Check Validates:
- ✅ All surface references in cells exist
- ✅ All material references exist
- ✅ IMP card count matches cell count
- ✅ Tally cell/surface references valid
- ✅ TR card references exist

### Quick Check Does NOT:
- ❌ Detect unused entities
- ❌ Build full dependency graph
- ❌ Analyze universe hierarchy
- ❌ Check FM card material references

---

## Procedure 2: Comprehensive Cross-Reference Analysis

**When to use:** Before major modifications, complex geometry review
**Time:** ~15 minutes
**Tool:** `mcnp_cross_reference_checker.py`

### Step 1: Build Complete Dependency Graph

```python
from scripts.mcnp_cross_reference_checker import MCNPCrossReferenceChecker

checker = MCNPCrossReferenceChecker()
graph = checker.build_dependency_graph('input.inp')
```

### Step 2: Validate All Reference Types

```python
# Check broken references
broken = checker.find_broken_references('input.inp')

# Check unused entities
unused = checker.detect_unused_entities(graph)

# Check universe hierarchy
circular = checker.detect_circular_universes(graph)

# Check count mismatches
count_errors = checker.validate_parameter_counts('input.inp')
```

### Step 3: Generate Comprehensive Report

```python
report = checker.generate_full_report('input.inp')

# Report structure:
# {
#     'fatal_errors': [...],      # Broken references
#     'warnings': [...],          # Unused entities, count issues
#     'statistics': {...},        # Dependency counts
#     'recommendations': [...]    # Suggested fixes
# }
```

### Step 4: Review by Severity

**Priority 1: FATAL (must fix)**
```
FATAL ERRORS:
✗ Cell 10 references undefined surface 203
✗ Material 5 for cell 15 not defined
✗ IMP:N has 16 entries, 15 cells exist
```

**Priority 2: WARNINGS (should fix)**
```
WARNINGS:
⚠ Surface 99 defined but never used
⚠ Material 4 defined but no cells use it
⚠ IMP:N has 4 entries, 5 cells (assuming 0 for cell 5)
```

**Priority 3: INFO (review)**
```
INFORMATION:
ℹ 15 cells reference 32 surfaces
ℹ 12 non-void cells use 3 materials
ℹ 2 tallies monitor 8 cells total
```

### Step 5: Fix Issues Systematically

**Fix order:**
1. Broken surface/material/transformation references
2. IMP/VOL/AREA count mismatches
3. Tally stale references
4. FM card material references
5. Remove unused entities (if appropriate)

### Comprehensive Analysis Includes:
- ✅ All quick check validations
- ✅ Unused entity detection
- ✅ FM card material validation
- ✅ Full dependency graph
- ✅ Universe hierarchy validation
- ✅ Circular dependency detection
- ✅ Impact analysis capabilities

---

## Procedure 3: Dependency Mapping

**When to use:** Understanding complex lattices, before major restructuring
**Time:** ~30 minutes
**Tool:** `dependency_visualizer.py`

### Step 1: Generate Text Dependency Map

```bash
python scripts/dependency_visualizer.py input.inp --output text
```

**Output:**
```
DEPENDENCY MAP:

Cells → Surfaces:
  Cell 1: [1, 2, 3, 4]
  Cell 2: [1, 5, 6, 7]
  Cell 10: [10, 11, 12]

Cells → Materials:
  Cells 1, 2: Material 1
  Cell 10: Material 2

Tallies → Cells:
  F4: [1, 2, 10]
  F14: [5, 10, 15]
```

### Step 2: Generate Universe Hierarchy

```bash
python scripts/dependency_visualizer.py input.inp --universe-tree
```

**Output:**
```
Universe 0 (base):
  Cells: 1, 2, 3, 10, 20
  ├─ Cell 10 (FILL=5)
  │  │
  │  Universe 5:
  │    Cells: 30, 31, 32
  │    └─ Cell 32 (FILL=10)
  │       │
  │       Universe 10:
  │         Cells: 40, 41, 42
```

### Step 3: Generate Graphviz Diagram

```bash
python scripts/dependency_visualizer.py input.inp --format dot > deps.dot
dot -Tpng deps.dot -o dependencies.png
```

### Step 4: Use for Impact Analysis

**Question:** "What breaks if I delete surface 20?"

```python
impact = checker.analyze_deletion_impact('surface', 20, graph)

# Shows:
# - Which cells will have broken geometry
# - Which tallies need updating
# - Recommended fix actions
```

---

## Procedure 4: Pre-Modification Validation

**When to use:** Before modifying existing inputs
**Purpose:** Understand current state before changes

### Step 1: Baseline Validation

```bash
# Run comprehensive check on ORIGINAL input
python scripts/cross_reference_validator.py original.inp --mode comprehensive > baseline.txt
```

### Step 2: Document Current Dependencies

```bash
# Generate dependency map
python scripts/dependency_visualizer.py original.inp > dependencies.txt
```

### Step 3: Make Modifications

```
Edit input file:
- Add/delete cells
- Modify geometry
- Change materials
- Update tallies
```

### Step 4: Post-Modification Validation

```bash
# Run comprehensive check on MODIFIED input
python scripts/cross_reference_validator.py modified.inp --mode comprehensive > modified.txt

# Compare to baseline
diff baseline.txt modified.txt
```

### Step 5: Fix New Errors

```
Common issues after modification:
- Stale tally references (deleted cells)
- IMP count mismatch (added/deleted cells)
- Broken surface references (geometry changes)
```

---

## Procedure 5: Integration with Validation Pipeline

**Complete validation workflow:**

```
1. Syntax Validation (mcnp-input-validator)
   └─→ Verifies basic structure, card format

2. Cross-Reference Validation (THIS SKILL)
   └─→ Ensures all references valid

3. Geometry Validation (mcnp-geometry-checker)
   └─→ Checks overlaps, gaps, lost particles

4. Physics Validation (mcnp-physics-validator)
   └─→ Verifies physics settings

5. Best Practices Check (mcnp-best-practices-checker)
   └─→ Reviews against 57-item checklist
```

**Integration points:**

```python
# Full validation pipeline
def validate_mcnp_input(filename):
    # Step 1: Syntax
    from mcnp_input_validator import validate_syntax
    syntax_ok = validate_syntax(filename)
    if not syntax_ok:
        return False  # Fix syntax first

    # Step 2: Cross-references (THIS SKILL)
    from mcnp_cross_reference_checker import MCNPCrossReferenceChecker
    checker = MCNPCrossReferenceChecker()
    broken = checker.find_broken_references(filename)
    if broken:
        print("FATAL: Fix cross-references before continuing")
        return False

    # Step 3: Geometry
    from mcnp_geometry_checker import check_geometry
    geom_ok = check_geometry(filename)

    # Step 4: Physics
    from mcnp_physics_validator import validate_physics
    phys_ok = validate_physics(filename)

    return geom_ok and phys_ok
```

---

## Automated Validation Scripts

### Script 1: Pre-Run Validation

```bash
#!/bin/bash
# pre_run_validation.sh

echo "Running pre-run validation..."

# Quick cross-reference check
python scripts/cross_reference_validator.py $1 --mode quick

if [ $? -ne 0 ]; then
    echo "FATAL: Cross-reference errors found"
    echo "Fix errors before running MCNP"
    exit 1
fi

echo "✓ Cross-references validated"
echo "Ready to run MCNP"
```

### Script 2: Modification Checker

```bash
#!/bin/bash
# check_modifications.sh

# Compare original and modified versions
echo "Checking modifications..."

python scripts/cross_reference_validator.py original.inp > orig.txt
python scripts/cross_reference_validator.py modified.inp > mod.txt

diff orig.txt mod.txt > changes.txt

echo "Changes detected:"
cat changes.txt
```

---

## Validation Checklists

### Quick Check Checklist
- [ ] All surface references exist
- [ ] All material references exist
- [ ] IMP count matches cells
- [ ] Tally references valid
- [ ] No FATAL errors reported

### Comprehensive Check Checklist
- [ ] All quick check items
- [ ] No unused surfaces
- [ ] No unused materials
- [ ] FM card materials exist
- [ ] Universe hierarchy valid
- [ ] No circular dependencies
- [ ] All warnings reviewed

### Pre-Modification Checklist
- [ ] Baseline validation completed
- [ ] Dependencies documented
- [ ] Modification plan created
- [ ] Impact analysis performed
- [ ] Backup created

### Post-Modification Checklist
- [ ] New validation completed
- [ ] Comparison to baseline done
- [ ] New errors fixed
- [ ] Dependencies updated
- [ ] Ready for geometry check

---

## Best Practices

1. **Always validate before running MCNP** - Saves compute time
2. **Use quick check for routine work** - Fast feedback
3. **Use comprehensive for complex inputs** - Thorough analysis
4. **Document dependencies for lattices** - Future reference
5. **Validate after every modification** - Catch errors early
6. **Keep validation reports** - Track changes over time
7. **Automate validation in workflows** - Consistent checking
8. **Fix FATAL errors first** - Most critical
9. **Review warnings carefully** - May indicate issues
10. **Use dependency graphs for communication** - Explain to others

---

**END OF VALIDATION_PROCEDURES.MD**

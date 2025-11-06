# MCNP Best Practices Checker - Scripts

**Purpose:** Automated checking tools for MCNP best practices compliance.

---

## Overview

These scripts help systematically review MCNP inputs against the 57-item best practices checklist from Chapter 3.4. While full review requires expert judgment, scripts can automate many checks.

---

## Planned Scripts

### 1. best_practices_checker.py (Future)

**Purpose:** Automated checklist compliance scanner

**Planned Features:**
- Parse MCNP input file
- Check for common violations
- Generate checklist report
- Prioritize critical items

**Usage (Planned):**
```python
from best_practices_checker import BestPracticesChecker

checker = BestPracticesChecker()
report = checker.check_input('input.inp')

print(f"Phase 1 (Setup): {report.phase1_complete}/22 items")
print(f"Critical missing: {report.critical_issues}")
```

**Automated Checks:**
- File structure validation
- PRINT card presence
- Material normalization
- Cross-section consistency
- Importance coverage

### 2. geometry_plotter.py (Future)

**Purpose:** Automated multi-view geometry plotting

**Planned Features:**
- Generate plots from 3 orthogonal views
- Highlight dashed lines (potential errors)
- Save plots for documentation

**Usage (Planned):**
```python
from geometry_plotter import GeometryPlotter

plotter = GeometryPlotter('input.inp')
plotter.plot_all_views(output_dir='plots/')
# Generates: xy_view.png, xz_view.png, yz_view.png
```

### 3. void_test_generator.py (Future)

**Purpose:** Generate VOID card test input automatically

**Planned Features:**
- Read original input
- Add VOID card and flood geometry
- Set appropriate flood boundaries
- Generate test input file

**Usage (Planned):**
```python
from void_test_generator import VoidTestGenerator

generator = VoidTestGenerator()
generator.create_void_test('original.inp', 'void_test.inp')
```

---

## Manual Review Workflow

Since many practices require expert judgment, use this workflow:

### Step 1: Automated Pre-Check

```bash
# Run automated checks (future)
python best_practices_checker.py input.inp

# Output:
# ✓ Phase 1 Item 20: PRINT card present
# ✗ Phase 1 Item 2: No evidence of geometry plotting
# ✗ Phase 1 Item 10: VOID test not documented
# ⚠ Phase 1 Item 9: Volumes not pre-calculated
```

### Step 2: Manual Review

Use checklist_reference.md to review items requiring judgment:
- Geometry complexity (Item 1.3, 1.4)
- Physics appropriateness (Item 1.13)
- VR strategy (Items 1.16, 1.17)
- Statistical interpretation (Phase 2 & 3 items)

### Step 3: Generate Report

Document review findings:
```markdown
# Best Practices Review: Reactor Core Model

## Phase 1: Setup (Before First Run)

**Critical Missing:**
- [ ] Item 2: Geometry not plotted
- [ ] Item 10: VOID test not performed

**Completed:**
- [x] Item 1: Geometry drawn (see doc/geometry_sketch.pdf)
- [x] Item 14: Consistent cross sections (all .80c)
- [x] Item 20: PRINT card included

**Recommendations:**
1. IMMEDIATELY plot geometry from 3 views
2. Run VOID test with 1M particles
3. Pre-calculate core volume for comparison

## Phase 2: Preproduction (After Test Run)

**Status:** Not yet reached

## Next Steps:
1. Complete Phase 1 critical items (plotting, VOID test)
2. Run 100k particle test
3. Proceed to Phase 2 review
```

---

## Integration Examples

### Example 1: Pre-Production Checklist

```python
# Manual checklist workflow

phases = {
    'Phase 1 (Setup)': [
        '✓ Geometry drawn',
        '✓ Geometry plotted (3 views)',
        '✓ VOID test passed',
        '✓ Volumes pre-calculated',
        '✗ Source checked with mesh tally',  # TODO
    ],
    'Phase 2 (Testing)': [
        'Not started'
    ]
}

# Print report
for phase, items in phases.items():
    print(f"\n{phase}:")
    for item in items:
        print(f"  {item}")
```

### Example 2: Automated File Checks

```python
# Check for basic compliance

def check_print_card(input_file):
    """Check if PRINT card present"""
    with open(input_file, 'r') as f:
        for line in f:
            if line.strip().upper().startswith('PRINT'):
                return True
    return False

def check_material_normalization(input_file):
    """Check if materials sum to 1.0"""
    # Parse M cards
    # Sum fractions
    # Return violations
    pass

# Usage
if check_print_card('input.inp'):
    print("✓ PRINT card present")
else:
    print("✗ PRINT card missing (Item 1.20)")
```

---

## Development Notes

### Priorities for Automation

**High Priority** (Easy to automate):
- File structure checks
- Card presence verification
- Material normalization
- Cross-section consistency
- Statistical check parsing

**Medium Priority** (Partial automation):
- Geometry plotting automation
- VOID test generation
- Volume calculation comparison
- Table extraction from output

**Low Priority** (Requires judgment):
- Geometry complexity assessment
- Physics appropriateness
- VR strategy evaluation
- Results reasonableness

### Testing

Test scripts with known good/bad inputs:
```python
# Test cases
test_cases = {
    'good_input.inp': {'print_card': True, 'materials_normalized': True},
    'missing_print.inp': {'print_card': False, 'materials_normalized': True},
    'bad_materials.inp': {'print_card': True, 'materials_normalized': False},
}

for input_file, expected in test_cases.items():
    result = check_input(input_file)
    assert result == expected
```

---

## Future Enhancements

1. **Interactive CLI:** Step-by-step checklist review
2. **PDF Reports:** Professional documentation output
3. **Integration:** Connect with MCNP workflow tools
4. **Learning System:** Track common violations, suggest improvements
5. **Templates:** Generate compliant input templates

---

## References

- **checklist_reference.md:** Complete 57-item checklist details
- **MCNP Manual Chapter 3.4:** Best practices documentation

---

**END OF SCRIPTS README**

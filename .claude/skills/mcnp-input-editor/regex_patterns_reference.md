# MCNP Input Editor - Regex Patterns Reference

This document provides common regular expression patterns for safe and effective MCNP input file editing.

---

## Pattern Basics

### Regex Fundamentals for MCNP Editing

**Anchors:**
- `^` - Start of line
- `$` - End of line
- `\b` - Word boundary

**Character Classes:**
- `\d` - Any digit (0-9)
- `\s` - Any whitespace (space, tab, newline)
- `\w` - Any word character (alphanumeric + underscore)
- `.` - Any character (except newline)

**Quantifiers:**
- `+` - One or more
- `*` - Zero or more
- `?` - Zero or one
- `{n}` - Exactly n times
- `{n,m}` - Between n and m times

**Groups:**
- `(pattern)` - Capture group
- `(?:pattern)` - Non-capturing group
- `(?=pattern)` - Positive lookahead
- `(?!pattern)` - Negative lookahead

---

## Cell Card Patterns

### Match Specific Cell Number

**Pattern:** `^123\s+`
```
Matches: Cell 123 at start of line
Does NOT match: Cell 1230, 1234, etc.
Usage: Find cell 123 specifically
```

**Example:**
```
Find: ^100\s+
Matches:
  100  1  -1.0  -1  IMP:N=1  ✓
Does not match:
  1000  2  -2.0  1  -2  IMP:N=1  ✗
```

### Match Cell Number Range

**Pattern:** `^(10[0-9])\s+`
```
Matches: Cells 100-109
Usage: Edit cells in specific range
```

**Example:**
```
Find: ^(40\d)\s+
Matches:
  400  1  -1.0  ...  ✓
  401  2  -2.0  ...  ✓
  409  3  -3.0  ...  ✓
Does not match:
  410  4  -4.0  ...  ✗
  4000  5  -5.0  ...  ✗
```

### Match Cell Density Field

**Pattern:** `^(\d+\s+\d+\s+)(-?[\d.eE+-]+)`
```
Group 1: Cell number + material number
Group 2: Density value
Usage: Change density while preserving cell/material
```

**Example:**
```
Find: ^(100\s+1\s+)(-1\.0)
Replace: $1-1.2
Result: 100  1  -1.2  (density changed)
```

### Match All Non-Void Cells

**Pattern:** `^(\d+)\s+([1-9]\d*)\s+`
```
Group 1: Cell number
Group 2: Material number (1 or greater)
Does NOT match: Void cells (m=0)
```

**Example:**
```
Find: ^(\d+)\s+([1-9]\d*)\s+(-?[\d.eE+-]+)
Matches:
  100  1  -1.0  ...  ✓ (material 1)
  200  5  -2.3  ...  ✓ (material 5)
Does not match:
  300  0  ...  ✗ (void cell)
```

---

## Surface Card Patterns

### Match Specific Surface Type

**Pattern:** `^\d+\s+(SO|SZ|S)\s+`
```
Matches: Sphere surfaces (SO, SZ, S)
Usage: Find all sphere surfaces
```

**Example:**
```
Find: ^\d+\s+SO\s+
Matches:
  1  SO  10.0  ✓
  5  SO  20.5  ✓
Does not match:
  2  CZ  5.0  ✗ (cylinder)
```

### Match Surface with Parameters

**Pattern:** `^(\d+\s+CZ\s+)([\d.]+)`
```
Group 1: Surface number + type
Group 2: Radius parameter
Usage: Scale cylinder radii
```

**Example:**
```
Find: ^(\d+\s+CZ\s+)([\d.]+)
Replace: $1$(echo "$2 * 1.1" | bc)
(Scale CZ radius by 1.1)
```

---

## Material Card Patterns

### Match ZAID Library Identifier

**Pattern:** `\.\d{2,3}c`
```
Matches: .70c, .80c, .31c, etc.
Usage: Change cross-section library
```

**Example:**
```
Find: \.70c
Replace: .80c
Result: All .70c → .80c
```

### Match Specific Isotope

**Pattern:** `92235\.\d+c`
```
Matches: U-235 with any library (.70c, .80c, etc.)
Usage: Change library for specific isotope
```

**Example:**
```
Find: 9223[58]\.\d+c
Matches:
  92235.70c  ✓ (U-235)
  92238.80c  ✓ (U-238)
Does not match:
  92234.70c  ✗ (U-234)
```

### Match Material Fraction

**Pattern:** `([\d]{4,5}\.\d+c)\s+([\d.eE+-]+)`
```
Group 1: ZAID
Group 2: Fraction
Usage: Modify isotopic fractions
```

**Example:**
```
Find: (92235\.80c)\s+(0\.03)
Replace: $1  0.032
(Change U-235 enrichment from 3% to 3.2%)
```

---

## Parameter Patterns

### Match Importance Parameter

**Pattern:** `IMP:N=(\d+)`
```
Captures: Neutron importance value
Usage: Change importances systematically
```

**Example:**
```
Find: IMP:N=[1-9]\d*
Replace: IMP:N=1
(Set all non-zero importances to 1)
```

### Match Importance (Excluding Zero)

**Pattern:** `IMP:N=(?!0\b)\d+`
```
Matches: IMP:N=1, IMP:N=2, IMP:N=10, etc.
Does NOT match: IMP:N=0 (graveyard)
Usage: Change importances while preserving graveyard
```

**Example:**
```
Find: IMP:N=(?!0\b)\d+
Replace: IMP:N=1
Result:
  IMP:N=2 → IMP:N=1  ✓
  IMP:N=4 → IMP:N=1  ✓
  IMP:N=0 → IMP:N=0  ✓ (unchanged)
```

### Match VOL Parameter

**Pattern:** `VOL=([\d.eE+-]+)`
```
Captures: Volume value
Usage: Scale volumes, update values
```

**Example:**
```
Find: VOL=([\d.eE+-]+)
Replace: VOL=$(echo "$1 * 2.0" | bc)
(Double all volumes)
```

---

## Comment-Aware Patterns

### Match Field But Exclude Comments

**Pattern:** `^([^$]*?)(pattern)(.*?)(\$.*)?$`
```
Group 1: Before pattern
Group 2: Pattern to match
Group 3: After pattern (before comment)
Group 4: Comment (including $)
Usage: Modify main content, preserve comments
```

**Example:**
```
Find: ^([^$]*?)(-1\.0)(.*?)(\$.*)?$
Replace: $1-1.2$3$4
Result:
  100  1  -1.0  -1  $ Water  →  100  1  -1.2  -1  $ Water
  (Density changed, comment preserved)
```

### Extract Comment

**Pattern:** `\$(.+)$`
```
Captures: Everything after $ to end of line
Usage: Extract, modify, or remove comments
```

**Example:**
```
Find: ^(.*?)\s*\$.*$
Replace: $1
(Remove all inline comments)
```

---

## Block-Specific Patterns

### Identify Cell Block Lines

**Pattern:** `^(\d+)\s+(-?\d+)\s+(-?[\d.eE+-]+)\s+`
```
Matches: Cell card format (j m d ...)
Usage: Identify lines in cell block
```

### Identify Surface Block Lines

**Pattern:** `^(\d+)\s+([A-Z]{1,3})\s+`
```
Matches: Surface card format (j type ...)
Note: Type is 1-3 uppercase letters
```

### Identify Data Block Lines

**Pattern:** `^([A-Z]\w*)`
```
Matches: Lines starting with letters (data cards)
Examples: MODE, M1, SDEF, F4:N, etc.
```

---

## Safe Editing Patterns

### Pattern Template for Safe Replacement

```python
import re

def safe_cell_density_edit(line, old_density, new_density):
    """Safely edit cell density, preserve comments"""
    # Match cell card format
    pattern = r'^(\d+\s+\d+\s+)(' + re.escape(str(old_density)) + r')(\s+.*?)(\$.*)?$'
    replacement = r'\g<1>' + str(new_density) + r'\g<3>\g<4>'

    # Apply replacement
    new_line = re.sub(pattern, replacement, line)

    return new_line
```

### Preview Matches Before Replacing

```python
import re

def preview_regex_matches(filename, pattern):
    """Show all matches before applying replacement"""
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            matches = re.findall(pattern, line)
            if matches:
                print(f"Line {line_num}: {matches}")
                print(f"  {line.rstrip()}")

# Usage
preview_regex_matches('input.i', r'IMP:N=\d+')
```

---

## Complex Patterns

### Multi-Card Material Definition

**Pattern:** `^(M\d+\s+.*?)\n((?:MT\d+.*?\n)?)`
```
Captures: M card and optional MT card
Usage: Edit material + thermal treatment together
Flags: MULTILINE, DOTALL
```

### Continuation Line Matching

**Pattern:** `^(.+?)&\s*\n\s+(.+?)$`
```
Captures: First line (with &) and continuation
Usage: Edit multi-line cards as unit
Flags: MULTILINE
```

**Example:**
```
Find: ^(F4:N.+?)&\s*\n\s+(.+?)$
Matches:
  F4:N  1 2 3 4 5 &
        6 7 8 9 10
```

---

## Validation Patterns

### Check for Common Errors

**Duplicate cell numbers:**
```python
cells_seen = set()
pattern = r'^(\d+)\s+'

for line in lines:
    match = re.match(pattern, line)
    if match:
        cell_num = match.group(1)
        if cell_num in cells_seen:
            print(f"Duplicate cell: {cell_num}")
        cells_seen.add(cell_num)
```

**Missing IMP:N parameter:**
```python
pattern = r'^(\d+\s+\d+\s+-?[\d.eE+-]+\s+.*)$'
no_imp_pattern = r'IMP:N'

for line in lines:
    if re.match(pattern, line) and not re.search(no_imp_pattern, line):
        print(f"Missing IMP:N: {line}")
```

---

## Testing Your Patterns

### Test Pattern Interactively

```python
import re

def test_pattern(pattern, test_strings):
    """Test regex pattern against sample strings"""
    print(f"Pattern: {pattern}\n")

    for test in test_strings:
        match = re.search(pattern, test)
        if match:
            print(f"✓ MATCH: {test}")
            print(f"  Groups: {match.groups()}")
        else:
            print(f"✗ NO MATCH: {test}")
        print()

# Example usage
test_pattern(
    r'^(\d+)\s+(\d+)\s+(-?[\d.eE+-]+)',
    [
        "100  1  -1.0  -1  IMP:N=1",
        "200  0  1  -2  IMP:N=0",
        "invalid line"
    ]
)
```

---

## Best Practices

### 1. Always Use Raw Strings
```python
# Good
pattern = r'\d+\.\d+c'

# Bad (need to escape backslashes)
pattern = '\\d+\\.\\d+c'
```

### 2. Anchor Your Patterns
```python
# Good - matches exact cell 100
pattern = r'^100\s+'

# Bad - also matches cells 1000, 1001, etc.
pattern = r'100\s+'
```

### 3. Use Non-Greedy Matching
```python
# Good - stops at first $
pattern = r'^(.*?)\$'

# Bad - goes to last $ on line
pattern = r'^(.*)\$'
```

### 4. Escape Special Characters
```python
# Good
pattern = r'\d+\.\d+c'  # Matches: 1001.70c

# Bad
pattern = r'\d+.\d+c'   # Matches: 1001X70c (. matches any char)
```

### 5. Test on Sample First
```python
# Always test on small sample before full file
sample = """
100  1  -1.0  -1  IMP:N=1
200  2  -2.3  1  -2  IMP:N=2
"""

# Test pattern here
# Then apply to full file
```

---

## Pattern Library

Quick reference of tested patterns:

| Purpose | Pattern | Notes |
|---------|---------|-------|
| Cell number exact | `^123\s+` | Cell 123 only |
| Cell number range | `^(1[0-9]{2})\s+` | Cells 100-199 |
| Cell density | `^(\d+\s+\d+\s+)(-?[\d.eE+-]+)` | Group 2 is density |
| ZAID library | `\.(\d{2,3})c` | Group 1 is library number |
| Importance (non-zero) | `IMP:N=(?!0\b)\d+` | Excludes IMP:N=0 |
| Volume parameter | `VOL=([\d.eE+-]+)` | Group 1 is volume |
| Comment extraction | `\$(.+)$` | Group 1 is comment text |
| Sphere surfaces | `^\d+\s+(SO|SZ|S)\s+` | All sphere types |
| Material card | `^M(\d+)\s+` | Group 1 is material number |

---

**END OF REGEX PATTERNS REFERENCE**

For editing examples, see detailed_examples.md.
For error handling, see error_catalog.md.
For main editing workflow, see SKILL.md.

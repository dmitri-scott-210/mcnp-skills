# MCNP Cross-Reference Validation Guide
## Ensuring All Referenced Entities Exist

**Purpose**: Comprehensive guide to validating cross-references in MCNP input files to prevent fatal errors and ensure all referenced entities are properly defined.

---

## OVERVIEW

**Cross-reference errors** are among the most common MCNP input errors:
- Cell references undefined surface → FATAL ERROR
- Cell references undefined material → BAD TROUBLE
- Cell fill references undefined universe → FATAL ERROR
- Circular universe references → FATAL ERROR

**This guide provides**:
1. Complete validation rules
2. Systematic checking procedures
3. Common error patterns
4. Automated validation approaches

---

## RULE 1: ALL SURFACES MUST BE DEFINED

### What to Check

Every surface number referenced in cell geometry MUST have a corresponding surface card.

### Examples

**CORRECT**:
```mcnp
c Cell references surfaces 100, 101, 102
1  1  -10.2  -100  101 -102  imp:n=1

c Surface definitions (all present)
100  so   5.0   $ Surface 100 defined
101  pz   0.0   $ Surface 101 defined
102  pz  10.0   $ Surface 102 defined
```

**ERROR - Missing surface**:
```mcnp
c Cell references surface 103 (NOT DEFINED)
1  1  -10.2  -100  101 -102  103  imp:n=1
                              ^^^
                              Surface 103 missing!

c Surface definitions
100  so   5.0
101  pz   0.0
102  pz  10.0
c ← Surface 103 not defined! FATAL ERROR
```

**MCNP error message**:
```
bad trouble in subroutine cell of icl
surface     103 not defined or outside range
```

### Validation Procedure

**Manual check**:
1. Extract all surface numbers from cell cards
2. List all defined surface numbers
3. Compare: every referenced surface must be in defined list

**Automated check** (Python):
```python
def extract_surfaces_from_cell(cell_line):
    """Extract surface numbers from cell geometry"""
    # Parse cell card: j m d geom params
    parts = cell_line.split()
    # Skip cell number, material, density
    # Remaining tokens are geometry (surfaces) and parameters
    surfaces = []
    for token in parts[3:]:  # After cell#, mat#, density
        if token.startswith('IMP') or token.startswith('VOL'):
            break  # Reached parameters
        # Remove sense (+/-)
        surf_num = token.lstrip('+-')
        if surf_num.isdigit():
            surfaces.append(int(surf_num))
    return surfaces

def validate_surfaces(cells, surfaces):
    """Check all referenced surfaces are defined"""
    referenced = set()
    for cell_line in cells:
        referenced.update(extract_surfaces_from_cell(cell_line))

    defined = set(surfaces.keys())

    missing = referenced - defined
    if missing:
        print(f"ERROR: Undefined surfaces: {sorted(missing)}")
        return False
    return True
```

---

## RULE 2: ALL MATERIALS MUST BE DEFINED

### What to Check

Every material number referenced in cell cards MUST have a corresponding material card (Mn).

**Special case**: Material 0 (void) never needs definition.

### Examples

**CORRECT**:
```mcnp
c Cells reference materials 0, 1, 2
1  1  -10.2  -100  imp:n=1  $ Material 1
2  2  -8.0   -200  imp:n=1  $ Material 2
3  0        -300  imp:n=1  $ Material 0 (void, no definition needed)

c Material definitions
m1  92235.70c  0.045   $ Material 1 defined
    92238.70c  0.955
     8016.70c  2.0
m2  26000.70c  1.0     $ Material 2 defined
```

**ERROR - Missing material**:
```mcnp
c Cell references material 3 (NOT DEFINED)
1  1  -10.2  -100  imp:n=1  $ Material 1
2  2  -8.0   -200  imp:n=1  $ Material 2
3  3  -6.5   -300  imp:n=1  $ Material 3 ← NOT DEFINED!
            ^

c Material definitions
m1  [...]  $ Material 1 defined
m2  [...]  $ Material 2 defined
c ← Material 3 not defined! BAD TROUBLE
```

**MCNP error message**:
```
warning. material     3 is not defined but is used in cell     3
```

### Validation Procedure

**Manual check**:
1. Extract all non-zero material numbers from cell cards
2. List all defined material numbers (M cards)
3. Compare: every referenced material (except 0) must be defined

**Automated check** (Python):
```python
def extract_material_from_cell(cell_line):
    """Extract material number from cell card"""
    parts = cell_line.split()
    if len(parts) >= 2:
        mat_num = int(parts[1])  # Second field is material number
        return mat_num
    return None

def validate_materials(cells, materials):
    """Check all referenced materials are defined"""
    referenced = set()
    for cell_line in cells:
        mat = extract_material_from_cell(cell_line)
        if mat is not None and mat != 0:  # Exclude void (0)
            referenced.add(mat)

    defined = set(materials.keys())

    missing = referenced - defined
    if missing:
        print(f"ERROR: Undefined materials: {sorted(missing)}")
        return False
    return True
```

---

## RULE 3: ALL UNIVERSES MUST BE DEFINED

### What to Check

Every universe number referenced in FILL cards MUST have cells defined in that universe (U=n).

**Special case**: Universe 0 is the global universe (never explicitly defined).

### Examples

**CORRECT**:
```mcnp
c Global cell fills with universe 100
1  0  -1  fill=100  imp:n=1  $ References universe 100
                    ^^^

c Universe 100 definition (cells with u=100)
10  1  -10.2  -10  u=100  imp:n=1  $ Cell in universe 100
20  2  -8.0   -20  u=100  imp:n=1  $ Another cell in u=100
```

**ERROR - Undefined universe**:
```mcnp
c Global cell fills with universe 200 (NOT DEFINED)
1  0  -1  fill=200  imp:n=1  $ References universe 200
                    ^^^
                    Universe 200 not defined!

c Universe definitions
10  1  -10.2  -10  u=100  imp:n=1  $ Only universe 100 defined
c ← Universe 200 not defined! FATAL ERROR
```

**MCNP error message**:
```
bad trouble in subroutine rpblk of mcrun
fill universe     200 not used by any cell
```

### Validation Procedure

**Manual check**:
1. Extract all universe numbers from FILL cards
2. List all defined universe numbers (U= parameters)
3. Compare: every referenced universe (except 0) must be defined

**Automated check** (Python):
```python
def extract_fill_from_cell(cell_line):
    """Extract FILL universe number from cell card"""
    if 'FILL=' in cell_line.upper():
        # Extract number after FILL=
        parts = cell_line.upper().split('FILL=')[1].split()
        fill_num = int(parts[0])
        return fill_num
    return None

def extract_universe_from_cell(cell_line):
    """Extract U= universe number from cell card"""
    if 'U=' in cell_line.upper():
        # Extract number after U=
        parts = cell_line.upper().split('U=')[1].split()
        u_num = int(parts[0])
        return u_num
    return None

def validate_universes(cells):
    """Check all FILL references are defined"""
    referenced = set()
    defined = set([0])  # Universe 0 always exists (global)

    for cell_line in cells:
        fill = extract_fill_from_cell(cell_line)
        if fill is not None:
            referenced.add(fill)

        u = extract_universe_from_cell(cell_line)
        if u is not None:
            defined.add(u)

    missing = referenced - defined
    if missing:
        print(f"ERROR: Undefined universes: {sorted(missing)}")
        return False
    return True
```

---

## RULE 4: UNIVERSE HIERARCHY MUST BE VALID

### What to Check

1. **Child before parent**: Universe must be defined BEFORE it is referenced in a FILL
2. **No circular references**: Universe A cannot fill universe B if B fills A
3. **Lattice consistency**: LAT=1 cells must use FILL array, not single universe

### Examples

**CORRECT hierarchy**:
```mcnp
c Step 1: Define innermost universe (u=10)
100  1  -10.2  -100  u=10  imp:n=1  $ Fuel pin (u=10)

c Step 2: Define middle universe (u=20) that fills with u=10
200  0  -200  u=20  lat=1  fill=-5:5 0:0 0:0  $ Lattice fills with u=10
     10 10 10 10 10 10 10 10 10 10 10

c Step 3: Global cell fills with u=20
1  0  -1  fill=20  imp:n=1  $ Global fills with lattice
```

**ERROR - Parent before child**:
```mcnp
c ERROR: Trying to fill with u=10 before it's defined
1  0  -1  fill=20  imp:n=1  $ Global fills with u=20
200  0  -200  u=20  fill=10  imp:n=1  $ u=20 fills with u=10 ← NOT DEFINED YET!
100  1  -10.2  -100  u=10  imp:n=1  $ u=10 defined AFTER being referenced
```

**ERROR - Circular reference**:
```mcnp
c ERROR: u=10 fills with u=20, u=20 fills with u=10 (circular!)
100  0  -100  u=10  fill=20  imp:n=1  $ u=10 fills with u=20
200  0  -200  u=20  fill=10  imp:n=1  $ u=20 fills with u=10 ← CIRCULAR!
```

**MCNP error message**:
```
bad trouble in subroutine rpblk of mcrun
fill universe circular reference detected
universe  10 fills with universe  20
universe  20 fills with universe  10
```

### Validation Procedure

**Manual check**:
1. List all universe definitions in order of appearance
2. For each FILL, verify referenced universe was defined earlier
3. Build dependency graph, check for cycles

**Automated check** (Python):
```python
def validate_universe_hierarchy(cells):
    """Check universe hierarchy for circular references"""
    defined_universes = set([0])  # Global universe
    fill_dependencies = {}  # {universe: [fills_with_universe_list]}

    for cell_line in cells:
        u = extract_universe_from_cell(cell_line)
        if u is not None:
            defined_universes.add(u)
            fill = extract_fill_from_cell(cell_line)
            if fill is not None:
                if u not in fill_dependencies:
                    fill_dependencies[u] = []
                fill_dependencies[u].append(fill)

    # Check for circular dependencies
    def has_circular_ref(universe, visited=None):
        if visited is None:
            visited = set()
        if universe in visited:
            return True  # Circular!
        visited.add(universe)
        if universe in fill_dependencies:
            for child in fill_dependencies[universe]:
                if has_circular_ref(child, visited.copy()):
                    return True
        return False

    for u in defined_universes:
        if has_circular_ref(u):
            print(f"ERROR: Circular universe reference involving u={u}")
            return False

    return True
```

---

## RULE 5: DENSITY-MATERIAL CORRELATION

### What to Check

1. **Positive density** → Material fractions must be atom fractions
2. **Negative density** → Material fractions must be mass fractions
3. **Void cells** (material 0) can have any density (ignored by MCNP)

### Examples

**CORRECT - Atom fractions with positive density**:
```mcnp
m1
    1001.70c  0.0667  $ Atom fractions (sum to 1.0 or normalize)
    8016.70c  0.0333

1  1  0.1000  -1  imp:n=1  $ Positive density = atoms/barn-cm
    ^^^^^^^^
    Positive → Atom fractions in m1
```

**CORRECT - Mass fractions with negative density**:
```mcnp
m2
   26056.70c  -0.604  $ Mass fractions (sum to 1.0)
   24052.70c  -0.143
   28058.70c  -0.253

2  2  -8.03  -2  imp:n=1  $ Negative density = g/cm³
    ^^^^^^^
    Negative → Mass fractions in m2
```

**ERROR - Mismatched signs**:
```mcnp
m1
    1001.70c  0.0667  $ Atom fractions
    8016.70c  0.0333

1  1  -1.0  -1  imp:n=1  $ ERROR: Negative density with atom fractions!
    ^^^^^^
    Should be positive!
```

**MCNP warning/error**:
```
warning. cell     1 density is negative but material fractions are positive
```

### Validation Procedure

**Check**:
1. Extract density from cell card (field 3)
2. Extract material number (field 2)
3. Check material definition for fraction signs
4. Verify consistency:
   - Positive cell density → positive material fractions
   - Negative cell density → negative material fractions

---

## RULE 6: IMPORTANCE SPECIFICATIONS

### What to Check

1. **All cells must have importance** (IMP card or in cell definition)
2. **At least one cell must have IMP=0** (particle kill boundary)
3. **IMP=0 cells cannot contain material** (must be void)
4. **Particle types must match MODE card**

### Examples

**CORRECT**:
```mcnp
c All cells have importance, one has IMP:N=0
1  1  -10.2  -1       imp:n=1  $ Normal region
2  2  -8.0    1  -2   imp:n=1  $ Normal region
3  0         2        imp:n=0  $ Graveyard (void, IMP=0)
             ^                                   ^^^^^^
             Material 0 (void)                   Kill boundary

c Data cards
MODE N
```

**ERROR - No kill boundary**:
```mcnp
c ERROR: All cells have IMP:N=1, no kill boundary!
1  1  -10.2  -1       imp:n=1
2  2  -8.0    1  -2   imp:n=1
3  0         2        imp:n=1  $ Should be IMP:N=0!
```

**MCNP warning**:
```
warning. there are no imp:n=0 cells in this problem
particles may leak from the geometry
```

**ERROR - Material in IMP=0 cell**:
```mcnp
c ERROR: Cell with IMP=0 contains material (should be void)
3  2  -8.0   2   imp:n=0  $ ERROR: Material 2 in kill boundary!
   ^                           Should be material 0 (void)
```

### Validation Procedure

**Check**:
1. Verify all cells have importance specified
2. Verify at least one IMP=0 cell exists per particle type
3. Verify IMP=0 cells use material 0 (void)
4. Verify particle types match MODE card

---

## COMPLETE VALIDATION CHECKLIST

### Pre-Run Validation

**Surfaces**:
- [ ] All surfaces referenced in cells are defined
- [ ] No duplicate surface numbers
- [ ] Surface parameters are physically reasonable

**Materials**:
- [ ] All non-zero materials referenced in cells are defined
- [ ] No duplicate material numbers
- [ ] Density signs match fraction signs (positive ↔ positive, negative ↔ negative)
- [ ] Thermal scattering (MT) cards reference defined materials

**Universes**:
- [ ] All FILL universes are defined (except u=0)
- [ ] No circular universe references
- [ ] Child universes defined before parent fills
- [ ] Lattice cells (LAT=1) use FILL arrays correctly

**Importance**:
- [ ] All cells have importance for all particle types in MODE
- [ ] At least one IMP=0 cell per particle type
- [ ] IMP=0 cells use material 0 (void)

**Data Cards**:
- [ ] MODE card exists and is first data card
- [ ] Tally cell/surface numbers exist
- [ ] Source cell/surface numbers exist
- [ ] Transformation (TR) numbers referenced are defined

---

## AUTOMATED VALIDATION SCRIPT

### Python Script Outline

```python
#!/usr/bin/env python3
"""
MCNP Input File Cross-Reference Validator

Checks:
- Surface references
- Material references
- Universe references
- Universe hierarchy
- Density-material correlation
- Importance specifications
"""

import re
from typing import Dict, Set, List

class MCNPValidator:
    def __init__(self, input_file):
        self.cells = []
        self.surfaces = {}
        self.materials = {}
        self.universes = {}
        self.parse_input(input_file)

    def parse_input(self, filename):
        """Parse MCNP input file into sections"""
        with open(filename, 'r') as f:
            lines = f.readlines()

        # Identify blocks (simplified)
        # In reality, need to handle continuations, comments, etc.
        in_cells = True
        in_surfaces = False
        in_data = False

        for line in lines:
            if line.strip() == '':
                if in_cells:
                    in_cells = False
                    in_surfaces = True
                elif in_surfaces:
                    in_surfaces = False
                    in_data = True
                continue

            if line.startswith('c') or line.startswith('C'):
                continue  # Comment

            if in_cells:
                self.cells.append(line)
            elif in_surfaces:
                parts = line.split()
                if parts:
                    surf_num = int(parts[0])
                    self.surfaces[surf_num] = line
            elif in_data:
                if line.strip().upper().startswith('M'):
                    # Material card
                    mat_num = int(re.match(r'[Mm](\d+)', line).group(1))
                    self.materials[mat_num] = line

    def validate_surfaces(self):
        """Check all referenced surfaces are defined"""
        print("\n=== Validating Surface References ===")
        referenced = set()
        for cell_line in self.cells:
            # Extract surface numbers (simplified)
            # Real parser needs to handle geometry properly
            numbers = re.findall(r'[-+]?(\d+)', cell_line)
            referenced.update(int(n) for n in numbers[3:])  # Skip cell, mat, dens

        defined = set(self.surfaces.keys())
        missing = referenced - defined

        if missing:
            print(f"ERROR: Undefined surfaces: {sorted(missing)}")
            return False
        else:
            print("✓ All surface references valid")
            return True

    def validate_materials(self):
        """Check all referenced materials are defined"""
        print("\n=== Validating Material References ===")
        referenced = set()
        for cell_line in self.cells:
            parts = cell_line.split()
            if len(parts) >= 2:
                mat = int(parts[1])
                if mat != 0:  # Exclude void
                    referenced.add(mat)

        defined = set(self.materials.keys())
        missing = referenced - defined

        if missing:
            print(f"ERROR: Undefined materials: {sorted(missing)}")
            return False
        else:
            print("✓ All material references valid")
            return True

    def validate_all(self):
        """Run all validation checks"""
        print("=" * 50)
        print("MCNP INPUT FILE VALIDATION")
        print("=" * 50)

        results = []
        results.append(self.validate_surfaces())
        results.append(self.validate_materials())
        # Add more checks...

        print("\n" + "=" * 50)
        if all(results):
            print("✓ ALL VALIDATION CHECKS PASSED")
        else:
            print("✗ VALIDATION FAILED - Fix errors before running MCNP")
        print("=" * 50)

        return all(results)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python validate_mcnp.py input_file.i")
        sys.exit(1)

    validator = MCNPValidator(sys.argv[1])
    success = validator.validate_all()
    sys.exit(0 if success else 1)
```

---

## COMMON ERROR PATTERNS

### Pattern 1: Typo in Surface Number

```mcnp
c Cell references surface 1001, but defined 1010 (typo)
1  1  -10.2  -1001  imp:n=1  $ Should be -1010

1010  so  5.0  $ Surface 1010 defined (not 1001)
```

### Pattern 2: Copy-Paste Error

```mcnp
c Copied cell but forgot to update surface reference
10  1  -10.2  -100  u=10  imp:n=1  $ Pin 1
20  1  -10.2  -100  u=20  imp:n=1  $ Pin 2 ← Should reference surface 200!
                ^^^
```

### Pattern 3: Incomplete Universe Fill

```mcnp
c Lattice fills with universe 100, but 100 not defined
1  0  -1  u=10  lat=1  fill=-5:5 0:0 0:0
   100 100 100 100 100 100 100 100 100 100 100
   ^^^ Universe 100 not defined!
```

---

## SUMMARY

**Critical cross-reference validations**:
1. ✅ All surfaces referenced in cells are defined
2. ✅ All non-zero materials referenced in cells are defined
3. ✅ All FILL universes are defined (child before parent)
4. ✅ No circular universe references
5. ✅ Density signs match material fraction signs
6. ✅ All cells have importance, at least one IMP=0
7. ✅ IMP=0 cells use material 0 (void)

**Validation workflow**:
1. Manual review using checklist
2. Automated script for systematic checks
3. MCNP geometry plot (visual verification)
4. MCNP run with small NPS to catch errors early

**Result**: Error-free input files that run on first attempt.

---

**END OF VALIDATION GUIDE**

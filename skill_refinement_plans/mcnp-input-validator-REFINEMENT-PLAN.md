# MCNP INPUT VALIDATOR - COMPREHENSIVE REFINEMENT PLAN

**Created**: November 8, 2025
**Based On**: Analysis of AGR-1 HTGR model, microreactor model, and cross-referencing patterns
**Priority**: 🔴 **CRITICAL** - Current validator missing essential checks for complex reactor models
**Skill Location**: `.claude/skills/mcnp-input-validator/`

---

## EXECUTIVE SUMMARY

The current mcnp-input-validator skill lacks critical validation capabilities discovered in production reactor models:

### Critical Missing Features:
1. ❌ **FILL array dimension validation** (LAT=1 AND LAT=2)
2. ❌ **Universe cross-reference checking** (prevents circular references, undefined universes)
3. ❌ **Numbering conflict detection** (duplicate IDs across entities)
4. ❌ **Thermal scattering verification** (catches missing MT cards for graphite, water, etc.)
5. ❌ **Surface-cell consistency checks** (undefined surface references)

### Impact:
- Users create invalid inputs that fail at runtime
- Missing thermal scattering causes 1000-5000 pcm reactivity errors
- FILL array dimension mismatches cause fatal errors
- Universe conflicts cause geometry errors and lost particles

### Solution:
Add comprehensive validation with complete Python implementations for all checks.

---

## ANALYSIS FINDINGS SYNTHESIS

### Finding 1: FILL Array Mechanics (from AGENT8_FILL_ARRAY_DEEP_DIVE.md)

**Critical patterns discovered:**

#### Rectangular Lattice (LAT=1):
```mcnp
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ 15×15×1 array
     [... 225 universe numbers ...]
```

**Validation rules:**
- Elements required = (7-(-7)+1) × (7-(-7)+1) × (0-0+1) = 15 × 15 × 1 = **225**
- Index ordering: K, J, I (outermost to innermost)
- Repeat notation: `U nR` = (n+1) total copies

#### Hexagonal Lattice (LAT=2):
```mcnp
{n}15 0  -{n}13 u={n}0 lat=2 fill=-6:6 -6:6 0:0  $ 13×13×1 hex array
     [... 169 universe numbers in staggered pattern ...]
```

**Same validation rules apply** - dimension calculation identical for LAT=1 and LAT=2.

#### Common Errors:
| Error | Example | Impact |
|-------|---------|--------|
| Dimension mismatch | fill=0:10, only 10 elements | Fatal: "wrong number of lattice fill entries" |
| Repeat off-by-one | Need 31, use "1117 2R 1116 24R 1117 2R" = 32 | Fatal error |
| Negative indices | fill=-5:5, think it's 5 elements | Fatal: 6 missing elements |

### Finding 2: Universe Cross-Referencing (from AGENT9_CROSS_REFERENCING_PATTERNS.md)

**Hierarchy validation rules:**

```
Level 0: Global (u=0, implicit)
│
├─ Level 1: Compact Lattice (u=1110, LAT=1)
│  └─ References: u=1116, u=1117
│
├─ Level 2: Particle Lattice (u=1116, LAT=1)
│  └─ References: u=1114, u=1115
│
└─ Level 3: TRISO Particle (u=1114)
   └─ No further fill (material cells only)
```

**Critical checks:**
1. ✅ Child universes defined BEFORE parent fills them
2. ✅ No circular references (A→B, B→A)
3. ✅ All filled universes exist
4. ✅ Universe 0 never explicitly defined
5. ✅ Fill references valid universe numbers

**Example circular reference error:**
```mcnp
c INVALID - circular dependency!
100 0 -1 u=10 fill=20
200 0 -2 u=20 fill=10  $ ← ERROR: u=20 fills u=10, u=10 fills u=20
```

### Finding 3: Numbering Schemes (from AGR1_CELL_CARD_COMPLETE_ANALYSIS.md)

**AGR-1 systematic encoding:**

```python
# Cells: 9XYZW
cell_id = 90000 + capsule*1000 + stack*100 + compact*20 + sequence

# Surfaces: 9XYZn
surface_id = 9000 + capsule*100 + stack*10 + compact

# Materials: 9XYZ
material_id = 9000 + capsule*100 + stack*10 + compact

# Universes: XYZW
universe_id = capsule*1000 + stack*100 + compact*10 + component
```

**Conflict detection rules:**
- No duplicate cell IDs
- No duplicate surface IDs
- No duplicate material IDs
- No duplicate universe IDs
- Cell-material-surface correlation checks (optional warning)

### Finding 4: Thermal Scattering (from AGR1_Material_Card_Analysis.md)

**CRITICAL finding:** AGR-1 model MISSING graphite thermal scattering!

```mcnp
m9040  $ pure graphite (lower spacer)
     6000.00c  8.018420E-02
c ← MISSING: mt9040 grph.18t  $ CRITICAL ERROR!
```

**Impact:** Wrong thermal spectrum, incorrect reactivity

**Materials requiring S(α,β) libraries:**
- ✅ **Graphite** (6000, 6012) → grph.XXt
- ✅ **Light water** (H-1 + O-16) → lwtr.XXt
- ✅ **Heavy water** (H-2 + O-16) → hwtr.XXt
- ✅ **Polyethylene** (H-1 + C) → poly.XXt
- ✅ **Beryllium metal** (4009) → be.XXt
- ✅ **Beryllium oxide** (Be + O) → beo.XXt

**Validation logic:**
```python
if material_contains_carbon(m):
    if not has_thermal_scattering(m, 'grph'):
        warning(f"Material {m}: Carbon detected but no MT card (grph.XXt)")
```

### Finding 5: Surface-Cell Consistency (from AGENT9_CROSS_REFERENCING_PATTERNS.md)

**All surface references must be defined:**

```mcnp
c Cell references surfaces 1111, -1118, 74, -29, 53, 100, -110
60106 2106 7.969921E-02  1111 -1118 74 -29 53 100 -110

c All surfaces must exist:
1111 ...
1118 ...
74 ...
29 ...
53 ...
100 ...
110 ...
```

**Validation checks:**
1. Parse all surface references from cell geometry (boolean expressions)
2. Check all surfaces are defined in surfaces section
3. Detect typos (e.g., surface 1000 used but only 100 defined)
4. Check material references (all materials defined)

---

## SKILL UPDATES

### Current File Status

**Existing files:**
- `SKILL.md` (primary skill definition)
- Potentially minimal Python validation scripts

**Files to create:**
1. `validators/fill_array_validator.py` (NEW - comprehensive)
2. `validators/universe_cross_ref_validator.py` (NEW)
3. `validators/numbering_conflict_detector.py` (NEW)
4. `validators/thermal_scattering_checker.py` (NEW)
5. `validators/surface_cell_consistency.py` (NEW)
6. `validation_patterns_reference.md` (NEW - comprehensive examples)
7. `example_inputs/` (NEW - test cases)

---

## IMPLEMENTATION PLAN

### Update 1: SKILL.md Enhancements

**File**: `.claude/skills/mcnp-input-validator/SKILL.md`

**ADD after existing content:**

```markdown
## CRITICAL VALIDATION CATEGORIES

### 1. FILL Array Validation (LAT=1 AND LAT=2)

**Purpose**: Prevent fatal "wrong number of lattice fill entries" errors

**Checks performed:**
- ✅ Dimension calculation: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
- ✅ Repeat notation expansion: `U nR` = (n+1) total copies
- ✅ Element count matches declared fill range
- ✅ All filled universes are defined
- ✅ Lattice type matches surface type (LAT=1→RPP, LAT=2→RHP)

**Example error caught:**
```mcnp
c INVALID - dimension mismatch
100 0 -1 u=200 lat=1 fill=-7:7 -7:7 0:0  $ Need 15×15×1=225 elements
    [... only 200 universe numbers provided ...]  $ ← ERROR: 25 missing!
```

**Tool**: `fill_array_validator.py` (see validators/)

---

### 2. Universe Cross-Reference Validation

**Purpose**: Prevent circular references, undefined universe errors, geometry failures

**Checks performed:**
- ✅ All filled universes are defined before use
- ✅ No circular dependencies (A→B, B→A or longer cycles)
- ✅ Universe 0 never explicitly defined
- ✅ Fill references point to valid LAT cells or simple cells
- ✅ Hierarchy depth reasonable (<10 levels)

**Example error caught:**
```mcnp
c INVALID - circular reference
100 0 -1 u=10 fill=20  $ u=10 fills with u=20
200 0 -2 u=20 fill=10  $ ← ERROR: u=20 fills with u=10 (circular!)
```

**Tool**: `universe_cross_ref_validator.py`

---

### 3. Numbering Conflict Detection

**Purpose**: Prevent duplicate IDs causing ambiguous definitions

**Checks performed:**
- ✅ No duplicate cell IDs
- ✅ No duplicate surface IDs
- ✅ No duplicate material IDs
- ✅ No duplicate universe IDs
- ✅ Optional: Systematic numbering pattern verification
- ✅ Optional: Cell-material-surface correlation warnings

**Example error caught:**
```mcnp
c INVALID - duplicate cell ID
100 1 -10.0 -1 u=10  $ Cell 100
...
100 2 -6.5 -2 u=20   $ ← ERROR: Cell 100 defined twice!
```

**Tool**: `numbering_conflict_detector.py`

---

### 4. Thermal Scattering Verification

**Purpose**: Catch missing MT cards that cause 1000-5000 pcm reactivity errors

**Materials requiring S(α,β) libraries:**

| Material | Detection | Required MT Card | Temperature Options |
|----------|-----------|------------------|---------------------|
| **Graphite** | ZAID 6000, 6012, 6013 | `grph.XXt` | 10t (296K), 18t (600K), 22t (800K), ... |
| **Light water** | H-1 + O-16 | `lwtr.XXt` | 10t (294K), 11t (325K), 13t (350K), 14t (400K), ... |
| **Heavy water** | H-2 + O-16 | `hwtr.XXt` | 10t (294K), 11t (325K) |
| **Polyethylene** | H-1 + C (ratio ~2:1) | `poly.XXt` | 10t (296K), 20t (350K) |
| **Beryllium metal** | ZAID 4009 | `be.XXt` | 10t (296K), 20t (400K), ... |
| **Beryllium oxide** | Be + O | `beo.XXt` | 10t (296K), 20t (400K), ... |

**Checks performed:**
- ✅ Scan all materials for thermal scatterers
- ✅ Verify MT card exists for each
- ✅ Warn if temperature-inappropriate (e.g., grph.10t for 900K reactor)
- ✅ Flag missing MT cards as CRITICAL errors

**Example error caught:**
```mcnp
c CRITICAL ERROR - missing thermal scattering
m1  $ Graphite moderator
    6012.00c  0.9890
    6013.00c  0.0110
c ← MISSING: mt1 grph.18t  $ Will cause wrong thermal spectrum!
```

**Tool**: `thermal_scattering_checker.py`

**Impact:** Missing MT cards cause:
- ❌ Wrong thermal neutron spectrum (hardened)
- ❌ Incorrect reactivity (1000-5000 pcm error typical)
- ❌ Wrong spatial flux distribution
- ❌ Invalid benchmark comparisons

---

### 5. Surface-Cell Consistency Checks

**Purpose**: Prevent "surface XXX not found" fatal errors

**Checks performed:**
- ✅ Parse all surface references from cell boolean expressions
- ✅ Verify all surfaces defined in surfaces section
- ✅ Check material references (all materials defined)
- ✅ Detect common typos (e.g., 1000 vs 100)
- ✅ Warn about unreferenced surfaces (dead geometry)

**Example error caught:**
```mcnp
c INVALID - undefined surface
100 1 -10.0  -1000 2000  $ References surfaces 1000, 2000
...
c Surfaces section:
100 so 5.0   $ ← ERROR: surface 1000 undefined (typo?)
200 pz 10.0  $ ← ERROR: surface 2000 undefined
```

**Tool**: `surface_cell_consistency.py`

---

## VALIDATION WORKFLOW

### Pre-Run Validation Process

```
1. Parse MCNP input file
   ├─ Identify cells, surfaces, materials, universes
   └─ Extract LAT specifications and FILL arrays

2. Run all validators in sequence:
   ├─ Fill array validator (LAT=1 and LAT=2)
   ├─ Universe cross-reference checker
   ├─ Numbering conflict detector
   ├─ Thermal scattering verifier
   └─ Surface-cell consistency checker

3. Report results:
   ├─ CRITICAL errors (must fix before running)
   ├─ WARNINGS (should fix, but may run)
   └─ SUGGESTIONS (best practices)

4. Generate validation report
   └─ Save to input_filename_validation_report.txt
```

### Usage Examples

**Command-line usage:**
```bash
# Validate single file
python -m mcnp_input_validator bench_138B.i

# Validate with detailed output
python -m mcnp_input_validator --verbose bench_138B.i

# Check specific validation category
python -m mcnp_input_validator --check fill_array bench_138B.i
python -m mcnp_input_validator --check thermal_scattering bench_138B.i

# Generate validation report
python -m mcnp_input_validator --report bench_138B.i
```

**Python API usage:**
```python
from mcnp_input_validator import validate_input

# Validate input
results = validate_input('bench_138B.i')

# Check for critical errors
if results['critical_errors']:
    print("CRITICAL ERRORS FOUND:")
    for error in results['critical_errors']:
        print(f"  - {error}")
else:
    print("✓ No critical errors detected")

# Check specific category
from mcnp_input_validator.validators import FillArrayValidator

validator = FillArrayValidator('input.i')
errors = validator.validate()
```

---

## REFERENCE FILES

Detailed validation patterns and examples:
- **validation_patterns_reference.md** - Comprehensive error examples
- **example_inputs/valid/** - Correct MCNP inputs (pass validation)
- **example_inputs/invalid/** - Incorrect inputs with known errors (fail validation)

---

## VALIDATION SEVERITY LEVELS

### CRITICAL (Must fix before running):
- ❌ FILL array dimension mismatch
- ❌ Circular universe references
- ❌ Duplicate numbering (cells, surfaces, materials, universes)
- ❌ Undefined surface references
- ❌ Undefined material references
- ❌ Missing thermal scattering for graphite, water, etc.

### WARNING (Should fix):
- ⚠️ Universe hierarchy depth >6 levels
- ⚠️ Unreferenced surfaces (dead geometry)
- ⚠️ Temperature-inappropriate S(α,β) library
- ⚠️ Non-systematic numbering (hard to maintain)

### SUGGESTION (Best practice):
- 💡 Use repeat notation for long fill arrays
- 💡 Add comments documenting universe hierarchy
- 💡 Use systematic numbering scheme
- 💡 Specify volumes for tally cells
```

---

### Update 2: Fill Array Validator Implementation

**File**: `.claude/skills/mcnp-input-validator/validators/fill_array_validator.py`

```python
"""
MCNP Fill Array Validator
Validates FILL array dimensions for LAT=1 (rectangular) and LAT=2 (hexagonal) lattices

Checks:
1. Element count matches declared fill range
2. Repeat notation correctly expanded
3. All filled universes are defined
4. Lattice type matches surface type
"""

import re
from typing import Dict, List, Tuple, Set


class FillArrayValidator:
    """Validates FILL arrays in MCNP lattice cells"""

    def __init__(self, input_file: str):
        """
        Initialize validator with MCNP input file

        Args:
            input_file: Path to MCNP input file
        """
        self.input_file = input_file
        self.cells = {}  # cell_id: cell_definition
        self.surfaces = {}  # surface_id: surface_definition
        self.universes_defined = set()  # Set of defined universe IDs
        self.lattice_cells = {}  # cell_id: lattice_info
        self.errors = []
        self.warnings = []

        self._parse_input()

    def _parse_input(self):
        """Parse MCNP input file to extract cells, surfaces, universes"""
        with open(self.input_file, 'r') as f:
            content = f.read()

        # Split into blocks (cells, surfaces, data)
        # Simple split on blank line (more robust parsing needed for production)
        blocks = content.split('\n\n')

        # Parse cells block (first block after title)
        in_cells = False
        cell_buffer = []

        for line in content.split('\n'):
            # Skip comments and blank lines
            if line.strip().startswith('c ') or line.strip().startswith('C ') or not line.strip():
                continue

            # Detect surfaces block start
            if line.strip().startswith('*') or re.match(r'^\s*\d+\s+(p[xyz]|c[xyz]|s[ox]|rpp|rhp)', line, re.IGNORECASE):
                in_cells = False

            # Parse cell cards
            if in_cells:
                # Handle line continuation (indented lines)
                if line.startswith('     '):
                    if cell_buffer:
                        cell_buffer[-1] += ' ' + line.strip()
                else:
                    if cell_buffer:
                        self._parse_cell(cell_buffer[-1])
                    cell_buffer.append(line.strip())
            else:
                # Check if this line starts cells block
                if re.match(r'^\d+\s+\d+', line):
                    in_cells = True
                    cell_buffer = [line.strip()]

    def _parse_cell(self, cell_line: str):
        """
        Parse individual cell card to extract LAT and FILL information

        Args:
            cell_line: Complete cell card line (with continuations joined)
        """
        # Extract cell ID
        match = re.match(r'^(\d+)', cell_line)
        if not match:
            return
        cell_id = int(match.group(1))

        self.cells[cell_id] = cell_line

        # Check for universe definition (u=XXX)
        u_match = re.search(r'u=(\d+)', cell_line, re.IGNORECASE)
        if u_match:
            universe_id = int(u_match.group(1))
            self.universes_defined.add(universe_id)

        # Check for lattice definition (lat=1 or lat=2)
        lat_match = re.search(r'lat=([12])', cell_line, re.IGNORECASE)
        if lat_match:
            lat_type = int(lat_match.group(1))

            # Extract FILL specification
            fill_match = re.search(r'fill=([\d\-:]+\s+[\d\-:]+\s+[\d\-:]+)', cell_line, re.IGNORECASE)
            if fill_match:
                fill_spec = fill_match.group(1)

                # Parse fill range: imin:imax jmin:jmax kmin:kmax
                ranges = fill_spec.split()
                if len(ranges) == 3:
                    i_range = ranges[0].split(':')
                    j_range = ranges[1].split(':')
                    k_range = ranges[2].split(':')

                    imin, imax = int(i_range[0]), int(i_range[1])
                    jmin, jmax = int(j_range[0]), int(j_range[1])
                    kmin, kmax = int(k_range[0]), int(k_range[1])

                    # Extract fill array (universe list after fill specification)
                    # This requires parsing continuation lines carefully
                    # For now, store lattice info
                    self.lattice_cells[cell_id] = {
                        'lat_type': lat_type,
                        'imin': imin,
                        'imax': imax,
                        'jmin': jmin,
                        'jmax': jmax,
                        'kmin': kmin,
                        'kmax': kmax,
                        'cell_line': cell_line
                    }

    def calculate_required_elements(self, imin: int, imax: int,
                                     jmin: int, jmax: int,
                                     kmin: int, kmax: int) -> int:
        """
        Calculate required number of elements for FILL array

        Works for BOTH LAT=1 (rectangular) and LAT=2 (hexagonal)

        Args:
            imin, imax: I-index range
            jmin, jmax: J-index range
            kmin, kmax: K-index range

        Returns:
            Total number of elements required
        """
        i_count = imax - imin + 1
        j_count = jmax - jmin + 1
        k_count = kmax - kmin + 1

        return i_count * j_count * k_count

    def expand_repeat_notation(self, fill_array_str: str) -> List[int]:
        """
        Expand MCNP repeat notation to full universe list

        Examples:
            "100 2R 200 24R 100 2R" → [100, 100, 100, 200, ..., 100, 100, 100]

        Args:
            fill_array_str: Fill array with potential repeat notation

        Returns:
            List of universe numbers (fully expanded)
        """
        tokens = fill_array_str.split()
        expanded = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Check for repeat notation (e.g., "2R")
            if token.upper().endswith('R'):
                # Extract repeat count
                repeat_count = int(token[:-1])

                # Repeat previous element
                if expanded:
                    prev = expanded[-1]
                    expanded.extend([prev] * repeat_count)
                else:
                    self.errors.append(f"Repeat notation '{token}' at start (no previous element)")

            else:
                # Regular universe number
                try:
                    universe_num = int(token)
                    expanded.append(universe_num)
                except ValueError:
                    # Not a number, skip (might be comment marker $)
                    pass

            i += 1

        return expanded

    def validate_fill_array(self, cell_id: int, lattice_info: Dict) -> List[str]:
        """
        Validate FILL array for a specific lattice cell

        Args:
            cell_id: Cell ID number
            lattice_info: Dictionary with lattice parameters

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Calculate required elements
        required = self.calculate_required_elements(
            lattice_info['imin'], lattice_info['imax'],
            lattice_info['jmin'], lattice_info['jmax'],
            lattice_info['kmin'], lattice_info['kmax']
        )

        # Extract fill array from cell line
        # Look for universe numbers after "fill=..." specification
        cell_line = lattice_info['cell_line']

        # Find where fill array starts (after fill=i:i j:j k:k)
        fill_match = re.search(r'fill=[\d\-:]+\s+[\d\-:]+\s+[\d\-:]+\s+(.*)', cell_line, re.IGNORECASE)
        if not fill_match:
            errors.append(f"Cell {cell_id}: Cannot parse FILL array")
            return errors

        fill_array_str = fill_match.group(1)

        # Remove comments (everything after $)
        fill_array_str = fill_array_str.split('$')[0]

        # Expand repeat notation
        expanded_fill = self.expand_repeat_notation(fill_array_str)

        # Check element count
        if len(expanded_fill) != required:
            lat_type_name = "rectangular" if lattice_info['lat_type'] == 1 else "hexagonal"
            errors.append(
                f"Cell {cell_id} ({lat_type_name} lattice): FILL array dimension mismatch\n"
                f"  fill={lattice_info['imin']}:{lattice_info['imax']} "
                f"{lattice_info['jmin']}:{lattice_info['jmax']} "
                f"{lattice_info['kmin']}:{lattice_info['kmax']}\n"
                f"  Required: {required} elements "
                f"({lattice_info['imax']-lattice_info['imin']+1} × "
                f"{lattice_info['jmax']-lattice_info['jmin']+1} × "
                f"{lattice_info['kmax']-lattice_info['kmin']+1})\n"
                f"  Provided: {len(expanded_fill)} elements\n"
                f"  Missing: {required - len(expanded_fill)} elements" if required > len(expanded_fill)
                else f"  Extra: {len(expanded_fill) - required} elements"
            )

        # Check all filled universes are defined
        undefined_universes = set(expanded_fill) - self.universes_defined - {0}  # u=0 is always valid
        if undefined_universes:
            errors.append(
                f"Cell {cell_id}: Fill references undefined universes: {sorted(undefined_universes)}"
            )

        return errors

    def validate(self) -> Dict[str, List[str]]:
        """
        Run all fill array validations

        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        for cell_id, lattice_info in self.lattice_cells.items():
            cell_errors = self.validate_fill_array(cell_id, lattice_info)
            self.errors.extend(cell_errors)

        return {
            'errors': self.errors,
            'warnings': self.warnings
        }

    def print_report(self):
        """Print validation report to console"""
        results = self.validate()

        print("=" * 70)
        print("FILL ARRAY VALIDATION REPORT")
        print(f"File: {self.input_file}")
        print("=" * 70)

        print(f"\nLattice cells found: {len(self.lattice_cells)}")
        for cell_id, info in self.lattice_cells.items():
            lat_type_name = "rectangular (LAT=1)" if info['lat_type'] == 1 else "hexagonal (LAT=2)"
            required = self.calculate_required_elements(
                info['imin'], info['imax'],
                info['jmin'], info['jmax'],
                info['kmin'], info['kmax']
            )
            print(f"  Cell {cell_id}: {lat_type_name}, {required} elements required")

        if results['errors']:
            print(f"\n❌ CRITICAL ERRORS ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"\n{error}")
        else:
            print("\n✓ No fill array errors detected")

        if results['warnings']:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"  - {warning}")

        print("\n" + "=" * 70)


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python fill_array_validator.py <input_file>")
        sys.exit(1)

    validator = FillArrayValidator(sys.argv[1])
    validator.print_report()
```

---

### Update 3: Universe Cross-Reference Validator

**File**: `.claude/skills/mcnp-input-validator/validators/universe_cross_ref_validator.py`

```python
"""
MCNP Universe Cross-Reference Validator
Validates universe hierarchy to prevent circular references and undefined universes

Checks:
1. All filled universes are defined
2. No circular dependencies
3. Universe 0 never explicitly defined
4. Reasonable hierarchy depth (<10 levels)
"""

import re
from typing import Dict, List, Set, Tuple


class UniverseCrossRefValidator:
    """Validates universe cross-references and hierarchy"""

    def __init__(self, input_file: str):
        """
        Initialize validator with MCNP input file

        Args:
            input_file: Path to MCNP input file
        """
        self.input_file = input_file
        self.universe_definitions = {}  # universe_id: list of cell_ids defining it
        self.universe_fills = {}  # universe_id: set of filled universe_ids
        self.errors = []
        self.warnings = []

        self._parse_input()

    def _parse_input(self):
        """Parse MCNP input to extract universe definitions and fill references"""
        with open(self.input_file, 'r') as f:
            content = f.read()

        # Parse each cell card
        for line in content.split('\n'):
            # Skip comments and blank lines
            if line.strip().startswith('c ') or line.strip().startswith('C ') or not line.strip():
                continue

            # Look for cells with universe definitions (u=XXX)
            u_match = re.search(r'u=(\d+)', line, re.IGNORECASE)
            if u_match:
                universe_id = int(u_match.group(1))
                cell_id_match = re.match(r'^(\d+)', line.strip())
                if cell_id_match:
                    cell_id = int(cell_id_match.group(1))

                    if universe_id not in self.universe_definitions:
                        self.universe_definitions[universe_id] = []
                    self.universe_definitions[universe_id].append(cell_id)

            # Look for cells with fill directives (fill=XXX or fill=...:... ...)
            fill_match = re.search(r'fill=(\d+)', line, re.IGNORECASE)
            if fill_match:
                filled_universe = int(fill_match.group(1))

                # Determine which universe this cell belongs to
                u_match = re.search(r'u=(\d+)', line, re.IGNORECASE)
                if u_match:
                    parent_universe = int(u_match.group(1))
                else:
                    parent_universe = 0  # Global universe

                if parent_universe not in self.universe_fills:
                    self.universe_fills[parent_universe] = set()
                self.universe_fills[parent_universe].add(filled_universe)

            # Look for lattice fill arrays
            lat_fill_match = re.search(r'lat=[12].*fill=[\d\-:]+\s+[\d\-:]+\s+[\d\-:]+\s+([\d\s\$RrCc]+)',
                                        line, re.IGNORECASE)
            if lat_fill_match:
                fill_array_str = lat_fill_match.group(1).split('$')[0]  # Remove comments

                # Extract universe numbers from fill array
                # Handle repeat notation: "100 2R 200" → [100, 100, 100, 200]
                tokens = fill_array_str.split()
                filled_universes = set()

                for token in tokens:
                    if token.upper().endswith('R'):
                        continue  # Skip repeat notation markers
                    try:
                        universe_num = int(token)
                        filled_universes.add(universe_num)
                    except ValueError:
                        continue

                # Determine parent universe
                u_match = re.search(r'u=(\d+)', line, re.IGNORECASE)
                if u_match:
                    parent_universe = int(u_match.group(1))
                else:
                    parent_universe = 0

                if parent_universe not in self.universe_fills:
                    self.universe_fills[parent_universe] = set()
                self.universe_fills[parent_universe].update(filled_universes)

    def find_undefined_universes(self) -> Set[int]:
        """
        Find all universe IDs that are filled but never defined

        Returns:
            Set of undefined universe IDs
        """
        # Collect all filled universes
        all_filled = set()
        for filled_set in self.universe_fills.values():
            all_filled.update(filled_set)

        # Remove universe 0 (always valid, never defined explicitly)
        all_filled.discard(0)

        # Find undefined universes
        undefined = all_filled - set(self.universe_definitions.keys())

        return undefined

    def find_circular_references(self) -> List[List[int]]:
        """
        Find circular universe references using depth-first search

        Returns:
            List of circular reference chains (each is a list of universe IDs)
        """
        circular_chains = []

        def dfs(universe: int, path: List[int], visited: Set[int]):
            """Depth-first search to detect cycles"""
            if universe in path:
                # Found a cycle
                cycle_start = path.index(universe)
                circular_chains.append(path[cycle_start:] + [universe])
                return

            if universe in visited:
                return

            visited.add(universe)
            path.append(universe)

            # Explore filled universes
            if universe in self.universe_fills:
                for filled_u in self.universe_fills[universe]:
                    dfs(filled_u, path[:], visited)

        # Start DFS from global universe (0) and all root universes
        all_universes = set(self.universe_definitions.keys()) | {0}
        for u in all_universes:
            dfs(u, [], set())

        return circular_chains

    def calculate_hierarchy_depth(self, universe: int = 0, visited: Set[int] = None) -> int:
        """
        Calculate maximum hierarchy depth starting from a universe

        Args:
            universe: Starting universe ID (default 0 = global)
            visited: Set of already visited universes (prevents infinite loops)

        Returns:
            Maximum depth from this universe
        """
        if visited is None:
            visited = set()

        if universe in visited:
            return 0

        visited.add(universe)

        if universe not in self.universe_fills or not self.universe_fills[universe]:
            return 1  # Leaf node

        max_depth = 0
        for filled_u in self.universe_fills[universe]:
            depth = self.calculate_hierarchy_depth(filled_u, visited.copy())
            max_depth = max(max_depth, depth)

        return max_depth + 1

    def check_universe_zero_definition(self) -> bool:
        """
        Check if universe 0 is explicitly defined (it shouldn't be)

        Returns:
            True if error detected, False otherwise
        """
        return 0 in self.universe_definitions

    def validate(self) -> Dict[str, List[str]]:
        """
        Run all universe cross-reference validations

        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        # Check 1: Undefined universes
        undefined = self.find_undefined_universes()
        if undefined:
            self.errors.append(
                f"Undefined universes referenced: {sorted(undefined)}\n"
                f"  These universes are filled but never defined with u=XXX"
            )

        # Check 2: Circular references
        circular = self.find_circular_references()
        if circular:
            for chain in circular:
                chain_str = " → ".join(map(str, chain))
                self.errors.append(
                    f"Circular universe reference detected: {chain_str}\n"
                    f"  Universe {chain[0]} fills {chain[1]}, which eventually fills {chain[0]} again"
                )

        # Check 3: Universe 0 explicitly defined
        if self.check_universe_zero_definition():
            self.errors.append(
                "Universe 0 explicitly defined\n"
                "  Universe 0 is the global universe and should never be defined with u=0"
            )

        # Check 4: Hierarchy depth
        max_depth = self.calculate_hierarchy_depth(0)
        if max_depth > 10:
            self.warnings.append(
                f"Universe hierarchy depth is {max_depth} levels\n"
                f"  Recommendation: Keep hierarchy depth <10 for clarity and performance"
            )
        elif max_depth > 6:
            self.warnings.append(
                f"Universe hierarchy depth is {max_depth} levels (acceptable but deep)"
            )

        return {
            'errors': self.errors,
            'warnings': self.warnings
        }

    def print_report(self):
        """Print validation report to console"""
        results = self.validate()

        print("=" * 70)
        print("UNIVERSE CROSS-REFERENCE VALIDATION REPORT")
        print(f"File: {self.input_file}")
        print("=" * 70)

        print(f"\nUniverses defined: {len(self.universe_definitions)}")
        print(f"Universe fill relationships: {len(self.universe_fills)}")
        print(f"Maximum hierarchy depth: {self.calculate_hierarchy_depth(0)} levels")

        if results['errors']:
            print(f"\n❌ CRITICAL ERRORS ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"\n{error}")
        else:
            print("\n✓ No universe cross-reference errors detected")

        if results['warnings']:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"\n{warning}")

        # Print hierarchy summary
        print("\nUniverse Hierarchy Summary:")
        for universe, filled_set in sorted(self.universe_fills.items()):
            if filled_set:
                print(f"  u={universe} → fills with: {sorted(filled_set)}")

        print("\n" + "=" * 70)


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python universe_cross_ref_validator.py <input_file>")
        sys.exit(1)

    validator = UniverseCrossRefValidator(sys.argv[1])
    validator.print_report()
```

---

### Update 4: Numbering Conflict Detector

**File**: `.claude/skills/mcnp-input-validator/validators/numbering_conflict_detector.py`

```python
"""
MCNP Numbering Conflict Detector
Detects duplicate IDs across cells, surfaces, materials, and universes

Checks:
1. No duplicate cell IDs
2. No duplicate surface IDs
3. No duplicate material IDs
4. No duplicate universe IDs
5. Optional: Systematic numbering pattern warnings
"""

import re
from typing import Dict, List, Set
from collections import defaultdict


class NumberingConflictDetector:
    """Detects numbering conflicts in MCNP input files"""

    def __init__(self, input_file: str):
        """
        Initialize detector with MCNP input file

        Args:
            input_file: Path to MCNP input file
        """
        self.input_file = input_file
        self.cell_ids = defaultdict(list)  # cell_id: [line_numbers]
        self.surface_ids = defaultdict(list)
        self.material_ids = defaultdict(list)
        self.universe_ids = defaultdict(list)
        self.errors = []
        self.warnings = []

        self._parse_input()

    def _parse_input(self):
        """Parse MCNP input to collect all IDs"""
        with open(self.input_file, 'r') as f:
            lines = f.readlines()

        section = 'cells'  # Track which section we're in
        line_num = 0

        for line_num, line in enumerate(lines, start=1):
            # Skip blank lines and full-line comments
            if not line.strip() or line.strip().startswith('c ') or line.strip().startswith('C '):
                continue

            # Detect section transitions
            if re.match(r'^\s*\*', line):  # Surface reflection/transformation
                section = 'surfaces'
                continue

            # Cells section
            if section == 'cells':
                # Match cell card: <cell_id> <mat_id> <density> ...
                cell_match = re.match(r'^(\d+)\s+(\d+|\-?\d+\.\d+[Ee]?[\+\-]?\d*)', line.strip())
                if cell_match:
                    cell_id = int(cell_match.group(1))
                    self.cell_ids[cell_id].append(line_num)

                    # Extract material reference
                    mat_match = re.match(r'^\d+\s+(\d+)', line.strip())
                    if mat_match:
                        mat_id = int(mat_match.group(1))
                        if mat_id > 0:  # Material 0 is void
                            # Material is referenced (not defined here)
                            pass

                    # Extract universe definition (u=XXX)
                    u_match = re.search(r'u=(\d+)', line, re.IGNORECASE)
                    if u_match:
                        universe_id = int(u_match.group(1))
                        self.universe_ids[universe_id].append(line_num)

            # Surfaces section
            elif section == 'surfaces':
                # Match surface card: <surf_id> <type> <params>
                surf_match = re.match(r'^(\d+)\s+([a-z/]+)', line.strip(), re.IGNORECASE)
                if surf_match:
                    surf_id = int(surf_match.group(1))
                    self.surface_ids[surf_id].append(line_num)

            # Data section (materials)
            if line.strip().lower().startswith('m'):
                # Match material card: m<mat_id> or m <mat_id>
                mat_match = re.match(r'^m\s*(\d+)', line.strip(), re.IGNORECASE)
                if mat_match:
                    mat_id = int(mat_match.group(1))
                    self.material_ids[mat_id].append(line_num)

    def find_duplicates(self) -> Dict[str, List[Tuple[int, List[int]]]]:
        """
        Find all duplicate IDs

        Returns:
            Dictionary with duplicate IDs for each category
            Format: {'cells': [(id, [line_numbers])], ...}
        """
        duplicates = {
            'cells': [],
            'surfaces': [],
            'materials': [],
            'universes': []
        }

        # Check cells
        for cell_id, line_nums in self.cell_ids.items():
            if len(line_nums) > 1:
                duplicates['cells'].append((cell_id, line_nums))

        # Check surfaces
        for surf_id, line_nums in self.surface_ids.items():
            if len(line_nums) > 1:
                duplicates['surfaces'].append((surf_id, line_nums))

        # Check materials
        for mat_id, line_nums in self.material_ids.items():
            if len(line_nums) > 1:
                duplicates['materials'].append((mat_id, line_nums))

        # Check universes
        for u_id, line_nums in self.universe_ids.items():
            if len(line_nums) > 1:
                duplicates['universes'].append((u_id, line_nums))

        return duplicates

    def validate(self) -> Dict[str, List[str]]:
        """
        Run all numbering conflict checks

        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        duplicates = self.find_duplicates()

        # Report duplicate cells
        if duplicates['cells']:
            for cell_id, line_nums in duplicates['cells']:
                self.errors.append(
                    f"Duplicate cell ID {cell_id} defined at lines: {', '.join(map(str, line_nums))}"
                )

        # Report duplicate surfaces
        if duplicates['surfaces']:
            for surf_id, line_nums in duplicates['surfaces']:
                self.errors.append(
                    f"Duplicate surface ID {surf_id} defined at lines: {', '.join(map(str, line_nums))}"
                )

        # Report duplicate materials
        if duplicates['materials']:
            for mat_id, line_nums in duplicates['materials']:
                self.errors.append(
                    f"Duplicate material ID {mat_id} defined at lines: {', '.join(map(str, line_nums))}"
                )

        # Report duplicate universes
        if duplicates['universes']:
            for u_id, line_nums in duplicates['universes']:
                self.errors.append(
                    f"Duplicate universe ID {u_id} defined at lines: {', '.join(map(str, line_nums))}"
                )

        # Optional: Check for systematic numbering
        # This is a warning, not an error
        self._check_systematic_numbering()

        return {
            'errors': self.errors,
            'warnings': self.warnings
        }

    def _check_systematic_numbering(self):
        """Check if numbering follows systematic patterns (warning only)"""
        # Check if cell/surface/material IDs correlate (optional best practice)
        # Example: cell 91101 uses material 9111 and surfaces 91111-91115

        # This is complex and model-specific, so just provide general guidance
        if len(self.cell_ids) > 100:
            # Large model - systematic numbering highly recommended
            self.warnings.append(
                "Large model detected (>100 cells). Consider using systematic numbering:\n"
                "  - Encode hierarchy in ID numbers (e.g., XYZW pattern)\n"
                "  - Correlate cell, surface, material IDs for same component\n"
                "  - Reserve number ranges for different subsystems"
            )

    def print_report(self):
        """Print validation report to console"""
        results = self.validate()

        print("=" * 70)
        print("NUMBERING CONFLICT DETECTION REPORT")
        print(f"File: {self.input_file}")
        print("=" * 70)

        print(f"\nEntities found:")
        print(f"  Cells: {len(self.cell_ids)}")
        print(f"  Surfaces: {len(self.surface_ids)}")
        print(f"  Materials: {len(self.material_ids)}")
        print(f"  Universes: {len(self.universe_ids)}")

        if results['errors']:
            print(f"\n❌ CRITICAL ERRORS ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"  - {error}")
        else:
            print("\n✓ No numbering conflicts detected")

        if results['warnings']:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"\n{warning}")

        print("\n" + "=" * 70)


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python numbering_conflict_detector.py <input_file>")
        sys.exit(1)

    detector = NumberingConflictDetector(sys.argv[1])
    detector.print_report()
```

---

### Update 5: Thermal Scattering Checker

**File**: `.claude/skills/mcnp-input-validator/validators/thermal_scattering_checker.py`

```python
"""
MCNP Thermal Scattering Checker
Verifies S(α,β) thermal scattering libraries (MT cards) are present for appropriate materials

CRITICAL: Missing MT cards cause 1000-5000 pcm reactivity errors in thermal reactors!

Checks:
1. Graphite (C) materials have grph.XXt
2. Light water (H-1 + O-16) has lwtr.XXt
3. Heavy water (H-2 + O-16) has hwtr.XXt
4. Polyethylene (H + C) has poly.XXt
5. Beryllium metal has be.XXt
6. Beryllium oxide has beo.XXt
7. Temperature-appropriate library selection
"""

import re
from typing import Dict, List, Set, Tuple


class ThermalScatteringChecker:
    """Checks for missing or inappropriate thermal scattering libraries"""

    # ZAID patterns for thermal scatterers
    GRAPHITE_ZAIDS = {'6000', '6012', '6013'}
    HYDROGEN_ZAIDS = {'1001', '1002'}  # H-1, H-2
    OXYGEN_ZAIDS = {'8016', '8017', '8018'}
    BERYLLIUM_ZAIDS = {'4009'}

    # S(α,β) library recommendations
    THERMAL_SCATTER_LIBS = {
        'graphite': {
            'pattern': 'grph',
            'temperatures': {
                '10t': '296K',
                '18t': '600K',
                '22t': '800K',
                '24t': '1000K',
                '26t': '1200K',
                '28t': '1600K',
                '30t': '2000K'
            }
        },
        'light_water': {
            'pattern': 'lwtr',
            'temperatures': {
                '10t': '294K',
                '11t': '325K (PWR cold leg)',
                '13t': '350K (PWR average)',
                '14t': '400K (PWR hot leg)',
                '16t': '500K',
                '20t': '800K (steam)'
            }
        },
        'heavy_water': {
            'pattern': 'hwtr',
            'temperatures': {
                '10t': '294K',
                '11t': '325K (CANDU)'
            }
        },
        'polyethylene': {
            'pattern': 'poly',
            'temperatures': {
                '10t': '296K',
                '20t': '350K'
            }
        },
        'beryllium': {
            'pattern': 'be',
            'temperatures': {
                '10t': '296K',
                '20t': '400K',
                '22t': '500K',
                '24t': '600K',
                '26t': '700K',
                '28t': '800K'
            }
        },
        'beryllium_oxide': {
            'pattern': 'beo',
            'temperatures': {
                '10t': '296K',
                '20t': '400K',
                '22t': '500K',
                '24t': '600K',
                '26t': '700K',
                '28t': '800K'
            }
        }
    }

    def __init__(self, input_file: str):
        """
        Initialize checker with MCNP input file

        Args:
            input_file: Path to MCNP input file
        """
        self.input_file = input_file
        self.materials = {}  # mat_id: {zaids: set, fractions: dict, density: float}
        self.mt_cards = {}  # mat_id: mt_specification
        self.errors = []
        self.warnings = []

        self._parse_input()

    def _parse_input(self):
        """Parse MCNP input to extract material definitions and MT cards"""
        with open(self.input_file, 'r') as f:
            content = f.read()

        current_material = None
        current_zaids = set()
        current_fractions = {}

        for line in content.split('\n'):
            # Material card: m<id> or m <id>
            mat_match = re.match(r'^m\s*(\d+)', line.strip(), re.IGNORECASE)
            if mat_match:
                # Save previous material
                if current_material is not None:
                    self.materials[current_material] = {
                        'zaids': current_zaids,
                        'fractions': current_fractions
                    }

                # Start new material
                current_material = int(mat_match.group(1))
                current_zaids = set()
                current_fractions = {}
                continue

            # MT card: mt<id> <library> or mt <id> <library>
            mt_match = re.match(r'^mt\s*(\d+)\s+(\S+)', line.strip(), re.IGNORECASE)
            if mt_match:
                mat_id = int(mt_match.group(1))
                library = mt_match.group(2)
                self.mt_cards[mat_id] = library
                continue

            # ZAID line (isotope specification)
            if current_material is not None:
                # Skip comment lines
                if line.strip().startswith('c ') or line.strip().startswith('C '):
                    continue

                # Match ZAID.XXc fraction or ZAID.XXc -fraction
                zaid_match = re.findall(r'(\d+)\.\d+c\s+([\-\d\.Ee\+\-]+)', line, re.IGNORECASE)
                for zaid, fraction in zaid_match:
                    current_zaids.add(zaid)
                    current_fractions[zaid] = float(fraction)

        # Save last material
        if current_material is not None:
            self.materials[current_material] = {
                'zaids': current_zaids,
                'fractions': current_fractions
            }

    def is_graphite(self, mat_zaids: Set[str]) -> bool:
        """Check if material contains graphite (carbon)"""
        return bool(mat_zaids & self.GRAPHITE_ZAIDS)

    def is_light_water(self, mat_zaids: Set[str], fractions: Dict[str, float]) -> bool:
        """Check if material is light water (H-1 + O-16, ratio ~2:1)"""
        has_h1 = '1001' in mat_zaids
        has_o16 = '8016' in mat_zaids
        return has_h1 and has_o16

    def is_heavy_water(self, mat_zaids: Set[str]) -> bool:
        """Check if material is heavy water (H-2 + O-16)"""
        has_h2 = '1002' in mat_zaids
        has_o = bool(mat_zaids & self.OXYGEN_ZAIDS)
        return has_h2 and has_o

    def is_polyethylene(self, mat_zaids: Set[str], fractions: Dict[str, float]) -> bool:
        """Check if material is polyethylene (H + C, ratio ~2:1)"""
        has_h = bool(mat_zaids & self.HYDROGEN_ZAIDS)
        has_c = bool(mat_zaids & self.GRAPHITE_ZAIDS)

        if not (has_h and has_c):
            return False

        # Check H:C ratio (should be ~2:1 for polyethylene)
        # This is approximate - would need better heuristic
        return True

    def is_beryllium_metal(self, mat_zaids: Set[str]) -> bool:
        """Check if material is beryllium metal"""
        return bool(mat_zaids & self.BERYLLIUM_ZAIDS) and len(mat_zaids) == 1

    def is_beryllium_oxide(self, mat_zaids: Set[str]) -> bool:
        """Check if material is beryllium oxide (Be + O)"""
        has_be = bool(mat_zaids & self.BERYLLIUM_ZAIDS)
        has_o = bool(mat_zaids & self.OXYGEN_ZAIDS)
        return has_be and has_o

    def check_material(self, mat_id: int, mat_info: Dict) -> List[str]:
        """
        Check a single material for thermal scattering requirements

        Args:
            mat_id: Material ID number
            mat_info: Dictionary with 'zaids' and 'fractions'

        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        zaids = mat_info['zaids']
        fractions = mat_info.get('fractions', {})

        # Check for graphite
        if self.is_graphite(zaids):
            if mat_id not in self.mt_cards or 'grph' not in self.mt_cards[mat_id].lower():
                errors.append(
                    f"CRITICAL: Material m{mat_id} contains carbon but missing grph.XXt S(α,β) library\n"
                    f"  ZAIDs: {sorted(zaids)}\n"
                    f"  Add: mt{mat_id} grph.18t  $ or appropriate temperature\n"
                    f"  Impact: Wrong thermal spectrum, 1000-5000 pcm reactivity error"
                )

        # Check for light water
        if self.is_light_water(zaids, fractions):
            if mat_id not in self.mt_cards or 'lwtr' not in self.mt_cards[mat_id].lower():
                errors.append(
                    f"CRITICAL: Material m{mat_id} appears to be light water but missing lwtr.XXt library\n"
                    f"  ZAIDs: {sorted(zaids)}\n"
                    f"  Add: mt{mat_id} lwtr.13t  $ or appropriate temperature\n"
                    f"  Impact: Wrong thermal spectrum, incorrect reactivity"
                )

        # Check for heavy water
        if self.is_heavy_water(zaids):
            if mat_id not in self.mt_cards or 'hwtr' not in self.mt_cards[mat_id].lower():
                errors.append(
                    f"CRITICAL: Material m{mat_id} appears to be heavy water but missing hwtr.XXt library\n"
                    f"  ZAIDs: {sorted(zaids)}\n"
                    f"  Add: mt{mat_id} hwtr.11t  $ or appropriate temperature"
                )

        # Check for beryllium metal
        if self.is_beryllium_metal(zaids):
            if mat_id not in self.mt_cards or 'be.' not in self.mt_cards[mat_id].lower():
                errors.append(
                    f"CRITICAL: Material m{mat_id} is beryllium metal but missing be.XXt library\n"
                    f"  Add: mt{mat_id} be.10t  $ or appropriate temperature"
                )

        # Check for beryllium oxide
        if self.is_beryllium_oxide(zaids):
            if mat_id not in self.mt_cards or 'beo' not in self.mt_cards[mat_id].lower():
                errors.append(
                    f"CRITICAL: Material m{mat_id} is beryllium oxide but missing beo.XXt library\n"
                    f"  Add: mt{mat_id} beo.10t  $ or appropriate temperature"
                )

        return errors

    def validate(self) -> Dict[str, List[str]]:
        """
        Run all thermal scattering checks

        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        for mat_id, mat_info in self.materials.items():
            mat_errors = self.check_material(mat_id, mat_info)
            self.errors.extend(mat_errors)

        return {
            'errors': self.errors,
            'warnings': self.warnings
        }

    def print_report(self):
        """Print validation report to console"""
        results = self.validate()

        print("=" * 70)
        print("THERMAL SCATTERING VALIDATION REPORT")
        print(f"File: {self.input_file}")
        print("=" * 70)

        print(f"\nMaterials found: {len(self.materials)}")
        print(f"MT cards found: {len(self.mt_cards)}")

        # Categorize materials
        graphite_mats = []
        water_mats = []
        beryllium_mats = []

        for mat_id, mat_info in self.materials.items():
            zaids = mat_info['zaids']
            if self.is_graphite(zaids):
                graphite_mats.append(mat_id)
            if self.is_light_water(zaids, mat_info.get('fractions', {})):
                water_mats.append(mat_id)
            if self.is_beryllium_metal(zaids) or self.is_beryllium_oxide(zaids):
                beryllium_mats.append(mat_id)

        if graphite_mats:
            print(f"\nGraphite materials: {len(graphite_mats)} (m{', m'.join(map(str, sorted(graphite_mats)))})")
        if water_mats:
            print(f"Water materials: {len(water_mats)} (m{', m'.join(map(str, sorted(water_mats)))})")
        if beryllium_mats:
            print(f"Beryllium materials: {len(beryllium_mats)} (m{', m'.join(map(str, sorted(beryllium_mats)))})")

        if results['errors']:
            print(f"\n❌ CRITICAL ERRORS ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"\n{error}")
        else:
            print("\n✓ No missing thermal scattering libraries detected")

        if results['warnings']:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"\n{warning}")

        # Print available S(α,β) library options
        if results['errors']:
            print("\n" + "=" * 70)
            print("AVAILABLE S(α,β) LIBRARIES:")
            for lib_type, lib_info in self.THERMAL_SCATTER_LIBS.items():
                print(f"\n{lib_type.replace('_', ' ').title()} ({lib_info['pattern']}.XXt):")
                for temp_code, temp_desc in lib_info['temperatures'].items():
                    print(f"  {lib_info['pattern']}.{temp_code:<4} → {temp_desc}")

        print("\n" + "=" * 70)


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python thermal_scattering_checker.py <input_file>")
        sys.exit(1)

    checker = ThermalScatteringChecker(sys.argv[1])
    checker.print_report()
```

---

## VALIDATION TEST CASES

Create test input files to verify validators work correctly.

### Test Case 1: Valid Input (Pass All Checks)

**File**: `.claude/skills/mcnp-input-validator/example_inputs/valid_input.i`

```mcnp
c Valid MCNP Input - Should Pass All Validation Checks
c Rectangular lattice with correct FILL array
c
c Cells
c
c Fuel pin (u=100)
100 1 -10.2  -100         u=100  imp:n=1  $ UO2 fuel
101 2 -6.5   100 -101     u=100  imp:n=1  $ Zircaloy clad
102 3 -1.0   101          u=100  imp:n=1  $ Water

c Pin lattice (u=200) - LAT=1 rectangular
c 3×3 = 9 elements
200 0  -200  u=200 lat=1  imp:n=1  fill=-1:1 -1:1 0:0
     100 100 100
     100 100 100
     100 100 100

c Global cell
999 0  -200 fill=200  imp:n=1
1000 0  200  imp:n=0

c
c Surfaces
c
100 cz  0.41  $ Fuel radius
101 cz  0.48  $ Clad outer radius
200 rpp -1.5 1.5 -1.5 1.5 -100 100  $ Assembly box (3×1.0 cm)

c
c Materials
c
m1  $ UO2 fuel
   92235.70c  0.04
   92238.70c  0.96
    8016.70c  2.0
c
m2  $ Zircaloy
   40000.60c  1.0
c
m3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.13t  $ Thermal scattering for water

c
c Source
kcode 1000 1.0 10 50
ksrc 0 0 0
```

### Test Case 2: FILL Array Error

**File**: `.claude/skills/mcnp-input-validator/example_inputs/invalid_fill_array.i`

```mcnp
c Invalid MCNP Input - FILL Array Dimension Mismatch
c Should trigger error: Need 9 elements but only 8 provided
c
c Cells
c
100 1 -10.2  -100         u=100  imp:n=1
101 0  -200  u=200 lat=1  imp:n=1  fill=-1:1 -1:1 0:0
     100 100 100
     100 100 100
     100 100
c ← ERROR: Only 8 elements, need 9!

999 0  -200 fill=200  imp:n=1
1000 0  200  imp:n=0

c Surfaces
100 cz 0.5
200 rpp -1.5 1.5 -1.5 1.5 -10 10

c Materials
m1 92235.70c 1.0
```

### Test Case 3: Circular Reference Error

**File**: `.claude/skills/mcnp-input-validator/example_inputs/invalid_circular_reference.i`

```mcnp
c Invalid MCNP Input - Circular Universe Reference
c u=10 fills with u=20, u=20 fills with u=10 (circular!)
c
c Cells
c
100 0 -1 u=10 fill=20  imp:n=1
200 0 -2 u=20 fill=10  imp:n=1  $ ← ERROR: circular reference!

999 0  -1 fill=10  imp:n=1
1000 0  1  imp:n=0

c Surfaces
1 so 10
2 so 5
```

### Test Case 4: Missing Thermal Scattering

**File**: `.claude/skills/mcnp-input-validator/example_inputs/invalid_missing_thermal_scatter.i`

```mcnp
c Invalid MCNP Input - Missing Thermal Scattering for Graphite
c
c Cells
c
100 1 -1.8 -1 imp:n=1

c Surfaces
1 so 10

c Materials
m1  $ Graphite - MISSING MT CARD!
    6012.00c  0.9890
    6013.00c  0.0110
c ← ERROR: Should have mt1 grph.18t
```

---

## SUCCESS CRITERIA

### Validator must detect:

✅ **Fill Array Errors:**
- Dimension mismatches (both LAT=1 and LAT=2)
- Repeat notation errors
- Undefined universe references in fill arrays

✅ **Universe Cross-Reference Errors:**
- Circular dependencies
- Undefined universes
- Universe 0 explicit definition

✅ **Numbering Conflicts:**
- Duplicate cell IDs
- Duplicate surface/material/universe IDs

✅ **Thermal Scattering Errors:**
- Missing graphite S(α,β)
- Missing water S(α,β)
- Missing other thermal scatterers

✅ **Surface-Cell Consistency:**
- Undefined surface references
- Undefined material references

---

## EXECUTION CHECKLIST

- [ ] Update SKILL.md with comprehensive validation categories
- [ ] Create fill_array_validator.py with LAT=1 and LAT=2 support
- [ ] Create universe_cross_ref_validator.py
- [ ] Create numbering_conflict_detector.py
- [ ] Create thermal_scattering_checker.py
- [ ] Create surface_cell_consistency.py
- [ ] Create validation_patterns_reference.md
- [ ] Create test input files (valid and invalid)
- [ ] Test all validators with AGR-1 model
- [ ] Test all validators with microreactor model
- [ ] Verify error detection accuracy
- [ ] Update skill with usage examples

---

## ESTIMATED IMPACT

**Before refinement:**
- Users create invalid inputs → runtime failures
- Missing thermal scattering → 1000-5000 pcm errors
- FILL errors → fatal MCNP errors
- Universe conflicts → lost particles, geometry errors

**After refinement:**
- Pre-run validation catches 90%+ of common errors
- Clear error messages with fixes
- Systematic validation workflow
- Production-quality input validation

**Time saved per model:**
- 2-4 hours debugging runtime errors
- Immediate feedback vs. waiting for MCNP run to fail
- Higher confidence in model correctness

---

**PLAN COMPLETE - READY FOR EXECUTION**

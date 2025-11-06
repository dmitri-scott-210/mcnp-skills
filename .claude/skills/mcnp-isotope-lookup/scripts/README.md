# MCNP Isotope Lookup - Python Tools

This directory contains Python tools for MCNP isotope property lookup, ZAID conversion, and library availability checking.

## Tools Overview

### 1. zaid_lookup.py
Convert element names and isotopes to MCNP ZAID format and vice versa.

**Features:**
- Isotope to ZAID conversion
- ZAID to isotope parsing
- ZAID format validation
- Interactive and command-line modes

### 2. isotope_properties.py
Look up atomic masses, natural abundances, and decay data.

**Features:**
- Atomic mass lookup
- Natural isotopic composition
- Half-life data
- Average mass calculation

### 3. library_checker.py
Check MCNP cross-section library availability (xsdir file).

**Features:**
- Verify ZAID availability
- Search for isotopes
- Check entire input files
- Library statistics

## Installation

No installation required. These are standalone Python 3 scripts with no external dependencies.

**Requirements:**
- Python 3.6 or later
- Standard library only

**Make scripts executable (Linux/Mac):**
```bash
chmod +x zaid_lookup.py
chmod +x isotope_properties.py
chmod +x library_checker.py
```

## Usage Guide

### zaid_lookup.py

**Interactive Mode:**
```bash
python zaid_lookup.py

lookup> isotope U-235
Isotope: U-235
ZAID: 92235.80c
Element: Uranium (Z=92)
Library: 80c

lookup> zaid 92235.80c
ZAID: 92235.80c
Isotope: U-235
Element: Uranium (Z=92)
Mass number: A=235
Library: 80c

lookup> element Pb
Element: Lead
Natural ZAID: 82000.80c
Atomic number: Z = 82

lookup> validate 92235.80c
ZAID: 92235.80c
Status: Valid ZAID
Isotope: U-235
```

**Command-Line Mode:**
```bash
# Convert isotope to ZAID
python zaid_lookup.py --isotope "U-235" --library "80c"
python zaid_lookup.py --isotope "Pb"

# Parse ZAID
python zaid_lookup.py --zaid "92235.80c"

# Validate ZAID format
python zaid_lookup.py --validate "92235.80c"

# Get natural element ZAID
python zaid_lookup.py --element "Pb"
```

### isotope_properties.py

**Interactive Mode:**
```bash
python isotope_properties.py

isotope> mass U-235
Isotope: U-235 (Z=92, A=235)
Atomic mass: 235.04393010 amu

isotope> abundance Cl
Element: Cl (Z=17)
Natural isotopic composition:
  Cl-35: 75.7600% (0.757600)
  Cl-37: 24.2400% (0.242400)
Total: 1.000000

isotope> halflife Co-60
Isotope: Co-60
Half-life: 1.663e+08 seconds
          5.27 years

isotope> average Fe
Element: Fe (Z=26)
Calculated average mass: 55.8450 amu

Calculation:
  Fe-54: 0.058450 × 53.939609 = 3.153089
  Fe-56: 0.917540 × 55.934937 = 51.318426
  Fe-57: 0.021190 × 56.935394 = 1.206431
  Fe-58: 0.002820 × 57.933276 = 0.163372
```

**Command-Line Mode:**
```bash
# Get atomic mass
python isotope_properties.py --isotope "U-235"
python isotope_properties.py --mass "Fe-56"

# Get natural abundances
python isotope_properties.py --element "Cl" --abundance

# Calculate average mass
python isotope_properties.py --element "Fe" --average
```

### library_checker.py

**Interactive Mode:**
```bash
python library_checker.py

library> check 92235.80c
ZAID: 92235.80c
Status: AVAILABLE ✓
Atomic weight: 235.04393 amu
File: endf80/U/92235.800nc

library> search ^92
Found 15 matches for '^92':
    1. 92000.80c
    2. 92233.80c
    3. 92234.80c
    4. 92235.80c
    5. 92238.80c
    ...

library> list U
Isotopes of U (Z=92):
  92000.80c
  92233.80c
  92234.80c
  92235.80c
  92238.80c

library> stats
Library Statistics:
Total ZAIDs: 423
By library type:
  .??c:  389
  .??p:   24
  .??e:   10
```

**Command-Line Mode:**
```bash
# Check single ZAID
python library_checker.py --zaid "92235.80c"

# Check all ZAIDs in input file
python library_checker.py --file input.i

# Search for uranium isotopes
python library_checker.py --search "^92"

# List all available ZAIDs
python library_checker.py --list-all
```

**Environment Setup:**
```bash
# Set DATAPATH environment variable
export DATAPATH=/path/to/mcnp/data

# Or specify datapath directly
python library_checker.py --datapath /path/to/mcnp/data --zaid "92235.80c"
```

## Common Workflows

### 1. Material Definition Workflow

**Problem:** Define natural chlorine material

```bash
# Step 1: Get ZAID for natural chlorine
python zaid_lookup.py --element "Cl"
# Output: Natural ZAID: 17000.80c

# Step 2: Check availability
python library_checker.py --zaid "17000.80c"
# Output: Status: AVAILABLE ✓

# Step 3: Get abundances (for explicit isotopes)
python isotope_properties.py --element "Cl" --abundance
# Output:
#   Cl-35: 75.76%
#   Cl-37: 24.24%

# MCNP Material Card:
# M1  17000.80c  1.0      $ Natural chlorine
# Or explicit:
# M1  17035.80c  0.7576   $ Cl-35
#     17037.80c  0.2424   $ Cl-37
```

### 2. Enriched Material Workflow

**Problem:** Define 4.5% enriched UO₂

```bash
# Step 1: Get ZAIDs for U-235 and U-238
python zaid_lookup.py --isotope "U-235"
# Output: ZAID: 92235.80c

python zaid_lookup.py --isotope "U-238"
# Output: ZAID: 92238.80c

# Step 2: Get atomic masses for density calculation
python isotope_properties.py --mass "U-235"
# Output: Atomic mass: 235.04393010 amu

python isotope_properties.py --mass "U-238"
# Output: Atomic mass: 238.05078820 amu

# Step 3: Calculate enriched mass
# A_enriched = 0.045 × 235.044 + 0.955 × 238.051 = 237.916 amu

# MCNP Material Card:
# M1  92235.80c  0.045    $ U-235 (4.5% enriched)
#     92238.80c  0.955    $ U-238 (balance)
#     8016.80c   2.0      $ Oxygen (UO₂)
```

### 3. Activation Analysis Workflow

**Problem:** Identify activation products in aluminum

```bash
# Step 1: Look up parent isotope
python zaid_lookup.py --isotope "Al-27"
# Output: ZAID: 13027.80c

# Step 2: Check natural abundance
python isotope_properties.py --element "Al" --abundance
# Output: Al-27: 100% (monoisotopic)

# Step 3: Identify products (from reference docs)
# Al-27(n,γ)Al-28 → Primary activation
# Al-27(n,α)Na-24 → Secondary (threshold)

# Step 4: Get decay data
python isotope_properties.py --isotope "Al-28" --halflife
# (Note: Limited data in tool, see decay_data.md)

# MCNP Input:
# M1  13027.80c  1.0      $ Aluminum target
# F4:N  10                $ Flux in cell 10
# FM4  (1 10 102)         $ (n,γ) reaction rate
```

### 4. Input Validation Workflow

**Problem:** Verify all isotopes available before running MCNP

```bash
# Check entire input file
python library_checker.py --file my_input.i

# Output if all available:
# Input file: my_input.i
# Total ZAIDs found: 25
# Available: 25
# Missing: 0
# All ZAIDs are available ✓

# Output if missing:
# Input file: my_input.i
# Total ZAIDs found: 25
# Available: 24
# Missing: 1
#
# Missing ZAIDs:
#   ✗ 95255.80c

# Fix: Use alternative
python zaid_lookup.py --element "Am"
# Output: Natural ZAID: 95000.80c (if available)
```

## Integration with Other Tools

These Python tools work seamlessly with:

- **mcnp-material-builder**: Use zaid_lookup.py for material definitions
- **mcnp-source-builder**: Use isotope_properties.py for decay data
- **mcnp-cross-section-manager**: Use library_checker.py for library management
- **mcnp-unit-converter**: Use for density calculations with atomic masses

## Error Handling

**Common Errors and Solutions:**

1. **"DATAPATH not set"** (library_checker.py):
   ```bash
   # Solution: Set environment variable
   export DATAPATH=/path/to/mcnp/data
   ```

2. **"xsdir file not found"**:
   ```bash
   # Solution: Verify DATAPATH points to correct directory
   ls $DATAPATH/xsdir
   ```

3. **"Unknown element"**:
   ```bash
   # Solution: Check spelling and capitalization
   # Correct: "U", "Pu", "Fe"
   # Incorrect: "u", "uranium", "iron"
   ```

4. **"Invalid ZAID format"**:
   ```bash
   # Solution: Use correct format ZZZAAA.nnX
   # Correct: 92235.80c
   # Incorrect: U-235.80c, 92-235.80c, 235.80c
   ```

## Data Sources

The isotope database includes:
- Atomic masses from NIST (2024)
- Natural abundances from IAEA
- Half-lives from NNDC

For complete isotope data, see the reference documentation files:
- `isotope_database.md` - Complete atomic masses and abundances
- `decay_data.md` - Comprehensive decay properties
- `library_availability.md` - Cross-section library information

## Extending the Tools

### Adding New Isotopes

Edit `isotope_properties.py` and add to dictionaries:

```python
# Add atomic mass
ATOMIC_MASSES[(Z, A)] = mass_in_amu

# Add natural abundance
NATURAL_ABUNDANCES[Z] = {A1: frac1, A2: frac2, ...}

# Add half-life
HALF_LIVES[(Z, A)] = half_life_in_seconds
```

### Adding New Elements

Edit `zaid_lookup.py` in ElementData class:

```python
ELEMENTS['Symbol'] = Z
ELEMENT_NAMES['Symbol'] = 'Full Name'
```

## Performance Notes

- **zaid_lookup.py**: Fast (no file I/O)
- **isotope_properties.py**: Fast (in-memory database)
- **library_checker.py**: First run loads xsdir (~1 sec), subsequent checks are cached

## License

These tools are part of the MCNP Skills Project. Use freely for MCNP work and nuclear engineering.

## Version History

**v2.0.0 (2025-11-06):**
- Complete rewrite with modular design
- Interactive and command-line modes
- Standalone tools (no external dependencies)
- Comprehensive isotope database

---

**For complete isotope data, see the parent SKILL.md and reference documentation files.**

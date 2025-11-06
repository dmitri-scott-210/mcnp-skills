# MCNP Unit Converter - Python Scripts

This directory contains standalone Python utilities for unit conversion in MCNP simulations. These tools require **Python 3.6 or later** and have **no external dependencies** (pure stdlib).

---

## 📋 **Contents**

1. **unit_converter.py** - Interactive/command-line unit conversion tool
2. **mcnp_unit_checker.py** - MCNP input file unit validation tool

---

## 🔧 **Tool 1: unit_converter.py**

### Purpose
Convert between different unit systems for MCNP input parameters. Supports interactive mode and command-line usage.

### Supported Conversions
- **Energy:** MeV, eV, keV, GeV, J
- **Length:** cm, m, mm, inch, Angstrom
- **Density:** g/cm³, kg/m³, atom/b-cm
- **Temperature:** K, °C, °F, MeV, eV
- **Cross section:** barn, mb, cm²
- **Activity:** Bq, Ci, mCi, μCi, dps
- **Mass:** g, kg, amu, MeV/c²
- **Time:** s, ms, μs, ns, shake
- **Angle:** degrees, radians, cosine

### Usage Examples

**Interactive Mode** (recommended for multiple conversions):
```bash
python unit_converter.py
```

Then follow the prompts:
```
Enter conversion type (or 'quit'): energy
Enter value: 14.1
From unit (MeV, eV, keV, GeV, J): keV
To unit (MeV, eV, keV, GeV, J): MeV

✓ 14.1 keV = 0.0141 MeV
```

**Command Line Mode** (for scripting):
```bash
# Energy conversion
python unit_converter.py energy 14.1 keV MeV
# Output: 14.1 keV = 0.0141 MeV

# Length conversion
python unit_converter.py length 2.5 m cm
# Output: 2.5 m = 250 cm

# Density conversion (requires atomic weight)
python unit_converter.py density 2.7 g/cm3 atom/b-cm 26.982
# Output: 2.7 g/cm3 = 0.0602646 atom/b-cm

# Temperature conversion
python unit_converter.py temperature 500 C K
# Output: 500 C = 773.15 K

# Activity conversion
python unit_converter.py activity 10 mCi Bq
# Output: 10 mCi = 3.7e+08 Bq

# Angle to cosine
python unit_converter.py angle 30 deg cosine
# Output: 30 deg → cos(30.00°) = 0.866025
```

**Get Help**:
```bash
python unit_converter.py --help           # Command line help
python unit_converter.py --help-detailed  # Detailed help with formulas
```

**Conversion History**:
In interactive mode, type `history` to see all conversions performed in the session.

### Physical Constants Used

From CODATA 2018:
- Speed of light: c = 2.998 × 10⁸ m/s
- Avogadro's number: N_A = 6.022 × 10²³ mol⁻¹
- Boltzmann constant: k_B = 8.617 × 10⁻¹¹ MeV/K
- Atomic mass unit: 1 amu = 931.494 MeV/c²
- 1 barn = 10⁻²⁴ cm²
- 1 Curie = 3.7 × 10¹⁰ Bq

### Scripting Example

Use in Python scripts:
```python
#!/usr/bin/env python3
from unit_converter import UnitConverter

converter = UnitConverter()

# Convert 14.1 keV to MeV
energy_MeV = converter.convert_energy(14.1, 'keV', 'MeV')
print(f"Energy: {energy_MeV} MeV")

# Convert 2.7 g/cm³ Al to atom/b-cm
density = converter.convert_density(2.7, 'g/cm3', 'atom/b-cm', atomic_weight=26.982)
print(f"Density: {density:.6f} atom/b-cm")

# Convert 500°C to Kelvin
temp_K = converter.convert_temperature(500, 'C', 'K')
print(f"Temperature: {temp_K} K")

# Show conversion history
converter.print_history()
```

---

## 🔍 **Tool 2: mcnp_unit_checker.py**

### Purpose
Scan MCNP input files to identify potential unit errors and inconsistencies. Validates:
- Material densities (g/cm³ vs. atom/b-cm)
- Source energies (MeV vs. keV)
- Temperature units (K vs. °C)
- Time bins (shakes vs. seconds)
- Energy bins (MeV vs. keV)

### Usage Examples

**Check Single File**:
```bash
python mcnp_unit_checker.py input.i
```

Output:
```
Checking MCNP input file: input.i
======================================================================

ISSUES (likely errors):
----------------------------------------------------------------------
  Line 25: High mass density
    Mass density 7850.00 g/cm³ exceeds osmium density (~22.6). Possible error.
    → Suggestion: Check if density should be in kg/m³ (divide by 1000) or atom/b-cm (use positive)

SUGGESTIONS (potential improvements):
----------------------------------------------------------------------
  Line 42: Possible keV units
    SDEF ERG=14.100 might be in keV? If so: ERG=0.0141

======================================================================
Summary: 1 issues, 0 warnings, 1 suggestions
======================================================================
```

**Save Report to File**:
```bash
python mcnp_unit_checker.py input.i --report=unit_check_report.txt
```

**Check Multiple Files**:
```bash
python mcnp_unit_checker.py *.i
```

**Verbose Mode**:
```bash
python mcnp_unit_checker.py input.i --verbose
```

### What It Checks

**Material Densities:**
- Flags mass densities outside 0.001–25 g/cm³ range
- Flags atomic densities outside 0.0001–0.15 atom/b-cm range
- Detects potential kg/m³ vs. g/cm³ errors

**Source Energies:**
- Checks SDEF ERG parameter for reasonable MeV range (10⁻¹¹ to 100 MeV)
- Detects likely keV instead of MeV errors
- Validates energy distributions (SI/SP cards)

**Temperature:**
- Checks TMP card for reasonable values (0.1–10000 K or equivalent MeV)
- Detects °C instead of K errors

**Time and Energy Bins:**
- Checks time bins are in shakes (10⁻⁸ s)
- Checks energy bins are in MeV
- Suggests conversions if units appear wrong

**Material Cards:**
- Validates atom fractions (positive) ≤ 1.0
- Validates weight fractions (negative) magnitude ≤ 1.0
- Checks ZAID format consistency

### Exit Codes

- **0**: No issues found (warnings and suggestions may exist)
- **1**: Issues found (likely errors that should be fixed)

Use in CI/CD pipelines:
```bash
python mcnp_unit_checker.py input.i || echo "Unit errors detected!"
```

---

## 🚀 **Quick Start**

### 1. Make Scripts Executable (Linux/Mac)
```bash
chmod +x unit_converter.py mcnp_unit_checker.py
./unit_converter.py
./mcnp_unit_checker.py input.i
```

### 2. Add to PATH (Optional)
```bash
export PATH=$PATH:/path/to/mcnp-skills/.claude/skills/mcnp-unit-converter/scripts
unit_converter.py
```

### 3. Create Alias (Optional)
```bash
# Add to ~/.bashrc or ~/.zshrc
alias mcnp-convert='python /path/to/unit_converter.py'
alias mcnp-check='python /path/to/mcnp_unit_checker.py'

# Usage
mcnp-convert energy 14.1 keV MeV
mcnp-check input.i
```

---

## 📊 **Common MCNP Units Quick Reference**

| Quantity | MCNP Standard | Common Alternatives |
|----------|---------------|---------------------|
| Energy | MeV | eV, keV, GeV, J |
| Length | cm | m, mm, inches |
| Density (mass) | g/cm³ (negative) | kg/m³ |
| Density (atomic) | atom/b-cm (positive) | atoms/cm³ |
| Temperature | K or MeV | °C, °F |
| Cross section | barn | cm², millibarn |
| Time | shake (10⁻⁸ s) | s, μs, ns |
| Mass | amu | g, kg, MeV/c² |
| Activity | Bq or Ci | mCi, μCi, dps |

### MCNP Sign Conventions

**Cell Card Density:**
- **Negative** (`-7.85`): Mass density in g/cm³
- **Positive** (`0.0602`): Atomic density in atom/b-cm

**Material Card Fractions:**
- **Negative** (`-0.98`): Weight fraction
- **Positive** (`0.562`): Atom fraction

---

## ⚠️ **Common Pitfalls**

### 1. Density Sign Error
```mcnp
c WRONG - Using atomic density value with negative sign
10  1  -0.06  -100   $ Should be +0.06 for atom/b-cm

c CORRECT
10  1  -2.7   -100   $ Mass density (g/cm³)
10  1  +0.06  -100   $ Atomic density (atom/b-cm)
```

### 2. Energy Units (keV vs. MeV)
```mcnp
c WRONG - 14.1 keV neutron
SDEF  ERG=14.1

c CORRECT
SDEF  ERG=0.0141   $ 14.1 keV = 0.0141 MeV
```

### 3. Temperature Units
```mcnp
c WRONG - 500°C without conversion
TMP  500

c CORRECT
TMP  773.15   $ 500°C = 773.15 K
```

### 4. Density Conversion (kg/m³ → g/cm³)
```mcnp
c WRONG - Using 7850 kg/m³ directly
10  1  -7850  -100

c CORRECT - Convert to g/cm³
10  1  -7.85  -100   $ 7850 kg/m³ / 1000 = 7.85 g/cm³
```

---

## 🧪 **Testing the Tools**

### Test unit_converter.py
```bash
# Test energy conversion
python unit_converter.py energy 1 MeV eV
# Expected: 1 MeV = 1e+06 eV

# Test density conversion (Aluminum)
python unit_converter.py density 2.7 g/cm3 atom/b-cm 26.982
# Expected: 2.7 g/cm3 = 0.0602646 atom/b-cm

# Test temperature conversion
python unit_converter.py temperature 300 K MeV
# Expected: 300 K = 2.58517e-08 MeV
```

### Test mcnp_unit_checker.py

Create a test file `test.i`:
```mcnp
Test problem with unit errors
c Cell cards
10  1  -7850  -10   $ Steel density in kg/m³ (should be g/cm³)
20  0         10    $ Void

c Surface cards
10  SO  250

c Data cards
M1  26000.80c  -0.98
    6000.80c   -0.02
SDEF  PAR=1  ERG=14.1   $ Likely keV, should be 0.0141 MeV
```

Run checker:
```bash
python mcnp_unit_checker.py test.i
```

Expected output shows issues with density (7850 should be 7.85) and energy (14.1 likely keV).

---

## 📚 **Additional Resources**

- **Main Skill Documentation**: See `../SKILL.md` for comprehensive conversion examples and use cases
- **MCNP Manual**: Chapter 2 (units), Chapter 3 (geometry), Chapter 5 (data cards)
- **Physical Constants**: CODATA 2018 recommended values
- **Integration**: These scripts can be imported as modules in other Python tools

### Related Skills
- `mcnp-material-builder`: Uses density conversions
- `mcnp-source-builder`: Uses energy and activity conversions
- `mcnp-geometry-builder`: Uses length conversions
- `mcnp-physics-builder`: Uses temperature conversions

---

## 🐛 **Troubleshooting**

### Python Version
```bash
python --version  # Should be 3.6 or later
```

If `python` points to Python 2.x, use `python3`:
```bash
python3 unit_converter.py
```

### File Encoding Issues
If you encounter Unicode errors with `mcnp_unit_checker.py`:
```bash
# The script uses utf-8 with error='ignore' to handle non-UTF8 characters
# This should work with most MCNP files
```

### Permission Denied (Linux/Mac)
```bash
chmod +x unit_converter.py mcnp_unit_checker.py
```

---

## 📝 **License**

MIT License - Free to use, modify, and distribute.

## 👤 **Author**

MCNP Skills Project - Phase 4 Utility Tools

For issues, suggestions, or contributions, see the main project repository.

---

**Last Updated**: 2025-11-06
**Python Version**: 3.6+
**Dependencies**: None (pure stdlib)

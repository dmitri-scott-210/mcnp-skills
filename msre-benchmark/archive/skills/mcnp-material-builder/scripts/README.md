# MCNP Material Builder Scripts

Python automation tools for material definition, density calculations, and ZAID validation.

---

## Scripts Overview

| Script | Purpose | Usage |
|--------|---------|-------|
| **material_density_calculator.py** | Calculate densities, convert fractions, temperatures | Interactive or as module |
| **zaid_library_validator.py** | Validate ZAID format, check xsdir availability | File validation or interactive |

---

## 1. material_density_calculator.py

### Features
- Mass density → atomic density conversion (ρ[g/cm³] → ρ[atoms/b-cm])
- Atomic fractions → weight fractions
- Weight fractions → atomic fractions
- Composition normalization
- Temperature conversion (K ↔ MeV)
- Molecular weight calculator
- M card generator

### Usage

**Interactive Mode:**
```bash
python material_density_calculator.py
```

**As Python Module:**
```python
from material_density_calculator import *

# Example: Water density calculation
rho_atomic = mass_density_to_atomic_density(1.0, 18, 3)
print(f"Water atomic density: {rho_atomic:.4f} atoms/b-cm")
# Output: Water atomic density: 0.1003 atoms/b-cm

# Example: H₂O atomic → weight fractions
weight_frac = atomic_fractions_to_weight_fractions({1: 2, 8: 1})
print(weight_frac)
# Output: {1: -0.1119, 8: -0.8881}

# Example: Temperature conversion
temp_MeV = temperature_K_to_MeV(600)
print(f"600 K = {temp_MeV:.6e} MeV")
# Output: 600 K = 5.170200e-08 MeV
```

### Interactive Menu Options

```
1. Mass density → Atomic density
   Input: Mass density (g/cm³), molecular weight (g/mol), atoms per molecule
   Output: Atomic density (atoms/b-cm), MCNP cell card density value

2. Atomic fractions → Weight fractions
   Input: Atomic composition {Z: count}
   Output: Weight fractions {Z: fraction}, sum check

3. Weight fractions → Atomic fractions
   Input: Weight fractions {Z: fraction}
   Output: Atomic fractions {Z: fraction}, sum check

4. Normalize fractions
   Input: Fractions {Z: value}, target sum
   Output: Normalized fractions

5. Temperature K → MeV
   Input: Temperature (K)
   Output: Temperature (MeV), TMP card format

6. Temperature MeV → K
   Input: Temperature (MeV)
   Output: Temperature (K and °C)

7. Calculate molecular weight
   Input: Atomic composition {Z: count}
   Output: Molecular weight (g/mol)

8. Generate M card
   Input: Material number, composition, density, library suffix, comment
   Output: Formatted M card
```

### Examples

**Example 1: UO₂ Fuel Density**
```python
from material_density_calculator import *

# UO₂: U + 2O, M = 238 + 2×16 = 270 g/mol, density = 10.5 g/cm³
rho_atomic = mass_density_to_atomic_density(10.5, 270, 3)  # 3 atoms per molecule
print(f"UO₂ atomic density: -{rho_atomic:.4f}")
# Output: UO₂ atomic density: -0.0702
```

**Example 2: Air Weight Fractions**
```python
# Air: 78% N₂, 21% O₂, 1% Ar by volume → weight fractions
# Molecular weights: N₂=28, O₂=32, Ar=40
volume_fractions = {7: 0.78 * 28, 8: 0.21 * 32, 18: 0.01 * 40}  # Z: mass
weight_frac = normalize_fractions(volume_fractions, -1.0)
print(weight_frac)
# Output: {7: -0.7552, 8: -0.2315, 18: -0.0133}
```

**Example 3: Temperature for Hot Fuel**
```python
# Fuel at 900 K
temp_MeV = temperature_K_to_MeV(900)
print(f"TMP1  {temp_MeV:.6e}")
# Output: TMP1  7.755300e-08
```

---

## 2. zaid_library_validator.py

### Features
- Validate ZAID format (ZZZAAA.nnX, Symbol-A, etc.)
- Check ZAID availability in xsdir file
- Validate M card syntax and consistency
- Detect mixed fraction types (atomic + weight)
- Verify fraction sums for weight fractions
- Suggest similar ZAIDs for typos

### Usage

**Validate Input File:**
```bash
python zaid_library_validator.py input.inp
```

**Validate Single ZAID:**
```bash
python zaid_library_validator.py --zaid 92235.80c
```

**Interactive Mode:**
```bash
python zaid_library_validator.py --interactive
```

### Output Example

```
======================================================================
MCNP Material Card Validation Results
======================================================================

Material 1:
  ZAIDs: 1001.80c, 8016.80c
  Fractions: 2, 1
  ✅ Valid

Material 2:
  ZAIDs: 92235.80c, 92238.80c, 8016.80c
  Fractions: 0.03, 0.97, 2
  ❌ ERRORS:
     - ZAID '92235.80c': Valid full ZAID: Z=92, A=235, lib=80, particle=c (continuous-energy neutron)
  ⚠️  WARNINGS:
     - ZAID '92238.90c': ZAID '92238.90c' not found, but similar: 92238.80c, 92238.70c

----------------------------------------------------------------------
Summary: 0 errors, 1 warnings
======================================================================
```

### As Python Module

```python
from zaid_library_validator import ZAIDValidator

validator = ZAIDValidator()

# Validate ZAID format
valid, msg = validator.validate_zaid_format("92235.80c")
print(msg)
# Output: Valid full ZAID: Z=92, A=235, lib=80, particle=c (continuous-energy neutron)

# Check availability in xsdir
avail, msg = validator.check_availability("92235.80c")
print(msg)
# Output: ZAID '92235.80c' found in xsdir

# Validate M card
m_card = "M1  1001.80c  2  8016.80c  1  NLIB=80c"
result = validator.validate_material_card(m_card)
print(f"Material {result['material_num']}: {len(result['errors'])} errors")
```

### xsdir Detection

The validator automatically searches for xsdir in:
1. `$DATAPATH/xsdir` (environment variable)
2. `/usr/local/MCNP_DATA/xsdir`
3. `/opt/mcnp/data/xsdir`
4. `C:/MCNP_DATA/xsdir`

Or specify manually:
```python
validator = ZAIDValidator(xsdir_path="/custom/path/to/xsdir")
```

---

## Integration with SKILL.md

These scripts support the mcnp-material-builder skill by:

1. **Automating calculations** that users would otherwise do manually
2. **Validating inputs** before expensive MCNP runs
3. **Catching errors early** (missing ZAIDs, fraction issues, library mismatches)
4. **Providing examples** for common material definitions

### Workflow Example

```bash
# Step 1: Calculate density for material
python material_density_calculator.py
# Select option 1, calculate UO₂ density

# Step 2: Generate M card
# Use option 8 to generate formatted M card

# Step 3: Validate M card in input file
python zaid_library_validator.py my_input.inp
# Check for errors/warnings before running MCNP
```

---

## Requirements

- Python 3.6+
- No external dependencies (uses standard library only)
- Optional: xsdir file for library availability checking

---

## Common Use Cases

### Use Case 1: Converting Material Composition Data Sheet
```
Data sheet: Concrete density 2.3 g/cm³
Composition: H 1.0%, C 0.1%, O 53.0%, ... (by weight)

→ Use material_density_calculator.py option 8
→ Generate M card with weight fractions
```

### Use Case 2: Fuel Assembly with Enrichment Change
```
Need to change UO₂ from 3% to 5% enrichment

→ Use atomic fractions: {92: 0.05, 238: 0.95, 8: 2.0}
→ Recalculate density with option 1
→ Generate new M card with option 8
```

### Use Case 3: Pre-Run Validation
```
Created input file with 10 materials

→ Run: python zaid_library_validator.py input.inp
→ Fix any errors/warnings before submitting to compute cluster
→ Saves hours of wasted compute time
```

### Use Case 4: Library Migration (ENDF/B-VII.0 → VIII.0)
```
Need to update all .70c to .80c

→ Validate current file to get list of ZAIDs
→ Check .80c availability for each
→ Update input file
→ Re-validate to confirm
```

---

## Troubleshooting

### Issue: xsdir not found
**Solution:** Set `DATAPATH` environment variable:
```bash
export DATAPATH=/path/to/mcnp/data
```

### Issue: "Module not found" when importing
**Solution:** Add scripts directory to Python path:
```python
import sys
sys.path.append('/path/to/.claude/skills/mcnp-material-builder/scripts')
from material_density_calculator import *
```

### Issue: Validation shows "library not found" for valid ZAID
**Solution:** Check that xsdir is up-to-date and contains the library you're using.

---

## See Also

- **Material References:** `../references/` for detailed M card specifications
- **Templates:** `../assets/templates/` for material definition examples
- **SKILL.md:** Main skill documentation for mcnp-material-builder

---

**Version:** 1.0
**Created:** 2025-11-03
**For:** mcnp-material-builder skill v2.0

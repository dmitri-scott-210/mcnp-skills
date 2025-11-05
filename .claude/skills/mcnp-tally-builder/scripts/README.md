# MCNP Tally Builder Scripts

Python automation tools for validating and analyzing MCNP tally specifications.

## Scripts

### 1. tally_validator.py

Validates tally card specifications in MCNP input files before running simulations.

**Features:**
- Checks F card references to valid cells/surfaces
- Validates energy bins are monotonically increasing
- Verifies FM card material references
- Checks DE/DF card entry count matching
- Validates FS/SD card compatibility
- Checks tally number conventions

**Usage:**
```bash
python tally_validator.py input.i
python tally_validator.py input.i --verbose
```

**Example Output:**
```
======================================================================
MCNP Tally Validation Report: reactor.i
======================================================================

Parsed: 25 cells, 42 surfaces, 5 materials, 8 tallies

✅ No errors found

WARNINGS (2):
  ⚠️  Tally F14: Has DE14 but no DF14
  ⚠️  Tally F20: Uses tally number ending in 0 (MCNP uses last digit for tally type)

======================================================================
```

**Requirements:**
- Python 3.6+
- No external dependencies

---

### 2. dose_function_plotter.py

Plots flux-to-dose conversion factors from MCNP DE/DF cards or built-in standards.

**Features:**
- Extracts DE/DF cards from MCNP input files
- Plots response functions on log-log scale
- Built-in ICRP-74 AP neutron dose factors
- Export plots to PNG/PDF
- Statistics summary box

**Usage:**
```bash
# Plot from MCNP input file
python dose_function_plotter.py input.i 14

# Plot built-in standard
python dose_function_plotter.py --builtin ICRP74_AP

# Save to file
python dose_function_plotter.py input.i 14 --output dose_response.png
```

**Built-in Standards:**
- `ICRP74_AP` - ICRP-74 Anterior-Posterior neutron dose factors

**Requirements:**
- Python 3.6+
- matplotlib
- numpy

**Installation:**
```bash
pip install matplotlib numpy
```

---

## Integration with MCNP Workflow

### Pre-Simulation Validation

Before running expensive MCNP simulations, validate tally specifications:

```bash
# Validate input file
python tally_validator.py my_model.i

# If no errors, proceed with MCNP
mcnp6 i=my_model.i
```

### Dose Function Verification

When using DE/DF dose conversion cards, visualize the response function:

```bash
# Plot dose function for tally 14
python dose_function_plotter.py my_model.i 14

# Compare with standard
python dose_function_plotter.py --builtin ICRP74_AP
```

### Batch Processing

Validate multiple input files:

```bash
for file in *.i; do
    echo "Validating $file..."
    python tally_validator.py "$file"
done
```

---

## Common Issues and Solutions

**Issue:** Script cannot find tally cards
- **Solution:** Ensure input file has proper three-block structure (cells, surfaces, data)

**Issue:** DE/DF entry count mismatch
- **Solution:** Check that DE and DF cards have equal number of values

**Issue:** Material not found warning
- **Solution:** Verify FM card material numbers match defined M cards

**Issue:** Energy bins not monotonically increasing
- **Solution:** Check E card values are in ascending order

---

## Examples

### Example 1: Basic Validation

```bash
$ python tally_validator.py example.i

======================================================================
MCNP Tally Validation Report: example.i
======================================================================

Parsed: 10 cells, 15 surfaces, 3 materials, 4 tallies

✅ No errors found
✅ All tally validations passed!

======================================================================
```

### Example 2: Validation with Errors

```bash
$ python tally_validator.py broken.i

======================================================================
MCNP Tally Validation Report: broken.i
======================================================================

Parsed: 10 cells, 15 surfaces, 3 materials, 4 tallies

ERRORS (2):
  ❌ Line 45: F14 references non-existent cell 999
  ❌ Line 52: E14 energy bins not monotonically increasing: 1.0 >= 0.5

WARNINGS (1):
  ⚠️  Line 48: FM14 references material M7 which is not defined

======================================================================
```

### Example 3: Dose Function Plotting

```bash
$ python dose_function_plotter.py reactor.i 14
Plot saved to: dose_response.png
```

---

## Development

### Running Tests

```bash
# Test validator
python tally_validator.py ../example_tallies/01_basic_flux_spectrum.i

# Test plotter
python dose_function_plotter.py --builtin ICRP74_AP
```

### Adding New Built-in Standards

Edit `dose_function_plotter.py` and add to built-in dictionaries:

```python
ICRP116_AP_NEUTRON = {
    'energies': [...],
    'factors': [...]
}
```

---

## License

MIT License - See main project LICENSE file

## Author

MCNP Skills Revamp Project

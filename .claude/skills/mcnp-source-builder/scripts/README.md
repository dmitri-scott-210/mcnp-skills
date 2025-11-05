# MCNP Source Builder - Automation Scripts

This directory contains Python scripts for visualizing and validating MCNP source definitions.

---

## 📋 Contents

1. **source_spectrum_plotter.py** - Energy spectrum visualization
2. **source_validator.py** - Source definition validation

---

## 1. source_spectrum_plotter.py

**Purpose:** Plot energy and angular distributions for MCNP source definitions.

**Dependencies:**
```bash
pip install numpy matplotlib
```

### Supported Spectra

| Spectrum Type | Formula | Parameters |
|---------------|---------|------------|
| Watt | p(E) ∝ exp(-E/a) × sinh(√(bE)) | a, b |
| Maxwellian | p(E) ∝ √E × exp(-E/T) | T |
| Gaussian | p(E) ∝ exp(-(E-E₀)²/(2σ²)) | E₀, σ |
| Exponential | p(E) ∝ exp(-λE) | λ |
| Discrete | Lines at specific energies | E[], I[] |

### Usage Examples

**Watt Fission Spectrum (U-235 thermal):**
```bash
python source_spectrum_plotter.py --type watt --param1 0.988 --param2 2.249
```

**Maxwellian Spectrum:**
```bash
python source_spectrum_plotter.py --type maxwell --param1 1.29
```

**Gaussian Spectrum:**
```bash
python source_spectrum_plotter.py --type gaussian --param1 2.5 --param2 0.1
```

**Discrete Gamma Lines (Co-60):**
```bash
python source_spectrum_plotter.py --type discrete \
    --energies 1.173 1.332 \
    --intensities 1.0 1.0
```

**Save to File:**
```bash
python source_spectrum_plotter.py --type watt --param1 0.988 --param2 2.249 \
    --output u235_spectrum.png
```

### Integration with MCNP

**For SDEF with Watt spectrum:**
```
SDEF  ERG=D1
SI1   -3        $ Watt spectrum (built-in function -3)
SP1   0.988 2.249
```

**For SDEF with discrete gammas:**
```
SDEF  ERG=D1
SI1 L 1.173 1.332  $ List of energies
SP1   1.0   1.0     $ Relative intensities
```

---

## 2. source_validator.py

**Purpose:** Validate SDEF, SI, SP, SB, and DS card consistency.

**No Dependencies** - Uses only Python standard library.

### Validation Checks

1. **SP Probability Normalization**
   - Type D (discrete): Should sum to 1.0
   - Type C (cumulative): Last value must be 1.0
   - Warns if normalization is off

2. **SI/SP Length Consistency**
   - Histogram (H) or Arbitrary (A): SI has n+1 values for n SP values
   - List (L) or Special (S): SI and SP must have equal length

3. **SDEF Distribution References**
   - All ERG=Dn, DIR=Dn, POS=Dn must have corresponding SIn

4. **Missing Cards**
   - Warns if SI exists without SP (uniform sampling assumed)
   - Errors if SP exists without SI

### Usage Examples

**Validate Single File:**
```bash
python source_validator.py input.i
```

**Interactive Mode:**
```bash
python source_validator.py --interactive
```

### Example Output

```
======================================================================
MCNP Source Validation Report: input.i
======================================================================

ERRORS FOUND: 1
  ERROR: SP1 (type C): Last cumulative probability is 0.95, not 1.0.
         This will cause source sampling errors.

WARNINGS: 1
  WARNING: SP2 (type D): Probabilities sum to 0.998, not 1.0.
           MCNP will normalize, but verify intent.

Summary:
  SI cards found: 3
  SP cards found: 3
  SB cards found: 1
  DS cards found: 0
  SDEF references: 2
======================================================================
```

### Exit Codes

- **0**: No errors (warnings OK)
- **1**: Errors found or file not accessible

---

## Common Workflows

### Workflow 1: Design Watt Spectrum Source

```bash
# 1. Plot spectrum to verify parameters
python source_spectrum_plotter.py --type watt --param1 0.988 --param2 2.249

# 2. Create MCNP input with SDEF
# (See templates/energy_spectrum_templates.i)

# 3. Validate source definition
python source_validator.py input.i
```

### Workflow 2: Validate Discrete Gamma Source

```bash
# 1. Visualize gamma lines
python source_spectrum_plotter.py --type discrete \
    --energies 0.662 1.173 1.332 \
    --intensities 0.85 1.0 1.0

# 2. Validate MCNP input
python source_validator.py gamma_source.i

# 3. Check SP normalization warnings
```

### Workflow 3: Compare Multiple Spectra

```bash
# Generate plots for comparison
python source_spectrum_plotter.py --type watt --param1 0.988 --param2 2.249 --output u235.png
python source_spectrum_plotter.py --type watt --param1 1.175 --param2 1.040 --output pu239.png
python source_spectrum_plotter.py --type maxwell --param1 1.29 --output maxwell.png
```

---

## Troubleshooting

**ImportError: No module named 'matplotlib'**
```bash
pip install matplotlib numpy
```

**FileNotFoundError in validator**
- Check file path is correct
- Use absolute paths if relative paths fail

**"SP probabilities don't sum to 1.0" warning**
- MCNP will normalize automatically
- Verify probabilities are correct (not a bug)
- If using type C (cumulative), last value MUST be 1.0

**"SI and SP length mismatch" error**
- For histogram (SI1 H): Use n+1 bin edges, n probabilities
- For list (SI1 L): Use n values, n probabilities
- Check for missing or extra values

---

## Integration with Other Skills

- **mcnp-tally-builder**: Validate source-tally consistency
- **mcnp-physics-builder**: Ensure MODE card matches source particles
- **mcnp-input-validator**: Comprehensive input file validation
- **mcnp-variance-reducer**: Optimize source biasing (SB cards)

---

## References

- MCNP Manual Chapter 5.08: Source Data Cards
- `source_distribution_reference.md` - Complete SI/SP specification
- `source_error_catalog.md` - Common source definition errors

---

**Created:** 2025-11-03
**Author:** Claude (Anthropic)
**Skill:** mcnp-source-builder v2.0

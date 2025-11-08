# Reproducibility Checklist for MCNP Reactor Models

**Purpose:** Ensure reactor models are reproducible by others

**Required for:** Publication, licensing, collaboration, archival

---

## Essential Elements

### 1. Version Control

**Requirement:** ALL source files under version control

**What to include:**
- [x] Input generation scripts (.py, .sh, etc.)
- [x] Templates (.template, .jinja2)
- [x] External data files (.csv, .json)
- [x] README and documentation
- [x] Validation scripts
- [x] Post-processing scripts

**What to exclude (.gitignore):**
- Generated MCNP inputs (*.i, *.inp) - too large, regenerable
- MCNP outputs (o, r, m, s files) - very large
- Temporary files

**Commands:**
```bash
git init
git add scripts/ data/ templates/ README.md requirements.txt
git commit -m "Initial reactor model - baseline configuration"
git tag v1.0-baseline
```

---

### 2. Dependencies Documentation

**Requirement:** Document ALL software and versions

**requirements.txt (Python):**
```
python==3.11.0
numpy==1.24.0
pandas==2.0.0
jinja2==3.1.2
matplotlib==3.7.0
```

**Software versions document:**
```markdown
# Software Dependencies

## MCNP
- Version: MCNP6.2 (build 2020-02-14)
- Platform: Linux x86_64
- MPI: OpenMPI 4.1.1

## Cross Sections
- Library: ENDF/B-VII.1
- xsdir date: 2018-05-01
- Location: /path/to/mcnp/data/

## Python Environment
- Python: 3.11.0
- See requirements.txt for package versions

## Operating System
- OS: Ubuntu 22.04 LTS
- Kernel: 5.15.0
```

---

### 3. Complete Workflow Documentation

**Requirement:** README explains regeneration from scratch

**Essential README sections:**

````markdown
# Reactor Model Name

## Purpose
Brief description of what model calculates and why.

## Regeneration from Scratch

**Prerequisites:**
- MCNP6.2 installed
- Python 3.11+ with packages from requirements.txt
- Cross sections: ENDF/B-VII.1

**Steps:**
```bash
# 1. Clone repository
git clone https://github.com/user/reactor-model.git
cd reactor-model

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Generate all inputs
python scripts/create_inputs.py

# 4. Validate outputs
python scripts/validate_inputs.py

# Expected output: 13 inputs in outputs/mcnp/, 0 errors
```

## Input Files

### External Data
- `data/power.csv`: Experimental power history
  - Source: ECAR-3569, "ATR Power History"
  - Date: 2023-01-15
  - Columns: cycle, lobe, power_MW, duration_days

- `data/positions.csv`: Control drum angles
  - Source: ATR operations logbook
  - Date: 2023-01-20
  - Columns: cycle, angle_deg, timestamp

- `data/materials.json`: Material compositions
  - Source: INL/EXT-10-17686, "Fuel Specification"
  - Date: 2022-12-01
  - Contains: Enrichments, densities, isotopic fractions

### Templates (if used)
- `templates/atr_base.template`: ATR quarter-core base model
  - Lines: 13,727
  - Source: Validated ATR model (2020)
  - Static sections: ATR fuel elements, reflector
  - Variable sections: Experiment region, control positions

## Outputs

### Generated MCNP Inputs
- Location: `outputs/mcnp/`
- Count: 13 files (one per cycle)
- Naming: `reactor_{cycle}.i` (e.g., reactor_138B.i)
- Size: ~18,400 lines each

### Validation
- Geometry plots: Run `mcnp6 ip i=outputs/mcnp/reactor_138B.i`
- VOID test: Included in validation script
- Expected: 0 lost particles, no geometry errors

## Validation Criteria

**Geometry:**
- [ ] Plotted from XY, XZ, YZ views (no dashed lines)
- [ ] VOID test passed (0 lost particles in 1M particle run)
- [ ] Volume check: MCNP vs CAD < 2% difference

**Physics:**
- [ ] All graphite has MT cards (grph.18t for operating)
- [ ] All cross sections from same library (.70c family)
- [ ] Keff for baseline within 50 pcm of benchmark

**Reproducibility:**
- [ ] Single command regenerates all inputs
- [ ] Generated inputs match reference (if available)
- [ ] No manual editing required

## Citation

If using this model, please cite:

```
Author, A. & Collaborator, B. (2024). Reactor Model for X Analysis.
Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX
```

## License

MIT License (or specify your license)

## Contact

For questions: author@institution.edu
````

---

### 4. Data Provenance

**Requirement:** Every value traceable to source

**data_sources.md:**
```markdown
# Data Provenance

## Fuel Composition
- **Source:** INL/EXT-10-17686, "AGR-1 Irradiation Test Specification"
- **Date:** June 2006
- **Enrichment:** 19.75% U-235 (Table 3.1)
- **Kernel diameter:** 350 μm ± 10 μm (measured, Section 2.3)
- **Packing fraction:** 0.37 (calculated from particle count and compact volume)

## Graphite Properties
- **Source:** Toyo Tanso IG-110 Product Data Sheet
- **Date:** Revision 3, 2019
- **Density:** 1.74 g/cm³ (nominal, Table 1)
- **Purity:** >99.9% carbon
- **Thermal conductivity:** 116 W/m·K @ 298K

## Power History
- **Source:** ECAR-3569, "ATR Core Internal Changeout #138B Power History"
- **Date:** March 2023
- **Measured by:** Automated data acquisition system (ATRC DAQ)
- **Time resolution:** 1-hour averages
- **Accuracy:** ±2% (instrument specification)

## Control Positions
- **Source:** ATR Operations Logbook, Cycles 138B-145A
- **Date:** 2018-2020
- **Recorded by:** Reactor operators (each shift)
- **Precision:** ±0.1° (OSCC position indicator)
```

---

### 5. External Data Files

**Requirement:** Include data, freeze versions

**data/power.csv:**
```csv
cycle,lobe,power_MW,duration_days,source
138B,NE,1.235,42.5,ECAR-3569
138B,SE,1.312,42.5,ECAR-3569
139A,NE,1.401,38.2,ECAR-3570
139A,SE,1.378,38.2,ECAR-3570
```

**Include metadata:**
```markdown
# power.csv Metadata

- **Created:** 2024-01-15
- **Version:** 2.1
- **SHA256:** a1b2c3d4e5f6... (compute with `sha256sum power.csv`)
- **Rows:** 26 (13 cycles × 2 lobes)
- **Columns:** cycle, lobe, power_MW, duration_days, source
- **Units:** Power in MW(thermal), duration in days
```

---

### 6. Validation Test Suite

**Requirement:** Automated checks for correctness

**scripts/validate_inputs.py:**
```python
#!/usr/bin/env python3
"""Comprehensive validation of all generated inputs."""

def validate_all():
    """Run all validation checks."""
    checks = [
        ('Geometry', validate_geometry),
        ('Numbering', validate_numbering),
        ('Cross-refs', validate_cross_references),
        ('Thermal scattering', validate_thermal_scattering),
        ('Lattices', validate_lattice_dimensions),
    ]

    results = {}
    for name, check_func in checks:
        print(f"Running {name} validation...")
        results[name] = check_func()

    # Summary
    passed = sum(results.values())
    total = len(results)

    if passed == total:
        print(f"\n✓ All {total} validation checks PASSED")
        return 0
    else:
        print(f"\n✗ {total-passed} of {total} checks FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(validate_all())
```

---

### 7. Permanent Identifier (DOI)

**Requirement:** Assign DOI for permanent citation

**How to assign DOI (using Zenodo):**

1. **Create Zenodo account:** https://zenodo.org/

2. **Link GitHub repository:**
   - Settings → Integrations → Zenodo
   - Enable repository

3. **Create release:**
   ```bash
   git tag v1.0
   git push --tags
   ```

4. **Zenodo automatically creates DOI**
   - Example: 10.5281/zenodo.1234567

5. **Add DOI badge to README:**
   ```markdown
   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)
   ```

---

### 8. License Specification

**Requirement:** Specify usage terms

**Common choices:**

**MIT License (permissive):**
- Allows commercial use
- Minimal restrictions
- Most common for research code

**Apache 2.0 (permissive with patent grant):**
- Like MIT + patent protection
- Good for industry collaboration

**CC0 (public domain):**
- No restrictions whatsoever
- Good for data and simple scripts

**GPL v3 (copyleft):**
- Derived works must also be open
- Ensures modifications stay open

**Add LICENSE file to repository root.**

---

## Complete Checklist

### Before First Commit
- [ ] Git repository initialized
- [ ] .gitignore configured (exclude generated outputs)
- [ ] README.md started

### During Development
- [ ] Commit frequently with meaningful messages
- [ ] External data files in data/ directory
- [ ] Generation scripts in scripts/ directory
- [ ] Templates (if used) in templates/ directory

### Before Publication/Sharing
- [ ] README complete with regeneration instructions
- [ ] requirements.txt or dependencies documented
- [ ] data_sources.md documenting provenance
- [ ] Validation script working
- [ ] All tests passing
- [ ] LICENSE file added
- [ ] DOI assigned (Zenodo or institutional repository)
- [ ] Citation information in README

### Test of Reproducibility
- [ ] Fresh clone on different machine
- [ ] Install dependencies
- [ ] Run generation script
- [ ] Compare outputs to originals
- [ ] All match (or differences documented)

---

## Common Pitfalls

**Avoid:**
- ❌ Hardcoded paths (`/home/myuser/...`)
- ❌ Manual editing of generated files
- ❌ Undocumented magic numbers
- ❌ "Latest" dependencies (pin versions!)
- ❌ Missing data files
- ❌ Uncommitted changes before sharing

**Instead:**
- ✅ Relative paths or configurable paths
- ✅ All changes in generation scripts
- ✅ Every value documented
- ✅ Specific versions (numpy==1.24.0)
- ✅ All data version-controlled
- ✅ Clean repository, all committed

---

## Minimal Example

**Absolute minimum for reproducibility:**

```
reactor-model/
├── README.md          # How to regenerate
├── requirements.txt   # Python dependencies
├── data/
│   └── parameters.csv # All input parameters
├── scripts/
│   └── create_input.py # Generation script
└── reference/
    └── baseline.i     # Known-good reference
```

**README.md (minimal):**
```markdown
# Reactor Model

## Regeneration
```bash
pip install -r requirements.txt
python scripts/create_input.py
```

Expected output: reactor.i (18,400 lines)

## Software
- Python 3.11
- MCNP6.2
- ENDF/B-VII.1 cross sections

## Data Source
data/parameters.csv from INL/EXT-10-17686 (2006)

## Validation
```bash
mcnp6 ip i=reactor.i  # Plot geometry
# Expect: No errors, matches reference/baseline.i
```
```

---

**END OF REPRODUCIBILITY CHECKLIST**

This ensures your reactor model can be regenerated and trusted by others.

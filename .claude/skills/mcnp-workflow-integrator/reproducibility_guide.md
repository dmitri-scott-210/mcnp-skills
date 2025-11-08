# Reproducibility Engineering Guide

Making MCNP workflows reproducible for peer review and archival.

## Overview

Reproducibility is essential for:
- Peer review and publication
- Future extensions by others
- Regulatory compliance
- Scientific integrity
- Long-term archival

**Goal**: Anyone with the repository can regenerate inputs, rerun calculations, and reproduce results.

---

## Version Control Best Practices

### Repository Structure

**Recommended directory layout**:

```
mcnp-project/
├── README.md                 # Complete documentation
├── LICENSE                   # Legal framework
├── CITATION.cff              # Citation information
├── .gitignore                # Ignore generated files
├── requirements.txt          # Python dependencies
├── data/                     # External data (CSV, Excel)
│   ├── power.csv
│   ├── control_positions.csv
│   ├── geometry_params.yaml
│   └── experimental_results.csv
├── scripts/                  # Generation and analysis
│   ├── input_definition.py  # Shared parameters
│   ├── create_inputs.py     # Input generation
│   ├── validate.py          # Pre-run checks
│   ├── run_workflow.sh      # Orchestration script
│   └── post_process.py      # Results analysis
├── templates/                # Jinja2 templates (if used)
│   └── base_model.template
├── inputs/                   # Generated MCNP inputs (gitignored)
├── outputs/                  # MCNP outputs (gitignored)
└── results/                  # Processed results, figures
    ├── plots/
    └── tables/
```

### .gitignore Patterns

**What to exclude from version control**:

```gitignore
# MCNP outputs
*.o
*.r
*.m
*.s
*.msht
*.mctal
*.runtpe
*.comout

# Generated inputs (regenerate with scripts)
inputs/*.i
inputs/*.inp

# Large output files
outputs/
*.h5
*.hdf5

# Temporary files
*.tmp
*.swp
*~
.DS_Store

# Python cache
__pycache__/
*.pyc
*.pyo
*.egg-info/
.pytest_cache/

# Jupyter checkpoints
.ipynb_checkpoints/

# Virtual environments
venv/
env/
.venv/

# IDE files
.vscode/
.idea/
*.sublime-*

# Plots (if regenerable)
results/plots/*.png
results/plots/*.pdf

# Logs
*.log
```

### What to Version Control

✅ **Always version control**:
- Source code (Python, bash scripts)
- Templates (Jinja2, etc.)
- External data files (CSV, Excel - if reasonable size)
- Configuration files
- Documentation (README, guides)
- Requirements files (requirements.txt, environment.yml)
- LICENSE
- CITATION.cff

❌ **Never version control**:
- Generated MCNP inputs (regenerate from scripts)
- MCNP output files (too large)
- Compiled binaries
- Large data files (use Git LFS or external storage)
- API keys, passwords, credentials

### Commit Message Conventions

**Use conventional commit format**:

```
<type>: <short summary>

<optional detailed description>

<optional footer>
```

**Types**:
- `feat`: New feature (e.g., "feat: Add hexagonal lattice support")
- `fix`: Bug fix (e.g., "fix: Correct FILL array dimension calculation")
- `docs`: Documentation (e.g., "docs: Update README with workflow description")
- `test`: Tests (e.g., "test: Add validation for thermal scattering")
- `refactor`: Code restructuring (e.g., "refactor: Simplify material generation")
- `style`: Code formatting (e.g., "style: Apply PEP8 formatting")
- `chore`: Maintenance (e.g., "chore: Update dependencies")

**Examples**:

```bash
git commit -m "feat: Add TRISO particle generation functions"

git commit -m "fix: Correct packing fraction calculation

Previous calculation did not account for SiC layer thickness.
Now includes all 5 TRISO layers in volume calculation."

git commit -m "docs: Add complete workflow diagram to README"
```

### Branch Strategy

**For parameter studies**:

```bash
# Main branch: stable, working code
git checkout main

# Feature branch for new capability
git checkout -b feature/add-control-assembly

# Make changes, commit
git add scripts/control_assembly.py
git commit -m "feat: Add control assembly generation"

# Merge back to main when ready
git checkout main
git merge feature/add-control-assembly
```

**For parametric variations**:

```bash
# Tag each cycle/case
git tag -a cycle_138B -m "AGR-1 Cycle 138B parameters"
git tag -a cycle_139A -m "AGR-1 Cycle 139A parameters"

# List tags
git tag -l

# Checkout specific cycle
git checkout cycle_138B
```

---

## Documentation Standards

### README.md Template

**Comprehensive README structure**:

```markdown
# Project Title

Brief description of reactor model and analysis goals.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

## Purpose

What question does this analysis answer?

**Example**: This repository contains MCNP models for shutdown dose rate calculations of a microreactor core, supporting decommissioning planning and personnel safety analysis.

## Repository Contents

- `data/`: External data sources
  - `power.csv`: Reactor power history
  - `geometry.yaml`: Geometric parameters
  - `experimental_results.csv`: Validation data
- `scripts/`: Model generation and analysis
  - `input_definition.py`: Shared parameter definitions
  - `create_inputs.py`: MCNP input generator
  - `validate.py`: Pre-run validation
  - `post_process.py`: Results analysis
- `templates/`: Jinja2 templates (if applicable)
- `results/`: Publication-quality outputs

## Requirements

### Software

- MCNP6.2 or later
- Python 3.8+
- (Optional) MOAA for depletion coupling

### Python Packages

Install dependencies:

    pip install -r requirements.txt

Required packages:
- pandas >= 1.3.0
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- jinja2 >= 3.0.0

## Usage

### 1. Generate MCNP Inputs

    python scripts/create_inputs.py

This generates MCNP input files in `inputs/` directory.

### 2. Validate Inputs

    python scripts/validate.py inputs/*.i

### 3. Run Calculations

**Local execution**:

    ./scripts/run_workflow.sh

**HPC cluster (SLURM)**:

    sbatch scripts/submit_job.sh

### 4. Post-Process Results

    python scripts/post_process.py

Results are saved to `results/` directory.

## Validation

Results have been compared to:
- Experimental measurements (data/experimental_results.csv)
- Benchmark calculations (Smith et al., 2023)
- Expected physical trends

See `results/validation_report.pdf` for details.

## Results

Key findings:
- Shutdown dose rate at 1 day cooling: X.XX Sv/h
- Maximum dose location: (coordinates)
- Comparison to regulatory limit: within/exceeds

## Citation

If you use this work, please cite:

    Author, A., Author, B. (2024). Title of Work. Journal Name, Volume(Issue), Pages.
    DOI: 10.xxxx/xxxxx

BibTeX:

```bibtex
@article{author2024,
  title={Title of Work},
  author={Author, A. and Author, B.},
  journal={Journal Name},
  volume={XX},
  number={X},
  pages={XXX--XXX},
  year={2024},
  doi={10.xxxx/xxxxx}
}
```

## License

This project is licensed under [LICENSE TYPE] - see LICENSE file for details.

## Contact

- Author Name: author@institution.edu
- Institution: University/Lab Name
- ORCID: 0000-0000-0000-0000

## Acknowledgments

This work was supported by [Funding Agency] under Grant No. [XXX].

Computational resources provided by [HPC Center].
```

### CITATION.cff Format

**Machine-readable citation file**:

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: "HTGR Burnup and Dose Rate Analysis"
version: 1.0.0
date-released: 2024-01-15
doi: 10.5281/zenodo.1234567
url: "https://github.com/user/repo"
repository-code: "https://github.com/user/repo"
license: MIT

authors:
  - family-names: "Doe"
    given-names: "Jane"
    orcid: "https://orcid.org/0000-0000-0000-0001"
    affiliation: "University of Example"
    email: "jane.doe@example.edu"
  - family-names: "Smith"
    given-names: "John"
    orcid: "https://orcid.org/0000-0000-0000-0002"
    affiliation: "National Laboratory"

keywords:
  - MCNP
  - reactor physics
  - shutdown dose rate
  - TRISO fuel
  - HTGR

abstract: |
  This repository contains MCNP models and analysis scripts for
  calculating shutdown dose rates in a high-temperature gas-cooled
  reactor. The workflow demonstrates coupling between neutron transport,
  depletion, and photon transport calculations.

references:
  - type: article
    title: "Shutdown Dose Rate Calculations for HTGR Decommissioning"
    authors:
      - family-names: "Doe"
        given-names: "Jane"
      - family-names: "Smith"
        given-names: "John"
    journal: "Nuclear Engineering and Design"
    volume: 400
    year: 2024
    doi: "10.1016/j.nucengdes.2024.xxxxx"
```

### requirements.txt

**Python dependencies**:

```txt
# Core dependencies
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
jinja2>=3.0.0

# Optional dependencies
scipy>=1.7.0
h5py>=3.0.0
openpyxl>=3.0.0  # For Excel files

# Development dependencies
pytest>=7.0.0
black>=22.0.0
flake8>=4.0.0
```

Or use `environment.yml` for conda:

```yaml
name: mcnp-workflow
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - pandas>=1.3.0
  - numpy>=1.21.0
  - matplotlib>=3.4.0
  - jinja2>=3.0.0
  - scipy>=1.7.0
  - h5py>=3.0.0
  - pip
  - pip:
    - openpyxl>=3.0.0
```

---

## Data Provenance

### Tracking Data Sources

**Provenance metadata**:

```python
# In input generation script

PROVENANCE = {
    'power_data': {
        'source': 'ATR operational records',
        'source_url': 'https://example.gov/atr-data',
        'file': 'data/power.csv',
        'date_accessed': '2024-01-10',
        'date_range': '2005-12-01 to 2009-04-01',
        'notes': 'Lobe-specific power by cycle and timestep',
        'contact': 'data-manager@example.gov'
    },
    'control_positions': {
        'source': 'ATR control system logs',
        'file': 'data/oscc.csv',
        'date_accessed': '2024-01-10',
        'notes': 'Outer safety control cylinder rotation angles',
        'processing': 'Time-weighted averaging applied to get discrete values'
    },
    'geometry': {
        'source': 'ORNL-TM-6744 (AGR-1 design report)',
        'reference': 'Maki et al., ORNL/TM-6744, 2009',
        'url': 'https://info.ornl.gov/sites/publications/Files/Pub12602.pdf',
        'notes': 'TRISO particle dimensions, compact specifications, capsule geometry'
    },
    'cross_sections': {
        'library': 'ENDF/B-VII.1',
        'version': '00c',
        'temperature': '600K',
        'source': 'MCNP Data Library',
        'path': '/projects/mcnpdata/xsdir_mcnp6.2'
    },
    'validation_data': {
        'source': 'AGR-1 Post-Irradiation Examination',
        'reference': 'Demkowicz et al., INL/EXT-10-20722, 2011',
        'file': 'data/experimental_results.csv',
        'parameters_measured': ['burnup_FIMA', 'isotopic_ratios']
    }
}

# Save provenance with results
import json
with open('results/data_provenance.json', 'w') as f:
    json.dump(PROVENANCE, f, indent=2)

print("Data provenance saved to results/data_provenance.json")
```

### Calculation Metadata

**Record calculation details**:

```python
import platform
import datetime
import subprocess

def record_calculation_metadata(output_dir='results'):
    """Record metadata about calculation environment."""

    metadata = {
        'timestamp': datetime.datetime.now().isoformat(),
        'hostname': platform.node(),
        'os': platform.system(),
        'os_version': platform.release(),
        'python_version': platform.python_version(),
        'cpu_count': os.cpu_count(),
        'user': os.getenv('USER'),
        'working_directory': os.getcwd(),
    }

    # MCNP version
    try:
        result = subprocess.run(['mcnp6', 'v'], capture_output=True, text=True, timeout=5)
        metadata['mcnp_version'] = result.stderr.split('\n')[0] if result.stderr else 'Unknown'
    except:
        metadata['mcnp_version'] = 'Unknown'

    # Python packages
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
    metadata['python_packages'] = result.stdout

    # Git commit
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
        metadata['git_commit'] = result.stdout.strip()

        result = subprocess.run(['git', 'describe', '--tags'], capture_output=True, text=True)
        metadata['git_tag'] = result.stdout.strip()
    except:
        metadata['git_commit'] = 'Unknown'
        metadata['git_tag'] = 'Unknown'

    # Save metadata
    with open(f'{output_dir}/calculation_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Calculation metadata saved to {output_dir}/calculation_metadata.json")

    return metadata
```

---

## Archival Best Practices

### Zenodo Integration

**Create DOI for permanent citation**:

1. **Connect GitHub to Zenodo**:
   - Go to https://zenodo.org
   - Connect GitHub account
   - Enable repository

2. **Create Release**:
   ```bash
   git tag -a v1.0.0 -m "Version 1.0.0 - Initial publication release"
   git push origin v1.0.0
   ```

3. **Zenodo Automatically Creates DOI**

4. **Add DOI Badge to README**:
   ```markdown
   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
   ```

### Long-Term File Formats

**Choose archival-friendly formats**:

✅ **Recommended for archival**:
- Text files: `.txt`, `.csv`, `.dat` (plain ASCII)
- Structured data: `JSON`, `YAML`, `XML`
- Documents: `PDF/A` (archival PDF standard)
- Scientific data: `HDF5`, `NetCDF`
- Images: `PNG`, `TIFF`

❌ **Avoid for archival**:
- Proprietary binary formats
- Format versions likely to become obsolete
- Compressed formats without documentation
- Platform-specific formats

**Convert MCNP outputs for archival**:

```python
def archive_mcnp_outputs(output_file, archive_dir='archive'):
    """
    Convert MCNP outputs to archival formats.

    - Extract key results to CSV/JSON
    - Convert plots to PDF/A
    - Save mesh tallies to HDF5
    """
    os.makedirs(archive_dir, exist_ok=True)

    # Extract keff to CSV
    keff, uncert = extract_keff(output_file)
    pd.DataFrame([{
        'keff': keff,
        'uncertainty': uncert,
        'file': output_file,
        'date': datetime.datetime.now().isoformat()
    }]).to_csv(f'{archive_dir}/keff_results.csv', index=False)

    # Extract tallies to JSON
    tallies = extract_all_tallies(output_file)
    with open(f'{archive_dir}/tally_results.json', 'w') as f:
        json.dump(tallies, f, indent=2)

    # Convert plots to PDF/A
    # (Use matplotlib with PDF backend)

    print(f"Archived results in {archive_dir}/")
```

### Minimal Reproducibility Package

**Essential files for reproduction**:

```
minimal_reproducibility_package/
├── README.md                 # Complete instructions
├── LICENSE                   # Legal framework
├── CITATION.cff              # How to cite
├── requirements.txt          # Dependencies
├── data/                     # All input data
│   └── *.csv
├── scripts/                  # All generation scripts
│   ├── create_inputs.py
│   └── post_process.py
├── expected_results/         # For validation
│   └── keff_expected.csv
└── run.sh                    # One-command execution
```

**Checklist before archival**:

```markdown
## Reproducibility Checklist

- [ ] All data files included
- [ ] All generation scripts included
- [ ] README with complete instructions
- [ ] Software version requirements documented
- [ ] Expected runtime and resources documented
- [ ] Validation data included
- [ ] LICENSE file included
- [ ] CITATION.cff created
- [ ] DOI assigned (Zenodo)
- [ ] Tested on clean system
- [ ] All dependencies installable
- [ ] Scripts run without errors
- [ ] Results match expected values
```

---

## Continuous Reproducibility

**Automated testing of reproducibility**:

```yaml
# .github/workflows/reproducibility-test.yml
name: Test Reproducibility

on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly
  workflow_dispatch:  # Manual trigger

jobs:
  test-reproducibility:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Generate inputs
        run: |
          python scripts/create_inputs.py

      - name: Compare to reference
        run: |
          diff -r inputs/ reference_inputs/ || echo "Inputs differ from reference"

      - name: Test runs (if MCNP available)
        run: |
          # Would run MCNP if available in CI environment
          # For now, just test scripts run
          echo "MCNP execution skipped in CI"

      - name: Validate results format
        run: |
          python scripts/validate_results.py

      - name: Generate report
        run: |
          python scripts/generate_reproducibility_report.py

      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: reproducibility-report
          path: reproducibility_report.html
```

---

## Summary

**Reproducibility Engineering Principles**:

1. **Version Control Everything**: Code, data, templates, documentation
2. **Document Thoroughly**: README, CITATION.cff, inline comments
3. **Track Provenance**: Record where every piece of data came from
4. **Use Standard Formats**: CSV, JSON, HDF5 for archival
5. **Assign DOI**: Permanent identifier via Zenodo
6. **Test Reproducibility**: Ensure others can actually reproduce

**Essential Files**:
- README.md (complete instructions)
- LICENSE (legal framework)
- CITATION.cff (machine-readable citation)
- requirements.txt (dependencies)
- .gitignore (exclude generated files)
- data/ (all input data)
- scripts/ (all generation/analysis code)

**Long-Term Success Criteria**:
- Repository cloneable by anyone
- Dependencies installable
- Scripts run without modification
- Results reproducible
- Work citable with DOI

**Next Steps**:
1. Adopt repository structure
2. Create comprehensive README
3. Implement data provenance tracking
4. Assign DOI via Zenodo
5. Test reproducibility on clean system

---
category: B
name: mcnp-input-updater
description: Systematically update MCNP input files for version changes, library updates, deprecated syntax, and modernization while preserving functionality
activation_keywords:
  - update input
  - upgrade mcnp
  - convert version
  - modernize input
  - library update
  - ENDF update
  - deprecated syntax
  - batch update
  - systematic update
---

# MCNP Input Updater Skill

## Purpose

This skill guides users in systematically updating MCNP input files to accommodate version changes (MCNP5→MCNP6), cross-section library updates (ENDF/B-VII→VIII), deprecated syntax modernization, and adding new features to legacy inputs. It focuses on batch updates, automated transformations, validation of changes, and preserving simulation functionality while leveraging modern MCNP6 capabilities.

## When to Use This Skill

- Migrating inputs from MCNP5 to MCNP6
- Updating cross-section libraries (ENDF/B-VII.0 → ENDF/B-VIII.0)
- Modernizing legacy inputs (10+ years old)
- Replacing deprecated cards or syntax
- Adding new MCNP6 features to existing inputs
- Batch updating multiple inputs systematically
- Standardizing input format across project
- Fixing compatibility issues after MCNP updates
- Updating thermal scattering tables (S(α,β))
- Converting between file naming conventions
- Systematic parameter updates (densities, temperatures, etc.)

## Prerequisites

- **mcnp-input-editor**: Understanding of input editing techniques
- **mcnp-input-validator**: Ability to validate updated inputs
- **mcnp-material-builder**: Knowledge of material definitions and libraries
- Basic understanding of MCNP version differences
- Knowledge of cross-section library conventions
- Text processing skills (regex, scripting useful but not required)

## Core Concepts

### Version Differences (MCNP5 vs MCNP6)

**Major Changes in MCNP6**:

1. **Particle Designators**: New notation for some particles
   ```
   MCNP5: MODE H        (heavy ions)
   MCNP6: MODE H        (same, but expanded capabilities)
   ```

2. **PHYS Card Enhancements**: More options
   ```
   MCNP5: PHYS:N  100
   MCNP6: PHYS:N  100  J  J  1  J  J  J  J  (additional parameters)
   ```

3. **New Cards**: MCNP6 additions
   - `DBRC` (Doppler Broadening Rejection Correction)
   - `PIKMT` (Photonuclear physics)
   - Enhanced `FMESH` capabilities
   - `EMBED` geometry (embedded meshes)

4. **Library Updates**: New ZAID suffixes
   ```
   MCNP5: 92235.70c     (ENDF/B-VII.0)
   MCNP6: 92235.80c     (ENDF/B-VIII.0)
   MCNP6: 92235.00c     (Latest library, version-agnostic)
   ```

5. **Deprecated Features**:
   - Some old macrobody syntax (rare)
   - Certain tally options (TALLYX, legacy formats)

### Cross-Section Library Evolution

**Library Identifiers**:
```
.50c  : ENDF/B-V
.60c  : ENDF/B-VI (MCNP4C)
.70c  : ENDF/B-VII.0 (MCNP5/6)
.80c  : ENDF/B-VIII.0 (MCNP6.2+)
.00c  : Latest available (MCNP6.3+)
```

**Key Differences ENDF/B-VII.0 vs VIII.0**:
- Updated resonance parameters
- Improved thermal scattering kernels
- More isotopes available
- Better covariance data
- Some ZAID changes (e.g., natural element definitions)

**Thermal Scattering Updates**:
```
ENDF/B-VII:  LWTR.01T  (293K water)
ENDF/B-VIII: LWTR.20T  (updated kernel)
```

### Update Strategies

**Strategy 1: Conservative** (Minimal Changes)
- Update only what's required for MCNP6 compatibility
- Keep existing library versions if working
- Validate against original results

**Strategy 2: Moderate** (Recommended Updates)
- Update to MCNP6
- Upgrade to ENDF/B-VIII.0 (latest validated)
- Add new cards for improved physics (DBRC for U-238)
- Modernize formatting

**Strategy 3: Aggressive** (Full Modernization)
- Latest MCNP6.3 features
- Latest libraries (.00c)
- Mesh tallies instead of point detectors
- Automatic variance reduction (WWG)
- DBRC, enhanced physics options

**Selection Criteria**:
- Legacy validation important? → Conservative
- Standard production work? → Moderate
- New project with modern tools? → Aggressive

## Decision Tree: Update Planning

```
START: What needs updating?
  |
  +--> Version Migration (MCNP5 → MCNP6)
  |      ├─> Input runs in MCNP5 currently? Yes
  |      ├─> Test MCNP6 compatibility first
  |      ├─> Update PHYS cards (add default J values)
  |      ├─> Check for deprecated cards
  |      └─> Validate results match MCNP5 (within stats)
  |
  +--> Library Update (ENDF/B-VII → VIII)
  |      ├─> Identify all ZAID references
  |      |    ├─> M cards (material definitions)
  |      |    ├─> MT cards (thermal scattering)
  |      |    └─> MX cards (nuclide substitution)
  |      ├─> Systematic replacement (.70c → .80c)
  |      ├─> Update thermal scattering tables
  |      ├─> Validate material compositions unchanged
  |      └─> Compare results (expect small differences)
  |
  +--> Deprecated Syntax Modernization
  |      ├─> Identify deprecated cards (from warnings)
  |      ├─> Replace with modern equivalents
  |      ├─> Test incrementally (one change at a time)
  |      └─> Validate functionality preserved
  |
  +--> Add New Features
  |      ├─> DBRC for U-238 resonance treatment
  |      ├─> Mesh tallies (FMESH) for spatial distributions
  |      ├─> Enhanced physics (PHYS card options)
  |      ├─> Automatic variance reduction (WWG)
  |      └─> Test features independently before combining
  |
  +--> Batch Update (Multiple Files)
  |      ├─> Identify common patterns across files
  |      ├─> Create update script/procedure
  |      ├─> Test on single file first
  |      ├─> Apply to all files
  |      └─> Validate sample of updated files
  |
  +--> Format Standardization
         ├─> Consistent commenting style
         ├─> Card alignment and spacing
         ├─> Naming conventions (cells, surfaces, materials)
         └─> Documentation blocks
```

## Use Case 1: MCNP5 to MCNP6 Migration (Conservative)

**Scenario**: Legacy MCNP5 input needs to run in MCNP6 with minimal changes

**Original MCNP5 Input**:
```
Legacy Reactor Model - MCNP5
c Cell Cards
1  1  -10.5  -1  IMP:N=1
2  0  1  IMP:N=0

c Surface Cards
1  SO  10

c Data Cards
MODE  N
M1  92235.70c  -0.03  92238.70c  -0.97
PHYS:N  20                         $ MCNP5 format
SDEF  POS=0 0 0  ERG=2.0
F4:N  1
NPS  1000000
```

**Updated MCNP6 Input** (Conservative):
```
Legacy Reactor Model - MCNP6 Compatible
c Cell Cards
1  1  -10.5  -1  IMP:N=1
2  0  1  IMP:N=0

c Surface Cards
1  SO  10

c Data Cards
MODE  N
M1  92235.70c  -0.03  92238.70c  -0.97    $ Keep .70c (validated)
PHYS:N  20  J  J  J  J  J  J  J           $ Add default parameters for MCNP6
SDEF  POS=0 0 0  ERG=2.0
F4:N  1
NPS  1000000
```

**Changes Made**:
1. Title updated to indicate MCNP6
2. PHYS:N card expanded with default J values
3. Libraries kept at .70c (no physics changes)

**Validation**:
```bash
# Run both versions
mcnp5 inp=original.i outp=out5.o
mcnp6 inp=updated.i outp=out6.o

# Compare keff or tally results (should match within statistics)
```

**Key Points**:
- Minimal changes reduce risk
- Keep original for validation
- Results should match (same libraries, same physics)

## Use Case 2: Library Update (ENDF/B-VII.0 to VIII.0)

**Scenario**: Update all materials to ENDF/B-VIII.0 libraries

**Original Materials**:
```
M1  1001.70c  2  8016.70c  1        $ Water (ENDF/B-VII.0)
MT1  LWTR.01T                       $ Thermal scattering (old)

M2  92235.70c  -0.03  92238.70c  -0.97  $ Fuel
TMP2  1.2e-7                        $ Reactor temperature

M3  6000.70c  1.0                   $ Graphite
MT3  GRPH.01T
```

**Updated Materials**:
```
M1  1001.80c  2  8016.80c  1        $ Water (ENDF/B-VIII.0)
MT1  LWTR.20T                       $ Thermal scattering (updated kernel)

M2  92235.80c  -0.03  92238.80c  -0.97  $ Fuel (updated library)
TMP2  1.2e-7
DBRC2  92238                        $ Add DBRC for U-238 (MCNP6 feature)

M3  6000.80c  1.0                   $ Graphite (updated)
MT3  GRPH.10T                       $ Updated graphite kernel
```

**Systematic Replacement**:
```
Find: .70c
Replace: .80c
(All material ZAIDs updated)

Find: .01T
Replace: .20T or .10T (depending on material)
(Thermal scattering tables updated)
```

**Validation**:
```
c Expected differences:
c - keff may change by ~0.1-0.5% (cross-section updates)
c - Reaction rates may differ slightly
c - This is EXPECTED and correct (improved physics)
```

**Key Points**:
- Systematic replacement (all ZAIDs at once)
- Update thermal scattering tables to match
- Add DBRC for U-238 (recommended for ENDF/B-VIII.0)
- Results WILL differ slightly (this is correct)

## Use Case 3: Add DBRC (Doppler Broadening Rejection Correction)

**Scenario**: Add DBRC to materials with U-238 for improved resonance treatment

**Before** (Standard treatment):
```
M1  92235.80c  0.03  92238.80c  0.97
TMP1  1.2e-7                        $ Reactor temperature
```

**After** (With DBRC):
```
M1  92235.80c  0.03  92238.80c  0.97
TMP1  1.2e-7
DBRC1  92238                        $ DBRC for U-238 only
```

**When to Use DBRC**:
- Reactor calculations (especially LWRs)
- U-238 present in significant amounts
- Temperature >600K
- Resonance region important (1 eV - 10 keV)

**Impact**:
- More accurate capture rates
- Slight increase in runtime (~5-10%)
- Improved keff accuracy (typically +20-50 pcm)

**Key Points**:
- MCNP6 feature (not in MCNP5)
- Specify ZAID, not material (DBRC1 92238, not DBRC1 1)
- Can list multiple isotopes: DBRC1 92238 94239
- Only for nuclides in resolved resonance range

## Use Case 4: Modernize Thermal Scattering Tables

**Scenario**: Update S(α,β) tables to latest versions

**Legacy Tables** (MCNP5 era):
```
M1  1001  2  8016  1
MT1  LWTR.01T                       $ 293K light water (old)

M2  1002  2  8016  1
MT2  HWTR.01T                       $ Heavy water (old)

M3  6000  1.0
MT3  GRPH.01T                       $ Graphite (old)

M4  4009  1.0
MT4  BE.01T                         $ Beryllium metal (old)
```

**Modern Tables** (MCNP6.2+):
```
M1  1001  2  8016  1
MT1  LWTR.20T                       $ Updated H in H2O kernel

M2  1002  2  8016  1
MT2  HWTR.20T                       $ Updated D in D2O kernel

M3  6000  1.0
MT3  GRPH.10T                       $ Updated graphite kernel

M4  4009  1.0
MT4  BE.30T                         $ Updated Be metal kernel
```

**Temperature Variants**:
```
c Available temperature suffixes:
MT1  LWTR.01T                       $ 293.6 K (room temp)
MT1  LWTR.02T                       $ 350 K
MT1  LWTR.03T                       $ 400 K
MT1  LWTR.04T                       $ 450 K
... (up to .16T for some materials)
```

**Key Points**:
- New kernels more accurate (especially at high temperature)
- Temperature suffix (.01T, .02T) must match TMP card
- Not all materials have updated kernels (check MCNP6 documentation)
- Results may differ (improved physics)

## Use Case 5: Batch Update Multiple Files

**Scenario**: Update 50 input files with same library change

**Strategy**:

**Step 1 - Create Update Script** (Python example):
```python
import re
import os

def update_input_file(filename):
    """Update MCNP input: .70c → .80c"""
    with open(filename, 'r') as f:
        content = f.read()

    # Backup original
    with open(filename + '.backup', 'w') as f:
        f.write(content)

    # Replace ZAIDs
    content = re.sub(r'\.70c', '.80c', content)

    # Replace thermal scattering
    content = re.sub(r'LWTR\.01T', 'LWTR.20T', content)
    content = re.sub(r'GRPH\.01T', 'GRPH.10T', content)

    # Write updated file
    with open(filename, 'w') as f:
        f.write(content)

    print(f"Updated: {filename}")

# Process all .i files in directory
for file in os.listdir('.'):
    if file.endswith('.i'):
        update_input_file(file)
```

**Step 2 - Test on Single File**:
```bash
# Test on one file first
python update_script.py model_01.i
mcnp6 inp=model_01.i outp=test.o
# Verify it works
```

**Step 3 - Batch Update**:
```bash
# Update all files
for file in *.i; do
    python update_script.py "$file"
done
```

**Step 4 - Validation Sample**:
```bash
# Run 5-10 representative cases
# Verify results reasonable
```

**Key Points**:
- Always backup originals
- Test script on single file first
- Validate sample of updated files (not all 50)
- Document changes in README

## Use Case 6: Add Mesh Tallies to Legacy Point Detectors

**Scenario**: Replace point detectors (F5) with mesh tallies (FMESH) for better spatial resolution

**Original** (Point detectors):
```
F5:N  100 0 0  0.5                  $ Single point
F15:N 200 0 0  0.5                  $ Another point
F25:N 300 0 0  0.5                  $ Third point
```

**Updated** (Mesh tally):
```
c --- Replace F5/F15/F25 with single mesh tally ---
FMESH4:N  GEOM=XYZ  ORIGIN=0 0 -50
          IMESH=350  IINTS=70      $ x: 0 to 350, 70 bins (5 cm)
          JMESH=50  JINTS=10       $ y: 0 to 50
          KMESH=50  KINTS=10       $ z: -50 to 50
          OUT=IJ                   $ Output format

c --- Original point detector locations now covered by mesh ---
c F5:  x=100 → FMESH bin 20
c F15: x=200 → FMESH bin 40
c F25: x=300 → FMESH bin 60
```

**Advantages**:
- Single tally instead of many point detectors
- Continuous spatial coverage
- Better variance (track-length vs point)
- Output to file for post-processing

**Key Points**:
- FMESH more efficient than many F5 detectors
- Choose bin size appropriate for geometry
- OUT=IJ produces compact output
- Post-processing required (meshtal file)

## Use Case 7: Standardize Input Format

**Scenario**: Make input file follow modern formatting standards

**Original** (Poor formatting):
```
1 1 -1.0 -1 IMP:N=1
2 0 1 IMP:N=0
1 SO 10
MODE N
M1 1001 2 8016 1
SDEF POS=0 0 0 ERG=14.1
F4:N 1
NPS 1000000
```

**Updated** (Standardized format):
```
Modern Water Sphere Model
c ==================================================
c DESCRIPTION:
c   Simple water sphere with 14.1 MeV source at center
c   Calculates flux in water cell
c ==================================================
c
c ==================================================
c CELL CARDS
c ==================================================
1   1   -1.0   -1         IMP:N=1  VOL=4188.79  $ Water sphere
2   0          1          IMP:N=0               $ Graveyard

c ==================================================
c SURFACE CARDS
c ==================================================
1   SO  10.0                                     $ Outer boundary

c ==================================================
c DATA CARDS
c ==================================================
c
c --- Physics ---
MODE  N
c
c --- Materials ---
M1   1001.80c  2  8016.80c  1                    $ Water (ENDF/B-VIII.0)
MT1  LWTR.20T                                    $ H in H2O thermal
c
c --- Source ---
SDEF  POS=0 0 0  ERG=14.1                        $ Point source, 14.1 MeV
c
c --- Tallies ---
F4:N  1                                          $ Volume-averaged flux
FC4   Neutron flux in water sphere
c
c --- Run Control ---
NPS  1000000                                     $ 1 million particles
c
c ==================================================
c END OF INPUT
c ==================================================
```

**Improvements**:
- Title block with description
- Section headers (cells, surfaces, data)
- Aligned columns
- Inline comments ($)
- Card-level comments (c)
- Consistent spacing
- Documentation

## Use Case 8: Update for Parallel Execution

**Scenario**: Add parallel execution cards to legacy input

**Original** (Serial execution):
```
[... geometry and data cards ...]
NPS  1e8                            $ Long serial run
```

**Updated** (Parallel execution):
```
[... geometry and data cards ...]

c --- Parallel Execution ---
c Use MPI tasks for parallelism
c Command line: mcnp6 inp=input.i tasks 16

c --- Checkpoint/Restart ---
PRDMP  J  J  1  J  J  J  J  2      $ Dump every 2 hours
c      ^nps ^mctal ^runtpe ^ptrac ^create_wait(hr)

NPS  1e8                            $ Run with 16 MPI tasks

c --- Command line usage ---
c mpirun -np 16 mcnp6 inp=input.i outp=output.o
```

**Key Points**:
- No INPUT file changes required (tasks on command line)
- PRDMP for checkpointing (avoid losing long runs)
- Typical scaling: 80-95% efficiency up to ~100 cores

## Common Errors and Troubleshooting

### Error 1: ZAID Not Found After Update

**Symptom**: Fatal error "ZAID xxxxx.80c not in xsdir"

**Cause**: ENDF/B-VIII.0 library not installed or xsdir not updated

**Fix**:
```
c Option 1: Verify library installation
c Check DATAPATH environment variable
c Ensure xsdir includes .80c libraries

c Option 2: Use .70c instead (if .80c unavailable)
M1  92235.70c  0.03  92238.70c  0.97

c Option 3: Use version-agnostic .00c
M1  92235.00c  0.03  92238.00c  0.97  $ Uses latest available
```

### Error 2: Thermal Scattering Table Mismatch

**Symptom**: Warning "MT table xxx not found" or wrong temperature

**Cause**: Updated ZAID but not MT table, or vice versa

**Example (Bad)**:
```
M1  1001.80c  2  8016.80c  1        $ Updated to .80c
MT1  LWTR.01T                       $ Still using old table (mismatch!)
```

**Fix**:
```
M1  1001.80c  2  8016.80c  1
MT1  LWTR.20T                       $ Match to .80c library
```

### Error 3: DBRC Card Syntax Error

**Symptom**: Fatal error "DBRC card ZAID not in material"

**Cause**: DBRC references wrong material or ZAID not present

**Example (Bad)**:
```
M1  92235.80c  0.03  92238.80c  0.97
DBRC2  92238                        $ Wrong! Material 2 doesn't exist
```

**Fix**:
```
M1  92235.80c  0.03  92238.80c  0.97
DBRC1  92238                        $ Correct: Material 1
```

### Error 4: Results Don't Match After Update

**Symptom**: Updated input gives different keff or tally results

**Diagnosis**:
```
c Expected differences:
c - Library update (.70c → .80c): Δkeff ~0.1-0.5% (normal)
c - Added DBRC: Δkeff ~+20-50 pcm (normal)
c - Format changes only: Δkeff ~0.001% (statistical)
```

**If difference too large** (>1%):
```
c Check:
c 1. Material definitions unchanged (densities, fractions)
c 2. Geometry unchanged
c 3. Source unchanged
c 4. No accidental card deletions
c 5. Thermal scattering tables updated correctly
```

**Validation**:
```
c Run old and new inputs with same NPS
c Compare:
c - keff ± 3σ should overlap
c - Tally results ± 3σ should overlap
```

### Error 5: Batch Update Script Corrupts Input

**Symptom**: Some updated files won't run, fatal errors

**Cause**: Regex too broad, replaced unwanted text

**Example (Bad Script)**:
```python
# Too aggressive - replaces .70 everywhere (including comments!)
content = content.replace('.70', '.80')
# Corrupts: "Using ENDF/B-VII.0" → "Using ENDF/B-VIII.0" (OK)
#           "Density: 1.70" → "Density: 1.80" (BAD!)
```

**Fix (Good Script)**:
```python
# Targeted replacement - only ZAID suffixes
content = re.sub(r'(\d{4,6})\.70c', r'\1.80c', content)
# Only matches: 92235.70c → 92235.80c
# Ignores: "1.70" (no trailing 'c')
```

### Error 6: PHYS Card Incompatibility

**Symptom**: MCNP6 warning about PHYS card format

**Cause**: MCNP5 PHYS card missing default parameters for MCNP6

**Example** (MCNP5 format):
```
PHYS:N  20                          $ MCNP5: only emax specified
```

**Fix** (MCNP6 format):
```
PHYS:N  20  J  J  J  J  J  J  J     $ MCNP6: add defaults
```

**Or** (Explicit):
```
PHYS:N  20  0  0  1  0  J  1  0     $ Specify all parameters
```

## Integration with Other Skills

### 1. **mcnp-input-validator**

Validator essential after updates to ensure correctness.

**Workflow**:
```
1. input-updater: Apply updates to input file
2. input-validator: Check syntax, cross-references
3. Fix any issues found
4. Repeat until validation passes
```

### 2. **mcnp-input-editor**

Editor provides tools for manual adjustments after batch updates.

**Pattern**:
```
1. input-updater: Batch changes (libraries, PHYS cards)
2. input-editor: Manual refinements (specific cards)
3. input-validator: Final validation
```

### 3. **mcnp-material-builder**

Material builder helps verify updated material definitions.

**Use Case**:
```
c After library update, verify material physics:
1. material-builder: Check atomic densities correct
2. material-builder: Verify thermal scattering appropriate
3. input-updater: Apply any corrections needed
```

### 4. **mcnp-output-parser**

Parser compares old vs new results for validation.

**Workflow**:
```
1. input-updater: Update input
2. Run old and new versions
3. output-parser: Extract keff, tallies from both
4. Compare statistically (3σ overlap)
5. Document differences
```

### 5. **mcnp-geometry-builder**

Geometry builder may be needed if update requires geometry changes.

**Example**:
```
c Adding FMESH may require adjusting geometry
1. input-updater: Plan mesh tally addition
2. geometry-builder: Verify mesh covers geometry
3. input-updater: Add FMESH card with correct extents
```

## Validation Checklist

After updating inputs:

- [ ] **Backup original**: Saved with .backup or .old extension
- [ ] **Version compatibility**: Runs in target MCNP version (test quickly)
- [ ] **Library consistency**:
  - [ ] All ZAIDs updated (no mix of .70c and .80c)
  - [ ] Thermal scattering tables match ZAID libraries
  - [ ] All materials have required libraries in xsdir
- [ ] **Syntax validation**:
  - [ ] No fatal errors
  - [ ] Warnings reviewed and understood
  - [ ] PHYS cards have all required parameters
- [ ] **Physics validation**:
  - [ ] Material densities unchanged
  - [ ] Geometry unchanged (unless intentional)
  - [ ] Source definition unchanged
- [ ] **Results comparison** (old vs new):
  - [ ] keff within 3σ (if criticality)
  - [ ] Tally results within 3σ
  - [ ] Differences documented and understood
  - [ ] Large differences (>1%) investigated
- [ ] **New features** (if added):
  - [ ] DBRC applied correctly (only relevant isotopes)
  - [ ] FMESH covers intended region
  - [ ] WWG tested and improves FOM
- [ ] **Documentation**:
  - [ ] Changes documented in input comments
  - [ ] Validation results recorded
  - [ ] Differences from original noted

## Advanced Topics

### 1. Automated Testing Framework

**Concept**: Systematically validate updates across test suite

**Framework**:
```python
import subprocess
import json

class MCNPTestSuite:
    def __init__(self, test_cases):
        self.test_cases = test_cases  # List of input files

    def run_test(self, input_file):
        """Run MCNP and extract keff"""
        result = subprocess.run(
            ['mcnp6', f'inp={input_file}', 'outp=test.o'],
            capture_output=True
        )
        # Parse output for keff, tallies
        keff = self.extract_keff('test.o')
        return keff

    def validate_update(self, original, updated):
        """Compare original vs updated results"""
        keff_old = self.run_test(original)
        keff_updated = self.run_test(updated)

        diff = abs(keff_old['mean'] - keff_updated['mean'])
        sigma_combined = (keff_old['sigma']**2 + keff_updated['sigma']**2)**0.5

        if diff < 3 * sigma_combined:
            return "PASS"
        else:
            return "FAIL: difference too large"

# Usage
suite = MCNPTestSuite(['test1.i', 'test2.i', 'test3.i'])
results = suite.validate_update('original.i', 'updated.i')
```

### 2. Version Control Integration

**Best Practice**: Track updates with git

```bash
# Initialize repo
git init
git add *.i
git commit -m "Original MCNP5 inputs"

# Create update branch
git checkout -b endf-viii-update

# Apply updates
python update_script.py *.i

# Review changes
git diff

# Commit updates
git add *.i
git commit -m "Update libraries: ENDF/B-VII.0 → VIII.0"

# Tag validated version
git tag -a v2.0-endf8 -m "Validated with ENDF/B-VIII.0"
```

### 3. Regression Testing

**Strategy**: Maintain reference results for comparison

**Directory Structure**:
```
project/
├── inputs/
│   ├── model_01.i
│   ├── model_02.i
│   └── ...
├── reference/
│   ├── model_01_ref.o       # Known good results
│   ├── model_02_ref.o
│   └── ...
├── scripts/
│   ├── update.py
│   └── validate.py
└── results/
    └── validation_report.txt
```

**Validation Script**:
```python
def compare_to_reference(output_file, reference_file):
    """Compare current results to reference"""
    results_current = extract_results(output_file)
    results_ref = extract_results(reference_file)

    for key in results_ref:
        diff = abs(results_current[key] - results_ref[key])
        if diff > TOLERANCE:
            print(f"FAIL: {key} differs by {diff}")
        else:
            print(f"PASS: {key}")
```

### 4. Library Availability Check

**Problem**: Not all ENDF/B-VIII.0 ZAIDs exist

**Solution**: Check xsdir before updating

```python
def check_zaid_available(zaid, xsdir_path='/path/to/xsdir'):
    """Check if ZAID exists in xsdir"""
    with open(xsdir_path) as f:
        xsdir_content = f.read()
    return zaid in xsdir_content

# Before updating:
if check_zaid_available('92235.80c'):
    # Update to .80c
else:
    # Keep .70c or use .00c
```

## Quick Reference: Common Update Patterns

| Update Type | Find Pattern | Replace Pattern | Notes |
|-------------|--------------|-----------------|-------|
| Library VII→VIII | `\.70c` | `.80c` | All neutron data |
| Thermal H2O | `LWTR\.01T` | `LWTR.20T` | Light water |
| Thermal graphite | `GRPH\.01T` | `GRPH.10T` | Carbon |
| Add DBRC | (after M card) | `DBRC1  92238` | Material 1, U-238 |
| PHYS defaults | `PHYS:N  100` | `PHYS:N  100  J  J  J  J  J  J  J` | MCNP6 format |
| Version-agnostic | `\.80c` | `.00c` | Latest library |

## Best Practices

1. **Always Backup**: Never update without saving original
   ```bash
   cp input.i input.i.backup_$(date +%Y%m%d)
   ```

2. **Test Small First**: Single file before batch update
   ```bash
   # Test one file, verify it works
   # Then batch update
   ```

3. **Document Changes**: In input file comments
   ```
   c ==================================================
   c UPDATE HISTORY:
   c 2024-01-15: Updated ENDF/B-VII.0 → VIII.0 (JDoe)
   c 2024-01-20: Added DBRC for U-238 (JDoe)
   c ==================================================
   ```

4. **Validate Statistically**: Compare with 3σ criterion
   ```
   Δ < 3 × √(σ₁² + σ₂²)  → PASS
   ```

5. **Incremental Updates**: One change type at a time
   ```
   Step 1: Update libraries only
   Step 2: Validate
   Step 3: Add DBRC
   Step 4: Validate
   ```

6. **Version Control**: Track all changes
   ```bash
   git commit -m "Descriptive message"
   ```

7. **Keep Notes**: Record validation results
   ```
   Validation Results:
   - Original keff: 1.00523 ± 0.00015
   - Updated keff:  1.00531 ± 0.00014
   - Difference: 8 pcm (within 3σ) ✓
   ```

8. **Automate When Possible**: Scripts for repetitive tasks
   ```python
   # update_library.py
   # Run on all inputs consistently
   ```

9. **Check Library Availability**: Before committing to .80c
   ```bash
   grep "92235.80c" $DATAPATH/xsdir
   ```

10. **Plan for Rollback**: Keep working originals accessible
    ```
    inputs_v1.0/  ← Original working versions
    inputs_v2.0/  ← Updated versions
    ```

11. **Programmatic Input Updating**:
    - For automated input file updates and batch processing, see: `mcnp_input_updater.py`
    - Useful for systematic library updates, batch card replacements, and version migration workflows

## References

- **Documentation Summary**: `CATEGORIES_AB_DOCUMENTATION_SUMMARY.md`
  - Section 7: Material Data Cards (library identifiers)
  - Section 8: Physics Data Cards (PHYS, DBRC)
- **Related Skills**:
  - mcnp-input-editor (manual editing after updates)
  - mcnp-input-validator (validation of updated inputs)
  - mcnp-material-builder (material verification)
  - mcnp-output-parser (results comparison)
- **User Manual**:
  - Appendix F: ENDF/B Libraries and Availability
  - Chapter 5.6: Material Cards (M, MT, DBRC)
  - Release Notes: MCNP6 vs MCNP5 differences
- **External Resources**:
  - MCNP6 Release Notes (version differences)
  - ENDF/B-VIII.0 Release Documentation
  - xsdir file (library availability)

---

**End of MCNP Input Updater Skill**

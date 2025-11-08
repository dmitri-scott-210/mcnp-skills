# MCNP Input Templates

This directory contains template input files for common MCNP problem types. Templates use placeholder values marked with `<...>` that should be replaced with actual parameters.

## Available Templates

### 1. basic_fixed_source_template.i
**Purpose:** Simple fixed-source problems with sphere geometry

**Use When:**
- Learning MCNP basics
- Testing simple configurations
- Quick flux calculations
- Single-region problems

**Key Features:**
- Spherical geometry (1 active cell + graveyard)
- Point source at center
- F4 volume flux tally
- Optional F2 surface flux and F5 point detector

**Typical Applications:**
- Water activation studies
- Simple shielding estimates
- Material testing

---

### 2. kcode_criticality_template.i
**Purpose:** Criticality calculations using KCODE

**Use When:**
- Calculating k-effective
- Fissile system analysis
- Reactor physics studies
- Criticality safety

**Key Features:**
- KCODE card (replaces SDEF + NPS)
- KSRC starting source positions
- Fissile material (U-235, Pu-239, etc.)
- Typical parameter guidance (Nsrc, Nskip, Ntotal)

**Typical Applications:**
- Bare metal critical mass
- Moderated systems
- Fuel assemblies

---

### 3. shielding_template.i
**Purpose:** Multi-layer shielding with variance reduction

**Use When:**
- Deep penetration problems
- Multi-material shields
- Dose calculations behind shields
- Radiation protection

**Key Features:**
- 3 shield layers (expandable)
- Source void + detector region
- Importance cards (variance reduction)
- Multiple tallies (flux in each layer)
- CTME time limit for long runs

**Typical Applications:**
- Concrete/steel/poly composite shields
- Reactor shielding
- Spent fuel cask analysis

---

### 4. detector_template.i
**Purpose:** Source-detector geometry with F5 point detector

**Use When:**
- Detector response calculations
- Flux at specific locations
- Angular distributions
- Inverse square law verification

**Key Features:**
- F5 point detector tally (next-event estimator)
- Exclusion radius for accuracy
- Optional scattering medium
- Optional ring detectors for angular dependence

**Typical Applications:**
- Detector calibration
- Measurement geometry modeling
- Gamma spectroscopy

---

## How to Use Templates

### Step 1: Copy Template
```bash
cp basic_fixed_source_template.i my_problem.i
```

### Step 2: Replace Placeholders
Search for `<...>` markers and replace with actual values:

**Example:**
```
Before: 1    <mat#>  <density>  -1      IMP:N=1
After:  1    1       -1.0       -1      IMP:N=1
```

### Step 3: Customize
- Add/remove optional cards as needed
- Adjust geometry for your problem
- Add more materials if needed
- Modify tallies for quantities of interest

### Step 4: Validate
```bash
# Check input structure
python ../../scripts/validate_input_structure.py my_problem.i

# Plot geometry
mcnp6 inp=my_problem.i ip
```

### Step 5: Run
```bash
mcnp6 inp=my_problem.i outp=my_problem.o
```

---

## Common Placeholder Meanings

| Placeholder | Meaning | Example Values |
|-------------|---------|----------------|
| `<mat#>` | Material number | 1, 2, 3, ... |
| `<density>` | Material density | 1.0 (g/cm³), -0.1 (atoms/barn-cm) |
| `<radius>` | Sphere radius | 10.0 (10 cm) |
| `<ZAID>` | Isotope identifier | 1001 (H-1), 8016 (O-16), 92235 (U-235) |
| `<fraction>` | Atomic fraction | 2, 1 (for H2O) |
| `<energy>` | Particle energy | 14.1 (14.1 MeV), 1.0 (1 MeV) |
| `<histories>` | Number of particles | 1000000 (10^6), 10000000 (10^7) |
| `<x> <y> <z>` | Coordinates | 0 0 0 (origin), 100 0 0 (x=100 cm) |

---

## Template Modification Tips

### Changing Geometry
- **From sphere to cylinder:** Replace `SO` with `CZ` (infinite cylinder) or `RCC` (finite)
- **Adding regions:** Add cell cards with new materials, update surface cards
- **Complex geometry:** Consider using mcnp-geometry-builder skill

### Adding Materials
```
M1   1001  2  8016  1    $ Water
M2   26000  1.0          $ Iron
M3   82000  1.0          $ Lead
```

### Multiple Tallies
```
F4:N  1                  $ Flux in cell 1
F14:N  2                 $ Flux in cell 2 (note: 14, not 5)
F24:N  3                 $ Flux in cell 3 (note: 24, not 6)
```

### Energy Distribution Source
```
SDEF  POS=0 0 0  ERG=D1
SI1   H  0.01 0.1 1 10   $ Energy bins (MeV)
SP1   D  0.1 0.3 0.4 0.2 $ Probabilities (must sum to 1.0)
```

---

## Validation Before Running

**Always check:**
1. ✅ Three blank lines (after cells, after surfaces, at EOF)
2. ✅ MODE card is first data card
3. ✅ All materials referenced in cells are defined
4. ✅ All surfaces referenced in cells are defined
5. ✅ Particle designators present (`:N`, `:P`, etc.)
6. ✅ Source in cell with IMP>0
7. ✅ Graveyard cell with IMP=0

**Use validator script:**
```bash
python ../../scripts/validate_input_structure.py my_problem.i
```

---

## Further Help

- **Skill:** mcnp-input-builder - Complete input file creation guide
- **Skill:** mcnp-geometry-builder - Complex geometry construction
- **Skill:** mcnp-material-builder - Material definitions
- **Skill:** mcnp-source-builder - Source specifications
- **Skill:** mcnp-tally-builder - Tally setup

---

**See also:**
- `../example_inputs/` - Real example files from basic_examples/
- `../../references/` - Detailed format specifications
- `../../scripts/` - Automation tools

---

**Last Updated:** 2025-11-02 (Session 6 - Skill Revamp)

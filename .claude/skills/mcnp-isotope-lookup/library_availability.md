# MCNP Cross-Section Library Availability

## Overview

This guide provides comprehensive information on MCNP cross-section library availability, version selection, temperature-dependent libraries, and procedures for verifying isotope availability in the xsdir file. Proper library selection is critical for accurate MCNP simulations.

## ENDF/B Library Versions

### Major Releases

**ENDF/B-VIII.0 (2018)** - Latest Release:
```
Library suffix: .80c (continuous energy neutrons)

Key improvements:
  - Updated evaluations for major actinides (U, Pu)
  - Improved fission product data
  - Better thermal scattering treatments
  - Enhanced resonance region accuracy

Recommended for:
  - All new calculations
  - Research and development
  - High-precision criticality
  - Modern reactor designs

Availability:
  - Most isotopes have .80c evaluations
  - Limited isotopes may require .70c fallback
```

**ENDF/B-VII.0 (2006)**:
```
Library suffix: .70c

Status:
  - Mature, well-validated
  - Extensive benchmark database
  - Broad isotope coverage

Recommended for:
  - Benchmark comparisons
  - Validation studies
  - When .80c not available

Availability:
  - Very broad coverage (~400 isotopes)
  - Most fission products available
```

**ENDF/B-VI.8 (2001)**:
```
Library suffix: .68c (less common)

Status: Legacy, rarely used in new work
```

**ENDF/B-VI.6 (1998)**:
```
Library suffix: .66c

Status:
  - Legacy, but still available
  - Historical benchmark comparisons

Use when:
  - Reproducing historical calculations
  - Specific validation requirements
```

### Library Selection Guidelines

```
Decision tree:
1. Try .80c first (most recent)
2. If not available, use .70c (mature, validated)
3. If not available, use .66c (legacy)
4. If none available, consider:
   - Natural element mix (ZZZ000)
   - Nearby isotope approximation
   - NJOY processing (advanced users)
```

## Temperature-Dependent Libraries

### Standard Temperature Libraries

Cross-section data is evaluated at specific temperatures. MCNP provides multiple temperature libraries to minimize interpolation errors.

**Standard Temperature Points**:
```
Library  Temperature    Use Case
.80c     293.6 K        Room temperature, cold systems
.81c     600 K          Moderate temperature reactors
.82c     900 K          High temperature reactors
.83c     1200 K         Very high temperature systems
.84c     2500 K         Ultra-high temperature (gas reactors)
```

**Extended Temperature Libraries** (selected isotopes):
```
.85c     523.6 K        (250°C)
.86c     573.6 K        (300°C)
.87c     623.6 K        (350°C)
.88c     ...            (additional as available)
```

### Temperature Selection Guidelines

```
System Temperature Range    Recommended Library
───────────────────────    ───────────────────
T < 400 K                  .80c + TMP card
400 K ≤ T < 800 K          .81c (or .80c + TMP)
800 K ≤ T < 1100 K         .82c
1100 K ≤ T < 1800 K        .83c
T ≥ 1800 K                 .84c

General rule:
  - Select library closest to system temperature
  - Use TMP card for exact temperature
  - MCNP interpolates between library temperatures
```

### TMP Card Usage

**Without TMP Card**:
```
M1  92235.82c  1.0       $ Uses 900 K cross sections (fixed)
```

**With TMP Card** (interpolation):
```
M1  92235.80c  1.0       $ Base library at 293.6 K
TMP  600                 $ MCNP interpolates to 600 K

M2  92235.82c  1.0       $ Base library at 900 K
TMP  1000                $ MCNP interpolates to 1000 K
```

**Best Practice**:
```
Choose library close to system temperature:

Good:
  M1  92235.82c  1.0     $ 900 K library
  TMP  950               $ Interpolate to 950 K (50 K away)

Less optimal:
  M1  92235.80c  1.0     $ 293.6 K library
  TMP  950               $ Interpolate to 950 K (656 K away)
```

### Temperature Effects

**Doppler Broadening**:
- Higher temperature → broader resonances
- Critical for U-238 resonances around 6.67 eV
- Affects reactivity feedback (Doppler coefficient)
- Important for criticality safety

**Impact on keff**:
```
Example (U-238 temperature effects):
  T = 300 K  → keff ≈ 1.000
  T = 900 K  → keff ≈ 0.995  (negative Doppler feedback)

Magnitude: ~100-1000 pcm for 600 K change
```

## Thermal Scattering Libraries (S(α,β))

### Purpose and Importance

For bound atoms at thermal energies (E < ~4 eV), free-atom approximations fail. Thermal scattering libraries provide molecular/crystalline binding effects.

**Physical Effects**:
- Chemical binding (H in H₂O vs. free H)
- Crystal lattice effects (C in graphite)
- Molecular rotations and vibrations
- Coherent scattering (Bragg peaks)

### Common Thermal Scattering Libraries

**Water (H₂O)**:
```
Light water:
  lwtr.80t  → 293.6 K (20.44°C)
  lwtr.81t  → 323.6 K (50.44°C)
  lwtr.82t  → 373.6 K (100.44°C)
  lwtr.83t  → 423.6 K (150.44°C)
  lwtr.84t  → 473.6 K (200.44°C)
  lwtr.85t  → 523.6 K (250.44°C)
  lwtr.86t  → 573.6 K (300.44°C)
  lwtr.87t  → 623.6 K (350.44°C)

Heavy water:
  hwtr.80t  → 293.6 K
  hwtr.81t  → 323.6 K
  (similar temperature series)
```

**Solid Moderators**:
```
Graphite:
  grph.80t  → 293.6 K (reactor grade graphite)
  graph.80t → 293.6 K (alternate name)
  grph.82t  → Higher temperature graphite

Beryllium metal:
  be.80t    → 293.6 K
  be.82t    → Higher temperature

Beryllium oxide:
  beo.80t   → 293.6 K
```

**Hydrides** (reactor materials):
```
Zirconium hydride:
  zrzh.80t  → ZrH₁.₆ to ZrH₂ (TRIGA fuel)
  zrh.80t   → Alternate name

Yttrium hydride:
  yzh.80t   → YH₁.₆ to YH₂
```

**Organic Materials**:
```
Polyethylene:
  poly.80t  → (CH₂)n polymer

Benzene:
  benz.80t  → C₆H₆ (liquid)

Lucite/PMMA:
  lucite.80t → (C₅H₈O₂)n
```

**Ice and Special Cases**:
```
Ice:
  ice.80t   → Solid H₂O (hexagonal)

Liquid methane:
  lmeth.80t → CH₄ (liquid)

Solid methane:
  smeth.80t → CH₄ (solid)
```

### MCNP MT Card Syntax

**Basic Usage**:
```
M1   1001.80c  2.0      $ Hydrogen
     8016.80c  1.0      $ Oxygen
MT1  lwtr.80t           $ S(α,β) for material M1
```

**Important Rules**:
- MT number MUST match M number (M1 → MT1, M2 → MT2)
- Thermal scattering applies to entire material
- Only affects thermal/epithermal neutrons (typically E < 4 eV)
- Multiple materials can have different thermal treatments

**Complete Example**:
```
c PWR fuel pin unit cell
c
c Fuel (UO₂ at 900 K)
M1  92235.82c  0.045    $ U-235 (4.5% enriched)
    92238.82c  0.955    $ U-238
    8016.82c   2.0      $ Oxygen
c
c Clad (Zircaloy at 600 K)
M2  40000.81c  1.0      $ Zirconium alloy
c
c Moderator (H₂O at 580 K)
M3  1001.80c   2.0      $ Hydrogen in water
    8016.80c   1.0      $ Oxygen
MT3 lwtr.86t            $ S(α,β) at 573.6 K (closest to 580 K)
TMP  580                $ Exact temperature
```

### When Thermal Scattering is Critical

**REQUIRED** (results significantly affected):
- Thermal reactor keff calculations (error >1000 pcm without)
- Critical assembly benchmarks (thermal spectrum)
- Accurate flux distributions in thermal systems
- Reactivity coefficient predictions

**IMPORTANT** (accuracy improved):
- Mixed spectrum reactors
- Neutron shielding with thermal component
- Activation calculations (thermal flux)
- Neutron dose calculations

**OPTIONAL** (small effect):
- Fast reactors (hard spectrum, E > 100 keV)
- High-energy shielding (MeV neutrons)
- Quick scoping calculations

**Effect Magnitude**:
```
Thermal reactor keff without S(α,β):
  Error: +500 to +2000 pcm (too high)
  Spectrum: Significantly distorted
  Reaction rates: 10-50% error in thermal region
```

## Cross-Section Library Files

### xsdir File

The `xsdir` (cross-section directory) file is the master index of all available nuclear data.

**Location**:
```
Typical paths:
  Unix/Linux: $DATAPATH/xsdir
  Windows: %DATAPATH%\xsdir

Environment variable:
  export DATAPATH=/path/to/mcnp/data
  set DATAPATH=C:\MCNP\data
```

**xsdir Entry Format**:
```
ZAID  aw  filename  access  filetype  NXS(3)  NXS(5)  length  ...

Example:
92235.80c 235.04393 endf80/U/92235.800nc 0 1 4687 0 0 2.53e-08
│         │         │                     │ │ │    │ │ │
│         │         │                     │ │ │    │ │ └─ Thermal energy (eV)
│         │         │                     │ │ │    │ └─ Zero temperature
│         │         │                     │ │ │    └─ Zero atomic displacement
│         │         │                     │ │ └─ Number of energy points
│         │         │                     │ └─ File type (1=ACE)
│         │         │                     └─ Access route (0=default)
│         │         └─ Data file path (relative to DATAPATH)
│         └─ Atomic weight (amu)
└─ ZAID identifier
```

**xsdir Sections**:
```
directory
  atomic weight library
  <ZAID entries for continuous energy neutron>

thermal
  <thermal scattering library entries>

photoatomic
  <photon interaction data>

photoelectron
  <electron data>
```

### Checking Library Availability

**Method 1: grep Command** (Linux/Mac):
```bash
# Check specific isotope
grep "92235.80c" $DATAPATH/xsdir

# Check all uranium isotopes in .80c
grep "92[0-9][0-9][0-9].80c" $DATAPATH/xsdir

# Check thermal scattering libraries
grep "\.80t" $DATAPATH/xsdir

# Check all plutonium isotopes
grep "94[0-9][0-9][0-9]\.80c" $DATAPATH/xsdir

# Count available isotopes
grep "\.80c" $DATAPATH/xsdir | wc -l
```

**Method 2: findstr Command** (Windows):
```cmd
REM Check specific isotope
findstr "92235.80c" %DATAPATH%\xsdir

REM Check all uranium isotopes
findstr /R "92[0-9][0-9][0-9].80c" %DATAPATH%\xsdir
```

**Method 3: Python Script**:
```python
def check_library_availability(zaid, datapath):
    """Check if ZAID available in xsdir"""
    import os

    xsdir_path = os.path.join(datapath, 'xsdir')

    if not os.path.exists(xsdir_path):
        return False, "xsdir file not found"

    with open(xsdir_path, 'r') as f:
        for line in f:
            if line.startswith(zaid):
                # Parse atomic weight and filename
                parts = line.split()
                aw = float(parts[1])
                filename = parts[2]
                return True, f"Available: aw={aw}, file={filename}"

    return False, "ZAID not found in xsdir"

# Example usage
available, info = check_library_availability('92235.80c', '/path/to/data')
print(f"U-235: {info}")
```

**Method 4: MCNP Test Run**:
```
Create minimal input with desired ZAID:
  Test ZAID availability
  M1  95241.80c  1.0    $ Am-241
  c (rest of minimal geometry)

Run MCNP:
  - If runs: ZAID available
  - If fatal error "nuclide not found": Not available
```

### Handling Missing Isotopes

**Option 1: Use Natural Element**:
```
Specific isotope not available:
  95255.80c → NOT FOUND

Try natural element:
  95000.80c → Use if available
```

**Option 2: Use Different Library Version**:
```
Try in order:
  1. 95241.80c (ENDF/B-VIII.0)
  2. 95241.70c (ENDF/B-VII.0)
  3. 95241.66c (ENDF/B-VI.6)
```

**Option 3: Use Nearby Isotope** (approximation):
```
If 93238 not available, consider:
  93237.80c (Np-237) - nearby mass number

WARNING: Only for scoping; not for production
Document assumption clearly
```

**Option 4: NJOY Processing** (advanced):
```
Process ENDF evaluation with NJOY:
  1. Obtain ENDF file from NNDC
  2. Run NJOY to generate ACE file
  3. Add entry to xsdir
  4. Verify with MCNP test

Requires:
  - NJOY expertise
  - Quality assurance
  - Validation testing
```

## Library Coverage by Element Group

### Excellent Coverage (>95% isotopes)

```
- Light elements (H, C, N, O)
- Structural materials (Fe, Ni, Cr, Zr)
- Shielding materials (Pb, W, U)
- Major actinides (U, Pu, Am, Cm)
- Common fission products
```

### Good Coverage (>75% isotopes)

```
- Transition metals
- Lanthanides (rare earths)
- Most stable isotopes
```

### Limited Coverage

```
- Very short-lived isotopes (t₁/₂ < 1 day)
- Very heavy elements (Z > 100)
- Some exotic isotopes
```

### Isotope-Specific Notes

**Always Available**:
```
1001.80c  (H-1)
6000.80c  (natural C)
8016.80c  (O-16)
26000.80c (natural Fe)
92235.80c (U-235)
92238.80c (U-238)
94239.80c (Pu-239)
```

**Often Missing**:
```
Very heavy elements (Z > 99)
Short-lived fission products
Exotic metastable states
Some lanthanides (individual isotopes)
```

## Library Installation and Management

### Verifying Installation

**Check DATAPATH**:
```bash
# Linux/Mac
echo $DATAPATH
ls -lh $DATAPATH/xsdir

# Windows
echo %DATAPATH%
dir %DATAPATH%\xsdir
```

**List Library Files**:
```bash
# Find all ACE files
find $DATAPATH -name "*.??nc" | head -20

# Check library size
du -sh $DATAPATH
```

### Library Updates

**When to Update**:
- New ENDF/B release available
- Improved evaluations for key isotopes
- Bug fixes in specific evaluations
- Need for new isotopes

**Update Procedure**:
1. Download new library from LANL or OECD/NEA
2. Install to separate directory (keep old version)
3. Update DATAPATH environment variable
4. Run validation suite
5. Compare critical benchmarks
6. Switch production calculations

### Multiple Library Versions

**Maintain Multiple Versions**:
```bash
# Directory structure
/data/mcnp/
  ├─ endfb80/  (ENDF/B-VIII.0)
  ├─ endfb70/  (ENDF/B-VII.0)
  └─ xsdir_master

# Switch with environment variable
export DATAPATH=/data/mcnp/endfb80
export DATAPATH=/data/mcnp/endfb70
```

**xsdir Merging** (advanced):
```
Combine multiple library versions:
  - Use .80c where available
  - Fall back to .70c for missing isotopes
  - Custom xsdir file with mixed entries

WARNING: Requires careful validation
```

## Best Practices

### 1. Always Verify Library Availability

```bash
# Before running production calculation
grep "92235.80c" $DATAPATH/xsdir
grep "94239.80c" $DATAPATH/xsdir
# ... check all isotopes
```

### 2. Use Consistent Library Version

```
Good:
  M1  92235.80c  1.0
  M2  94239.80c  1.0
  M3  8016.80c   1.0

Bad (mixing versions):
  M1  92235.80c  1.0
  M2  94239.70c  1.0    ← Different version
```

### 3. Document Library Choices

```
c MCNP6 Input - PWR Core
c Cross sections: ENDF/B-VIII.0 (.80c)
c Thermal scattering: lwtr.87t (623.6 K)
c Date: 2024-11-06
c
M1  92235.80c  0.045    $ U-235
```

### 4. Match Temperature Libraries

```
c High-temperature system (900 K)
M1  92235.82c  1.0      $ Use .82c (900 K library)
M2  8016.82c   2.0      $ Consistent temperature
TMP  900                $ System temperature
```

### 5. Include Thermal Scattering

```
c Always include S(α,β) for thermal systems
M1  1001.80c  2.0       $ H in H₂O
    8016.80c  1.0       $ O
MT1 lwtr.80t            $ REQUIRED for accuracy
```

### 6. Test Before Production

```
Run quick test:
  - Verify all ZAIDs found
  - Check for warnings
  - Validate keff in expected range
  - Review cross-section plots
```

## Troubleshooting

### Error: "nuclide ZAID not found"

**Cause**: Requested ZAID not in xsdir

**Solution**:
1. Check xsdir: `grep "ZAID" $DATAPATH/xsdir`
2. Try different library version (.70c, .66c)
3. Try natural element (ZZZ000)
4. Check DATAPATH environment variable

### Warning: "interpolating to temperature"

**Cause**: TMP card temperature differs from library

**Action**:
- Usually acceptable (MCNP interpolates)
- For high accuracy, use library close to temperature
- Check if interpolation range is reasonable

### Error: "thermal scattering library not found"

**Cause**: MT card references missing .??t file

**Solution**:
1. Check xsdir thermal section: `grep "lwtr.80t" $DATAPATH/xsdir`
2. Verify thermal library installation
3. Check MT card syntax (MT1 matches M1)

## References

**MCNP Documentation**:
- MCNP6 User Manual, Appendix G (Cross-Section Libraries)
- LA-UR-17-29981 (MCNP6.2 Release Notes)

**Nuclear Data Sources**:
- ENDF/B-VIII.0: https://www.nndc.bnl.gov/endf-b8.0/
- OECD/NEA Data Bank: https://www.oecd-nea.org/
- LANL Nuclear Data: https://nucleardata.lanl.gov/

**Related Documentation**:
- NJOY2016 Manual (cross-section processing)
- ACE Format Specification (LA-UR-02-3538)

---

**For ZAID format details, see `zaid_format_guide.md`**
**For isotope properties, see `isotope_database.md`**
**For decay data, see `decay_data.md`**

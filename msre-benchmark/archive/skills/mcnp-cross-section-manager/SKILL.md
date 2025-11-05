---
category: F
name: mcnp-cross-section-manager
description: Manage and verify MCNP cross-section libraries including checking xsdir availability, diagnosing library errors, finding alternatives for missing data, and understanding library versions and types
activation_keywords:
  - cross section library
  - xsdir
  - library not found
  - missing cross section
  - ZAID not available
  - library error
  - data path
  - cross section data
---

# MCNP Cross-Section Manager Skill

## Purpose

This utility skill helps Claude manage MCNP cross-section libraries by verifying data availability, diagnosing library errors, suggesting alternatives for missing isotopes, and ensuring proper library configuration. Essential for preventing runtime errors and optimizing data usage.

## When to Use This Skill

- Verifying cross-section library availability before running MCNP
- Diagnosing "cross-section table not found" errors
- Finding alternative libraries when primary choice unavailable
- Checking xsdir file for specific ZAIDs
- Understanding library types (.c, .t, .p, .e) and when to use each
- Managing multiple ENDF/B versions (.80c, .70c, .66c)
- Troubleshooting DATAPATH environment variable issues
- Identifying temperature-dependent library availability
- Recommending natural element mix when isotope unavailable
- Optimizing library selection for performance

## Prerequisites

- **mcnp-isotope-lookup**: Provides ZAID identification
- **mcnp-material-builder**: Uses verified cross sections
- **mcnp-physics-builder**: Uses thermal scattering libraries
- Understanding of ZAID format (ZZZAAA.nnX)
- Basic knowledge of ENDF/B library versions
- Familiarity with MCNP error messages

## Core Concepts

### xsdir File Structure

**Purpose**: Index file listing all available cross-section libraries

**Location**:
```
Environment variable: $DATAPATH or %DATAPATH%
Typical paths:
  Linux: /path/to/mcnpdata/xsdir
  Windows: C:\mcnp\data\xsdir

MCNP searches for xsdir in:
  1. Path specified by DATAPATH environment variable
  2. Current working directory
  3. Default installation directory
```

**xsdir Entry Format**:
```
ZAID  AWR  filename  access  file_length  record_length  entries  temperature  ...

Example:
1001.80c  0.999167  endf80/H/1001.800c  0  1  1  4553  2.5301E-08

Fields:
  ZAID: 1001.80c (H-1 with ENDF/B-VIII.0)
  AWR: 0.999167 (atomic weight ratio relative to neutron)
  filename: endf80/H/1001.800c (relative to DATAPATH)
  access: 0 (direct access)
  file_length: 1 (number of records)
  record_length: 1 (length of each record)
  entries: 4553 (number of entries in table)
  temperature: 2.5301E-08 MeV (= 293.6 K)
```

### Library Type Suffixes

**Continuous Energy (.c)**:
```
.80c → ENDF/B-VIII.0 (most recent, recommended)
.70c → ENDF/B-VII.0
.66c → ENDF/B-VI.6
.60c → ENDF/B-VI.0

Coverage: Neutron cross sections with full energy resolution
Use for: All general-purpose calculations
```

**Thermal Scattering (.t)**:
```
lwtr.80t → Light water (H₂O) thermal scattering
hwtr.80t → Heavy water (D₂O)
grph.80t → Graphite
poly.80t → Polyethylene
be.80t   → Beryllium metal
beo.80t  → Beryllium oxide

Use: With MT card for bound thermal scattering (E < 4 eV)
Required: Accurate thermal neutron transport in moderators
```

**Photoatomic (.p)**:
```
1000.80p → Hydrogen photoatomic
6000.80p → Carbon photoatomic
82000.80p → Lead photoatomic

Coverage: Photon interaction cross sections
Use for: MODE P or MODE N P calculations
```

**Electron (.e)**:
```
1000.80e → Hydrogen electron
6000.80e → Carbon electron
82000.80e → Lead electron

Coverage: Electron interaction cross sections
Use for: MODE E calculations (coupled electron-photon)
```

**Discrete Reaction (.d)**:
```
Not commonly used in modern MCNP
Legacy format for specific reactions
```

### Temperature-Dependent Libraries

**Neutron Library Temperatures**:
```
.80c → 293.6 K (20.45°C, room temperature)
.81c → 600 K (327°C)
.82c → 900 K (627°C)
.83c → 1200 K (927°C)
.84c → 2500 K (2227°C)

Not all isotopes available at all temperatures!

Common availability:
  - Structural materials: .80c to .84c
  - Fissile isotopes (U-235, Pu-239): Full temperature range
  - Minor actinides: Often only .80c available
  - Fission products: Limited temperature coverage
```

**Interpolation with TMP Card**:
```
When exact temperature library unavailable:
  - Use closest library (e.g., .80c for 400 K)
  - Add TMP card for interpolation
  - MCNP interpolates cross sections to specified temp

Example:
  M1  92235.80c  1.0    $ Use 293.6 K library
  TMP  600               $ MCNP interpolates to 600 K

Limitation: Interpolation less accurate than native library
```

### Common Library Errors

**Error 1: "cross-section table (ZAID) not found"**
```
Cause: Library not in xsdir or file missing
Solution: Check xsdir, verify DATAPATH, use alternative
```

**Error 2: "cannot open file (filename)"**
```
Cause: Data file missing or incorrect path
Solution: Verify file exists, check file permissions
```

**Error 3: "atomic weight ratio (AWR) is zero"**
```
Cause: Corrupted xsdir entry
Solution: Regenerate xsdir or repair entry
```

**Error 4: "temperature (T) out of range"**
```
Cause: TMP value incompatible with available libraries
Solution: Use appropriate library or adjust TMP
```

## Decision Tree: Cross-Section Library Selection

```
START: Need cross-section library for isotope
  |
  +--> Check if library available
  |      ├─> Search xsdir: grep "ZAID" xsdir
  |      ├─> Found?
  |      │   ├─> Yes: Verify file exists → Use library
  |      │   └─> No: Go to alternatives
  |      |
  |      └─> Alternatives when not found:
  |            ├─> Use natural element (ZZZ000.nnc)
  |            ├─> Use different ENDF version (.70c vs .80c)
  |            ├─> Use similar isotope (e.g., Np-238 → Np-237)
  |            └─> Request library if critical
  |
  +--> Select library version
  |      ├─> .80c available? → Use (most recent)
  |      ├─> Not available? → Try .70c
  |      └─> Still not available? → Try .66c, .60c
  |
  +--> Check temperature requirements
  |      ├─> System temp < 400 K? → .80c + TMP OK
  |      ├─> System temp 400-800 K? → .81c or .82c
  |      ├─> System temp > 800 K? → .82c or higher
  |      └─> Exact temp not available? → Use closest + TMP
  |
  +--> Verify special libraries
  |      ├─> Thermal moderator? → Check .nnT libraries
  |      ├─> Photon transport? → Check .nnP libraries
  |      └─> Electron transport? → Check .nnE libraries
  |
  +--> Verify DATAPATH
  |      ├─> echo $DATAPATH (Linux) or %DATAPATH% (Windows)
  |      ├─> Path correct?
  |      └─> xsdir file present?
  |
  └─> Document library choice
         └─> Comment in input file with library source
```

## Tool Invocation

This skill includes a Python implementation for automated cross-section library management.

### Importing the Tool

```python
from mcnp_cross_section_manager import MCNPCrossSectionManager

# Initialize the manager
manager = MCNPCrossSectionManager()
```

### Basic Usage

**Check if Specific ZAID Available**:
```python
# Check single ZAID availability
available = manager.check_availability('92235.80c')
if available:
    print("U-235 (.80c) library available")
else:
    print("U-235 (.80c) NOT available - check alternatives")
```

**List Available Library Types**:
```python
# Get all library types
libraries = manager.list_available_libraries()

print("Available library types:")
for lib_id, description in libraries.items():
    print(f"  {lib_id}: {description}")

# Example output:
# Available library types:
#   80c: ENDF/B-VIII.0 continuous energy
#   70c: ENDF/B-VII.0 continuous energy
#   80t: ENDF/B-VIII.0 thermal scattering
#   80p: ENDF/B-VIII.0 photoatomic
```

**Get Library Information**:
```python
# Get description of specific library
info = manager.get_library_info('80c')
print(f"Library 80c: {info}")

# Output: Library 80c: ENDF/B-VIII.0 continuous energy neutron data
```

**Suggest Temperature Library**:
```python
# Get recommended library based on temperature
temp_kelvin = 900
suggested = manager.suggest_temperature_library('U-235', temp_kelvin)
print(f"For {temp_kelvin} K, use library: {suggested}")

# Output: For 900 K, use library: 82c
```

**Parse and Check xsdir File**:
```python
# Parse xsdir file (if needed for detailed analysis)
xsdir_path = '/path/to/mcnpdata/xsdir'
manager.parse_xsdir(xsdir_path)

# Then check availability
print("Checking ZAIDs...")
zaids_to_check = ['1001.80c', '8016.80c', '92235.80c', '95243.80c']

for zaid in zaids_to_check:
    if manager.check_availability(zaid):
        print(f"  ✓ {zaid}: Available")
    else:
        print(f"  ✗ {zaid}: NOT AVAILABLE")
```

### Integration with MCNP Workflow

```python
from mcnp_cross_section_manager import MCNPCrossSectionManager

def validate_material_libraries(material_zaids, temperature_k=None):
    """Validate that all ZAIDs in materials have available libraries"""
    print("Validating cross-section libraries...")
    print("=" * 60)

    manager = MCNPCrossSectionManager()

    # Check each ZAID
    missing = []
    available = []

    for zaid in material_zaids:
        if manager.check_availability(zaid):
            available.append(zaid)
            print(f"✓ {zaid}: Available")
        else:
            missing.append(zaid)
            print(f"✗ {zaid}: NOT AVAILABLE")

    # Recommend temperature libraries if needed
    if temperature_k and temperature_k > 400:
        print(f"\n💡 TEMPERATURE RECOMMENDATIONS (System at {temperature_k} K):")
        for zaid in available:
            isotope = zaid.split('.')[0]
            suggested_lib = manager.suggest_temperature_library(isotope, temperature_k)
            current_lib = zaid.split('.')[1]

            if suggested_lib != current_lib:
                print(f"  • {zaid}: Consider using .{suggested_lib} instead")

    # Report summary
    print("\n" + "=" * 60)
    print(f"Summary: {len(available)} available, {len(missing)} missing")

    if missing:
        print("\n❌ MISSING LIBRARIES:")
        for zaid in missing:
            print(f"  {zaid}")
            # Suggest alternatives
            base_zaid = zaid.split('.')[0]
            lib = zaid.split('.')[1]
            alt_lib = '70c' if lib == '80c' else '80c'
            alt_zaid = f"{base_zaid}.{alt_lib}"

            print(f"    Try alternative: {alt_zaid}")
            if manager.check_availability(alt_zaid):
                print(f"      ✓ {alt_zaid} is available!")

        return False
    else:
        print("\n✓ All cross-section libraries available")
        return True

# Example usage
if __name__ == "__main__":
    # Define materials needed for input file
    materials = [
        '1001.80c',   # H-1
        '8016.80c',   # O-16
        '92235.80c',  # U-235
        '92238.80c',  # U-238
        '95243.80c',  # Am-243 (might not be available)
    ]

    # Validate at reactor temperature
    if validate_material_libraries(materials, temperature_k=900):
        print("\nReady to run MCNP simulation")
    else:
        print("\nFix library issues before running")
```

---

## Use Case 1: Check Library Availability Before Running

**Problem**: Want to verify all materials have cross sections before expensive run

**Check Process**:
```bash
# Extract ZAIDs from input file
grep "\.80c\|\.70c\|\.66c" input.inp | awk '{print $2}' > zaids_needed.txt

# Check each ZAID in xsdir
while read zaid; do
  if grep -q "^$zaid " xsdir; then
    echo "$zaid: Found"
  else
    echo "$zaid: MISSING - CHECK REQUIRED"
  fi
done < zaids_needed.txt
```

**Example Output**:
```
1001.80c: Found
8016.80c: Found
26000.80c: Found
95243.80c: MISSING - CHECK REQUIRED
```

**Resolution for Missing (Am-243)**:
```
Option 1: Check if different version available
  grep "95243" xsdir
  Result: 95243.70c available
  Action: Use 95243.70c instead

Option 2: Use natural americium (if exists)
  grep "95000" xsdir
  Result: Not typically available

Option 3: Request library or modify problem
```

## Use Case 2: Diagnose "Cross-Section Table Not Found" Error

**MCNP Error Message**:
```
fatal error.  cross-section table 92237.80c not found.
              table = 92237.80c
```

**Diagnostic Steps**:

**Step 1: Verify ZAID in xsdir**
```bash
grep "92237.80c" $DATAPATH/xsdir
# Result: No output (not found)
```

**Step 2: Check if isotope exists in other versions**
```bash
grep "92237" $DATAPATH/xsdir
# Result:
# 92237.70c  235.005  endf70/U/92237.700c  ...
# 92237.66c  235.005  endf66/U/92237.700c  ...
```

**Step 3: Solution options**
```
1. Use available version:
   Change: 92237.80c → 92237.70c

2. Use natural uranium (usually not appropriate for U-237):
   92237 is radioactive, natural won't work

3. Check if really needed:
   U-237 has 6.75 day half-life, often not in steady-state fuel
   May be able to omit from material definition
```

**Fix**:
```
c U-237 not available in ENDF/B-VIII.0
c Using ENDF/B-VII.0 library instead
M1  92235.80c  ...
    92237.70c  ...    $ Changed from .80c to .70c
    92238.80c  ...
```

## Use Case 3: Select Temperature-Dependent Library

**Problem**: Reactor core at 900 K, need appropriate cross sections

**Selection Process**:
```
Target temperature: 900 K

Check available temperature libraries:
  grep "92235.*c" xsdir | grep -v "#"

Results:
  92235.80c  ...  2.5301E-08  $ 293.6 K
  92235.81c  ...  5.1704E-08  $ 600 K
  92235.82c  ...  7.7559E-08  $ 900 K ✓
  92235.83c  ...  1.0341E-07  $ 1200 K

Best match: .82c (exactly 900 K)
```

**MCNP Input**:
```
c Core at 900 K - using .82c libraries at native temperature
M1  92235.82c  0.045       $ U-235 at 900 K
    92238.82c  0.955       $ U-238 at 900 K
    8016.82c   2.0         $ O-16 at 900 K
c
c No TMP card needed - using native 900 K libraries
```

**If .82c Not Available** (e.g., for minor isotope):
```
c Gd-155 only available at room temperature
c Core at 900 K - must interpolate
M2  64155.80c  1.0         $ Gd-155 (only .80c available)
TMP  900                    $ MCNP interpolates to 900 K
c
c Note: Less accurate than native library
c Consider if Gd-155 critical to results
```

## Use Case 4: Find Alternative When Primary Unavailable

**Problem**: Want Tc-99 (.80c) but not in library

**Search Process**:
```bash
# Search for Tc-99
grep "43099" xsdir
# Result: No .80c, but found:
# 43099.70c  98.871  endf70/Tc/43099.700c  ...
```

**Alternative Selection Tree**:
```
1. Try older ENDF version: 43099.70c ✓ Available
   Pros: Official evaluation, validated
   Cons: Slightly older data

2. Try natural technetium: 43000.nnc
   Check: grep "43000" xsdir
   Result: Not available (Tc has no stable isotopes)

3. Use similar isotope: Tc-98 or Tc-100
   Check: grep "43098\|43100" xsdir
   Result: Not typically available

4. Omit if not critical:
   Tc-99 is fission product, long-lived (211,000 yr)
   For short-term calculations: May be negligible
   For long-term waste: Must include

Decision: Use 43099.70c (ENDF/B-VII.0)
```

**Implementation**:
```
c Tc-99 (fission product)
c .80c not available, using .70c
M10 43099.70c  1.0         $ Tc-99 (ENDF/B-VII.0)
```

## Use Case 5: Verify Thermal Scattering Library

**Problem**: Light water reactor, verify lwtr library available

**Check Process**:
```bash
# Search for light water thermal scattering
grep "lwtr" xsdir

# Expected results:
lwtr.80t  ...  $ ENDF/B-VIII.0, 293.6 K
lwtr.81t  ...  $ 323.6 K
lwtr.82t  ...  $ 373.6 K
lwtr.83t  ...  $ 423.6 K
...
```

**Verify Temperature Match**:
```
System: PWR at 580 K (307°C)

Available lwtr temperatures:
  lwtr.80t → 293.6 K
  lwtr.81t → 323.6 K
  lwtr.82t → 373.6 K
  lwtr.83t → 423.6 K
  lwtr.84t → 473.6 K
  lwtr.85t → 523.6 K
  lwtr.86t → 573.6 K ✓ (closest)
  lwtr.87t → 623.6 K

Best: lwtr.86t (573.6 K, ~7 K difference)
Alternative: lwtr.87t (623.6 K)
```

**MCNP Input**:
```
c PWR water at 580 K (~307°C)
c Using lwtr.86t (573.6 K, closest available)
M1  1001.80c  2.0          $ H-1
    8016.80c  1.0          $ O-16
MT1  lwtr.86t              $ Thermal scattering at ~580 K
```

## Use Case 6: Fix DATAPATH Configuration

**Problem**: MCNP can't find any cross sections

**MCNP Error**:
```
bad trouble in subroutine rdcont
          opened library file C:\mcnp\data\endf80\H\1001.800c
          cannot open file C:\mcnp\data\endf80\H\1001.800c
```

**Diagnosis**:
```
Issue: MCNP trying to open files but path incorrect

Check 1: Is DATAPATH set?
  Windows: echo %DATAPATH%
  Linux: echo $DATAPATH

  Result: Empty or points to wrong location

Check 2: Where is xsdir actually located?
  Windows: dir /s xsdir (from likely root)
  Linux: find /path -name xsdir

  Result: C:\mcnpdata\xsdir (actual location)
```

**Fix**:

**Windows**:
```cmd
REM Set temporarily for current session
set DATAPATH=C:\mcnpdata

REM Set permanently (system-wide)
setx DATAPATH "C:\mcnpdata" /M

REM Or add to user environment variables via GUI
```

**Linux**:
```bash
# Set temporarily
export DATAPATH=/opt/mcnpdata

# Set permanently in ~/.bashrc or ~/.bash_profile
echo "export DATAPATH=/opt/mcnpdata" >> ~/.bashrc
source ~/.bashrc

# Verify
echo $DATAPATH
ls $DATAPATH/xsdir
```

**Verification**:
```bash
# Test MCNP can find libraries
mcnp6 i=test.inp tasks 1

# Should see:
# "establishing xsdir file: /opt/mcnpdata/xsdir"
# No "cannot open file" errors
```

## Use Case 7: Check Photon Library for Coupled Transport

**Problem**: MODE N P calculation, verify photon libraries available

**Requirements**:
```
For MODE N P (coupled neutron-photon):
  - Neutron libraries (.nnc) for all isotopes
  - Photoatomic libraries (.nnp) for all elements
  - Photon production data in neutron libraries
```

**Check Process**:
```bash
# Extract elements from material cards
# Example: Material has H, O, Fe

# Check photon libraries
for Z in 1 8 26; do
  zaid="${Z}000.80p"
  if grep -q "^$zaid " xsdir; then
    echo "$zaid: Available"
  else
    echo "$zaid: MISSING"
  fi
done

Results:
  1000.80p: Available  ✓
  8000.80p: Available  ✓
  26000.80p: Available ✓
```

**MCNP Input**:
```
c Coupled neutron-photon transport
MODE N P
c
c Materials (neutron cross sections)
M1  1001.80c  2.0          $ H-1
    8016.80c  1.0          $ O-16
M2  26000.80c  1.0         $ Natural iron
c
c Photon physics uses .80p automatically if available
c No explicit .80p needed in M cards
c MCNP finds photoatomic data based on Z
```

**If Photon Library Missing**:
```
Warning: If .nnp not available for element:
  - MCNP may use default photon cross sections
  - Results less accurate for that element
  - Consider using available data library version
  - Or omit element if minor contributor
```

## Common Errors and Troubleshooting

### Error 1: Mixed Library Versions

**Symptom**: Some isotopes .80c, others .70c, inconsistent results

**Problem**: Mixing ENDF/B versions can cause physics inconsistencies

**Example (Bad)**:
```
M1  92235.80c  0.045       $ ENDF/B-VIII.0
    92238.70c  0.955       $ ENDF/B-VII.0 (INCONSISTENT!)
    8016.80c   2.0         $ ENDF/B-VIII.0
```

**Fix (Good)**:
```
M1  92235.80c  0.045       $ All ENDF/B-VIII.0
    92238.80c  0.955       $ Consistent version
    8016.80c   2.0         $ Same library version
```

**Best Practice**: Use same ENDF/B version for all isotopes when possible

### Error 2: Thermal Scattering Temperature Mismatch

**Symptom**: Incorrect keff or spectrum in thermal system

**Problem**: Thermal library temperature doesn't match material temperature

**Example (Bad)**:
```
c Water at 573 K (300°C)
M1  1001.80c  2.0
    8016.80c  1.0
MT1  lwtr.80t              $ WRONG! This is 293.6 K
TMP  573                    $ TMP doesn't affect S(α,β)!
```

**Fix (Good)**:
```
c Water at 573 K (300°C)
M1  1001.80c  2.0
    8016.80c  1.0
MT1  lwtr.86t              $ Correct: 573.6 K thermal library
```

**Important**: TMP card does NOT affect thermal scattering (S(α,β))
Must use correct .nnT library for temperature

### Error 3: Missing Thermal Scattering Data

**Symptom**: keff significantly off for thermal system

**Problem**: No MT card for moderator material

**Example (Bad)**:
```
c Light water reactor (MISSING MT card!)
M1  1001.80c  2.0          $ H-1
    8016.80c  1.0          $ O-16
c No MT1 lwtr.80t !        $ ERROR: Required for accuracy
```

**Fix (Good)**:
```
c Light water reactor
M1  1001.80c  2.0          $ H-1
    8016.80c  1.0          $ O-16
MT1  lwtr.80t              $ Thermal scattering (REQUIRED)
```

**Impact**: Missing S(α,β) can cause ~1-5% error in keff for thermal systems

### Error 4: Photon Production Not Available

**Symptom**: Warning about missing photon production data

**MCNP Warning**:
```
warning.  nuclide 43099 does not have photon production data.
```

**Explanation**: Some isotopes lack coupled neutron-photon data

**Options**:
```
1. Accept warning if photon yield from that isotope negligible
2. Use different library version (may have photon production)
3. Remove MODE P if photons not critical to problem
4. Model neutron and photon transport separately
```

**Example**:
```
c Tc-99 doesn't have photon production in .70c
c For shielding dominated by other isotopes:
c → Accept warning, photon contribution from Tc-99 minimal
c
c For detailed gamma spectroscopy:
c → Consider omitting Tc-99 or using different approach
```

## Integration with Other Skills

### 1. **mcnp-isotope-lookup**
Provides ZAIDs, cross-section-manager verifies availability.

### 2. **mcnp-material-builder**
Checks library availability before creating M cards.

### 3. **mcnp-input-validator**
Validates all ZAIDs have available cross sections.

### 4. **mcnp-fatal-error-debugger**
Diagnoses library-related fatal errors.

### 5. **mcnp-physics-builder**
Verifies thermal scattering and special libraries.

## Validation Checklist

- [ ] DATAPATH environment variable set correctly
- [ ] xsdir file exists and readable at DATAPATH
- [ ] All material ZAIDs found in xsdir
- [ ] Library version consistent across isotopes (.80c preferred)
- [ ] Temperature libraries appropriate for system
- [ ] Thermal scattering (.nnT) available for moderators
- [ ] Photoatomic (.nnP) available for MODE P calculations
- [ ] Cross-section files exist at paths specified in xsdir
- [ ] File permissions allow MCNP to read data files
- [ ] Documented any library version mixing with justification

## Best Practices

1. **Use Latest ENDF/B Version**: Prefer .80c when available
2. **Check Before Running**: Verify libraries to avoid expensive failed runs
3. **Keep Versions Consistent**: All .80c or all .70c when possible
4. **Match Temperatures**: Use .nnc library close to system temperature
5. **Include Thermal Scattering**: Always use MT card for moderators
6. **Document Alternatives**: Comment why using non-standard library
7. **Maintain DATAPATH**: Set permanently in environment
8. **Update xsdir Carefully**: Regenerate rather than hand-edit
9. **Test New Installations**: Run test case to verify library access
10. **Keep Backups**: Save working xsdir when libraries functional

## References

- **MCNP Manual**: Appendix G (Cross-Section Libraries)
- **Related Skills**:
  - mcnp-isotope-lookup
  - mcnp-material-builder
  - mcnp-physics-builder
  - mcnp-fatal-error-debugger
- **External Resources**:
  - ENDF/B-VIII.0 documentation
  - MCNP installation guides
  - NEA Data Bank

---

**End of MCNP Cross-Section Manager Skill**

---
category: F
name: mcnp-cross-section-manager
description: Manage and verify MCNP cross-section libraries including checking xsdir availability, diagnosing library errors, finding alternatives for missing data, and understanding library versions and types
version: 2.0.0
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

## Prerequisites

- **mcnp-isotope-lookup**: Provides ZAID identification
- **mcnp-material-builder**: Uses verified cross sections
- **mcnp-physics-builder**: Uses thermal scattering libraries
- Understanding of ZAID format (ZZZAAA.nnX)
- Basic knowledge of ENDF/B library versions
- Familiarity with MCNP error messages

## Core Concepts - Quick Reference

### xsdir File

**Purpose**: Index file listing all available cross-section libraries

**Location**: `$DATAPATH/xsdir` or `%DATAPATH%\xsdir`

**Entry Format**:
```
ZAID  AWR  filename  access  file_length  record_length  entries  temperature

Example:
92235.80c  235.043930  endf80/U/92235.800nc  0  1  1  78901  2.5301E-08

Components:
  ZAID: 92235.80c (U-235, ENDF/B-VIII.0)
  AWR: Atomic weight ratio (235.04393)
  filename: Path relative to DATAPATH
  temperature: 2.5301E-08 MeV = 293.6 K
```

**Detailed Reference**: See `xsdir_format.md` for complete specification.

### Library Types

| Type | Extension | Use Case | Example |
|------|-----------|----------|---------|
| Continuous Energy | .nnc | General neutron transport | 92235.80c |
| Thermal Scattering | .nnT | Bound thermal neutrons (E < 4 eV) | lwtr.80t |
| Photoatomic | .nnP | Photon transport (MODE P) | 82000.80p |
| Photoelectron | .nnE | Electron transport (MODE E) | 6000.80e |
| Discrete Reaction | .nnD | Legacy format (rarely used) | 92235.80d |

**Detailed Reference**: See `library_types.md` for complete guide.

### Library Versions

| Version | ENDF/B | Year | Availability |
|---------|--------|------|--------------|
| .80c/.80t/.80p | VIII.0 | 2018 | Latest, recommended |
| .70c/.70t/.70p | VII.0 | 2006 | Widely available |
| .71c | VII.1 | 2011 | Moderate coverage |
| .66c | VI.8 | 2001 | Legacy systems |

**Best Practice**: Use .80c when available; keep versions consistent within materials.

### Temperature Libraries

**Common Temperatures**:
```
.80c → 293.6 K (20°C, room temperature)
.81c → 600 K (327°C)
.82c → 900 K (627°C)
.83c → 1200 K (927°C)
.84c → 2500 K (2227°C)
```

**Availability**: Not all isotopes have all temperatures. Actinides and structural materials have best coverage.

**Detailed Reference**: See `temperature_libraries.md` for interpolation guidelines.

## Python Tools

This skill includes three command-line tools for library management:

### 1. xsdir_parser.py - Query xsdir Files
```bash
# Find specific ZAID
python xsdir_parser.py --zaid "92235.80c"

# Search for isotopes
python xsdir_parser.py --search "^92"

# Show statistics
python xsdir_parser.py --statistics

# Interactive mode
python xsdir_parser.py
```

### 2. library_finder.py - Find Available Libraries
```bash
# Find all libraries for isotope
python library_finder.py --isotope "U-235"

# Check if ZAID available
python library_finder.py --check "92235.80c"

# Get recommendations for missing library
python library_finder.py --recommend "92235.70c"

# Interactive mode
python library_finder.py
```

### 3. missing_library_diagnoser.py - Troubleshoot Errors
```bash
# Verify DATAPATH setup
python missing_library_diagnoser.py --verify-setup

# Diagnose MCNP error message
python missing_library_diagnoser.py --error "cross-section table 92235.80c not found"

# Check input file for missing libraries
python missing_library_diagnoser.py --input input.i

# Interactive mode
python missing_library_diagnoser.py
```

**Detailed Documentation**: See `scripts/README.md` for complete usage guide.

## Decision Tree: Library Selection

```
START: Need cross-section library
  |
  +--> Is ZAID in xsdir?
  |      ├─> Yes: Verify file exists → Use library
  |      └─> No: Try alternatives:
  |            ├─> Different version (.70c instead of .80c)
  |            ├─> Natural element (ZZZ000.nnc)
  |            └─> Similar isotope (if appropriate)
  |
  +--> Select library version
  |      ├─> .80c available? → Prefer (most recent)
  |      ├─> .70c available? → Use if .80c missing
  |      └─> .66c available? → Last resort
  |
  +--> Check temperature requirements
  |      ├─> T < 400 K? → .80c + TMP acceptable
  |      ├─> 400-800 K? → .81c or .82c preferred
  |      ├─> T > 800 K? → .82c, .83c, or .84c
  |      └─> Exact T unavailable? → Use closest + TMP
  |
  +--> Verify special libraries
  |      ├─> Moderator? → Check .nnT (thermal scattering)
  |      ├─> MODE P? → Check .nnP (photoatomic)
  |      └─> MODE E? → Check .nnE (photoelectron)
  |
  └─> Verify DATAPATH
         └─> echo $DATAPATH (Linux) or %DATAPATH% (Windows)
```

## Use Cases

### Use Case 1: Verify Libraries Before Running

**Objective**: Check all materials have cross sections before expensive simulation

**Quick Check Using Python Tools**:
```bash
# Check input file for missing libraries
python missing_library_diagnoser.py --input input.i
```

**Output**:
```
Input file: input.i
Total ZAIDs: 15
Available: 12
Missing: 3

Missing ZAIDs:
  ✗ 92235.70c
  ✗ 94239.70c
  ✗ 43099.80c
```

**Resolution**:
```bash
# Get alternatives for each missing ZAID
python library_finder.py --recommend "92235.70c"
# → Suggests: 92235.80c (alternative version)

python library_finder.py --recommend "43099.80c"
# → Suggests: 43099.70c (older ENDF version)
```

**Manual Check (Bash)**:
```bash
# Extract ZAIDs and check xsdir
grep "\.80c\|\.70c" input.i | awk '{print $2}' | while read zaid; do
  grep -q "^$zaid " $DATAPATH/xsdir && echo "$zaid: OK" || echo "$zaid: MISSING"
done
```

### Use Case 2: Diagnose "Table Not Found" Error

**MCNP Error**:
```
fatal error.  cross-section table 92235.80c not found.
              table = 92235.80c
```

**Diagnosis Using Python Tool**:
```bash
python missing_library_diagnoser.py --error "cross-section table 92235.80c not found"
```

**Output**:
```
Error type: ZAID_NOT_FOUND
ZAID: 92235.80c
Problem: Cross-section table 92235.80c not found in xsdir

Recommended fixes:
  1. Check if DATAPATH set: echo $DATAPATH
  2. Search xsdir for 92235.80c: grep '92235.80c' $DATAPATH/xsdir
  3. Try alternative library version (e.g., .70c instead of .80c)
  4. Use natural element (e.g., 92000.80c for natural uranium)
  5. Verify library installation is complete
```

**Find Alternative**:
```bash
# Search for any U-235 libraries
python xsdir_parser.py --search "92235"

# Get specific recommendation
python library_finder.py --recommend "92235.80c"
```

**Manual Diagnostic Steps**:
```bash
# Step 1: Check DATAPATH
echo $DATAPATH
ls $DATAPATH/xsdir

# Step 2: Search for ZAID
grep "92235" $DATAPATH/xsdir

# Step 3: Check file exists
# (from xsdir entry)
ls $DATAPATH/endf80/U/92235.800nc
```

### Use Case 3: Select Temperature Library

**Problem**: Reactor core at 900 K, need appropriate cross sections

**Selection Using Python Tool**:
```bash
# Find all U-235 temperature libraries
python xsdir_parser.py --search "92235\.8[0-9]c"
```

**Results**:
```
92235.80c  (293.6 K)
92235.81c  (600 K)
92235.82c  (900 K) ← Best match
92235.83c  (1200 K)
92235.84c  (2500 K)
```

**MCNP Input**:
```
c Core at 900 K - using native .82c libraries
M1  92235.82c  0.045       $ U-235 at 900 K
    92238.82c  0.955       $ U-238 at 900 K
    8016.82c   2.0         $ O-16 at 900 K
c No TMP card needed - using native temperature
```

**If Temperature Unavailable** (e.g., for minor isotope):
```
c Gd-155 only available at 293.6 K
M2  64155.80c  1.0         $ Gd-155 (only .80c exists)
TMP  900                    $ MCNP interpolates to 900 K
c Note: Less accurate than native library
```

**Detailed Reference**: See `temperature_libraries.md` for interpolation effects.

### Use Case 4: Verify Thermal Scattering Library

**Problem**: Light water reactor, need lwtr.80t library

**Check Using Python Tool**:
```bash
# List all thermal scattering libraries
python xsdir_parser.py --list-section thermal
```

**Manual Check**:
```bash
# Search for light water thermal libraries
grep "lwtr" $DATAPATH/xsdir

# Expected:
# lwtr.80t  (293.6 K)
# lwtr.81t  (323.6 K)
# lwtr.82t  (373.6 K)
# ...
```

**Temperature Matching**:
```
System: PWR at 580 K (307°C)

Available:
  lwtr.85t → 523.6 K
  lwtr.86t → 573.6 K ← Closest (Δ = 7 K)
  lwtr.87t → 623.6 K

Best choice: lwtr.86t
```

**MCNP Input**:
```
c PWR water at 580 K
M1  1001.80c  2.0          $ H-1
    8016.80c  1.0          $ O-16
MT1  lwtr.86t              $ S(α,β) at ~580 K
```

**Important**: TMP card does NOT affect S(α,β) data. Must use correct .nnT library.

## Common Errors - Quick Reference

### Error 1: ZAID Not Found
**Symptom**: `fatal error. cross-section table ZAID not found`
**Causes**: Library missing, DATAPATH wrong, wrong version
**Fixes**: Check xsdir, try .70c/.66c, use natural element
**Tool**: `python missing_library_diagnoser.py --error "<message>"`
**Reference**: See `troubleshooting_libraries.md` sections 1-4

### Error 2: Cannot Open File
**Symptom**: `cannot open file /path/to/file`
**Causes**: File missing, permissions, path wrong
**Fixes**: Verify file exists, check permissions, fix DATAPATH
**Tool**: `python missing_library_diagnoser.py --verify-setup`
**Reference**: See `troubleshooting_libraries.md` sections 5-8

### Error 3: AWR is Zero
**Symptom**: `atomic weight ratio (AWR) is zero`
**Causes**: Corrupted xsdir
**Fixes**: Restore xsdir backup, regenerate
**Reference**: See `troubleshooting_libraries.md` sections 9-10

### Error 4: Temperature Out of Range
**Symptom**: `temperature T K out of range for ZAID`
**Causes**: TMP too high, temp library missing
**Fixes**: Use .81c/.82c/.83c, accept default
**Tool**: `python xsdir_parser.py --search "ZZZAAA.8[0-9]c"`
**Reference**: See `temperature_libraries.md`

### Error 5: Mixed Library Versions
**Symptom**: Inconsistent results, physics warnings
**Problem**: Mixing .80c and .70c in same material
**Fix**: Standardize on single version (.80c preferred)
**Best Practice**: Use same ENDF/B version for all isotopes

## Integration with Other Skills

- **mcnp-isotope-lookup**: Provides ZAIDs → cross-section-manager verifies availability
- **mcnp-material-builder**: Checks libraries before creating M cards
- **mcnp-input-validator**: Validates all ZAIDs have available cross sections
- **mcnp-fatal-error-debugger**: Diagnoses library-related fatal errors
- **mcnp-physics-builder**: Verifies thermal scattering and special libraries

## Validation Checklist

- [ ] DATAPATH environment variable set correctly
- [ ] xsdir file exists and readable at `$DATAPATH/xsdir`
- [ ] All material ZAIDs found in xsdir
- [ ] Library version consistent across isotopes (.80c preferred)
- [ ] Temperature libraries appropriate for system conditions
- [ ] Thermal scattering (.nnT) available for moderators (lwtr, grph, etc.)
- [ ] Photoatomic (.nnP) available if using MODE P
- [ ] Cross-section files exist at paths specified in xsdir
- [ ] File permissions allow MCNP to read data files
- [ ] Any library version mixing documented with justification

## Best Practices

1. **Use Latest ENDF/B Version**: Prefer .80c (ENDF/B-VIII.0) when available
2. **Check Before Running**: Verify libraries to avoid expensive failed runs
3. **Keep Versions Consistent**: All .80c or all .70c when possible
4. **Match Temperatures**: Use .nnc library close to system temperature
5. **Include Thermal Scattering**: Always use MT card for moderators (lwtr, grph, etc.)
6. **Document Alternatives**: Comment why using non-standard library
7. **Maintain DATAPATH**: Set permanently in environment (`~/.bashrc` or system variables)
8. **Verify New Installations**: Run test case to verify library access
9. **Keep Backups**: Save working xsdir when libraries functional
10. **Use Python Tools**: Automate checking with provided scripts

## DATAPATH Configuration

### Linux/Mac Setup
```bash
# Temporary (current session)
export DATAPATH=/opt/mcnpdata

# Permanent (user)
echo 'export DATAPATH=/opt/mcnpdata' >> ~/.bashrc
source ~/.bashrc

# Verify
echo $DATAPATH
ls $DATAPATH/xsdir
```

### Windows Setup
```cmd
REM Temporary (current session)
set DATAPATH=C:\mcnpdata

REM Permanent (user)
setx DATAPATH "C:\mcnpdata"

REM Permanent (system-wide, requires admin)
setx DATAPATH "C:\mcnpdata" /M

REM Verify
echo %DATAPATH%
dir %DATAPATH%\xsdir
```

**GUI Method (Windows)**:
1. Right-click "This PC" → Properties
2. Advanced system settings → Environment Variables
3. New → Variable: `DATAPATH`, Value: `C:\mcnpdata`
4. OK, Apply, Restart terminal

## Resources and References

### Reference Files (Detailed Guides)
- `xsdir_format.md` - Complete xsdir file specification, parsing methods, format details
- `library_types.md` - Detailed library type reference (.c, .t, .p, .e, .d) with use cases
- `temperature_libraries.md` - Temperature-dependent library guide, interpolation effects
- `troubleshooting_libraries.md` - Comprehensive error diagnosis procedures and fixes

### Python Tools
- `scripts/xsdir_parser.py` - Query and analyze xsdir files
- `scripts/library_finder.py` - Find available libraries and alternatives
- `scripts/missing_library_diagnoser.py` - Diagnose library errors systematically
- `scripts/README.md` - Complete tool documentation and workflows

### Example Data
- `example_inputs/xsdir_example.txt` - Sample xsdir entries showing format
- `example_inputs/error_messages.txt` - Common MCNP error examples for practice
- `example_inputs/library_matrix.csv` - Library availability matrix by version

### Related MCNP Skills
- **mcnp-isotope-lookup**: ZAID format and isotope identification
- **mcnp-material-builder**: Material definition with verified libraries
- **mcnp-physics-builder**: Physics configuration including thermal scattering
- **mcnp-input-validator**: Input file validation including library checks
- **mcnp-fatal-error-debugger**: Fatal error diagnosis and resolution

### External Resources
- **MCNP Manual**: Appendix G (Cross-Section Libraries)
- **ENDF/B-VIII.0 Documentation**: Latest evaluation details
- **MCNP Installation Guides**: Library setup procedures
- **NEA Data Bank**: Nuclear data resources

---

**Version**: 2.0.0
**Last Updated**: 2025-11-06
**Status**: Production-ready with comprehensive Python tooling

---

**End of MCNP Cross-Section Manager Skill**

# xsdir File Format Reference

## Overview

The `xsdir` (cross-section directory) file is MCNP's master index of all available nuclear data libraries. Understanding its structure is essential for diagnosing library errors, verifying data availability, and troubleshooting cross-section issues.

## File Location

**Environment Variable:** `DATAPATH`
```bash
# Linux/Mac
export DATAPATH=/path/to/mcnp/data
ls $DATAPATH/xsdir

# Windows
set DATAPATH=C:\mcnp\data
dir %DATAPATH%\xsdir
```

**MCNP Search Order:**
1. Path specified by `DATAPATH` environment variable
2. Current working directory
3. Default installation directory (platform-dependent)

## File Structure

### Header Section
```
directory
atomic weight library
```

### Data Entry Format
```
ZAID  AWR  filename  access  file_length  record_length  entries  temperature  ...

Components:
ZAID = Z and A identifier with library (e.g., 92235.80c)
AWR = Atomic weight ratio (relative to neutron mass)
filename = Path to data file (relative to DATAPATH)
access = Access method (0 = direct)
file_length = Number of records in file
record_length = Length of each record
entries = Number of data entries
temperature = Thermal energy in MeV (k·T where k = Boltzmann constant)
```

### Example Entries

**Neutron Continuous Energy:**
```
1001.80c  0.999167  endf80/H/1001.800nc  0  1  1  4553  2.5301E-08
│         │         │                     │  │  │  │     │
│         │         │                     │  │  │  │     └─ kT = 2.53E-08 MeV (293.6 K)
│         │         │                     │  │  │  └─ 4553 energy points
│         │         │                     │  │  └─ Record length
│         │         │                     │  └─ File length
│         │         │                     └─ Direct access
│         │         └─ Data file path
│         └─ Atomic weight ratio (H-1 / neutron)
└─ ZAID: H-1 with ENDF/B-VIII.0
```

**Temperature-Dependent:**
```
92235.80c  235.04393  endf80/U/92235.800nc  0  1  1  15234  2.5301E-08
92235.81c  235.04393  endf80/U/92235.810nc  0  1  1  15234  5.1704E-08
92235.82c  235.04393  endf80/U/92235.820nc  0  1  1  15234  7.7559E-08
│                                                            │
└─ Same isotope, different temperatures ─────────────────────┘
   .80c = 293.6 K
   .81c = 600 K
   .82c = 900 K
```

**Thermal Scattering:**
```
lwtr.80t  0.99917  endf80/thermal/lwtr.01t  0  1  1  3389  2.5301E-08
│         │        │                         │  │  │  │     │
│         │        │                         │  │  │  │     └─ 293.6 K
│         │        │                         │  │  │  └─ 3389 entries
│         │        │                         │  │  └─ Record info
│         │        │                         │  └─ File info
│         │        │                         └─ Access method
│         │        └─ S(α,β) data file
│         └─ H in H₂O molecular weight
└─ Light water thermal scattering at 293.6 K
```

**Photoatomic Data:**
```
1000.80p  1.007825  endf80/photoat/1000.80p  0  1  1  1024  0.0
│                                                            │
└─ Hydrogen photoatomic library ───────────────────────────┘
```

## Temperature Encoding

Temperature in xsdir is stored as thermal energy (k·T in MeV):

| Library | Temperature (K) | kT (MeV) | xsdir Value |
|---------|----------------|----------|-------------|
| .80c    | 293.6 K        | 0.0253 eV | 2.5301E-08 |
| .81c    | 600 K          | 0.0517 eV | 5.1704E-08 |
| .82c    | 900 K          | 0.0776 eV | 7.7559E-08 |
| .83c    | 1200 K         | 0.1034 eV | 1.0341E-07 |
| .84c    | 2500 K         | 0.2154 eV | 2.1544E-07 |

**Conversion:**
```
T (K) = (kT in MeV) / (8.617333E-11 MeV/K)
kT (MeV) = T (K) × 8.617333E-11
```

## Section Markers

xsdir file is divided into sections:

```
directory
  <continuous energy neutron data entries>

thermal
  <thermal scattering S(α,β) entries>

photoatomic
  <photoatomic interaction entries>

photoelectron
  <electron interaction entries>

dosimetry
  <dosimetry response entries>
```

## Parsing xsdir

### Bash/Grep Method
```bash
# Find specific ZAID
grep "^92235.80c " $DATAPATH/xsdir

# Find all uranium isotopes
grep "^92[0-9][0-9][0-9]\.80c " $DATAPATH/xsdir

# Find all thermal scattering libraries
grep "\.80t " $DATAPATH/xsdir

# Count available continuous energy libraries
grep "\.80c " $DATAPATH/xsdir | wc -l
```

### Python Parsing
```python
def parse_xsdir(xsdir_path):
    """Parse xsdir file into dictionary"""
    libraries = {}
    section = 'directory'

    with open(xsdir_path, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('c '):
                continue

            # Section markers
            if line.lower() in ['directory', 'thermal', 'photoatomic',
                                'photoelectron', 'dosimetry']:
                section = line.lower()
                continue

            # Skip header lines
            if 'atomic weight library' in line.lower():
                continue

            # Parse data entry
            parts = line.split()
            if len(parts) >= 8:
                zaid = parts[0]
                awr = float(parts[1])
                filename = parts[2]
                temperature_mev = float(parts[7])

                libraries[zaid] = {
                    'awr': awr,
                    'filename': filename,
                    'temperature_mev': temperature_mev,
                    'temperature_k': temperature_mev / 8.617333e-11,
                    'section': section
                }

    return libraries

# Usage
libraries = parse_xsdir('/path/to/xsdir')
if '92235.80c' in libraries:
    info = libraries['92235.80c']
    print(f"U-235: {info['filename']}, T={info['temperature_k']:.1f} K")
```

## Common xsdir Issues

### Issue 1: Corrupted xsdir
**Symptoms:** Multiple "cross-section not found" errors, AWR = 0

**Fix:** Regenerate xsdir from scratch using MCNP tools

### Issue 2: Missing Entries
**Symptoms:** Specific isotopes not found

**Check:**
```bash
# Verify data file exists
ls $DATAPATH/endf80/U/92235.800nc

# If file exists but not in xsdir, add entry manually or regenerate
```

### Issue 3: Path Issues
**Symptoms:** MCNP can't open files even though xsdir looks correct

**Fix:** Ensure paths in xsdir are relative to DATAPATH, not absolute

### Issue 4: Mixed Line Endings
**Symptoms:** Parse errors, unexpected behavior on Windows/Linux

**Fix:** Convert line endings (dos2unix or unix2dos as needed)

## xsdir Maintenance

### Backup
```bash
# Always backup before modifications
cp $DATAPATH/xsdir $DATAPATH/xsdir.backup
```

### Combining Multiple Libraries
```bash
# Merge two xsdir files
# 1. Copy header from primary xsdir
# 2. Append entries from secondary (avoiding duplicates)
# 3. Verify no duplicate ZAIDs
```

### Verifying Integrity
```python
def verify_xsdir_integrity(xsdir_path, datapath):
    """Check that all files referenced in xsdir exist"""
    errors = []

    libraries = parse_xsdir(xsdir_path)

    for zaid, info in libraries.items():
        filepath = os.path.join(datapath, info['filename'])
        if not os.path.exists(filepath):
            errors.append(f"{zaid}: File not found - {filepath}")

    if errors:
        print(f"Found {len(errors)} missing files:")
        for error in errors:
            print(f"  {error}")
    else:
        print(f"All {len(libraries)} library files verified ✓")

    return len(errors) == 0
```

## Best Practices

1. **Never Hand-Edit xsdir** - Use MCNP tools to regenerate
2. **Keep Backups** - Before any library changes
3. **Verify After Updates** - Check critical ZAIDs still available
4. **Document Changes** - Note any manual modifications
5. **Test Access** - Run simple test case after xsdir changes
6. **Use Version Control** - Track xsdir changes over time
7. **Consistent Paths** - Keep paths relative to DATAPATH
8. **Check File Permissions** - Ensure MCNP can read all referenced files

## Diagnostic Checklist

When troubleshooting library issues:

- [ ] DATAPATH set and correct
- [ ] xsdir file exists at DATAPATH location
- [ ] xsdir file readable (permissions)
- [ ] ZAID exists in xsdir
- [ ] Referenced data file exists
- [ ] File path correct relative to DATAPATH
- [ ] No special characters or spaces in paths
- [ ] Line endings correct for platform
- [ ] AWR non-zero and reasonable
- [ ] Temperature appropriate for application

---

**See also:**
- `library_types.md` - Detailed library type reference
- `temperature_libraries.md` - Temperature-dependent data guide
- `troubleshooting_libraries.md` - Error diagnosis procedures

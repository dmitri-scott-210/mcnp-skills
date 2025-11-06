# MCNP Cross-Section Manager - Python Tools

This directory contains Python tools for managing, querying, and troubleshooting MCNP cross-section libraries.

## Overview

These tools help you:
- Parse and query xsdir files
- Find available libraries for isotopes
- Diagnose missing library errors
- Verify DATAPATH and library installation
- Get alternative library recommendations

## Requirements

- Python 3.6+
- No external dependencies (uses stdlib only)
- MCNP cross-section data installed
- DATAPATH environment variable set (or provide path explicitly)

## Tools

### 1. xsdir_parser.py

Parse and query MCNP xsdir files.

**Features:**
- Find specific ZAIDs
- Search by pattern
- List by section (directory, thermal, photoatomic, etc.)
- Extract library statistics
- Interactive and command-line modes

**Usage:**

```bash
# Interactive mode
python xsdir_parser.py

# Find specific ZAID
python xsdir_parser.py --zaid "92235.80c"

# Search for uranium isotopes
python xsdir_parser.py --search "^92"

# List thermal scattering tables
python xsdir_parser.py --list-section thermal

# Show statistics
python xsdir_parser.py --statistics
```

**Interactive commands:**
```
xsdir> find 92235.80c         # Find U-235 ENDF/B-VIII.0
xsdir> search 92              # Search uranium isotopes
xsdir> isotope 92 235         # Find all U-235 libraries
xsdir> section thermal        # List thermal tables
xsdir> stats                  # Show statistics
```

**Example output:**
```
ZAID: 92235.80c
Section: directory
Atomic Weight Ratio: 235.043930
Filename: endf80/U/92235.800nc
Temperature: 293.6 K (2.5301e-08 MeV)
Z = 92, A = 235
Library: .80c
```

---

### 2. library_finder.py

Find available libraries for isotopes and recommend alternatives.

**Features:**
- Find all libraries for an isotope
- List all isotopes of an element
- Check ZAID availability
- Recommend alternatives for missing libraries
- Interactive and command-line modes

**Usage:**

```bash
# Interactive mode
python library_finder.py

# Find libraries for U-235
python library_finder.py --isotope "U-235"

# Find all uranium isotopes
python library_finder.py --element 92

# Check if ZAID available
python library_finder.py --check "92235.80c"

# Get recommendations
python library_finder.py --recommend "92235.70c"
```

**Interactive commands:**
```
library> isotope U-235        # Find U-235 libraries
library> element 92           # Find all uranium isotopes
library> check 92235.80c      # Check availability
library> recommend 92235.70c  # Get alternatives
```

**Example output:**
```
Isotope: U-235 (Z=92)
Available libraries:

  Continuous energy (.??c):
    92235.80c
    92235.81c
    92235.82c
    92235.70c
    92235.66c

  Discrete energy (.??d):
    92235.80d
```

**Recommendation output:**
```
Requested: 92235.70c
Status: NOT FOUND ✗

Recommended alternatives:
  1. 92235.80c
     Reason: Alternative library version (.80c)
  2. 92000.80c
     Reason: Natural U mix (includes all isotopes)
```

---

### 3. missing_library_diagnoser.py

Diagnose and troubleshoot cross-section library errors.

**Features:**
- Verify DATAPATH and xsdir setup
- Diagnose MCNP error messages
- Check input files for missing libraries
- Provide systematic troubleshooting steps
- Interactive and command-line modes

**Usage:**

```bash
# Interactive mode
python missing_library_diagnoser.py

# Verify setup
python missing_library_diagnoser.py --verify-setup

# Diagnose error
python missing_library_diagnoser.py --error "cross-section table 92235.80c not found"

# Check input file
python missing_library_diagnoser.py --input input.i
```

**Interactive commands:**
```
diagnose> verify              # Verify library setup
diagnose> diagnose <error>    # Diagnose error message
diagnose> check input.i       # Check input file
```

**Setup verification output:**
```
Setup Verification:
============================================================

Passed checks:
  ✓ DATAPATH set: /opt/mcnpdata
  ✓ DATAPATH directory exists
  ✓ xsdir file found
  ✓ xsdir file readable
  ✓ xsdir size: 2,456,789 bytes
```

**Error diagnosis output:**
```
Diagnosis:
============================================================
Error type: ZAID_NOT_FOUND
ZAID: 92235.80c

Problem: Cross-section table 92235.80c not found in xsdir

Possible causes:
  1. DATAPATH not set or incorrect
  2. 92235.80c not in xsdir file (library not installed)
  3. Wrong library version specified
  4. xsdir file corrupted or incomplete

Recommended fixes:
  1. Check if DATAPATH set: echo $DATAPATH
  2. Search xsdir for 92235.80c: grep '92235.80c' $DATAPATH/xsdir
  3. Try alternative library version (e.g., .70c instead of .80c)
  4. Use natural element (e.g., 92000.80c for natural uranium)
  5. Verify library installation is complete
```

**Input file check output:**
```
Input file: input.i
Total ZAIDs: 15
Available: 12
Missing: 3

Missing ZAIDs:
  ✗ 92235.70c
  ✗ 94239.70c
  ✗ 8017.80c

Recommendations:
  1. Use 'diagnose' command for each missing ZAID
  2. Check alternative library versions
  3. Use natural element mix if specific isotope unavailable
```

---

## Common Workflows

### Workflow 1: Verify Library Setup

```bash
# Step 1: Verify DATAPATH
python missing_library_diagnoser.py --verify-setup

# Step 2: Check xsdir statistics
python xsdir_parser.py --statistics

# Step 3: Test common isotopes
python library_finder.py --check "1001.80c"  # H-1
python library_finder.py --check "8016.80c"  # O-16
python library_finder.py --check "92235.80c" # U-235
```

### Workflow 2: Prepare MCNP Input

```bash
# Step 1: Find available libraries for isotopes
python library_finder.py --isotope "U-235"
python library_finder.py --isotope "Pu-239"

# Step 2: Check thermal scattering libraries
python xsdir_parser.py --list-section thermal

# Step 3: Verify all ZAIDs in input
python missing_library_diagnoser.py --input input.i
```

### Workflow 3: Debug MCNP Error

```bash
# Step 1: Copy error from MCNP output
# Example: "fatal error.  cross-section table 92235.80c not found."

# Step 2: Diagnose error
python missing_library_diagnoser.py --error "cross-section table 92235.80c not found"

# Step 3: Get alternatives
python library_finder.py --recommend "92235.80c"

# Step 4: Verify alternative available
python library_finder.py --check "92235.70c"
```

### Workflow 4: Explore Element Libraries

```bash
# Step 1: Find all isotopes of uranium
python library_finder.py --element 92

# Step 2: Get details for specific isotope
python xsdir_parser.py --search "92235"

# Step 3: Check temperature libraries
python xsdir_parser.py --zaid "92235.80c"
python xsdir_parser.py --zaid "92235.81c"
python xsdir_parser.py --zaid "92235.82c"
```

---

## Error Types Diagnosed

### 1. ZAID_NOT_FOUND
```
cross-section table 92235.80c not found
```
**Causes:** DATAPATH wrong, library not installed, wrong version
**Fixes:** Check DATAPATH, try .70c/.66c, use natural element

### 2. CANNOT_OPEN_FILE
```
cannot open file /path/to/92235.800nc
```
**Causes:** File missing, path wrong, permissions, network issue
**Fixes:** Check file exists, verify DATAPATH, check permissions

### 3. AWR_ZERO
```
atomic weight ratio (AWR) is zero
```
**Causes:** xsdir corrupted, edited incorrectly
**Fixes:** Restore backup, regenerate xsdir, reinstall

### 4. TEMPERATURE_OUT_OF_RANGE
```
temperature 2000.0 K out of range for 92235.80c
```
**Causes:** TMP too high, temperature library not installed
**Fixes:** Use .81c/.82c/.83c, accept default, remove TMP

---

## Environment Setup

### Linux/Mac

**Temporary (current session):**
```bash
export DATAPATH=/opt/mcnpdata
```

**Permanent (user):**
```bash
echo 'export DATAPATH=/opt/mcnpdata' >> ~/.bashrc
source ~/.bashrc
```

**Permanent (system-wide):**
```bash
# /etc/environment
DATAPATH=/opt/mcnpdata
```

### Windows

**Temporary (current session):**
```cmd
set DATAPATH=C:\mcnpdata
```

**Permanent (user):**
```cmd
setx DATAPATH "C:\mcnpdata"
```

**Permanent (system-wide):**
```cmd
setx DATAPATH "C:\mcnpdata" /M
```

**GUI Method:**
1. Right-click "This PC" → Properties
2. Advanced system settings
3. Environment Variables
4. New → Variable: DATAPATH, Value: C:\mcnpdata
5. OK, Apply, Restart terminal

---

## Troubleshooting

### "DATAPATH not set"

**Problem:** Tools can't find xsdir file

**Solution:**
```bash
# Linux/Mac
export DATAPATH=/path/to/mcnpdata

# Windows
set DATAPATH=C:\path\to\mcnpdata

# Or provide explicit path
python xsdir_parser.py --xsdir /path/to/xsdir
```

### "xsdir file not found"

**Problem:** xsdir doesn't exist at DATAPATH/xsdir

**Solution:**
```bash
# Verify DATAPATH
echo $DATAPATH  # Linux
echo %DATAPATH% # Windows

# Check xsdir location
ls $DATAPATH/xsdir      # Linux
dir %DATAPATH%\xsdir    # Windows

# If wrong, correct DATAPATH or reinstall libraries
```

### "No ZAIDs found in input file"

**Problem:** ZAID pattern not matching

**Solution:**
- Verify ZAIDs use correct format: ZZZAAA.nnX
- Check for commented-out material cards
- Ensure material cards not in title/comment block

---

## Integration with MCNP Workflow

### Pre-simulation checks:
```bash
# 1. Verify setup
python missing_library_diagnoser.py --verify-setup

# 2. Check input file
python missing_library_diagnoser.py --input input.i

# 3. If missing libraries, get alternatives
python library_finder.py --recommend "92235.70c"
```

### Post-error diagnosis:
```bash
# 1. Copy error from output file
grep "fatal error" output.o

# 2. Diagnose
python missing_library_diagnoser.py --error "<error message>"

# 3. Find alternatives
python library_finder.py --recommend "<missing zaid>"

# 4. Verify alternative exists
python library_finder.py --check "<alternative zaid>"
```

---

## Advanced Usage

### Batch checking multiple ZAIDs:
```bash
for zaid in 1001.80c 6000.80c 8016.80c 92235.80c 92238.80c; do
    python library_finder.py --check "$zaid"
done
```

### Finding temperature libraries:
```bash
# Search for all U-235 temperature variants
python xsdir_parser.py --search "92235\.8[0-9]c"
```

### Generating library inventory:
```bash
# List all available ZAIDs
python xsdir_parser.py --list-all > available_zaids.txt

# Count by library type
python xsdir_parser.py --statistics
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Verify setup | `python missing_library_diagnoser.py --verify-setup` |
| Find ZAID | `python xsdir_parser.py --zaid "92235.80c"` |
| Search pattern | `python xsdir_parser.py --search "^92"` |
| Check input | `python missing_library_diagnoser.py --input input.i` |
| Find isotope | `python library_finder.py --isotope "U-235"` |
| Get alternatives | `python library_finder.py --recommend "92235.70c"` |
| List thermal | `python xsdir_parser.py --list-section thermal` |
| Statistics | `python xsdir_parser.py --statistics` |
| Diagnose error | `python missing_library_diagnoser.py --error "<msg>"` |

---

## Support

For issues or questions:
1. Verify DATAPATH is set correctly
2. Check xsdir file exists and is readable
3. Review MCNP documentation for library installation
4. Use interactive mode for guided troubleshooting

---

**See also:**
- `../xsdir_format.md` - xsdir file structure
- `../library_types.md` - Library type reference
- `../troubleshooting_libraries.md` - Detailed troubleshooting procedures
- `../temperature_libraries.md` - Temperature library guide

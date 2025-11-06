# Cross-Section Library Troubleshooting Guide

## Overview

This guide provides systematic procedures for diagnosing and resolving MCNP cross-section library errors. Follow decision trees for common error messages and library issues.

## Common Error Messages

### Error 1: "cross-section table (ZAID) not found"

**Example:**
```
fatal error.  cross-section table 92235.80c not found.
              table = 92235.80c
```

**Diagnostic Procedure:**

**Step 1: Check DATAPATH**
```bash
# Linux/Mac
echo $DATAPATH
ls $DATAPATH/xsdir

# Windows
echo %DATAPATH%
dir %DATAPATH%\xsdir

# If empty or wrong: Set DATAPATH
export DATAPATH=/path/to/mcnpdata  # Linux
set DATAPATH=C:\mcnpdata           # Windows
```

**Step 2: Check xsdir**
```bash
# Search for ZAID
grep "^92235.80c " $DATAPATH/xsdir

# If not found: Try different version
grep "92235" $DATAPATH/xsdir
```

**Step 3: Solutions**

```
Option A: Use available version
Result: 92235.70c found
Action: Change input to use .70c

Option B: Use natural element
Check: grep "92000" $DATAPATH/xsdir
Action: Use 92000.80c (natural uranium)

Option C: Verify file exists
Check: ls $DATAPATH/endf80/U/92235.800nc
If missing: Library installation incomplete
```

---

### Error 2: "cannot open file"

**Example:**
```
bad trouble in subroutine rdcont
opened library file /path/to/92235.800nc
cannot open file /path/to/92235.800nc
```

**Diagnostic Procedure:**

**Step 1: Verify path**
```bash
# Check if file exists at reported path
ls /path/to/92235.800nc

# Check xsdir entry
grep "92235.80c" $DATAPATH/xsdir
# Verify filename field matches actual location
```

**Step 2: Check permissions**
```bash
# Linux: Verify read permissions
ls -l $DATAPATH/endf80/U/92235.800nc
# Should show: -r--r--r-- or -rw-r--r--

# If no permission: Fix
chmod +r $DATAPATH/endf80/U/92235.800nc
```

**Step 3: Common causes**

```
1. DATAPATH incorrect
   - xsdir paths relative to DATAPATH
   - Set DATAPATH to directory containing xsdir

2. File actually missing
   - Incomplete installation
   - Corrupted download
   - Deleted file

3. Path separator issues (Windows)
   - Use backslash or forward slash consistently
   - No spaces in paths

4. Network drive issues
   - Permissions on network storage
   - Connection dropped during access
```

---

### Error 3: "atomic weight ratio (AWR) is zero"

**Example:**
```
fatal error. atomic weight ratio (AWR) is zero.
             zaid = 92235.80c  awr = 0.0000000
```

**Diagnostic Procedure:**

**Step 1: Check xsdir entry**
```bash
grep "92235.80c" $DATAPATH/xsdir
# Check second field (AWR)
# Should be: 92235.80c  235.04393 ...
```

**Step 2: Corrupted xsdir**
```
Symptoms: AWR = 0.0, wrong value, or parse error
Cause: xsdir edited improperly or corrupted

Fix: Regenerate xsdir from backup or reinstall
```

**Step 3: Solutions**

```
Option A: Restore from backup
cp $DATAPATH/xsdir.backup $DATAPATH/xsdir

Option B: Fix entry manually (RISKY)
Edit xsdir, correct AWR from reference
U-235 AWR should be 235.04393

Option C: Regenerate xsdir
Use MCNP tools to rebuild from library files
```

---

### Error 4: "temperature (T) out of range"

**Example:**
```
warning. temperature 2000.0 K out of range for 92235.80c
         using 293.6 K cross sections
```

**Diagnostic Procedure:**

**Step 1: Check TMP card**
```
TMP  2000   $ 2000 K requested
```

**Step 2: Check library availability**
```bash
# What temperatures available for U-235?
grep "92235" $DATAPATH/xsdir | awk '{print $1, $NF}'

# Convert kT (MeV) to Kelvin:
# T(K) = kT(MeV) / 8.617333E-11
```

**Step 3: Solutions**

```
Option A: Use higher temperature library
M1  92235.84c  1.0     $ 2500 K library
TMP  2000              $ Interpolate down to 2000 K

Option B: Use highest available
M1  92235.83c  1.0     $ 1200 K library
TMP  2000              $ MCNP extrapolates (less accurate)

Option C: Accept warning
If temperature effect minor: Use default
Document in comments
```

---

## Diagnostic Decision Tree

```
MCNP library error occurred
    │
    ├─> Error message contains "not found"
    │   ├─> Check DATAPATH set correctly
    │   ├─> Search xsdir for ZAID
    │   ├─> Try alternative version (.70c, .66c)
    │   └─> Use natural element or omit if minor
    │
    ├─> Error message contains "cannot open"
    │   ├─> Verify file exists at path in xsdir
    │   ├─> Check read permissions
    │   ├─> Confirm DATAPATH correct
    │   └─> Test with absolute path
    │
    ├─> Error message contains "AWR is zero"
    │   ├─> Check xsdir entry for ZAID
    │   ├─> Restore xsdir from backup
    │   └─> Regenerate xsdir if corrupted
    │
    ├─> Error message contains "temperature"
    │   ├─> Check available temperature libraries
    │   ├─> Use closest library + TMP
    │   └─> Accept interpolation/extrapolation
    │
    └─> Other library errors
        └─> See specific error sections below
```

---

## Specific Library Issues

### Thermal Scattering Not Available

**Symptom:** keff significantly different from expected

**Diagnosis:**
```bash
# Check if thermal library in xsdir
grep "lwtr.80t" $DATAPATH/xsdir

# If missing: Thermal scattering not installed
```

**Solutions:**
```
Option A: Install thermal libraries
Download and install S(α,β) library package

Option B: Use free-gas approximation
Remove MT card
Results less accurate for thermal systems

Option C: Use different moderator
Change problem to material with available S(α,β)
```

---

### Mixed Library Versions

**Symptom:** Inconsistent physics, unexpected results

**Diagnosis:**
```
M1  92235.80c  ...     $ ENDF/B-VIII.0
    92238.70c  ...     $ ENDF/B-VII.0 (MIXED!)
    8016.80c   ...     $ ENDF/B-VIII.0
```

**Fix:**
```
Standardize on one version:

M1  92235.80c  ...     $ All ENDF/B-VIII.0
    92238.80c  ...     $ Consistent version
    8016.80c   ...     $ Same library
```

---

### Photon Production Data Missing

**Warning:**
```
warning.  nuclide 43099 does not have photon production data.
```

**Diagnosis:**
```
For MODE N P (coupled transport):
Some isotopes lack photon production cross sections
```

**Solutions:**
```
Option A: Accept warning
If photon contribution from isotope negligible

Option B: Try different library version
Check if .70c has photon production:
grep "43099" $DATAPATH/xsdir

Option C: Remove MODE P
If photons not critical to problem

Option D: Use separate calculations
Run neutron transport, then photon transport
```

---

## DATAPATH Configuration

### Linux/Mac Setup

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

**Verify:**
```bash
echo $DATAPATH
ls $DATAPATH/xsdir
```

### Windows Setup

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

**Verify:**
```cmd
echo %DATAPATH%
dir %DATAPATH%\xsdir
```

### GUI Method (Windows)
```
1. Right-click "This PC" → Properties
2. Advanced system settings
3. Environment Variables
4. New (User or System)
5. Variable: DATAPATH
6. Value: C:\mcnpdata
7. OK, Apply
8. Restart terminal
```

---

## Library Installation Issues

### Incomplete Installation

**Symptoms:**
- Many cross sections missing
- Errors for common isotopes (H-1, O-16)
- xsdir exists but small

**Diagnosis:**
```bash
# Check xsdir size
ls -lh $DATAPATH/xsdir
# Should be 1-5 MB typically

# Count entries
grep "\.80c" $DATAPATH/xsdir | wc -l
# Should be 300-500+ for complete library
```

**Fix:**
```
1. Re-download library package
2. Verify download integrity (checksum)
3. Extract completely
4. Regenerate xsdir if needed
```

### Corrupted Downloads

**Symptoms:**
- Binary data appears corrupted
- AWR values wrong or zero
- Unexpected EOF errors

**Fix:**
```
1. Verify file checksums (MD5/SHA256)
2. Re-download from official source
3. Check disk space during extraction
4. Use reliable network connection
```

---

## xsdir Maintenance

### Backup Before Changes
```bash
cp $DATAPATH/xsdir $DATAPATH/xsdir.backup.$(date +%Y%m%d)
```

### Verify Integrity
```bash
# Check for duplicate ZAIDs
awk '{print $1}' $DATAPATH/xsdir | sort | uniq -d

# Check for zero AWR
awk '$2 == 0.0 {print $1}' $DATAPATH/xsdir

# Verify file references exist
while read line; do
    zaid=$(echo $line | awk '{print $1}')
    file=$(echo $line | awk '{print $3}')
    if [ ! -f "$DATAPATH/$file" ]; then
        echo "Missing: $zaid -> $file"
    fi
done < <(grep "\.80c" $DATAPATH/xsdir)
```

### Merge Libraries
```bash
# Combine two xsdir files (ADVANCED)
# 1. Copy primary xsdir
cp xsdir1 xsdir_merged

# 2. Append unique entries from secondary
grep -v "^#" xsdir2 | while read line; do
    zaid=$(echo $line | awk '{print $1}')
    if ! grep -q "^$zaid " xsdir_merged; then
        echo "$line" >> xsdir_merged
    fi
done
```

---

## Validation Tests

### Quick Test
```bash
# Create minimal test input
cat > test.inp <<EOF
Test cross section access
1  1  -1.0  -1
2  0       1

1  so 10

MODE N
M1  1001.80c  1.0
KCODE 1000 1.0 10 50
KSRC 0 0 0
EOF

# Run MCNP
mcnp6 i=test.inp tasks 1

# Check for library errors in output
grep -i "not found\|cannot open" test.o
```

### Comprehensive Test
```python
def validate_library_installation(datapath):
    """Test common isotopes"""
    test_zaids = [
        '1001.80c',  # H-1
        '6000.80c',  # C
        '8016.80c',  # O-16
        '26000.80c', # Fe
        '92235.80c', # U-235
        '92238.80c', # U-238
        'lwtr.80t',  # Light water
    ]

    xsdir_path = os.path.join(datapath, 'xsdir')
    issues = []

    for zaid in test_zaids:
        # Check in xsdir
        found = False
        with open(xsdir_path, 'r') as f:
            for line in f:
                if line.startswith(zaid):
                    found = True
                    # Check file exists
                    filename = line.split()[2]
                    filepath = os.path.join(datapath, filename)
                    if not os.path.exists(filepath):
                        issues.append(f"{zaid}: Entry in xsdir but file missing")
                    break

        if not found:
            issues.append(f"{zaid}: Not in xsdir")

    return issues
```

---

## Emergency Procedures

### If All Libraries Fail

1. **Verify MCNP Installation**
   ```bash
   which mcnp6
   mcnp6 --version
   ```

2. **Check Example Problems**
   ```bash
   cd $MCNP_HOME/examples
   mcnp6 i=basic_example.inp
   ```

3. **Reinstall Libraries**
   - Download fresh copy
   - Extract to clean directory
   - Set DATAPATH
   - Test with example

4. **Contact Support**
   - Provide MCNP version
   - OS and environment details
   - xsdir head/tail
   - Complete error messages

---

**See also:**
- `xsdir_format.md` - xsdir file structure
- `library_types.md` - Library types and usage
- `temperature_libraries.md` - Temperature-specific issues

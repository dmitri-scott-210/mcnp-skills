# TR Card Error Catalog and Troubleshooting

## Error 1: Non-Orthogonal Rotation Matrix

### Symptoms
- MCNP warning: "transformation matrix not orthonormal"
- MCNP fatal error during geometry initialization
- Unexpected geometry distortions

### Cause
Rotation matrix rows are not unit vectors or not mutually perpendicular.

### Common Mistakes

**Bad Example 1: Non-unit row**
```
*TR1  0 0 0  1 0 0  0 2 0  0 0 1    $ Row 2 has length 2, not 1
```

**Bad Example 2: Non-perpendicular rows**
```
*TR2  0 0 0  1 1 0  0 1 0  0 0 1    $ Row1·Row2 ≠ 0
```

**Bad Example 3: Typo in matrix**
```
*TR3  0 0 0  0.707 -0.707 0  0.707 0.707 0  0 0 2  $ Last element should be 1
```

### Detection

**Method 1: Manual verification**
```
For matrix:
*TR1  0 0 0  a11 a12 a13  a21 a22 a23  a31 a32 a33

Check:
1. ||row1|| = √(a11² + a12² + a13²) = 1 ?
2. ||row2|| = √(a21² + a22² + a23²) = 1 ?
3. ||row3|| = √(a31² + a32² + a33²) = 1 ?
4. row1·row2 = a11·a21 + a12·a22 + a13·a23 = 0 ?
5. row1·row3 = a11·a31 + a12·a32 + a13·a33 = 0 ?
6. row2·row3 = a21·a31 + a22·a32 + a23·a33 = 0 ?
```

**Method 2: Use validation script**
```bash
python scripts/tr_matrix_validator.py
```

### Fix

**Step 1:** Identify the problem (which row is wrong, which orthogonality fails)

**Step 2:** Correct the matrix
- If one row has wrong norm: normalize it (divide by its length)
- If rows not perpendicular: likely transcription error, recalculate from rotation definition

**Example Fix:**
```
Bad:  *TR1  0 0 0  1 0 0  0 2 0  0 0 1
Good: *TR1  0 0 0  1 0 0  0 1 0  0 0 1   $ Normalized row 2
```

### Prevention

- Always generate matrices from known formulas (Euler angles, axis-angle)
- Use scripts/rotation_matrix_generator.py for complex rotations
- Validate with tr_matrix_validator.py before running MCNP
- When entering matrices manually, double-check each element

---

## Error 2: Wrong Transformation Direction

### Symptoms
- Geometry appears at wrong location
- Component mirrored or inverted
- Particle tracks show unexpected positions

### Cause
Confusion between forward and inverse transformations, or misunderstanding of how MCNP applies TR cards.

### Common Mistakes

**Bad Example 1: Reversed translation**
```
c Goal: Move sphere from origin to (10, 0, 0)
c Mistake: Using negative translation
*TR1  -10 0 0    $ WRONG - sphere ends up at (-10, 0, 0)
10 1 SO 5.0
```

**Bad Example 2: Inverted rotation**
```
c Goal: Rotate component 90° CCW about z
c Mistake: Using CW rotation matrix
*TR1  0 0 0  0 1 0  -1 0 0  0 0 1    $ WRONG - rotates CW, not CCW
```

### Detection

**Method 1: Geometry plotter**
```
Run MCNP with plotting:
mcnp6 i=input.i ip
```
Visually verify component position/orientation matches intent.

**Method 2: Test case**
```
c Test with simple geometry at known position
999  1  SO  1.0    $ Sphere at (1,0,0) with TR1
c Check output geometry plot
```

### Fix

**For surface transformations:**
Translation vector points FROM origin TO desired location
```
Correct: *TR1  10 0 0    $ Move to x=+10
```

**For rotations:**
Use right-hand rule (CCW positive looking down axis toward origin)
```
c 90° CCW about z:
*TR1  0 0 0  0 -1 0  1 0 0  0 0 1    $ Correct

c 90° CW about z (same as -90° or 270° CCW):
*TR2  0 0 0  0 1 0  -1 0 0  0 0 1
```

**For TRCL transformations:**
The filled universe's origin is placed at the specified translation with specified orientation.

### Prevention

- Test transformations on simple geometry first (sphere, box)
- Use geometry plotter before full simulation
- Check signs carefully when entering translation vectors
- For rotations, visualize right-hand rule

---

## Error 3: Mixing Surface TR and Cell TRCL

### Symptoms
- Component appears at unexpected location
- Geometry doubled or missing
- "Lost particle" errors

### Cause
Applying transformation twice: once via surface number, once via TRCL parameter.

### Common Mistakes

**Bad Example: Double transformation**
```
*TR1  10 0 0
10 1 SO 5.0                      $ Surface uses TR1 (transforms to x=10)
1  1  -1.0  -10  TRCL=1  IMP:N=1  $ Cell ALSO uses TR1 (double transformation!)
```
Result: Sphere ends up at x=20 (transformed twice)

**Bad Example: Conflicting transformations**
```
*TR1  10 0 0
*TR2  0 10 0
10 2 SO 5.0                      $ Surface uses TR2
1  1  -1.0  -10  TRCL=1  IMP:N=1  $ Cell uses different TR1
```
Result: Confusing geometry, hard to debug

### Detection

**Warning signs:**
- Surfaces with transformation number (second field ≠ 0)
- Same surfaces referenced in cells with TRCL parameter
- Geometry plots showing components at wrong scale or position

**Systematic check:**
```
1. List all surfaces using TR: grep "^\s*[0-9]+ [1-9]" input.i
2. List all cells with TRCL: grep "TRCL=" input.i
3. Verify no overlap in surface usage
```

### Fix

**Choose one approach:**

**Option 1: Transform surface only**
```
*TR1  10 0 0
10 1 SO 5.0              $ Surface transformed to x=10
1  1  -1.0  -10  IMP:N=1  $ Cell uses surface 10 as-is, no TRCL
```

**Option 2: Transform cell contents only**
```
*TR1  10 0 0
10 SO 5.0                           $ Surface defined at origin
1  1  -1.0  -10  TRCL=1  IMP:N=1    $ Cell FILL uses TR1
```

**When to use which:**
- **Surface TR:** Simple repositioning of surfaces
- **Cell TRCL:** Placing filled universes with orientation

### Prevention

- Establish convention: use surface TR OR TRCL, not both
- Document which approach is used for each component
- Use TRCL primarily for FILL operations (universes)
- Use surface TR for simple geometric repositioning

---

## Error 4: Transformation Number Conflicts

### Symptoms
- Geometry changes unexpectedly when editing file
- MCNP warning about duplicate TR definitions
- Components appear in wrong locations

### Cause
Same transformation number (TRn) defined multiple times with different parameters.

### Common Mistakes

**Bad Example: Duplicate TR number**
```
*TR1  10 0 0  1 0 0  0 1 0  0 0 1    $ TR1 defined
...
*TR1  0 10 0  1 0 0  0 1 0  0 0 1    $ TR1 redefined! Only second is used
```

**Bad Example: Unintended overwrite**
```
c File created by merging two inputs
c From input1.i:
*TR5  5 0 0
c From input2.i:
*TR5  0 5 0    $ Conflict! Same number, different transformation
```

### Detection

**Automated check:**
```bash
# Find duplicate TR numbers
grep "^\*TR" input.i | awk '{print $1}' | sort | uniq -d
```

**MCNP output:**
Check for warnings about "transformation redefined" or "duplicate TR number"

### Fix

**Renumber conflicting transformations:**
```
Original (bad):
*TR1  10 0 0
...
*TR1  0 10 0    $ Conflict

Fixed (good):
*TR1  10 0 0
...
*TR2  0 10 0    $ Different number
```

**Update all references:**
```
If renumbering TR5 → TR15:
1. Change *TR5 → *TR15
2. Update all surface cards using TR5
3. Update all TRCL=5 → TRCL=15
```

### Prevention

- Number transformations systematically (e.g., TR1-10 for fuel, TR11-20 for control rods)
- Comment TR cards with purpose:
  ```
  *TR1  10 0 0    $ Fuel assembly position 1
  *TR2  20 0 0    $ Fuel assembly position 2
  ```
- When merging inputs, check for TR number conflicts first
- Use scripts to auto-number TRs in large files

---

## Error 5: Lost Particles Due to Transformation

### Symptoms
- Fatal error: "lost particle" after adding transformation
- Geometry appears valid in plotter but simulation fails
- Particle tracks show gaps or overlaps

### Cause
Transformation creates geometry overlap, void, or inconsistency that particle tracking cannot handle.

### Common Causes

**Cause 1: Transformed geometry overlaps existing geometry**
```
c Original cell 1 at origin
1  1  -1.0  -10  IMP:N=1

c Transformed cell 2 overlaps cell 1
*TR1  1 0 0    $ Only 1 cm offset - likely overlaps
2  1  -1.0  -20  TRCL=1  IMP:N=1
```

**Cause 2: Non-orthogonal matrix distorts geometry**
```
*TR1  0 0 0  1.1 0 0  0 1 0  0 0 1    $ Row 1 not unit length
c Distorts geometry, creates overlaps
```

**Cause 3: Reflection creates improper geometry**
```
*TR1  0 0 0  -1 0 0  0 -1 0  0 -1 1    $ Typo: should be 0 0 1
c Invalid matrix causes geometry errors
```

### Detection

**Step 1: Validate transformation matrix**
```bash
python scripts/tr_matrix_validator.py
# Check determinant ≈ ±1
# Check orthonormality
```

**Step 2: Test transformation isolation**
```
1. Comment out all other geometry
2. Keep only the transformed component
3. Run geometry plot
4. Verify no errors
5. Gradually add back other geometry
```

**Step 3: Check geometry with plotter**
```
mcnp6 i=input.i ip

In plotter:
- Look for overlaps (red regions)
- Check voids (black regions)
- Verify transformations visual makes sense
```

### Fix

**Fix 1: Correct transformation matrix**
```
Bad:  *TR1  0 0 0  1.1 0 0  0 1 0  0 0 1
Good: *TR1  0 0 0  1.0 0 0  0 1 0  0 0 1
```

**Fix 2: Adjust translation to avoid overlaps**
```
Bad:  *TR1  1 0 0     $ Too close
Good: *TR1  15 0 0    $ Sufficient separation
```

**Fix 3: Fix matrix determinant**
```
c Check:
import numpy as np
R = np.array([[a11, a12, a13],
              [a21, a22, a23],
              [a31, a32, a33]])
det = np.linalg.det(R)
# Should be ≈ 1.0 or -1.0

c If det ≠ ±1, recalculate matrix from rotation definition
```

### Prevention

- Always validate matrices before use (tr_matrix_validator.py)
- Test transformations on simple geometry first
- Use geometry plotter extensively during development
- Maintain adequate spacing between transformed components
- Check determinant: must be ±1 (exactly, within numerical precision)

---

## Error 6: Incorrect Euler Angle Interpretation

### Symptoms
- Geometry rotated incorrectly when using degree input mode (m=1)
- Component orientation doesn't match expectation
- Need to try multiple angle combinations to get desired result

### Cause
Misunderstanding MCNP's Euler angle convention (rotation order and direction).

### MCNP Euler Angle Convention

**Format:**
```
*TRn  dx dy dz  θx θy θz  1
```

**Rotation order:** Rx(θx) · Ry(θy) · Rz(θz)
- First rotate about x-axis by θx
- Then rotate about (rotated) y-axis by θy
- Finally rotate about (twice-rotated) z-axis by θz

**Direction:** Positive angle = counterclockwise looking down axis toward origin (right-hand rule)

### Common Mistakes

**Bad Assumption 1: Wrong rotation order**
```
c User thinks: "I'll rotate about z first, then y"
c Reality: MCNP rotates about x, then y, then z (fixed order)
*TR1  0 0 0  0 45 90  1    $ Not "z then y", but "x(0°), y(45°), z(90°)"
```

**Bad Assumption 2: Wrong angle convention**
```
c User thinks: "Positive z rotation is clockwise"
c Reality: Positive is CCW (right-hand rule)
*TR1  0 0 0  0 0 90  1     $ 90° CCW, not CW
```

**Bad Assumption 3: Gimbal lock confusion**
```
c When θy = ±90°, rotation about x and z become equivalent (gimbal lock)
*TR1  0 0 0  45 90 45  1   $ θx and θz rotations are degenerate
```

### Detection

**Test with single-axis rotations:**
```
*TR1  0 0 0  90 0 0  1    $ Rotate about x only
*TR2  0 0 0  0 90 0  1    $ Rotate about y only
*TR3  0 0 0  0 0 90  1    $ Rotate about z only
```

Plot with known geometry (e.g., rectangular box) and verify orientation.

**Convert to explicit matrix and verify:**
```
Use scripts/rotation_matrix_generator.py to see the actual matrix generated:

python scripts/rotation_matrix_generator.py --euler 30 45 60

Compare to expected orientation.
```

### Fix

**Solution 1: Use single-axis rotations when possible**
```
c Instead of: *TR1  0 0 0  30 45 60  1
c Use: *TR1  0 0 0  0 0 90  1    $ Single z-axis rotation (if appropriate)
```

**Solution 2: Convert to explicit matrix**
```
c Calculate matrix from desired orientation
c Use scripts/rotation_matrix_generator.py
c Specify matrix directly instead of Euler angles
*TR1  0 0 0  0.866 -0.5 0  0.5 0.866 0  0 0 1    $ Explicit 30° z rotation
```

**Solution 3: Use axis-angle (Rodrigues)**
```
c For rotation about arbitrary axis
c Use scripts/rotation_matrix_generator.py --axis 1 1 1 --angle 30
c Get explicit matrix, use in TR card
```

### Prevention

- Prefer explicit matrix for non-trivial rotations
- Test degree input with simple cases first (single-axis, known angles)
- Use scripts to generate matrices from clearer rotation specifications
- Document what rotation is intended in comments:
  ```
  *TR1  0 0 0  0 0 90  1    $ Rotate part 90° CCW about z-axis
  ```

---

## General Troubleshooting Workflow

### Step 1: Isolate the Problem
- Comment out all TR cards
- Verify original geometry is valid
- Add TR cards back one at a time
- Identify which TR causes the issue

### Step 2: Validate Transformation
- Check matrix orthonormality (scripts/tr_matrix_validator.py)
- Verify determinant = ±1
- Check translation vector is reasonable (not 1e10 cm)

### Step 3: Test Incrementally
- Start with identity transformation
- Add translation only, verify
- Add rotation, verify
- Build up to full transformation

### Step 4: Use Visualization
- Run geometry plotter: `mcnp6 i=input.i ip`
- Check for overlaps, voids, lost particles
- Verify component positions match intent

### Step 5: Check Cross-References
- Verify TR number is unique (no duplicates)
- Confirm all surface/cell references are correct
- Check for conflicts between surface TR and TRCL

### Step 6: Consult Logs
- Review MCNP output for warnings
- Check for "transformation" related messages
- Note any particle lost locations

## Diagnostic Scripts

All troubleshooting scripts are located in `scripts/` directory:

- **tr_matrix_validator.py** - Validate orthonormality and determinant
- **rotation_matrix_generator.py** - Generate matrices from various inputs
- **tr_composition.py** - Compose transformations and verify results

See `scripts/README.md` for detailed usage instructions.

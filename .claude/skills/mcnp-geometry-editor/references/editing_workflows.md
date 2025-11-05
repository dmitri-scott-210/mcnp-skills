# MCNP Geometry Editing Workflows

**Purpose:** Systematic procedures for common geometry editing tasks

---

## Workflow Categories

1. **Scaling Operations** - Uniform and non-uniform dimension changes
2. **Translation Operations** - Moving components
3. **Rotation Operations** - Reorienting components
4. **Batch Editing** - Multiple similar changes
5. **Boolean Optimization** - Simplifying complex expressions
6. **Lattice Modifications** - Expanding, compacting, or reorganizing

---

## Workflow 1: Uniform Geometry Scaling

**Objective:** Scale entire model or component by constant factor

### Phase 1: Planning
```
1. Determine scale factor f (e.g., 1.2 for 20% increase)
2. Identify all surfaces to scale
3. Identify dependent parameters (VOL, distances)
4. Create backup of input file
```

### Phase 2: Surface Scaling
```
1. List all surfaces with their types:
   PX, PY, PZ: Multiply D by f
   S: Multiply x,y,z,R by f
   C/X, C/Y, C/Z: Multiply position and R by f
   RPP: Multiply all 6 bounds by f
   RCC: Multiply base, axis vector, R by f
   SPH: Multiply center and R by f
   RHP, REC: Multiply all vectors by f

2. Apply scaling systematically:
   - Process one surface type at a time
   - Verify each calculation
   - Update surface cards

3. Document changes:
   c GEOMETRY SCALED factor × DATE
   c Original dimensions: [list key values]
   c Scaled dimensions: [list key values]
```

### Phase 3: Parameter Updates
```
1. Volume parameters:
   VOL_new = VOL_original × f³
   Update all VOL cards in cell definitions

2. Distance parameters (if any):
   Update any distance-dependent cards
   (e.g., DXTRAN sphere radii)

3. Check material densities:
   Usually unchanged (unless modeling requires adjustment)
```

### Phase 4: Verification
```
1. Geometry plot:
   - Visual inspection of scaled geometry
   - Check proportions maintained
   - Verify no gaps or overlaps

2. Test run:
   - NPS 100-1000 (short test)
   - Check for lost particles
   - Verify tallies in correct locations

3. Results check:
   - Compare to expected physics
   - Flux distributions reasonable?
   - Reaction rates scale as expected?
```

---

## Workflow 2: Component Translation

**Objective:** Move geometric component to new location

### Phase 1: Identify Component
```
1. List all cells in component
2. List all surfaces used by those cells
3. Note current position/bounds
4. Determine target position
5. Calculate translation vector: Δr = (Δx, Δy, Δz)
```

### Phase 2: Choose Method

**Method A: Direct Surface Edit**
```
Use when:
- Simple surfaces (S, RCC, RHP, RPP, BOX)
- Single component
- Permanent change desired

Steps:
1. For each surface:
   S: x→x+Δx, y→y+Δy, z→z+Δz, R unchanged
   RCC: base→base+Δr, axis unchanged, R unchanged
   RPP: all bounds shifted by Δr
   BOX: corner→corner+Δr, edges unchanged

2. Update surface cards
3. Verify with plot
```

**Method B: TR Card**
```
Use when:
- Complex surfaces
- Multiple components moving together
- Want reversibility

Steps:
1. Create TR card:
   *TRn  Δx Δy Δz

2. Apply to surfaces:
   surface_number  n  surface_type  parameters

3. OR apply to cell:
   cell_card  TRCL=n

4. Verify with plot
```

### Phase 3: Check Interactions
```
1. Verify no overlaps with neighboring cells
2. Check cell complement operators (#) still valid
3. Update any cell LIKE relationships if affected
4. Test for lost particles at boundaries
```

---

## Workflow 3: Component Rotation

**Objective:** Rotate component about axis

### Phase 1: Define Rotation
```
1. Identify rotation axis:
   - Standard (x, y, or z axis)
   - Arbitrary axis (requires general matrix)

2. Determine rotation angle θ (degrees)

3. Identify rotation center:
   - Component center
   - Origin
   - Other point

4. Calculate if translation needed:
   If rotating about point P ≠ origin:
   - Translate P to origin
   - Rotate
   - Translate back
```

### Phase 2: Create TR Card
```
Method A: Single-axis rotation (simple)
*TRn  dx dy dz  α β γ  1

Examples:
*TR1  0 0 0  30 0 0  1  $ 30° about x-axis
*TR2  0 0 0  0 45 0  1  $ 45° about y-axis
*TR3  0 0 0  0 0 90  1  $ 90° about z-axis

Method B: Combined rotation (Euler angles)
*TRn  dx dy dz  α β γ  1
where α, β, γ are rotations about x, y, z in sequence

Method C: Rotation about arbitrary axis
Use rotation matrix (requires calculation)
- See transformation_specifications.md for formulas
```

### Phase 3: Apply Rotation
```
Option 1: Surface transformation
surface_number  TR_number  surface_type  params

Option 2: Cell transformation
cell_card  TRCL=TR_number

Option 3: Filled universe rotation
FILL=universe (dx dy dz TR_number)
```

### Phase 4: Verify
```
1. Plot geometry from multiple angles:
   - Check axis alignment
   - Verify rotation direction (right-hand rule)

2. Verify surfaces:
   - Normals point correct direction
   - No inverted surfaces (sense reversal)

3. Test run:
   - Check particle transport through rotated region
   - Verify tallies capture expected results
```

---

## Workflow 4: Non-Uniform Scaling

**Objective:** Scale different axes by different factors

### Phase 1: Determine Scale Factors
```
fx: Scale factor for x-dimension
fy: Scale factor for y-dimension
fz: Scale factor for z-dimension

Example: Stretch in z by 2×, keep x and y
fx=1, fy=1, fz=2
```

### Phase 2: Identify Compatible Surfaces
```
Compatible (direct edit):
- RPP: Scale bounds independently
- BOX: Scale edge vectors independently
- REC: Scale axis and radii independently

Incompatible (become different shape):
- Sphere → Ellipsoid (use ELL or REC)
- Circular cylinder → Elliptical cylinder (use REC)

For incompatible: Use transformation matrix method
```

### Phase 3: Apply Scaling

**Method A: Direct Edit (Compatible Surfaces)**
```
RPP: xmin→xmin×fx, xmax→xmax×fx, etc.

Example:
Original: RPP  -5 5  -5 5  -5 5
Scale (2,1,1.5): RPP  -10 10  -5 5  -7.5 7.5
```

**Method B: Transformation Matrix (Any Surface)**
```
*TRn  0 0 0  fx 0 0  0 fy 0  0 0 fz
Apply to surfaces or cells
```

### Phase 4: Volume Update
```
V_new = V_original × fx × fy × fz

Update VOL parameters in cell cards
```

---

## Workflow 5: Batch Surface Editing

**Objective:** Apply same edit to multiple similar surfaces

### Phase 1: Identify Pattern
```
1. List all surfaces to edit
2. Identify commonality:
   - Same surface type?
   - Same modification needed?
   - Related by pattern (e.g., lattice of cylinders)?

3. Verify uniformity of changes
```

### Phase 2: Script or Manual

**Small Count (<10 surfaces): Manual**
```
1. Edit first surface
2. Copy-paste-modify for others
3. Verify each edit
4. Update cell cards if needed
```

**Large Count (>10 surfaces): Script**
```python
# Example: Scale all sphere radii by 1.5×
import re

with open('input.i', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # Match sphere surfaces (SO or S)
    if re.match(r'^\s*\d+\s+(SO|S)\s+', line):
        parts = line.split()
        surf_num = parts[0]
        surf_type = parts[1]

        if surf_type == 'SO':
            # SO R
            R = float(parts[2])
            R_new = R * 1.5
            lines[i] = f"{surf_num}  {surf_type}  {R_new}\n"
        elif surf_type == 'S':
            # S x y z R
            x, y, z = map(float, parts[2:5])
            R = float(parts[5])
            R_new = R * 1.5
            lines[i] = f"{surf_num}  {surf_type}  {x} {y} {z}  {R_new}\n"

with open('input_scaled.i', 'w') as f:
    f.writelines(lines)
```

### Phase 3: Validation
```
1. Plot original and modified geometries side-by-side
2. Verify systematic changes applied correctly
3. Check no surfaces accidentally missed
4. Test run to verify particles behave correctly
```

---

## Workflow 6: Boolean Expression Simplification

**Objective:** Reduce complexity of cell geometry definitions

### Phase 1: Analyze Current Expression
```
Example complex cell:
1  1  -1.0  -10 11 -12 13 -14 15 : -20 21 : -30  IMP:N=1
              ^region A      ^B      ^C

Identify:
- Intersection operators (space = AND)
- Union operators (: = OR)
- Complement operators (#)
- Redundant terms
```

### Phase 2: Simplify Algebra
```
Rules:
1. A : A = A (idempotent)
2. A A = A (idempotent for intersection)
3. A : ~A = Universe (always true, remove)
4. A ~A = Empty (never true, error!)
5. (A : B) C = AC : BC (distributive)

Example:
Original: -10 11 : -10 12
Simplified: -10 (11 : 12)  $ Factor out common -10
```

### Phase 3: Use Complement Operator

**Original (explicit list):**
```
1  1  -1.0  -1 -2 -3 -4 -5 -6  IMP:N=1  $ Inside 6 surfaces
```

**Simplified (complement):**
```
1  1  -1.0  #2 #3  IMP:N=1  $ NOT in cells 2 or 3
```

**Use when:** Easier to list what to EXCLUDE than INCLUDE

### Phase 4: Verify Equivalence
```
1. Plot both versions:
   - Color-by-cell should be identical
   - Check multiple views

2. Test run:
   - Compare particle histories
   - Verify tally results match

3. Document:
   c GEOMETRY SIMPLIFIED: DATE
   c Original: [old expression]
   c Simplified: [new expression]
```

---

## Workflow 7: Lattice Expansion/Contraction

**Objective:** Change lattice dimensions

### Phase 1: Current State Assessment
```
1. Identify LAT cell:
   cell_num  0  geom  LAT=1  FILL=i1:i2 j1:j2 k1:k2  ...

2. Current dimensions:
   nx = i2-i1+1
   ny = j2-j1+1
   nz = k2-k1+1
   Total elements = nx × ny × nz

3. Current FILL array (count elements):
   Must equal nx × ny × nz

4. Current bounding surface dimensions
```

### Phase 2: Calculate New Dimensions
```
Determine new lattice size:
nx_new, ny_new, nz_new

New FILL range:
i1_new:i2_new (e.g., -2:2 for 5 elements)
j1_new:j2_new
k1_new:k2_new

Verify: (i2_new-i1_new+1) = nx_new (and similarly for j, k)
```

### Phase 3: Update FILL Array
```
1. Create new FILL array with nx_new × ny_new × nz_new elements

2. Populate array:
   - Copy existing pattern if expanding
   - Center new elements around original
   - Use 0 for empty lattice positions if needed

3. Format with proper line breaks:
   LAT=1  FILL=i1:i2 j1:j2 k1:k2  &
          u11 u12 u13 ...  &  $ First j-row
          u21 u22 u23 ...  &  $ Second j-row
          ...

4. Remember: i-index varies fastest (Fortran ordering)
```

### Phase 4: Update Bounding Surface
```
1. Calculate new dimensions:
   If pitch = p:
   width_new = nx_new × p
   height_new = ny_new × p
   depth_new = nz_new × p

2. Update lattice bounding surface:
   Original: RPP  x1 x2  y1 y2  z1 z2
   New: RPP  x1_new x2_new  y1_new y2_new  z1_new z2_new

   where bounds are centered if expanding uniformly
```

### Phase 5: Verify
```
1. Plot with lattice labels:
   - Check indices match intent
   - Verify all elements filled correctly

2. Count elements visually:
   - Should see nx × ny × nz distinct elements

3. Test run:
   - Particles should track through all lattice elements
   - No "lattice index out of bounds" errors
```

---

## Workflow 8: Parametric Studies

**Objective:** Create series of inputs with varying dimensions

### Phase 1: Define Parameters
```
1. Parameter name (e.g., "shield_thickness")
2. Parameter location in input (surface number, card)
3. Range of values: min, max, step
4. Number of variations

Example:
Parameter: Shield thickness
Range: 5 cm to 20 cm
Step: 2.5 cm
Values: [5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0]
```

### Phase 2: Create Template
```
1. Create base input file
2. Mark parameter location with placeholder:
   100  RPP  -50 50  -50 50  0  THICKNESS_PLACEHOLDER

3. OR use comment-based markers:
   100  RPP  -50 50  -50 50  0  10.0  c PARAM: shield_thickness
```

### Phase 3: Generate Input Series
```python
# Automated generation
template = "input_template.i"
param_values = [5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0]

for val in param_values:
    with open(template, 'r') as f:
        content = f.read()

    # Replace placeholder
    modified = content.replace('THICKNESS_PLACEHOLDER', str(val))

    # Write new input
    output_name = f"input_thickness_{val:.1f}.i"
    with open(output_name, 'w') as f:
        f.write(modified)

    print(f"Created: {output_name}")
```

### Phase 4: Verify Series
```
1. Check first and last inputs:
   - Plot geometry
   - Verify parameter changed correctly

2. Run short test on each:
   - NPS 1000
   - Check for errors

3. Document parameter sweep:
   README.txt with parameter ranges and file list
```

---

## Validation Checklist (All Workflows)

After ANY geometry editing:

### Geometric Checks
- [ ] No negative dimensions (radii, lengths)
- [ ] No gaps between cells (unless intentional)
- [ ] No overlapping regions (unless using #)
- [ ] Bounding surfaces enclose geometry
- [ ] Surface sense conventions maintained

### Parameter Checks
- [ ] Volumes updated if scaled (×f³ for uniform)
- [ ] Densities still reasonable
- [ ] Material assignments unchanged (unless intended)
- [ ] Importance values appropriate for new geometry

### Verification Tests
- [ ] Geometry plot shows expected result
- [ ] Multiple views checked (xy, xz, yz)
- [ ] Color-by-cell shows no overlaps
- [ ] Test run (NPS 100-1000) has zero lost particles
- [ ] Tallies in expected locations

### Documentation
- [ ] Changes documented in input file comments
- [ ] Date and reason for modification noted
- [ ] Original values preserved in comments (if useful)
- [ ] Scale factors or transformation matrices documented

---

**END OF EDITING WORKFLOWS**

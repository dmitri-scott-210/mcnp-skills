# MCNP Boolean Operations Guide

Boolean operations combine surfaces to create complex cell geometries. Understanding operator precedence (order of operations) is **critical** - most geometry errors stem from Boolean logic mistakes.

## The Three Boolean Operators

### 1. Intersection (space)

**Operator:** Space (implicit AND)

**Meaning:** Region satisfying ALL conditions

**Example:**
```
1  1  -10.5  -1 2 -3  IMP:N=1
```
**Reads as:** Inside surface 1 AND outside surface 2 AND inside surface 3

**Common use:** Default operator - regions must satisfy all surface conditions

---

### 2. Union (colon :)

**Operator:** `:` (explicit OR)

**Meaning:** Region satisfying ANY condition

**Example:**
```
1  1  -10.5  -1 : -2  IMP:N=1
```
**Reads as:** Inside surface 1 OR inside surface 2

**Common use:** Combining separate regions into single cell

---

### 3. Complement (#)

**Operator:** `#` (NOT)

**Meaning:** All space NOT in specified cell or region

**Two forms:**

**Form 1: Cell complement**
```
#n
```
All space NOT in cell n

**Form 2: Region complement**
```
#(expression)
```
All space NOT in the region defined by expression

**Examples:**
```
c Cell complement
1  1  -10.5  -1 2 #10  IMP:N=1   $ Inside 1, outside 2, not in cell 10

c Region complement
2  1  -10.5  #(-1 2)  IMP:N=1    $ Complement of (inside 1 and outside 2)
```

---

## ORDER OF OPERATIONS (CRITICAL!)

**This is where most Boolean errors occur.**

### Evaluation Order:

1. **Complement (#) - FIRST**
2. **Intersection (space) - SECOND**
3. **Union (:) - THIRD**
4. **Parentheses () override default order** - Innermost to outermost

### Why This Matters

**Example 1: Without parentheses**
```
-1 2 : -3 4
```
**Evaluation:**
1. Intersections first: `(-1 2)` and `(-3 4)`
2. Union last: `(-1 2) : (-3 4)`

**Means:** (Inside 1 AND outside 2) OR (Inside 3 AND outside 4)

**Example 2: With parentheses**
```
-1 (2 : -3) 4
```
**Evaluation:**
1. Parentheses first: `(2 : -3)` becomes (outside 2 OR inside 3)
2. Intersections: `-1 (result) 4`

**Means:** Inside 1 AND (outside 2 OR inside 3) AND outside 4

**These are COMPLETELY DIFFERENT geometries!**

---

## Surface Sense in Boolean Expressions

**Negative sense (-n):** Typically "inside" or "less than"
- Spheres: -n = inside sphere
- Planes: -n = below plane
- Cylinders: -n = inside cylinder

**Positive sense (+n or n):** Typically "outside" or "greater than"
- Spheres: n = outside sphere
- Planes: n = above plane
- Cylinders: n = outside cylinder

**Surface equation test:**
For surface S: f(x,y,z) - D = 0
- If f(x,y,z) < 0: Point is on negative side (-n)
- If f(x,y,z) > 0: Point is on positive side (+n or n)

**Example:**
```
1  SO  10.0        $ Sphere: x² + y² + z² - 100 = 0

At point (5, 0, 0): 25 + 0 + 0 - 100 = -75 < 0  → negative side (inside)
At point (15, 0, 0): 225 + 0 + 0 - 100 = 125 > 0 → positive side (outside)
```

---

## Parentheses for Grouping

**Purpose:** Override default order of operations

**Common patterns:**

**Pattern 1: Union of intersections**
```
(-1 2) : (-3 4)
```
Parentheses ensure intersections are formed BEFORE union

**Pattern 2: Intersection with union**
```
-1 (2 : -3)
```
Union formed first, then intersected with -1

**Pattern 3: Nested grouping**
```
((-1 2) : (-3 4)) (5 : 6)
```
Innermost parentheses first: `(-1 2)` and `(-3 4)`
Then union: `(result1 : result2)`
Finally intersect with: `(5 : 6)`

**Best practice:** Use parentheses liberally for clarity, even if not required by precedence

---

## 10+ Progressively Complex Examples

### Example 1: Simple intersection
**Geometry:** Inside sphere
```
1  1  -10.5  -1  IMP:N=1
2  0          1  IMP:N=0

1  SO  10.0
```
**Logic:** `-1` = inside surface 1

### Example 2: Spherical shell
**Geometry:** Between two concentric spheres
```
1  1  -10.5  -2 1  IMP:N=1
2  0         -1    IMP:N=0
3  0          2    IMP:N=0

1  SO  8.0         $ Inner sphere
2  SO  10.0        $ Outer sphere
```
**Logic:** `-2 1` = inside surf 2 AND outside surf 1
**Order:** Intersection (space) processes left to right: `-2` AND `1`

### Example 3: Cylinder with end caps
**Geometry:** Finite cylinder
```
1  1  -10.5  -1 -2 3  IMP:N=1
2  0          1:2:-3  IMP:N=0

1  CZ  5.0          $ Cylinder radius
2  PZ  0.0          $ Bottom plane
3  PZ  100.0        $ Top plane
```
**Cell 1 logic:** `-1 -2 3` = inside cyl AND above bottom AND below top
**Cell 2 logic:** `1:2:-3` = outside cyl OR below bottom OR above top (graveyard)

### Example 4: Simple union (two spheres)
**Geometry:** Two separate spheres, single cell
```
1  1  -10.5  -1 : -2  IMP:N=1
2  0          1 2     IMP:N=0

1  S  -5 0 0  5.0    $ Left sphere
2  S   5 0 0  5.0    $ Right sphere
```
**Logic:** `-1 : -2` = inside surf 1 OR inside surf 2
**Union creates:** Two separate regions in same cell

### Example 5: Union of intersections (common pattern)
**Geometry:** Two cylindrical regions
```
1  1  -10.5  (-1 -2 3) : (-4 -5 6)  IMP:N=1

1  CZ  5.0           $ Cylinder 1 radius
2  PZ  0.0           $ Cylinder 1 bottom
3  PZ  100.0         $ Cylinder 1 top
4  C/X 10 0  5.0     $ Cylinder 2 (parallel to x)
5  PX  0.0           $ Cylinder 2 left end
6  PX  100.0         $ Cylinder 2 right end
```
**Logic:**
- First intersection: `(-1 -2 3)` = finite cylinder along z
- Second intersection: `(-4 -5 6)` = finite cylinder along x
- Union: Both cylinders in same cell

**Order of operations:**
1. Parentheses create two intersections
2. Union combines them

### Example 6: Intersection of unions
**Geometry:** Less common, creates complex shape
```
1  1  -10.5  (-1 : -2) (3 : 4)  IMP:N=1

1  SO  10.0          $ Sphere 1
2  S  5 0 0  8.0     $ Sphere 2
3  PZ  0.0           $ Plane 1
4  PZ  10.0          $ Plane 2
```
**Logic:**
- First union: `(-1 : -2)` = inside sphere 1 OR inside sphere 2
- Second union: `(3 : 4)` = above plane 1 OR above plane 2
- Intersection: (union1) AND (union2)

**Means:** Inside either sphere AND above either plane

### Example 7: Cell complement (simple)
**Geometry:** Box with hole
```
c Box cell
1  1  -10.5  -1 2 -3 4 -5 6 #10  IMP:N=1  $ Box minus cell 10

c Hole cell
10  0  -7 -5 6  IMP:N=1              $ Cylindrical hole

1  PX  -10.0         $ Box faces
2  PX   10.0
3  PY  -10.0
4  PY   10.0
5  PZ  -10.0
6  PZ   10.0
7  CZ  3.0           $ Hole radius
```
**Logic:** `-1 2 -3 4 -5 6 #10` = inside box AND not in cell 10

**Order:**
1. Complement first: `#10` = all space not in cell 10
2. Intersections: box boundaries AND complement

### Example 8: Region complement
**Geometry:** Complement of intersection
```
1  1  -10.5  #(-1 2)  IMP:N=1
2  0          -1 2    IMP:N=0

1  SO  10.0
2  PZ  0.0
```
**Cell 1 logic:** `#(-1 2)` = NOT (inside sphere AND above plane)
**Means:** Outside sphere OR below plane (De Morgan's law)

**Cell 2 logic:** `-1 2` = inside sphere AND above plane (original region)

### Example 9: Multiple cell complements
**Geometry:** Space excluding three cells
```
1  1  -10.5  -1 #10 #20 #30  IMP:N=1

10  2  -8.0  -2  U=1  IMP:N=1
20  2  -8.0  -3  U=1  IMP:N=1
30  2  -8.0  -4  U=1  IMP:N=1

1  SO  20.0          $ Outer boundary
2  S  -5 0 0  3.0    $ Component 1
3  S   0 5 0  3.0    $ Component 2
4  S   5 0 0  3.0    $ Component 3
```
**Logic:** `-1 #10 #20 #30` = inside outer sphere, not in any of three component cells

**Order:**
1. Complements: `#10`, `#20`, `#30` (three separate NOT regions)
2. Intersections: `-1` AND `#10` AND `#20` AND `#30`

### Example 10: Complex nested expression
**Geometry:** Demonstrates full order of operations
```
1  1  -10.5  (-1 2 : -3 4) #10 (5 : 6)  IMP:N=1
```
**Order of evaluation:**
1. **Complement first:** `#10` = not in cell 10
2. **Intersections within parentheses:** `(-1 2)` and `(-3 4)`
3. **Union:** `(result1 : result2)` = first union group
4. **Second union:** `(5 : 6)` = second union group
5. **Final intersection:** (first union) AND #10 AND (second union)

**Means:**
- [(Inside 1 AND outside 2) OR (Inside 3 AND outside 4)]
- AND not in cell 10
- AND (outside 5 OR outside 6)

### Example 11: Fuel pin with four regions (realistic)
**Geometry:** Fuel, gap, clad, coolant
```
c Four cells share surfaces, no complements needed
1  1  -10.5  -1       IMP:N=1  $ Fuel (inside surf 1)
2  0          1 -2    IMP:N=1  $ Gap (between 1 and 2)
3  2  -6.5    2 -3    IMP:N=1  $ Clad (between 2 and 3)
4  3  -1.0    3 -4 -5 6  IMP:N=1  $ Coolant (outside 3, bounded by 4,5,6)
5  0          4:5:-6  IMP:N=0  $ Graveyard (union of three conditions)

1  CZ  0.4095        $ Fuel radius
2  CZ  0.4180        $ Gap outer radius
3  CZ  0.4750        $ Clad outer radius
4  CZ  0.6500        $ Pin cell boundary
5  PZ  0.0           $ Bottom
6  PZ  365.76        $ Top
```
**Logic:**
- Cell 1: `-1` = simple, inside surface 1
- Cell 2: `1 -2` = outside 1 AND inside 2 (intersection)
- Cell 3: `2 -3` = outside 2 AND inside 3
- Cell 4: `3 -4 -5 6` = outside 3, inside 4, above 5, below 6 (four intersections)
- Cell 5: `4:5:-6` = union of outside boundaries (graveyard)

---

## Testing Boolean Expressions

### Method 1: Geometry Plotter
```bash
mcnp6 inp=file.i ip
```
**Interactive commands:**
- Plot slices: `px 0`, `py 0`, `pz 0`
- Check cell boundaries
- Verify surface sense (colors show cells)

### Method 2: Particle Location Test
```
c Add test source at specific location
SDEF  POS=5 5 5
```
Run with few particles (NPS=10), check if particles start in expected cell

### Method 3: VOID Card Validation
```
VOID  1 2 3    $ Treat cells 1-3 as voids temporarily
```
Use with external source to flood-test geometry, finds gaps/overlaps

---

## Common Boolean Mistakes

### Mistake 1: Missing parentheses (order of operations)

**Intended:** (Inside 1 and outside 2) OR (Inside 3)
```
(-1 2) : -3        $ CORRECT
```

**Mistake:**
```
-1 2 : -3          $ WRONG! Means: -1 AND (2 OR -3)
```
**Order:** Union evaluated AFTER intersection
**Result:** Completely different geometry

**Fix:** Add parentheses to force intended order

---

### Mistake 2: Complement misuse

**Intended:** Not in cell 10
```
#10                $ CORRECT (complement of cell 10)
```

**Mistake:**
```
#(-10)             $ WRONG! Invalid surface sense in complement
```
**Error:** Cannot use negative surface sense inside #()

**Fix:** Use cell complement #n for cells, region complement #(...) for expressions

---

### Mistake 3: Union/intersection confusion

**Intended:** Cylinder bounded by two planes
```
-1 -2 3            $ CORRECT (intersection: inside cyl, above plane2, below plane3)
```

**Mistake:**
```
-1 : -2 : 3        $ WRONG! Union creates unbounded region
```
**Result:** Inside cylinder OR above plane2 OR below plane3 = almost all space

**Fix:** Use intersection (space) for AND conditions

---

### Mistake 4: Surface sense errors

**Intended:** Inside sphere
```
-1                 $ CORRECT (negative side = inside for spheres)
```

**Mistake:**
```
1                  $ WRONG! Outside sphere
```
**Result:** Inverted geometry (graveyard becomes active, active becomes void)

**Fix:** Check surface definition, test with geometry plotter

---

### Mistake 5: Overlapping cells

**Problem:** Two cells both claim same space
```
1  1  -10.5  -1 2  IMP:N=1    $ Intended: between surfaces 1 and 2
2  2  -8.0   -2 3  IMP:N=1    $ ERROR: Overlaps if surf 1 not between 2 and 3
```

**Fix:** Ensure cell definitions are mutually exclusive

---

### Mistake 6: Gaps between cells

**Problem:** Space not assigned to any cell
```
1  1  -10.5  -1    IMP:N=1    $ Inside surf 1
2  0          2    IMP:N=0    $ Outside surf 2
c GAP: If surf 1 and 2 don't touch, space between them is undefined
```

**Fix:** Ensure all space is assigned to exactly one cell

---

## Debugging Boolean Expressions

### Step-by-Step Process:

1. **Identify operators:** Mark intersections (space), unions (:), complements (#)

2. **Apply order of operations:**
   - Parentheses first (innermost to outermost)
   - Complements second
   - Intersections third
   - Unions last

3. **Evaluate incrementally:**
   - Start with simplest sub-expression
   - Build up to full expression
   - Check each step

4. **Verify with plots:**
   - Plot multiple slices
   - Check cell colors (each cell unique)
   - Verify boundaries match intent

5. **Test with particles:**
   - Small NPS run (1000)
   - Check for lost particles
   - Verify source starts in correct cell

### Example Debug Session:

**Expression:** `(-1 2) : (-3 4) #10 (5 : 6)`

**Step 1:** Identify operators
- Parentheses: `(-1 2)`, `(-3 4)`, `(5 : 6)`
- Union: `:`
- Complement: `#10`
- Intersections: spaces within parentheses

**Step 2:** Order of operations
1. Parentheses: `(-1 2)`, `(-3 4)`, `(5 : 6)` evaluated first
2. Complement: `#10` evaluated
3. Intersection: All results combined with AND (space)
4. Union within parentheses already handled

**Step 3:** Evaluate
- `(-1 2)` = inside 1 AND outside 2
- `(-3 4)` = inside 3 AND outside 4
- First union: `(result1) : (result2)` = (inside 1 AND outside 2) OR (inside 3 AND outside 4)
- `#10` = not in cell 10
- `(5 : 6)` = outside 5 OR outside 6
- Final: (first union) AND #10 AND (second union)

**Step 4:** Verify
```bash
mcnp6 inp=test.i ip
px 0
py 0
pz 0
```
Check that cell boundaries match expected geometry

---

## Best Practices

1. **Use parentheses liberally** - Clarify intent, even if not required
2. **One Boolean pattern per line** - Use continuation if complex
3. **Comment complex expressions** - Explain intent
4. **Test incrementally** - Build complex expressions step-by-step
5. **Plot geometry** - Verify before full run
6. **Check surface sense** - Use plotter to verify positive/negative sides
7. **Avoid excessive complements** - Use intersection/union when possible
8. **Document order of operations** - Note precedence in comments
9. **Use standard patterns** - Union of intersections most common
10. **Validate with VOID card** - Find gaps/overlaps early

---

## Quick Reference: Operator Precedence

| Priority | Operator | Symbol | Example |
|----------|----------|--------|---------|
| 1 (First) | Complement | # | #10 or #(-1 2) |
| 2 | Intersection | space | -1 2 -3 |
| 3 (Last) | Union | : | -1 : -2 |
| Override | Parentheses | () | (-1 2) : (-3 4) |

**Remember:** Complement → Intersection → Union (unless parentheses override)

---

**References:**
- MCNP6 User Manual, Chapter 5.02: Cell Cards - Boolean Geometry
- MCNP6 User Manual, Chapter 5.01: Geometry Specification - Surface Sense
- See also: cell_definition_comprehensive.md for cell card format
- See also: complex_geometry_patterns.md for advanced Boolean patterns

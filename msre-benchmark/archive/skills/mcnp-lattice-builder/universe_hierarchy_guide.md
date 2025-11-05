# Universe Hierarchy Guide

**Reference for:** mcnp-lattice-builder skill
**Source:** LATTICE-INFO-SUMMARY.md + current SKILL.md nested lattice examples
**Created:** 2025-11-04 (Session 16)

---

## OVERVIEW

Universe hierarchy allows building complex geometries from simple repeated components. Essential for modeling multi-level systems like reactor cores (pins → assemblies → core) or HTGR fuel (particles → compacts → assemblies → core).

**Key Principle:** Define small components once, reuse many times through universe nesting.

---

## UNIVERSE CONCEPT

### What is a Universe?

A universe is either:
1. A lattice cell (has LAT parameter)
2. A user-specified collection of cells (has U parameter)

**Universe 0:** The "real world" (default universe)
- All geometry ultimately exists in universe 0
- Main geometry level where simulation actually occurs

**Other universes (U=1, 2, 3, ...):** Building blocks
- Defined once, reused multiple times via FILL
- Can contain infinite cells (will be truncated by filled cell boundary)
- Can contain nested universes (up to 20 levels deep)

### Universe Assignment

**Cell-card parameter:**
```
CELL  MAT  DENSITY  GEOM  U=n  [other params]
```

**Data-card form:**
```
U  n₁ n₂ ... nⱼ
```

**Examples:**
```
c Cell-card form (preferred)
1  1  -10.0  -1  U=1  IMP:N=1   $ Fuel cell in universe 1

c Data-card form
U  1 2 3   $ Assigns previous cells to universes 1, 2, 3
```

---

## UNIVERSE HIERARCHY LEVELS

### Level 0: Real World (Universe 0)

**Always the top level.** Contains main geometry and all filled cells that bring in other universes.

```
c Real world geometry
1000  0  -1000  FILL=10  IMP:N=1  $ Fill with universe 10
1001  5  -8.0  1000 -1001  IMP:N=1  $ Structure around filled cell
1002  0  1001  IMP:N=0  $ Outside world
```

**Key point:** Default universe is 0. If no U parameter specified, cell belongs to universe 0.

### Level 1: First-Level Universes

Simple building blocks defined in their own coordinate system.

```
c Universe 1: Fuel pin
1  1  -10.5  -1     U=1  IMP:N=1  $ Fuel
2  2  -6.5    1 -2  U=1  IMP:N=1  $ Cladding
3  3  -1.0    2     U=1  IMP:N=1  $ Coolant

c Surfaces (defined in universe 1 coordinate system)
1  CZ  0.4   $ Fuel radius
2  CZ  0.5   $ Clad outer radius
```

**Coordinate system:** Independent from universe 0. Origin at (0,0,0) in universe 1 frame.

### Level 2: Second-Level Universes

Can contain Level 1 universes via FILL or LAT+FILL.

```
c Universe 10: Fuel assembly (17×17 lattice)
10  RPP  -0.63  0.63  -0.63  0.63  -100  100   $ Lattice element

100  0  -10  U=10  LAT=1  FILL=0:16 0:16 0:0  IMP:N=1
                          1 1 1 1 ... [289 entries]  $ All filled with U=1
```

**Key point:** Lattice cell (100) is IN universe 10. It gets FILLED with universe 1 (fuel pin).

### Level 3: Third-Level Universes

Can contain Level 2 universes.

```
c Universe 20: Assembly with shroud
1000  0  -100  FILL=10  U=20  IMP:N=1   $ Fill with assembly lattice
1001  5  -8.0   100 -101  U=20  IMP:N=1   $ Shroud
1002  3  -1.0   101  U=20  IMP:N=1   $ Water outside

100  RPP  -10.71  10.71  -10.71  10.71  -100  100   $ 17×1.26 = 21.42 cm
101  RPP  -11     11     -11     11     -101  101
```

### Level 4+ : Higher Levels

Can continue nesting up to **20 levels total**.

```
c Universe 100: Core lattice (15×15 assemblies)
10000  RPP  -11  11  -11  11  -101  101   $ Assembly element

100000  0  -10000  U=100  LAT=1  FILL=0:14 0:14 0:0  IMP:N=1
                          20 20 20 ... [225 entries]  $ Filled with U=20

c Real world: Fill with core
1000000  0  -1000000  FILL=100  IMP:N=1   $ Core lattice
```

**Hierarchy summary:**
```
Universe 0 (real world)
  └─ Universe 100 (core lattice, 15×15)
       └─ Universe 20 (assembly + shroud)
            └─ Universe 10 (pin lattice, 17×17)
                 └─ Universe 1 (fuel pin)
```

**Nesting depth:** 4 levels in this example (0 → 100 → 20 → 10 → 1)

---

## FILL MECHANISM

### Single Universe Fill

**Syntax:**
```
CELL  0  -SURF  FILL=n  [other params]
```

**Effect:** Entire cell filled with universe n. All cells in universe n exist within the filled cell's boundary.

**Example:**
```
c Fill cell 1000 with universe 5
1000  0  -100  FILL=5  IMP:N=1

c Universe 5 defined elsewhere
10  1  -10.0  -10  U=5  IMP:N=1  $ Fuel in universe 5
11  2  -1.0    10  U=5  IMP:N=1  $ Coolant in universe 5
```

**Key behavior:**
- Universe 5 cells infinite? Truncated by surface 100.
- Universe 5 coordinate origin at filled cell's origin (unless TRCL used).

### Lattice Fill (Array)

**Syntax:**
```
CELL  0  -SURF  U=n  LAT=1  FILL=i1:i2 j1:j2 k1:k2  u₁ u₂ ... uₘ
```

**Effect:** Lattice elements filled with different universes based on array.

**Example:**
```
c 3×3 lattice with fuel (U=1) and control (U=2) assemblies
100  0  -10 11 -12 13 -14 15  U=10  LAT=1
     FILL=0:2 0:2 0:0
          1 1 2    $ j=0: i=0,1,2
          1 2 1    $ j=1
          2 1 1    $ j=2
```

**Result:** 9 lattice elements, each filled with universe 1 or 2 as specified.

### Fill with Transformation

**Syntax:**
```
CELL  0  -SURF  FILL=n (TRm)     $ Reference TR card
CELL  0  -SURF  FILL=n (inline)  $ Inline transformation
```

**Effect:** Universe n filled into cell with rotation/translation applied.

**Example:**
```
TR5  1  10 0 0  0 0 45   $ Translate +10X, rotate 45° about Z
1000  0  -1000  FILL=20 (TR5)  IMP:N=1
```

---

## UNIVERSE CONTAINMENT RULES

### Infinite Cells in Universes

**Allowed:** Universe cells can be infinite (unbounded).

**Effect:** When filled into finite cell, universe geometry truncated at filled cell boundary.

**Example:**
```
c Universe 3 has infinite coolant cell
1  1  -10.0  -1  U=3  IMP:N=1  $ Fuel (finite)
2  2  -1.0    1  U=3  IMP:N=1  $ Coolant (infinite)

c Fill into finite cell 500
500  0  -50  FILL=3  IMP:N=1

50  RPP  -5  5  -5  5  -10  10   $ Coolant truncated at this boundary
```

**Key point:** Coolant (cell 2) extends to infinity in universe 3, but only exists within RPP when filled.

### Background Cells in Universes

**Purpose:** Fill space not occupied by other universe cells.

**Common use:** Lattice element background outside pin geometry.

**Example:**
```
c Universe 1: Fuel pin in coolant background
1  1  -10.0  -1     U=1  IMP:N=1  $ Fuel
2  2  -6.5    1 -2  U=1  IMP:N=1  $ Clad
3  3  -1.0    2     U=1  IMP:N=1  $ Coolant (infinite background)

c Universe cells contained when filled into lattice element
```

**Rule:** All space within universe must be defined. No voids allowed (would cause lost particles).

---

## NEGATIVE UNIVERSE OPTIMIZATION

### What is Negative Universe?

**Syntax:**
```
U = -n  (instead of U = n)
```

**Effect:** Tells MCNP that all cells in universe are FULLY ENCLOSED within filled cell boundary. No truncation occurs.

**Computational benefit:** MCNP skips boundary checks between universe and filled cell (slight speed improvement, memory savings).

### When to Use

**Safe to use when:**
1. ALL universe cells fully enclosed (no cells touch filled cell boundary)
2. Geometry thoroughly verified with plots
3. VOID card used to check for leaks
4. Validated against known solution

**Example (safe usage):**
```
c Fuel pin with gap around it (never touches element boundary)
1  1  -10.0  -1     U=-5  IMP:N=1  $ Fuel (r < 0.4)
2  2  -6.5    1 -2  U=-5  IMP:N=1  $ Clad (0.4 < r < 0.5)
3  3  -1.0    2 -3  U=-5  IMP:N=1  $ Gap (0.5 < r < 0.6)
4  0   3         U=-5  IMP:N=1  $ Void beyond gap

c Lattice element boundary at r = 0.63 (larger than gap at 0.6)
c Safe to use U=-5 because all cells fully enclosed
```

### When NOT to Use

**⚠️ DANGEROUS if:**
1. Any universe cell could touch filled cell boundary
2. Geometry not thoroughly verified
3. Complex nesting (hard to verify containment)
4. Learning/testing phase (not production)

**Example (WRONG usage):**
```
c DANGEROUS: Coolant extends to lattice element boundary
1  1  -10.0  -1     U=-10  IMP:N=1  $ Fuel
2  2  -6.5    1 -2  U=-10  IMP:N=1  $ Clad
3  3  -1.0    2     U=-10  IMP:N=1  $ Coolant (extends to boundary!)

c Cell 3 touches filled cell boundary
c Using U=-10 causes SILENT ERRORS (wrong results, no warnings)
```

### Warning

**From MCNP Manual:**
> "MCNP cannot detect errors caused by improper use of negative universes. Extremely wrong answers can be calculated."

**Recommendation:** Avoid negative universes unless:
- Computational performance critical
- Geometry verified exhaustively
- Validated against reference solution

**Default:** Use positive universes (U=n). Small computational cost worth the safety.

---

## UNIVERSE HIERARCHY DESIGN PRINCIPLES

### Principle 1: Define Smallest Component First

Build from bottom up:
1. Define simplest component (e.g., fuel pin)
2. Combine into next level (e.g., assembly)
3. Combine assemblies into core
4. Place core in real world

**Example workflow:**
```
Step 1: Define fuel pin (U=1)
Step 2: Create pin lattice (U=10 contains U=1)
Step 3: Add assembly structure (U=20 contains U=10)
Step 4: Create core lattice (U=100 contains U=20)
Step 5: Place core in real world (U=0 fills with U=100)
```

### Principle 2: Independent Coordinate Systems

Each universe has its own coordinate system (origin at 0,0,0 in that frame).

**Example:**
```
c Universe 1: Fuel pin centered at origin
1  1  -10.0  -1  U=1  IMP:N=1  $ Fuel at origin

c Universe 10: Assembly centered at origin
100  0  -10 11  U=10  LAT=1  FILL=1  $ Assembly lattice at origin

c When U=10 filled into real world at X=+50:
1000  0  -1000  FILL=10 (1 50 0 0)  IMP:N=1
c Assembly (and all pins) translated to X=+50 in real world
```

### Principle 3: Document Hierarchy Clearly

**Always include hierarchy diagram in comments:**

```
c ============= UNIVERSE HIERARCHY =============
c U=0:   Real world (main geometry)
c          ├─ Core barrel
c          ├─ Moderator
c          └─ Core lattice (filled with U=100)
c
c U=100: Core lattice (15×15 assemblies)
c          └─ Assemblies (filled with U=20)
c
c U=20:  Assembly + shroud
c          ├─ Assembly lattice (filled with U=10)
c          └─ Shroud structure
c
c U=10:  Assembly lattice (17×17 pins)
c          ├─ Fuel pins (U=1)
c          ├─ Guide tubes (U=2)
c          └─ Instrument tubes (U=3)
c
c U=1:   Fuel pin
c          ├─ Fuel pellet
c          ├─ Gap
c          ├─ Cladding
c          └─ Coolant
c
c U=2:   Guide tube (similar structure)
c U=3:   Instrument tube (similar structure)
c =============================================
```

**Why:** Future users (including yourself) need to understand nesting structure quickly.

### Principle 4: Use Consistent Numbering Scheme

**Recommended convention:**
- U=0: Real world (reserved)
- U=1-9: Basic components (pins, particles, single elements)
- U=10-99: Low-level lattices (pin lattices, compact lattices)
- U=100-999: Mid-level structures (assemblies with internal structure)
- U=1000+: High-level structures (core lattices, reactor systems)

**Example:**
```
U=1:    Fuel pin
U=2:    Control rod
U=10:   Pin lattice (17×17)
U=20:   Assembly + shroud
U=100:  Core lattice (15×15)
```

**Benefit:** Numbering reveals hierarchy level at a glance.

---

## PARTICLE TRACKING THROUGH HIERARCHIES

### How MCNP Tracks Particles

**At each collision:**
1. Determine current universe and cell
2. Sample collision physics (scattering, absorption, etc.)
3. Transport to next collision site
4. If crossing universe boundary, transform coordinates
5. Determine new universe and cell
6. Repeat

**Example:** Particle born in fuel pin, travels to adjacent assembly:
```
Step 1: Born in universe 1 (fuel pin), cell 1 (fuel)
Step 2: Scatter, travel within fuel
Step 3: Cross to cell 2 (cladding), still in U=1
Step 4: Exit U=1, enter lattice element boundary in U=10
Step 5: MCNP transforms coordinates from U=1 frame to U=10 frame
Step 6: Determine next lattice element (adjacent pin)
Step 7: Enter different instance of U=1 (adjacent fuel pin)
Step 8: MCNP transforms to that pin's U=1 frame
Step 9: Continue transport...
```

### Coordinate Transformation Overhead

**Each universe crossing:**
- Transform particle position (main ↔ auxiliary coordinates)
- Transform direction vector
- Check containment in new universe

**Computational cost:** Negligible for <5 levels. Measurable for >10 levels.

**MCNP limit:** Up to 20 hierarchical levels (more than sufficient for any reactor model).

---

## MULTI-LEVEL HIERARCHY EXAMPLE

### Complete 4-Level PWR Core

**Goal:** Model PWR core with explicit fuel pins

**Hierarchy:**
```
Level 0: Real world (core barrel, downcomer)
Level 1: Fuel pin (U=1), Guide tube (U=2), Instrument tube (U=3)
Level 2: Assembly lattice (U=10, 17×17 pins)
Level 3: Assembly + shroud (U=20)
Level 4: Core lattice (U=100, 15×15 assemblies)
```

**Input structure:**

```
c ===== LEVEL 1: Fuel Pin (Universe 1) =====
1  1  -10.5  -1     U=1  IMP:N=1  $ UO2 fuel
2  0         1 -2   U=1  IMP:N=1  $ Gap
3  2  -6.5    2 -3  U=1  IMP:N=1  $ Zircaloy clad
4  3  -0.7    3     U=1  IMP:N=1  $ Water

1  CZ  0.409   $ Fuel radius
2  CZ  0.418   $ Gap outer
3  CZ  0.475   $ Clad outer

c ===== LEVEL 1: Guide Tube (Universe 2) =====
10  2  -6.5   -10 11  U=2  IMP:N=1  $ Inner clad
11  3  -0.7     10     U=2  IMP:N=1  $ Water inside
12  2  -6.5     11 -12 U=2  IMP:N=1  $ Outer clad
13  3  -0.7     12     U=2  IMP:N=1  $ Water outside

10  CZ  0.561   $ Inner clad inner
11  CZ  0.602   $ Inner clad outer
12  CZ  0.613   $ Outer clad outer

c ===== LEVEL 2: Assembly Lattice (Universe 10) =====
100  RPP  -0.63  0.63  -0.63  0.63  -200  200   $ Pin cell (1.26 cm pitch)

200  0  -100  U=10  LAT=1  FILL=0:16 0:16 0:0  IMP:N=1
                          1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1  $ j=0
                          1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1  $ j=1
                          ... [17 rows total]

c ===== LEVEL 3: Assembly + Shroud (Universe 20) =====
1000  0   -1000  FILL=10  U=20  IMP:N=1   $ Assembly
1001  2  -6.5   1000 -1001  U=20  IMP:N=1   $ Shroud
1002  3  -0.7   1001  U=20  IMP:N=1   $ Water gap

1000  RPP  -10.71  10.71  -10.71  10.71  -200  200  $ 17×1.26 = 21.42 cm
1001  RPP  -11.0   11.0   -11.0   11.0   -205  205

c ===== LEVEL 4: Core Lattice (Universe 100) =====
10000  RPP  -11  11  -11  11  -205  205   $ Assembly element (22 cm pitch)

100000  0  -10000  U=100  LAT=1  FILL=0:14 0:14 0:0  IMP:N=1
                          20 20 20 20 ... [15×15 = 225 assemblies]

c ===== LEVEL 0: Real World =====
1000000  0  -1000000  FILL=100  IMP:N=1   $ Core
1000001  4  -7.8   1000000 -1000001  IMP:N=1   $ Core barrel
1000002  3  -0.7   1000001  IMP:N=1   $ Downcomer
1000003  0  1000002  IMP:N=0   $ Outside world

1000000  RPP  -165  165  -165  165  -205  205  $ Core outer
1000001  RPP  -170  170  -170  170  -210  210  $ Barrel outer
1000002  RPP  -200  200  -200  200  -230  230  $ Problem boundary
```

**Total cells in model:**
- Level 1: 4 cells (pin) × 289 locations × 225 assemblies = 260,100 effective cells
- Defined in input: ~20 cells
- **Reduction factor: 13,000×**

---

## IMPORTANCE INHERITANCE

### Importance in Nested Universes

**Rule:** Importance (IMP:N, IMP:P, etc.) specified at EACH level independently.

**Example:**
```
c Universe 1: Fuel pin
1  1  -10.0  -1  U=1  IMP:N=1  $ Fuel importance = 1
2  2  -1.0    1  U=1  IMP:N=1  $ Coolant importance = 1

c Filled cell in real world
1000  0  -1000  FILL=1  IMP:N=10  $ Filled cell importance = 10

c Net importance of fuel:
c   IMP:N = 1 (from universe cell) × 10 (from filled cell) = 10
```

**Multiplication rule:** Importance of universe cell = (cell IMP) × (filled cell IMP)

**Best practice:** Set importance = 1 in universes, adjust only in real world (U=0). Easier to manage.

---

## DEBUGGING UNIVERSE HIERARCHIES

### Common Issues

**1. "Cell N not found in universe M"**
- Fill references nonexistent universe
- Check FILL=n matches existing U=n

**2. "Lost particle in universe transition"**
- Universe cells not fully contained
- Add background cells in universes

**3. "Geometry overlap at universe boundary"**
- Universe cell extends beyond lattice element
- Check universe cell sizes vs lattice element size

**4. "Cannot find cell for particle"**
- Gap in geometry (void space undefined)
- Ensure all space in universe covered by cells

### Debugging Process

**Step 1: Verify hierarchy diagram**
```
Draw ASCII diagram showing all universe relationships
Trace FILL references from U=0 down to lowest level
Confirm no circular references (U=10 fills U=20, U=20 fills U=10 - INVALID!)
```

**Step 2: Test each level independently**
```
c Comment out higher levels
c Test fuel pin (U=1) by filling directly into U=0
1000  0  -1000  FILL=1  IMP:N=1   $ Test U=1 alone

c Once working, add next level (U=10)
1000  0  -1000  FILL=10  IMP:N=1  $ Test U=10 (contains U=1)

c Continue building up hierarchy
```

**Step 3: Plot at each level**
```
c Plot universe 1 contents
c Plot universe 10 with universe 1 filled
c Plot universe 20 with universe 10 filled
c Plot full hierarchy in universe 0
```

**Step 4: Run with detailed output**
```
c Add to data block:
PRINT  110  128  160  170   $ Detailed cell/universe tracking
```

---

## BEST PRACTICES SUMMARY

1. **Build from bottom up** (smallest component first)
2. **Use independent coordinate systems** (each universe centered at origin)
3. **Document hierarchy clearly** (ASCII diagram in comments)
4. **Use consistent numbering** (scheme reveals hierarchy level)
5. **Test each level independently** (before combining)
6. **Avoid negative universes** (unless verified exhaustively)
7. **Set importance = 1 in universes** (adjust only in U=0)
8. **Plot thoroughly at each level** (catch errors early)
9. **Add background cells** (prevent lost particles)
10. **Keep nesting < 5 levels** (if possible, for simplicity)

---

**References:**
- MCNP6 User Manual §3.3: Repeated Structures and Universes
- MCNP6 User Manual §5.2.1: U Parameter
- MCNP6 User Manual §5.2.2: FILL Parameter
- MCNP6 Primer Chapter 9: Universes and Lattices

---

**END OF UNIVERSE_HIERARCHY_GUIDE.MD**

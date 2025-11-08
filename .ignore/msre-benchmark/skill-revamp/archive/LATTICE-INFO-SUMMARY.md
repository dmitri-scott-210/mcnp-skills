# LATTICE INFORMATION SUMMARY - MCNP CHAPTERS 5.02 & 5.05

**Source Documents:**
- Chapter 5.02: Cell Cards
- Chapter 5.05: Geometry Data Cards (focusing on U, LAT, FILL, TRCL)

**Created:** 2025-11-04 (Session 15)
**Purpose:** Comprehensive summary of MCNP lattice geometry information for mcnp-lattice-builder skill revamp

---

## OVERVIEW OF MCNP REPEATED STRUCTURES

The repeated structures capability allows users to describe cells and surfaces once and reuse them multiple times throughout geometry. This is essential for:
- Reactor cores with dozens of identical fuel modules
- Complex objects arranged in regular or irregular patterns
- Fuel assemblies with repeated TRISO particles or fuel pins

**Key concept:** Repeated structures do NOT make problems run faster - they only reduce input and memory use.

---

## CELL CARD FUNDAMENTALS (Chapter 5.02)

### Basic Cell Card Format

**Form 1: Standard Cell Definition**
```
j m d geom params
```
- j = Cell number (1 ≤ j ≤ 99,999,999)
- m = Material number (0 for void, >0 for material)
- d = Density (>0 atomic density in 10²⁴ atoms/cm³, <0 mass density in g/cm³)
- geom = Geometry specification (signed surface numbers + Boolean operators)
- params = Cell parameters (IMP, VOL, U, TRCL, LAT, FILL, etc.)

**Form 2: LIKE BUT Construction**
```
j LIKE n BUT list
```
- Very useful for repeated structures with minor variations
- Cell j inherits all attributes from cell n except those in list
- Cell n card must appear BEFORE cell j in input file
- Special keywords: MAT (material number), RHO (density)

### Boolean Operators for Geometry

- `<space>` = intersection (AND)
- `:` = union (OR)
- `#` = complement (NOT)

**Default order of operations:**
1. Complement (first)
2. Intersection (second)
3. Union (third)

**Complement operator shortcuts:**
- `#n` = complement of entire cell n geometry
- `#(...)` = complement of surfaces in parentheses

---

## UNIVERSE CONCEPT (U CARD)

### What is a Universe?

A universe is either:
1. A lattice cell (LAT card)
2. A user-specified collection of cells

**Key principles:**
- Universe 0 = "real world" (default)
- All cells belong to either universe 0 OR some other universe
- A cell can be FILLED with a universe
- Up to 20 hierarchical levels permitted
- Universe cells can be finite or infinite (will be truncated by filled cell boundary)

### Universe Card Formats

**Cell-card form:**
```
U = n
```

**Data-card form:**
```
U n₁ n₂ ... nⱼ
```
- n = Universe number (0 ≤ n ≤ 99,999,999)
- Default: U = 0 (real world)
- Negative universe (-n): Indicates cell is fully enclosed, no boundary calculations needed in higher levels (computational efficiency)

**⚠️ CAUTION on negative universes:**
- Use with extreme caution - MCNP cannot detect errors
- Extremely wrong answers can be calculated silently
- Plot geometry thoroughly and/or run with VOID card to verify

### Universe Hierarchy

- **Level 0** = Real world (highest level)
- **Level 1** = Lower level (universes filling level 0 cells)
- **Level 2** = Even lower (universes filling level 1 cells)
- ... up to 20 levels

**Materials:** Normally placed in cells of lowest level universe, except for lattices.

**Surfaces:** Can be shared between universes (planar surfaces). Coincident surfaces CANNOT be:
- Reflecting or periodic
- Source surfaces
- Tally surfaces

---

## LATTICE CARD (LAT)

### Lattice Types

**LAT = 1:** Rectangular (square) lattice
- Comprised of hexahedra (6 faces)
- Base element can be infinite in 1 or 2 dimensions
- Opposite sides must be identical and parallel

**LAT = 2:** Hexagonal (triangular) lattice
- Comprised of hexagonal prisms (8 faces)
- Base element can be infinite along prism length
- Cross-sectional shape must be convex

### Lattice Requirements

1. A lattice must be the ONLY thing in its universe
2. Real world (level 0) itself can be a lattice
3. Each lattice cell must have an associated FILL card
4. Cross-sectional shape must be convex
5. Elements must fill space exactly (opposite sides identical and parallel)

### Lattice Indexing

**Surface order on cell card defines lattice indices:**

**For hexahedral lattice (LAT=1):**
- Surface 1 → [1, 0, 0] element beyond
- Surface 2 → [-1, 0, 0] element beyond
- Surface 3 → [0, 1, 0] element beyond
- Surface 4 → [0, -1, 0] element beyond
- Surface 5 → [0, 0, 1] element beyond
- Surface 6 → [0, 0, -1] element beyond

**For hexagonal prism lattice (LAT=2):**
- Surface 1 → [1, 0, 0] element beyond
- Surface 2 → [-1, 0, 0] element beyond
- Surface 3 → [0, 1, 0] element beyond
- Surface 4 → [0, -1, 0] element beyond
- Surface 5 → [-1, 1, 0] element beyond
- Surface 6 → [1, -1, 0] element beyond
- Surface 7 → [0, 0, 1] element beyond (base surface)
- Surface 8 → [0, 0, -1] element beyond (base surface)

**Verification:** Use MCNP geometry plotter to label lattice cells with indices.

---

## FILL CARD

### Single Fill

**Simplest form:**
```
FILL = n
```
- Every cell of the lattice is filled by universe n

### Array Fill (Fully Specified)

**Lattice array specification:**
```
FILL = i₁:i₂ j₁:j₂ k₁:k₂
       n(i₁,j₁,k₁) n(i₁+1,j₁,k₁) ... n(i₂,j₂,k₂)
```

**Dimension declarations:**
- Three-dimensional array (Fortran-like syntax)
- Both lower and upper bounds must be explicitly stated
- Indices can be positive, negative, or zero
- Example: -5:5 defines 11 elements (-5, -4, ..., 4, 5)

**Array values:**
- Each element corresponds to universe number filling that lattice element
- Only lattice elements with array entries actually exist
- Order follows Fortran convention (first index varies fastest)

### Special Array Values

**nⱼ = 0:** In level-zero lattice
- Lattice element does not exist
- Allows non-rectangular arrays

**nⱼ = universe number of lattice:**
- Element filled with material from lattice cell card (not a universe)
- NOT allowed for real world lattice

### Fill with Transformation

**With transformation number:**
```
FILL = n (transformation_number)
```

**With explicit transformation:**
```
FILL = n (o₁ o₂ o₃ xx' yx' zx' xy' yy' zy' xz' yz' zz' m)
```
or
```
*FILL = n (o₁ o₂ o₃ angles...)
```
- Transformation between filled cell and filling universe coordinate systems
- Universe in auxiliary coordinate system
- If no transformation: universe inherits filled cell transformation
- `*FILL` uses angles in degrees instead of cosines

### FILL Card Example

```
FILL = 0:2 1:2 0:1
    4 4 2    $ i=0,1,2 for j=1 & k=0
    0 4 0    $ i=0,1,2 for j=2 & k=0
    0 3 3    $ i=0,1,2 for j=1 & k=1
    4 4 0    $ i=0,1,2 for j=2 & k=1
```
- 8 lattice elements exist
- Elements [0,1,0], [1,1,0], [1,2,0], [0,2,1], [1,2,1] filled with universe 4
- Element [2,1,0] filled with universe 2
- Elements [1,1,1], [2,1,1] filled with universe 3

---

## COORDINATE TRANSFORMATIONS (TR and TRCL)

### TR Card: Surface Transformation

**Format:**
```
TRn o₁ o₂ o₃ xx' yx' zx' xy' yy' zy' xz' yz' zz' m
```
or
```
*TRn o₁ o₂ o₃ angles_in_degrees
```

**Parameters:**
- n = Transformation number (1 ≤ n ≤ 999 for surfaces, unlimited for TRCL)
- o₁ o₂ o₃ = Displacement vector (default: 0 0 0)
- Rotation matrix entries (9 values, or fewer with automatic completion)
- m = Displacement vector origin interpretation
  - m = 1 (default): Displacement is origin of auxiliary system in main system
  - m = -1: Displacement is origin of main system in auxiliary system

**Rotation matrix shortcuts:**
- All 9 elements: Required if coordinate systems have different handedness
- 6 elements: Two vectors (MCNP creates third by cross product)
- 5 elements: One vector each way (MCNP uses Eulerian angles)
- 3 elements: One vector (MCNP creates others arbitrarily - good for rotation axis)
- 0 elements: Identity matrix (pure translation)

**Special restrictions for cones:**
- One-sheet cone: Can only rotate by multiples of 90° between coordinate axes
- Two-sheet cone: Can transform anywhere
- Ambiguity surfaces must have same transformation number as two-sheet cone

### TRCL: Cell Transformation

**Two formats:**

**Format 1: Reference TR card**
```
TRCL = n
```
- References TRn card in data section

**Format 2: Inline transformation**
```
TRCL = (o₁ o₂ o₃ xx' yx' zx' xy' yy' zy' xz' yz' zz' m)
```
or
```
*TRCL = (o₁ o₂ o₃ angles_in_degrees)
```

**Key points:**
- Most useful with repeated structures
- Cells with same universe inherit transformation
- Surfaces defining those cells also inherit transformation
- Simplifies definition of multiple identical cells at different locations/orientations

**Limitations:**
- Can only apply to cells with surface numbers < 1000
- Generated surface number = original surface + 1000 × cell number
- Limits: Cell numbers ≤ 6 digits, original surface numbers ≤ 3 digits

**LIKE BUT with TRCL:**
```
1  1  0  -17        $ rcc can
21 LIKE 1 BUT *TRCL=(20 0 0 45 -45 90 135 45 90 90 90 0)
```
- Cell 21 identical to cell 1
- Translated to (20, 0, 0)
- Rotated 45° counter-clockwise with respect to x and y

---

## REPEATED STRUCTURES WORKFLOW

### Four Primary Cards

1. **U (Universe):** Identifies universe to which cell belongs
2. **FILL:** Specifies which universe fills a cell
3. **LAT (Lattice):** Defines infinite array of hexahedra or hexagonal prisms
4. **TRCL (Transformation):** Positions identical cells at different locations/orientations

### Supporting Features

- **LIKE n BUT:** Shorthand for creating similar cells
- **URAN (Stochastic):** Random transformation for HTGR fuel kernels

### Key Details

1. Cell parameters can be defined on cell cards directly
2. Universe assigned to cell specifies grouping
3. Fill specifies which universe fills cell
4. Cell transformation allows multiple positions/orientations of same surfaces
5. Lattice defines infinite array and indexing
6. Source definition can be in repeated structures (but NOT surface sources)
7. Importance in universe = multiplier of filled cell importance
8. Weight windows are NOT multipliers (use MESH card for mesh-based weight windows)

---

## IMPORTANCE NOTES FOR REPEATED STRUCTURES

### Cell Parameters on Cell Cards

Cell parameters (IMP, VOL, PWT, EXT, FCL, WWN, DXC, NONU, PD, TMP, U, TRCL, LAT, FILL, ELPT, COSY, BFLCL, UNC) can be defined:
- Directly on cell cards (KEYWORD = value format)
- In data card section

**Rules:**
- If parameter on ANY cell card → cannot have card with that name in data section
- Cannot use parameter in vertical-format input card
- Some parameters can be on cell cards, others in data section

**TMP and WWN special syntax:**
- Form 1: `TMP1=value TMP2=value ...`
- Form 2: `TMP` followed by all temperatures (order from THTME card)
- Similar for WWN: `WWN1:n=value` or `WWN:n` followed by all lower bounds

### Optimization with Negative Universe

**When cell is NOT truncated by higher-level boundary:**
- Precede U card entry with minus sign (e.g., `U=-2`)
- Omits distance-to-boundary calculations in higher levels
- **⚠️ EXTREME CAUTION:** MCNP cannot detect errors
- Can produce extremely wrong answers silently
- **Verification required:** Plot multiple views, run with VOID card

---

## PRACTICAL EXAMPLES

### Example 1: Simple Lattice

```
1  0  1 -2 -3  4 -5  6  FILL=1         $ Container cell
2  0 -7  1 -3  8      U=1 FILL=2 LAT=1 $ Lattice base [0,0,0]
3  0 -11              U=-2             $ Fuel sphere (finite, negative U)
4  0  11              U=2              $ Background (infinite)
5  0 -1:2:3:-4:5:-6                    $ Outside world

1  PX  0
2  PX  50
3  PY  10
4  PY -10
5  PZ  5
6  PZ -5
7  PX  10
8  PY  0
11 S   5 5 0 4
```
- 50×20×10 cm box filled with lattice of 10×10×10 cm cubes
- Each cube contains sphere (cell 3) and background (cell 4)
- Cell 3 uses negative universe (fully enclosed by surface 11)

### Example 2: Macrobody Version

```
1  0  -20        FILL=1         $ Container
2  0  -30  U=1   FILL=2  LAT=1  $ Lattice base
3  0  -11  U=-2                 $ Fuel sphere
4  0   11  U=2                  $ Background
5  0   20                       $ Outside

20 RPP  0 50 -10 10 -5 5
30 RPP  0 10   0 10  0 10
11 S    5  5   0  4
```
- Identical to Example 1, using macrobodies for cleaner definition

### Example 3: Array Fill

```
FILL = 0:2  1:2  0:1
    4 4 2    $ i=0,1,2 for j=1 & k=0
    0 4 0    $ i=0,1,2 for j=2 & k=0
    0 3 3    $ i=0,1,2 for j=1 & k=1
    4 4 0    $ i=0,1,2 for j=2 & k=1
```
- Non-rectangular array (some elements don't exist: 0 entries)
- Different universes in different positions
- 8 active elements total

---

## LATTICE DESIGN CHECKLIST

### Before Creating Lattice

1. ✅ Decide which element will be [0,0,0]
2. ✅ Decide index increase directions (must follow rules for LAT type)
3. ✅ Ensure opposite sides are identical and parallel
4. ✅ Ensure cross-section is convex
5. ✅ Determine if lattice will be finite or infinite
6. ✅ Verify surfaces are in correct order for indexing

### Lattice Cell Requirements

1. ✅ LAT card specifying lattice type (1 or 2)
2. ✅ U card assigning lattice to universe (if not in real world)
3. ✅ FILL card specifying universe(s) filling elements
4. ✅ Surface order on cell card matches intended indices
5. ✅ Bounding surfaces form valid hexahedra (LAT=1) or hexagonal prisms (LAT=2)

### Verification Steps

1. ✅ Use MCNP geometry plotter with lattice index labels
2. ✅ Verify [0,0,0] element is in intended position
3. ✅ Check index directions match design intent
4. ✅ Verify edge/boundary handling for finite lattices
5. ✅ Plot multiple views to catch truncation issues
6. ✅ Run with VOID card if using negative universes

---

## COMMON PITFALLS AND SOLUTIONS

### Pitfall 1: Incorrect Surface Order

**Problem:** Lattice indices don't increase in intended direction

**Solution:**
- Review surface order on LAT cell card
- First two surfaces define first index direction
- Next two surfaces define second index direction
- Last two surfaces define third index direction
- Use geometry plotter with index labels to verify

### Pitfall 2: Non-Convex Cross-Section

**Problem:** Lattice elements don't fill space properly

**Solution:**
- Ensure hexahedra have opposite sides identical and parallel
- Ensure hexagonal prisms have convex cross-section
- Check for surface orientation errors

### Pitfall 3: Missing FILL Card

**Problem:** Fatal error - lattice cell has no FILL card

**Solution:**
- Every cell with LAT card MUST have FILL card
- FILL can be single universe or array specification

### Pitfall 4: Array Index Mismatch

**Problem:** FILL array indices don't align with lattice

**Solution:**
- Verify dimension declarations match desired lattice extent
- Remember: i₁:i₂ means elements i₁, i₁+1, ..., i₂ (inclusive)
- Count elements: i₂ - i₁ + 1 elements in that direction
- Array values must follow Fortran ordering (first index varies fastest)

### Pitfall 5: Transformation Confusion

**Problem:** Filled cell and filling universe coordinate systems misaligned

**Solution:**
- Use TRCL on filled cell OR fill universe (preferably filled cell)
- If both filled cell and universe have TRCL: universe inherits filled cell transformation
- Test with simple geometries first
- Use geometry plotter extensively

### Pitfall 6: Negative Universe Errors

**Problem:** Wrong answers, lost particles, or geometry errors

**Solution:**
- Only use negative universe when cell is FULLY enclosed
- Never for cells truncated by higher-level boundaries
- Plot multiple views of geometry
- Run with VOID card to check for errors
- When in doubt, use positive universe (safer)

---

## COMPUTATIONAL CONSIDERATIONS

### Performance

- Repeated structures do NOT speed up particle transport
- Only benefit: Reduced input file size and memory usage
- Same geometry with explicit cells runs at same speed

### Token Efficiency for Large Models

For models with thousands of repeated elements:
- Define once, reference many times
- Significant reduction in input file size
- Easier to modify and maintain
- Clear hierarchical organization

### Volume Calculations

**For repeated structures:**
- Must specify total volume of material in ALL instances of repeated cell
- Not just volume of single instance
- Example: 100 identical cells, each 5 cm³ → Specify VOL = 500 cm³

---

## INTEGRATION WITH OTHER MCNP FEATURES

### With Tallies

- Can tally on specific lattice elements using expanded cell notation
- Can tally on entire universe
- Segment tallies by lattice element possible

### With Variance Reduction

- Importance assigned to universe cells = multiplier of filled cell importance
- Mesh-based weight windows automatically handle repeated structures
- Non-mesh weight windows: more complex with universes

### With Source Definition

- General source (SDEF) can be defined in repeated structures
- Surface sources CANNOT use surfaces from repeated structures
- Must use real-world surfaces only

### With Geometry Plotting

- Repeated structures plotted correctly
- Can display lattice indices on plots
- Essential tool for verification
- Use multiple views and zoom levels

---

## SUMMARY OF KEY TAKEAWAYS

1. **Lattices require four cards:** LAT, U, FILL, plus cell card with proper surface order
2. **Surface order matters:** Defines lattice indexing scheme
3. **Two lattice types:** Hexahedral (LAT=1) and hexagonal prism (LAT=2)
4. **FILL flexibility:** Single universe OR array of universes
5. **Transformation power:** TRCL allows positioning without redefinition
6. **Negative universe optimization:** Use only when safe, verify thoroughly
7. **Verification essential:** Always plot geometry, especially with lattices
8. **No speed benefit:** Repeated structures save input/memory, not runtime
9. **Volume specification:** Must account for ALL instances in repeated structure
10. **Hierarchical power:** Up to 20 levels of nesting possible

---

**END OF LATTICE-INFO-SUMMARY.MD**

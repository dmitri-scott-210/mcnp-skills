# MCNP Geometry Templates

This directory contains reusable templates for common MCNP geometry patterns. Each template includes detailed instructions and parameter explanations.

## Available Templates

### 1. nested_spheres_template.i
**Purpose:** Multi-layer concentric spherical shells (shielding, detector layers, target/moderator systems)

**Use When:**
- Spherically symmetric geometry
- Multiple material layers (fuel/reflector/shield)
- Center-point source problems

**Key Parameters:**
- `<r1>` through `<r4>`: Shell radii (increasing order)
- `<mat#>` and `<dens#>`: Material numbers and densities
- Volume calculations: V = (4/3)π(r_outer³ - r_inner³)

**Example Application:** Bare sphere criticality, detector calibration sphere, target-moderator assembly

---

### 2. cylinder_array_template.i
**Purpose:** Rectangular (NxN) array of cylindrical pins using LAT=1 lattice

**Use When:**
- PWR/BWR fuel assemblies
- Rectangular pin arrays (detector arrays, control rod clusters)
- Research reactor elements

**Key Parameters:**
- `FILL=<imin>:<imax> <jmin>:<jmax> 0:0` - Array dimensions
- `<r_core>`, `<r_clad>`, `<r_cell>` - Pin dimensions (must satisfy r_core < r_clad < r_cell)
- Lattice boundaries from pitch × count

**LAT=1 Index Ordering (CRITICAL):**
- i (X) varies FASTEST (innermost loop)
- j (Y) varies MIDDLE
- k (Z) varies SLOWEST (outermost loop)

**Example Application:** 17×17 PWR assembly, 3×3 test lattice, BWR bundle

---

### 3. hex_lattice_template.i
**Purpose:** Hexagonal lattice using LAT=2 with RHP macrobody

**Use When:**
- VVER assemblies
- AGR fuel elements
- Hexagonal research reactor cores
- HTGR graphite blocks

**Key Parameters:**
- `RHP` surface: **9 values minimum** (vx vy vz, h1 h2 h3, r1 r2 r3)
  - **r1 r2 r3 is apothem VECTOR** (perpendicular distance from center to face)
  - For flat-to-flat distance = 2p: apothem vector = (p, 0, 0) or (0, p, 0)
- `FILL=<ring_min>:<ring_max>` - Hexagonal ring indexing

**LAT=2 Ring Indexing:**
- Ring 0: 1 element (center)
- Ring 1: 6 elements
- Ring 2: 12 elements
- Ring n: 6n elements

**Common Configurations:**
- 7 pins: FILL=0:1 (1 + 6)
- 19 pins: FILL=0:2 (1 + 6 + 12)
- 37 pins: FILL=0:3 (1 + 6 + 12 + 18)

**Example Application:** VVER-1000 assembly, prismatic HTGR fuel element

---

### 4. transformed_geometry_template.i
**Purpose:** Coordinate transformations using TR cards for positioning/rotating geometry

**Use When:**
- Multiple copies of same object at different locations/orientations
- Skewed cylinders, rotated boxes
- Complex assemblies with rotational symmetry
- Simplifying surface definitions in auxiliary coordinate systems

**Key Features:**
- **TR card:** Surface transformations (n ≤ 999)
- **TRCL parameter:** Cell transformations (unlimited n)
- ***TR card:** Angles in degrees (easier than direction cosines)

**Transformation Types:**
- Translation only: `TR1  10 0 0` (move 10 cm along x)
- Rotation only: `*TR2  0 0 0  90 0 90  0 90 0  90 90 0` (90° about z)
- Combined: `*TR3  5 5 0  45 45 90  135 45 90  90 90 0` (translate + rotate 45°)

**Example Application:** Rotated fuel assemblies, detector banks at angles, reflected geometry

---

## Template Usage Workflow

### Step 1: Select Template
Choose template based on geometry type:
- Spherical → nested_spheres
- Rectangular pin array → cylinder_array
- Hexagonal array → hex_lattice
- Positioned/rotated objects → transformed_geometry

### Step 2: Copy Template
```bash
cp nested_spheres_template.i my_problem.inp
```

### Step 3: Replace Placeholders
Search for `<...>` patterns and replace with actual values:
- `<mat1>` → Material number (e.g., 1, 2, 3)
- `<dens1>` → Density (negative for g/cm³, positive for atoms/b-cm)
- `<r_core>` → Dimension in cm
- `<ZAID>` → Isotope ID (e.g., 92235.80c, 1001.80c)
- `<frac>` → Atomic fraction (sum to 1.0 for each material)
- `<energy>` → Source energy in MeV
- `<histories>` → NPS count (e.g., 10000, 1000000)

### Step 4: Verify MCNP Format
**CRITICAL - Check before running:**
- Title card on line 1 ✓
- Cell Cards block (NO internal blank lines) ✓
- EXACTLY ONE blank line after Cell Cards ✓
- Surface Cards block (NO internal blank lines) ✓
- EXACTLY ONE blank line after Surface Cards ✓
- Data Cards block ✓
- Total: EXACTLY 2 blank lines in entire file ✓

### Step 5: Validate Geometry
```bash
# Geometry check (no particle transport)
mcnp6 inp=my_problem.inp ip

# Check for errors in output
grep -i "error\|warning\|fatal" my_problem.outp
```

### Step 6: Test Run
```bash
# Short test run (low NPS)
mcnp6 inp=my_problem.inp outp=test.out

# Check particle tracking, no lost particles
grep "lost" test.out
```

---

## Common Template Modifications

### Adding Tallies
Insert after material cards, before NPS:
```
c --- Tallies ---
F4:N  1 2 3          $ Track-length flux in cells 1, 2, 3
E4    1E-8 20I 20    $ 20 log-spaced bins from 1E-8 to 20 MeV
```

### Changing Source
Replace `SDEF` card:
```
c Point source:
SDEF  POS=0 0 0  ERG=14.1

c Volumetric source:
SDEF  CEL=1  ERG=D1
SI1   0 5 10         $ Energy bins (MeV)
SP1   0 0.3 0.7      $ Cumulative probabilities

c Surface source:
SDEF  SUR=1  DIR=D1  ERG=2.0
SI1  -1 0.8 1        $ Cosine bins (inward directed)
SP1   0 0.5 1        $ Probabilities
```

### Adding Variance Reduction
Insert importance cards:
```
IMP:N  1 1 2 4 8 0   $ Increasing importance away from source
```

---

## Template Verification Checklist

Before using modified template:
- [ ] All `<...>` placeholders replaced
- [ ] Material definitions complete (M cards with valid ZAIDs)
- [ ] Cross-references valid (cell materials, surface numbers)
- [ ] Dimensions physically reasonable (no negative radii, proper nesting)
- [ ] Exactly 2 blank lines in file (one after cells, one after surfaces)
- [ ] No blank lines WITHIN cell or surface blocks
- [ ] Comments use 'c' or '$', not '//' or '#'
- [ ] Geometry plotted (`mcnp6 inp=file.i ip`)
- [ ] No lost particles in test run

---

## Troubleshooting

### "Fatal Error: Cell X undefined"
**Cause:** Missing cell card or cell numbering gap
**Fix:** Verify all cells from 1 to J are defined

### "Warning: Cell volumes not calculated"
**Cause:** Complex geometry, non-polyhedral cells
**Fix:** Add `VOL=<value>` to cell cards or use stochastic volume calculation

### "Lost Particle in Cell X"
**Cause:** Geometry gaps, overlaps, or errors
**Fix:** Use `VOID` card testing, plot geometry, check Boolean operations

### "Bad Trouble: Surface X does not exist"
**Cause:** Cell references undefined surface
**Fix:** Verify all surfaces in cell definitions are defined in surface block

### "RHP/HEX specification error"
**Cause:** Using scalar instead of vector for apothem
**Fix:** RHP requires 9 values: vx vy vz, h1 h2 h3, **r1 r2 r3** (vector, not scalar!)

---

## Additional Resources

**Reference Documentation (in ../references/):**
- `surface_types_comprehensive.md` - All surface types and equations
- `macrobodies_reference.md` - Macrobody specifications (BOX, RPP, RCC, RHP, etc.)
- `cell_definition_comprehensive.md` - Cell card format and Boolean operations
- `lattice_geometry_reference.md` - LAT=1 and LAT=2 detailed specifications
- `transformations_reference.md` - TR card usage and examples

**Example Files (in ../example_geometries/):**
- `01_nested_spheres.i` - Working nested sphere example
- `04_simple_lattice.i` - 3×3 LAT=1 array
- `06_transformed_geometry.i` - TR card examples
- `10_nested_universe.i` - Universe hierarchy

**MCNP Documentation:**
- MCNP6 User Manual, Chapter 5: Input Cards
- MCNP6 Primer (LA-UR-20-20530)

---

## Template Development Guidelines

If creating new templates:
1. Use `<parameter_name>` for all user-replaceable values
2. Include detailed instructions in comments at end of file
3. Provide at least 2 examples showing parameter usage
4. Verify MCNP format (2 blank lines total, correct block structure)
5. Test with `mcnp6 ip` before committing
6. Document common pitfalls and restrictions
7. Add to this README with use cases

---

**Note:** These templates follow MCNP6.3 syntax and have been verified against the official MCNP6 User Manual Chapter 5 specifications.

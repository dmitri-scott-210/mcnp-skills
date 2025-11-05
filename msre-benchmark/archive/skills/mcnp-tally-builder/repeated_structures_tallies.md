# Repeated Structures Tallies

## Overview

MCNP provides specialized syntax for tallying in lattice elements and repeated structures using bracket notation and universe format shorthand. These features are essential for reactor core modeling, fuel assembly analysis, and any geometry with periodic structures.

## Bracket Notation for Lattice Elements

### Syntax Forms

**Single Element:**
```
Fn:p cell[i j k]
```

**Element Range:**
```
Fn:p cell[i1:i2 j1:j2 k1:k2]
```

**Individual Elements:**
```
Fn:p cell[i1 j1 k1, i2 j2 k2, i3 j3 k3]
```

### Index Interpretation

- `i, j, k` - Lattice indices in x, y, z directions
- Indices start at 0 for centered lattices
- Range includes both endpoints (i1:i2 includes i1, i1+1, ..., i2)

### Example: Single Fuel Pin

```
F4:n 10[0 0 0]     $ Tally in lattice element at (0,0,0)
```

For cell 10 in LAT=1 hexagonal prism lattice or LAT=2 hexagonal lattice

### Example: Central 3×3 Region

```
F4:n 10[-1:1 -1:1 0]   $ Central 3×3 elements at z-level 0
```

Creates 9 tally bins (3×3) for adjacent elements

### Example: Specific Elements

```
F4:n 10[0 0 0, 5 5 0, -3 2 1]   $ Three specific elements
```

Creates 3 separate tally bins

## Universe Format Shorthand

### U=# Syntax

```
Fn:p U=#
```

Expands to all cells filled by universe number #

### Example Usage

**Geometry:**
```
c Cell 1 fills entire lattice with universe 5
1 0 -100 FILL=5 LAT=1
c Universe 5 defines fuel pin
5 like 1 but U=5
```

**Tally:**
```
F4:n U=5      $ Tally in all instances of universe 5
```

Automatically tallies in every lattice element containing universe 5

### Advantages

- No need to enumerate all lattice indices
- Robust to geometry changes (add/remove lattice elements)
- Simpler input for large lattices

### Limitations

- Cannot specify subset of elements (all or nothing)
- Use bracket notation for selective element tallying

## Lattice Tally Chains

### Chain Operator (<)

```
Fn:p cell1 < cell2[i j k]
```

Specifies cell1 within the lattice element cell2[i j k]

### Nested Universe Example

**Geometry:**
```
c Outer lattice (cell 1) contains inner lattices
1 0 -10 FILL=2 LAT=1
c Universe 2 contains cell 3 (fuel) and cell 4 (clad)
3 1 -10.4 -30 U=2
4 2 -6.5 30 -31 U=2
```

**Tally:**
```
F4:n 3<1[5 5 0]    $ Cell 3 within lattice element [5,5,0] of cell 1
```

### Multi-Level Nesting

```
F4:n cell1 < cell2[i j k] < cell3[l m n]
```

Three levels: cell1 within element [i,j,k] of cell2, which is in element [l,m,n] of cell3

## Multiple Bin Format (N×M×P Bins)

### Creating Product Bins

```
F4:n (10[0:2 0 0]) (10[0 1:3 0])
```

Creates 3 bins × 3 bins = 9 total bins:
- First set: [0,0,0], [1,0,0], [2,0,0]
- Second set: [0,1,0], [0,2,0], [0,3,0]

### Factorized Binning

**Syntax:**
```
F4:n (cellA[range1]) (cellB[range2]) (cellC[range3]) T
```

Total bins = bins(range1) × bins(range2) × bins(range3) + 1 (if T)

**Example:**
```
F4:n (10[-5:5 0 0]) (10[0 -5:5 0]) T
```

Creates 11×11 = 121 bins plus 1 total bin = 122 total

## SD Card for Repeated Structures

### Two Distinct Options

**Option 1: Volumes for lattice elements not explicitly in problem**
```
F4:n 10[0:4 0:4 0]
SD4 1.0        $ Each of 25 elements divided by 1.0 cm³
```

**Option 2: Cell filling universe has volume**
```
F4:n U=5
SD4 8.547      $ Volume 8.547 cm³ for each instance of universe 5
```

### When SD Required

- Lattice element volumes cannot be calculated automatically
- Complex fill patterns where MCNP volume calculator fails
- User wants consistent normalization across elements

### When SD Not Required

- Simple lattice geometries (rectangular pins in square lattice)
- MCNP successfully calculates volumes (no warning in output)

## SPDTL Card for Performance

### Purpose

The SPDTL card controls track-length tallies (F4) in lattices for performance.

**Syntax:**
```
SPDTL option
```

**Options:**
- `-1` - No special treatment (default behavior)
- `0` - Optimize for large lattices with few elements tallied
- `1` - Optimize for tallying many elements

### When to Use

**Large Lattice (e.g., 21×21×20), Few Tallied:**
```
F4:n 10[10 10 10]   $ Only center element
SPDTL 0             $ Optimize for sparse tallying
```

**Large Lattice, Many Tallied:**
```
F4:n 10[0:20 0:20 0:19]   $ All 8,820 elements
SPDTL 1                   $ Optimize for dense tallying
```

### Performance Impact

- Can significantly reduce runtime for large lattice problems
- Test both settings to determine optimal for specific geometry
- Monitor MCNP output for performance statistics

## Practical Examples

### Example 1: PWR Fuel Assembly (17×17)

```
c Tally flux in central 5×5 fuel pins
F4:n 100[-2:2 -2:2 0]     $ 25 central pins
FM4 -1.0 235 -6 -7        $ Fission rate
SD4 1                     $ Normalize to 1 cm³ per pin
SPDTL 0                   $ Sparse tally in large lattice
```

### Example 2: Full Reactor Core Power Distribution

```
c 193 fuel assemblies, tally all
F4:n U=10                 $ Universe 10 = fuel assembly cell
FM4 (-1.0 235 -6 -7) (-1.0 238 -6 -7) T   $ U-235 and U-238 fission
SD4 1                     $ Consistent normalization
FQ4 F M E                 $ Organize output: assembly, fission type, energy
SPDTL 1                   $ Dense tallying
```

### Example 3: Axial Power Profile

```
c Tally in central assembly at multiple axial levels
F4:n 100[0 0 0:19]        $ 20 axial levels in central assembly
E4 0 0.1 20               $ Thermal and fast
FM4 -1.0 235 -6 -7        $ Fission rate
```

### Example 4: Hot Channel Analysis

```
c Identify hottest fuel pins
F4:n 100[-8:8 -8:8 10]    $ All pins at mid-plane (17×17 = 289 pins)
FM4 -1.0 92235 -6         $ U-235 fission
FQ4 F E                   $ Pin by energy
```

### Example 5: Peripheral vs Interior Comparison

```
c Compare edge pins to interior pins
F4:n (100[-8 -8:8 0]) (100[0 0 0])   $ Edge row vs center pin
FM4 -1.0 235 -6 -7
```

## Output Interpretation

### Bin Numbering

MCNP numbers lattice element bins sequentially:
- [0,0,0] = bin 1
- [1,0,0] = bin 2
- [0,1,0] = bin 3 (for range [0:1 0:1 0])
- etc.

### MCTAL File

Lattice element data appears in MCTAL with:
- Tally number
- Bin identification
- Value and relative error

### Post-Processing

Extract data and reshape to lattice geometry:
- Python: `data.reshape((ni, nj, nk))`
- MATLAB: `reshape(data, ni, nj, nk)`
- Visualize as 2D slice or 3D volume

## Integration with Other Features

### Tally Segmentation (FS)

Can segment lattice element tallies:
```
F4:n 100[5 5 0]
FS4 -20 T       $ Subdivide element into regions
```

### Energy Bins

```
F4:n 100[-5:5 -5:5 0]
E4 0 0.625e-6 20    $ Thermal and fast groups
```

Creates 11×11×2 = 242 bins

### Time Bins

```
F4:n U=5
T4 0 1e-6 1e-3 1e0  $ Time evolution
```

Useful for kinetics calculations in lattices

## Common Pitfalls

1. **Incorrect Index Range**
   - Remember ranges are inclusive: [0:2] = 3 elements (0, 1, 2)
   - Verify lattice dimensions match indices

2. **Mixing Bracket and Non-Bracket**
   - Cannot mix: `F4:n 10 10[0 0 0]` is invalid
   - Use separate tallies if needed

3. **Chain Operator Confusion**
   - Order matters: `3<1[i j k]` ≠ `1[i j k]<3`
   - First cell is innermost in nesting hierarchy

4. **SD Card Errors**
   - Wrong number of entries (must match bins)
   - Using wrong SD option for lattice type

5. **Performance Issues**
   - Tallying too many elements without SPDTL
   - Creating excessive bins (10,000+)

## Best Practices

1. **Start small** - Test with single element, then expand
2. **Use U=# when possible** - Simpler and more robust
3. **Visualize first** - MCNP plotter shows lattice structure
4. **Check output** - Verify bin numbering matches expectation
5. **Monitor statistics** - Many bins = lower statistics per bin
6. **Use SPDTL** - Significant performance gains for large lattices
7. **Organize output with FQ** - Makes multi-bin output readable
8. **Post-process systematically** - Consistent scripts for lattice data extraction
9. **Document indices** - Comment cards explaining lattice indexing
10. **Validate with known case** - Test against analytical solution or simplified geometry

## See Also

- **SKILL.md** - Main tally workflow
- **tally_flagging_segmentation.md** - FS and SD card details
- **Chapter 5.09 Section 5.9.1.5** - MCNP Manual repeated structures syntax
- **Chapter 4 Geometry** - LAT and FILL specifications
- **mcnp-lattice-builder** - Skill for creating repeated structure geometries

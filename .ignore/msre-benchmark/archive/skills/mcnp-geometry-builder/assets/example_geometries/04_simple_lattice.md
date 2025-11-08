# Example 4: Simple 3×3 Lattice

## Purpose
Demonstrates rectangular lattice (LAT=1) with multiple pin types in a 3×3 array.

## Concepts Illustrated
- **Universe (U) parameter** - Define repeated units in local coordinates
- **LAT=1** - Rectangular lattice type
- **FILL parameter** - Index ordering (i,j,k) = (X,Y,Z)
- **Multiple universes** - Two pin types in same lattice
- **Nested geometry** - Pin → Lattice → Base universe

## Geometry Description

### Universe 1 (Fuel Pin):
- Fuel pellet: r < 0.5 cm
- Cladding: 0.5 < r < 0.55 cm
- Water: 0.55 < r < 0.707 cm (pin cell boundary)

### Universe 2 (Control Rod):
- Cadmium absorber: r < 0.5 cm
- Cladding: 0.5 < r < 0.55 cm
- Water: 0.55 < r < 0.707 cm

### Lattice (Universe 3):
3×3 array from i=-1:1, j=-1:1, k=0:0

FILL array (read i varies fastest):
```
j=1:  1 1 2  (fuel, fuel, control rod)
j=0:  1 1 1  (all fuel)
j=-1: 2 1 1  (control rod, fuel, fuel)
```

## Materials
- M1: UO₂ (4% enriched)
- M2: Zircaloy cladding
- M3: Light water with thermal scattering
- M4: Cadmium absorber

## Source
Volumetric source throughout filled lattice cell (CEL=30) with 2.0 MeV neutrons

## Index Ordering (CRITICAL)
For LAT=1, FILL array is read with **i (X) varying fastest**:
- **Outer loop**: k (Z) - slowest
- **Middle loop**: j (Y)
- **Inner loop**: i (X) - fastest

Reading order: (k, j, i) → (0, -1, -1), (0, -1, 0), (0, -1, 1), (0, 0, -1), ...

## Usage
```bash
mcnp6 inp=04_simple_lattice.i
```

## Expected Results
- Fission neutrons from fuel pins
- Strong absorption in control rods
- Thermal flux peak in water
- Asymmetric flux pattern (2 control rods in opposite corners)

## Learning Points
1. **U parameter**: Defines geometry in local coordinate system
2. **LAT=1**: Requires box geometry (6 PX/PY/PZ planes)
3. **FILL indexing**: i varies fastest (inner loop)
4. **Pitch calculation**: (X_max - X_min) / (i_max - i_min + 1)
5. **Nested filling**: Universe 3 fills base cell 30

## Pitch Calculation
- X range: -1.5 to 1.5 = 3.0 cm
- i range: -1 to 1 = 3 cells
- Pitch: 3.0 / 3 = 1.0 cm

## Modifications to Try
- Add more pin types (U=3 for guide tube, U=4 for instrument tube)
- Expand to 5×5 or 17×17 array
- Add axial layers (k=0:1 for two-height lattice)
- Try different control rod patterns
- Add F4 tally for each cell in lattice

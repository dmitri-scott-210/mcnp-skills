# Example 10: Nested Universe Hierarchy

## Purpose
Demonstrates three-level universe nesting without lattices: pin → assembly → core.

## Concepts Illustrated
- **Four universe levels**: U=1 (pin), U=2 (assembly), U=3 (core), U=0 (base)
- **FILL without LAT** - Single universe filling (not array)
- **Hierarchical geometry** - Each level contains the previous
- **Local coordinates** - Each universe has its own origin

## Geometry Hierarchy

### Level 1: Pin (Universe 1)
- Defined in local coordinates centered at (0,0,0)
- Fuel: r < 0.5 cm
- Clad: 0.5 < r < 0.6 cm
- Void: r > 0.6 cm (fills to assembly boundary)

### Level 2: Assembly (Universe 2)
- Contains one pin from U=1 at assembly center
- Boundary: 4×4×10 cm box (RPP -2 to 2 in X,Y)
- FILL=1 places pin universe at assembly origin

### Level 3: Core (Universe 3)
- Contains one assembly from U=2 at core center
- Boundary: 10×10×14 cm box
- FILL=2 places assembly universe at core origin

### Level 4: Base Geometry (Universe 0)
- Contains core from U=3
- Boundary: 20×20×20 cm box
- FILL=3 places core universe in base cell 30
- Graveyard surrounds everything

## Materials
- M1: UO₂ fuel (4% enriched)
- M2: Zircaloy cladding

## Source
Volumetric source in filled base cell (CEL=30) with 2.0 MeV neutrons

## Usage
```bash
mcnp6 inp=10_nested_universe.i
```

## Expected Results
- Single pin at center of nested geometry
- Particles track through pin → assembly void → core void → base void → graveyard
- Simple hierarchy for understanding FILL mechanics

## Learning Points
1. **Universe nesting**: Each FILL references universe from previous level
2. **Local coordinates**: Each universe centered at (0,0,0) in its own system
3. **FILL vs LAT**: FILL alone = single copy, FILL with LAT = array
4. **Hierarchy depth**: Can nest many levels (pin → assembly → core → reactor)
5. **Cell 30 contains everything**: All nested universes inside base cell 30

## Comparison to LAT=1 Example
- Example 04 used LAT=1 for 3×3 array (9 pins)
- This example uses FILL only (1 pin)
- Both use U parameter, but LAT creates array

## Modifications to Try
- Add second pin in assembly (define cells 11, 12, 13 in U=2)
- Use LAT=1 at assembly level for pin array
- Add more hierarchy levels (reactor → building)
- Transform assembly with TRCL

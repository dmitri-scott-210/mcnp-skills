# Example 1: Nested Spheres

## Purpose
Demonstrates the most basic MCNP geometry: three concentric spherical shells with a point source at the origin.

## Concepts Illustrated
- **Cell definitions** with material number, density, and geometry
- **Spherical surfaces** using SO card (sphere at origin)
- **Intersection geometry**: `-1` (inside surf 1), `1 -2` (outside 1, inside 2)
- **Importance specification**: IMP:N increasing with depth (variance reduction)
- **Graveyard cell**: IMP:N=0 for particle termination
- **Volume specification**: VOL parameter for normalization

## Geometry Description
- **Cell 1**: Tungsten core, r < 2 cm
- **Cell 2**: Lead shield, 2 cm < r < 4 cm
- **Cell 3**: Iron shield, 4 cm < r < 6 cm
- **Cell 4**: Void region, 6 cm < r < 20 cm
- **Cell 5**: Graveyard, r > 20 cm

## Materials
- M1: Tungsten (W, Z=74) at 19.0 g/cm³
- M2: Lead (Pb, Z=82) at 10.5 g/cm³
- M3: Iron (Fe, Z=26) at 8.0 g/cm³

## Source
Point isotropic source at origin with 14.1 MeV neutrons (D-T fusion energy)

## Usage
```bash
mcnp6 inp=01_nested_spheres.i
```

## Expected Results
- Flux should decrease through each shield layer
- Importance increases (1→2→4) to improve statistics in outer regions
- Most particles absorbed in tungsten core

## Learning Points
1. Surface sense: `-n` means inside surface n
2. Intersection: Multiple surface numbers with spaces = AND operation
3. Graveyard: Always use IMP:N=0 for outermost cell
4. Density: Negative value = mass density (g/cm³)
5. Importance: Higher values = more particle splitting (better statistics)

## Modifications to Try
- Change shield materials (different Z values)
- Add more shells
- Modify importance values
- Change source energy
- Add tallies (F4 cell flux, F2 surface current)

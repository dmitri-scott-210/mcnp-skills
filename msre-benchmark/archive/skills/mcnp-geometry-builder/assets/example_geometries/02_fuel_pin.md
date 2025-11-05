# Example 2: Cylindrical Fuel Pin

## Purpose
Demonstrates a realistic PWR (Pressurized Water Reactor) fuel pin with four regions: fuel, gap, cladding, and coolant.

## Concepts Illustrated
- **Cylindrical surfaces** using CZ card (cylinder on Z-axis)
- **Planar boundaries** using PZ card (planes perpendicular to Z-axis)
- **Multi-region geometry**: Four concentric cylinders
- **Union operator** `:` for graveyard (outside OR above OR below)
- **Gap region**: Void cell between fuel and clad
- **Thermal scattering**: MT card for water (lwtr.10t)

## Geometry Description
- **Cell 1**: UO₂ fuel pellet, r < 0.4095 cm, 0 < z < 365.76 cm
- **Cell 2**: Helium gap (void), 0.4095 < r < 0.4180 cm
- **Cell 3**: Zircaloy cladding, 0.4180 < r < 0.4750 cm
- **Cell 4**: Water coolant, 0.4750 < r < 0.6350 cm (square pitch boundary)
- **Cell 5**: Graveyard, outside pin cell or beyond axial boundaries

## Materials
- M1: UO₂ (4% enriched uranium dioxide)
  - U-235: 4 wt%
  - U-238: 96 wt%
  - Oxygen: 2 atoms per U
- M2: Zircaloy (Zr, Z=40) at 6.56 g/cm³
- M3: Light water (H₂O) with thermal scattering data

## Source
Uniform volumetric source in fuel with 2.0 MeV neutrons (approximates fission spectrum peak)

## Usage
```bash
mcnp6 inp=02_fuel_pin.i
```

## Expected Results
- Fission neutrons thermalize in water
- Most flux in fuel and moderator
- Clad acts as structural material (low absorption)
- Gap improves thermal performance (real physics)

## Learning Points
1. CZ surfaces define cylinders centered on Z-axis
2. PZ surfaces truncate cylinders axially
3. Gap cell uses `m=0` (void) but still has geometry
4. Union `:` in graveyard: `(4 : 10 : -11)` = outside 4 OR below 10 OR above 11
5. MT card specifies thermal scattering library for low-energy neutrons

## Typical PWR Parameters
- Fuel radius: 0.4095 cm (standard UO₂ pellet)
- Clad thickness: 0.057 cm (Zircaloy-4)
- Pin pitch: 1.26-1.27 cm (square lattice)
- Active height: 365.76 cm (12 feet)
- Enrichment: 3-5% U-235

## Modifications to Try
- Change enrichment (M1 U-235 fraction)
- Vary clad thickness
- Add plenum region above fuel
- Model actual square pin cell (use PX/PY instead of CZ for cell 4)
- Add F4 tally for flux in each region

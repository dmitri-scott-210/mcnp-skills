# Example 1: Simple Cartesian FMESH

**Purpose:** Basic FMESH card for uniform Cartesian mesh

**File:** `01_simple_fmesh_cartesian.i`

## Description

Demonstrates simplest FMESH setup:
- 20×20×20 mesh covering a water sphere
- Uniform binning (20 bins per direction)
- XDMF output for ParaView visualization
- 14 MeV neutron point source at origin

## Key Features

- **Geometry:** XYZ Cartesian
- **Extent:** -10 to +10 cm in all directions
- **Resolution:** 1 cm per bin (20 bins × 1 cm = 20 cm total)
- **Total bins:** 8,000 (20×20×20)
- **Output:** XDMF format for ParaView

## Physics

- Water sphere (radius 20 cm)
- 14 MeV neutron source (fusion neutrons)
- Flux mesh tally (tracks/cm² per source particle)

## Expected Results

- Peak flux at origin (source location)
- Exponential attenuation with distance
- Relatively uniform azimuthal distribution

## Visualization

```bash
# Run MCNP
mcnp6 i=01_simple_fmesh_cartesian.i

# Open in ParaView
paraview meshtal.xdmf
```

## Use Case

- Testing FMESH setup
- Verifying mesh extent covers geometry
- Learning XDMF output format

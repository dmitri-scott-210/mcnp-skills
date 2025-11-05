# Magnetic Field Tracking Reference

## Overview

MCNP6 provides two methods for simulating magnetic field effects on charged particles:

1. **Transfer Map Method** (COSY INFINITY) - Fast, accurate, vacuum only, narrow energy spread
2. **Particle Ray Tracing** (MARS-based) - Versatile, material/vacuum, wide energy range

## Method 1: COSY Transfer Maps

### Advantages
- Very fast (precomputed maps applied in one step)
- High accuracy within convergence volume

### Limitations
- Void regions only (no material)
- Limited to one particle type per map
- Finite convergence volume in phase space
- Maps specific to reference momentum

### Cards: COSYP and COSY

#### COSYP: Map File Parameters

```
COSYP prefix axsh axsv emapk...
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| prefix | required | COSY map file prefix number |
| axsh | 1 | Horizontal axis (1=x, 2=y, 3=z) |
| axsv | 2 | Vertical axis (1=x, 2=y, 3=z) |
| emapk | map energy | Operating beam energy of kth map (MeV) |

#### COSY: Cell Assignments

```
COSY m1 m2 ... mJ
```

Assigns COSY map number to each cell (J = total cells).

#### Example

```
COSYP 57 2 1 23070 11R
COSY 3J 1 J 2 J 3 J 4 10J 5 J 5 J 6 J 6
```

- Map files: 571, 572, 573, 574, 575, 576
- Horizontal axis: y, Vertical axis: x
- Operating energy: 23,070 MeV for all maps
- Cell 4 uses map 1, cell 6 uses map 2, etc.

## Method 2: Magnetic Field Ray Tracing

### Advantages
- Works in void AND material cells
- Wide energy range
- Multiple particle types
- Quadrupole fringe-field effects (edge kicks)

### Limitations
- Particles can get lost in complex geometries
- Rare cases: infinite loops

### Supported Field Types

1. **Dipole (CONST):** Uniform field
2. **Quadrupole (QUAD):** Gradient field
3. **Quadrupole with Fringe Fields (QUADFF):** Includes edge kicks

### Cards: BFLD and BFLCL

#### BFLD: Field Definition

```
BFLDn type KEYWORD=value
```

**Required:**
- n: Magnetic field ID number
- type: const, quad, or quadff
- field: Field strength or gradient

**Keywords:**

| Keyword | Description | Units | Default |
|---------|-------------|-------|---------|
| field | Field strength (const) or gradient (quad/quadff) | Tesla or T/cm | required |
| vec | Field direction (const) or focusing direction (quad) | direction cosines | 1 0 0 |
| axs | Quadrupole beam axis direction (quad/quadff only) | direction cosines | 0 0 1 |
| refpnt | Point on quadrupole beam axis (quad/quadff only) | cm | 0 0 0 |
| mxdeflc | Maximum deflection angle per step | mrad | 10 |
| maxstep | Maximum step size | cm | 100 |
| ffedges | Surface numbers for fringe-field kicks (quadff only) | list | none |

#### BFLCL: Field Cell Assignment

```
BFLCL m1 m2 ... mJ
```

Assigns magnetic field m to each cell (J = total cells).

### Examples

#### Example 1: Constant Dipole Field

```
BFLD1 CONST FIELD=0.03 VEC=0 1 0
BFLCL 2J 1
```

- Field strength: 0.03 Tesla
- Direction: +y
- Applied to cell 3

#### Example 2: Quadrupole with Fringe Fields

```
BFLD2 QUADFF FIELD=0.195 FFEDGES=31 2I 34
BFLCL 31J 2 0 2
```

- Gradient: 0.195 T/cm
- Fringe-field kicks at surfaces 31, 32, 33, 34
- Applied to cells 32 and 34

#### Example 3: Quadrupole with Custom Axis

```
BFLD3 QUAD FIELD=0.116 &
      VEC=0.5 0.5 0.707 &
      AXS=0.85 -0.14 -0.5 &
      REFPNT=40 30 100 &
      MXDEFLC=10 MAXSTEP=1
BFLCL 101J 3 0 3 7J 3 0 3
```

- Gradient: 0.116 T/cm
- Focusing direction: (0.5, 0.5, 0.707)
- Beam axis: (0.85, -0.14, -0.5) through point (40, 30, 100)
- Max step: 1 cm, max deflection: 10 mrad
- Applied to cells 102, 104, 112, 114

## Fringe-Field Edge Kicks

For quadrupole fields (QUADFF type), particles passing through upstream/downstream fringe experience position and momentum jumps (third-order aberrations).

**Equations (particle along z-axis):**

Δx' = -(G p/q) x² / 2
Δy' = +(G p/q) y² / 2
Δx = -(G p/q) x y
Δy = +(G p/q) x y

Where:
- x', y' = direction cosines
- G = gradient (T/m)
- p/q = particle rigidity (T-m)

**For downstream fringe:** Replace G p/q with -G p/q.

## Choosing Method

**Use COSY Maps when:**
- Vacuum transport through beam optics
- Narrow energy spread (<10% typical)
- High speed required
- Magnetic elements well-characterized
- Particle type consistent with map

**Use Ray Tracing when:**
- Transport through materials
- Wide energy range
- Multiple particle types
- Fringe-field effects important
- Magnetic field not available as COSY map

## Integration

**Required Before Magnetic Fields:**
- MODE must include charged particles (H, E, /, D, T, S, A, etc.)
- PHYS cards for charged particles

**Related Skills:**
- mcnp-source-builder - Define charged particle beams
- mcnp-geometry-builder - Create beam line geometry
- mcnp-tally-builder - Tally at focal planes, image planes
- mcnp-fatal-error-debugger - Debug lost particles in magnetic fields

**Common Applications:**
- Proton radiography beam lines
- Proton therapy gantries
- Mass spectrometers
- Particle accelerator beam transport
- Magnetic lenses

# MCNP Cell Parameters - Complete Reference

Cell parameters modify cell behavior beyond basic material and geometry. MCNP provides 18 cell parameters that control variance reduction, universe hierarchy, transformations, temperature, and physics options.

## Parameter Placement Rules

**Two locations:**
1. **On cell card** (after geometry): `1  1  -10.5  -1  IMP:N=1  VOL=100`
2. **In data block** (separate card): `IMP:N  1  1  1  1  0` (values for cells 1-5)

**Critical rule:** Same parameter CANNOT be in both locations for same cell

**Recommendation:** Use cell card placement for clarity (parameter tied to specific cell)

---

## Particle Designators

Many parameters require particle type specification using colon syntax:

**Format:** `PARAMETER:particle`

**Common designators:**
- `:N` - Neutrons
- `:P` - Photons
- `:E` - Electrons
- `:N,P` - Both neutrons and photons
- `:#` - All particles in MODE card

**Example:**
```
1  1  -10.5  -1  IMP:N=1  IMP:P=0.5  IMP:E=0  $ Different importance for each particle
```

---

## 1. IMP (Importance)

**Purpose:** Variance reduction - controls particle splitting and Russian roulette

**Syntax:** `IMP:particle=value`

**Values:**
- `IMP=0`: Particle killed when entering cell (use for graveyard/boundary)
- `IMP>0`: Relative importance (higher = more particles, better statistics)
- Default: 1 if not specified (no variance reduction)

**Common patterns:**
```
c Deep penetration problem - increase importance with depth
1  1  -10.5  -1  IMP:N=1      $ Source region
2  2  -8.0    1 -2  IMP:N=2   $ Shield layer 1 (2x splitting)
3  2  -8.0    2 -3  IMP:N=4   $ Shield layer 2 (4x from source)
4  3  -1.0    3 -4  IMP:N=8   $ Detector region (8x from source)
5  0          4     IMP:N=0   $ Graveyard
```

**Particle behavior:**
- Moving to higher IMP cell: Particle splits (creates copies)
- Moving to lower IMP cell: Russian roulette (may be killed)
- Split/roulette factor = IMP_new / IMP_old

**Best practices:**
- Always specify IMP explicitly (don't rely on default)
- IMP must be specified for ALL particles in MODE card
- Typical pattern: Increase by factors of 2 or 4
- Set IMP:N=0 for outermost boundary cell (graveyard)

---

## 2. VOL (Volume)

**Purpose:** Specify cell volume for normalization and flux calculations

**Syntax:** `VOL=value`

**Units:** cm³

**Values:**
- Positive: Volume in cm³
- `NO`: MCNP will NOT calculate volume (use for complex geometry)
- Omitted: MCNP attempts automatic calculation (may be slow or fail)

**Examples:**
```
1  1  -10.5  -1  IMP:N=1  VOL=523.6    $ Explicit volume
2  2  -8.0   -2   IMP:N=1  VOL=NO      $ Suppress volume calculation
```

**When to specify:**
- Always for F4 (cell flux) tallies - required for correct normalization
- Complex cells where automatic calculation is slow
- Cells with # (complement) operator - automatic calc may fail
- Lattice cells - automatic calc very slow

**How to calculate:**
- Simple geometries: Analytical formula
- Complex geometries: CAD tools, Monte Carlo volume estimation
- MCNP can calculate with `PRINT 40` output (slow)

---

## 3. PWT (Photon Weight)

**Purpose:** Adjust photon weight at photon production (biasing)

**Syntax:** `PWT=value`

**Values:** Positive real number (default: 1.0)

**Use:** Photon variance reduction (rarely used - weight windows preferred)

---

## 4. EXT (Exponential Transform)

**Purpose:** Variance reduction for deep penetration problems

**Syntax:** `EXT:particle=value  stretch`

**Parameters:**
- `value`: Cell importance (similar to IMP but continuous)
- `stretch`: Stretching parameter (optional)

**Use:** Advanced variance reduction (less common than IMP and weight windows)

---

## 5. FCL (Forced Collision)

**Purpose:** Force collision in thin or low-density cells (variance reduction)

**Syntax:** `FCL:particle=value`

**Values:**
- `0`: No forced collision (default)
- Positive: Probability of forcing collision

**Use:** Thin shields, detectors with low interaction probability

**Example:**
```
1  1  -0.001  -1  IMP:N=1  FCL:N=0.9  $ Force 90% collision probability in thin gas
```

---

## 6. WWN (Weight Window Bounds)

**Purpose:** Variance reduction using weight windows

**Syntax:** `WWN:particle=lower  upper`

**Parameters:**
- `lower`: Lower weight bound
- `upper`: Upper weight bound

**Use:** Advanced variance reduction (typically use WWG card to generate automatically)

---

## 7. DXC (DXTRAN Contribution)

**Purpose:** Control DXTRAN sphere contribution from cell

**Syntax:** `DXC:particle=value`

**Use:** Advanced variance reduction with DXTRAN spheres

---

## 8. NONU (No Fission Neutrons)

**Purpose:** Suppress fission neutron production (treat fission as capture)

**Syntax:** `NONU=value`

**Values:**
- `0`: Normal fission (default)
- `1`: No fission neutrons produced
- `2`: Fission neutrons from only prompt fission

**Critical use case:** SSR (surface source read) with fissionable materials
- SSR does NOT work with fission neutrons
- Must use NONU=1 in all cells with fissionable material

**Example:**
```
c Problem using surface source from previous calculation
1  1  -10.5  -1  IMP:N=1  NONU=1  $ Fuel cell, suppress fission for SSR
```

---

## 9. PD (Detector Contribution)

**Purpose:** Include/exclude cell from point detector tallies

**Syntax:** `PD=value`

**Values:**
- `1`: Include in F5 point detector tallies (default)
- `-1`: Exclude from point detector tallies

**Use:** Exclude cells that interfere with detector line-of-sight

---

## 10. TMP (Temperature)

**Purpose:** Set cell temperature for Doppler broadening of cross sections

**Syntax:** `TMP=value`

**Units:** MeV (yes, energy units!)

**Conversion:** TMP (MeV) = k_B × T(K) = 8.617e-11 MeV/K × T(K)

**Common values:**
- 293.6 K (20°C): TMP=2.53e-8 MeV
- 600 K: TMP=5.17e-8 MeV
- 900 K: TMP=7.75e-8 MeV

**Example:**
```
1  1  -10.5  -1  IMP:N=1  TMP=5.17e-8  $ Fuel at 600 K
```

**Requirements:**
- Needs S(α,β) thermal scattering data (MT card) for low-energy neutrons
- Requires cross-section library with temperature data
- Use with OTFDB (on-the-fly Doppler broadening) or pre-generated libraries

**Default:** Room temperature (~293 K) if not specified

---

## 11. U (Universe)

**Purpose:** Assign cell to a universe (local coordinate system)

**Syntax:** `U=value`

**Values:** Integer (0-99,999,999)
- `U=0`: Base universe (default, main geometry)
- `U>0`: Local universe (can be filled into other cells)

**Use with FILL:** Cells with U>0 can be filled into other cells

**Example:**
```
c Define pin in universe 1
1  1  -10.5  -1  U=1  IMP:N=1    $ Fuel in universe 1
2  2  -6.5   1 -2  U=1  IMP:N=1  $ Clad in universe 1

c Fill lattice with universe 1
10  0  -10  LAT=1  FILL=1  IMP:N=1  $ Fill with U=1 pins

1  CZ  0.4                        $ Pin surfaces
2  CZ  0.5
10  RPP  -5 5  -5 5  0 100       $ Lattice boundary
```

**Best practices:**
- U=0 for main geometry (don't specify, it's default)
- U=1, 2, 3... for repeated structures (pins, assemblies)
- Higher U numbers for nested hierarchy (U=1 pin, U=2 assembly, U=3 core)

---

## 12. TRCL (Cell Transformation)

**Purpose:** Rotate or translate cell contents (not surfaces)

**Syntax - Two forms:**

**Form 1: Reference TR card**
```
TRCL=n
```
References *TRn card in data block

**Form 2: Inline matrix**
```
TRCL=(dx dy dz  a11 a12 a13  a21 a22 a23  a31 a32 a33  [m])
```
Specify transformation directly on cell card

**Example:**
```
*TR5  10 0 0  0 1 0  -1 0 0  0 0 1    $ 90° rotation + 10 cm translation

1  0  -1  U=1  FILL=2  TRCL=5  IMP:N=1    $ Fill U=2, apply TR5
2  0  -1  U=1  FILL=2  TRCL=(10 0 0  1 0 0  0 1 0  0 0 1)  $ Inline translation
```

**Use cases:**
- Rotate filled universe (hexagonal assembly in square lattice)
- Translate repeated components
- Create symmetric geometry with rotated copies

**See:** transformations_reference.md for TR card details

---

## 13. LAT (Lattice Type)

**Purpose:** Define cell as lattice for repeated structure array

**Syntax:** `LAT=value`

**Values:**
- `LAT=1`: Rectangular lattice (Cartesian grid)
- `LAT=2`: Hexagonal lattice

**Requirements:**
- Must have U parameter (defines universe to repeat)
- Must have FILL parameter (specifies which universes fill array)
- Cell geometry must be appropriate for lattice type

**Example:**
```
c Pin universe
1  1  -10.5  -1  U=1  IMP:N=1

c 3×3 lattice of pins
2  0  -2 -3 4 -5 6  LAT=1  U=2  FILL=1  IMP:N=1

1  CZ  0.5                      $ Pin radius
2  PX  -1.5                     $ Lattice boundaries (3×1cm pitch = 3cm)
3  PX   1.5
4  PY  -1.5
5  PY   1.5
6  PZ  100                      $ Height
```

**See:** lattice_geometry_reference.md for detailed LAT=1 and LAT=2 specifications

---

## 14. FILL (Fill with Universe)

**Purpose:** Fill cell with another universe or array of universes

**Syntax - Three forms:**

**Form 1: Single universe**
```
FILL=n
```
Fill entire cell with universe n

**Form 2: Indexed array (with LAT)**
```
FILL  imin:imax  jmin:jmax  kmin:kmax  universe_list
```
Array specification for LAT=1 lattice

**Form 3: Transform and fill**
```
FILL=n  TRCL=m
```
Fill with universe n, apply transformation m

**Examples:**

**Single fill:**
```
1  0  -1  FILL=10  IMP:N=1     $ Fill with universe 10
```

**Array fill (3×3):**
```
2  0  -2  LAT=1  FILL=-1:1 -1:1 0:0
                        1 1 2
                        1 1 1
                        2 1 1  IMP:N=1
c Fill pattern: 9 positions, U=1 or U=2
```

**Rotated fill:**
```
3  0  -3  FILL=5  TRCL=10  IMP:N=1  $ Fill with U=5, rotate by TR10
```

**Requirements:**
- Filled universe must be fully defined in its local coordinates
- For LAT cells, FILL must specify array
- Cannot fill with U=0 (base universe)

---

## 15. ELPT (Exponential Power Transform)

**Purpose:** Variance reduction (similar to EXT, rarely used)

**Syntax:** `ELPT:particle=value`

**Use:** Specialized variance reduction (weight windows preferred)

---

## 16. COSY (Coordinate System Transformation)

**Purpose:** Transform to different coordinate system

**Syntax:** `COSY=value`

**Values:**
- `1`: Rectangular (default)
- `2`: Cylindrical (r, θ, z)
- `3`: Spherical (r, θ, φ)

**Use:** Rare - primarily for special applications with coordinate-dependent sources or tallies

---

## 17. BFLCL (Boundary Flux Calculation)

**Purpose:** Calculate flux at cell boundaries

**Syntax:** `BFLCL=value`

**Use:** Specialized tallies at interfaces

---

## 18. UNC (Uncollided Flux Estimator)

**Purpose:** Improve tally statistics by separating uncollided flux

**Syntax:** `UNC:particle=value`

**Values:**
- `0`: Do not use uncollided estimator (default)
- `1`: Use uncollided flux estimator

**Use:** F4 tallies in optically thin regions (improves statistics)

---

## Parameter Combinations

### Common Combination 1: Basic cell
```
1  1  -10.5  -1  IMP:N=1  VOL=100.0  $ Minimal but complete
```

### Common Combination 2: Universe + Fill
```
10  0  -10  U=1  FILL=2  IMP:N=1  $ Fill universe 1 with universe 2
```

### Common Combination 3: Lattice
```
20  0  -20  LAT=1  U=3  FILL=1  IMP:N=1  VOL=NO  $ Rectangular lattice, suppress volume calc
```

### Common Combination 4: Transformed fill
```
30  0  -30  U=4  FILL=5  TRCL=10  IMP:N=1  $ Fill U=5 into U=4, rotate
```

### Common Combination 5: Temperature + NONU
```
40  1  -10.5  -40  IMP:N=1  TMP=7.75e-8  NONU=1  VOL=500  $ Hot fuel, SSR compatible
```

### Common Combination 6: Multiple importance
```
50  1  -10.5  -50  IMP:N=1  IMP:P=2  IMP:E=0  VOL=100  $ Different VR for each particle
```

---

## Parameter Restrictions

**Cannot be in both locations:**
- Same parameter on cell card AND in data block = ERROR

**LAT requires:**
- U parameter (universe assignment)
- FILL parameter (what fills lattice)
- Appropriate geometry (rectangular or hexagonal)

**FILL requires:**
- Target universe must exist (U>0 cells defined)
- For LAT cells: array specification required

**TRCL requires:**
- Either *TRn card defined OR inline matrix valid
- Used with FILL (transforms filled universe)

**NONU critical for:**
- SSR (surface source read) with fissionable materials
- MUST suppress fission in all fissionable cells

**TMP requires:**
- S(α,β) data (MT card) for thermal neutrons
- Cross-section library with temperature dependence
- OTFDB data card or multi-temperature libraries

---

## Data Block Format (Alternative to Cell Card)

**Format:** `PARAMETER:particle  value1  value2  value3  ...`

**Example:**
```
c Cell cards without parameters
1  1  -10.5  -1
2  2  -8.0    1 -2
3  3  -1.0    2 -3
4  0          3

c Data block with parameters
IMP:N  1  2  4  0           $ Importance for cells 1-4
VOL    100.0  200.0  300.0  1e10   $ Volumes for cells 1-4
```

**When to use data block:**
- Many cells with same parameter pattern
- Table format easier to read
- Parametric studies (single line to modify)

**When to use cell card:**
- Few cells with unique parameters
- Parameter specific to cell (clearer connection)
- Most common practice (recommended)

---

## Best Practices

1. **Always specify IMP** - Don't rely on default (IMP=1)
2. **Use VOL for F4 tallies** - Required for correct normalization
3. **Cell card placement preferred** - Clearer parameter-to-cell connection
4. **LAT requires U and FILL** - Always specify both
5. **NONU=1 for SSR** - Critical for surface source with fissionable materials
6. **TMP in MeV** - Convert from Kelvin: TMP = 8.617e-11 × T(K)
7. **TRCL with FILL** - Transforms filled universe, not cell geometry
8. **VOL=NO for complex cells** - Avoid slow automatic calculation
9. **Document unusual parameters** - Inline comments for EXT, PWT, FCL
10. **Check particle designators** - :N, :P, :E required for MODE particles

---

## Quick Reference Table

| Parameter | Purpose | Common Values | Required For |
|-----------|---------|---------------|--------------|
| IMP | Variance reduction | 0 (kill), >0 (importance) | All cells |
| VOL | Volume | cm³ or NO | F4 tallies |
| U | Universe | 0 (default), >0 (local) | FILL, LAT |
| TRCL | Transformation | n (ref) or inline | Rotated fills |
| LAT | Lattice type | 1 (rect), 2 (hex) | Repeated arrays |
| FILL | Fill universe | n or array | LAT cells |
| TMP | Temperature | MeV (8.617e-11×K) | Temperature effects |
| NONU | Suppress fission | 0 (normal), 1 (suppress) | SSR with fission |
| IMP=0 | Kill particle | 0 | Graveyard |

---

**References:**
- MCNP6 User Manual, Chapter 5.02: Cell Cards - Cell Parameters
- See also: cell_definition_comprehensive.md for cell card format
- See also: lattice_geometry_reference.md for LAT and FILL details
- See also: transformations_reference.md for TRCL and TR cards

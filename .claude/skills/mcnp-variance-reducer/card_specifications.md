# Variance Reduction Card Specifications

## Overview

This reference provides detailed syntax and parameter specifications for all MCNP variance reduction cards.

---

## IMP - Cell Importance

### Syntax

```
IMP:p  i₁  i₂  i₃  ...  iₙ
```

**Where:**
- `p` = Particle type (N, P, E, |, etc.)
- `iₙ` = Importance for cell n

### Parameters

**Importance Values:**
- `0` = Particle killed immediately (graveyard)
- `>0` = Relative importance (any positive value)
- Default = 1 (if not specified)

**Common Values:**
- `1` = Baseline importance
- `2, 4, 8, 16, ...` = Geometric progression (recommended)
- `0.5, 0.25, ...` = Decreasing importance (rare)

### Rules

1. **All cells must have importance** for each transported particle type
2. **Graveyard cell must have IMP=0**
3. **Importance ratio ≤4× recommended** between adjacent cells
4. **Multiple particle types** need separate IMP cards:
   ```
   IMP:N  1  2  4  8  0      $ Neutron importance
   IMP:P  1  1  2  4  0      $ Photon importance
   ```

### Examples

**Basic concentric shells:**
```
IMP:N  1  2  4  8  16  0
c      ^source ^detector ^graveyard
```

**Decreasing importance (unusual):**
```
IMP:N  8  4  2  1  0
c      ^high importance near source
```

---

## WWN - Weight Window Lower Bounds

### Syntax

**Cell-based:**
```
WWNn:p  wwn₁  wwn₂  wwn₃  ...
```

**Energy-dependent (with WWE):**
```
WWNn:p  wwn₁,₁  wwn₁,₂  ...  &
        wwn₂,₁  wwn₂,₂  ...  &
        ...
```

**Mesh-based (with MESH card):**
```
WWNn:p  J
```
(Values from wwout file)

**Where:**
- `n` = Time group index (optional, default 0)
- `p` = Particle type
- `wwnᵢ,ⱼ` = Lower bound for cell i, energy group j

### Parameters

**Weight Window Values:**
- Must be positive
- Typically 0.1 to 10.0
- Relative values matter more than absolute

**Entry Rules:**
- **Without WWE:** One value per cell
- **With WWE:** Rows = cells, columns = energy groups
- **Use J:** Read from wwout file (most common)

### Examples

**Simple cell-based:**
```
WWN:N  1.0  0.8  0.6  0.4  0.2
c      ^cell1 ... cell5
```

**Energy-dependent:**
```
WWE:N  0  1e-6  0.01  1  20   $ 4 energy groups
WWN:N  1.0  0.9  0.8  0.7  &   $ Cell 1, all energies
       0.8  0.7  0.6  0.5  &   $ Cell 2, all energies
       0.6  0.5  0.4  0.3      $ Cell 3, all energies
```

**From wwout file (most common):**
```
WWN:N  J
```

---

## WWE - Weight Window Energy Bounds

### Syntax

```
WWEn:p  e₀  e₁  e₂  ...  eₘ
```

**Where:**
- `n` = Time group index (optional)
- `p` = Particle type
- `eᵢ` = Energy bounds (MeV)

### Parameters

**Energy Values:**
- Must be monotonically increasing
- Units: MeV
- Include e₀ (lower bound) and eₘ (upper bound)
- Creates m energy groups: [e₀,e₁], [e₁,e₂], ..., [eₘ₋₁,eₘ]

**Typical Energy Structures:**

**Thermal neutrons:**
```
WWE:N  0  1e-10  1e-8  1e-6  1e-4  0.01  0.1  1  10  20
c      ^thermal ^epithermal ^fast ^high energy
```

**Fast neutrons:**
```
WWE:N  0  0.1  1  5  10  14  20
c      ^slow    ^fast range
```

**Photons:**
```
WWE:P  0  0.01  0.1  0.5  1  2  5  10  20
c      ^low     ^medium  ^high energy
```

### Rules

1. **Must match problem physics** (thermal vs. fast, etc.)
2. **More groups = better resolution** but more memory
3. **Typical:** 5-20 energy groups
4. **First value must be 0** (or minimum energy of interest)

---

## WWP - Weight Window Parameters

### Syntax

```
WWPn:p  wupn  wsurvn  mxspln  switchn  mwhere
```

**Where:**
- `n` = Time group (optional)
- `p` = Particle type

### Parameters

**wupn (Upper Bound Multiplier):**
- `w_upper = w_lower × wupn`
- Default: 5
- Range: 2-20 typical
- Larger = wider window, less aggressive VR

**wsurvn (Survival Weight Multiplier):**
- `w_survive = w_lower × wsurvn`
- Default: 3
- Range: 1 < wsurvn < wupn
- Target weight for particles

**mxspln (Maximum Splits):**
- Limits number of splits per event
- Default: 5
- Range: 2-10 typical
- Prevents memory overflow

**switchn (Weight Window Type):**
- `-1`: Read from wwout file (most common)
- `0`: Use WWN card values
- `+n`: Read from wwinp file

**mwhere (Application Location):**
- `0`: Surface crossing only (default)
- `1`: Collision + surface
- `2`: Everywhere

### Common Configurations

**Default (read from wwout):**
```
WWP:N  5  3  5  0  -1
c      ^default values  ^read wwout
```

**Less aggressive (wider window):**
```
WWP:N  10  5  5  0  -1
c      ^wider window
```

**More aggressive (narrow window):**
```
WWP:N  3  2  5  0  -1
c      ^narrower window
```

**Apply everywhere:**
```
WWP:N  5  3  5  0  -1  2
c                      ^everywhere
```

---

## WWG - Weight Window Generator

### Syntax

```
WWG  n  m  c
```

**Where:**
- `n` = Tally number (F5, F4, FMESH, etc.)
- `m` = Mesh number (0 = MESH card, 1+ = FMESH mesh_id)
- `c` = Target weight (optional, default 1.0)

### Parameters

**Tally Number (n):**
- Must be existing tally (F4, F5, FMESH, etc.)
- Tally defines response of interest
- Point detector (F5) most common

**Mesh Number (m):**
- `0`: Use MESH card for spatial mesh
- `1+`: Use FMESH mesh_id
- Mesh defines spatial binning

**Target Weight (c):**
- Controls overall weight scale
- Default: 1.0
- Smaller → more particles (lower weights)
- Larger → fewer particles (higher weights)

### Examples

**Point detector with MESH card:**
```
F5:N  100 0 0  0.5              $ Detector at (100,0,0)
MESH  GEOM=XYZ  ORIGIN=0 0 0
      IMESH=100  IINTS=10
      JMESH=100  JINTS=10
      KMESH=100  KINTS=10
WWG   5  0  1.0                 $ Tally 5, MESH 0
```

**Cell tally with target adjustment:**
```
F4:N  (1 2 3 4 5)               $ Cells 1-5
WWG   4  0  10.0                $ Higher target weight
```

**FMESH-based:**
```
FMESH4:N  GEOM=XYZ  ORIGIN=0 0 0  ...
WWG   4  1  1.0                 $ Tally 4, mesh_id=1
```

### Usage Workflow

1. **Stage 1 (WWG generation):**
   - Include WWG card
   - Run with moderate statistics (1e5-1e6)
   - Produces wwout file

2. **Stage 2 (production):**
   - Remove WWG card
   - Add WWP with switchn=-1
   - Run with full statistics
   - Uses wwout from Stage 1

3. **Iteration (optional):**
   - Keep WWP switchn=-1
   - Add WWG again
   - Regenerates improved wwout

---

## WWT - Weight Window Time Bounds

### Syntax

```
WWTn:p  t₀  t₁  t₂  ...  tₘ
```

**Where:**
- `n` = Optional index
- `p` = Particle type
- `tᵢ` = Time bounds (shakes, 1 shake = 10⁻⁸ seconds)

### Parameters

**Time Values:**
- Units: shakes (10⁻⁸ s)
- Must be monotonically increasing
- Creates m time groups

**Example:**
```
WWT:N  0  1e2  1e3  1e4  1e5
c      ^0-100 ^100-1000 ^1000-10000 shakes
```

### Use Cases

- Time-dependent problems (pulses)
- Decay chain tracking
- Transient simulations

---

## DXTRAN - Deterministic Transport

### Syntax

```
DXTRAN  r  x  y  z  max  p  [a]
```

**Where:**
- `r` = Sphere radius (cm)
- `x y z` = Sphere center coordinates (cm)
- `max` = Maximum contributions per source particle
- `p` = Particle type (optional)
- `a` = Angular biasing parameter (optional)

### Parameters

**Radius (r):**
- Typical: 0.5-10 cm
- Should enclose detector
- Larger = more computational overhead

**Center (x y z):**
- **MUST match detector location**
- Common error: mismatch with F5 coordinates

**Max Contributions:**
- Prevents memory overflow
- Typical: 100-1000
- Higher = better statistics but more memory

**Particle Type (p):**
- Optional (default: all particle types)
- Use for specific particles (N, P, etc.)

### Example

```
c Point detector
F5:N  100 0 0  0.5              $ At (100,0,0)
c
c DXTRAN sphere at same location
DXTRAN  1.0  100 0 0  1000      $ R=1cm, max=1000
```

### Related Card: DXC

**Syntax:**
```
DXC  c₁  c₂  ...  cₙ  J  J  J  ...
```

**Where:**
- `cᵢ` = Cells that contribute to DXTRAN
- `J` = All cells contribute (default)

**Example:**
```
DXC  1  2  3  4  J  J  J        $ Only cells 1-4 contribute
```

---

## FCL - Forced Collisions

### Syntax

```
FCLn:p  c₁  c₂  ...  cₙ
```

**Where:**
- `n` = Optional index
- `p` = Particle type
- `cᵢ` = Cell numbers

### Parameters

**Cell Selection:**
- List cells where collisions forced
- Typically low-density materials
- Threshold: ρ < 0.01 g/cm³

### Example

```
c Air gap (low density)
10  5  -0.001  -10  IMP:N=1     $ ρ = 0.001 g/cm³
c
FCL:N  10                        $ Force collisions in cell 10
```

### When to Use

- ✅ Low-density regions (air, vacuum gaps)
- ✅ Particles stream through without interaction
- ❌ High-density materials (wastes time)

---

## EXT - Exponential Transform

### Syntax

```
EXTn:p  s₁  s₂  ...  sₘ  p_param
```

**Where:**
- `n` = Optional index
- `p` = Particle type
- `sᵢ` = Surface numbers (concentric spheres)
- `p_param` = Stretching parameter (0-1)

### Parameters

**Surface List:**
- Must be concentric spheres
- Centered on source
- Detector at largest radius

**Stretching Parameter (p_param):**
- `0` = No transform (analog)
- `0.5` = Moderate biasing
- `0.9` = Strong biasing
- `1.0` = Maximum (can cause instabilities)

### Example

```
c Concentric spheres (source at origin)
1  SO  10
2  SO  30
3  SO  50
4  SO  70
5  SO  100                      $ Detector region
c
EXT:N  0  1  2  3  4  5  0.9    $ Strong biasing outward
```

### Limitations

- Requires spherical or near-spherical geometry
- Not suitable for backscatter problems
- Combine with weight windows for best results

---

## Source Biasing Cards

### SB - Source Bias

**Syntax:**
```
SBn  b₁  b₂  ...  bₘ
```

**Where:**
- `n` = Distribution number (matches SI/SP)
- `bᵢ` = Bias correction factor

**Purpose:** Corrects for biased source sampling

### SI/SP - Source Information/Probability

Used with SDEF for biased source distributions.

**Energy Biasing Example:**
```
SDEF  POS=0 0 0  ERG=FERG  D1
SI1   H  1e-8  1e-6  0.01  1  14      $ Energy bins
SP1   D  0.4   0.3   0.2   0.1        $ Biased probabilities
SB1      1.0   1.5   2.0   3.0        $ Correction factors
```

**Spatial Biasing Example:**
```
SDEF  POS=FPOS  D1  ERG=14.1
SI1   L  0 0 0  10 0 0  20 0 0        $ Three positions
SP1     0.5  0.3  0.2                  $ Biased toward detector
c       ^source  ^middle  ^near detector
```

---

## MESH - Importance Mesh (for WWG)

### Syntax

```
MESH  GEOM=geometry  REF=x y z  ORIGIN=x y z
      IMESH=values  IINTS=bins
      JMESH=values  JINTS=bins
      KMESH=values  KINTS=bins
```

**Where:**
- `geometry` = XYZ (Cartesian) or CYL (cylindrical) or SPH (spherical)
- `REF` = Reference point
- `ORIGIN` = Mesh origin
- `IMESH/JMESH/KMESH` = Mesh boundaries
- `IINTS/JINTS/KINTS` = Number of bins

### Example

**Cartesian mesh:**
```
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-50 -50 -50
      IMESH=50  IINTS=10              $ x: -50 to 50, 10 bins
      JMESH=50  JINTS=10              $ y: -50 to 50, 10 bins
      KMESH=50  KINTS=10              $ z: -50 to 50, 10 bins
```

**Cylindrical mesh:**
```
MESH  GEOM=CYL  AXS=0 0 1  VEC=1 0 0  ORIGIN=0 0 0
      IMESH=50  IINTS=10              $ r: 0 to 50
      JMESH=360 JINTS=36              $ θ: 0 to 360°
      KMESH=100 KINTS=10              $ z: 0 to 100
```

### Mesh Resolution Guidelines

- **Coarse:** 10×10×10 (1,000 cells) - fast but less accurate
- **Medium:** 20×20×20 (8,000 cells) - good balance
- **Fine:** 50×50×50 (125,000 cells) - slow but accurate

---

## Quick Reference Table

| Card | Purpose | Typical Usage |
|------|---------|---------------|
| IMP | Cell importance | Manual VR, simple geometries |
| WWN | Weight window lower bounds | Usually from wwout (J) |
| WWE | Energy-dependent WW | Energy-specific problems |
| WWP | Weight window parameters | Configure WW behavior |
| WWG | Generate weight windows | Automatic WW creation |
| WWT | Time-dependent WW | Time-dependent problems |
| DXTRAN | Deterministic to detector | Point detectors, far from source |
| DXC | DXTRAN cell contributors | Limit DXTRAN overhead |
| FCL | Force collisions | Low-density regions |
| EXT | Exponential transform | Deep penetration, spherical geometry |
| SB | Source bias correction | With biased SI/SP distributions |
| MESH | Importance mesh | Spatial binning for WWG |

---

## Parameter Tuning Guidelines

### Weight Window Parameters

**wupn (Upper Bound Multiplier):**
- Start: 5 (default)
- Increase (10-20): If too many splits/roulettes
- Decrease (2-3): If need more aggressive VR

**wsurvn (Survival Weight Multiplier):**
- Relationship: 1 < wsurvn < wupn
- Typical: wsurvn = wupn / 2
- Default: 3 (for wupn=5)

**mxspln (Maximum Splits):**
- Start: 5 (default)
- Increase (10): If splitting limited
- Decrease (2-3): If memory issues

### WWG Target Weight

**Effect:**
- Small (0.1): More particles, lower weights
- Medium (1.0): Balanced (default)
- Large (10): Fewer particles, higher weights

**When to Adjust:**
- Too many particles → Increase target
- Poor statistics → Decrease target

---

## References

**See Also:**
- `variance_reduction_theory.md` - Theoretical foundation
- `wwg_iteration_guide.md` - WWG workflow and examples
- `error_catalog.md` - Common card specification errors

**MCNP6 Manual:**
- Chapter 5.12: Variance Reduction Data Cards
- Chapter 3: Syntax and Format Rules

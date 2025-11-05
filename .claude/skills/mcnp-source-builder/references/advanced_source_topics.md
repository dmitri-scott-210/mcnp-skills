# Advanced Source Topics

This reference covers advanced MCNP source specification topics that extend beyond basic SDEF usage. These features enable complex source modeling for specialized applications.

---

## 1. Dependent Source Distributions (DS Card)

The DS card allows one source variable to depend on another, enabling correlated sampling.

### DS Options

**DS H (or blank) - Histogram/Continuous:**
```
SDEF CEL=D1 ERG=FCEL=D2
SI1  L  1 2 3              $ Cells
SP1    0.2 0.3 0.5
DS2  H  1.0 2.0 14.1       $ Energy depends on cell
```
Sampled cell determines which energy bin/value is used.

**DS T - Table Lookup:**
```
SDEF CEL=D1 POS=FCEL=D2
SI1  L  1 2 3 4 5          $ Five cells
DS2  T  1 0 0 0  2 5 0 0  3 0 5 0  $ Only cells 1,2,3 get specific positions
```
If cell doesn't match SI1 entry, POS gets default value.

**DS Q - Conditional Distribution:**
```
SDEF ERG=D1 DIR=FERG=D2
SI1  H  0.1 1.0 10.0       $ Energy bins
SP1    0 0.6 0.4
DS2  Q  1.0 10  10.0 20    $ If ERG≤1.0 use D10, if ERG≤10.0 use D20
SI10 -21 1                 $ Cosine for low energy
SI20 L 1                   $ Isotropic for high energy
```
Energy value determines which directional distribution is sampled.

**Key Points:**
- Dependent variable appears on SDEF with `FVAR=Dn` syntax
- Independent variable must be defined first on SDEF
- DS card number matches dependent distribution number
- No SP or SB card used with DS

---

## 2. Embedded Source Distributions

Embedded distributions enable micro-pulse structures and repeated time patterns.

### Syntax
```
SDEF TME=(D11 < D12 < D13)
```
or
```
SDEF TME=D41
SI41 S 51 (D11 < D12 < D13) 52
```

### Requirements
- Embedded distributions (D11, D12) **must start at zero**
- Inner distribution repeated to fill outer distribution exactly
- D11 fills D12, D12 fills D13
- Only works for continuous variables: ERG, TME, X, Y, Z, DIR, RAD, EXT

### Example: Accelerator Micro-Pulses
```
c ========================================================================
c Accelerator with 10 ns micro-pulses every 1 μs, running for 1 ms
c ========================================================================
SDEF POS=0 0 0 ERG=14.1 TME=(D1 < D2 < D3)
c
SI1  H  0 10e-9           $ 10 ns micro-pulse width
SP1    0 1
c
SI2  H  0 1e-6            $ 1 μs between micro-pulses
SP2    0 1
c
SI3  H  0 1e-3            $ 1 ms total beam duration
SP3    0 1
```

**Caution:** Cannot use SP -21 (power law) with embedded distributions.

---

## 3. Spontaneous Fission Sources

The `PAR=SF` option samples spontaneous fission neutrons from actinide materials.

### Available Nuclides (18 total)
Th-232, U-232/233/234/235/236/238, Np-237, Pu-238/239/240/241/242, Am-241, Cm-242/244, Bk-249, Cf-252

### Usage
```
c ========================================================================
c Cf-252 spontaneous fission source in cell 1
c ========================================================================
SDEF CEL=1 PAR=SF POS=0 0 0
```

### Behavior
- Code samples fissioning nuclide proportional to atom fraction × SF yield
- Multiplicity sampled from Santi data (or FREYA/CGMF if FMULT card present)
- Energy from Watt spectrum with nuclide-specific parameters
- If no SF nuclide in cell → Fatal error "spontaneous fission impossible"

### Normalization
**PAR=SF:**
- Summary table source tracks = ν·N (number of neutrons)
- Summary table source weight = W
- Tallies normalized by ν·N

**PAR=-SF:**
- Summary table source tracks = ν·N
- Summary table source weight = ν·W
- Tallies normalized by N (number of fissions)

---

## 4. Lattice and Repeated Structure Sources

Sources in lattices or repeated structures require special path notation.

### Source Path Format
```
CEL=(c_n < c_n-1 < ... < c_1 < c_0)
```
where c_i is cell at level i, or D_m for cell distribution, or 0 to search.

### Lattice Element Specification
```
CEL=(c < lat_cell[i j k] < parent)
```

**Four index formats:**
- Single index: `[5]` = 5th element in FILL array
- Three indices: `[2 1 0]` = element at (i=2, j=1, k=0)
- Range: `[0:2 0:1 0:0]` = all elements with i=0-2, j=0-1, k=0
- Universe: `[U=3]` = all lattice elements with universe 3

### Example: Source in Lattice Elements
```
c ========================================================================
c Source in 3x2 lattice, center 4 elements only
c ========================================================================
SDEF CEL=D1 POS=0 0 0 RAD=D2 AXS=0 0 1 EXT=D3
SI1  L  (10<7[0 0 0]<1) (10<7[1 0 0]<1) (10<7[0 1 0]<1) (10<7[1 1 0]<1)
SP1     0.25 0.25 0.25 0.25
```

**PDS Level:** Position/direction sampling coordinate system determined by first negative or zero cell in path (from right to left).

**Caution:**
- Ensure all lattice elements in source path actually exist
- Position rejection occurs at all levels where c_i=0
- Automatic lattice sampling can be inefficient for small source regions

---

## 5. Transformation (TR Keyword)

The TR keyword applies coordinate transformations to source positions and directions.

### Usage
```
SDEF POS=0 0 0 ERG=14.1 TR=5
TR5  10 0 0  1 0 0  0 1 0  0 0 1    $ Translate +10 cm in x
```

### Applications
- Move source to different location without changing geometry
- Rotate beam direction
- Create symmetric source arrays with SSR TR=Dn

### With SSR
```
SSR OLD=1 TR=D1
SI1  L  10 20 30           $ Three transformations
SP1     0.3 0.4 0.3        $ Relative probabilities
```
Surface source read from RSSA and placed at three transformed locations.

---

## 6. Cookie-Cutter Cell Rejection (CCC Keyword)

CCC limits source to specific cell, rejecting particles outside it.

### Usage
```
c ========================================================================
c Gaussian beam limited to cylindrical cell 50
c ========================================================================
SDEF POS=0 0 0 DIR=1 VEC=0 0 1 X=D1 Y=D2 Z=0 CCC=50
SP1  -41 2.0 0            $ Gaussian, FWHM=2 cm, centered at x=0
SP2  -41 2.0 0            $ Gaussian, FWHM=2 cm, centered at y=0
```

**Effect:** Particles sampled outside cell 50 are rejected and resampled until position is inside cell 50.

**Caution:** High rejection rate if source distribution poorly matches cell geometry. Monitor source efficiency in output.

---

## 7. Efficiency Control (EFF Keyword)

EFF sets maximum allowable source sampling efficiency before warning.

### Default Behavior
- MCNP tracks source particles rejected due to CEL, CCC, or geometry
- If rejection rate > (1 - EFF) → Warning message
- Default: EFF = 0.01 (99% rejection allowed before warning)

### Usage
```
SDEF CEL=D1 POS=0 0 0 RAD=10 EFF=0.10
SI1  L  1 2 3 4 5
SP1     0.02 0.02 0.02 0.02 0.92     $ 92% in cell 5, only 2% in each 1-4
```
If sampling uniformly from R=10 sphere but most probability in cell 5 → High rejection rate → Reduce EFF to catch this.

**Best Practice:** Lower EFF (e.g., 0.001) for lattice sources or highly selective cell distributions.

---

## 8. Unstructured Mesh Sources (POS=VOLUMER)

For unstructured mesh models (Abaqus or HDF5 format), VOLUMER enables volume source sampling.

### Basic Usage
```
SDEF POS=VOLUMER ERG=14.1     $ Sample uniformly over all volume sources in mesh
```

### Selective Sampling
```
SDEF CEL=D1 POS=FCEL=D2
SI1  L  101 103               $ Pseudo-cells with volume sources
SP1     0.4 0.6               $ 40% from cell 101, 60% from cell 103
DS2  L  VOLUMER VOLUMER
```

### Combined with Point Sources
```
SDEF CEL=D1 POS=FCEL=D2
SI1  L  101 102 103
SP1     0.4 0.2 0.4
DS2  S  4 5 6
SI4  L  VOLUMER               $ Cell 101: volume source
SI5  L  0.1 0.2 0.3           $ Cell 102: point source
SI6  L  VOLUMER               $ Cell 103: volume source
```

**Requirements:**
- Volume sources must be defined in mesh model
- Fatal error if VOLUMER used but no volume sources exist
- Sampling within element uniform, element selection proportional to volume

---

## 9. Area-Weighted Sources (ARA Keyword)

ARA enables area-weighted source sampling on surfaces.

### Usage
```
SDEF SUR=10 POS=D1 ARA=D2
SI1  L  0 0 0  10 0 0  0 10 0        $ Three points on surface
SP1     1 1 1                        $ Equal probability
SI2  L  100 50 75                    $ Areas associated with each point
```

**Effect:** Sampling probability proportional to area values, enabling non-uniform surface sources based on geometric considerations.

---

## 10. Weight Control (WGT Keyword)

WGT sets initial source particle weight (default = 1.0).

### Usage
```
SDEF POS=0 0 0 ERG=14.1 WGT=0.5      $ Each particle starts with weight 0.5
```

### Applications
- Normalize source when using SP W (intensity weighting)
- Match weight windows at source
- Combine multiple sources with different weights

**Caution:** For KCODE, do not change WGT from default (1.0).

---

## Integration with mcnp-variance-reducer

Many advanced source features work in conjunction with variance reduction:

- **TR + SSR:** Transform surface sources to create symmetric variance reduction
- **CCC + Importance:** Cookie-cutter with importance sampling for deep penetration
- **DS:** Correlate source with importance regions (high energy → forward direction)
- **EFF:** Monitor sampling efficiency when using weight windows

See `mcnp-variance-reducer` skill for complementary techniques.

---

## Summary of Advanced Keywords

| Keyword   | Purpose                          | Primary Use Case                |
|-----------|----------------------------------|---------------------------------|
| DS        | Dependent distributions          | Correlated source variables     |
| Embedded  | (D1 < D2 < D3)                   | Micro-pulses, repeated patterns |
| PAR=SF    | Spontaneous fission              | Cf-252, actinide sources        |
| Lattice   | (c1<c2[i j k]<c3)                | Sources in fuel arrays          |
| TR        | Transformation                   | Source positioning, SSR arrays  |
| CCC       | Cookie-cutter cell               | Limit source to specific region |
| EFF       | Efficiency threshold             | Monitor rejection rate          |
| VOLUMER   | Unstructured mesh volume         | CAD-based source definitions    |
| ARA       | Area weighting                   | Non-uniform surface sources     |
| WGT       | Initial weight                   | Source normalization            |

---

**For basic source specification, see main SKILL.md.**
**For distribution functions (SI/SP), see source_distribution_reference.md.**
**For troubleshooting, see source_error_catalog.md.**

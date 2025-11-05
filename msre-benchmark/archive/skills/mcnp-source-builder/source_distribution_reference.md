# Source Distribution Reference (SI/SP/SB Cards)

Complete reference for MCNP source distribution specifications using SI (Source Information), SP (Source Probability), and SB (Source Bias) cards.

---

## SI Card Options

The SI card defines the values or bins for a source variable distribution.

### SI H (Histogram) - DEFAULT
Monotonically increasing bin boundaries (integral/bin-wise).

```
SI1  H  0 1 5 10          $ Energy bins: [0-1], [1-5], [5-10] MeV
SP1     0 0.5 0.3 0.2     $ First entry MUST be 0, then bin probabilities
```

**Use when:** You have integrated probability over energy/position/direction bins.

### SI L (List)
Discrete values (e.g., specific energies, cell numbers).

```
SI1  L  1 2 3 4 5         $ Cell numbers
SP1     0.2 0.2 0.2 0.2 0.2
c
SI2  L  0.662 1.173 1.332 $ Discrete gamma energies (MeV) from Co-60
SP2     1 1 1             $ Equal probability
```

**Use when:** Source has discrete values (photon lines, specific cells, specific angles).

### SI A (Arbitrary)
Point-wise probability density function (differential/point-wise).

```
SI1  A  0 5 10 15 20      $ Energy points where PDF is defined
SP1     0 2.5 4.0 1.5 0   $ PDF values at those points (can start/end with 0)
```

**How it works:**
- Code integrates PDF using corrected trapezoidal (linear) scheme
- Linear interpolation between points
- First/last SP entry can be non-zero (unlike H option)

**Use when:** You have differential distribution d N/d E and want point-wise specification.

### SI S (Distribution of Distributions)
List of distribution numbers to sample from.

```
SDEF CEL=D1 ERG=FCEL=D2
SI1  L  1 2 3             $ Three cells
SP1     0.5 0.3 0.2
DS2  S  10 20 30          $ Cell 1→D10, Cell 2→D20, Cell 3→D30
SI10 L  14.1              $ 14 MeV for cell 1
SI20 H  0 1 10            $ Spectrum for cell 2
SP20    0 0.8 0.2
SI30 -3 0.965 2.29        $ Watt spectrum for cell 3
```

**Use when:** Different cells/conditions require different energy/directional distributions.

---

## SP Card Options

The SP card defines probabilities corresponding to SI card entries.

### SP D (Discrete) - DEFAULT for H/L
Bin or discrete value probabilities (need not be normalized).

```
SP1  D  0 0.3 0.5 0.2     $ For SI H: first=0, then bin probabilities
SP2  D  1 2 3 4 5         $ For SI L: discrete probabilities (code normalizes)
```

### SP C (Cumulative)
Cumulative probabilities (0 → 1).

```
SI1  L  1 2 3 4 5
SP1  C  0.2 0.4 0.6 0.8 1.0    $ Cumulative (must end at 1.0)
```

**Use when:** Input data is already cumulative.

### SP V (Volume-weighted)
For CEL distributions: probability proportional to cell volume (× SP values if present).

```
SDEF CEL=D1 POS=0 0 0 RAD=10
SI1  L  1 2 3 4 5
SP1  V  1 1 1 1 1         $ Equal volume weighting (or omit SP1 entirely)
```

**Use when:** Source emission rate proportional to cell volume (e.g., activation, fission in large cells).

**Caution:** MCNP must calculate or have VOL card for cell volumes, else fatal error.

### SP W (Intensity-weighted)
For PAR distributions: specify intensities for mixed particle sources.

```
SDEF PAR=D1 POS=0 0 0
SI1  L  N P E             $ Neutrons, photons, electrons
SP1  W  1e10 5e9 2e9      $ Intensities (particles/second)
```

**Effect:** Normalization factor applied to source weight → Tallies have correct magnitude.

**Use when:** Multiple particle types with different emission rates.

---

## Built-in Probability Functions

Special analytic functions specified as `SP n -f a b`.

### Energy Functions

| Function | Code | Parameters | Description |
|----------|------|------------|-------------|
| Maxwell fission | `-2` | `a` | E·exp(-E/a), a=temp (MeV) |
| Watt fission | `-3` | `a b` | exp(-E/a)·sinh(√(b·E)) |
| Gaussian fusion | `-4` | `a b` | Width a (MeV), mean E=b (MeV) |
| Evaporation | `-5` | `a` | E·exp(-E/a), a=1.2895 MeV default |
| Muir Gaussian | `-6` | `a b` | Velocity-space Gaussian |

**Default for -3 (Watt):** a=0.965 MeV, b=2.29 MeV⁻¹ (U-235)

**Example:**
```
SDEF ERG=D1 POS=0 0 0
SP1  -3 0.965 2.29        $ Watt spectrum for U-235 fission
```

**Gaussian -4 Special Values:**
- If `a<0`: Interpreted as temperature in MeV
- If `b=-1`: D-T fusion energy calculated automatically
- If `b=-2`: D-D fusion energy calculated automatically

**Example:**
```
SP1  -4 -0.01 -1          $ D-T fusion at 10 keV temperature
```

### Directional/Position Functions

| Function | Code | Parameters | Variables | Description |
|----------|------|------------|-----------|-------------|
| Power law | `-21` | `a` | DIR, RAD, EXT | p(x) = c·\|x\|^a |
| Exponential | `-31` | `a` | DIR, EXT | p(μ) = c·exp(a·μ) |
| Gaussian | `-41` | `a b` | TME, X, Y, Z | FWHM=a, mean=b |

**Default for -21:**
- DIR: a=1 (cosine, gives isotropic flux)
- RAD: a=2 (spherical volume), a=1 if AXS or SUR=0 (cylindrical/planar)
- EXT: a=0 (uniform)

**Example - Cosine directional:**
```
SDEF SUR=10 POS=0 0 0 DIR=D1
SP1  -21 1                $ Cosine (default for surface sources)
```

**Example - Exponential bias:**
```
SDEF SUR=999 AXS=0 0 1 EXT=D1 DIR=D2
SB1  -31 1.5              $ Bias toward +z direction
SP2  -21 1                $ Cosine emission (unbiased)
```

### Time Functions

| Function | Code | Parameters | Description |
|----------|------|------------|-------------|
| Exponential decay | `-7` | `a` | Activity α₀·exp(-0.693·t/a), a=half-life (shakes) |

**Example:**
```
SDEF POS=0 0 0 ERG=0.662 TME=D1
SP1  -7 1e8               $ Decay with t₁/₂ = 100 ns
```

---

## SB Card (Source Biasing)

The SB card provides a biased sampling distribution different from the true SP distribution. Particle weights adjusted automatically.

### Purpose
Improve simulation efficiency by sampling more particles in important regions while maintaining correct physics.

### Usage
```
SDEF ERG=D1 POS=0 0 0
SI1  H  0 0.1 1 10        $ True energy bins
SP1     0 0.05 0.15 0.80  $ True: most probability at high energy
SB1     0 0.40 0.40 0.20  $ Biased: oversample low energy
```

**Effect:** 40% of source particles sampled at 0.1-1 MeV (true: only 15%), but weights adjusted so tallies reflect true 15%.

### Allowed Functions
Only `-21` and `-31` can be used on SB cards.

```
SDEF SUR=10 DIR=D1
SP1  -21 1                $ True: cosine
SB1  -21 2                $ Biased: more peaked forward (μ²)
```

### Rules
- If built-in function on SB, same or compatible function required on SP
- Cannot mix table (SI/SP) with SB function
- Biasing affects bin probabilities, not function shape within bins

---

## Special Defaults

MCNP provides convenient defaults when cards are partially specified:

1. **If SB present but SP absent:**
   SP with default parameters automatically provided

2. **RAD or EXT with only SI:**
   - SP -21 with defaults automatically provided

3. **DIR or EXT with only SP -21 or -31:**
   - SI 0 1 (for -21) or SI -1 1 (for -31) automatically provided

4. **RAD with SI x and SP -21:**
   - Treated as SI 0 x

5. **EXT with SI x and SP -21/-31:**
   - Treated as SI -x x

---

## Complete Example: Multi-Distribution Source

```
c ========================================================================
c Fixed source with cell-dependent energy and direction
c ========================================================================
SDEF CEL=D1 ERG=FCEL=D2 DIR=FCEL=D3 POS=FCEL=D4
c
c Cell distribution (three fission cells)
SI1  L  10 20 30
SP1     0.5 0.3 0.2
c
c Energy depends on cell
DS2  S  11 12 13
SI11 -3 0.965 2.29                 $ Cell 10: U-235 Watt
SI12 -3 0.977 2.546                $ Cell 20: Pu-239 Watt
SI13 -4 -0.01 -1                   $ Cell 30: D-T fusion
c
c Direction depends on cell
DS3  S  21 21 22
SI21 -21 1                         $ Cells 10,20: Isotropic
SI22 L  1                          $ Cell 30: Monodirectional
c
c Position depends on cell
DS4  L  0 0 0  10 0 0  0 10 0      $ Positions for cells 10, 20, 30
```

---

## Verification Checklist

Before running, verify:
- [ ] SP first entry = 0 for SI H option
- [ ] SP probabilities sum to reasonable value (code normalizes, but check for typos)
- [ ] SI entries monotonically increasing for H and A options
- [ ] Distribution numbers referenced on SDEF actually have SI/SP cards
- [ ] Dependent distributions (FVAR) have DS card, not SP card
- [ ] Built-in function parameters physically reasonable (e.g., positive energies)
- [ ] SB biasing not too extreme (check source particle weights in output)

---

**For advanced features (DS, embedded, lattices), see advanced_source_topics.md.**
**For basic source setup, see main SKILL.md.**
**For troubleshooting, see source_error_catalog.md.**

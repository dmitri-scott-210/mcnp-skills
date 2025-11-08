# TRISO Fuel Reference (Supplemental)
## Material Specifications for TRISO Particle Fuel

**Purpose**: Supplemental reference for TRISO-specific patterns
**Note**: This supplements fuel_compositions_reference.md - refer there for general fuel types

---

## TRISO PARTICLE STRUCTURE

5-layer coated particle design:

```
Layer 1: Kernel (UCO or UO2, fissile)
Layer 2: Buffer (porous carbon, accommodate fission gases)
Layer 3: IPyC (inner pyrolytic carbon, diffusion barrier)
Layer 4: SiC (silicon carbide, structural, fission product retention)
Layer 5: OPyC (outer pyrolytic carbon, protect SiC)
```

**Complete 5-layer example**: See fuel_compositions_reference.md Section 2.1

---

## COMMON TRISO SPECIFICATIONS

### AGR-1 Experiment (INL)

**UCO kernel**: 19.75% enriched, 10.924 g/cm³
**Coating densities**: Buffer 1.10, IPyC 1.912, SiC 3.207, OPyC 1.901 g/cm³

**Complete material cards**:
```mcnp
c ========================================================================
c AGR-1 TRISO Particle - Complete 5-layer structure
c ========================================================================

c Layer 1: UCO Kernel (UC0.32O1.36, 19.75% enriched)
c Density: 10.924 g/cm3
M1    92234.00c  3.34179E-03  $ U-234
      92235.00c  1.99636E-01  $ U-235 (19.75% enriched)
      92236.00c  1.93132E-04  $ U-236
      92238.00c  7.96829E-01  $ U-238
       6012.00c  0.3217217    $ C-12
       6013.00c  0.0035783    $ C-13
       8016.00c  1.3613       $ O-16 (>1.0 valid!)
TMP1  7.75e-8                 $ 900 K

c Layer 2: Buffer (Porous carbon)
c Density: 1.10 g/cm3
M2     6012.00c  0.9890       $ C-12
       6013.00c  0.0110       $ C-13
MT2   C-GRPH.43t              $ REQUIRED! (600K graphite S(alpha,beta))
TMP2  5.17e-8                 $ 600 K

c Layer 3: IPyC (Inner Pyrolytic Carbon)
c Density: 1.912 g/cm3
M3     6012.00c  0.9890
       6013.00c  0.0110
MT3   C-GRPH.43t              $ REQUIRED!
TMP3  5.17e-8

c Layer 4: SiC (Silicon Carbide)
c Density: 3.207 g/cm3
M4    14028.00c  0.9223       $ Si-28 (92.23%)
      14029.00c  0.0467       $ Si-29 (4.67%)
      14030.00c  0.0310       $ Si-30 (3.10%)
       6012.00c  0.9890       $ C-12
       6013.00c  0.0110       $ C-13
MT4   C-GRPH.43t              $ Recommended for carbon component
TMP4  5.17e-8

c Layer 5: OPyC (Outer Pyrolytic Carbon)
c Density: 1.901 g/cm3
M5     6012.00c  0.9890
       6013.00c  0.0110
MT5   C-GRPH.43t              $ REQUIRED!
TMP5  5.17e-8

c Layer 6: Graphite Matrix (if compact fuel)
c Density: 1.256 g/cm3
M6     6012.00c  0.9890
       6013.00c  0.0110
MT6   C-GRPH.43t              $ REQUIRED!
TMP6  5.17e-8
```

**CRITICAL**: All carbon layers MUST have MT cards for accurate thermal neutron physics!

### HTR-10 (China)

**UO₂ kernel**: 17% enriched, 10.4 g/cm³
**Coating densities**: Similar to AGR-1

```mcnp
c HTR-10 TRISO UO2 Kernel
c Density: 10.4 g/cm3
M10   92235.80c  0.17     $ U-235 (17% enriched)
      92238.80c  0.83     $ U-238
       8016.80c  2.0      $ O-16
TMP10  7.75e-8             $ 900 K

c Coating layers (2-5) same as AGR-1 structure
```

### PBMR (South Africa)

**UO₂ kernel**: 9.6% enriched, fuel element design

```mcnp
c PBMR TRISO UO2 Kernel
c Density: 10.8 g/cm3
M20   92235.80c  0.096    $ U-235 (9.6% enriched)
      92238.80c  0.904    $ U-238
       8016.80c  2.0      $ O-16
TMP20  8.62e-8             $ 1000 K
```

---

## TRISO PARTICLE DIMENSIONS

### AGR-1 Typical Specifications

| Layer | Inner Radius (μm) | Outer Radius (μm) | Thickness (μm) |
|-------|-------------------|-------------------|----------------|
| Kernel | 0 | 212.5 | 212.5 |
| Buffer | 212.5 | 312.5 | 100 |
| IPyC | 312.5 | 352.5 | 40 |
| SiC | 352.5 | 387.5 | 35 |
| OPyC | 387.5 | 427.5 | 40 |

**Total particle diameter**: ~855 μm (0.855 mm)

**Packing fraction** (in compact):
- Typical: 30-40% particle volume fraction
- Remaining: Graphite matrix

---

## CRITICAL: MT CARDS FOR ALL CARBON LAYERS

**REQUIRED for correct physics**:
```mcnp
MT2   C-GRPH.43t  $ Buffer carbon - MANDATORY!
MT3   C-GRPH.43t  $ IPyC - MANDATORY!
MT4   C-GRPH.43t  $ SiC (carbon component) - Recommended
MT5   C-GRPH.43t  $ OPyC - MANDATORY!
MT6   C-GRPH.43t  $ Matrix - MANDATORY!
```

**Why MANDATORY**:
- Thermal neutrons dominate in HTGR spectrum
- Missing MT cards cause 1000-5000 pcm reactivity error
- Flux distribution spatially incorrect
- Benchmark validation will FAIL

**Professional models have missed this - DO NOT SKIP!**

---

## GEOMETRY MODELING OPTIONS

### Option 1: Explicit Sphere Geometry

**Model each TRISO layer as concentric spheres**:
```mcnp
c Cell cards for TRISO particle
1  1  -10.924  -1           IMP:N=1  $ Kernel (UCO)
2  2  -1.10    -2 +1        IMP:N=1  $ Buffer
3  3  -1.912   -3 +2        IMP:N=1  $ IPyC
4  4  -3.207   -4 +3        IMP:N=1  $ SiC
5  5  -1.901   -5 +4        IMP:N=1  $ OPyC
6  6  -1.256   -6 +5        IMP:N=1  $ Matrix
7  0           +6           IMP:N=0  $ Outside (void)

c Surface cards
1  SO  0.02125               $ Kernel outer radius (212.5 μm = 0.02125 cm)
2  SO  0.03125               $ Buffer outer radius
3  SO  0.03525               $ IPyC outer radius
4  SO  0.03875               $ SiC outer radius
5  SO  0.04275               $ OPyC outer radius
6  SO  0.10000               $ Matrix outer boundary (example)
```

### Option 2: Homogenized Compact

**Volume-weighted smearing of all TRISO components**:
```mcnp
c Homogenized fuel compact (AGR-1 typical)
c 40% TRISO particles, 60% graphite matrix by volume
c Material densities scaled by volume fractions
M100  92235.00c  X.XXX      $ U-235 (from kernel, scaled by packing fraction)
      92238.00c  X.XXX      $ U-238
       6012.00c  X.XXX      $ C-12 (from all carbon layers + matrix)
       6013.00c  X.XXX      $ C-13
       8016.00c  X.XXX      $ O-16
      14028.00c  X.XXX      $ Si-28 (from SiC, scaled)
      14029.00c  X.XXX      $ Si-29
      14030.00c  X.XXX      $ Si-30
MT100 C-GRPH.43t            $ Graphite S(alpha,beta) for carbon component
TMP100 5.17e-8
```

**See mcnp-lattice-builder skill for detailed TRISO lattice modeling**

---

## BURNUP CONSIDERATIONS FOR TRISO

### Kernel Isotope Tracking

**During burnup, track**:
```mcnp
c Actinides
92234.00c  ...  $ U-234
92235.00c  ...  $ U-235 (depletes)
92236.00c  ...  $ U-236 (builds from U-235)
92238.00c  ...  $ U-238
93237.00c  ...  $ Np-237
94239.00c  ...  $ Pu-239 (builds from U-238)
94240.00c  ...  $ Pu-240
94241.00c  ...  $ Pu-241

c Key fission products
54135.00c  ...  $ Xe-135 (equilibrium poison)
62149.00c  ...  $ Sm-149 (residual poison)
55133.00c  ...  $ Cs-133 (stable, high yield)
```

**See burnup_tracking_guide.md for complete isotope list**

### SiC Layer Activation

**Track for dose calculations**:
```mcnp
14028.00c  ...  $ Si-28 (activation)
14029.00c  ...  $ Si-29
14030.00c  ...  $ Si-30
 6012.00c  ...  $ C-12 (activation)
 6013.00c  ...  $ C-13
```

---

## FISSION GAS RELEASE MODELING

### Buffer Volume Calculation

**Purpose**: Buffer accommodates fission gas pressure

**Gas generation** (per fission):
- Stable Xe: ~0.25 atoms/fission
- Stable Kr: ~0.05 atoms/fission

**Pressure in buffer** (at EOL):
```
P = nRT/V
where:
  n = moles of gas produced
  T = temperature (K)
  V = buffer volume (cm³)
```

**Buffer void fraction**: ~50% (porous carbon)

**See mcnp-burnup-builder skill for fission gas tracking setup**

---

## COMPARISON: UCO vs UO₂ Kernels

| Property | UCO (UC₀.₃₂O₁.₃₆) | UO₂ |
|----------|-------------------|-----|
| Density | 10.924 g/cm³ | 10.4-10.8 g/cm³ |
| Enrichment (typical) | 19.75% | 17% |
| Carbon content | Yes (carbide) | No |
| Oxygen content | Lower than UO₂ | Stoichiometric O/U=2 |
| CO production | Reduced | Higher |
| Kernel pressure | Lower | Higher |
| Fission gas release | Better containment | Standard |

**Why UCO?**
- Reduced CO production → lower particle pressure
- Better fission product retention
- Used in AGR program (DOE-NGNP)

**Why UO₂?**
- Simpler fabrication
- More operational experience (HTR-10, AVR)
- Lower cost

---

## SEE ALSO

**For complete fuel coverage**:
- fuel_compositions_reference.md - All reactor fuel types (UO₂, MOX, UCO, metallic, HALEU)

**For MT cards**:
- thermal_scattering_reference.md - Complete S(α,β) table listings, temperature selection

**For geometry**:
- mcnp-lattice-builder skill - TRISO particle lattice structures, repeated geometry

**For burnup**:
- burnup_tracking_guide.md - Which isotopes to track, why, how many
- mcnp-burnup-builder skill - Complete depletion calculation setup

**For validation**:
- scripts/thermal_scattering_checker.py - Verify MT cards present for all carbon layers

---

**Version:** 1.0
**Created:** 2025-11-08
**For:** mcnp-material-builder skill v2.0

# Benchmark Cross Sections

Reference guide for typical microscopic cross sections used in MCNP for validation, estimation, and understanding neutron interactions. All values are for thermal neutrons (E = 0.0253 eV) unless otherwise specified.

## Cross Section Fundamentals

### Barn Definition

**Unit of cross section:**
```
1 barn (b) = 10⁻²⁴ cm² = 10⁻²⁸ m²
```

**Physical interpretation:**
- Effective "target area" for nuclear reaction
- Probability that incident particle interacts with nucleus
- NOT actual geometric size of nucleus

**Relation to reaction rate:**
```
Reaction rate = Φ × Σ = Φ × N × σ

where:
  Φ = neutron flux (n/cm²/s)
  Σ = macroscopic cross section (cm⁻¹)
  N = atom density (atoms/cm³ or atoms/barn-cm)
  σ = microscopic cross section (barns)
```

### Cross Section Types

**Total cross section:**
```
σ_total = σ_scatter + σ_absorption

where:
  σ_scatter = elastic + inelastic scattering
  σ_absorption = capture + fission (for fissile nuclei)
```

**Absorption:**
```
σ_absorption = σ_capture + σ_fission
σ_capture = (n,γ) + (n,α) + (n,p) + other reactions
```

**Capture-to-fission ratio:**
```
α = σ_capture / σ_fission

Reproduction factor:
  η = ν σ_fission / (σ_fission + σ_capture)
  η = ν / (1 + α)
```

### Energy Dependence

**1/v behavior (thermal region):**
```
Many absorption cross sections follow:
  σ(E) ∝ 1/v ∝ 1/√E

Scaling from thermal (0.0253 eV):
  σ(E) = σ₀ × √(0.0253/E)

Example: ¹⁰B(n,α) at E = 1 eV
  σ₀ = 3837 b at 0.0253 eV
  σ(1 eV) = 3837 × √(0.0253/1) = 610 b
```

**Resonances:**
```
Breit-Wigner formula (single level):
  σ(E) = σ₀ × (Γ/2)² / [(E - E_R)² + (Γ/2)²]

where:
  E_R = resonance energy
  Γ = total width
  σ₀ = peak cross section
```

**Fast region (MeV):**
- Generally decrease with energy
- Fission cross sections relatively flat
- Important for fusion neutron (14.1 MeV) applications

## Hydrogen and Light Elements

### Hydrogen-1

**Scattering:**
```
σ_scatter = 20.491 barns (thermal)
σ_total ≈ σ_scatter (absorption negligible)
```

**Capture:**
```
¹H(n,γ)²H cross section:
σ_capture = 0.3326 barns (thermal)

Very small compared to scattering
```

**Properties:**
- Best moderator (large energy loss per collision)
- Bound scattering (in H₂O, hydrocarbons) differs from free atom
- Thermal scattering S(α,β) data essential for accurate modeling

**MCNP Applications:**
```
Water moderator:
M1  1001.80c  2  8016.80c  1    $ H₂O
MT1  lwtr.10t                   $ Light water S(α,β)

Polyethylene (CH₂)_n:
M2  1001.80c  2  6000.80c  1    $ CH₂
MT2  poly.10t                   $ Polyethylene S(α,β)
```

### Deuterium (²H)

**Scattering:**
```
σ_scatter = 7.64 barns (thermal)
```

**Capture:**
```
²H(n,γ)³H cross section:
σ_capture = 0.000519 barns (thermal)

Extremely small (factor of 640 less than ¹H)
```

**Properties:**
- Lower capture than H-1 (advantage for heavy water)
- Lower scattering (slightly worse moderator)
- Heavy water (D₂O) has very low neutron absorption

**MCNP Applications:**
```
Heavy water moderator:
M3  1002.80c  2  8016.80c  1    $ D₂O
MT3  hwtr.10t                   $ Heavy water S(α,β)
```

### Carbon-12

**Scattering:**
```
σ_scatter = 4.746 barns (thermal)
```

**Capture:**
```
σ_capture = 0.00353 barns (thermal)

Very small (good moderator)
```

**Properties:**
- Excellent moderator (low absorption)
- A = 12 → logarithmic energy decrement ξ = 0.158
- Graphite density: ρ = 1.6-2.25 g/cm³ (depending on grade)

**MCNP Applications:**
```
Graphite moderator:
M4  6000.80c  1                 $ Natural carbon
MT4  grph.10t                   $ Graphite S(α,β)

Atom density (ρ = 1.7 g/cm³):
  N = 1.7 × 6.022e23 / 12 = 8.53e22 atoms/cm³ = 0.0853 atoms/b-cm
```

### Beryllium-9

**Scattering:**
```
σ_scatter = 7.63 barns (thermal)
```

**Capture:**
```
σ_capture = 0.0076 barns (thermal)
```

**Properties:**
- Good reflector (low absorption, low mass)
- Beryllium density: ρ = 1.85 g/cm³
- Toxic (berylliosis hazard)

**Special reaction:**
```
⁹Be(α,n)¹²C: Used in AmBe neutron sources
  Q = 5.7 MeV
  Neutron energy: continuous spectrum, avg ~4.5 MeV
```

### Oxygen-16

**Scattering:**
```
σ_scatter = 3.888 barns (thermal)
```

**Capture:**
```
σ_capture = 0.00019 barns (thermal)

Negligible absorption
```

**Properties:**
- Major component of water (H₂O)
- Low scattering compared to H (but still significant)
- Contributes ~11% of scattering in light water

## Structural and Moderator Materials

### Zirconium (Natural)

**Composition:**
```
Zr-90: 51.45%
Zr-91: 11.22%
Zr-92: 17.15%
Zr-94: 17.38%
Zr-96: 2.80%
```

**Cross sections (natural Zr):**
```
σ_scatter ≈ 6.46 barns
σ_absorption ≈ 0.184 barns

Very low absorption (excellent for fuel cladding)
```

**MCNP Applications:**
```
Zircaloy-4 cladding:
M5  40000.80c  0.0423          $ Natural Zr
    26000.80c  0.00095         $ Fe (impurity)
    24000.80c  0.00050         $ Cr (impurity)
    50000.80c  0.00122         $ Sn (alloying element)
```

### Iron-56

**Scattering:**
```
σ_scatter = 11.62 barns (thermal)
```

**Absorption:**
```
σ_capture = 2.59 barns (thermal)
```

**Natural iron composition:**
```
Fe-54: 5.845%   (σ_abs = 2.25 b)
Fe-56: 91.754%  (σ_abs = 2.59 b)
Fe-57: 2.119%   (σ_abs = 2.48 b)
Fe-58: 0.282%   (σ_abs = 1.28 b)

Natural Fe: σ_abs ≈ 2.56 barns
```

### Stainless Steel (Type 304)

**Typical composition:**
```
Fe: 68-70%
Cr: 18-20%
Ni: 8-12%
Mn, Si, C: balance
```

**Effective cross sections:**
```
σ_scatter ≈ 11 barns (weighted average)
σ_absorption ≈ 3.1 barns
```

**MCNP Applications:**
```
Stainless steel 304:
M6  26000.80c  0.0600          $ Fe (68%)
    24000.80c  0.0162          $ Cr (18%)
    28000.80c  0.0072          $ Ni (10%)
    25055.80c  0.0012          $ Mn (2%)
```

### Aluminum-27

**Scattering:**
```
σ_scatter = 1.595 barns (thermal)
```

**Absorption:**
```
σ_capture = 0.231 barns (thermal)
```

**Properties:**
- Low absorption
- Light metal (ρ = 2.70 g/cm³)
- Used for structural components in research reactors

### Lead (Natural)

**Composition:**
```
Pb-204: 1.4%
Pb-206: 24.1%
Pb-207: 22.1%
Pb-208: 52.4%
```

**Cross sections (natural Pb):**
```
σ_scatter ≈ 11.22 barns
σ_absorption ≈ 0.171 barns

High scattering, very low absorption
```

**Properties:**
- Excellent gamma shield (high Z, ρ = 11.34 g/cm³)
- Good neutron reflector (large scattering)
- Minimal parasitic absorption

## Fissile and Fertile Materials

### Uranium-235

**Fission:**
```
σ_fission = 585.1 barns (thermal, ENDF/B-VIII.0)
```

**Capture:**
```
σ_capture = 95.7 barns (thermal)
σ_(n,γ) → ²³⁶U
```

**Total absorption:**
```
σ_absorption = σ_fission + σ_capture = 680.8 barns
```

**Derived parameters:**
```
α (capture/fission ratio) = 95.7 / 585.1 = 0.164
ν (neutrons per fission) = 2.43 (thermal)
η (neutrons per absorption) = ν/(1+α) = 2.43/1.164 = 2.087
```

**Resonance integral:**
```
I_fission = 275 barns
I_capture = 144 barns
I_absorption = 419 barns
```

**Energy-dependent fission cross section:**
```
Thermal (0.0253 eV):  585 b
1 eV:                  ~10 b (resonance minimum)
10 eV:                 ~200 b (resonance peak)
1 keV:                 ~3 b (average)
1 MeV:                 1.2 b (fast)
14 MeV:                2.0 b (D-T fusion)
```

### Uranium-238

**Fission:**
```
σ_fission = 0 barns (thermal, threshold ~1 MeV)
σ_fission = 0.3 barns (at 1 MeV)
σ_fission = 0.55 barns (at 14.1 MeV, D-T fusion)
```

**Capture:**
```
σ_capture = 2.68 barns (thermal)
σ_(n,γ) → ²³⁹U → ²³⁹Np → ²³⁹Pu (Pu breeding)
```

**Scattering:**
```
σ_scatter = 9.36 barns (thermal)
```

**Inelastic scattering threshold:**
```
(n,n') threshold: 45 keV (first excited state)

Important for fast reactors (degrades neutron energy)
```

**Resonance region:**
```
Large resonances at:
  6.67 eV: σ_tot ≈ 23,000 barns
  21 eV: σ_tot ≈ 35,000 barns
  37 eV: σ_tot ≈ 31,000 barns

Doppler broadening critical for safety (negative feedback)
```

### Plutonium-239

**Fission:**
```
σ_fission = 747.4 barns (thermal)
```

**Capture:**
```
σ_capture = 269.3 barns (thermal)
σ_(n,γ) → ²⁴⁰Pu
```

**Total absorption:**
```
σ_absorption = 1016.7 barns
```

**Derived parameters:**
```
α = 269.3 / 747.4 = 0.360
ν = 2.87 (thermal)
η = 2.87 / 1.36 = 2.11
```

**Resonance:**
```
Strong resonance at 0.296 eV:
  σ_tot ≈ 8,000 barns
```

**Fast fission:**
```
At 1 MeV: σ_f = 1.8 barns
At 14.1 MeV: σ_f = 2.5 barns
```

### Plutonium-240

**Fission:**
```
σ_fission = 0.06 barns (thermal, essentially zero)

Threshold fissile (requires fast neutrons)
At 1 MeV: σ_f = 1.4 barns
```

**Capture:**
```
σ_capture = 289.5 barns (thermal)
σ_(n,γ) → ²⁴¹Pu
```

**Properties:**
- Bred from Pu-239 capture
- Poison in thermal reactors (large capture, no thermal fission)
- Spontaneous fission source: 920 n/s/g (interferes with weapons design)

### Uranium-233

**Fission:**
```
σ_fission = 531.1 barns (thermal)
```

**Capture:**
```
σ_capture = 45.5 barns (thermal)
```

**Total absorption:**
```
σ_absorption = 576.6 barns
```

**Derived parameters:**
```
α = 45.5 / 531.1 = 0.086
ν = 2.492 (thermal)
η = 2.492 / 1.086 = 2.295 (highest η)
```

**Breeding:**
```
Bred from Th-232:
  ²³²Th(n,γ)²³³Th → ²³³Pa → ²³³U

Thorium fuel cycle
```

### Thorium-232

**Fission:**
```
σ_fission = 0 barns (thermal, threshold ~1.3 MeV)
```

**Capture:**
```
σ_capture = 7.37 barns (thermal)
σ_(n,γ) → ²³³Th → ²³³Pa → ²³³U (breeding)
```

**Scattering:**
```
σ_scatter = 13.0 barns (thermal)
```

**Properties:**
- Fertile material (breeds U-233)
- Lower capture than U-238 (better for breeding)
- Thorium cycle produces less transuranics

## Neutron Absorbers and Poisons

### Boron-10

**Absorption:**
```
¹⁰B(n,α)⁷Li cross section:
σ_(n,α) = 3837 barns (thermal)

Q = 2.79 MeV (exothermic)
Products:
  93.7%: α (1.78 MeV) + ⁷Li (1.01 MeV) + γ (0.48 MeV)
  6.3%: α (1.47 MeV) + ⁷Li (0.84 MeV)
```

**Natural boron:**
```
B-10: 19.9%  (σ_abs = 3837 b)
B-11: 80.1%  (σ_abs = 0.005 b)

Natural B: σ_abs ≈ 767 barns
```

**1/v behavior:**
```
σ(E) = 3837 × √(0.0253/E)

At 1 eV: σ = 610 barns
```

**MCNP Applications:**
```
Boron carbide (B₄C) control rod:
M7  5010.80c  0.2828          $ B-10 (enriched to 90%)
    5011.80c  0.0314          $ B-11
    6000.80c  0.0785          $ C

Boric acid (H₃BO₃) solution:
M8  1001.80c  3  5010.80c  0.199  5011.80c  0.801  8016.80c  3
```

### Cadmium (Natural)

**Absorption:**
```
Cd-113: 20,600 barns (thermal)

Natural Cd (abundance-weighted):
σ_absorption ≈ 2,520 barns
```

**Cadmium cutoff:**
```
Energy below which Cd is opaque to neutrons:
E_cutoff ≈ 0.5 eV

Used to define:
  - Thermal flux (E < 0.5 eV)
  - Epithermal flux (E > 0.5 eV)

Cadmium ratio = (count without Cd) / (count with Cd cover)
```

**MCNP Applications:**
```
Cadmium absorber:
M9  48000.80c  1                $ Natural Cd (many isotopes)

Cd cover (thin sheet):
  Thickness: 0.5-1 mm typically
```

### Xenon-135

**Absorption:**
```
σ_capture = 2,650,000 barns = 2.65 × 10⁶ barns (thermal)

Largest known thermal neutron cross section
```

**Properties:**
- Fission product poison
- Half-life: 9.14 hours (decays to Cs-135)
- Equilibrium concentration depends on flux
- Causes xenon transient after shutdown/startup

**Reactor poisoning:**
```
In equilibrium (reactor operating):
  Production rate = Destruction rate + Decay rate
  ΔρXe ≈ -2800 pcm (typical PWR at full power)

After shutdown:
  Xenon builds up (from I-135 decay)
  Peak Xe at ~11 hours
  ΔρXe ≈ -3000 to -3500 pcm (may prevent restart)
  "Xenon dead time": ~40 hours until reactivity recovers
```

### Samarium-149

**Absorption:**
```
σ_capture = 40,140 barns (thermal)
```

**Properties:**
- Fission product poison
- Stable (does not decay)
- Equilibrium concentration proportional to burnup
- "Permanent" poison (unlike Xe-135 which decays)

**Reactor poisoning:**
```
Equilibrium (after long operation):
  ΔρSm ≈ -700 pcm (typical PWR)

Does not change with shutdown (stable)
```

### Hafnium (Natural)

**Absorption:**
```
Hf-177: σ_abs = 373 barns
Natural Hf: σ_abs ≈ 104 barns
```

**Properties:**
- Used in control rods (especially naval reactors)
- Better mechanical properties than B or Cd
- Higher melting point than Cd

### Gadolinium-157

**Absorption:**
```
σ_capture = 254,000 barns (thermal)
```

**Natural gadolinium:**
```
Gd-155: 14.80%  (σ_abs = 60,900 b)
Gd-157: 15.65%  (σ_abs = 254,000 b)
Other isotopes: lower σ

Natural Gd: σ_abs ≈ 48,890 barns
```

**MCNP Applications:**
```
Gadolinium burnable poison:
M10  64152.80c  0.002  64154.80c  0.0218  64155.80c  0.148
     64156.80c  0.2047 64157.80c  0.1565  64158.80c  0.2484
     64160.80c  0.2186  $ Natural Gd distribution

Or enriched in Gd-157 for stronger absorption
```

## MCNP Validation Benchmarks

### k-infinity Validation (Infinite Lattice)

**Simple thermal system (H₂O + UO₂):**
```
Expected k∞:
  UO₂ (2% enrichment): k∞ ≈ 1.05-1.10
  UO₂ (3% enrichment): k∞ ≈ 1.15-1.20
  UO₂ (5% enrichment): k∞ ≈ 1.30-1.40

Depends on:
  - Fuel enrichment
  - Water-to-fuel ratio
  - Temperature
```

**Fast system (no moderator):**
```
Pu metal critical mass:
  Bare sphere: ~10 kg (subcritical)
  Reflected: ~5 kg (critical)
```

### Multiplication Factor Limits

**Thermal systems:**
```
k∞ (infinite): typically 1.2-1.4 for fresh fuel
k_eff (finite): must be < 1.00 for safety (typically < 0.95)

Reactivity shutdown margin: Δk/k = (k-1)/k ≈ 0.05-0.10
```

**Fast systems:**
```
k∞ (infinite): typically 1.3-1.5
Critical mass (bare): ~50 kg U-235, ~10 kg Pu-239
Critical mass (reflected): ~25 kg U-235, ~5 kg Pu-239
```

### Cross Section Sanity Checks

**Thermal absorption hierarchy:**
```
Xe-135  > Gd-157  > Cd-113  > Sm-149  > B-10  > U-235  > other
2.65M b   254K b    20.6K b   40.1K b   3837 b  585 b
```

**Material self-shielding:**
```
Thick uranium:
  Surface sees full flux
  Interior shadowed by outer layers
  Effective σ_abs < tabulated σ

Requires:
  - Resonance self-shielding factors
  - Equivalence theory
  - Or explicit geometry in MCNP (Monte Carlo handles automatically)
```

## References

### Cross Section Libraries for MCNP

**ENDF/B-VIII.0 (current U.S. standard):**
- Released 2018
- Improved accuracy for many nuclides
- Better uncertainty quantification

**ENDF/B-VII.1 (previous standard):**
- Released 2011
- Still widely used

**JEFF-3.3, JENDL-5.0:**
- European and Japanese evaluations
- Useful for comparison/validation

### Cross Section Databases

**NNDC (National Nuclear Data Center):**
- https://www.nndc.bnl.gov/
- Browse evaluated data
- Plot cross sections online

**JANIS (Java-based Nuclear Information Software):**
- https://www.oecd-nea.org/janis/
- Compare libraries
- Download tabulated data

**IAEA:**
- https://www-nds.iaea.org/
- International cross section standards

### Textbook References

**Reactor Physics:**
- Lamarsh & Baratta, "Introduction to Nuclear Engineering"
- Duderstadt & Hamilton, "Nuclear Reactor Analysis"
- Stacey, "Nuclear Reactor Physics"

**Cross Section Data:**
- Beckurts & Wirtz, "Neutron Physics"
- Glasstone & Sesonske, "Nuclear Reactor Engineering"

### Related MCNP Skills

- **mcnp-material-builder**: Uses cross section data for materials
- **mcnp-physics-validator**: Checks physics settings including XS libraries
- **mcnp-cross-section-manager**: Manages xsdir and library files
- **mcnp-isotope-lookup**: Provides ZAID and library availability

---

**End of Benchmark Cross Sections Reference**

# FM Card Special Reaction Numbers - Complete Reference

**Purpose:** Complete catalog of all special reaction numbers (R) available for FM tally multipliers in MCNP, extracted from Chapter 5.09 Table 5.19.

**Source:** MCNP6 Manual Chapter 5.09, section 5.9.7.2, Table 5.19 (lines 1293-1388)

---

## Overview

The FM card multiplies tallies by cross sections to calculate reaction rates, heating, criticality, and other derived quantities. The general form is:

```
Integral = ∫ φ(E) × R_m(E) dE
```

Where:
- **φ(E)** = Energy-dependent fluence (particles/cm²) from tally
- **R_m(E)** = Cross section or response function from material m
- **C** = Arbitrary normalization constant

**Key concepts:**
- **Material number (m):** Must appear on M card (but doesn't need to be in geometry)
- **Reaction number (R):** ENDF/B MT number or special R number from Table 5.19
- **Cross sections:** Microscopic (barns), not macroscopic
- **Normalization:** c = atom density (atoms/barn-cm) gives results per cm³

---

## Table 5.19: Special Reaction Numbers

### Neutron Reactions (Standard)

| R Value | Description | Units | Notes |
|---------|-------------|-------|-------|
| **-1** | Total cross section without thermal | barns | Excludes thermal scattering law contribution |
| **-2** | Absorption cross section | barns | Sum of all reactions removing neutrons from transport |
| **-3** | Elastic cross section without thermal | barns | Excludes S(α,β) thermal treatment |
| **-4** | Average neutron heating number | MeV/collision | Energy deposited per collision (KERMA factor) |
| **-5** | Gamma-ray production cross section | barns | Total photon production |
| **-6** | Total fission cross section | barns | Sum of all fission reactions (MT=18, 19, 20, 21, 38) |
| **-7** | Fission ν (prompt or total) | neutrons/fission | Neutron multiplicity (prompt ν_p or total ν_t depending on library) |
| **-8** | Fission Q | MeV/fission | Energy release per fission |
| **-9** | Fission ν, delayed | neutrons/fission | Delayed neutron multiplicity ν_d |

**Common neutron MT numbers (standard ENDF):**
- **1:** Total cross section (σ_t)
- **2:** Elastic scattering (σ_el)
- **16:** (n,2n) reaction
- **17:** (n,3n) reaction
- **18:** Total fission (most nuclides)
- **19, 20, 21, 38:** First, second, third, fourth-chance fission (some actinides like Pu-240)
- **102:** (n,γ) radiative capture
- **103:** (n,p) proton production
- **107:** (n,α) alpha production

---

### Photoatomic Reactions

| R Value | Description | Units | Notes |
|---------|-------------|-------|-------|
| **-1** | Incoherent scattering cross section | barns | Compton scattering |
| **-2** | Coherent scattering cross section | barns | Rayleigh scattering |
| **-3** | Photoelectric cross section, with fluorescence | barns | Includes fluorescence photons |
| **-4** | Pair production cross section | barns | e⁺e⁻ pair creation (E > 1.022 MeV) |
| **-5** | Total cross section | barns | Sum of all photon interactions |
| **-6** | Average photon heating number | MeV/collision | Energy deposited per collision |

**Use cases:**
- Photon flux to energy deposition: FM4 -1 m -5 -6 (flux × σ_total × heating)
- Compton scattering rate: FM2 -1 m -1 (flux × σ_incoherent)

---

### Proton Reactions (LA150H Library)

| R Value | Description | Units | Notes |
|---------|-------------|-------|-------|
| **±1** | Total cross section | barns | Sign determines treatment |
| **±2** | Non-elastic cross section | barns | All inelastic reactions |
| **±3** | Elastic cross section | barns | Elastic scattering |
| **±4** | Average proton heating number | MeV/collision | Energy deposition |

**Special notes:**
- Only available with LA150H proton library
- Beyond R = ±1, ±2, ±3, ±4, only MT=5 and multiplicities are available
- Multiplicity format: 1000 × (secondary particle number) + MT
  - **1005:** Neutron multiplicity from MT=5
  - **9005:** Proton multiplicity from MT=5
  - **31005:** Deuteron multiplicity from MT=5

**Extrapolation behavior:**
- Cross section at lowest energy extended down to E = 0 for MT < 0
- Cross section at highest energy extended to E = ∞ for MT < 0

---

### Photonuclear Reactions

| R Value | Description | Units | Notes |
|---------|-------------|-------|-------|
| **1** | Total cross section | barns | All photonuclear reactions |
| **2** | Non-elastic cross section | barns | All non-elastic reactions |
| **3** | Elastic cross section | barns | Elastic scattering |
| **4** | Average photonuclear heating number | MeV/collision | Energy deposition |

**Standard MT numbers:**
- **18:** (γ,f) photofission

**Particle yield format:** 1000 × (particle type) + MT
- **1001:** Total neutron yield (particle type n = 1, MT=1)
- **31001:** Total deuteron yield (particle type D = 31, MT=1)
- **34001:** Total alpha yield (particle type α = 34, MT=1)
- **1018:** Neutron yield from photofission (MT=18)

**Extrapolation behavior:**
- Cross section at highest energy extended to E = ∞ for MT < 1000

---

### Multigroup Neutron & Photon

| R Value | Description | Units | Notes |
|---------|-------------|-------|-------|
| **-1** | Total cross section | barns | σ_t |
| **-2** | Fission cross section | barns | σ_f |
| **-3** | Fission ν data | neutrons/fission | Neutron multiplicity |
| **-4** | Fission χ data | - | Fission spectrum |
| **5** | Absorption cross section | barns | σ_a |

**Use case:**
- Multigroup transport parameter generation for deterministic codes

---

### Electron Stopping Powers

| R Value | Description | Units | Notes |
|---------|-------------|-------|-------|
| **1** | de/dx electron collision stopping power | MeV/cm | Collision losses (ionization, excitation) |
| **2** | de/dx electron radiative stopping power | MeV/cm | Bremsstrahlung losses |
| **3** | de/dx total electron stopping power | MeV/cm | Sum of collision + radiative |
| **4** | Electron range | cm | CSDA (continuous slowing down approximation) range |
| **5** | Electron radiation yield | - | Fraction of energy lost to bremsstrahlung |
| **6** | Relativistic β² | - | (v/c)² |
| **7** | Stopping power density correction | - | Density effect correction factor |
| **8** | Ratio of radiative/collision stopping powers | - | (de/dx)_rad / (de/dx)_col |
| **9** | Drange | - | Detour factor (range / straight-line penetration) |
| **10** | dyield | - | Derivative of radiation yield |
| **11** | MG array values | - | Internal array |
| **12** | QAV array values | - | Internal array |
| **13** | EAR array values | - | Internal array |

**Use case:**
- Electron dose calculations: Use R=1 or R=3 for stopping power

---

## Special FM Card Features

### k = -3 Option: First Interaction Cross Section

**Syntax:**
```
FMn (k=-3 m R)
```

**Purpose:**
- Multiplies tally by microscopic cross section of the FIRST interaction only
- Used with LCA NOACT=-2 to convert multiplicities into secondary production cross sections

**Units:** barns

**Applications:**
- Secondary particle production cross sections
- Photon production yields from neutron reactions

**Restrictions:**
- Works for all incident particles EXCEPT electrons
- Use caution with charged particles (may use maximum cross sections instead of actual)

---

### Photon Production MT Numbers

**Format:** MT_base × 1000 + photon_index

**Example:**
- **MT 102:** (n,γ) radiative capture produces 40 distinct photons
- **MT numbers:** 102001, 102002, 102003, ..., 102040
- **Each has:** Individual energy-dependent cross section, angular distribution, energy distribution

**Use case:**
- Detailed gamma-ray spectroscopy calculations
- Photon flux by source reaction

---

### PERT Card Interaction with FM Multipliers

When using PERT (perturbation) card with FM multipliers:

**Requirements for correct perturbation:**
1. R reactions on FM card must match RXN reactions on PERT card
2. FM constant c must be NEGATIVE (indicating multiplication by atom density → macroscopic σ)

**Example (CORRECT):**
```
FM4 -1 10 -6    $ c=-1 (macro), material 10, fission
PERT ...  RXN=-6  $ Fission perturbation (same R)
```

**Example (WRONG):**
```
FM4 -1 10 -6    $ c=-1 (macro), material 10, fission (R=-6)
PERT ...  RXN=18  $ Fission with MT=18 ← MISMATCH!
```

**Why it matters:**
- If c > 0: Cross sections are microscopic, assumed no perturbation dependence R_ij' = 0
- If c < 0 and R matches RXN: Correction made for perturbed cross section

**Automatic correction for:**
- F6 tally (energy deposition)
- KCODE k_eff calculation
- F7 tally if perturbation reaction is fission

---

## Cross Section Verification

**Always plot cross sections first:**

```bash
# Plot cross sections to verify availability and reaction numbers
mcnp6 i=input.i xs    # Interactive cross section plotting
```

**Why plotting is critical:**
- Verify reaction numbers are correct for your library
- Check energy range coverage
- Identify extrapolation regions (low/high energy)
- Confirm expected cross section magnitude

**Extrapolation warnings:**
- Low energy: Check if extended to E=0 is appropriate
- High energy: Check if extended to E=∞ is appropriate
- Model interactions: May have different R numbers than library

---

## FM Card Syntax Rules

### Reaction List Operators

**Format:**
```
FMn c m r1 r2 : r3 # r4
```

**Operators:**
- **Space:** Multiply reactions (r1 × r2)
- **Colon (:):** Add reactions (r1 + r3)
- **Pound (#):** Subtract reactions (r1 - r4)

**Hierarchy:** Multiply first, then add/subtract (left to right)

**Parentheses:** NOT allowed within reaction list

### Examples

**Example 1: Product and sum**
```
FM4 1.0 10 -6 -7    $ One bin: fission × ν
```
Result: Fission neutron production

**Example 2: Sum then product**
```
FM4 1.0 10 16:17    $ One bin: (n,2n) + (n,3n)
```
Result: Total (n,xn) reaction rate

**Example 3: Multiple bins**
```
FM4 1.0 10 (-6) (-2) (-6 -7)
```
Result: Three bins (fission, capture, fission production)

---

## Practical Examples

### Example 1: Track-Length Criticality Estimate

```
F4:n 1 2            $ Flux in fuel cells
FM4 -1 3 -6 -7      $ c=-1 (atom density), m=3, σ_f × ν
SD4 1 1             $ Override volume divisors with 1
```

**Result:** Track-length estimate of k_eff
**Formula:** k_eff ≈ (volume × atom_density × flux × σ_f × ν) summed over fuel

### Example 2: Neutron Lifetime

```
F4:n 1              $ Flux in active region
FM4 (-1 1 -2)       $ Bin 1: ρN × σ_capture (removal rate)
    (1 -2)          $ Bin 2: flux/velocity (time integral)
```

**Result:**
- Divide Bin 2 by Bin 1 → (n,γ) lifetime
- R = 1 gives 1/velocity for time integral of population

### Example 3: Reaction Rates in Fuel

```
F4:n 10             $ Flux in fuel cell
FM4 (-1 3 -6)       $ Fission rate
    (-1 3 -2)       $ Capture rate
    (-1 3 16:17)    $ (n,xn) rate
    (-1 3 102)      $ (n,γ) rate
```

**Result:** Four bins with reaction rates (reactions/cm³)
**c = -1:** Multiplies by atom density of material 3

### Example 4: Total Energy Deposition (Two Methods)

**Method 1: FM with F4**
```
F4:p 1              $ Photon flux
FM4 -1 2 -5 -6      $ ρN × σ_total × heating
SD4 1               $ Volume divisor = 1 (multiply by volume)
```

**Method 2: Direct F6**
```
F6:p 1              $ Photon heating (MeV/g)
SD6 1               $ Mass divisor = 1 (multiply by mass)
```

**Result:** Both give total energy deposition in cell (MeV)

### Example 5: Photon Production from Neutrons

```
F4:n 10             $ Neutron flux
FM4 -1 5 -5         $ Material 5, photon production σ
```

**Result:** Photon production rate (photons/cm³) from neutron reactions

---

## Integration with Other Skills

**Related skills:**
- **mcnp-tally-builder:** General FM card usage and tally setup
- **mcnp-material-builder:** Material definitions required for FM
- **mcnp-physics-builder:** PHYS card interactions affecting cross sections
- **dose_and_special_tallies.md:** DE/DF vs FM for dose calculations

**Typical workflows:**

**Workflow 1: Reaction rate calculation**
1. Set up F4 flux tally in region of interest
2. Define material with desired nuclide (M card)
3. Create FM card with: c=-1 (atom density), m=material, R=reaction
4. Add SD card with value 1 to get total rate (not per-cm³)
5. Result: Total reaction rate in region

**Workflow 2: Energy deposition**
1. Set up F4 flux tally
2. Use FM with R=-4 (heating) and R=-1/-5 (total cross section)
3. Compare with F6 direct heating tally for validation

---

## Common Errors and Troubleshooting

### Error 1: "Reaction MT not found in library"

**Cause:** Requested reaction number doesn't exist for that nuclide/library

**Solutions:**
- Plot cross sections first to verify available reactions
- Check if using correct MT vs R number
- For fission: Try R=-6 instead of MT=18 (catches all fission types)

### Error 2: Inconsistent PERT and FM

**Cause:** R on FM doesn't match RXN on PERT, or c > 0

**Solution:**
- Use same reaction identifier: FM4 ... -6 and PERT RXN=-6
- Ensure FM constant c is negative

### Error 3: FM results don't match expected

**Cause:** Cross section extrapolation or wrong units

**Solutions:**
- Plot cross sections to check extrapolation regions
- Verify c = -1 for atom density (macroscopic results)
- Check SD card for proper normalization
- Remember: Cross sections are microscopic (barns), not macroscopic

### Error 4: "Too few parameters on FM card"

**Cause:** Missing required parameters c, m, or R

**Solution:**
```
FM4 1.0              ← WRONG (just constant)
FM4 1.0 10 -6        ← CORRECT (c, m, R all present)
```

---

## Best Practices

1. **Always plot cross sections first** to verify reaction numbers and energy range
2. **Use R = -6 for fission** instead of MT=18 to catch all fission reactions
3. **Use c = -1** with material's atom density for per-cm³ results
4. **Combine with SD card** to control normalization (volume, mass, custom)
5. **Verify units:** Microscopic σ (barns) × N (atoms/barn-cm) = macroscopic Σ (1/cm)
6. **Multiple bins:** Use parentheses and multiple reaction lists for separate bins
7. **Cross-check results:** Compare FM-based tallies with direct tallies (F6) when possible
8. **Document assumptions:** Use FC card to explain what each FM bin calculates

---

**For more information:**
- MCNP6 Manual: Chapter 5.09, sections 5.9.7.1-5.9.7.8
- ENDF/B documentation for standard MT numbers
- MCNP Theory Manual for cross section treatment

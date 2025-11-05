# Model Physics Comprehensive Reference

## Overview

Model physics in MCNP6 provide physics-based transport for particles at energies where cross-section data are unavailable or exceed library energy limits. This reference covers all model physics control cards and their parameters.

## When Model Physics Are Used

**Automatic Activation:**
- Any MODE particle other than n, p, or e automatically activates model physics
- Particles exceeding cross-section library maximum energy
- Isotopes missing cross-section libraries

**Manual Control:**
- MPHYS card enables/disables model physics
- Default: OFF for MODE n p e problems
- Default: ON for problems with other particles

---

## MPHYS: Model Physics Control

### Syntax
```
MPHYS toggle
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `on` | Enable model physics |
| `off` | Disable model physics (default for n, p, e) |

### Default Behavior
- MODE n p e problems: `MPHYS off`
- Any other particle on MODE card: `MPHYS on` (automatic)

### Use
- To disable model physics: `MPHYS off`
- To enable model physics: `MPHYS on` or include `MPHYS` with no entries

---

## LCA: Model Selection and Control

The LCA card selects the intranuclear cascade (INC) model and sets parameters for Bertini, ISABEL, CEM03.03, or INCL4.

### Syntax
```
LCA ielas ipreq iexisa ichoic jcoul nexite npidk noact icem ilaq nevtype
```

### Parameters

#### Entry 1: ielas - Elastic Scattering Control
- `0` = No nucleon elastic scattering
- `1` = Elastic scattering for neutrons only
- `2` = Elastic scattering for neutrons and protons (DEFAULT)

#### Entry 2: ipreq - Pre-equilibrium Model
- `0` = No pre-equilibrium model
- `1` = Use pre-equilibrium model after INC (DEFAULT)
- `2` = Random selection (energy-dependent probability, requires iexisa=0)
- `3` = Pre-equilibrium instead of INC (requires iexisa=0)

**Note:** CEM03.03 and LAQGSM03.03 use their own pre-equilibrium model always. INCL uses no pre-equilibrium model.

#### Entry 3: iexisa - Model Choice
- `0` = Do not use ISABEL INC for any particle (DEFAULT if icem=2)
- `1` = Bertini for nucleons/pions, ISABEL for other particles (DEFAULT)
- `2` = ISABEL for all incident particle types

#### Entry 4: ichoic - ISABEL INC Control (4-digit integer ijkl)
Four digits control ISABEL parameters (DEFAULT: 0023):

**Digit i (Pauli Blocking):**
- `0` = Partial Pauli blocking (DEFAULT)
- `1` = Total Pauli blocking
- `-2` = No Pauli blocking (not recommended)

**Digit j (CAS-CAS Interactions):**
- `0` = No interaction between excited particles (DEFAULT)
- `j > 0` = Number of time steps between CAS-CAS interactions

**Digit k (Density Prescription):**
- `0` = Meyer's density prescription (8 steps)
- `1` = Original isobar density prescription (8 steps)
- `2` = Krappe's folded-Yukawa prescription (16 steps, DEFAULT)
- `3-5` = Same as 0-2 but with larger Bertini nuclear radius

**Digit l (Surface Treatment):**
- `1` = Reflection/refraction at surface, no escape cutoff for isobars
- `2` = Reflection/refraction at surface, with escape cutoff
- `3` = No reflection/refraction, with escape cutoff (DEFAULT)
- `4-6` = Same as 1-3 but with 25-MeV potential well for pions

#### Entry 5: jcoul - Coulomb Barrier
- `1` = Coulomb barrier on (DEFAULT)
- `0` = Coulomb barrier off

#### Entry 6: nexite - Nuclear Recoil Energy
- `1` = Subtract nuclear recoil energy to get excitation energy (DEFAULT)
- `0` = Feature off

#### Entry 7: npidk - Pion Termination Treatment
- `0` = Force π⁻ to interact by nuclear capture at cutoff (DEFAULT)
- `1` = Force π⁻ to terminate by decay at pion cutoff energy

#### Entry 8: noact - Particle Transport Options
- `-2` = Source particles immediately collide; all progeny escape (for computing double-differential cross sections with F1/F8 + FT res)
- `-1` = Nuclear interactions of source particles only; transport and slowing down off
- `0` = Turn off all non-elastic reactions
- `1` = Perform normal transport (DEFAULT)
- `2` = Attenuation mode; transport primary source particles without non-elastic reactions

#### Entry 9: icem - Alternative Physics Model
- `0` = Use Bertini or ISABEL (determined by iexisa)
- `1` = Use CEM03.03 model (DEFAULT)
- `2` = Use INCL4 model (default evaporation: ABLA, see ievap on LEA card)

#### Entry 10: ilaq - Light Ion and Nucleon Physics Modules
- `0` = Use LAQGSM03.03 for heavy ions and light ions >940 MeV/nucleon; ISABEL for light ions <940 MeV/nucleon; LAQGSM03.03 for p/n above flenb1/flenb2 energy (DEFAULT)
- `1` = Use LAQGSM03.03 for all heavy-ion and light-ion interactions

#### Entry 11: nevtype - GEM2 Evaporation Particles
- DEFAULT: `66` (evaporation modeling up to ²⁸Mg)
- Minimum: `6` (n, p, d, t, ³He, ⁴He)
- Recommended: Use 66 only when evaporation of fragments heavier than ⁴He desired; otherwise use 6 for computational performance

### Permissible Model Physics Combinations

| Model Combination | LCA Entry 3 (iexisa) | LCA Entry 9 (icem) | LEA Entry 7 (ievap) |
|-------------------|----------------------|--------------------|---------------------|
| Bertini/Dresner   | 1                    | 0                  | 0 or -1             |
| ISABEL/Dresner    | 2                    | 0                  | 0 or -1             |
| Bertini/ABLA      | 1                    | 0                  | 2                   |
| ISABEL/ABLA       | 2                    | 0                  | 2                   |
| CEM03.03          | N/A                  | 1                  | N/A                 |
| INCL4/Dresner     | 0                    | 2                  | 0 or -1             |
| INCL4/ABLA        | 0                    | 2                  | 2                   |

**Note:** CEM03.03 contains integrated INC and evaporation/fission models; iexisa and ievap options not applicable when icem=1.

### Recommended Use
```
LCA 8J 1 1
```
This selects CEM03.03 and LAQGSM03.03, which are highly recommended.

**noact=-2** is very useful for examining single reactions without transport.

### Important Details

**CEM03.03 Model:**
- Allows n, p, π, γ to initiate nuclear reactions
- Recommended for target-nuclei energies:
  - Up to ~5 GeV for nucleon/pion-induced reactions on heavy nuclei
  - Up to ~1.2 GeV for photonuclear reactions
  - Up to ~1 GeV for reactions on light nuclei
- Consists of: INC model → pre-equilibrium model → evaporation/fission
- Fission possible for Z > 65
- Uses modified GEM2 for evaporation/fission
- Uses Fermi break-up for A < 13
- PHT code generates de-excitation gammas after evaporation

**Light Ion Handling:**
- Default: ISABEL below 940 MeV/nucleon, LAQGSM03.03 above
- ilaq=1: LAQGSM03.03 at all energies
- icem=2: INCL for all energies

**Antinucleons and Kaons:**
- Unaffected by model choice
- Always use ISABEL below flenb5 energy
- Always use LAQGSM03.03 above flenb6 energy
- Weighted random choice between flenb5 and flenb6

---

## LCB: Energy-Dependent Model Selection

The LCB card controls which physics module is used based on particle kinetic energy.

### Syntax
```
LCB flenb1 flenb2 flenb3 flenb4 flenb5 flenb6 ctofe flim0
```

### Parameters

#### flenb1 (DEFAULT: 3500 MeV)
Nucleon kinetic energy below which CEM/Bertini/INCL INC model is used (see LCA icem parameter).

#### flenb2 (DEFAULT: 3500 MeV)
Nucleon kinetic energy above which LAQGSM03.03 high-energy generator is used (see LCA ilaq parameter).

**Note:** Model selection is sampled uniformly, weighted by proximity to energy bound, between flenb1 and flenb2.

#### flenb3 (DEFAULT: 2500 MeV)
Pion kinetic energy below which CEM/Bertini/INCL INC model is used (see LCA icem parameter).

#### flenb4 (DEFAULT: 2500 MeV)
Pion kinetic energy above which LAQGSM03.03 high-energy generator is used (see LCA ilaq parameter).

**Note:** Model selection is sampled uniformly, weighted by proximity to energy bound, between flenb3 and flenb4.

#### flenb5 (DEFAULT: 800 MeV)
Kinetic energy below which ISABEL INC model is used.

#### flenb6 (DEFAULT: 800 MeV)
Kinetic energy above which appropriate model is used. Application depends on iexisa:
- `iexisa=2`: flenb5 and flenb6 apply to all particle types
- `iexisa=1`: flenb5 and flenb6 apply to all particles except nucleons and pions
- `iexisa=0`: flenb5 and flenb6 are immaterial

**Note:** Model selection is sampled uniformly, weighted by proximity to energy bound, between flenb5 and flenb6.

#### ctofe (DEFAULT: -1.0)
Cutoff kinetic energy (MeV) for particle escape during INC when using Bertini model.
- `ctofe ≥ 0`: Use ctofe as cutoff energy
- `ctofe < 0`: Random cutoff energy uniformly distributed from 0 to 2× mean binding energy (sampled per interaction, separately for n and p)

For protons: actual cutoff = max(ctofe, Coulomb barrier)
For ISABEL INC: randomized cutoff energy always used

#### flim0 (DEFAULT: -1.0)
Maximum correction allowed for mass-energy balancing in cascade stage (used with nobalc=1 on LEA card).
- `flim0 > 0`: Kinetic energies reduced by no more than fraction flim0; resample if exceeded
- `flim0 = 0`: No correction attempted; resample if negative excitation
- `flim0 < 0`: Maximum correction is 0.02 for E>250 MeV, 0.05 for E<100 MeV, 5/E between limits

### Important Details

**Bertini Scaling:**
- Nucleons: Switches to scaling procedure above 3.495 GeV (scales from 3.495 GeV interaction)
- Pions: Switches to scaling at 2.495 GeV
- Plausible upper limit for Bertini scaling: 10 GeV

**Energy Boundaries:**
- Model selection between energy bounds (flenb1/flenb2, flenb3/flenb4, flenb5/flenb6) uses weighted random sampling

### Example
```
LCA 2J 2 4J -2 0
LCB 3000 3000 2000
```
- For iexisa=1: Nucleons switch to Bertini below 3 GeV; pions switch below 2 GeV
- For iexisa=2: Nucleons and pions switch to ISABEL below 1 GeV
- ISABEL upper energy limit: 1 GeV/nucleon

---

## LCC: INCL4 and ABLA Control

The LCC card specifies control parameters for INCL4 INC model and ABLA fission-evaporation model.
- INCL4 invoked by: LCA entry 9, icem=2
- ABLA invoked by: LEA entry 7, ievap=2

### Syntax
```
LCC stincl v0incl xfoisaincl npaulincl nosurfincl J J ecutincl ebankincl ebankabla
```

### Parameters

#### stincl (DEFAULT: 1.0)
Rescaling factor of cascade duration.

#### v0incl (DEFAULT: 45 MeV)
Potential depth.

#### xfoisaincl (DEFAULT: 8.0)
Controls maximum impact parameter for Pauli blocking: rmaxws = r₀ + xfoisaincl × a
(where r₀ is nuclear radius, a is diffuseness)

#### npaulincl (DEFAULT: 0)
Controls Pauli blocking:
- `1` = Pauli strict blocking
- `0` = Pauli statistic blocking (DEFAULT)
- `-1` = No Pauli blocking

#### nosurfincl (DEFAULT: -2)
Controls diffuse nuclear surface based on Wood-Saxon density:
- `-2` = Wood-Saxon density with INCL4 stopping time (DEFAULT)
- `-1` = Wood-Saxon density with impact-dependent stopping time
- `0` = Wood-Saxon density with stopping time (no impact dependence)
- `1` = Sharp surface

#### J placeholders (entries 6-7)
Unused placeholders - must include J in keyword string.

#### ecutincl (DEFAULT: 0)
Use Bertini model below this energy.

#### ebankincl (DEFAULT: 0)
Write no INCL bank particles below this energy.

#### ebankabla (DEFAULT: 0)
Write no ABLA bank particles below this energy.

---

## LEA: Evaporation, Fermi-Breakup, and Fission Models

The LEA card controls evaporation, Fermi-breakup, level-density parameters, and fission models. These are external to the INC/pre-equilibrium model and may be used with Bertini, ISABEL, or INCL (except CEM03.03 and LAQGSM03.03).

### Syntax
```
LEA ipht icc nobalc nobale ifbrk ilvden ievap nofis
```

### Parameters

#### Entry 1: ipht - De-excitation Photons
- `0` = Generation of de-excitation photons OFF
- `1` = Generation of de-excitation photons ON (DEFAULT)

#### Entry 2: icc - LAHET-PHT Photon Physics Level
- `0` = Continuum model
- `1` = Troubetzkoy (E1) model
- `2` = Intermediate model (hybrid between 1 and 3)
- `3` = Spin-dependent model
- `4` = Full model with experimental branching ratios (DEFAULT)

#### Entry 3: nobalc - Mass-Energy Balancing (Cascade Stage)
- `0` = Use mass-energy balancing in cascade phase
- `1` = Turn OFF mass-energy balancing in cascade phase (DEFAULT)

Energy balancing controlled by flim0 parameter on LCB card. Forced balance may distort INC model intent.

#### Entry 4: nobale - Mass-Energy Balancing (Evaporation Stage)
- `0` = Use mass-energy balancing in evaporation stage (DEFAULT)
- `1` = Turn OFF mass-energy balancing in evaporation stage

#### Entry 5: ifbrk - Fermi-Breakup Model Range
- `1` = Use Fermi-breakup for A≤13 and for 14≤A≤20 with excitation <44 MeV (DEFAULT)
- `0` = Use Fermi-breakup only for A≤5

#### Entry 6: ilvden - Level-Density Model
- `-1` = Original HETC level-density formulation (see LEB card for parameters)
- `0` = Gilbert-Cameron-Cook-Ignatyuk level-density model (DEFAULT)
- `1` = Jülich level-density parameterization (function of mass number)

#### Entry 7: ievap - Evaporation and Fission Models
- `0` = RAL fission model
- `-1` = ABLA evaporation with built-in fission when icem=2; RAL fission for other cases (DEFAULT)
- `1` = ORNL fission model (allows fission only for Z≥91)
- `2` = ABLA evaporation with built-in fission model

**Note:** Bertini and ISABEL invoke Dresner evaporation with RAL fission by default. Can switch to ORNL fission using ievap option. Can switch from Dresner to ABLA by setting ievap=2.

#### Entry 8: nofis - Fission Control
- `1` = Allow fission (DEFAULT)
- `0` = Suppress fission

---

## LEB: Original HETC Level-Density Parameters

The LEB card controls level-density input options for original HETC implementation (ilvden=-1 on LEA card).

### Syntax
```
LEB yzere bzere yzero bzero
```

### Parameters

| Parameter | Z Range | Default | Description |
|-----------|---------|---------|-------------|
| yzere     | Z ≤ 70  | 1.2     | Y₀ parameter in level-density formula |
| bzere     | Z ≤ 70  | 8.0     | B₀ parameter in level-density formula |
| yzero     | Z ≥ 71  | 1.5     | Y₀ parameter for Z≥71 and all fission fragments |
| bzero     | Z ≥ 71  | 10.0    | B₀ parameter for Z≥71 and all fission fragments |

**Note:** Zero or negative values are error conditions.

---

## Integration with Other Skills

**Required Before mcnp-physics-builder:**
- mcnp-input-builder - Understand 3-block structure
- mcnp-material-builder - Define materials for physics models

**Use After mcnp-physics-builder:**
- mcnp-source-builder - Define high-energy sources
- mcnp-tally-builder - Tally secondary particles from models
- mcnp-fatal-error-debugger - Debug model physics errors
- mcnp-best-practices-checker - Verify model selections

**Related Skills:**
- mcnp-cross-section-manager - When cross sections unavailable
- mcnp-physics-validator - Validate model physics setup
- mcnp-output-parser - Parse residual nuclei from models

---

## Summary

Model physics in MCNP6 provide crucial capabilities for high-energy transport and situations where cross-section data are unavailable. Key points:

1. **Model Selection:**
   - CEM03.03 + LAQGSM03.03 recommended for most applications
   - Use LCA card to select INC model
   - Use LCB card to control energy transitions

2. **Complexity:**
   - Many parameters with interdependencies
   - Inappropriate combinations can lead to incorrect results
   - Test with known benchmarks

3. **Performance:**
   - Model physics more computationally intensive than table-based transport
   - nevtype=6 recommended for performance when heavy fragments not needed
   - ISABEL requires much greater execution time than Bertini

4. **Validation:**
   - Verify residual nuclei production
   - Check energy-angle distributions
   - Compare with experimental data when available

5. **Common Use Cases:**
   - Accelerator applications above table data energies
   - Spallation neutron sources
   - Cosmic ray transport
   - Proton therapy at high energies
   - Heavy ion transport
   - Missing cross-section data workarounds

---

## References

- MCNP6 User Manual, Chapter 5.7.8: Model Physics and Physics Models
- CEM03.03 documentation (references [200-216] in manual)
- LAQGSM03.03 documentation
- INCL4 documentation (references [252-254])
- Bertini model (references [248-249])
- ISABEL model (references [250-251])

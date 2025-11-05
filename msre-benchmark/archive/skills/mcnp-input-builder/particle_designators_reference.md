# MCNP Particle Designators Reference

**Reference Document for mcnp-input-builder Skill**

This document provides comprehensive information about particle types, designators, and properties in MCNP6.

---

## Particle Designator Syntax

MCNP uses particle designators to specify which particle type a card applies to:

### Format
```
CARD:PARTICLE_SYMBOL  parameters
```

**Examples:**
```
MODE  N P                      $ Neutron and photon transport
IMP:N  1 1 0                   $ Neutron importance
IMP:P  1 1 0                   $ Photon importance
F4:N   1                       $ Neutron flux tally
F4:P   1                       $ Photon flux tally
PHYS:N  100 J J 1              $ Neutron physics options
```

### Multiple Particles
Some cards can specify multiple particles:

```
MODE  N P E                    $ Neutron, photon, electron transport
IMP:N,P  1 1 0                 $ Same importance for neutrons and photons
F4:N,P   1                     $ Combined neutron and photon flux
```

---

## Common Particle Types

### Most Frequently Used

| Symbol | Name | Typical Use Cases |
|--------|------|-------------------|
| `:N` | Neutron | Reactor physics, criticality, shielding |
| `:P` | Photon (gamma) | Shielding, dose calculations, imaging |
| `:E` | Electron | Electron beam, bremsstrahlung, dose |
| `:\|` | Proton | Proton therapy, accelerator physics |
| `:H` | Heavy ions | Deuteron, triton, He-3, He-4 |

### Example Problem Types by Particle

**Neutron only (`:N`):**
```
MODE  N
IMP:N  1 1 1 0
F4:N   1
```
- Reactor criticality
- Neutron shielding
- Activation analysis

**Neutron + Photon (`:N :P`):**
```
MODE  N P
IMP:N  1 1 1 0
IMP:P  1 1 1 0
F6:N,P  1
```
- Coupled neutron-gamma transport
- Heating calculations
- Dose assessments

**Electron + Photon (`:E :P`):**
```
MODE  E P
IMP:E  1 1 1 0
IMP:P  1 1 1 0
F8:E,P  999
```
- Electron beam simulations
- X-ray production
- Medical physics

---

## Complete Particle Table

MCNP6 supports 37 particle types. The table below provides comprehensive information:

| ID | Symbol | Name | Mass (MeV/c²) | Charge | Energy Cutoff | Mean Life (s) |
|----|--------|------|---------------|--------|---------------|---------------|
| 1 | N | Neutron | 939.565 | 0 | 0 | 887 |
| 2 | P | Photon | 0 | 0 | 0.001 | Stable |
| 3 | E | Electron | 0.511 | -1 | 0.001 | Stable |
| 4 | \| | Proton | 938.272 | +1 | 1.0 | Stable |
| 5 | F | Electron neutrino | 0 | 0 | 0 | Stable |
| 6 | ! | Antineutron | 939.565 | 0 | 0 | 887 |
| 7 | < | Antiproton | 938.272 | -1 | 1.0 | Stable |
| 8 | Q | Deuteron | 1875.613 | +1 | 1.0 | Stable |
| 9 | T | Triton | 2808.921 | +1 | 1.0 | 3.89×10⁸ |
| 10 | S | He-3 | 2808.392 | +2 | 1.0 | Stable |
| 11 | A | Alpha (He-4) | 3727.379 | +2 | 1.0 | Stable |
| 12 | * | Heavy ions | Variable | Variable | 1.0 | Variable |
| 13 | ? | Generic | Variable | Variable | - | - |
| 14 | / | Positron | 0.511 | +1 | 0.001 | Stable |
| 15 | G | Muon neutrino | 0 | 0 | 0 | Stable |
| 16 | H | Antineutrino (electron) | 0 | 0 | 0 | Stable |
| 17 | O | Antimuon neutrino | 0 | 0 | 0 | Stable |
| 18 | U | Muon (negative) | 105.658 | -1 | 1.0 | 2.20×10⁻⁶ |
| 19 | V | Antimuon (positive) | 105.658 | +1 | 1.0 | 2.20×10⁻⁶ |
| 20 | X | Lambda baryon | 1115.683 | 0 | 1.0 | 2.63×10⁻¹⁰ |
| 21 | Y | Sigma+ baryon | 1189.370 | +1 | 1.0 | 8.02×10⁻¹¹ |
| 22 | Z | Sigma- baryon | 1197.449 | -1 | 1.0 | 1.48×10⁻¹⁰ |
| 23 | B | Xi0 baryon | 1314.860 | 0 | 1.0 | 2.90×10⁻¹⁰ |
| 24 | C | Xi- baryon | 1321.710 | -1 | 1.0 | 1.64×10⁻¹⁰ |
| 25 | W | Omega- baryon | 1672.450 | -1 | 1.0 | 8.21×10⁻¹¹ |
| 26 | @ | K0-short | 497.614 | 0 | 1.0 | 8.95×10⁻¹¹ |
| 27 | # | K0-long | 497.614 | 0 | 1.0 | 5.12×10⁻⁸ |
| 28 | % | K+ | 493.677 | +1 | 1.0 | 1.24×10⁻⁸ |
| 29 | ^ | K- | 493.677 | -1 | 1.0 | 1.24×10⁻⁸ |
| 30 | + | Pion+ | 139.570 | +1 | 1.0 | 2.60×10⁻⁸ |
| 31 | - | Pion- | 139.570 | -1 | 1.0 | 2.60×10⁻⁸ |
| 32 | Z | Pion0 | 134.977 | 0 | 1.0 | 8.52×10⁻¹⁷ |
| 33 | K | K0 | 497.614 | 0 | 1.0 | - |
| 34 | % | Anti-K0 | 497.614 | 0 | 1.0 | - |
| 35 | ^ | Antilambda | 1115.683 | 0 | 1.0 | 2.63×10⁻¹⁰ |
| 36 | G | Tau neutrino | 0 | 0 | 0 | Stable |
| 37 | $ | Anti-tau neutrino | 0 | 0 | 0 | Stable |

**Notes:**
- **Energy Cutoff:** Default minimum energy (MeV) for transport (can be overridden by CUT card)
- **Mean Life:** Decay lifetime for unstable particles
- **Stable:** Particle does not decay (or lifetime >> simulation time)
- **Heavy ions (*):** User-defined ions (see ZAID specification)

---

## Particle Designation in Common Cards

### MODE Card (Required)
Specifies which particle types to transport:

```
MODE  N                        $ Neutrons only
MODE  N P                      $ Neutrons and photons
MODE  N P E                    $ Neutrons, photons, electrons
MODE  E P                      $ Electrons and photons (no neutrons)
MODE  N P | H                  $ Neutrons, photons, protons, heavy ions
```

**Rules:**
- MODE must be first data card
- Only listed particles will be transported
- Secondary particles of unlisted types are killed

### IMP Card (Importance)
Specifies cell importance for each particle type:

```
IMP:N  1 1 1 0                 $ Neutron importance
IMP:P  1 1 1 0                 $ Photon importance
IMP:E  1 1 1 0                 $ Electron importance
```

**Alternative (in cell card):**
```
1  1  -1.0  -1  IMP:N=1 IMP:P=1
```

### Tally Cards (F1-F8)
Specify which particle type to tally:

```
F1:N   1                       $ Neutron current through surface 1
F2:P   2                       $ Photon flux on surface 2
F4:N   10 20 30                $ Neutron flux in cells 10, 20, 30
F6:N,P  1                      $ Neutron and photon heating in cell 1
```

**Particle-specific tally numbers:**
- Neutron F4 → F14, F24, F34, ... (4, 14, 24, ...)
- Photon F4 → F4, F14, F24, ... (same numbering scheme)

### PHYS Card (Physics Options)
Control physics parameters per particle:

```
PHYS:N  100 J J 1              $ Neutron physics (Emax=100 MeV, defaults, analog)
PHYS:P  100 J 1 J 0            $ Photon physics
PHYS:E  100                    $ Electron physics (Emax=100 MeV)
```

### CUT Card (Energy Cutoffs)
Set minimum energy for particle transport:

```
CUT:N  J 0                     $ Neutron cutoff (default time, 0 MeV energy)
CUT:P  J 0.001                 $ Photon cutoff (0.001 MeV)
CUT:E  J 0.001                 $ Electron cutoff (0.001 MeV)
```

---

## Special Particle Designations

### All Particles (:A)
Some cards support `:A` to apply to all active particles:

```
IMP:A  1 1 1 0                 $ Same importance for all particles (not recommended)
```

**Note:** Usually better to specify explicitly for clarity.

### Heavy Ion Groups (:H)
`:H` represents a group of light heavy ions:

- Deuteron (Q)
- Triton (T)
- He-3 (S)
- Alpha/He-4 (A)

```
MODE  N P | H                  $ Transport protons and light heavy ions
IMP:H  1 1 1 0                 $ Importance for heavy ion group
```

---

## Energy Cutoffs by Particle Type

Energy cutoffs determine when particles stop being transported:

| Particle | Default Cutoff (MeV) | Typical Range | Notes |
|----------|---------------------|---------------|-------|
| Neutron | 0 | 0 - 20 | Often set to thermal energy (1E-11 MeV) or 0 |
| Photon | 0.001 | 0.001 - 0.1 | 1 keV common lower bound |
| Electron | 0.001 | 0.001 - 0.1 | Below this, local deposition |
| Proton | 1.0 | 1.0 - 10 | High cutoff for computational efficiency |
| Heavy ions | 1.0 | 1.0 - 10 | Similar to protons |

**Set via CUT card:**
```
CUT:N  J 1E-11                 $ Neutron cutoff to thermal energy
CUT:P  J 0.01                  $ Photon cutoff to 10 keV
CUT:E  J 0.01                  $ Electron cutoff to 10 keV
```

---

## Coupled Particle Transport

### Neutron-Photon Coupling
Most common coupled transport:

```
MODE  N P
IMP:N  1 1 1 0
IMP:P  1 1 1 0
PHYS:N  100
PHYS:P  100 J 1 J 0
F6:N,P  1                      $ Combined heating tally
```

**Physics:**
- Neutron reactions produce photons
- Photon interactions produce electrons (if MODE E included)
- Energy deposition accounts for both particles

### Neutron-Photon-Electron Coupling
Full electromagnetic cascade:

```
MODE  N P E
IMP:N  1 1 1 0
IMP:P  1 1 1 0
IMP:E  1 1 1 0
PHYS:N  100
PHYS:P  100 J 1 J 0
PHYS:E  100 J J J J J 1
F6:N,P,E  1                    $ Total heating
```

**Physics:**
- Photons produce electrons via photoelectric, Compton, pair production
- Electrons produce bremsstrahlung photons
- Full electromagnetic shower development

---

## Quick Reference: Particle Designators

### Essential Particles
- `:N` - Neutron (most common)
- `:P` - Photon/gamma
- `:E` - Electron
- `:|` - Proton
- `:H` - Heavy ions (D, T, He-3, Alpha)

### Card Usage Pattern
```
MODE  [particles]
IMP:[particle]  [values]
F[n]:[particle]  [parameters]
PHYS:[particle]  [parameters]
CUT:[particle]  [parameters]
```

### Example: Complete Coupled Problem
```
MODE  N P E                    $ All three particles
IMP:N  1 1 1 0                $ Neutron importance
IMP:P  1 1 1 0                $ Photon importance
IMP:E  1 1 1 0                $ Electron importance
F4:N   1                      $ Neutron flux
F4:P   1                      $ Photon flux
F6:N,P,E  1                   $ Total heating (all particles)
PHYS:N  100
PHYS:P  100 J 1 J 0
PHYS:E  100
CUT:N   J 0
CUT:P   J 0.001
CUT:E   J 0.001
```

---

## Further Reading

- MCNP6 User Manual, Chapter 4: Particle Designators and Properties
- MCNP6 User Manual, Chapter 5.7: Physics Data Cards (MODE, PHYS, CUT)
- Skill: mcnp-physics-builder (for detailed physics options)

---

**End of Particle Designators Reference**

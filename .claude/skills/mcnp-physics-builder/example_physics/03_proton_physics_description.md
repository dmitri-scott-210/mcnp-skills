# Example 3: Proton Physics

## Purpose
Demonstrates proton transport physics configuration for proton therapy applications with secondary particle production.

## Key Features
- **MODE H N P**: Coupled proton-neutron-photon transport
- **PHYS:H card**: Proton physics up to 250 MeV (therapy range)
- **PHYS:N card**: Secondary neutron transport
- **PHYS:P card**: Secondary photon transport
- **Material**: Water phantom (tissue-equivalent)
- **Source**: 150 MeV proton beam (therapeutic energy)
- **Geometry**: 8×8×8 cm³ water box (typical phantom size)
- **Tallies**: Proton flux, secondary neutron flux, total energy deposition

## Physics Settings Explained

### PHYS:H 250 0 1
- `emax=250 MeV`: Maximum proton energy (covers therapy range: 70-250 MeV)
- `ean=0`: Implicit capture
- `tabl=1`: Use cross-section tables when available (DEFAULT)
  - For E > table limits: Model physics automatically invoked (Bertini/ISABEL/CEM03.03)

### PHYS:N 250 0
- `emax=250 MeV`: Transport secondary neutrons up to 250 MeV
- `ean=0`: Implicit capture

### PHYS:P 250 0
- `emax=250 MeV`: Transport secondary photons up to 250 MeV

## Physical Processes

### Proton Energy Loss
1. **Ionization**: Continuous energy loss via Coulomb interactions (dominant)
2. **Nuclear elastic scattering**: Protons scatter off nuclei (small angle, small energy loss)
3. **Nuclear reactions**: (p,n), (p,p'), (p,α) reactions produce secondary particles

### Secondary Particle Production
- **Neutrons**: From (p,n) and (p,xn) reactions (important for dose calculations)
- **Photons**: From nuclear de-excitation and bremsstrahlung
- **Protons**: From (p,p') inelastic scattering

### Bragg Peak Physics
- Proton energy loss increases with decreasing energy (dE/dx ∝ 1/E)
- Maximum dose deposition near end of range (Bragg peak)
- Precise range control critical for therapy

## When to Use This Configuration
- **Proton therapy treatment planning**: Dose calculations, range verification
- **Proton radiography**: Imaging applications
- **Accelerator shielding**: Proton beam losses, secondary neutron production
- **Space radiation**: Proton transport through shielding materials
- **Research**: Proton-induced nuclear reactions

## Expected Behavior
- 150 MeV protons enter water phantom along +z axis
- Continuous energy loss via ionization (Bethe-Bloch formula)
- Protons produce secondary neutrons and photons via nuclear reactions
- Bragg peak forms near end of range (~16 cm depth for 150 MeV in water)
- F6 tally shows total dose: protons + secondary neutrons + photons
- Secondary neutron flux peaks near Bragg peak region

## Important Notes
- **Table limits**: Proton cross-section tables typically cover up to ~150-200 MeV
  - Above this, MCNP automatically invokes model physics (Bertini/ISABEL/CEM03.03)
  - Ensure model physics parameters appropriate if source >150 MeV
- **Secondary neutrons**: Can contribute 5-10% of total dose in proton therapy
- **Range uncertainty**: ~1-3% due to cross-section uncertainties and CT Hounsfield unit conversion

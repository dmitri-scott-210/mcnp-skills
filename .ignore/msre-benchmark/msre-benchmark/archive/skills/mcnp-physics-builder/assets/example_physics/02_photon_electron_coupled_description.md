# Example 2: Coupled Photon-Electron Physics

## Purpose
Demonstrates coupled photon-electron transport with detailed physics settings for dose and energy deposition calculations.

## Key Features
- **MODE P E**: Coupled photon-electron transport (no neutrons)
- **PHYS:P card**: Detailed photon physics with electron production
- **PHYS:E card**: Electron transport with energy-loss straggling
- **Material**: Lead (high-Z material for electromagnetic interactions)
- **Source**: 2 MeV photon point source
- **Tallies**: Photon flux, electron flux, and total energy deposition

## Physics Settings Explained

### PHYS:P 10 0 J 1 0
- `emax=10 MeV`: Maximum photon energy (5× source energy for safety)
- `ean=0`: Implicit capture
- `J`: Use default for tabl
- `ides=1`: Detailed photon physics (enables accurate electron production)
- `nocoh=0`: Coherent (Rayleigh) scattering ON (important for low-energy photons in high-Z)

### PHYS:E 10 0 J 1 J 1
- `emax=10 MeV`: Maximum electron energy
- `ean=0`: Implicit capture
- `J`: Use default for tabl
- `ides=1`: Detailed bremsstrahlung physics
- `J`: Default ibad
- `istrg=1`: Energy-loss straggling ON (Landau straggling for accurate energy deposition)

## Physical Processes

### Photon Interactions in Lead
1. **Photoelectric effect** (dominant at E < 500 keV): Photon absorbed, electron ejected
2. **Compton scattering** (dominant 0.5-5 MeV): Photon scatters, electron knocked on
3. **Pair production** (threshold 1.022 MeV): Photon → e⁺ + e⁻

### Electron Transport
- **Ionization**: Electrons lose energy continuously
- **Bremsstrahlung**: Electrons produce photons (important in high-Z materials)
- **Straggling**: Statistical fluctuations in energy loss (modeled with istrg=1)

## When to Use This Configuration
- Gamma-ray shielding with dose calculations
- Medical physics (photon beam therapy, imaging)
- Radiography applications
- Any problem requiring accurate energy deposition from photons + electrons
- High-Z materials where bremsstrahlung significant

## Expected Behavior
- 2 MeV photons undergo Compton scattering and pair production in lead
- Photoelectric effect contributes at lower energies
- Secondary electrons transport and deposit energy
- Bremsstrahlung photons produced by electrons in high-Z lead
- F6 tally shows total energy deposition from both photons and electrons

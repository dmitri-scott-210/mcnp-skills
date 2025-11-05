# Example 1: Basic Neutron Physics

## Purpose
Demonstrates fundamental neutron physics configuration using PHYS:N and CUT:N cards for a simple neutron transport problem.

## Key Features
- **PHYS:N card**: Sets maximum neutron energy (emax=20 MeV) and implicit capture (ean=0)
- **CUT:N card**: Establishes transport cutoff at 1 keV (0.001 MeV)
- **Material**: Aluminum-27 target
- **Source**: 14.1 MeV point source (D-T fusion neutrons)
- **Tallies**: Volume-averaged flux with energy bins

## Physics Settings Explained

### PHYS:N 20 0
- `emax=20 MeV`: Maximum neutron energy for transport (sufficient for 14.1 MeV source plus (n,2n) reactions)
- `ean=0`: Implicit capture everywhere (most efficient for deep penetration problems)

### CUT:N J 5J 0.001
- `J`: No time cutoff (use default)
- `5J`: Skip next 5 parameters (use defaults)
- `0.001`: Transport cutoff energy = 1 keV (0.001 MeV)
  - Neutrons below 1 keV are killed
  - Appropriate for fast neutron problem where thermal neutrons unimportant

## When to Use This Configuration
- Fast neutron shielding problems
- D-T or D-D fusion neutron sources
- Problems where thermal neutrons (<1 keV) don't contribute significantly
- Baseline neutron-only transport (no photon coupling needed)

## Expected Behavior
- Neutrons transport from 14.1 MeV source down to 1 keV cutoff
- Some (n,2n) reactions will produce neutrons up to ~15-16 MeV
- Implicit capture improves efficiency (no weight game at low energies)
- Flux tally will show energy spectrum from cutoff (1 keV) to source energy

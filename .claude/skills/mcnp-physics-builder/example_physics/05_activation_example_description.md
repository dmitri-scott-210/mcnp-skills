# Example 5: Activation and Delayed Particles (ACT Card)

## Purpose
Demonstrates delayed neutron and photon production from fission using the ACT card in a criticality calculation.

## Key Features
- **MODE N P**: Coupled neutron-photon transport
- **ACT fission=both**: Enable both delayed neutrons and delayed photons
- **KCODE**: Criticality calculation with delayed particles
- **Material**: Bare U-235 sphere (simplified critical system)
- **Geometry**: 2.4 cm radius sphere (approximately critical bare U-235)
- **Tallies**: Neutron flux and photon flux

## Physics Settings Explained

### ACT fission=both

**ACT Card Options**:
- `fission=none`: No delayed particles (DEFAULT)
- `fission=dn`: Delayed neutrons only
- `fission=dg`: Delayed photons only
- `fission=both`: Both delayed neutrons and delayed photons (THIS EXAMPLE)

**What Are Delayed Particles?**

1. **Prompt Particles** (emitted instantly at fission, t < 10⁻¹⁴ s):
   - ~99.3% of fission neutrons
   - Prompt fission gammas

2. **Delayed Neutrons** (emitted from fission product decay, t = 0.1s - 60s):
   - ~0.7% of fission neutrons
   - Critical for reactor control (allow human reaction time)
   - 6-8 precursor groups with different half-lives (0.2s - 56s)

3. **Delayed Photons** (emitted from fission product decay, t = seconds - years):
   - Fission product decay gammas
   - Important for shutdown dose, decay heat
   - Continue long after reactor shutdown

## Physical Impact

### Effect on keff
Including delayed neutrons increases keff by:
- **Bare U-235**: +0.3% to +0.5% Δk/k (~300-500 pcm)
- **Thermal reactors**: +0.5% to +0.7% Δk/k (~500-700 pcm)

**Why?**
- Delayed neutrons have lower average energy (~0.5 MeV vs ~2 MeV prompt)
- Lower energy → less leakage → higher keff

### Effect on Criticality Calculation
- **Prompt neutron lifetime**: τ_prompt ~ 10⁻⁸ to 10⁻⁵ s
- **Effective neutron lifetime** (with delayed): τ_eff ~ 0.1 s
- Delayed neutrons slow down power excursions (stabilizing effect)

## When to Use ACT Card

### Use fission=dn (delayed neutrons) When:
- **Accurate keff required** (keff uncertainty < 100 pcm)
- Criticality safety calculations
- Reactor physics benchmarks
- Kinetics calculations (delayed neutron importance)

### Use fission=dg (delayed photons) When:
- **Shutdown dose calculations** (dose rates minutes/hours after shutdown)
- Decay heat calculations
- Spent fuel handling (gamma dose from fission products)
- Time-dependent problems (TSPLT card)

### Use fission=both When:
- Comprehensive reactor physics model
- Both keff accuracy and shutdown dose needed
- Validation against experimental data (criticality + dose)

### Skip ACT Card When:
- Shielding problems (no fission, or delayed particles negligible)
- Fast spectrum criticality (delayed neutron impact small)
- Computational time critical (ACT adds ~10-20% runtime)

## Delayed Neutron Precursor Groups

MCNP models delayed neutrons with 6-8 precursor groups (isotope-dependent):

**Example: U-235 (6 groups)**:
| Group | Half-life (s) | Yield (%) | Energy (MeV) |
|-------|---------------|-----------|--------------|
| 1     | 55.7          | 0.021     | 0.25         |
| 2     | 22.7          | 0.142     | 0.56         |
| 3     | 6.2           | 0.128     | 0.43         |
| 4     | 2.3           | 0.257     | 0.62         |
| 5     | 0.61          | 0.075     | 0.42         |
| 6     | 0.23          | 0.027     | 0.56         |

**Total**: ~0.65% of fission neutrons are delayed

## Expected Behavior

### Criticality Calculation
- KCODE runs 125 cycles (25 skip, 100 active)
- keff with ACT fission=both ≈ 1.003 to 1.005 (bare U-235 sphere)
- keff without ACT ≈ 1.000 (prompt neutrons only)
- Difference: ~0.3-0.5% Δk/k

### Flux Tallies
- **F4:N (neutron flux)**: Includes prompt + delayed neutrons
  - Delayed neutrons contribute at lower energies (0.2-0.6 MeV peak)
  - Prompt neutrons dominate at higher energies (fission spectrum)

- **F14:P (photon flux)**: Includes prompt + delayed gammas
  - Prompt gammas: High energy (1-7 MeV)
  - Delayed gammas: Broad spectrum (0.1-3 MeV, depends on fission product mix)

## Important Notes

### Computational Cost
- ACT card adds ~10-20% to runtime
- Tracks precursor inventories
- Samples delayed particle emission times and energies

### Time-Dependent Problems
For time-dependent simulations (pulsed sources, transients):
- Use TSPLT card to bin tallies by time
- ACT fission=both captures delayed particle contributions at different times
- Important for decay heat and dose rate vs time

### Compatibility with Other Cards
- **FMULT card**: ACT dnbias (delayed neutron biasing) CANNOT be used with FMULT method=5, 6, 7 (LLNL/FREYA/CGMF)
- **KOPTS card**: Can specify prompt/delayed neutron details for criticality

## Advanced Use: Delayed Neutron Biasing

For problems where delayed neutrons rare but important:
```
ACT fission=dn dnbias=10
```
- Increases delayed neutron weight by factor of 10
- Improves statistics for delayed neutron tallies
- Use with caution (can bias keff if not corrected properly)

## Validation
Compare keff with/without ACT:
```
c No ACT (prompt only):
keff = 1.0000 ± 0.0005

c With ACT fission=dn:
keff = 1.0035 ± 0.0005

c Difference: +0.35% Δk/k (typical for U-235)
```

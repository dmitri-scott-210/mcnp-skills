# ACT Card Comprehensive Reference

## Overview

The ACT card controls activation and delayed particle production including delayed neutrons, delayed photons, and radioactive decay during transport.

## Syntax

```
ACT KEYWORD=value
```

## Keywords

### fission - Delayed Particle Production from Fission

```
ACT fission=option
```

| Option | Description |
|--------|-------------|
| none | No delayed particle production (DEFAULT) |
| dn | Delayed neutron production only |
| dg | Delayed photon production only |
| both | Both delayed neutrons and photons |
| all | Delayed neutrons, photons, and light ions |

### dn - Delayed Neutron Control

```
ACT dn=option dnbias=b
```

**Options:**
- none: No delayed neutrons
- model: Use delayed neutron model
- library: Use library data (if available)

**dnbias:** Delayed neutron biasing factor (default: 0 = no biasing)

**Important:** dnbias CANNOT be used with FMULT method=5, 6, or 7.

### dg - Delayed Photon Control

```
ACT dg=option
```

**Options:**
- none: No delayed photons
- model: Use delayed photon model
- lines: Line-emission photons
- continuum: Continuum photons
- all: Both lines and continuum

### thresh - Energy Thresholds

```
ACT thresh=e_neutron e_photon
```

Delayed particles below threshold energies are not transported (killed immediately).

### hlcut - Half-Life Cutoff

```
ACT hlcut=t_min t_max
```

Only include precursors with half-lives in range [t_min, t_max] seconds.

### nap - Neutron Activation Product Transport

```
ACT nap=option
```

Controls transport of activation products (residual nuclei from (n,γ), (n,2n), etc.)

## Use Cases

### 1. Delayed Neutron Criticality

```
MODE N
ACT fission=dn dnbias=1
```

Includes delayed neutrons in criticality calculation (eigenvalue slightly higher).

### 2. Decay Gamma Dose

```
MODE N P
ACT fission=dg
```

Transports delayed photons from fission product decay (important for shutdown dose).

### 3. Pulsed Source with Delayed Particles

```
SDEF PAR=SF
ACT fission=both thresh=0.01 1e-4
```

Spontaneous fission source with both delayed neutrons (>0.01 MeV) and photons (>0.0001 MeV).

## Important Notes

1. **Increases run time:** Delayed particle tracking adds significant computational cost
2. **Memory usage:** Storing precursor data increases memory
3. **Criticality:** Delayed neutrons affect keff (typically +0.3% to +0.7% Δk/k)
4. **Time-dependent:** Most useful for time-dependent problems (TSPLT card)

## Integration

**Required Before ACT:**
- MODE card - Define particles (must include particles to be produced)
- PHYS cards - Set physics for delayed particles

**Related Cards:**
- FMULT - Fission multiplicity (NOTE: dnbias incompatible with FMULT method=5,6,7)
- TSPLT - Time splitting (for time-dependent delayed particle problems)
- KOPTS - Criticality options (delayed neutrons in keff)

**Related Skills:**
- mcnp-source-builder - Especially spontaneous fission sources
- mcnp-criticality-analyzer - Interpret keff with delayed neutrons
- mcnp-tally-analyzer - Separate prompt vs delayed contributions

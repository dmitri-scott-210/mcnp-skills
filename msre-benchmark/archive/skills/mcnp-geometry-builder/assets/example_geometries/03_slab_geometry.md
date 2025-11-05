# Example 3: Multi-Layer Slab Geometry

## Purpose
Demonstrates one-dimensional slab geometry for deep penetration shielding calculations.

## Concepts Illustrated
- **Planar surfaces only** (PZ cards) - no lateral boundaries
- **Infinite lateral extent** - particles only track in Z direction
- **Multi-layer shielding** - alternating materials for optimization
- **Importance increase** - variance reduction for deep penetration
- **Directional source** - VEC and DIR parameters for beam source
- **Energy-dependent tallies** - flux binned by energy

## Geometry Description
- **Cell 1**: Source void, z < 0 cm
- **Cell 2**: Water layer 1, 0 < z < 10 cm
- **Cell 3**: Lead shield, 10 < z < 15 cm (5 cm thick)
- **Cell 4**: Water layer 2, 15 < z < 25 cm
- **Cell 5**: Concrete shield, 25 < z < 30 cm (5 cm thick)
- **Cell 6**: Detector void, 30 < z < 50 cm
- **Cell 7**: Graveyard, z > 50 cm

## Materials
- M1: Light water (H₂O) with thermal scattering
- M2: Lead (Pb, Z=82) at 11.35 g/cm³
- M3: Concrete (simplified composition) with thermal scattering

## Source
Planar source at z=0, directed along +Z axis:
- Position: (0, 0, 0)
- Energy: 14.1 MeV (D-T fusion neutrons)
- Direction: VEC=0 0 1 (pointing toward +Z)
- DIR=1 (cosine distribution, forward-peaked)

## Variance Reduction
Importance increases through shield layers:
- Source region: IMP:N=1
- Water 1: IMP:N=1
- Lead: IMP:N=2 (2× splitting)
- Water 2: IMP:N=4 (4× splitting)
- Concrete: IMP:N=8 (8× splitting)
- Detector: IMP:N=8 (maintain statistics)

## Tallies
F4:N tally in detector region (cell 6) with 5 energy bins:
- 0.0 - 0.1 MeV (thermal and epithermal)
- 0.1 - 1.0 MeV (intermediate)
- 1.0 - 10.0 MeV (fast)
- 10.0 - 15.0 MeV (source energy range)

## Usage
```bash
mcnp6 inp=03_slab_geometry.i
```

## Expected Results
- Fast neutrons penetrate lead better than concrete
- Water moderates neutrons (energy decreases)
- Thermal flux builds up in water layers
- Importance helps statistics in detector region
- Source energy (14.1 MeV) should dominate highest energy bin initially

## Learning Points
1. **Slab geometry**: PZ surfaces only = infinite X-Y extent
2. **Directional source**: VEC sets direction, DIR sets angular spread
3. **Importance scaling**: Powers of 2 (1→2→4→8) typical for deep penetration
4. **Material layering**: Water + heavy metal more effective than single material
5. **Energy binning**: Reveals spectrum changes through shield

## Typical Applications
- Reactor biological shield design
- Spent fuel cask analysis
- Accelerator vault shielding
- Medical treatment room walls

## Modifications to Try
- Add more shield layers (optimize thickness)
- Try different materials (boron, tungsten, polyethylene)
- Change importance scheme (test 1-2-4-8 vs 1-4-16-64)
- Add F2 tally on surfaces to see transmission
- Model actual finite lateral dimensions with PX/PY

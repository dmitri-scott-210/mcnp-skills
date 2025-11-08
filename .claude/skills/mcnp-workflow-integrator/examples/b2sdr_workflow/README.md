# Burnup-to-Shutdown-Dose-Rate (B2SDR) Workflow Example

Complete example workflow for calculating shutdown dose rates from burnup simulations.

## Overview

This workflow demonstrates the complete multi-physics coupling for shutdown dose rate calculations:

1. **Neutron Transport** (MCNP) → Establish flux/power distributions
2. **Depletion** (ORIGEN) → Track isotopic evolution during irradiation
3. **Decay Source Generation** (Python) → Calculate photon sources from decay
4. **Photon Transport** (MCNP) → Calculate dose rates from decay gammas
5. **Post-Processing** (Python) → Generate dose rate maps and reports

## Workflow Diagram

```
[Neutron MCNP]
      ↓ (flux, power)
[ORIGEN Depletion]
      ↓ (isotopic inventory)
[Decay Source Generation]
      ↓ (photon sources)
[Photon MCNP]
      ↓ (dose rates)
[Post-Processing]
      ↓ (plots, tables)
```

## Directory Structure

```
b2sdr_workflow/
├── README.md                       # This file
├── data/
│   └── power.csv                   # Reactor power history
├── scripts/
│   ├── 01_generate_neutron_model.py
│   ├── 02_run_mcnp_neutron.sh
│   ├── 03_extract_flux.py
│   ├── 04_run_origen.sh
│   ├── 05_generate_photon_sources.py
│   ├── 06_generate_sdr_model.py
│   ├── 07_run_mcnp_photon.sh
│   └── 08_post_process_dose.py
└── run_complete_workflow.sh        # Execute entire workflow
```

## Requirements

### Software

- MCNP6.2 or later
- ORIGEN2.2 or MOAA (MCNP-ORIGEN coupling tool)
- Python 3.8+

### Python Packages

```bash
pip install pandas numpy matplotlib
```

## Usage

### Option 1: Complete Workflow (Automated)

Run the entire workflow with one command:

```bash
./run_complete_workflow.sh
```

This executes all stages sequentially with error checking.

### Option 2: Step-by-Step Execution

Execute each stage individually for debugging or customization:

#### Stage 1: Generate Neutron Transport Model

```bash
python scripts/01_generate_neutron_model.py
```

Creates `neutron_transport.i` with fuel geometry and tallies.

#### Stage 2: Run Neutron Transport

```bash
bash scripts/02_run_mcnp_neutron.sh
```

Runs MCNP neutron transport calculation. **Estimated time**: 2-4 hours.

#### Stage 3: Extract Flux/Power Data

```bash
python scripts/03_extract_flux.py
```

Parses MCNP output and creates `flux_data.csv` and `power_data.csv`.

#### Stage 4: Run Depletion Calculation

```bash
bash scripts/04_run_origen.sh
```

Runs ORIGEN depletion for tracked cells. **Estimated time**: 1-2 hours.

#### Stage 5: Generate Photon Sources

```bash
python scripts/05_generate_photon_sources.py
```

Calculates decay gamma sources from depleted isotopic inventory.
Creates `photon_sources.txt` with SDEF cards.

#### Stage 6: Generate Photon Transport Model

```bash
python scripts/06_generate_sdr_model.py
```

Creates `photon_transport.i` using photon sources from Stage 5.

#### Stage 7: Run Photon Transport

```bash
bash scripts/07_run_mcnp_photon.sh
```

Runs MCNP photon transport for dose rate calculation. **Estimated time**: 2-4 hours.

#### Stage 8: Post-Process Results

```bash
python scripts/08_post_process_dose.py
```

Generates dose rate plots and tables in `results/` directory.

## Key Parameters

### Reactor Geometry (Stage 1)

- Core radius: 150 cm
- Active height: 400 cm
- Fuel: TRISO particles in graphite matrix
- Moderator: Graphite reflector

### Irradiation History (Stage 4)

- Irradiation time: 1000 days
- Average power: 100 MW
- Time steps: 10 (100 days each)

### Cooling Time (Stage 5)

- Default: 1 day after shutdown
- Modify in `scripts/05_generate_photon_sources.py` to vary cooling time

### Dose Rate Tallies (Stage 6)

- Point detectors: 5 locations around reactor
- FMESH: 3D dose rate map (100×100×100 cm³ voxels)
- Dose conversion: ANSI/ANS-6.1.1-1977 factors

## Outputs

### Generated Files

- `neutron_transport.i` - MCNP neutron transport input
- `neutron.o` - MCNP neutron output
- `flux_data.csv` - Cell-wise flux distributions
- `power_data.csv` - Cell-wise power distributions
- `origen_output.txt` - ORIGEN depletion results
- `isotopic_inventory.json` - Depleted isotopics
- `photon_sources.txt` - SDEF cards for photon sources
- `photon_transport.i` - MCNP photon transport input
- `photon.o` - MCNP photon output

### Results

- `results/dose_rates.png` - Dose rate bar chart
- `results/dose_map_xy.png` - 2D dose rate map (XY plane)
- `results/dose_map_xz.png` - 2D dose rate map (XZ plane)
- `results/dose_rates.csv` - Dose rate data table
- `results/dose_rates_report.txt` - Summary report

## Validation

Expected dose rates at 1 day cooling:

- **Near vessel wall** (150 cm radius): ~10-100 Sv/h
- **Maintenance area** (300 cm radius): ~1-10 Sv/h
- **Outer shielding** (500 cm radius): ~0.01-0.1 Sv/h

Compare your results to these ranges for reasonableness check.

## Troubleshooting

### Issue: ORIGEN Not Found

**Solution**: Ensure ORIGEN or MOAA is in your PATH, or modify `scripts/04_run_origen.sh` with full path.

### Issue: Lost Particles in Photon Transport

**Solution**: Check photon source positions in Stage 5. Ensure they're within fuel cells.

### Issue: Poor Statistical Quality

**Solution**: Increase particle count in KCODE/SDEF cards. Recommended: 50,000+ particles.

### Issue: Long Run Times

**Solution**:
- Reduce geometry complexity in Stage 1
- Reduce time steps in Stage 4 (10 → 5)
- Use variance reduction in Stage 6 (weight windows)

## Customization

### Change Cooling Time

Edit `scripts/05_generate_photon_sources.py`:

```python
COOLING_TIME_DAYS = 7  # Change from 1 to 7 days
```

### Add More Detector Locations

Edit `scripts/06_generate_sdr_model.py`:

```python
detector_positions = [
    (200, 0, 0),
    (300, 0, 0),
    (400, 0, 0),  # Add new position
]
```

### Change Dose Conversion Factors

Edit `scripts/06_generate_sdr_model.py` to use different dose factor library (e.g., ICRP-21).

## References

1. **MCNP Manual**: LA-UR-17-29981 (Chapter 3.3 - Source definitions, Chapter 4 - Tallies)
2. **ORIGEN Manual**: ORNL/TM-2005/39
3. **Dose Factors**: ANSI/ANS-6.1.1-1977
4. **Example Study**: Fairhurst-Agosta & Kozlowski, "Shutdown Dose Rate Calculations for HTGR", Nuclear Science and Technology Open Research, 2024

## Contact

For questions about this workflow example, see the main skill documentation at:
`.claude/skills/mcnp-workflow-integrator/SKILL.md`

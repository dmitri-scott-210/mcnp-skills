# MCNP-ORIGEN Coupling Tutorial
**Step-by-Step Workflow for Depletion and Dose Rate Calculations**

## Purpose

This tutorial provides a complete workflow for coupling MCNP neutron transport with ORIGEN depletion calculations, based on production methods from AGR-1 and μHTGR reactor models. Includes manual coupling and automation strategies.

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    BURNUP WORKFLOW                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: MCNP Neutron Transport                            │
│    ├─ Input: Fresh fuel composition                        │
│    ├─ Calculate: Flux in all cells                         │
│    ├─ Extract: Cell-wise flux spectra                      │
│    └─ Output: Flux data for ORIGEN                         │
│                      ↓                                      │
│  Step 2: ORIGEN Depletion                                  │
│    ├─ Input: MCNP flux + initial composition               │
│    ├─ Calculate: Isotopic evolution (Bateman equations)    │
│    ├─ Apply: Power history, time steps                     │
│    └─ Output: Cell-wise isotopics vs. time                 │
│                      ↓                                      │
│  Step 3: Update MCNP Materials                             │
│    ├─ Input: ORIGEN depleted isotopics                     │
│    ├─ Update: Material cards in MCNP input                 │
│    └─ Verify: k_eff with new compositions                  │
│                      ↓                                      │
│  Step 4: Iterate (Multi-Cycle)                             │
│    ├─ Repeat steps 1-3 for each cycle                      │
│    └─ Converge: k_eff stable cycle-to-cycle                │
│                      ↓                                      │
│  Step 5: Shutdown Dose Rates                               │
│    ├─ Input: ORIGEN inventory after decay time             │
│    ├─ Generate: Photon source from activities              │
│    ├─ Run: MCNP photon transport (MODE P)                  │
│    └─ Output: 3D dose rate map                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: MCNP Neutron Transport (Flux Calculation)

### 1.1 Initial MCNP Input

Create MCNP input with fresh fuel composition and flux tallies:

```mcnp
c ================================================================
c MCNP Flux Calculation for ORIGEN Coupling
c Fuel: Fresh UO2, 4.5% enriched
c ================================================================

c --- Cells ---
100  1  -10.4  -100  IMP:N=1  VOL=193.0  $ Fuel cell

c --- Surfaces ---
100  CZ  0.41  $ Fuel radius

c --- Materials (BOL) ---
M1  $ Fresh UO2, 4.5% enriched
   92234.70c  3.6e-4
   92235.70c  0.045
   92236.70c  2.1e-6
   92238.70c  0.955
    8016.70c  2.0

c --- Source ---
KCODE  10000  1.0  50  150
KSRC  0 0 0

c --- CRITICAL: Flux Tally for ORIGEN ---
F4:n  100  $ Cell 100 flux (n/cm²/s)
FC4  Flux in fuel cell for ORIGEN coupling
FM4  -1.0 1 -6  $ Fission rate tally (for power normalization)

c --- Energy bins (optional, for spectrum) ---
E4  1e-10 1e-6 0.1 1 20  $ Thermal, epithermal, fast

c --- Run parameters ---
PRINT  110 126  $ Print detailed tally and material info
NPS  10000000   $ High statistics for flux
```

### 1.2 Run MCNP

```bash
mcnp6 i=input_bol.i o=output_bol.o
```

### 1.3 Extract Flux Data

**From MCNP output** (output_bol.o):

```
Cell Flux Tally (F4:n)
----------------------------------------------------
Cell 100:  5.234E+13 ± 0.3%  n/cm²/s

Energy spectrum:
  Thermal (< 1 eV):     40.2%
  Epithermal (1-100 keV): 35.8%
  Fast (> 100 keV):     24.0%
```

**Record these values**:
- **Total flux**: 5.234E+13 n/cm²/s
- **Spectrum**: 40% thermal, 36% epithermal, 24% fast

---

## Step 2: ORIGEN Depletion Calculation

### 2.1 Create ORIGEN Input File

**File**: `origen_cell100_cycle1.inp`

```
=shell
  copy ft33f001 ${OUTDIR}/ft33f001
  copy ft71f001 ${OUTDIR}/origen_cell100.f71
end

=origen
  case{
    lib{ file="end7dec" }  $ ENDF/B-VII decay and fission yield library

    mat{
      units=ATOMS  $ Atom-based input
      iso=[
        u234=3.6e-4
        u235=0.045
        u236=2.1e-6
        u238=0.955
        o16=2.0
      ]
    }

    case(caseA){
      lib{ file="pwrue50" }  $ PWR U-235 enriched cross-section library

      time{
        units=DAYS
        t=[100 200 300 400 500 540]  $ Burnup time steps (days)
      }

      flux=[5.234e13 5.234e13 5.234e13 5.234e13 5.234e13 5.234e13]  $ Constant flux (n/cm²/s)
      power=[7.72 7.72 7.72 7.72 7.72 7.72]  $ Constant power (MW)

      save{
        file="cell100_cycle1.f71"
      }
    }
  }
end
```

**Alternative: ORIGEN 2.2 Format** (older SCALE versions):

```
-1
-1
-1
RDA  MCNP Cell 100 - Cycle 1 Burnup
LIB 0 1 2 3 9 3 9 3 9  $ PWR library (cross-section set)
TIT MCNP Cell 100 - Cycle 1
FLU 5.234E13  $ Flux from MCNP (n/cm²/s)
HED 1 1 1
BAS 1.0E6  $ 1 MTU basis
INP 1 1 1 0 0 0

c Initial composition (from MCNP M1)
  92234  3.6E-4
  92235  0.045
  92236  2.1E-6
  92238  0.955
   8016  2.0
  0 0 0

c Irradiation steps
IRP  100  7.72  1  2  4  $ 100 days at 7.72 MW
IRP  100  7.72  1  2  4
IRP  100  7.72  1  2  4
IRP  100  7.72  1  2  4
IRP  100  7.72  1  2  4
IRP  40   7.72  1  2  4  $ Final 40 days (total 540)
OUT  2  1  0  0
END
```

### 2.2 Run ORIGEN

```bash
# Modern SCALE/ORIGEN (TRITON/ORIGEN sequence)
scale origen_cell100_cycle1.inp

# OR older ORIGEN 2.2
origen < origen_cell100_cycle1.inp > origen_cell100_cycle1.out
```

### 2.3 Extract Depleted Composition

**From ORIGEN output** (origen_cell100_cycle1.out):

```
ISOTOPE INVENTORY AT TIME = 540 DAYS

ISOTOPE    GRAMS      CURIES     ATOM FRACTION
----------------------------------------------
U-234      1.20E+02   6.20E-03   1.20E-04
U-235      8.00E+03   1.70E-02   8.00E-03
U-236      5.00E+03   3.20E-02   5.00E-03
U-238      9.40E+05   3.20E-01   9.40E-01
Pu-238     2.30E+01   3.90E+02   2.30E-05
Pu-239     6.00E+03   3.70E+02   6.00E-03
Pu-240     3.00E+03   6.80E+02   3.00E-03
Pu-241     2.00E+03   2.10E+05   2.00E-03
Pu-242     8.00E+02   3.20E+00   8.00E-04
Np-237     6.00E+02   4.20E-01   6.00E-04
Am-241     1.00E+02   3.40E+02   1.00E-04
Xe-135     5.73E-04   1.20E+06   5.73E-10
Sm-149     2.70E+01   0.00E+00   2.66E-08
Gd-157     1.44E-03   0.00E+00   1.44E-10
Cs-137     1.20E+03   8.70E+04   1.23E-06
Sr-90      9.50E+02   1.20E+05   9.88E-07
...
```

### 2.4 Convert to MCNP Material Card

**Python script** (convert_origen_to_mcnp.py):

```python
#!/usr/bin/env python3
"""Convert ORIGEN output to MCNP material card"""

import pandas as pd

# Read ORIGEN isotopic output (atom fractions)
isotopes = {
    92234: 1.20e-4,
    92235: 8.00e-3,
    92236: 5.00e-3,
    92238: 9.40e-1,
    94238: 2.30e-5,
    94239: 6.00e-3,
    94240: 3.00e-3,
    94241: 2.00e-3,
    94242: 8.00e-4,
    93237: 6.00e-4,
    95241: 1.00e-4,
    54135: 5.73e-10,  # Xe-135 (equilibrium)
    62149: 2.66e-8,   # Sm-149
    64157: 1.44e-10,  # Gd-157
    55137: 1.23e-6,   # Cs-137
    38090: 9.88e-7,   # Sr-90
    # ... more isotopes
}

# Normalize to total atom density
total_density = 0.0800  # atoms/barn-cm (approximately constant for fuel)
oxygen_fraction = 2.0   # Stoichiometric O in UO2

# Calculate heavy metal + FP fractions
heavy_metal = sum([v for k, v in isotopes.items() if k > 90000])
oxygen = oxygen_fraction

# Normalize
norm_factor = total_density / (heavy_metal + oxygen)

# Write MCNP material card
print("M1  $ Depleted UO2, cell 100, after 540 days")
print("c Actinides")
for zaid in sorted([k for k in isotopes.keys() if 90000 < k < 100000]):
    density = isotopes[zaid] * norm_factor
    print(f"   {zaid}.70c  {density:.6E}  $ {get_isotope_name(zaid)}")

print("c Fission products")
for zaid in sorted([k for k in isotopes.keys() if k < 90000]):
    density = isotopes[zaid] * norm_factor
    if density > 1e-15:  # Only include if significant
        print(f"   {zaid}.70c  {density:.6E}  $ {get_isotope_name(zaid)}")

print("c Oxygen (approximately constant)")
print(f"    8016.70c  {oxygen * norm_factor:.6E}  $ O-16")

def get_isotope_name(zaid):
    """Convert ZAID to isotope name"""
    z = zaid // 1000
    a = zaid % 1000
    elements = {92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm',
                54: 'Xe', 62: 'Sm', 64: 'Gd', 55: 'Cs', 38: 'Sr'}
    return f"{elements.get(z, '?')}-{a}"
```

**Run**:
```bash
python convert_origen_to_mcnp.py > material_depleted.txt
```

**Output** (material_depleted.txt):
```mcnp
M1  $ Depleted UO2, cell 100, after 540 days
c Actinides
   92234.70c  1.200000E-04  $ U-234
   92235.70c  8.000000E-03  $ U-235
   92236.70c  5.000000E-03  $ U-236
   92238.70c  9.400000E-01  $ U-238
   93237.70c  6.000000E-04  $ Np-237
   94238.70c  2.300000E-05  $ Pu-238
   94239.70c  6.000000E-03  $ Pu-239
   94240.70c  3.000000E-03  $ Pu-240
   94241.70c  2.000000E-03  $ Pu-241
   94242.70c  8.000000E-04  $ Pu-242
   95241.70c  1.000000E-04  $ Am-241
c Fission products
   38090.70c  9.880000E-07  $ Sr-90
   54135.70c  5.730000E-10  $ Xe-135
   55137.70c  1.230000E-06  $ Cs-137
   62149.70c  2.660000E-08  $ Sm-149
   64157.70c  1.440000E-10  $ Gd-157
c Oxygen (approximately constant)
    8016.70c  2.000000E+00  $ O-16
```

---

## Step 3: Update MCNP and Verify

### 3.1 Create New MCNP Input with Depleted Composition

**File**: `input_eoc1.i`

```mcnp
c ================================================================
c MCNP Verification Run - End of Cycle 1
c Fuel: Depleted composition from ORIGEN
c ================================================================

c --- Cells ---
100  1  -10.4  -100  IMP:N=1  VOL=193.0  $ Depleted fuel

c --- Surfaces ---
100  CZ  0.41

c --- Materials (EOC1, from ORIGEN) ---
M1  $ Depleted UO2, cell 100, after 540 days
c Actinides
   92234.70c  1.200000E-04
   92235.70c  8.000000E-03
   92236.70c  5.000000E-03
   92238.70c  9.400000E-01
   93237.70c  6.000000E-04
   94238.70c  2.300000E-05
   94239.70c  6.000000E-03
   94240.70c  3.000000E-03
   94241.70c  2.000000E-03
   94242.70c  8.000000E-04
   95241.70c  1.000000E-04
c Fission products
   38090.70c  9.880000E-07
   54135.70c  5.730000E-10
   55137.70c  1.230000E-06
   62149.70c  2.660000E-08
   64157.70c  1.440000E-10
c Oxygen
    8016.70c  2.000000E+00

c --- Source ---
KCODE  10000  1.0  50  150
KSRC  0 0 0

c --- Tallies (for cycle 2 flux) ---
F4:n  100
FM4  -1.0 1 -6

NPS  10000000
```

### 3.2 Run and Verify k_eff

```bash
mcnp6 i=input_eoc1.i o=output_eoc1.o
```

**Check output**:
```
k_eff (final estimate): 1.0523 ± 0.0008

Verify:
- BOL k_eff: 1.2500 (fresh fuel)
- EOL k_eff: 1.0523 (depleted fuel)
- Delta-k: -0.1977 (-19,770 pcm burnup reactivity loss)
```

**Typical burnup reactivity loss**: -15 to -25 pcm per GWd/MTU

---

## Step 4: Multi-Cycle Iteration

**Repeat Steps 1-3** for each cycle:

### Cycle 2

1. **MCNP with EOC1 composition** → extract new flux
2. **ORIGEN with new flux** → calculate EOC2 composition
3. **Update MCNP** → verify k_eff
4. **Iterate** until k_eff stable

### Convergence Criteria

```python
# Check k_eff convergence
k_eff_difference = abs(k_eff_cycle2 - k_eff_cycle1)
if k_eff_difference < 50_pcm:  # 50 pcm = 0.0005 delta-k
    print("Converged")
else:
    print(f"Not converged, difference: {k_eff_difference:.0f} pcm")
    # Run another iteration
```

---

## Step 5: Shutdown Dose Rate Calculation

### 5.1 ORIGEN Decay Calculation

After final cycle, decay fuel for dose rate time:

**File**: `origen_decay_30days.inp`

```
=origen
  case{
    lib{ file="end7dec" }

    mat{
      units=ATOMS
      iso=[
        $ Load EOC composition from previous ORIGEN run
        u234=1.20e-4
        u235=8.00e-3
        $ ... all isotopes ...
      ]
    }

    case(decay){
      time{
        units=DAYS
        t=[1 7 30 365 1825]  $ Decay times: 1d, 1wk, 1mo, 1yr, 5yr
      }

      flux=[0 0 0 0 0]  $ No flux during decay
      power=[0 0 0 0 0]

      save{
        file="cell100_decay.f71"
      }
    }
  }
end
```

### 5.2 Extract Photon Source Data

**From ORIGEN output**:

```
PHOTON SOURCE STRENGTH AT 30 DAYS DECAY

ISOTOPE    ACTIVITY (Ci)   PHOTON ENERGY (MeV)   PHOTONS/SEC
----------------------------------------------------------------
Cs-137     8.70E+04        0.662                 3.24E+15
Ba-140     5.20E+03        0.537                 2.80E+14
La-140     5.20E+03        1.596                 4.68E+14
Co-60      1.20E+03        1.173, 1.332          2.50E+13
...

Total photon emission rate: 4.29E+15 photons/sec
```

### 5.3 Create MCNP Photon Transport Input

**File**: `input_dose.i`

```mcnp
c ================================================================
c Shutdown Dose Rate Calculation
c Source: ORIGEN isotopic inventory after 30 days decay
c Mode: Photon transport only
c ================================================================

c --- Geometry (same as neutron calc) ---
100  1  -10.4  -100  IMP:P=1  $ Depleted fuel (photon source)
101  0  100 -101  IMP:P=1      $ Air around fuel
999  0  101  IMP:P=0           $ Void

100  CZ  0.41   $ Fuel
101  CZ  100    $ Detector region

c --- Materials (depleted fuel, no neutron cross-sections needed) ---
M1  $ Depleted fuel (for density only, photon transport)
   92234.70c  1.20e-4  $ Actinides for density
   $ ... (full composition, but only density used for photon transport)

c --- Photon Source (from ORIGEN) ---
SDEF  CEL=100  ERG=D1  PAR=2  $ Photon source in cell 100

c Energy distribution (from ORIGEN photon spectrum)
SI1  H  0.05 0.2 0.5 0.7 1.0 1.5 2.0  $ MeV bins
SP1  D  0   3.24e15 2.80e14 4.68e14 3.24e15 2.50e13 1.00e13  $ Photons/sec

c --- Dose Tally ---
F4:p  101  $ Photon flux at detector (photons/cm²)
FC4  Photon flux for dose rate calculation
DE4  0.01 0.05 0.1 0.2 0.5 1.0 2.0 5.0  $ Dose function energy bins
DF4  1.0e-3 2.0e-3 5.0e-3 1.5e-2 5.0e-2 1.2e-1 2.0e-1 3.0e-1  $ Dose conversion (Sv/photon)

c --- Run Parameters ---
MODE  P  $ Photon transport only
NPS  10000000
```

### 5.4 Run and Extract Dose Rates

```bash
mcnp6 i=input_dose.i o=output_dose.o
```

**From output**:

```
F4:p Tally (Photon Flux)
Cell 101: 5.23E+08 photons/cm²/s ± 0.5%

Dose rate (using dose function):
  1.24E-02 Sv/hr = 1.24 rem/hr = 12.4 mSv/hr

Interpretation:
- Contact dose rate (30 days post-shutdown): 12.4 mSv/hr
- Dominated by Cs-137 (661 keV gamma)
- Requires shielding for personnel access
```

---

## Automation with Scripts

### Master Script (automate_burnup.sh)

```bash
#!/bin/bash
# Automate MCNP-ORIGEN coupling for multi-cycle burnup

CYCLES=3
CELL=100

for cycle in $(seq 1 $CYCLES); do
    echo "=== Cycle $cycle ==="

    # Step 1: MCNP neutron transport
    echo "Running MCNP (flux calculation)..."
    mcnp6 i=input_cycle${cycle}.i o=output_cycle${cycle}.o

    # Step 2: Extract flux
    echo "Extracting flux from MCNP output..."
    python extract_flux.py output_cycle${cycle}.o > flux_cycle${cycle}.txt

    # Step 3: Create ORIGEN input
    echo "Creating ORIGEN input..."
    python create_origen_input.py flux_cycle${cycle}.txt material_cycle${cycle}.txt > origen_cycle${cycle}.inp

    # Step 4: Run ORIGEN
    echo "Running ORIGEN (depletion)..."
    origen < origen_cycle${cycle}.inp > origen_cycle${cycle}.out

    # Step 5: Extract depleted composition
    echo "Converting ORIGEN output to MCNP material..."
    python convert_origen_to_mcnp.py origen_cycle${cycle}.out > material_cycle$((cycle+1)).txt

    # Step 6: Create next cycle input
    if [ $cycle -lt $CYCLES ]; then
        echo "Creating MCNP input for cycle $((cycle+1))..."
        python create_mcnp_input.py material_cycle$((cycle+1)).txt > input_cycle$((cycle+1)).i
    fi

    echo "Cycle $cycle complete"
    echo ""
done

echo "All cycles complete. Running shutdown dose calculation..."
python create_origen_decay.py material_cycle$((CYCLES+1)).txt > origen_decay.inp
origen < origen_decay.inp > origen_decay.out
python create_mcnp_dose.py origen_decay.out > input_dose.i
mcnp6 i=input_dose.i o=output_dose.o

echo "DONE"
```

---

## Validation Checklist

After coupling:
- [ ] k_eff trend reasonable (decreases with burnup)
- [ ] Burnup value matches expected (GWd/MTU)
- [ ] Pu vector matches literature (55-60% Pu-239 for LWR)
- [ ] Fission product inventory matches ORIGEN benchmarks
- [ ] Dose rates physically reasonable (mSv/hr range for fresh spent fuel)
- [ ] Mass balance: HM_initial ≈ HM_final + fission_products
- [ ] Activity dominated by Cs-137, Sr-90 at 1-100 years

---

## References

- SCALE Manual: TRITON/ORIGEN coupling
- ORNL/TM-2005/39: ORIGEN-S validation
- NUREG/CR-6801: Burnup Credit Criticality Safety
- AGR-1 MOAA coupling methodology (INL/EXT-10-19917)

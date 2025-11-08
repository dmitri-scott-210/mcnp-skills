# Tally Multipliers: EM, TM, CM Cards (Histogram)

**Purpose:** Detailed specifications for energy-dependent (EM), time-dependent (TM), and cosine-dependent (CM) histogram multipliers for MCNP tallies.

**Source:** MCNP6 Manual Chapter 5.09, sections 5.9.9-5.9.11 (EM, TM, CM cards)

---

## Overview

The EM, TM, and CM cards provide histogram-based multipliers for tallies, allowing per-unit-energy, per-unit-time, and per-steradian normalization. These differ from DE/DF cards which use continuous interpolation.

**Three histogram multiplier types:**
- **EM:** Energy-dependent multipliers (requires E card energy bins)
- **TM:** Time-dependent multipliers (requires T card time bins)
- **CM:** Cosine-dependent multipliers for F1/F2 (requires C card angular bins)

**Key difference from DE/DF:**
- **EM/TM/CM:** Histogram (step function) - constant value within each bin
- **DE/DF:** Continuous function - interpolated between energy points

---

## EM Card: Energy-Dependent Multiplier

### Purpose

Multiply tally results by energy-dependent factors to create per-unit-energy tallies or apply energy-dependent response functions as histograms.

### Syntax

```
EMn   m1 m2 m3 ... mk
```

**Parameters:**
- **n:** Tally number (e.g., EM4 for tally F4)
- **m1, m2, ..., mk:** Multiplier values for each energy bin (k = number of E card bins)

**Requirements:**
- E card must exist for tally n
- Number of multipliers must equal number of energy bins from E card

### Common Use Cases

#### Use Case 1: Per-Unit-Energy Flux

Convert integrated flux (particles) to differential flux (particles/MeV):

```
F4:n  10                   $ Cell flux tally
E4    0.1 0.5 1.0 2.0 5.0 10.0  $ Energy bins (MeV)
EM4   2.5 2.0 1.0 0.667 0.4 $ Divide by bin width: 1/ΔE
c     1/(0.5-0.1)  1/(1.0-0.5)  1/(2.0-1.0)  1/(5.0-2.0)  1/(10.0-5.0)
```

**Result:** Tally output in particles/cm²/MeV instead of particles/cm²

#### Use Case 2: Histogram Response Function

Apply energy-dependent response (e.g., detector efficiency) as histogram:

```
F5:p  0 0 10  0.5         $ Point detector
E5    0.05 0.1 0.5 1.0 2.0 5.0  $ Photon energy bins
EM5   0.10 0.25 0.40 0.50 0.45  $ Detector efficiency per bin
c     10% efficiency 0.05-0.1 MeV
c     25% efficiency 0.1-0.5 MeV
c     40% efficiency 0.5-1.0 MeV
c     50% efficiency 1.0-2.0 MeV
c     45% efficiency 2.0-5.0 MeV
```

**Result:** Tally weighted by detector efficiency

### EM0 Card: Default for All Tallies

```
EM0   m1 m2 m3 ... mk
```

Sets default energy multipliers for ALL tallies that have E cards. Individual EMn cards override EM0 for specific tallies.

---

## TM Card: Time-Dependent Multiplier

### Purpose

Multiply tally results by time-dependent factors to create per-unit-time tallies or apply time-dependent weighting.

### Syntax

```
TMn   m1 m2 m3 ... mk
```

**Parameters:**
- **n:** Tally number (e.g., TM4 for tally F4)
- **m1, m2, ..., mk:** Multiplier values for each time bin (k = number of T card bins)

**Requirements:**
- T card must exist for tally n
- Number of multipliers must equal number of time bins from T card

### Common Use Cases

#### Use Case 1: Per-Unit-Time Reaction Rate

Convert integrated reaction rate to rate per unit time:

```
F4:n  50                   $ Fuel cell flux
FM4   1.0 10 -6            $ Fission reaction multiplier
T4    0 1e-8 1e-7 1e-6 1e-5  $ Time bins (shakes)
TM4   1e8 1.1e7 1e6 1e5    $ Divide by bin width: 1/Δt
c     1/(1e-8-0)  1/(1e-7-1e-8)  1/(1e-6-1e-7)  1/(1e-5-1e-6)
```

**Result:** Fission rate per shake instead of integrated fissions

#### Use Case 2: Pulsed Source Weighting

Weight time bins by pulse importance (e.g., detector active time fraction):

```
F5:n  0 0 100  1.0        $ Detector location
T5    0 10 20 30 40 50    $ Time bins (μs)
TM5   1.0 0.2 1.0 0.2 1.0 $ Detector alive: 10-20, 30-40, 50+
c     Full weight when detector active
c     20% weight during dead time
```

**Result:** Weighted tally reflecting detector availability

### TM0 Card: Default for All Tallies

```
TM0   m1 m2 m3 ... mk
```

Sets default time multipliers for ALL tallies that have T cards.

---

## CM Card: Cosine-Dependent Multiplier

### Purpose

Multiply F1 or F2 tallies by cosine-dependent factors to create per-steradian tallies or apply angular-dependent weighting.

### Syntax

```
CMn   m1 m2 m3 ... mk
```

**Parameters:**
- **n:** Tally number for F1 or F2 only (e.g., CM1 for tally F1)
- **m1, m2, ..., mk:** Multiplier values for each cosine bin (k = number of C card bins)

**Requirements:**
- C card must exist for tally n
- Tally must be F1 (surface current) or F2 (surface flux)
- Number of multipliers must equal number of cosine bins from C card

### Common Use Cases

#### Use Case 1: Per-Steradian Surface Current

Convert surface current to angular current density (particles/sr):

```
F1:n  100                  $ Surface current
C1    -1.0 -0.5 0.0 0.5 1.0  $ Cosine bins
CM1   0.637 0.849 0.849 0.637  $ 1/[2π(cosθᵢ-cosθᵢ₋₁)]
c     For uniformly spaced cosine bins:
c     Ω = 2π(cosθᵢ - cosθᵢ₋₁) = solid angle
c     m = 1/Ω for per-steradian normalization
```

**Calculation:**
```
θ: -1.0→-0.5: Ω = 2π(0.5) = 3.14 sr    → m = 0.318
θ: -0.5→0.0:  Ω = 2π(0.5) = 3.14 sr    → m = 0.318
θ:  0.0→0.5:  Ω = 2π(0.5) = 3.14 sr    → m = 0.318
θ:  0.5→1.0:  Ω = 2π(0.5) = 3.14 sr    → m = 0.318
```

**Result:** Angular current in particles/cm²/sr

#### Use Case 2: Angular Response Weighting

Weight angular bins by direction-dependent detector efficiency:

```
F2:n  200                  $ Surface flux on detector
C2    -1.0 -0.707 0.0 0.707 1.0  $ Cosine bins (angles)
CM2   0.5 0.8 1.0 0.8      $ Efficiency vs angle
c     50% efficiency for grazing angles (±180°)
c     80% efficiency for ±45°
c     100% efficiency for normal incidence
```

**Result:** Flux weighted by angular-dependent response

### CM0 Card: Default for All Tallies

```
CM0   m1 m2 m3 ... mk
```

Sets default cosine multipliers for ALL F1/F2 tallies that have C cards.

---

## Comparison: EM/TM/CM vs DE/DF

### Histogram (EM/TM/CM) vs Continuous (DE/DF)

**EM/TM/CM characteristics:**
- **Step function:** Constant multiplier within each bin
- **No interpolation:** Bin edges create discontinuities
- **Bin-specific:** Each bin has independent multiplier
- **Use case:** Bin-by-bin normalization, detector efficiency histograms

**DE/DF characteristics:**
- **Continuous function:** Interpolated between energy points
- **Smooth:** LIN or LOG interpolation between points
- **Energy-dependent:** Response varies continuously with energy
- **Use case:** Smooth response functions (dose coefficients, cross sections)

### When to Use Each

**Use EM/TM/CM when:**
- Normalizing by bin width (per-unit-energy, per-unit-time, per-steradian)
- Applying histogram-based detector efficiency
- Each bin needs independent treatment
- Step function appropriate for physical situation

**Use DE/DF when:**
- Smooth energy-dependent response (ICRP dose coefficients)
- Physical quantity varies continuously
- Interpolation between points appropriate
- Built-in response functions (IC keyword)

### Example: Same Response, Different Methods

**Histogram approach (EM):**
```
E4    0.1 0.5 1.0 2.0 5.0
EM4   0.3 0.5 0.7 0.8     $ Constant in each bin
```

**Continuous approach (DE/DF):**
```
DE4   0.1 0.5 1.0 2.0 5.0
DF4   0.3 0.5 0.7 0.8 0.85  $ Interpolated between points
```

**Difference:**
- EM: Step changes at bin boundaries
- DE/DF: Smooth transition between energies

---

## Multiple Multipliers Combined

### Combining EM, TM, CM

All three can be used simultaneously on a single tally:

```
F1:n  100                  $ Surface current tally
E1    0.1 1.0 10.0         $ Energy bins
T1    0 1e-8 1e-6          $ Time bins
C1    -1.0 0.0 1.0         $ Cosine bins
EM1   10.0 1.0             $ Energy-dependent multiplier
TM1   1e8 1e6              $ Time-dependent multiplier (1/Δt)
CM1   0.318 0.318          $ Per-steradian normalization
```

**Result:** Tally multiplied by EM × TM × CM for each (E, T, C) bin combination

### Combining with FM Card

EM/TM/CM can be used with FM (reaction rate multiplier):

```
F4:n  10                   $ Cell flux
FM4   1.0 10 -6            $ Fission multiplier
E4    0.1 1.0 10.0
EM4   10.0 1.0             $ Per-unit-energy normalization
```

**Result:** Fission rate per unit energy

**Order of operations:**
1. Tally scored (flux)
2. FM multiplier applied (flux × cross section = reaction rate)
3. EM multiplier applied (reaction rate × 1/ΔE = rate per MeV)

---

## Best Practices

### Bin Width Normalization

**Per-unit-energy (EM):**
```
EM values should be 1/ΔE for each bin
Check units: MeV bins → use ΔE in MeV
```

**Per-unit-time (TM):**
```
TM values should be 1/Δt for each bin
Check units: Shakes vs seconds vs microseconds
```

**Per-steradian (CM):**
```
CM values should be 1/Ω where Ω = 2π(cosθᵢ - cosθᵢ₋₁)
For equal cosine spacing Δμ: Ω = 2πΔμ
```

### Verification

**Check multiplier count:**
```
Number of EM values must equal number of E bins
Number of TM values must equal number of T bins
Number of CM values must equal number of C bins
MCNP will give FATAL ERROR if counts don't match
```

**Verify units:**
```
After applying multipliers, check output units make sense
Example: F4 (flux) × EM (1/MeV) = flux per MeV ✓
```

### Common Errors

**Error: Too few multipliers**
```
E4    0.1 0.5 1.0 2.0 5.0 10.0  $ 5 bins
EM4   2.5 2.0 1.0 0.667         $ Only 4 values - FATAL ERROR
```

**Error: Wrong units**
```
T4    0 1 2 3 4 5              $ Time in microseconds
TM4   1 1 1 1 1                $ Should be 1/Δt = 1.0 per μs
c     Correct: All bins same width, so all TM = 1.0 is OK
c     But check if you wanted per-second: TM = 1e6 1e6 1e6 1e6 1e6
```

---

## Integration with Other Skills

**Related skills:**
- **mcnp-tally-builder:** General tally setup requiring EM/TM/CM
- **mcnp-source-builder:** Time-dependent sources need TM normalization
- **dose_and_special_tallies.md:** DE/DF comparison and dose functions

**Typical workflows:**

**Workflow 1: Differential flux calculation**
1. Set up F4 cell flux tally
2. Define E card with energy bins
3. Calculate bin widths: ΔEᵢ = Eᵢ₊₁ - Eᵢ
4. Create EM card: EMn = 1/ΔE₁, 1/ΔE₂, ..., 1/ΔEₖ
5. Result: Flux per unit energy (particles/cm²/MeV)

**Workflow 2: Angular current density**
1. Set up F1 surface current tally
2. Define C card with cosine bins
3. Calculate solid angles: Ωᵢ = 2π(cosθᵢ₊₁ - cosθᵢ)
4. Create CM card: CMn = 1/Ω₁, 1/Ω₂, ..., 1/Ωₖ
5. Result: Current per steradian (particles/cm²/sr)

---

**For more information:**
- MCNP6 Manual: Chapter 5.09, sections 5.9.9-5.9.11
- Solid angle calculation reference
- Tally units and normalization guide

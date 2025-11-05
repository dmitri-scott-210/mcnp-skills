# Dose Functions and F8 Special Tallies

**Purpose:** Comprehensive reference for DE/DF dose conversion functions, F8 pulse-height tally special features, and FT card special treatments.

**Source:** MCNP6 Manual Chapter 5.09, sections 5.9.8 (DE/DF), 5.9.1.8 (F8 tallies), 5.9.18 (FT special treatments)

---

## Overview

This document covers three main topics:

1. **DE/DF cards:** Continuous energy-dependent response functions (dose coefficients)
2. **F8 pulse-height tallies:** Special considerations, zero/epsilon bins, flagging, variance reduction
3. **FT card special treatments:** Advanced tally modifications (PHL, CAP, RES, TAG, etc.)

---

## Part 1: DE/DF Dose Conversion Functions

### Purpose

Convert flux tallies to dose, dose equivalent, or other energy-dependent responses using continuous interpolation functions.

### Syntax

```
DEn log/lin E1 E2 E3 ... Ek
DFn log/lin F1 F2 F3 ... Fk
```

**Parameters:**
- **n:** Tally number
- **log/lin:** Interpolation method for table (default: log-log)
- **Ei:** Energy points (MeV)
- **Fi:** Response function values at Ei

**Interpolation modes:**
- **LOG LOG:** Log-log interpolation (default) - appropriate for most dose functions
- **LIN LIN:** Linear-linear interpolation
- **LIN LOG:** Linear interpolation on DF, log on DE
- **LOG LIN:** Log interpolation on DF, linear on DE

### Built-In Response Functions (IC Keyword)

Instead of providing DE/DF tables, use IC keyword on DF card with built-in functions:

```
DFn IC=code IU=units FAC=factor
```

**IC codes:**
- **IC=99:** ICRP-60 dose conversion factors (RECOMMENDED for modern calculations)
  - Neutrons: Radiation weighting factors w_R
  - Charged particles: Quality factors Q(LET)
- **IC=[other]:** See Table 5.21 in MCNP Manual for detector response functions
  - he3-1: He-3 detector
  - nai-1: NaI scintillator
  - bgo-1: BGO scintillator
  - Many others (see PHL detector table)

**IU keyword:** Units control
- **IU=1:** rem/h
- **IU=2:** Sv/h (DEFAULT)

**FAC keyword:** Normalization factor
- **FAC=-3:** Use ICRP-60 dose conversion factors (DEFAULT with IC=99)
- **FAC>0:** User-supplied normalization factor
- **FAC=0:** No normalization

### ICRP-60 Dose Conversion (IC=99, FAC=-3)

**For neutrons:**
Radiation weighting factors w_R convert absorbed dose to ambient dose equivalent:

```
w_R = 2.5 + 18.2 × exp[−ln²(E)/(6)] for E_n < 1 MeV
w_R = 5.0 + 17.0 × exp[−ln²(2×E)/(6)] for 1 ≤ E_n ≤ 50 MeV
w_R = 2.5 + 3.25 × exp[−ln²(0.04×E)/(6)] for E_n > 50 MeV
```

Where E is in MeV.

**For charged particles:**
Quality factors Q based on stopping power S(E,p) in keV/μm:

```
Q = 1                               for S < 10 keV/μm
Q = 0.32×S − 2.2                    for 10 ≤ S < 100 keV/μm
Q = 300/√S                          for S ≥ 100 keV/μm
```

**Applications:**
- Energy deposition tallies (F6, +F8)
- Converting absorbed dose (Gy) to dose equivalent (Sv)
- Regulatory dose assessments

### DE/DF vs EM/TM/CM Comparison

| Feature | DE/DF | EM/TM/CM |
|---------|-------|----------|
| **Function type** | Continuous interpolation | Histogram (step function) |
| **Bin requirement** | Independent of tally bins | Must match E/T/C bins exactly |
| **Interpolation** | LOG-LOG, LIN-LIN, LIN-LOG, LOG-LIN | None (constant per bin) |
| **Use case** | Smooth energy-dependent response (dose, detector efficiency) | Bin-by-bin normalization (per-MeV, per-second) |
| **Built-in functions** | Yes (IC keyword) | No |

**When to use DE/DF:**
- Dose conversion factors (ICRP, ANSI/ANS)
- Smooth detector response functions
- Energy-dependent cross sections
- Physical quantities varying continuously with energy

**When to use EM/TM/CM:**
- Dividing by bin width (per-MeV, per-second, per-steradian)
- Histogram-based response (e.g., detector efficiency table)
- Independent treatment per energy bin

### DE/DF Examples

**Example 1: User-Supplied Response Function**
```
fc5 Point detector tally modified by user-supplied response
f5:p 0 0 5 1
de5 0.01 0.1 0.2 0.5 1.0
df5 lin 0.062 0.533 1.03 2.54 4.6
```
- Logarithmic interpolation on DE (default)
- Linear interpolation on DF

**Example 2: ICRP-60 Alpha Dose Equivalent**
```
fc6 Helium-4 (alpha) dose equivalent (Sv)
f6:a 77
df6 IC=99 IU=2 FAC=-3
```
- ICRP-60 dose conversion
- Units: Sv/h per source particle
- Source strength must be weighted by particles/sec

**Example 3: He-3 Detector Response**
```
fc26 Helium-3 detector response for tritium
f26:t 6
df26 IC=he3-1
```
- Built-in He-3 detector response function
- Tritium tally

### DE/DF Best Practices

1. **IC=99 for regulatory dose:** Always use ICRP-60 for modern dose assessments
2. **Check units:** IU=2 (Sv/h) is standard, IU=1 (rem/h) for legacy calculations
3. **Source normalization:** FAC>0 requires source strength in particles/sec
4. **DE0/DF0 cards:** Set default dose function for all tallies without specific DE/DF
5. **Verify interpolation:** Default LOG-LOG appropriate for most dose functions
6. **Energy range:** Ensure DE covers full energy range of tally (extrapolation occurs outside)

---

## Part 2: F8 Pulse-Height Tally Special Features

### Overview

F8 tallies score energy deposited in a cell per source particle, creating a pulse-height distribution. Special features include:

- Zero and epsilon bins (highly recommended)
- Asterisk (*F8) and plus (+F8) flagging
- Variance reduction limitations
- Roulette control
- Microscopic realism requirements

### Zero and Epsilon Bins (CRITICAL)

**Recommendation:**
```
E8 0 1E-5 1E-3 0.01 0.1 1.0 10.0
```

**Why critical:**
- **Zero bin:** Captures histories with NO energy deposition in cell
- **Epsilon bin (1E-5):** Captures very small depositions (e.g., delta rays escaping)
- Without these: Lose normalization and statistical interpretation

**Physical meaning:**
- Zero bin → Particles passed through without interaction or deposited < numerical precision
- Epsilon bin → Particles deposited tiny amounts (often computational artifacts)
- Higher bins → Physical pulse-height distribution

### Energy Bins Interpretation

**E8 bins are PULSE energy (total deposited), NOT particle energy at scoring:**

```
F8:p 10
E8 0 1E-5 0.1 0.5 1.0 2.0 5.0
```

Each history contributes to ONE bin based on TOTAL energy deposited in cell:
- If 0 MeV deposited → Bin 1 (zero)
- If 1E-7 MeV deposited → Bin 2 (epsilon)
- If 0.3 MeV deposited → Bin 3 (0.1-0.5 MeV)
- If 1.5 MeV deposited → Bin 5 (1.0-2.0 MeV)

**Scoring details:**
- Pulse = Σ(entry energies) − Σ(departure energies) per history
- Includes all particles of specified type in cell during history
- Union tallies (multiple cells): Sum energy, not average

### Asterisk Flagging (*F8): Energy Deposition Tally

**Syntax:**
```
*F8:p 10
```

**Conversion:**
Converts pulse-height tally to energy deposition tally (still per history).

**Difference from +F8:**
- *F8: Total energy deposition (MeV per history)
- F8: Pulse height (MeV per history, same result as *F8 for neutral particles)
- +F8: Charge deposition (electrons = −1, positrons = +1)

**Use case:**
- When you want F8's per-history behavior but with energy deposition semantics
- Similar to F6, but per-history instead of per-particle

### Plus Flagging (+F8): Charge Deposition Tally

**Syntax:**
```
+F8:e 10
```

**Conversion:**
Scores charge instead of energy:
- Electron: score = −1
- Positron: score = +1

**Use case:**
- Electron/positron charge balance in detector
- Verification of charge conservation
- Current calculations with F8 geometry

**Cannot combine with asterisk:**
```
+*F8:e 10    ← ILLEGAL
*+F8:e 10    ← ILLEGAL
```

### Variance Reduction for F8 Tallies

**Allowed methods:**
- IMP (importance)
- CUT (cutoffs)
- WWN (weight windows)
- FCL (forced collisions)
- EXT (exponential transform)
- DXT (DXTRAN)
- SB (source biasing)
- ESPLT (energy splitting)
- TSPLT (time splitting)

**NOT allowed:**
- WWG (weight-window generator) - MCNP will issue fatal error

**Roulette control:**
```
VAR RR=off
```

Disables Russian roulette to preserve pulse-height realism.

**Why variance reduction is tricky for F8:**
- Pulse-height tallies require microscopic realism (actual particle tracks)
- Weight games can distort pulse-height distribution
- Best practice: Use analog transport or very conservative VR

### Union Tallies for F8

**Multiple cells:**
```
F8:p 10 20 30 T
```

**Scoring:**
- Each history contributes to EACH cell's tally based on energy deposited in that cell
- Total bin (T): Sum of all cell depositions per history
- NOT an average - preserves total energy deposition

**Use case:**
- Multiple detectors in coincidence
- Total energy in detector array

### Forbidden with F8

**Cannot use:**
- DE/DF dose functions
- Flagging bins (CF/SF)
- Multiplier bins (FM card)

**Why:**
- F8 is fundamentally different from other tallies (per-history vs per-particle)
- These features designed for fluence-based tallies
- Use F6 with these features if needed

---

## Part 3: FT Card Special Treatments

### Overview

The FT card provides special tally modifications beyond standard binning. Key options:

- **PHL:** Pulse-height light (anticoincidence detectors)
- **CAP:** Coincidence capture (neutron coincidence counting)
- **RES:** Residual nuclides production
- **TAG:** Tally tagging (track particle production history)
- **FRV:** Fixed reference vector (for cosine binning)
- **GEB:** Gaussian energy broadening
- **ICD:** Identify contributing cell (detector tallies)
- **ELC:** Electron charge tally (F1 current)
- Many others (see Table 5.20)

### FT Card Syntax

```
FTn id1 p11 p12 ... id2 p21 p22 ... idK pK1 pK2 ...
```

**Parameters:**
- **n:** Tally number
- **idk:** Keyword identifier (e.g., PHL, CAP, RES, TAG)
- **pkj:** Parameters for keyword idk

**Multiple treatments:**
- Can specify multiple keywords on one FT card
- Some combinations prohibited (FU-requiring options are mutually exclusive)

### PHL: Pulse-Height Light (Anticoincidence)

**Purpose:**
Model pulse-height tally with multiple detector regions, applying material-specific light/charge conversion and anticoincidence logic.

**Syntax:**
```
FT8 PHL [N ta1 ba1 ... taN baN] [det1]
        [M tb1 bb1 ... tbM bbM] [det2]
        [J tc1 bc1 ... tcJ bcJ] [det3]
        [K td1 bd1 ... tdK bdK] [det4]
        [0] [TDEP tg tt]
```

**Parameters:**
- **N, M, J, K:** Number of F6 tallies for each detector region (up to 4 regions)
- **tai, bai:** Tally number and F-bin number pairs
- **deti:** Detector descriptor (he3-1, nai-1, bgo-1, etc.) - see Table 5.21

**Detector descriptors:**

| Detector | Name | Particle Type | Response | Default | Notes |
|----------|------|---------------|----------|---------|-------|
| He-3 | HE3-1 | p, t, h | Multiplication | 100 | 42.3 eV/ion pair |
| BF₃ | BF3-1 | a, Li | Multiplication | 100 | 36.0 eV/ion pair |
| Li Glass | LIG-1 | t, a | Quenching | 5.0E-4 cm/MeV | Generic |
| NaI | NAI-1 | e | Quenching | 3.4E-4 cm/MeV | Scintillator |
| BGO | BGO-1 | e | Quenching | 6.5E-4 cm/MeV | Scintillator |
| CsI | CSI-1 | e | Quenching | 1.5E-4 cm/MeV | Scintillator |
| BC-400 | BC4-1 | e | Quenching | 4.6E-3 cm/MeV | Plastic scintillator |
| HPGe | HPG-1 | e | Gain | 1.0 | 3.0 eV/ion pair |

**Override defaults:**
```
FT8 PHL 1 6 1 HE3-1_25.0    $ Use multiplication = 25 instead of 100
FT8 PHL 1 6 1 LIG-1_2.5e-3  $ Use quenching = 2.5E-3 instead of 5.0E-4
```

**Scintillator response (Birks's Law):**

```
dL/dx = S × dE/dx / (1 + k_B × dE/dx)
```

Where:
- **S:** Scintillation efficiency
- **k_B:** Birks's constant (quenching factor)
- **dE/dx:** Stopping power

**TDEP keyword:**
Make T8 times relative to first contribution (trigger):
```
FT8 PHL ... TDEP [tg] [tt]
```
- **tg:** Trigger tally number (default: F8 tally itself)
- **tt:** Energy threshold (MeV) (default: 0)

**Use cases:**
- Neutron detectors with light output conversion
- Gamma spectroscopy with scintillators
- Coincidence/anticoincidence measurements
- Time-of-flight detectors

### CAP: Coincidence Capture

**Purpose:**
Score neutron capture multiplicities and moments for coincidence counting.

**Syntax:**
```
FT8 CAP [-mc] [-mo] i1 i2 ... [GATE td tw] [EDEP tg tt]
```

**Parameters:**
- **mc:** Maximum number of captures (default: 21)
- **mo:** Maximum number of moments (default: 12)
- **i1, i2, ...:** Capture nuclide identifiers (ZAID format)

**GATE keyword:**
- **td:** Pre-delay time (shakes)
- **tw:** Gate width (shakes)

**EDEP keyword:**
- **tg:** Trigger tally number
- **tt:** Trigger threshold (MeV)

**Automatic settings:**
- Analog capture: CUT:n 2J 0 0
- Fission multiplicity: PHYS:n J 100 3J -1
- No variance reduction allowed

**Example:**
```
F8:n 2 (5 6) 7 T
FT8 CAP Li-6 B-10
T8 1 7LOG 1E8
```

Tallies ⁶Li and ¹⁰B captures in cells 2, 7, union (5,6), and total, with time bins from 1 to 10⁸ shakes.

### RES: Residual Nuclides Production

**Purpose:**
Record heavy-ion residual nuclides produced by high-energy or neutron reactions.

**Syntax:**
```
FT8 RES [z1 z2]              $ Z range
FT8 RES [za1 za2 ... zaN]    $ Explicit list
```

**Parameters:**
- **z1, z2:** Atomic number range (e.g., 25 27 for Mn, Fe, Co)
- **zai:** Target identifiers in ZAID format

**Binning:**
- FU card required
- Each residual isotope gets separate bin
- Elemental identifier (e.g., Fe-0) groups all iron isotopes

**Use with LCA noact=-2:**
- Source particle collides in source material immediately
- All daughters transported without further collision (vacuum)
- F8 RES → Distribution of nuclides from single collision

**Example:**
```
F8:# 1 100 T
FT8 RES 25 27
```
Residual nuclides with Z = 25-27 (Mn, Fe, Co) in cells 1, 100, and total.

### TAG: Tally Tagging

**Purpose:**
Separate tally into components based on particle production history (cell, nuclide, reaction).

**Syntax:**
```
FTn TAG a
```

**Parameter a (scatter treatment):**
- **a=1:** Elastic scatter → lose tag; bremsstrahlung/annihilation → scatter bin
- **a=2:** Elastic scatter → lose tag; bremsstrahlung/annihilation → separate bins
- **a=3:** Elastic scatter → retain tag; multiple production → use last tag
- **a=4:** Same as a=3, but Compton retains tag

**FU card format:**
```
FUn CCCCCZZAAA.RRRRR ...
```

Where:
- **CCCCC:** Cell number (00000 = all cells)
- **ZZAAA:** Target nuclide ZAID (00000 = any nuclide, for electrons)
- **RRRRR:** Reaction MT or special designator

**Special designators:**

**Source:**
- **−1 or −0000000001:** Source particle (all cells)
- **CCCCC00001:** Source particle in cell CCCCC

**Elastic scatter:**
- **0 or 0000000000:** Elastic-scattered particles

**Everything else:**
- **1e10 or 10000000000:** All other contributions

**Photon tags:**
- **00000.00001:** Bremsstrahlung
- **ZZ000.00003:** Fluorescence from element ZZ
- **00000.00003:** K x-rays from electrons
- **00000.00004:** Annihilation photons
- **ZZ000.00005:** Compton photons from element ZZ
- **ZZAAA.00006:** Muonic x-rays
- **00000.00007:** Cerenkov photons

**Neutron/photon tags:**
- **ZZAAA.99999:** Delayed particles from fission of ZZAAA
- **ZZAAA.00016:** (n,2n) from ZZAAA
- **ZZAAA.00102:** (n,γ) from ZZAAA
- **ZZAAA.00018:** Fission from ZZAAA (but may be 19,20,21,38 depending on isotope)

**Example:**
```
F1:p 1
FT1 TAG 1
FU1 0.0                  $ Elastic scatter bin
    1001                 $ Hydrogen (any reaction)
    01001.00102          $ H(n,γ) specifically
    26056.00051          $ Fe-56 (n,n') 1st level
    26056.00000          $ All other Fe-56 reactions
```

---

## FT Options Summary Table

| Keyword | Purpose | FU Required | Example Use Case |
|---------|---------|-------------|------------------|
| **PHL** | Pulse-height light with detector response | Yes | Scintillator spectroscopy |
| **CAP** | Coincidence capture multiplicities | No | Neutron coincidence counting |
| **RES** | Residual nuclide production | Yes | Activation analysis |
| **TAG** | Track particle production history | Yes | Source term analysis |
| **FRV** | Fixed reference vector for cosine | No | Custom angular binning |
| **GEB** | Gaussian energy broadening | No | Realistic detector resolution |
| **TMC** | Time convolution | No | Pulsed source simulation |
| **INC** | Number of collisions binning | Yes | Track history analysis |
| **ICD** | Contributing cell identification | Yes | Detector response mapping |
| **SCX** | Source distribution index | No | Multi-source tracking |
| **SCD** | Source distribution identification | Yes | Nuclide-specific sources |
| **ELC** | Electron charge tally | No | Charge current measurement |
| **LET** | Linear energy transfer binning | No | Proton therapy dosimetry |
| **ROC** | Receiver-operator characteristic | No | Signal/noise discrimination |
| **PDS** | Point detector pre-collision | No | Improved convergence |
| **FFT** | First fission tally | Yes | Fission chain tracking |
| **COM** | Compton imaging | No | Compton camera simulation |

---

## Integration with Other Skills

**Related skills:**
- **mcnp-tally-builder:** General tally setup and modification cards
- **mcnp-source-builder:** Source definitions for time-dependent and tagged calculations
- **mcnp-geometry-builder:** Detector geometry for pulse-height and special tallies
- **fm_reaction_numbers_complete.md:** Reaction multipliers vs dose functions

**Typical workflows:**

**Workflow 1: Dose calculation**
1. Set up flux tally (F5 point detector or F4 track-length)
2. Add DF card with IC=99 (ICRP-60)
3. Verify source normalization (particles/sec)
4. Result: Dose equivalent (Sv/h) per source particle

**Workflow 2: Pulse-height spectrum**
1. Define detector cell geometry
2. Set up F8 tally with zero and epsilon bins: E8 0 1E-5 ...
3. Add FT8 PHL with appropriate detector (NaI-1, BGO-1, etc.)
4. Use analog transport or conservative variance reduction
5. Result: Realistic pulse-height distribution (MeVee or pC)

**Workflow 3: Particle production tracking**
1. Set up F1/F2/F4/F6 tally
2. Add FT TAG with appropriate scatter treatment (a=1,2,3,4)
3. Define FU bins for specific production mechanisms
4. Result: Tally separated by production cell/nuclide/reaction

---

**For more information:**
- MCNP6 Manual: Chapter 5.09, sections 5.9.8 (DE/DF), 5.9.1.8 (F8), 5.9.18 (FT)
- ICRP-60 documentation for dose conversion factors
- Detector physics references for scintillator response (Birks's Law)

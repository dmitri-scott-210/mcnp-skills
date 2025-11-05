# MCNP Source Builder - Template Files

This directory contains MCNP input file templates for common source configurations.

---

## 📋 Template Files

| Template File | Description | Source Types |
|---------------|-------------|--------------|
| **fixed_source_templates.i** | Point, beam, surface, and volume sources | Point isotropic, monodirectional beam, surface source, volume source, ring source |
| **energy_spectrum_templates.i** | Energy distributions | Watt, Maxwellian, Gaussian, discrete lines, histogram, arbitrary tabular |
| **criticality_templates.i** | Criticality calculations | KCODE, KSRC, KOPTS options |
| **surface_source_templates.i** | Two-stage SSW/SSR | Surface source write/read for variance reduction |

---

## 🚀 Quick Start Guide

### Step 1: Choose Template

Select the template file that matches your source type:

- **Fixed spatial source** (point, beam, surface, volume) → `fixed_source_templates.i`
- **Specific energy spectrum** (Watt, Maxwell, discrete) → `energy_spectrum_templates.i`
- **Criticality calculation** (KCODE) → `criticality_templates.i`
- **Two-stage calculation** (SSW/SSR) → `surface_source_templates.i`

### Step 2: Copy Template

```bash
cp fixed_source_templates.i my_problem.i
```

### Step 3: Uncomment Desired Section

Each template has multiple options commented out with `c`. Uncomment the section you need:

```
c ========================================================================
c TEMPLATE 1: Point Isotropic Source
c ========================================================================
c Uncomment this section for point isotropic neutron source at origin
SDEF  POS=0 0 0  ERG=14.1  PAR=N
```

### Step 4: Modify Parameters

Adjust source parameters for your specific problem:
- Energy (ERG)
- Position (POS, X, Y, Z)
- Direction (DIR, VEC, AXS)
- Particle type (PAR=N/P/E)

### Step 5: Run MCNP

```bash
mcnp6 i=my_problem.i o=my_problem.out
```

---

## 📖 Detailed Template Descriptions

### 1. fixed_source_templates.i

**Purpose:** Common fixed-source spatial configurations

**Templates Included:**

1. **Point Isotropic Source**
   - Position: Origin (0, 0, 0)
   - Direction: Isotropic (4π)
   - Energy: Monoenergetic (14.1 MeV default)
   - Use case: Simple neutron generator, benchmarking

2. **Monodirectional Beam**
   - Position: Below target (0, 0, -40)
   - Direction: Collimated along +Z axis
   - Distribution: Uniform over circular cross-section
   - Use case: Accelerator beam, external source

3. **Surface Source on Sphere**
   - Position: On surface 1
   - Direction: Inward (NRM=-1)
   - Use case: Cosmic ray shower, ambient field

4. **Volume Source in Sphere**
   - Position: Uniform throughout cell 1
   - Energy: Discrete spectrum (multiple lines)
   - Use case: Activation products, distributed source

5. **Ring Source (Cylindrical)**
   - Position: Ring at z=0, radius 5-10 cm
   - Use case: Toroidal plasma source, annular configuration

**Modification Tips:**
- Change `POS=0 0 0` to relocate source
- Change `ERG=14.1` to desired energy (MeV)
- Change `PAR=N` to P (photons) or E (electrons)
- Adjust radial distribution (SI1/SP1) for beam width

---

### 2. energy_spectrum_templates.i

**Purpose:** Realistic energy distributions for neutrons and photons

**Templates Included:**

1. **Watt Fission Spectrum** (SI -3)
   - Formula: p(E) = exp(-E/a) × sinh(√(bE))
   - Default: U-235 thermal (a=0.988, b=2.249)
   - Use case: Fission neutron sources

2. **Maxwellian Spectrum** (SI -30)
   - Formula: p(E) = √E × exp(-E/T)
   - Default: T=1.29 MeV (fast reactor)
   - Use case: Thermal neutron distributions

3. **Discrete Gamma Lines**
   - Co-60: 1.173 MeV, 1.332 MeV
   - Cs-137: 0.662 MeV
   - Use case: Calibration sources, shielding studies

4. **Histogram Spectrum** (SI H)
   - Custom energy bins with probabilities
   - Use case: User-defined spectra from measurements

5. **Arbitrary Tabular** (SI A)
   - Linear interpolation between (E, p(E)) points
   - Use case: Complex measured spectra

6. **Biased Spectrum** (with SB card)
   - Source probabilities + importance biasing
   - Use case: Variance reduction for rare events

7. **Gaussian Spectrum** (SI -41)
   - Formula: p(E) = exp(-(E-E₀)²/(2σ²))
   - Use case: Monochromatic with energy spread

**Modification Tips:**
- Watt: Adjust a, b parameters (see MCNP Manual Table 5.14)
  - U-235: a=0.988, b=2.249
  - Pu-239: a=1.175, b=1.040
- Maxwell: Adjust T (temperature in MeV)
- Discrete: Add/remove energy lines in SI/SP
- Histogram: Must have n+1 SI values for n SP probabilities
- **Change MODE to MODE P for photon sources**

---

### 3. criticality_templates.i

**Purpose:** K-eigenvalue calculations with KCODE

**Templates Included:**

1. **Bare Sphere** (Godiva-like)
   - Unreflected HEU sphere
   - Use case: Benchmark problems, critical mass studies

2. **Water-Reflected Sphere**
   - Core + water reflector
   - Use case: Reflected assemblies, reactors

3. **Multi-Region Assembly**
   - Fuel + moderator + reflector
   - Use case: Realistic reactor configurations

**KCODE Parameters:**

```
KCODE  nsrck  rkk  ikz  kct
       5000   1.0  50   150
```

- **nsrck**: Histories per cycle (5,000 - 50,000 typical)
- **rkk**: Initial k-eff guess (1.0 usually fine)
- **ikz**: Skip cycles (50-100 for convergence)
- **kct**: Total cycles (150-500 for statistics)

**KSRC Options:**

- Single point: `KSRC 0 0 0`
- Multiple points: `KSRC 0 0 0  5 0 0  -5 0 0`
- Grid: Use KSRC with many points distributed in fuel

**KOPTS Advanced Options:**

- `KINETICS=yes`: Point kinetics parameters
- `PRECURSOR=yes`: Delayed neutron precursors
- `FMESH=101`: Use mesh tally for source convergence

**Modification Tips:**
- Adjust fuel enrichment in M1 card
- Change geometry dimensions (surface card radii)
- Increase cycles for better statistics (kct)
- Add more KSRC points for complex geometries
- Monitor entropy (H) for source convergence

---

### 4. surface_source_templates.i

**Purpose:** Two-stage calculations using surface source write/read

**When to Use:**
- Deep penetration shielding (separate shield and detector)
- Variance reduction (run source-to-surface, then surface-to-detector)
- Portability (share surface source between users)

**Workflow:**

**Stage 1 (Write):**
1. Run with `SSW 1` to write surface crossings
2. MCNP creates `WSSA` file (ASCII) or `WSSB` (binary)
3. Rename to `RSSA` or `RSSB` for stage 2

**Stage 2 (Read):**
1. Modify geometry (downstream side of surface)
2. Use `SSR 1 NPS=50000` to read particles
3. Run with new geometry, tallies downstream

**Templates Included:**

1. **Basic SSW** - Write forward crossings
2. **SSW Both Directions** - Write all crossings
3. **Basic SSR** - Read and sample from surface
4. **SSR with Options** - TR, COL keywords
5. **SSR Spherically Symmetric** - For spherical problems

**Modification Tips:**
- Surface number in SSR must match SSW
- NPS in SSR determines sampling (can be > or < stage 1 NPS)
- Use `SSW -n` to write both forward and backward crossings
- `TR=n` applies transformation to source particles
- `COL=1` forces first collision (variance reduction)

**Common Pitfall:**
- Surface source must be on geometry boundary
- Must have particles crossing surface in stage 1
- WSSA files can be large (GB for many crossings)

---

## 🔧 MCNP Format Requirements

**CRITICAL:** All template files follow MCNP format rules:

- **EXACTLY 2 blank lines** in complete input files:
  - One blank line after cell cards
  - One blank line after surface cards
- **NO blank lines** within any block (cells, surfaces, data)
- Comments (`c`) for readability, never blank lines

**Verification Before Running:**
```bash
grep -c "^$" my_input.i
# Should return: 2
```

---

## 🎓 Integration with Scripts

Use automation scripts in `scripts/` directory:

```bash
# Visualize spectrum before running
python ../scripts/source_spectrum_plotter.py --type watt --param1 0.988 --param2 2.249

# Validate source definition
python ../scripts/source_validator.py my_problem.i
```

---

## 📚 References

- MCNP Manual Chapter 5.08: Source Data Cards
- `../source_distribution_reference.md` - Complete SI/SP options
- `../advanced_source_topics.md` - DS, TR, CCC, spontaneous fission
- `../source_error_catalog.md` - Common mistakes

---

## 🔗 Related Skills

- **mcnp-input-builder**: Overall input structure
- **mcnp-geometry-builder**: Cell and surface definitions
- **mcnp-tally-builder**: Coupling sources with tallies
- **mcnp-variance-reducer**: Source biasing (SB cards)

---

**Created:** 2025-11-03
**Author:** Claude (Anthropic)
**Skill:** mcnp-source-builder v2.0

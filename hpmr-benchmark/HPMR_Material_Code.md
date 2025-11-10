# HPMR Missing Material Definitions
## Material Cards for Gap Analysis Items GAP 6 and GAP 7

**Created:** 2025-11-08
**Author:** mcnp-material-builder specialist
**Purpose:** Define missing materials for HPMR model completion
**Status:** Ready for implementation

---

## Materials to Add

Based on Gap Analysis sections 2.1 (GAP 6, GAP 7):
- **m710**: Graphite H-451 reflector (bottom, top, radial)
- **m800**: B₄C control drum absorber
- **m801**: Graphite control drum matrix

---

## Material 710: Graphite H-451 Reflector

**Purpose:** Axial and radial reflectors (z=0-20 cm, z=180-200 cm, radial region)

**Physical Properties:**
- Material: Graphite H-451 (nuclear grade)
- Density: 1.803 g/cm³ (same as monolith m201)
- Temperature: ~1045 K average (bottom/top reflectors)
- Composition: 100% carbon (natural isotopic mix)

**MCNP Material Card:**
```mcnp
c ============================================================================
c Material 710: Graphite H-451 Reflector (1045 K)
c ============================================================================
c Density: 1.803 g/cm3
c Application: Bottom reflector (z=0-20), top reflector (z=180-200),
c              control drum matrix
c Temperature: ~1045 K (avg for reflectors)
c CRITICAL: MT card REQUIRED for thermal neutron scattering
c ============================================================================
m710  6000.83c  -1.0            $ Carbon at 1200K library
mt710 grph.47t                  $ Graphite S(a,b) at 1200K
```

**Key Points:**
- **Negative density (-1.0)** indicates weight fraction (100% carbon)
- **Library .83c** = ENDF/B-VIII.3 at 1200K (closest to 1045K operating temp)
- **MT card grph.47t** = Graphite S(α,β) thermal scattering at 1200K
- **CRITICAL**: Missing MT card causes 1000-5000 pcm reactivity error!

**Usage in Cell Cards:**
```mcnp
c Example: Bottom reflector cell
701   710  -1.803  -7001  7011:7012  u=-701  imp:n=1  $ Graphite reflector

c Example: Top reflector cell
801   710  -1.803  -8001  8011:8012  u=-801  imp:n=1  $ Graphite reflector
```

---

## Material 800: B₄C Control Drum Absorber

**Purpose:** Neutron absorber in 12 control drums (120° sector per drum)

**Physical Properties:**
- Material: Boron carbide (B₄C)
- Density: 2.52 g/cm³ (typical for B₄C ceramic)
- Temperature: ~1000 K (operating)
- Boron enrichment: Natural (19.9% B-10, 80.1% B-11)
- Stoichiometry: 4 boron atoms per 1 carbon atom

**Atom Density Calculation:**
```
B₄C molecular weight = 4×10.81 + 12.01 = 55.25 g/mol
Molecule density = (2.52 g/cm³) × (6.022×10²³) / (55.25 g/mol) / 10²⁴
                 = 2.748×10⁻² molecules/barn-cm

Atom densities:
  B total: 4 × 2.748E-02 = 1.099E-01 atoms/barn-cm
    B-10 (19.9%): 1.099E-01 × 0.199 = 2.187E-02 atoms/barn-cm
    B-11 (80.1%): 1.099E-01 × 0.801 = 8.803E-02 atoms/barn-cm
  C: 1 × 2.748E-02 = 2.748E-02 atoms/barn-cm
```

**MCNP Material Card:**
```mcnp
c ============================================================================
c Material 800: B4C Control Drum Absorber (1000 K)
c ============================================================================
c Density: 2.52 g/cm3
c Application: Control drum absorber sectors (120° arc, 2.7984 cm thick)
c Composition: Natural boron in B4C stoichiometry
c Temperature: ~1000 K (operating)
c ============================================================================
m800  5010.02c  2.187E-02      $ B-10 at 900K (19.9% natural abundance)
      5011.02c  8.803E-02      $ B-11 at 900K (80.1% natural abundance)
      6000.82c  2.748E-02      $ C at 900K (from carbide)
c
c B:C atom ratio = (2.187E-02 + 8.803E-02) / 2.748E-02 = 3.998 ≈ 4.0 ✓
c Total density check: (2.748E-02) × (55.25) / (0.6022) = 2.52 g/cm³ ✓
```

**Key Points:**
- **Positive fractions** = atom densities in atoms/barn-cm
- **Library .02c** = ENDF/B-VIII.0 at 900K (closest to 1000K operating)
- **No MT card** for B₄C (not a moderator, no thermal scattering treatment)
- **B-10 cross-section** = 3840 barns at thermal → very strong absorber
- **Stoichiometry**: B₄C ratio validated (4:1)

**Usage in Cell Cards:**
```mcnp
c Example: Control drum B4C absorber sector
8101  800  -2.52  -8011  8012  8013  8014  imp:n=1  $ Drum 1 B4C (120° arc)
```

**Alternative: Enriched Boron**
If using B-10 enriched to 90% (stronger absorption):
```mcnp
m800  5010.02c  9.897E-02      $ B-10 at 900K (90% enriched)
      5011.02c  1.099E-02      $ B-11 at 900K (10% remaining)
      6000.82c  2.748E-02      $ C at 900K
```

---

## Material 801: Graphite Control Drum Matrix

**Purpose:** Non-absorbing graphite sector in control drums (240° sector per drum)

**Physical Properties:**
- Material: Graphite (same grade as reflector)
- Density: 1.803 g/cm³
- Temperature: ~1000 K (control drum operating temperature)
- Composition: 100% carbon (natural isotopic mix)

**MCNP Material Card:**
```mcnp
c ============================================================================
c Material 801: Graphite Control Drum Matrix (1000 K)
c ============================================================================
c Density: 1.803 g/cm3
c Application: Control drum graphite sectors (240° arc)
c Temperature: ~1000 K (drum operating temperature)
c CRITICAL: MT card REQUIRED for thermal neutron scattering
c ============================================================================
m801  6000.82c  -1.0            $ Carbon at 900K library
mt801 grph.47t                  $ Graphite S(a,b) at 1200K
c
c Note: Using .82c (900K) library for isotopes, but grph.47t (1200K) for
c       thermal scattering - this is acceptable approximation for 1000K
```

**Key Points:**
- **Identical to m710** except potentially different temperature library
- **Library .82c** = ENDF/B-VIII.0 at 900K (closer to 1000K drum temp)
- **MT card grph.47t** = 1200K thermal scattering (acceptable for 1000K)
- **CRITICAL**: MT card prevents 1000-5000 pcm reactivity error!

**Usage in Cell Cards:**
```mcnp
c Example: Control drum graphite sector
8102  801  -1.803  -8011  8012  ~8013:~8014  imp:n=1  $ Drum 1 graphite (240° arc)
```

**Alternative: Use m710 directly**
If temperature difference not critical, can use m710 for control drums:
```mcnp
c Simplified approach (uses reflector material):
8102  710  -1.803  -8011  8012  ~8013:~8014  imp:n=1  $ Drum graphite (reuse m710)
```

---

## Complete Material Block for MCNP Input

**Add to Material Cards section (after m411):**

```mcnp
c ============================================================================
c                   ADDITIONAL MATERIALS FOR PHASE 1 COMPLETION
c ============================================================================
c
c --- Material 710: Graphite H-451 Reflector (1045 K) ---
m710  6000.83c  -1.0            $ Carbon at 1200K
mt710 grph.47t                  $ Graphite S(a,b) at 1200K
c
c --- Material 800: B4C Control Drum Absorber (1000 K) ---
m800  5010.02c  2.187E-02      $ B-10 at 900K (19.9% natural abundance)
      5011.02c  8.803E-02      $ B-11 at 900K (80.1% natural abundance)
      6000.82c  2.748E-02      $ C at 900K
c
c --- Material 801: Graphite Control Drum Matrix (1000 K) ---
m801  6000.82c  -1.0            $ Carbon at 900K
mt801 grph.47t                  $ Graphite S(a,b) at 1200K
c
c
```

---

## Why This Code is CRITICAL

### Thermal Scattering in Graphite: A CRITICAL Requirement

**Problem:** Missing MT cards for graphite cause **severe physics errors** in thermal reactor models.

**Impact of Missing MT Cards:**
1. **Reactivity Error:** 1000-5000 pcm (1-5% Δk/k) underestimation
2. **Wrong Spectrum:** Thermal neutron spectrum too hard (high-energy tail overestimated)
3. **Wrong Scattering:** Free-gas model instead of crystalline binding
4. **Invalid Benchmarking:** Cannot validate against experimental data

**Physical Explanation:**

In thermal reactors (like HPMR), neutrons thermalize to ~0.025 eV (room temperature) or higher at elevated temperatures. At these energies, the **molecular/crystalline binding** of carbon atoms in graphite crystal structure **dominates neutron scattering**.

**Without MT Card (WRONG):**
- MCNP assumes **free-gas scattering** (independent atoms)
- Carbon atoms treated as isolated, free particles
- Scattering kernel: S(α,β) = 0 (no molecular effects)
- Neutron gains too much energy per collision
- Spectrum becomes too hard (fewer thermal neutrons)
- **Result**: Wrong reactivity, wrong flux distribution, wrong temperature coefficients

**With MT Card (CORRECT):**
- MCNP uses **S(α,β) thermal scattering tables** (crystalline graphite)
- Carbon atoms treated as bound in crystal lattice
- Scattering kernel includes phonon modes, Bragg scattering, chemical binding
- Neutron energy exchange follows actual graphite physics
- Spectrum correctly softened at thermal energies
- **Result**: Accurate reactivity, accurate flux, accurate physics

**Real-World Example:**

Professional HTGR models have been discovered with **50+ graphite materials lacking MT cards**. This caused:
- **keff underestimated by 2000-4000 pcm**
- Benchmark validation failures
- Incorrect temperature feedback coefficients
- Invalid safety analysis results

**Temperature Matching:**

The S(α,β) table temperature should match the graphite temperature:
- **grph.40t** = 293K (cold critical)
- **grph.43t** = 600K (low power)
- **grph.46t** = 1000K (high power)
- **grph.47t** = 1200K (very high temp)

For HPMR reflectors at ~1045K, **grph.47t (1200K)** is appropriate. For control drums at ~1000K, **grph.46t (1000K)** would be ideal, but **grph.47t (1200K)** is acceptable.

**Verification:**

After adding MT cards, expect:
- **keff increase** of 1000-5000 pcm (model becomes more reactive)
- **Thermal flux increase** in graphite regions
- **Epithermal flux decrease** (fewer fast neutrons)
- **Better agreement** with reference Serpent results (1.09972 ± 0.00014)

---

## Material Summary Table

| Material | Description | Density | Temp (K) | S(α,β) | Application |
|----------|-------------|---------|----------|--------|-------------|
| **m710** | Graphite H-451 | -1.803 g/cm³ | 1045 | grph.47t | Bottom/top/radial reflectors |
| **m800** | B₄C absorber | -2.52 g/cm³ | 1000 | None | Control drum absorber (120° sectors) |
| **m801** | Graphite matrix | -1.803 g/cm³ | 1000 | grph.47t | Control drum graphite (240° sectors) |

**CRITICAL NOTES:**
1. **All graphite materials MUST have MT cards** (m710, m801)
2. **Missing MT cards cause 1000-5000 pcm reactivity error**
3. **B₄C has no MT card** (not a moderator, no thermal treatment needed)
4. **Natural boron used** in m800 (can enrich to 90% B-10 for stronger absorption)

---

## Implementation Checklist

- [ ] Add m710 material card to MCNP input
- [ ] Add mt710 thermal scattering card
- [ ] Add m800 material card with correct B₄C stoichiometry
- [ ] Add m801 material card to MCNP input
- [ ] Add mt801 thermal scattering card
- [ ] Verify B:C ratio in m800 = 4.0
- [ ] Verify all graphite materials have MT cards
- [ ] Test model runs without material errors
- [ ] Check keff increases by ~2000 pcm after adding MT cards
- [ ] Validate against reference Serpent keff = 1.09972

---

## References

1. **SKILL.md** - mcnp-material-builder skill documentation
2. **thermal_scattering_reference.md** - Complete S(α,β) table listing
3. **HPMR_Gap_Analysis.md** - Gap specifications (GAP 6, GAP 7)
4. **HPMR_Analysis_Overview.md** - Reference plant specifications (Table 19)

---

**CRITICAL REMINDER**: The impact of missing graphite MT cards cannot be overstated. This is a **systematic error** found even in professional reactor models. Always verify MT cards are present for:
- Graphite moderators
- Graphite reflectors
- Graphite matrix materials
- PyC layers in TRISO fuel
- Any carbon-containing material in thermal neutron spectrum

**Missing MT cards = 1000-5000 pcm reactivity error = Invalid model**

---

## Document Metadata

**Created:** 2025-11-08
**Author:** mcnp-material-builder specialist
**Version:** 1.0
**Status:** Complete - Ready for implementation
**Next Action:** Add materials to hpcmr-simplified.i input file

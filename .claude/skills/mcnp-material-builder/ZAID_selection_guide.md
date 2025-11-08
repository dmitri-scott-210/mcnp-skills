# ZAID Library Selection Guide
## Complete Decision Tree for Cross-Section Library Extensions

**Purpose**: Help users choose the correct .nnX extension for ZAIDs
**Scope**: When to use .80c vs .70c vs .60c vs .00c, isotopic vs natural elements

---

## ZAID FORMAT REVIEW

```
ZZZAAA.nnX

ZZZ:    Atomic number (Z) - 001 to 098
AAA:    Mass number (A) - 000 for natural element, specific for isotope
nn:     Library identifier (00-99)
X:      Particle/physics type (c=continuous-energy neutron, most common)
```

**Examples**:
- `92235.80c` = U-235, ENDF/B-VIII.0, continuous-energy neutrons
- `6000.70c` = Natural carbon, ENDF/B-VII.0, continuous-energy neutrons
- `1001.80c` = H-1, ENDF/B-VIII.0, continuous-energy neutrons

---

## LIBRARY EXTENSIONS (nn)

### Modern Libraries (Preferred)

| Extension | ENDF Version | Status | When to Use |
|-----------|--------------|--------|-------------|
| **.80c** | ENDF/B-VIII.0 | Latest (2018+) | **Preferred** for new models if available |
| **.70c** | ENDF/B-VII.0 | Standard (2006) | **Default** for most applications |
| **.71c** | ENDF/B-VII.1 | Updated (2011) | Alternative to .70c, minor updates |

### Legacy Libraries (Use if Required)

| Extension | ENDF Version | When to Use |
|-----------|--------------|-------------|
| **.60c** | ENDF/B-VI.8 | Natural elements if .70c unavailable |
| **.50c** | ENDF/B-V | Structural materials (legacy models) |
| **.00c** | ENDF/B-VI.0 or earlier | Benchmark reproduction only |

### Special Libraries

| Extension | Purpose | Example Use |
|-----------|---------|-------------|
| **.20c** | B-10 optimized thermal | Burnable poison, control rods |
| **.55c** | W special evaluation | Tungsten shielding |
| **.31c** | JEFF-3.1 European library | European benchmark validation |

---

## DECISION TREE

### Step 1: New Model or Benchmark Validation?

```
Are you reproducing a published benchmark?
  ├─→ YES: Use EXACT library specified in benchmark documentation
  │         Example: AGR-1 benchmark specifies .00c for graphite
  └─→ NO: Continue to Step 2
```

### Step 2: Library Availability

```
Check xsdir for availability:
  grep "92235" $DATAPATH/xsdir

Is .80c available for your isotope?
  ├─→ YES: Use .80c (latest data)
  └─→ NO: Is .70c available?
           ├─→ YES: Use .70c (standard)
           └─→ NO: Use .60c or consult mcnp-cross-section-manager
```

### Step 3: Isotopic vs Natural Element

```
Does isotopic composition matter for physics?
  ├─→ YES (actinides, absorbers, fission products):
  │    Use specific isotope: 92235.80c, 54135.70c, 62149.70c
  │
  └─→ NO (structural materials, low-importance):
       Use natural element: 26000.70c (Fe-nat), 24000.70c (Cr-nat)
```

**When isotopic detail MATTERS**:
- ✅ Actinides (U, Pu, Np, Am, Cm): ALWAYS isotopic
- ✅ Fission products: Individual isotopes (Xe-135, Sm-149, Gd-157)
- ✅ Carbon in HTGR: C-12 and C-13 for accuracy
- ✅ Boron: B-10 and B-11 for control/burnable poison
- ✅ Silicon in SiC: Si-28/29/30 for TRISO coating
- ✅ Lithium: Li-6 and Li-7 for tritium breeding

**When natural element OK**:
- ✅ Structural steel: Fe, Cr, Ni, Mn (unless activation study)
- ✅ Concrete: Ca, Si, Al (bulk composition)
- ✅ Coolant impurities: Trace elements
- ✅ Shielding: Pb, W (unless detailed gamma transport)

### Step 4: Consistency Check

```
All materials using same library version?
  ├─→ YES: Proceed
  └─→ NO: Mix only if necessary (e.g., special B-10 evaluation)
           Document reason in comments
```

---

## LIBRARY SELECTION BY APPLICATION

### 1. Light Water Reactors (PWR/BWR)

**Standard approach**:
```mcnp
c UO2 fuel
M1   92235.80c  0.045    $ ENDF/B-VIII.0 (preferred)
     92238.80c  0.955
      8016.80c  2.0

c Zircaloy clad
M2   40000.70c  1.0      $ Natural Zr, ENDF/B-VII.0 (widely available)

c Water
M3    1001.80c  2        $ H-1, ENDF/B-VIII.0
      8016.80c  1
MT3  H-H2O.40t

c Stainless steel
M4   26000.70c  -0.70    $ Natural elements for structure
     24000.70c  -0.19
     28000.70c  -0.11
```

**Why**:
- Actinides: Latest evaluations (.80c) for best accuracy
- Zr: .70c widely available, .80c if you have it
- Structure: Natural elements sufficient, .70c standard
- Consistency: Mostly .80c, acceptable to mix .70c for unavailable isotopes

### 2. High-Temperature Gas Reactors (HTGR)

**Observed in AGR-1 benchmark**:
```mcnp
c UCO fuel kernel
M10  92235.00c  0.1996   $ ENDF/B-VI.0 (benchmark specified .00c)
     92238.00c  0.7968
      6012.00c  0.3217
      8016.00c  1.3613

c Graphite (CRITICAL: needs MT card!)
M11   6012.00c  0.9890   $ .00c for AGR-1 benchmark
      6013.00c  0.0110
MT11  C-GRPH.43t          $ 600 K thermal scattering

c SS316L structure
M12  26056.00c  -0.6041  $ Isotopic Fe, .00c for benchmark
     24052.00c  -0.1426  $ Isotopic Cr
     28058.00c  -0.0805  $ Isotopic Ni
```

**Why**:
- Benchmark validation: Must use .00c to reproduce published results
- New HTGR model: Use .80c or .70c instead

**For new HTGR models (not benchmark)**:
```mcnp
M10  92235.80c  0.1975   $ Use .80c for new designs
     92238.80c  0.8025
      6012.80c  0.9890   $ C-12 with latest evaluation
      6013.80c  0.0110
      8016.80c  2.0
```

### 3. Fast Reactors (Metallic or MOX Fuel)

**Standard approach**:
```mcnp
c U-Pu-Zr metallic fuel
M20  92238.80c  -0.686
     94239.80c  -0.120
     94240.80c  -0.050
     40000.70c  -0.100   $ Zr: .70c widely available

c SS316 clad (isotopic for activation)
M21  26054.70c  -0.038
     26056.70c  -0.604
     26057.70c  -0.013
     24050.70c  -0.007
     24052.70c  -0.143
     28058.70c  -0.081
```

**Why**:
- Actinides: .80c for best resonance data in fast spectrum
- Zr: Natural element, .70c or .60c
- Structure: Isotopic if activation calculation, .70c standard

### 4. Research Reactors (MTR-Type)

**U-Al dispersion**:
```mcnp
M30  92235.70c  -0.089   $ LEU fuel
     92238.70c  -0.361
     13027.70c  -0.550   $ Al-27
```

**Why**:
- .70c standard for research reactors
- .80c if available and consistent
- Older facilities may have .50c or .60c legacy data

---

## MIXING LIBRARY VERSIONS

### When Mixing is Acceptable

✅ **Special evaluations for specific isotopes**:
```mcnp
M1    5010.20c  ...      $ B-10 special thermal evaluation
      5011.70c  ...      $ B-11 standard ENDF/B-VII.0
      6000.70c  ...      $ C-nat standard
```
**Reason**: B-10 .20c library optimized for thermal neutron absorption

✅ **Unavailable isotope in standard library**:
```mcnp
M2   92235.80c  ...      $ U-235 ENDF/B-VIII.0
     92238.80c  ...      $ U-238 ENDF/B-VIII.0
     40000.70c  ...      $ Zr-nat only in .70c, not .80c
```
**Reason**: Natural Zr not in ENDF/B-VIII.0, use .70c

### When Mixing is WRONG

❌ **Inconsistent for no reason**:
```mcnp
M3   92235.80c  ...      $ BAD: mixing .80c and .70c for same element type
     92238.70c  ...      $ Should be 92238.80c
      8016.70c  ...      $ Should be 8016.80c
```

❌ **Benchmark validation with wrong library**:
```mcnp
c AGR-1 benchmark specifies .00c for graphite
M4   6012.70c  ...       $ WRONG: should be 6012.00c per benchmark spec
     6013.70c  ...
```

---

## LIBRARY VERSION HISTORY

### ENDF/B-VIII.0 (.80c) - 2018

**Major improvements**:
- Updated U-235, U-238 resonances (better reactivity predictions)
- Improved fission product data (Xe, Sm, Gd)
- Better thermal scattering (water, graphite)
- Pu-239, Pu-240, Pu-241 evaluations updated

**Use for**: New reactor designs, modern calculations

### ENDF/B-VII.0 (.70c) - 2006

**Standard for 15+ years**:
- Widely validated
- Available for most isotopes
- Default in many MCNP installations

**Use for**: General-purpose calculations, broad availability

### ENDF/B-VI.8 (.60c) - 2001

**Legacy**:
- Natural elements (Mg, Si, Ti, Zr, Mo)
- Some benchmarks specify .60c

**Use for**: Natural element backups, benchmark reproduction

### ENDF/B-VI.0 (.00c) - 1990

**Old but sometimes required**:
- Some benchmarks (AGR-1) specify .00c
- Legacy models

**Use for**: Benchmark validation ONLY

---

## VERIFICATION

### Check xsdir for Availability

```bash
# Check if isotope available in specific library
grep "92235.80c" $DATAPATH/xsdir

# Check all available versions of U-235
grep "92235" $DATAPATH/xsdir

# Check natural element
grep "40000" $DATAPATH/xsdir
```

**Interpretation**:
```
92235.80c   237.048080  endf80sab  ...   <- ENDF/B-VIII.0 available
92235.70c   235.043924  endf70sab  ...   <- ENDF/B-VII.0 available
92235.60c   235.043924  endf60sab  ...   <- ENDF/B-VI.8 available
```

### Use scripts/zaid_library_validator.py

```bash
python scripts/zaid_library_validator.py input.i
```

**Checks**:
- ✅ All ZAIDs exist in xsdir
- ✅ Library version consistency
- ✅ Flags mixed libraries (with reason if acceptable)
- ✅ Suggests alternatives if ZAID not found

---

## COMMON PATTERNS FROM PROFESSIONAL MODELS

### AGR-1 Benchmark (Mixed Libraries)

**Observations**:
```mcnp
c Actinides and oxygen: .70c (ENDF/B-VII.0)
   92235.70c, 92238.70c, 8016.70c

c Natural elements (Mg, Si, Ti, Zr, Mo): .60c (ENDF/B-VI.8)
   12000.60c, 14000.60c, 22000.60c, 40000.60c, 42000.60c

c Structural steel (Fe, Cr, Ni): .50c (ENDF/B-V)
   24000.50c, 26000.50c, 28000.50c

c AGR-specific materials: .00c (ENDF/B-VI.0)
   6012.00c, 2004.00c (for graphite, helium)

c B-10 special: .20c (optimized thermal)
   5010.20c

c Air: .80c (ENDF/B-VIII.0)
   7014.80c, 8016.80c
```

**Lesson**: Professional models mix libraries for specific reasons (benchmark specs, availability, optimization). Document reasons in comments!

---

## BEST PRACTICES

1. **Prefer latest library (.80c) for new models** unless specific reason not to
2. **Use .70c as default** if .80c not available (widely supported)
3. **Check xsdir availability** before running MCNP (use validation script)
4. **Be consistent within material type** (all actinides same library)
5. **Document exceptions** when mixing libraries (comments explaining why)
6. **For benchmarks: use EXACT library specified** in documentation
7. **Isotopic detail for physics-important nuclides** (U, Pu, FPs, absorbers)
8. **Natural elements for structural materials** (Fe, Cr, Ni) unless activation study
9. **Validate with mcnp-cross-section-manager** skill for complex cases

---

## DECISION SUMMARY FLOWCHART

```
START: Need to select ZAID library extension

├─→ Benchmark validation?
│    └─→ YES: Use library specified in benchmark → DONE
│    └─→ NO: Continue
│
├─→ Check xsdir for .80c
│    ├─→ Available: Use .80c → DONE
│    └─→ Not available: Continue
│
├─→ Check xsdir for .70c
│    ├─→ Available: Use .70c → DONE
│    └─→ Not available: Continue
│
├─→ Check xsdir for .60c
│    ├─→ Available: Use .60c (document why) → DONE
│    └─→ Not available: Consult mcnp-cross-section-manager
│
└─→ Special case (B-10, W, etc.)?
     └─→ Use special library (.20c, .55c, etc.) → DONE
```

---

## TROUBLESHOOTING

### Error: "nuclide zaid.nnx not available on any cross-section table"

**Cause**: Library extension not in xsdir

**Solution**:
1. Check xsdir: `grep "ZAID" $DATAPATH/xsdir`
2. Try alternative: .80c → .70c → .60c
3. For natural elements: ZZZAAA → ZZZ000
4. Consult mcnp-cross-section-manager skill

### Warning: "using old library .60c instead of newer .80c"

**Not an error**, but check if .80c available for better accuracy

**Action**:
- Review xsdir for .80c availability
- Update if consistent across materials
- Document reason if keeping .60c

---

## REFERENCES

**For library management**:
- mcnp-cross-section-manager skill - xsdir parsing, library installation

**For validation**:
- scripts/zaid_library_validator.py - Automated checking

**External Resources**:
- NNDC ENDF/B Library: https://www.nndc.bnl.gov/endf/
- MCNP6 Manual Section 1.2.2: Target Identifier Formats

---

**Version:** 1.0
**Created:** 2025-11-08
**For:** mcnp-material-builder skill v2.0

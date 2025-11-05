# Material Definition Error Catalog

## Purpose
Comprehensive troubleshooting guide for MCNP material-related errors, warnings, and common mistakes.

---

## Fatal Errors

### Error 1: Cross Section Not Found

**Symptom:**
```
fatal error.
    material        1 nuclide 92235 has no cross section data.
    please supply data or omit nuclide.
```

**Causes:**
1. ZAID not available in cross-section libraries (xsdir)
2. Wrong library suffix (.70c vs .80c vs .90c)
3. XSDIR file missing entry
4. Typo in ZAID specification

**Diagnosis:**
1. Check available libraries in `$DATAPATH/xsdir`
2. Search for isotope: `grep "92235" xsdir`
3. Verify library suffix matches available data

**Fix:**
```
c BAD:
M1  92235.90c  1.0                          $ .90c may not exist

c GOOD:
M1  92235.80c  1.0                          $ Use available library (.80c)
```

**Alternative Fix (Use NLIB):**
```
M1  92235  1.0  NLIB=80c                    $ Specify library explicitly
```

---

### Error 2: Material Number Mismatch

**Symptom:**
```
fatal error. cell  1  material  5  is not defined.
```

**Cause:** Cell card references material 5, but no M5 card exists.

**Diagnosis:**
- Check cell cards: `grep "^[0-9]" input.i | awk '{print $2}'` (lists material numbers)
- Check M cards: `grep "^M" input.i`

**Fix:**
```
c Cell card:
1    5  -19.1  -1  IMP:N=1                  $ References material 5

c Missing M5 card - ADD IT:
M5   92235  0.93  92238  0.07               $ Material 5 definition
```

---

### Error 3: Negative Neutron Energy

**Symptom:**
```
bad trouble in subroutine col1at of mcrun
    particle has negative energy. probable cause is use of wrong atomic weight ratio.
    nps =    1234  particle lost at cell  1
```

**Cause:** Atomic weight ratio mismatch or AWTAB error.

**Diagnosis:**
- Verify AWTAB entries against NIST/IAEA values
- Check for typos in atomic weights
- Ensure AWTAB not overriding standard data unnecessarily

**Fix:**
```
c BAD:
AWTAB  92235  200.0                         $ WRONG atomic weight!

c GOOD:
AWTAB  92235  235.0439                      $ Correct atomic weight
```

**Prevention:** Avoid AWTAB unless absolutely necessary.

---

### Error 4: S(α,β) Table Not Found

**Symptom:**
```
fatal error. s(alpha,beta) table H-H2O.99t not found in xsdir.
```

**Cause:** Specified S(α,β) table doesn't exist in library.

**Diagnosis:**
- Check available S(α,β) tables: `grep "t$" xsdir | grep H2O`
- Verify temperature code (40-49 typical range)

**Fix:**
```
c BAD:
MT1  H-H2O.99t                              $ .99t doesn't exist

c GOOD:
MT1  H-H2O.40t                              $ Use 293.6 K table (.40t)
```

**See:** `thermal_scattering_reference.md` for complete S(α,β) table listing.

---

## Warnings (Non-Fatal)

### Warning 1: Weight Fractions Don't Sum to 1

**Symptom:**
```
warning. material  1  unnormalized fractions renormalized.
```

**Cause:** Weight fractions don't sum to 1.0 (or -1.0).

**Impact:** MCNP renormalizes automatically, but indicates potential user error.

**Diagnosis:**
```python
# Check sum:
fractions = [-0.8, -0.3]  # Example
print(sum(fractions))     # Should be -1.0
```

**Fix:**
```
c BAD:
M1  7014  -0.8  8016  -0.3                  $ Sum = -1.1 (WRONG!)

c GOOD:
M1  7014  -0.7273  8016  -0.2727            $ Sum = -1.0 (normalized)
```

**Calculation:**
```
Normalize:
f₁' = f₁ / (f₁ + f₂)
f₂' = f₂ / (f₁ + f₂)

Example:
-0.8 / (-0.8 + -0.3) = -0.8 / -1.1 = 0.7273
-0.3 / (-0.8 + -0.3) = -0.3 / -1.1 = 0.2727
```

---

### Warning 2: Multiple S(α,β) Tables Affect Same Nuclide

**Symptom:**
```
warning. multiple s(alpha,beta) tables affect hydrogen in material 1.
    only the first table will be used.
```

**Cause:** Two or more S(α,β) tables target the same element.

**Example:**
```
M1   1001  2  8016  1                       $ H₂O
MT1  H-H2O.40t  H-CH2.40t                   $ CONFLICT: Both affect hydrogen!
```

**Fix (Remove conflicting table):**
```
M1   1001  2  8016  1
MT1  H-H2O.40t                              $ Only water S(α,β)
```

**Fix (Use MT0 for stochastic mixing):**
```
c If intentional (stochastic mixing):
MT0  H-H2O.40t  1001.00c                   $ Match water S(α,β) to H at 293 K
     H-H2O.54t  1001.01c                   $ Match water S(α,β) to H at 600 K

M1   1001.00c  1.0  8016.00c  0.5          $ H and O at 293 K
     1001.01c  1.0  8016.01c  0.5          $ H and O at 600 K

MT1  H-H2O.40t  H-H2O.54t                  $ Both tables used, matched by MT0
```

---

### Warning 3: Elemental Identifiers Used

**Symptom:**
```
warning. material  1  uses elemental identifier  26000.
    isotopic identifiers recommended for accuracy.
```

**Cause:** Using natural element (AAA=000) instead of specific isotopes.

**Impact:**
- Older elemental data may be less accurate
- Natural abundance assumptions may not match actual composition

**When OK:**
- Non-fissile structural materials (Fe, Pb)
- Elements with stable natural composition

**When NOT OK:**
- Fissile materials (U, Pu)
- Materials requiring isotopic detail

**Fix (if needed):**
```
c ELEMENTAL (less accurate):
M1   26000  1.0                             $ Fe-natural

c ISOTOPIC (more accurate):
M1   26054  0.0585  26056  0.9175  26057  0.0212  26058  0.0028    $ Fe isotopes
```

---

## Physical Inconsistencies

### Error 5: Density Sign Mismatch

**Symptom:** Unusual tally results, incorrect reaction rates, physics warnings.

**Cause:** Atomic fractions with positive density (or vice versa).

**Diagnosis:**
- Check M card: positive fractions = atomic, negative fractions = weight
- Check cell card: negative density = atomic, positive density = mass

**Fix:**
```
c BAD (Atomic fractions + positive density):
M1  1001  2  8016  1                        $ Atomic fractions
1   1  1.0  -1  IMP:N=1                     $ Positive density (WRONG!)

c GOOD (Atomic fractions + negative density):
M1  1001  2  8016  1
1   1  -0.1003  -1  IMP:N=1                 $ Negative density (correct)
```

**Verification:**
- Atomic fractions: `ρ_cell < 0` (atoms/b-cm)
- Weight fractions: `ρ_cell > 0` (g/cm³)

---

### Error 6: Temperature Mismatch (TMP vs MT)

**Symptom:** Inaccurate thermal neutron flux, keff drift, physics warnings.

**Cause:** MT table temperature doesn't match TMP card temperature.

**Diagnosis:**
- Compare MT table temperature code to TMP value
- Use: `T[K] = T[MeV] / 8.617×10⁻¹¹`

**Fix:**
```
c BAD (Inconsistent temperatures):
M1  1001  2  8016  1
MT1  H-H2O.40t                              $ S(α,β) at 293.6 K
1   1  -0.08  -1  TMP=5.17e-8  IMP:N=1     $ Cell at 600 K (MISMATCH!)

c GOOD (Consistent):
M1  1001  2  8016  1
MT1  H-H2O.43t                              $ S(α,β) at 600 K
1   1  -0.08  -1  TMP=5.17e-8  IMP:N=1     $ Cell at 600 K (matches)
```

---

### Error 7: Missing MT Card for Moderator

**Symptom:** Inaccurate criticality (keff), thermal flux distribution incorrect.

**Cause:** Water/graphite/polyethylene defined without S(α,β).

**Impact:**
- Thermal neutron scattering treated as free gas
- Criticality calculations incorrect (typically overestimate keff)
- Thermal flux spectrum wrong

**Diagnosis:**
- Check if material contains H, D, C, Be
- Check if thermal neutrons significant (E < 1 eV)
- Verify MT card exists for moderator materials

**Fix:**
```
c BAD (Water without S(α,β)):
M1  1001  2  8016  1                        $ H₂O defined
c NO MT CARD! → Free-gas scattering (WRONG!)

c GOOD (Water with S(α,β)):
M1  1001  2  8016  1
MT1  H-H2O.40t                              $ Thermal scattering included
```

---

## Troubleshooting Decision Tree

```
Material Error?
  |
  +--[Fatal: Cross section not found]-------> Check xsdir, verify ZAID suffix
  |
  +--[Fatal: Material not defined]----------> Add missing M card
  |
  +--[Fatal: Negative neutron energy]--------> Check AWTAB, verify atomic weights
  |
  +--[Fatal: S(α,β) not found]---------------> Check table name, use correct temp code
  |
  +--[Warning: Fractions renormalized]-------> Sum fractions to 1.0 or -1.0
  |
  +--[Warning: Multiple S(α,β) tables]-------> Remove conflict or use MT0
  |
  +--[Warning: Elemental ID used]------------> Consider isotopic specification
  |
  +--[Physics: Incorrect keff]---------------> Check MT card for moderators
  |
  +--[Physics: Wrong thermal flux]-----------> Verify TMP matches MT temperature
  |
  +--[Physics: Unusual reaction rates]-------> Check density sign matches fractions
```

---

## Common User Mistakes

### Mistake 1: Mixing Atomic and Weight Fractions
```
c WRONG:
M1  1001  2  8016  -0.8881                  $ Mixed! (atomic + weight)

c CORRECT (Pick one):
M1  1001  2  8016  1                        $ All atomic
M1  1001  -0.1119  8016  -0.8881            $ All weight
```

### Mistake 2: Forgetting Negative Sign for Atomic Density
```
c WRONG:
M1  1001  2  8016  1
1   1  0.1003  -1  IMP:N=1                  $ Positive (interprets as mass!)

c CORRECT:
1   1  -0.1003  -1  IMP:N=1                 $ Negative (atomic)
```

### Mistake 3: Using Old Library (.50c, .60c) Without Verification
```
c QUESTIONABLE:
M1  1001.50c  2  8016.50c  1                $ ENDF/B-V (very old!)

c RECOMMENDED:
M1  1001.80c  2  8016.80c  1                $ ENDF/B-VIII.0 (latest)
```

**Reason:** Older libraries may have less accurate data or lack evaluations for new isotopes.

### Mistake 4: No S(α,β) for Graphite-Moderated Reactor
```
c WRONG:
M1  6000  1.0                               $ Graphite, no S(α,β)
c → Free-gas scattering (physically incorrect)

c CORRECT:
M1  6000  1.0
MT1  C-GRPH.46t                             $ S(α,β) at 1000 K
```

### Mistake 5: NONU with KCODE
```
c WRONG:
KCODE  10000  1.0  50  150
NONU                                        $ Disables fission → no criticality!

c CORRECT:
KCODE  10000  1.0  50  150
c NO NONU card → fission enabled for criticality
```

---

## Verification Checklist

Before running MCNP, verify:

- [ ] **Material numbers match:** Cell m = M card number
- [ ] **Density convention:** Atomic fractions → negative density, weight fractions → positive density
- [ ] **Fractions sum:** Weight fractions sum to -1.0 (or normalized)
- [ ] **Library availability:** All ZAIDs exist in xsdir
- [ ] **S(α,β) for moderators:** MT card for H₂O, D₂O, graphite, polyethylene, Be
- [ ] **Temperature consistency:** MT table temp = TMP card temp
- [ ] **No mixing:** All fractions atomic OR all weight (not mixed)
- [ ] **No NONU with KCODE:** NONU only for fixed-source problems

---

## See Also

- **Material Specifications:** `material_card_specifications.md` for M card syntax
- **Thermal Scattering:** `thermal_scattering_reference.md` for MT, MT0 troubleshooting
- **Advanced Cards:** `advanced_material_cards.md` for OTFDB, NONU, AWTAB errors
- **MCNP Documentation:** Chapter 5.6 (Material Data Cards)

---

**Version:** 1.0
**Created:** 2025-11-03
**For:** mcnp-material-builder skill v2.0

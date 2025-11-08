# Source Error Catalog

Common MCNP source specification errors, causes, and solutions.

---

## Error 1: Fatal - "no source particles started"

**MCNP Output:** `fatal error.  no source particles started.`

**Causes:**
- Source position outside all cells (in void or zero-importance region)
- All source particles rejected by CEL or CCC rejection
- KSRC points all in void or zero-importance cells

**Solutions:**
1. **Check source position:**
   ```
   SDEF POS=0 0 0            $ Is (0,0,0) actually inside a cell?
   ```
   Run with `VOID` card to see all cells, verify position is in geometry.

2. **Check cell/importance:**
   - Ensure source cell has IMP:N > 0 (or IMP:P, IMP:E for photons/electrons)
   - KSRC points must be in fissile cells, away from boundaries

3. **Check rejection efficiency:**
   - If CEL=D1 with narrow SI1/SP1 but broad POS distribution → High rejection
   - Add `EFF=0.001` to catch rejection problems earlier

---

## Error 2: "SP card first entry must be zero"

**MCNP Output:** `bad trouble in subroutine rdist ... sp card first entry must be zero`

**Cause:** For SI H (histogram) option, SP first entry must be 0.

**Wrong:**
```
SI1  H  0 1 5 10
SP1     0.2 0.3 0.3 0.2      $ ERROR: First entry should be 0
```

**Correct:**
```
SI1  H  0 1 5 10
SP1     0 0.3 0.3 0.4        $ First entry = 0, then bin probabilities
```

**Note:** This does NOT apply to SI L (list) or SI A (arbitrary) options.

---

## Error 3: Distribution not normalized

**MCNP Output:** `warning.  distribution n not normalized. renormalized from X to 1.0`

**Cause:** SP probabilities don't sum to 1.0 (not fatal - MCNP renormalizes).

**Example:**
```
SI1  L  1 2 3 4 5
SP1     0.1 0.2 0.3 0.4 0.5   $ Sums to 1.5
```

**Solutions:**
1. **Ignore if intentional** (MCNP automatically normalizes)
2. **Fix if error:**
   ```
   SP1     0.067 0.133 0.2 0.267 0.333   $ Sums to 1.0
   ```

**Check:** Large renormalization (e.g., 100→1.0) indicates likely input error.

---

## Error 4: "distribution m referenced but not supplied"

**MCNP Output:** `fatal error. distribution m referenced but not supplied.`

**Cause:** SDEF or DS card references distribution Dm but no SIm card exists.

**Wrong:**
```
SDEF CEL=D1 ERG=FCEL=D2
SI1  L  1 2 3
SP1     0.33 0.33 0.34
$ Missing: SI2/DS2 cards
```

**Correct:**
```
SDEF CEL=D1 ERG=FCEL=D2
SI1  L  1 2 3
SP1     0.33 0.33 0.34
DS2  S  10 20 30              $ Now D2 is defined
SI10 L  14.1
...
```

---

## Error 5: "kcode and sdef both specified"

**MCNP Output:** `warning. both kcode and sdef are present. kcode used.`

**Cause:** Both KCODE and SDEF cards in same input (KCODE takes precedence).

**Solutions:**
1. **For criticality:** Remove SDEF, keep KCODE+KSRC or SRCTP
2. **For fixed source:** Remove KCODE, keep SDEF

**Exception:** SDEF can define initial source for KCODE (CEL, POS, RAD, EXT only). SDEF energy/direction ignored.

---

## Error 6: Embedded distribution doesn't start at zero

**MCNP Output:** `fatal error.  embedded distribution nn does not start at zero.`

**Cause:** Using (D11 < D12 < D13) but SI11 or SI12 doesn't start at 0.

**Wrong:**
```
SDEF TME=(D1 < D2)
SI1  H  1 10                  $ ERROR: Should start at 0
SP1     0 1
SI2  H  0 1000
SP2     0 1
```

**Correct:**
```
SDEF TME=(D1 < D2)
SI1  H  0 10                  $ Starts at 0
SP1     0 1
SI2  H  0 1000
SP2     0 1
```

---

## Error 7: "spontaneous fission impossible"

**MCNP Output:** `bad trouble. spontaneous fission impossible.`

**Cause:** PAR=SF specified but source cell contains no spontaneous fission nuclides.

**Available SF nuclides:** Th-232, U-232/233/234/235/236/238, Np-237, Pu-238/239/240/241/242, Am-241, Cm-242/244, Bk-249, Cf-252

**Solutions:**
1. **Check material:** Ensure cell has M card with at least one SF nuclide
2. **Check ZAID:** Verify isotope is in above list (e.g., Pu-239 yes, Pu-244 no)
3. **Use SDEF PAR=N ERG=D1 / SP1 -3 a b** for fission spectrum without SF physics

---

## Error 8: Source on surface boundary causes lost particles

**MCNP Output:** `lost particle` warnings, particles near surface

**Cause:** Degenerate volume source (disk, line) positioned exactly on geometry surface.

**Problem:**
```
c Cell 1 bounded by surface 10 (plane at z=0)
SDEF POS=0 0 0 RAD=5 AXS=0 0 1 EXT=0    $ Disk source AT z=0
```

**Solutions:**
1. **Use surface source instead:**
   ```
   SDEF SUR=10 POS=0 0 0 RAD=D1
   SI1  H  0 5
   SP1     0 1
   ```

2. **Offset slightly:**
   ```
   SDEF POS=0 0 0.001 RAD=5 AXS=0 0 1 EXT=0    $ 0.001 cm above surface
   ```

**Rule:** Never position degenerate volume sources on defined surfaces.

---

## Error 9: Inconsistent lattice source path

**MCNP Output:** `fatal error. cell path inconsistent with geometry.`

**Cause:** Source path (c1 < c2[i j k] < c3) references non-existent lattice element or incorrect universe structure.

**Solutions:**
1. **Verify lattice element exists:**
   - FILL card defines [0:2 0:1 0:0] → Only [i j k] with i≤2, j≤1, k=0 valid
   - Don't reference [3 0 0] if FILL only goes to i=2

2. **Check universe hierarchy:**
   - If c2 fills c1, ensure c1 FILL or U cards match
   - Check for negative universe signs (affect PDS level)

3. **Use simpler notation for debugging:**
   ```
   SDEF CEL=10 POS=1 1 1      $ Direct cell, no path
   ```

---

## Error 10: Rejection efficiency too low

**MCNP Output:** `warning. source sampling efficiency is X percent`

**Cause:** Many sampled particles rejected (CEL rejection, CCC rejection, position outside geometry).

**Example:**
```
SDEF CEL=D1 POS=0 0 0 RAD=100 CCC=50
SI1  L  50 51 52
SP1     0.98 0.01 0.01         $ 98% in cell 50, but sampling from R=100 sphere
```

**Solutions:**
1. **Match distribution to geometry:**
   - If 98% in cell 50, define POS/RAD specific to cell 50, not large sphere

2. **Use volume-weighted:**
   ```
   SI1  L  50 51 52
   SP1  V  1 1 1               $ Weight by volumes
   ```

3. **Reduce EFF threshold if intentional:**
   ```
   EFF=0.001                   $ Expect low efficiency
   ```

**Check output:** "source particles generated" vs "source tracks started" ratio.

---

## Troubleshooting Workflow

1. **No particles started?**
   → Check POS in valid cell, check IMP>0, check KSRC in fissile regions

2. **Fatal on distribution?**
   → Verify all Dn referenced on SDEF/DS have corresponding SIn cards

3. **Warning on normalization?**
   → Usually safe (MCNP normalizes), but check if sum is very wrong (typo indicator)

4. **Lost particles?**
   → Check if source on surface boundary, offset slightly or use SUR keyword

5. **Low efficiency warning?**
   → Match source distribution shape to cell/geometry shape, or reduce EFF

6. **KCODE vs SDEF conflict?**
   → Remove one (keep KCODE for criticality, SDEF for fixed source)

---

**For advanced source topics, see advanced_source_topics.md.**
**For distribution specifications, see source_distribution_reference.md.**
**For basic usage, see main SKILL.md.**

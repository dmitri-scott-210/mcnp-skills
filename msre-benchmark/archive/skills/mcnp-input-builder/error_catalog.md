# MCNP Input Error Catalog

**Reference Document for mcnp-input-builder Skill**

Comprehensive catalog of common MCNP input errors, their causes, and solutions.

---

## Error Message Hierarchy

MCNP classifies error messages into four categories:

### 1. FATAL Errors
**Severity:** Simulation cannot proceed, MCNP terminates immediately

**Characteristics:**
- Input syntax errors
- Missing required cards
- Invalid card parameters
- Geometry errors preventing particle tracking

**Example Messages:**
```
fatal error. bad trouble in subroutine...
fatal error. cell card not terminated by blank line.
fatal error. material M does not exist.
```

**Action Required:** Fix error before running again

### 2. BAD TROUBLE Errors
**Severity:** Critical runtime error, simulation unstable

**Characteristics:**
- Internal code errors
- Unexpected conditions
- Particle tracking failures
- Memory issues

**Example Messages:**
```
bad trouble in subroutine mcrun
bad trouble in subroutine track
```

**Action Required:** Check geometry, reduce problem complexity, report to MCNP team if persistent

### 3. WARNING Messages
**Severity:** Unconventional but not necessarily incorrect

**Characteristics:**
- Unusual parameter values
- Deprecated syntax
- Potential inefficiencies
- Questionable choices

**Example Messages:**
```
warning. tally may need a particle designator.
warning. cell importance is zero but source is in cell.
warning. negative photon weight.
```

**Action Required:** Review warnings, confirm intentional, fix if unintended

### 4. COMMENT Messages
**Severity:** Informational only

**Characteristics:**
- Parameter assumptions
- Default value usage
- Informational notes

**Example Messages:**
```
comment. using default value for...
comment. particle type not specified, assuming neutron.
```

**Action Required:** Awareness only, no action needed unless unexpected

---

## Common Input Format Errors

### Error 1: Missing Blank Line Between Blocks

**Symptom:**
```
fatal error. bad trouble in subroutine getcl of mcrun
   cell card not terminated by blank line.
```

**Cause:** No blank line separating cell cards from surface cards

**Bad Example:**
```
c Cell Cards
1    1  -1.0   -1   IMP:N=1
2    0         1    IMP:N=0
c Surface Cards              <--- Missing blank line here
1    SO   10.0
```

**Good Example:**
```
c Cell Cards
1    1  -1.0   -1   IMP:N=1
2    0         1    IMP:N=0
                             <--- Blank line required
c Surface Cards
1    SO   10.0
```

**Solution:**
- Add blank line after cell card block
- Add blank line after surface card block
- Add blank line at end of file

**Prevention:**
- Use visual separators (comment lines with =====)
- Configure editor to show whitespace
- Use validation script before running

---

### Error 2: Tab Characters in Input

**Symptom:**
- Misaligned continuation lines
- Cards not recognized
- Parameters read incorrectly
- Unexpected behavior

**Cause:** MCNP treats tabs as single spaces (not multiple spaces)

**Bad Example:**
```
F4:N	1	2	3        (uses tabs between entries)
M1	1001	2	8016	1    (tabs for alignment)
```

**Good Example:**
```
F4:N  1  2  3            (uses spaces)
M1    1001  2  8016  1   (spaces for alignment)
```

**Solution:**
- Replace all tabs with spaces
- Configure text editor to use spaces for indentation
- Use "Expand tabs to spaces" option
- Set tab width to 2 or 4 spaces

**Prevention:**
- Text editor settings: "Insert spaces for tabs"
- Notepad++: Settings → Preferences → Language → Replace by space
- VS Code: "editor.insertSpaces": true
- vim: set expandtab

---

### Error 3: Card Out of Order

**Symptom:**
```
fatal error. bad trouble in subroutine mcrun
   mode card must precede all data cards.
```

**Cause:** MODE card is not the first data card

**Bad Example:**
```
c Data Cards
M1    1001  2  8016  1   <--- Material before MODE
MODE  N                  <--- MODE should be first
SDEF  POS=0 0 0
```

**Good Example:**
```
c Data Cards
MODE  N                  <--- MODE first
M1    1001  2  8016  1
SDEF  POS=0 0 0
```

**Required Data Card Order:**
1. MODE (must be first)
2. Materials (M, MT, MX)
3. Source (SDEF, KCODE, SSR)
4. Tallies (F1-F8, E, T, etc.)
5. Variance reduction (IMP, WWE, WWN, etc.)
6. Physics (PHYS, CUT, TMP)
7. Output (PRINT, PRDMP)
8. Termination (NPS, CTME)

**Solution:** Reorder cards to place MODE first

---

### Error 4: Missing Particle Designator

**Symptom:**
```
warning. tally or card may need a particle designator.
```

**Cause:** Card requires `:N` or `:P` suffix but none provided

**Bad Example:**
```
F4  1          $ Missing particle designator
IMP  1 1 0     $ Missing particle designator
```

**Good Example:**
```
F4:N  1        $ Neutron flux tally
IMP:N  1 1 0   $ Neutron importance
```

**Cards Requiring Particle Designators:**
- F1-F8 (tallies)
- IMP (importance)
- PHYS (physics options)
- CUT (energy cutoffs)
- Many variance reduction cards

**Solution:** Add appropriate particle designator (`:N`, `:P`, `:E`, etc.)

---

### Error 5: Incorrect Continuation Lines

**Symptom:**
- Card reads incorrectly
- Extra entries ignored
- Unexpected parameter values

**Cause:** Improper indentation or missing `&`

**Bad Example:**
```
F4:N  1 2 3 4 5
6 7 8 9 10        <--- Treated as new card, not continuation
```

**Good Examples:**

**Method 1: Five-space continuation (recommended)**
```
F4:N  1 2 3 4 5
      6 7 8 9 10  <--- 5+ leading spaces
```

**Method 2: Ampersand**
```
F4:N  1 2 3 4 5 &
      6 7 8 9 10
```

**Method 3: Card name repetition**
```
F4:N  1 2 3 4 5
F4:N  6 7 8 9 10
```

**Solution:** Use one of the three correct continuation methods

---

### Error 6: Unterminated Input File

**Symptom:**
- MCNP hangs during input reading
- Reads past end of file
- Unexpected behavior

**Cause:** No blank line at end of file

**Bad Example:**
```
...
NPS   1000000
PRINT
<EOF - no blank line>
```

**Good Example:**
```
...
NPS   1000000
PRINT
<--- Blank line required before EOF
<EOF>
```

**Solution:** Add blank line as last line of file

**Prevention:**
- Configure editor to add final newline
- Visual check: cursor should be on line after PRINT

---

### Error 7: Comment Character in Wrong Column

**Symptom:**
- Card not recognized
- Entire line treated as comment
- Parameters missing

**Cause:** `C` or `$` in columns 1-5 of non-comment line

**Bad Example:**
```
C    F4:N  1        $ This entire line is a comment
```

**Good Example:**
```
     F4:N  1        $ Proper card with inline comment
C    This is a comment line
```

**Comment Rules:**
- Full-line comment: `C` or `c` in columns 1-5, then space
- Inline comment: `$` anywhere on line (after data)
- Never use `C` in columns 1-5 unless intending full-line comment

---

## Geometry Errors

### Lost Particle Errors

**Symptom:**
```
lost particle
  x= ...  y= ...  z= ...
```

**Common Causes:**
1. **Cell overlap:** Two cells claim same spatial region
2. **Geometry gap:** Space not defined by any cell
3. **Surface definition error:** Incorrect surface equation
4. **Transformation error:** TRCL/TR card incorrect

**Diagnostic Tools:**

1. **Geometry Plotter:**
```bash
mcnp6 inp=input.i ip
```
- Visual inspection of geometry
- Plot at lost particle location
- Check for gaps and overlaps

2. **VOID Card (automated detection):**
```
VOID
```
- Places test sources throughout geometry
- Identifies gaps and overlaps
- Prints diagnostic information

**Solution Process:**
1. Note lost particle coordinates from output
2. Plot geometry at that location
3. Identify problem cell(s)
4. Fix surface definitions or cell logic
5. Re-run validation

---

### Geometry Error Messages

**Error: "cell has no volume"**
**Cause:** Cell geometry defines empty region
**Solution:** Check Boolean logic, surface senses

**Error: "cell is defined more than once"**
**Cause:** Two cells have overlapping geometry
**Solution:** Fix cell definitions to be mutually exclusive

**Error: "surface X is not used"**
**Cause:** Surface defined but not referenced by any cell
**Solution:** Remove unused surface or add to geometry

**Error: "cell X has zero importance but particles can enter"**
**Cause:** Cell with IMP=0 is not fully surrounded by IMP=0 cells
**Solution:** Extend zero-importance region or set IMP>0

---

## Material and Data Card Errors

### Material Errors

**Error: "material M does not exist"**
**Cause:** Cell references material not defined
**Example:**
```
1  5  -1.0  -1  IMP:N=1   <--- Material 5 not defined
```
**Solution:** Add M5 card or change cell to use existing material

**Error: "ZAID not on cross-section library"**
**Cause:** Isotope identifier not found in xsdir
**Example:**
```
M1  99999.80c  1.0         <--- Invalid ZAID
```
**Solution:** Use correct ZAID format, check xsdir availability

**Error: "sum of fractions not equal to 1"**
**Cause:** Material card has incorrect normalization
**Example:**
```
M1  1001  3  8016  1        <--- Sum = 4, not normalized
```
**Solution:** Normalize fractions or use negative fractions (atomic)

---

### Source Errors

**Error: "source particle not in any cell"**
**Cause:** Source position outside geometry
**Solution:** Check POS coordinates, ensure within cells

**Error: "source in cell with zero importance"**
**Cause:** SDEF POS is in cell with IMP=0
**Example:**
```
SDEF  POS=0 0 0            <--- In graveyard cell
...
999  0  999  IMP:N=0       <--- Source cell
```
**Solution:** Place source in cell with IMP>0

**Error: "kcode before fission neutrons"**
**Cause:** No fissile material in KCODE problem
**Solution:** Add fissile material (U-235, Pu-239, etc.)

---

### Tally Errors

**Error: "tally X is not defined"**
**Cause:** Energy bins (En) or multiplier (FMn) without corresponding Fn tally
**Solution:** Add Fn tally or remove orphaned cards

**Error: "cell/surface Y not found for tally"**
**Cause:** Tally references non-existent cell/surface
**Example:**
```
F4:N  999                   <--- Cell 999 not defined
```
**Solution:** Use correct cell/surface number

**Error: "tally has no particle crossing surface"**
**Cause:** Tally on surface with no particle flux
**Solution:** Check geometry, source location, importance

---

## Best Practices for Error Prevention

### 1. Input Validation Before Running
```bash
# Check three-block structure
# Verify blank lines
# Validate card order
python validate_input_structure.py input.i
```

### 2. Geometry Validation
```bash
# Run geometry plotter
mcnp6 inp=input.i ip

# Use VOID card for automated checking
# Add VOID to data cards, run once
```

### 3. Incremental Development
- Start with simple geometry
- Add complexity gradually
- Validate at each step
- Comment changes thoroughly

### 4. Use Comments Liberally
```
c =================================================================
c KNOWN ISSUES / TO-DO
c =================================================================
c  - Check material 5 density (placeholder value)
c  - Verify transformation TR1 (rotated 30 degrees?)
c  - Add energy bins to F4 tally
c =================================================================
```

### 5. Version Control
- Keep working versions
- Document changes
- Ability to revert if errors introduced

---

## Validation Checklist

Before running MCNP, verify:

**Format:**
- [ ] Three-block structure (cells, surfaces, data)
- [ ] Blank lines between blocks and at EOF
- [ ] No tabs (only spaces)
- [ ] Continuation lines properly formatted
- [ ] MODE card is first data card

**Geometry:**
- [ ] All surfaces used in cells are defined
- [ ] All cells have importance (IMP:N, IMP:P, etc.)
- [ ] Graveyard cell exists with IMP=0
- [ ] No obvious gaps or overlaps
- [ ] Geometry plotted and visually inspected

**Materials:**
- [ ] All materials referenced in cells are defined (M cards)
- [ ] ZAID identifiers valid (check xsdir)
- [ ] Densities reasonable
- [ ] S(α,β) cards (MT) match material

**Source:**
- [ ] Source position inside geometry
- [ ] Source in cell with IMP>0
- [ ] Source energy/distribution reasonable
- [ ] KCODE or SDEF present (not both)

**Tallies:**
- [ ] Tally cells/surfaces exist
- [ ] Particle designators correct
- [ ] Energy bins reasonable
- [ ] Multipliers (FM) match tally numbers

**Physics:**
- [ ] MODE includes all needed particles
- [ ] PHYS cards for all MODE particles
- [ ] Energy cutoffs appropriate

**Termination:**
- [ ] NPS or KCODE specified
- [ ] CTME for long runs (optional)

---

## Quick Reference: Error Categories

| Category | Severity | Action |
|----------|----------|--------|
| FATAL | Critical | Must fix before run |
| BAD TROUBLE | Critical | Fix and potentially report |
| WARNING | Caution | Review and confirm intent |
| COMMENT | Info | Awareness only |

---

## Further Reading

- MCNP6 User Manual, Chapter 4: Input File Description
- MCNP6 User Manual, Appendix F: Error Messages
- Skill: mcnp-input-validator (automated validation)
- Skill: mcnp-geometry-checker (geometry diagnostics)
- Skill: mcnp-fatal-error-debugger (error troubleshooting)

---

**End of Error Catalog**

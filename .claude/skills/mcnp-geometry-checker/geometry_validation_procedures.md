# MCNP Geometry Validation Procedures

**Version:** 2.0.0
**Skill:** mcnp-geometry-checker

---

## VOID Card Test Procedure

### Purpose
Detect overlapping cells where multiple cells claim the same physical space.

### Procedure
1. **Add VOID card to Data Cards block:**
   ```
   MODE N
   ... other cards ...
   VOID
   NPS 1000
   ```

2. **Run MCNP with minimal histories**
3. **Search output for VOID result:**
   ```
   1-pass void check:    void =  0.00000E+00
   ```

4. **Interpret result:**
   - `VOID = 0.00000E+00` → No overlaps (PASS)
   - `VOID ≠ 0` → Overlaps exist (FAIL - must fix)

### If Overlaps Found
- MCNP output lists overlapping cell pairs
- Plot geometry in overlap region
- Fix Boolean expressions or surface definitions
- Re-run VOID test until VOID=0

---

## Lost Particle Debugging

### Symptoms
- Output shows "lost particle" warnings
- Particles escape valid geometry

### Debugging Steps
1. **Extract coordinates from output:**
   ```
   lost particle at x=10.5 y=2.3 z=15.8
     in cell 0
     surface 25
   ```

2. **Plot at lost particle location:**
   ```
   mcnp6 ip i=input.inp
   plot origin=10.5 2.3 15.8 extent=5 5 basis=xy
   ```

3. **Identify problem:**
   - Dashed line → Gap between cells
   - Multiple colors → Overlap
   - No cell → Geometry incomplete

4. **Fix geometry:**
   - Gap → Extend cell boundaries
   - Overlap → Fix Boolean operators
   - Incomplete → Add missing cells

---

## Geometry Plotting Guide

### Basic Commands
```bash
# Launch plotter
mcnp6 ip i=input.inp

# In plotter:
plot origin=0 0 0 basis=xy extent=50 50    # XY plane
plot origin=0 0 0 basis=xz extent=50 50    # XZ plane
plot origin=0 0 0 basis=yz extent=50 50    # YZ plane
```

### Interpretation
- **Solid lines:** Cell boundaries (surfaces)
- **Dashed lines:** Gaps or undefined regions (BAD)
- **Colors:** Different cells
- **White/void:** No cell defined

---

## Best Practices

1. Always run VOID test before production
2. Plot from multiple views (XY, XZ, YZ)
3. Fix overlaps immediately (causes wrong physics)
4. Debug lost particles at exact coordinates
5. Test complex geometries incrementally

---

**END OF PROCEDURES**

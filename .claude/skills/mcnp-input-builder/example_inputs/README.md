# MCNP Input Builder - Example Input Files

This directory contains annotated example MCNP input files demonstrating professional numbering schemes, commenting conventions, and organization practices.

---

## Example Files

### 1. annotated_pwr_pin.i

**Description**: Single PWR fuel pin with UO2 fuel, gas gap, Zircaloy cladding, and water coolant.

**Demonstrates**:
- Basic systematic numbering (100-series for fuel pin components)
- Correlated cell/surface numbering
- Comprehensive inline and block comments
- Material definitions with mass fractions
- Thermal scattering (MT cards) for water
- Fixed source definition
- Multiple tallies with energy bins

**Complexity Level**: Beginner

**Key Learning Points**:
- Three-block structure (cells, surfaces, data)
- Section dividers and headers
- Units documented in comments
- Material properties explained
- Surface dimensions with units

**Use this example for**:
- First MCNP input file
- Understanding basic organization
- Learning comment conventions
- Simple geometry validation

---

### 2. annotated_htgr_triso.i

**Description**: Single TRISO-coated fuel particle (5 layers) in graphite matrix, demonstrating universe-based geometry.

**Demonstrates**:
- Hierarchical position encoding (111XX pattern)
- Universe component encoding (W digit for component type)
- Multiple universes (u=1114 particle, u=1115 matrix)
- Complex material definitions (UCO fuel, multiple carbon types, SiC)
- Thermal scattering for graphite
- Atom fraction materials (positive densities)
- Volume specifications for small cells

**Complexity Level**: Intermediate

**Key Learning Points**:
- Universe definitions (U= parameter)
- Correlated numbering across entities
- Small-scale geometry (μm → cm conversions)
- Multiple thermal scattering treatments
- Component type encoding in universe numbers

**Use this example for**:
- Understanding universe concepts
- Hierarchical numbering schemes
- Complex material specifications
- Small particle modeling
- Repeated structure preparation (lattices)

---

## Numbering Schemes Used

### PWR Pin Example

```
Cells:     100-series (fuel pin components)
           101 = fuel, 102 = gap, 103 = clad, 104 = coolant
Surfaces:  100-series (correlated with cells)
           101 = fuel outer, 102 = clad inner/axial bottom, 103 = axial top, 104 = clad outer
Materials: Single digit (m1 = fuel, m2 = clad, m3 = coolant)
Universes: Not used (simple geometry, global universe only)
```

### HTGR TRISO Example

```
Cells:     111XX (Position 1-1-1, sequence XX)
           11101-11106 = particle layers, 11107 = matrix filler
Surfaces:  111XX (correlated with cells)
           11101-11105 = particle layer boundaries, 11107 = matrix boundary
Materials: 111 (position-based kernel) or 90X (shared coatings)
           m111 = kernel, m901-905 = shared coating/matrix materials
Universes: 111W (Position 1-1-1, W = component type)
           1114 = TRISO particle (type 4)
           1115 = Matrix filler (type 5)
```

**Component type encoding**:
- 4 = Special component (TRISO particle)
- 5 = Matrix/filler

---

## How to Use These Examples

### 1. Study the Structure

Read each file from top to bottom, noting:
- File header documentation
- Numbering scheme explanation
- Section dividers (===, ---, headers)
- Comment placement and content
- Card organization within blocks

### 2. Run the Examples

```bash
# Copy example to working directory
cp annotated_pwr_pin.i my_pwr_test.i

# Run MCNP (adjust path as needed)
mcnp6 i=my_pwr_test.i

# Check output for errors/warnings
# Review tally results
```

### 3. Modify and Experiment

**Try these modifications**:

**PWR Pin**:
- Change enrichment (92235.70c fraction in m1)
- Add additional fuel pins (copy and renumber)
- Change source energy or spectrum
- Add more tally types (F1 current, F6 heating)

**HTGR TRISO**:
- Change particle dimensions (update surface radii)
- Create a lattice of particles (add LAT=1 cell with FILL array)
- Add another universe (e.g., 1116 for failed particle)
- Change kernel composition (UCO → UO2)

### 4. Validate Your Changes

After modifying:
1. Check three-block structure (blank lines present)
2. Verify all referenced entities exist (surfaces, materials, universes)
3. Plot geometry: `mcnp6 inp=file.i ip`
4. Run with small NPS first to catch errors quickly
5. Review output for warnings

---

## Extending to Larger Models

### From PWR Pin → PWR Assembly

1. Define fuel pin as universe (u=101)
2. Create guide tube universe (u=102)
3. Create lattice cell with fill array (17×17 for PWR)
4. Update numbering: 10XXX for assembly 1, 20XXX for assembly 2, etc.
5. Add assembly-level surfaces (RPP box)

### From Single TRISO → Compact

1. Keep particle universes (u=1114, u=1115)
2. Create particle lattice (u=1116, LAT=1, 15×15 array)
3. Create compact cell filling with u=1116
4. Update numbering for multiple compacts (111XX, 112XX, etc.)
5. Add capsule hardware around compacts

---

## Common Mistakes to Avoid

Based on these examples:

### 1. Forgetting Thermal Scattering

**Wrong**:
```mcnp
m3  1001.70c 2  8016.70c 1  $ Water (missing MT card!)
```

**Right**:
```mcnp
m3  1001.70c 2  8016.70c 1  $ Water
mt3  lwtr.01t  $ REQUIRED for accurate thermal neutron physics
```

### 2. Mismatched Density Signs

**Wrong**:
```mcnp
m1
   92235.70c  0.045  $ Atom fractions
   92238.70c  0.955
   8016.70c   2.0
c
1  1  -10.2  -1  imp:n=1  $ ERROR: Negative density with atom fractions!
```

**Right**:
```mcnp
m1
   92235.70c -0.032  $ Mass fractions (negative)
   92238.70c -0.855
   8016.70c  -0.113
c
1  1  -10.2  -1  imp:n=1  $ Correct: Negative density with mass fractions
```

### 3. Missing Kill Boundary

**Wrong**:
```mcnp
1  1  -10.2  -1  imp:n=1
2  0        1   imp:n=1  $ No IMP:N=0 cell! Particles leak!
```

**Right**:
```mcnp
1  1  -10.2  -1  imp:n=1
2  0        1   imp:n=0  $ Correct: Graveyard with IMP:N=0
```

---

## References

- **numbering_schemes_reference.md** - Complete numbering pattern guide
- **input_organization_guide.md** - File structure and formatting
- **cross_reference_validation.md** - Validation rules
- **comment_conventions_guide.md** - Professional commenting practices
- **SKILL.md** - Main skill documentation

---

## Questions and Modifications

If you want to:
- **Add photon transport**: Change `MODE N` to `MODE N P`, add `IMP:P` to all cells
- **Switch to criticality**: Replace SDEF with KCODE/KSRC, add fissile material
- **Add variance reduction**: Add importance cards or weight windows
- **Create lattices**: Use LAT=1 in cell card, add FILL array
- **Burn fuel**: Add BURN card (see mcnp-burnup-builder skill)

Refer to the relevant skill documentation for detailed guidance.

---

**Last Updated**: 2024-11-08
**Skill**: mcnp-input-builder
**Version**: 2.0

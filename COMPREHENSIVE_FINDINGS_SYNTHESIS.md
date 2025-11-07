# COMPREHENSIVE SYNTHESIS: HTGR Reactor Model Analysis
## All Agent Findings Integrated for MCNP Skills Refinement

**Date**: November 7, 2025
**Purpose**: Synthesize findings from 10 parallel analysis agents to inform comprehensive MCNP skill refinement
**Repository Analyzed**: htgr-model-burnup-and-doserates (AGR-1 experiment + μHTGR microreactor)

---

## EXECUTIVE SUMMARY

This synthesis integrates findings from **13 comprehensive analysis documents** (469 KB total) covering every aspect of professional HTGR reactor modeling in MCNP. The analysis reveals systematic best practices for:

1. **Multi-level lattice hierarchies** (up to 6 levels deep)
2. **FILL array mechanics** with repeat notation
3. **Systematic numbering schemes** that prevent conflicts
4. **Template-based and programmatic input generation**
5. **Cross-referencing validation** for complex geometries
6. **Material tracking** for burnup calculations
7. **Workflow integration** (MCNP → ORIGEN → dose rates)

### Key Statistics

- **Files Analyzed**: 15 MCNP inputs (13 cycles + SDR + template)
- **Total Lines**: ~250,000 lines of MCNP code
- **Cells**: 1,607 cells representing 6+ capsules × 3 stacks × 4 compacts × ~4,000 TRISO particles
- **Surfaces**: 725 (sdr-agr.i) + 1,150 (bench_138B.i)
- **Materials**: 385 materials (130 in SDR model)
- **Universe Levels**: 6-level hierarchy (particle → lattice → compact → stack → capsule → room)

---

## PART 1: CRITICAL PATTERNS FOR LATTICE BUILDING

### 1.1 Multi-Level Lattice Hierarchies

**Pattern Discovered**: Up to 6 levels of nested universes

```
Level 1: TRISO Particle (u=XYZ4)
   ├─ 5 concentric spherical shells
   └─ Materials: kernel, buffer, IPyC, SiC, OPyC

Level 2: Matrix Cell (u=XYZ5)
   └─ Single cell filled with SiC matrix

Level 3: Particle Lattice (u=XYZ6) - LAT=1
   ├─ 15×15×1 rectangular array
   ├─ fill=-7:7 -7:7 0:0 (225 positions)
   └─ Circular packing: 169 particles + 56 matrix

Level 4: Matrix Filler (u=XYZ7)
   └─ Top/bottom caps for compact

Level 5: Compact Lattice (u=XYZ0) - LAT=1
   ├─ 1×1×31 vertical stack
   ├─ fill=0:0 0:0 -15:15
   └─ Pattern: 1117 2R 1116 24R 1117 2R
       (3 caps + 25 particle layers + 3 caps)

Level 6: Global Placement
   └─ fill=XYZ0 (x,y,z) transformation
```

**Efficiency**: Represents **~300,000 TRISO particles** using **~900 cells** (333× reduction)

### 1.2 FILL Array Mechanics - THE CRITICAL RULES

**Index Ordering** (MEMORIZE):
- Arrays filled in **K, J, I** order (K outermost, I innermost)
- For `fill=-7:7 -7:7 0:0`, first row is j=-7 with i from -7 to 7

**Dimension Calculation**:
```
Elements = (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)

fill=-7:7 -7:7 0:0:
  I: -7 to 7 = 15 elements
  J: -7 to 7 = 15 elements
  K: 0 to 0 = 1 element
  Total: 15 × 15 × 1 = 225 elements ✓
```

**Repeat Notation** (Off-by-One Trap):
```
U nR = (n+1) total copies!

Examples:
  1117 2R = 1117 1117 1117 (3 copies)
  1116 24R = 1116 repeated 25 times

Full example:
  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
  = 3 + 25 + 3 = 31 elements ✓
```

**Common Pitfalls**:
| Error | Example | Fix |
|-------|---------|-----|
| Dimension mismatch | fill=0:10 → need 11, give 10 | Count (10-0+1)=11 |
| Repeat off-by-one | "U 10R" = 11 copies not 10 | U nR = n+1 |
| Negative indices | fill=-5:5 = 11 not 5! | Include zero |

### 1.3 Circular Packing in Rectangular Lattices

**Key Pattern**: 15×15 square lattice arranged to approximate cylinder

```
Outer ring (j=-7 to 7):
  1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115

Middle rows (j=-4 to 4):
  1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114

Result: ~169 particles (u=1114) + ~56 matrix (u=1115)
```

**Physical Constraint**: Fits circular compact (r=6.35 mm) using ~0.87 mm lattice pitch

---

## PART 2: SYSTEMATIC NUMBERING SCHEMES

### 2.1 AGR-1 Encoding System

**Cell Numbers** (9XYZW):
```python
cell_id = 90000 + capsule*1000 + stack*100 + compact*20 + sequence

Example: 91234
  9 = AGR experiment
  1 = Capsule 1
  2 = Stack 2
  3 = Compact 2 (encoded as 2×10)
  4 = Sequence number 4
```

**Surface Numbers** (9XYZn):
```python
surface_id = 9000 + capsule*100 + stack*10 + compact

Example: 9123
  91 = Capsule 1, Stack 2
  3 = Compact 3
```

**Material Numbers** (9XYZ):
```python
material_id = 9000 + capsule*100 + stack*10 + compact

Example: 9123 → Material for capsule 1, stack 2, compact 3
```

**Universe Numbers** (XYZW):
```python
universe_id = capsule*1000 + stack*100 + compact*10 + component

Components:
  0 = Compact lattice container
  4 = TRISO particle
  5 = Matrix cell
  6 = Particle lattice
  7 = Matrix filler

Example: 1234 → Capsule 1, Stack 2, Compact 3, TRISO particle (4)
```

**Benefits**:
- Zero numbering conflicts across 1,500+ entities
- Instant location identification from number
- Enables automated generation
- Simplifies debugging

### 2.2 Microreactor Parametric Numbering

**Function-Generated IDs**:
```python
def fuel(layer, number):
    n = f"{layer+1}{number:02d}"  # e.g., "201" for layer 2, assembly 01

    surfaces = f"""
{n}01  so  0.0250    $ Kernel
{n}02  so  0.0350    $ Buffer
{n}10 c/z  0 0  1.150 $ Fuel channel
"""
```

**Subsystem Ranges**:
- 2000-2999: Layer 1 assemblies
- 3000-3999: Layer 2 assemblies
- 4000-4999: Layer 3 assemblies
- 5000-5999: Layer 4 assemblies
- 8000-8999: Shield/SDR components
- 9000-9999: Reflector

---

## PART 3: CELL CARD BEST PRACTICES

### 3.1 TRISO Particle 5-Layer Structure

**Standard Pattern** (from 72 compacts):
```mcnp
91101 9111 -10.924 -91111         u=1114 vol=0.092522  $ Kernel (UO2)
91102 9090 -1.100  91111 -91112  u=1114              $ Buffer (porous C)
91103 9091 -1.904  91112 -91113  u=1114              $ IPyC (dense C)
91104 9092 -3.205  91113 -91114  u=1114              $ SiC (ceramic)
91105 9093 -1.911  91114 -91115  u=1114              $ OPyC (dense C)
91106 9094 -1.344  91115         u=1114              $ SiC Matrix
```

**Critical Features**:
1. **Unique universe** (u=1114) - allows lattice replication
2. **Volume specification** - only for kernel (tally normalization)
3. **Density consistency** - negative = g/cm³, positive = atoms/barn-cm
4. **Surface references** - concentric spheres (SO surfaces)
5. **Material correlation** - material 9111 matches kernel of compact 1, stack 1, capsule 1

### 3.2 Lattice Cell Definitions

**Particle Lattice** (15×15):
```mcnp
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     [... 15 rows total, 225 elements ...]
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
```

**Critical Elements**:
1. **Material 0** - void cell, lattice container
2. **u=1116** - unique universe for this lattice
3. **lat=1** - rectangular lattice
4. **fill=-7:7 -7:7 0:0** - index ranges
5. **Bounding surface** - RPP surface 91117

**Compact Lattice** (1×1×31 vertical):
```mcnp
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
```

**Repeat Notation Breakdown**:
- `1117 2R` = 3 matrix layers (bottom cap)
- `1116 24R` = 25 particle lattice layers (fuel region)
- `1117 2R` = 3 matrix layers (top cap)
- Total: 31 layers filling z=-15 to z=+15

### 3.3 Fill Directive with Transformation

**Global Placement**:
```mcnp
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
```

**Components**:
1. **Material 0** - cell that will be filled
2. **Surface definition** - cylinder 97011 + z-planes 98005, 98051
3. **fill=1110** - universe to fill into this region
4. **Transformation** - (x, y, z) translation in cm

**Purpose**: Places compact lattice universe at off-axis location in capsule

---

## PART 4: SURFACE CARD BEST PRACTICES

### 4.1 Multi-Scale Geometry (5 Orders of Magnitude)

**Scale Range**: 174.85 μm (TRISO kernel) to 190.5 mm (B-10 channel)

**TRISO Particle Surfaces** (9 per particle type):
```mcnp
91111 so   0.017485  $ Kernel (174.85 μm radius)
91112 so   0.027905  $ Buffer (279.05 μm)
91113 so   0.031785  $ IPyC (317.85 μm)
91114 so   0.035375  $ SiC (353.75 μm)
91115 so   0.039305  $ OPyC (393.05 μm)
91116 so   1.000000  $ Matrix (10 mm sphere for lattice element)
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000  $ Lattice element
91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715  $ Compact lattice element
91119 c/z  0.0 0.0   0.6500  $ Compact outer radius
```

**Key Patterns**:
1. **SO surfaces** - centered at origin (used in universes)
2. **RPP surfaces** - define lattice element boundaries
3. **C/Z surfaces** - define compact cylindrical boundary
4. **Dimension consistency** - lattice pitch 0.08743 cm, compact radius 6.5 mm

### 4.2 Concentric Cylinder Hierarchy (Capsule)

**7-Layer Nesting**:
```mcnp
97011 c/z   25.547039 -24.553123   0.63500  $ Compact outer R
97012 c/z   25.547039 -24.553123   0.64135  $ Gas gap outer R
97060 c/z   25.337    -25.337      1.51913  $ Compact holder outer R
97061 c/z   25.337    -25.337      1.58750  $ Inner wall gap R
97062 c/z   25.337    -25.337      1.62179  $ SS316L wall outer R
97063 c/z   25.337    -25.337      1.64719  $ Hf shroud outer R
97064 c/z   25.337    -25.337      1.64846  $ Gas gap outer R
97065 c/z   25.337    -25.337      1.78562  $ Capsule wall outer R
97066 c/z   25.337    -25.337      1.90500  $ B-10 channel outer R
```

**Off-Axis Positioning**:
- 3 stacks positioned at 120° intervals
- Centers at (25.547, -24.553), (24.553, -25.547), (25.911, -25.911) mm
- All share same radii, different centers

### 4.3 Axial Segmentation (PZ Planes)

**Compact Stack** (4 compacts + spacers):
```mcnp
98005 pz   17.81810  $ Bottom of compact 1
98051 pz   20.35810  $ Top of compact 1 (calculated)
98006 pz   22.89810  $ Bottom of compact 2
98052 pz   25.43810  $ Top of compact 2 (calculated)
98007 pz   27.97810  $ Bottom of compact 3
```

**Pattern**:
- Compact height: 2.54 cm
- Gap between compacts: 2.54 cm
- Calculated planes marked with comment

---

## PART 5: MATERIAL CARD BEST PRACTICES

### 5.1 ZAID Selection Patterns

**Primary Libraries Used**:
- **.70c** (ENDF/B-VII.0): H, O, C, Al, actinides, fission products
- **.60c** (ENDF/B-VI.8): Natural Mg, Si, Ti, Zr, Mo
- **.50c** (ENDF/B-V): Natural Cr, Fe, Ni (structural steel)
- **.00c** (ENDF/B-VI.0): AGR graphite, helium, SS316L
- **.20c** (Special): B-10 optimized
- **.80c** (ENDF/B-VIII.0): Air constituents

**Isotopic Resolution**:
- **Always isotopic**: U, Pu, Np, fission products, C (12/13), Si, B (10/11)
- **Natural ZAIDs**: Cr (24000), Fe (26000), Ni (28000), Zr (40000), Hf (72000)

### 5.2 UCO Fuel Kernel Composition

**Standard Pattern**:
```mcnp
m9111  $ kernel, UCO: density=10.924 g/cm3
   92234.00c  3.34179E-03  $ U-234
   92235.00c  1.99636E-01  $ U-235 (19.96% enriched)
   92236.00c  1.93132E-04  $ U-236
   92238.00c  7.96829E-01  $ U-238
    6012.00c  0.3217217    $ C-12
    6013.00c  0.0035783    $ C-13
    8016.00c  1.3613       $ O-16 (>1.0 = stoichiometric ratio)
```

**Formula**: UC₀.₃₂O₁.₃₆ (uranium carbide-oxide)

**Note**: Oxygen fraction >1.0 is valid - MCNP normalizes using cell density

### 5.3 Thermal Scattering (MT Cards)

**Applied Correctly**:
```mcnp
mt2106  lwtr.10t  $ Light water at 294K
mt9040  grph.10t  $ Graphite at 294K (SHOULD BE ADDED)
```

**CRITICAL OMISSION FOUND**:
- ❌ NO graphite thermal scattering in AGR-1 model
- ❌ Affects ~50 materials (m9040-m9094)
- ❌ Impact: Wrong thermal neutron spectrum

**Recommended Fix**:
```mcnp
mt9040  grph.18t  $ 600K graphite
mt9090  grph.18t  $ Buffer carbon
mt9091  grph.18t  $ IPyC
mt9093  grph.18t  $ OPyC
mt9094  grph.18t  $ Matrix carbon
```

### 5.4 Burnup Tracking Materials

**ATR Fuel** (210 unique compositions):
```mcnp
m2106  $ Element 6, radial zone 1, axial zone 1
    1001.70c  3.393340E-02  $ H-1
    8016.70c  1.696670E-02  $ O-16
   13027.70c  2.793720E-02  $ Al-27
   92235.70c  4.198373E-04  $ U-235 (depleted from ~93%)
   94239.70c  3.962382E-07  $ Pu-239 (bred during operation)
   [+ 25 fission products including Sm-149, Gd-157]
```

**Fission Products Tracked**:
- Noble gases: Kr-83, Xe-131/133/135
- Strong absorbers: Sm-149 (40,000 barn), Gd-157 (254,000 barn)
- Stable FPs: Mo-95, Ru-101, Cs-133, Nd-143/145

---

## PART 6: TEMPLATE-BASED AUTOMATION

### 6.1 Jinja2 Template Structure

**bench.template** (13,727 lines):
```python
{{ne_cells}}      # NE neck shim cells (line 621)
{{se_cells}}      # SE neck shim cells (line 674)
{{cells}}         # AGR-1 TRISO test assembly (line 1430)
{{oscc_surfaces}} # Control drum positions (line 1782)
{{surfaces}}      # AGR-1 compact surfaces (line 2214)
{{materials}}     # AGR-1 kernel materials (line 13603)
```

**Result**: 1 template + CSV data → 13 cycle-specific inputs

### 6.2 Time-Weighted Parameter Averaging

**Control Drum Angles**:
```python
# 616 timesteps → single representative angle per cycle
ave_angle = (angle × time_interval).sum() / total_time
closest = find_closest([0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150])
```

**Neck Shim Binary State**:
```python
ave_insertion = (insertion × time).sum() / total
condition = int(np.rint(ave_insertion))  # Round to 0 or 1

materials = {
    0: (10, 1.00276E-1),   # Withdrawn: water
    1: (71, 4.55926E-2),   # Inserted: hafnium
}
```

### 6.3 Automated Validation

**Quality Assurance Plots**:
```python
# Generate 39 diagnostic plots before running MCNP
plot_power_vs_time(cycle)
plot_oscc_vs_time(cycle)
plot_neck_shim_vs_time(cycle)
```

**Purpose**: Visual verification catches data anomalies early

---

## PART 7: PROGRAMMATIC GENERATION

### 7.1 Function-Based Geometry

**Parametric Assembly Definition**:
```python
def fuel(layer, number):
    # Calculate positions
    h = 2*68 - 68*layer
    hm = h + 68/2

    # Generate surfaces
    surfaces = f"""
{n}01  so  0.0250    $ Kernel
{n}10 c/z  0 0  1.150 $ Fuel channel
{n}13 rhp  0 0 {h}  0 0 68  0  1.6  0  $ Hex prism
"""

    # Generate cells
    cells = f"""
{n}01 {n}1 -10.8  -{n}01  u={n}4 vol=948.35  imp:n=1  $ Kernel
{n}10 0  -{n}10  u={n}1 fill={n}8  (0 0 {hm:.1f}) imp:n=1  $ Fuel channel
"""

    # Generate materials
    materials = f"""
m{n}1  $ Kernel UO2
     92235.00c   4.816186e-03
     92238.00c   1.932238e-02
      8016.00c   4.827713e-02
"""

    return cells, surfaces, materials
```

**Consistent Interface**: All functions return (cells, surfaces, materials) tuple

### 7.2 Assembly Loop Generation

**Core Model Creation**:
```python
import input_definition as indef

cells = """c\nc Cells\nc\n"""
surfaces = """c\nc Surfaces\nc\n"""
materials = """c\nc Materials\nc\n"""

# Generate all assemblies
for layer, asse_list in indef.assemblies.items():
    for asse in asse_list:
        sp = asse.split('_')
        if len(sp) == 2:  # Control assembly
            cell, surface, material = indef.control(layer, sp[0])
        else:  # Fuel assembly
            cell, surface, material = indef.fuel(layer, sp[0])

        cells += cell
        surfaces += surface
        materials += material

# Write output
with open('micro.i', 'w+') as f:
    f.write(indef.comments + cells + surfaces + materials + indef.source)
```

### 7.3 Model Consistency Between Analysis Types

**Shared Core** (burnup vs. SDR):
```python
# IDENTICAL generation loop for core geometry
for layer, asse_list in indef.assemblies.items():
    [... exact same code ...]

# ADDITIONAL for SDR model only
surfaces += """c\n8000 c/z  0 0   175  $ Shield\n"""
cells += """c\n8000 9996  -1.164e-03  9130 -8001  $ Air\n"""
materials += """c\nm9996  $ Air\n     7014.80c -0.76\n"""
```

**Benefits**:
- Core geometry guaranteed identical
- Changes propagate automatically
- Reduced error potential

---

## PART 8: CROSS-REFERENCING VALIDATION

### 8.1 Boolean Expression Patterns

**Standard Cell Definition**:
```mcnp
60106 2106 7.969921E-02  1111 -1118 74 -29 53 100 -110

Translation:
  +1111: inside surface 1111
  -1118: outside surface 1118
  +74: inside surface 74
  -29: outside surface 29
  +53: inside surface 53
  +100: inside surface 100
  -110: outside surface 110

  All connected by AND (intersection)
```

**Surface Reuse**:
- Axial planes (100, 110, 120, ...) shared across multiple cells
- Reduces total surface count
- Ensures geometric consistency

### 8.2 Material Reference Validation

**Three Material Types**:
1. **Void (0)**:
   - Lattice containers: `0 ... lat=1`
   - Fill targets: `0 ... fill=U`
   - True voids: `0 ...` (particle termination)

2. **Atom density** (positive): `2106 7.969921E-02 ...`

3. **Mass density** (negative): `9000 -8.03 ...`

### 8.3 Universe Fill Validation

**Hierarchy Rules**:
1. Define child universes before parents
2. No circular references (A fills B, B fills A)
3. All filled universes must exist
4. Universe 0 is always global

**Example Validation**:
```
Define: u=1114 (TRISO particle)
Define: u=1115 (matrix cell)
Define: u=1116 (lattice) - fills with 1114, 1115 ✓
Define: u=1117 (matrix filler)
Define: u=1110 (compact lattice) - fills with 1116, 1117 ✓
Use: fill=1110 in global cell ✓
```

---

## PART 9: WORKFLOW INTEGRATION

### 9.1 Multi-Physics Coupling

**3-Step Process**:
```
Step 1: MCNP Neutron Transport
  ├─ Calculate neutron flux in 150 cells
  └─ Output: flux spectra by cell

Step 2: MOAA Depletion (MCNP + ORIGEN coupling)
  ├─ Burnup cells tracked individually
  ├─ Isotopic evolution calculated
  └─ Output: isotopic inventory vs. time

Step 3: MCNP Photon Transport
  ├─ Use isotopic inventory as photon source
  ├─ Calculate dose rates
  └─ Output: dose rate map

Formula: D [Sv/h] = F4:p × Σ(Sᵢ) × 3.6×10⁻⁹
```

### 9.2 Repeated Structures Workflow

**Verification Exercise**:
```
Reference Model:
  - 164 individual cells tracked
  - Each fuel pin explicit

Repeated Structures Model:
  - 1 lattice cell
  - 164 universe instances

Result: <5% difference with 90× faster execution
```

**Key Insight**: Flux-based grouping enables massive computational savings while preserving accuracy

---

## PART 10: CRITICAL LESSONS FOR SKILLS

### 10.1 Lattice Building Must Teach

1. **Multi-level nesting** (up to 6 levels practical)
2. **FILL array dimension calculation** (include zero!)
3. **Repeat notation** (nR = n+1 copies)
4. **Circular packing in rectangular lattices**
5. **Index ordering** (K, J, I - outermost to innermost)
6. **Universe numbering schemes** (systematic, hierarchical)
7. **Lattice element sizing** (surface must contain N×pitch)
8. **Fill transformations** (x,y,z positioning)

### 10.2 Input Building Must Teach

1. **Systematic numbering** (encode hierarchy in numbers)
2. **Comment conventions** (inline, descriptive)
3. **Material-geometry correlation** (same numbering)
4. **Volume calculations** (for tally normalization)
5. **Importance specifications** (variance reduction prep)
6. **Universe hierarchy planning** (bottom-up definition)
7. **Cross-reference validation** (all referenced entities exist)

### 10.3 Material Building Must Teach

1. **ZAID library selection** (.70c vs .00c vs .80c)
2. **Isotopic resolution** (when to use natural ZAIDs)
3. **Thermal scattering** (ALWAYS for graphite, water)
4. **Temperature-appropriate libraries** (600K graphite not 294K)
5. **Burnup tracking** (fission products, actinides)
6. **Density specifications** (negative=g/cm³, positive=atoms/barn-cm)
7. **Stoichiometric ratios** (>1.0 is valid, MCNP normalizes)

### 10.4 Automation Must Teach

1. **Template vs. programmatic** (when to use each)
2. **Jinja2 basics** ({{variable}} syntax)
3. **Function-based generation** (consistent returns)
4. **Loop-based assembly** (scalability)
5. **CSV data integration** (external parameters)
6. **Time-weighted averaging** (operational history)
7. **Automated validation** (pre-run checks, plots)

### 10.5 Validation Must Teach

1. **Dimension verification** (FILL array element counts)
2. **Cross-reference checking** (undefined surfaces, materials, universes)
3. **Numbering conflict detection** (duplicate IDs)
4. **Geometry plotting** (visual verification)
5. **Lost particle analysis** (overlap/gap detection)
6. **Statistical quality** (10 checks)
7. **Benchmark comparison** (code-to-code, code-to-experiment)

---

## PART 11: SKILL REFINEMENT PRIORITIES

### 11.1 HIGH PRIORITY (Fix Immediately)

**mcnp-lattice-builder**:
- Add FILL array dimension calculator
- Add repeat notation converter (user-friendly → MCNP format)
- Add circular packing generator for TRISO particles
- Add multi-level lattice templates (2-6 levels)
- Add universe hierarchy validator

**mcnp-material-builder**:
- Add thermal scattering checker (warns if missing for C, H₂O, Be)
- Add temperature-dependent library selector
- Add TRISO material templates
- Add burnup tracking material generator

**mcnp-input-validator**:
- Add FILL array dimension checker
- Add universe cross-reference validator
- Add numbering conflict detector
- Add surface-cell reference checker

### 11.2 MEDIUM PRIORITY (Major Enhancement)

**mcnp-template-generator** (NEW SKILL):
- Convert existing inputs → Jinja2 templates
- Identify parameterizable sections
- Generate CSV data files
- Create rendering script

**mcnp-programmatic-generator** (NEW SKILL):
- Generate function-based geometry modules
- Create assembly definition dictionaries
- Implement consistent return interfaces
- Build multi-variant generators

**mcnp-geometry-builder**:
- Add TRISO particle geometry templates
- Add concentric cylinder generators
- Add hexagonal assembly generators
- Add transformation calculators

### 11.3 LOW PRIORITY (Nice to Have)

**mcnp-workflow-integrator** (NEW SKILL):
- MCNP-ORIGEN coupling setup
- Multi-step calculation workflows
- Data handoff automation

**mcnp-burnup-modeler** (ENHANCE):
- Cell selection for tracking
- Fission product selection
- Isotopic inventory management

---

## APPENDIX A: DOCUMENT LOCATIONS

All analysis documents created by agents:

1. **Research Article Analysis**:
   - AGR-1_Technical_Analysis_Report.md (58 KB)
   - QUICK_REFERENCE_TRISO_SPECS.md (20 KB)

2. **Cell Card Analysis**:
   - AGR1_CELL_CARD_COMPLETE_ANALYSIS.md (31 KB)

3. **Surface Card Analysis**:
   - AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md (39 KB)

4. **Material Card Analysis**:
   - AGR1_Material_Card_Analysis.md (46 KB)

5. **Template Structure Analysis**:
   - AGR1_TEMPLATE_STRUCTURE_ANALYSIS.md (50 KB)

6. **Input Generation Workflow**:
   - ANALYSIS_INPUT_GENERATION_WORKFLOW.md (50 KB)

7. **Microreactor Programmatic Model**:
   - Included in Agent 7 output (embedded in synthesis)

8. **FILL Array Deep Dive**:
   - AGENT8_FILL_ARRAY_DEEP_DIVE.md (46 KB)

9. **Cross-Referencing Patterns**:
   - AGENT9_CROSS_REFERENCING_PATTERNS.md (45 KB)
   - AGENT9_QUICK_REFERENCE.md (8.7 KB)
   - AGENT9_VISUAL_DIAGRAMS.md (37 KB)
   - README_AGENT9.md (11 KB)

10. **Best Practices Synthesis**:
    - HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md (39 KB)

**Total**: 13 documents, 469 KB of detailed analysis

---

## APPENDIX B: EXAMPLE FILE STATISTICS

**sdr-agr.i** (AGR-1 shutdown dose rate model):
- Lines: 4,653
- Cells: 1,607
- Surfaces: 725
- Materials: 130
- Universes: 72 × 4 types = 288

**bench_138B.i** (ATR cycle 138B with AGR-1):
- Lines: 18,414
- Cells: ~2,000
- Surfaces: 1,150
- Materials: 385
- Template variables: 6

**input_definition.py** (Microreactor parameter file):
- Lines: 461
- Functions: 3 (fuel, control, reflector)
- Assemblies: 144 (4 layers × 36 per layer)
- Universes: 9 per assembly type

---

## CONCLUSION

This comprehensive synthesis reveals that **professional reactor modeling in MCNP** requires integration of:

1. ✅ **Complex geometry** (multi-level lattices, 6-level hierarchies)
2. ✅ **Systematic numbering** (hierarchical, conflict-free)
3. ✅ **Proper materials** (isotopic resolution, thermal scattering)
4. ✅ **Automation** (templates + programmatic generation)
5. ✅ **Validation** (cross-referencing, dimension checking)
6. ✅ **Workflow integration** (multi-physics coupling)

**The current MCNP skills do NOT adequately teach these patterns.** The skill refinement plan must address all six areas comprehensively to enable users to build production-quality reactor models.

**Next Step**: Create detailed skill-by-skill refinement plan with specific updates to SKILL.md files, Python scripts, and example files.

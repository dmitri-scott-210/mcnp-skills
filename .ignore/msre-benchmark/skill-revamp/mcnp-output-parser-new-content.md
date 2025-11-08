# New Content Sections for mcnp-output-parser SKILL.md

**Date:** 2025-11-06
**Purpose:** Content to be integrated into mcnp-output-parser SKILL.md

---

## Section 1: Legacy EEOUT Format (Appendix D.7)

**Location in SKILL.md:** After "HDF5 Format (RUNTPE.H5)" section

```markdown
### EEOUT Legacy Format (Deprecated)

**⚠️ DEPRECATION NOTICE:** The EEOUT format is deprecated as of MCNP6.3+. Use HDF5 format instead (Appendix D.6). This documentation is provided for backward compatibility only.

**Purpose:** Legacy unstructured mesh output format from MCNP6's Revised Extended Grid Library (REGL)

**File Types:**
- `EEOUT` - Binary format (default, Fortran unformatted)
- `EEOUT_ASCII` - ASCII text format (convertible via `um_post_op -bc`)

**Why Deprecated:**
- Non-portable binary format (Fortran record markers)
- Limited modern visualization tool support
- Large file sizes without compression
- Replaced by HDF5/XDMF workflow

**File Structure:**

Version 6 EEOUT format follows a self-describing structure with keyword-value pairs:

**First Line:**
```
MCNP EDITS A    (ASCII version)
MCNP EDITS B    (Binary version)
```

**Data Sets (in order):**
1. **Mesh source** - Abaqus (currently only supported source)
2. **File version** - Version number (currently 6)
3. **Calling code labels** - Problem ID, code version, date/time, associated files
4. **Integer parameters** - Nodes, materials, instances, element counts by type
5. **Real parameters** - Length conversion factor, normalization factor
6. **Particle list** - Particle type numbers (1=neutron, 2=photon, etc.)
7. **Particle edit list** - Mapping of particles to edits
8. **Edit descriptions** - Number of particles, edits, energy/time/response bins
9. **Edit data groups** - Per-particle edit details, conversion factors, bin definitions
10. **Materials** - Alphanumeric material names
11. **Instance element totals** - Cumulative element counts per instance
12. **Instance element names** - Pseudo-cell names
13. **Instance element type totals** - Element numbers by type (tet, pent, hex)
14. **Nodes group** - X, Y, Z coordinates for all nodes (in cm)
15. **Element type** - Type code per element (4/5/6 for 1st order, 14/15/16 for 2nd order)
16. **Element materials** - Material number per element
17. **Connectivity data** - Node connectivity per element (element-ordered)
18. **Nearest neighbor data** - Neighboring element numbers per face
19. **Edit sets group** - Edit results by particle, time bin, energy bin
20. **Centroids group** - Element centroid X, Y, Z coordinates
21. **Densities** - Material density per element (g/cm³)
22. **Volumes** - Element volumes (cm³)

**Element Type Codes:**
- 4 = 1st order tetrahedron
- 5 = 1st order pentahedron
- 6 = 1st order hexahedron
- 14 = 2nd order tetrahedron
- 15 = 2nd order pentahedron
- 16 = 2nd order hexahedron

**Fortran Binary Format Note:**

Binary EEOUT files contain Fortran record markers (4-8 bytes before and after each record). When reading with non-Fortran languages:
1. Read first 12 characters to determine record marker size
2. Skip markers when reading subsequent records
3. Or use REGL library routines (if source code available)

**Migration to Modern Format:**

**Instead of EEOUT:**
```
c Old approach (deprecated)
EMBED 14
```

**Use HDF5/XDMF:**
```
c Modern approach (recommended)
FMESH14:N GEOM=XYZ ...
          OUT=xdmf
```

**To convert existing EEOUT:**
```bash
# Convert binary to ASCII
um_post_op -bc -o eeout.ascii eeout.binary

# Convert to VTK for ParaView
um_post_op -vtk -o mesh_data.vtk eeout.binary
```

**Python Parsing Strategy:**

Due to Fortran binary complexity, recommend:
1. Use `um_post_op` utility for conversion
2. Parse resulting ASCII or VTK format
3. Or link against REGL library (if available)

**ASCII EEOUT Parsing Example:**
```python
def parse_eeout_ascii(filepath):
    """
    Parse ASCII EEOUT file (basic structure)

    Note: Full parser complex due to variable structure.
    Consider using um_post_op utility instead.
    """
    with open(filepath, 'r') as f:
        # Check header
        first_line = f.readline().strip()
        if not first_line.startswith('MCNP EDITS'):
            raise ValueError("Not a valid EEOUT file")

        if first_line.endswith('B'):
            raise ValueError("Binary EEOUT - use um_post_op to convert")

        # EEOUT uses self-describing format
        # Each dataset has:
        #   - Meta data line (6 integers)
        #   - Optional title line
        #   - Data records

        # Due to complexity, recommend using um_post_op
        # for conversion to more parseable formats

        print("EEOUT ASCII detected")
        print("Recommend: um_post_op -vtk -o output.vtk eeout.ascii")
        print("Then use VTK tools or ParaView for processing")

# For practical use, rely on um_post_op utility
```
```

---

## Section 2: um_post_op Utility (Appendix E.11)

**Location in SKILL.md:** After EEOUT Legacy Format section

```markdown
### um_post_op Utility (Legacy EEOUT Processing)

**⚠️ DEPRECATION NOTICE:** um_post_op is deprecated along with EEOUT format. Use for legacy file processing only.

**Purpose:** Command-line utility for manipulating legacy EEOUT files

**Availability:** Included with MCNP6 distribution (Fortran, uses REGL library)

**Command Line Help:**
```bash
um_post_op --help
```

**Mutually Exclusive Operations:**

| Option | Long Form | Function |
|--------|-----------|----------|
| `-m` | `--merge` | Merge multiple files (history-weighted) |
| `-a` | `--add` | Add multiple files (no weighting) |
| `-bc` | `--binconvert` | Convert binary ↔ ASCII |
| `-vtk` | `--vtkfile` | Generate VTK visualization file |
| `-ta` | `--tally` | Generate pseudo-tallies by instance |
| `-wse` | `--writesedit` | Write single edit to file |
| `-eh` | `--errorhist` | Generate error histogram |

**Output Options:**

| Option | Long Form | Use |
|--------|-----------|-----|
| `-o` | `--output` | Single output filename |
| `-ex` | `--extension` | File extension for multiple outputs |

**Common Workflows:**

**1. Merge Parallel Runs:**
```bash
# Merge multiple EEOUT files from independent runs
# Results weighted by number of histories
um_post_op -m -o merged_eeout eeout1 eeout2 eeout3 eeoutN

# Input files can be mixed ASCII/binary
# Output is always ASCII
```

**2. Add Results from Different Sources:**
```bash
# Combine results from different calculations
# NO history weighting (already normalized results)
um_post_op -a -o combined_eeout eeout_source1 eeout_source2
```

**3. Convert Binary to ASCII:**
```bash
# Single file with specific output name
um_post_op -bc -o eeout.ascii eeout.binary

# Single file with extension
um_post_op -bc -ex ascii eeout.binary
# Creates: eeout.binary.ascii

# Multiple files
um_post_op -bc -ex asc eeout1 eeout2 eeoutN
# Creates: eeout1.asc, eeout2.asc, ..., eeoutN.asc
```

**4. Generate VTK for ParaView:**
```bash
# Single file
um_post_op -vtk -o mesh_data.vtk eeout1

# Multiple files
um_post_op -vtk -ex vtk eeout1 eeout2 eeoutN
# Creates: eeout1.vtk, eeout2.vtk, ..., eeoutN.vtk
```

**ParaView Workflow:**
1. Generate VTK: `um_post_op -vtk -o mesh.vtk eeout`
2. Open ParaView
3. File → Open → Select `mesh.vtk`
4. Apply filters (Slice, Clip, Threshold)
5. Visualize mesh tally results

**5. Generate Pseudo-Tallies:**
```bash
# Create volume-weighted averages per pseudo-cell
um_post_op -ta -o eeout.tally eeout1
```

**Pseudo-Tally Formula:**
```
tally_i = Σ(edit_n × vol_n) / Σ(vol_n)

Where:
  tally_i = pseudo-tally for pseudo-cell i
  edit_n  = edit result of element n
  vol_n   = volume of element n
  Sum over all elements in pseudo-cell i
```

**Output:** Instance-based averages (like MCNP F4/F6 tallies)
**Note:** No statistical uncertainties provided

**6. Write Single Edit:**
```bash
# Extract specific edit to detailed file
um_post_op -wse 1 -o edit1.txt eeout1

# With value filtering (only values > 0)
um_post_op -wse 1 -p 1 -o edit1_positive.txt eeout1

# Only values ≤ 0.005
um_post_op -wse 1 -p -5.0e-3 -o edit1_small.txt eeout1

# Ordered by position (x,y,z)
um_post_op -wsep 1 -o edit1_spatial.txt eeout1
```

**7. Generate Error Histograms:**
```bash
# Default 10 bins
um_post_op -eh -o error_hist.txt eeout1

# Custom number of bins
um_post_op -eh 20 -o error_hist.txt eeout1
```

**Histogram Output:**
- Minimum and maximum errors
- Error bin distribution (absolute and relative %)
- Cumulative percentages
- Results per pseudo-cell and overall

**Important Notes:**

1. **File Consistency:** When merging/adding, all files must have matching:
   - Node counts
   - Material counts
   - Instance counts
   - Element type counts

2. **Mixed Format Support:** Input files can mix ASCII and binary (auto-detected)

3. **Precision Loss:** Binary→ASCII conversion loses precision (6 significant digits)

4. **VTK Version:** Generates VTK 4.2 format (may need `.vtk` extension for recognition)

5. **REGL Integration:** um_post_op uses REGL library - maintain consistency with MCNP6

**When to Use um_post_op:**
- Processing legacy EEOUT files
- Converting old simulations to modern formats
- Merging parallel runs from MCNP6.2 and earlier
- Backward compatibility requirements

**Modern Alternative:**

Instead of EEOUT + um_post_op workflow, use:
```
FMESH:N ... OUT=xdmf
```
Then open `meshtal.xdmf` directly in ParaView.
```

---

## Section 3: inxc File Format (Appendix D.9)

**Location in SKILL.md:** After um_post_op section

```markdown
### inxc File Format (Cross-Section Editing Output)

**Purpose:** Input format for `inxc` utility - generates double-differential cross-section edits

**Format:** 128-column card-based format (fixed width)
**Input Style:** List-directed with repeat counts, forward slash (/) terminates lines

**File Structure:**

**Card 1: Problem Title**
- 80-character problem description

**Card 2: Control Parameters**
```
ncase  kplot  l_res
```
- `ncase` - Number of desired XS edit cases (default: 0)
- `kplot` - If nonzero, write to MCTAL file for plotting (default: 0)
- `l_res` - If nonzero, perform residual nuclei edit (default: 0)

**For Each Case (repeat ncase times):**

**Card 3: Case Title**
- 128-character case description

**Card 4: Edit Specification**
```
nerg  nang  ntype  fnorm  imom  iyield
```
- `nerg` - Number of energy (momentum) bin boundaries (default: 0 = energy-integrated)
- `nang` - Number of angle bin boundaries (default: 0 = angle-integrated)
  - `nang > 0` → cosine bins
  - `nang < 0` → degree bins
- `ntype` - Number of particle types to tally (default: 0 = all types)
- `fnorm` - Normalization factor (default: 1.0)
  - Example: `fnorm=1000.0` converts output to millibarns
- `imom` - If nonzero, momentum bins (MeV/c) instead of energy (MeV) (default: 0)
- `iyield` - If nonzero, output differential multiplicities instead of cross sections (default: 0)

**Card 5: Energy/Momentum Bins** (present if nerg > 0)

Four input modes:
1. **All bins explicit:** E₁, E₂, ..., Eₙ (increasing order)
2. **Linear spacing:** E₁ only → Eᵢ = i×E₁ for i=2,...,nerg
3. **Final bin + spacing:** E₁,...,Eₙ → Eᵢ = Eᵢ₋₁ + (Eₙ-Eₙ₋₁) for i=N+1,...,nerg
4. **Log spacing:** V₁ < 0, V₂ > 0 → Eₙₑᵣ_g = V₂, log₁₀(Eᵢ₋₁/Eᵢ) = V₁ (equal lethargy)

**Card 6: Angle Bins** (present if nang ≠ 0)

**For cosine bins (nang > 0):**
1. Explicit: μ₁, μ₂, ..., μₙ (increasing), μₙₐₙ_g always set to 1
2. Null record `/` → nang equally spaced bins from -1 to 1
3. One value → μ₁ given, μₙₐₙ_g = 1, others interpolated uniformly
4. Two+ values → μ₁, μₙₐₙ_g₋₁ given, μₙₐₙ_g = 1, others interpolated

**For degree bins (nang < 0):**
1. Explicit: φ₁, φ₂, ..., φₙ (decreasing), φₙₐₙ_g always set to 0
2. Null record `/` → |nang| equally spaced bins from 180° to 0°
3. One value → φ₁ given, φₙₐₙ_g = 0, others interpolated uniformly
4. Two+ values → φ₁, φₙₐₙ_g₋₁ given, φₙₐₙ_g = 0, others interpolated

**Card 7: Particle Type Flags** (present if ntype > 0)

**Flags:** k₁, k₂, ..., kₙₜᵧₚₑ (see Table D.22)

**Positive values** (kᵢ > 0): Particle production by nonelastic processes
**Negative values** (kᵢ < 0): Elastic scattering related

**Common particle flags:**
| Flag | Particle | Flag | Particle |
|------|----------|------|----------|
| 1 | neutron | -1 | elastic scattered projectile |
| 2 | photon | -2 | elastic recoil nucleus |
| 3 | electron | 13 | μ neutrino |
| 4 | positron | 14 | anti-μ neutrino |
| 5 | proton | 15 | K⁺ |
| 6 | π⁺ | 16 | K⁻ |
| 7 | π⁻ | 19 | anti-proton |
| 8 | π⁰ | 21 | deuteron |
| 9 | μ⁻ | 22 | triton |
| 10 | μ⁺ | 23 | helion (³He) |
| 11 | νₑ | 24 | alpha (⁴He) |
| 12 | anti-νₑ | | |

**⚠️ CAUTION:** Particle type identifiers differ from general MCNP particle numbering (Table 4.3). Choose carefully.

**Default behavior (ntype=0):**
All 26 edit types allowed, output ordered:
proton, neutron, π⁺, π⁰, π⁻, K⁺, K⁰, K̄⁰, K⁻, anti-proton, anti-neutron, deuteron, triton, helion, alpha, photon, electron, positron, μ⁻, μ⁺, νₑ, ν̄ₑ, νμ, ν̄μ, elastic scattered projectile, elastic recoil nucleus

**Example inxc Input:**
```
U-235 fission double-differential cross sections
1  1  1
Neutron-induced fission on U-235
10  8  1  1.0  0  0
0.01 0.1 1.0 5.0 10.0 15.0 20.0
-1 0 45 90 135 180
1
```

**Parsing inxc Output:**

Due to 128-column fixed format, use structured parsing:

```python
def parse_inxc_card(line):
    """Parse 128-column inxc card"""
    # Fixed-width field parsing
    # Adjust field widths per card type
    pass

# Recommend using MCNP's inxc utility directly
# Output typically goes to MCTAL if kplot=1
```

**Practical Usage:**

```bash
# Run inxc with input file
mcnp6 ixr i=inxc_input.txt

# If kplot=1, output written to mctal
# Parse mctal with mcnp_mctal_parser
```

**When to Use inxc:**
- Detailed reaction cross-section analysis
- Angular distribution studies
- Energy spectrum characterization
- Code verification and validation
```

---

## Section 4: HDF5 Structure Exploration (Appendix D.8)

**Location in SKILL.md:** In HDF5 section, before "Navigation with h5py"

```markdown
### HDF5 Structure Exploration Tool

**Tool:** `scripts/h5_dirtree.py`

**Purpose:** Generate hierarchical tree visualization of HDF5 file structure (LaTeX dirtree format)

**Usage:**
```bash
# Explore entire file
python scripts/h5_dirtree.py runtpe.h5

# Explore specific group
python scripts/h5_dirtree.py runtpe.h5 --group /results

# Explore particle track data
python scripts/h5_dirtree.py runtpe.h5 -g /particle_1
```

**Output Format:**

LaTeX dirtree syntax (for documentation):
```
\dirtree{%
.1 /.
  .2 config\_control (group).
  .2 problem\_info (group).
    .3 title (dataset).
    .3 nps (dataset).
  .2 results (group).
    .3 mesh\_tally\_14 (group).
      .4 energy\_total (group).
        .5 time\_total (group).
          .6 values (dataset).
          .6 errors (dataset).
}
```

**Human-Readable Alternative:**

For terminal display, modify output or use `h5ls`:
```bash
# Built-in HDF5 tool
h5ls -r runtpe.h5

# Detailed info
h5dump -H runtpe.h5
```

**Python Script Features:**
- Automatic group/dataset detection
- Attribute listing
- Configurable starting point (group parameter)
- Adjustable indentation offset

**Integration with Parsing Workflow:**

```python
# Step 1: Explore structure
# python scripts/h5_dirtree.py runtpe.h5

# Step 2: Navigate to data
import h5py

with h5py.File('runtpe.h5', 'r') as f:
    # Based on h5_dirtree output, access data
    mesh_values = f['/results/mesh_tally_14/energy_total/time_total/values'][:]
    mesh_errors = f['/results/mesh_tally_14/energy_total/time_total/errors'][:]
```

**See Also:** `scripts/h5_dirtree.py` (complete implementation bundled)
```

---

## Status

**Content Created:** 4 major sections
**Total Length:** ~800 lines (concise, focused documentation)
**Next Steps:**
1. Create `scripts/h5_dirtree.py`
2. Create 4 core parsing scripts
3. Integrate into SKILL.md
4. Validate and test

**Token Usage:** Efficient - focused on essential information

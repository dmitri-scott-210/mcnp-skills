# MCNP6.3 Claude Skills - Comprehensive Requirements Document

**Version**: 1.0
**Date**: 2025-10-30
**Purpose**: Define complete requirements for Claude Code to develop MCNP6.3 Claude Skills for creating, editing, debugging, and analyzing MCNP input and output files.

---

## Executive Summary

This document specifies the requirements for developing a comprehensive suite of Claude Skills to assist nuclear engineers and physicists in working with MCNP6.3 (Monte Carlo N-Particle Transport Code). The skills must handle the full spectrum of MCNP capabilities from basic geometry creation to advanced variance reduction, while addressing critical edge cases such as large-scale models (9,000+ lines), complex geometries, cross-section library management, and parallel execution.

---

## Table of Contents

1. [Core MCNP6.3 Capabilities](#1-core-mcnp63-capabilities)
2. [Skills Architecture](#2-skills-architecture)
3. [Input File Creation & Editing](#3-input-file-creation--editing)
4. [Output File Analysis](#4-output-file-analysis)
5. [Debugging & Validation](#5-debugging--validation)
6. [Edge Cases & Challenges](#6-edge-cases--challenges)
7. [Advanced Features](#7-advanced-features)
8. [Knowledge Base Requirements](#8-knowledge-base-requirements)
9. [Testing & Validation Strategy](#9-testing--validation-strategy)
10. [Success Metrics](#10-success-metrics)

---

## 1. Core MCNP6.3 Capabilities

### 1.1 Particle Transport
Skills must support all 37+ particle types transported by MCNP6.3:

- **Neutral particles**: neutrons, antineutrons, photons
- **Charged particles**: electrons, positrons, protons, antiprotons
- **Light ions**: deuterons, tritons, helium-3, alpha particles
- **Heavy ions**: transportable heavy ions per Appendix C
- **Mesons**: positive/negative pions, positive/negative muons
- **Baryons**: lambdas, sigmas, cascade particles (Ξ) and antiparticles
- **Energy ranges**: thermal energies to 1 TeV/nucleon

### 1.2 Physics Models
Skills must understand both tabulated data and physics models:

- **Neutron physics**:
  - Continuous-energy cross sections
  - S(α,β) thermal scattering
  - Delayed neutron production
  - Fission multiplication

- **Photon physics**:
  - Photoelectric absorption with fluorescence
  - Compton scattering (coherent and incoherent)
  - Pair production with annihilation
  - Bremsstrahlung radiation

- **Electron/positron physics**:
  - Thick-target bremsstrahlung
  - Continuous slowing down approximation
  - Elastic scattering

- **Heavy charged particle physics**:
  - dE/dx energy loss
  - Nuclear elastic scattering
  - Heavy ion transport models

- **Model physics**: MPHYS card enabling CEM, LAQGSM, INCL models

### 1.3 Geometry Capabilities
Skills must handle:

- **Constructive Solid Geometry (CSG)**:
  - Boolean operators: union (`:`, space), intersection, complement (`#`)
  - Macrobodies: RPP, BOX, RCC, RHP, HEX, REC, TRC, ELL, WED, ARB
  - First-degree surfaces: planes (P, PX, PY, PZ)
  - Second-degree surfaces: spheres (S, SO, SX, SY, SZ), cylinders (C/X, C/Y, C/Z), cones (K/X, K/Y, K/Z)
  - Fourth-degree surfaces: ellipsoids, hyperboloids, paraboloids
  - Special surfaces: toroids (TX, TY, TZ), boxes, polyhedra

- **Repeated structures**:
  - Universes and fills (U, FILL, LAT)
  - Lattices: hexagonal (1), rectangular (2)
  - Coordinate transformations (TR, *TR cards)
  - Cell transformations (TRCL)

- **Unstructured mesh**:
  - Hybrid geometry (CSG + mesh)
  - ABAQUS mesh format
  - External mesh embedding (EMBED card)

### 1.4 Material Specifications
Skills must handle:

- **Material cards (Mn)**:
  - ZAID format (ZZZAAA.nnX)
  - Isotopic composition
  - Natural element expansion
  - Mass/atom fractions
  - Material densities (g/cm³ or negative for atom density)

- **Cross-section libraries**:
  - ENDF/B continuous-energy data
  - Multi-group data
  - Dosimetry cross sections
  - Photonuclear data
  - Thermal scattering libraries (S(α,β))

- **Material properties**:
  - TOTNU card (total ν for fission)
  - NONU card (no ν)
  - MT card (material/thermal treatment)
  - PIKMT card (photo-induced reactions)

### 1.5 Source Definitions
Skills must support all source types:

- **General source (SDEF)**:
  - Position distributions (POS, X, Y, Z)
  - Direction distributions (DIR, VEC, AXS)
  - Energy distributions (ERG, SP, SI)
  - Time distributions (TME)
  - Dependent distributions (DS)
  - Probability distributions (SI/SP pairs)

- **Criticality source (KCODE/KSRC)**:
  - K-effective calculations
  - Initial fission sites
  - Active/inactive cycles
  - Shannon entropy tracking

- **Surface source (SSR/SSW)**:
  - Surface source read
  - Surface source write
  - RSSA files

- **Special sources**:
  - Fixed sources in criticality problems
  - Spontaneous fission sources
  - Radioisotope decay sources

### 1.6 Tally Specifications
Skills must support all tally types:

- **Standard tallies (F1-F8)**:
  - F1: surface current
  - F2: surface flux
  - F4: track-length cell flux
  - F5: point detector/ring detector
  - F6: energy deposition
  - F7: fission energy deposition
  - F8: pulse height

- **Mesh tallies**:
  - FMESH: superimposed mesh tallies
  - TMESH: track-length mesh tallies
  - Cylindrical, rectangular, spherical coordinates

- **Tally modifiers**:
  - Energy bins (En)
  - Time bins (Tn)
  - Cosine bins (Cn)
  - User bins (Un)
  - Segment bins (Sn)
  - Multiplier bins (Mn)
  - Flagging bins (FTn, FQn, FMn, FCn, FUn)

- **Special tallies**:
  - DXTRAN detectors
  - Point detector NEXT events
  - Radiography tallies (FIRn, FCLn)
  - PERT perturbation tallies

- **Tally output**:
  - Statistical error reporting
  - Relative error convergence
  - Ten statistical checks
  - MCTAL file format
  - MESHTAL file format
  - XDMF/HDF5 format for unstructured meshes

### 1.7 Variance Reduction Techniques
Skills must implement:

- **Geometry splitting/Russian roulette**:
  - IMP card (importance)
  - Cell-based splitting

- **Weight windows**:
  - WWN card (weight window bounds)
  - WWE card (weight window energies)
  - WWINP/WWOUT files
  - Mesh-based weight windows

- **Exponential transform**:
  - EXT card
  - Stretching/biasing parameter

- **Forced collisions**:
  - FCL card
  - DXTRAN spheres (DXT, DXC)
  - Nested DXTRAN capability

- **Source biasing**:
  - Source energy biasing
  - Source position biasing
  - Source direction biasing

- **Time splitting**:
  - T-DXTRAN

- **Energy cutoffs**:
  - CUT card (time/energy cutoffs)
  - ELPT card (electron/photon cutoffs)
  - PHYS card (physics options)

### 1.8 Output Control
Skills must handle:

- **Execution control**:
  - NPS card (number of particles)
  - CTME card (computer time limit)
  - STOP card (stop criteria)
  - RAND card (random number control)

- **Print control**:
  - PRINT card (print options)
  - PRDMP card (print dump cycles)
  - PTRAC card (particle track output)
  - MPLOT card (geometry plots)

- **File management**:
  - FILES card (file handling)
  - RUNTPE file (restart)
  - SRCTP file (source)
  - MCTAL file (tallies)
  - OUTP file (output)

---

## 2. Skills Architecture

### 2.1 Skill Categories

The MCNP Claude Skills suite shall be organized into the following categories:

#### Category A: Input Creation & Generation
- `mcnp-input-generator`: Create new MCNP input files from requirements
- `mcnp-geometry-builder`: Build complex geometries interactively
- `mcnp-material-builder`: Create material specifications
- `mcnp-source-builder`: Define source specifications
- `mcnp-tally-builder`: Create tally specifications
- `mcnp-template-generator`: Generate template files for common problems

#### Category B: Input Editing & Modification
- `mcnp-input-editor`: Edit existing MCNP input files
- `mcnp-geometry-editor`: Modify geometry specifications
- `mcnp-transform-editor`: Apply/modify transformations
- `mcnp-variance-reducer`: Add/optimize variance reduction
- `mcnp-input-updater`: Update MCNP5 files to MCNP6 format

#### Category C: Validation & Debugging
- `mcnp-input-validator`: Pre-run validation and error checking
- `mcnp-geometry-checker`: Validate geometry definitions
- `mcnp-fatal-error-debugger`: Diagnose fatal errors from output
- `mcnp-warning-analyzer`: Analyze and fix warnings
- `mcnp-cross-reference`: Check cell/surface/tally cross-references

#### Category D: Output Analysis
- `mcnp-output-analyzer`: Parse and analyze MCNP output files
- `mcnp-tally-analyzer`: Extract and analyze tally results
- `mcnp-criticality-analyzer`: Analyze KCODE results
- `mcnp-statistics-checker`: Verify statistical convergence
- `mcnp-mctal-parser`: Parse MCTAL files

#### Category E: Advanced Operations
- `mcnp-burnup-builder`: Create MCNP-ORIGEN coupled inputs
- `mcnp-mesh-builder`: Create unstructured mesh inputs
- `mcnp-lattice-builder`: Build hexagonal/rectangular lattices
- `mcnp-ww-optimizer`: Generate optimal weight windows
- `mcnp-parallel-configurator`: Configure MPI/OpenMP runs

#### Category F: Utilities & Helpers
- `mcnp-unit-converter`: Convert between units systems
- `mcnp-isotope-lookup`: Look up ZAIDs and properties
- `mcnp-cross-section-manager`: Manage xsdir and libraries
- `mcnp-physical-constants`: Calculate nuclear constants
- `mcnp-example-finder`: Search example database

### 2.2 Skill Interaction Model

Skills should:
- **Be composable**: One skill can call another
- **Share context**: Pass information between skills seamlessly
- **Be stateful**: Maintain context across multiple invocations
- **Be documented**: Each skill has clear usage documentation

### 2.3 Knowledge Base Integration

Each skill must have access to:
- Converted markdown documentation (71 files)
- Example input files database (100+ examples)
- Common error patterns database
- Best practices documentation
- Cross-section library metadata

---

## 3. Input File Creation & Editing

### 3.1 Input File Structure Understanding

Skills must understand the 5-block MCNP input structure:

```
[Block 0: Execution Options - Optional]
message: block
nps 10000000
ctme 480
...

[Blank line]

[Block 1: Cell Cards - Required]
c Cell cards define volumes
1 1 -2.7 -1 imp:n=1 $ Aluminum sphere
2 0     1 imp:n=0 $ Void outside

[Blank line]

[Block 2: Surface Cards - Required]
c Surface cards define boundaries
1 so 10.0 $ Sphere at origin, radius 10 cm

[Blank line]

[Block 3: Data Cards - Optional but typical]
c Material specifications
m1 13027 1.0 $ Aluminum
c Source specification
sdef pos=0 0 0 erg=14.1
c Tally specification
f4:n 1
c Physics and variance reduction
...

[Blank line]

[Block 4: Comments - Optional]
c Additional comments can go here
```

### 3.2 Cell Card Requirements

Skills must create/edit cell cards with:

- **Syntax**: `j m d geom params`
  - `j`: cell number (1-99999999)
  - `m`: material number (0 for void)
  - `d`: density (positive=g/cm³, negative=atoms/b-cm)
  - `geom`: geometry specification using surface logic
  - `params`: IMP, VOL, PWT, EXT, FCL, WWN, DXC, U, TRCL, LAT, FILL, ELPT, COSY, BFLCL, UNC

- **Geometry operators**:
  - Space or `:` for union
  - Intersection (juxtaposition)
  - `#` for complement
  - Parentheses for grouping

- **Special cells**:
  - Void cells (m=0)
  - Universe cells (U=n)
  - Lattice cells (LAT=1 or 2)
  - Fill cells (FILL=n or FILL=nx:ny:nz i1 i2 ...)

### 3.3 Surface Card Requirements

Skills must create/edit all surface types:

| Type | Mnemonic | Description | Parameters |
|------|----------|-------------|------------|
| Plane | P, PX, PY, PZ | General/axis-aligned planes | A B C D or D |
| Sphere | S, SO, SX, SY, SZ | General/origin/axis spheres | x y z R or R |
| Cylinder | C/X, C/Y, C/Z, C, CX, CY, CZ | Infinite cylinders | varies |
| Cone | K/X, K/Y, K/Z, KX, KY, KZ | Infinite cones | varies |
| Torus | TX, TY, TZ | Toroids | varies |
| Macrobody | RPP, BOX, RCC, etc. | Complex primitive shapes | varies |

### 3.4 Material Card Requirements

Skills must:
- Look up correct ZAIDs from isotope names
- Expand natural element compositions
- Handle library identifiers (.80c, .31c, etc.)
- Calculate mass/atomic fractions
- Validate cross-section availability
- Apply thermal scattering (MT card)

**Example material card generation**:
```
User: "Create material card for water at 1 g/cm³"

Skill output:
m1 1001.80c 2    $ H-1
   8016.80c 1    $ O-16
mt1 lwtr.20t     $ Light water S(alpha,beta)
```

### 3.5 Source Card Requirements

Skills must build complex sources using:
- Multiple distributions (SI/SP/DS cards)
- Dependent sources
- Energy spectra (discrete, histogram, Watt fission, etc.)
- Direction biasing
- Position distributions (point, volume, surface)
- Time-dependent sources

**Example**:
```
User: "Create 14.1 MeV D-T neutron point source at origin"

Skill output:
sdef pos=0 0 0 erg=14.1 par=n
```

### 3.6 Tally Card Requirements

Skills must:
- Select appropriate tally type for user's needs
- Apply energy/time/angle binning
- Add multiplier cards (FM)
- Set up dose functions (DE/DF cards)
- Configure FMESH parameters
- Apply tally flags appropriately

**Example**:
```
User: "Set up neutron flux tally in cell 5 with 10 energy bins from 1e-8 to 20 MeV"

Skill output:
f4:n 5
e4 1e-8 99log 20
```

---

## 4. Output File Analysis

### 4.1 Output File Parsing

Skills must extract information from:

- **OUTP file sections**:
  - Problem summary (cells, surfaces, materials)
  - Cross-section tables
  - Warning messages
  - Tally specifications echo
  - Tally results with statistics
  - KCODE results (if applicable)
  - Computer time summary
  - Fatal error messages

- **MCTAL file**:
  - Binary or ASCII format
  - Tally numbers and types
  - Bin structures (E, T, C, U, S, M)
  - Values and relative errors
  - TFC (tally fluctuation chart) data

- **MESHTAL file**:
  - Mesh geometry specification
  - Mesh tally results
  - Energy/time bin data
  - Statistical uncertainties

### 4.2 Statistical Analysis

Skills must evaluate the "10 statistical checks":

1. Mean behavior (should settle down)
2. Relative error (should decrease as 1/√N)
3. Variance of variance (should decrease as 1/√N)
4. Figure of merit (should be constant)
5. Relative error < 0.10 for final result
6. Relative error < 0.05 for reliable result
7. VOV < 0.10 for well-behaved tally
8. All checks passed
9. Large tally fluctuations detected
10. Probability density function slope convergence

**Skills must**:
- Extract these checks from TFC bins
- Warn if checks fail
- Suggest remedies (more particles, variance reduction)

### 4.3 KCODE Analysis

For criticality problems, skills must:
- Extract k-effective value and uncertainty
- Check cycle-by-cycle convergence
- Evaluate Shannon entropy behavior
- Identify inactive/active cycle performance
- Check fission source convergence
- Warn about dominance ratio issues

### 4.4 Error Extraction

Skills must:
- Parse fatal error messages
- Identify the problematic input cards
- Suggest corrections based on error type
- Cross-reference with common error patterns

---

## 5. Debugging & Validation

### 5.1 Pre-Execution Validation

Skills must check:

**Input formatting**:
- Two blank lines separating blocks
- Proper comment syntax (`c` in column 1)
- Continuation lines (5 spaces or `&`)
- Card length limits
- Duplicate card detection

**Geometry validation**:
- All surfaces referenced in cells exist
- No undefined surface numbers
- Cell volumes are non-overlapping (if not intentional)
- Lost particle check (all space defined)
- Importance ≠ 0 for source cells

**Material validation**:
- All material numbers referenced exist
- ZAIDs are valid and available in libraries
- Densities have correct sign
- S(α,β) thermal scattering consistency

**Source validation**:
- Source particle type on MODE card
- Source location in non-void, non-zero-importance cell
- Energy distributions normalized
- Dependent source consistency

**Tally validation**:
- Tally particle type on MODE card
- Tally cells/surfaces exist
- Energy bins in ascending order
- Multiplier bins exist

### 5.2 Fatal Error Debugging

Skills must diagnose and fix common fatal errors:

| Error Message | Cause | Fix |
|---------------|-------|-----|
| "bad trouble in subroutine sourcc" | Source outside geometry | Move source position |
| "source particle type not on mode card" | MODE card missing particle | Add particle to MODE |
| "geometry error - lost particle" | Geometry gaps | Check cell definitions |
| "duplicate card" | Card appears twice | Remove duplicate |
| "bad cell number" | Invalid cell ID | Fix cell reference |
| "surface xxx undefined" | Missing surface card | Add surface definition |
| "xsdir file not found" | Cross-section path wrong | Set DATAPATH |
| "model required" | Model physics needed but off | Add MPHYS ON |

**Skill must**:
- Parse the error message
- Locate the problematic line number
- Suggest specific fix with corrected syntax

### 5.3 Warning Analysis

Skills must interpret warnings:

- **Geometry warnings**:
  - "cell xxx is not used" → remove or include in geometry
  - "surface xxx not used" → remove unused surface
  - "cells xxx and yyy overlap" → check geometry logic

- **Material warnings**:
  - "material xxx not used" → remove or reference in cell
  - "zaid not in library" → check xsdir, use different library ID

- **Tally warnings**:
  - "no tracks in tally" → check importance, tally location
  - "poor statistics" → increase NPS or variance reduction

### 5.4 Geometry Validation Tools

Skills must:
- Generate PLOT commands for visual inspection
- Suggest BASIS, ORIGIN, EXTENT for good views
- Create cross-section plots (PX, PY, PZ)
- Identify void regions
- Detect overlapping cells

---

## 6. Edge Cases & Challenges

### 6.1 Large Model Management (Priority: CRITICAL)

**Challenge**: Handle input files with 9,000+ lines (e.g., HFIR reactor model)

**Requirements**:

1. **Memory management**:
   - Lazy loading of model components
   - Stream processing for large files
   - Efficient data structures (avoid full in-memory duplication)

2. **Incremental validation**:
   - Validate in chunks (cells → surfaces → data cards)
   - Early error detection without full parse
   - Progressive error reporting

3. **Selective editing**:
   - Target specific sections without loading entire file
   - Search/replace with regex support
   - Batch modifications (e.g., "change all densities in cells 1-1000")

4. **Performance targets**:
   - Parse 10,000 line file in < 5 seconds
   - Validate 10,000 line file in < 10 seconds
   - Edit operations < 1 second response time

**Implementation strategy**:
- Use streaming parsers
- Index cell/surface/card locations
- Implement caching for repeated operations

### 6.2 Complex Geometry Handling (Priority: CRITICAL)

**Challenge**: Decompose, understand, and modify complex geometries

**Requirements**:

1. **Macrobody decomposition**:
   - Expand RPP/BOX/RCC/etc. to fundamental surfaces
   - Show equivalent surface definitions
   - Convert between macrobody and surface representations

2. **Repeated structures**:
   - Track universe hierarchy (U, FILL)
   - Visualize lattice structures
   - Extract hexagonal lattice ring patterns
   - Resolve fill indices to actual universe numbers

3. **Surface transformations**:
   - Parse TR card coefficients (translation + rotation)
   - Apply *TR (degrees) vs TR (direction cosines)
   - Transform coordinates between systems

4. **Cell transformations (TRCL)**:
   - Apply transformations to cell geometry
   - Compound transformations (multiple TRCLs)
   - Reverse transformations for debugging

5. **Hexagonal lattice handling**:
   - Ring/position extraction: LAT=1 hexagonal indexing
   - Convert (i,j) indices to (ring, position) format
   - Generate fill patterns for hexagonal assemblies

**Implementation strategy**:
- Create geometry AST (abstract syntax tree)
- Implement coordinate transformation library
- Build lattice indexing utilities
- Provide visualization helpers (PLOT card generation)

**Example**:
```
User: "Show me ring 3 of the hexagonal lattice in cell 100"

Skill:
- Parse cell 100 FILL specification
- Extract i,j indices corresponding to ring 3
- List universe numbers for those positions
- Optionally generate PLOT commands to visualize
```

### 6.3 Cross-Section Library Management (Priority: HIGH)

**Challenge**: Manage library versions, temperature dependencies, and Doppler broadening

**Requirements**:

1. **Library version compatibility**:
   - Track available libraries (.80c, .31c, .70c, etc.)
   - Parse xsdir file (or xsdir_mcnp6.1)
   - Warn about library incompatibilities
   - Suggest alternative libraries if unavailable

2. **Temperature-dependent cross sections**:
   - Select appropriate TMP card values
   - Match to available library temperatures
   - Warn if interpolation is needed

3. **On-the-fly Doppler broadening**:
   - Configure DBRC (Doppler Broadening Rejection Correction)
   - Select isotopes for OTF broadening
   - Set temperature ranges appropriately

4. **S(α,β) thermal scattering**:
   - Match MT card libraries to temperatures
   - Ensure lwtr.nnT / grph.nnT availability
   - Validate thermal/fast energy consistency

**Implementation strategy**:
- Build xsdir parser
- Create ZAID-to-library lookup database
- Implement temperature matching algorithm
- Provide library recommendation engine

**Example**:
```
User: "Use uranium-235 at 900 K"

Skill:
- Check xsdir for 92235 at temperatures near 900K
- Find: 92235.80c (293.6K), 92235.81c (600K), 92235.82c (900K), 92235.83c (1200K)
- Recommend: 92235.82c (exact match)
- Generate: m1 92235.82c 1.0
           tmp1 900
```

### 6.4 Parallel Execution Configuration (Priority: MEDIUM)

**Challenge**: Configure MPI/OpenMP execution for HPC environments

**Requirements**:

1. **MPI configuration**:
   - Generate appropriate TASKS card
   - Set up domain decomposition
   - Configure particle distribution
   - Handle multiple RUNTPE files

2. **OpenMP configuration**:
   - Set OMP_NUM_THREADS environment
   - Balance with MPI processes
   - Hybrid MPI+OpenMP strategies

3. **Distributed computing setup**:
   - Generate PBS/SLURM job scripts
   - Configure resource requests (nodes, cores, memory, walltime)
   - Set up file I/O for parallel runs
   - Handle RUNTPE merging for restarts

4. **Job queue management**:
   - Submit jobs to queuing systems
   - Monitor job status
   - Retrieve results
   - Handle failed runs

**Implementation strategy**:
- Template-based job script generation
- Platform-specific configurations (SLURM vs PBS vs LSF)
- Automatic resource estimation based on problem size

**Example**:
```
User: "Configure this job for 256 cores on 8 nodes, 24 hour walltime"

Skill generates:
TASKS 256 256
+ SLURM script:
#!/bin/bash
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=32
#SBATCH --time=24:00:00
#SBATCH --job-name=mcnp_job

export OMP_NUM_THREADS=1
mpiexec -n 256 mcnp6 i=input.i
```

### 6.5 Units & Physical Conversions (Priority: MEDIUM)

**Challenge**: Handle multiple unit systems and provide automatic conversions

**Requirements**:

1. **Length units**:
   - cm (MCNP default) ↔ mm ↔ m ↔ inches
   - Convert surface coefficients
   - Convert source positions
   - Convert tally geometries

2. **Density units**:
   - g/cm³ ↔ kg/m³ ↔ lbm/ft³
   - atoms/b-cm (negative density in MCNP)
   - Molecular weight calculations

3. **Energy units**:
   - MeV (MCNP default) ↔ eV ↔ keV ↔ GeV ↔ Joules
   - Temperature ↔ energy conversions (kT)

4. **Activity units**:
   - Ci ↔ Bq ↔ mCi ↔ µCi
   - Specific activity calculations

5. **Dose units**:
   - rem ↔ Sv ↔ mrem ↔ mSv
   - Gray ↔ rad
   - Dose rate conversions

6. **Physical constants calculator**:
   - Avogadro's number
   - Speed of light
   - Boltzmann constant
   - Barn ↔ cm²
   - MeV ↔ joule

**Implementation strategy**:
- Unit-aware data types
- Automatic unit inference from context
- Conversion factor database
- Dimensional analysis validation

**Example**:
```
User: "Convert aluminum density from 2.7 g/cm³ to atoms/b-cm"

Skill:
- Molecular weight of Al = 26.982 g/mol
- Density in atoms/cm³ = (2.7 g/cm³) × (6.022e23 atoms/mol) / (26.982 g/mol)
                       = 6.026e22 atoms/cm³
- Density in atoms/b-cm = 6.026e22 × 1e-24 = 0.06026 atoms/b-cm
- MCNP input: "1 13000.80c -0.06026"
```

### 6.6 Legacy File Support (Priority: MEDIUM)

**Challenge**: Support MCNP5 files and MCNPX-specific features

**Requirements**:

1. **MCNP5 backward compatibility**:
   - Identify MCNP5-specific syntax
   - Convert deprecated cards (e.g., PIKMT → LCOLR)
   - Update library identifiers (.50c → .80c)
   - Translate removed features

2. **MCNPX feature detection**:
   - Identify MCNPX-only capabilities (proton/heavy ion tallies)
   - Warn if MCNPX-specific physics used
   - Suggest MCNP6 equivalents where available

3. **Version detection**:
   - Infer MCNP version from input syntax
   - Provide version-specific documentation
   - Flag incompatible features

4. **Automatic migration**:
   - Convert MCNP5 → MCNP6 automatically
   - Generate migration report (changes made)
   - Validate converted file

**Implementation strategy**:
- Version-specific syntax databases
- Deprecation mapping table
- Automated testing with version-specific reference files

**Example**:
```
User: "Convert this MCNP5 input to MCNP6"

Skill identifies:
- Library IDs: .50c → .80c (update xsdir reference)
- PIKMT card → LCOLR card (photonuclear)
- NOTRN card → PHYS:P (photon physics)
- Generate updated input with change log
```

---

## 7. Advanced Features

### 7.1 Burnup and Depletion

Skills must support MCNP-ORIGEN coupling:

**Requirements**:
- Generate BURN card specifications
- Set up burnup steps (time, power, flux normalization)
- Configure FISPACT or ORIGEN2 integration
- Track isotopic evolution
- Handle decay chains
- Create material compositions at different burnup steps

**Example applications**:
- Fuel management in reactor cores
- Activation calculations
- Waste characterization
- Isotope production

### 7.2 Unstructured Mesh

Skills must handle hybrid geometry:

**Requirements**:
- Parse ABAQUS mesh files
- Create EMBED cards for mesh insertion
- Define mesh-based tallies on unstructured grids
- Configure UM, URAN, UMSH cards
- Utilize UM tools (um_pre_op, um_post_op, um_converter)
- Handle HDF5 output formats

### 7.3 Weight Window Generation

Skills must optimize variance reduction:

**Requirements**:
- Use MAGIC (Method of Automatic Generation of Importances by Calculation)
- Set up WWG (weight window generator) runs
- Iterate weight windows
- Convert between mesh-based and cell-based weight windows
- Optimize energy-dependent weight windows
- Balance computational efficiency vs. statistical quality

### 7.4 Criticality Search

Skills must perform parametric searches:

**Requirements**:
- Critical dimension search (KCODE + dimension parameter)
- Critical concentration search (material composition variation)
- Critical boron search (soluble poison)
- Automated iteration to k-eff = 1.0000 ± tolerance
- Track search history

### 7.5 Coupled Physics

Skills must support:

- **Photonuclear physics** (MODE N P G, LCOLR card)
- **Electron-photon coupling** (MODE P E)
- **Neutron-photon coupling** (MODE N P)
- **Delayed particle production** (ACT card)
- **Moving objects** (MCNP6 feature)

---

## 8. Knowledge Base Requirements

### 8.1 Documentation Access

Skills must have indexed access to:

1. **MCNP User Manual** (21 chapters):
   - Chapter 3: Introduction to MCNP Usage
   - Chapter 4: Description of MCNP6 Input
   - Chapter 5: All input cards (13 sections)
   - Chapter 6: Plotting and visualization
   - Chapter 7-8: Advanced features

2. **MCNP Theory Manual** (13 chapters):
   - Chapter 2.2: Geometry mathematics
   - Chapter 2.3: Cross-section data
   - Chapter 2.4: Physics models
   - Chapter 2.5: Tally theory
   - Chapter 2.7: Variance reduction theory
   - Chapter 2.8: Criticality theory

3. **MCNP Primers**:
   - MCNP6 Primer (general)
   - Source Primer (5 chapters)

4. **Example Database**:
   - Converted documentation examples (Chapters 9-10)
   - External example repository:
     - basic_examples/
     - criticality_examples/
     - intermediate_examples/
     - rad-protection_examples/
     - reactor-model_examples/
     - safeguards_examples/
     - unstructured-mesh_examples/
     - variance-reduction_examples/
     - MCNP6_VnV/

5. **Appendices** (25 documents):
   - File format specifications
   - Utility tool documentation
   - Conversion factors

### 8.2 Example Search Capability

Skills must:
- Search example database by keywords
- Filter by:
  - Geometry complexity
  - Physics type (neutron, photon, coupled)
  - Application domain (reactor, shielding, dosimetry)
  - Card types used
  - Variance reduction techniques
- Extract relevant snippets
- Explain example context

### 8.3 Error Pattern Database

Skills must maintain:
- Common fatal error messages with fixes
- Warning patterns and interpretations
- Geometry pitfalls (lost particles, overlaps)
- Material specification errors
- Statistical troubleshooting guides

---

## 9. Testing & Validation Strategy

### 9.1 Test Suite Requirements

Comprehensive test suite must include:

1. **Unit tests** (per skill):
   - Input parsing correctness
   - Output parsing accuracy
   - Transformation calculations
   - Unit conversions

2. **Integration tests**:
   - End-to-end input generation → validation → execution → analysis
   - Multi-skill workflows
   - Large file handling (test with 10,000+ line inputs)

3. **Validation tests**:
   - Compare skill-generated inputs with reference inputs
   - Run MCNP on generated inputs (must execute without fatal errors)
   - Verify tally results match expectations (±5% for test problems)

4. **Regression tests**:
   - Re-test on all examples after skill updates
   - Ensure backward compatibility

5. **Edge case tests** (critical):
   - 10,000+ line reactor models
   - Complex hexagonal lattices (>100 assemblies)
   - Multi-universe nested geometries (depth >5)
   - 1000+ material compositions
   - Mesh-based weight windows (>1M mesh cells)

### 9.2 Validation Benchmarks

Skills must be tested against:

1. **MCNP6 Validation & Verification Suite**:
   - Official LANL test problems
   - ICSBEP criticality benchmarks
   - SINBAD shielding benchmarks

2. **Reactor physics benchmarks**:
   - UAM (Uncertainty Analysis in Modeling) exercises
   - VERA (Virtual Environment for Reactor Applications) problems
   - BEAVRS (Benchmark for Evaluation And Validation of Reactor Simulations)

3. **Dosimetry benchmarks**:
   - ICRP reference geometries
   - Phantom models (MIRD, ICRP, voxelized)

### 9.3 Success Criteria

A skill is considered validated if:

1. **Correctness**: 100% of generated inputs execute without fatal errors
2. **Accuracy**: Results within ±5% of reference solutions (where available)
3. **Performance**: Meets performance targets (§6.1)
4. **Usability**: User can accomplish task in <5 interactions
5. **Robustness**: Handles edge cases gracefully (no crashes)

---

## 10. Success Metrics

### 10.1 Quantitative Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Input Generation Success Rate** | >95% | % of user requests resulting in executable MCNP input |
| **Fatal Error Prevention** | >90% | % of skill-generated inputs that run without fatal errors |
| **Debug Success Rate** | >80% | % of user-reported errors successfully diagnosed and fixed |
| **Performance (Large Files)** | <10s | Time to validate 10,000-line input file |
| **Statistical Check Pass Rate** | >85% | % of skill-recommended tally setups passing all 10 checks |
| **Example Match Rate** | 100% | % of documentation examples successfully parsed |

### 10.2 Qualitative Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **User Expertise Required** | Reduced | Compare time for novice vs. expert to create equivalent input |
| **Learning Curve** | Accelerated | Time to first successful MCNP run for new users |
| **Confidence in Results** | Increased | User survey: confidence in tally setup and variance reduction |
| **Documentation Accessibility** | Improved | Time to find relevant documentation section |

### 10.3 Coverage Metrics

| Feature Category | Target Coverage | Status |
|-----------------|-----------------|--------|
| **Surface Types** | 100% (all 30+ types) | TBD |
| **Cell Parameters** | 100% (all 20+ params) | TBD |
| **Data Cards** | >95% (200+ cards) | TBD |
| **Tally Types** | 100% (F1-F8, mesh) | TBD |
| **Variance Reduction** | 100% (all methods) | TBD |
| **Physics Options** | >90% | TBD |
| **Example Database** | 100% indexed | TBD |

---

## 11. Development Priorities

### Phase 1: Foundation (Weeks 1-4)
**Priority: CRITICAL**

1. Input parser and validator (`mcnp-input-validator`)
2. Basic geometry builder (`mcnp-geometry-builder`)
3. Material builder with ZAID lookup (`mcnp-material-builder`)
4. Output parser (`mcnp-output-analyzer`)
5. Fatal error debugger (`mcnp-fatal-error-debugger`)

**Success criteria**: Can create simple sphere/box models, detect common errors

### Phase 2: Core Functionality (Weeks 5-8)
**Priority: HIGH**

1. Source builder with all SDEF options (`mcnp-source-builder`)
2. Tally builder with energy binning (`mcnp-tally-builder`)
3. Geometry editor for transformations (`mcnp-transform-editor`)
4. Statistical checker (`mcnp-statistics-checker`)
5. Unit converter (`mcnp-unit-converter`)

**Success criteria**: Can create realistic shielding/dosimetry problems

### Phase 3: Advanced Geometry (Weeks 9-12)
**Priority: HIGH**

1. Lattice builder (hexagonal/rectangular) (`mcnp-lattice-builder`)
2. Macrobody decomposition (in `mcnp-geometry-builder`)
3. Universe hierarchy resolver
4. Complex transformation handler
5. Large file optimizer (streaming parser)

**Success criteria**: Can handle reactor core models with 1000+ cells

### Phase 4: Variance Reduction (Weeks 13-16)
**Priority: MEDIUM**

1. Variance reducer (`mcnp-variance-reducer`)
2. Weight window optimizer (`mcnp-ww-optimizer`)
3. Importance map generator
4. DXTRAN sphere configurator

**Success criteria**: Can optimize deep penetration shielding problems

### Phase 5: Criticality & Burnup (Weeks 17-20)
**Priority: MEDIUM**

1. Criticality analyzer (`mcnp-criticality-analyzer`)
2. KCODE builder
3. Burnup builder (`mcnp-burnup-builder`)
4. Isotopic evolution tracker

**Success criteria**: Can set up reactor criticality and depletion calculations

### Phase 6: Advanced Features (Weeks 21-24)
**Priority: LOW**

1. Mesh builder for unstructured mesh (`mcnp-mesh-builder`)
2. Parallel configurator (`mcnp-parallel-configurator`)
3. Cross-section manager (`mcnp-cross-section-manager`)
4. Legacy file updater (`mcnp-input-updater`)

**Success criteria**: Can configure HPC runs and handle MCNP5 legacy files

---

## 12. Implementation Notes

### 12.1 Technology Stack

**Recommended tools**:
- **Language**: Python 3.10+ (for Claude Skills implementation)
- **Parsing**: PLY (Python Lex-Yacc) or Lark for formal grammar
- **Data structures**: Pandas for tally data, NumPy for transformations
- **File I/O**: Pathlib, h5py (for HDF5), struct (for binary MCTAL)
- **Visualization**: Matplotlib for quick plots (optional)
- **Documentation**: Markdown with front matter (already converted)

### 12.2 Code Organization

```
mcnp-skills/
├── skills/
│   ├── input_creation/
│   │   ├── mcnp_input_generator.py
│   │   ├── mcnp_geometry_builder.py
│   │   ├── mcnp_material_builder.py
│   │   └── ...
│   ├── input_editing/
│   ├── validation/
│   ├── output_analysis/
│   ├── advanced/
│   └── utilities/
├── parsers/
│   ├── input_parser.py
│   ├── output_parser.py
│   ├── mctal_parser.py
│   └── ...
├── knowledge_base/
│   ├── documentation/  (71 markdown files)
│   ├── examples/
│   ├── error_patterns.json
│   ├── zaid_database.json
│   └── xsdir_cache.json
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── validation/
│   └── benchmarks/
└── utils/
    ├── transformations.py
    ├── unit_conversions.py
    ├── lattice_indexing.py
    └── ...
```

### 12.3 Key Algorithms

**Input parsing**:
- Use formal grammar for cell/surface cards
- Tokenize on whitespace and special characters (`:`, `#`, `(`, `)`)
- Build AST for geometry expressions
- Track line numbers for error reporting

**Geometry validation**:
- Ray-tracing to check for lost particles
- Monte Carlo sampling of random points
- CSG expression evaluation
- Overlap detection via point classification

**Transformation composition**:
- Matrix multiplication for rotations
- Translation vector addition
- Homogeneous coordinates (4x4 matrices)
- Inverse transformations for debugging

**Statistical analysis**:
- Parse TFC bins (10 checks × 8 bins = 80 values)
- Fit 1/√N curves to rel. error vs. NPS
- Chi-squared tests for distribution quality
- Convergence trend detection

**Weight window optimization**:
- Adjoint flux estimation
- Mesh-based space partitioning
- Energy group collapsing
- Iterative refinement

---

## 13. Documentation Requirements

Each skill must have:

1. **Skill description**: One-sentence summary of capability
2. **Usage examples**: 5-10 example invocations with expected outputs
3. **Input requirements**: What information the skill needs from user
4. **Output format**: What the skill returns
5. **Error handling**: How the skill handles invalid inputs
6. **Limitations**: What the skill cannot do
7. **References**: Links to relevant documentation sections

---

## 14. Open Questions & Future Enhancements

### 14.1 Open Questions

1. Should skills directly execute MCNP, or only prepare input files?
   - **Recommendation**: Prepare inputs only; user executes MCNP

2. How to handle proprietary cross-section libraries?
   - **Recommendation**: Check for library availability, warn if missing

3. Should skills support Visual Editor integration?
   - **Recommendation**: Phase 6 enhancement

4. How to handle very large MCTAL files (GB+)?
   - **Recommendation**: Streaming/chunked parsing

### 14.2 Future Enhancements (Beyond Initial Scope)

1. **Automated variance reduction tuning**: AI-driven optimization loop
2. **Real-time execution monitoring**: Parse output during MCNP execution
3. **Multi-fidelity modeling**: Couple MCNP with deterministic codes
4. **Uncertainty quantification**: Automatic sensitivity/uncertainty analysis
5. **Collaborative modeling**: Version control integration (Git)
6. **CAD import**: Convert CAD geometry to MCNP CSG
7. **Machine learning**: Predict optimal variance reduction from geometry
8. **Natural language queries**: "Show me all cells with uranium" → skill extracts

---

## 15. Risk Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Incomplete documentation parsing** | High | Medium | Prioritize most-used chapters; validate against examples |
| **Edge case not handled** | High | High | Extensive testing; graceful degradation |
| **Performance issues on large files** | Medium | Medium | Implement streaming; benchmark early |
| **Cross-section library variability** | Medium | High | Abstract xsdir interface; make library-agnostic |
| **MCNP version differences** | Low | Medium | Focus on MCNP6.3; document version limitations |
| **User expertise assumptions** | Medium | High | Provide multiple difficulty modes (beginner/expert) |

---

## 16. Conclusion

This requirements document specifies a comprehensive suite of Claude Skills for MCNP6.3 that:

✅ Covers all core MCNP capabilities (geometry, materials, sources, tallies, variance reduction)
✅ Addresses critical edge cases (large files, complex geometry, cross-section management)
✅ Provides debugging and validation tools
✅ Supports advanced features (burnup, unstructured mesh, parallel execution)
✅ Includes units/conversions and legacy file support
✅ Defines clear success metrics and testing strategy

**The skills will enable users to**:
- Create MCNP input files 10x faster
- Reduce fatal errors by 90%
- Debug problems in minutes instead of hours
- Apply best practices automatically
- Learn MCNP more effectively

**Next steps**:
1. Review and approve this requirements document
2. Prioritize Phase 1 skills
3. Develop skill templates and interfaces
4. Begin implementation starting with `mcnp-input-validator`
5. Iterate based on user feedback

---

**Document Status**: Draft v1.0 - Awaiting Review
**Last Updated**: 2025-10-30
**Contact**: [Your contact information]

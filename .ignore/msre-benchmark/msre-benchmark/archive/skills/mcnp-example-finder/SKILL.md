---
category: F
name: mcnp-example-finder
description: Find relevant MCNP example files, primers, and documentation sections for specific problem types including geometry patterns, source definitions, tally setups, and physics configurations
activation_keywords:
  - find example
  - example input
  - sample problem
  - reference problem
  - primer example
  - documentation example
  - how to model
  - example for
---

# MCNP Example Finder Skill

## Purpose

This utility skill helps Claude quickly locate relevant MCNP examples, primers, and documentation sections for specific problem types. Guides users to appropriate reference materials and working input examples for geometry, sources, tallies, physics, and advanced features.

## When to Use This Skill

- Finding example input files for specific problem types
- Locating primer sections for learning features
- Discovering reference problems for validation
- Finding documentation sections with working examples
- Learning syntax for complex features
- Adapting existing examples to new problems
- Verifying implementation approaches
- Finding best practices through examples
- Locating test problems for specific features
- Getting started with unfamiliar MCNP capabilities

## Prerequisites

- Access to MCNP documentation
- **mcnp-template-generator**: Creates starting templates
- **All other MCNP skills**: Benefit from example references
- Basic understanding of problem types
- Familiarity with MCNP card syntax

## Core Concepts

### Documentation Structure

**Main Documentation Sources**:
```
1. User Manual (mcnp631_user-manual.pdf)
   - Complete card reference
   - Syntax examples for each card
   - Chapter 3: Examples and usage

2. Primers (tutorial documents)
   - Criticality Primer
   - Source Primer
   - Geometry Primer
   - Shielding Primer
   - Step-by-step examples with explanations

3. Test Suite
   - Verification problems
   - Benchmark calculations
   - Feature demonstrations

4. Example Files (distributed with MCNP)
   - Simple demonstration problems
   - Complex real-world applications
```

### Problem Type Categories

**Geometry Examples**:
- Simple shapes (spheres, cylinders, boxes)
- Lattices (fuel assemblies, detector arrays)
- Repeated structures (FILL cards)
- Complex CAD geometries (unstructured mesh)
- Universe nesting
- Transformations (TR cards)

**Source Examples**:
- Point sources (isotropic, directional)
- Surface sources (planar, cylindrical)
- Volume sources (distributed, criticality)
- Energy distributions (mono-energetic, spectra)
- Time-dependent sources
- Fusion sources (D-T, D-D)

**Tally Examples**:
- Surface current (F1)
- Cell flux (F4)
- Detector response (F5)
- Energy deposition (F6)
- Pulse height (F8)
- Mesh tallies (FMESH, TMESH)
- Dose tallies (DE/DF cards)

**Physics Examples**:
- Thermal scattering (S(α,β))
- Photon transport
- Electron transport
- Coupled neutron-photon
- Variance reduction (IMP, WWG)
- Burnup/depletion (BURN card)

## Decision Tree: Finding Examples

```
START: Need example for MCNP problem
  |
  +--> What problem type?
  |      |
  |      +--> Geometry modeling
  |      |      ├─> Simple shapes → User Manual Ch 3.2
  |      |      ├─> Lattices → Criticality Primer Ch 5
  |      |      ├─> Repeated structures → User Manual Ch 3.3
  |      |      └─> Complex → Geometry Primer
  |      |
  |      +--> Source definition
  |      |      ├─> Point/surface → Source Primer Ch 1-2
  |      |      ├─> Volume → Source Primer Ch 3
  |      |      ├─> Criticality → Criticality Primer Ch 2
  |      |      └─> Fusion → Fusion examples
  |      |
  |      +--> Tally setup
  |      |      ├─> Basic tallies → User Manual Ch 3.4
  |      |      ├─> Dose → Shielding Primer Ch 4
  |      |      ├─> Pulse height → User Manual F8 section
  |      |      └─> Mesh → User Manual FMESH section
  |      |
  |      +--> Physics configuration
  |      |      ├─> Thermal neutrons → Criticality Primer
  |      |      ├─> Photon transport → Shielding examples
  |      |      ├─> Electron → User Manual MODE E
  |      |      └─> Burnup → BURN card examples
  |      |
  |      └─> Variance reduction
  |             ├─> Importance → Shielding Primer Ch 5
  |             ├─> Weight windows → WWG examples
  |             └─> DXTRAN → User Manual DXTRAN section
  |
  +--> Find in documentation
  |      ├─> Check primer table of contents
  |      ├─> Search user manual index
  |      ├─> Look for "example" or "sample problem"
  |      └─> Check test suite files
  |
  +--> Adapt example to problem
  |      ├─> Identify key features used
  |      ├─> Modify dimensions/materials as needed
  |      ├─> Update source/tally as required
  |      └─> Verify syntax with manual
  |
  └─> Document source
         └─> Comment: "Based on [primer/manual] example"
```

## Tool Invocation

This skill includes a Python implementation for automated example searching.

### Importing the Tool

```python
from mcnp_example_finder import MCNPExampleFinder
finder = MCNPExampleFinder()
```

### Basic Usage

```python
# Search for examples
examples = finder.search_examples('lattice')

for ex in examples:
    print(f"{ex['file']}: {ex['description']}")
```

### Integration with MCNP Workflow

```python
from mcnp_example_finder import MCNPExampleFinder

finder = MCNPExampleFinder()
examples = finder.search_examples_by_category('criticality')

for ex in examples[:5]:
    print(f"Example: {ex['name']}")
    print(f"  File: {ex['file']}")
    print(f"  Description: {ex['description']}")
```

---

## Example Locations by Problem Type

### Criticality Problems

**Primer**: Criticality Primer (LA-UR-15-29136)

**Key Examples**:
```
Chapter 2: KCODE Basics
  - Example 1: Bare sphere (Godiva)
  - Example 2: Reflected sphere
  - Example 3: Cylinder with reflector

Chapter 5: Lattice Problems
  - Example 9: Simple fuel pin lattice
  - Example 10: Fuel assembly
  - Example 11: Core with control rods

Chapter 6: Source Convergence
  - Examples with Shannon entropy
  - KSRC card usage
```

**Location in Documentation**:
```
markdown_docs/primers/criticality_primer/
  - 02_Getting_Started.md
  - 05_Lattice_Problems.md
  - 06_Advanced_Topics.md
```

### Shielding Problems

**Primer**: Shielding Primer (X-5 Monte Carlo Team)

**Key Examples**:
```
Chapter 2: Simple Point Source
  - Point isotropic source
  - Detector tallies (F5)
  - Dose conversion (DE/DF)

Chapter 3: Distributed Sources
  - Volume source (cylindrical)
  - Surface source
  - Energy distributions

Chapter 5: Variance Reduction
  - Importance splitting
  - Weight windows
  - Geometry splitting
```

**Location**: Often in test suite or example directories

### Source Definition

**Primer**: Source Primer (LA-UR-13-20140)

**Key Examples**:
```
Chapter 1: Simple Sources
  - Point isotropic
  - Directional beam
  - Surface source

Chapter 2: SDEF Card Details
  - Energy distributions (SI, SP)
  - Directional distributions
  - Position distributions

Chapter 3: Advanced Sources
  - Volume sources
  - User-defined distributions
  - Source transformations
```

**Location in Documentation**:
```
markdown_docs/primers/source_primer/
  - 01_Introduction.md
  - 02_SDEF_Card.md
  - 03_Advanced_Features.md
```

### Geometry Modeling

**Primer**: Geometry Primer (unofficial, various sources)

**Key Sections**:
```
Basic Surfaces:
  - Planes (P, PX, PY, PZ)
  - Spheres (S, SO, SX, SY, SZ)
  - Cylinders (C, CX, CY, CZ)

Boolean Operations:
  - Union (:)
  - Intersection (space)
  - Complement (#)

Advanced:
  - Macrobodies (RPP, SPH, RCC)
  - General quadrics (GQ, SQ)
  - Lattices (LAT, FILL)
```

**User Manual Examples**:
```
Chapter 3: Description of Input Cards
  - §3.3.1: Surface examples
  - §3.3.2: Cell examples
  - §3.3.3: Lattice examples
```

## Use Case 1: Find Fuel Pin Lattice Example

**Problem**: Need to model LWR fuel assembly with pins in square lattice

**Search Process**:
```
Step 1: Identify problem type
  Type: Criticality, lattice geometry

Step 2: Check Criticality Primer
  Chapter 5: Lattice Problems
  Example 9: Simple Fuel Pin Lattice
  → markdown_docs/primers/criticality_primer/05_Lattice_Problems.md

Step 3: Review example structure
  - PIN universe (fuel rod)
  - Lattice cell with LAT=1 (square)
  - FILL card with universe numbers

Step 4: Key features to extract
  - Universe definition pattern
  - LAT card syntax (LAT=1 for square)
  - FILL card format
```

**Example Structure from Primer**:
```
c Pin cell universe (U=1)
10  1  -10.2  -10        U=1  IMP:N=1  $ UO2 fuel
11  0         10 -11     U=1  IMP:N=1  $ Gap
12  2  -6.5   11         U=1  IMP:N=1  $ Clad

c Lattice cell
20  3  -1.0   -20  LAT=1  U=2  IMP:N=1  FILL=-5:5 -5:5 0:0
                1 1 1 1 1 1 1 1 1 1 1  $ 11x11 array
                ...                       $ Repeat for all rows

c Main cell
30  0  -30  FILL=2  IMP:N=1           $ Fill with lattice universe
```

## Use Case 2: Find Dose Tally Example

**Problem**: Calculate dose rate from neutron source

**Search Process**:
```
Step 1: Identify keywords
  Keywords: Dose, dose conversion, DE/DF, shielding

Step 2: Check Shielding Primer
  Chapter 4: Dose Tallies
  → Shows DE/DF card usage with flux tallies

Step 3: Check User Manual
  Chapter 5.7: Tally Cards
  § F4 tally with dose conversion
```

**Example Pattern**:
```
c Flux tally
F4:N  10                    $ Average flux in cell 10
c
c Energy bins (must match DE card)
E4  0  0.01  0.1  1.0  10.0  20.0
c
c Dose conversion factors (rem/hour per particle/cm²-s)
DE4  0  0.01  0.1  1.0  10.0  20.0
DF4  3.67E-6  5.08E-6  9.26E-6  1.32E-5  1.45E-5  1.47E-5
c
c Multiply F4 result by dose factor
FM4  (constant for flux-to-dose conversion)
```

## Use Case 3: Find Weight Window Example

**Problem**: Deep penetration shielding, need variance reduction

**Search Process**:
```
Step 1: Identify technique
  Technique: Weight windows (WWG)

Step 2: Check Shielding Primer
  Chapter 5: Variance Reduction
  Example: WWG card usage

Step 3: Check User Manual
  §5.8: Variance Reduction Cards
  WWG card syntax and MESH card
```

**Example Pattern**:
```
c Weight window generator
WWG  10  0                  $ Generate for tally 10, no iterations
c
c Mesh for weight window generation
MESH  GEOM=xyz              $ Cartesian mesh
      ORIGIN=-50 -50 -50
      IMESH=50  IINTS=10    $ X boundaries
      JMESH=50  JINTS=10    $ Y boundaries
      KMESH=50  KINTS=10    $ Z boundaries
c
c On first run: generates weight window mesh
c On subsequent runs: uses generated windows
```

## Use Case 4: Find Fusion Source Example

**Problem**: Model D-T fusion neutron source

**Search Process**:
```
Step 1: Identify source type
  Type: Fusion, 14 MeV neutrons, anisotropic

Step 2: Check Source Primer
  Advanced examples for fusion
  → May need test suite examples

Step 3: Check MCNP test problems
  Look for "fusion" or "DT" examples
```

**Example Pattern**:
```
c D-T fusion neutron source
c 14.1 MeV neutrons, anisotropic emission
SDEF  PAR=1  ERG=14.1  POS=0 0 0  VEC=0 0 1  DIR=D1
c
c Angular distribution (forward-peaked)
SI1  -1  1                  $ Cosine bins
SP1   0  1                  $ Linear between -1 and 1 (isotropic)
c For anisotropic:
c SP1  D  0.5  1.5          $ Weighted toward forward direction
```

## Integration with Other Skills

### All MCNP Skills Benefit
Example-finder supports all other skills by providing reference implementations.

### Typical Workflow:
```
1. User asks: "Create fuel assembly model"
2. mcnp-template-generator: Creates basic structure
3. example-finder: Locates lattice example
4. mcnp-geometry-builder: Implements using example pattern
5. mcnp-criticality-analyzer: Validates against similar problems
```

## Documentation Quick Reference

### Primers
```
Criticality Primer: LA-UR-15-29136
  - Getting started (Ch 2)
  - Basic problems (Ch 3-4)
  - Lattices (Ch 5)
  - Advanced (Ch 6-7)

Source Primer: LA-UR-13-20140
  - Simple sources (Ch 1)
  - SDEF card (Ch 2)
  - Advanced (Ch 3-4)

Shielding Primer: X-5 Monte Carlo Team
  - Point sources (Ch 2)
  - Distributed sources (Ch 3)
  - Dose tallies (Ch 4)
  - Variance reduction (Ch 5)
```

### User Manual Key Chapters
```
Chapter 3: Input Overview
  - §3.2: Geometry examples
  - §3.3: Lattice examples
  - §3.4: Tally examples

Chapter 5: Card Descriptions
  - §5.1-5.3: Cell, Surface, Data cards
  - §5.4: Source cards (SDEF, SI, SP)
  - §5.6: Tally cards (F1-F8)
  - §5.7: Tally modification (E, T, DE, DF)
  - §5.8: Variance reduction
```

## Best Practices

1. **Start with Primers**: More tutorial than manual
2. **Check Test Suite**: Verified working examples
3. **Verify Syntax**: Cross-reference with manual
4. **Adapt, Don't Copy**: Understand before using
5. **Document Source**: Credit example origin
6. **Test Modifications**: Small changes, verify results
7. **Build Complexity**: Start simple, add features
8. **Compare Results**: Validate against similar problems

## References

- **MCNP Primers**: Tutorial documents for specific topics
- **User Manual**: Chapter 3 (examples), Chapter 5 (card syntax)
- **Test Suite**: MCNP installation test problems
- **Related Skills**: All MCNP skills benefit from examples
- **Documentation**: markdown_docs/ directory structure

---

**End of MCNP Example Finder Skill**

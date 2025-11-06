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
version: "2.0.0"
---

# MCNP Example Finder Skill

## Purpose

Quickly locate relevant MCNP examples, primers, and documentation sections for specific problem types. Guides users to appropriate reference materials and working input examples for geometry, sources, tallies, physics, and advanced features.

## When to Use This Skill

- Finding example input files for specific problem types
- Locating primer sections for learning features
- Discovering reference problems for validation
- Finding documentation with working syntax examples
- Learning complex features through examples
- Adapting existing examples to new problems
- Getting started with unfamiliar MCNP capabilities

## Prerequisites

- **example_catalog.md**: Comprehensive catalog of examples by problem type
- **mcnp-template-generator**: Creates starting templates
- Basic understanding of MCNP problem types

## Core Concepts

### Documentation Sources

**Four Main Sources:**
```
1. Criticality Primer (LA-UR-15-29136)
   - KCODE basics, lattices, control rods
   - Fuel assemblies, universe nesting

2. Source Primer (LA-UR-13-20140)
   - SDEF card details, distributions
   - Point, surface, volume sources

3. Shielding Primer (X-5 Monte Carlo Team)
   - Dose tallies, variance reduction
   - Point detectors, deep penetration

4. User Manual (mcnp631_user-manual.pdf)
   - Complete card syntax
   - Chapter 3: Examples and usage
```

**See example_catalog.md** for comprehensive catalog organized by problem type and documentation source.

### Problem Type Categories

| Category | Examples | Primary Source |
|----------|----------|----------------|
| **Criticality** | Godiva, fuel lattices, control rods | Criticality Primer |
| **Shielding** | Point sources, dose conversion | Shielding Primer |
| **Geometry** | Lattices, transformations, macrobodies | User Manual Ch 3.2-3.3 |
| **Sources** | SDEF, energy distributions, fusion | Source Primer |
| **Tallies** | F1-F8, mesh tallies, dose | User Manual Ch 3.4 |
| **Variance Reduction** | IMP, WWG, DXTRAN | Shielding Primer Ch 5 |

## Decision Tree: Finding Examples

```
START: Need example for MCNP problem
  |
  +--> What problem type?
  |      |
  |      +--> Geometry modeling
  |      |      ├─> Simple shapes → User Manual Ch 3.2
  |      |      ├─> Lattices → Criticality Primer Ch 5
  |      |      └─> Repeated structures → User Manual Ch 3.3
  |      |
  |      +--> Source definition
  |      |      ├─> Point/surface → Source Primer Ch 1-2
  |      |      ├─> Volume → Source Primer Ch 3
  |      |      └─> Criticality → Criticality Primer Ch 2
  |      |
  |      +--> Tally setup
  |      |      ├─> Basic tallies → User Manual Ch 3.4
  |      |      ├─> Dose → Shielding Primer Ch 4
  |      |      └─> Mesh → User Manual FMESH section
  |      |
  |      +--> Physics configuration
  |      |      ├─> Thermal neutrons → Criticality Primer
  |      |      ├─> Photon transport → Shielding examples
  |      |      └─> Burnup → BURN card examples
  |      |
  |      └─> Variance reduction
  |             ├─> Importance → Shielding Primer Ch 5
  |             ├─> Weight windows → WWG examples
  |             └─> DXTRAN → User Manual DXTRAN section
  |
  +--> Find in documentation
  |      ├─> Check example_catalog.md
  |      ├─> Search primer table of contents
  |      └─> Check test suite files
  |
  +--> Adapt example to problem
  |      ├─> Identify key features used
  |      ├─> Modify dimensions/materials as needed
  |      └─> Verify syntax with manual
  |
  └─> Document source
         └─> Comment: "Based on [primer/manual] example"
```

## Tool Invocation

Python implementation for automated example searching.

### Basic Usage

```python
from mcnp_example_finder import MCNPExampleFinder

# Initialize
finder = MCNPExampleFinder()

# Search by keyword
examples = finder.search_examples('lattice')

for ex in examples:
    print(f"{ex['name']}: {ex['description']}")
    print(f"  Location: {ex['location']}")

# Search by category
criticality_examples = finder.search_by_category('criticality')

# Find card examples
sdef_examples = finder.find_card_examples('SDEF')
```

**See scripts/README.md** for detailed Python API documentation and integration examples.

---

## Use Case 1: Find Fuel Pin Lattice Example

**Problem**: Model LWR fuel assembly with pins in square lattice

**Solution**:
1. Identify type: Criticality, lattice geometry
2. Check **example_catalog.md § Reactor Physics**
3. Find: Criticality Primer Ch 5, Example 9 (Simple Fuel Pin Lattice)
4. Extract key pattern:

```
c Pin cell universe (U=1)
10  1  -10.2  -10        U=1  IMP:N=1  $ UO2 fuel
11  0         10 -11     U=1  IMP:N=1  $ Gap
12  2  -6.5   11         U=1  IMP:N=1  $ Clad

c Lattice cell
20  3  -1.0   -20  LAT=1  U=2  IMP:N=1  FILL=-5:5 -5:5 0:0
                1 1 1 1 1 1 1 1 1 1 1  $ 11x11 array

c Main cell
30  0  -30  FILL=2  IMP:N=1           $ Fill with lattice universe
```

**Key Features**: Universe definition (U=1), LAT=1 (square), FILL array

## Use Case 2: Find Dose Tally Example

**Problem**: Calculate dose rate from neutron source

**Solution**:
1. Keywords: Dose, DE/DF cards, shielding
2. Check **example_catalog.md § Dose Tallies**
3. Find: Shielding Primer Ch 4 (Dose Tallies)
4. Extract pattern:

```
c Flux tally
F4:N  10                    $ Average flux in cell 10

c Energy bins (must match DE card)
E4  0  0.01  0.1  1.0  10.0  20.0

c Dose conversion factors (rem/hour per particle/cm²-s)
DE4  0  0.01  0.1  1.0  10.0  20.0
DF4  3.67E-6  5.08E-6  9.26E-6  1.32E-5  1.45E-5  1.47E-5
```

**Key Features**: F4 flux tally, E4 energy bins, DE4/DF4 dose conversion

## Use Case 3: Find Weight Window Example

**Problem**: Deep penetration shielding, need variance reduction

**Solution**:
1. Technique: Weight windows (WWG)
2. Check **example_catalog.md § Variance Reduction**
3. Find: Shielding Primer Ch 5 (Variance Reduction)
4. Extract pattern:

```
c Weight window generator
WWG  10  0                  $ Generate for tally 10, no iterations

c Mesh for weight window generation
MESH  GEOM=xyz              $ Cartesian mesh
      ORIGIN=-50 -50 -50
      IMESH=50  IINTS=10    $ X boundaries
      JMESH=50  JINTS=10    $ Y boundaries
      KMESH=50  KINTS=10    $ Z boundaries
```

**Key Features**: WWG card for tally, MESH card for spatial binning

## Use Case 4: Find Fusion Source Example

**Problem**: Model D-T fusion neutron source

**Solution**:
1. Type: Fusion, 14.1 MeV neutrons
2. Check **example_catalog.md § Source Examples by Type**
3. Extract pattern:

```
c D-T fusion neutron source (14.1 MeV, anisotropic)
SDEF  PAR=1  ERG=14.1  POS=0 0 0  VEC=0 0 1  DIR=D1

c Angular distribution
SI1  -1  1                  $ Cosine bins
SP1   0  1                  $ Isotropic
c For anisotropic:
c SP1  D  0.5  1.5          $ Forward-peaked
```

**Key Features**: SDEF with ERG=14.1, DIR=D1 for angular distribution

## Integration with Other Skills

Example-finder supports all other MCNP skills by providing reference implementations.

### Typical Workflow:
```
1. User: "Create fuel assembly model"
2. mcnp-template-generator: Creates basic structure
3. mcnp-example-finder: Locates lattice example
4. mcnp-geometry-builder: Implements using example pattern
5. mcnp-best-practices-checker: Validates approach
```

## Quick Reference: Where to Find Examples

| Need Example For | Check First | Also See |
|-----------------|-------------|----------|
| KCODE setup | Criticality Primer Ch 2 | example_catalog.md §1 |
| Fuel lattice | Criticality Primer Ch 5 | example_catalog.md §4 |
| SDEF source | Source Primer Ch 1-2 | example_catalog.md §2 |
| Dose tally | Shielding Primer Ch 4 | example_catalog.md §3 |
| Weight windows | Shielding Primer Ch 5 | example_catalog.md §5 |
| Basic geometry | User Manual Ch 3.2 | example_catalog.md §4 |
| F1-F8 tallies | User Manual Ch 3.4 | example_catalog.md §5 |

**Always consult example_catalog.md for comprehensive details, locations, and complete example listings.**

## Best Practices

1. **Start with Primers**: More tutorial-focused than manual
2. **Check Test Suite**: Verified working examples
3. **Verify Syntax**: Cross-reference with manual
4. **Adapt, Don't Copy**: Understand features before using
5. **Document Source**: Credit example origin in comments
6. **Test Modifications**: Small changes, verify results
7. **Build Incrementally**: Start simple, add features
8. **Use Catalog**: Reference example_catalog.md for comprehensive listings

## References

- **example_catalog.md**: Complete catalog of examples organized by problem type
- **scripts/README.md**: Python tools for automated example searching
- **MCNP Primers**: Tutorial documents (markdown_docs/primers/)
- **User Manual**: Chapter 3 (examples), Chapter 5 (card syntax)
- **Test Suite**: MCNP installation test problems

---

**End of MCNP Example Finder Skill**

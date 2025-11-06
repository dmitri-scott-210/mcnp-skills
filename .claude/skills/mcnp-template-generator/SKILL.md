---
category: A
name: mcnp-template-generator
description: Create reusable MCNP input templates for common problem types including shielding, criticality, dose calculations, and activation analysis
version: 2.0.0
activation_keywords:
  - template
  - generate template
  - input template
  - starting point
  - example input
  - boilerplate
---

# MCNP Template Generator Skill

## Purpose

Generate reusable MCNP input templates for common problem types to accelerate input development, ensure best practices, and maintain consistency across projects.

## When to Use This Skill

- Starting new MCNP project (need quick starting point)
- Repeating similar simulations (parameter studies, shielding variations)
- Training new users (provide standard examples)
- Ensuring team consistency
- Rapid prototyping of geometries

## Prerequisites

- **mcnp-input-builder**: Input file structure
- **mcnp-geometry-builder**: Basic geometry
- **mcnp-material-builder**: Material definitions
- **mcnp-source-builder**: Source specifications
- **mcnp-tally-builder**: Tally definitions

## Core Concepts - Quick Reference

### Template Types

| Type | Use Case | Customization |
|------|----------|---------------|
| **Complete** | Ready to run with minor edits | Replace parameters |
| **Skeleton** | Structure only | Fill in all sections |
| **Parameterized** | Script-generated | Modify Python script |

### Common Problem Templates

| Problem Type | Template | Key Features |
|--------------|----------|--------------|
| Shielding | Simple sphere, multilayer slab | Point source, dose tallies |
| Criticality | Bare sphere, reflected sphere | KCODE, keff tallies |
| Dose | Ambient dose, effective dose | DE/DF cards, ICRP factors |
| Activation | Simple activation | BURN card, decay photons |

**Detailed Reference**: See `problem_type_catalog.md` for complete template descriptions.

## Python Tool

### template_generator.py - Create Custom Templates

```bash
# Interactive mode
python template_generator.py

# Generate shielding template
python template_generator.py --type shielding --geometry sphere

# Generate criticality template
python template_generator.py --type criticality --geometry sphere

# Custom output
python template_generator.py --type dose --output my_dose.i
```

**Detailed Documentation**: See `scripts/README.md` for usage guide.

## Decision Tree: Template Selection

```
START: What problem type?
  |
  +--> Shielding
  |      ├─> Simple geometry → shielding_sphere.i
  |      └─> Multilayer → shielding_slab.i
  |
  +--> Criticality
  |      ├─> Bare system → criticality_bare.i
  |      └─> Reflected → criticality_reflected.i
  |
  +--> Dose
  |      ├─> Point dose → dose_ambient.i
  |      └─> Organ dose → dose_effective.i
  |
  └─> Activation
         └─> Simple → activation_simple.i
```

## Use Cases

### Use Case 1: Quick Shielding Study

**Objective**: Dose from point source through lead shield

**Using Template**:
```bash
# Copy template
python template_generator.py --type shielding --geometry sphere --output shield_study.i

# Edit parameters (opens in editor)
# - Source strength: 1.0E10 n/s
# - Shield material: Lead (Z=82)
# - Shield thickness: 5 cm
# - Detector distance: 100 cm

# Run MCNP
mcnp6 inp=shield_study.i
```

**Result**: Complete input in <5 minutes

### Use Case 2: Criticality Calculation

**Objective**: keff of bare U-235 sphere

**Using Template**:
```bash
# Generate template
python template_generator.py --type criticality --geometry sphere

# Template includes:
# - KCODE card pre-configured
# - Material M1 (U-235 metal)
# - F4 and F7 tallies
# - Appropriate NPS

# Modify sphere radius, run
mcnp6 inp=criticality_sphere.i
```

### Use Case 3: Custom Template Library

**Objective**: Create project-specific templates

**Workflow**:
```bash
# Create directory
mkdir my_project_templates

# Generate base templates
python template_generator.py --type shielding --output my_project_templates/base_shield.i
python template_generator.py --type dose --output my_project_templates/base_dose.i

# Customize templates with project-specific:
# - Material library references
# - Standard tally configurations
# - Comment headers
# - NPS defaults

# Use templates for all project simulations
```

## Template Catalog

### Shielding Templates

**shielding_sphere.i** - Point source, spherical shield
- Simple geometry (2 cells)
- Point isotropic source
- F2 current tally at shield surface
- F4 flux tally beyond shield

**shielding_slab.i** - Plane source, multilayer slab
- 3-layer geometry (configurable)
- Planar source
- F2 transmission tally
- Energy bins for spectrum

### Criticality Templates

**criticality_bare.i** - Bare fissile sphere
- Single sphere geometry
- KCODE configured
- F4 flux, F7 fission tallies
- Standard materials (U-235, Pu-239)

**criticality_reflected.i** - Reflected sphere
- Core + reflector geometry
- KCODE with skip/run cycles
- Detailed tallies
- Water or beryllium reflector options

### Dose Templates

**dose_ambient.i** - Ambient dose equivalent
- Point source
- H*(10) dose conversion (ICRP-74)
- DE/DF cards pre-configured
- F6 or F4+FM tallies

**dose_effective.i** - Effective dose
- Phantom geometry included
- Organ tallies
- ICRP-116 coefficients
- Energy-dependent conversion

### Activation Templates

**activation_simple.i** - Basic activation
- Target material
- BURN card configured
- Decay photon tallies
- Post-irradiation times

## Template Customization

### Quick Parameter Replacement

Templates use `[PARAMETER]` placeholders:

```
c ===== PARAMETERS TO CUSTOMIZE =====
c [SOURCE_STRENGTH] = Source strength (particles/s)
c [SHIELD_THICKNESS] = Shield thickness (cm)
c [SHIELD_MATERIAL] = Material number
c =====================================

M1  [SHIELD_MATERIAL]  -[DENSITY]  $ Shield material
```

**Find and replace**:
```bash
sed -i 's/\[SOURCE_STRENGTH\]/1.0E10/g' input.i
sed -i 's/\[SHIELD_THICKNESS\]/5.0/g' input.i
```

### Script-Based Generation

Use Python for complex parameterization:

```python
# generate_from_template.py
import sys

template = open('template.i').read()

# Replace parameters
params = {
    'RADIUS': 10.0,
    'THICKNESS': 5.0,
    'SOURCE': '1.0E10'
}

for key, value in params.items():
    template = template.replace(f'[{key}]', str(value))

# Write output
with open('generated.i', 'w') as f:
    f.write(template)
```

## Validation Checklist

- [ ] Template has header with description and instructions
- [ ] All [PARAMETER] placeholders documented
- [ ] Geometry is correct (no overlaps, verified with plots)
- [ ] Materials realistic (densities, compositions)
- [ ] Source appropriate for problem type
- [ ] Tallies relevant to physics question
- [ ] NPS sufficient for statistics (or marked as [NPS])
- [ ] MODE card appropriate (N, P, N P, etc.)
- [ ] KCODE configured correctly (if criticality)
- [ ] Comments explain key choices

## Best Practices

1. **Document Parameters**: List all customizable values in header
2. **Use Clear Placeholders**: `[VALUE]` or `999.99` (easy to find)
3. **Include Instructions**: Step-by-step customization guide
4. **Test Templates**: Verify they run without errors
5. **Standard Organization**: Consistent structure across templates
6. **Version Control**: Track template changes
7. **Minimal Customization**: Keep required edits to minimum
8. **Realistic Defaults**: Use physically reasonable values
9. **Comment Rationale**: Explain non-obvious choices
10. **Provide Examples**: Include sample customized versions

## Resources and References

### Pre-Made Templates
- `templates/shielding_sphere.i` - Point source shielding
- `templates/shielding_slab.i` - Slab transmission
- `templates/criticality_bare.i` - Bare sphere keff
- `templates/criticality_reflected.i` - Reflected sphere
- `templates/dose_ambient.i` - Ambient dose equivalent
- `templates/activation_simple.i` - Basic activation

### Python Tools
- `scripts/template_generator.py` - Generate custom templates
- `scripts/README.md` - Tool documentation

### Reference Files
- `problem_type_catalog.md` - Complete template descriptions
- `template_customization_guide.md` - Advanced customization techniques

### Related MCNP Skills
- **mcnp-input-builder**: Basic input structure
- **mcnp-geometry-builder**: Geometry creation
- **mcnp-material-builder**: Material definitions
- **mcnp-source-builder**: Source specifications
- **mcnp-tally-builder**: Tally configurations

### External Resources
- **MCNP Primer**: Example problems by problem type
- **LA-UR-16-29043**: MCNP6.2 Feature Enhancements
- **Project Templates**: Organization-specific libraries

---

**Version**: 2.0.0
**Last Updated**: 2025-11-06
**Status**: Production-ready with template library

---

**End of MCNP Template Generator Skill**

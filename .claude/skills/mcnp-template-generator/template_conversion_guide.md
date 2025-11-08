# Template Conversion Guide
## Converting Existing MCNP Inputs to Jinja2 Templates

This guide details the process of converting an existing MCNP input file into a parameterized Jinja2 template.

## Step 1: Identify Fixed vs. Variable Content

**Fixed content** (stays the same across all scenarios):
- Core reactor geometry (if constant)
- Structural materials (if constant)
- Most physics cards (MODE, KCODE, etc.)
- Source definition (if constant)

**Variable content** (changes between scenarios):
- Control rod/drum positions
- Material compositions (enrichment, burnup state)
- Test assembly configurations
- Operational parameters (power, temperature)

## Step 2: Mark Template Boundaries

**Choose strategic insertion points** for template variables:

**Good insertion points**:
- Between major comment blocks
- At start of repeated geometry sections
- Before/after material definitions

**Bad insertion points**:
- Middle of cell definition
- Inside surface definitions
- Breaking MCNP syntax

## Step 3: Replace Variable Sections

### Example: Control Drum Surfaces

**Original MCNP input**:
```mcnp
c   ---------------------------------------------------------------------------
c      CONTROL DRUM POSITION SURFACES
c   ---------------------------------------------------------------------------
c
  981   c/z   48.0375  -18.1425  9.195       $ DRUM E1 AT 85 DEGREES
  982   c/z   31.5218  -27.3612  9.195       $ DRUM E2 AT 85 DEGREES
c
  983   c/z   27.3612  -31.5218  9.195       $ DRUM E3 AT 85 DEGREES
  984   c/z   18.1425  -48.0375  9.195       $ DRUM E4 AT 85 DEGREES
c
```

**Template version**:
```jinja2
c   ---------------------------------------------------------------------------
c      CONTROL DRUM POSITION SURFACES
c   ---------------------------------------------------------------------------
{{oscc_surfaces}}
```

**Rendering script generates**:
```python
oscc_surfaces[cycle] = """c
  981   c/z   48.0375  -18.1425  9.195       $ DRUM E1 AT 85 DEGREES
  982   c/z   31.5218  -27.3612  9.195       $ DRUM E2 AT 85 DEGREES
c
  983   c/z   27.3612  -31.5218  9.195       $ DRUM E3 AT 85 DEGREES
  984   c/z   18.1425  -48.0375  9.195       $ DRUM E4 AT 85 DEGREES
c
"""
```

### Example: Material Definitions

**Original**:
```mcnp
m1  $ UO2 fuel, 4.5% enriched
   92235.70c  0.045
   92238.70c  0.955
    8016.70c  2.0
```

**Template**:
```jinja2
{{fuel_material}}
```

**Rendering**:
```python
# For enrichment study
enrichments = [3.0, 3.5, 4.0, 4.5, 5.0]
for enr in enrichments:
    fuel_material = f"""m1  $ UO2 fuel, {enr}% enriched
   92235.70c  {enr/100:.6f}
   92238.70c  {1-enr/100:.6f}
    8016.70c  2.0
"""
    template.render(fuel_material=fuel_material)
```

## Step 4: Validate Template

**Checks**:
1. Template is valid MCNP input (can run standalone with placeholders as comments)
2. Placeholder names are descriptive ({{oscc_surfaces}} not {{var1}})
3. Minimal number of placeholders (3-6 typical, >10 is complex)
4. All placeholders documented

## Step 5: Test Rendering

**Minimal test**:
```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('test.template')

# Test with dummy data
output = template.render(
    oscc_surfaces="c\n  981 c/z 0 0 1\n",
    ne_cells="c\n  701 10 -1.0 -701\n"
)

print(output)

# Check for leftover placeholders
assert '{{' not in output, "Template variables not fully replaced"
```

## Complete Workflow Example

See `example_inputs/conversion_workflow_example.py`

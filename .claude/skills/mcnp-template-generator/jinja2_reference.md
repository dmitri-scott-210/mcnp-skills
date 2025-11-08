# Jinja2 Reference for MCNP Templates
## Template Syntax and Best Practices

This reference covers Jinja2 template syntax specifically for MCNP input generation.

## Basic Variable Substitution

### Simple Variables

**Template**:
```jinja2
c Control drum surfaces
{{oscc_surfaces}}

c Neck shim cells
{{ne_cells}}
{{se_cells}}
```

**Python rendering**:
```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('base.template')

output = template.render(
    oscc_surfaces=drum_surfaces_text,
    ne_cells=ne_cells_text,
    se_cells=se_cells_text
)
```

### Multi-Line String Substitution

**Python preparation**:
```python
# Multi-line MCNP content
oscc_surfaces = """c
  981   c/z   48.0375  -18.1425  9.195       $ DRUM E1 AT 85 DEGREES
  982   c/z   31.5218  -27.3612  9.195       $ DRUM E2 AT 85 DEGREES
c
  983   c/z   27.3612  -31.5218  9.195       $ DRUM E3 AT 85 DEGREES
  984   c/z   18.1425  -48.0375  9.195       $ DRUM E4 AT 85 DEGREES
"""

# Note: Leading 'c' and proper indentation preserved
```

**Result in rendered template**:
```mcnp
c
  981   c/z   48.0375  -18.1425  9.195       $ DRUM E1 AT 85 DEGREES
  982   c/z   31.5218  -27.3612  9.195       $ DRUM E2 AT 85 DEGREES
c
  983   c/z   27.3612  -31.5218  9.195       $ DRUM E3 AT 85 DEGREES
  984   c/z   18.1425  -48.0375  9.195       $ DRUM E4 AT 85 DEGREES
```

## Why Keep It Simple?

**For MCNP templates, use ONLY simple variable substitution** `{{variable}}`.

**Avoid**:
- Loops in template: `{% for ... %}`
- Conditionals in template: `{% if ... %}`
- Filters in template: `{{ value|filter }}`

**Rationale**:
1. Keep template valid MCNP input (can test standalone)
2. Logic belongs in Python (more maintainable)
3. Easier debugging (template is static structure)

## Template Organization

### Recommended Structure

```jinja2
c ==============================================================================
c    MCNP INPUT GENERATED FROM TEMPLATE
c    Template: base_model.template
c    Cycle: {{cycle_id}}
c    Generated: {{generation_date}}
c ==============================================================================
c
c    BLOCK 1: CELL CARDS
c
c --- Fixed Core Geometry ---
  1  1  -2.7   -10  100  -200          $ Core structure
  2  2  -1.0   -20  200  -300          $ Moderator
c
c --- Variable Test Assembly ---
{{test_assembly_cells}}
c
c --- End of Cell Block ---

c
c ==============================================================================
c    BLOCK 2: SURFACE CARDS
c ==============================================================================
c
c --- Fixed Surfaces ---
  10  rpp  0 100  0 100  0 100          $ Core boundary
  20  rpp  0 120  0 120  0 120          $ Tank boundary
c
c --- Variable Control Positions ---
{{control_surfaces}}
c
c --- End of Surface Block ---

c
c ==============================================================================
c    BLOCK 3: DATA CARDS
c ==============================================================================
c
mode n p
c
c --- Materials ---
{{materials}}
c
c --- Physics Cards ---
phys:n 20.0
c
c --- Source ---
{{source_definition}}
c
c --- Tallies ---
f4:n  1
e4    0.1 1.0 10.0
c
nps {{nps}}
```

### Variable Naming Conventions

**Good variable names**:
```python
oscc_surfaces        # Outer shim control cylinders - surfaces
ne_cells            # Northeast neck shim - cells
test_assembly_cells # Test assembly geometry
fuel_materials      # Fuel material definitions
```

**Bad variable names**:
```python
var1, var2, var3    # Non-descriptive
s, c, m             # Too short
the_surfaces_for_the_control_drums  # Too long
```

## Common Patterns

### Pattern 1: Static + Variable Content

**Template**:
```jinja2
c --- Reactor Core (Static) ---
  1  1  -2.7   -10
  2  2  -1.0   -20  10
  3  3  -8.0   -30  20

c --- Test Section (Variable) ---
{{test_section}}

c --- End of Cells ---
```

**Python**:
```python
# Different test assemblies
test_sections = {
    'config_A': """c  
  100  10  -5.0   -100
  101  11  -3.5   -101  100
""",
    'config_B': """c
  100  12  -4.8   -100
  101  13  -3.2   -101  100
"""
}

for config, test_section in test_sections.items():
    output = template.render(test_section=test_section)
    write_output(f'input_{config}.i', output)
```

### Pattern 2: Multiple Independent Variables

**Template**:
```jinja2
c --- Cell Block ---
{{core_cells}}
{{test_cells}}
{{shield_cells}}

c --- Surface Block ---
{{core_surfaces}}
{{test_surfaces}}

c --- Data Block ---
{{core_materials}}
{{test_materials}}
```

**Python**:
```python
# All variables prepared independently
output = template.render(
    core_cells=core_cells_text,
    test_cells=test_cells_text,
    shield_cells=shield_cells_text,
    core_surfaces=core_surfaces_text,
    test_surfaces=test_surfaces_text,
    core_materials=core_materials_text,
    test_materials=test_materials_text
)
```

### Pattern 3: Metadata Injection

**Template header**:
```jinja2
c ==============================================================================
c    GENERATED INPUT
c ==============================================================================
c    Template: {{template_name}}
c    Cycle: {{cycle}}
c    Date: {{generation_date}}
c    
c    Data sources:
c      - {{data_source_1}}
c      - {{data_source_2}}
c
c    Parameters:
c      - Average power: {{average_power}} MW
c      - Burnup: {{burnup}} GWd/MTU
c      - Control angle: {{control_angle}} degrees
c ==============================================================================
```

**Python**:
```python
from datetime import datetime

metadata = {
    'template_name': 'base_model.template',
    'cycle': cycle,
    'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'data_source_1': 'power.csv',
    'data_source_2': 'oscc.csv',
    'average_power': f'{ave_power:.2f}',
    'burnup': f'{burnup:.1f}',
    'control_angle': control_angle
}

output = template.render(**metadata, **data)
```

## Environment Configuration

### Basic Setup

```python
from jinja2 import Environment, FileSystemLoader

# Create environment
env = Environment(
    loader=FileSystemLoader('./templates'),  # Template directory
    trim_blocks=True,                        # Remove first newline after block
    lstrip_blocks=True,                      # Strip leading whitespace
    keep_trailing_newline=True               # Preserve final newline
)

# Load template
template = env.get_template('base_model.template')
```

### Multiple Template Directories

```python
from jinja2 import Environment, FileSystemLoader, ChoiceLoader

# Search multiple directories
loader = ChoiceLoader([
    FileSystemLoader('./templates'),
    FileSystemLoader('./project_templates'),
    FileSystemLoader('./archived_templates')
])

env = Environment(loader=loader)
```

## Validation and Error Checking

### Check for Unreplaced Variables

```python
def validate_template_rendering(output, filename):
    """Ensure all template variables were replaced."""
    if '{{' in output or '}}' in output:
        # Find unreplaced variables
        import re
        unreplaced = re.findall(r'\{\{([^}]+)\}\}', output)
        raise ValueError(f"Unreplaced variables in {filename}: {unreplaced}")
```

### Check Template Syntax

```python
def validate_template_syntax(template_path):
    """Check template can be parsed."""
    try:
        env = Environment(loader=FileSystemLoader('./'))
        template = env.get_template(template_path)
        print(f"✓ Template syntax valid: {template_path}")
        return True
    except Exception as e:
        print(f"✗ Template syntax error: {e}")
        return False
```

## Complete Rendering Workflow

```python
from jinja2 import Environment, FileSystemLoader
import os

def render_template_workflow(template_path, data_dict, output_path):
    """
    Complete template rendering with validation.
    
    Args:
        template_path: Path to .template file
        data_dict: Dictionary of template variables
        output_path: Where to write rendered output
    """
    # Setup environment
    template_dir = os.path.dirname(template_path)
    template_name = os.path.basename(template_path)
    
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    
    # Render
    output = template.render(**data_dict)
    
    # Validate
    validate_template_rendering(output, output_path)
    
    # Write
    with open(output_path, 'w') as f:
        f.write(output)
    
    print(f"✓ Rendered: {output_path} ({len(output)} bytes)")
    
    return output

# Usage
data = {
    'oscc_surfaces': drum_surfaces,
    'ne_cells': ne_cells,
    'se_cells': se_cells,
    'materials': materials_text
}

render_template_workflow('templates/base.template', data, 'mcnp/input_138B.i')
```

## Best Practices Summary

1. **Keep templates simple**: Only `{{variable}}` substitution
2. **Logic in Python**: All loops, conditionals, calculations in Python
3. **Descriptive names**: Clear variable names (not var1, var2)
4. **Document placeholders**: List all variables in template header
5. **Validate rendering**: Check for unreplaced `{{...}}`
6. **Preserve formatting**: Maintain MCNP indentation and spacing
7. **Test templates**: Render with dummy data first
8. **Version control**: Track template changes separately from data

## Troubleshooting

### Problem: Extra blank lines in output

**Cause**: Newlines around `{{variable}}`

**Fix**: Use Jinja2 whitespace control
```jinja2
{# Instead of: #}
c --- Section ---
{{variable}}

{# Use: #}
c --- Section ---
{{- variable }}
```

### Problem: Variable not replaced

**Cause**: Typo in variable name

**Fix**: Double-check spelling
```python
# Template has: {{oscc_surfaces}}
# Python must have: oscc_surfaces="..." (exact match)
template.render(oscc_surfaces=surfaces_text)
```

### Problem: Template file not found

**Cause**: Wrong FileSystemLoader path

**Fix**: Use absolute path or verify relative path
```python
import os
template_dir = os.path.abspath('./templates')
env = Environment(loader=FileSystemLoader(template_dir))
```

## See Also

- **template_conversion_guide.md** - Converting inputs to templates
- **workflow_patterns.md** - Complete workflow examples
- **example_inputs/agr1_burnup_workflow.py** - Real-world example
- Jinja2 docs: https://jinja.palletsprojects.com/

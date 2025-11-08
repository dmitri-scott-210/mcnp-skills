"""
Generate assembly function templates
Helps users create new assembly types quickly
"""

def generate_assembly_template(assembly_name, description=""):
    """
    Create a template function for a new assembly type

    Args:
        assembly_name: Name for the assembly (e.g., "fuel", "control", "reflector")
        description: Brief description of assembly

    Returns:
        Python function template as string
    """

    template = f'''def {assembly_name}_assembly(layer, number, **kwargs):
    """
    Generate {assembly_name} assembly

    {description}

    Args:
        layer (int): Axial layer (1-N)
        number (str): Assembly number ('01'-'NN')
        **kwargs: Additional parameters

    Returns:
        tuple: (cells_str, surfaces_str, materials_str)

    Example:
        >>> c, s, m = {assembly_name}_assembly(2, '15')
    """
    # Calculate numbering
    n = f"{{layer+1}}{{number:02d}}"

    # TODO: Define geometry parameters
    radius_1 = 0.41  # cm
    radius_2 = 0.48  # cm

    # Generate cells
    cells = f"""c {{assembly_name.capitalize()}} Assembly L{{layer}} N{{number}}
{{n}}01 {{n}}1 -10.0  -{{n}}01  u={{n}}0  imp:n=1  $ Component 1
{{n}}02 {{n}}2 -5.0   {{n}}01 -{{n}}02  u={{n}}0  imp:n=1  $ Component 2
{{n}}03 0     {{n}}02  u={{n}}0  imp:n=1  $ Outer region
"""

    # Generate surfaces
    surfaces = f"""c {{assembly_name.capitalize()}} assembly surfaces
{{n}}01 cz  {{radius_1:.2f}}  $ Inner radius
{{n}}02 cz  {{radius_2:.2f}}  $ Outer radius
"""

    # Generate materials
    materials = f"""m{{n}}1  $ Material 1 description
   [TODO: Add isotopes]
c
m{{n}}2  $ Material 2 description
   [TODO: Add isotopes]
"""

    return cells, surfaces, materials
'''

    return template


def generate_input_definition_template(n_layers, n_assemblies_per_layer):
    """
    Generate input_definition.py template

    Args:
        n_layers: Number of axial layers
        n_assemblies_per_layer: Assemblies per layer
    """

    template = f'''"""
Reactor Parameter Definition
{n_layers} layers × {n_assemblies_per_layer} assemblies = {n_layers * n_assemblies_per_layer} total positions
"""

# Core configuration
# Format: 'NN' = fuel, 'NN_C' = control, 'NN_R' = reflector
assemblies = {{
'''

    for layer in range(1, n_layers + 1):
        assy_list = [f"'{i:02d}'" for i in range(1, n_assemblies_per_layer + 1)]
        template += f"    {layer}: [{', '.join(assy_list)}],\n"

    template += '''}

# Assembly-specific parameters
fuel_enrichments = {
    # Example: higher enrichment in center
    '15': 5.5,
    '16': 5.5,
    # Default: 4.5%
}

# Geometry parameters
fuel_radius = 0.41  # cm
clad_radius = 0.48  # cm
active_height = 200  # cm
assembly_pitch = 21.5  # cm

# Material parameters
default_enrichment = 4.5  # %
uo2_density = 10.2  # g/cm³
water_temp = 350  # K
'''

    return template


def generate_generation_script_template(model_name='reactor'):
    """
    Generate template for generate_model.py script

    Args:
        model_name: Name of the model (e.g., 'reactor', 'criticality')
    """

    template = f'''"""
Generate {model_name} MCNP input
Programmatically generated using function-based approach
"""

import input_definition as indef
import geometry_functions as geom

# Initialize
header = """{model_name.upper()} Model
c Programmatically generated
c
"""

cells = """c
c Cells
c
"""

surfaces = """c
c Surfaces
c
"""

materials = """c
c Materials
c
"""

# Generate all assemblies
for layer, asse_list in indef.assemblies.items():
    for asse in asse_list:
        # Parse assembly type
        sp = asse.split('_')
        asse_num = sp[0]
        asse_type = sp[1] if len(sp) > 1 else 'F'  # F=fuel, C=control

        if asse_type == 'C':
            # Control assembly
            c, s, m = geom.control_assembly(layer, asse_num)
        elif asse_type == 'R':
            # Reflector assembly
            c, s, m = geom.reflector_assembly(layer, asse_num)
        else:
            # Fuel assembly
            c, s, m = geom.fuel_assembly(layer, asse_num)

        # Accumulate
        cells += c
        surfaces += s
        materials += m

# Add global components
c_refl, s_refl, m_refl = geom.reflector()
cells += c_refl
surfaces += s_refl
materials += m_refl

# Add physics cards
physics = """c
c Physics
c
mode n
kcode 10000 1.0 50 250
ksrc 0 0 0
"""

# Write output
output_file = '{model_name}.i'
with open(output_file, 'w') as f:
    f.write(header)
    f.write(cells)
    f.write(surfaces)
    f.write(materials)
    f.write(physics)

print(f"✓ Generated: {{output_file}}")
'''

    return template


# Example usage
if __name__ == "__main__":
    print("Assembly Template Generator")
    print("=" * 60)

    # Generate fuel assembly template
    fuel_template = generate_assembly_template(
        "fuel",
        "Standard UO2 fuel assembly with clad and coolant"
    )

    print("\nFuel Assembly Function Template:")
    print(fuel_template)

    # Generate control assembly template
    control_template = generate_assembly_template(
        "control",
        "Control assembly with B4C absorber rod"
    )

    print("\n" + "=" * 60)
    print("\nControl Assembly Function Template:")
    print(control_template)

    # Generate input definition template
    input_def = generate_input_definition_template(4, 36)

    print("\n" + "=" * 60)
    print("\nInput Definition Template:")
    print(input_def)

    # Generate generation script template
    gen_script = generate_generation_script_template('smr_criticality')

    print("\n" + "=" * 60)
    print("\nGeneration Script Template:")
    print(gen_script)

    print("\n" + "=" * 60)
    print("\nTemplates generated successfully!")
    print("\nUsage:")
    print("  1. Copy fuel_assembly template to geometry_functions.py")
    print("  2. Copy input_definition template to input_definition.py")
    print("  3. Copy generation script to generate_model.py")
    print("  4. Modify templates to match your reactor design")
    print("  5. Run: python generate_model.py")

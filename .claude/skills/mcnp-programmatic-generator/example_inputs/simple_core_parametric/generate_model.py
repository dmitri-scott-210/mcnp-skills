"""
Generate Simple Core MCNP Input
Programmatically generated using function-based approach
"""

import input_definition as indef
import geometry_functions as geom

# Initialize
header = """Simple Core Model
c Programmatically generated
c 4 layers × 36 assemblies = 144 positions
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
print("Generating assemblies...")
assembly_count = 0
fuel_count = 0
control_count = 0

for layer, asse_list in indef.assemblies.items():
    for asse in asse_list:
        # Parse assembly type
        sp = asse.split('_')
        asse_num = sp[0]
        asse_type = sp[1] if len(sp) > 1 else 'F'  # F=fuel, C=control

        if asse_type == 'C':
            # Control assembly
            position = indef.control_positions.get((str(layer), asse), 'withdrawn')
            c, s, m = geom.control_assembly(layer, asse_num, position)
            control_count += 1
        else:
            # Fuel assembly
            enrich = indef.fuel_enrichments.get(asse_num, indef.default_enrichment)
            c, s, m = geom.fuel_assembly(layer, asse_num, enrich)
            fuel_count += 1

        # Accumulate
        cells += c
        surfaces += s
        materials += m
        assembly_count += 1

print(f"  Generated {assembly_count} assemblies:")
print(f"    Fuel: {fuel_count}")
print(f"    Control: {control_count}")

# Add reflector
print("Generating reflector...")
c_refl, s_refl, m_refl = geom.reflector()
cells += c_refl
surfaces += s_refl
materials += m_refl

# Add outer boundary
print("Generating outer boundary...")
c_bound, s_bound, m_bound = geom.outer_boundary()
cells += c_bound
surfaces += s_bound
materials += m_bound

# Add physics cards
physics = """c
c Physics
c
mode n
kcode 10000 1.0 50 250
ksrc 0 0 0  10 10 50  -10 -10 -50
"""

# Write output
output_file = 'simple_core.i'
print(f"Writing output to {output_file}...")
with open(output_file, 'w') as f:
    f.write(header)
    f.write(cells)
    f.write(surfaces)
    f.write(materials)
    f.write(physics)

print(f"\n✓ Generated: {output_file}")
print(f"  Total assemblies: {assembly_count}")
print(f"  Fuel assemblies: {fuel_count}")
print(f"  Control assemblies: {control_count}")
print()
print("Next steps:")
print("  1. Validate: python validate.py")
print("  2. Run MCNP: mcnp6 i=simple_core.i")

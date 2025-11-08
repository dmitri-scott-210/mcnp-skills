"""
Generate Microreactor Burnup (Criticality) Model
Core + reflector only (no shield)

Demonstrates model variant generation with shared core geometry
"""

import input_definition as indef

# NOTE: This is a simplified conceptual example
# For complete TRISO fuel implementation, see function_patterns_reference.md

def triso_fuel_block(layer, number):
    """
    Generate simplified TRISO fuel block
    (In full model, this would include particle lattices)

    Returns: (cells, surfaces, materials)
    """
    n = f"{layer+1}{number:02d}"

    # Simplified: homogenized TRISO fuel
    cells = f"""c TRISO Fuel Block L{layer} N{number}
{n}01 {n}1 -1.8  -{n}01  u={n}0  imp:n=1  $ Homogenized TRISO fuel
{n}02 {n}2 -{indef.graphite_density}  {n}01 -{n}02  u={n}0  imp:n=1  $ Graphite
"""

    surfaces = f"""c Fuel block surfaces
{n}01 cz  {indef.compact_radius * 10:.2f}  $ Fuel region
{n}02 cz  {indef.block_radius:.2f}  $ Block outer
"""

    # Homogenized TRISO material (simplified)
    materials = f"""m{n}1  $ Homogenized TRISO fuel
   92235.70c  0.00482
   92238.70c  0.01932
    8016.70c  0.04897
    6012.00c  0.9890  $ Carbon matrix
c
m{n}2  $ Graphite moderator
    6012.00c  0.9890
    6013.00c  0.0110
mt{n}2 grph.18t
"""

    return cells, surfaces, materials


def control_block(layer, number):
    """Generate control block"""
    n = f"{layer+1}{number:02d}"

    cells = f"""c Control Block L{layer} N{number}
{n}01 {n}3 -2.5  -{n}01  u={n}0  imp:n=1  $ B4C control material
{n}02 {n}2 -{indef.graphite_density}  {n}01 -{n}02  u={n}0  imp:n=1  $ Graphite
"""

    surfaces = f"""c Control block surfaces
{n}01 cz  {indef.compact_radius * 10:.2f}
{n}02 cz  {indef.block_radius:.2f}
"""

    materials = f"""m{n}3  $ B4C absorber
    5010.70c  0.72
    5011.70c  2.88
    6012.00c  1.0
c
m{n}2  $ Graphite
    6012.00c  0.9890
    6013.00c  0.0110
mt{n}2 grph.18t
"""

    return cells, surfaces, materials


# Initialize
header = """Microreactor Burnup Model
c Programmatically generated
c HTGR-style TRISO fuel (simplified)
c Core + reflector (no shield)
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

# Generate all assemblies (SAME CODE in both burnup and SDR models)
print("Generating core assemblies...")
for layer, asse_list in indef.assemblies.items():
    for asse in asse_list:
        sp = asse.split('_')
        asse_num = sp[0]
        asse_type = sp[1] if len(sp) > 1 else 'F'

        if asse_type == 'C':
            c, s, m = control_block(layer, asse_num)
        else:
            c, s, m = triso_fuel_block(layer, asse_num)

        cells += c
        surfaces += s
        materials += m

# Add reflector (BURNUP MODEL: reflector only)
print("Adding reflector...")
cells += """c
c Radial reflector
9001 9001 -1.7  -9001 9002  imp:n=1  $ Graphite reflector
"""

surfaces += f"""c
c Reflector surfaces
9001 cz  {indef.core_radius + indef.reflector_thickness:.1f}
9002 cz  {indef.core_radius:.1f}
"""

materials += """c
m9001  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt9001 grph.18t
"""

# Outer boundary
cells += """c
c Outer boundary
9999  0   9001  imp:n=0
"""

# Physics: CRITICALITY (burnup model)
physics = f"""c
c Physics - Criticality
c
mode n
kcode 10000 1.0 50 250
ksrc 0 0 0  10 0 0  -10 0 0
tmp {indef.temperature}j
"""

# Write output
output_file = 'microreactor_burnup.i'
with open(output_file, 'w') as f:
    f.write(header)
    f.write(cells)
    f.write(surfaces)
    f.write(materials)
    f.write(physics)

print(f"\n✓ Generated: {output_file}")
print("  Model type: Burnup (criticality)")
print("  Boundaries: Core + reflector")
print("  Physics: KCODE (criticality)")
print()
print("Note: Core geometry is IDENTICAL to SDR model")
print("      (Different boundaries and physics only)")

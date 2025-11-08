"""
Generate Microreactor Shielding/Dose Rate (SDR) Model
Core + reflector + shield + room

Demonstrates model variant generation with shared core geometry
"""

import input_definition as indef

# NOTE: This is a simplified conceptual example
# For complete TRISO fuel implementation, see function_patterns_reference.md

def triso_fuel_block(layer, number):
    """
    Generate simplified TRISO fuel block
    (IDENTICAL to burnup model)

    Returns: (cells, surfaces, materials)
    """
    n = f"{layer+1}{number:02d}"

    # Simplified: homogenized TRISO fuel
    cells = f"""c TRISO Fuel Block L{layer} N{number}
{n}01 {n}1 -1.8  -{n}01  u={n}0  imp:n=1  imp:p=1  $ Homogenized TRISO fuel
{n}02 {n}2 -{indef.graphite_density}  {n}01 -{n}02  u={n}0  imp:n=1  imp:p=1  $ Graphite
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
    """Generate control block (IDENTICAL to burnup model)"""
    n = f"{layer+1}{number:02d}"

    cells = f"""c Control Block L{layer} N{number}
{n}01 {n}3 -2.5  -{n}01  u={n}0  imp:n=1  imp:p=1  $ B4C control material
{n}02 {n}2 -{indef.graphite_density}  {n}01 -{n}02  u={n}0  imp:n=1  imp:p=1  $ Graphite
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
header = """Microreactor Shielding/Dose Rate Model
c Programmatically generated
c HTGR-style TRISO fuel (simplified)
c Core + reflector + shield + room
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

# Generate all assemblies (IDENTICAL CODE to burnup model!)
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

# Add reflector
print("Adding reflector...")
cells += """c
c Radial reflector
9001 9001 -1.7  -9001 9002  imp:n=1  imp:p=1  $ Graphite reflector
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

# Add shield (SDR MODEL ONLY: includes shield + room)
print("Adding shield and room...")
shield_outer = indef.core_radius + indef.reflector_thickness + indef.shield_thickness

cells += f"""c
c Concrete biological shield
9010 9010 -2.35  -9010 9001  imp:n=1  imp:p=1  $ Concrete shield
c
c Air gap / room
9020 9020 -1.164e-03  -9020 9010  imp:n=1  imp:p=1  $ Air
c
c Outer boundary
9999  0   9020  imp:n=0  imp:p=0
"""

surfaces += f"""c
c Shield surfaces
9010 cz  {shield_outer:.1f}  $ Shield outer
9020 cz  {shield_outer + 50:.1f}  $ Room boundary
"""

materials += """c
m9010  $ Ordinary concrete
    1001.70c  0.0221
    6000.70c  0.002484
    8016.70c  0.5748
   11023.70c  0.01541
   12000.60c  0.002565
   13027.70c  0.01996
   14000.60c  0.3045
   19000.60c  0.01068
   20000.70c  0.04266
   26000.55c  0.00524
c
m9020  $ Air
    7014.80c  -0.755636
    8016.80c  -0.231475
   18000.59c  -0.012889
"""

# Physics: FIXED SOURCE + PHOTONS (shielding model)
physics = f"""c
c Physics - Fixed Source Shielding
c
mode n p
sdef  pos=0 0 0  erg=2.0  par=1
f4:p  9020  $ Photon dose at room boundary
de4   0.01  0.03  0.1  0.3  1.0  3.0  10.0
df4   3.7e-6  5.3e-6  9.2e-6  1.5e-5  2.7e-5  3.8e-5  4.9e-5
tmp {indef.temperature}j
"""

# Write output
output_file = 'microreactor_sdr.i'
with open(output_file, 'w') as f:
    f.write(header)
    f.write(cells)
    f.write(surfaces)
    f.write(materials)
    f.write(physics)

print(f"\n✓ Generated: {output_file}")
print("  Model type: Shielding/Dose Rate (SDR)")
print("  Boundaries: Core + reflector + shield + room")
print("  Physics: Fixed source + photon transport")
print()
print("Note: Core geometry is IDENTICAL to burnup model")
print("      (Same assembly generation code)")
print()
print("Comparison:")
print("  Burnup: Core + reflector, KCODE")
print("  SDR:    Core + reflector + shield + room, SDEF + photons")

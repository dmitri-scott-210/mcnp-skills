"""
Geometry Generation Functions for Simple Core
All functions return (cells, surfaces, materials)
"""

import input_definition as indef


def fuel_assembly(layer, number, enrichment=None):
    """
    Generate fuel assembly

    Args:
        layer (int): Axial layer (1-4)
        number (str): Assembly number ('01'-'36')
        enrichment (float): U-235 enrichment (%), default from config

    Returns:
        tuple: (cells_str, surfaces_str, materials_str)
    """
    if enrichment is None:
        enrichment = indef.fuel_enrichments.get(number, indef.default_enrichment)

    # Calculate numbering (LNNCC format)
    n = f"{layer+1}{number}"

    # Generate cells
    cells = f"""c Fuel Assembly L{layer} N{number} E={enrichment:.1f}%
{n}01 {n}1 -{indef.uo2_density:.1f}  -{n}01  u={n}0  imp:n=1  $ UO2 fuel
{n}02 {n}2 -{indef.zr_density:.1f}   {n}01 -{n}02  u={n}0  imp:n=1  $ Zr clad
{n}03 {n}3 -1.0   {n}02  u={n}0  imp:n=1  $ Water coolant
"""

    # Generate surfaces
    surfaces = f"""c Assembly {layer}-{number} surfaces
{n}01 cz  {indef.fuel_radius:.2f}
{n}02 cz  {indef.clad_radius:.2f}
"""

    # Generate materials
    u235_frac = enrichment / 100.0
    u238_frac = 1.0 - u235_frac

    materials = f"""m{n}1  $ UO2 {enrichment:.1f}% enriched
   92235.70c  {u235_frac:.6f}
   92238.70c  {u238_frac:.6f}
    8016.70c  2.0
c
m{n}2  $ Zircaloy-4 clad
   40000.60c  0.98
   50000.42c  0.015
   26000.50c  0.005
c
m{n}3  $ Water at {indef.water_temp}K
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    return cells, surfaces, materials


def control_assembly(layer, number, position='withdrawn'):
    """
    Generate control assembly with rod position

    Args:
        layer (int): Axial layer (1-4)
        number (str): Assembly number ('01'-'36')
        position (str): 'withdrawn', 'inserted', or float 0-100 (%)

    Returns:
        tuple: (cells_str, surfaces_str, materials_str)
    """
    n = f"{layer+1}{number}"

    # Guide tube (always present)
    cells = f"""c Control Assembly L{layer} N{number} pos={position}
{n}01 {n}2 -8.0  -{n}01 {n}02  u={n}0  imp:n=1  $ SS guide tube
"""

    surfaces = f"""c Control assembly surfaces
{n}01 cz  0.55
{n}02 cz  0.62
"""

    materials = f"""m{n}2  $ SS304 guide tube
   26000.50c  0.70
   24000.50c  0.19
   28000.50c  0.10
"""

    # Control rod (position-dependent)
    if position == 'inserted':
        cells += f"""{n}03 {n}4 -2.5  -{n}01  u={n}0  imp:n=1  $ B4C absorber
"""
        materials += f"""c
m{n}4  $ B4C absorber
    5010.70c  0.72
    5011.70c  2.88
    6012.00c  1.0
"""

    elif position == 'withdrawn':
        cells += f"""{n}03 {n}3 -1.0  -{n}01  u={n}0  imp:n=1  $ Water
"""
        materials += f"""c
m{n}3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    else:
        # Partial insertion (0-100%)
        try:
            insertion_fraction = float(position) / 100.0
            insertion_height = insertion_fraction * indef.active_height

            cells += f"""{n}03 {n}4 -2.5  -{n}01  -{n}10  u={n}0  imp:n=1  $ B4C
{n}04 {n}3 -1.0  -{n}01   {n}10  u={n}0  imp:n=1  $ Water above
"""
            surfaces += f"""{n}10 pz  {insertion_height:.2f}  $ Rod tip
"""
            materials += f"""c
m{n}4  $ B4C absorber
    5010.70c  0.72
    5011.70c  2.88
    6012.00c  1.0
c
m{n}3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""
        except ValueError:
            raise ValueError(f"Invalid control position: {position}")

    return cells, surfaces, materials


def reflector():
    """
    Generate radial reflector

    Returns:
        tuple: (cells_str, surfaces_str, materials_str)
    """
    reflector_outer = indef.core_radius + indef.reflector_thickness

    cells = f"""c Radial reflector
9001 9001 -1.7  -9001 9002  imp:n=1  $ Graphite reflector
"""

    surfaces = f"""c Reflector surfaces
9001 cz  {reflector_outer:.1f}  $ Reflector outer radius
9002 cz  {indef.core_radius:.1f}  $ Core outer radius
"""

    materials = f"""m9001  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt9001 grph.18t
"""

    return cells, surfaces, materials


def outer_boundary():
    """
    Generate outer boundary cell

    Returns:
        tuple: (cells_str, surfaces_str, materials_str)
    """
    reflector_outer = indef.core_radius + indef.reflector_thickness

    cells = f"""c Outer boundary
9999  0   9001  imp:n=0  $ Outside world
"""

    surfaces = ""  # Uses surface 9001 from reflector

    materials = ""  # No materials

    return cells, surfaces, materials

import openmc

# CAD model thermal shield starts at z=-60, cutout goes to z=77.23, so we need
# to cut out total thickness of 137.23 cm.

xs = '80'

model = openmc.Model.from_model_xml(f'msre_csg_endf{xs}.xml')

# Cut out 90° segment from thermal shield
plane1 = openmc.Plane(-1., 1., 0., 0.)
plane2 = openmc.Plane(1., 1., 0., 0.)

# z-plane at -89.779
z_bottom = model.geometry.get_all_surfaces()[2006]
z_cutout = openmc.ZPlane(z_bottom.z0 + 137.23)
univ = model.geometry.root_universe

cells = model.geometry.get_all_material_cells()
for cell in cells.values():
    if cell.fill.name != '3':
        continue

    # If cell's highest z is less than z_cutout, we don't need to include z_cutout
    bbox = cell.bounding_box
    if bbox.upper_right[2] < z_cutout.z0:
        cutout_region = -plane1 & -plane2
        univ.add_cell(openmc.Cell(region=cell.region & cutout_region))
        cell.region &= ~cutout_region

    # If cell's highest z is more than z_cutout and lowest z is less, need to include z_cutout
    elif bbox.upper_right[2] > z_cutout.z0 and bbox.lower_left[2] < z_cutout.z0:
        cutout_region = -plane1 & -plane2 & -z_cutout
        univ.add_cell(openmc.Cell(region=cell.region & cutout_region))
        cell.region &= ~cutout_region

model.export_to_model_xml(f'msre_csg_endf{xs}_thermal_shield_cutout.xml')

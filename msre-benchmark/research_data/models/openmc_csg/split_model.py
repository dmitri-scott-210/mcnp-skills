import openmc

xs = '80'

model = openmc.Model.from_model_xml(f'msre_csg_endf{xs}.xml')

# Create split plane
split_plane = openmc.ZPlane(10.0, boundary_type='vacuum')

# Limit root universe cells to region below plane
root: openmc.Universe = model.geometry.root_universe
for cell in root.cells.values():
    cell.region &= -split_plane
model.export_to_model_xml(f'msre_csg_endf{xs}_z10_bottom.xml')

# Not limit root universe cells to region above plane
for cell in root.cells.values():
    cell.region.pop()
    cell.region &= +split_plane
model.settings.source[0].space.xyz = (0., 0., 60.)
model.export_to_model_xml(f'msre_csg_endf{xs}_z10_top.xml')

import openmc
import numpy as np

xs = '80'
model = openmc.Model.from_model_xml(f'msre_csg_endf{xs}.xml')

# Radial flux/fission distribution over fuel
width = 152.0
mesh = openmc.RegularMesh()
mesh.lower_left = (-width/2, -width/2, -35.)
mesh.upper_right = (width/2, width/2, 202.)
mesh.dimension = (500, 500, 1)
mesh_tally = openmc.Tally(name='mesh tally')
mesh_tally.filters = [openmc.MeshFilter(mesh)]
mesh_tally.scores = ['flux', 'fission']

spectrum_tally = openmc.Tally(name='spectrum')
spectrum_tally.filters = [openmc.EnergyFilter(np.geomspace(1e-5, 20.e6, 501))]
spectrum_tally.scores = ['flux']

axial_mesh = openmc.RegularMesh()
axial_mesh.lower_left = (-width/2, -width/2, -35.0)
axial_mesh.upper_right = (width/2, width/2, 202.0)
axial_mesh.dimension = (1, 1, 200)
axial_tally = openmc.Tally(name='axial tally')
axial_tally.filters = [openmc.MeshFilter(axial_mesh)]
axial_tally.scores = ['flux', 'nu-fission', 'absorption']

model.tallies = [mesh_tally, spectrum_tally, axial_tally]
model.export_to_model_xml(f'msre_csg_endf{xs}_tallies.xml')

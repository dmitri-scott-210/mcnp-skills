import openmc
import numpy as np

# Define materials
hot_temp = 911.0  # in K

# Fuel salt
salt = openmc.Material(name="salt", temperature=hot_temp)
salt.add_components({
    "Li6": 1.0944e-06,
    "Li7": 2.1888e-02,
    "Be9": 9.8747e-03,
    "Zr": 1.7056e-03,
    "Hf": 4.3588e-08,
    "U235": 8.4044e-05,
    "U234": 8.6090e-07,
    "U236": 3.5191e-07,
    "U238": 1.8048e-04,
    "Fe": 4.0658e-06,
    "Cr": 7.5479e-07,
    "Ni": 7.1646e-07,
    "O": 4.2927e-05,
    "F": 4.9450e-02,
})
salt.set_density("g/cm3", 2.3275)

# Moderator graphite block
graphite = openmc.Material(name="graphite", temperature=hot_temp)
graphite.set_density("g/cm3", 1.8507)
graphite.add_components({
    "C": 9.2789e-02,
    "B10": 1.6412e-08,
    "B11": 6.6060e-08,
    "V": 1.9690e-07,
    "S": 1.7378e-07,
    "O": 1.7235e-07,
    "Si": 5.3518e-08,
    "Al": 3.7225e-08,
    "Fe": 3.6679e-09,
    "Ti": 1.2688e-09,
    "Mg": 1.0027e-09,
    "Ca": 4.3868e-10,
})
graphite.add_s_alpha_beta("c_Graphite")

# inor-8
inor = openmc.Material(name="inor-8", temperature=hot_temp)
inor.set_density("g/cm3", 8.7745)
inor.add_components({
    "Ni": 68.5,
    "Mo": 16.5,
    "Cr": 7.0,
    "Fe": 5.0,
    "C": 0.06,
    "Al": 0.25,
    "Ti": 0.25,
    "S": 0.02,
    "Mn": 1.0,
    "Si": 1.0,
    "Cu": 0.35,
    "B": 0.010,
    "W": 0.5,
    "P": 0.015,
    "Co": 0.2,
}, percent_type='wo')

# helium
helium = openmc.Material(name="helium", temperature=hot_temp)
helium.add_element("He", 1.0833e-5)
helium.set_density("g/cm3", 7.2e-5)

# Control rods inconel clad
inconel = openmc.Material(name="inconel", temperature=hot_temp)
inconel.add_components({
    "C": 3.2017e-04,
    "Mn": 3.0625e-04,
    "P": 2.3279e-05,
    "S": 2.2486e-05,
    "Si": 5.9905e-04,
    "Cr": 1.7565e-02,
    "Ni": 4.2998e-02,
    "Mo": 1.5283e-03,
    "Nb": 2.6517e-03,
    "Ti": 9.0383e-04,
    "Al": 8.9080e-04,
    "Co": 8.1568e-04,
    "B10": 5.3090e-06,
    "B11": 2.1369e-04,
    "Cu": 2.2694e-04,
    "Ta": 1.3283e-05,
    "Fe": 1.4426e-02,
})
inconel.set_density("g/cm3", 7.9823)

# SS316 control rod flexible hose
ss316 = openmc.Material(name="ss316", temperature=65.6 + 273.15)
ss316.add_element("C", 0.026, "wo")
ss316.add_element("Si", 0.37, "wo")
ss316.add_element("Mn", 0.16, "wo")
ss316.add_element("Cr", 16.55, "wo")
ss316.add_element("Cu", 0.16, "wo")
ss316.add_element("Ni", 10, "wo")
ss316.add_element("P", 0.029, "wo")
ss316.add_element("S", 0.027, "wo")
ss316.add_element("Mo", 2.02, "wo")
ss316.add_element("N", 0.036, "wo")
ss316.add_element("Fe", 70.622, "wo")
ss316.set_density("g/cm3", 7.99)

# Control rods bushing posion material
bush = openmc.Material(name="bush", temperature=hot_temp)
bush.add_components({
    "Gd": 1.3310e-02,
    "Al27": 2.0280e-02,
    "O16": 5.0384e-02,
})
bush.set_density("g/cm3", 5.7227)

# Concrete block
concrete = openmc.Material(name="concrete")
concrete.add_element("H", 0.005, "wo")
concrete.add_element("O", 0.496, "wo")
concrete.add_element("Si", 0.314, "wo")
concrete.add_element("Ca", 0.083, "wo")
concrete.add_element("Na", 0.017, "wo")
concrete.add_element("Mn", 0.002, "wo")
concrete.add_element("Al", 0.046, "wo")
concrete.add_element("S", 0.001, "wo")
concrete.add_element("K", 0.019, "wo")
concrete.add_element("Fe", 0.012, "wo")
concrete.set_density("g/cm3", 2.35)

# Thermal shielding as material mix of water and SS304 50-50 vo
shield = openmc.Material(name="steelwater", temperature=305.0)
shield.add_components({
    "Fe": 4.1902e-02,
    "C": 1.9679e-03,
    "H1": 3.3248e-02,
    "O16": 1.6662e-02,
    "K": 1.3995e-05,
    "B10": 3.3854e-07,
    "B11": 1.3627e-06,
    "N14": 8.8896e-06,
})
shield.set_density("g/cm3", 4.42)

# "Careytemp 1600" by Philip Carey Manufacturing Compamy (Cincinnati)
insulation = openmc.Material(name="insulation", temperature=305.0)
insulation.add_components({
    "Ca": 2.9375e-05,
    "Fe": 1.2589e-04,
    "Al27": 1.2589e-04,
    "Si": 3.3570e-04,
    "O16": 1.3428e-03,
    "H1": 8.3924e-04,
})
insulation.add_s_alpha_beta('c_H_in_H2O')

# Sand water (not sure about this material)
sandwater = openmc.Material(name="sandwater")
sandwater.add_element("Fe", 3)
sandwater.add_element("O", 4)
sandwater.set_density("g/cm3", 6)

# Vessel amnular steel
steel = openmc.Material(name="steel", temperature=911.0)
steel.add_element("Fe", 1)
steel.set_density("g/cm3", 7.8244)

model = openmc.Model()
model.materials = openmc.Materials(
    [
        salt,
        graphite,
        inor,
        helium,
        inconel,
        shield,
        concrete,
        steel,
        ss316,
        sandwater,
        insulation,
        bush,
    ]
)

# Import h5m files
core_h5m = "h5m/msre_reactor_1e-2.h5m"
cr_h5m = "h5m/msre_control_rod_1e-2.h5m"

# Create DAGMC universes out of h5m files
core = openmc.DAGMCUniverse(filename=core_h5m, auto_geom_ids=True, universe_id=1)
cr = openmc.DAGMCUniverse(filename=cr_h5m, auto_geom_ids=True, universe_id=2)

# Create regions
core_region = core.bounding_region()
cr1_region = cr.bounding_region(boundary_type="transmission", starting_id=20000)

# Extend control rod region, to include upwards translations
cr1_region |= cr1_region.translate([0, 0, 150])

# Create control rod region 2 and 3 as translated region of control rod 1
offset = 10.163255
cr2_region = cr1_region.translate([-offset, 0, 0])
cr3_region = cr1_region.translate([-offset, offset, 0])

# Create openmc Cells
core_cell = openmc.Cell(
    region=~(cr1_region | cr2_region | cr3_region) & core_region, fill=core
)
cr1_cell = openmc.Cell(name="CR1", region=cr1_region, fill=cr)
cr2_cell = openmc.Cell(name="CR2", region=cr2_region, fill=cr)
cr3_cell = openmc.Cell(name="CR3", region=cr3_region, fill=cr)

# translate control rods at top position (fully withdrawn)
inch_to_cm = 2.54
start_pos = 19.2  # cm
top_pos = 51  # inches
insertion = 4.4  # inches
cr1_cell.translation = [0, 0, start_pos + top_pos * inch_to_cm]
cr2_cell.translation = [-offset, 0, start_pos + (top_pos - insertion) * inch_to_cm]
cr3_cell.translation = [-offset, offset, start_pos + top_pos * inch_to_cm]

# Create openmc Geometry object
model.geometry = openmc.Geometry([core_cell, cr1_cell, cr2_cell, cr3_cell])

model.settings.temperature = {"method": "interpolation", "range": (293.15, 923.15)}
model.settings.batches = 1050
model.settings.inactive = 50
model.settings.particles = 1_000_000
model.settings.output = {'tallies': False}
model.settings.sourcepoint = {'write': False}
source_area = openmc.stats.Box(
    [-100.0, -100.0, 0.0], [100.0, 100.0, 200.0], only_fissionable=True
)
model.settings.source = openmc.IndependentSource(space=source_area)

# Radial flux/fission distribution over fuel
dz = 31.86
width = 152.0
mesh = openmc.RegularMesh()
mesh.lower_left = (-width/2, -width/2, -35. + dz)
mesh.upper_right = (width/2, width/2, 202. + dz)
mesh.dimension = (500, 500, 1)
mesh_tally = openmc.Tally(name='mesh tally')
mesh_tally.filters = [openmc.MeshFilter(mesh)]
mesh_tally.scores = ['flux', 'fission']

spectrum_tally = openmc.Tally(name='spectrum')
spectrum_tally.filters = [openmc.EnergyFilter(np.geomspace(1e-5, 20.e6, 501))]
spectrum_tally.scores = ['flux']

axial_mesh = openmc.RegularMesh()
axial_mesh.lower_left = (-width/2, -width/2, -35.0 + dz)
axial_mesh.upper_right = (width/2, width/2, 202.0 + dz)
axial_mesh.dimension = (1, 1, 200)
axial_tally = openmc.Tally(name='axial tally')
axial_tally.filters = [openmc.MeshFilter(axial_mesh)]
axial_tally.scores = ['flux', 'nu-fission', 'absorption']

model.tallies = [mesh_tally, spectrum_tally, axial_tally]

model.export_to_model_xml("msre_cad.xml")

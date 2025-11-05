import openmc
import openmc.data

def thermal_scatter_from_ace(ace_file):
    # Create instance from ACE tables within library
    lib = openmc.data.Library(ace_file)
    data = openmc.data.ThermalScattering.from_ace(lib.tables[0])
    for table in lib.tables[1:]:
        data.add_temperature_from_ace(table)
    return data

openmc.data.make_ace_thermal(
    '/opt/data/endf/endf-b-viii.0/neutrons/n-006_C_012.endf',
    '/opt/data/endf/endf-b-viii.0/thermal_scatt/tsl-crystalline-graphite.endf',
    ace='graphite_iwt1.ace',
    iwt=1,
    stdout=True
)
crystal_graphite = thermal_scatter_from_ace('graphite_iwt1.ace')
crystal_graphite.export_to_hdf5('c_Graphite.h5', 'w')

openmc.data.make_ace_thermal(
    '/opt/data/endf/endf-b-viii.0/neutrons/n-006_C_012.endf',
    '/opt/data/endf/endf-b-viii.0/thermal_scatt/tsl-reactor-graphite-10P.endf',
    ace='graphite10p_iwt1.ace',
    iwt=1,
    stdout=True
)
graphite_10p = thermal_scatter_from_ace('graphite10p_iwt1.ace')
graphite_10p.export_to_hdf5('c_Graphite_10p.h5', 'w')

openmc.data.make_ace_thermal(
    '/opt/data/endf/endf-b-viii.0/neutrons/n-006_C_012.endf',
    '/opt/data/endf/endf-b-viii.0/thermal_scatt/tsl-reactor-graphite-30P.endf',
    ace='graphite30p_iwt1.ace',
    iwt=1,
    stdout=True
)
graphite_30p = thermal_scatter_from_ace('graphite30p_iwt1.ace')
graphite_30p.export_to_hdf5('c_Graphite_30p.h5', 'w')

openmc.data.make_ace_thermal(
    '/opt/data/endf/endf-b-viii.0/neutrons/n-001_H_001.endf',
    '/opt/data/endf/endf-b-viii.0/thermal_scatt/tsl-HinH2O.endf',
    ace='water_iwt1.ace',
    iwt=1,
    stdout=True
)
water = thermal_scatter_from_ace('water_iwt1.ace')
water.export_to_hdf5('c_H_in_H2O.h5', 'w')

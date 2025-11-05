from openmc_serpent_adapter import serpent_conversion
import openmc

configs = [
    ('/opt/data/hdf5/endfb-vii.1-hdf5/cross_sections.xml', 'main_no_mix', 'msre_csg_endf71.xml'),
    ('/opt/data/hdf5/endfb-viii.0-hdf5/cross_sections.xml', 'main_no_mix', 'msre_csg_endf80.xml'),
    ('/opt/data/hdf5/endfb-viii.0-hdf5/cross_sections.xml', 'main_no_mix_15', 'msre_csg_endf80_mix.xml'),
]

for xs, serpent_file, output in configs:
    openmc.config['cross_sections'] = xs
    openmc.reset_auto_ids()
    model = serpent_conversion.serpent_to_model(f'../serpent/{serpent_file}')
    model.settings.particles = 1_000_000
    model.settings.batches = 1050
    model.settings.inactive = 50
    model.settings.output = {'tallies': False}
    model.settings.sourcepoint = {'write': False}
    model.export_to_model_xml(output)

import openmc

xs = '80'

model = openmc.Model.from_model_xml(f'msre_csg_endf{xs}.xml')
thermal_shield_base = model.geometry.get_all_material_cells()[2296]
thermal_shield_base.fill = None

model.export_to_model_xml(f'msre_csg_endf{xs}_no_base.xml')

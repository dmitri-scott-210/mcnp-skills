import openmc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl

# Plot customizations
mpl.rcParams['axes.axisbelow'] = True
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['savefig.bbox'] = 'tight'

ext = 'pdf'

model = openmc.Model.from_model_xml('msre_csg_endf80.xml')

materials = {mat.name: mat for mat in model.materials}


colors = {
    materials['salt']: (102, 204, 255),
    materials['gas']: (255, 255, 204),
    materials['helium']: (255, 204, 204),
    materials['poison']: (153, 51, 51),
    materials['graphite']: (255, 153, 153),
    materials['INOR']: (193, 193, 215),
    materials['sta_steel']: (0, 153, 51),
    materials['Inconel']: (204, 204, 0),
    materials['region_P']: (0, 71, 179),
    materials['region_E']: (103, 204, 255),
    materials['5']: (255, 165, 0),
    materials['3']: (178, 34, 34),
    materials['carb_steel']: (160, 160, 160),
    materials['stra']: (128, 0, 128),
}
names = {
    'salt': 'Salt',
    'gas': 'Cell gas',
    'helium': 'Helium',
    'poison': 'Poison',
    'graphite': 'Graphite',
    'INOR': 'INOR-8',
    'sta_steel': 'Stainless steel',
    'Inconel': 'Inconel',
    'region_P': '90.8% Salt / 9.2% INOR-8',
    'region_E': '97.1% Salt / 2.9% INOR-8',
    '5': 'Insulation',
    '3': 'Thermal shield',
    'carb_steel': 'Carbon steel',
    'stra': 'Strainer'
}

def add_legend(ax, material_names, **kwargs):
    name_to_mat = {mat.name: mat for mat in colors}
    patches = [
        mpatches.Patch(color=np.array(colors[name_to_mat[name]]) / 255., label=names[name])
        for name in material_names
    ]
    kwargs.setdefault('framealpha', 1.0)
    ax.legend(handles=patches, **kwargs)


kwargs = {'color_by': 'material', 'colors': colors}


ax = model.geometry.plot(
    origin=(0., -5.083, 180.),
    width=(45., 80.),
    pixels=500_000,
    basis='xz',
    **kwargs
)
add_legend(ax, ['salt', 'graphite', 'gas', 'INOR', 'sta_steel', 'poison', 'Inconel', 'stra'])
plt.savefig(f'cr_top.{ext}')

# Berkeley report, Figure 3.1
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
model.geometry.plot(
    origin=(0., 0., 145.417),
    width=(320., 320.),
    pixels=(1000, 1000),
    basis='xy',
    axes=ax,
    **kwargs
)
add_legend(ax, ['salt', 'graphite', 'INOR', 'carb_steel', '5', '3', 'sta_steel', 'gas'])
plt.savefig(f'core_xy.{ext}')

ax = model.geometry.plot(
    origin=(0., 5.08339, 79.5),
    width=(317.5, 429.),
    pixels=(635, 856),
    basis='xz',
    **kwargs
)
add_legend(ax, ['salt', 'graphite', 'INOR', 'region_P', 'carb_steel', '5', '3', 'sta_steel', 'gas', 'Inconel', 'stra'], loc='upper left', framealpha=0.8)
plt.savefig(f'core_xz.{ext}')

# Berkeley report, Figure 3.8
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
model.geometry.plot(
    origin=(0., 0., 163.),
    width=(24.3, 24.3),
    pixels=(1000, 1000),
    axes=ax,
    basis='xy',
    **kwargs
)
add_legend(ax, ['salt', 'graphite', 'gas', 'INOR', 'poison', 'Inconel', 'sta_steel'], framealpha=0.8)
plt.savefig(f'cr_sample_basket.{ext}')


# Berkeley report, Figure 3.7
ax = model.geometry.plot(
    origin=(0., 0., 184.5),
    width=(155., 65.),
    pixels=300_000,
    basis='xz',
    **kwargs
)
add_legend(ax, ['salt', 'graphite', 'INOR', 'stra'])
plt.savefig(f'centering_bridge.{ext}')

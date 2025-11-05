import openmc
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import PercentFormatter
import serpentTools
import numpy as np

# Plot customizations
mpl.rcParams['axes.axisbelow'] = True
mpl.rcParams['font.size'] = 12.0
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['savefig.bbox'] = 'tight'

ext = 'pdf'

# Read OpenMC CSG data
with openmc.StatePoint('../models/openmc_csg/results/tallies/statepoint.1050.h5') as sp:
    radial_tally = sp.get_tally(name='mesh tally')
    spectral_tally = sp.get_tally(name='spectrum')
    axial_tally = sp.get_tally(name='axial tally')
data = radial_tally.get_reshaped_data(expand_dims=True).squeeze()
openmc_radial_flux = data[..., 0].T
openmc_radial_fission = data[..., 1].T

# Read OpenMC CSG data
with openmc.StatePoint('../models/openmc_cad/results/tallies/statepoint.1050.h5') as sp:
    cad_radial_tally = sp.get_tally(name='mesh tally')
    cad_spectral_tally = sp.get_tally(name='spectrum')
    cad_axial_tally = sp.get_tally(name='axial tally')
data = cad_radial_tally.get_reshaped_data(expand_dims=True).squeeze()
cad_radial_flux = (data[..., 0].T)[::-1]
cad_radial_fission = (data[..., 1].T)[::-1]

# Read Serpent data
serpent_results = serpentTools.read('../models/serpent/results/endfb80/main_det0.m')
serpent_radial_flux = serpent_results.detectors['flux_radial'].tallies

# Plot radial flux spectrum
fig, ax = plt.subplots()
pos = ax.imshow(openmc_radial_flux, origin='lower', extent=[-76., 76., -76., 76.])
cbar = plt.colorbar(pos)
cbar.set_label('Flux [neutron-cm/source]')
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
fig.savefig(f'openmc_radial_flux.{ext}')

# Plot radial fission rate
fig, ax = plt.subplots()
pos = ax.imshow(openmc_radial_fission, origin='lower', extent=[-76., 76., -76., 76.])
cbar = plt.colorbar(pos)
cbar.set_label('Fission [reaction/source]')
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
fig.savefig(f'openmc_radial_fission.{ext}')

# Compare radial flux spectrum
relative_diff = (openmc_radial_flux - serpent_radial_flux)/serpent_radial_flux
abs_max = np.abs(relative_diff).max()
abs_max = 0.03
fig, ax = plt.subplots()
pos = ax.imshow(relative_diff, cmap='RdBu_r', vmin=-abs_max, vmax=abs_max, origin='lower', extent=[-76., 76., -76., 76.])
cbar = plt.colorbar(pos, format=PercentFormatter(xmax=1, decimals=1))
cbar.set_label('Relative difference')
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
fig.savefig(f'serpent_openmc_radial.{ext}')

# Compare radial flux spectrum
relative_diff = (cad_radial_flux - openmc_radial_flux)/openmc_radial_flux
abs_max = 0.1
fig, ax = plt.subplots()
pos = ax.imshow(relative_diff, cmap='RdBu_r', vmin=-abs_max, vmax=abs_max, origin='lower', extent=[-76., 76., -76., 76.])
cbar = plt.colorbar(pos, format=PercentFormatter(xmax=1, decimals=1))
cbar.set_label('(CAD - CSG)/CSG')
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
fig.savefig(f'csg_cad_radial.{ext}')

# Compare flux spectra
openmc_spectra = spectral_tally.mean.ravel()
openmc_unc = spectral_tally.std_dev.ravel() / openmc_spectra
energies = spectral_tally.filters[0].values
serpent_spectra = serpent_results.detectors['flux_energy'].tallies
serpent_unc = serpent_results.detectors['flux_energy'].errors
unc = np.sqrt(openmc_unc**2 + serpent_unc**2)
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.stairs(serpent_spectra, energies, label='Serpent')
ax1.stairs(openmc_spectra, energies, label='OpenMC')
ax1.grid(True)
ax1.set_xscale('log')
ax1.set_xlim(1e-3, 2.0e6)
ax1.set_ylabel('Flux [neutron-cm/source]', fontsize=10)
ax1.legend()
ax2.fill_between(energies[:-1], -2*unc, 2*unc, alpha=0.3, color='C0', step='post', label=r'2$\sigma$')
ax2.stairs((openmc_spectra - serpent_spectra)/serpent_spectra, energies, color='C1')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Relative difference')
ax2.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
ax2.set_ylim(-0.04, 0.04)
ax2.legend()
fig.savefig(f'serpent_openmc_spectrum.{ext}')

# Compare axial flux
serpent_det = serpent_results.detectors['flux_axial']
openmc_axial = axial_tally.mean.squeeze()[..., 0]
openmc_unc = axial_tally.std_dev.squeeze()[..., 0] / openmc_axial
serpent_axial = serpent_det.tallies
serpent_unc = serpent_det.errors
unc = np.sqrt(openmc_unc**2 + serpent_unc**2)
zvalues = np.concatenate([serpent_det.z[:, 0], [202.]])
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.stairs(serpent_axial, zvalues, label='Serpent')
ax1.stairs(openmc_axial, zvalues, label='OpenMC')
ax1.grid(True)
ax1.set_ylabel('Flux [neutron-cm/source]', fontsize=10)
ax1.legend()
ax2.stairs((openmc_axial - serpent_axial)/serpent_axial, zvalues, color='C1')
ax2.fill_between(zvalues[:-1], -2*unc, 2*unc, alpha=0.3, color='C0', step='post', label=r'2$\sigma$')
ax2.set_ylim(-0.002, 0.002)
ax2.set_xlabel('z [cm]')
ax2.set_xlim(zvalues[0], zvalues[-1])
ax2.set_ylabel('Relative difference')
ax2.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=1))
ax2.legend()
fig.savefig(f'serpent_openmc_axial.{ext}')

# Compare axial flux
csg_nufiss = axial_tally.mean.squeeze()[..., 1]
cad_nufiss = cad_axial_tally.mean.squeeze()[..., 1]
zvalues = np.linspace(-35.0, 202., 201)
fig, ax = plt.subplots()
ax.stairs(csg_nufiss, zvalues, label='CSG')
ax.stairs(cad_nufiss, zvalues, label='CAD')
ax.grid(True)
ax.set_xlim(-35., 202.)
ax.set_xlabel('z [cm]')
ax.set_ylabel('Neutron production [neutron/source]')
ax.legend()
fig.savefig(f'csg_cad_axial.{ext}')

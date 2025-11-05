# MCNP6 Lockwood Electron-transport Validation

The MCNP Lockwood Electron-transport Validation Suite is a collection of 334
calculations using eight materials of varying thickness bombarded by electrons
at a variety of incident energies and angles.

This directory contains the `experiments` subdirectory, which contains each of
the individual 334 calculation inputs and a `description.json` file that
contains metadata about the particular benchmark, the benchmark value, and
execution information.

To avoid periods complicating file names, a `p` is used to indicate periods in
values that may be fractional (e.g., 0.3 MeV may be abbreviated as 0p3mev).

As such, input file names follow the naming convention
`{Material}_{Energy}_{Angle}_{FMR Index}_{Transport Algorithm}` where

*  Material is an elemental abbreviation such as`al` for aluminum, `be` for
   beryllium, etc.,
*  Energy is the energy of the incident electrons using the aforementioned
   abbreviation approach,
*  Angle is the angle in degrees relative to the surface normal that the electron
   beam is incident on the foil at,
*  FMR Index is the fractional mean-range table row index from which a particular
   thickness is derived using SAND79-0414, and
*  Transport Algorithm is either `ch` for "condensed history" or `se` for "single
   event".

The principal reference for this work is:

*  G. J. Lockwood, L. E. Ruggles, G. H. Miller, and J. A. Halbleib,
   "Calorimetric Measurement of Electron Energy Deposition in Extended
   Media—Theory vs. Experiment," Sandia National Laboratories, Albuquerque, NM,
   USA, SAND79-0414, Jan. 1980.

Other relevant references include:

1. G. J. Lockwood, L. E. Ruggles, G. H. Miller, and J. A. Halbleib, "Electron
   Energy and Charge Albedos—Calorimetric Measurement vs. Monte Carlo Theory,"
   Sandia National Laboratories, SAND80-1968, Nov. 1981.
2. J. Sempau, J. M. Fernández-Varea, E. Acosta, and F. Salvat, "Experimental
   Benchmarks of the Monte Carlo Code PENELOPE," Nuclear Instruments and Methods
   in Physics Research Section B: Beam Interactions with Materials and Atoms,
   vol. 207, no. 2, pp. 107-123, Jun. 2003, doi: 10.1016/S0168-583X(03)00453-1.
3. O. Kadri, V. N. Ivanchenko, F. Gharbi, and A. Trabelsi, "GEANT4 Simulation of
   Electron Energy Deposition in Extended Media," Nuclear Instruments and
   Methods in Physics Research Section B: Beam Interactions with Materials and
   Atoms, vol. 258, no. 2, pp. 381-387, May 2007, doi:
   10.1016/j.nimb.2007.02.088.
4. H. G. Hughes, III, "Recent Developments in Low-energy Electron/Photon
   Transport for MCNP6," Los Alamos National Laboratory, Los Alamos, NM, USA,
   LA-UR-12-24213, Rev. 4, Jul. 2013.
5. D. A. Dixon and H. G. Hughes, III, "Validation of MCNP6 for Electron
   Energy Deposition in Extended Media,: Los Alamos National Laboratory, Los
   Alamos, NM, USA, LA-UR-15-28708, Nov. 2015.
6. D. A. Dixon and H. G. Hughes, III, "A Complete Reporting of MCNP6 Validation
   Results for Electron Energy Deposition in Single-Layer Extended Media for
   Source Energies ≤ 1 MeV," Los Alamos National Laboratory, Los Alamos, NM,
   USA, LA-UR-16-22749, May 2016.
7. D. A. Dixon, "A New MCNP6 Electron-Photon Transport Validation Test: The
   Lockwood Energy Deposition Experiment," Los Alamos National Laboratory, Los
   Alamos, NM, USA, LA-UR-16-23838, Jun. 2016.
8. D. A. Dixon, "An Update to the Computation of the Goudsmit-Saunderson
   Distribution in MCNP® Version 6.2," Los Alamos National Laboratory, Los
   Alamos, NM, USA, LA-UR-16-27959, Oct. 2016.
9. D. A. Dixon, "An Update to the Lockwood Energy Deposition Validation Suite
   for the MCNP® Version 6.2 Electron-photon Transport Algorithms," Los Alamos
   National Laboratory, Los Alamos, NM, USA, LA-UR-17-23433, Apr. 2017.


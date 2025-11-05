---
title: "Source Primer Chapter 2 - Basic Sources"
chapter: "Source-2"
source_pdf: "mcnp6-primer-docs/mcnp6-source-primer/2.Basic_Sources.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

Basic sources with single variables and independent probability
distributions.

## 2.1 Basic Distributions and Built-in Functions

## 2.1.1 Histograms Bins with Probabilities

Example where energy bin boundaries are assigned with probabilities
within each tabulated histogram bin. Within each bin, the energy is
sampled uniformly. This example is from 'An MCNP Primer' by Shultis and
Faw, page 11 (see Helpful Links ).

```
Tabulated energy spectrum -histograms c 10 0 -1 IMP:P=1 99 0 +1 IMP:P=0 1 SO 1.0 MODE P NPS 1e6 c c ===> tabulated histogram PDF c ===> supply UPPER boundaries of bins c ===> lower bound of first bin assumed 0.0 c ===> supply probability for each bin c ===> probabilities need not be normalized c SDEF POS 0 0 0 PAR=2 ERG=D1 SI1 H .1 .3 .5 1. 2.5 SP1 D .0 .2 .4 .3 .1 c c ===> Tally leakage, 1000 equal delta-E bins c F1:P 1 E1 .01 999i 30. c
```

Listing 2.1: MCNP6 Input File

Below is the histogram plot for the simulated energy spectrum.

CHAPTER

## TWO

## BASIC SOURCES

<!-- image -->

Listing 2.2: MCNP6 Plotting Commands

```
tal 1 linlin xlims 0 3 file end end
```

## 2.1.2 Piecewise Linear

Example of a piecewise linear energy distribution where probabilities
are user-defined at points and linearly interpolated between these
points.

```
Tabulated energy spectrum -piecewise linear c 10 0 -1 IMP:N=1 99 0 +1 IMP:N=0 1 SO 1.0 MODE N NPS 1e6 c c ===> Tabulated, piecewise linear PDF c ===> Supply E points & pdf(E) c ===> Linear interp between points c SDEF X=0 Y=0 Z=0 ERG=D1
```

Listing 2.3: MCNP6 Input File

```
c SI1 A 1.0 2.0 3.0 10.0 15.0 SP1 1. 1. 8. 3. 1. c c ===> Tally leakage, 1000 equal delta-E bins c F1:N 1 E1 .01 999i 30.
```

Below is the plot of the piecewise linear simulated energy spectrum
tally.

<!-- image -->

Listing 2.4: MCNP6 Plotting Commands

```
tal 1 linlin file end end
```

## 2.1.3 Discrete Probabilities

An example of a point isotropic source with discrete energy photons from
'An MCNP Primer' by Shultis and Faw, page 11 (see Helpful Links ).

```
Point Isotropic Source with Discrete Energy Photons 10 0 -1 IMP:P=1 $ Inside sphere
```

Listing 2.5: MCNP6 Input File

```
99 0 +1 IMP:P=0 $ Outside world 1 SO 1.0 MODE P NPS 1e6 c SDEF POS=0 0 0 ERG=D1 PAR=2 c SI1 L 0.3 0.5 1.0 2.5 $ The 4 discrete energies(MeV) SP1 0.2 0.1 0.3 0.4 $ Frequency of each energy c F1:P 1 E1 0.01 999i 30.0 c print
```

The four discrete photons energies can be seen below. The 2.5 MeV photon
has the highest frequency of 40% and 0.5 MeV has the lowest frequency of
10%. The frequencies for 0.3 MeV and 1.0 MeV are 20% and 30%,
respectively.

<!-- image -->

```
tal 1 linlin xlims 0 3 file end end
```

Listing 2.6: MCNP6 Plotting Commands

## 2.1.4 Gaussian Fusion Spectrum

Example of the MCNP built-in Gaussian spectrum for fusion neutrons.

## Listing 2.7: MCNP6 Input File

```
Gaussian spectrum, fusion neutrons point source c 10 0 -1 IMP:N=1 99 0 +1 IMP:N=0 1 SO 1.0 MODE N NPS 1e6 c c ===> Use built-in Gaussian PDF for DT fusion, 10 KeV c ===> No SI1 card needed c SDEF X=0 Y=0 Z=0 ERG=D1 SP1 -4 c c ===> Tally leakage, 1000 equal delta-E bins c F1:N 1 E1 .01 999i 30.
```

Below is the Gaussian energy spectrum plotted using the standard tally
plotter.

<!-- image -->

Listing 2.8: MCNP6 Plotting Commands

```
tal 1 file end end
```

## 2.1.5 Watt Fission Spectrum

Example of Watt fisson neutrons from a point source.

```
Fission neutron point source c 10 0 -1 IMP:N=1 $ Inside sphere 99 0 +1 IMP:N=0 $ Outside world 1 SO 1.0 MODE N NPS 1e6 c c ===> Use built-in fisson spectrum c ===> Watt spectrum for u235 thermal fission c SDEF X=0 Y=0 Z=0 ERG=D1 SP1 -3 c
```

Listing 2.9: MCNP6 Input File

```
c ===> Tally leakage, 1000 equal delta-E bins c F1:N 1 E1 .01 999i 30.
```

Below is the fission neutron energy spectrum.

<!-- image -->

Listing 2.10: MCNP6 Plotting Commands

```
tal 1 loglin xlims 1.e-2 3.e+1 file end end
```

## 2.1.6 Mixture of Fission and Fusion Spectra

Example of two independent distributions, Watt fission and Gaussian
fusion spectra, weighted and combined to create a single energy
distribution.

```
Fusion neutrons + fission neutrons point source c 10 0 -1 IMP:N=1 $ Inside sphere 99 0 +1 IMP:N=0 $ Outside sphere 1 SO 1.0
```

Listing 2.11: MCNP6 Input File

```
MODE N NPS 1e6 c c ===> Combine fission (75%) & fusion (25%) c SDEF X=0 Y=0 Z=0 ERG=D1 c c ===> Select the PDF, 3 or 4 SI1 s 3 4 SP1 .75 .25 c c ===> Sample E from the selected PDF SP3 -3 $ Fission SP4 -4 $ Fusion c c ===> Tally leakage, 1000 equal delta-E bins c F1:N 1 E1 .01 999i 30.
```

The plot below shows the energy spectrum of the source with a combined
75% fission and 25% fusion.

<!-- image -->

Listing 2.12: MCNP6 Plotting Commands

```
tal 1 loglin xlims 1.e-2 3.e+1 file end end
```

## 2.2 Positional Sources

## 2.2.1 Isotropic Point Source

Example of a 14 MeV neutron isotropic point source (default position,
energy, direction).

```
14 MeV neutrons point source c 10 0 -1 IMP:N=1 99 0 +1 IMP:N=0 1 SO 1.0 MODE N NPS 1e6 c c ===> Single source energy c SDEF X=0 Y=0 Z=0 ERG=14.0 c c ===> Tally leakage, 1000 equal delta-E bins c F1:N 1 E1 .01 999i 30. c FMESH4:N GEOM= xyz ORIGIN= -1.0 -1.0 -1.0 IMESH= 1.0 IINTS= 100 JMESH= 1.0 JINTS= 100 KMESH= 1.0 KINTS= 100 c print
```

Listing 2.13: MCNP6 Input File

Below is a plot of the single energy of the point source.

<!-- image -->

Below is the mesh plot of the flux from the point source.

<!-- image -->

Listing 2.14: MCNP6 Plotting Commands

```
tal 1 fmesh 4 file end end
```

## 2.2.2 Line Source along Coordinate Axis

Line source example from 'An MCNP Primer' by Shultis and Faw, page 12
(see Helpful Links ).

```
Line Sources (Degenerate Rectangular Parallelepiped) c 10 0 -1 IMP:P=1 $ Inside parallelpiped 99 0 +1 IMP:P=0 $ Outside parallelpiped 1 RPP -20 20 -20 20 -20 20 MODE P NPS 1e6 c c ---Line monoenergetic photon source lying along the x-axis
```

Listing 2.15: MCNP6 Input File

```
c this uses a degenerate Cartisian volumetric source. c SDEF POS=0 0 0 X=d1 Y=0 Z=0 ERG=1.25 PAR=2 SI1 -10 10 $ Xmin to xmax for line source SP1 -21 0 $ Uniform sampling on line here x^0 c c FMESH4:P GEOM= xyz ORIGIN= -30.0 -30.0 -30.0 IMESH= 30.0 IINTS= 100 JMESH= 30.0 JINTS= 100 KMESH= 30.0 KINTS= 100 TYPE=SOURCE
```

Degenerate rectangular parallelepiped line source lying along the x-axis
from -10 to 10.

<!-- image -->

Listing 2.16: MCNP6 Plotting Commands

```
fmesh 4 ex 10 file end end
```

## 2.2.3 Line Source along User-defined Axis

Line source example from 'An MCNP Primer' by Shultis and Faw, page 13
(see Helpful Links ).

```
Line Sources (Degenerate Cylinder) c 10 0 -1 IMP:P=1 $ Inside parallelpiped 99 0 +1 IMP:P=0 $ Outside parallelpiped
```

Listing 2.17: MCNP6 Input File

```
1 RPP -20 20 -20 20 -20 20 MODE P NPS 1e6 c c ---Line monoenergetic photon source lying along the AXS direction c this uses a degenerate cylindrical volumetric source. c SDEF POS=0 0 0 AXS=1 1 0 EXT=D1 RAD=0 ERG=1.25 PAR=2 SI1 -10 10 $ axial sampling range: -X to X SP1 -21 0 $ weighting for axial sampling: here constant c c FMESH4:P GEOM= xyz ORIGIN= -30.0 -30.0 -30.0 IMESH= 30.0 IINTS= 100 JMESH= 30.0 JINTS= 100 KMESH= 30.0 KINTS= 100 TYPE=SOURCE
```

Degenerate cylindrical line source lying along a user-defined axis, 20
cm long.

<!-- image -->

Listing 2.18: MCNP6 Plotting Commands

```
fmesh 4 ex 10 file
```

```
end end
```

## 2.2.4 Plane Source

Degenerate cartisian volumetric source example from 'An MCNP Primer' by
Shultis and Faw, page 13 (see Helpful Links ).

```
Plane Sources (Degenerate Rectangular Parallelepiped) c 10 0 -1 IMP:P=1 $ Inside parallelpiped 99 0 +1 IMP:P=0 $ Outside parallelpiped 1 RPP -20 20 -20 20 -20 20 MODE P NPS 1e6 c c ---Rectangular plane source centered on the orgin and perpendicular c to th y-axis. this uses a degenerate Cartesian volumetric source. c SDEF POS=0 0 0 X=D1 Y=D2 Z=0 ERG=1.25 PAR=2 SI1 -10 10 $ Xmin to xmax for line source SP1 0 1 $ Weighting for x sampling: here constant SI2 -15 15 $ Sampling range ymin to ymax SP2 0 1 $ Weighting for y sampling: here constant c FMESH4:P GEOM= xyz ORIGIN= -30.0 -30.0 -30.0 IMESH= 30.0 IINTS= 100 JMESH= 30.0 JINTS= 100 KMESH= 30.0 KINTS= 100 TYPE=SOURCE
```

Listing 2.19: MCNP6 Input File

Below is the mesh plot of the degenerate rectangular parallelepiped
plane lying along XY plane.

<!-- image -->

Listing 2.20: MCNP6 Plotting Commands

```
fmesh 4 ex 17 file end end
```

## 2.2.5 Disk Source

Degenerate cylindrical source example from 'An MCNP Primer' by Shultis
and Faw, page 13 (see Helpful Links ).

```
Degenerate Cylindrical Source c 10 0 -1 IMP:P=1 99 0 +1 IMP:P=0 1 SO 30 MODE P NPS 1e6
```

Listing 2.21: MCNP6 Input File

```
c SDEF PAR=2 POS=0 0 0 AXS=0 0 1 EXT=0 ERG=1.25 RAD=D1 c si1 0 11 $ Radial sampling range: 0 to Rmax sp1 -21 1 $ Radial sampling weighting: r^1 for disk source c c fmesh tally surrounding the source c FMESH4:P GEOM= xyz ORIGIN= -30.0 -30.0 -30.0 IMESH= 30.0 IINTS= 100 JMESH= 30.0 JINTS= 100 KMESH= 30.0 KINTS= 100 TYPE=SOURCE c print
```

Below is the mesh plot of the degenerate cylindrical disk seen on the XY
plane.

<!-- image -->

Below is the mesh plot of the degenerate cylindrical disk seen on the XZ
plane.

<!-- image -->

Listing 2.22: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 ex 13 basis 1 0 0 0 0 1 ex 13 file end end
```

## 2.2.6 Radial Shell Source Distribution

Example of the starting source position within a spherical shell.

```
14 MeV neutrons spherical shell source c 10 0 -1 imp:n=1 99 0 +1 imp:n=0 1 SO 2.0 MODE N NPS 1e6 c c ===> Single source energy c SDEF POS=0 0 0 ERG=14.0 RAD=d1 SI1 H 0.5 0.75 SP1 -21 2 c c ===> fmesh tally surrounding the source c FMESH4:N GEOM= xyz ORIGIN= -1.0 -1.0 -1.0 IMESH= 1.0 IINTS= 100
```

Listing 2.23: MCNP6 Input File

```
JMESH= 1.0 JINTS= 100 KMESH= 1.0 KINTS= 100 TYPE=SOURCE c print
```

Below is the mesh plot of the source locations within a spherical shell.

<!-- image -->

Listing 2.24: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 0 1 basis 0 1 0 1 0 0 file end end
```

## 2.2.7 Surface Source

Example of source position defined on a spherical surface.

```
14 MeV neutrons spherical surface source c 10 0 -1 IMP:N=1 20 0 +1 -2 IMP:N=1 99 0 +2 IMP:N=0 1 SO 0.5 2 SO 2.0 MODE N NPS 1e6 c c ===> Single source energy c SDEF POS=0 0 0 ERG=14.0 RAD=D1 SUR=1 SI1 H 0.0 0.75 SP1 -21 1 c c ===> fmesh tally surrounding the source c FMESH4:N GEOM= xyz ORIGIN= -1.0 -1.0 -1.0 IMESH= 1.0 IINTS= 100 JMESH= 1.0 JINTS= 100 KMESH= 1.0 KINTS= 100 TYPE=SOURCE c FMESH14:N GEOM= xyz ORIGIN= -1.0 -1.0 -1.0 IMESH= 1.0 IINTS= 100 JMESH= 1.0 JINTS= 100 KMESH= 1.0 KINTS= 100 c print
```

Listing 2.25: MCNP6 Input File

Below is the mesh plot of the surface source locations on the spherical
surface.

Note that the default directional distribution of surface source particles is a cosine distribution. Below is the mesh plot of the flux of particles due to the surface source distribution.

<!-- image -->

<!-- image -->

Listing 2.26: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 end fmesh 14 file end end
```

## 2.2.8 Uniform Cylindrical Source

Cylindrical source using the built-in power law distribution with bin
boundaries defined for radius and extent.

```
14 MeV neutrons cylindrical volume source c 10 0 -1 IMP:N=1 $ Inside sphere 99 0 +1 IMP:N=0 $ Outside world 1 SO 2.0 MODE N NPS 1e6
```

Listing 2.27: MCNP6 Input File

```
c SDEF POS=0 0 0 ERG=14.0 RAD=D1 AXS= 0 0 1 EXT=D2 SI1 H 0.0 0.5 $ Histogram bin boundaries SP1 -21 1 c SI2 -0.75 0.75 SP2 -21 0 c c ===> fmesh tally surrounding the source c FMESH4:N GEOM= xyz ORIGIN= -1.0 -1.0 -1.0 IMESH= 1.0 IINTS= 100 JMESH= 1.0 JINTS= 100 KMESH= 1.0 KINTS= 100 print
```

Below is the flux mesh plot on the side of the cylindrical source on the
XZ plane.

<!-- image -->

Below is the flux mesh plot on top of the cylindrical source on the XY
plane.

<!-- image -->

Listing 2.28: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 0 1 basis 0 1 0 1 0 0 file end end
```

## 2.3 Directional Sources

## 2.3.1 Monodirectional Source

Monodirectional disk source example from 'An MCNP Primer' by Shultis and
Faw, page 13 (see Helpful Links ).

```
Degenerate Cylindrical Source c 10 0 -1 IMP:N=1 99 0 +1 IMP:N=0 1 SO 30
```

Listing 2.29: MCNP6 Input File

Below is the mesh plot of the flux of degenerate cylindrical disk seen on the XY plane.

<!-- image -->

The 1.2-Mev neutrons are uniformly emitted in the +z-direction as seen below in the flux mesh plot. Note that the default direction of the neutrons is isotropic if no DIR distribution is specified.

<!-- image -->

<!-- image -->

Listing 2.30: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 ex 20 basis 1 0 0 0 0 1 ex 26 file end end
```

## 2.3.2 Cone Beam

Example of uniformly distributed cone source with azimuthal symmetry.

```
14 MeV neutrons point source c 10 0 -1 IMP:N=1 $ Inside shpere 99 0 +1 IMP:N=0 $ Outside world 1 SO 2.0 MODE N NPS 1e6 c
```

Listing 2.31: MCNP6 Input File

```
c ===> Single source energy c SDEF X=0 Y=0 Z=0 ERG=14.0 VEC= 1 0 0 DIR=D1 SI1 -1 0.90 1 SP1 0 0.0 1 c c ===> fmesh tally surrounding the source c FMESH4:N GEOM= xyz ORIGIN= -1.0 -1.0 -1.0 IMESH= 1.0 IINTS= 100 JMESH= 1.0 JINTS= 100 KMESH= 1.0 KINTS= 100 c print
```

Below is a mesh plot of the flux showing a cone source with half angle
of 25.8 degrees along the positive x-axis.

<!-- image -->

Flux mesh plot slicing through the x=0.5 cm plane seen on the YZ plane.

<!-- image -->

Listing 2.32: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 0 1 basis 1 0 0 0 0 1 px 0.5 file end end
```

## 2.3.3 Hollow Cone Source

Example of uniformly sampled hollow cone source with azimuthal symmetry.

```
14 MeV neutrons point source c 10 0 -1 IMP:N=1 $ Inside sphere 99 0 +1 IMP:N=0 $ Outside world 1 SO 2.0 MODE N NPS 1e3 c SDEF X=0 Y=0 Z=0 ERG=14.0 VEC= 1 0 0 DIR=D1 SI1 -1 0.80 0.90 1 $ Variable information SP1 0 0.0 1.0 0 $ Variable probability c FMESH4:N GEOM= xyz ORIGIN= -1.0 -1.0 -1.0 IMESH= 1.0 IINTS= 100 JMESH= 1.0 JINTS= 100 KMESH= 1.0 KINTS= 100
```

Listing 2.33: MCNP6 Input File

print

Below is a mesh plot of the flux showing a hollow cone source in the XY
plane seen between 0 . 9 &lt; 𝜇 &lt; 0 . 8 only, with no source for 𝜇 &lt; 0 . 8
and 𝜇 &gt; 0 . 9 .

<!-- image -->

From the bottom of the source cone shape seen from the YZ plane, a
circular ring can be seen in the sliced source cone.

<!-- image -->

Listing 2.34: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 0 1 basis 1 0 0 0 0 1 px 0.5 file end end
```

## 2.4 Multiple Independent Distributions

## 2.4.1 Space, Energy and Time Distributions

Example of a uniformly sampled spherical distribution with independent
energy and time distributions.

```
Basic Source in a Sphere 100 0 -1 IMP:N=1 $ inside sphere 999 0 1 IMP:N=0 $ outside world 1 SO 1 MODE N NPS 1E6 PRDMP 2J -1 c SDEF POS=0 0 0 RAD=D1 ERG=D2 TME=D3 c
```

Listing 2.35: MCNP6 Input File

```
SI1 0 1 $ RAD distribution SP1 -21 2 c SI2 S 21 22 $ ERG distribution SP2 1 2 SP21 -3 $ Watt spectrum SI22 L 1.1 1.5 2.2 $ Discrete lines SP22 2 1 3 c SI3 H 10 100 $ Pulse SP3 0 1 c F1:N 1 $ ERG and TME tallies E1 1E-6 100ilog 10 T1 0 100i 200 c FMESH4:N GEOM=XYZ $ Geometry tally ORIGIN=-1 -1 -1 IMESH=1 IINTS=50 JMESH=1 JINTS=50 KMESH=1 KINTS=50 TYPE=SOURCE OUT=NONE
```

The energy distribution can be seen below where a continuous Watt
spectrum defined by distribution 21 and the three discrete lines are
defined in distribution 22. The selection of these two independent
energy distributions is defined in distribution 2.

<!-- image -->

The time distribution can be seen below where the uniform PDF is defined
in distribution 3.

The position distribution can be seen below with a uniform PDF in the spherical volume is defined in distribution 1.

<!-- image -->

<!-- image -->

Listing 2.36: MCNP6 Plotting Commands

```
tal 1 loglog free e xlims 1e-3 10 tal 1 linlin free t xlims 0 200 fmesh 4 file end end
```

## 2.4.2 Multiple Spatial Variable Distributions

Example of a uniformly distributed monoenergetic source inside a
rectangular parallelpiped taken from 'An MCNP Primer' by Shultis and
Faw, page 12 (see Helpful Links ).

```
Rectangular Parallelepiped Parallel to Axis c 10 0 -1 IMP:P=1 $ Inside parallelpiped 99 0 +1 IMP:P=0 $ Outside parallelpiped 1 RPP -15 15 -20 20 -30 30 MODE P NPS 1e6
```

Listing 2.37: MCNP6 Input File

```
c SDEF X=D1 Y=D2 Z=D3 ERG=1.25 PAR=2 SI1 -10 10 $ X-range limits for source volume SP1 0 1 $ Umiform probability over x-range SI2 -15 15 $ Y-range limits for source volume SP2 0 1 $ Uniform probability over y-range SI3 -20 20 $ Z-range limits for source volume SP3 0 1 $ Uniform probability over z-range c FMESH4:P GEOM= xyz ORIGIN= -30.0 -30.0 -30.0 IMESH= 30.0 IINTS= 100 JMESH= 30.0 JINTS= 100 KMESH= 30.0 KINTS= 100 TYPE=SOURCE
```

Below is the source seen on the XY plane.

<!-- image -->

Below is the source seen on the YZ plane.

<!-- image -->

Below is the source seen on the XZ plane.

<!-- image -->

Listing 2.38: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 ex 20 basis 0 1 0 0 0 1 ex 20 basis 1 0 0 0 0 1 ex 20 file end end
```

## 2.4.3 Single Cell Rejection

Example of the cell rejection method, where sampling is uniform within a
parallelepliped and rejected if not within the desired cell. This
example is taken from 'An MCNP Primer' by Shultis and Faw, page 12 (
Helpful Links ).

```
Source in a Complex Cell: Enclosing Parallelepiped Rejection Method c 8 0 -1:-2:-3:-4:-5:-6 IMP:P=1 $ Inside complex cell 99 0 #8 IMP:P=0 $ Outside complex cell
```

Listing 2.39: MCNP6 Input File

```
1 SO 4 2 SX 4.1 3 3 SZ 4 3 4 SY 2 5 5 S 1 2 3 4 6 S -2 -3 -4 2.85 MODE P NPS 1e6 c c Cell 8 is a complex source in which monoenergetic isotropic volumetric c source exists. A rectangular parallelepiped envelops this cell (MCNP does c NOT Check this!). Points, randomly picke din the rectangular parallelepiped c are accepted as source points only if they are inside cell 8. c SDEF X=D1 Y=D2 Z=D3 ERG=1.25 PAR=2 CEL=8 c c NOTE: source parallelepipied is larger than cell 8, and hence source c positions sampled outside cell 8 are rejected c SI1 -12 12 $ X-range limits for source volume SP1 0 1 $ Umiform probability over x-range SI2 -11 11 $ Y-range limits for source volume SP2 0 1 $ Uniform probability over y-range SI3 -13 13 $ Z-range limits for source volume SP3 0 1 $ Uniform probability over z-range c FMESH4:P GEOM= xyz ORIGIN= -30.0 -30.0 -30.0 IMESH= 30.0 IINTS= 100 JMESH= 30.0 JINTS= 100 KMESH= 30.0 KINTS= 100 TYPE=SOURCE
```

Due to rejection method the source is only seen in cell 8 as in the mesh
plot below on the XY plane.

Mesh plot now viewed from the YZ plane.

<!-- image -->

Mesh plot now viewed from the XZ plane.

<!-- image -->

<!-- image -->

Listing 2.40: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 ex 10 basis 0 1 0 0 0 1 ex 10 basis 1 0 0 0 0 1 ex 10 file end end
```

## 2.4.4 Multiple Cell Rejection

Example of uniformly sampling in a cylindrical volume and rejecting the
sample if not in one of the two cells specified. This allows the source
strength to vary by cell location (strength). This example was taken
from 'An MCNP Primer' by Shultis and Faw, page 14 (see Helpful Links ).

```
Two Cylindrical Volumetric Sources 8 0 -10:-20:-30:-40:-50 IMP:N=1 9 0 -60:-70:-80 IMP:N=1 999 0 #8 #9 IMP:N=0 10 SY -25 15 20 S 0 -25 12 7 30 S -12 -25 0 6 40 S -2 -22 -13 8 50 S 0 -40 4 9 60 S 0 25 10 15 70 S -4 15 5 7
```

Listing 2.41: MCNP6 Input File

```
80 S 6 25 20 8 MODE N NPS 1E6 c c ---2 volumetric sources uniformly distributed in cells 8 & 9 both sources c emit-1.25 Mev photons. Surrounded both source cells by large sampling c cylinder defined by the POS RAD and EXT parameters. The rejection c technique is used to pick source points points with cells 8 & 9 with the c specified frequency. c SDEF ERG=1.25 CEL d1 AXS=0 0 1 POS 0 0 0 RAD d2 EXT d5 c SI1 L 8 9 $ Source cells: src 1=cell 8, src 2=cell9 SP1 0.8 0.2 $ 80% from src 1; 20% from src2=cell 9 c SI2 0 50 $ Radius of cyl. containing cells 8 & 9 c SI5 -30 30 $ Axial range of cyl. containing src cells c FMESH4:N GEOM= xyz ORIGIN= -50.0 -50.0 -50.0 IMESH= 50.0 IINTS= 200 JMESH= 50.0 JINTS= 200 KMESH= 50.0 KINTS= 200 TYPE=SOURCE
```

Below is cell 9 and 8 sources on the XZ plane.

<!-- image -->

Below is cell 9 and 8 sources on the XY plane.

<!-- image -->

Listing 2.42: MCNP6 Plotting Commands

<!-- image -->
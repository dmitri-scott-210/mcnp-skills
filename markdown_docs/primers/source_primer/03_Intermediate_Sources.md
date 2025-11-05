---
title: "Source Primer Chapter 3 - Intermediate Sources"
chapter: "Source-3"
source_pdf: "mcnp6-primer-docs/mcnp6-source-primer/3.Intermediate_Sources.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## THREE

## INTERMEDIATE SOURCES

Sources with dependant variables, embedded distributions and cookie
cutter cells.

## 3.1 Dependent Variables

## 3.1.1 Energy Dependent on Position

This example shows how the energy depends on the sampled position.

```
Photon dependent point sources c 10 0 -1 IMP:P=1 $ Inside sphere 99 0 +1 IMP:P=0 $ Outside world 1 SO 2.0 MODE P NPS 1e6 c SDEF POS=D10 ERG=FPOS=D20 c SI10 L 0 0 -0.6 0 0 +0.6 $ Discrete values SP10 1 1 $ Probabilities for values DS20 L 0.14 1.88 $ Discrete values c FMESH4:P GEOM= xyz ORIGIN= -1.0 -1.0 -1.0 IMESH= 1.0 IINTS= 100 JMESH= 1.0 JINTS= 100 KMESH= 1.0 KINTS= 100 OUT=NONE print
```

Listing 3.1: MCNP6 Input File

Below is an S-38 1.88 MeV gamma-ray point source and a Tc-99m 0.14 MeV
gamma-ray point source shown on the XZ plane.

One of the point sources alone on the XY plane is seen below. Note that the output file contains the first 50 source particles in print table 110, where the energy and position sampling can be verified.

<!-- image -->

<!-- image -->

Listing 3.2: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 0 1 basis 0 1 0 1 0 0 file end end
```

## 3.1.2 Position Dependent on Energy

Example of two cylindrical sources containing different sources. In this
example, the position, radius and extent are all functions of the
selected photon energy, taken from 'An MCNP Primer' by Shultis and Faw,
page 14 (see Helpful Links ).

```
Plane Sources (Degenerate Rectangular Parallelepiped) c 10 0 -1 IMP:P=1 $ Inside parallelpiped 99 0 +1 IMP:P=0 $ Outside parallelpiped 1 RPP -60 60 -60 60 -60 60 MODE P
```

Listing 3.3: MCNP6 Input File

```
NPS 1e6 c c ---Two spatially different cylindrical monoenergetic sources. The size c and position of each cyl. source depends on the source energy (FERG). c SDEF ERG=D1 POS=FERG D8 AXS=0 0 1 RAD=FERG D2 EXT=FERG D5 c c --Set source energies: 0.667 MeV for region 1 and 1.25 MeV for region 2 c SI1 L 0.667 1.25 $ Fix energies SP1 0.4 0.6 $ 20% from src 1(Cs-137); 80% from src 2 (Cs-60) c DS8 S 9 10 $ Get position for chosen source SI9 L -30 0 0 $ Center for sampling of src1 SP9 1 $ Prob. distn for src 2 center SI10 L 30 0 0 $ Center for sampling of src2 SP10 1 $ Prob. distn for src 2 center C --Set radius and axial limits for each source DS2 S 3 4 $ Sampling distn from each src axis SI3 0 20 $ Radial sampling limits for src1 SP3 -21 1 $ Radial sampling weight for src1 r^1 SI4 0 10 $ Radial sampling limits for src2 SP4 -21 1 $ Radial sampling weight for src2 r^1 DS5 S 6 7 $ Axial sampling distns for each src SI6 -10 10 $ Axial sampling limits for src1 SP6 -21 0 $ Axial sampling weight for src1 r^0 SI7 -30 30 $ Axial sampling limits for src2 SP7 -21 0 $ Axial sampling weight for src2 r^0 c FMESH4:P GEOM= xyz ORIGIN= -50.0 -50.0 -50.0 IMESH= 50.0 IINTS= 100 JMESH= 50.0 JINTS= 100 KMESH= 50.0 KINTS= 100 EMESH= 1 2 TYPE=SOURCE OUT=NONE
```

Below are the two monoenergetic sources.

<!-- image -->

## Below is the 0.667 MeV Cs-137 source on the left.

Below is the 1.25 MeV Co-60 source on the right.

<!-- image -->

<!-- image -->

Listing 3.4: MCNP6 Plotting Commands

```
fmesh 4 bas 1 0 0 0 1 0 ebin 1 ebin 2 file end end
```

## 3.1.3 Position and Energy Dependent on Cell

Example of the cell rejection method where the position, radius and
extent position sampling as well as the energy is dependent on the
sampled cell. This is an easy approach for two arbitrary volumetric
sources with different energy photons. This example was taken from 'An
MCNP Primer' by Shultis and Faw, page 14 (see Helpful Links ).

```
Two Arbitrary Volumetric Sources with different Energy Photons 8 0 -10:-30:-20:-40 IMP:N=1 9 0 -50:-60:-70:-80:-90:-100 IMP:N=1 999 0 #8 #9 IMP:N=0 10 S -32 0 -3 7 20 S -34 -5 0 5 30 S -25 3 -5 5 40 S -32 0 4 6 50 SX 30 6 60 S 30 0 3 6 70 S 30 0 -3 6 80 S 34 0 -4 6 90 S 31 0 -8 4 100 S 31 0 8 4
```

Listing 3.5: MCNP6 Input File

```
MODE N NPS 1E6 c c ---2 volumetric monoenergetic sources in comples-shaped cells 8 & 9 c Spatial sampling uses the rejection technique by placing a finite cylinder c over each source cell. A random point inside a cylinder is accepted as a c source point only if it is inside the source photon energies are functions c of the source cells (FCEL). c SDEF CEL=D1 AXS=0 0 1 POS=FCEL D2 RAD=FCEL D5 EXT=FCEL D8 ERG=FCEL D20 c SI1 L 8 9 $ Choose which cell source refion to use for source SP1 0.4 0.6 $ 40% from src 1; 60% from src2 c --Set POS for each source DS2 S 3 4 $ Based on the cell chosen, set distributions for POS SI3 L -30 0 0 $ Center for spatially sampling of src1 SP3 1 $ Prob. distn for src1 center SI4 L 30 0 0 $ Center for spatially sampling of src2 SP4 1 $ Prob. distn for src2 center c --Set RAD for each source (must completely include cells 8 & 9 DS5 S 6 7 $ Distns for sampling axially for each src SI6 0 20 $ Radial sampling limits for src1 SP6 -21 1 $ Radial sampling weight for src1 SI7 0 10 $ Radial sampling limits for src2 SP7 -21 1 $ Radial sampling weight for src2 c --Set EXT for each source (must completely include cells 8 & 9) DS8 S 9 10 $ Distns for sampling axially for each src SI9 -10 10 $ Axial Sampling limits for src1 SP9 -21 0 $ Axial sampling weight for src1 SI10 -30 30 $ Axial sampling limits for src2 SP10 -21 0 $ Axial sampling weight for src2 c --Set energies of photons for each source DS20 S 21 22 SI21 L 0.6938 1.1732 1.3325 $ Co-60 spectra for src1 SP21 D 1.6312E-4 1 1 $ Frequencies of gammas SI22 L 0.667 $ Cs-137 spectrum for src2 SP22 D 1 c F14:N 8 9 T SD14 1 1 1 E14 0.5 99i 1.5 c FMESH4:N GEOM= xyz ORIGIN= -75.0 -75.0 -75.0 IMESH= 75.0 IINTS= 100 JMESH= 75.0 JINTS= 100 KMESH= 75.0 KINTS= 100 TYPE=SOURCE OUT=NONE
```

Below is the energy distribution in cell 8.

<!-- image -->

Below is the energy distribution in cell 9.

<!-- image -->

Below is the total energy distribution in cells 8 and 9.

<!-- image -->

## Below is cell 8 and 9 sources on the XY plane.

<!-- image -->

Below is cell 8 and 9 sources on the XZ plane.

<!-- image -->

Listing 3.6: MCNP6 Plotting Commands

```
tal 14 fixed f 1 fixed f 2 fixed f 3 fmesh 4 bas 1 0 0 0 1 0 bas 1 0 0 0 0 1 file end end
```

## 3.1.4 Cell Dependent on Position

This example shows how the cell depends on the sampled position.
According to the manual, this should likely not work, but appears to
give the expected source distribution.

```
SDEF TESTING 10 1 1E-6 -1 IMP:N=1 $ inside sphere 1 20 1 1E-6 -2 IMP:N=1 $ inside sphere 2 30 1 1E-6 -3 IMP:N=1 $ inside sphere 3 40 1 1E-6 -4 IMP:N=1 $ inside sphere 4 50 2 1E-6 -5 1 2 3 4 IMP:N=1 $ inside box 99 0 5 IMP:N=0 $ outside 1 S 2.5 2.5 0 0.5 2 S 7.5 2.5 0 0.5 3 S 2.5 7.5 0 0.5 4 S 7.5 7.5 0 0.5 5 RPP 0 10 0 10 -1 1 MODE N
```

Listing 3.7: MCNP6 Input File

```
NPS 1e6 PRINT c M1 92235 1 M2 8016 1 1001 2 c FMESH4:N GEOM=XYZ ORIGIN=0 0 -1 IMESH=10 IINTS=100 JMESH=10 JINTS=100 KMESH=1 KINTS=1 TYPE=SOURCE c SDEF POS=D1 CEL=FPOS=D2 RAD=D7 c SI1 L 2.5 2.5 0 $ POS distribution 7.5 2.5 0 2.5 7.5 0 7.5 7.5 0 SP1 1 2 3 4 c DS2 S 3 4 5 6 c SI3 L 10 SP3 1 c SI4 L 20 SP4 1 c SI5 L 30 SP5 1 c SI6 L 40 SP6 1 c SI7 0 0.5 SP7 -21 2
```

Below is the XY mesh plot of the four spherical sources.

<!-- image -->

Listing 3.8: MCNP6 Plotting Commands

```
fmesh 4 file end end
```

## 3.1.5 Spherical Radius Dependent on Position

This example shows how the radius of the spherical volume source depends
on the sampled position (RAD=FPOS). According to the manual, this should
likely not work, but appears to give the expected source distribution in
the radial dimension.

```
SDEF TESTING 10 1 1E-6 -1 IMP:N=1 $ inside sphere 1 20 1 1E-6 -2 IMP:N=1 $ inside sphere 2 30 1 1E-6 -3 IMP:N=1 $ inside sphere 3 40 1 1E-6 -4 IMP:N=1 $ inside sphere 4 50 2 1E-6 -5 1 2 3 4 IMP:N=1 $ inside box 99 0 5 IMP:N=0 $ outside 1 S 2.5 2.5 0 0.5 2 S 7.5 2.5 0 0.5
```

Listing 3.9: MCNP6 Input File

```
3 S 2.5 7.5 0 0.5 4 S 7.5 7.5 0 0.5 5 RPP 0 10 0 10 -1 1 MODE N NPS 1e6 PRINT c M1 92235 1 M2 8016 1 1001 2 c FMESH4:N GEOM=XYZ ORIGIN=0 0 -1 IMESH=10 IINTS=200 JMESH=10 JINTS=200 KMESH=1 KINTS=50 TYPE=SOURCE c SDEF POS=D1 RAD=FPOS=D2 c SI1 L 2.5 2.5 0 $ POS distribution 7.5 2.5 0 2.5 7.5 0 7.5 7.5 0 SP1 1 1 1 1 c DS2 S 3 4 5 6 c SI3 0 0.2 SP3 -21 2 c SI4 0.2 0.4 SP4 -21 2 c SI5 0.4 0.6 SP5 0 1 c SI6 L 0.8 SP6 1
```

Below is the XY mesh plot of the four spherical sources to show the
radial sampling is correct for each of the sampled positions.

<!-- image -->

Listing 3.10: MCNP6 Plotting Commands

<!-- image -->

## 3.1.6 Cylindrical Extent Dependent on Position

This example shows how the extent of the cylindrical volume source
depends on the sampled position (EXT=FPOS). According to the manual,
this should likely not work, but appears to give the expected source
distribution in both radial and extent dimensions.

```
SDEF TESTING 10 1 1E-6 -1 IMP:N=1 $ inside sphere 1 20 1 1E-6 -2 IMP:N=1 $ inside sphere 2 30 1 1E-6 -3 IMP:N=1 $ inside sphere 3 40 1 1E-6 -4 IMP:N=1 $ inside sphere 4 50 2 1E-6 -5 1 2 3 4 IMP:N=1 $ inside box 99 0 5 IMP:N=0 $ outside 1 S 2.5 2.5 0 0.5 2 S 7.5 2.5 0 0.5
```

Listing 3.11: MCNP6 Input File

```
3 S 2.5 7.5 0 0.5 4 S 7.5 7.5 0 0.5 5 RPP 0 10 0 10 -1 1 MODE N NPS 1e6 PRINT c M1 92235 1 M2 8016 1 1001 2 c FMESH4:N GEOM=XYZ ORIGIN=0 0 -1 IMESH=10 IINTS=200 JMESH=10 JINTS=200 KMESH=1 KINTS=50 TYPE=SOURCE c SDEF POS=D1 EXT=FPOS=D2 AXS=0 0 1 RAD=D8 c SI1 L 2.5 2.5 -0.1 $ POS distribution 7.5 2.5 -0.1 2.5 7.5 -0.1 7.5 7.5 -0.1 SP1 1 1 1 1 c DS2 S 3 4 5 6 c SI3 L 0.1 SP3 1 c SI4 0 0.2 SP4 0 1 c SI5 0 0.4 SP5 0 1 c SI6 0.2 0.6 SP6 0 1 c SI8 0 0.5 SP8 -21 1
```

Below is the XY mesh plot of the four cylindrical sources to show the
radial sampling is correct for each of the sampled positions.

<!-- image -->

Both plots below show the XZ mesh plot of the four cylinders. Slicing
through the Y=2.5 plane:

<!-- image -->

And slicing through the Y=7.5 plane:

<!-- image -->

Listing 3.12: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 basis 1 0 0 0 0 1 origin 5 2.5 0 extent 4 basis 1 0 0 0 0 1 origin 5 7.5 0 extent 4 file end end
```

## 3.1.7 Cylindrical Radius Dependent on Position

This example shows how the radius of the cylindrical volume source
depends on the sampled position (RAD=FPOS). According to the manual,
this should likely not work, but appears to give the expected source
distribution in both radial and extent dimensions.

```
SDEF TESTING 10 1 1E-6 -1 IMP:N=1 $ inside sphere 1 20 1 1E-6 -2 IMP:N=1 $ inside sphere 2 30 1 1E-6 -3 IMP:N=1 $ inside sphere 3 40 1 1E-6 -4 IMP:N=1 $ inside sphere 4 50 2 1E-6 -5 1 2 3 4 IMP:N=1 $ inside box 99 0 5 IMP:N=0 $ outside 1 S 2.5 2.5 0 0.5 2 S 7.5 2.5 0 0.5 3 S 2.5 7.5 0 0.5 4 S 7.5 7.5 0 0.5 5 RPP 0 10 0 10 -1 1 MODE N NPS 1e6 PRINT
```

Listing 3.13: MCNP6 Input File

```
c M1 92235 1 M2 8016 1 1001 2 c FMESH4:N GEOM=XYZ ORIGIN=0 0 -1 IMESH=10 IINTS=200 JMESH=10 JINTS=200 KMESH=1 KINTS=50 TYPE=SOURCE c SDEF POS=D1 RAD=FPOS=D2 AXS=0 0 1 EXT=D7 c SI1 L 2.5 2.5 0.0 $ POS distribution 7.5 2.5 0.0 2.5 7.5 0.0 7.5 7.5 0.0 SP1 1 1 1 1 c DS2 S 3 4 5 6 c SI3 0 0.2 SP3 -21 1 c SI4 0.2 0.4 SP4 -21 1 c SI5 0.4 0.6 SP5 0 1 c SI6 L 0.8 SP6 1 c SI7 -0.1 0.1 SP7 0 1
```

Below is the XY mesh plot of the four cylindrical sources to show the
radial sampling is correct for each of the sampled positions.

<!-- image -->

Both plots below show the XZ mesh plot of the four cylinders. Slicing
through the Y=2.5 plane:

<!-- image -->

And slicing through the Y=7.5 plane:

<!-- image -->

Listing 3.14: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 basis 1 0 0 0 0 1 origin 5 2.5 0 extent 4 basis 1 0 0 0 0 1 origin 5 7.5 0 extent 4 file end end
```

## 3.2 Embedded Functions

## 3.2.1 Embedded Time Distributions

This example includes an embedded time distribution corresponding to a
pulsed source that varies in overall pulse strength as a function of
time. Taken from the MCNP6 User's Manual, page 3-153 (see Helpful Links
).

```
Embedded Time Distributions 8 0 -10 IMP:P=1 99 0 10 IMP:P=0 10 SO 1 MODE P NPS 1E6 c SDEF ERG D21 CEL=D11 TME=D41 c ---Set cell SI11 L 8 SP11 1 c ---Set energy SP21 -3
```

Listing 3.15: MCNP6 Input File

<!-- image -->

Below is a plot of the overall time distribution of the source that has
multiple levels of embedded distributions.

<!-- image -->

```
tal 1 linlin free t bar file end end
```

Listing 3.16: MCNP6 Plotting Commands

## 3.3 Cookie Cutter Cell

## 3.3.1 Intersecting Directional Beams

In this example, three monodirectional intersecting beams are modeled by
sampling the X and Y positions with a truncated Gaussian distribution
and then translating the source beam into three separate locations. To
truncate the Gaussian distribution, the cookie cutter cell (ellipsoid in
this case) is used on the CCC card. This example was taken from the
MCNP6 User's Manual, page 3-151 (see Helpful Links ).

```
Cookie Cutter Cell Beams 888 0 -10 +9 IMP:N=1 999 0 -9 -10 IMP:N=1 $ Cookie cutter cell 1000 0 #999 #888 IMP:N=0 $ outside world 10 SO 2.5 9 SQ 25 100 0 0 0 0 -4 0 0 0 $ cookie cutter surface NPS 1E5 c SDEF DIR=1 VEC=0 0 1 X=D1 Y=D2 Z=0 CCC=999 TR=D3 SP1 -41 0.470964 0 SP2 -41 0.235482 0 SI3 L 11 22 33 SP3 1 2 3 SB3 1 2 3 TR11 0 0 -2 1 0 0 0 1 0 0 0 1 TR22 -2 0 0 0 1 0 0 0 1 1 0 0 TR33 0 -2 0 0.707107 0 0.707107 0.707107 0 -0.707107 0 1 0 c FMESH4:N GEOM= xyz ORIGIN= -2.5 -2.5 -2.5 IMESH= 2.5 IINTS= 150 JMESH= 2.5 JINTS= 150 KMESH= 2.5 KINTS= 150 OUT=NONE
```

Listing 3.17: MCNP6 Input File

The flux from the source beams are seen intersecting on the different
planes with visual of the cookie cutter cell at the origin. Below is the
XY plane.

Below is the YZ plane.

<!-- image -->

Below is the XZ plane.

<!-- image -->

The following show the source locations and shape on the same mesh plots. Below is the XY plane.

<!-- image -->

<!-- image -->

## Below is the YZ plane.

<!-- image -->

Below is the XZ plane.

<!-- image -->

Listing 3.18: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 ex 3 basis 0 1 0 0 0 1 ex 3 basis 1 0 0 0 0 1 ex 3 basis 1 0 0 0 1 0 ex 3 or 0 0 -2 basis 0 0 1 0 1 0 ex 3 or -2 0 0 basis 1 0 0 0 0 1 ex 3 or 0 -2 0 file end end
```
---
title: "Chapter 5.11 - Superimposed Mesh Tallies"
chapter: "5.11"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.11_Superimposed_Mesh_Tallies.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

- The MCNP code may not be able to compute the volume of a region. In this case, the MCNP code prints zero to the TSUNAMI-B file.
- In the place where TSUNAMI-B reports the number of uses of the region, the MCNP code reports the number of spatial zones on this instance of KSEN .
- For fissionχ sensitivities, the ones reported are automatically summed over all incident energy grids as the TSUNAMI-B format does not support this.
- The TSUNAMI-B format does not support scattering laws, so these are omitted.

## 5.11 Superimposed Mesh Tallies

MCNP6 offers two different mesh tallies to the user. The TMESH tally was
developed for the MCNPX code, while the FMESH tally was developed for
MCNP5. Although similar, each method is characterized by its own syntax,
card format, and output files. The user is encouraged to read about both
methods and choose the one that is most appropriate for his or her
problem.

## 5.11.1 TMESH: Superimposed Mesh Tally A

The TMESH tally is a method of graphically displaying particle flux,
dose, or other quantities on a rectangular, cylindrical, or spherical
grid overlaid on top of the standard problem geometry. Particles are
tracked through the independent mesh as part of the regular transport
problem. The contents of each mesh cell are written to the RUNTPE file
and can be plotted with the MCNP6 geometry plotter superimposed over a
plot of the problem geometry. The TMESH tally data are also written to
the MCTAL file and can be plotted with the MCNP6 tally plotter, MCPLOT.

Further, the TMESH tally data are written to the mdata file at the end
of each initial or restarted calculation. The gridconv utility [Appendix
E.4] can convert the mdata file into a number of standard formats
suitable for reading by various graphical analysis packages.

Four different mesh-tally types are provided by TMESH , depending on the
information the user wishes to view:

| Type 1   | Track-Averaged Mesh Tally [§5.11.1.2]    |
|----------|------------------------------------------|
| Type 2   | Source Mesh Tally [§5.11.1.3]            |
| Type 3   | Energy Deposition Mesh Tally [§5.11.1.4] |
| Type 4   | DXTRAN Mesh Tally [§5.11.1.5]            |

Each of the four types has its own associated keywords and input values.

Examples involving the superimposed geometry TMESH tally are available
in §6.4.3.

## 5.11.1.1 Setting Up the TMESH Tally in the MCNP Input File

All of the input for TMESH tallies must be in a dedicated set of cards
in the MCNP input file data-card block. This set must start with a card
containing the word TMESH in the first five columns and end with a card
containing the word ENDMD in the first five columns. For each requested
mesh tally (a maximum of 20 TMESH tallies are permitted), a minimum of
four cards must exist between the TMESH and ENDMD cards: an RMESH ,
CMESH , or SMESH control card, and CORA , CORB , and CORC cards.
Optional cards within the mesh-tally block include ERGSH and MSHMF . An
FM tally multiplier card may be specified only for Type 1 TMESH mesh
tallies; however, if an FM card is associated with a Type 1 mesh tally,
it must appear outside of the TMESH / ENDMD card block. Each of these
cards is described in the discussion that follows.

The basic structure of the desired mesh as well as what quantities are
to be stored to the mesh tally are determined by a mesh control card (
RMESH , CMESH , or SMESH ). The general form of the control cards
follow:

```
RMESH n : P KEYWORD = value(s) ... CMESH n : P KEYWORD = value(s) ... SMESH n : P KEYWORD = value(s) ... where RMESH specifies a rectangular mesh; CMESH specifies a cylindrical mesh; SMESH specifies a spherical mesh; n is a user-defined mesh-tally number for which the last digit of n , defines the type (1, 2, 3, or 4) of mesh tally and, consequently, the type of information to be stored in the mesh; and P is the particle type to be tallied-this parameter may or may not be required, depending on the mesh-tally type; KEYWORD options vary depending on the mesh-tally type.
```

The notation X MESH will be used in subsequent sections to indicate any
of the three mesh geometries. Input keywords for the four mesh-tally
types are described in sections that follow. Note that the chosen mesh-
tally number must be different from all other tallies in the problem.
For example, an F1:N tally will conflict with a RMESH1:N tally.

In addition to the X MESH control card, the following set of cards
provides details about the TMESH mesh characteristics and must be
present for each requested mesh tally:

```
CORA n corra n, 1 corra n, 2 . . . CORB n corrb n, 1 corrb n, 2 . . . CORC n corrc n, 1 corrc n, 2 . . .
```

where n is the same user-defined mesh-tally number as that on the
associated X MESH control card. The mesh tally number must end in 1, 2,
3, or 4 corresponding to the mesh tally type. The entries on the CORA ,
CORB , and CORC cards describe a mesh in three coordinate directions as
defined by the mesh type (rectangular,

cylindrical, or spherical), prior to any transformation. Each tally type
supports an optional TRANS keyword to allow the application of a
coordinate transformation to the mesh.

To describe a rectangular mesh, the entries on the CORA card represent
planes perpendicular to the x axis, CORB entries are planes
perpendicular to the y axis, and CORC entries are planes perpendicular
to the z axis. Bins do not have to be equally spaced.

To describe a cylindrical mesh, the middle coordinate, CORB , is the
untransformed z axis, which is the symmetry axis of the cylinder, with
radial meshes defined on the CORA input line. The first smallest radius
must be equal to zero. The values following CORB define planes
perpendicular to the untransformed z axis. The values following CORC are
positive angles relative to a counter-clockwise rotation about the
untransformed z axis. These angles, in degrees, are measured from the
positive x axis and must have at least one entry of 360, which is also
required to be the last entry. The lower limit of zero degrees is
implicit and never appears on the CORC card.

For spherical meshes, scoring will happen within a spherical volume, and
can also be further defined to fall within a conical section defined by
a polar angle (relative to the + z axis) and azimuthal angle. The CORA
card entries are sphere radii; inner and outer radii are required. The
CORB entries define the polar angle meshing in which the polar angle
ranges from 0 to 180 degrees, the 1st bin must be greater than 0
degrees, and the last bin must be 180. The CORC entries are the same as
in the cylindrical case, with the 1st bin greater than 0 degrees and the
last bin equal to 360. It is helpful in setting up spherical problems to
think of the longitude-latitude coordinates on a globe.

The ' I ' data-input notation [§4.4.5.1] is allowed, enabling a large
number of regularly spaced mesh points to be defined with a minimum of
entries on the coordinate lines. All of the coordinate entries must be
monotonically increasing for the tally mesh features to work properly,
but do not need to be equally spaced. It should be noted that the size
of these meshes scales with the product of the number of entries for the
three coordinates. Machine memory could become a problem for very large
meshes with fine spacing.

Additional cards that can be used with TMESH mesh tallies include the
following:

ERGSH n e e

1 2 MSHMF m e 1 f 1 e 2 f 2 ... e K f K FM n ...

where positive values on the ERGSH card, e 1 and e 2 , are the lower and
upper energy limits for information to be stored to mesh tally n . On
the other hand, negative values of e 1 and e 2 represent lower and upper
time limits (in shakes) for information to be stored to mesh tally n .
The default is to consider all energies and all times. The value of m on
the MSHMF card does not refer to a corresponding mesh tally; instead, m
is an arbitrary user-assigned value between 1 and 9. The entries on the
MSHMF card, e k and f k , are pairs of energies and the corresponding
response functions; as many pairs as needed can be designated. Use of
the FM card is limited to TMESH Type 1 mesh tallies [§5.11.1.2] and the
card must not appear inside the TMESH card block.

Note that the type 1 (particle track) and type 3 (energy deposition)
mesh tallies work with heavy ions although there is no capability to
separate out contributions from particular heavy ion species.

## 5.11.1.2 Track-averaged TMESH Mesh Tally (Type 1)

## /warning\_sign Caution

Due to copyright concerns the DOSE keyword has been deactivated and the
built-in flux-to-dose conversion factors removed from the source code.
They are available in Appendix F.1 formatted as MCNP input for DE / DF
cards. Use the MFACT keyword and the MSHMF card to add a flux-to-dose
conversion response function.

The first TMESH mesh type scores track-averaged data such as flux,
tracks, population and energy deposition. The MSHMF card can be used to
apply a response function.

| Data-card Form: X MESH n: P KEYWORD = value(s) ...   | Data-card Form: X MESH n: P KEYWORD = value(s) ...                                                                                                                                                                                                                                                                   |
|------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                                    | Type 1 mesh-tally type identifier. Restriction: n = 1 , 11 , 21 , . . .                                                                                                                                                                                                                                              |
| P                                                    | the particle type(s).                                                                                                                                                                                                                                                                                                |
| TRAKS                                                | If TRAKS appears on the input line, tally the number of tracks through each mesh volume. No values accompany the keyword.                                                                                                                                                                                            |
| FLUX                                                 | If FLUX appears on the input line, then the average fluence is particle weight times track length divided by volume in units of number/cm 2 . If the source is considered to be steady state in particles per second, then the value becomes flux in number/cm 2 /second. No values accompany the keyword. (DEFAULT) |
| POPUL                                                | If POPUL appears on the input line, tally the population (i.e., weight times the track length) in each volume.                                                                                                                                                                                                       |
| PEDEP                                                | If PEDEP appears on the input line, scores the average energy deposition per unit volume (MeV/cm 3 /history) for the particle type P . In contrast to the 3rd type of mesh tally, energy deposition can be obtained in this option for any particular particle.                                                      |
| PEDEP                                                | This option allows one to score the equivalent of an F6 : P heating tally for the particle type P . Note, the mesh is independent of problem geometry, and a mesh cell may cover regions of several different masses. Therefore the normalization of the PEDEP option is per mesh cell volume, not per unit mass.    |
| MFACT                                                | Can have from one to four numerical entries following it. The value of the first entry, m , is an arbitrary number that refers to an energy-dependent response function given on an MSHMF m card. If m = - 1 , then it is followed by a single value that is used as a constant multiplier. (No                      |
| MFACT                                                | default)                                                                                                                                                                                                                                                                                                             |
| MFACT                                                | The second entry is 1 for linear interpolation and 2 for logarithmic interpolation. (DEFAULT is 1)                                                                                                                                                                                                                   |
| MFACT                                                | If the third entry is 0, the response is a function of the current particle energy; if the third entry is 1, the response is a function of the energy deposited (only valid with the PEDEP option). (DEFAULT is 0)                                                                                                   |
| MFACT                                                | The fourth entry is a constant multiplier and is the only floating-point entry allowed. (DEFAULT is 1.0)                                                                                                                                                                                                             |
| MFACT                                                | If any of the last three entries are used, the entries preceding it must be present so that the order of the entries is preserved. Only one MFACT keyword may be used per tally.                                                                                                                                     |

TRANS

## Default: None

## Details:

- 1 If a TR card is used with a TMESH tally, it must appear outside of the mesh data block between the TMESH and ENDMD cards.

It is possible to use the FM tally multiplier card to calculate reaction
rates in a type 1 mesh tally if both of the following criteria hold:

1. the FM card must not appear within the mesh data block between the TMESH and ENDMD cards; and
2. if the multiplier involves a MT reaction identifier, the FM card must be included in an equivalent F4 tally specification.

## 5.11.1.3 Source TMESH Mesh Tally (Type 2)

The second type of mesh tally scores source-point data, in which the
weight of the source particles P 1 , P 2 , P 3 , . . . , P n are scored
in mesh arrays 1 , 2 , 3 , ..., n . A separate mesh tally grid will be
produced for each particle chosen.

The usefulness of this method involves locating the source of particles
entering a certain volume, or crossing a certain surface. The user asks
the question, 'If particles of a certain type are present, where did
they originally come from?' In shielding problems, the user can then try
to shield the particles at their source.

This mesh tally is normalized as number of particles per SDEF source
particle.

| Data-card Form: X MESH n   | P 1 P 2 . . . KEYWORD = value(s) ...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                          | Type 2 mesh-tally type identifier. Restriction: n = 2 , 12 , 22 , . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| P k                        | Particle designators, i.e., n , p , e , etc. (See Table 4.3) Restriction: k ≤ 10 Source particles are considered to be those that come directly from the source defined by the user and those new particles created during nuclear interactions. One should be aware that storage requirements can get very large, very fast, depending on the dimensions of the mesh, because a separate histogram is created for each particle chosen. If there are no entries on this card, the information for neutrons is scored by default. |
| TRANS                      | Must be followed by a single reference to a TR card number that can be used to translate and/or rotate the entire mesh. Only one TR card reference is permitted with each card.                                                                                                                                                                                                                                                                                                                                                   |

Must be followed by a single reference to a TR card number that can be
used to translate and/or rotate the entire mesh. Only one TR card
reference is permitted with each card ( 1 ).

## 5.11.1.4 Energy Deposition TMESH Mesh Tally (Type 3)

The third type of mesh tally scores energy deposition data in which the
energy deposited per unit volume from all particles is included. This
can be due to the slowing of a charged particle, the recoil of a
nucleus, energy deposited locally for particles born but not tracked,
etc. The results are similar to the scoring of an +F6 tally.

Note that in MCNP6 the option to track energy deposition from one type
of particle alone in a problem is included in the first mesh tally type.
See the PEDEP keyword in §5.11.1.2. The energy deposition mesh tally
described here gives results for all particles tracked in the problem,
and has no option to specify a particular particle.

Because the mesh is independent of problem geometry, a mesh cell may
cover regions of several different masses. Therefore the normalization
of the output is per unit volume (MeV/cm 3 /source particle), not per
unit mass.

| Data-card Form: X   | MESH n KEYWORD = value(s) ...                                                                                                                                                                                                                                                                                                                                                        |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                   | Type 3 mesh-tally type identifier. Restriction: n = 3 , 13 , 23 , . . .                                                                                                                                                                                                                                                                                                              |
| TOTAL               | If TOTAL appears on the input line, score energy deposited from any source. No values accompany the keyword. (DEFAULT)                                                                                                                                                                                                                                                               |
| DE/DX               | If DE/DX appears on the input line, score ionization from charged particles. No values accompany the keyword.                                                                                                                                                                                                                                                                        |
| RECOL               | If RECOL appears on the input line, score energy transferred to recoil nuclei above tabular limits. No values accompany the keyword.                                                                                                                                                                                                                                                 |
| TLEST               | If TLEST appears on the input line, score track length folded with tabular heating numbers. No values accompany the keyword.                                                                                                                                                                                                                                                         |
| EDLCT               | If EDLCT appears on the input line, score non-tracked particles assumed to deposit energy locally. This allows the user to ascertain the potential error in the problem caused by allowing energy from non-tracked particles to be deposited locally. This can be a serious problem in neglecting the tracking of high-energy photons or electrons. No values accompany the keyword. |
| MFACT               | Can have from one to four numerical entries following it. The value of the first entry, m , is an arbitrary number that refers to an energy-dependent response function given on an MSHMF m card. If m = - 1 , then it is followed by a single value that is used as a constant multiplier. (No default)                                                                             |
| MFACT               | The second entry is 1 for linear interpolation, and 2 for logarithmic interpolation. (DEFAULT is 1)                                                                                                                                                                                                                                                                                  |
| MFACT               | If the third entry is 0, the response is a function of the current particle energy; if the third entry is 1, the response is a function of the energy deposited. (DEFAULT is 0)                                                                                                                                                                                                      |
| MFACT               | The fourth entry is a constant multiplier and is the only floating-point entry allowed (DEFAULT is 1.0).                                                                                                                                                                                                                                                                             |
| MFACT               | If any of the last three entries are used, the entries preceding it must be present so that the order of the entries is preserved. Only one MFACT keyword may be used per tally.                                                                                                                                                                                                     |

TRANS

Must be followed by a single reference to a TR card number that can be
used to translate and/or rotate the entire mesh. Only one TR card
reference is permitted with each card.

## 5.11.1.5 DXTRAN TMESH Mesh Tally (Type 4)

The fourth type of mesh tally scores the tracks contributing to all
point detectors defined in the input file for the P particle type. If
this card is preceded by an asterisk ( * ), tracks contributing to
DXTRAN spheres [§5.12.10] are recorded. Obviously, a point detector or
DXTRAN sphere must already be defined in the problem, and the tally will
record tracks corresponding to all such defined items in the problem.
The user should limit the geometric boundaries of the grid to focus on a
specific detector or DXTRAN sphere in order to prevent confusion with
multiple detectors (although the convergence of the particle tracks
should help in the interpretation). This tally is an analytical tool
useful in determining the behavior of detectors and how they may be
effectively placed in the problem.

| Data-card Form: X MESH n : P KEYWORD = value(s) ...   | Data-card Form: X MESH n : P KEYWORD = value(s) ...                                                                                                                             |
|-------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                                     | Type 4 mesh-tally type identifier. Restriction: n = 4 , 14 , 24 , . . .                                                                                                         |
| P                                                     | the particle type [neutron ( N ) or photon ( P )].                                                                                                                              |
| TRANS                                                 | Must be followed by a single reference to a TR card number that can be used to translate and/or rotate the entire mesh. Only one TR card reference is permitted with each card. |

## 5.11.1.6 Processing the TMESH Mesh Tally Results

The values of the coordinates, the tally quantity within each mesh bin,
and the relative errors are all written by MCNP6 to the runtpe file, the
optional mctal file, and an unformatted binary file named mdata .

The mesh tallies may be plotted with the MCNP6 geometry plotter either
during the course of a calculation (by placing an MPLOT card in the
input file or by using the TTY interrupt capability to invoke MCPLOT) or
after a calculation using the runtpe file and the MCNP6 geometry
plotter. These plots are superimposed over 2-D views of the problem
geometry. Note that the geometry plotter must be accessed via the tally
plotter. For example,

```
1 MCNP6 Z 2 MCPLOT>RUNTPE=<filename> 3 MCPLOT>PLOT 4 PLOT>py 4 ex 40 or 0 4 0 la 0 1 tal12 color on la 0 0 con 0 100 %
```

After the PLOT command, the MCNP6 interactive geometry plotter appears.
If the Plot&gt; button (bottom center) is clicked, then the above command
after the PLOT&gt; prompt can be entered. Alternatively, the mesh tally
superimposed on the geometry can be viewed by clicking buttons ( tal ,
etc.) of the interactive tally plot. Note that the command tal12 has no
space between tal and 12 and that the cell labels ( la 0 1 tal12 ) must
be turned on to set the color ( color on ) and then be turned off ( la 0
0 ).

The second mesh tally processing option is to use the MCNP6 tally
plotter (MCPLOT) after a calculation with the optional mctal file (see
PRDMP card). For example,

1

2

3

```
MCNP6 Z MCPLOT>RMCTAL=<filename> tal 12 free ik
```

Note that there is a space between tal and 12 and that the mesh tally
dimensionality [ i, j, k ] corresponding to CORA , CORB , and CORC )
must be specified.

The third mesh tally processing option is to post-process the mdata (or
mctal ) file with the gridconv utility [Appendix E.4] and then use an
external graphics package.

## 5.11.2 FMESH: Superimposed Mesh Tally B

The FMESH card allows the user to define a mesh tally superimposed over
the problem geometry. Tally results are either written to a separate
output file or can be accessed from the runtape file via the XDMF output
file. By default, the mesh tally calculates the track-length estimate of
the particle flux averaged over a mesh cell in units of particles/cm 2 .
If an asterisk precedes the FMESH card, energy times particle weight
will be tallied in units of MeV/cm 2 . Other mesh-tally types include
source points, partial current, and isotopic reaction rate tallies.

FMESH mesh tallies can be used in combination with the DE / DF , FC , FM
, SF , CF and TR cards. With the surface ( SF ) and cell ( CF ) flagging
cards, only one mesh tally, the flagged tally, is created. A separate
mesh tally is needed for unflagged tally results.

## /\_445 Deprecation Notice

Except for none and xdmf , all output formats for the FMESH are
deprecated.

Consistent with prior and current behavior, mesh tallies specified as
output type none will only be written to the runtape file for the
purpose of restarting the calculation and/or for use within the
interactive plotter.

Mesh tallies specified as output type xdmf will create a separate XDMF
[324, 325] file, named meshtal.xdmf by default. This file contains
metadata which is then used to access the mesh tally data and associated
attributes from the runtape file. This file permits direct and
hierarchical access to the mesh tally results in the runtape with a
variety of programming languages and also straightforward 3-D
visualization with third-party software such as ParaView [326] and VisIt
[327].

Note that this option will also create a new HDF5 group on the runtape
file, /results/mesh \_ tally , which is used by the XDMF file to access
the mesh tally data. For more details, see D.4.

<!-- image -->

| Data-card Form: FMESH n : P keyword = value(s)...   | Data-card Form: FMESH n : P keyword = value(s)...                                                                             |
|-----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| n                                                   | Tally number ending with 4 or 01                                                                                              |
| P                                                   | A single particle designator.                                                                                                 |
| geom                                                | Mesh geometry, either Cartesian ( XYZ or REC ) or cylindrical coordinates ( RZT or CYL ) . (DEFAULT: geom = XYZ )             |
| origin                                              | Coordinates (x,y,z) of the origin of the mesh in terms of the MCNP cell geometry (DEFAULT: origin = 0.0, 0.0, 0.0 ) ( 1 ). If |

DEP-53292

|       | geom = XYZ                                                                                                                                                                         | the origin corresponds to the bottom, left, behind of a rectangular mesh.                                                                                                          |
|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|       | geom = RZT                                                                                                                                                                         | the origin corresponds to the bottom center of a cylindrical mesh.                                                                                                                 |
| axs   | Vector giving the direction of the axis of the cylindrical mesh ( 2 ). (DEFAULT: axs = 0.0, 0.0, 1.0 )                                                                             | Vector giving the direction of the axis of the cylindrical mesh ( 2 ). (DEFAULT: axs = 0.0, 0.0, 1.0 )                                                                             |
| vec   | Vector defining, along with AXS , the plane for ( 2 ). (DEFAULT: vec = 1.0, 0.0, 0.0 )                                                                                             | Vector defining, along with AXS , the plane for ( 2 ). (DEFAULT: vec = 1.0, 0.0, 0.0 )                                                                                             |
| imesh | Locations of the coarse mesh points in the x direction for rectangular geometry or in the r direction for cylindrical geometry ( 3 ). (DEFAULT: none)                              | Locations of the coarse mesh points in the x direction for rectangular geometry or in the r direction for cylindrical geometry ( 3 ). (DEFAULT: none)                              |
| iints | Number of fine mesh points within each corresponding coarse mesh in the x direction for rectangular geometry or in the r direction for cylindrical geometry. (DEFAULT: iints = 1 ) | Number of fine mesh points within each corresponding coarse mesh in the x direction for rectangular geometry or in the r direction for cylindrical geometry. (DEFAULT: iints = 1 ) |
| jmesh | Locations of the coarse mesh points in the y direction for rectangular geometry or in the z direction for cylindrical geometry ( 3 ). (DEFAULT: none)                              | Locations of the coarse mesh points in the y direction for rectangular geometry or in the z direction for cylindrical geometry ( 3 ). (DEFAULT: none)                              |
| jints | Number of fine mesh points within each corresponding coarse mesh in the y direction for rectangular geometry or in the z direction for cylindrical geometry. (DEFAULT: = )         | Number of fine mesh points within each corresponding coarse mesh in the y direction for rectangular geometry or in the z direction for cylindrical geometry. (DEFAULT: = )         |
| kmesh | Locations of the coarse mesh points in the z direction for rectangular geometry or in the θ direction (in revolutions) for cylindrical geometry ( 3 ). (DEFAULT: none)             | Locations of the coarse mesh points in the z direction for rectangular geometry or in the θ direction (in revolutions) for cylindrical geometry ( 3 ). (DEFAULT: none)             |
| kints | Number of fine mesh points within each corresponding coarse mesh in the z direction for rectangular geometry or in the θ direction for cylindrical geometry. (DEFAULT: kints = 1 ) | Number of fine mesh points within each corresponding coarse mesh in the z direction for rectangular geometry or in the θ direction for cylindrical geometry. (DEFAULT: kints = 1 ) |
| emesh | Values of the coarse mesh points in energy in MeV. (DEFAULT: emesh = 0.0, E )                                                                                                      | Values of the coarse mesh points in energy in MeV. (DEFAULT: emesh = 0.0, E )                                                                                                      |
| eints | Number of fine mesh points within each corresponding coarse mesh in energy. (DEFAULT: eints = 1 )                                                                                  | Number of fine mesh points within each corresponding coarse mesh in energy. (DEFAULT: eints = 1 )                                                                                  |
| enorm | Energy normalization. (DEFAULT: enorm = no ) If                                                                                                                                    | Energy normalization. (DEFAULT: enorm = no ) If                                                                                                                                    |
|       | enorm = no                                                                                                                                                                         | then the tally results are not divided by energy bin width.                                                                                                                        |
|       | enorm = yes                                                                                                                                                                        | then the tally results are per unit energy (MeV - 1 ).                                                                                                                             |
| tmesh | Values of the coarse mesh points in time in shakes ( 4 ). (DEFAULT: tmesh = -∞ , T )                                                                                               | Values of the coarse mesh points in time in shakes ( 4 ). (DEFAULT: tmesh = -∞ , T )                                                                                               |
| tints | Number of fine mesh points within each corresponding coarse mesh in time. (DEFAULT: tints = 1 )                                                                                    | Number of fine mesh points within each corresponding coarse mesh in time. (DEFAULT: tints = 1 )                                                                                    |
| tnorm | Time normalization. (DEFAULT: tnorm = no ) If                                                                                                                                      | Time normalization. (DEFAULT: tnorm = no ) If                                                                                                                                      |
|       | tnorm = no                                                                                                                                                                         | then the tally results are not divided by time bin width.                                                                                                                          |

|              | tnorm = yes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | then provides the tally results per shake (sh - 1 ).                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| factor       | Multiplicative factor for each mesh. (DEFAULT: factor = 1. )                                                                                                                                                                                                                                                                                                                                                                                                                                     | Multiplicative factor for each mesh. (DEFAULT: factor = 1. )                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| out          | Output format, either in column format or as a series of 2-D matrices. If                                                                                                                                                                                                                                                                                                                                                                                                                        | Output format, either in column format or as a series of 2-D matrices. If                                                                                                                                                                                                                                                                                                                                                                                                                        |
|              | out = col                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | a columnar output format is provided, listing the coordinates of the center of the bin, the tally results, and associated relative error. (DEFAULT)                                                                                                                                                                                                                                                                                                                                              |
|              | out = colsci                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | the same as out = col but with all values formatted using scientific notation.                                                                                                                                                                                                                                                                                                                                                                                                                   |
|              | out = cf                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | a columnar output format is provided, listing the coordinates of the center of the bin, the tally results, and associated relative error. In addition, the volume and the tally results multiplied by the volume are also printed.                                                                                                                                                                                                                                                               |
|              | out = cfsci                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | the same as out = cf but with all values formatted using scientific notation.                                                                                                                                                                                                                                                                                                                                                                                                                    |
|              | out = ij or ik or jk                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | tally results are printed as a series of two 2-D matrices, with I = x or r , J = y or z , and K = z or θ , depending on the coordinate system chosen. The first matrix contains the tally results, and the second matrix the relative errors. The rows and columns are labeled by the mid-points of the corresponding mesh bins. These pairs of matrices will be printed for each mesh bin in the third coordinate.                                                                              |
|              | out = none                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | no meshtal file is printed (but the information is still written to the runtape file ( 5 ).                                                                                                                                                                                                                                                                                                                                                                                                      |
|              | out = xdmf                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | a meshtal.xdmf file is created that can be used to interrogate tally information that is additionally written to the runtape file. Because of other formats being deprecated [DEP-53292], one cannot combine XDMF output with another type of output except none in the same input file. ( 6 , 7 ).                                                                                                                                                                                              |
| tr           | Number of the transformation to be applied to the mesh ( 8 ). (DEFAULT: none)                                                                                                                                                                                                                                                                                                                                                                                                                    | Number of the transformation to be applied to the mesh ( 8 ). (DEFAULT: none)                                                                                                                                                                                                                                                                                                                                                                                                                    |
| inc low high | Defines a range of collisions that will contribute to the FMESH tally. (DEFAULT: low = 0 ; high = infinite ) For a particle track undergoing n collisions, the track will contribute to the FMESH tally if LOW ≤ n ≤ HIGH . The specification of LOW is optional. If only LOW is specified, then a particle track undergoing exactly n collisions will contribute to the FMESH tally if n = LOW . The keyword entry INFINITE can be used for HIGH to represent an infinite number of collisions. | Defines a range of collisions that will contribute to the FMESH tally. (DEFAULT: low = 0 ; high = infinite ) For a particle track undergoing n collisions, the track will contribute to the FMESH tally if LOW ≤ n ≤ HIGH . The specification of LOW is optional. If only LOW is specified, then a particle track undergoing exactly n collisions will contribute to the FMESH tally if n = LOW . The keyword entry INFINITE can be used for HIGH to represent an infinite number of collisions. |
| type         | Allows users to specify the quantity being tallied. If                                                                                                                                                                                                                                                                                                                                                                                                                                           | Allows users to specify the quantity being tallied. If                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|              | type = flux                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | volumetric track-length fluxes are tallied. See F4 type tally. (DEFAULT)                                                                                                                                                                                                                                                                                                                                                                                                                         |
|              | type = source                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | source points are tallied.                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

| kclear   | Used in KCODE calculations for generating visualizations of cycle wise quantities. Zeros out the mesh tally every n KCODE cycles, where n is specified with kclear = n . If n is non-zero, then tallies are accumulated both during active and inactive cycles; consequently, the output should only be used for visualizations and not as actual results. If n is zero, then the mesh tally behaves normally and mesh tally results are never cleared. (DEFAULT: kclear = 0 )   | Used in KCODE calculations for generating visualizations of cycle wise quantities. Zeros out the mesh tally every n KCODE cycles, where n is specified with kclear = n . If n is non-zero, then tallies are accumulated both during active and inactive cycles; consequently, the output should only be used for visualizations and not as actual results. If n is zero, then the mesh tally behaves normally and mesh tally results are never cleared. (DEFAULT: kclear = 0 )   |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tally    | Tallying algorithm. See §5.11.2.4 for more details.                                                                                                                                                                                                                                                                                                                                                                                                                              | Tallying algorithm. See §5.11.2.4 for more details.                                                                                                                                                                                                                                                                                                                                                                                                                              |
|          | tally = hist                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | basic history statistics-based algorithm.                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|          | tally = fast _ hist                                                                                                                                                                                                                                                                                                                                                                                                                                                              | high efficiency history statistics-based algorithm. Corresponds with the approach from version 6.2 and prior releases of the MCNP code. (DEFAULT)                                                                                                                                                                                                                                                                                                                                |
|          | tally = batch                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | batch statistics-based algorithm.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|          | tally = rma _ batch                                                                                                                                                                                                                                                                                                                                                                                                                                                              | batch statistics-based algorithm using remote memory access. Requires MPI and compatible software and hardware.                                                                                                                                                                                                                                                                                                                                                                  |

Use: Optional

## Details:

- 1 The location of the n th coarse mesh in the u direction ( r u,n in what follows) is given in terms of the most positive surface in the u direction. For a rectangular mesh, the coarse mesh locations ( r x,n , r y,n , r z,n ) , are given as planes perpendicular to the x , y , and z axis, respectively, in the MCNP cell geometry coordinate system. Thus the origin point ( x 0 , y 0 , z 0 ) is the most negative point of the mesh tally. For a cylindrical mesh, origin defines the bottom center point of the mesh. The z coordinate is then measured from the cylindrical mesh origin. For both types of geometry, the lowest energy value is 0 MeV. The coarse mesh locations and energy values must increase monotonically (beginning with the origin point). The fine meshes are evenly distributed within the n th coarse mesh in the u direction.
- 2 For a cylindrical mesh, the axs and vec vectors need not be orthogonal but they must not be parallel; the one half-plane that contains them and the origin point will define θ = 0 . The axs vector will remain fixed. The length of the axs or vec vectors must not be zero. The z coordinate is specified in the cylinder geometry coordinate system. The θ coarse mesh locations are given in revolutions and the last one must be 1.
- 3 At least one coarse mesh per coordinate direction must be specified using imesh , jmesh , and kmesh keywords. The code uses a default value of 1 fine mesh per coarse mesh if the iints , jints , or kints keywords are omitted. If the iints , jints , or kints keywords are present, the number of entries must match the number of entries on the imesh , jmesh , and kmesh keywords, respectively. Entries on the iints , jints , and kints keywords must be greater than zero.
- 4 Because the lower time bound is minus infinity, users are encouraged to specify the first bin as a dummy bin with the smallest time of interest (usually zero shakes). The user should then ignore the first time bin when plotting.
- 5 If the FMESH card is present in a restarted calculation, only the out keyword is permitted.
- 6 Appendix D.4 describes how to use the meshtal.xdmf file to plot mesh tally results with the third-party 3-D visualization software ParaView [326]. It also describes the new FMESH tally HDF5 hierarchy on the runtape file.

1

2

3

4

5

6

1

2

3

4

5

6

- 7 Both the runtape file and the XDMF output are affected by the PIO card.
- 8 Any FMESH mesh can be transformed using the tr keyword followed by a transformation number. The transformation is defined on the associated TR card.
- 9 As with the F card, a unique number is assigned to each FMESH tally relative to F4 tallies. Since only track-length mesh tallies are typical, the mesh tally number must end with a 4, and it must not be identical to any number that is used to identify an F4 tally. The track length is computed over the mesh tally cells, and is normalized to be per starting particle, except in KCODE criticality calculations, in which results are usually normalized by the active cycle weight [§2.8.2.9].

## 5.11.2.0.1 Example 1

Listing 5.60: example\_fmesh.mcnp.inp.txt

| FC4 Cylindrical FMESH tally   | example          |
|-------------------------------|------------------|
| FMESH4:n GEOM=CYL             | ORIGIN= -100 0 0 |
| IMESH= 5                      | 10 IINTS= 5 2    |
| JMESH= 100 200                | JINTS= 10 5      |
| KMESH= 0.5                    | 1 KINTS= 1 2     |
| AXS= 1 0 0                    | VEC=0 1 0        |

This example describes a cylindrical mesh tally along the x axis, with
base at x = -100 and θ = 0 along the + y axis. The tally is divided into
five bins from r = 0 to r = 5 , two bins from r = 5 to r = 10 , ten bins
from z = 0 to 100, five bins from z = 100 to z = 200 , one bin from θ =
0 ◦ to θ = 180 ◦ , and two bins from θ = 180 ◦ to 360 ◦ .

## 5.11.2.1 Special Cases of the FM Tally Multiplier Used in Conjunction with the FMESH Mesh Tally

## 5.11.2.1.1 Default Materials

When the FMESH capability is associated with a tally multiplier ( FM )
card, then the material number specified on the FM card determines the
cross sections that are used to calculate the mesh bin values. That is,
the cross sections of the specified material are used for the entire
mesh, even if the mesh covers several different materials. If instead, a
' 0 ' is entered as the material number on the FM card, then MCNP will
use the reaction data of the material through which the particle travels
to calculate the bin values. Thus, material-dependent quantities that
are computed with the use of the FM card (e.g., neutron heating) can be
calculated using mesh tallies that cover more than one material.

## 5.11.2.1.2 Example 1

Listing 5.61: example\_fmesh.mcnp.inp.txt

| FC14               | FMESH tally energy deposition (in MeV/cm^3)   | FMESH tally energy deposition (in MeV/cm^3)   |
|--------------------|-----------------------------------------------|-----------------------------------------------|
| FMESH14:n GEOM=xyz | FMESH14:n GEOM=xyz                            | ORIGIN= -5 -5 -5                              |
|                    | IMESH=                                        | 5 IINTS=100                                   |
|                    | JMESH=                                        | 5 JINTS= 1                                    |
|                    | KMESH=                                        | 5 KINTS=100                                   |
| FM14               | -1 0 1 -4                                     | -1 0 1 -4                                     |

This example describes an energy-deposition rectangular-mesh tally
covering a 10 × 10 × 10 cm box centered on the origin. The tally is
divided into 100 bins in both the x and z directions and one bin in the
y direction. The FM4 card specifies the energy deposition for all
materials in the mesh.

## /warning\_sign Caution

The use of parentheses anywhere on an FMESH FM card can cause the code
to exit with a fatal error.

## 5.11.2.2 Isotopic Reaction Rate Tallies

Individual isotopic reaction rates can be obtained throughout the mesh
tally geometry. To invoke this capability, define a new dummy material
card containing only the isotope(s) of interest. This dummy material
card should be specified in exactly the same way as a standard M card;
however, the dummy material number should not appear in the problem
geometry-instead the material number is used exclusively by the FM card.
Note that for these dummy materials, the isotopic densities are not used
by MCNP but values must be provided as placeholders. Instead, the
required isotopic atom fractions will be extracted from the appropriate
material data used during transport.

To specify a reaction-rate mesh tally based on isotopic fractions, place
a ' + ' symbol in front of the FM card associated with the mesh tally.
The rest of the FM card is set up the regular way, with a multiplicative
constant followed by the dummy material number and the ENDF reaction
numbers of interest.

When calculating the mesh tally, MCNP will multiply the particle flux
times the cross sections for the isotopes defined on the material card.
This value is then multiplied by the atom fraction of the dummy material
isotope(s) which are present in the material in which the particle is
traveling to calculate the isotopic reaction rate. Depending on the
units of the source, the units of the results will be (number of
reactions) · barn -1 · cm -1 , or (number of reactions) · barn -1 · cm
-1 · shake -1 .

Recall that placing a minus sign in front of the multiplicative constant
will multiply the results by the atom density of the cell. Therefore
using c = -1 will return units of (number of reactions) · cm -3 , or
(number of reactions) · cm -3 · shake -1 for the specific isotopes.

See §10.2.3 for examples of isotopic reaction rate mesh tallies

## 5.11.2.3 Special Case of Leakage Tallies using the FMESH Mesh Tally

As a very special and limited extension of the FMESH mesh tallies, FMESH
cards with a tally number ending in the two numerals 01 can be used to
obtain the outgoing leakage (or outgoing partial current) across each of
the 6 faces of each mesh element.

## Details:

- 1 Outgoing partial current FMESH tallies defined in the problem input must end in '01'.
- 2 Specifying FMESH 901:n in the problem input will result in the following FMESH tallies being created internally:
- FMESH911:n : outgoing partial current in the + x or + r direction
- FMESH921:n : outgoing partial current in the -x or -r direction

- FMESH931:n : outgoing partial current in the + y or + z direction
- FMESH941:n : outgoing partial current in the -y or -z direction
- FMESH951:n : outgoing partial current in the + z or + θ direction
- FMESH961:n : outgoing partial current in the -z or -θ direction
- 3 All 6 of the partial current tallies will have the same specifications that are supplied for FMESH901:n . The specific tally FMESH901:n will not actually be stored or be available for referencing with FM , DE / DF , SC , or SF cards.
- 4 These tallies are not divided by volume or area. They produce the total particle weight crossing each surface of a mesh cell in the outward direction, normalized to be per unit source particle.
- 5 The incoming partial currents to a mesh element can be obtained from the outgoing partial currents of neighboring elements. Since the partial current FMESH tally only tallies outward currents for each mesh element, it is necessary to specify the mesh to include a 'halo' of inactive elements surrounding the active problem domain in order to properly capture incoming current at the boundary of the problem domain.
- 6 Use of the ' * ' prefix, as in * FMESH 901:n , is permitted. This will result in the FMESH partial current tallies providing the energy crossing each mesh element surface in the outward direction.
- 7 The tally modifier cards, such as FM , DE / DF , CF , or SF may be used with the partial current tallies (although most modifiers don't make physical sense). To do so, however, the tally number for only the first of the created FMESH tallies must be used. For example, if FMESH901:n is specified, then tally number 911 should be used on any FM , DE / DF , CF , or SF cards. Those cards will also be applied to the FMESH912:n , . . . , FMESH 916:n partial current mesh tallies. Note that, FM modifiers that are typically used with flux tallies may not be appropriate with partial currents.
- 8 The partial current tallies can be plotted, using the tally numbers for the 6 created mesh tallies. For example, in the plotter one can specify ' fmesh 911 ' for the example above.
- 9 The tallies appear in the standard format in the meshtal file, with the 6 names of tallies created, e.g., FMESH911 , and can be combined using merge \_ meshtal .

The FMESH partial current tallies are deliberately limited in scope and
usage. They are provided primarily so that users can obtain a complete
particle balance for individual mesh elements. That is, using FMESH4
tallies for particle production and particle capture, the FMESH 01
tallies provide the leakage across mesh element surfaces.

## 5.11.2.4 FMESH Mesh Tally Algorithms

The tallying system provides four algorithms, History ( tally = hist ),
Fast History ( tally = fast \_ hist ), Batch ( tally = batch ), and Batch
RMA ( tally = rma \_ batch ). Each algorithm has various tradeoffs.

## To summarize:

- All methods will give the same mean when the same tally events occur (for KCODE , bear in mind 1 ).
- Methods that use batch statistics will have a higher variance of the error estimate than history statistics. This gets worse with fewer batches. See §2.6.11. One should use at least 100 batches, preferably more, for this reason.
- For KCODE , batch statistics can yield slightly more conservative error estimates as compared to history, as they properly handle correlation between histories in a given generation. Correlation between generations is not yet handled.

Table 5.24: Approximate Peak FMESH Memory Usage

| Algorithm                          | Peak Node Memory Usage, Bytes                                                                                                             |
|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| hist fast _ hist batch rma _ batch | 16 T size n rank +8 T size n rank n threads 16 T size n rank +8 . 8 T size n rank n threads 16 T size +8 T size n rank 24 T size /n nodes |

- For simulation speed, generally hist glyph[lessmuch] fast \_ hist &lt; batch . For rma \_ batch , it depends on the size of the problem and the MPI library.
- For memory usage, generally batch \_ rma &lt; batch glyph[lessmuch] hist &lt; fast \_ hist . An approximate memory usage estimate can be found in Table 5.24. T size is the number of tally regions, n rank is the number of MPI processes per node, n nodes is the number of nodes, and n threads is the number of threads per MPI process.
- As shown in that table, all except rma \_ batch use memory more efficiently when one maximizes the number of threads (via tasks , see § 3.3.2.3) and minimizes the number of MPI processes.

In general, if you do not know which to pick, fast \_ hist is a safe
choice and is default for that reason. batch will perform better and use
less memory, at the cost of the quality of the statistics. rma \_ batch
is ideal for use with extremely large tallies ( &gt; 10 8 regions) that are
beyond the reach of the other algorithms. hist is only useful for very
small tallies for performance reasons.

## 5.11.2.4.1 Fast History Tally Algorithm ( tally = fast \_ hist )

This algorithm, which is the default, acts as a drop-in replacement to
the algorithm used in versions of the MCNP code prior to 6.3. Relative
to the previous version of the algorithm, it should run faster and use
less memory in most circumstances. The approach used to compute
statistical parameters is identical to the previous version as well, so
answers should be identical within numerical roundoff.

## 5.11.2.4.2 History Tally Algorithm ( tally = hist )

This algorithm removes an optimization used in the Fast History
algorithm that speeds up problems in which a single particle history
touches a small fraction of tally regions. As a result, it should be
slower on all but the smallest problems. Statistics are computed quite
differently in this mode. First, statistical moments are computed using
a more numerically stable approach described in [328]. Second, the
number of degrees of freedom used for the standard error is always the
number of active histories simulated minus one. This will result in
slight changes to the standard error. The mean will match Fast History
within roundoff.

## 5.11.2.4.3 Batch Tally Algorithm ( tally = batch )

This algorithm switches from history to batch statistics, in order to
take advantage of the performance benefits. When running a fixed source
problem, batch size is set by the n \_ per \_ batch option on the NPS
card. The batch count is then npp / n \_ per \_ batch . For KCODE
problems, the batch size is nsrck , and the batch count is given by the
active generations. In KCODE problems, when a tally that uses batch
statistics is detected, the fission bank will be resampled to always be
a fixed size. This will change results when compared to not resampling,
but the solutions are equivalent within statistics. One can compare
algorithms by running both within the same simulation.

## 5.11.2.4.4 Remote Memory Access Batch Tally Algorithm ( tally = rma \_ batch )

This algorithm is only available if the MCNP code is built with MPI.
Otherwise, the Batch Tally Algorithm is used. This algorithm is
mathematically identical to the Batch Tally Algorithm and will give
identical results, but the two results arrays and the worker array are
uniformly distributed across all processes and nodes in the problem.
This means that running the problem with more nodes of a cluster will
increase the maximum problem size.

While this algorithm allows for the largest possible tallies of all the
methods, it comes with some caveats. The first is that it will generally
be slower than the Batch algorithm. Second, performance is very
sensitive to the MPI library and cluster interconnect. See the build
guide [329] for more details. Third, if the MPI \_ THREAD \_ MULTIPLE
build option is disabled (which is default, visible by running mcnp6.mpi
-v ), it is best to run simulations only with MPI (no tasks ) for
performance reasons.

## 5.11.3 SPDTL: Lattice Tally Speed Enhancement

The SPDTL card allows the user to force or prevent the use of the
lattice speed tally enhancement [330]. This feature allows the user to
run a short test case with and without the enhancements to verify they
are appropriate by comparing the tally results of the two runs.

| Data-card Form: SPDTL value   | Data-card Form: SPDTL value                                              | Data-card Form: SPDTL value                                                                          |
|-------------------------------|--------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| value                         | Toggles whether to force or prohibit lattice speed tally enhancement. If | Toggles whether to force or prohibit lattice speed tally enhancement. If                             |
|                               | value = FORCE                                                            | Force the use of the lattice speed tally enhancement feature. No values accompany the keyword ( 2 ). |
|                               | value = OFF                                                              | Prevent the use of the lattice speed tally enhancement feature. No values accompany the keyword.     |

Default:

Lattice speed tally enhancement is enabled by default if strict criteria
are met.

Use: Optional.

## Details:

1 Only one keyword may be specified for SPDTL.

2 Using SPDTL FORCE also causes comments to be printed about lattice
speed tally enhancement conflicts with other cards.

## 5.11.3.1 Conditions Required for Lattice Speed Tally Enhancements

The lattice speed tally enhancements greatly reduce the runtime of
certain problems, namely large lattices used for voxel phantoms. This
enhancement will only work under certain conditions, which MCNP6 will
try to detect. If any of the following criteria are not met, then the
lattice speed tally enhancement will not be used unless the SPDTL FORCE
card is used. Using the SPDTL FORCE card to run the lattice speed tally
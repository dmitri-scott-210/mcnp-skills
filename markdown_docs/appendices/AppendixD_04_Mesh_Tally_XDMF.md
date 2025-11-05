---
title: "Appendix D.4 - Mesh Tally XDMF Output Format"
chapter: "D.4"
source_pdf: "mcnp631_theory_user-manual/appendecies/D.4_Mesh_Tally_XDMF_Output_Format.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## D.4 Mesh Tally XDMF Output Format

This section describes the file formats of the new MCNP mesh tally xdmf
output option. Two files are used when a user selects out=xdmf on the
fmesh card.

To produce the xdmf output, the HDF5-formatted restart file is modified
to add a new results group at the root level as /results . Underneath
that, a mesh \_ tally group is created and the results for each mesh
tally are hierarchically organized therein. A variety of Boolean
attributes are provided that indicate the presence of additional
information on features used with the mesh tally (comments,
transformations, reaction multipliers, etc.). In this way, the results
can be easily interrogated using standard HDF5 libraries in a variety of
programming languages.

In addition, the traditional mesh tally output file ( meshtal or ...msht
) is written as a version-2 XDMF [324, 325] file ( meshtal.xdmf or
...msht.xdmf ). The XDMF file can be used with custom applications
and/or loaded into applications such as ParaView [326] or VisIt [327],
which provide interactive 3-D visualization capabilities.

The remainder of this section is organized as follows: Section D.4.1
describes the file organization for the HDF5 [§D.4.2] file with its
subsections describing attributes associated with mesh tally features.
XDMF files are described in Section D.4.3. Appendix D.8 provides a
Python script to process HDF5 elements into L A T E X dirtree listings.

## D.4.1 File Organization

Both HDF5 files (by definition) and XDMF files (as XML-formatted files)
are hierarchical in nature.

HDF5 files consist of groups (similar to directories) and data sets
(multidimensional arrays of homogeneous but arbitrary data). In
addition, HDF5 groups and data sets can have attributes assigned, which
are relatively low-overhead scalar or array quantities. These three
basic components can be arbitrarily arranged into a hierarchy that best
suits an application's need(s).

Meanwhile, XDMF files use a standard hierarchy to define mesh
geometries, and quantities on the mesh, for the purpose of post
processing. Usually, this post-processing is enabled by a visualization
application such as ParaView or Visit; however, C++ and Python XDMF
libraries exist to quantitatively process XDMF files directly.
Regardless, the XDMF format has a specific hierarchy and organization,
but can point to data within the HDF5 files located arbitrarily. Thus,
the XDMF can be used as a roadmap into the HDF5 file that defines where
to retrieve the data of interest. It has been said that the HDF5 files
contain the 'heavy' data while the XDMF files contain the 'light' data.

## D.4.2 HDF5

An example HDF5 hierarchy for two mesh tallies (identified as 14 and 24)
is given in Fig. D.1, which is generated from the MCNP input given in
Listing D.1.

Additional mesh tallies would reside at the same level as the mesh \_
tally \_ 14 and mesh \_ tally \_ 24 groups. Multiple energy and/or time
bins would be given at the respective levels. If the total over all
energy and/or time bins are given, they will be labeled as energy \_
total and/or time \_ total , respectively. There is a duplication of
datasets and attributes within each energy group to permit additional
flexibility in the future such that energy- and/or time-dependent
geometry variation is possible.

Figure D.1: Mesh Tally HDF5 Hierarchy

<!-- image -->

1

2

3

4

5

6

7

8

Listing D.1: Excerpt from fmesh\_xdmf.mcnp.inp.txt

| fmesh14:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3   |
|------------------------------------------------------|
| jmesh=4 jints=4                                      |
| kmesh=5 kints=5                                      |
| out=xdmf                                             |
| fmesh24:n geom=rzt origin=-3 -3 -3 imesh=3 iints=3   |
| jmesh=5 jints=5                                      |
| kmesh=1 kints=15                                     |
| out=xdmf                                             |

In addition to the groups and data sets in Fig. D.1, a variety of
attributes are shown. These attributes are often Boolean indicators of
additional features that may accompany mesh tallies and are meant as a
convenience when parsing the HDF5 results directly. Other attributes are
256-character strings, integers, or floating-point values that provide
supplemental information about the associated mesh tally. These
attributes are described in the next subsections.

## D.4.2.1 Attribute: number\_of\_normalizing\_histories

This integer attribute indicates the number of histories (e.g., the NPS
card entry) that is used to normalize the results by.

## D.4.2.2 Attribute: coordinate\_system

The this string attribute gives the coordinate system as Cartesian or
cylindrical , as appropriate. This entry will also indicate which
geometry data sets exist at the lowest level. If the mesh tally is
Cartesian, at the lowest level the geometry data sets are:

| grid _ x   | is a 1-D spatial grid along the x coordinate axis. This is defined based on the fmesh card imesh and iints entries. These coordinates are not modified by an additional tr card applied to the corresponding fmesh card.   |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| grid _ y   | is a 1-D spatial grid along the y coordinate axis. This is defined based on the fmesh card jmesh and jints entries. These coordinates are not modified by an additional tr card applied to the corresponding fmesh card.   |
| grid _ z   | is a 1-D spatial grid along the z coordinate axis. This is defined based on the fmesh card kmesh and kints entries. These coordinates are not modified by an additional tr card applied to the corresponding fmesh card.   |

and for cylindrical mesh tallies, at the lowest level the geometry data
sets are:

| grid _ r   | is a 1-D spatial grid along the r coordinate axis. This is defined based on the fmesh card imesh and iints entries. These coordinates are not modified by an additional tr card applied to the corresponding fmesh card.   |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| grid _ t   | is a 1-D spatial grid along the θ coordinate axis. This is defined based on the fmesh card jmesh and jints entries. These coordinates are not modified by an additional tr card applied to the corresponding fmesh card.   |

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

| grid _ z       | is a 1-D spatial grid along the z coordinate axis. This is defined based on the fmesh card kmesh and kints entries. These coordinates are not modified by an additional tr card applied to the corresponding fmesh card.                                                                              |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| coords         | is a 3-D spatial grid in a Cartesian coordinate system used to define an XDMF 3DSMesh structured curvilinear mesh. This array is modified according to the fmesh card's axis and vector ( axs and vec ) entries but is not modified by an additional tr card applied to the corresponding fmesh card. |
| basis _ axis   | is the axis of the cylinder, which is (0 , 0 , 1) by default.                                                                                                                                                                                                                                         |
| basis _ vector | is the axis defining θ = 0 , which is (1 , 0 , 0) by default.                                                                                                                                                                                                                                         |
| basis _ cross  | is the cross product of the axis and vector, which is (0 , 1 , 0) by default.                                                                                                                                                                                                                         |

## D.4.2.3 Attribute: has\_collision\_binning

This Boolean attribute indicates whether the fmesh has collision binning
using the inc option. Examples of using this option are given in Listing
D.2.

Listing D.2: Excerpt from fmesh\_xdmf\_inc.mcnp.inp.txt

| fmesh14:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3   |
|------------------------------------------------------|
| fmesh24:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3   |
| geom=xyz origin=-3 -3 -3 imesh=3 iints=3             |
| kmesh=5 kints=5                                      |
| out=xdmf inc=1 3                                     |
| fmesh34:n                                            |
| kmesh=5 kints=5                                      |
| jmesh=4 jints=4                                      |
| out=xdmf                                             |
| inc=1 infinite                                       |

These three mesh tallies show different ways of applying the inc option.
In all cases, has \_ collision \_ binning is true. When true, two
additional attributes are added to the corresponding energy group:
collision \_ bin \_ lower and collision \_ bin \_ upper .

For fmesh14 , collision \_ bin \_ lower is 1 (as entered) and collision \_
bin \_ upper is -2 .

For fmesh24 , collision \_ bin \_ lower is 1 (as entered) and collision \_
bin \_ upper is 3 (as entered).

For fmesh34 , collision \_ bin \_ lower is 1 (as entered) and collision \_
bin \_ upper is -1 .

## D.4.2.4 Attribute: has\_comment\_lines

This Boolean attribute indicates whether the FMESH card has an
associated FC card. Examples of using this option are given in Listing
D.3.

10

11

```
1 fmesh14:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3 2 jmesh=4 jints=4 3 kmesh=5 kints=5 4 out=xdmf 5 fc14 single line comment 6 fmesh24:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3 7 jmesh=4 jints=4 8 kmesh=5 kints=5 9 out=xdmf fc24 double line comment second line comment
```

Listing D.3: Excerpt from fmesh\_xdmf\_fc.mcnp.inp.txt

These two mesh tallies show a single and multi-line comment card for
mesh tallies 14 and 24, respectively. In all cases, has \_ comment \_
lines is true. When true, additional string data sets appear, one for
each comment line. These data sets are comment \_ lines \_ 1 , comment \_
lines \_ 2 , etc. and contain a 256-character string. These are written
in this way because of a current limitation regarding writing arrays of
strings to an HDF5 file.

## D.4.2.5 Attribute: has\_dose\_response\_function

This Boolean attribute indicates whether the FMESH card has an
associated set of de / df cards applied. An example using this option is
given in Listing D.4.

Listing D.4: Excerpt from fmesh\_xdmf\_dedf.mcnp.inp.txt

<!-- image -->

| fmesh14:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3   |
|------------------------------------------------------|
| jmesh=4 jints=4                                      |
| kmesh=5 kints=5                                      |
| out=xdmf                                             |
| de14 log 1e-8 9ilog 1e2                              |
| df14 log 1e-8 9ilog 1e2                              |

In this case, has \_ dose \_ response \_ function is true. Accordingly,
another 256-character string attribute, dose \_ response \_ interpolation
, indicates the interpolation method as loglog (other options are linlog
, loglin , and linlin ). Finally, two data sets are added at the lowest
group level, dose \_ response \_ function \_ domain and dose \_ response \_
function \_ range , which correspond to the entries on the de and df
cards, respectively.

## D.4.2.6 Attribute: has\_flagged\_cells

This Boolean attribute indicates whether the FMESH card has an
associated set of cell-flagging ( cf ) cards applied. An example using
this option is given in Listing D.5.

In this case, has \_ flagged \_ cells is true. Accordingly, another
integer attribute, flagged \_ cell \_ count , indicates the number of
flagged cells (in this example: 1). Finally, another 1-D integer data
set is added at the lowest group level, flagged \_ cells , which contains
the ID numbers for each of the flagged cells.

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

1

2

3

4

5

10

11

12

13

14

15

16

17

Listing D.5: Excerpt from fmesh\_xdmf\_cf.mcnp.inp.txt

| fmesh14:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3   |
|------------------------------------------------------|
| cf14 100                                             |

## D.4.2.7 Attribute: has\_flagged\_surfaces

This Boolean attribute indicates whether the FMESH card has an
associated set of surface-flagging ( sf ) cards applied. An example
using this option is given in Listing D.6.

Listing D.6: Excerpt from fmesh\_xdmf\_sf.mcnp.inp.txt

| fmesh14:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3   |
|------------------------------------------------------|
| sf14 10                                              |

In this case, has \_ flagged \_ surfaces is true. Accordingly, another
integer attribute, flagged \_ surface \_ count , indicates the number of
flagged surfaces (in this example: 1). Finally, another 1-D integer data
set is added at the lowest group level, flagged \_ surfaces , which
contains the ID numbers for each of the flagged surfaces.

## D.4.2.8 Attribute: has\_score\_multiplier

This Boolean attribute indicates whether the FMESH card has an
associated score multiplier applied using a tally multiplier ( fm )
card. An example using this option is given in Listing D.7.

Listing D.7: Excerpt from fmesh\_xdmf\_fm.mcnp.inp.txt

<!-- image -->

| fmesh14:n geom=xyz origin=-3 -3 -3 imesh=3   | iints=3            |
|----------------------------------------------|--------------------|
| fm14 2.3 fmesh24:n geom=xyz origin=-3 -3     | -3 imesh=3 iints=3 |
| fm24 2.3 1 1 2 fmesh34:n geom=xyz            | iints=3            |
| origin=-3 -3 -3                              | jmesh=4 jints=4    |
|                                              | kmesh=5 kints=5    |
|                                              | factor=1.2         |
|                                              | kmesh=5 kints=5    |
|                                              | out=xdmf           |
|                                              | factor=1.2         |
|                                              | imesh=3            |
| out=xdmf                                     |                    |

1

2

3

4

5

6

For mesh tally 14, h as \_ score \_ multiplier is true and two additional
attributes are added. First, a floatingpoint score \_ multiplier \_
constant is present and is set to 1 . 2 × 2 . 3 = 2 . 76 . Next, a
256-character string attribute named score \_ multiplier \_ type is
present and set to 'arbitrary scaler'.

For mesh tally 24, h as \_ score \_ multiplier is true and four additional
attributes are added. First, a floatingpoint score \_ multiplier \_
constant is present and is set to 2.3 (i.e., the factor entry on the
FMESH card is ignored). Next, a 256-character string attribute named
score \_ multiplier \_ type is present and set to 'reaction'. Finally,
integer attribute score \_ multiplier \_ material is set to 1 and integer
attribute score \_ multiplier \_ reaction \_ count is set to 2 (to indicate
that two reactions are used from material one). In addition, a new
floating-point 1-D data set is added at the lowest level indicating the
reaction values from the fm card, which is [1 . 0 , 2 . 0] in this case.

For mesh tally 34, h as \_ score \_ multiplier is true and four additional
attributes are added. First, a floating-point score \_ multiplier \_
constant is present and is again set to 2.3 (i.e., the factor entry on
the FMESH card is ignored). Next, a 256-character string attribute named
score \_ multiplier \_ type is present and set to 'reaction'. Finally,
integer attribute score \_ multiplier \_ material is set to 1 and integer
attribute score \_ multiplier \_ reaction \_ count is set to 3 (to indicate
that two reactions are used from material one as well as the ':' used to
sum the reactions). In addition, a new floating-point 1-D data set is
added at the lowest level indicating the reaction values from the fm
card, which is [1 . 0 , 1050000003 . 0 , 2 . 0] in this case. The value
1050000003.0 is effectively an enumeration that represents the colon.

Note that other available score \_ multiplier \_ type s are '1/velocity'
and 'tracks'.

## D.4.2.9 Attribute: has\_transformation

This Boolean attribute indicates whether the FMESH card has an
associated geometry transformation applied using a TR card. An example
using this option is given in Listing D.8.

Listing D.8: Excerpt from fmesh\_xdmf\_tr.mcnp.inp.txt

| fmesh14:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3   |
|------------------------------------------------------|
| tr6 10 20 30 0 0 1 0 1 0 1 0 0                       |

In this case, h as \_ transformation is true and an additional 1-D
floating-point data set is added:

## transformation \_ matrix

which contains the MCNP transformation matrix entries.

The entries in this 'matrix' correspond to the entries on the TR card.
In this case, transformation \_ matrix is equal to [ -6 , -3 , -2 , -1 ,
0 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 0 , 1 , 1 , 2 , 3] . The rotation matrix
is given in entries 5-13. The translation components are given in the
final three entries. The other entries (2, 3, 4, 14) are intended for
calculations internal to the MCNP code and are not described further.

1

2

3

4

5

## D.4.2.10 Attribute: is\_isotopic\_reaction\_rate\_tally

This Boolean attribute indicates whether the FMESH card has an
associated score multiplier applied using a tally multiplier ( fm ) card
modified to act as an isotopic reaction rate tally. An example using
this option is given in Listing D.9.

Listing D.9: Excerpt from fmesh\_xdmf\_fmrxnrate.mcnp.inp.txt

| fmesh24:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3   |
|------------------------------------------------------|
| jmesh=4 jints=4                                      |
| kmesh=5 kints=5                                      |
| out=xdmf                                             |
| factor=1.2                                           |

In this case, is \_ isotopic \_ reaction \_ rate \_ tally is true.
Otherwise, the additional attributes and data sets are consistent with
mesh tally 24 in Section D.4.2.8.

## D.4.2.11 Attribute: multiplicative\_factor

This floating-point attribute indicates the multiplicative factor
applied using the factor entry on the FMESH card. An example using this
option is given in Listing D.10.

Listing D.10: Excerpt from fmesh\_xdmf\_factor.mcnp.inp.txt

| fmesh14:n geom=xyz origin=-3 -3 -3 imesh=3 iints=3   |
|------------------------------------------------------|
| jmesh=4 jints=4                                      |
| kmesh=5 kints=5                                      |
| out=xdmf                                             |
| factor=2.3                                           |

In this case, multiplicative \_ factor is equal to 2.3. By default, this
is equal to 1.0.

## D.4.2.12 Attribute: particle\_number

This integer attribute indicates the particle type that the mesh tally
applies to. It follows MCNP conventions, so a neutron mesh tally
corresponds to particle \_ number equal to 1, photon mesh tallies are
identified as 2, etc.

## D.4.2.13 Attribute: tally\_quantity

This 256-character string attribute indicates the quantity being
tallied. This is either:

```
track _ length _ particle _ flux the default,
```

1

2

3

4

5

track \_ length \_ energy \_ flux as specified by prefixing the FMESH card
with an asterisk, or

partial current... in a particular direction (implicitly specified by
using a type-1 mesh tally).

## D.4.2.14 Attribute: tally\_type

This 256-character string attribute indicates the type of mesh tally.
This is either flux (the default), source (as specified using the type
parameter on the FMESH card), or current (implicitly specified by using
a type-1 mesh tally).

## D.4.3 XDMF

The XDMF standard is documented elsewhere [325] and it is rare that
someone works with the file contents directly. Therefore, minimal
details are given here regarding the detailed structure of the file.
However, the general organization is described along with suggested
methods for working with the file using ParaView.

The XDMF file used to interrogate mesh tallies is formatted according to
the version 2 API (cf. version 3) and is an ASCII XML-formatted file. A
temporal grid collection is used to represent time steps within time-
dependent mesh tallies. General grid collections are used to group
energy bins within time steps. When applicable, totals over all bins for
energy and/or time are given by name (i.e., \_ total ) otherwise time-
and energy- bins are zero indexed (including unbinned mesh tallies).
Mesh tally voxel volumes are referred to generically as a volume
dataset. Individual mesh tally data sets for the tally and relative
standard deviation values are prefixed by the mesh tally ID, e.g., 14 \_
, 44 \_ , 104 \_ , etc.

These naming approaches can lead to data sets that are not represented
over all mesh voxels if multiple mesh tallies are displayed at once
and/or if multiple energy bins are used. However, different mesh tallies
can have different energy and/or time binning structures, so this method
attempts to isolate data that is unique to each energy bin and time step
at the cost of a suboptimal interactive manipulation and display
experience.

Methods to load and work with an XDMF file follow.

## D.4.3.1 Loading the XDMF File for Visualization

To load the mesh tally for visualization from Listing D.1 with ParaView,
select File→Open. . . and select the appropriate XDMF file. Because the
XDMF file uses format version 2, a dialog will likely appear to select a
reader for the file, where 'XDMF Reader' is the correct choice, as shown
in Fig. D.2.

## D.4.3.2 Navigating to a Dataset of Interest

Once the data is loaded into the ParaView pipeline and applied to the
render view (by clicking the Apply button), one might see the two mesh
tallies from Listing D.1 displayed as shown in Fig. D.3. Each mesh tally
is a separate block that can be individually shown/hidden using either
the Blocks or Hierarchy checkbox lists. In this case. the coloring is by
volume so all voxels are shaded correctly. However, as noted previously,
if shading by 14 \_ tally , 24 \_ tally , 14 \_ relative \_ standard \_
deviation , or 24 \_ relative \_ standard \_ deviation , then only the
respective tally will be colored as shown in Fig. D.4, which is shaded
by the 14 \_ tally field (i.e., the tally values for mesh tally 14).

Figure D.2: Open Data With. . . Dialog Example

<!-- image -->

Figure D.3: Voxelwise Volume Example

<!-- image -->

Figure D.4: Voxelwise 14 \_ tally Example

<!-- image -->

Figure D.5: Truncated Time &amp; Energy-dependent Mesh Tally HDF5 File

<!-- image -->

Note that, as shown in Fig. D.3, the cylindrical mesh tally is shown
with facets despite being a curvilinear structured grid. No
visualization application is known at this time that can faithfully
display the curvilinear nature of the mesh.

## D.4.3.3 Saving Animation Frames from a Time-dependent Mesh Tally

An example time- and energy-dependent mesh tally is given in Listing
D.11, which produces the (truncated)

Listing D.11: Excerpt from fmesh\_xdmf\_tdep\_edep.mcnp.inp.txt

<!-- image -->

| fmesh14:n geom=xyz origin= 0 0 0 imesh=3   | iints=3              |
|--------------------------------------------|----------------------|
|                                            | jmesh=4 jints=4      |
|                                            | kmesh=5 kints=5      |
|                                            | tmesh=0 2 tints=1 50 |
|                                            | emesh=20 eints=2     |
|                                            | out=xdmf             |

HDF5 file shown in Fig. D.5. To export the time steps for the animation,
select a data set to color by that corresponds to the current time step
(e.g., 14 \_ tally \_ energy \_ total \_ time \_ current \_ bin ). Having done
so, one can then select File→Save Animation. . . , choose a prefix for
the saved file(s), click OK, configure the frame attributes (size, file
type, etc.), and click OK again. The export will the commence. Example
frames from the resulting animation are shown in Fig. D.6.

Figure D.6: Animation Frames

<!-- image -->
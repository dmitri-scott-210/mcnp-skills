---
title: "Appendix E.12 - Unstructured Mesh Pre-processing (um_pre_op)"
chapter: "E.12"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.12_Unstructured_Mesh_Pre-processing_(um_pre_op).pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## E.12 Unstructured Mesh Pre-processing ( um \_ pre \_ op )

## /\_445 Deprecation Notice

DEP-53422

The um \_ pre \_ op application is deprecated because its main
capabilities have been duplicated elsewhere.

The skeleton-input-file generation functionality has been duplicated in
an easier-to-maintain and distribute form such as that described in
[359]. Elemental quality assessment is now a standard part of MCNP UM
input processing, which is controlled using the elementchk argument on
the EMBED card.

The lattice-conversion capability is not duplicated elsewhere. People
interested in continuing to use these features should send an email to
mcnp\_help@lanl.gov.

The um\_pre\_op (unstructured mesh pre operations) program is a utility
program that performs various manipulations on input designed to aid in
problem setup with the unstructured mesh (UM). This program is written
in Fortran and uses various routines and data structures from the
Revised Extended Grid Library (REGL) in order to maintain consistency
with MCNP6. Like MCNP6, um\_pre\_op is designed to run from the command
line. Current supported features include creating a skeleton MCNP6 input
deck ( -m ) from the Abaqus/CAE mesh input file, converting a simple
lattice-voxel geometry ( -lc ) to an Abaqus mesh input file, volume
checking ( -vc ) the finite element volumes, and element checking ( -ec
) the mesh input file for twisted and/or deformed elements. As with
um\_post\_op , there is limited error handling.

## E.12.1 Command Line Options

To be reminded of um\_pre\_op's functionality and to see the command line
options, enter the following at the command line prompt:

<!-- formula-not-decoded -->

Note, your path must include the path to the program. A message similar
to the following should appear:

## ** PRE-PROCESSOR PROGRAM FOR UM CAPABILITY **

## Functions:

- 1) Create MCNP input file from Abaqus .inp file
- 2) Convert MCNP simple lattice to Abaqus .inp file
- 3) Volume check the Abaqus .inp file and pseudo-cells
- 4) Element check the Abaqus .inp file

```
Command Line Arguments: -b, --back
```

background material for input file

```
-h, --help summary of features & arguments -m, --mcnp generate MCNP skeleton input file -o, --output output file name
```

```
-cf, --controlfile file with lattice conversion controls -dc, --datacards data cards file to include -ex, --extension output file extension -ff, --fillfile file with lattice fill description -lc, --latconvert convert simple lattice to Abaqus ---vc, --volcheck volume check the .inp file ---ec, --elementcheck element check the .inp file ---len, --length scale factor for mesh dimensions
```

## Mutually Exclusive Options

Currently, this utility program has four mutually exclusive options:
generating (-m) a skeleton MCNP6 input file, converting ( -lc ) a simple
lattice-voxel geometry to an Abaqus mesh input file, volume checking (
-vc ) the finite element volumes, and element checking ( -vc ) for
twisted and/or deformed elements.

## The -o and -ex Options

The output file name ( -o, --output ) and extension name ( -ex,
--extension ) options are intended to be mutually exclusive. The user
should receive error messages if both of these arguments appear on the
same command line. However, one or the other must be used except where
indicated in the following feature discussions. If the -o argument is
present then the output is placed in a file with the name (or argument)
that immediately follows on the command line. If the -ex argument is
present, then the output is placed in a file with a name built from the
input file name followed by a period, '.', and the argument immediately
following on the command line.

## The -b Option

The -b option is currently only used with the -m option to specify a
background cell material number. See the discussion below for more
information.

## The -len Option

The -len option is currently only used with the -lc option. This is a
scale factor to apply to dimensions from the lattice mesh file.

```
--(1) (2) (3) (4)
```

## E.12.2 Examples

## Generating an MCNP6 Input File

A skeleton MCNP6 input file can be created from the Abaqus mesh input
file using the -m option. The name of the input file to be created is
set with either the -o or -ex options. The intent of this option is to
make it easier for users to get up and running with the unstructured
mesh capability and not necessarily to generate a fully functional input
file. The degree to which a fully functional input deck can be generated
depends upon the completeness and correctness of the data card file
provided with the -dc option.

The um\_pre\_op program can read the Abaqus mesh input file and generate a
global mesh model just as if MCNP6 was performing this function. The
information in the global mesh model is then used to create the
appropriate pseudo-cell cards, background cell, and minimal CSG world to
hold the mesh universe plus the embed control card for the data section.
If more than a minimal CSG structure is required outside the mesh
universe, the user must create this by hand.

If the -b option is not specified on the command line to supply a valid
material number from the Abaqus mesh input file, um\_pre\_op will make the
background cell void. If an invalid material number (i.e., a number for
a material that is not defined in the Abaqus mesh input file) is
specified with the -b option, um\_pre\_op will default to making the
background cell void. At this time the -b option only works with the -m
option.

When using the -m option it is possible to read a data cards file, -dc
argument, for inclusion in the new MCNP6 input file. The um\_pre\_op
program scans the data cards file for existing cards. For each particle
on an existing and active mode card, a default flux edit ( EMBEE card)
is specified and written to the new input file. If active IMP cards are
present in the data cards file, they are written to the new input file,
otherwise um\_pre\_op creates default IMP cards for each particle present
on the mode card. If an active SDEF card is present in the data cards
file, it is written to the new input file, otherwise a skeleton SDEF
card is written provided volume source elsets are present in the Abaqus
mesh input file. All other cards in the data cards file, regardless if
they are active cards or comments, are written to the new input file.

Note: At this point the material numbers for the material definitions in
the data cards file should be consistent with those used in the Abaqus
mesh input file. This may be the biggest source of error for some users.

Example command line with data cards argument and the -b argument to use
material 7 from the Abaqus mesh input file as the background material
for the mesh universe:

```
um _ pre _ op --mcnp -o newinput abaqus.inp -dc dc _ cards -b 7
```

## Converting a Simple Lattice Geometry

Simple lattice geometries in MCNP6 that use the fill parameter along
with the lat parameter on a cell card can be converted to an Abaqus mesh
input file for use with the -m option described previously or for
viewing as an orphan mesh geometry in Abaqus. This lattice geometry is
described as simple in that each voxel should have a homogenous
structure since each voxel is converted to a first order hexahedra with
a homogeneous material assignment.

For this feature, two input files are required and the mesh input file
must be specified using the -o option; the -ex option is invalid here.
In addition, a file named lat2abq.summary is created that contains
details about the conversion process. The first of the two input files
must contain only the fill information as it appears with the fill
parameter on the MCNP6 lattice cell card. A short example is given in
Listing E.14.

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

This is known as the fill file and is specified to um\_pre\_op with the
-ff option. Any attempt to put other information is this file will
undoubtedly cause um\_pre\_op to terminate in an unfriendly manner.

Listing E.14: Example fill file.

| 1 19R         |
|---------------|
| 2 7r 3 11R    |
| 2 2 4 2r      |
| 2 2 4 2r      |
| 3 4 3R 3 4 3R |

The second of the two required input files is the control file and is
specified to the um\_pre\_op program with the -cf option. An example is
provided in Listing E.15.

```
1 Jacksonville 1000 x 1000 x 31 model; 1 meter resolution 2 Deltas 100 100 100 3 fill 0:999 0:999 0:30 4 Origin center 5 # 6 universe 1 -1.25000E-03 air 7 universe 2 -0.05 ext _ building 8 universe 3 -0.01 int _ building 9 universe 4 -1.2 ground universe 5 -0.01 int _ garage universe 6 -0.087058 ext _ garage universe 7 -0.00125 air # exclude 1 extents 0 999 0 999 0 0 hints 200 200 50 threshhold 1
```

Listing E.15: Example control file

As can be seen from the description of this file that follows, there are
a number of parameters that can be adjusted for this feature, making it
tedious to implement and use as command line options.

The first line in the control file is the title line. The line is
required, must be the first line in the file, and can contain 256
characters of information. This line is inserted in the Abaqus mesh
input file on the line after the * Heading parameter at the beginning of
the file. This is the line that is used for the MCNP6 input file title
line if the um\_pre\_op -m option is invoked.

Any line after the first line with either a #, %, or $ in the first
column is treated as a comment line by um\_pre\_op and ignored.

All of the other parameters for this feature are implemented with a set
of keywords where the keyword appears at the beginning of the line
before any values. The keywords do not need to start in the first
column; they can be either upper case, lower case, or a mixture of both.
Most keywords have default values. Those that do not have defaults are
required keywords and should contain meaningful data.

The deltas keyword is required. Three values are needed that specify the
length of the voxels in centimeters along the x , y , and z directions.
These values will be used to size the hexahedra. All hexahedra will have
these dimensions.

The fill keyword is required. Three sets of values for the x , y , and z
directions are needed in the same format that MCNP6 requires for this
keyword on the lattice cell card. Each set consists of two lattice

locations separated by a colon. The value to the left of the colon is
the smallest index for that direction (for um\_pre\_op this value should
be 0) while the value to the right of the colon is the largest index for
that direction. The values specified for the fill keyword should be the
full extents of the problem described in the fill file. A subset of this
geometry can be specified with the extents parameter described below.

The universe keyword is required. There may be as many universes
specified on separate lines in the control file as needed to fully
describe the problem. For the sake of um\_pre\_op and converting a lattice
description to an equivalent unstructured mesh equivalent, the concept
of a universe is more restrictive than what MCNP6 allows in general. As
stated above, each voxel in the lattice must be homogeneous so that one
material can be assigned to it. Therefore, the universe numbers double
as material numbers. If the universe and material numbers don't coincide
in the existing description, it is up to the user to ensure that they do
coincide (are identical). If the user wishes to convert a more complex
voxel lattice to unstructured mesh, the complex voxels must be
homogenized.

Three values are required for each universe keyword. The first is the
universe number. There should be one for every universe number that is
used in the fill file. The universe numbers will be used as the material
numbers when describing the material elsets in the Abaqus mesh input
file. There is no default value for the universe number; so valid input
is required. The second value for the universe keyword is the material
density (either number or physical). This value will be written to the
pseudo-cell cards if um\_pre\_op is used with the -m option on this file.
The third value for this keyword, is the universe / material name that
can contain as many as 128 alphanumeric characters. This name is used in
creating material and part names. More information on the parts created
in this process can be found in the discussion for the hints keyword.

The following keywords are optional.

The exclude keyword is optional. It contains a single integer
instructing um\_pre\_op to exclude the specified universe number from any
of the parts. In the Fig. E.15 example, universe 1 is part of the simple
lattice, but because it is air that we don't want MCNP6 to track through
as a mesh, we exclude it. This can save computation time, but will not
let the program accumulate results on a mesh in these locations. When
excluding any universe, it is probably a good idea to set the background
material for the mesh universe to this material; see the -b option in
conjunction with the -m option..

The extents keyword is optional and is used to select a contiguous
extent of the lattice specified from the fill keyword. Default values
are 0, but any values specified are taken to apply in the order lower x
-index, upper x -index, lower y -index, upper y -index, lower z -index,
and upper z -index.

The hints keyword is optional, but highly recommended since values
associated with this keyword set the overall size of segments and parts.
Three values, one for each direction, are permitted with the default for
each being 9999999. The values are not physical units, but rather the
number of columns (X), rows (Y), or planes (Z). Since MCNP6 input
processing for parts in the unstructured mesh can be time intensive if
the parts have more than ~50,000 elements, it is best to segment any
geometry, whether it comes from a lattice or not, into smaller pieces.
The values associated with this keyword provide guidance to um\_pre\_op in
order to create these segments. um\_pre\_op will construct segments that
are close to the size specified. Each segment has a set of i -j -k
indices that describes its location from the lower left hand corner in
the overall geometry. Once the segments are defined, the program can
create parts from the segments. All elements with the same material are
lumped together into a part whose name is derived from the i -j -k
indices, the material number, and the material name. For example, a part
composed of the material 'ground' with an associated material number of
4 and possessing i -j -k indices of 2, 3, 1 would be given the name:
part \_ 2 \_ 3 \_ 1 \_ 4 \_ ground .

The origin keyword is optional and is used to adjust the location of the
mesh origin. If this keyword is not included, the origin defaults to 0 0
0, otherwise it is shifted to the value specified. An X Y Z location can
be specified, or as a convenience, the characters CENTER may be input.
With CENTER specified, the program calculates the problem's center based
upon the overall extents specified with the fill and deltas keywords.
Any triples of values causes the origin to shift to that location.

The threshold keyword is optional. It contains a single value
instructing um\_pre\_op to make parts when the number of elements in the
part exceed the value specified. The default value is 1. It is always a
good idea to create parts with more than 1 element.

The information in the lat2abq.summary file is fairly self-explanatory.
The information in this file can help the user set or adjust values for
the hints keyword, among other things. It was decided that it was more
appropriate to write this information to a file rather than to the
terminal screen.

Example command line to convert a simple lattice geometry:

<!-- formula-not-decoded -->

## Volume Checking

This option enables the user to check the finite element volumes
(against a value) and obtain volumes and masses for the pseudo-cells.
Results are printed to a file specified with either the -o or -ex
options. See the results from the example file at the end of this
section.

Any value appearing on the command line after the -vc argument is
treated as the test value. If this value is positive, um\_pre\_op will
print out all elements and their corresponding volumes that are greater
than or equal to the specified value. If this value is negative, all
elements and their corresponding volumes that are less than or equal to
the specified value are printed. If no value follows the -vc argument,
the test is for volumes less than or equal to zero.

Once the volume checks are performed on all of the finite elements,
um\_pre\_op calculates the volumes and masses for all of the pseudo-cells.
Masses are based on the densities that are present in the Abaqus mesh
input file. This information appears in the output file after the
element listing from the finite element volume check. After this, a list
of the instance names appears followed by a list of the material names
and associated densities.

Example command line to find all finite elements with a volume less than
or equal to 15:

```
um _ pre _ op -vc -15 -o vc.out simple _ cube _ warped.inp
```

## Element Checking

This option enables the user to check the Abaqus mesh input file for
deformed and/or twisted elements (an example is shown in Fig. E.8) by
calculating the determinant of the Jacobian at the appropriate Gauss
points and at all node locations that define the finite element. Normal
elements (i.e., not deformed or twisted) will have a positive Jacobian
indicating that each point (finite volume) in the master space is mapped
to an appropriate point (finite volume) in the global space (where some
of the tracking algorithms operate). However, very small positive values
indicate distortion in the mapping. With appropriate positive Jacobians,
the volumes and masses will be correct (as modeled) and there should be
no problem with the particle transport.

If a failed element is found (negative Jacobian) during the execution of
this option, the global element number and appropriate location
information are written to the terminal screen. This same information as
well as the results for the Jacobian evaluation at each Gauss and node
point are written to the file specified with either the -o or -ex
options. Note that the information is organized by instance. See the
results from the example

Figure E.8: Example twisted first-order tetrahedra.

<!-- image -->

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

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

file at the end of this section. It is the user's responsibility to fix
the problem mesh with the appropriate meshing tool.

Example command line:

```
um _ pre _ op -ec -o warped.out simple _ cube _ warped.inp
```

## Example Volume Check File

<!-- image -->

## Example Element Check File

<!-- image -->

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

<!-- image -->

| Number        | Name --------------------------------------------------------------------------------------   | Name --------------------------------------------------------------------------------------   | Name --------------------------------------------------------------------------------------   | Name --------------------------------------------------------------------------------------   | Name --------------------------------------------------------------------------------------   | Name --------------------------------------------------------------------------------------   | Name --------------------------------------------------------------------------------------   | Name --------------------------------------------------------------------------------------   |
|---------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| 1 part-cube-1 | 1 part-cube-1                                                                                 | 1 part-cube-1                                                                                 | 1 part-cube-1                                                                                 | 1 part-cube-1                                                                                 | 1 part-cube-1                                                                                 | 1 part-cube-1                                                                                 | 1 part-cube-1                                                                                 | 1 part-cube-1                                                                                 |
| Element:      | 2                                                                                             | failed.                                                                                       | Centroid:                                                                                     | 1.50000E+00                                                                                   | 1.50000E+00                                                                                   | 5.00000E-01                                                                                   | 5.00000E-01                                                                                   | 1.50000E+00                                                                                   |
|               |                                                                                               |                                                                                               | Nodes:                                                                                        | X Y                                                                                           | X Y                                                                                           | Z                                                                                             | Z                                                                                             |                                                                                               |
|               |                                                                                               |                                                                                               | 1                                                                                             | 2.00000E+00                                                                                   | 2.00000E+00                                                                                   | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   |
|               |                                                                                               |                                                                                               | 2                                                                                             | 2.00000E+00                                                                                   | 2.00000E+00                                                                                   | 0.00000E+00                                                                                   | 0.00000E+00                                                                                   | 1.00000E+00                                                                                   |
|               |                                                                                               |                                                                                               | 3                                                                                             | 2.00000E+00                                                                                   | 2.00000E+00                                                                                   | 0.00000E+00                                                                                   | 0.00000E+00                                                                                   | 2.00000E+00                                                                                   |
|               |                                                                                               |                                                                                               | 4                                                                                             | 2.00000E+00                                                                                   | 2.00000E+00                                                                                   | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   | 2.00000E+00                                                                                   |
|               |                                                                                               |                                                                                               | 5                                                                                             | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   |
|               |                                                                                               |                                                                                               | 6                                                                                             | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   | 0.00000E+00                                                                                   | 0.00000E+00                                                                                   | 1.00000E+00                                                                                   |
|               |                                                                                               |                                                                                               | 7                                                                                             | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   | 2.00000E+00                                                                                   |
|               |                                                                                               |                                                                                               | 8                                                                                             | 1.00000E+00                                                                                   | 1.00000E+00                                                                                   | 0.00000E+00                                                                                   | 0.00000E+00                                                                                   | 2.00000E+00                                                                                   |
|               |                                                                                               |                                                                                               |                                                                                               | Determinate Values At Gauss Points                                                            | Determinate Values At Gauss Points                                                            | Determinate Values At Gauss Points                                                            | Determinate Values At Gauss Points                                                            | Determinate Values At Gauss Points                                                            |
|               |                                                                                               |                                                                                               |                                                                                               | Gauss Points                                                                                  | Gauss Points                                                                                  | Gauss Points                                                                                  | Gauss Points                                                                                  | Jacobian                                                                                      |
|               |                                                                                               |                                                                                               | 1                                                                                             | -0.57735                                                                                      | -0.57735                                                                                      | -0.57735                                                                                      | -0.57735                                                                                      | 1.14E-01                                                                                      |
|               |                                                                                               |                                                                                               | 2                                                                                             | 0.57735                                                                                       | -0.57735                                                                                      | -0.57735                                                                                      | -0.57735                                                                                      | 1.14E-01                                                                                      |
|               |                                                                                               |                                                                                               | 3                                                                                             | 0.57735                                                                                       | 0.57735                                                                                       | 0.57735                                                                                       | -0.57735                                                                                      | 8.33E-02                                                                                      |
|               |                                                                                               |                                                                                               | 4                                                                                             | -0.57735                                                                                      | 0.57735                                                                                       | 0.57735                                                                                       | -0.57735                                                                                      | 8.33E-02                                                                                      |
|               |                                                                                               |                                                                                               | 5                                                                                             | -0.57735                                                                                      | -0.57735                                                                                      | -0.57735                                                                                      | 0.57735                                                                                       | 8.33E-02                                                                                      |
|               |                                                                                               |                                                                                               | 6                                                                                             | 0.57735                                                                                       | -0.57735                                                                                      | -0.57735                                                                                      | 0.57735                                                                                       | 8.33E-02                                                                                      |
|               |                                                                                               |                                                                                               | 7                                                                                             | 0.57735                                                                                       | 0.57735                                                                                       | 0.57735                                                                                       | 0.57735                                                                                       | -3.05E-02                                                                                     |
|               |                                                                                               |                                                                                               | 8                                                                                             | -0.57735                                                                                      | 0.57735                                                                                       | 0.57735                                                                                       | 0.57735                                                                                       | -3.05E-02                                                                                     |
|               |                                                                                               |                                                                                               | Determinate Values At Master Space Nodes                                                      | Determinate Values At Master Space Nodes                                                      | Determinate Values At Master Space Nodes                                                      | Determinate Values At Master Space Nodes                                                      | Determinate Values At Master Space Nodes                                                      | Determinate Values At Master Space Nodes                                                      |
|               |                                                                                               |                                                                                               | Gauss Points                                                                                  | Gauss Points                                                                                  | Gauss Points                                                                                  | Gauss Points                                                                                  | Gauss Points                                                                                  | Jacobian                                                                                      |
|               |                                                                                               |                                                                                               | 1                                                                                             | -1.00000                                                                                      | -1.00000                                                                                      | -1.00000                                                                                      | -1.00000                                                                                      | 1.25E-01                                                                                      |
|               |                                                                                               |                                                                                               | 2                                                                                             | 1.00000                                                                                       | -1.00000                                                                                      | -1.00000                                                                                      | -1.00000                                                                                      | 1.25E-01                                                                                      |
|               |                                                                                               |                                                                                               | 3                                                                                             | 1.00000                                                                                       | 1.00000                                                                                       | 1.00000                                                                                       | -1.00000                                                                                      | 1.25E-01                                                                                      |
|               |                                                                                               |                                                                                               | 4                                                                                             | -1.00000                                                                                      | 1.00000                                                                                       | 1.00000                                                                                       | -1.00000                                                                                      | 1.25E-01                                                                                      |
|               |                                                                                               |                                                                                               | 5                                                                                             | -1.00000                                                                                      | -1.00000                                                                                      | -1.00000                                                                                      | 1.00000                                                                                       | 1.25E-01                                                                                      |
|               |                                                                                               |                                                                                               | 6                                                                                             | 1.00000                                                                                       | -1.00000                                                                                      | -1.00000                                                                                      | 1.00000                                                                                       | 1.25E-01                                                                                      |
|               |                                                                                               |                                                                                               | 7                                                                                             | 1.00000                                                                                       | 1.00000                                                                                       | 1.00000                                                                                       | 1.00000                                                                                       | -1.25E-01                                                                                     |
|               |                                                                                               |                                                                                               | 8                                                                                             | -1.00000                                                                                      | 1.00000                                                                                       | 1.00000                                                                                       | 1.00000                                                                                       | -1.25E-01                                                                                     |
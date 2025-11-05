---
title: "Appendix E.11 - Unstructured Mesh Post-processing (um_post_op)"
chapter: "E.11"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.11_Unstructured_Mesh_Post-processing_(um_post_op.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## E.11 Unstructured Mesh Post-processing ( um \_ post \_ op )

## /\_445 Deprecation Notice

DEP-53423

The um \_ post \_ op application is deprecated because the legacy EEOUT
ASCII and binary files upon which it operates is deprecated [DEP-53294].

The um\_post\_op (unstructured mesh post operations) program is a utility
program that performs various manipulations on MCNP6's elemental edit
output file, EEOUT [DEP-53294]. This program is written in Fortran and
uses various routines and data structures from the Revised Extended Grid
Library (REGL) in order to maintain consistency with MCNP6. Like MCNP6,
um\_post\_op is designed to run from the command line. Current supported
features include adding and merging multiple EEOUT files into one,
converting binary files to ASCII, generating Visualization TooKit (VTK)
visualization files, creating instance-based pseudo-tallies, writing a
single edit to a file, and generating error histograms for those edits
with errors. Some of these features support the processing of multiple
files with one command.

## E.11.1 Command Line Options

To be reminded of um\_post\_op's functionality and to see the command line
options, enter the following at the command line prompt:

```
um _ post _ op --help
```

Note, your path must include the path to the program. A message similar
to the following should appear:

```
** UTILITY PROGRAM FOR UNSTRUCTURED MESH EEOUT FILE ** Functions:
```

- 1) add many eeout files into one
- 2) merge many eeout files into one
- 3) convert binary files into ascii files
- 4) generate vtk files for VisIt visualization
- 5) generate pseudo-tallies by pseudo-cell
- 6) write a single edit to an ascii file
- 7) generate a histogram of edit errors

## Command Line Arguments:

```
-h, --help summary of features & arguments -a, --add add multiple files (no weighting) -m, --merge merge multiple files -o, --output single output file name
```

| -p,   | --pos        | value range for wse and wsep        |
|-------|--------------|-------------------------------------|
| -bc,  | --binconvert | convert binary file to ascii        |
| -eh,  | --errorhist  | generate a histogram of edit errors |
| -ex,  | --extension  | multiple output file extension      |
| -ta,  | --tally      | pseudo-tallies from file            |
| -vtk, | --vtkfile    | generate ascii visualization file   |
| -wse, | --writesedit | write a single edit to file         |

## Mutually Exclusive Options

This utility program has seven mutually exclusive options: merging (-m)
many files into one ASCII file, adding (-a) many files together into one
ASCII file, converting (-bc) any number of binary files into ASCII
files, generating VTK files (-vtk) for visualization, generating pseudo-
tallies (-ta) for instances, writing a single edit (-wse) to an ASCII
file, and generating a histogram of edit errors (-eh) for those edits
that have errors. Only one of these options may be requested at a time.

## The -o and -ex Options

The output file name (-o, --output) and extension name (-ex,
--extension) options are intended to be mutually exclusive. The user
should receive error messages if both of these arguments appear on the
same command line. However, one or the other must be used. The output
file name is intended for use when there is one EEOUT file to manipulate
or many files that are to be merged into one. The extension name is pre-
appended with a period, '.', and then appears as the suffix to the input
file name(s) when new files must be created after processing many input
files (e.g., converting many files from ASCII to binary). The first
argument following these arguments is interpreted as either the output
file name or the extension name.

## E.11.2 Examples

## Merging Files

The original intent for this utility program was to establish a means of
merging many EEOUT files into one file. These many files are expected to
be from independent runs of a problem so that results are weighted by
the number of histories in the file. This differs from adding files
where there is no history weighting.

When the um\_post\_op utility is given a list of files to merge into one,
it reads the header information (that includes number of nodes,
materials, instances, tetrahedra, pentahedra, hexahedra) and checks the
consistency of this header information for each subsequent file against
the first file. For all files other than the first one, a message about
that consistency is output to the terminal window. Without consistency
among the files, the utility program can not make a meaningful and
successful merge.

If there is only one file specified for merging, the program will print
out an error message and stop. Since one file is created from many, the
output file name argument is required.

Example command line:

```
um _ post _ op -m -o my _ merge _ file eeout1 eeout2 ... eeoutN
```

Note that the first argument after the -o argument is interpreted as the
output file name.

At this time, the output file that is generated is ASCII, even if all of
the input files are binary. The input files may be any mixture of ASCII
or binary.

## Adding Files

This capability provides a means of adding (or collecting) many EEOUT
files into one file. These many files are expected to be from different
calculational runs on the same mesh geometry; results are NOT weighted
by the number of histories in the file. Rather, already normalized
results are simply added together. This differs from merging files where
there is history weighting. For example, this capability is useful if
there are different runs because independent sources were used in
different calculations and there is a need for the results to be
combined.

Cautions and restrictions discussed under the merging files section
apply here and are not repeated.

Example command line:

```
um _ post _ op -a -o my _ add _ file eeout1 eeout2 ... eeoutN
```

Note that the first argument after the -o argument is interpreted as the
output file name.

## Converting Files

This capability allows the conversion of EEOUT files from binary format
to ASCII. In performing this operation there is a loss of precision
since all double precision reals are written with only six significant
digits. Currently, there is no capability to convert from ASCII to
binary.

On the command line, one or many files may be specified for conversion.
When many files are requested for conversion, there is no consistency
check performed as there is when merging files since that is a
meaningless action for this option.

When the conversion request asks for only one file, the -o argument may
be used. Example command line:

```
um _ post _ op -bc -o eeout.ascii eeout.binary
```

It is also legitimate to use the -ex argument. Example command line:

```
um _ post _ op -bc -ex ascii eeout.binary
```

The resulting output file is named: eeout.binary.ascii

When more than one file is to be converted, the -ex argument must be
used. Example command line:

```
um _ post _ op -bc -ex asc eeout1 eeout2 ... eeoutN
```

The resulting files appear with the names

```
eeout1.asc eeout2.asc ... eeoutN.asc
```

## Creating Visualization Files

This capability should generate files in the VTK format for
visualization from EEOUT files. The geometry data and the edit
information is taken from the EEOUT file and reformatted to be
consistent with version 4.2 of the VTK standard and written to an ASCII
file. Details on the VTK file format and requirements can be found in
the VTK documentation, available on the worldwide web and in text books.

On the command line, one or many files may be specified for conversion
to the VTK format. When many files are requested for conversion, there
is no consistency check performed as there is when merging is requested
since that is a meaningless action for this option.

When the generation request asks for only one file, the -o argument may
be used.

Example command line:

```
um _ post _ op -vtk -o eeout.vtk eeout1
```

It is also legitimate to use the -ex argument. Example command line:

```
um _ post _ op -vtk -ex vtk eeout1
```

The resulting output file is named: eeout1.vtk

When more than one file is to be generated, the -ex argument must be
used. Example command line:

```
um _ post _ op -vtk -ex vtk eeout1 eeout2 ... eeoutN
```

The resulting files appear with the names

```
eeout1.vtk eeout2.vtk ... eeoutN.vtk
```

Note that while it is possible to specify any file extension or output
file name for the VTK file, some visualization programs will not
recognize it as such unless there is a VTK extension.

Note that this capability has not received extensive testing and may not
be supported in the future.

## Generating Pseudo-Tallies

This capability will generate a pseudo-tally for each pseudo-cell from
the corresponding edit and write the results to an output file (see
example at the end of this section). If no output file is specified, the
output is written to a file named 'fort.1001'. These tallies are volume
weighted according to the following equation:

<!-- formula-not-decoded -->

where

```
tally i tally for pseudo-cell i form corresponding edit vol n volume of element n edit n edit result of element n N total number of elements in i
```

These results are termed pseudo-tallies since they are equivalent to an
MCNP tally averaged over a cell ( i.e., F4, F6, F7), but do not have an
associated statistical uncertainty, tally fluctuation chart, etc. Note
that these pseudo-tallies are over pseudo-cells.

On the command line one or many files may be specified for pseudo-tally
creation. When many files are requested for pseudo-tally creation, there
is no consistency check performed as there is when merging files since
that is a meaningless action for this option.

When the conversion request asks for only one file, the -o argument may
be used.

Example command line:

```
um _ post _ op -ta -o eeout.tally eeout.binary
```

It is also legitimate to use the -ex argument.

## Writing A Single Edit To A File

This capability allows the user to write the edit results from a single
edit in the EEOUT file (see example at the end of this section) to an
ASCII file that is reformatted with detailed information. For each
element in the problem ( EEOUT file) the information that is available
with each edit result is element number, element type number, material
number, density, volume, and centroid location. The utility of this file
is left to the imagination of the user. Results are ordered by
increasing element number.

This request requires that an edit number be specified with the
um\_post\_op command line argument, -wse or --writesedit; this number
should be the argument immediately following this keyword argument. The
correct edit number can be found in the output from the pseudo-tally
option (see example at the end of this section for edit numbers in blue
font), described previously. Since an edit my contain multiple energy,
time, and particle bins, using the internal edit number requires less
input on the um\_post\_op command line.

Example command line:

```
um _ post _ op -wse 1 -o eeout.wse eeout1
```

It is also legitimate to use the -ex argument.

It is possible to filter the output for this capability using the -p or
--pos arguments. If the value following this argument is 1 or +1, only
values greater than zero are included in the edit. Conversely, if the
value following the argument is -1, only values less than or equal to
zero are included. If a real value is specified instead of the integers
just described, its value is the decision point with the sign of the
value indicating whether the filter provides values greater than ( + )
or less than or equal to ( -).

Example command line requesting to see all results less than or equal to
0.005.

um \_ post \_ op -wse 1 -p -5.e-3 -o eeout.wse eeout1

## Writing A Single Edit To A File By Position

This capability is similar to that discussed in the previous section,
except that the output is ordered by increasing position (i.e., x , y ,
z location). The appropriate arguments to use on the command line are:
-wsep or --writeseditpos. Value filtering, as described in the previous
section, works the same way with this capability.

## Generating A Histogram Of Edit Errors

This capability allows the user to write error histograms to an output
file for all of the edits in the EEOUT file for which errors were
requested (see example at the end of this section). If no output file is
specified, the output is written to a file named 'fort.1001'. The number
of histogram bins can be specified directly after the -eh command line
option. The default value is 10 if none is specified. The error bins are
defined such that the smallest error is assigned to the first bin and
the largest error is assigned to last bin. Bins are evenly spaced
between the first and the last bins. Relative error values are in the
range of 0 to 1, inclusive. See §8.4 for more details on errors and the
EEOUT file.

The essential header information from the EEOUT file is written at the
beginning of the error histogram file. Following this information, there
is a section for each edit for which errors were requested. There is a
description of each edit. In each section following the edit
description, there are results by pseudo-cell and results over all mesh
in the model. For each group of results there is the minimum and maximum
errors on the edit in addition to a table with the error histogram. For
each row in the histogram table there is the upper limit for the error
bin, the absolute number of elements that fall into this bin, the
relative percentage these elements represent of the total, and the
cumulative percentage of the current row and all preceding rows.

Example command line specifying a table with 20 bins:

```
um _ post _ op -eh 20 -o my _ error _ histogram eeout1
```

It is also legitimate to use the -ex argument.

## Miscellaneous

The REGL routine that reads valid EEOUT files [DEP-53294] has the
ability to detect whether the file it is reading is ASCII or binary. If
it can't make a determination that the file is a valid EEOUT file, an
error message appears in the terminal window. Therefore, when a list of
files is specified on the command line, for either merging, adding, or
generating VTK files, they may be a mixture of ASCII or binary.

## Example Pseudo-Tally File

What follows is not a complete example. Only enough details are provided
to illustrate the main points.

<!-- image -->

| Pseudo-tallies for eeout file via um _ post _ op Eeout file: eeout1007                     | Pseudo-tallies for eeout file via um _ post _ op Eeout file: eeout1007                     |
|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Created on : 4- 3-2012 @ 9: 0:37                                                           | Created on : 4- 3-2012 @ 9: 0:37                                                           |
| Prob ID : simple cube, each element is a statistical set, 8 total                          | Prob ID : simple cube, each element is a statistical set, 8 total                          |
| Calling Code : MCNP6                                                                       | Calling Code : MCNP6                                                                       |
| Inp File : inp1007                                                                         | Inp File : inp1007                                                                         |
| Outp File : inp1007o                                                                       | Outp File : inp1007o                                                                       |
| Runtpe File : inp1007r                                                                     | Runtpe File : inp1007r                                                                     |
| Geom Inp File : um1007.inp                                                                 | Geom Inp File : um1007.inp                                                                 |
| NUMBER OF NODES :                                                                          | 27                                                                                         |
| NUMBER OF MATERIALS:                                                                       | 1                                                                                          |
| NUMBER OF INSTANCES:                                                                       | 1                                                                                          |
| NUMBER OF 1st TETS :                                                                       | 0                                                                                          |
| NUMBER OF 1st PENTS:                                                                       | 0                                                                                          |
| NUMBER OF 1st HEXS :                                                                       | 8                                                                                          |
| NUMBER OF 2nd TETS :                                                                       | 0                                                                                          |
| NUMBER OF 2nd PENTS:                                                                       | 0                                                                                          |
| NUMBER OF 2nd HEXS :                                                                       | 0                                                                                          |
| NUMBER OF COMPOSITS:                                                                       | 1                                                                                          |
| NUMBER OF HISTORIES:                                                                       | 1000                                                                                       |
| NUMBER OF REG EDITS:                                                                       | 19                                                                                         |
| NUMBER OF COM EDITS:                                                                       | 9                                                                                          |
| EDIT: 1 :: TALLY for EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14 | EDIT: 1 :: TALLY for EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14 |
| Energy Bin Boundary: 1.00000E+36 Energy Bin                                                | Multiplier: 1.00000E+00                                                                    |
| Time Bin Boundary : 1.00000E+33                                                            | Time Bin Multiplier : 1.00000E+00                                                          |
| Instance Name                                                                              | Volume Result                                                                              |
| -------- ----                                                                              | ------ ------                                                                              |

<!-- image -->

## Example Single Edit File

| Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     | Write single edit for eeout file via um _ post _ op                                     |
|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   | Eeout file: eeout1007                                                                   |
| Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       | Created on : 4- 3-2012 @ 12:11:25                                                       |
| Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       | Prob ID : simple cube, each element is a statistical set, 8 total                       |
| Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    | Calling Code : MCNP6                                                                    |
| Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    | Outp File : inp1007o                                                                    |
| Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  | Runtpe File : inp1007r                                                                  |
| Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              | Geom Inp File : um1007.inp                                                              |
| 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      | 12                                                                                      |
| NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    | NUMBER OF NODES : 27                                                                    |
| NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  | NUMBER OF MATERIALS: 1                                                                  |
| NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  | NUMBER OF INSTANCES: 1                                                                  |
| NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  | NUMBER OF 1st PENTS: 0                                                                  |
| NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  | NUMBER OF 1st HEXS : 8                                                                  |
| NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  | NUMBER OF 2nd TETS : 0                                                                  |
| NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  | NUMBER OF 2nd PENTS: 0                                                                  |
| NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  | NUMBER OF 2nd HEXS : 0                                                                  |
| NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        | NUMBER OF COMPOSITS: 1 NUMBER OF HISTORIES: 1000                                        |
| NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 | NUMBER OF REG EDITS: 19                                                                 |
| NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- | NUMBER OF COM EDITS: 9 ---------------------------------------------------------------- |
| 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              | 1 :: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 14              |
| 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                | 28 EDIT:                                                                                |
| 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      | 29                                                                                      |
| 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  | 30 Energy Bin Boundary: 1.00000E+36 Energy Bin Multiplier: 1.00000E+00                  |
| 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    | 31 Time Bin Boundary : 1.00000E+33 Time Bin Multiplier : 1.00000E+00                    |
| 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      | 32                                                                                      |

40

41

42

43

44

|   4 |   6 |   1 |   1.87401E+01 |   1.25000E+02 |   -2.50000E+00 |   2.50000E+00 |   2.50000E+00 |   4.99248E-02 |
|-----|-----|-----|---------------|---------------|----------------|---------------|---------------|---------------|
|   5 |   6 |   1 |       18.7401 |           125 |            2.5 |          -2.5 |           7.5 |     0.0459879 |
|   6 |   6 |   1 |       18.7401 |           125 |            2.5 |           2.5 |           7.5 |     0.0514196 |
|   7 |   6 |   1 |       18.7401 |           125 |            2.5 |          -2.5 |           2.5 |     0.0433516 |
|   8 |   6 |   1 |       18.7401 |           125 |            2.5 |           2.5 |           2.5 |     0.0494486 |

## Example Error Histogram File

| Write                                                                      | error histograms for eeout file via um _ post _ op block01 _ 6part _ 6type.eeout   |
|----------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| Eeout file: Created on                                                     | : 3-11-2014 @ 13: 8:21                                                             |
| Prob ID Calling Code Code Version                                          | : block01 8x8x6 6 parts, 6 element types : MCNP6 _ DEVEL :                         |
| Date & Time                                                                | 6-1-02                                                                             |
| :                                                                          | 03/11/14 12.43.38                                                                  |
| Inp File :                                                                 | block01mgv1                                                                        |
| Outp File :                                                                | outy                                                                               |
| Runtpe File :                                                              |                                                                                    |
| Geom Inp File : job _                                                      | runtpn block _ 6part _ 6type _ 01.inp                                              |
| NUMBER OF NODES : NUMBER OF MATERIALS:                                     | 1258 6                                                                             |
| NUMBER OF 1st TETS : NUMBER OF 1st PENTS: NUMBER OF 1st HEXS :             | 6                                                                                  |
| NUMBER OF INSTANCES:                                                       |                                                                                    |
|                                                                            | 30                                                                                 |
|                                                                            | 8                                                                                  |
|                                                                            | 128                                                                                |
| NUMBER OF 2nd TETS :                                                       | 29                                                                                 |
| NUMBER OF 2nd PENTS:                                                       | 8                                                                                  |
| NUMBER OF 2nd HEXS :                                                       | 128                                                                                |
| NUMBER OF COMPOSITS:                                                       | 0                                                                                  |
| NUMBER OF HISTORIES:                                                       | 1000000                                                                            |
| NUMBER OF REG EDITS:                                                       | 2                                                                                  |
| NUMBER OF COM EDITS:                                                       | 0                                                                                  |
| EDIT: EDIT __ PARTICLE _ 1 __ TIME _ BIN _ 1 _ ENERGY _ BIN _ 1 _ FLUX _ 4 | ---------------------------------------------------------------                    |

<!-- image -->

| Energy Bin Boundary:                                                              | Energy Bin Boundary:                                                              | Energy Bin Boundary:                                                              | 1.00000E+10                                                                       | Energy Bin Multiplier:                                                            | 1.00000E+00                                                                       |
|-----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Time Bin Boundary :                                                               | Time Bin Boundary :                                                               | Time Bin Boundary :                                                               | 1.00000E+39                                                                       | Time Bin Multiplier :                                                             | 1.00000E+00                                                                       |
| ---------------------------------------------------- _ _                          | ---------------------------------------------------- _ _                          | ---------------------------------------------------- _ _                          | ---------------------------------------------------- _ _                          | ---------------------------------------------------- _ _                          | ---------------------------------------------------- _ _                          |
| Minmum Error Maximum Error :                                                      | Minmum Error Maximum Error :                                                      | Minmum Error Maximum Error :                                                      | : 1.64393E-02                                                                     | : 1.64393E-02                                                                     | : 1.64393E-02                                                                     |
| Bin Width                                                                         | Bin Width                                                                         | Bin Width                                                                         | 1.70379E-02                                                                       | 1.70379E-02                                                                       | 1.70379E-02                                                                       |
|                                                                                   |                                                                                   |                                                                                   | : 2.99308E-05                                                                     | : 2.99308E-05                                                                     | : 2.99308E-05                                                                     |
| ------                                                                            | --------                                                                          | --------                                                                          | --------                                                                          | ----------                                                                        |                                                                                   |
| Bin                                                                               | Upper                                                                             | Absolute                                                                          | Relative                                                                          | Cumulative                                                                        |                                                                                   |
| Number                                                                            | Bound                                                                             | Number                                                                            | (%) --------                                                                      | (%)                                                                               |                                                                                   |
| ------                                                                            | --------                                                                          | --------                                                                          |                                                                                   | ----------                                                                        |                                                                                   |
| 1 2                                                                               | 1.6469E-02 1.6499E-02                                                             | 1                                                                                 | 1 0.7812                                                                          | 0.7812 0.7812 1.5625                                                              |                                                                                   |
| 3                                                                                 | 1.6529E-02                                                                        | 3                                                                                 | 2.3438                                                                            | 3.9062                                                                            |                                                                                   |
| 4                                                                                 | 1.6559E-02                                                                        | 5                                                                                 | 3.9062                                                                            | 7.8125                                                                            |                                                                                   |
| 5                                                                                 | 1.6589E-02                                                                        | 0                                                                                 | 0.0000                                                                            | 7.8125                                                                            |                                                                                   |
| 6                                                                                 | 1.6619E-02                                                                        | 7                                                                                 | 5.4688                                                                            | 13.2812                                                                           |                                                                                   |
| 7                                                                                 | 1.6649E-02                                                                        | 6                                                                                 | 4.6875                                                                            | 17.9688                                                                           |                                                                                   |
| 8                                                                                 | 1.6679E-02                                                                        | 14                                                                                | 10.9375                                                                           | 28.9062                                                                           |                                                                                   |
| 9                                                                                 | 1.6709E-02                                                                        | 5                                                                                 | 3.9062                                                                            | 32.8125                                                                           |                                                                                   |
| 10                                                                                | 1.6739E-02                                                                        | 6                                                                                 | 4.6875                                                                            | 37.5000                                                                           |                                                                                   |
| 11                                                                                | 1.6769E-02                                                                        | 13                                                                                | 10.1562                                                                           | 47.6562                                                                           |                                                                                   |
| 12                                                                                | 1.6798E-02                                                                        | 14                                                                                | 10.9375                                                                           | 58.5938                                                                           |                                                                                   |
| 13                                                                                | 1.6828E-02                                                                        | 12                                                                                | 9.3750                                                                            | 67.9688                                                                           |                                                                                   |
| 14                                                                                | 1.6858E-02                                                                        | 11                                                                                | 8.5938                                                                            | 76.5625                                                                           |                                                                                   |
| 15                                                                                | 1.6888E-02                                                                        | 5                                                                                 | 3.9062                                                                            | 80.4688                                                                           |                                                                                   |
| 16                                                                                | 1.6918E-02                                                                        | 10                                                                                | 7.8125                                                                            | 88.2812                                                                           |                                                                                   |
| 17                                                                                | 1.6948E-02                                                                        | 4                                                                                 | 3.1250                                                                            | 91.4062                                                                           |                                                                                   |
| 18                                                                                | 1.6978E-02                                                                        | 7                                                                                 | 5.4688                                                                            | 96.8750                                                                           |                                                                                   |
| 19                                                                                | 1.7008E-02                                                                        | 3                                                                                 | 2.3438                                                                            | 99.2188                                                                           |                                                                                   |
| 20                                                                                | 1.7038E-02                                                                        | 1                                                                                 | 0.7812                                                                            | 100.0000                                                                          |                                                                                   |
| 67 (Results for instances 2 through 6 were removed to make this example shorter.) | 67 (Results for instances 2 through 6 were removed to make this example shorter.) | 67 (Results for instances 2 through 6 were removed to make this example shorter.) | 67 (Results for instances 2 through 6 were removed to make this example shorter.) | 67 (Results for instances 2 through 6 were removed to make this example shorter.) | 67 (Results for instances 2 through 6 were removed to make this example shorter.) |
| ---------------------                                                             | ---------------------                                                             | ---------------------                                                             | ---------------------                                                             | ---------------------                                                             | ---------------------                                                             |
| Results Over All Mesh                                                             | Results Over All Mesh                                                             | Results Over All Mesh                                                             | Results Over All Mesh                                                             | Results Over All Mesh                                                             | Results Over All Mesh                                                             |
| Minmum Error                                                                      |                                                                                   | : 9.33224E-03                                                                     | : 9.33224E-03                                                                     | : 9.33224E-03                                                                     | : 9.33224E-03                                                                     |

| Maximum Error               | :                 | 1.95299E-02                             |
|-----------------------------|-------------------|-----------------------------------------|
| Bin Width                   | : 5.09881E-04     | : 5.09881E-04                           |
| ------ -------- Bin Upper   | -------- Absolute | -------- ---------- Relative Cumulative |
| 1 9.8421E-03                | 4                 | 1.2085 1.2085                           |
| 2 1.0352E-02 1.0862E-02     | 8                 | 2.4169 0.0000                           |
| 3                           | 0                 | 3.6254 3.6254                           |
| 4 1.1372E-02                | 0                 | 0.0000 3.6254                           |
| 1.1882E-02                  |                   | 1.2085 4.8338                           |
| 5 6 1.2392E-02              | 4 1               | 0.3021 5.1360                           |
| 7 1.2901E-02                | 0                 | 0.0000 5.1360                           |
| 8 1.3411E-02                | 3                 | 0.9063 6.0423                           |
| 9 1.3921E-02                | 3                 | 0.9063 6.9486                           |
| 10 1.4431E-02               | 9                 | 2.7190 9.6677                           |
| 11 1.4941E-02               | 9                 |                                         |
| 12                          |                   | 2.7190 12.3867                          |
| 1.5451E-02                  | 4                 | 1.2085 13.5952                          |
| 13 1.5961E-02               | 0                 | 0.0000 13.5952 4.5317                   |
| 14 1.6471E-02               | 15                | 18.1269                                 |
| 16                          | 18                | 5.4381                                  |
| 1.7490E-02                  |                   | 96.3746                                 |
| 17 1.8000E-02 18 1.8510E-02 | 5 6               | 1.5106 97.8852 1.8127 99.6979           |
| 19 1.9020E-02 20 1.9530E-02 | 0 1               | 0.0000 99.6979 0.3021 100.0000          |
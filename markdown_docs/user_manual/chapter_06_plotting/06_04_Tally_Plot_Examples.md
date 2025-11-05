---
title: "Chapter 6.4 - Tally Plotting Examples"
chapter: "6.4"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/6_MCNP_Geometry_and_Tally_Plotting/6.4_Tally_Plotting_Examples.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

1

values is a list of tally value-error data pairs, on as many lines as
necessary. The ordering is similar to that of the standard tally
ordering but with fewer bins. In a RMESH tally with 3 bins on the CORA
card ( x ), 2 bins on the CORB card ( y ), and 2 bins on the CORC card (
z ), the ordering is as follows: ( x 1 , y 1 , z 1 ) , ( x 2 , y 1 , z 1
) , ( x 3 , y 1 , z 1 ) , ( x 1 , y 2 , z 1 ) , ( x 2 , y 2 , z 1 ) , (
x 3 , y 2 , z 1 ) , ( x 1 , y 1 , z 2 ) , ( x 2 , y 1 , z 2 ) ,... , ( x
3 , y 2 , z 2 ) . In the event that there are multiple S-bins, the CORA
, CORB , and CORC coordinates for each S-bin are grouped. In other
words, the CORA bins are under the CORB bins, which are under the CORC
bins, which are under the S-bins.

## 6.3.4.1.4 KCODE Information

If a MCTAL file is written during a KCODE problem, the following
information is included:

kcode kcz ikz l (A5,3I5) (or (A5, 3I10) if kcz or ikz &gt; 9999), where

```
kcz is the number of recorded KCODE cycles. ikz is the number of settle cycles. l is the number of variables provided for each cycle (set in code to 19).
```

List of KCODE quantities on as many lines as necessary (5ES12.6). The
quantities are: k eff. (collision), k eff. (absorption), k eff. (track
length), prompt removal lifetime (collision), prompt removal lifetime
(absorption), average collision k eff. , average collision k eff.
standard deviation, average absorption k eff. , average absorption k
eff. standard deviation, average track length k eff. , average track
length k eff. standard deviation, average col/abs/trklen k eff. ,
average col/abs/trk-len k eff. standard deviation, average col/abs/trk-
len k eff. by cycles skipped, average col/abs/trk-len k eff. by cycles
skipped standard deviation, prompt removal lifetime (col/abs/trklen),
prompt removal lifetime (col/abs/trk-len) standard deviation, number of
histories used in each cycle, col/abs/trk-len k eff. figure of merit 1 .

## Details:

- 1 The col/abs/trk-len k eff. figure of merit is only printed if the mct option on the PRDMP card is equal to 1. If the MCTAL file is written with mct = -1 or -2 , this value will always be zero.

## 6.4 Tally Plotting Examples

## 6.4.1 Example of Use of COPLOT

Assume all parameter-setting commands [§6.3.3.5] have been previously
defined. The following input line will put two curves on one plot:

RUNTPE A.h5 COPLOT RUNTPE B.h5

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

The first curve will display tally data from RUNTPE file ' A.h5 ' and
the second curve will display tally data from the RUNTPE file ' B.h5 '
for the same tally number. Unless reset, MCPLOT will continue to read
from B.h5 for subsequent plot commands.

If there is a current RUNTPE file read, the following commands can be
entered:

```
1 XLIMS min max TALLY 11 COPLOT RMCTAL AUX TALLY 41 & 2 COPLOT RUNTPE A.h5 TALLY 1
```

These commands change the upper and lower limits of the x -axis to max
and min , respectively and plots tally 11 from the current RUNTPE . The
first COPLOT entry requests the plotter to draw a second curve (tally
41) from the MCTAL file named ' AUX '. The third curve is requested on
the next line (note the &amp; at the end of the first line). This final
curve is tally 1 from The RUNTPE file named ' A.h5 '. Any subsequent
plot requests will use data from RUNTPE A.h5 unless reset.

The command

```
1 TALLY 24 NONORM FILE COPLOT TALLY 44
```

will output tally 24 and tally 44 to the graphics metafile.

## 6.4.2 Radiography Tally Contour Plot Example

Tally output may be plotted as 2-D color contours from either MCTAL or
RUNTPE files. For example, a radiography tally with s and t -axes
specified on FS and C cards can be plotted with the MCNP6 Z execute
option, as described below.

The following example is a radiograph of a 4-cm-radius, 1-cm-thick 238 U
disc with an embedded 4-mm-void sphere and skew-oriented 1-cm × 1-cm ×
8-mm box. The input file is given in Listing 6.1.

```
1 Radiography Tally 2 1 5 -25.0 -1 4 5 imp:p=1 3 2 0 1 -2 imp:p=1 4 3 0 2 imp:p=0 5 4 0 -4 imp:p=1 6 5 0 -5 imp:p=1 7 8 1 RCC 0 0 0 0 0 1 4 9 2 RPP -100 100 -100 100 -100 100 4 SPH 3 0 0.5 0.4 5 BOX -1 1 0.1 0.6 0.8 0 -0.8 0.6 0 0 0 0.8 mode p nps 100 5 sdef pos=0 0 -20 axs=0 0 1 rad=d1 ext=0 vec=0 0 1 dir=d2 erg=6 si1 0 0.1 sp1 -21 1 si2 -1 1 sp2 -31 1 m5 92238 1
```

Listing 6.1: example\_radiograph\_tally.mcnp.inp.txt

<!-- image -->

Figure 6.5: Geometry plot of radiograph example.

<!-- image -->

The x -y plot of this geometry is given in Fig. 6.5. To get the contour
plot, first run the input, then type the following MCNP6 execution line
command:

1

## MCNP6 Z RUNTPE=filename

The contour plots may also be read from a MCTAL file instead of the
RUNTPE file [§6.3 introduction]. When the code presents the MCPLOT&gt;
prompt, enter the two tally dimensions corresponding to the horizontal
and vertical axes of the radiography plot with the FREE command
[§6.3.3.7]. For example to see the radiography tally in Listing 6.1,
which has image bins defined by the 'S' tally dimension (from the FS
entries) and the 'C' tally dimension (from the C entries), one would
simply enter ' FREE SC ' at the MCPLOT&gt; prompt. The plot axes are then
oriented according to the right-hand rule between the reference
direction on the FIR entry and the global coordinates. For more
information on how this orientation is determined, see Section
5.9.1.3.3.

The results are plotted in Figure 6.6. The embedded sphere and box are
seen plainly in the disc.

Figure 6.6: Scattered photon radiographic image of 238 U disc.

<!-- image -->

Recall that the possible tally dimensions are FDUSMCET [§5.9.19,
§6.3.3.7].

Thus, if the radiography tally has other bins such as energy or time
bins, the plot for these bins can be examined with the ' FIXED ' command
[§6.3.3.7] following the ' FREE SC ' command.

## 6.4.3 TMESH Mesh Tally Plot Examples

TMESH mesh tallies may be plotted either in the MCNP6 tally plotter (
MCPLOT ) from MCTAL files or superimposed over geometry plots in the
geometry plotter ( PLOT ) from RUNTPE files.

## 6.4.3.1 MCPLOT TMESH Mesh Tally

Listing 6.2 is a critical configuration of seven identical barrels of
fissionable material.

Listing 6.2: example\_plotting\_tmesh\_tally.mcnp.inp.txt

<!-- image -->

<!-- image -->

Figure 6.7: Geometry of the seven-barrel problem.

<!-- image -->

The geometry is shown in Figure 6.7.

The mesh tally is generated from a MCTAL file in the MCPLOT tally
plotter, called with the MCNP6 Z input line. The plot command to enter
at the MCPLOT&gt; prompt to read the MCTAL file and plot the TMESH tally
is:

```
1 rmctal mctal _ filename tal 12 free ik
```

Figure 6.8 shows the resulting TMESH tally of the configuration.

## 6.4.3.2 Superimposed Geometry Plot TMESH MESH Tally

Figure 6.9 shows the TMESH mesh tally results superimposed over the
geometry plot. First, the RUNTPE file

Figure 6.8: Mesh tally of barrel geometry.

<!-- image -->

Figure 6.9: TMESH Mesh plot superimposed on geometry plot.

<!-- image -->

1

```
1
```

1

2

3

4

5

6

must be loaded using the MCNP6 Z option:

```
mcnp6 z r=runtpe _ filename
```

Then, at the MCPLOT&gt; prompt, the MCNP geometry plotter is invoked with
the PLOT command.

Next, the MCNP geometry needs to be oriented such that the mesh tally is
in view. For the geometry of Figure 6.9, click on the lower left box
('Click here or picture. . . ') and enter the following command:

```
or 0 4 0 py 4 ex 40 la 0 0
```

To plot the TMESH tally results, make the mesh tallies the 'Edit'
quantity by clicking the tal button at the bottom of the right-hand
control bar (§6.2.3.3):

Click tal and check if the tally number expected shows on the left-hand
information pane (see entry for ' Value for var ' in §6.2.3.2). If the
tally number presented in the information pane is not the mesh tally of
interest, click the N button below tal to cycle available tallies.

Note: The format of the information pane for the tallies sometimes makes
the tally number and tally value appear as a single digit like so:
tal1114.6784-5. In these cases, the plotter is not broken.

After the 'Edit' quantity is specified, the color parameter must be
changed to reflect the selected tally. Change the color parameter by
clicking the COLOR button in the lower left control box twice. The first
click will change the text in the box to ' COLOR off ' and, for this
example, the next click will change it to read ' COLOR tal12 '. Once the
color parameter is set, the Redraw button in the bottom-middle of the
plotter must be clicked.

In addition, the actual mesh tally voxel borders can be displayed by
clicking CellLine button and cycling through the options to get either '
MeshTaly ' (which draws mesh tally grid lines over the results) or
MT+Cell (which draws mesh tally grid lines and cell surface lines over
the plot).

## 6.4.4 MCPLOT FREE Command Examples

## 6.4.4.1 Example 1

Consider the input shown in Listing 6.3, which is a simple 3x3x2 lattice
of water spheres surrounded by air with a monoenergetic and
monodirectional photon source incident on the lattice parallel to the i
-dimension in the top layer and bisecting the j -dimension. Thus, we
would expect to see a higher tally value on the [-1:1 1 1] lattice
elements (refer to §5.9.1.5 for information on lattice tally indexing).

```
Example lattice tally 10 100 -1 -1 u=1 imp:p=1 20 200 -0.00125 1 u=1 imp:p=1 30 0 -2 u=2 lat=1 imp:p=1 fill=-1:1 -1:1 0:1 1 17r
```

Listing 6.3: example\_mcplot\_free.mcnp.inp.txt

```
7 40 0 2 u=2 imp:p=0 8 50 0 -3 fill=2 imp:p=1 9 60 0 3 -4 imp:p=1 10 70 0 4 imp:p=0 11 12 1 so 0.75 13 2 rpp -1 1 -1 1 -1 1 14 3 rpp -3 3 -3 3 -1 3 15 4 so 100 16 17 mode p 18 nps 1e4 19 sdef par=p dir=1 vec=1 0 0 pos=-4 0 2 20 c 21 f4:p (10<30[-1:1 -1:1 0:1]<50) 22 c 23 prdmp 2j 1 24 print -128 25 m100 1001 2 8016 1 26 m200 7014 0.78 8016 0.22
```

First, each layer (in the k -dimension) can be examined by first calling
the MCPLOT module with the MCNP6 Z execution line then entering:

1

tally 4 free ij 3x3 fixed

```
k=1
```

which gives Figure 6.10.

The second layer can be seen with:

```
1 tally 4 free ij 3x3 fixed k=2
```

which gives Figure 6.11.

It can then be useful to examine a single row of lattice elements. In
this case, the elements directly in the line of the source beam may be
of interest. The way to do this is somewhat non-intuitive. To get a
1-dimensional plot of the three elements directly inline with the beam,
the following command is entered at the MCPLOT&gt; prompt:

free i 3x3 fixed j=2 fixed k=2

Which gives Figure 6.12.

The first command in the sequence, FREE i 3x3 , preps the MCPLOT module
to expect a FIXED command for the other two tally dimensions and the
lattice positions of interest lie in the 3x3 plane on the second level
of the lattice. The FIXED j=2 command requests the second slice into the
j -dimension and likewise the second FIXED command sets the k -index to
the second layer. Referring to Listing 6.3 the lattice is specified as
'fill= -1:1 -1:1 0:1' but it is accessed with the location of the
desired position in the 1-indexed Fortran array (i.e., the middle slice
of the i and j -dimensions is '2', not '0').

When considering the resulting MCTAL file (shown in Listing 6.4), the
offset into the MCTAL output can be easily determined. The description
of the MCTAL file format is in Section 6.3.4 and describes the order of
the values in the file.

1

<!-- image -->

ijk tally: i

Figure 6.10: FREE Command Bottom Layer ( FIXED K=1 )

<!-- image -->

jk tally: i

Figure 6.11: FREE Command Top Layer ( FIXED K=2 )

Figure 6.12: 1-Dimensional Slice of the 3x3x2 Lattice Tally

<!-- image -->

Listing 6.4: example\_mcplot\_free.mcnp.mctal.txt

<!-- image -->

In the case of the lattice tally in this example, there are no bins in
the FDUSMCET array other than the F -bins which are indexed with their
ijk locators. The values go as follows: ( i 1 , j 1 , k 1 ) , ( i 2 , j
1 , k 1 ) , ( i 3 , j 1 , k 1 ) , ( i 1 , j 2 , k 1 ) , ( i 2 , j 2 , k
1 ) , ( i 3 , j 2 , k 1 ) , . . . , ( i 1 , j 3 , k 2 ) , ( i 2 , j 3 ,
k 2 ) , ( i 3 , j 3 , k 2 ) . Following this ordering, it's clear that
the slice of interest for this problem is the 13th to 15th value-error
pairs. Thus, we expect an offset into the array of 12 value-error pairs.
Examining the way the values are ordered, first we step over all the
values where k n = k 1 to get to the start of the second layer: (3 × 3)
× (2 -1) = 9 . Then, we need to step over all the values where k n = k 2
and j m = j 1 to get to the start of the j 2 values in the second layer:
3 × 1 = 3 . Thus, our offset is 9 + 3 = 12 , as evident in the MCTAL
file with the largest value-error pairs on line 21. In other words, we
can consider the offset indexing of the value-error pairs to be from 0,
where the values on the FIXED command are from 1, so one can account for
the off-by-one error and calculate the offset like:

```
( i -dimension × j -dimension ) × ( Fixed k -dimension -1) + j -dimension × ( Fixed j -dimension -1) (6.1)
```

The above equation can be generalized with an understanding of the way
the values in the MCTAL files are presented, and the desired results to
plot.

If the j and k -indices had not been specified, their default value of 1
is assumed, which results in an offset of 0.

Finally, the normalization of the values comes from the minimum and
maximum value of the 3 i -bin values shown in the plot.

## 6.4.4.2 Example 2

The command

```
1 FREE IJ 10x30 ALL FIXED K=60
```

specifies a 10 × 30 2-D contour plot, which corresponds to a lattice
tally with 10 i -bins, 30 j -bins, and at least 60 k -bins. The k -index
is specified using the FIXED command, which sets the offset into the F
-bins as

```
( i -dimensions × j -dimensions ) × ( Fixed k -dimension -1) = (10 × 30) × 59 = 17 , 700 (6.2)
```

In this case, the ALL option on the FREE command causes the contour
range to taken from all of the F -bin tally values.

## 6.4.5 Photonuclear and Photoatomic Cross-section Plots

MCNP6 can plot photonuclear data in addition to the photoatomic data of
MCNP6. A list of the special reaction numbers available in the MCNP code
(in addition to the standard ENDF reaction numbers found in the ENDF-6
manual [45]) is in Table 5.19. For photonuclear reactions with R &gt; 4 ,
refer to the list of standard ENDF reaction numbers.

The photonuclear yields (multiplicities) for various secondary particles
are specified by adding 1000 times the secondary particle number to the
reaction number. For example, 31,001 is the total yield of deuterons
(particle type D = 31 ), 34,001 is the total yield of alphas (particle
type α = 34 ), and 1018 is the total number of neutrons (particle type N
= 1 ) from fission.

The example input in Listing 6.5 shows a basic input that photoatomic
and photonuclear cross sections can be plotted from.

```
1 photonuclear and photoatomic cross section plotting example 2 1 100 -1 -1 imp:n=1 3 2 0 1 imp:n=0 4 5 1 so 10 6 7 m100 82208 1 6012 1 8 pnlib=24u 9 plib=84p 10 c 11 c Turn on photonuclear physics 12 phys:p 3j -1 13 mode p n 14 sdef par=p
```

Listing 6.5: example\_photonuclear\_photoatomic\_plotting.mcnp.inp.txt

When the file is run with the mcnp6 ixz execution line, the code
processes the cross sections and calls the MCPLOT module. The user is
presented with the MCPLOT&gt; prompt.

To find out which reactions are available for a particular nuclide or
material, enter an invalid reaction number with the MT command, followed
by the XS command and the nuclide or material of interest. For example,
determining the allowed photonuclear reactions and available yields for
carbon-12 is accomplished with:

```
1 mt 99 xs 6012.24u
```

The resulting output is shown in Listing 6.6.

```
1 mcplot> 2 mt 99 xs 6012.24u 3 setting particle type to p 4 5 no data found for reaction 99 6 7 6012.24u allowable reactions: 8 1 2 3 4 5 50 600 9 1001 1004 1005 1050 2001 2004 2005 9001 9004 9005 10 9600 31001 31004 31005 34001 34004 34005
```

Listing 6.6: Console Output For Requesting Photonuclear MT=99 on Carbon-12

The console output shows the reaction numbers in Table 5.19 in addition
to numbers 5, 50, and 600, plus a series of yields. To determine the
meaning of the non-yield numbers, the ENDF-6 manual should be
referenced. There, we find that 5 is a catchall for reactions not
defined by other MT numbers, 50 is the production of a neutron, leaving
the residual nucleus in the ground state, and 600 is the production of a
proton, leaving the residual nucleus in the ground state.

We can plot the total photonuclear cross sections for the carbon, lead,
and material 100 with the following command:

```
1 xlim 5 200 ylim 1e-5 1 mt 1 xs 6012.24u cop mt 1 xs 82208.24u cop mt 1 xs m100
```

This command first sets the x and y -axis limits to a convenient value,
then coplots the total photonuclear cross sections of each table along
with the total material which results in the plot shown in Figure 6.13.

Entering a bad table identifier with the XS command (i.e., 12345.67u),
will cause MCNP6 to list the available nuclides and library suffixes
which can inform the user of the availability of other data to plot. In
this example, the .00c and .84p data are both available, and their cross
sections, along with the total material cross section can be plotted
with:

```
ylim 1e-1 1e7 mt -5 xs 6000.84p cop mt -5 xs 82000.84p cop mt -5 xs
```

Which results in Figure 6.14.

## 6.4.6 Weight-Window-generator Superimposed Mesh Plots

MCNP6 can plot the WWG superimposed mesh specified on the MESH card in
an input file. In the MCNP6 interactive geometry plotter, toggle
CellLine in the left-hand controls (§6.2.3.2) for the following options:

```
CellLine Plot constructive solid geometry cells, outlined in black. (DEFAULT) No Lines Plot cells not outlined in black.
```

```
m100
```

1

Figure 6.13: Photonuclear cross-section plot.

<!-- image -->

Cross Section Plot

Total Photon Cross Section

<!-- image -->

Energy (MeV)

Figure 6.14: Photoatomic cross-section plot.

10

11

12

13

14

1

2

3

4

1

| WW MESH   | Plot weight-window superimposed mesh without cell outlines.   |
|-----------|---------------------------------------------------------------|
| WW+Cell   | Plot weight-window superimposed mesh and cell outlines.       |
| WWG MESH  | Plot weight-window generator mesh.                            |
| WWG+Cell  | Plot weight-window generator mesh and cell outlines.          |
| MeshTaly  | Plot TMESH mesh tally boundaries.                             |

The CellLine and No Lines options are always available. WW MESH and
WW+Cell are available only when the WWP card calls for using a
superimposed weight-window mesh (5th entry negative) and a WWINP file is
provided. WWG MESH and WWG+Cell are available only when a MESH card
appears in the input and when the WWG card requests superimposed mesh
generation (2nd entry is 0). MeshTaly and MT+Cell are available only
when a TMESH mesh tally has been requested.

## 6.4.6.1 Cylindrical Mesh Example

One can generate a plot using the MCNP input file in Listing 6.7 and the
interactive plotter command input file in Listing 6.8 with the execution
line:

```
1 mcnp6 i=example _ cylindrical _ mesh.mcnp.inp.txt com=example _ cylindrical _ mesh.mcnp.comin.txt ip
```

Listing 6.7: example\_cylindrical\_mesh.mcnp.inp.txt

```
1 Demonstration of WWG Plot 2 1 1 1.0 -1 imp:p 1 3 2 0 1 imp:p 0 4 5 1 rcc 0 0 0 0 10 0 5 6 7 mode p 8 sdef sur 1.3 vec 0 1 0 dir 1 erg 100 9 m1 1001 2 8016 1 nps 1000 f1:p 1.2 wwg 1 0 mesh geom=cyl origin=0 -1 0 ref=0 .1 0 axs=0 1 0 vec=1 0 0 imesh 6 iints 7 jmesh 12 jints 7 kmesh 1 kints 3
```

Listing 6.8: example\_cylindrical\_mesh.mcnp.comin.txt

```
ex 10 lab 0 0 px 0 mesh 4 pause py 5 pause
```

Or, instead of using the command file (with plot commands in command
mode), the interactive plotter can be used:

```
mcnp6 i=example _ cylindrical _ mesh.mcnp.inp.txt ip
```

Figure 6.15: WWG mesh plot, axial view.

<!-- image -->

The superimposed mesh can displayed with the following sequence:

1. Click the CellLine button in the lower left-hand control box twice to get WWG+Cell
2. Click the L1 sur button once to turn off surface labels
3. Click XY to get the view equivalent to px = 0 (axial view, Fig. 6.15)
4. Click '10' on the Zoom bar twice to get a 10 times magnification at the origin
5. Click Origin then click in the center of the mesh to center the geometry in the plotter window
6. (a) The origin information in the top left of the plotter should show approximately (0 , 5 , 0)
6. Click ZX to get a view approximately equivalent to py = 5 (radial view, Fig. 6.16)

## 6.4.6.2 Spherical Mesh Example With Weight Windows

The spherical mesh geometry may be thought of as a globe where the phi (
ϕ ) polar angles are latitude and the theta ( θ ) azimuthal angles are
longitude. The north pole is at ϕ = 0 ◦ ; the south pole is at ϕ = 180 ◦
; Greenwich (near London) is at θ = 0 ◦ and all the way around the globe
at θ = 360 ◦ .

The interface for geometry plots of the spherical mesh window boundaries
is the same as for cylindrical mesh boundaries. An example input
(Listing 6.9) and associated WWINP file (Listing 6.10) are given and are
attached to this document.

Figure 6.16: WWG mesh plot, radial view.

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

```
1 Demonstration of Spherical WW Mesh Plot 2 1 1 1.0 -1 imp:p=1 3 2 0 1 imp:p=0 4 5 1 so 10 6 7 mode p 8 sdef erg=5 9 m1 1001 2 8016 1 10 nps 1000 11 f1:p 1 12 wwp:p 4j -1 13 c The lines below are used to generate the WWINP file with the wwp card commented out. 14 c wwg 1 0 15 c mesh geom=sph ref=0 0 0 origin=0 0 0 16 c axs=0 0 1 $ Reference vector for the polar axis 17 c vec=1 0 0 $ Reference vector for the azimuthal axis 18 c imesh 3 7.5 10 $ Radii of the mesh, cm 19 c jmesh 36 126 180 $ Polar angles (phi), implicit 0 lower bound 20 c kmesh 72 306 360 $ Azimuthal angles (theta), implicit 0 lower bound
```

Listing 6.9: example\_spherical\_mesh.mcnp.inp.txt

Listing 6.10: example\_spherical\_mesh.mcnp.wwinp.txt

<!-- image -->

|         1 | 1       | 2           | 16      | 07/14/22 12:19:24   | 07/14/22 12:19:24   |
|-----------|---------|-------------|---------|---------------------|---------------------|
|   0       | 1       |             |         |                     |                     |
|   3       | 3.0000  | 3.0000      | 0.0000  | 0.0000              | 0.0000              |
|   3       | 3.0000  | 3.0000      | 0.0000  | 0.0000              | 10.000              |
|  10       | 0.0000  | 0.0000      | 3.0000  |                     |                     |
|   0       | 1.0000  | 3.0000      | 1.0000  | 1.0000              | 7.5000              |
|   1       | 1.0000  | 10.000      | 1.0000  |                     |                     |
|   0       | 1.0000  | 0.10000     | 1.0000  | 1.0000              | 0.35000             |
|   1       | 1.0000  | 0.50000     | 1.0000  |                     |                     |
|   0       | 1.0000  | 0.20000     | 1.0000  | 1.0000              | 0.85000             |
|   1       | 1.0000  | 1.0000      | 1.0000  |                     |                     |
| 100       |         |             |         |                     |                     |
|   0.5     | 0.32667 | 0.94444E-01 | 0.28333 | 0.18519             | 0.68571E-01         |
|   0.59048 | 0.32500 | 0.77778E-01 | 0.37500 | 0.32500             | 0.11481             |
|   0.20523 | 0.16637 | 0.62500E-01 | 0.25648 | 0.17368             | 0.59459E-01         |
|   0.55833 | 0.35833 | 0.10833     | 0.24815 | 0.17976             | 0.90909E-01         |
|   0.63333 | 0.40667 | 0.79167E-01 |         |                     |                     |

To see these weight windows, first run the following MCNP6 execution
line:

```
1 mcnp6 i=example _ spherical _ mesh.mcnp.inp.txt wwinp=example _ spherical _ mesh.mcnp.wwinp.txt ip
```

This will load the familiar geometry plotter. The view in Figure 6.17,
which is looking down the polar axis (in this case, the global z -axis)
is achieved through the following steps:

1. Click the CellLine button twice so that WW+Cell shows.
2. Click the L1 sur button once so it reads L1 off .
3. Click the wwn button on the right-hand bar, then COLOR twice so it reads COLOR wwn1:p .
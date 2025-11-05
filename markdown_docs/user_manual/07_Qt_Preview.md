---
title: "Chapter 7 - Technology Preview Qt Based MCNP Geometry and Tally"
chapter: "7"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/7_Technology_Preview_Qt_Based_MCNP_Geometry_and_Ta.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Chapter 7

## Technology Preview: Qt Based MCNP Geometry and Tally Plotting

With this version of the MCNP6 code we are bundling a preview of our
next-generation Qt Framework based plotter that enables visualization of
2-D slices of the geometry. Depending on how the preview plotter
(henceforth referred to as the plotter) is invoked, these slices can be
overlaid with spatial tally results or display graphs of the standard
tallies. It is expected that in a future release of the MCNP6 code this
plotter will replace the current plotter described in the previous
chapter [§6]. With this new Qt-based plotter the MCNP6 code will run as
a native app any time the plotter is invoked - using X-windows on linux
and the native OS infrastructure on Windows and macOS. As a result, the
MCNP code can run and display graphics on the local machine with no
special software install required.

It is expected that the plotter will primarily be used to verify the
geometry before starting transport and to peruse the results after
transport is done since this does not require using any additional
tools. For deeper data exploration and advanced visualization our
recommended path is to use the HDF5/XDMF capability described in §D.4.3
in conjunction with a dedicated visualization package such as ParaView
[326].

In addition to the capabilities described in this chapter, the plotter
can also be invoked in a mode that displays the cross sections of
nuclear data loaded for the run. The invocation and the commands allowed
are identical to those described elsewhere [§6.3.3.8], so the cross-
section mode is not described here. Note that:

## Details:

- 1 All keyboard input to the plotter should be followed by the Enter key for the plotter to act on them. For brevity we have omitted this repetitive piece of information in the text. Hence, when the manual directs the user to type a command in the Input Pane, it is explicitly assumed that the user will follow that command by hitting the Enter key to execute it.
- 2 Plotter keyboard entry is case insensitive, so PLOT is the same as plot which is the same as pLoT . For clarity, we have used uppercase for the text entry keywords in this chapter.
- 3 All graphical capabilities of the plotter can be controlled via keyboard input in the Input Pane. For large, complex geometries it is recommended to use the plotter in batch mode ( NOTEK option, §7.1.2) with the SAVEPDF command to generate the image.

## 7.1 Viewing Geometry

The plotter renders 2-D slices of the geometry with the capability to
overlay the slice with FMESH and TMESH tally results loaded from a
runtape file [§D.2]. The user also has the option to graph other tally
data within the runtape file. Figure 7.1 shows the interface that the
plotter presents when invoked in Geometry

Figure 7.1: Overlay showing the four panes of the Plotter: the Viewport Pane which displays the rendered slice, the Control Pane which provides controls for manipulating the view, the Information Pane which displays the current view information and details of the cell clicked, and the Input pane where command line input can be entered. These panes are described in §7.3.

<!-- image -->

Viewing mode. The plotter interface has four distinct panes that are hi-
lighted. These are the Viewport Pane [§7.3.1], the Control Pane
[§7.3.2], the Information Pane [§7.3.3], and the Input Pane [§7.3.4].
The user interacts with the plotter using graphical controls present in
these panes. When viewing geometries, the view can be changed using
either the mouse in the Viewport Pane, the controls in the Control Pane,
or keyboard input in the Input Pane. For example, once a slice has been
rendered by the plotter, the Viewport Pane displays the rendered image
and enables mouse-based interaction for translation, rotation, and zoom.
Left-clicking in the Viewport Pane will display information about the
clicked cell in the Information Pane. The Control Pane enables direct
access to frequently used operations for both the view and the rendered
quantities. The Information Pane displays the current view details and
information on the last cell clicked. The Input Pane allows the user to
input text commands to control the view rendered.

## 7.1.1 Geometry Specification

To plot a 2-D slice of geometry, one needs to specify the plane to be
plotted, the orientation of the geometry within that plane, and the
extents of the plane that are visible in the slice. The plotter enables
this through use of three concepts: BASIS vectors, ORIGIN at the center
of the Viewport Pane, and EXTENT of space visible

1

1

within the Viewport Pane. The first of these keywords, BASIS , defines
the orientation within the Viewport Pane by specifying the horizontal
and vertical directions. The normal direction is computed as the cross
product of these two bases. Specifying the basis vectors orients the
geometry, but does not identify where the slice is located along the
normal direction. This is done by specifying the ORIGIN , which
identifies the point in space that is at the center of the Viewport Pane
irrespective of the BASIS selected. The combination of the BASIS and
ORIGIN uniquely determines the plane to be plotted. The EXTENT concept
limits how much of the plane is visible in the horizontal and vertical
directions. Together these three concepts completely specify the slice
to be rendered.

The plotter uses these three concepts to render geometry. In the current
implementation the plotter does not limit the basis to orthogonal
vectors but it does require that they not be collinear. If the basis
vectors specified are not perpendicular to each other, then the
horizontal direction is set to the first basis and the normal direction
is computed using the cross product of the two basis vectors. The
vertical direction is then determined from the horizontal direction and
the normal. The plotter also does not constrain the extent in the
horizontal and vertical direction to be the same. This enables the user
to stretch the view in a given direction to tease out details in highly
asymmetric structures. The basis and origin are specified in real-world
coordinates whereas the extents are relative to the origin. So, for
example, if the origin is specified as ( x, y, z ) , the point at the
center of the Viewport Pane will be set to this, irrespective of the
basis vectors selected. The extent command is then interpreted as
distance along the horizontal and vertical bases, so the point at the
bottom right of the Viewport Pane would then be ( x, y, z ) + e hor × (
b 1 x , b 1 y , b 1 z ) -e vert × ( b 2 x , b 2 y , b 2 z ) , where b 1
is the unit vector in the horizontal direction, b 2 is the unit vector
in the vertical direction, and e hor and e vert are the extents in the
horizontal and vertical direction respectively.

The next few sections describe how the plotter provides access to these
concepts to plot different slices through the geometry defined in the
input.

## 7.1.2 Launching The Plotter

The plotter is launched in geometry/tally mode using either an MCNP6
input file (with or without an associated runtape) or with just a
runtape file by using one of the following two methods at the shell
command prompt:

mcnp6 \_ preview IP INP=filename [KEYWORD=value(s)]

or mcnp6 \_ preview Z RUNTPE=filename.h5 [KEYWORD=value(s)]

The first line with the IP option will initialize the geometry from the
input file specified by the INP keyword, perform the normal input
checks, and display the geometry. In this launch mode, if a runtape file
is specified using the RUNTPE keyword, tallies will be read in from that
file. The initial view in this mode of invocation is looking down the x
axis with the z axis along the horizontal direction, the y axis along
the vertical direction, origin set to (0 , 0 , 0) , and with extents of
± 100 in each direction.

The second line, invoked with the Z option, is useful once transport has
been run and a runtape file has been generated. In this case the plotter
initializes the geometry and tally data from the runtape file provided
and presents a view of the first tally specified in the file. The window
presented has a keyboard Input Pane at the bottom left and a view of the
tally in the body.

1

The plotter provides the capability to switch seamlessly between these
two views of the data. To switch from the geometry view to the tally
view, the user types MCPLOT in the Input Pane, and to switch in the
other direction, the user types PLOT in the Input Pane. Note that in
Geometry View mode, if a runtape has not been specified, the MCPLOT
command is ignored. An example of the two views displayed by launching
the plotter in Geometry/Tally mode using the above two lines is shown in
Fig. 7.2.

We recommend launching with the IP option to verify the geometry before
running transport, especially with complicated geometries. The time that
is required to plot and verify the geometry model is small compared with
the potential time lost working with an erroneous geometry. See §7.1.5
for hints on debugging geometries.

The keywords allowed at the command line during launch are:

| RUNTPE = filename   | Name of the runtape that holds the tally data. When the plotter is invoked with IP , the user can optionally provide a runtape using the RUNTPE keyword either at the command line or in the Input Pane after launching. If the plotter is launched with Z , then this keyword is required at the command line.                                                                                                                              |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| COM = filename      | Execute plotter commands within filename upon startup. When an end-of-file (EOF) is read, control is transferred to the plotter. In a production or batch situation, end the file with an END command to prevent transfer of control. Never end the COM file with a blank line. If COM is absent, the plotter starts up in interactive mode.                                                                                                 |
| PLOTM = filename    | Prefix for PDF/PS/PNG files. If this is not specified, the plotter will select a unique filename prefix to avoid overwriting existing files. When commands SAVEPDF or SAVEPNG are executed, the PDF and PNG files with the current view will be saved as PLOTM _ #####.PDF or PLOTM _ #####.PNG with the index incremented with every invocation. If the command SAVEPS is executed, the plotter will add a page to the file PLOTM _ qt.PS . |
| COMOUT = filename   | Write all plotter commands to file filename . The default name is comout . This output file can be used at a later time to regenerate the views of the current session by using all or part of the old COMOUT file as the COM file in the second run. Unique names for the output file, COMOUT, will be chosen by MCNP6 to avoid overwriting existing files.                                                                                 |
| NOTEK               | Specifies off-screen rendering without displaying any windows. This is useful when running in batch mode or remotely over a slow network. The user can change the views using the keyboard commands in §7.1.6, and save the resulting view with one of SAVEPDF , SAVEPNG , or SAVEPS to save PDF, PNG, or PS files respectively.                                                                                                             |

To recreate Fig. 7.2a, launch the plotter with the following command
mcnp6 \_ preview ip inp=tech \_ preview \_ plotter.mcnp.txt

The user can change the view from the default (Fig. 7.2a) by typing
BASIS 0 1 0 0 0 1 ORIGIN 1 1 1 EXTENT 15 15 LABEL 1 0 in the Input Pane.
This command sets the basis vectors to the y and z axes and the normal
to the x axis. The origin is selected as 1 , 1 , 1 and the extents of
the viewport are then set to origin ± 15 in the horizontal and vertical
directions. The label command turns on surface labels and turns off the
cell labels. The input used here can be found in program Listing 7.1.

The user can also change the view by using the mouse in the Viewport
Pane [§7.3.1], the controls in the Control Pane [§7.3.2] or by entering
commands from Table §7.1.6 in the Input Pane. A command consists of a
keyword typically followed by some parameters. Multiple keywords and
their parameters can be entered on

(a) Initial geometry view [§7.1]

<!-- image -->

(b) Initial tally view [§7.2]

<!-- image -->

Figure 7.2: Initial views displayed when launching the plotter with
either IP or Z specified at command line. In geometry mode, a default
view of the geometry is provided with an x axis normal, origin at (0 , 0
, 0) , and extents of ± 100 . In tally mode, the first tally from the
results is displayed.

each line. Keywords and parameters are space-delimited. Keywords can be
shortened to any degree as long as they are not ambiguous. Parameters
following the keywords cannot be abbreviated. Numbers can be entered in
free-form format and do not require a decimal point for floating point
data. Keywords and parameters remain in effect until changed. Note: if a
shortened, ambiguous keyword is used, the entire command line from that
point on will be rejected and a message to that effect will be printed
to the terminal. The most common keywords are represented in the Control
Pane in the form of buttons and menus. These can be used to change the
rendered slice as well. For example, to color the cells by their IDs,
the user selects Cell from the Color menu. Similarly the user can toggle
the display of surface labels by clicking the Surface ID checkbox, and
select a label for all the cells by selecting an item from the Cell
Label menu.

## /warning\_sign Caution

Placing the plot plane exactly on a surface defined by the geometry can
stall the geometry engine.

If the view plane selected is coincident with a surface defined by the
geometry, undefined behavior can occur, and performance can drop
significantly. For example, if the input geometry has a PX plane at x =
0 , that plane coincides with the default plot plane. When this occurs,
some portion of the geometry may be displayed in dotted lines, which
usually indicates a geometry error or part of the geometry may simply
not show up at all. Very infrequently the code may crash with an error.
To prevent all these unpleasantries, move the plot plane a tiny amount
away from surfaces.

## 7.1.3 Saving the View

A PDF file is saved by clicking the Save PDF button or typing SAVEPDF in
the Input Pane. To save PNG or PS files, the user would type SAVEPNG and
SAVEPS respectively in the Input Pane. Each of the three commands
SAVEPDF , SAVEPNG , and SAVEPS saves the current view. If the user
enters other commands on the same line, e.g. ORIGIN 20 1 0 SAVEPS EX 10
10 , then the origin would first be set to (20 , 1 , 0) and then the
view would be saved to the PS file. Then the extents would be changed.
Although the button to save PDF files is not visible in all modes, the
keyboard commands are available anytime the Input Pane is visible.

## 7.1.4 Plotting Embedded-mesh Geometries

The plotter supports color-shaded plotting of the materials, mass
density, or number density of an imported embedded mesh. For these cases
the values from the external mesh geometry file (typically a LNK3DNT or
Abaqus-style file) are used; these values may vary element to element.

For mass density ( den ) and number density ( rho ) plots, each element
will be shown in one solid color. The element net value is displayed,
i.e., the net mass density or net number density of the element. The
color distribution is set by the minima and maxima. These net values are
also the values reported in the Information Pane when a cell is clicked.

For material plots, multi-material zones may appear striped as the color
to plot is chosen randomly based on the material mass fraction. This
means that redrawing a color-bymat plot may give a slightly different
striping. For example, in a two-material element with a 50/50 mass-
fraction mix, approximately 50/50 color striping will display
horizontally. If Material is selected from the Color menu, clicking on a
spot containing multiple materials will randomly select which material
to report. Repeated clicking on such a spot may show different materials
on different clicks. Void elements in the mesh are not shaded (i.e.,
shown as white) on material plots.

## 7.1.5 Geometry Debugging

Surfaces appearing on a plot as red dashed lines usually indicate that
adjoining space is improperly defined. Dashed lines caused by a geometry
error can indicate space that has been defined in more than one cell or
space that has never been defined. These geometry errors need to be
corrected. Dashed lines also can occur because the plot plane
corresponds to a bounding planar surface. The plot plane should be moved
so it is not coincident with a problem surface. Dashed lines can
indicate a cookie cutter cell or a DXTRAN sphere. These are not errors.
The reason for the presence of dashed lines on an MCNP6 plot should be
understood before running a problem. When checking a geometry model,
errors may not appear on the two-dimensional slice chosen, but one or
more particles will get lost in tracking. To find the modeling error,
use the coordinates and trajectory of the particle when it got lost.
Entering the particle coordinates as the ORIGIN and the particle
trajectory as the first basis vector will result in a plot displaying
the problem space.

## 7.1.6 Keyboard Commands In Geometry View

In addition to mouse manipulation described in the section on Navigating
The Plotter [§7.3], the view can be changed using a number of keyboard
commands. We list here the different keyboard commands that can be
issued. All keyboard input to the plotter should be followed by the
Enter key for the plotter to act on them. For brevity we have omitted
this repetitive piece of information in the text. Hence, when the manual
directs the user to type a command in the Input Pane, it is explicitly
assumed that the user will follow that command by hitting the Enter key
to execute it.

<!-- image -->

## BASIS b1x b1y b1z b2x b2y b2z

Specify the basis vectors for the horizontal and vertical axes of the
Viewport Pane as triples of xyz for each of the vectors. The vectors
need not be orthogonal, but must not be collinear. The plotter will
normalize the vectors to unit vectors, determine an orthogonal basis and
display the orthogonal basis in the Information Pane.

Translate the center of the viewport by dh along the horizontal basis
and dv along the vertical basis

Turns filling of cells on or off, or change coloring parameters based on
command . Valid Entries for command are:

| ON          | Turn filling of cells on                                                                                                                    |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| OFF         | Turns off filling of cells                                                                                                                  |
| [50-5000]   | Set resolution of shape decomposition, with 5000 represent- ing the highest resolution (smoothest curves) gained at the cost of performance |
| BY CEL      | Color by Cell IDs                                                                                                                           |
| BY DEN      | Color by mass density                                                                                                                       |
| BY GRADIENT | Use a 256 color palette to display values                                                                                                   |
| BY MAT      | Color by material (default). See also SHADE command                                                                                         |
| BY RHO      | Color by atomic density                                                                                                                     |
| BY SOLID    | Use a solid color to represent values                                                                                                       |
| BY TMP      | Color by temperature                                                                                                                        |

Ends the current plotter session

Sets the extents of current view. If only ex is specified, ey is set
equal to ex

CENTER dh dv

COLOR command

END

EXTENT ex [ey]

| EBIN n     | Select Energy Bin n to display when an FMESH is active                                                                                                                                                                                                                                                                                                                                     |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FACTOR f   | Scale the plot by a factor of f i.e. zoom by 1/f                                                                                                                                                                                                                                                                                                                                           |
| FLINES 0|1 | If an FMESH is active, turn on or off drawing the outlines of the FMESH cells                                                                                                                                                                                                                                                                                                              |
| FMESH ID   | If no runtape file has been read in, displays the outline of the FMESH grid with the specified ID defined in the input. If a runtape has been read in using either the RUNTPE command or as a command line argument, display the values of the selected Energy and Time bin tallies superimposed on the geometry. If ID is set to OFF , revert to filling the geometry by material number. |

HELP

print available commands to the terminal window

## LABEL slabel [clabel [par]]

Put labels of size slabel on the surfaces and, optionally, labels of
size clabel in the cells. The parameter, par , following clabel is
further optional and defaults to MAT . The sizes specified by slabel and
clabel are relative to 0.01 times the height of the view window. If
slabel or clabel is zero, that kind of label will be omitted. The
allowed range of sizes for the labels is [0.2-100]. In case Cell labels
are set to on, The cell label is selected by providing one of the
following entries:

| CEL     | cell ID                                                                   |
|---------|---------------------------------------------------------------------------|
| DEN     | mass density                                                              |
| DXC: P  | DXTRAN contribution by particle type                                      |
| EXT: P  | Exponential transform by particle type                                    |
| FCL: P  | Forced collision by particle type                                         |
| FILL    | Filling Universe                                                          |
| IJK     | Lattice indices of repeated structure/lattice geometries                  |
| IMP: P  | Importance by particle type                                               |
| LAT     | Lattice type                                                              |
| MAS     | Mass                                                                      |
| MAT     | Material number                                                           |
| NONU    | Fission turnoff                                                           |
| PDn     | Detector contribution ( n = tally number)                                 |
| TMPn    | Temperature ( n = index of time)                                          |
| U       | Universe number                                                           |
| WWNn: P | Weight-window lower bound ( n = energy or time interval) by particle type |

| LEVEL n      | Plot only the n th level of repeated structure geometries                                                                                   |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| MBODY on|off | Display macrobody surface number in addition to surface labels. Only available if surface labels are set to on.                             |
| MCPLOT       | Switch the view to tally viewing. If no RUNTPE has been read in, this command does nothing.                                                 |
| MESH n       | Controls plotting of the weight-window, weight-window generator, FMESH , and TMESH superimposed structured mesh. The valid values of n are: |
|              | 0 No lines on plot                                                                                                                          |
|              | 1 Geometry cell outlines                                                                                                                    |

|   2 | Weight-window mesh outlines                           |
|-----|-------------------------------------------------------|
|   3 | Weight-window mesh + geometry cell outlines           |
|   4 | Weight-window generator mesh outlines                 |
|   5 | Weight-window generator mesh + geometry cell outlines |
|   6 | TMESH Tally outlines                                  |
|   7 | TMESH Tally outlines + geometry cell outlines         |
|   8 | FMESH Tally outlines                                  |
|   9 | FMESH Tally outlines + geometry cell outlines         |

## MYMACROS add|load|save|remove|addCurrentView

See §7.3.2.2 for details

| ORIGIN ox oy oz   | Sets origin for the Viewport Pane                                                                                                                                                                                                                                           |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PX vx             | Set the x coordinate of the origin to vx and set the view to point down the x axis. This is equivalent to the command BASIS 010001 ORIGIN vx vy vz , where vy and vz are the current y and z coordinates of the origin.                                                     |
| PY vy             | Set the y coordinate of the origin to vy and set the view to point down the y axis. This is equivalent to the command BASIS 001100 ORIGIN vx vy vz , where vx and vz are the current x and z coordinates of the origin.                                                     |
| PZ vz             | Set the z coordinate of the origin to vz and set the view to point down the z axis. This is equivalent to the command BASIS 100010 ORIGIN vx vy vz , where vx and vy are the current x and y coordinates of the origin.                                                     |
| RUNTPE filename   | Read in tallies from the specified runtape. This command can also be used to load up a runtape file from a different run with the constraint that the geometries in the two files must be identical. If the geometries do not match, the plotter will fail with a SIGSEGV . |
| SAVEPDF           | Saves current Viewport and Information panes to a PDF file                                                                                                                                                                                                                  |
| SAVEPNG           | Saves current Viewport and Information panes to a PNG file                                                                                                                                                                                                                  |
| SAVEPS            | Saves current Viewport and Information panes to a legacy postscript file                                                                                                                                                                                                    |
| SCALES 0|1|2      | Specify whether the extents ruler and grid are drawn on the viewport: 0 turns off ruler and grid, 1 draws the ruler, and 2 draws both ruler and grid.                                                                                                                       |

## SHADE m1=value1 m2=value2 ...

This command is only valid when COLOR by mat is in effect. This sets the
shade for material m1 to value1 , and so on, where values are integers
in the range [1-64]. Alternately, values could be specified as colors
(e.g. red, blue, green, etc.). Color names are case sensitive. The
command options will list available color values. Indices in the list
run from top left to bottom right.

| STATUS   | Print currently selected plot options to the terminal                                                                               |
|----------|-------------------------------------------------------------------------------------------------------------------------------------|
| TBIN n   | Select time bin to display when an FMESH is active                                                                                  |
| THETA θ  | Rotates the plot by θ degrees counterclockwise around the center of current view.                                                   |
| TMESH ID | If a RUNTPE has been read in then the plotter colors are the TMESH cells by the tally values and superimposes them on the geometry. |

1

## 7.2 Viewing Tally Results

Although visualizing the geometry is extremely useful, oftentimes one
would like to take a look at the results of a run. To do this run the
MCNP code with mcnp6 \_ preview i= tech \_ preview \_ plotter.mcnp.txt n=
preview \_ 1 which creates the runtape file preview \_ 1r.h5 . The results
are then visualized using the command:

mcnp6 \_ preview Z RUNTPE= preview \_ 1r.h5 [keyword=value]

This will generate Fig. 7.2b. The Z argument to the plotter reads in the
geometry and the results from the runtape file specified by the RUNTPE
argument. In this mode one can graph the different tallies specified in
the input file/runtape file. The default view shows the lowest numbered
tally on a log-lin scale with energy on the x axis and tally value on
the y axis. Typing PRINTAL in the Input Pane at the bottom of the window
will print out the tallies available in the terminal window. For this
file, there are two tallies: 1 and 21 . To switch between them type the
commands TALLY 1 and TALLY 21 .

An alternate way to visualize the tally results is to launch with the IP
option, as in §7.1, specifying a runtape file either on the command line
or in the Input Pane with RUNTPE= &lt;filename&gt; , and then typing MCPLOT in
the Input Pane.

Except when viewing FMESH and TMESH tallies, the Tally Viewing mode is
driven by command line input in the bottom left.

## 7.2.1 Plotting Standard (F) Tally Results

The standard tallies in the MCNP code specified using the F cards are
stored as 8-dimensional arrays. Not surprisingly, plotting 8-D objects
is beyond the current capabilities of the plotter. Instead the plotter
allows the user to display 2-D projections of this 8-D space. The
simplest of these views displays one of the dimensions along the x axis
and the corresponding tally values on the y axis. The default view is
such an example. It displays the tally particles as a function of energy
on a log-linear scale. The axes can be switched between log and linear
by using the command &lt;x-mode&gt;&lt;y-mode&gt; where &lt;x-mode&gt; and &lt;y-mode&gt; are
either LOG or LIN . So to switch to a log-linear scale the user would
type LOGLIN resulting in the image shown in Fig. 7.3. Similarly to
switch to a log-log scale, the user would enter LOGLOG in the Input Pane
and so on. Plotting tallies in the MCNP code is described in detail in
§6.3, §6.4, and §6.5. The user is directed to those chapters for the
commands available since the new plotter provides identical
capabilities.

## 7.2.2 Viewing FMESH And TMESH Superimposed Mesh Tallies

When a runtape file is loaded, FMESH and TMESH tally results within the
file can be superimposed on the geometry. Available tallies are
enumerated in the Color menu. To view FMESH tally results the user must
first switch to the geometry view by typing PLOT . Then the user can
select the FMESH 14 menu item from the Color menu in the control pane.
When an FMESH is selected, the entries FMESH and FMESH + Cell Boundary
are enabled in the Lines menu enabling the user to draw the mesh and
geometry outlines superimposed on the tally results. The first time an
FMESH is selected, the view is auto-adjusted to change orientation and
scale to show the entire mesh. For rectangular meshes, the horizontal
axis is in the direction of the dimension with the greatest number of
bins, and the vertical axis is in the direction of the dimension with
the second greatest number of bins. For cylindrical meshes, the
horizontal axis is along the axis of the cylinder and the vertical axis
is along the θ = 0 plane. The center of the plot in both cases is at the
center of the mesh. In

Figure 7.3: Energy tally plotted on a log-linear scale. This is achieved by typing LOGLIN in the Input Pane when the tally is displayed. The ability to switch the axes between log and linear mode is available any time a tally chart is displayed by entering the command &lt;x-mode&gt;&lt;y-mode&gt; where &lt;x-mode&gt; and &lt;y-mode&gt; are one of LOG and LIN for log and linear mode respectively.

<!-- image -->

Figure 7.4: Results from a short calculation showing tallies on an FMESH. In this view, time bin 4 and energy bin 2 are selected for FMESH 14. FMESH cell (8 , 9 , 9) has been clicked and is indicated by the cross-hair with the yellow halo in the image.

<!-- image -->

this case, the default FMESH view results in a cartesian mesh centered
at (0 , 0 , 0) with a dimension of 150 in each direction. To display
this FMESH , the view is first rotated so that the z axis is the normal,
with the x axis along the horizontal direction. Then the extents for the
view are reset to ± 75 . This is shown in 7.4.

To select the TMESH 111 that is defined in the input, the user would
either enter TMESH 111 in the Input Pane or select TMESH 111 from the
Color menu. As with FMESH tallies, when a TMESH is selected, the entries
Mesh Tally and Mesh Tally + Cell are enabled in the Lines menu enabling
the user to draw the mesh and geometry outlines superimposed on the
tally results. This is shown in 7.5.

## 7.3 Navigating the Plotter

## 7.3.1 Viewport Pane

The user interacts with the Viewport using the mouse to interrogate,
translate, rotate, and zoom the scene displayed. Left-clicking on a cell
in the viewport will display additional information in the Information
Pane. Left-clicking the mouse and dragging the rendered image around
will dynamically change the origin for the

Figure 7.5: Results from a short calculation showing tallies on a TMESH. In this view, TMESH 111 is selected from the Color menu.

<!-- image -->

Figure 7.6: Control Pane of graphical interface annotated with functions of the different elements.

<!-- image -->

plot and translate the view. If the Shift ⇑ key pressed when the mouse
button is depressed, then dragging will rotate the basis vectors around
the center of the Viewport. If the Ctrl key pressed when the mouse
button is depressed, dragging the mouse will zoom the rendered view
around the point where the mouse was pressed proportional to the
vertical displacement of the mouse from the original point. In the zoom
mode the origin is dynamically shifted so as to keep the originally
clicked point stationary within the Viewport.

The rendered view can also be shifted by using a combination of the Ctrl
and the four arrow keys ← , → , ↑ , ↓ to translate the view left, right,
up, or down respectively. Zooming around the origin is achieved by using
Ctrl + / Ctrl -. Keeping the Shift ⇑ key pressed with these combinations
will increase the magnitude of the change. Note that on Macintosh
computers the Ctrl key will be mapped to the Command key. This is
because the default key bindings on macOS use the Ctrl key to navigate
different desktops.

The EXTENT , ORIGIN and THETA commands from the listing in §7.1.6 enable
the user to emulate the results of mouse based view control. There are
no keyboard equivalents for the selection of a cell by mouse click.

The End button at the bottom right of the Viewport Pane will exit the
plotter. The status bar to the left of the End button provides hints
regarding the state of the plotter driver when it is executing a command
in the background, such as when plotting a complex geometry which can
cause the interface to become non-responsive while the rendered view is
being calculated.

## 7.3.2 Control Pane

The Control pane is the set of buttons, checkboxes, and menus shown in
Fig. 7.1. An annotated view is shown in Fig. 7.6 and a description of
the elements is given in §7.3.2.1. These graphical elements are
enabled/disabled

depending on the features present in the input file. The contents of
menus change dynamically based on input. All menus in this interface can
be 'torn off' making it easier to navigate auto-populated menu items
that the user might want to switch between. Except for Tips, all other
Control Pane actions can be emulated using keyboard input.

## 7.3.2.1 Control Pane Elements

The following elements are components within the Control Pane. If a
command line equivalent from §7.1.6 is available, it is listed in
parenthesis at the end.

)

| Cell label       | Controls display of cell labels on the rendered slices. Individual menu items are enabled or disabled depending on the active elements within the input file. ( LABEL )                                                                                                                                              |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Color            | Controls how the cells in the rendered slice are filled. The selections are Atomic Density, Mass Density, Cell ID, Material ID, Temperature, Importance, and available FMESH and TMESH tallies. ( COLOR , FMESH , TMESH )                                                                                            |
| Energy Bin       | List of energy bins in the selected FMESH . When an energy bin is selected, the results displayed are restricted to only that bin. When no runtape is provided the entries are grayed out, but can be inspected to ensure that the bins found are the ones expected. This menu is dynamically instantiated. ( EBIN ) |
| Extents Grid     | Draws a grid within the view port. This checkbox is disabled if Extents Ruler is not checked. ( SCALES )                                                                                                                                                                                                             |
| Extents Ruler    | Draws a ruler around the viewport that shows distance from the origin. The ruler goes from -extent to +extent in the x and y directions. ( SCALES )                                                                                                                                                                  |
| Lines            | Controls display of cell outlines. The outlines available are the Constructive Solid Geometry cells, Weight Window cells, Weight Window Generator Mesh cells, FMESH , and TMESH outlines. ( MESH )                                                                                                                   |
| Macrobody Facets | Adds macro-body facet suffixes to surface ID labels. Only active if Surface ID is checked. ( MBODY )                                                                                                                                                                                                                 |
| My Macros        | AUser controlled menu for executing arbitrary plotter commands [§7.3.2.2]. ( MYMACROS                                                                                                                                                                                                                                |
| Surface ID       | Controls display of surface ID labels on the rendered slices. ( LABEL )                                                                                                                                                                                                                                              |
| Time Bin         | List of time bins in the selected FMESH . When a time bin is selected, the results displayed are restricted to only that bin. As with energy bins, the entries are grayed out and for information only when no runtape is provided. This menu is dynamically instantiated. ( TBIN )                                  |
| Tips             | Enables/disables the display of tool tips when the mouse is hovered over other graphical elements.                                                                                                                                                                                                                   |
| Universe Level   | Controls display of repeated structure geometries [§2.2.2]. This menu is disabled if no Universes are defined in the problem. ( LEVEL )                                                                                                                                                                              |
| XY / YZ / ZX     | Direct access to common basis functions for views down the z , x , and y axis respectively. ( BASIS )                                                                                                                                                                                                                |

Figure 7.7: Sample My Macros menu created by launching the MCNP code as shown in §7.2 and loading Listing 7.2 using either the command MYMACROS load tech \_ preview \_ plotter \_ mymacros.txt or the Load menu item in the My Macros menu. The first five entries created enable the user to recreate the figures in this chapter. The sixth entry is an emulated separator with no command associated. The final entry provides a zoomed and shifted view of FMESH 14 defined in the input file.

<!-- image -->

## 7.3.2.2 My Macros Menu

The My Macros menu allows the user to create a menu to execute arbitrary
graphics commands. This could, for example, be a set of commands to load
up a specific view, or to switch to a given FMESH tally at a specific
energy bin. Our expectation is that the menu will primarily be used to
define a set of views that can be provided to collaborators or for
checking critical regions of a given geometry so that it is easy to
recreate a view across different invocations of the code. On start up,
the menu has three entries: Add Current View , Help , and Load .
Selecting Help will print out help on how to use the My Macros menu to
the terminal. If the Add Current View menu item is selected, it will add
the current view in the viewport to the menu as View 1 . This will also
add a Save entry to the menu. Selecting the Add Current View item a
second time will increment the View number. Once views are loaded in the
menu, they can be saved to a file for loading at a future date by using
the Save item. The format of the tech \_ preview \_ plotter \_ mymacros.txt
file is very simple with each line representing a view. The first word
of the line is the label that is shown in the menu. Spaces can be
included in the label by using quotes to enclose the entire label. The
rest of the line is the command that is executed. The saved file can be
loaded during a different invocation of the MCNP code by using the Load
item and selecting the saved file. Duplicate labels in the file will not
overwrite previous entries but will result in duplicate entries in the
menu.

A sample input file can be found in program Listing 7.2 with entries
that will regenerate the figures in this chapter when loaded with the
command MYMACROS load tech \_ preview \_ plotter \_ mymacros.txt or the
Load menu item in the My Macros menu with the MCNP code invoked as shown
in §7.2. The menu shown in Figure 7.7 is displayed on the screen. The
first five entries in this menu enable the user to recreate the figures
in this chapter. The sixth entry is an emulated separator with no
command associated. The seventh entry provides a zoomed, shifted view of
FMESH14 defined in the input file. Following the user-defined entries in
the menu are the default entries for adding the current view, printing
help to the terminal, loading menu entries from a file or saving the
current entries to a file.

Below are the keyboard equivalents of the My Macros menu:

## MYMACROS addCurrentView

Adds the current view to the My Macros menu

## MYMACROS add 'view name' commands to execute

Adds view name to the My Macros menu. The first word is interpreted as
the label to display in the menu and the rest of the words up to the end
of the line are taken as the command to execute. If spaces are desired
in the label then use double quotes as shown. No special treatment is
needed for the words in the command.

## MYMACROS load filename

Loads macro file with predefined macros for the menu. This command will
'Tear off' the My Macros menu. at the current mouse location.

## MYMACROS save filename

Saves the current views defined in the My Macros menu to the given
filename. This file can be edited in a text editor to modify the view
settings.

## MYMACROS remove 'view name'

Removes the named view from the current menu. Use quotes to encapsulate
menu entries with spaces in the name.

## 7.3.3 Information Pane

Left-clicking on cells in the Viewport Pane will display extended cell
information in the Information Pane. A sample is shown in Fig. 7.8.
Changing the view either using the mouse or keyboard commands to
translate/rotate/zoom the picture will erase the current cell
information. Using the Save PDF button will save the Viewport Pane to a
PDF file and include the contents of the information pane.

The information displayed includes the following fields:

## Current View

## FMESH Related Fields

This includes the BASIS , EXTENT , and ORIGIN for Viewport Pane. This
information can be copied and pasted into the Input Pane for
editing/reuse. If the current view is an on-axis view, then that view
will be printed as basis YZ / basis XZ / basis XY as well. This
information is always displayed in the information pane.

If an FMESH is active, the next few lines provide FMESH related
information including:

Number of source histories ( NPS )

KCODE cycles

Runtape file name

Dump number

The

FMESH Tally ID

Comments from the FMESH description

Energy range selected

Time range selected

FMESH value for cell that is clicked

Relative error for cell that is clicked

Indices of cell that is clicked

Figure 7.8: Example of information displayed when a cell is clicked in the Viewport Pane with the left mouse button. The information displayed is context sensitive and will include only fields that are defined for the current input file/runtape.

<!-- image -->

1

2

Cell Information

MCNP cell information that includes:

Cell ID

Coordinates of the clicked point

Universe, Lattice and Fill Universe, and Lattice ijk for repeated data
structures

Atom density

Mass density

Volume

Mass

PWT value

Material information

Temperature(s)

Importance for each particle type

Forced collision values for each particle type ( FCL )

Weight window lower bounds for energy or time interval values by window
number and particle type ( WWN : P )

Detector contribution values ( PD N )

Information that is not part of the calculation will not be displayed.
For instance, if an input file does not use WWN values, then those
values will be omitted from the clicked-cell-information.

## 7.3.4 Input Pane

The input pane sits at the bottom left of the main window and is shown
in Fig. 7.9. It consists of three elements: An input area at the bottom,
a history area in the middle, and a Clear History button at the top.
Keyboard commands are entered in the input area at the bottom. It is not
necessary to click in the input area. Any time the mouse focus is on the
Viewport Pane, the Information pane or the Control Pane, the keyboard
focus will be set to the input area of the Input Pane. A keyboard
command is terminated by the Enter key. Once the Enter key is pressed,
processing is started for executing the command just entered. As
described in §7.1, a command is a keyword from §7.1.6 followed by
appropriate parameters. Multiple keywords can be entered on a line, each
followed by its parameters. If an error is detected in either a keyword
or its parameters, then the rest of the command line from that point
onwards is ignored. Once a command is entered, it appears in the History
section of the Input Pane. Commands can be copied from the History
section and pasted into the Input area for editing/execution using the
arrow keys. Additionally, previously typed entries can be accessed using
the ↑ and ↓ keys. Once the entry desired is displayed, the command can
be edited, using the ← and → keys to move the cursor left or right if
required. Once editing is complete, pressing the Enter key will execute
it.

## 7.4 Program Listings for Generating Images

The MCNP input file used in the examples in this chapter is given in
Listing 7.1. The MYMACROS input file that generates figures in this
chapter is given in Listing 7.2.

Listing 7.1: tech\_preview\_plotter.mcnp.txt

Nested spheres in a box.

c Cell Definitions

<!-- image -->

Figure 7.9: The Input Pane is where users can enter keyboard input.
Entries are typed in the text box at the bottom left followed by the
Enter key. Previous entries are shown in the history label and can be
copied and pasted into the entry pane. Users can scroll through previous
entries in the text entry pane using the ↑ , ↓ , ← , and → keys.

```
3 1000 10 -0.5 -100 imp:n=1 $ Inner sphere 4 2000 20 -8 100 -200 imp:n=1 $ Outer sphere 5 3000 30 -1.20e-3 200 -300 imp:n=1 $ Air box 6 9999 0 300 imp:n=0 $ Graveyard 7 8 c Surface Definitions 9 100 so 30 10 200 so 35 11 300 rpp -75 75 -75 75 -75 75 12 13 c Data Cards 14 mode n 15 sdef pos = 0 0 0 erg = 14 $ 14-MeV isotropic point source of neutrons at the origin 16 c 17 fc1 Detector neutron F1 type tally on Surface 100 18 f1:n 100 $ surface current tally 19 e1 1e-9 999ilog 10 $ log scale, 0.001 eV to 10 MeV 20 c1 -.866 -.5 0 0.6 0.866 1.0 $ cosines for cosine tally 21 c 22 fc21 Detector neutron F1 type tally on Surface 100 23 f21:n 200 $ surface current tally 24 e21 1e-9 999ilog 10 $ log scale, 0.001 eV to 10 MeV 25 c21 -.866 -.5 0 0.6 0.866 1.0 $ cosines for cosine tally 26 c 27 m10 1001.80c 2 8016.80c 1 $ Water, 50% density 28 mt10 lwtr.10 29 m20 26056.80c 0.97 6000.80c 0.03 $ Pseudo Carbon Steel 30 m30 7014.80c 0.79 8016.80c 0.21 $ Pseudo Air 31 c 32 fmesh14:n geom = xyz origin = -75 -75 -75 out = xdmf 33 imesh = -60 -15 15 60 75 iints = 1 3 9 3 1 34 jmesh = -60 -15 15 60 75 jints = 1 3 9 3 1 35 kmesh = -60 -15 15 60 75 kints = 1 3 9 3 1 36 emesh = 1 14 100 37 eints = 1 1 1 38 tmesh = 0 1 10 100 39 tints = 1 10 9 1
```

```
40 fmesh24:n geom = xyz origin = -75 -75 -75 out = xdmf 41 imesh = 75 iints = 5 42 jmesh = 75 jints = 5 43 kmesh = 75 kints = 5 44 emesh = 1 14 100 45 eints = 1 1 1 46 tmesh = 0 1 10 100 47 tints = 1 1 1 1 48 c 49 rand gen=2 seed=12345 50 print 51 prdmp j 25000 52 nps 1e5 53 tmesh 54 rmesh111:n 55 cora111 -75 5i 75 56 corb111 -75 5i 75 57 corc111 -75 5i 75 58 endmd
```

Listing 7.2: tech\_preview\_plotter\_mymacros.txt

```
1 "Figure 1, 2 Top: Overview" plot FMESH OFF color by mat ba 1 0 0 0 1 0 or 0 0 0 ex 75 mbody off la 0 0 2 "Figure 2 Bottom: LinLog Tally 1" mcplot linlog tally 1 3 "Figure 3: LogLin Tally 1" mcplot loglin tally 1 4 "Figure 4: FMESH 14" plot FMESH 14 ebin 2 tbin 4 ba 1 0 0 0 1 0 or 0 0 0 ex 75 mbody off la 0 0 mesh 9 5 "Figure 5: TMESH 111" plot TMESH 111 ba 1 0 0 0 1 0 or 0 0 0 ex 75 mbody off la 0 0 mesh 7 6 "----------------" 7 "Zoomed, Shifted FMESH 14" plot FMESH 14 ba 0 1 0 0 0 1 or 0 7.5 0 ex 15 15 la 1 0
```
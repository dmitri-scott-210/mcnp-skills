---
title: "Chapter 6.2 - The Geometry Plotter, PLOT"
chapter: "6.2"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/6_MCNP_Geometry_and_Tally_Plotting/6.2_The_Geometry_Plotter,_PLOT.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

hosts and provide X Windows forwarding. This is considered to be more
secure, and it handles setting the DISPLAY variable for the user. If SSH
is used, do not manually set DISPLAY as this will interfere with the
secure forwarding. On local systems (where displayhost and executehost
are the same), this warning does not apply.

## 6.2 The Geometry Plotter, PLOT

The geometry plotter is used to plot two-dimensional slices of a problem
geometry specified in the INP file. This feature of MCNP6 is invaluable
for debugging geometries. You should first verify your geometry model
with the MCNP6 geometry plotter before running the transport part of
MCNP6, especially with a complicated geometry where it is easy to make
mistakes. The time that is required to plot the geometry model is small
compared with the potential time lost working with an erroneous
geometry.

## 6.2.1 PLOT Input and Execute Line Options

To plot geometries with MCNP6, enter the following command:

MCNP6 IP INP= filename KEYWORD=value(s)

where IP stands for 'initiate and plot.' The allowed keywords are:

| NOTEK            | Suppress plotting at the terminal and send all plots to the graphics metafile, PLOTM . The NOTEK keyword is used for production and batch situations or when the user's terminal has no graphics capability.                                                                                                                                                                  |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| COM= filename    | Use file filename as the source of plot requests. When an end-of-file (EOF) is read, control is transferred to the terminal. In a production or batch situation, end the file with an END command to prevent transfer of control. Never end the COM file with a blank line. If COM is absent, the terminal is used as the source of plot requests.                            |
| PLOTM= filename  | Name the graphics metafile filename . The default name is PLOTM . For some systems this metafile is a standard postscript file and is named plotm.ps . Unique names for the output file, PLOTM , will be chosen by MCNP6 to avoid overwriting existing files.                                                                                                                 |
| COMOUT= filename | Write all plot requests to file filename . The default name is comout . PLOT writes the COMOUT file in order to give the user the opportunity to do the same plotting at some later time, using all or part of the old COMOUT file as the COM file in the second run. Unique names for the output file, COMOUT , will be chosen by MCNP6 to avoid overwriting existing files. |

The most common method of plotting is with an interactive graphics
terminal. First, MCNP6 will read the input file and perform the normal
checks for consistency, then the interactive point-and-click geometry
plotting window will appear in its own window.

When X Windows is in use, the plot window supports a variety of
interactive features that assist the user in manipulating the plot. The
interactive options are discussed after the discussion of the command-
line plot options.

When names are defaulted, unique names for the output files, PLOTM and
COMOUT , will be chosen by MCNP6 to avoid overwriting existing files.
Unique names are created by changing the last letter of the default name

until the next available name is found. For example, if the file
plotm.ps already exists, MCNP6 tries the name plotn.ps , etc., until it
finds an available name.

MCNP6 can be run in a batch environment without much difficulty, but the
user interaction with the plotter is significantly reduced. When not
using an interactive graphics terminal, use the NOTEK option on the
MCNP6 execution line or set TERM=0 along with other PLOT commands when
first prompted by PLOT . Setting NOTEK will prevent a blank window from
appearing prior to the first PLOT command being entered. In systems with
no X Windows support, using NOTEK will prevent the MCNP6 code from
returning an error that there is no display available. In the
interactive mode, plots can be sent to the graphics metafile with the
FILE keyword. See the keyword description in §6.2.4 for a complete
explanation. The plotm.ps file is a postscript file that can be sent to
a postscript printer. Every view plotted will be put in a postscript
file called plot?.ps where ? begins at M and goes to the next letter in
the alphabet if plotm.ps exists.

## 6.2.2 Geometry Plotting Basic Concepts

Before describing the individual plotting commands, it is helpful to
understand some basic mechanics of two-dimensional (2-D) plotting. To
obtain a 2-D slice of a geometry, one must decide where the slice should
be taken and how much of the slice should be viewed in the plotting
window. The slice is a 2-D plane that may be arbitrarily oriented in
space; therefore, the first problem is to decide the plane position and
orientation.

In an orthogonal three-dimensional coordinate system the three axes are
perpendicular to each other. An orthogonal axis system is defined with a
set of BASIS vectors on the 2-D plane used to slice the geometry to
determine the plot orientation. The first BASIS vector is in the
horizontal direction of the screen. The second BASIS vector is the
vertical direction on the screen. The surface normal for the plane being
viewed is perpendicular to the two BASIS vectors and directed out of the
screen towards the viewer.

For example, the BASIS vectors that define a view of the x -y plane (or
'down' the z -axis) are 1, 0, 0 and 0, 1, 0 . The x -axis view can be
mirrored by changing the vectors to: -1, 0, 0 and 0, 1, 0 . This would
cause the x -axis values to decrease from left to right while the y
-axis values increase from bottom to top as before. A complete mirror on
both axes can be obtained by setting the basis to -1, 0, 0 and 0, -1, 0
. Usage of BASIS and other commands referenced in this section are
discussed in §6.2.4.1.4.

The default BASIS vectors define views of the y -z , z -x , and x -y
planes, which are generally sufficient for viewing geometry. However, if
required, the flexibility of the BASIS command can be used to examine
the geometry along any desired slice. Arbitrarily oriented basis vectors
are defined with component magnitudes that need not be normalized (e.g.
0, 1, 1 is functionally equivalent to 0, 2, 2 ). If an angle between the
vector and an axis is known, the sine or cosine of the angle can be used
to determine the magnitudes. A few decimal places of precision will
often suffice.

The center of the view plane may be set with the ORIGIN command. For
example, on a y -z plot, the x coordinate of ORIGIN sets the 'depth'
that the slice is viewed from and the y and z coordinates translate the
view in that slice. Because planes are infinite and only a finite area
can be displayed at any given time, the extent of the cross-sectional
plane displayed can be specified with the EXTENT command. For instance,
on a y -z plot at an ORIGIN of x1, y1, z1 , the y -z plane is viewed at
a depth of x = x1 , and it is centered at y1 and z1 . If EXTENT y2 z2 is
entered, the plot displayed would have a horizontal extent from y1 -y2
to y1 + y2 and a vertical extent of z1 -z2 to z1 + z2 . Thus EXTENT may
be used to zoom the view of the plot slice in or out.

All the plot parameters for the MCNP6 plotter have defaults. In command-
line mode, respond to the first MCNP6 prompt with Enter to obtain a
default plot; in the interactive mode, click on the plot area of the
interactive screen. The default geometry plot is a PX plane centered at
0, 0, 0 with an extent of -100 &lt; y &lt; 100 and -100 &lt; z &lt; 100 . The y
-axis will be the horizontal axis of the plot, and the z -axis will be
the vertical axis. Surface labels are printed. In command-prompt mode,
this default is the equivalent of entering the following command line:

1

## ORIGIN 0 0 0 EXTENT 100 100 BASIS 0 1 0 0 0 1 LABEL 1 0

By manipulating selected plot parameters, any arbitrary 2-D plot can be
obtained. Most parameters remain set until they are explicitly changed
either by the same command with new values or by a conflicting command.

## /warning\_sign Caution

Placing the plot plane exactly on a surface of the geometry is not a
good idea.

For example, if the input geometry has a PX plane at x = 0 , that plane
coincides with the default plot plane. Several results can occur:

1. Some portion of the geometry may be displayed in dotted lines, which usually indicates a geometry error (even if there is none in this case).
2. Some portion of the geometry may simply not show up at all.
3. Very infrequently the code may crash with an error.

To prevent all these unpleasantries, move the plot plane some tiny
amount away from surfaces. The terminal will show a warning when the
plot plane is coplanar with a geometry plane.

## 6.2.3 Interactive Geometry Plotting in Point-and-click Mode

The geometry plotter supports interactive point-and-click plotting for
all systems with X Windows graphics [§6.1]. The plot area is active at
all times when the interactive plotter is enabled. However, it is not
active when the command-line interface is in use (e.g., requested via
the Plot&gt; button) except for text commands that need mouse input from
the plot window such as the LOCATE command [§6.2.4.1]. This command
requires a mouse click in the plot area to provide the intended terminal
output. Figure 6.1 shows an example geometry plot window with the
interactive controls outlined. The controls are separated into left,
right, top, and bottom menus. The plot area itself is also active. An
explanation of the point-and-click commands in each control menu
follows.

## 6.2.3.1 Top Menu: Translate and Zoom Functions

| UP RT DN LF       | When clicked, these buttons move the plot frame one full window upwards ( UP ), to the right ( RT ), downwards ( DN ), or to the left ( LF ).                                                                                                                                                                                                                                                             |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ORIGIN            | After clicking, the user can click in the plot geometry to set the origin and center the view at the clicked point.                                                                                                                                                                                                                                                                                       |
| .1 .2 Zoom 5. 10. | The zoom command requires a minimum of two mouse clicks: The first click on the zoom scale selects a discrete zoom factor between 0.1 and 10 for the current plot. The selected scale factor is displayed above the 'Click here or picture or menu' box in the lower-left of the plot window. A second mouse click on the same scale factor will zoom at that factor centered at the current plot origin. |

Figure 6.1: Geometry Plot Window Interactive Plotting Controls

<!-- image -->

If the second mouse click is on a different scale factor, it then counts
as a new 'first click.'

If the second click occurs in the plot geometry, the origin is set to
that point and the zoom occurs about this new origin.

Hint: To effectively cancel a zoom command, click the Zoom label (which
corresponds to a 1 × zoom) on the scale twice.

## 6.2.3.2 Left Menu: What is Plotted and How

| (Hidden   | button)   | A 'hidden' button resides in the upper left quadrant of the plot window and triggers a redraw. If your plot window appears blank when exposed, click in the upper left of the screen to refresh it. On some systems, the entire plot window may appear blank if resized or minimized and then restored. Just click this hidden button to redraw the window if this happens. This button is equivalent to the Redraw button [§6.2.3.4], but is easier to find when the window is blank.                                                                                                                                                                                        |
|-----------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Value     | for var   | While not a control, this area immediately above the lower left control box provides useful information: By default, var is 'mat' and provides information on the material number under the cursor. The line under the Value for var always lists the current cell the cursor is in. Without any other button clicked, one can click through the geometry and see the cell number and value attached to var change. The var can take any of the parameters listed on the right menu bar [§6.2.3.3]. This provides an easy way to query parameters like density or cell importance. The last line before the control box gives the coordinates of the current cursor location. |
| CURSOR    |           | Clicking this button activates the cursor-region selector; the cursor changes shape to appear like the upper left corner of a box. Click in the plot window at a point representing the upper left spatial boundary of the desired plot. The cursor will change shape again; now click the lower right position of the desired plot. The plot will be redrawn using the new boundaries and keep a 1:1 aspect ratio. This is equivalent to an EXTENT command and an ORIGIN command.                                                                                                                                                                                            |
| RESTORE   |           | This button restores the view to the previous 'frame.' For example, if CURSOR is used to zoom on a portion of the geometry from a full view, Restore can be used to return to the full view without having to enter ORIGIN and EXTENT commands. It is a single level 'undo' button for the plotted geometry.                                                                                                                                                                                                                                                                                                                                                                  |

## CellLine

Toggles among available line modes:

- CellLine Plot constructive solid geometry cells, outlined in black. (DEFAULT)
- No Lines Plot cells not outlined in black.
- WW MESH Plot weight-window superimposed mesh without cell outlines.
- WW+Cell Plot weight-window superimposed mesh and cell outlines.
- WWG MESH Plot weight-window generator mesh.
- WWG+Cell Plot weight-window generator mesh and cell outlines.
- MeshTaly Plot TMESH mesh tally boundaries.
- MT+Cell Plot TMESH mesh tally boundaries and cell outlines.

## PostScript

## ROTATE

## COLOR var

## SCALES

The CellLine and No Lines options are always available. WW MESH and
WW+Cell are available only when the WWP card calls for using a
superimposed weight-window mesh (5th entry negative) and a WWINP file is
provided. WWG MESH and WWG+Cell are available only when a MESH card
appears in the input and when the WWG card requests superimposed mesh
generation (2nd entry is 0). MeshTaly and MT+Cell are available only
when a TMESH mesh tally has been requested.

Note: After a line mode is chosen, click REDRAW from the bottom menu to
force the selected mesh and/or cell lines to be drawn on the plot.

When clicked, writes the next plot to a postscript file (default name,
plotm.ps ). The image in the postscript file is of far higher quality
than a screenshot of the plot window because it is a vector graphic. To
create a postscript image of the current plot, activate the PostScript
button and then click Redraw from the bottom menu. After one plot is
written to the postscript file, the PostScript button is reset.

The function of the PostScript button is equivalent to the non-
interactive command FILE with no argument; i.e., only the next plot is
written to the file.

Toggles between two modes: ROTATE on and ROTATE off .

ROTATE on interchanges the first two basis vectors, resulting in a 90 ◦
rotation of the plot around the 'off-basis' axis (e.g., the z -axis in
an x -y plot). Whether the rotation is clockwise or counter-clockwise
depends on the initial basis vectors.

Note: After a rotation mode is chosen, click Redraw from the bottom menu
to force the plot to be redrawn with new orientation.

Toggles colors on and off.

Color shading of geometry plots may be on a variety of cell parameters.

By default, var registers the cell parameter mat , which indicates that
plot colors are assigned to materials. By toggling the COLOR button, all
color can be turned off, presenting only a line drawing after a redraw
of the plot (which can substantially improve plotter speed).

Alternatively, the cell parameter on which the plot color scheme is
based can typically be changed to any parameter in the right margin
control menu appropriate to the problem [§6.2.3.3]. To change the
parameter, click a cell parameter from the right menu, click the COLOR
button to turn off color, then click COLOR again to reactivate it. The
new selected cell parameter will now register as var .

For example, to color by cell density, one would click the den parameter
on the right menu, then click COLOR so ' COLOR off ' appears. Clicking
the ' COLOR off ' button again will show ' COLOR den '. A click of the
Redraw button will display the new colors.

Note: Any changes in plot colors require a redraw of the plot via the
Redraw button.

Toggles among three scale modes on each click:

- If SCALES is set to 0, no scale is provided on the plot (DEFAULT).
- If SCALES is set to 1, dimensional scales for both horizontal and vertical axes are provided; and
- If SCALES is set to 2, dimensional scales for both horizontal and vertical axes with an associated grid are provided.

The values drawn on the axes are the distance from the origin of the
current plot, i.e., they go from -EXTENT to +EXTENT in the two
directions.

Note: after the scale mode is chosen, click Redraw from the bottom menu
to force the scales to be drawn on the plot.

LEVEL

## XY, YZ, ZX

## LABELS, L1, L2

Toggles through universe levels in repeated-structure geometry. If there
are no sublevels, then the LEVEL button is not active. The button label
identifies the level to be plotted if levels are present in the input.
Requires that the Redraw command from the bottom menu be clicked to
create the revised plot.

Alter plot perspective to corresponding planar combinations:

- The XY command sets the basis to (1 0 0 0 1 0);
- The YZ command sets the basis to (0 1 0 0 0 1) (DEFAULT); and
- The ZX command sets the basis to (0 0 1 1 0 0).

In all cases, the origin is unchanged.

Controls the status of surface and cell labels.

If L1 is set to sur , then surface labels are displayed (DEFAULT).

If L1 is set to off , then surface labels are not displayed.

If L2 is set to off , then cell labels are not displayed (DEFAULT).

If L2 is set to var , then the cell parameter, var , is the cell label.
To change the cell parameter, click one from the right menu, then click
the L2 button to change the label type to the new selection.

A change in state of any LABELS parameter requires a redraw of the plot
to update the view.

| MBODY   | Toggles labeling of macrobody facets. If MBODY is on and if L1 of the LABEL command is set to sur , then general macrobody surface numbers are displayed (DEFAULT). If MBODY is off and if L1 is set to sur , then macrobody facet numbers for each macrobody surface are displayed. A change in state of MBODY requires the plot be redrawn to update the surface labels.   |
|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FMESH   | Cycle through mesh tallies. Does not change plot layout. Only present if FMESH tallies exist in the input. A change in state of FMESH requires that Redraw be clicked from the bottom menu to display the revised plot.                                                                                                                                                      |
| LEGEND  | When activated, displays a contour plot legend for a mesh tally. The legend will display the association of the color key to the numerical values in the plot.                                                                                                                                                                                                               |

## Click here or picture or menu

Clicking in this area changes the button to show ' Enter Data&gt; ' and
requires the user to enter a plot command. A list of commands is in
§6.2.4.1. Up to 29 characters representing one or more plot commands can
be entered. Pressing Enter accepts the command string. If the command
line is terminated with an ' &amp; ', the ' Enter Data&gt; ' prompt remains and
another command (or a continuation of a long command) can be entered. A
line that does not end with an ' &amp; ' sends the command(s) and triggers a
redraw when Enter is pressed.

<!-- image -->

An example of the usefulness of this feature is entering a specific
origin to center the plot at. Where clicking the Origin button in the
top menu and clicking the plot is convenient, if more precision is
required (such as tracking geometry errors leading to lost particles), a
user should click the Click here... box and type something like ' origin
10.725 -2.663 1.004" .

Note: for extended access to the command-line interface, use the Plot&gt;
option in the bottom menu to pass control to the terminal window.

## 6.2.3.3 Right Menu: Parameter Choices for Labels, Colors, etc.

The right menu is used to set the variables used for for cell labels and
geometry coloring. After clicking a button in the right menu, the left
menu L2 or COLOR button must be set to the new parameter. A redraw must
be triggered before the plot is updated with the new labels and/or
colors. Some right-menu options work for both colors and labels such as
cel . Other options only work as labels.

| cel   | Cell labels/colors will be cell numbers.                                                                                                                                                                                                                      | Cell labels/colors will be cell numbers.                                                                                                                                                                                                                      |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| imp   | Cell labels will be importance by particle type.                                                                                                                                                                                                              | Cell labels will be importance by particle type.                                                                                                                                                                                                              |
| rho   | Cell labels/colors will be atom densities (barn - 1 · cm - 1 ).                                                                                                                                                                                               | Cell labels/colors will be atom densities (barn - 1 · cm - 1 ).                                                                                                                                                                                               |
| den   | Cell labels/colors will be mass densities (g/cm 3 ).                                                                                                                                                                                                          | Cell labels/colors will be mass densities (g/cm 3 ).                                                                                                                                                                                                          |
| vol   | Cell labels will be volumes (calculated or user-supplied, cm 3 ).                                                                                                                                                                                             | Cell labels will be volumes (calculated or user-supplied, cm 3 ).                                                                                                                                                                                             |
| fcl   | Cell labels will be forced-collision fraction by particle type.                                                                                                                                                                                               | Cell labels will be forced-collision fraction by particle type.                                                                                                                                                                                               |
| mas   | Cell labels will be masses (g).                                                                                                                                                                                                                               | Cell labels will be masses (g).                                                                                                                                                                                                                               |
| pwt   | Cell labels will be photon production weights.                                                                                                                                                                                                                | Cell labels will be photon production weights.                                                                                                                                                                                                                |
| mat   | Cell labels/colors will be material numbers (DEFAULT for COLOR variable, var ).                                                                                                                                                                               | Cell labels/colors will be material numbers (DEFAULT for COLOR variable, var ).                                                                                                                                                                               |
| tmp   | Cell labels/colors will be temperature (MeV) for time index 1: TMP 1.                                                                                                                                                                                         | Cell labels/colors will be temperature (MeV) for time index 1: TMP 1.                                                                                                                                                                                         |
| wwn   | Cell labels/colors will be weight windows for energy or time index N (or combined energy-time index N ): WWN N : P .                                                                                                                                          | Cell labels/colors will be weight windows for energy or time index N (or combined energy-time index N ): WWN N : P .                                                                                                                                          |
|       | Note: When combining time and energy binning, the index N varies as follows: For 3 time bins and 3 energy bins, the index, N , would map to the following sequence: (T1, E1), (T1, E2), (T1, E3), (T2, E1), (T2, E2), (T2, E3), (T3, E1), (T3, E2), (T3, E3). | Note: When combining time and energy binning, the index N varies as follows: For 3 time bins and 3 energy bins, the index, N , would map to the following sequence: (T1, E1), (T1, E2), (T1, E3), (T2, E1), (T2, E2), (T2, E3), (T3, E1), (T3, E2), (T3, E3). |
| ext   | Cell labels will be exponential transform stretching parameter by particle type.                                                                                                                                                                              | Cell labels will be exponential transform stretching parameter by particle type.                                                                                                                                                                              |
| pd    | Cell labels will be detector contribution frequency fraction by particle type.                                                                                                                                                                                | Cell labels will be detector contribution frequency fraction by particle type.                                                                                                                                                                                |
| dxc   | Cell labels will be DXTRAN contribution frequency fraction.                                                                                                                                                                                                   | Cell labels will be DXTRAN contribution frequency fraction.                                                                                                                                                                                                   |
| u     | Cell labels will be universe numbers.                                                                                                                                                                                                                         | Cell labels will be universe numbers.                                                                                                                                                                                                                         |
| lat   | Cell labels will be the enclosed lattice type.                                                                                                                                                                                                                | Cell labels will be the enclosed lattice type.                                                                                                                                                                                                                |
| fill  | Cell labels will be filling universe identification numbers.                                                                                                                                                                                                  | Cell labels will be filling universe identification numbers.                                                                                                                                                                                                  |
| ijk   | Cell labels will be lattice indices.                                                                                                                                                                                                                          | Cell labels will be lattice indices.                                                                                                                                                                                                                          |
| nonu  | Cell labels will be fission turnoffs.                                                                                                                                                                                                                         | Cell labels will be fission turnoffs.                                                                                                                                                                                                                         |
| pac   | When the interactive plotter is called from MCPLOT , cell labels will be values of columns in PRINT Table 126. Use the par and N buttons to toggle particle and column respectively. The columns shown by this button are:                                    | When the interactive plotter is called from MCPLOT , cell labels will be values of columns in PRINT Table 126. Use the par and N buttons to toggle particle and column respectively. The columns shown by this button are:                                    |
|       | pac1 : P                                                                                                                                                                                                                                                      | The labels are the 'tracks entering' column.                                                                                                                                                                                                                  |
|       | pac2 : P                                                                                                                                                                                                                                                      | The labels are the 'population' column.                                                                                                                                                                                                                       |
|       | pac3 : P                                                                                                                                                                                                                                                      | The labels are the 'collisions' column.                                                                                                                                                                                                                       |
|       | pac4 : P                                                                                                                                                                                                                                                      | The labels are the 'collisions * weight (per history)' column.                                                                                                                                                                                                |
|       | pac5 : P                                                                                                                                                                                                                                                      | The labels are the 'number weighted energy' column.                                                                                                                                                                                                           |

|     | pac6 : P                                                                                                                                                                                                                                                                                                                                                                                         | The labels are the 'flux weighted energy' column.                                                                                                                                                                                                                                                                                                                                                |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     | pac7 : P                                                                                                                                                                                                                                                                                                                                                                                         | The labels are the 'average track weight (relative)' column.                                                                                                                                                                                                                                                                                                                                     |
|     | pac8 : P                                                                                                                                                                                                                                                                                                                                                                                         | The labels are the 'average track mfp (cm)' column.                                                                                                                                                                                                                                                                                                                                              |
| tal | Used for plotting TMESH usage.                                                                                                                                                                                                                                                                                                                                                                   | tally results when PLOT is called from MCPLOT . See §6.4.3 for                                                                                                                                                                                                                                                                                                                                   |
| par | Selects particle type for cell quantities that have particle-specific values (e.g., imp: P ). Click the par button then another button in the right menu to toggle the particle type. Prior to redrawing the plot, the associated LABELS or COLOR button should be clicked twice to toggle from the current particle to 'off' then back to the desired parameter with the updated particle type. | Selects particle type for cell quantities that have particle-specific values (e.g., imp: P ). Click the par button then another button in the right menu to toggle the particle type. Prior to redrawing the plot, the associated LABELS or COLOR button should be clicked twice to toggle from the current particle to 'off' then back to the desired parameter with the updated particle type. |
| N   | Selects a numerical index for cell quantities or mesh-based weight-window bins that have indexed values. Updating the index for a displayed parameter follows the same process described in the description of par .                                                                                                                                                                             | Selects a numerical index for cell quantities or mesh-based weight-window bins that have indexed values. Updating the index for a displayed parameter follows the same process described in the description of par .                                                                                                                                                                             |
|     | Example: WWN3:P would provide photon weight windows in the 3 rd energy group and be selected by clicking wwn , par , and N .                                                                                                                                                                                                                                                                     | Example: WWN3:P would provide photon weight windows in the 3 rd energy group and be selected by clicking wwn , par , and N .                                                                                                                                                                                                                                                                     |
|     | Note: For both the par and N buttons, clicking these with a relevant parameter selected will show the change in particle or index in the ' Value for var ' information box. This is useful for keeping track of the index or particle currently selected.                                                                                                                                        | Note: For both the par and N buttons, clicking these with a relevant parameter selected will show the change in particle or index in the ' Value for var ' information box. This is useful for keeping track of the index or particle currently selected.                                                                                                                                        |

## 6.2.3.4 Bottom Menu: Commands

| Redraw   | Triggers a redraw of the plot.                                                                                                                                                                                                                                                                                   |
|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Plot>    | Passes control to the command-line window enabling traditional plot commands to be entered. Once in the command-line mode, control can be returned to the interactive plotter with the command INTERACT . Note: For brief text commands, use the Click here ... button to type up to 29-character text commands. |
| End      | Terminates the plot session and exit PLOT .                                                                                                                                                                                                                                                                      |

## 6.2.4 Interactive Geometry Plotting in Command-prompt Mode

Invoking the geometry plotter through the command-line interface offers
more flexibility for combining commands when compared to the point-and-
click interactive plotter. Command-line-interface entry of commands can
be invoked in two ways:

1. The non-interactive plotter can be called with the NOTEK keyword as described in §6.2.1 and results will be viewable in the plot?.ps file. The user can open the X Window plotter after execution with the PLOT command TERM 1 .
2. The interactive plotter is started and the user clicks the Plot&gt; button in the bottom menu of the interactive window (§6.2.3.4). This transfers command entry to the terminal window with the results of the command visible in the interactive window. In this mode the user can still use the interactive plotter buttons. For more information on this interactive environment, see §6.2.3. The user may return to the point-and-click interactive mode by entering the command INTERACT at the terminal prompt.

A plot request consists of a sequence of commands terminated by pressing
the Enter key. A command consists of a keyword that is usually followed
by some parameters. A plot request line cannot have more than 128
characters on a single line, but lines can be continued by typing an &amp;
(ampersand) before pressing the Enter key. However, each keyword and its
parameter(s) must be complete on one line. The &amp; character can be used
in the input COM file [§6.2.7] as well as at the PLOT prompt. Keywords
and parameters are blank-delimited with commas and equal signs
interpreted as blanks. Numbers can be entered in free-form format and do
not require a decimal point for floating-point data. Keywords and
parameters remain in effect until they are explicitly changed. The
commands OPTIONS , HELP , and ? display a complete list of keywords.

Keywords can be abbreviated by shortening them to any degree as long as
they are not ambiguous and are spelled correctly. If a shortened keyword
is ambiguous, the entire command string will be rejected and the
terminal will warn that an ambiguous command was used. An example of an
ambiguous keyword would be ' O '. It is unclear if O refers to ORIGIN or
OPTION , thus another character is required to differentiate it.
Parameters following keywords can not be abbreviated.

## 6.2.4.1 PLOT Commands

## 6.2.4.1.1 Device-control Commands

Normally PLOT draws plots to a system's X Window display. By using the
following commands, the user can specify that plots not be drawn to the
display and/or that they be sent to a graphics metafile or PostScript
file for processing later by a graphics utility program.

| TERM n      | Output device type is specified by n . n =0 for a terminal with no graphics forwarding capability (for a system without the X Window System). No plots are drawn to a display window, and all plots are sent to the graphics metafile. TERM 0 is equivalent to putting NOTEK on MCNP6's execution line [§6.2.1].   | Output device type is specified by n . n =0 for a terminal with no graphics forwarding capability (for a system without the X Window System). No plots are drawn to a display window, and all plots are sent to the graphics metafile. TERM 0 is equivalent to putting NOTEK on MCNP6's execution line [§6.2.1].   |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FILE aa     | Send or do not send plots to the graphics metafile PLOTM.PS according to the value of the parameter aa . The graphics metafile is not created until the first FILE command is entered. FILE has no effect in the NOTEK or TERM 0 cases. The allowed values of aa are the following:                                | Send or do not send plots to the graphics metafile PLOTM.PS according to the value of the parameter aa . The graphics metafile is not created until the first FILE command is entered. FILE has no effect in the NOTEK or TERM 0 cases. The allowed values of aa are the following:                                |
|             | aa is blank                                                                                                                                                                                                                                                                                                        | Only the current plot is sent to the graphics metafile.                                                                                                                                                                                                                                                            |
|             | aa =ALL                                                                                                                                                                                                                                                                                                            | The current plot and all subsequent plots are sent to the metafile until another FILE command is entered.                                                                                                                                                                                                          |
|             | aa =NONE                                                                                                                                                                                                                                                                                                           | The current plot is not sent to the metafile nor are any subsequent plots until another FILE command is entered.                                                                                                                                                                                                   |
| VIEWPORT aa | Make the viewport rectangular or square according to the value of aa . This option does not affect the appearance of the plot. It only determines whether the area around the plot is padded for a legend, scales, and interactive controls.                                                                       | Make the viewport rectangular or square according to the value of aa . This option does not affect the appearance of the plot. It only determines whether the area around the plot is padded for a legend, scales, and interactive controls.                                                                       |
|             | If aa =RECT , allow space beside the plot for a legend and around the plot for scales. (DEFAULT)                                                                                                                                                                                                                   | If aa =RECT , allow space beside the plot for a legend and around the plot for scales. (DEFAULT)                                                                                                                                                                                                                   |
|             | If aa =SQUARE , the legend area, the legend, and scales are omitted.                                                                                                                                                                                                                                               | If aa =SQUARE , the legend area, the legend, and scales are omitted.                                                                                                                                                                                                                                               |
|             | Note: Use of the SQUARE option disables the interactive-window plotter capability.                                                                                                                                                                                                                                 | Note: Use of the SQUARE option disables the interactive-window plotter capability.                                                                                                                                                                                                                                 |

## 6.2.4.1.2 General Commands

| &        | Continue reading commands for the current plot from the next input line. The & must be the last character on the line. The & command must not break another command and its parameters onto two lines; instead, it is used to continue long user command strings on new lines.                                                                                                                  |
|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| INTERACT | Return to the interactive point-and-click geometry plotter interface. This command is used to return from the terminal-command interface when the Plot> button is clicked or the command PLOT is entered in the ' Click here or ... ' box while in the interactive plotter.                                                                                                                     |
| RETURN   | If MCPLOT was called during investigation of geometry with PLOT (via the ip execution option), control returns to PLOT . Otherwise RETURN has no effect.                                                                                                                                                                                                                                        |
| MCPLOT   | Call the MCPLOT tally and cross-section plotter [§6.3]. For tally results, a RUNTAPE file or MCTAL must be read [§6.3.1.1 and §6.3.3.4].                                                                                                                                                                                                                                                        |
| PAUSE n  | Can be used on any line of a plot command file that is specified with the execute COM= filename option [§6.2.1]. Holds each view for n seconds. If no n value is provided, each view remains until Enter is pressed. When absent, the commands specified in the command file will run sequentially until the end of the command file is reached at which point control returns to the terminal. |
| END      | Terminate execution of PLOT . Closes any open X Windows and returns the terminal from the PLOT prompt to a standard system shell prompt.                                                                                                                                                                                                                                                        |

## 6.2.4.1.3 Inquiry Commands

The following commands print information to the terminal.

| OPTIONS or ? or HELP   | Display a list of the PLOT commands and available colors.                                                                                                                                                                                                                                                                                                                                                                                                         |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| STATUS                 | Prints to the terminal the current values of the plotting parameters such as the EXTENT , BASIS , and ORIGIN .                                                                                                                                                                                                                                                                                                                                                    |
| LOCATE                 | Present the graphics cursor and prepare to receive cursor input from the user. This command is available only if the system has graphics (X Windows [§6.1]) capability. After entering this command, left-click on the plot window. The cursor icon changes to a '+'. Move this cursor to a point in the picture and left-click again. The x , y , and z coordinates of the point are displayed. The LOCATE command should be the only command on the input line. |

## 6.2.4.1.4 Plot Commands

Plot commands define the values of the parameters used in drawing the
next plot. Parameters entered for one plot remain in effect for
subsequent plots until they are overridden, either by the same command
with new values or by a conflicting command.

| BASIS x1 y1 z1 x2   | Orient the plot so that the direction ( x 1 , y 1 , z 1 ) points to the right and the direction ( x 2 , y 2 , z 2 ) points up. The default values are 0 1 0 0 0 1 , causing the y axis to point to the right and the z axis to point up. The two vectors of BASIS do not have to be normalized, but they should be orthogonal. If the two vectors are not orthogonal, MCNP6 chooses an arbitrary second vector that is orthogonal to the first vector. MCNP6 will ignore the command if parallel or zero-length vectors are entered.   |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ORIGIN vx vy vz     | Position the plot so that the origin, which is in the middle of the geometry slice, is at the point ( v x , v y , v z ) . The default values are 0 0 0 . The BASIS vectors are relative to this point.                                                                                                                                                                                                                                                                                                                                 |
| EXTENT eh [ev]      | Set the scale of the plot so that the horizontal distance from the origin to either side of the plot is eh and the vertical distance from the origin to the top or bottom is ev The ev parameter is optional, and if omitted, it is set equal to eh . If ev is set and not equal to eh , the plot aspect ratio will be distorted. The default values are 100 and 100, creating a viewport of the geometry covering 200 × 200 cm.                                                                                                       |
| PX vx               | Plot a cross section of the geometry in the plane normal to the x axis at a distance vx from the origin. This command is a shortcut equivalent of ' BASIS 0 1 0 0 0 1 ORIGIN vx vy vz ' where vy and vz are the current values of vy and vz .                                                                                                                                                                                                                                                                                          |
| PY vy               | Plot a cross section of the geometry in the plane normal to the y axis at a distance vy from the origin.                                                                                                                                                                                                                                                                                                                                                                                                                               |
| PZ vz               | Plot a cross section of the geometry in the plane normal to the z axis at a distance vz from the origin.                                                                                                                                                                                                                                                                                                                                                                                                                               |

## LABEL slabel [clabel [par]]

Put labels of size slabel on the surfaces and, optionally, labels of
size clabel in the cells. The parameter, par , following clabel is
further optional and defaults to MAT . The sizes specified by slabel and
clabel are relative to 0.01 times the height of the view window. If
slabel or clabel is zero, that kind of label will be omitted. The
allowed range of sizes for the labels is [0.2-100].

The default is LABEL 1 0 . The possible values of par follow, where : P
indicates the particle type.

| CEL     | Cell labels will be cell numbers.                                                                                            |
|---------|------------------------------------------------------------------------------------------------------------------------------|
| IMP: P  | Cell labels will be cell importances for particle type P .                                                                   |
| RHO     | Cell labels will be atom densities (barn - 1 · cm - 1 ).                                                                     |
| DEN     | Cell labels will be mass density (g/cm 3 ).                                                                                  |
| VOL     | Cell labels will be volume (calculated or user-supplied, cm 3 ).                                                             |
| FCL: P  | Cell labels will be forced-collision fraction (from FCL : P ) for particle type P .                                          |
| MAS     | Cell labels will be masses (g).                                                                                              |
| PWT     | Cell labels will be photon production weights.                                                                               |
| MAT     | Cell labels will be material number (DEFAULT).                                                                               |
| TMP [n] | Cell labels will be temperature (MeV) at time n (specified on the TMP and THTME cards). The n is optional and defaults to 1. |

## /warning\_sign Caution

In the command-prompt PLOT mode, the PD n option for the LABEL command
will show all zeros on the cell labels even if the user has specified
values on a PD card. If these labels are desired, then use the preview
plotter cell-label capability discussed in §7.3.2.1.

LEVEL n

Plot only the n th level of a repeated structure geometry. A negative
entry (DEFAULT) plots the geometry at all levels. If user-supplied n is
greater than the

| WWN [n] : P   | Cell labels will be weight windows for time or energy index n (or combined time-energy index n ) for particle type P . The n is optional and defaults to 1. Note: When combining time and energy binning, the index n varies as follows: For 3 time bins (T) and 3 energy bins (E), the index, n , would map to the following sequence: (T1, E1), (T1, E2), (T1, E3), (T2, E1), (T2, E2), (T2, E3), (T3, E1), (T3, E2), (T3, E3).   |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EXT: P        | Cell labels will be exponential transform stretching param- eter for particle type P .                                                                                                                                                                                                                                                                                                                                              |
| PD n          | Cell labels will be detector contribution frequency fraction to tally n .                                                                                                                                                                                                                                                                                                                                                           |
| DXC: P        | Cell labels will be DXTRAN contribution frequency frac- tion.                                                                                                                                                                                                                                                                                                                                                                       |
| U             | Cell labels will be universe numbers.                                                                                                                                                                                                                                                                                                                                                                                               |
| LAT           | Cell labels will be the enclosed lattice type.                                                                                                                                                                                                                                                                                                                                                                                      |
| FILL          | Cell labels will be filling universe identification numbers.                                                                                                                                                                                                                                                                                                                                                                        |
| IJK           | Cell labels will be lattice indices.                                                                                                                                                                                                                                                                                                                                                                                                |
| NONU          | Cell labels will be fission behavior toggles.                                                                                                                                                                                                                                                                                                                                                                                       |

PAC [n] : P

When PLOT is called from MCPLOT , cell labels will be values of columns
in PRINT Table 126 [§5.13.3.15]. The n is optional and defaults to 1.

Allowed values of n are:

| PAC1 : P   | The labels are the 'tracks entering' column of Table 126.      |
|------------|----------------------------------------------------------------|
| PAC2 : P   | The labels are the 'population' column of Table 126.           |
| PAC3 : P   | The labels are the 'collisions' col- umn.                      |
| PAC4 : P   | The labels are the 'collisions * weight (per history)' column. |
| PAC5 : P   | The labels are the 'number weighted energy' column.            |
| PAC6 : P   | The labels are the 'flux weighted energy' column.              |
| PAC7 : P   | The labels are the 'average track weight (relative)' column.   |
| PAC8 : P   | The labels are the 'average track mfp (cm)' column.            |

## MBODY state

## MESH n

## FMESH n

number of levels in the geometry, all levels are plotted as if a
negative entry was supplied.

Note: n ≤ 20 .

Where state can be:

| ON   | Display only the macrobody surface number. (DEFAULT)   |
|------|--------------------------------------------------------|
| OFF  | Display the macrobody surface facet numbers.           |

Controls plotting of cell lines, and/or the weight-window or weight-
window generator superimposed mesh.

Always Available:

| n = 0 (No Lines)   | Plot cells not outlined in black.                                    |
|--------------------|----------------------------------------------------------------------|
| n = 1 (CellLine)   | Plot constructive solid geometry cells, outlined in black. (DEFAULT) |

Available when appropriate cards are present:

| n = 2 (WW MESH)   | Plot weight-window superimposed mesh without cell out- lines.   |
|-------------------|-----------------------------------------------------------------|
| n = 3 (WW+Cell)   | Plot weight-window superimposed mesh and cell outlines.         |
| n = 4 (WWG MESH)  | Plot weight-window generator mesh.                              |
| n = 5 (WWG+Cell)  | Plot weight-window generator mesh and cell outlines.            |
| n = 6 (MeshTaly)  | Plot TMESH mesh tally boundaries (RMESH, CORA, etc., required). |
| n = 7 (MT+Cell)   | Plot TMESH mesh tally boundaries + CellLine                     |

The CellLine and No Lines options are always available. WW MESH and
WW+Cell are available only when the WWP card calls for using a
superimposed weight-window mesh (5th entry negative) and a WWINP file is
provided on the MCNP6 execution line. WWG MESH and WWG+Cell are
available only when a MESH card appears in the input and when the WWG
card requests superimposed mesh generation (2nd entry is 0). Similarly,
MeshTaly and MT+Cell are available only when a TMESH mesh tally has been
requested.

Depending on the combination of cards in an input, a user may have a WWP
card, no mesh generation cards, and a TMESH card. In this case, MESH n
for n = 0 to 3 will behave as described, but n = 4 and 5 would be the
MeshTaly and MT+Cell options above and anything above n = 5 would
default to No Lines . Other behavior can occur with different
combinations of input cards. The user is encouraged to experiment and
arrive at an understanding for an input-by-input basis.

Plot FMESH mesh tally n . FMESH off will turn off the mesh tally
plotter.

Changes the layout of the plot depending on the type of mesh tally:

For rectangular meshes, the horizontal axis is in the direction of the
dimension with the greatest number of bins, and the vertical axis is in
the direction of the dimension with the second greatest number of bins.

For cylindrical meshes, the horizontal axis is along the axis of the
cylinder and the vertical axis is along the θ = 0 plane. The center of
the plot in both cases is at the center of the mesh.

Note: To keep the original layout, use the FMESH button of the
interactive plotter instead.

## SCALES n

Put scales, or scales and a grid, on the plot. Scales and grids are
incompatible with VIEWPORT SQUARE .

Note: Scales are centered at the current plot origin and go to plus or
minus EXTENT in both directions.

| n = 0   | Neither scales nor a grid are displayed. (DEFAULT)                          |
|---------|-----------------------------------------------------------------------------|
| n = 1   | Display scales on the edges of the viewport.                                |
| n = 2   | Display scales on the edges of the viewport and overlay an associated grid. |

## CONTOUR cmin cmax cint

The parameters cmin , cmax , and cint are the minimum, maximum, and
interpolation scheme, respectively. All 3 arguments are required: cmin ,
cmax , and cint . If this is not satisfied, the plotter hangs
indefinitely and must be killed. The CONTOUR command is valid for TMESH
mesh tallies only, for FMESH , see §6.3.3.11. The CONTOUR command usage
and syntax is different in MCPLOT [§6.3.3.10].

The expected form of both cmin and cmax changes between cint options ( 1
):

| cint = % or PCT   | If either the % symbol or the PCT keyword is used, cmin and cmax are percentages between the minimum and maximum values of the TMESH tally results. Values between cmin and cmax are linearly interpolated across 10 values. Restriction: 0 ≤ cmin < cmax ≤ 100   |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| cint = LIN        | Behaves similarly to % or PCT , but values specified for cmin and cmax are actual tally values instead of percents. Re- striction: cmin < cmax                                                                                                                    |
| cint = LOG        | Values of cmin and cmax are tally values that are logarith- mically interpolated between. Can result in a smoother color-map than the other two options, especially when there is a large range in data. Restriction: cmin < cmax                                 |
| Special usage:    |                                                                                                                                                                                                                                                                   |
| CONTOUR OFF       | After using the CONTOUR command as described above, re- vert to a default view with CONTOUR OFF . This is the same as CONTOUR MIN _ TMESH MAX _ TMESH LOG . Valid for TMESH mesh tallies.                                                                         |

| COLOR n   | Turn color on or off, set the resolution, or select the physical property for color shading.   | Turn color on or off, set the resolution, or select the physical property for color shading.                                                             | Turn color on or off, set the resolution, or select the physical property for color shading.                                                             |
|-----------|------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
|           | n = ON                                                                                         | Turn color on. (DEFAULT)                                                                                                                                 | Turn color on. (DEFAULT)                                                                                                                                 |
|           | n = OFF                                                                                        | Turn color off.                                                                                                                                          | Turn color off.                                                                                                                                          |
|           | 50 ≤ n ≤ 5000                                                                                  | Set the color resolution to n . A larger value increases resolution (which can better represent color shading along curved interfaces) and drawing time. | Set the color resolution to n . A larger value increases resolution (which can better represent color shading along curved interfaces) and drawing time. |
|           | n = BY aa                                                                                      | Select the physical property to use for geometry shading. Allowed aa options for COLOR BY include:                                                       | Select the physical property to use for geometry shading. Allowed aa options for COLOR BY include:                                                       |
|           |                                                                                                | aa = MAT                                                                                                                                                 | Cell colors will be cell materials. (DEFAULT)                                                                                                            |
|           |                                                                                                | aa = DEN                                                                                                                                                 | Cell colors will be mass density (g/cm 3 ).                                                                                                              |

## SHADE m1 value1 m2 value2 m3 value3 ...

Sets the color of material number m1 to value1 and so on. This command
is only valid when COLOR BY MAT is active (the default with ' COLOR ON
').

Legal entries for valueN are either an integer from 1-64 or one of the
color names that are displayed with the HELP (or ? or OPTIONS ) command.
The integers map to the color names by row first, then column (top to
bottom, left to right). For example, SHADE 1000 4 and SHADE 1000 green
both set material 1000 to green. See Fig. 6.2 for a list of colors.
Note: color names are case-sensitive.

## Details:

- 1 For all valid combinations of cmin , cmax , and cint , a description of the TMESH tally's minimum and maximum values are given to the right of the text ' contour plot values: '. Similarly, the range of the values that are covered by colors in the plotter are shown to the right of the ' colors: ' text. The interpolation scheme and number of histories follows. This is helpful to query useful minimums and maximums of cmin and cmax respectively.

## 6.2.4.1.5 View Manipulation Commands

View manipulation commands redefine the origin, bases, and extent
relative to the current view origin, bases, and extent. The new origin,
bases, and extent will be used for all subsequent plots until they are
again redefined, either by view manipulation commands or by plot
commands such as ORIGIN . The view manipulation commands are usually
used to zoom in on some feature of the plot.

| aa = RHO        | Cell colors will be atom density (barn - 1 · cm - 1 ).            |
|-----------------|-------------------------------------------------------------------|
| aa = TMP        | Cell colors will be temperature (MeV).                            |
| aa = CEL        | Cell colors will be cell numbers.                                 |
| aa = IMP: P     | Cell colors will be cell importances for particle type P .        |
| aa = GRADIENT , | use a continuous gradient of 256 colors to show the color values. |
| aa = SOLID ,    | use a solid color to represent a range of cell values.            |

When DEN , RHO , TMP , or IMP: P is used, the geometry will be shaded
using the color GRADIENT mode. Linear interpolation between the minimum
non-zero value and the maximum value is used to select the color. If
shading by cell importance and if the minimum and maximum importance
varies enough, then logarithmic interpolation is used. A color bar
legend of the shades will be drawn in the left margin. The legend is
labeled with the property name and the minimum and maximum values. See
Fig. 6.1 for an example of coloring by mass density ( DEN ). Coloring by
material ( MAT ) or cell ( CEL ) does not invoke the color bar legend.

Figure 6.2: Available MCNP Plotter Colors for SHADE

<!-- image -->

| 1 VioletRed (208, 31, 144) (0.816, 0.125, 0.565) 2 5 cyan (0, 255, 255) (0.0, 1.0, 1.0) 9 brown (164, 42, 42) (0.647, 0.165, 0.165) 13 chartreuse (126, 255, 0) (0.498, 1.0, 0.0) 17 firebrick (177, 33, 33) (0.698, 0.133, 0.133) 21 maroon (175, 47, 95) (0.69, 0.188, 0.376) 25 seashell (255, 245, 237) (1.0, 0.961, 0.933) 29 turquoise (64, 223, 208) (0.251, 0.878, 0.816) 33 DarkGoldenrod (184, 133, 10) (0.722, 0.525, 0.043) 37   | blue (0, 0, 255) (0.0, 0.0, 1.0) 6 orange (255, 164, 0) (1.0, 0.647, 0.0) 10 SlateGray (111, 128, 144) (0.439, 0.502, 0.565) 14 magenta (255, 0, 255) (1.0, 0.0, 1.0) 18 gold (255, 214, 0) (1.0, 0.843, 0.0) 22 orchid (218, 111, 213) (0.855, 0.439, 0.839) 26 sienna (159, 82, 44) (0.627, 0.322, 0.176) 30 wheat   | 3 yellow (255, 255, 0) (1.0, 1.0, 0.0) 7 pink (255, 192, 202) (1.0, 0.753, 0.796) 11 azure (239, 255, 255) (0.941, 1.0, 1.0) 15 coral (255, 126, 80) (1.0, 0.498, 0.314) 19 honeydew (239, 255, 239) (0.941, 1.0, 0.941) 23 goldenrod (218, 164, 31) (0.855, 0.647, 0.125)   | 4 green (0, 255, 0) (0.0, 1.0, 0.0) 8 purple (159, 31, 239) (0.627, 0.125, 0.941) 12 burlywood (222, 184, 134) (0.871, 0.722, 0.529) 16 cornsilk (255, 248, 220) (1.0, 0.973, 0.863) 20 khaki (239, 230, 139) (0.941, 0.902, 0.549) 24 plum (221, 159, 221) (0.867, 0.627, 0.867)   |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                        | 27 thistle (215, 190, 215) (0.847, 0.749, 0.847)                                                                                                                                                                                                                             | 28 tomato (255, 98, 70) (1.0, 0.388, 0.278)                                                                                                                                                                                                                                         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                              | (245, 222, 179) (0.961, 0.871, 0.702)                                                                                                                                                                                                                                                                                  | 31 salmon (249, 128, 113) (0.98, 0.502, 0.447)                                                                                                                                                                                                                               | 32 CadetBlue (95, 158, 159)                                                                                                                                                                                                                                                         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                              | 34 DarkOliveGreen (84, 107, 46)                                                                                                                                                                                                                                                                                        | 35 SlateBlue (106, 90, 205)                                                                                                                                                                                                                                                  | (0.373, 0.62, 0.627) 36 DarkOrange (255, 139, 0) (1.0, 0.549, 0.0)                                                                                                                                                                                                                  |
| DarkOrchid (153, 49, 204) (0.6, 0.196, 0.8) 41 DeepSkyBlue (0, 190, 255) (0.0, 0.749, 1.0) 45 LightGoldenrod (237, 221, 130)                                                                                                                                                                                                                                                                                                                 | (0.333, 0.42, 0.184) 38 DarkSeaGreen (143, 187, 143) (0.561, 0.737, 0.561) 42 AntiqueWhite                                                                                                                                                                                                                             | (0.416, 0.353, 0.804) 39 DarkSlateGray (46, 79, 79) (0.184, 0.31, 0.31) 43 LavenderBlush (255, 239, 245)                                                                                                                                                                     | 40 DeepPink (255, 19, 146) (1.0, 0.078, 0.576) 44 LightBlue (172, 215, 230) (0.678, 0.847,                                                                                                                                                                                          |
| (0.933, 0.867, 0.51) 49 LightSkyBlue                                                                                                                                                                                                                                                                                                                                                                                                         | (249, 235, 214) (0.98, 0.922, 0.843) 46 LightPink (255, 182, 193) (1.0, 0.714, 0.757)                                                                                                                                                                                                                                  | (1.0, 0.941, 0.961) 47                                                                                                                                                                                                                                                       | 0.902)                                                                                                                                                                                                                                                                              |
| (134, 206, 249) (0.529, 0.808, 0.98)                                                                                                                                                                                                                                                                                                                                                                                                         | 50 LightYellow (255, 255, 223)                                                                                                                                                                                                                                                                                         | DodgerBlue (30, 144, 255) (0.118, 0.565, 1.0) 51 MediumOrchid (185, 84, 210)                                                                                                                                                                                                 | 48 LightSalmon (255, 159, 121) (1.0, 0.627, 0.478) 52 LightSteelBlue                                                                                                                                                                                                                |
| (1.0, 1.0, 53 MediumPurple (146, 111, 219) (0.576, 0.439, 0.859)                                                                                                                                                                                                                                                                                                                                                                             | 0.878) 54 OrangeRed (255, 69, 0) (1.0, 0.271, 0.0)                                                                                                                                                                                                                                                                     | (0.729, 0.333, 0.827) 55 PaleGreen (151, 250, 151) (0.596, 0.984, 0.596)                                                                                                                                                                                                     | (175, 196, 222) (0.69, 0.769, 0.871) 56 PaleTurquoise (174, 237, 237) (0.686, 0.933,                                                                                                                                                                                                |
| 57 PaleVioletRed (219, 111, 146)                                                                                                                                                                                                                                                                                                                                                                                                             | 58 LightCyan (223, 255, 255) (0.878, 1.0, 1.0)                                                                                                                                                                                                                                                                         | 59 RoyalBlue (65, 105, 224)                                                                                                                                                                                                                                                  | 0.933) 60 RosyBrown (187, 143, 143)                                                                                                                                                                                                                                                 |
|                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                        | (0.255, 0.412, 0.882)                                                                                                                                                                                                                                                        | (0.737, 0.561, 0.561)                                                                                                                                                                                                                                                               |
| (0.859, 0.439, 0.576) 61 SkyBlue                                                                                                                                                                                                                                                                                                                                                                                                             | 62 SpringGreen                                                                                                                                                                                                                                                                                                         | 63 SteelBlue (70, 130, 180)                                                                                                                                                                                                                                                  | 64                                                                                                                                                                                                                                                                                  |
| (134, 206, 235)                                                                                                                                                                                                                                                                                                                                                                                                                              | (0, 255, 126) (0.0, 1.0, 0.498)                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                     |
|                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                        | (0.275, 0.51, 0.706)                                                                                                                                                                                                                                                         | red (255, 0, 0)                                                                                                                                                                                                                                                                     |
| (0.529, 0.808, 0.922)                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                     |
|                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                              | (1.0, 0.0,                                                                                                                                                                                                                                                                          |
|                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                              | 0.0)                                                                                                                                                                                                                                                                                |

| CENTER dh dv   | Change the origin of the plot by the amount dh in the horizontal direction and by the amount dv in the vertical direction. This command is usually used to define the center of a portion of the current plot that the user wants to enlarge.                                                                                                                                                                                                                                                                                                                                                                                                               |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FACTOR f       | Enlarge the plot by the factor 1/ f . The parameter f must be greater than 10 - 6 .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| THETA th       | Rotate the plot counterclockwise by the angle th , in degrees. Negative values rotate the plot clockwise.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| CURSOR         | Present the graphics cursor and prepare to receive cursor input from the user. This command is available only if the system has graphics (X Windows [§6.1]) capability. After entering this command, left-click on the plot window. The cursor changes shape to appear like the upper left corner of a box. Click in the plot window at a point representing the upper left spatial boundary of the desired plot. The cursor will change shape again; now click the lower right position of the desired plot. The plot will be redrawn using the new boundaries and keep a 1:1 aspect ratio. This is equivalent to an EXTENT command and an ORIGIN command. |
| RESTORE        | Restore the origin and extent to the values they had before the most recent CURSOR command. The RESTORE command should be the only command on the input line. It cannot be used to undo the effects of the CENTER , FACTOR , and THETA commands.                                                                                                                                                                                                                                                                                                                                                                                                            |

## 6.2.5 Plotting Embedded-mesh Geometries

The MCNP6 plotter supports color-shaded plotting of the materials, mass
density, or atom density of an imported embedded mesh. For these cases,
the values from the external mesh geometry file (typically a LNK3DNT or
Abaqus-style file) are used; these values may vary element to element.

When the geometry is plotted with COLOR BY DEN (mass density) or COLOR
BY RHO (atom density), each mesh element is shown in one solid color.
The element net value is plotted, i.e., the net mass density or net
number density of the element. The color distribution is set by the
minima and maxima. These net values are also the values reported for
plot queries when DEN or RHO is selected from the right-hand-side
interactive menu [§6.2.3.3].

If MAT is selected from the right-hand-side interactive menu, clicking
on a spot containing multiple materials will randomly select which
material to report. Repeatedly clicking on such a spot may show
different materials on different clicks. Void elements in the mesh are
not shaded (i.e., shown as white) on material plots.

## 6.2.6 Geometry Debugging

Surfaces appearing on a plot as red dashed lines usually indicate that
the geometry is improperly defined. A geometry error can arise when a
region has been defined in more than one cell or a particular region has
never been defined. These geometry errors must be corrected.

Dashed or incomplete lines also can occur because the plot plane is
coincident with a plot surface. In this case, the terminal will issue a
warning. The plot plane should be moved so it is not coincident with any
geometry surface.

Dashed lines may also indicate a cookie cutter cell (red dashes) or a
DXTRAN sphere (blue dashes). These are not errors.

11/01/21 10:55:00

Dashed Lines Example

Figure 6.3: Different types of Dashed Lines

<!-- image -->

## 11/01/2110:58:03 Dashed Lines Example

Figure 6.4: Dashed Lines with no Geometry Errors

<!-- image -->
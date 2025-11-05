---
title: "Chapter 6.3 - The Tally and Cross-Section Plotter, MCPLOT"
chapter: "6.3"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/6_MCNP_Geometry_and_Tally_Plotting/6.3_The_Tally_and_Cross-Section_Plotter,_MCPLOT.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

In Figure 6.3 and 6.4, both geometry errors and cookie cutter cells are
represented with the same red dashed line. Thus, the reason for dashed
lines on an MCNP6 geometry plot must be understood before running a
problem.

When checking a geometry model, errors may not appear on the two-
dimensional slice chosen, but one or more particles may get lost in
tracking. To find the modeling error, use the coordinates and trajectory
of the particle when it got lost (listed in the output file). Entering
the particle coordinates as the ORIGIN and the particle trajectory as
the first BASIS vector with any other non-colinear vector as the second
BASIS vector will result in the plotter centered on the point the
particle was lost with the horizontal direction of the plot consistent
with the direction the particle was moving.

## /warning\_sign Caution

In some cases, particles may be lost in a lattice but entering the
ORIGIN and BASIS as described above will not display any broken geometry
lines. In these cases, the user has likely not fully specified the
geometry universes filling the lattice. Just as the top level universe
must have all regions of space defined, the sub universes should be
fully defined. If the user is still losing particles, surfaces of
filling universes should be made non-coincident with surfaces on the
filled lattice cells.

## 6.2.7 Geometry Plotting in Batch Mode

Although MCNP6 can be run in a batch environment, user interaction with
the plotter is significantly reduced. Rather than entering commands
manually in this environment, it is recommended to use the NOTEK option
on the MCNP6 execution line and read a command file with the COM option.
Every view plotted will be put in a local graphics file. See §6.2.1 for
more information on NOTEK and the COM execute options.

## 6.3 The Tally and Cross-Section Plotter, MCPLOT

Tally results and cross-section data are plotted by MCNP6 through the
MCPLOT module. It can draw ordinary two-dimensional x -y plots and
contour or color-filled tally plots of three-dimensional data. MCPLOT
supports a wide variety of plot options including plotting data linearly
or logarithmically, manipulation of the axes limits, and data
coplotting. Tally plots can be created from tally data that exists
within a MCTAL or RUNTPE file. However, when plotting from a MCTAL file,
not all options are available because not all the information is
available in that format.

In addition to plotting tally results, MCPLOT plots cross-section data
specified in an INP file. Either individual nuclides or the complete
material composed of constituent nuclei properly weighted by atomic
fraction may be plotted. The data plotted reflect adjustments to the
cross sections made by MCNP6 such as energy cutoffs, neutron cross-
section temperatures, S ( α, β ) treatment, the summation of photon
reactions to provide a total photon cross section, simple physics
treatment for photon data, electron stopping powers, and more. Cross-
section plots cannot be made from a RUNTPE file.

Final tally results can be plotted after particle transport has
finished. The temporary status of one or more tallies can also be
displayed during the calculation as transport is ongoing. After
transport is finished, MCPLOT is invoked by typing a Z on the MCNP6
execution line, and reading an existing RUNTPE or MCTAL file. The RUNTPE
file may be read as an execution line option or after invoking the tally
plotter. The MCTAL file may only be read after invoking the tally
plotter.

## MCNP6 Z RUNTPE= filename

or

MCNP6 Z then type runtpe= filename at the MCPLOT&gt; prompt.

or, for a MCTAL file:

MCNP6 Z then type rmctal= filename at the MCPLOT&gt; prompt.

To superimpose a mesh tally with problem geometries, initiate MCPLOT
using one of the execute lines above and then enter the geometry plotter
using the PLOT command. A RUNTPE file must be read to obtain the mesh
tally data.

There are two ways to request that a plot be produced periodically
during the run: use an MPLOT card in the INP file or use the TTY
interrupt feature [§3.3.3]. Note: The TTY interrupt capability is not
always possible during parallel computations, particularly when using
MPI parallelization.

The TTY interrupt, Ctrl + c , m , causes MCNP6 to pause at the end of
the history that is running when the interrupt occurs and allows plots
to be made by calling MCPLOT . During run-time plotting, no output is
sent to the COMOUT file. In addition, the following commands cannot be
used after invoking MCPLOT with an interrupt: RMCTAL , RUNTPE , and DUMP
. The END or RETURN commands are used to exit MCPLOT and return MCNP6 to
transport mode. Cross-section data cannot be displayed after a TTY
interrupt or by use of the MPLOT card.

Mesh tally, radiography tally, and lattice tally results can be
displayed as color contour plots. Mesh tallies can also be plotted
superimposed over problem geometries. All of these plots are done in
MCNP6 without the need of auxiliary post-processing codes.

MCPLOT can make tally plots on a machine different from the one on which
the problem was run by using the MCTAL file. When the INP file has a
PRDMP card with a non-zero third entry, a MCTAL file is created at the
end of the run. The MCTAL file is an ASCII file that contains all the
tally data in the last RUNTPE dump. When the MCTAL file is created, its
name can be specified in the execute line using the following format:

## MCNP6 I= inpfile MCTAL= filename

If the MCTAL option is omitted, the default filename is a unique name
based on MCTAL : First MCTAL , then MCTAM , then MCTAN and so on.

The MCPLOT HELP command provides an alphabetized columnar listing of
options [333]. Below the listing of commands are instructions describing
how to:

1. invoke a listing of all HELP commands with an explanation of their function and use syntax ( HELP ALL ),
2. provide a listing of function and syntax for a single command ( HELP command ),
3. request an overview of the MCPLOT capability ( HELP OVERVIEW ), and
4. summarize input and execution-line options ( HELP EXECUTE ).

See §6.4 for examples of using MCPLOT .

## 6.3.1 Execution Line Options Related to MCPLOT Initiation

To run only MCPLOT and plot tallies upon termination of the calculation
by MCNP6, enter the following command:

## MCNP6 Z KEYWORD[=value(s)]

where Z invokes MCPLOT . Cross-section data cannot be plotted by this method. The allowed keywords are:

| NOTEK            | Suppress plotting at the terminal and send all plots to the graphics metafile, PLOTM . The NOTEK keyword is used for production and batch situations or when the user's terminal has no graphics capability.                                                                                                                                                                                                                            |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| COM= filename    | Use file filename as the source of plot requests. When an end-of-file (EOF) is read, control is transferred to the terminal. In a production or batch situation, end the file with an END command to prevent transfer of control. Never end the COM file with a blank line. If COM is absent, the terminal is used as the source of plot requests.                                                                                      |
| RUNTPE= filename | Read file filename as the source of MCNP6 tally data. The default file name is runtpe.h5 . If the default restart file does not exist, the user will be prompted at the MCPLOT> prompt to read a restart file with the RUNTPE command.                                                                                                                                                                                                  |
| PLOTM= filename  | Name the graphics metafile filename . The default metafile is a standard postscript file and named plotm.ps . In the absence of a specified metafile name, MCNP6 increments the last character until it runs out of unique names: plotm.ps , plotn.ps , ploto.ps , . . . , plotl.ps . Unique names for the output file, PLOTM , will be chosen by MCNP6 to avoid overwriting existing files.                                            |
| COMOUT= filename | Write all plot requests to file filename . The default name is comout . PLOT writes the COMOUT file in order to give the user the opportunity to do the same plotting at some later time, using all or part of the old COMOUT file as the COM file in the second run. In the absence of a specified COMOUT filename, MCNP6 increments the last character until it runs out of unique names: comout , comouu , comouv , . . . , comous . |

To run transport, plot cross-section data, and tallies in one line, use
the execution line:

## MCNP6 INP= filename IXRZ KEYWORD[=value(s)]

This causes MCNP6 to run the problem specified in filename , following
which the prompt MCPLOT&gt; appears for MCPLOT commands. At this point,
both cross-section data and tallies can be plotted.

Cross-section data cannot be plotted after a TTY interrupt or by use of
the MPLOT card.

To plot only cross-section data, use the execute line command:

## MCNP6 INP= filename IXZ KEYWORD[=value(s)]

The problem cross sections are read in, but no transport occurs. When
using this method to plot cross sections, the following commands cannot
be used: BAR , CONTOUR , DUMP , FREQ , HIST , PLOT , RETURN , RMCTAL ,
RUNTPE , SPLINE , WASH , and WMCTAL .

1

2

```
1 2
```

## 6.3.1.1 MCPLOT Basic Concepts

Plot requests are entered from the terminal or they can be read from a
file. A plot is requested on the terminal by entering a sequence of plot
commands at the MCPLOT&gt; prompt. The request is terminated with the Enter
key. Commands consist of keywords usually followed by some parameters,
either space or comma delimited. Command keywords, but not parameters,
can be abbreviated to any degree not resulting in ambiguity, but they
must be correctly spelled. The maximum line length is 128 characters. If
the line is terminated with the &amp; character, the command string may be
continued on the next line.

Note that the &amp; character may only break a string between subsequent
commands and not between the values entered for a command. For example:

```
xlim 1e-8 1e-4 & ylim 1e-5 1e-1
```

is valid, while

```
xlim 1e-8 & 1e-4 ylim 1e-5 1e-1
```

is invalid.

Termination of a line with the COPLOT command will wait to draw the plot
until the next string of commands is terminated with the Enter key. Only
those commands marked with a dagger ( † ) in the list presented in
§6.3.3 can be used after the first COPLOT command in a plot request
because the others affect the framework of the plot or are for contour
or 3-D plots only.

When MCNP6 is run with just Z as the execute line option ( mcnp6 z ),
the code will attempt to locate and read the file runtpe.h5 . If this
file is present and has more than one energy bin in a tally, a default
plot is obtained by pressing the Enter key once MCPLOT&gt; prompt is
displayed. This default is a lin-log histogram plot of the lowest
numbered tally in tally / MeV against energy, with error bars and
suitable labels. If any of these default requirements are unsatisfied a
message to that degree will be printed to the terminal window.

In this Section, the term 'current plot' means the plot that is being
defined by the commands currently being typed in, which might not be the
plot that is showing on the screen.

## 6.3.2 Plot Types Available in MCNP6

## 6.3.2.1 2-D Plot

The origin of coordinates for two-dimensional MCPLOT plots is at the
lower-left corner of the picture. The horizontal axis is called the x
-axis. It is the axis of the independent variable such as user bin, cell
number, or energy. The vertical axis is called the y -axis. It is the
axis of the dependent variable such as flux, current, or dose. Each axis
can independently be either linear or logarithmic.

## 6.3.2.2 Contour Plot

Similarly, the origin of coordinates for MCPLOT contour plots is at the
lower-left corner of the picture. The horizontal axis is called the x
-axis. It is the axis of the first of the two independent variables. The
vertical axis is called the y -axis. It is the axis of the second
independent variable. The contours represent the values of the dependent
variable. For contour plots, only linear axes are available. Each
contour is drawn in a different color depending on its value with
respect to the z -value extrema. Extensions to the FREE and CONTOUR
commands allow for shaded contour plots of tally and mesh data.

For additional examples involving contour plots see §6.4.2 and §6.4.3.

## 6.3.2.3 Color-wash Plot

This plot option is similar to contour plotting, but instead of drawing
contours of z ( x, y ) data, each tally bin is filled with a color
selected by the tally value in the bin. The axis conventions are the
same as in contour plotting. This option is selected with the command
WASH . If two free variables have been selected with the FREE command, a
color-filled plot is drawn. This is a useful option for radiography
tallies. The color index is selected by linear interpolation between the
z -minimum and the z -maximum values.

## 6.3.3 Tally Plot Commands Grouped by Function

A dagger ( † ) indicates a command can be used after the first COPLOT
command in a plot request.

## 6.3.3.1 Device-control Commands

Normally MCPLOT draws plots to a system's X Window display. By using the
following commands, the user can specify that plots not be drawn to the
display and/or that they be sent to a graphics metafile or PostScript
file for processing later by a graphics utility program.

| TERM n   | Output device type is specified by n . n =0 for a terminal with no graphics forwarding capability (for a system without the X Window System). No plots are drawn to a display window, and all plots are sent to the graphics metafile. TERM 0 is equivalent to putting NOTEK on MCNP6's execution line [§6.3.1]. n =1 restores the plotting window on the next plot request.   | Output device type is specified by n . n =0 for a terminal with no graphics forwarding capability (for a system without the X Window System). No plots are drawn to a display window, and all plots are sent to the graphics metafile. TERM 0 is equivalent to putting NOTEK on MCNP6's execution line [§6.3.1]. n =1 restores the plotting window on the next plot request.   |
|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FILE aa  | Send or do not send plots to the graphics metafile PLOTM.PS according to the value of the parameter aa . The graphics metafile is not created until the first FILE command is entered. FILE has no effect in the NOTEK or TERM 0 cases.                                                                                                                                        | Send or do not send plots to the graphics metafile PLOTM.PS according to the value of the parameter aa . The graphics metafile is not created until the first FILE command is entered. FILE has no effect in the NOTEK or TERM 0 cases.                                                                                                                                        |
|          | The allowed values of aa are the following:                                                                                                                                                                                                                                                                                                                                    | The allowed values of aa are the following:                                                                                                                                                                                                                                                                                                                                    |
|          | aa is blank                                                                                                                                                                                                                                                                                                                                                                    | Only the current plot is sent to the graphics metafile.                                                                                                                                                                                                                                                                                                                        |
|          | aa =ALL                                                                                                                                                                                                                                                                                                                                                                        | The current plot and all subsequent plots are sent to the metafile until another FILE command is entered.                                                                                                                                                                                                                                                                      |
|          | aa =NONE                                                                                                                                                                                                                                                                                                                                                                       | The current plot is not sent to the metafile nor are any subsequent plots until another FILE command is entered.                                                                                                                                                                                                                                                               |

## 6.3.3.2 General Commands

| &         | Continue reading commands for the current plot from the next input line. The & must be the last character on the line. The & command must not break another command and its parameters onto two lines; instead, it is used to continue long user command strings on new lines. †                                                                                                                                |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| COPLOT    | Plot a curve according to the commands entered so far and keep the plot open for co-plotting one or more additional curves. COPLOT is effective for 2-D plots only. If COPLOT is the last command on a line, it functions as if it were followed by an & . Only the commands followed by a dagger ( † ) in this section are valid to enter following COPLOT .                                                   |
| FREQ n    | Use with the MPLOT card; has no effect when MCPLOT is called through the Z execution option. Specifies the interval between calls to MCPLOT to be every n histories. In a KCODE cal- culation, the interval is every n cycles. If n is negative, the interval is in CPU minutes. If n = 0 , MCPLOT is not called while MCNP6 is running histories. Note: An 8-byte integer is allowed for n . (DEFAULT: n = 0 ) |
| RETURN    | If MCPLOT was called by MCNP6 while running histories or by PLOT while doing geometry plotting, control returns to the calling subroutine. Otherwise RETURN has no effect.                                                                                                                                                                                                                                      |
| PLOT      | Call or return to the PLOT geometry plotter. This cannot be done when plotting from a MCTAL file.                                                                                                                                                                                                                                                                                                               |
| PAUSE [n] | Can be used on any line of a plot command file that is specified with the execute COM= filename option [§6.3.1]. Holds each view for n seconds. If no n value is provided, each view remains until Enter is pressed. When absent, the commands specified in the command file will run sequentially until the end of the command file is reached at which point control returns to the terminal.                 |
| END       | Terminate execution of PLOT . Closes any open X Windows and returns the terminal from the PLOT prompt to a standard system shell prompt.                                                                                                                                                                                                                                                                        |

## 6.3.3.3 Inquiry Commands

When one of these commands is encountered, the requested display is made
and then MCPLOT waits for the user to enter another line, which can be
just pressing the Enter key, before resuming. The same thing will happen
if MCPLOT sends any kind of warning or comment to the user as it
prepares the data for a plot.

OPTIONS or ? or HELP OPTIONS or ? may be interchanged in: †

| HELP [COMMAND]   | Display a list of available MCPLOT commands or the help text of the specified MCPLOT command. While this can be convenient for a quick reminder of the usage of the command, this Manual should be referenced as some of the help text provided by this option is out of date.   |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| HELP OVERVIEW    | Display a description of the MCPLOT module akin to the introduction of this Section (§6.3).                                                                                                                                                                                      |
| HELP EXECUTE     | Display help text for MCPLOT input and execution-line op- tions.                                                                                                                                                                                                                 |

†

## /warning\_sign Caution

The HELP EXECUTE text incorrectly implies that RMCTAL is an execution
line option in MCNP6.

## /warning\_sign Caution

While the HELP [COMMAND] functionality can be useful for quick syntax
checks, some of the help-text is out of date or incorrect. The user
should primarily refer to this manual for instruction on using the tally
plotter module. Please email mcnp\_help@lanl.gov if there is a
discrepancy in the functionality of a command.

| STATUS              | Display the current values of the plotting parameters including the name of the file being plotted from, tally number, bin information, and more. †                                                                                                                             |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PRINTAL             | Display the available tally numbers in the current RUNTPE or MCTAL file. †                                                                                                                                                                                                      |
| IPTAL               | Display the IPTAL array for the current tally. The command prints how many bins are in each dimension of the current 8-dimensional tally. This helps remind the user of how the tally is setup and may eliminate the need to reference the input file. †                        |
| PRINTPTS [filename] | Display the x - y coordinates and the relative error of the points in the current plot. PRINTPTS is not available for co-plots, contour plots, color-wash plots, or 3-D plots. Print to the terminal (default behavior) or to the file named filename (optional, if specified). |

## 6.3.3.4 File Manipulation Commands

| RUNTPE filename [n]   | Read dump n from RUNTPE file filename . If the parameter n is omitted, the last dump in the file is read. †   |
|-----------------------|---------------------------------------------------------------------------------------------------------------|
| DUMP n                | Read dump n of the current RUNTPE file. †                                                                     |
| WMCTAL filename       | Write the tally data in the current RUNTPE dump to MCTAL file filename . †                                    |
| RMCTAL filename       | Read tally data from MCTAL file filename .                                                                    |

Read tally data from MCTAL file filename . †

## 6.3.3.5 Parameter-setting Commands

Parameters entered for one curve or plot remain in effect for subsequent
curves and plots (including co-plots) until they are either reset to
their default values with the RESET command or are overridden, either by
the same command with new values, by a conflicting command, or by the
FREE command that resets many parameters. There are two exceptions:
FACTOR and LABEL are effective for the current curve only. An example of
a conflicting command is BAR , which turns off HIST , PLINEAR , and
SPLINE .

| TALLY n   | Define tally n as the current tally. †                                                                                                                                                                                                                                                                                                                                                    |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|           | The parameter n is the tally designation on the F card in the INP file of the problem represented by the current RUNTPE or MCTAL file. The default is the first tally in the problem: which is the lowest numbered neutron tally or, if there are no neutron tallies, the lowest numbered photon tally or, if there are no neutron or photon tallies, the lowest numbered electron tally. |

| PERT n         | Plot a perturbation associated with the current tally, where n corresponds to a PERT n card. † The command PERT 0 will reset PERT n .                                                                                                                                                                                                                                                                                                                                                 |
|----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| LETHARGY       | Divide tally bin by lethargy bin width for log energy abscissa. Produces visually accurate area plots for a 2-D logarithmic energy abscissa ( FREE E ). A lethargy-normalized plot is equivalent to plotting e · f ( e ) . Note: LOGLIN or LOGLOG must be specified and NONORM must not be invoked. See §6.5.                                                                                                                                                                         |
| NONORM         | Suppress bin normalization. The default in a 2-D plot is to divide the tallies by the bin widths if the independent variable is cosine, energy, or time. Bin structure is described in the description of the MCTAL file [§6.3.4]. Bin normalization is not done in 3-D, contour, or color-wash plots.                                                                                                                                                                                |
| FACTOR a f [s] | Multiply the data for axis a by the factor f (restriction: f > 0 ) and then add the term s . † The parameter a is a cartesian axis: X , Y , or Z . The parameter s is optional and defaults to 0.                                                                                                                                                                                                                                                                                     |
| RESET aa       | Reset the parameters of command aa to their default values. † The parameter aa can be a parameter-setting command or ALL . If aa is ALL , the parameters of all parameter-setting commands are reset to their default values. After a COPLOT command, only ALL or any of the parameter-setting commands that are marked with a † in this list may be reset. Resetting ALL while COPLOT is in effect causes the next plot to be an initial plot of the most recently read RUNTPE file. |

## 6.3.3.6 Titling Commands

The use of quotation marks is required for character strings that have
whitespace within them.

| TITLE n "aa"      | Use aa as line n of the main title at the top of the plot. The allowed values of n are 1 and 2. The maximum length of aa is 40 characters. The default is the comment on the FC card for the current tally, if any. Otherwise it is the name of the current RUNTPE or MCTAL file plus the name of the tally. KCODE plots have their own special default title.   |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BELOW             | Put the title below the plot instead of above it. The keyword BELOW has no effect on 3-D plots.                                                                                                                                                                                                                                                                  |
| SUBTITLE x y 'aa' | Write subtitle aa at location x , y , which can be anywhere on the plot including outside the plot as long as it is within the limits of the X Window. The values of x and y are x - and y -axis values. The maximum length of aa is 40 characters.                                                                                                              |
| XTITLE 'aa'       | Use aa as the title for the x -axis. The default is the name of the variable represented by the x -axis. The maximum length of aa is 40 characters.                                                                                                                                                                                                              |

| YTITLE 'aa'   | Use aa as the title for the y -axis. The default is the name of the variable represented by the y -axis. The maximum length of aa is 40 characters.                                                                                                                                                                                                                                                                                     |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ZTITLE 'aa'   | Use aa as the title for the z -axis in 3-D plots. The default is the name of the variable represented by the z -axis. The maximum length of aa is 40 characters.                                                                                                                                                                                                                                                                        |
| LABEL 'aa'    | Use aa as the label for the current curve. † The label is printed in the lower right of the plot window beside a sample of the line style used to plot the curve. The maximum length of aa is 10 characters. The value of LABEL reverts to its default value, blank, after the current curve is plotted. If LABEL is blank, the name of the RUNTPE or MCTAL file being plotted is printed as the label for the curve.                   |
| FONT ax title | Use to adjust font size for plot axes ( ax ) and title(s) ( title ). Allowable values for the parameters are dependent on the user's system, but cannot exceed 100% ( ax , title = 1 ). Default: FONT 0.4375 0.6667 . Example: FONT 0.3 0.7 sets the axis labels to 30% and the title to 70% of their maximum. Example: FONT j 0.5 uses previously specified value for the axis font (or default) and sets the title to 50% of maximum. |

## 6.3.3.7 Plot-Variable Control Commands

Tallies in MCNP6 are binned according to the values of eight independent
variables:

| F   | Tally bins on an F tally (cell, surfaces, or detector),                 |
|-----|-------------------------------------------------------------------------|
| D   | Total vs. direct or flagged vs. unflagged contributions (see CF , SF ), |
| U   | User-defined bins. For example, FT TAG bins (§5.9.18.13),               |
| S   | Segment bins on an FS card,                                             |
| M   | Multiplier bins from an FM card,                                        |
| C   | Cosine bins from a C card,                                              |
| E   | Energy bins from an E card,                                             |
| T   | Time bins from a T card.                                                |

Note: Other cards may affect binning of the eight dimensions. The reader
should reference §5.9 for more information.

Because only one or two of those variables can be used as independent
variables in any one plot, one or two of the eight independent variables
have to be designated as free variables, and the rest become fixed
variables. Fixed values (bin numbers) are defaulted for all fixed
variables, but may be explicitly overridden. The default value for each
fixed variable is the total bin, if present; otherwise the first is
used.

## FREE x[y] [nXm] [ALL|NOALL]

Use variable x ( y blank) or variables x and y as the independent
variable or variables in the plot. Valid values for x and y are the
tally bin indices F , D , U , S , M , C , E , T , I , J , and K , where
I , J , and K refer to lattice or mesh indices. If only x is specified,
2-D

## FIXED q n

## SET f d u s m c e t

plots are made. If both x and y are specified, contour, color-wash, or
3-D plots are made, depending on whether 3-D is in effect. The default
value of x is E , and gives a 2-D plot in which the independent variable
is energy.

The nXm (' n by m ') entry specifies the number of bins associated with
the I and J lattice indices. Only valid when x = I , J , or K or when xy
is a combination of of those indexes.

The ALL entry specifies that the minimum and maximum contour range
should be taken from all the tally bins. Only valid when x = I , J , or
K or when xy is a combination of of those indexes. Omitting this
parameter results in the default minimum and maximum contour range,
which includes only those tally values contained in the specified 2-D
plot.

The NOALL entry specifies that the minimum and maximum contour range
should be taken only from those of the FIXED command slice. (DEFAULT)

The FREE command resets XTITLE , YTITLE , ZTITLE , XLIMS , YLIMS , HIST
, BAR , and PLINEAR to their defaults.

For more information regarding usage of the FREE command, see §6.3.3.12.

Set n as the bin number for fixed variable q . † The symbols that can be
used for q , are F , D , U , S , M , C , E , T , I , J , and K , where I
, J , and K refer to lattice or mesh indices. Restriction: Only the J
and K indices are allowed for a 1-D IJK plot and only the K index is
allowed for a 2-D IJK contour plot.

Define which variables are free and define the bin numbers of the fixed
variables.

SET effectively executes the FREE and several FIXED commands in one
compact command.

The value of each parameter can be either a bin number (the
corresponding variable is then a fixed variable) or an asterisk ( * )
(the corresponding variable is then a free variable). If there is only
one * , 2-D plots are made. If there are two, contour plots are made.
SET performs the same resetting of parameters that FREE does.

TFC info Plot the tally fluctuation chart of the current tally. Unless
otherwise noted, the independent variable is nps , the number of source
histories.

Allowed values of info include the following:

| M   | Mean*                                                                                                                          |
|-----|--------------------------------------------------------------------------------------------------------------------------------|
| E   | Relative fractional uncertainty*                                                                                               |
| F   | Figure of merit* (See §2.6.5)                                                                                                  |
| L   | 201 largest tallies vs x (Unnormalized tally density vs x ; the PDF of the tally. See §5.13.3.18.)                             |
| N   | Cumulative number of scores in TFC bin under consider- ation (Cumulative f ( x ) vs x ; the CDF of the tally. See §5.13.3.19.) |
| P   | TFC bin PDF probability f ( x ) vs x ( NONORM for number frequency vs x .)                                                     |
| S   | Slope of the Pareto fit for high tallies as a function of nps                                                                  |
| T   | Cumulative tally fraction of f ( x ) vs x                                                                                      |
| V   | Variance of the variance as a function of nps                                                                                  |
| 1-8 | 1st to 8th moments of x 1 - 8 · f ( x ) vs x ( NONORM for x 1 - 8 · ∆ x f ( x ) vs x .)                                        |

·

1

1c-8c 1st to 8th cumulative moments of 1 -8 vs

* These data are available when plotting from a MCTAL file.

- KCODE i The independent variable is the KCODE cycle. The individual estimator plots start with cycle one. The average col/abs/track-length plots start with the fourth active

Plot k eff or removal lifetime according to the value of i :

cycle. †

| 1       | k eff (collision)                                                                                                                                 |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| 2       | k eff (absorption)                                                                                                                                |
| 3       | k eff (track)                                                                                                                                     |
| 4       | Depends on value of FMAT on the KOPTS card:                                                                                                       |
|         | FMAT=yes The k eff of the fission matrix solu- tion.                                                                                              |
| 5       | Depends on value of FMAT on the KOPTS card:                                                                                                       |
|         | FMAT=no Prompt removal lifetime (absorp- tion).                                                                                                   |
|         | FMAT=yes Shannon entropy of the fission ma- trix solution.                                                                                        |
| 6       | Shannon entropy of fission source distribution. Can be plotted only from a runtape file, not from a MCTAL file.                                   |
| 11 - 15 | The quantity corresponding to i - 10 , averaged over the cycles so far in the problem.                                                            |
| 16      | Average collision/absorption/track-length k eff and one esti- mated standard deviation.                                                           |
| 17      | Average collision/absorption/track-length k eff and one esti- mated standard deviation by cycle skipped. Cannot plot fewer than 10 active cycles. |
| 18      | Average collision/absorption/track-length k eff figure of merit                                                                                   |
| 19      | Average collision/absorption/track-length k eff relative frac- tional uncertainty.                                                                |

## 6.3.3.8 Cross-section Plotting Commands

The cross section plotter is initiated with the IXZ option on the
execution line:

mcnp6 ixz i=inputfile

Cross section plots cannot be made from a runtape or MCTAL file.

XS m

Plot a cross section according to the value of m . Where m is one of: †

M

n

A material card in the input file for material n . For example: XS M15
for the total cross-section. The available materials will be listed if a
material is requested that does not exist in the INP file.

x · f ( x ) x

|               | Z A                                                                                                                                                      | table identifier [§1.2.3]. Example: XS 92235.00C . The full identifier with extension must be provided. Only the tables requested in the input file may be plotted. The available tables will be listed if a table is requested that does not exist in the input file.   |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MT n          | Plot reaction n of material or nuclide specified by XS m . †                                                                                             | Plot reaction n of material or nuclide specified by XS m . †                                                                                                                                                                                                             |
| PAR P         | file will be listed if a reaction number that is invalid or doesn't exist is entered (e.g., 999) Plot the data for particle type P , of material M n . † | file will be listed if a reaction number that is invalid or doesn't exist is entered (e.g., 999) Plot the data for particle type P , of material M n . †                                                                                                                 |
| 6.3.3.9 2-D   | Plotting Commands                                                                                                                                        | Plotting Commands                                                                                                                                                                                                                                                        |
|               | Use linear x -axis and linear y -axis. (DEFAULT for tally contour plots)                                                                                 | Use linear x -axis and linear y -axis. (DEFAULT for tally contour plots)                                                                                                                                                                                                 |
| LINLOG        | Use linear x -axis and logarithmic y -axis. (DEFAULT for all except tally contour plots)                                                                 | Use linear x -axis and logarithmic y -axis. (DEFAULT for all except tally contour plots)                                                                                                                                                                                 |
| LOGLIN        | Use logarithmic x -axis and linear y -axis.                                                                                                              | Use logarithmic x -axis and linear y -axis.                                                                                                                                                                                                                              |
| LOGLOG        | x y                                                                                                                                                      | x y                                                                                                                                                                                                                                                                      |
| XLIMS min max | Use logarithmic -axis and logarithmic -axis.                                                                                                             | Use logarithmic -axis and logarithmic -axis.                                                                                                                                                                                                                             |
| YLIMS min max | [nsteps] Define the lower limit: min , upper limit: max , and (optionally) number of subdivisions: nsteps , on the x -axis. [nsteps]                     | [nsteps] Define the lower limit: min , upper limit: max , and (optionally) number of subdivisions: nsteps , on the x -axis. [nsteps]                                                                                                                                     |
|               | are determined automatically. Put scales on the plots according to the value of n :                                                                      | are determined automatically. Put scales on the plots according to the value of n :                                                                                                                                                                                      |
| SCALES n      | 0 No scales on the edges and no grid. 1                                                                                                                  |                                                                                                                                                                                                                                                                          |
|               | plot. Make histogram plots. †                                                                                                                            | plot. Make histogram plots. †                                                                                                                                                                                                                                            |
| HIST          | 2 Scales on the edges and a grid on                                                                                                                      | Scales on the edges (DEFAULT). the                                                                                                                                                                                                                                       |
|               | is the default if the independent variable is cosine, energy, or                                                                                         | time.                                                                                                                                                                                                                                                                    |
|               | This                                                                                                                                                     | This                                                                                                                                                                                                                                                                     |

| PLINEAR        | Make piecewise, linear plots. † This is the default if the independent variable is not cosine, energy, or time.                                                                                                                                                                                                                                                                                                                                                                                                            |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BAR            | Make bar plots. †                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| NOERRBAR       | Suppress default error bars. †                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| THICK x        | Set the thickness of the plot curves to the value x . † The legal values are x ≥ 0 . 01 and the default value of n is 0.02.                                                                                                                                                                                                                                                                                                                                                                                                |
| THIN           | Set the thickness of the plot curves to the legal minimum of 0.01. †                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| LEGEND [x] [y] | Include or omit the legend according to the values of optional parameters x and y . If neither x nor y is specified, put the legend in its normal place at the right side of the plot window. (DEFAULT) If x = 0 and y is blank, omit the legend. If both x and y defined, for 2-D plots only, put most of the legend (restart file, tally bin information, etc) in the default location, but place the line labels at location x, y , where the values of x and y are based on the units and values of the x and y -axes. |

## 6.3.3.10 Contour-plot Commands

The CONTOUR command can be used to examine 3-D data such as plots of
TMESH tallies, or from a FREE command calling out two free tally
dimensions. The general form of the contour command is:

## CONTOUR cmin cmax cstep [scheme]

The parameters cmin , cmax , and cstep are the minimum, maximum, and
step values for contours, respectively. The optional scheme parameter is
the interpolation scheme between cmin and cmax . The cstep parameter
varies based on scheme. The default is CONTOUR 5 95 10 % .

Options for the scheme parameter are:

| scheme = % or PCT   | The first two parameters ( cmin , cmax ) are interpreted as percentages of the range between the minimum and maximum value of the dependent variable. The cstep parameter is the stride between drawn levels and dictates how many levels exist between cmin and cmax . Example: CONTOUR 5 95 10 % sets the lower contour level at 5% of the range of the tally and the upper level at 95% with a stride of 10% between drawn contours (5%, 15%, 25%, . . . , 95%).   |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| scheme = LIN        | The first two parameters ( cmin , cmax ) are actual values of the tally. The cstep parameter is the stride in terms of the actual values of the tally. Example: CONTOUR 1e-4 1e-1 1e-2 LIN sets the lower contour level at 1 × 10 - 4 and the upper level at 1 × 10 - 1 with steps of 1 × 10 - 2 for a total of 11 values: 1 × 10 - 4 , 1 . 01 × 10 - 2 , 2 . 01 × 10 - 2 , 3 . 01 × 10 - 2 , . . . , 2 × 10 - 2                                                      |
| scheme = LOG        | The first two parameters ( cmin , cmax ) are actual values of the tally and the cstep parameter sets the number of logarithmically spaced values to draw contours be- tween. Values of cmin and cmax are defaulted internally when the user first requests CONTOUR LOG . The default cstep is 10. Example: CONTOUR 1e-4 1e-1 4 LOG draws contours between 1 × 10 - 4 , 1 × 10 - 3 , 1 10 - 2 , and 1 10 - 1 .                                                         |

Example: CONTOUR 1e-4 1e-1 4 LOG draws contours between 1 × 10 -4 , 1 ×
10 -3 , 1 × 10 -2 , and 1 × 10 -1 .

Special uses of CONTOUR :

| CONTOUR   | [ALL|NOALL]     |                                                                                                                    |                                                                                                                    |
|-----------|-----------------|--------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
|           |                 | ALL                                                                                                                | Specifies that the minimum and maximum contour range should be taken from all of the tally bins                    |
|           |                 | NOALL                                                                                                              | Sets the minimum and maximum contour range from the bins in the current plot (DEFAULT)                             |
| CONTOUR   | [LINE|NOLINE]   |                                                                                                                    |                                                                                                                    |
|           |                 | LINE                                                                                                               | Draws lines at each contour level (DEFAULT)                                                                        |
|           |                 | NOLINE                                                                                                             | Does not draw lines at contour levels                                                                              |
| CONTOUR   | [COLOR|NOCOLOR] |                                                                                                                    |                                                                                                                    |
|           |                 | COLOR                                                                                                              | The contour plot is colored between the contour values (DEFAULT)                                                   |
|           |                 | NOCOLOR                                                                                                            | The contour plot is uncolored and just displays lines at the contour levels                                        |
| WASH      | aa              | Set or unset z ( x, y ) plotting to use color-wash instead of contours. The parameter aa can be one of two values: | Set or unset z ( x, y ) plotting to use color-wash instead of contours. The parameter aa can be one of two values: |
|           |                 | aa = ON                                                                                                            | Turn on color-wash plotting for two free variables                                                                 |
|           |                 | aa = OFF                                                                                                           | Turn off color-wash plotting and return to contour plotting for two free variables. (DEFAULT)                      |

Any value for aa other than ON is equivalent to OFF .

## 6.3.3.11 FMESH Mesh Tally Plot Commands

MCNP6 uses the geometry plotter to display the results of the FMESH mesh
tally.

The default view depends on the geometry of the mesh tally. For
rectangular mesh tallies, the horizontal axis is in the direction of the
dimension with the most number of bins, and the vertical axis is in the
direction of the dimension with the second most number of bins. For
cylindrical mesh tallies, the horizontal axis is along the axis of the
cylinder and the vertical axis is along the θ = 0 plane.

The center of the plot in both cases is at the center of the mesh.
Different views are obtained by using the MCNP6 geometry plotter
commands [§6.2.3 and §6.2.4]. Exiting the mesh tally plotter will return
control to the tally plotter interface.

Note: there are two ways to change the FMESH tallies that are plotted.
One way is to use the FMESH button of the interactive plotter command
panel [§6.2.3.2]. This will change the mesh tally that is drawn, but not
the plot attributes ( BASIS , EXTENT , and ORIGIN ). In other words,
using the button will not center the view on the center of the new mesh
with the horizontal and vertical axes described above. The second method
is to enter the FMESH n command in the command box. This will reset the
plot layout to the default for that particular mesh tally.

The only FMESH tally plotting related command accessible directly from
MCPLOT is the FMESH n command. The others are input in the command box
in the interactive geometry plotter after a mesh tally is drawn.

1

## FMESH n

## FMRELERR [n]

## ZLEV scale [n1 n2]

Plot FMESH tally n .

Plot the relative errors of the current FMESH tally if the parameter n
is not provided. The tally number n does not need to match the current
FMESH tally number, so the plot will show the relative error for the
requested tally.

Controls the visualization of the FMESH tally results. The parameters ni
are optional and set the range of the scale:

| scale = LOG ,   | the tally data scaling is set to logarithmic. (DEFAULT)   |
|-----------------|-----------------------------------------------------------|
| scale = LIN ,   | the tally data scaling is set to linear.                  |
| n1 ,            | the lower limit of the tally scale.                       |
| n2 ,            | the upper limit of the tally scale.                       |

If only n1 is provided, n2 is defaulted to the maximum value of the
plot. If neither n1 nor n2 are provided, the range is reset. The default
value of scale or the last value of scale is stored by MCPLOT and the
form of ZLEV can simply be:

zlev n1 n2

The ZLEV command can also be used to set discrete values to plot without
a gradient. The form of this usage is:

zlev n1 n2 n3 ... ni

|        | To get discrete values, there must be at least 3 values of ni provided.                                                                                                                                       |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EBIN n | Plot energy bin n of the current FMESH tally. The total energy bin is the last bin of the tally (e.g., if there are three energy bins in an FMESH tally, the total energy bin can be requested with EBIN 4 ). |
| TBIN n | Plot time bin n of the current FMESH tally. Similar to the energy bins, the total time bin is the last bin of the tally.                                                                                      |

## 6.3.3.12 Additional Guidance When Using the FREE Command

The FREE command, described in §6.3.3.7, can be used to plot TMESH or
lattice tallies with the I , J , and K parameters.

For TMESH tallies, the I , J , and K parameters of the FREE command
refer to the CORA , CORB , and CORC mesh-tally dimensions.

For lattice tallies, the I , J , and K parameters of the FREE command
refer to i , j , and k lattice indices.

For radiography tallies, the command FREE S C is used to make a contour
plot of the radiograph's s and t axes.

For lattice tallies that are not fully specified, the n X m dimensions
must be provided (e.g. ' FREE IJ 5X3 '). Mesh and radiography tallies
are always specified fully, so [nXm] is never required for them.

One-dimensional mesh, radiography, and lattice tallies may be specified
by giving the free dimension of the FREE command and fixing the other
two dimensions:

FREE I FIXED J=10 FIXED K=12

## 6.3.4 MCTAL Files

A MCTAL file contains the tally data of one dump of a RUNTAPE file. It
can be written by the MCRUN module of MCNP6 or by the MCPLOT module, by
other codes, or even by hand in order to send data to MCPLOT for co-
plotting with MCNP6 tally data. Data from TMESH mesh tallies are written
to the MCTAL file; however, data from FMESH mesh tallies are not.

As written by MCNP6, a MCTAL file has the format described in §6.3.4.1,
but only as much of it as is essential to contain the information of
real substance is necessary. Furthermore the numerical items do not need
to be in the columns implied by the formats as long as they are in the
right order and are blank delimited. For example, to give MCPLOT a table
of some value and the associated error versus energy, the user might
write a file as simple as the following (note: the file is case-
sensitive):

1

2

3

4

5

<!-- image -->

| e       | 7                                      |
|---------|----------------------------------------|
|         | .2 .4 .7 1 3 8 12                      |
| 4.00E-5 | .022 5.78E-4 .054 3.70E-5 .079 1.22E-5 |
| 7.60E-6 | .187 2.20E-6 .245 9.10E-7 .307         |

If more than one independent variable is desired, other lines such as a
t line followed by a list of time values would be needed and the table
of tally/error values would need to be expanded. If more than one table
of tally/error values is wanted, the file would have to include an ntal
line followed by a list of arbitrarily chosen tally numbers, a tally
line, and lines to describe all of the pertinent independent variables
would have to be added for each table.

The order of expansion of the value/error table depends on the
independent variables. For example, with two time bins and n energy
bins, the order of the values would be: val ( e 1 , t 1 ) , val ( e 1 ,
t 2 ) , val ( e 2 , t 1 ) , val ( e 2 , t 2 ) , . . . , val ( e n , t 1
) , val ( e n , t 2 ) .

When the limits on permitted cell and surface numbers were expanded to
99,999,999, the formatting of MCTAL files was modified to accommodate
these values. The cell and surface numbers for the problem are first
checked to see if any are greater than 99,999. If not, then the
traditional formatting is used when writing the MCTAL file. If there are
numbers greater than 99,999, then (I10) format is used instead for these
integers written to the MCTAL file. Although the MCTAL file is defined
to be free-format, some simple user-written utility programs that read
the MCTAL file may expect fixed format. If such user-written programs
cannot be modified to handle the larger integers, then users should be
careful to use only numbers less than 99,999 for cell and surface
numbers in their input files.

## 6.3.4.1 Form of the MCTAL File

The (case sensitive) form of the MCTAL file as written by MCNP6 with the
PRDMP card is as follows:

## 6.3.4.1.1 Header Information

code \_ name ver probid knod nps rnr (A8,3x,A5,A19,I11,1x,I20,1x,I15) (or
(A8,3x,A5,A19,I5,1x,I15,1x,I15) if knod and nps are smaller), where code
\_ name

is the name of the code, MCNP6.

| ver    | is the version, e.g., 6.3.                                                                                          |
|--------|---------------------------------------------------------------------------------------------------------------------|
| probid | is the date and time when the problem was run and, if it is available, the designator of the machine that was used. |
| knod   | is the dump number.                                                                                                 |
| nps    | is the number of histories that were run.                                                                           |
| rnr    | is the number of pseudorandom numbers that were used.                                                               |

One blank followed by columns 1-79 of the problem identification
(1x,A79) line, which is the first line in the problem's input file.

ntal n npert m (A5,I11,A6,I11) (or (A5,I5,A6,I5) if n and m are
smaller), where

| n   | is the number of tallies in the problem.       |
|-----|------------------------------------------------|
| m   | is the number of perturbations in the problem. |

List of the tally numbers, on as many lines as necessary. (16I5 1 )

## 6.3.4.1.2 Tally Information

If there are tallies in the problem, the following information is
written for each tally:

tally m i j k (A5,I4 2 ,T20,I21,2I5) where

| m   | is the problem name of the tally, one of the numbers in the list after the ntal line.                                                                                                                                 | is the problem name of the tally, one of the numbers in the list after the ntal line.                                                                                                                                 |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| i   | If i > 0 , then i is the particle type: 1=N, 2=P, 3=N+P, 4=E, 5=N+E, 6=P+E, 7=N+P+E, where N=neutron, P=photon, E=electron. If i < 0 , then i is the number of particle types and the next MCTAL line will list which | If i > 0 , then i is the particle type: 1=N, 2=P, 3=N+P, 4=E, 5=N+E, 6=P+E, 7=N+P+E, where N=neutron, P=photon, E=electron. If i < 0 , then i is the number of particle types and the next MCTAL line will list which |
| j   | is the type of detector tally with values                                                                                                                                                                             | is the type of detector tally with values                                                                                                                                                                             |
|     | 0                                                                                                                                                                                                                     | none,                                                                                                                                                                                                                 |
|     | 1                                                                                                                                                                                                                     | point,                                                                                                                                                                                                                |
|     | 2                                                                                                                                                                                                                     | ring,                                                                                                                                                                                                                 |
|     | 3                                                                                                                                                                                                                     | pinhole radiograph ( FIP ),                                                                                                                                                                                           |
|     | 4                                                                                                                                                                                                                     | transmitted image radiograph (rectangular grid, FIR ),                                                                                                                                                                |
|     | 5                                                                                                                                                                                                                     | transmitted image radiograph (cylindrical grid, FIC )                                                                                                                                                                 |
| k   | is tally modifier information with values                                                                                                                                                                             | is tally modifier information with values                                                                                                                                                                             |
|     | 0                                                                                                                                                                                                                     | none                                                                                                                                                                                                                  |
|     | 1                                                                                                                                                                                                                     | for * modifier                                                                                                                                                                                                        |
|     | 2                                                                                                                                                                                                                     | for + modifier                                                                                                                                                                                                        |

List of 37 entries indicating which particle types are used by the
tally. (40I2). This is only present if particle type value ( i ) above
is negative. Entries follow the order of particles listed in Table 4.3
and are 1 if the particle is present in the tally and 0 if it is not.

The FC card lines, if any, each starting with 5 blanks. (5x,A75)

f n (A2,1x,I7) where n is the number of cell, surface, or detector bins.
For repeated-structures tallies, the F -bins have an i, j, k index which
goes like: ( i 1 , j 1 , k 1 ) , ( i 2 , j 1 , k 1 ) , . . . , ( i n , j
1 , k 1 ) , ( i 1 , j 2 , k 1 ) , ( i 2 , j 2 , k 1 ) , . . . , ( i n ,
j 2 , k 1 ) , . . . , ( i 1 , j m , k 2 ) , ( i 2 , j m , k 2 ) , . . .
, ( i n , j m , k 2 ) , etc. This order is reflected in the vals section
of the MCTAL file.

List of the cell or surface numbers, on as many lines as necessary.
(11I7 3 ) If a cell or surface bin is made up of several cells or
surfaces, a zero is written. This list is omitted if the tally is a
detector tally.

d n (A2,1x,I7) where

n is the number of total vs. direct or flagged vs. unflagged bins. For
detectors, n = 2 unless there is an ND on the F5 card; for cell and
surface tallies, n = 1 unless there is an SF or CF card. u n or ut n or
uc n (A2,1x,I7) where n is the number of user bins, including the total
bin if there is one. If there is only one unbounded bin, n = 0 instead
of 1. If there is a total bin, the line begins with ' ut '. If there is
cumulative binning, the line begins with ' uc '. These conventions
concerning a single unbounded bin and the total bin also apply to the s
, m , c , e , and t lines below. s n or st n or sc n (A2,1x,I7) where n
is the number of segment bins. If the tally is a radiograph tally, then
a list of the bin boundaries will be printed. m n or mt n or mc n
(A2,1x'I7) where n is the number of multiplier bins. c n f or ct n f or
cc n f (A2,1x,I7,I4) where n is the number of cosine bins. 3 This field
is increased for big problems (cells or surfaces &gt; 99,999).

f

is an integer flag.

If f = 0 or is absent, the cosine values in the following list are
histogram bin upper boundaries. Otherwise they are the discrete points
where the tally values ought to be plotted and the values are not
divided by the bin widths (see NONORM , §6.3.3.5). The e and t entries
have similar flags. This integer flag is not written by MCNP6 but can be
added to hand-written MCTAL files.

List of cosine values, on as many lines as necessary. (6ES13.5)

e n f or et n f or ec n f (A2,1x,I7,I4) where n is the number of energy
bins.

List of energy values, on as many lines as necessary. (6ES13.5)

t n f or tt n f or tc n f (A2,1x,I7,I4) where n is the number of time
bins.

List of time values, on as many lines as necessary. (6ES13.5)

vals values (A4,4(ES13.5,F7.4)) or vals pert values (A10,4(ES13.5,F7.4))
where values

is a list of tally value-error data pairs, on as many lines as
necessary. The order of the values is that of a 9-dimensional Fortran
array if it were dimensioned (2,NT,NE,...,NF) where NT is the number of
time bins, NE is the number of energy bins, . . . , and NF is the number
of cell, surface, or detector bins. In other words, time bins are under
energy bins, which are under cosine bins, . . . , which are under the
cell, surface, or detector bins. Values printed in this list are exactly
the same as those in the problem's OUTP file.

tfc n jtf (A4,I4,8(1x,I7)) (or (A4,I11,8(1x,I11)) if bins are large),
where

```
n is the number of sets of tally fluctuation data. jtf is a list of 8 numbers, the bin indexes of the tally fluctuation chart bin (see TF card)
```

nps mean error fom (1x,I14,3ES13.5) (or (1x,I20,3ES13.5) for large
problems), where

| nps   | is the histories run at the time of the TFC dump   |
|-------|----------------------------------------------------|
| mean  | is the mean of the tally                           |
| error | is the tally error                                 |
| fom   | is the tally figure of merit                       |

This is the end of the information written for each standard tally.

## 6.3.4.1.3 Superimposed Mesh Tally Type A Information

If a problem contains a TMESH tally, the ntal entry in the general tally
information will reflect the numbers of any TMESH tallies, and the
following information is written:

tally nugd -j -j8 (A5,3I5), where

| nugd   | is the mesh tally number                     | is the mesh tally number                     |
|--------|----------------------------------------------|----------------------------------------------|
| j      | is the number of particles in the mesh tally | is the number of particles in the mesh tally |
| j8     | is the mesh type:                            | is the mesh type:                            |
|        | 1                                            | rectangular                                  |
|        | 2                                            | cylindrical                                  |
|        | 3                                            | spherical                                    |

List of 37 entries indicating which particle types are used by the
tally. (40I2). Entries follow the order of particles listed in Table 4.3
and are 1 if the particle is present in the tally and 0 if it is not.

f

mxgc

0

ng1

ng2

ng3

(A2,I8,4I5), where

```
mxgc is the total number of spatial bins (or 'voxels') in the TMESH tally. ng1 is the number of bins on the CORA card ng2 is the number of bins on the CORB card ng3 is the number of bins on the CORC card List of CORA bin values on as many lines as necessary (6ES13.5). List of CORB bin values on as many lines as necessary (6ES13.5). List of CORC bin values on as many lines as necessary (6ES13.5). d 1 (A2,I8) u 1 (A2,I8) s mxgv (A2,I8), where mxgv is the number of S bins on the tally from different keywords. For example, mxgv = 1 ' RMESH1: P FLUX ' and mxgv = 3 for ' RMESH3 TOTAL DE/DX RECOL ' m 1 (A2,I8) c 1 (A2,I8) e 1 (A2,I8) t 1 (A2,I8) vals values (4(ES13.5,f7.4)), where
```

```
for
```
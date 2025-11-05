---
title: "Appendix E.4 - Gridconv (gridconv)"
chapter: "E.4"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.4_Gridconv_(gridconv).pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## E.4 Gridconv ( gridconv )

The gridconv program is a post-processing code used with mdata and mctal
output files. Gridconv converts the data in these files to formats
compatible with various external graphics packages. Those permitted are:

| IDL ®   | IDL (Interactive Data Language) is a product of Harris Geospatial Solutions, Inc. (https://www.l3harrisgeospatial.com/Software-Technology/IDL)   |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Tecplot | Tecplot is a product of Tecplot, Inc. (https://www.tecplot.com)                                                                                  |
| Gnuplot | Freeware. (http://www.gnuplot.info). Only 1D and 2D plots supported.                                                                             |

## /warning\_sign Caution

GRIDCONV has historically supported the IDL and Tecplot output formats;
however, these output formats have not been tested in modern viewers at
the time of writing.

## E.4.1 User Interface

Gridconv has no command line options. Once started, the code will prompt
the user for the information needed to create the desired formatted
graphics input files.

After the header information from the mdata or mctal file has been read,
gridconv can either produce an ASCII file from the data file or generate
the required graphics input files as requested by the user. Note that
the ASCII file contains raw data not normalized to the number of source
particles. The reason for the option to write an ASCII file is that
sometimes users will want to look at the values in the mdata file before
doing any plotting, or check the numerical results for a test case. The
ASCII option is also useful for porting the data in the mdata file to
another computer platform and for reading the data into graphics
packages not currently supported by gridconv .

Gridconv is currently set up to generate one-, two-, or three-
dimensional graphics input files with any combination of binning
choices. Once the graphics input file has been generated, gridconv gives
the user the option of producing another file from the currently
selected TMESH tally, selecting a different TMESH tally available in
this mdata file, or reading information from a different file. There is
always the option to exit the program.

Gridconv can also process any and all tallies written to the mctal file.
The code is still interactive but now shows all tallies in the problem,
from which any tally may be selected. The user has the option of
generating one- or two-dimensional output. The user is then told about
the bin structure so the one or two free variables may be selected.
Energy is the default independent variable in the one-dimensional case.
There are no default variables for the two-dimensional case. The order
in which the two-dimensional bin variables are selected does not make
any difference to the output; the order of the processing will be as it
appears in the mctal file.
---
title: "Chapter 6.1 - System Graphics Information"
chapter: "6.1"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/6_MCNP_Geometry_and_Tally_Plotting/6.1_System_Graphics_Information.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Chapter 6

## MCNP Geometry and Tally Plotting

MCNP6 has two plotting capabilities. The first, PLOT , is used to plot
two-dimensional slices of the problem geometry specified in the INP
file. The user can perform interactive geometry plotting in two ways:
either 'point-and-click' mode or 'command-prompt' mode. In addition,
generation of plot files can be done in batch mode using a command file.
The second plotting capability, MCPLOT , plots tally results produced by
MCNP6 and cross-section data used by MCNP6. Mesh tallies may be plotted
either in MCPLOT from mctal files or superimposed over geometry plots in
PLOT from runtpe files.

Section 6.1 addresses system issues external to MCNP6 related to
graphics. Section 6.2 discusses how to invoke the PLOT features, whereas
§(6.3) discusses the MCPLOT features. An explanation of each set of
input commands is given. Lines the user will type are shown in
typewriter font. The Enter key must be pressed after each input line.
Although in this section plot options and keywords are shown in UPPER
CASE, they are case insensitive.

## 6.1 System Graphics Information

X Windows is the only graphics system supported by MCNP6. This graphics
library is device-independent in general and gives considerable
flexibility in processing graphical output.

The X-window graphics library (http://www.x.org) allows the user to
send/receive graphics output to/from remote hosts as long as the window
manager on the display device supports the X protocol [e.g., OpenLook
window manager, MOTIF window manager, Cygwin (PC Windows), etc.]. Before
running MCNP6, perform the following steps to use these capabilities.
Note that these steps use UNIX C-shell commands. Other shells may
require different syntax.

1. On the host that will execute MCNP6, enter setenv DISPLAY displayhost:0 where displayhost is the name of the host that will receive the graphics. If the displayhost is the same as the execution host ( executehost ), set DISPLAY to localhost:0 or just :0 .
2. If the two hosts are different, in a CONSOLE window of the display host enter xhost executehost where executehost is the name of the host that will execute MCNP6.

With the setenv or the xhost command, the host IP address can be used in
place of the host name. For example, setenv DISPLAY 128.10.3.1:0 . This
option is useful when one remote system does not recognize the host name
of another.

Note to LANL Users: On some systems, including the Los Alamos Integrated
Computing Network (ICN) and other LANL local area networks, use of the
xhost command is strongly discouraged. This is because it creates a
security problem. In place of using xhost , the secure shell (SSH) can
be used to log into remote
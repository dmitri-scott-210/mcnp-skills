---
title: "Source Primer Chapter 1 - What is this document"
chapter: "Source-1"
source_pdf: "mcnp6-primer-docs/mcnp6-source-primer/1.What_is_this_document.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## 1.1 Introduction

This document contains examples of MCNP general source usage to support
the MCNP6 User's Manual. The examples range from basic to advanced
sources with different applications. There are also examples of how MCNP
can fail and warnings for the users to look for at the output to ensure
proper results are being created.

The overall aim of this document is to provide solid examples of how to
define sources with MCNP as well as how to verify the sources are setup
properly. The reasoning for needing such complex sources is not
discussed in the present work. Also, this document is not meant to be
exhaustive of every MCNP source option and combinations of source
options possible. However, it is intended to frequently update this
document with new source examples provided by users. Please feel free to
contact the MCNP6 development team to learn about how to submit a new or
updated source example. Please include 'General Sources Primer' in the
subject line to route the request to the appropriate developers.

## 1.2 Sources in MCNP

For information on defining sources in MCNP, see the source section
(3.3.4 pg. 3-122) in the MCNP6 User's Manual.

The SDEF card is the generalized user-defined source definition. SDEF
can define particle types (neutrons, photons, electrons, etc.), position
on surfaces and in volumes, direction (beam, isotropic, etc.), and time
distributions for each source particle. SDEF can also have dependent
functions (ERG=FDIR=D1) and sources in repeated structures. In general,
the source variables can be described as a single/discrete value,
independent distribution, or a dependent distribution of another source
variable.

There are many more source options within MCNP, and depending on the
user's applications, these may be very useful. Source biasing can alter
the sampling of probability distribution functions (PDFs), while
adjusting particle weight, in order to sample important particles more
often while sampling less important particles less frequently. Surface
source write and read couples one problem with a complex source
description (SSW) to problems with further calculations (SSR). The SSW
calculation will take the particles from the source that cross user-
defined surfaces and write them to a file. The SSR reads the specified
surface(s) needed from the SSW file and continues the calculations with
proper tallies. Examples of many of these kinds of sources are included
in this document to help user's get started defining complex sources.

## 1.3 Tallies in MCNP

To verify sources in MCNP, the present document uses standard tallies,
seen in the tallies section (3.3.5 pg. 3-176) in the MCNP6 User's
Manual.

## WHAT IS THIS DOCUMENT?

Standard tallies can verify energy, time, cell/surfaces, and direction
(1D) by showing their distributions in the tally/cross section plotter.
Mesh Tallies can show geometry and direction (3D) using the geometry
plotter. Included in this current document are all of the MCNP6-specific
plotting commands so that all of the plots can be reproduced.

Although not discussed in this version of this document, verification of
source accuracy can also be shown using the MCTAL/MESHTAL or PTRAC
features in MCNP. It is generally very easy to generate a MCTAL/MESHTAL
file with MCNP and read and fetch the data using MCNPtools.
Alternatively, PTRAC can be used to write all source events and
MCNPtools can read the data and fetch the state of each source particle
as it is created in MCNP6. These alternative source verification
techniques will be explored in future versions of this document.

## 1.4 Example Source

This examples serve to show how the remainder of this document is
organized. First, a short description of the source example is given.
Second, the full MCNP input file is listed. Third, the tally plots are
shown, each with a short description. Last, the MCNP plotting commands
are given to reproduce the displayed plots.

## 1.4.1 SDEF Defaults

The SDEF card is inserted with only default values.

```
The default SDEF source in a vacuum 100 0 -1 IMP:N=1 $ inside sphere 999 0 1 IMP:N=0 $ outside world 1 SO 1 MODE N NPS 1E6 c SDEF c c F1:N 1 $ ERG and TME tallies E1 1E-6 100ilog 20 T1 0 99i 100 c FMESH4:N GEOM=XYZ $ Geometry source tally ORIGIN=-1 -1 -1 IMESH=1 IINTS=51 JMESH=1 JINTS=51 KMESH=1 KINTS=51 TYPE=SOURCE c FMESH14:N GEOM=XYZ $ Geometry flux tally ORIGIN=-1 -1 -1 IMESH=1 IINTS=51 JMESH=1 JINTS=51 KMESH=1 KINTS=51
```

Listing 1.1: MCNP6 Input File

The energy distribution can be seen below where the default 14 MeV
energy is the only bin with a value.

<!-- image -->

The time distribution can be seen below where the default 0 shake bin is
the only bin with a value.

<!-- image -->

The position of the source can be seen below in the mesh plot where the
origin location (x=0, y=0, z=0) is the only bin with a value.

The position of the flux can be seen below in the mesh plot where the flux is distributed isotropically by default.

<!-- image -->

<!-- image -->

Listing 1.2: MCNP6 Plotting Commands

```
tal 1 loglog free e xlims 1e-3 20 tal 1 linlin free t xlims 0 100 fmesh 4 basis 1 0 0 0 1 0 end fmesh 14 file end end
```

## 1.5 Helpful Links

## 1.5.1 Documents

```
MCNP6 General Source MCNP6 User's Manual An MCNP Primer by Shultis & Faw
```

Primer [PDF of this webpage]

## 1.5.2 Websites

MCNP Website

Python Sphinx Documentation
---
title: "Appendix E.1 - Doppler Broadening Resonance Correction Library"
chapter: "E.1"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.1_Doppler_Broadening_Resonance_Correction_Librar.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## E.1 Doppler Broadening Resonance Correction Library Generation ( dbrc \_ make \_ lib )

In order to use the DBRC capabilities, the code needs access to 0-K
elastic-scattering data. This tool will scan xsdir \_ mcnp6.3 within
DATAPATH for ENDF/B-VII.1 data (with suffix .85c ) and ENDF/B-VIII.0
data (with suffix .05c ) and store them in DBRC \_ endf71.txt and DBRC \_
endf80.txt respectively. These should be moved into the root of DATAPATH
for the code to find them.

## E.1.1 User Interface

This utility has no command line options. If any files the utility is
expecting are missing, it will print out the file it attempted to open
and exit. If any files the utility expected are missing, it will print
out the files it attempted to open and exit.

During operation, the utility will print out some diagnostic data,
including which table is being processed, what file it was found in, the
number of data points, and whether or not unresolved resonances adjusted
the data points extracted. The utility will then note that the data were
written to disk. This process will repeat, once for ENDF/B-VII.1 and
once for ENDF/B-VIII.0.
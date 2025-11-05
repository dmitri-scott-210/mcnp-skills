---
title: "Appendix E.5 - Cross Section Library Manipulation Tool (makxsf)"
chapter: "E.5"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.5_Cross_Section_Library_Manipulation_Tool_(makxs.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## E.5 Cross Section Library Manipulation Tool ( makxsf )

The makxsf code is a utility program for manipulating cross-section
library files for use with the MCNP code and potentially other codes
that make use of A Compact ENDF (ACE) formatted nuclear data files
[344]. It can be used to convert ACE data files between ASCII and binary
formats, to make customized libraries containing selected datasets, and
to create temperature-dependent libraries.

## /warning\_sign Caution

The makxsf utility is no longer actively supported as the capabilities
of this code have been usurped by other openly available software
packages. If people rely on the capabilities of makxsf , please read
about the known issues and alternative solutions in §E.5.2.

## E.5.1 User Interface

As the interface to makxsf has remained unchanged for an extended period
of time, please refer to the user guidance within the 'The makxsf Code
with Doppler Broadening' report [344].

## E.5.2 Known Issues and Alternative Solutions

## Temperature Interpolation of Continuous S ( α, β ) Thermal Scattering Data

The temperature interpolation capabilities are unavailable for use with
the continuous form of the S ( α, β ) thermal scattering data tables.
When makxsf was originally developed, the continuous form of the S ( α,
β ) data did not exist.

Because makxsf was never updated to handle the continuous S ( α, β )
data, the alternative solutions to handling temperature-specific
continuous thermal scattering data include:

- using NJOY [354] to generate S ( α, β ) data at the precise temperature needed.
- using stochastic mixing of S ( α, β ) data to approximate temperature effects (see the MT0 card for more details).
- running bounding calculations with nearest lower and upper temperatures.
- using the nearest-temperature continuous S ( α, β ) data.

## General Temperature Treatments

Both the Doppler broadening implementation used for resolved resonance
data and the temperature interpolation scheme used for unresolved
resonance data and discrete S ( α, β ) thermal scattering data are
approximate methods that have not been updated nor re-validated in
recent years.

It is recommended that people migrate toward using the production NJOY
code [354], available as open-source software
(https://github.com/njoy/NJOY2016), for all of their needs with respect
to processing nuclear data at precise temperatures.
---
title: "Source Primer Chapter 5 - Known Source Errors"
chapter: "Source-5"
source_pdf: "mcnp6-primer-docs/mcnp6-source-primer/5.Known_Source_Errors.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

Dependent source variable combinations that do not work together.

## 5.1 Fatal Error Given

## 5.1.1 Axis as a Function of Position

The axis (AXS) variable cannot be a function of position (POS).

```
SDEF TESTING 10 1 1E-6 -1 IMP:N=1 $ inside sphere 1 20 1 1E-6 -2 IMP:N=1 $ inside sphere 2 30 1 1E-6 -3 IMP:N=1 $ inside sphere 3 40 1 1E-6 -4 IMP:N=1 $ inside sphere 4 50 2 1E-6 -5 1 2 3 4 IMP:N=1 $ inside box 99 0 5 IMP:N=0 $ outside 1 S 2.5 2.5 0 0.5 2 S 7.5 2.5 0 0.5 3 S 2.5 7.5 0 0.5 4 S 7.5 7.5 0 0.5 5 RPP 0 10 0 10 -1 1 MODE N NPS 1e6 PRINT c M1 92235 1 M2 8016 1 1001 2 c FMESH4:N GEOM=XYZ ORIGIN=0 0 -1 IMESH=10 IINTS=200 JMESH=10 JINTS=200 KMESH=1 KINTS=1 TYPE=SOURCE c SDEF POS=D1 AXS=FPOS=D2 EXT=D7 RAD=D8 c SI1 L 2.5 2.5 -0.1 $ POS distribution 7.5 2.5 -0.1
```

Listing 5.1: MCNP6 Input File

## KNOWN SOURCE ERRORS

```
2.5 7.5 -0.1 7.5 7.5 -0.1 SP1 1 1 1 1 c DS2 S 3 4 5 6 c SI3 L 0 0 1 SP3 1 c SI4 L 0 1 0 SP4 1 c SI5 L 1 0 0 SP5 1 c SI6 L 1 1 1 SP6 1 c SI7 0 0.2 SP7 0 1 c SI8 0 0.5 SP8 -21 1
```

Below is the fatal error MCNP will give with the AXS=FPOS dependent
variable in the input file.

Code Name &amp; Version = MCNP6,1.0 Copyright LANS/LANL/DoE - See output
file

<!-- image -->

warning. Physics models disabled.

comment. total nubar used if fissionable isotopes are present.

fatal error. impossible source variable dependencies.

warning.

1 materials had unnormalized fractions. print table 40.

comment. using random number generator  1, initial seed = 19073486328125

imcn isdone xact is done

mcnp ver=6 1d=05/28/1308/01/1708:27:36 Code Name &amp; Version = MCNP6, 1.0
Copyright LANS/LANL/DoE - See output file

## 5.1.2 Surface as a Function of Position

The surface (SUR) variable cannot be a function of position (POS).

```
SDEF TESTING 10 1 1E-6 -1 IMP:N=1 $ inside sphere 1 20 1 1E-6 -2 IMP:N=1 $ inside sphere 2 30 1 1E-6 -3 IMP:N=1 $ inside sphere 3 40 1 1E-6 -4 IMP:N=1 $ inside sphere 4 50 2 1E-6 -5 1 2 3 4 IMP:N=1 $ inside box 99 0 5 IMP:N=0 $ outside 1 S 2.5 2.5 0 0.5 2 S 7.5 2.5 0 0.5 3 S 2.5 7.5 0 0.5 4 S 7.5 7.5 0 0.5 5 RPP 0 10 0 10 -1 1 MODE N NPS 1e6 PRINT c M1 92235 1 M2 8016 1 1001 2 c FMESH4:N GEOM=XYZ ORIGIN=0 0 -1 IMESH=10 IINTS=100 JMESH=10 JINTS=100 KMESH=1 KINTS=1 TYPE=SOURCE c SDEF POS=D1 SUR=FPOS=D2 RAD=D7 c SI1 L 2.5 2.5 0 $ POS distribution 7.5 2.5 0 2.5 7.5 0 7.5 7.5 0 SP1 1 3 5 10 c DS2 S 3 4 5 6 c SI3 L 1 SP3 1 c SI4 L 2 SP4 1 c SI5 L 3 SP5 1 c SI6 L 4 SP6 1 c SI7 L 0.5 SP7 1
```

Listing 5.2: MCNP6 Input File

Below is the fatal error MCNP will give with the SUR=FPOS dependent
variable in the input file.

Code Name &amp; Version = MCNP6,1.0 Copyright LANS/LANL/DoE - See output
file

warning. Physics models disabled.

<!-- image -->

comment.

total nubar used if fissionable isotopes are present.

fatalerror.

impossible source variable dependencies.

warning.

1 materials had unnormalized fractions. print table 40.

comment. using random number generator  1, initial seed = 19073486328125

imcn isdone

xact

is done

mcnp

ver=6 1d=05/28/1308/01/1708:27:36 Code Name &amp; Version = MCNP6, 1.0
Copyright LANS/LANL/DoE - See output file

## 5.2 No Fatal Error Given
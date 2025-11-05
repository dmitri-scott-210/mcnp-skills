---
title: "Appendix E.6 - Merge ASCII Tally Files (merge_mctal.pl)"
chapter: "E.6"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.6_Merge_ASCII_Tally_Files_(merge_mctal.pl).pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## E.6 Merge ASCII Tally Files ( merge \_ mctal.pl )

The merge \_ mctal.pl utility is a command-line interface-based Perl
script that can be used to statistically merge multiple MCNP ASCII tally
( mctal ) files into a single resulting mctal file. MCNP practitioners
are welcome to use this utility as is; however, only limited support is
available for it. Note that a similar C++-based utility with the same
name is provided with the MCNPTools software as of version 5.3.0.

Further documentation can be found in [355].

## E.6.1 User Interface

To run this program, the user should have Perl version 5.8.5 or newer.
All interaction with it is performed in a command-line interface.

The utility can be executed by typing perl merge \_ mctal.pl mctal1
mctal2 etc. at the command line where mctal1 , mctal2 , and any other
such entries form a space-delimited list of MCNP ASCII tally file names.
Alternatively, one can make the script executable and provide the
appropriate Perl path as the first line in the file. In either case, and
optionally, the name of the resulting file can be given with the -o
option such as perl merge \_ mctal mctal1 mctal2 -o mctal.out .

## E.6.2 Example

If one performs two statistically independent but otherwise identical
MCNP calculations using the input shown in Listing E.3 and another
modifying the random number generator as shown in Listing E.4 to produce
ASCII tally files mctal and mctam , respectively, they can be merged
with the command perl merge \_ mctal.pl mctal mctam -o merged \_ mctal.txt
.

The expected output is shown in Listing E.5, where it is important to
note that the merged file has individual tally results merged but the
tally fluctuation chart values are not merged.

```
1 Generate mctal file to merge with another 2 1000 10 -9.98207e-1 -100 imp:n=1 3 9999 0 100 imp:n=0 4 5 100 so 90 6 7 mode n 8 sdef 9 m10 1001.70c 0.666657 $ Pseudo-Water, Liquid @ 23.15 deg-C 10 8016.70c 0.333343 $ Density: 0.998207 g/cc from PNNL-15870, Rev. 1 11 mt10 lwtr.10t 12 f4:n 1000 13 c 14 print 15 prdmp 2j 1 $ Write MCTAL file at conclusion of calculation 16 rand gen=2 seed=12345 17 nps 10000
```

Listing E.3: merge\_mctal1.mcnp.inp.txt

```
16 rand gen=2 seed=34567
```

Listing E.4: merge\_mctal2.mcnp.inp.txt

1

2

3

4

5

```
...Reading MCTAL file: mctal ...Reading MCTAL file: mctam ...Merging (except TFC) ...Creating merged MCTAL file = merged _ mctal.txt
```

Listing E.5: Expected Output from Merging Two ASCII Tally Files

## E.6.3 Change Log

This section describes the evolution of merge \_ mctal.pl .

## Version 1.0, December 2003

- Original release.

## Version 1.1, July 2010

- Added ability to handle MCNP6 mctal formats and larger numbers (up to 99,999,999).

## Version 1.2, January 2022

- Reformatted README file to Markdown. Migrated content to MCNP manual. Revised wording and added example.
- Added .pl file extension.
- Assigned version numbers within utility.
---
title: "Appendix E.7 - Merge Mesh Tally Files (merge_meshtal.pl)"
chapter: "E.7"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.7_Merge_Mesh_Tally_Files_(merge_meshtal.pl).pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

1

2

3

## E.7 Merge Mesh Tally Files ( merge \_ meshtal.pl )

The merge \_ meshtal.pl utility is a command-line interface-based Perl
script that drives a compiled binary based on C++ code can be used to
statistically merge multiple MCNP Type B (MCNP5-style) ASCII mesh tally
( meshtal ) files, such as those created with the FMESH card using the
out = col option, into a single resulting file. Note that only the col
output option provides the format needed by this utility, so newer
output options such as cf , colsci , cfsci , and xdmf are incompatible
with this utility.

MCNP practitioners are welcome to use this utility as is; however, only
limited support is available for it. Note that a similar C++-based
utility with the same name is provided with the MCNPTools software as of
version 5.3.0.

Further documentation can be found in [355].

## E.7.1 User Interface

To run this program, the user should have Perl version 5.8.5 or newer.
All interaction with it is performed in a command-line interface.

The utility can be executed by typing perl merge \_ meshtal.pl meshtal1
meshtal2 etc. at the command line where meshtal1 , meshtal2 , and any
other such entries form a space-delimited list of MCNP ASCII mesh tally
file names. Alternatively, one can make the script executable and
provide the appropriate Perl path as the first line in the file. In
either case, and optionally, the name of the resulting file can be given
with the -o option such as perl merge \_ meshtal.pl meshtal1 meshtal2 -o
meshtal.out .

Note that the merge \_ meshtal \_ one utility that merge \_ meshtal.pl
requires is typically built as a part of the overall MCNP build process
for utilities. However, this file can also be trivially built with most
C++ compilers using a command such as g++ -o merge \_ meshtal \_ one merge
\_ meshtal \_ one.cpp or icpc -o merge \_ meshtal \_ one merge \_ meshtal \_
one.cpp for the GNU and Intel C++ compilers, respectively. Regardless,
the binary merge \_ meshtal \_ one utility must be in the user's path so
it can be called by merge \_ meshtal.pl .

By default, these utilities keep the mesh-tally file together with all
tally numbers present. This behavior can be disabled such that results
for individual tally numbers are split into separate files with the
-split command-line option.

Increased debug-type output can be enabled with the -debug command-line
option.

## E.7.2 Example

If one performs two statistically independent but otherwise identical
MCNP calculations using the input shown in Listing E.6 and another
modifying the random number generator as shown in Listing E.7 to produce
ASCII tally files meshtal and meshtam , respectively, they can be merged
with the command perl merge \_ meshtal.pl meshtal meshtam -o merged \_
meshtal.txt .

The expected output is shown in Listing E.8.

```
Generate meshtal file to merge with another 1000 10 -9.98207e-1 -100 imp:n=1 9999 0 100 imp:n=0
```

Listing E.6: merge\_meshtal1.mcnp.inp.txt

```
4 5 100 so 90 6 7 mode n 8 sdef 9 m10 1001.70c 0.666657 $ Pseudo-Water, Liquid @ 23.15 deg-C 10 8016.70c 0.333343 $ Density: 0.998207 g/cc from PNNL-15870, Rev. 1 11 mt10 lwtr.10t 12 fmesh14:n geom=xyz origin=-50 -50 -50 imesh=50 iints=50 13 jmesh=50 jints=50 14 kmesh=50 kints=50 15 out=col 16 c 17 print 18 rand gen=2 seed=12345 19 nps 10000
```

Listing E.7: merge\_meshtal2.mcnp.inp.txt

```
18 rand gen=2 seed=34567
```

Listing E.8: Expected Output from Merging Two ASCII Mesh Tally Files

10

11

12

13

14

15

16

17

18

```
1 MESHTAL _ FILES: 2 meshtal 3 meshtam 4 5 MESHTAL _ NUMBERS: 6 14 7 8 Processing: 9 meshtal meshtam Combination of mesh tally files completed succesfully. Output stored in merged _ meshtal.txt *** done ***
```

## E.7.3 Change Log

This section describes the evolution of merge \_ meshtal .

## Version 1.0, July 2007

Original development.

## Version 1.1, January 2010

- Extended C++ and Perl compatibility with each other.

## Version 1.2, January 2022

- Reformatted README file to Markdown. Migrated content to MCNP manual. Revised wording and added example.
- Added .pl file extension.
- Assigned version numbers within utility.
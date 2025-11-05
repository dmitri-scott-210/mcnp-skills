---
title: "MCNP6 Primer"
chapter: "Primer"
source_pdf: "mcnp6-primer-docs/MCNP6_Primer.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## AN MCNP6 PRIMER

by

## J. Kenneth Shultis

( jks@ksu.edu )

and

## Amir A. Bahadori

( bahadori@ksu.edu )

Alan Levin Department of Mechanical and Nuclear Engineering Kansas State
University Manhattan, KS 66506

(c) Copyright 2004-2024 All Rights Reserved

## Notice

This primer is a revision of an earlier one for MCNP5 and is intended
for for use by students in our course NE690, Radiation Protection and
Shielding, who are introduced to MCNP for the first time. Thus, this
primer is mainly oriented towards fixed-source, steady-state
applications involving neutrons and photons. The authors acknowledge
that this primer presents only a tiny fraction of the vast capabilities
of MCNP6.

Although this primer is the property of the authors, we give permission
for others to freely copy and distribute it provided no changes are made
to it. We would appreciate receiving error corrections or suggestions
for improvements so that future versions of this primer are enhanced.

A sporadically updated errata for this primer, as well as the primer
itself, can be found on the world wide web at
http://www.mne.ksu.edu/~jks/books.htm . Revised versions, when created,
will also be made available on this web site.

## Contents

| 1 Structure of the MCNP Input File   | 1 Structure of the MCNP Input File                     | 1 Structure of the MCNP Input File                                                                 | 2     |
|--------------------------------------|--------------------------------------------------------|----------------------------------------------------------------------------------------------------|-------|
| 1.1                                  | Annotating the Input File . .                          | . . . . . . . . . . . . . . . . . . . .                                                            | 2     |
| 1.2                                  | Units Used by MCNP . . . . . . . . . . . . . . . . . . | . . . . . .                                                                                        | 3     |
| 2 Geometry                           | Specifications                                         | Specifications                                                                                     |       |
|                                      |                                                        |                                                                                                    | 3     |
| 2.1                                  | Cells - Block 1 .                                      | . . . . . . . . . . . . . . . . . . . . . . . . . . .                                              | 5     |
| 2.2                                  | Macrobodies                                            | . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                          | 6     |
|                                      | 2.2.1 Unstructured Meshes .                            | . . . . . . . . . . . . . . . . . . . .                                                            | 8     |
| 3                                    | Data Specifications - Block 3                          | Data Specifications - Block 3                                                                      | 9     |
| 3.1                                  | Interaction Data Used by MCNP6                         | . . . . . . . . . . . . . . . . .                                                                  | 9     |
| 3.2                                  | Materials Specification - M Card . .                   | . . . . . . . . . . . . . . . .                                                                    | 9     |
| 3.3                                  | Cross-Section Specification                            | . . . . . . . . . . . . . . . . . . . . .                                                          | 11    |
| 3.4                                  | Source Specification .                                 | . . . . . . . . . . . . . . . . . . . . . . . .                                                    | 11    |
|                                      | 3.4.1                                                  | SI: Source Information Card . . . . . . . . . . . . . . . . .                                      | 11    |
|                                      | 3.4.2                                                  | SP: Source Probability Card . . . . . . . . . . . . . . . .                                        | 13    |
| 3.5                                  | Examples of Simple Sources                             | . . . . . . . . . . . . . . . . . . . . .                                                          | 13    |
|                                      | 3.5.1 Point Isotropic Sources . . . .                  | . . . . . . . . . . . . . . .                                                                      | 13    |
|                                      | 3.5.2                                                  | Isotropic Volumetric Sources . . . . . . . . . . . . . . . .                                       | 15    |
|                                      | 3.5.3                                                  | Line and Area Sources (Degenerate Volumetric Sources) .                                            | 15    |
|                                      | 3.5.4                                                  | Monodirectional and Collimated Sources . . . . . . . . . .                                         | 16    |
|                                      | 3.5.5                                                  | Multiple Volumetric Sources . . . . . . . . . . . . . . . . .                                      | 17    |
| 3.6                                  | Tally Specifications .                                 | . . . . . . . . . . . . . . . . . . . . . . . . .                                                  | 19    |
|                                      | 3.6.1 The Surface Current Tally (Type                  | F1 ) . . . . . . . . . . . .                                                                       | 19    |
|                                      | 3.6.2                                                  | The Average Surface Flux Tally (Type F2 ) . . . . . . . .                                          | 20    |
|                                      | 3.6.3                                                  | The Average Cell Flux Tally (Type F4 ) . . . . . . . . . .                                         | 20    |
|                                      | 3.6.4                                                  | Flux Tally at a Point or Ring Detector (Type F5 ) . . . .                                          | 21    |
|                                      | 3.6.5                                                  | Tally Specification Cards . . . . . . . . . . . . . . . . . .                                      | 23    |
|                                      | 3.6.6                                                  | Cards for a Few Optional Tally Features . . . . . . . . . .                                        | 24    |
|                                      | 3.6.7 3.6.8                                            | Miscellaneous Block 3 Commands . . . . . . . . . . . . . Entry . . . . . . . . . . . . . . . . . . | 25 25 |
|                                      | Short Cuts for Data Running MCNP6 . . . .              | Short Cuts for Data Running MCNP6 . . . .                                                          |       |
| 3.7                                  |                                                        | . . . . . . . . . . . . . . . . . . . . . . .                                                      | 25    |
| 4 Variance                           |                                                        |                                                                                                    |       |
|                                      | Reduction                                              | Reduction                                                                                          | 26    |
| 4.1                                  | Tally Variance                                         | . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                            | 26    |
|                                      | 4.1.1 Relative Error and FOM                           | . . . . . . . . . . . . . . . . . . .                                                              | 27    |
| 4.2                                  | Truncation Techniques                                  | . . . . . . . . . . . . . . . . . . . . . . . .                                                    | 27    |
|                                      | 4.2.1 Energy, Time and Weight Cutoff                   | . . . . . . . . . . . . . .                                                                        | 28    |
|                                      | 4.2.2 Physics Simplification                           | . . . . . . . . . . . . . . . . . . . .                                                            | 28    |

5

| 4.3   | 4.2.3                           | Histories and Time Cutoffs . . .    | 30    |
|-------|---------------------------------|-------------------------------------|-------|
|       | Nonanalog                       | Simulation . . . . . . . . . .      | 30    |
| 4.4   | MCNP                            | Variance Reduction Techniques .     | 31    |
|       | 4.4.1                           | Geometry Splitting . . . . . . . .  | 32    |
|       | 4.4.2                           | Weight Windows . . . . . . . . .    | 33    |
|       | 4.4.3                           | An Example . . . . . . . . . . .    | 34    |
|       | 4.4.4                           | Exponential Transform . . . . . .   | 36    |
|       | 4.4.5                           | Energy Splitting/Russian Roulette   | 37    |
|       | 4.4.6                           | Forced Collisions . . . . . . . . . | 37    |
|       | 4.4.7                           | Source Biasing . . . . . . . . . .  | 37    |
| 4.5   | Final Recommendations Output    | . . . . . . . . .                   | 38 38 |
| MCNP  | MCNP                            | MCNP                                |       |
| 5.1   | Output Tables . . .             | . . . . . . . . . . .               | 38    |
| 5.2   | Accuracy versus Precision . .   | . . . . . .                         | 39    |
| 5.3   | Statistics Produced by MCNP . . | . . . .                             | 40    |
|       | 5.3.1                           | Relative Error . . . . . . . . . .  | 40    |
|       | 5.3.2                           | Figure of Merit . . . . . . . . . . | 40    |
|       | 5.3.3                           | Variance of the Variance . . . . .  | 41    |
|       | 5.3.4                           | The Empirical PDF for the Tally     | 41    |
|       | 5.3.5                           | Confidence Intervals . . . . . . .  | 43    |
|       | 5.3.6                           | A Conservative Tally Estimate .     | 43    |
|       | 5.3.7                           | The Ten Statistical Tests . . . .   | 44    |
|       | 5.3.8                           | Another Example Problem . . .       | 44    |

## A Primer Presenting

## AN INTRODUCTION TO THE MCNP6 CODE

J. Kenneth Shultis and Amir A. Bahadori

## Introduction

The MCNP R © Code, developed and maintained by Los Alamos National
Laboratory (LANL), is the internationally recognized code for analyzing
the transport of neutrons and photons. The current MCNP6 code can
simulate the transport of many other radiation particle, namely nine
elementary particles ( γ , e -, e + , µ -, µ + , ν e , ν m , ¯ ν e , ¯ ν
m ), 16 composite particles (n, p, Λ 0 , Σ + , Σ -, Ξ 0 , Ξ -, Ξ + , Ω
-, π + , π -, π 0 , K + , K -, K 0 S , K 0 L ), seven composite
antiparticles (¯ n , ¯ p , Λ 0 , Σ + , Σ -, Ξ 0 , Ω -), four complex
particles (d, t, 3 He, α ) and several hundred heavy ions ( Z = 3 to
92). MCNP is one of the most popular Monte Carlo radiation transport
codes.

Brief Code History The MCNP series of codes has perhaps the longest
history of any Monte Carlo radiation transport code. In the 1950s and
1960s, a number of special purpose Monte Carlo codes, such as MCS, MCN,
MCP, and MCG, were developed at LANL. MCS, MCN, and MCG were merged in
1973 to create MCNG, which was merged with the photon code MCP in 1977
to create the first version of MCNP. In 1983, MCNP3 was released for
public distribution. Between 1986 and 2011, 19 versions of MCNP were
released, each adding additional capability to the code. MCNP6 Beta2 was
released in 2012. This version merged MCNP5 with MCNPX (a variant of
MCNP5 for high-energy applications). Besides the merging of MCNP5 with
MCNPX, 21 new features were incorporated into MCNP6. As a result, MCNP6
has five times the 100k coding lines of MCNP5 and took 12 person-years
of effort. In 2023, MCNP 6.3 was released.

Some of the terminology used in the MCNP documentation betrays the
code's historical origins. For example, the term card , originally an
actual punched card, is now just a line of an electronic input file,
which is still sometimes referred to as an input deck .

Code Documentation The documentation for the MCNP6.3 code is contained
in several Parts. The current version is MCNP6.3 and Parts I through IV
are contained in the technical report Theory &amp; User's Manual [Kulesza et
al., 2022]. Part I of this report (Chs. 1 and 2) gives the theory behind
MCNP6.3. Part II (Chs. 3-8) is the User's Manual : Chs. 3 and 4 present,
respectively, an overview of MCNP6 and the input to the program. Chapter
5 defines all the commands and options that can be used in the code
input; it is essential for both the novice and expert user. Part II ends
with Chs. 6-8 which cover advanced features of geometry and tally
plotting, a new (to MCNP6.3) alternative plotting capability, and
unstructured meshes, respectively. Part III of the Manual (Chs. 9 and
10) contains, respectively, a much more detailed Primer than this humble
offering and a large series of examples of the many features of MCNP6.3.
These examples are extremely helpful to gain experience with the myriad
capabilities of the code. Finally, Part IV comprises six Appendices
describing different file formats, utilities, and useful data.

There is another important part of the MCNP6 documentation that is now
available only with the MCNP6.3 source code package, namely the MCNP
Developer's Guide . 1 This restricted manual gives many of the technical
details of code; however, it is needed by only MCNP experts who want to
alter the code and there is no need for it in this primer.

1 This restriction is a result of Export Control rules.

The 1078-page MCNP6.3 Theory &amp; User's Manual is very comprehensive;
thus, it is difficult for new users of the code to distinguish between
information vital for learning how to use the code and information
needed to use the many hundreds of code options. For this reason, this
tutorial document was prepared to introduce the novice with the more
basic (and essential) aspects of the MCNP code.

A novice user should first peruse Ch. 1 of the Theory &amp; User's Manual to
gain an overview of MCNP that summarizes the code's features. Then, a
careful reading of this primer describes the preparation of input files,
the execution of the code, and the interpretation of results. Here the
focus is on so-called steady-state fixed-source problems , in which some
property of the radiation field, produced by a specified radiation
source, is sought at locations or regions of phase space ( r , E, Ω ). 2

After gaining some experience with MCNP, the beginning user should
periodically browse through Chapter 2 of the Theory &amp; User's Manual to
gain a better understanding of the theory behind the many features of
MCNP6. Likewise, by periodic skimming Chs. 3-5, an MCNP pupil will
become more familiar with all the commands and options that make MCNP
such a powerful radiation transport code. In this primer there are
several margin notes indicating the page or section in the MCNP6.3
Theory &amp; User's Manual (or, for simplicity, the Manual ) that discuss in
more detail the subject being summarized in the primer.

## 1 Structure of the MCNP Input File

An input file consists of a problem title card and a maximum of five
blocks of input cards (lines) arranged as shown to the right. The first
and last blocks are optional and often omitted. A single blank card
separates each block. The input file must not begin with a blank card
nor should it end with one. Block 0 contains options (see § 3.3.2.3 of
the Manual ) that are added to the MCNP execution line. The message
block starts with the string MESSAGE: . The message block ends with a
blank line delimiter before the single required problem title card .
Blocks 1 and 2 define the problem geometry. Block 1 defines all the
regions or cells of Cartesian ( x, y, z ) space. Every point ( x, y, z )
must be in one cell or on a cell boundary. Block 2 defines the surfaces
used to form the boundaries of the cells. Block 3 specifies what MCNP is
to do in the simulation. Finally, block 4 contains com-

<!-- image -->

mand or data cards that are ignored by MCNP but the user wants to keep
with the input file. For example, to analyze different shield materials,
it is a simple matter to swap material cards between blocks 3 and 4 to
analyze a different shield material.

Input Cards Input cards (or lines) have a maximum of 128 columns and
command mnemonics begin in the first 5 columns. Free field format (one
or more spaces separating items on a line) is used and alphabetic
characters can be upper or lower case. A continuation line must begin
with five blank columns, unless a blank followed by an &amp; is placed at
the end of the card to be continued. Tabs are allowed and replaced by
blanks to reach the next tab stop (eight columns between tab stops).
However, the authors recommend that users refrain from use of tabs for
simplicity.

## 1.1 Annotating the Input File

It is good practice to add comments liberally to an input MCNP file so
that it is easier for you and others to understand what problem is
addressed and how it was solved. A comment line begins with C or c
followed by a space. Such a line is ignored by MCNP. Alternatively,
anything following a $ sign on a line is ignored. See Fig. 8 on page 35
for a well-annotated MCNP input file.

2 Criticality or transient problems, which MCNP6 can also address, are
not considered here.

## 1.2 Units Used by MCNP

The units used by MCNP are (1) length in cm, (2) energy in MeV, (3) time
in shakes (10 -8 s), 3 (4) temperature in MeV (kT), (5) atom density in
atoms b -1 cm -1 , (6) mass density in g cm -3 , (7) cross sections in
b, and (8) deposited energy in jerks g -1 . 4

## 2 Geometry Specifications

The cards in Blocks 1 and 2 of the input file define, respectively, the
region(s) of 3-D Cartesian space contained in each cell and the surfaces
used for the boundaries of the cells. All dimensions are in centimeters
(cm). Each of the infinite number of points in the Cartesian space must
be in one and only one cell (or be on a boundary surface), i.e., the
cells are contiguous and collectively contain all points ( x, y, z ) ,
x, y, z ∈ ( -∞ , ∞ ) in the infinite Cartesian space. There can be no
'holes' in the geometry with points that are in no cell. A simulated
particle that reaches such a point becomes lost . If many particles
become lost, then it is likely that there are errors in the MCNP
geometry. This is a problem encountered frequently when developing a
geometric model, especially by those first learning to use MCNP.

Cells are defined in terms of surface regions that lie to one side of
first and second degree surfaces. Each surface thus has two surface
regions which are often infinite in size. Specifically, cells are
defined by Boolean intersections, unions, and compliments of these
surface regions. Each cell is filled with a user-defined materials. The
union and intersection of two regions A and B are shown by the shaded
regions in Fig. 1.

The union operation may be thought of as a logical OR, in that the union
of A and B is a new region containing all space either in region A OR
region B. The intersection operation may be thought of as a logical AND,
in that the result is a region that contains only space common to both A
AND B. The complement operator # plays the roll of a logical NOT. For
example # (A:B) represents all space outside the union of A and B.

Figure 1. Left: the union A:B or 'A OR B'. Right: the intersection A B or 'A AND B'.

<!-- image -->

Developing a geometric model for a particular application is usually the
most difficult part of preparing the input file and, for a novice, a
source of great frustration. After reading the deceptively simple
presentation that follows, the introductory discussion in § 1.3 should
be read. Then to learn more about geometric models study § 2.2. Finally,
as experience is gained in the development of geometry models, there are
many examples provided in § 10.1 worthy of careful study.

Table 1, taken from the MCNP manual, lists the surfaces used by MCNP to
create the geometry

3 The shake is a convenient small time interval (10 ns) used by bomb
designers in the once top secret Manhattan Project for use in their
experiments and calculations. For example, the time needed to complete
one step in a bomb's chain reaction (or, in nuclear parlance, the prompt
neutron lifetime ) is about 10 -8 s. The name shake comes from the
vernacular idiomatic expression 'two shakes of a lamb's tail' to denote
a very small time interval.

4 The jerk is another Manhattan Project made-up name defined as 1 jerk =
10 9 J = 1 GJ. One jerk equals 6 . 241 × 10 21 MeV or the explosive
energy released by the detonation of 0.238 tonnes of TNT. It should be
noted that this nuclear jerk has nothing to do with the jerk of
classical mechanics that is a vector and equals the rate of change of
the acceleration of an object and so has units of cm/s 3 . Why the bomb
designers recycled the name jerk is a mystery to the authors.

§ 1.3, § 2.2, § 10.1

Table 1. MCNP Surface Cards [after page 262 of MCNP6.3 Theory &amp; User's Manual ].

| Mnemonic                     | Type                                                                                                        | Description                                                                                           | Equation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Card Entries                                                    |
|------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| P                            | plane                                                                                                       | general normal to x -axis                                                                             | Ax + By + Cz - D = 0 x - D = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | A B C D D                                                       |
| PX PY PZ SO S SZ C/X C/Y C/Z | normal to y -axis normal to z -axis sphere ( x - ¯ x ) 2 cylinder parallel to x parallel to y parallel to z | centered at origin x 2 general +( y - ¯ y centered on x -axis centered on y -axis centered on z -axis | y - D = 0 z - D = 0 + y 2 + z 2 - R 2 = 0 ) 2 +( z - ¯ z ) 2 - R 2 =0 ( y - ¯ y ) 2 +( z - ¯ z ) 2 - R 2 = 0 ( x - ¯ x ) 2 +( z - ¯ z ) 2 - R 2 = 0 ( x - ¯ x ) 2 +( y - ¯ y ) 2 - R 2 = 0 y 2 + z 2 - R 2 = 0 x 2 + z 2 - R 2 = 0 x 2 + y 2 - R 2 = 0 √ ( y - ¯ y ) 2 +( z - ¯ z ) 2 - t ( x - ¯ x ) = 0 √ ( x - ¯ x ) 2 +( z - ¯ z ) 2 - t ( y - ¯ y ) = 0 √ ( x - ¯ x ) 2 +( y - ¯ y ) 2 - t ( z - ¯ z ) = 0 √ y 2 + z 2 - t ( x - ¯ x ) = 0 √ x 2 + z 2 - t ( y - ¯ y ) = 0 √ x 2 + y 2 - t ( z - ¯ z ) = 0 ± 1 used only for 2 2 2 | D D R ¯ x ¯ y ¯ z R ¯ y ¯ z R ¯ x ¯ z R ¯ x ¯ y R               |
| SX SY CX                     | on x -axis                                                                                                  |                                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | R                                                               |
| CY CZ K/X KZ                 | on y -axis on z -axis cone                                                                                  |                                                                                                       | ( x - ¯ x ) 2 + y 2 + z 2 - R 2 = 0 x 2 +( y - ¯ y ) 2 + z 2 - R 2 = 0 x 2 + y 2 +( z - ¯ z ) 2 - R 2 = 0 -axis -axis -axis                                                                                                                                                                                                                                                                                                                                                                                                             | ¯ x R ¯ y R ¯ z R R R ¯ y ¯ z t 2 ± 1                           |
| K/Y K/Z KX KY SQ             | ellipsoid hyperboloid                                                                                       | parallel to x -axis parallel to y -axis parallel to z -axis on x -axis on y -axis                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | ¯ y ¯ z t 2 ± 1 ¯ x ¯ y ¯ z t 2 ± 1 ¯ x t 2 ± ¯ y t 2 ± ¯ z t 2 |
|                              |                                                                                                             | on z -axis                                                                                            | ¯ x ¯ x                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 1 1 ± 1 1-sheet cone                                            |
|                              |                                                                                                             | axis parallel to x -, y -, or z -axis                                                                 | A ( x - ¯ x ) + B ( y - ¯ y ) + C ( z - ¯ z ) +2 D ( x - ¯ x )+2 E ( y - ¯ y )                                                                                                                                                                                                                                                                                                                                                                                                                                                          | A B C D E F G ¯ x ¯ y ¯ z                                       |
| GQ                           | ellipsoid                                                                                                   |                                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | A B C D E F G H J K ¯ x ¯ y ¯ z A B C                           |
| TY                           | paraboloid cylinder, cone hyperboloid                                                                       | ( x - ¯ x ) 2 /B 2 +( √ ( ( y - ¯ y ) 2 /B 2 +( √ ( ( z - ¯ z ) 2 /B 2 +( (                           | y - ¯ y ) 2 +( z - ¯ z ) 2 - A ) 2 /C 2 - 1 = 0 x - ¯ x ) 2 +( z - ¯ z ) 2 - A ) 2 /C 2 - 1 = 0                                                                                                                                                                                                                                                                                                                                                                                                                                         | ¯ x ¯ y ¯ z A B C                                               |
|                              |                                                                                                             | axis not parallel                                                                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                 |
| TX                           | paraboloid elliptical or circular torus. Axis is                                                            | to x -, y -, or z -axis                                                                               | +2 F ( z - ¯ z )+ G = 0 Ax 2 + By 2 + Cz 2 + Dxy + Eyz + Fzx + Gz + Hy + Jz + K = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                 |
|                              | parallel to x -,                                                                                            |                                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                 |
| TZ                           | y -, or z -axis                                                                                             |                                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                 |
| XYZP                         |                                                                                                             | √                                                                                                     | x - ¯ x ) 2 +( y - ¯ y ) 2 - A ) 2 /C 2 - 1 = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | ¯ x ¯ y ¯ z A B C                                               |
|                              | surfaces defined by                                                                                         |                                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                 |
|                              | points - see 5.3.2 and 5.3.3 of the Theory &                                                                |                                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                 |
|                              | § § User's                                                                                                  |                                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                 |
|                              |                                                                                                             |                                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Manual                                                          |

of a problem. 5 All surfaces are defined in a Cartesian coordinate
system. A surface is represented functionally in the form of an
equation, as f ( x, y, z ) = 0. For example, for a cylinder of radius R
parallel to the z -axis is defined as f ( x, y, z ) = ( x -¯ x ) 2 + ( y
-¯ y ) 2 -R 2 , where the cylinder's axis is parallel to the z -axis and
passes through the point (¯ x, ¯ y, 0). The MCNP input line for such a
surface, which is denoted by the mnemonic C/Z (or c/z , since MCNP is
case insensitive), is

1

C/Z

5 5

10

$ a cylindrical surface parallel to z-axis

defines surface 1 as an infinitely long cylindrical surface parallel to
z -axis with radius of 10 cm and whose axis passes through the point ( x
= 5 cm , y = 5 cm , z = 0). Note that the length of the cylinder is
infinite. Note also the in-line comment , introduced by the $ symbol.

Every surface has a 'positive' side and a 'negative' side. These
directional senses for a surface are defined formally as follows: any
point at which f ( x, y, z ) &gt; 0 is located in the positive sense (+) to
the surface, and any point at which f ( x, y, z ) &lt; 0 is located in the
negative sense ( -) to the surface. These are the two surface regions
associated with every surface. For example, a region within a
cylindrical surface is negative with respect to the surface and a region
outside the cylindrical surface is positive with respect to the surface.

## 2.1 Cells - Block 1

We illustrate how surfaces and Boolean logic are used to define cells by
considering a simple example of a cylindrical storage cask whose wall
and ends are composed of iron 1-cm thick. Inside and outside the cask
are void regions. Suppose the outer cylindrical surface is that used in
the illustration in the previous section. The geometry for this problem
is shown in Fig. 2.

<!-- image -->

x

To define the inside surface of the cask, we need another cylinder
inside and concentric with the first cylinder but with a radius smaller
by 1 cm. We shall call this smaller cylindrical surface number 4, so
that the surface definition lines in the input file for these two
cylinders are

- 1 C/Z 5 5 10

- $ outer cylindrical surface

- 4 C/Z 5 5 9

- $ inner cylindrical surface

To define the base and top of the cask, planes perpendicular to the z
-axis are needed at locations z = 40 cm and z = 60 cm, respectively.
Similarly, to define the base and top of the inner cavity

5 Because surfaces must be defined before the cells can be specified in
terms of the bounding surfaces, we discuss Block 2 before Block 1. Why
MCNP requires the input of cell definitions before the bounding surface
definitions is unknown to the authors. In practice, one creates block 2
before block 1.

Figure 2. Geometry for a simple cylindrical cask. Numbers in triangles
are surface identification numbers and the triangle points to the (+)
side of the surface. Numbers in circles define the cell identification
number. The axis of the cask passes through the point ( x = 5 cm, y = 5
cm) and the cask outer radius is 10 cm.

§ 5.3.4

of the cask two more planes perpendicular to the z -axis are needed at z
= 41 cm and z = 59 cm. These four planes are defined by

```
2 PZ 40 $ base of cask 3 PZ 60 $ top of cask 5 PZ 41 $ base of inner cavity 6 PZ 59 $ top of inner cavity
```

The surface definition cards (or input lines) can appear in any order in
Block 2 of the input file. Each surface must have a unique positive
integer identifier ( &lt; 10 8 ). Here the surface numbers are 1, 2, 3, 4,
5, and 6. They need not be ordered as in this example but they must
begin in columns 1-5.

With the problem surfaces defined, we now begin to define the volumes or
cells which must fill all ( x, y, z ) space. These cell definition cards
comprise the content of Block 1 of the input file. First, we define the
inner void of the cask as cell 8. This volume is negative with respect
to surface 4, positive with respect to the plane 5, and negative with
respect to plane 6. Thus, cell 8 is defined as

```
8 0 -4 5 -6 IMP:N=0 IMP:P=1 $ inner cask void
```

The first number on a cell definition card is the cell identifier (any
positive integer &lt; 10 8 ) and must begin in columns 1-5. Here the second
entry 0 denotes that the cell is filled by a void, and -4 5 -6 indicate
that all points in cell 8 are inside the cylinder 4 AND are above plane
5 AND are below plane 6. region. The last two IMP specifications define
the importance of this region to neutrons ( N ) and ( P ). Neutrons in
this cell have zero weight and photons have unit weight (i.e., we assume
only photon sources are stored in the cask). We'll discuss importances
later. The order of surfaces in an intersection string is arbitrary.
Thus, we could have defined cell 8 by intersection of surfaces -6 -4 5.

Now consider the iron shell of the cask. Suppose this cell is given 7 as
its id number and consists of material 5, as yet to be defined, with
density 7.86 g cm -3 . Space within this cell is negative with respect
to surface 1, positive with respect to surface 2 and negative with
respect to surface 3 AND also cannot be inside the void or cell 8. This
cell can thus be defined as

```
7 5 -7.86 -1 2 -3 #8 IMP:N=0 IMP:P=1 $ iron cask shell
```

Although the complement operator # (for NOT) is often a convenient way
to exclude an inner region, this operator often reduces the efficiency
of MCNP. In fact, theoretically one never has to use # . The region
outside cell 8 can be defined by the union string (4:6:-5) and the
definition of cell 7 can be equivalently defined as

```
7 5 -7.86 -1 2 -3 (4:6:-5) IMP:N=0 IMP:P=1 $ iron cask shell
```

Now suppose that cells 7 and 8 describe all space of interest for
radiation transport. In other words, suppose that all photons passing
outside the outer surface of the finite cylinder may be killed, i.e.,
their path tracking can be ended. One still needs to assign this space
to a cell. Further by setting the photon importance in this cell to
zero, any photon entering is killed. This 'graveyard' cell, say cell 9,
is the union of all regions positive with respect to surfaces 1 and 3
and negative with respect to surface 2. Hence the graveyard is defined
by

```
9 0 1:3:-2 IMP:N=0 IMP:P=0 $ graveyard
```

The graveyard could also be defined by using the complement operator and
by specifying that the kill zone is all space outside the union of cells
7 and 8, namely

```
9 0 #(7:8) IMP:N=0 IMP:P=0 $ graveyard
```

Note that the second entry on this cell card is zero, indicating a
vacuum and that the photon importance is set to zero.

## 2.2 Macrobodies

MCNP has an alternative way to define cells and surfaces through the use
of macrobodies. These macrobodies can be mixed with the standard cells
and surfaces and are defined in Block 2. For example, the command in
Block 2

Table 2. Macrobodies available in MCNP.

| Mnemonic                                       | Type of body                                                                                                                                                                                                                                             |
|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BOX RPP SPH RCC RHP or HEX REC TRC ELL WED ARB | arbitrarily oriented orthogonal box (90 ◦ corners) rectangular parallelepiped (surfaces parallel to axes) sphere right circular cylinder right hexagonal prism right elliptical cylinder truncated right-angle cone ellipsoid wedge arbitrary polyhedron |

<!-- formula-not-decoded -->

defines a right circular cylinder with the following properties: the
center of the base is at (1,2,5); the height is 50 cm and the axis is
parallel to the z -axis; the radius is 10 cm; and the macrobody has 15
as its identifier.

The macrobodies available in MCNP are shown in Table 2. MCNP
automatically decomposes the macrobody surface into surface equations
and the facets are assigned identifying numbers according to a
predetermined sequence. The assigned surface number consists of the
macrobody identifier number follow by a decimal point and an integer 1 ,
2 , . . . . For example in the RCC example above, the cylindrical
surface has the identifier 15.1, the plane of the top is 15.2, and the
plane of the base is 15.3. These facet surfaces can be used for anything
standard surfaces are used for, e.g., tallies, other cell definitions,
source definitions, etc.

The definition of a macrobody can require many parameters. Here we give
the details for three of the most useful macrobodies.

BOX Arbitrarily oriented orthogonal box: This body is defined by four
vectors: v defining a corner of the box and three orthogonal vectors a ,
b , and c defining the length and direction of the sides from the
specified corner. The syntax is

```
BOX v x v y v z a x a y a z b x b y b z c x c y c z The facet suffixes are: .1/.2 plane perpendicular to the end/beginning of a .3/.4 plane perpendicular to the end/beginning of b .5/.6 plane perpendicular to the end/beginning of c
```

RPP Rectangular parallelepiped: This orthogonal box has sides
perpendicular to the coordinate § 5.3.4.2 axes. This body is defined by
the range each side has along its parallel axis. The syntax is

```
RPP x min x max y min y max z min z max
```

The facet suffixes are: .1/.2 plane x max /x min ; .3/.4 plane y max /y
min ; .5/.6 plane z max /z min .

RCC right circular cylinder: A right cylinder is specified by a vector v
giving the center of the base, a vector h defining the axis and height
of the cylinder, and the radius R . The syntax is

<!-- formula-not-decoded -->

The facet suffixes are: .1 cylindrical surface; .2/.3 plane normal to
the end/beginning of h .

NOTE: The space inside a macrobody has a negative sense with repsect to
all the macrobody's bounding surfaces . The space outside the bounding
surfaces has a positive sense to the macrobody.

§ 5.3.4.1

§ 5.3.4.4

More important to remeber is that the sense of a macrobody's bounding
surfaces or facets is the sense assigned to it by the macrobody and the
facet surface retains this sense even if it appears in other cell
definitions. For example, the base of the RCC cylinder discussed above
is a plane normal to the z -axis with intercept of 5 cm and has the
identifier 15.3. The space with z &gt; 5 has a negative sense to this
surface because this space is towards the interior of the cylinder. The
space for z &lt; 5 has a positive sense because this region is outside the
macrobody. This sense convention for macrobody surfaces is different
from the sense convention of standard surfaces. The surface 15.3 is
equivalent to a plane surface 16 defined as 16 PZ 5 , but space with z &gt;
5 has a positive sense with respect to surface 16 while it has a
negative sense for surface 15.3!

Figure 3. Geometry for a simple cylindrical cask. Two macrobody right cylinders are used to define the inside and ouside surfaces of the cask and numbers in circles are the cell identification number. As before, the axis of the cask passes through the point ( x = 5 cm, y = 5 cm, z = 0)

<!-- image -->

The use of macrobodies can greatly ease the specification of a problem's
geometry. We illustrate this by returning to the simple cask problem
considered in the previous section. Rather than define 6 surfaces to
form the cask, we use two nested cylinder macrobodies. The subsequent
Boolean logic used to define the three cells now becomes considerably
simpler. For the geometry shown in Fig. 3, the input geometry
specification becomes

```
Use of macrobodies for cask problem c ***************** BLOCK 1 -- cells 8 0 -18 IMP:P,N=1 $ inside the cask 7 5 -7.86 18 -17 IMP:P,N=1 $ cask iron shell 9 0 17 IMP:P,N=0 $ void outside cask c ***************** BLOCK 2 -- surfaces/macrobodies 17 RCC 5 5 40 0 0 20 10 $ outer cylinder 18 RCC 5 5 41 0 0 18 9 $ inner cylinder
```

Cell 8 is simply all the space inside macrobody 18 and is denoted by
-18. Cell 7 is all the space inside macrobody 17 and outside macrobody
18, namely 18 -17. These cell definitions are considerably simpler than
those based on the intersections and unions of the six standard surfaces
used in the previous definition of this cask.

## 2.2.1 Unstructured Meshes

The use of macrobodies and the ability to construct geometric regions
from Boolean operations on bounding surfaces gives MCNP a very powerful
constructive solid geometry (CSG) capability. It has been extensively
tested and verified. However for complex geometries the CSG approach for
specifying a problem geometry is labor intensive and susceptible to
errors which are often hard to debug.

New to MCNP6 is the ability to use an unstructured mesh (UM) to define a
problem geometry. This alternative to CSG is an exciting development but
one that is still evolving and one novice MCNP users should ignore until
they have gained some experience with MCNP.

## 3 Data Specifications - Block 3

This block of input cards defines the type of particles, problem
materials, radiation sources, how results are to be scored (or tallied),
the level of detail for the physics of particle interactions, variance
reduction techniques, cross section libraries, the amount and type of
output, and much more. In short, the third input block provides almost
all a problem's specifications other than the geometry.

The 60 or so different commands cards and the sometimes many KEYWORDS
(options) for the commands are extensively discussed in Ch. 5 of the
Manual . Here some necessary background and a few of the more commonly
used commands for simple problems are briefly reviewed.

## 3.1 Interaction Data Used by MCNP6

The nuclear data needed by MCNP6 to describe the interactions of
particles with the ambient medium as they transported through the
problem geometry are provided by (1) pointwise crosssection data and
other extensive data tables and/or (2) various nuclear physics models,
used primarily for high-energy particles ( &gt; 150 MeV). Unlike many other
transport codes, all this nuclear data is an integral part of the MCNP
code. The various libraries and data tables distributed with MCNP6.3 are
listed in LA-UR-17-20709 (Conlin, 2017). Relevant nuclear data are now
distributed separately from the MCNP code to decouple updates between
the two. Nuclear data for use with MCNP can be obtained from
https://nucleardata.lanl.gov/ .

For neutrons with energies up to 150 MeV, the comprehensive ENDF/B-VII
data files are composed of pointwise (continuous-energy) interaction
data and secondary-particle production data, for a few hundred target
isotopes. 6 Proton interaction data for 48 isotopes are provided for
energies from 1 to 150 MeV. Photon and electron/positron data are
included for energies of 1 eV to 100 GeV and from 10 eV to 1 GeV,
respectively. Photonuclear data for 157 isotopes are included for photon
energies up to 150 MeV. Above the maximum energies of these data
tabulations, and for all hadrons, interaction physics are based on
theoretical models with empirical corrections.

## 3.2 Materials Specification M Card

Specification of materials filling the the various cells in an MCNP
calculation uses an M card in block 3 for each material. This card
specifies (a) defining a unique material number (a positive integer &lt; 10
8 ), (b) the elemental (or isotopic for neutrons) composition, and (c)
the libraries of cross section and data tables to be used. The ZAID
number ZZZAAA identifies a specific nuclide or element. For example,
elemental uranium is 092000 , or simply 92000 , whereas the isotope 235
92 U has a ZAID of 92235 .

Note that mass density is not specified here. Instead, density is
specified on the cell definition card. This permits one material to
appear at different densities in different cells. Suppose that the first
material to be identified in problem input is (light) water and that
only gamma-ray transport is of interest. Comment cards (cards beginning
with C or c ) may be used for narrative descriptions. In the following
card images, the designation M21 refers to material 21. For a compound,
unnormalized (stoichiometric) atomic fractions may be used. For example,

- c ---------------------------------------------------------
- c WATER for gamma-ray transport (by atom fraction)

c

---------------------------------------------------------

6 Some discrete reaction tables in which the cross sections are averaged
over 262 groups are also available for use on computers with very
limited memory. These tables should be avoided.

Ch. 8

§ 2.3

§ 2.3.1, § 2.3.6

§ 5.6

§ 2.3.1

§ 5.6.2

```
M21 1000 2 $ elemental H and atomic abundance 8000 1 PLIB=04p $ elemental O and atomic abundance
```

The designations 1000 and 8000 identify elemental hydrogen, atomic
number Z = 1, and elemental oxygen ( Z = 8). The three zeros in each
designation are place holders for the atomic mass number, which would be
required to identify specific isotopes of the element and which,
generally, are required for neutron transport, as described later. For
gamma ray and electron transport, one needs to specify only the atomic
number. The keyword PLIB=04p says the 04p photon library is to be used.
Alternatively one could omit PLIB=04p and just append it to the ZAIDs,
i.e., 1000.04p and 8000.04p .

For compounds or mixtures, composition may alternatively be specified by
mass fraction, indicated by a minus sign, as follows:

```
c ---------------------------------------------------------c WATER for gamma-ray transport (by mass fraction) c ---------------------------------------------------------M21 1000.04p -0.11190 $ elemental H mass fraction 8000.04p -0.88810 $ elemental O mass fraction
```

Note mass and atom fractions need not sum to unity; MCNP will normalize
them.

For neutron transport problems, often specific isotopes of an element
must be specified. If neutron cross sections for an element composed of
its isotopes in their naturally occurring abundances is desired, then
sometimes the ZAID can be specified as ZZZ000. Note, such elemental
neutron cross section sets are old and not available for all elements.
Usually one must list all of the important isotopes. As an example,
light water for neutron problems could be defined as

```
c ---------------------------------------------------------c WATER for neutron transport (by mass fraction) c (ignore H-2, H-3, O-17, and O-18) c ---------------------------------------------------------M21 1001.80c -0.11190 $ H-1 and mass fraction 8016.80c -0.88810 $ O-16 and mass fraction
```

Here 1001 and 8016 provide atomic number and atomic mass designations,
in the form of the ZAID numbers. The 80c designation identifies the
ENDF/B-VII.1 cross section compilation. Other compilations distributed
with MCNP6.3 are given by Conlin [2017]. There is no hard and fast rule
as to which neutron library is 'best' (see also Section 3.2 below).

When hydrogen is molecularly bound in water, either in pure form or as a
constituent in some other material, the binding affects energy loss in
collisions experienced by slow neutrons. For this reason, special cross-
section data treatments are provided that take binding effects into
account. To use this special treatment, an additional MT card is
required, as shown below.

```
c ---------------------------------------------------------c WATER for neutron transport (by mass fraction) c (ignore H-2, H-3, O-17, and O-18) c Specify S(alpha,beta) treatment for binding effects c ---------------------------------------------------------M21 1001.80c -0.11190 $ H-1 and mass fraction 8016.80c -0.88810 $ O-16 and mass fraction MT21 lwtr.20t $ light water at 293.6 K
```

Without the MT card, hydrogen would be treated as if it were a monatomic
gas. With the S ( α, β ) treatment, fast neutrons slowing down to
thermal energies will develop a Maxwellian energy distribution with the
specified temperature. Treatment of binding effects for other nuclides,
materials and temperatures are also provided [Conlin et al. 2017].

## 3.3 Cross-Section Specification

Neutron interactions and the history and many sources of cross-section
data tables are described in Section 2.3.1 of the the MCNP6 Manual . A
comprehensive list of cross section compilations in the ACE format
distributed with MCNP6 is provided by Conlin and the LANL Nuclear Data
Team [2017]. This 500-page Technical Report replaces the infamous Table
G2 of Appendix G to Vol. I for MCNP5 and MCNP4. Specification of a
particular cross-section compilation depends somewhat on the nature of
the problem being solved and on the data available to the user. Not all
cross section sets are available to all users. For users obtaining data
through the Radiation Safety Information Computation Center (RSICC), a
common choice would be the 80c library, which was derived from the
ENDF/B-VII.1 evaluated nuclear data files for room-temperature, Doppler
broadening of neutron cross sections. For Doppler broadening at other
temperatures, other libraries are also available.

In a few instances, neutron cross sections are available for elements
with naturally occurring atomic abundances. For example, natural
chromium can be specified as 24000.50c. However, elemental neutron cross
sections are rare and, for the very few such libraries available, the
underlying data are old. Generally, it is necessary for the user to
define a natural element as a combination of the natural occuring
isotopes. Even then, data for nuclides with small ( &lt; 0.1%) isotopic
abundances are often not available and the trace isotopes must be
neglected (as was done in the previous section for light water).

## 3.4 Source Specification

The source and the radiation particles it emits in a fixed-source MCNP
problem are specified by the SDEF command. The SDEF command has many
keywords or parameters that are used to define all the characteristics
of all sources in the problem. The SDEF command with its many keywords
and their possible values is one of the more complex MCNP commands and
is capable of producing an incredible variety of sources - all with a
single SDEF command. And only one SDEF card is allowed in an input file!

On the SDEF card values of appropriate keywords in Table 4 are entered,
if other than the default values, that are needed to characterize a
particular source. The = sign is optional, so that PAR=1 is equivalent
to PAR 1 . Values of variables can be specified at three levels: (1)
explicitly (e.g., ERG=1.25), (2) with a distribution number (e.g.,
ERG=d5 ), and (3) as a function of another variable (e.g., ERG=Fpos ).
Specifying variables at levels 2 and 3 requires the use of two ancillary
source cards: the SI (source information) card and the SP (source
probabilities) card. 7

## 3.4.1 SI: Source Information Card

This card tells MCNP how K values i 1 , . . . i K about a source
variable (e.g., energies of photon spectral lines) are to be
interpreted. The form of the SI card is

SIn option i 1 , . . . i K

where n is the distribution number specified on the SDEF card. The four
possible options are listed below

option = H i values are monotonically increasing histogram bin upper
boundaries

option = L i values are discrete source variable values (e.g., cell
numbers or

energies of photon spectrum lines).

option = A

i values are points where a probability density is defined. Entries must
be monotonically increasing, with the lowest and highest val- ues
defining the range of the variable.

option = S i values are distribution numbers.

7 Two other ancillary source cards are available for more advanced
applications: the SB (source biasing) card and the DS (source dependent)
distribution card.

§ 5.8.1 to § 5.8.6

§ 5.8.2

Table 3. MCNP6 particle identifiers and the minimum tracking energy for the more commonly used particles. Data for other leptons, baryons and mesons are given in Table 4.3 of the Manual .

|   PAR | Name             | MCNP Symbol   | Low-E Cutoff (MeV)   | Default Cutoff (MeV)   |   PAR | Name                 | MCNP Symbol   | Low-E Cutoff (MeV)   |   Default Cutoff (MeV) |
|-------|------------------|---------------|----------------------|------------------------|-------|----------------------|---------------|----------------------|------------------------|
|     1 | neutron (n)      | N             | 0.0                  | 0.0                    |    31 | deuteron (d)         | D             | 10 - 3               |                      2 |
|     2 | photon ( γ )     | P             | 10 - 6               | 10 - 3                 |    32 | triton (t)           | T             | 10 - 3               |                      3 |
|     3 | electron ( e - ) | E             | 10 - 5               | 10 - 3                 |    33 | helion ( 3 He)       | S             | 10 - 3               |                      3 |
|     8 | positron ( e + ) | F             | 10 - 3               | 10 - 3                 |    34 | alpha particle ( α ) | A             | 10 - 3               |                      4 |
|     9 | proton ( e + )   | H             | 10 - 3               | 1 . 0                  |    37 | heavy ion ( A Z X)   | #             | 10 - 3               |                      5 |

Table 4. Source keywords for the SDEF command.

| Variable   | Meaning                                                                                                                                 | Default                                                                                                                                  |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| CEL        | cell                                                                                                                                    | determined from the position of the particle, and pos- sibly the particle's flight direction if the position is on a cell surface.       |
| SUR        | surface                                                                                                                                 | SUR=0 means cell (volume) source                                                                                                         |
| ERG        | kinetic energy (MeV)                                                                                                                    | 14 MeV                                                                                                                                   |
| DIR        | µ , the cosine of the angle between VEC and particle flight direction. The azimuthal angle is always sam- pled uniformly in [0 , 2 π ]. | Volume case: µ is sampled uniformly in [ - 1 . 1] (isotropic). Surface case: p ( µ ) = 2 µ for µ/epsilon1 [0 , 1] (cosine distribution). |
| VEC        | reference vector for VEC                                                                                                                | Volume case: required unless isotropic. Surface case: vector normal to the surface with sign determined by NRM .                         |
| NRM        | sign of the surface normal                                                                                                              | +1                                                                                                                                       |
| POS        | reference point for positioning sampling                                                                                                | 0 , 0 , 0                                                                                                                                |
| RAD        | radial distance of the position from POS or AXS                                                                                         | 0                                                                                                                                        |
| EXT        | Cell case: distance from POS along AXS . Surface case: cosine of angle from AXS                                                         | 0                                                                                                                                        |
| AXS        | reference vector for EXT and RAD                                                                                                        | no direction                                                                                                                             |
| X          | x-coordinate of position                                                                                                                | X=0                                                                                                                                      |
| Y          | y-coordinate of position                                                                                                                | Y=0                                                                                                                                      |
| Z          | z-coordinate of position                                                                                                                | Z=0                                                                                                                                      |
| CCC        | cookie-cutter cell                                                                                                                      | no cookie-cutter cell                                                                                                                    |
| ARA        | area of surface (required only for di- rect contributions to point detectors from a plane surface source)                               | none                                                                                                                                     |
| WGT        | particle weight                                                                                                                         | 1                                                                                                                                        |
| EFF        | reference efficiency criterion for po- sition sampling                                                                                  | 0 . 01                                                                                                                                   |
| PAR        | type of particle source emits. Many choices e.g., cosmic ray, background, particles from radioactive decay.                             | particle with smallest IPT value on MODE card: N=1, P=2, E=3, ...                                                                        |

## 3.4.2 SP: Source Probability Card

This card gives the probabilites for each item on the corresponding SI
card. It has the two forms SPn option p 1 , . . . p K and SPn -f a b
where n is the distribution number specified on the SDEF card and the
option letter specifies how the p i are to be interpreted according to
the following list (only the 5 most frequently used options are listed
here).

| option   | omitted   | the same as D for an H or L distribution on the SI card or a proba- bility density for an A distribution on the SI card.         |
|----------|-----------|----------------------------------------------------------------------------------------------------------------------------------|
| option   | = D       | p i values are bin probabilities for an H or L distribution on the SI card. (Default value).                                     |
| option   | = C       | p i values are cumulative bin probabilities for an H or L distribution on the SI card.                                           |
| option   | = V       | p i values are for CEL distributions; the probability is proportional to a cell's volume ( × p i if the p i are present)         |
| option   | = - f     | a negative integer specifies the use of a built-in function with pa- rameter values a and possibly b . See 5.8.3.1 of the Manual |

a negative integer specifies the use of a built-in function with
parameter values a and possibly b . See § 5.8.3.1 of the Manual

## 3.5 Examples of Simple Sources

Often MCNP problems involve fairly simple fixed sources that for a
novice can be challenging to implement in MCNP. The documentation for
MCNP5 and earlier versions devoted only a few exceptionally terse pages
to the SDEF and ancillary cards. The few source examples in the examples
chapter were far too complex for an MCNP beginner to understand and use
to create a simple source, which was a primary motivation for our Primer
on MCNP5. With the simple examples in our first MCNP Primer, our
students were able to start using MCNP with greater ease.

With the advent of MCNP6(v.1), the user's manual has greatly expanded
the discussion about sources until the latest version for MCNP6.3
[Kulesza et al., 2022] devotes almost 60 very understandable pages and
many 'simple' examples to the subject. Kudos to the authors! However,
many of these simple examples illustrate advanced features not covered
in this primer. Presented below are some even simpler source examples.
These are designed to help the novice MCNP user model many common source
situations, rather than demonstrate the subtleties or alternative syntax
for keywords and options of the SDEF card.

Once users have gained confidence with simple source models, they should
begin studying the often complicated source examples given in Chapter 10
of the Manual . From periodic perusuals of § 5.8 and § 10.3 of the
Manual one usually gains new insight into the robustness of the SDEF
command. It is probably the most powerful, complex, and flexible of all
the MCNP commands, and consequently, the most difficult one to master.

Finally, a cautionary word learned from experience. When you develop a
new source model, always check and recheck that source particles are
truly being generated where you think they should be and are born with
the correct energies and directions of travel. HINT: place the VOID card
and the PRINT 110 statement somewhere in block 3 of the input file. The
PRINT 110 causes the starting locations. directions, and energies of the
first 50 particles to be printed to the output file. Examine this output
table to convince yourself that particles are being generated as you
expect.

## 3.5.1 Point Isotropic Sources

## Two Point Isotropic Sources at Different Positions

c SDEF ERG=1.00 PAR=2 POS=d5 SI5 L -10 0 0 10 0 0 SP5 .75 .25

----- Two point, isotropic, 1-MeV, photon sources on x-axis

- $ energy, particle type, location

- $ (x,y,z) coords of the two pt sources

- $ relative strengths of each source

§ 5.8.3

§ 5.8

§ 10.3

<!-- image -->

## Point Isotropic Source with Discrete Energy Photons

```
c ----- Point isotropic source with 4 discrete photon energies SDEF POS 0 0 0 ERG=d1 PAR=2 SI1 L .3 .5 1. 2.5 $ the 4 discrete energies (MeV) SP1 .2 .1 .3 .4 $ frequency of each energy
```

## Point Isotropic Source with a Histogram of Energies

c ----- Point isotropic photon source with 4 histogram energy bins c
NOTE: range of first E-bin is (-infty,E1) with prob p1=0 SDEF POS 0 0 0
PAR=P ERG=d1 $ position, part type, E distn SI1 H .1 .3 .5 1. 2.5 $
histogram upper boundaries SP1 D 0 .2 .4 .3 .1 $ probabilities for each
bin

## Point Isotropic Source with a Continuum of Energies

```
c ----- Point isotropic neutron souce with Maxwellian energy spectrum SDEF POS 0 0 0 PAR=N ERG=d1 $ position, particle type, energy SP1 -2 0.5 $ Maxwellian spectrum (2) with temp a=0.5 MeV
```

## Point Isotropic Source with Tabulated Energy Distribution

## (a) Horizontal Input

```
c ----- Isotropic proton source w cont.-E PDF listed at discrete Es SDEF POS 0 0 0 PAR=H ERG=d7 $ position, particle type, E distn SI7 A 1 2 3 4 5.5 7.0 7.5 $ tabulated energies E1 ... E7 SP7 D 0 .2 .27 .3 .28 .18 0 $ tabulated PDF values f(Ei)
```

## (b) Vertical Input

c ----- Isotropic proton source w cont.-E PDF listed at discrete Es SDEF
POS 0 0 0 PAR=H ERG=d7 $ position, particle type, E distn.

```
c ----- use vertical input for PDF -easiest if many Ei # SI7 SP7 $ # sign indicates start of vertical input A D 1.0 0.0 $ E1 f(E1) start of PDF 2.0 .20 $ E2 f(E2) 3.0 .27 $ E3 f(E3) 4.0 .30 $ E4 f(E4) 5.5 .28 $ E5 f(E5) 7.0 .18 $ E6 f(E6) 7.5 0.0 $ E7 f(E7) end of PDF and vertical input
```

## Two Point Sources with Different Energy Distributions

c --- 2 pt iso sources: src 1 (4-bins) src 2 (4 discrete Ei) SDEF PAR=2
POS=d1 ERG FPOS d2

SI1 L -10 0 0 10 0 0

$ coords of srcs on x-axis

SP1

.4

.6

$ rel strengths of sources

DS2

S

3

4

$ energy distributions

SI3

H

.1

.3

.5

1.

2.5

$ E bin limits src 1

SP3

D

0

.2

.4

.3

.1

$ bin prob for src 1

SI4

L .3

.5

.9

1.25

$ discrete Ei for src 2

SP4

.20 .10 .30

.40

$ rel freq for src 2

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## 3.5.2 Isotropic Volumetric Sources

## Rectangular Parallelepiped Parallel to Axes

c

--- volumetric monoenergetic source inside a rectangular parallelepiped

SDEF X=d1 Y=d2 Z=d3 ERG=1.25 PAR=2 SI1 -10. 10. $ x-range limits for
source volume SP1 0 1 $ uniform probability over x-range SI2 -15. 15. $
y-range limits for source volume SP2 0 1 $ uniform probability over
y-range SI3 -20. 20. $ z-range limits for source volume SP3 0 1 $
uniform probability over z-range

## Source in a Complex Cell: Enclosing Parallelepiped Rejection Method

```
c --- Cell 8 is some complex cell in which a monoenergetic isotropic c volumetric source exists. A rectangular parallelepiped envelops c this cell (MCNP does NOT check this!). Points, randomly picked c in the rectangular parallelepiped, are accepted as source points c only if they are inside cell 8. c SDEF X=d1 Y=d2 Z=d3 ERG=1.25 PAR=2 CEL=8 c NOTE: source parallelepiped is larger that cell 8, and hence c source positions sampled outside cell 8 are rejected. SI1 -12. 12. $ x-range limits for source volume SP1 0 1 $ uniform probability over x-range SI2 -11. 11. $ y-range limits for source volume SP2 0 1 $ uniform probability over y-range SI3 -13. 13. $ z-range limits for source volume SP3 0 1 $ uniform probability over z-range cell/.notdef8
```

## Source in a Complex Cell: Enclosing Sphere Rejection Method

```
c --- Cell 8 is some complex cell in which a monoenergetic isotropic c volumetric source exists. A sphere envelops this cell {MCNP c does NOT check this!). Points, randomly picked in the sphere, c are accepted as source points only if they are inside cell 8. c SDEF POS=0 0 0 RAD=d1 CEL=8 SI1 0 20. $ radial sampling range: 0 to Rmax (=20cm)
```

```
SP1 -21 2 $ weighting for radial sampling: here r^2
```

## 3.5.3 Line and Area Sources (Degenerate Volumetric Sources)

## Line Source (Degenerate Rectangular Parallelepiped)

```
c --- Line monoenergetic photon source lying along x-axis c This uses a degenerate Cartesian volumetric source. c SDEF POS=0 0 0 X=d1 Y=0 Z=0 PAR=P ERG=1.25 SI1 -10 10 $ Xmin to Xmax for line source SP1 -21 0 $ uniform sampling on line Here x^0 z x y 10 -10
```

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Disk Source (Degenerate Cylindrical Source)

```
c --- disk source in x-y plane centered at the origin. c This is a degenerate cylindrical volume source. c SDEF POS 0 0 0 AXS 0 0 1 EXT 0 RAD d1 PAR P ERG 1.25 SI1 0 11 $ radial sampling range: 0 to Rmax SP1 -21 1
```

```
$ radial sampling weighting: r^1 for disk source z x y Rmax
```

<!-- image -->

## Plane Source (Degenerate Rectangular Parallelepiped)

```
c --- rectangular plane source centered on the origin and perpendicular c to the y-axis. This uses a degenerate Cartesian volumetric source. c SDEF POS=0 0 0 X=d1 Y=d2 Z=0 PAR=P ERG=1.25 SI1 -10 10 $ sampling range Xmin to Xmax SP1 0 1 $ weighting for x sampling: here constant SI2 -15 15 $ sampling range Ymin to Ymax SP2 0 1 $ weighting for y sampling: here constant x
```

## Line Source (Degenerate Cylindrical Source)

```
c --- line source (degenerate cylindrical volumetric source) SDEF pos=0 0 0 axs=1 0 0 ext=d1 rad=0 par=2 erg=1.25 SI1 -10 10 $ axial sampling range: -X to X SP1 -21 0 $ weighting for axial sampling: here constant
```

## 3.5.4 Monodirectional and Collimated Sources

## Monodirectional Disk Source

```
c --- Disk source perpendicular to z-axis uniformly emitting c 1.2-MeV neutrons monodirectionally in the +ve z-direction. c SDEF POS=0 0 0 AXS=0 0 1 EXT=0 RAD=d1 PAR=1 ERG=1.2 VEC=0 0 1 DIR=1 SI1 0 15 $ radial sampling range: 0 to Rmax (=15cm) SP1 -21 1 $ radial sampling weighting: r^1 for disk
```

## Point Source Collimated into a Cone of Directions

```
c --- Point isotropic 1.5-MeV photon source collimated into c an upward cone. Particles are confined to an upward c (+z axis) cone whose half-angle is acos(0.9) = 25.8 c degrees about the z-axis. Angles are with respect to c the vector specified by VEC c SDEF POS=0 0 0 ERG=1.25 PAR=2 VEC=0 0 1 DIR=d1 SI1 -1 0.9 1 $ histogram for cosine bin limits SP1 0 0.95 0.05 $ frac. solid angle for each bin SB1 0. 0. 1. $ source bias for each bin
```

z

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

With this conical source, tally normalization is per source particle in
4 π steradians. To normalize the tally per source particle in the cone,
put WGT=1/fsa2 on the SDEF card, where fsa2 is the fraction solid angle
of the cone (0.05 in the above example).

## Biasing the Source Emission Direction

The above conical collimation trick can also be used to preferentially
bias the emission of particles in certain directions. The SIn entries
are the upper bin cosine limits µ i ≡ cos θ i in ascending order . The
first entry is -1. Angles are with respect to the direction specified by
VEC . The SPn entries give the fractional solid angle fsa i = [(1 -µ i
-1 ) -(1 -µ i )] / 2 for the bin from µ i -1 to µ i , and the SBn
entries give the desired (biased) relative probabilities for emission in
each angular bin. Note the first probability must be 0 for the
unrealistic bin from ( -∞ , -1). From the true bin probabilities (from
the SPn card), the weights of the source particles are adjusted by MCNP
to remove the bias when scoring (or tallying) a history. A side note: it
is not necessarry to normalize the sum of the p i s on the SPn or SBn
cards. MCNP automatically ensures the probabilities are properly
normalized.

## 3.5.5 Multiple Volumetric Sources

## Two Cylindrical Volumetric Sources

```
c --- Two volumetric sources uniformly distributed in cells 8 & 9. c Both sources emit-1.25 MeV photons. Surround both source cells c by a large sampling cylinder defined by the POS RAD and EXT c parameters. The rejection technique is used to pick source c points with cells 8 and 9 with the specified frequency. c SDEF ERG=1.25 CEL d1 AXS=0 0 1 POS 0 0 0 RAD d2 EXT d5 SI1 L 8 9 $ source cells: src 1 =cell 8, src 2 =cell 9 SP1 0.8 0.2 $ 80% from src 1; 20% from src 2 SI2 0 50 $ radius of cyl. containing cells 8 & 9 SI5 -30 30 $ axial range of cyl. containing src cells
```

## Two Cylindrical Sources with Different Energy Photons

```
c --- Two spatially different cylindrical monoenergetic sources. c The size and position of each cyl. source depends on the c source energy (FERG). c SDEF ERG=d1 POS=FERG d8 AXS=0 0 1 RAD=FERG d2 EXT=FERG d5 c c -- set source energies: .667 MeV for region 1 and 1.25 MeV for region 2 SI1 L 0.667 1.25 $ fix energies: .667 MeV for region 1 and 1.25 MeV for region 2 SP1 0.4 0.6 $ 20% from src 1(Cs-137); 80% from src 2 (Co-60) c -- set positions of the 2 source cylinders DS8 S 9 10 $ get position for chosen source SI9 L -30 0 0 $ center for sampling of src 1 SP9 1 $ prob. distn for src 1 center SI10 L 30 0 0 $ center for sampling of src 2 SP10 1 $ prob. distn for src 2 center c -- set radius and axial limits for each source DS2 S 3 4 $ sampling distns from each src axis SI3 0 20 $ radial sampling limits for src1 SP3 -21 1 $ radial sampling weight for src1 r^1 SI4 0 10 $ radial sampling limits for src2 SP4 -21 1 $ radial sampling weight for src2 r^1 DS5 S 6 7 $ axial sampling distns for each src SI6 -10 10 $ axial sampling limits for src1 SP6 -21 0 $ axial sampling weight for src1 r^0 SI7 -30 30 $ axial sampling limits for src2 SP7 -21 0 $ axial sampling weight for src2 r^0 z x y source/.notdef2 sourse/.notdef1 30 -30
```

<!-- image -->

<!-- image -->

## Two Arbitrary Volumetric Sources with Different Energy Photons

```
c --- Two volumetric monoenergetic sources in complex-shaped cells 8 & 9 c Spatial sampling uses the rejection technique by placing a finite c cylinder over each source cell. A random point inside a cylinder c is accepted as a source point only if it is inside the source c cell. Location and size of the sampling cylinders and source c photon energies are functions of the source cells (FCEL). c SDEF CEL=d1 POS=FCEL d2 AXS=0 0 1 RAD=FCEL d5 EXT=FCEL d8 ERG=FCEL d20 c SI1 L 8 9 $ choose which cell source region to use for source SP1 0.4 0.6 $ 40% from src 1; 60% from src 2 c -- set POS for each source DS2 S 3 4 $ based on the cell chosen, set distribution for POS SI3 L -30 0 0 $ center for spatially sampling of source 1 SP3 1 $ prob. distn for src 1 center SI4 L 30 0 0 $ center for spatially sampling of source 2 SP4 1 $ prob. distn for src 2 center c -- set RAD for each source (must completely include cells 8 or 9) DS5 S 6 7 $ distns for sampling radially from each src axis SI6 0 20 $ radial sampling limits for src1 SP6 -21 1 $ radial sampling weight for src1 SI7 0 10 $ radial sampling limits for src2 SP7 -21 1 $ radial sampling weight for src2 c -- set EXT for each source (must completely include cells 8 or 9) DS8 S 9 10 $ distns for sampling axially for each src SI9 -10 10 $ axial sampling limits for src1 SP9 -21 0 $ axial sampling weight for src1 SI10 -30 30 $ axial sampling limits for src2 SP10 -21 0 $ axial sampling weight for src2 c -- set energies of photons for each source DS20 S 21 22 SI21 L 0.6938 1.1732 1.3325 $ Co-60 spectra for src 1 SP21 D 1.6312E-4 1 1 $ frequencies of gammas SI22 L 0.667 $ Cs-137 spectrum for src 2 SP22 D 1
```

<!-- image -->

## 3.6 Tally Specifications

The tally command F tells MCNP what information about the radiation
field should be calculated and output. MCNP6 has 12 basic tallies, which
together with 20 ancillary commands and several variations of the basic
tallies, allow the user to estimate a great many properties of the
radiation field, such as doses at important locations from both primary
and secondary particles.

With such flexibility afforded by the tally and associated commands, the
about 10% of the Manual is devoted to this topic. The theory supporting
the various types of tallies available in MCNP6 is given in Sections
2.5.1 to 2.5.9. The detailed description on the use of the tally and
associated commands is in Sections 5.9.1 to 5.9.20. Finally many
examples are provided in Section 10.2. A summary of available tallies in
MCNP6 is given below.

Table 5. Types of tallies available in MCNP. The type of particle tallied is denoted by pl .

| Mneumonic                                                                                | Tally Type                                                                                                                                                                                                                                                                                                                                                                 | Fn Units                                                                                            | *Fn Units                                                                                                 |
|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| F1: pl F2: pl F4: pl F5a: pl FIP5: pl FIR5: pl FIC5: pl F6: pl +F6 F7: pl F8: pl +F8: pl | Integrated current over a surface Average surface flux Average flux in a cell(s) Flux at a point or averaged on a ring pin-hole flux image planar radiograph flux image cylindrical radiograph flux image energy deposition averaged over a cell collison heating fission energy deposition in a cell energy distn of pulses created in a cell charge deposition in a cell | # # cm - 2 # cm - 2 # cm - 2 # cm - 2 # cm - 2 # cm - 2 MeV g - 1 MeV g - 1 MeV g - 1 pulses charge | MeV MeV cm - 2 MeV cm - 2 MeV cm - 2 MeV cm - 2 MeV cm - 2 MeV cm - 2 jerks g - 1 N/A jerks g - 1 MeV N/A |

Tallies are identified by a unique tally id integer m &lt; 10 8 , the last
digit of which specifies the tally type. Thus F4:P , F134:P , and
F748374:P are all tallies for the average photon flux in a cell(s).
Multiple F cards may be placed in Block 3. Thus, for example, one could
use F2:N , F12:P , and F22:E to give the average surface flux of
neutrons, photons, and electrons, respectively. Some tally types allow
multiple types of particles. For example, an energy deposition tally for
both gamma rays and electrons may be specified as F6:n,p . In the case
of collision heating, +F6 always applies to all particles in a problem;
therefore, this tally has no particle designator.

The most frequently used tallies for fixed source problems are current
at a surface ( F1 ), average flux at a surface ( F2 ), at a point or
ring ( F5 ), and flux averaged over a cell ( F4 ). Similar to flux
tallies over a cell are various tallies of energy deposition ( F6 and F7
). Unless otherwise specified with an FM card, tallies are normalized to
one source particle. Except for tallies F6 and F7 , designating a tally
as *F1:P , for example, multiplies the tally of each event by the photon
energy. This results in tallies of energy flux or energy current.
Tallies F6 and F7 are already in energy units.

The following sections describe the physical nature of several tallies.
In the description, time dependence is suppressed, which is the normal
case in MCNP calculations. The flux is integrated over time, and might
better be called the fluence.

## 3.6.1 The Surface Current Tally (Type F1 )

Each time a particle crosses the specified surface, its weight is added
to the tally, and the sum of the weights is reported as the F1 tally in
the MCNP output. Note that there is no division by surface area A . Nor
is there a distinction between direction of surface crossing. When used

§ 5.9.1

§ 2.5.1

§ 2.5.2.2

with problem geometry voided (zero density), the tally is useful for
verifying conservation of energy and conservation of number of
particles. Technically, if J ( r , E, Ω ) ≡ Ω Φ( r , E, Ω ) were the
energy and angular distribution of the flow (current vector) as a
function of position, the F1 tallies would measure

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where n is the outward normal to the surface at r s .

## 3.6.2 The Average Surface Flux Tally (Type F2 )

Figure 4. Particle crossing a surface at an angle θ i from the outward normal n .

<!-- image -->

Often the fluence, averaged over some surface (or portion of a surface)
is sought. Imagine a parallel surface a very small distance δ from the
surface of interest as shown in Fig. 4. The fluence (flux density
integrated over all time or all simulated histories) is just the
weighted sum of the path lengths of all the particles passing through
this incremental volume ∆ V = Aδ divided by the volume of the extended
region, i.e., Φ = ∑ i W i s i / ∆ V , where W i is the weight of
particle i . The path length for the particle shown is s i = δ/ | cos θ
i | where θ i is the angle between the particle's exit direction and the
outward normal n . Thus, the fluence contribution of the i th particle
crossing the surface is Φ i = lim δ → 0 ( W i δ/ | cos θ i | ) /Aδ = W i
/ ( A | cos θ i | ) = W i / ( A | Ω i · n | ). Every time a particle
crosses the surface, the value of its W i / cos θ i is added to the
tally. Of course, many histories may not cross the surface in question
and so no score is contributed to the tally. Finally, after N histories
the average fluence, per source particle , is estimated as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where n i is the number of surface crossing made by the i th particle, 8
W j i the i th particle's weight on its j th crossing, and θ j i is the
angle with respect to the outward normal at the j th crossing. Here Φ( r
, E, Ω ) is the energy and angular fluence normalized to one source
particle.

It should be noted that the variance of this fluence estimator is
infinite and, hence, the central limit theorem can not be used to
estimate confidence intervals. If many particles cross the surface in
nearly tangential directions, i.e., cos θ is very small, the tally
contributions becomes very large. To avoid such large scoring events,
MCNP sets | µ | = 0 . 0005 whenever | µ | &lt; 0 . 001 | . Because of this
approximation the F2 surface flux tally is not quite exact.

## 3.6.3 The Average Cell Flux Tally (Type F4 )

The idea behind the F2 tally, i.e., Φ = sum of path lengths in V /V ,
can also be extended to determine the average fluence in the volume of a
cell. In this type of tally, the sum of path lengths s i each particle
makes in the volume V of interest is accumulated (see Fig. 5). Again, if
a particle history never reaches the cell in question, then s i = 0. The
average fluence, per source particle, is then estimated as

8 Typically n i is 0 or 1. But a particle may make several crossing
especially if the surface is re-entrant.

<!-- formula-not-decoded -->

Figure 5. Particle paths in a cell of volume V .

<!-- image -->

particular, if R ( E ) = 1 or E one obtains F4 or *F4 , respectively.

where n i is the number of times the i th particle enters V , s j i is
the j th track length in V , and W j i is the particle's weight when
entering V for the j th time. By breaking the energy range into a
contiguous set of bins and adding each weighted path length to the tally
in the appropriate energy bin, the energy spectrum of the volume-average
fluence can be estimated as

<!-- formula-not-decoded -->

where ∆ E i is the width of the energy bin containing E i and S i is the
weighted sum of path lengths tallied in that energy bin. As before the
tally for each particle can be multiplied by some function R ( E ) so
that when the results in each energy bin are summed, the average value
of ∫ dE R ( E )Φ V ( E ) is estimated. In

If the volume V is large so that many histories enter it, the path-
length estimator is generally a good tally. If the region is a thin
curved shell most track lengths have similar lengths and the estimator
has a small variance. By contrast, for a regions bounded by two closely
spaced parallel planes, there may be a wide variation in the track
lengths through the region, and the resulting path-length estimator may
have a large variance. The path length estimator is also computationally
quite efficient, since particle tracking already computed the track
lengths in the regions, so little extra effort is needed for this tally.

## 3.6.4 Flux Tally at a Point or Ring Detector (Type F5 )

Point Detector A very powerful technique for scoring is to combine
deterministic tally contributions and the stochastic collisions that
occur during a history. One such estimator is the next event estimator .
To simplify description of this type of tally, assume that calculations
are being performed in a uniform medium. Consider the small spherical
detector, with cross sectional area dA , shown in Fig. 6. A particle
traveling in direction Ω ′ has a collision at r ′ . The collision may
not be a scatter, and even if it were a scatter, it is very unlikely to
scatter in the direction of the detector or even reach it to contribute
to the fluence tally for the detector. However, one can analytically
calculate the probability the particle will scatter at r ′ and reach the
detector without further interaction, and thus provide a contribution to
the fluence tally for the detector, thereby short-cutting the Monte
Carlo process.

The probability the particle with energy E scatters at r ′ through a
scattering angle θ s and has a new direction of travel in d Ω about Ω
with energy E ′ is 9

<!-- formula-not-decoded -->

where p ( ω s ) is the PDF (defined by the terms in the square brackets)
for scattering through an angle θ s = cos -1 Ω · Ω ′ . The distance
between r ′ and r d is R = | r ′ -r d | so that d Ω = dA/R 2 . The
probability that such a scattered particle actually reaches the detector
without further collision is p 2 = exp [ -µ t ( E ′ ) R ], where the
argument of the exponential is the total number of mean-free-path
lengths between r ′ and r d .

The flux density can be interpreted as the number of particles entering
a spherical detector of cross sectional area dA divided by dA [Shultis
and Faw, 2002]. Thus, the contribution to the fluence made by the
particle with weight W that interacts at r ′ is

<!-- formula-not-decoded -->

9 Here µ i is the interaction coefficient or macroscopic cross section
for interactions of type i . The Manual uses the symbol Σ i .

§ 2.5.6.1

Figure 6. A particle moving in direction Ω ′ makes a collision at r ′ and scatters towards a small spherical detector at r d of cross sectional area dA and a distance R = | r ′ -r d | from the scattering point.

<!-- image -->

This result is independent of dA and, thus, is used as a fluence tally
for a point detector at r d . After each interaction in a particle's
history, an estimate is made deterministically for the expected
contribution of that interaction to the fluence at point r d .

A difficulty with this point detector tally occurs when the tally point
lies within a scattering medium. Because of the 1 /R 2 term in the above
equation an enormous contribution is made to the tally if an interaction
occurs very near the tally point. In fact, in a scattering region the
variance of this estimator is infinite! An infinite variance, however,
does not mean the tally cannot be used; indeed the tally will converge,
but the asymptotic behavior is reduced to 1 / 3 √ N , slower than the 1
/ √ N convergence for a tally with a finite variance [Kalos et al.
1968]. Of course, if the tally point is in a vacuum or non-scattering
medium no such problem occurs.

MCNP avoids the infinite variance in a scattering medium by surrounding
the tally point by a small sphere of radius R o and, if an interaction
occurs with R &lt; R o , the F5 tally records the average fluence uniformly
distributed in the volume, i.e.,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Although the next event estimator can produce good estimates of the
fluence at a point, its convergence may be rather slow. Further, F5
tallies are computationally expensive because a tally contribution is
calculated every time a particle has any interaction even when it is far
from the detector and makes very many small and negligible contributions
δ Φ. This problem is aggravated with multiple F5 detectors.

Ring Detector If the problem is axially symmetric about one of the
coordinate axes, then a ring § 2.5.6.2 detector centered on the symmetry
axis experiences the same fluence at all points on the ring. With a ring
detector a point on the ring is randomly sample and the fluence
contribution δ Φ is calculated as for a point detector for each
interaction a particle makes. The advantage of a ring detector over a
simple point detector is that sampling the tally point on the ring can
be biased to obtain points closer to the interaction site, i.e., R is
smaller (and δ Φ larger) than if the sampling were uniform around the
ring. The biased sampling is discussed in Section 2.5.6.2 of the Manual
. Unlike the point detector, a ring detector has a finite variance.

## 3.6.5 Tally Specification Cards

At least one tally card is required, with the first entry on the card
being F n : pl , in which n is the tally id number (the last digit of
which determines the type of tally), and pl stands for N (neutron
tally), P (photon tally), N,P for joint neutron and photon tallies, and
E for electron tallies. Following the tally type is a designation of the
surfaces for the tally (types F1 and F2 ), or the cells (tally F4 ). For
the type 5 detector tally, there follows a designation of the position
of the detector. The energy deposition, pulse-height, and other
specialized tallies are not discussed in this primer. In the subsections
below, several examples are given to demonstrate the parameters on the F
n : pl card.

## Surface and Cell Tallies: The card

<!-- formula-not-decoded -->

specifies electron current tallies through surfaces 1 and 2, and the
total ( T ) over both surfaces. Note that the current tally is not
divided by surface area. The card

<!-- formula-not-decoded -->

specifies photon surface-integrated fluence tallies for surface 1, the
average over surfaces 1 and 2, the average over surfaces 2 through 4,
and the average ( T ) over all surfaces 1 through 4. Similarly, the card

<!-- formula-not-decoded -->

specifies cell-averaged neutron fluence tallies for cell 1 and for cells
2 through 4. No composite average is called for.

Point-Detector Tallies: In the sense of an experiment or a Monte Carlo
calculation, as the volume of a cell approaches zero, the path length
segments in the cell and the number of particles intersecting the
surface of the cell also approach zero and, hence, the flux tally
becomes indeterminate. However, there is a way of computing the flux at
a point by using the deterministic last-flight-estimator tally F5. This
tally is invoked by a card such as

<!-- formula-not-decoded -->

Here 75 is the tally number, the last digit 5 denotes the F5 tally type,
and P specifies the tally is for photons. The values of X , Y , and Z
specify the coordinates of the point detector, and R designates the
radius of a spherical exclusion zone surrounding the detector point. The
need for an exclusion zone is evident from the 1 /r 2 term in the flux
contribution tallied, namely,

<!-- formula-not-decoded -->

where r is the distance between the particle interaction site and the
point detector. If r approaches zero, the tally contribution approaches
infinity. Such large contributions make the F5 tally much less stable
than the cell ( F4 ) or surface ( F2 ) flux tally. This instability is
minimized by establishing a spherical 'exclusion volume' of radius R
centered on the point detector. For interactions occurring within this
exclusion zone, an abnormally large tally contribution is avoided by
scoring the fluence uniformly averaged over the exclusion spherical
surface. The exclusion radius R can be specified, as a positive number
(centimeters, and is the preferred method), or a negative number (mean
free paths). Typically, R should be about 0.2 to 0.5 mean free path
(averaged over the energy spectrum at the sphere). For a point detector
inside a void region, no interactions can occur near the detector and R
should be set to zero. Finally, several point detectors may be specified
on one tally card, e.g.,

<!-- formula-not-decoded -->

Ring Detectors: The manual also describes the use of a ring detector -
useful for problems with symmetry about one of the problem axes. The
form of this command is

<!-- formula-not-decoded -->

where n is the tally number (last digit 5), a is X , Y , or Z to denote
the symmetry axis, pl the particle type (P,N,...), a o distance along
axis a where the plane of the ring intersects the axis, r is the ring
radius, and R o is the exclusion radius around the ring (as discussed
above).

§ 5.9.1.1

§ 5.9.1.2

§ 5.9.1.2.2

The MCNP6 Manual describes 20 optional commands that modify the output
from a specified type of tally. Three such tally modification commands,
which are frequently used, are sorting a tally into energy bins (the En
card), multiply a tally by some quantity (the FMn card), and multiply
each tally contribution by a fluence-to-response conversion factor (the
DEn and DFn cards). These are

- 3.6.6 Cards for a Few Optional Tally Features § 5.9.2 to § 5.9.20 addressed individually below.
- The Tally Energy Card: Suppose one wanted to divide the total flux or current normally produced § 5.9.3 by tally Fn into energy groups, say E1 to E2 , E2 to E3 , and E3 to E4 . This might be useful, for example, to isolate an uncollided component of the flux. This may be accomplished by use of a tally energy card (En card), such as

<!-- formula-not-decoded -->

With this card the results for tally 24 (of type F4 ) are binned into
four energy groups where E1 , E2 , E3 and E4 are the group (bin) upper
limits. The lowest bin would extend down from E1 to zero (or to a
specified cutoff energy ) for the type of particle being tallied. To
create m equispaced bins between E1 and Emax use

<!-- formula-not-decoded -->

If all tallies in a problem have the same energy group structure, a
single card may be used, with En replaced by E0 .

- The Energy Multiplier Card: Associated with the tally energy card is an optional energy multiplier § 5.9.9 EMn card of the form

EMn M1 M2 M3 M4 $ multiply energy bin k by Mk

Here the multiplier Mk is applied to each contribution to the tally for
the k th energy group. This card is useful, for example, to convert a
fluence per source photon to a flux per curie source strength. For this
example, one would add the following EM card for, say tally F64 .

<!-- formula-not-decoded -->

The units of tally F64 would then be 'photons (cm -2 s -1 ) per Ci.'

- Dose Energy and Function Cards: Suppose one wanted to compute a dose rate of some type § 5.9.8 associated with a flux or current tally, either total or by energy group. For example, suppose one wanted to compute

in which /Rfractur ( E ) is a fluence-to-dose conversion factor. MCNP
will carry out this calculation, obtaining values of /Rfractur ( E ) by
interpolation of values specified in a table placed in the input file.
The form of the table is

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Entries E1 through Ek are tabulated values of energy and F1 through Fk
are corresponding tabulated values of /Rfractur ( E ). Entries A and B ,
either LOG or LIN , specify linear or logarithmic interpolation. If
omitted, the default is logarithmic interpolation for both variables. If
all tallies are to have the same dose conversion factors, a single
table, designated by DE0 and DF0 , may be used to avoid repeating the
table.

- The Tally Comment Card: If tallies are modified, it is good practice to explain the modification § 6.9.2 in a comment card that will be printed in the output file for the calculation. For example, an explanation of tally Fn could be entered in the card

FCn This tally has units of Sieverts per source photon

Continuation lines may be added so long as there are blanks in columns 1
through 5.

## 3.6.7 Miscellaneous Block 3 Commands

The Mode Card: This card is used to specify the type of particles to be
to be tracked. Every input file must have a MODE card somewhere in block
3 of the input file. In the command line MODE x , the variable x may be
just a single particle such as P , E , etc. or a combination such as N P
E . A minus sign [ -] in front of a particle's symbol means the
antiparticle. Thus MODE E F , MODE E -E , and MODE F -F are equivalent.

Time and History Cards: The usual method for limiting how long MCNP runs
is to specify either the maximum number of source particle histories or
the maximum execution time. The maximum number of histories N is
specified as NPS N . Alternatively, the maximum computing time T , in
minutes, may be specified by the card CTME T .

The Print-and-Dump Cycle Card: By default, an output file is created
only at the conclusion of a calculation, a binary continuation file,
RUNTPE, is written every 15 minutes, and no tally-plot file, MCTAL, is
written. Options to control the dump cycle are provided by the PRDMP
card

PRDMP NDP NDM MCT NDMP DMMP

Here NDP is the increment for printing tallies in the output file ( &gt; 0
the number of histories, &lt; 0 the time in minutes, = 0 for no
intermediate dump); NDM is the increment for writing a continuation
RUNTPE file ( &gt; 0 the number of histories, &lt; 0 the time in minutes, = 0
to suppress all intermediate dumps); MCT is a flag to write tallies for
plotting (1 yes, 0 no); NDMP is the maximum number of dumps written in
the RUNTPE file (all by default); and DMMP is related to the use of
multiple processors in the execution of MCNP. A typical card might read

```
PRDMP 0 -60 $ create continuation RNTPE every 60 min.
```

With this card, at most, 60 minutes of computing time would be lost if a
calculation were aborted.

## 3.6.8 Short Cuts for Data Entry

- nR repeats the preceeding entry n times. Thus IMP:n 2 4R produces IMP:n 2 2 2 2 2 .
- nI generated n linear interpolates. Thus E24 1 3I 5 produces E24 1 2 3 4 5 .
- xM multiplies previous entry by x . Thus IMP:n 2 2X 3X 2X produces IMP:n 2 4 12 24 .
- nJ jumps over n items. Thus PHYS:P 4J 1 changes the default physics PHYS:p 100 0 0 0 0 J 0 PHYS:p 100 0 0 0 1 J 0 .

## 3.7 Running MCNP6

If the input file is named inp , then running MCNP is as simple as
entering the the command MCNP6 in the MCNP command (DOS) window, which
the installation of MCNP placed on your computer's desktop (after the
window is set to the directory containing inp ). However, one generally
also specifies additional information. The general form of the
executable command is mcnp6 KEYWORD=value ... KEYWORD=value
execution\_option(s) other\_options where each instance of KEYWORD is one
of 25 MCNP6 default file names (see Table 3.4 of the Manual ) that the
user wants to change, execution option(s) specify which of 5 execution
module(s) are to be run, and other option(s) provides the user with
additional execution control. The KEYNAME requires only enough letters
of the default name to identify it uniquely. Much of this file renaming
and option specification can be placed in block 0 (message block) of the
input file to minimize typing for the MCNP6 executable command.

Interrupting a Run:

MCNP6 allows the following interactive interrupts while running.

〈 ctrl+c 〉 , k kills the job immediately without normal termination. If
this re- quest fails, enter 〈 ctrl+c 〉 three or more times. 〈 ctrl+c 〉 ,
q stops the job normally after the current history 〈 ctrl+c 〉 , s gives
the status of the job (number of particles and collisions pro-

cessed so far and the time used)

§ 5.7.1

§ 5.13

§ 5.13.5

§ 3.3.2

## 4 Variance Reduction

The challenge in using MCNP is to minimize the computing expense needed
to obtain a tally estimate with acceptable relative error (as well as
satisfying nine other statistical criteria). For many deeppenetration
problems, a direct simulation (analog MCNP) would require far too many
histories to achieve acceptable results with the computer time
available. For such cases, the analyst must employ 'tricks' to reduce
the relative error of a tally (or its variance) for a fixed computing
time, or to reduce the computing time to achieve the same relative
error.

Two basic approaches can be applied to reduce the computational effort
for a particular problem: (1) simplify the MCNP model, and (2) use non-
analog simulations. In the first approach, the model geometry and the
physics used to simulate particle transport can often be simplified or
truncated . For example, it is a waste of computing effort to use a
detailed geometric model of a region that is far from the detector tally
location and that has little influence on the radiation field near the
detector. Similarly, it is a waste of computer time to track neutrons as
they thermalize in a shield if only the fast neutron fluence in some
structural component is sought. For such a problem, once a neutron
leaves the fast energy region, it can be killed without affecting the
tally.

The second basic approach to reduce the variance of a tally is to modify
the simulation process itself by making certain events more or less
probable than actually occur in nature. Such a modified simulation is
referred to as nonanalog Monte Carlo. As discussed in this section, MCNP
has many nonanalog options many of which an analyst can use in
combination to make a difficult analog problem much more tractable.
These nonanalog tricks can be categorized into three general methods:
(1) population control, (2) modified sampling, and (3) partially-
deterministic calculations. In population control, for example, the
number of particles in regions of high/low importance can be
artificially increased/reduced. In modified sampling methods, certain
events can be altered from their natural frequencies. Finally, in the
partially-deterministic methods, part of the random-walk simulation can
be replaced by a deterministic point-kernel type of calculation.

## 4.1 Tally Variance

Before discussing the tricks used to reduce the variance of MCNP
tallies, it is appropriate to examine § 2.6.1 exactly what it is that we
are trying to reduce. When we run a Monte Carlo simulation, the i th
history contributes a score x i to the tally. If the particle (or its
daughters) never reaches the tally region, then x i = 0, whereas, if it
reaches the tally without interaction, the score x i often is very
large. The probability any history will contribute a score between x and
x + dx is denoted by p ( x ) dx where p ( x ) is a probability
distribution function (PDF). In an MCNP simulation, we seek the mean
score (or expected value) of x , namely

<!-- formula-not-decoded -->

Unfortunately, we don't know p ( x ) a priori (although MCNP will
construct it and generate a plot of it - see Section 2.6.8.6). Instead,
MCNP approximates 〈 x 〉 by the average x of the scores of N particles,
i.e.,

<!-- formula-not-decoded -->

As N →∞ , the strong law of large numbers guarantees that x →〈 x 〉 ,
provided 〈 x 〉 is finite.

The variation in the different scores x i is measured by the standard
deviation of the population (histories), which for large N

<!-- formula-not-decoded -->

where

The estimated variance of the average x is then

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The central limit theorem states that if we repeated the simulation a
large number of times (each with N histories), the variation of the
means x from each simulation will be distributed normally about the true
mean 〈 x 〉 and have a variance S 2 x . It is this uncertainty or
variance we are trying to reduce in our MCNP simulations, i.e., for a
fixed number of particles, we seek an estimate x which has the least
uncertainty or minimum S x .

## 4.1.1 Relative Error and FOM

In any variance reduction method, we change the simulation and hence
change the underlying distribution p ( x ) so that it produces fewer
zero-score histories and becomes more concentrated about its mean 〈 x 〉
. By making p ( x ) more concentrated about its mean (which remains the
same as the mean of the analog PDF), the variance of the mean S 2 x will
be less than that of the analog PDF, i.e., our estimate of the mean will
be more precise.

For each tally, MCNP not only calculates the sample mean x , but several
other statistics. One of the most important is the relative error R
defined as

<!-- formula-not-decoded -->

Clearly, we want to make R as small as possible with as few histories as
possible. As discussed in the manual, R generally must be less than 0.1
for meaningful results (and even smaller if point/ring detectors are
used). From Eqs. (7) and (8), it is seen that R ∼ 1 / √ N . Thus
increasing the number of particle histories is generally a very poor way
of reducing R . This property of the relative error is the great
weakness of the Monte Carlo method, because, generally, many histories
must be generated to obtain acceptable results.

Another important statistic generated by MCNP is the figure of merit
(FOM). This is defined as

<!-- formula-not-decoded -->

where T is the simulation time, which is proportional to N the number of
histories run. Since R 2 ∼ 1 /N , we see that, except near the beginning
of the simulation, the FOM should remain relatively constant. Also, for
different simulations of the same problem, the simulation with the
largest FOM is preferred since it requires the least time or produces a
specified relative error.

Now on to ways of how to perform nonanalog techniques with MCNP.

## 4.2 Truncation Techniques

The basic idea behind truncation methods is to reduce the time per
particle history by either simplifying the geometry or the physics used
to generate the random walk for each particle. Proper application of
this approach for variance reduction requires considerable experience
and intuition by the analyst, since any simplification in the geometry
or physics introduces a bias into the tally. Although a very precise
(i.e., low variance or relative error) can be achieved, the tally
estimate may not be very accurate . Generally, multiple runs with
different approximations must be made to assess the importance of any
simplification. MCNP can give you no warning about errors caused by
geometric simplifications. Even for physics simplifications, MCNP
produces, at best, a warning in the output, but no indication of whether
serious bias has been introduced.

§ 2.6.4

2.6.5

§

## 4.2.1 Energy, Time and Weight Cutoff

- The CUT command is used to specify a minimum energy, time, or particle weight below which the § 5.7.4.1 particle is killed. The values specified on the CUT card apply everywhere in the geometry. Here is an example:

CUT:p j 0.075 $ kill photons with E &lt; 75 keV

In this example, whenever a photon falls below 75 keV, it is killed. The
CUT command has 5 parameters. The first is a time limit for an
individual history, which in the above example is specified as j to jump
over the default value of a very large time. Parameters 3 to 5 are
limits on the weights of particles.

- The ELPT is like the CUT card, but allows you to specify the cutoff on a cell-by-cell basis. For § 5.7.4.6 example,

<!-- formula-not-decoded -->

terminates photons in cell 1, 2, 3, 4, and 5 that have energies less
than 10, 20, 30, 40, and 50 keV, respectively. Should both the ELPT and
the global CUT commands be used, the higher limit prevails.

The CUT and ELPT commands are particularly useful for energy deposition
tallies for which low energy particles make little contribution.
However, for neutron problems, use CUT and ELPT carefully since low
energy neutrons cause most of the fissions and produce most of the
capture gamma photons.

## 4.2.2 Physics Simplification

- The PHYS command is used to specify energy cutoffs and the physics treatments to be used for § 5.7.2 photons, neutrons and electrons. Each particle has different parameters which are specified with this command.

Photons: There are two inherent physics approximations for photon
interactions in MCNP: (1) only K and L edges are considered for
photoelectric interaction, and (2) no triplet production (pairproduction
near an orbital electron). In addition, other physics simplifications
can be imposed with the PHYS card. This card has the form

PHYS:P EMCPF IDES NOCOH PNINT NODOP

The EMCPF parameter is the energy in MeV above which simple physics is
to be used. In simple physics, no fluorescence from photoelectric
interactions is produced, no binding effects are used in photon
scattering, and no coherent scattering is included. IDES = 0 / 1
indicates that Bremsstrahlung is included/ignored for MODE P and, for
MODE P E , electron production and transport is used/not used. NOCOH = 0
/ 1 specifies that coherent scattering is included/ignored. PNINT = -1 /
0 / 1 indicates photonuclear interactions are used in an analog manner /
not used / used with a bias. If PNINT = 0 there must be a MPNn card
following the material Mn card. Finally, NODOP = 0 / 1 turns Doppler
broadening (from the speed of bound electrons) on/off. The default is

/negationslash

PHYS:P 100 0 0 0 0 $ 100 MeV, brems, coh scat, no photonuc, Doppler

The various physics options selected can greatly affect the run time,
especially if electron transport is turn on. As an example of how
different physics simplifications can affect the run time, consider a
point isotropic source emitting 7-MeV photons into an infinite iron
medium. The ambient dose equivalent 20 cm from the source is estimated
by using an F2 spherical surface detector. In Table 6 the tally mean and
the runtime are shown for different physics assumptions. Notice that
turning Bremsstrahlung off more than halves the compute time with only
about a 15% reduction in the estimated dose. Thus, the no Bremsstrahlung
option is very effective for initial scoping calculations. Also notice
that using simplified photon physics increases the compute time, a
mystery to the authors. Although not shown in the table, if secondary
electron transport had been used instead of the thick-target
Bremsstrahlung approximation (by invoking the MODE P E command) the
compute time is very much longer (about 1700 minutes for the test
problem). Use electron transport only when necessary!

Table 6. MCNP6.2 results with different physics models for a point 10-MeV photon source in an infinite lead medium. Tally is the ICRP 1987 ambient dose equivalent at 5 cm from the source. Results are for simulations of 4 × 10 6 source photons, split among 8 tasks, on an Apple M2 Pro Mac Mini All cases passed the 10 statistical tests, unless otherwise noted.

| MCNP6 Commands             | Description*                                    |   F2 Tally (Sv/photon) |   Relative Error | FOM     |   mcrun Time (min) |
|----------------------------|-------------------------------------------------|------------------------|------------------|---------|--------------------|
| PHYS:P 100.0 0 0 0 0 J 0   | default: dphys + brem + coh + no pn + dop       |            1.2061e-14  |           0.001  | 293 393 |               3.31 |
| PHYS:P 10.0 0 0 0 1 J 0    | dphys + brem + coh + no pn + no dop             |            1.20597e-14 |           0.001  | 293 685 |               3.26 |
| PHYS:P 10.0 0 1 0 1 J 0**  | dphys + brem + no coh + no pn + no dop          |            1.20609e-14 |           0.001  | 290 038 |               3.21 |
| PHYS:P 0.0 0 0 0 0 J 0***  | sphys + brem + coh + no pn + dop                |            1.20775e-14 |           0.001  | 148 802 |               6.6  |
| PHYS:P 0.1 0 1 0 1 J 0     | sphys > 10 keV + brem + no coh + no pn + no dop |            1.20873e-14 |           0.001  | 145 006 |               6.73 |
| PHYS:P 10.0 1 1 0 1 J 0    | dphys + no brem + no coh + no pn + no dop       |            7.11461e-15 |           0.0015 | 864 296 |               0.49 |
| PHYS:P 0 1 1 0 1           | sphys + no brem + no coh + no pn + no dop       |            7.11551e-15 |           0.0015 | 965 105 |               0.44 |
| no PHYS card CUT:p j 0.1** | default: + kill photons if E < 0 . 1 MeV        |            1.20321e-14 |           0.001  | 696 922 |               1.32 |

* dphys = detailed physics, sphys = simple physics; coh = coherent
scatter; pn = photonuclear brem = Bremsstrahlung; dop = Doppler
broadening

** Did not pass VoV Decrease Rate Test

*** Did not pass PDF Slope Test

Neutrons: MCNP with its integrated neutron cross section libraries is an
ideal tool for neutron transport studies. Nevertheless there are several
approximations MCNP uses for neutron interactions: (1) secondary
particles from neutron interactions are sampled independently, (2)
delayed gammas from fission products are ignored so about one-half of
the steady-state gamma-ray energy is ignored, (3) treatment of
temperature effects with the S ( α, β ) method is limited to about 15
moderators, and (4) the number of fission neutrons is always sampled
from the closest two integers about ν ( E ).

For neutrons the PHYS card has only four parameters, namely

## PHYS:N EMAX EMCNF IUNR DNB

The EMAX parameter is the energy in MeV above which neutron data is not
placed in memory (default is very large). Neutrons below EMCNF (in MeV)
are treated by analog capture while above EMCNF implicit capture is used
(see next section). If IUNR = 1 the averaged cross sections above the
resolved cross section region are used, while if IUNR = 0 (the default)
probability tables, describing interactions over the myriad levels and
widths of the unresolved resonances, are sampled. The final parameter
DNB specifies if ν ( E ) includes prompt plus delayed neutrons (= -1,
the default), or if only propmt neutrons are included (= 0), or if DNB (
&gt; 0) delayed neutrons per fission are to be used. Here is an example.

PHYS:n 5.0 0.1 $ max sigma table energy; analog capture below 100 keV

Here cross section data only below 5 MeV is retained (to save data
storage memory). For neutrons

below 0.1 MeV, analog absorption (direct simulation) will be used, while
above 0.1 MeV, implicit absorption is used.

## 4.2.3 Histories and Time Cutoffs

Normally an MCNP run is terminated when a certain number of particle
histories have been run § 5.13.1.1 , § 5.13.1.2 or a desired computing
time has been exceeded. These cutoffs are specified by the NPS and CTME
commands such as

```
NPS 1000000 $ stop after a million source particles have been run CTME 20.0 $ stop run after twenty minutes
```

If both are specified, the first cutoff to occur causes program
termination.

## 4.3 Nonanalog Simulation

In many problems, very few of the source particles reach the detector or
region used for the tally, i.e., most particles produce a zero score .
The number of particles reaching the tally region can, however, often be
dramatically increased by abandoning a strict analog simulation. Of
course, the expected value of the tally must not be changed. How can the
tally remain unchanged when we artificially force more particles to the
scoring region? The key is to assign each particle a weight , and, as
the particle is 'forced' towards the scoring region, the particle weight
is decreased in a manner such that the average of the particle weights
reaching the detector is the same as the expected tally in a true analog
simulation. Thus, if we make a certain event in a particle history m
times more likely, we must multiply the particle's weight by 1 /m to
avoid biasing the tally expectation.

MCNP has many nonanalog simulation options whose use, often in
combination, can decrease the variance of a tally without increasing the
computational expense.

## 4.3.1 Simple Examples

To understand the basic idea of nonanalog techniques, consider the
simple slab transmission problem illustrated in Fig. 7. In this problem
a point isotropic source is placed on one side of a slab shield, and the
problem is to determine the fraction of source particles that reach the
opposite face of the slab. A direct analog simulation is represented by
Fig. 7(a).

Figure 7. Examples of analogue and nonanalogue Monte Carlo simulations.

<!-- image -->

æ

Source Biasing: A non-analog simulation can considerably reduce the
computing effort compared to an analog simulation. For example, in the
analog simulation half of the source particles are

'wasted', i.e., those emitted away from the slab cannot reach the
scoring surface and computer time is wasted sampling backward source
directions and tracking these particles to the left problem boundary. It
would be more efficient to start each source particle towards the slab,
as shown in Fig. 7(b). However, by restricting or biasing the source
emission directions to only those oriented toward the slab, twice as
many particles will subsequently penetrate the slab in case (b) compared
to analog case (a), for the same number of particle histories tracked.
To avoid doubling the transmission tally (no. transmitted per real
(analog) source particle), we adjust the source particle's weight in the
biased simulation to be 0.5. Thus the average of the weights of
transmitted particles still equals the particle transmission fraction
obtained with the analog simulation. Moreover, for the same number of
source particles, twice as many reach the tally surface in case (b)
compared to case (a), and thus the variance of the case (b) tally is
less.

Splitting: Another technique for increasing the number of particles
reaching the scoring surface is illustrated in Fig. 7(c). Here the slab
is conceptually divided into two sublayers. Whenever a particle crosses
from the layer nearest the source to the layer nearest the tally
surface, it is split into two particles, each with half of the original
particle's weight and both moving with the same velocity as the original
particle. The random walk simulation is then performed independently for
each new particle, beginning at the entry point into the second layer of
the original particle. Twice as many particles will now reach the tally
surface (thereby reducing the tally's variance); but, since their
weights have been reduced by one-half, the expected tally value remains
unchanged.

Russian Roulette: When a particle reaches a region of space far from the
tally region it is unlikely, with further random walk simulation, to
reach the tally region, and the run time can be reduced by terminating
or killing such a particle. Thus, in the example case (c), when a
particle in the right-hand sublayer returns to the first left sublayer,
we may think it has a relatively poor chance of returning yet again the
right sublayer and reaching the tally surface. When a particle renters
the first layer from the second, the particle is hence killed with a
probability of 0.5. If the particle survives this winnowing process, its
weight is increased by a factor of two, to keep the simulation unbiased,
and the particle's random walk continues.

Implicit Absorption: Those particles which are tracked through the slab
but are absorbed before they reach the tally surface represent wasted
computing effort. Another variance reduction trick is to replace analog
capture with implicit capture . At a collision site, a particle is
killed, in an analog simulation, with a probability σ a /σ t (analog
capture). However, in implicit capture, the particle is allow to
continue on its trajectory as if no interaction had occurred but with
the particle's weight changed to 1 -( σ a /σ t ) times its original
weight. In this way, no particles are lost due to absorption, but
absorption effects are properly accounted for.

## 4.4 MCNP Variance Reduction Techniques

MCNP offers a variety of variance reduction techniques based on
different nonanalog simulations. The art of using MCNP to solve
difficult problems is to use these program features to obtain both
precise and computationally efficient results. In this section, the use
of several of the most useful variance reduction techniques are
described.

The variance reduction techniques offered by MCNP can be categorized as
follows:

1. Population Control Methods: These methods artificially increase/decrease the number of particles in spatial or energy regions that are important/unimportant to the tally score. Specific population control methods include
- Geometry splitting and Russian roulette ( IMP )
- Weight cutoff ( CUT , PWT )
- Energy splitting/roulette ( ESPLT )

§ 2.7.2.1-4 , § 5.12

- Weight windows ( WWE , WWN , WWP , WWG , WWGE )
2. Modified Sampling Methods: These methods artificially increase the likelihood of events that increase the probability a particle reaches the tally region. Included in MCNP are
- Exponential transform ( EXT , VECT )
- Forced collisions ( FCL )
- Implicit capture ( PHYS )
- Bremsstrahlung biasing ( BBREM )
- neutron-induced photon production biasing ( PWT )
- source direction and energy biasing ( SDEF , SP , SB , SI )
3. Partially Deterministic Methods: These method replace the random-walk process by a deterministic process (e.g., exponential attenuation) to move particles from one region to another. In MCNP the following are available:
- Point and ring detectors ( F5a )
- Correlated sampling ( PD )
- DXTRAN spheres ( DXT , DXC )

The selection of effective variance reduction methods for a particular
problem requires considerable experience and skill on the part of the
analyst in interpreting the MCNP output. To gain experience in using
these variance reduction techniques, the novice is encouraged to try
using them on simple problems, sometimes separately and sometimes in
various combinations. Through such experimentation, valuable experience
and insight into variance reduction is gained. In the sections below,
some of the simpler variance reduction techniques are discussed and
illustrated.

## 4.4.1 Geometry Splitting

- In geometry splitting, importances are assigned to each cell in the problem. Generally, cells near the § 2.7.2.7 , § 5.12.1 tally region should have a greater importance than cells farther away. When a particle leaves a cell with importance I 1 and enters a cell of importance I 2 , the particle is split/rouletted according to the ratio I 2 /I 1 . For example, if I 2 /I 1 = 2 . 75 the entering particle is split into three particles with 75% probability and into two particles with 25% probability. If I 2 /I 1 = 0 . 6, the entering particle is killed with 40% probability and allowed to survive with 60% probability. Of course, in each splitting or Russian roulette the weight of the remaining particles is adjusted to leave the tally unbiased. This technique of geometry splitting with Russian roulette is very reliable since, if no other biasing techniques are used, all the particles in a cell will have the same weight regardless of the paths taken to reach the cell. The importance of a cell can be defined on the cell definition line, such as

```
c Set cell importance on the cell definition line 20 1 -7.86 10 -20 IMP:p=7 $ cell 20; matl 1; density; defn; importance
```

or the importances of all cells can be set in Block 3 with the IMP
command

```
c Set cell importances in a geometric progression IMP 1 2m 2m 2m 2m 2m 0 $ import. of cells 1--7 = 1 2 4 8 16 32 0
```

The importance of a cell is intimately related to the average adjoint
fluence in the cell (a quantity generally not known a priori ). As a
practical matter, the cell importances should be adjusted so as to keep
the population of particles in the cells relatively constant as one
moves from the source region to the tally region. First, perform a short
run with all importances set to unity, examine the 'cell population'
found in output print table 126, and estimate the cell importances by
the ratio of cell populations P in adjacent cells, i.e. I n
/similarequal P n -1 /P n . Typically, source cells have an importance
of unit and cells closer to the tally region have larger importances.

Adjacent cells should not have importances that are greatly different.
As a rule, the ratio of importances in adjacent cells should not exceed
a factor of 6 to 8. Consequently, it is often necessary to subdivide
cells into many cells to prevent adjacent cell importances from changing
too rapidly. It should also be remembered that, when Russian roulette is
used to terminate some particles, information is lost; subsequent
building up the particle population with large cell importances cannot
regain this lost information.

A warning about large importances. In problems with large attenuation of
particles between the source and tally region, importances of cells near
the tally can reach many orders of magnitude. For these cases, if a VOID
command is used to flood the geometry with particles in order to find
geometry errors, the cell importances are still in effect, and a few
source particles will be magnified into millions of particles, all of
which MCNP must track. Instead of a short run, hours or days can be
required!

## 4.4.2 Weight Windows

The weight-window variance reduction technique adjusts the weights of
particles as they change energy and move through the various cells in
the problem geometry. In each cell, a lower weight bound and an upper
bound (defined as a multiple of the lower bound) are specified. If a
particle entering a cell or a particle created in the cell has a weight
above the upper bound, the particle is split such that all split
particles are within the weight window. Similarly, if a particle has a
weight below the lower bound, Russian roulette is used to increase the
particle's weight until it lies within the window or until it is killed.
In most problems weight-windows is preferred over importance biasing.

## Advantages:

- Weight-windows can equalized the weights of scoring particles, by requiring important regions to have small weight windows, thereby producing a tally with a small variance. (Recall if every particles gives the same score, an answer with zero variance is obtained.)
- The weight-windows variance reduction technique is a space and energy biasing scheme, whereas importance sampling is only a spatial biasing technique.
- Weight window discriminates on particle weight before taking appropriate action. Geometry splitting is done regardless of the particle's weight.
- Weight windows uses absolute bounds, whereas geometry splitting is based on ratios so that a particle's weight can grow or decrease without limit. This is particularly useful when using ring and point detectors with which large particle weights can cause large tally perturbations.
- Weight windows is applied at surfaces and collision sites whereas geometry splitting occurs only at surfaces.
- Weight windows is immune to weight fluctuations caused by other biasing techniques, whereas geometry splitting preserves such fluctuations.
- Weight windows can be turned off in large cells, in which no single importance applies, by setting the lower limit to zero.
- Weight windows can be generated automatically by MCNP whereas cell importances requires considerable insight by the user.
- Weight windows is more compatible with other variance reduction techniques such as the exponential transform.
- Weight Windows can be based on user-defined meshes superimposed on the geometry.

## Disadvantages:

- Weight windows is not as straight forward as geometry splitting. Without the automatic weight-window generator, weight windows would be very difficult to use since window limits of each cell are difficult to predict. By contrast, cell importances are much easier to guess.

§ 2.7.2.12 , § 5.12.3

- When the weight of source particles is changed, the weight-window limits have to be renormalized.
- Generating Weight Windows The weight-windows biasing is specified with the WWE , WWN , and WWP § 5.12.14.1 commands. The reader is referred to the manual for the command parameters. However, the nonexpert rarely enters these command directly; rather, the weight-windows generator is usually used to automatically calculate these commands and their parameters.

To use the weight-window generator, the WWG (and, optionally, the WWGE )
commands are placed in Block 3 of the input file. The WWG command is

<!-- formula-not-decoded -->

where I t is the tally number, I c is a reference (usually source) cell,
10 W g is the value of generated lower weight-window bound (if 0, set to
0.5 of source particle weight), the next four parameters are not used
and simply 'jumped' ( j ) over, 11 and I E = 0 specifies the generated
WWGE card is for energy bins while I E = 1 means time bins are used.

The optional WWGE can be included generate weight windows for a set of
contiguous energy bins. This command is

```
WWGE: n E 1 E 2 . . . E j
```

where n = N / P / E for neutrons/photons/electrons, E i is the upper
energy bound for weight-window group ( E i +1 &gt; E i ), and j is the
maximum number of energy groups ( j ≤ 15).

As an example, for a point photon source in cell 10 and tally F2 , the
following weight-window generator command

```
WWG 2 10 0 j j j j 0 $ generate weight windows using energy bins
```

is placed in Block 3 of the input. Near the end of the resulting output
file, lines similar to the following appear.

```
wwp:p 5 3 5 0 0 0 wwe:p 1.0000E+02 wwn1:p 5.0000E-01 5.0000E-01 4.0810E-01 2.5853E-01 1.5586E-01 9.1319E-02 5.2707E-02 3.0064E-02 1.6959E-02 9.4621E-03 5.2438E-03 2.8816E-03 0.0000E+00 -1.0000E+00
```

The ten leading blanks on these lines are edited out, the weights
inspected and changed if necessary to ensure there are no spurious
fluctuations (caused by incomplete sampling), and then these lines are
placed in Block 3 of the input for a second run. This interation process
can be repeated to perfect the 'best' weight windows.

## 4.4.3 An Example

Consider a point isotropic source emitting 7-MeV photons surrounded by
an iron annular spherical shell 30-cm in thickness with an inner radius
of 30 cm. The ambient dose 160 cm from the source is sought. Three
approaches are used: (1) analog simulation, (2) geometty splitting, and
(3) weight windows. The MCNP input file for the analog simulation is
shown in Fig. 8.

With this thick iron shield, few source particles penetrate the shield,
and hence we need to use some biasing technique to help particles
through the shield. This problem is ideally suited for geometry
splitting. To implement this, split the 30-cm spherical cell into 10
cells, each 3-cm in thickness. Examination of the output produced when
this 10-cell shield problem is run as an analog simulation shows that
the photon population in each shield cell decreases by about a factor of
two

10 If &lt; 0 weight windows is based on a user specified mesh, but we do
not discuss this in this primer.

11 These parameters were used in debugging the weight window algorithm.

<!-- image -->

```
Point isotropic 7-MeV photon sources in iron shell: (analog base case): c ********************* BLOCK 1: CELL CARDS ***************************** c GEOMETRY: X isotropic point source (7-MeV) c D ambient dose 100 cm from outer shield surface (160 cm) c iron shield 30-cm thick (r=30 to 60 cm) c (without shield, dose is 6.013x10^{-17} Sv/gamma) c c z-axis ^ c | \ \ void c | \ Fe \ c | void | | c X -------|-------|--------D----> x-axis c source | | c / / c / / c c ********************* BLOCK 1: CELLS ********************************* 10 0 -10 imp:p=1 $ inside of shield 20 1 -7.86 10 -20 imp:p=1 $ iron shell 30 0 20 -50 imp:p=1 $ void outside shld and inside detect 40 0 50 -100 imp:p=1 $ void past detector 50 0 100 imp:p=0 $ vacuum outside problem boundary c ********************* BLOCK 2: SURFACE CARDS ************************* 10 so 30.0 $ inner shield surface 20 so 60.0 $ outer shield surface 50 so 160.0 $ detector surface 100 so 10.E+02 $ spherical problem boundary (at 10 m) c ********************* BLOCK 3: DATA CARDS **************************** SDEF erg=7.00 par=2 $ 7-Mev pt photon source at origin c mode p phys:p 100 1 1 $ no bremsstrahlung; no coherent scattering nps 10000 $ 10000 particle cutoff f2:p 50 $ tally on surface 50 as ambient dose c c ---- Photon ambient dose equivalent H*(10mm) Sv cm^2; ICRP [1987] de2 0.100E-01 0.150E-01 0.200E-01 0.300E-01 0.400E-01 0.500E-01 0.600E-01 0.800E-01 0.100E+00 0.150E+00 0.200E+00 0.300E+00 0.400E+00 0.500E+00 0.600E+00 0.800E+00 0.100E+01 0.150E+01 0.200E+01 0.300E+01 0.400E+01 0.500E+01 0.600E+01 0.800E+01 0.100E+02 df2 0.769E-13 0.846E-12 0.101E-11 0.785E-12 0.614E-12 0.526E-12 0.504E-12 0.532E-12 0.611E-12 0.890E-12 0.118E-11 0.181E-11 0.238E-11 0.289E-11 0.338E-11 0.429E-11 0.511E-11 0.692E-11 0.848E-11 0.111E-10 0.133E-10 0.154E-10 0.174E-10 0.212E-10 0.252E-10 c c --- Natural iron (density 7.86 g/cm^3) m1 26000 -1.00000
```

Figure 8. Input for analog simulation of example problem.

§ 2.7.2.13 , § 5.12.7

over its neighbor closer to the source. Thus, to use geometry splitting,
change the importances of the shield cells to 1 for the innermost iron
cell, 2 for the next, 4 for the next, and so on to the tenth cell with
an importance of 2 9 = 256. This is done with the IMP command

<!-- formula-not-decoded -->

The mean and relative error with such a nonanalog simulation are shown
in Figs. 9 and 10. For this nonanalog simulation, the figure-of-merit
(FOM) was 4.9 times larger than that for the analog simulation, so that,
to achieve the same relative error, the analog simulation would have to
be run 4 . 9 2 = 24 times longer.

An alternative approach is use weight windows for the 10-cell shield
model. First run the problem as an analog problem with the weight window
generator command placed in Block 3. Here we use

<!-- formula-not-decoded -->

Then place the generated weight-window cards written near the bottom of
the output (with the appropriate blanks removed) into Block 3 and rerun
as a weight-window biased simulation. The results are also shown in
Figs. 9 and 10. For this weight-window simulation, the figure-of-merit
(FOM) was 5.4 times larger than that for the analog simulation.

Figure 9. The mean of the tally for the example problem.

<!-- image -->

## 4.4.4 Exponential Transform

The exponential transform artificially changes the distance to the next
collision. In this technique, particles can be moved preferentially
towards the tally region and inhibited from moving away from it. The
exponential transform stretches the path length between collisions in a
preferred direction by adjusting the total cross section as Σ t (1 -pµ )
where p is the stretching parameter, and µ is cosine of the angle
between the particle direction and the preferred direction.

The exponential transform biasing is invoked with the EXT and VECT
commands. The EXT command has the form

<!-- formula-not-decoded -->

where n = N / P / E for neutrons/photons/electrons, and for the i-th
cell A i has the form Q V m , and j is the number of cells. Usually Q =
p , while Q = 0 indicates the exponential transform is not to

Figure 10. The relative (fractional) error for the test problem.

be used (and V and m are omitted). The stretching direction is specified
by the V and m part of A i and the VECT command.

## 4.4.5 Energy Splitting/Russian Roulette

In some problems, e.g., finding the high-energy neutron fluence in a
pressure vessel, only particles with a certain range of energies are of
interest. When such a particle is created, the ESPLT command can be used
to split the particle into more daughter particles of the same type.
Also, when a particle of energy outside the energy region of interest is
created, Russian roulette is used to eliminated some of these particles.
An example of the ESPLT command is

```
c Energy splitting with Russian roulette c split to 4 for 1 if parent energy falls below 3 MeV c split to 2 for 1 if parent energy falls below 1 MeV c split to 1 for 2 if parent energy falls below 0.4 MeV c split to 1 for 4 if parent energy falls below 0.1 MeV ESPLT:n 4 3 2 1 0.5 0.4 0.25 0.1
```

## 4.4.6 Forced Collisions

The forced collision biasing method increases the sampling of collisions
in specified cells, generally those near a DXTRAN sphere or point/ring
detector. This method splits particles into collided and uncollided
parts. The collided part is forced to interact within the current cell
while the uncollided particle exits the cell without collision. The
weight windows game is not played at surfaces bounding a cell in which
forced collisions are specified. The forced collision option is invoked
with the command

```
FCL: n x 1 x 2 . . . x i . . . x j
```

where n = N / P for neutrons/photons, j is the number of cells, and x i
controls which particles undergo forced collisions (see manual for
details)

## 4.4.7 Source Biasing

One of the easiest nonanalog techniques to implement is source biasing .
In MCNP, any of the SDEF variables can be biased. For example, source
particles can be started with enhanced weights, with preferred energies,
and in regions closer to the detector. One of the most useful source
biasing techniques is to start particles in preferred directions,
generally towards tally regions.

As an example, consider the spherical iron shell problem of Section
4.4.3. Rather than use a spherical F2 detector at 160 cm from the
source, place a point detector on the x-axis 160 cm from the point
source. (This is a terrible idea compared to using the surface F2
detector, but it illustrates the importance of source biasing.) Then to
start particles preferentially towards the detector on the positive
x-axis, we might use

```
SDEF ERG=7.00 PAR=2 VEC=1 0 0 DIR=d1 $ bias source direction SB1 -31 2.0 $ exp bias exp[2mu]
```

Here source particles will be emitted with the PDF p ( µ ) = Ce Kµ where
µ = cos θ , the cosine of the angle between the emission direction and
the VEC direction (here the x-axis). C is a normalization constant C =
K/ ( e K -e -K ) that is calculated by MCNP. In this example we specify
p ( µ ) = Ce 2 µ so that 50% of all source particles are emitted within
48 degrees of the x-axis. Here the forward-tobackward emission
probabilities, p (1) /p ( -1) = e -4 /similarequal 1 / 54 . 5.

Another approach for source direction biasing is to restrict source
emission to a set of nested cones about the bias direction. This
discontinuous conical biasing is more time consuming to implement but
can produce better results, when optimized, than can the continuous
direction biasing. In some problems involving a collimated source, it
must be used. Suppose we set up a set of nested cones about the source
parameter VEC direction with cosines of the conical half angles -1 &lt; µ 1
&lt; µ 2 &lt; . . . &lt; µ n &lt; 1. We want particles to be emitted in µ i -1 &lt; µ &lt;
µ i with probability p i (here µ 0 ≡ -1

§ 2.7.2.8 , § 5.12.5

§ 2.7.2.15 , 5.12.9

§

§ 2.7.2.16 ,

§ 5.8.4

§ 5.13.3

and µ n +1 ≡ 1). Then on the SDEF card place the parameter DIR = d n
with the following lines placed after the SDEF card:

```
SI n -1 µ 1 µ 2 . . . µ n 1 SP n 0 f 1 f 2 . . . f n f n +1 SB n 0 p 1 p 2 . . . p n p n +1
```

Here f i is the fraction of the solid angle of the i-th cone and is
calculated as f i = [ µ i -µ i -1 ] / 2.

## 4.5 Final Recommendations

Here are some recommendations for using the various variance reduction
techniques.

- Before attempting to use variance reduction techniques for the first time, use the contemplated technique on a simple problem before using it on the practical and more complex problem. You need to get a feel for how the technique works without the confounding complexities of a difficult problem.
- One of the key parameters for assessing the effectiveness of different variance reduction techniques for your problem is the figure-of-merit (FOM). Generally, the better the improvement in the FOM, the better is the variance reduction technique.
- For deep penetration problems, use either cell importances or (preferably) weight windows to keep the particle population high in the cells of interest. Weight windows is more difficult to implement but more effective when done correctly. However, geometry splitting through cell importances is relatively safe and easier to implement.
- Use the CUT , ELPT , and PHYS commands when appropriate to avoid time-consuming tracking, physic, or unimportant tally contributions. This can speed up calculational times for some problem by a factor of 10.

## 5 MCNP Output

The output produced by MCNP provides a wealth of information about the
simulation. The skill of the analyst is in using this output to
interpret the precision and acceptability of the tally results produced
by the Monte Carlo run and to decide what changes need to be made to
improve the tally in subsequent runs.

## 5.1 Output Tables

MCNP provides a wealth of information about the simulation, and a
skilled user can elicit much insight from this voluminous output. By
default only a small portion of all the possible output is produced.
Always output are (1) input file listing, (2) summary of particle
loss/creation, (3) summary of KCODE cycles (if KCODE is used), (4)
tallies (if used), and (5) tally fluctuations charts. In addition,
certain output tables deemed basic are always produced-they cannot be
avoided. Other default tables are also generated unless turned off by
the PRINT command. The various MCNP tables are listed in Table 7.

The output is changed from the default with the PRINT command in Block 3
of the input. Examples of the three forms of this command are

```
PRINT $ produce everything PRINT 110 20 $ basic & default tables plus Tables 110 and 20 PRINT -110 -20 $ all Tables except Tables 110 and 20
```

Table 7. Selected output tables available in MCNP. (d)=default; (b)=basic

| Table No.                                                          | Table Description                                                                                                                                                                                                                                                                                                                                                                               | Table No.                                                                               | Table Description                                                                                                                                                                                                                                                                                                                                                                             |
|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 10 20 30 35 40 50 60 (b) 62 (b) 70 72 (b) 85 90 98 100 (b) 102 110 | Source information Weight windows information Tally descriptions Coincident detectors Material compositions Cell vols & masses; surface areas Cell importances Forced coll.; expon. transform Surface coefficients Cell temperatures Electron range & straggling KCODE source data Physics const.& compile options Cross section tables S( α,β ) nuclide assignment First 50 starting histories | 120 126 128 (b) 130 140 150 160 (d) 161 (d) 162 (d) 170 175 178 180 190 (b) 198 200 (b) | Importance function analysis Cell particle activity Universe map Particle weight balances Neutron/photon nuclide activity DXTRAN diagnostics TFC bin tally analysis p ( x ) tally PDF plot Cumulative p ( x ) plot Source frequency; surface source Estimated k eff by cycle Estimated k eff by batch size WWG bookkeeping summary WWG summary WW from multigroup fluxes WW generated windows |

## 5.2 Accuracy versus Precision

With MCNP and its various variance reduction techniques, it is possible
(and often the case for § 2.6.2 novice users) to produce tally results
that, while very precise , i.e., a small relative error, are not very
accurate . Technically, precision is the uncertainty (as measured by the
tally variance) in the tally mean x caused by the statistical
fluctuations in the individual scores x i of the simulated histories. By
contrast, accuracy is a measure of how close the tally mean x is to the
true physical quantity being estimated. The difference between the true
value and the expectation value of the simulation tally is called the
systematic error , an important quantity but one that is seldom known.

## Factors Affecting Accuracy:

- The MCNP code: This includes inaccuracies introduced by MCNP in its use of (1) physics models, (2) mathematical models, (3) uncertainties in the nuclear/atomic data, including cross sections, atomic weights, Avogadro's number, etc., and (4) coding errors. MCNP is a very mature code and these sources of error, while always present, are not generally thought to be a major concern for 'standard neutron/photon problems.' Many MCNP benchmark validation problems have been analyzed and documented.
- The MCNP model: Improper modeling of source energy and angular distributions, poor representation of the actual geometry by the MCNP geometric model, and errors in the material compositions can lead to significant inaccuracies.
- User errors: Probably the most important source of inaccuracies (at least for novices) is error introduced by the user in incorrectly using program options or making errors in the input file. Similarly, a novice often misunderstands the difference between a particular tally and the physical quantity being sought.

## Factors Affecting Precision:

- Forward versus adjoint calculations: For problems with spatially extended sources and a tally in a small region, an adjoint simulation often produces more precise results with few histories compared to a forward simulation.

§ 2.6.2.1

§ 2.6.2.2

- Tally type: The choice of tally type often greatly affects the precision of the results. For example, point detectors are often less precise than surface detectors in a scattering medium.
- Variance reduction: The use of different variance reduction techniques can affect the tally precision tremendously.
- Number of histories: The more histories run (and the greater computer effort expended) the better will be the precision of the tallies.

## 5.3 Statistics Produced by MCNP

MCNP produces a wealth of information about a simulation to allow the
user to assess the precision (not the accuracy) of the result. While
much of the detailed assessment performed by an experienced user depends
on careful examination of the many output tables, the initial focus
should be on the ten statistical indices calculated by MCNP. In this
section we review these ten statistics.

## 5.3.1 Relative Error

Many beginners examine only the relative error R , and, while this is a
very important statistic, it § 2.6.4 alone cannot decide the
acceptability of the tally result. The relative error is the fractional
1-sigma estimated uncertainty in the tally mean, i.e., R ≡ S x /x , the
ratio of the standard deviation of the tally mean to the mean. Here is
how R is to be used to interpret the tally value:

Table 8. Interpretation of the relative error R .

| Range of R                          | Quality of Tally                                                                                              |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------|
| > 0 . 5 0.2 to 0.5 < 0 . 1 < 0 . 05 | Meaningless Factor of a few Reliable (except for point/ring detectors) Reliable even for point/ring detectors |

The value of R is determined by two quantities: (1) the history scoring
efficiency q , which is the fraction of histories producing non-zero x i
's, and (2) the dispersion in nonzero scores. In almost every tally, the
tally PDF f ( x ) (whose mean the tally is trying to estimate) has a
delta-function at x = 0 representing the probability a source particle
makes no contribution to the tally (e.g., a source particle is absorbed
before reaching the tally region).

MCNP breaks R up into two components such that R 2 = R 2 eff + R 2 int .
Here R eff is the spread in R caused by scoring inefficiency and R imp
is the intrinsic spread of the non-zero history-scoring events. If every
source particle contributes to the tally ( q = 1) then R eff = 0; but as
more and more particles produce zero score, R eff increases. By
contrast, R imp measures the uncertainty produced by the spread of
nonzero scoring events. If some particles produce zero scores and the
remainder produce the same score , R imp = 0. As the scoring particles
have increasingly different scores, R imp increases.

The purpose of variance reduction techniques is to increase the scoring
efficiency q and hence to reduce R eff . At the same time we want to
decrease the spread in nonzero scores, i.e. to make f ( x ) more
concentrated about its mean so that R imp decreases.

## 5.3.2 Figure of Merit

Another important statistic generated by MCNP is the figure of merit
(FOM), defined as § 2.6.5

<!-- formula-not-decoded -->

where T is the run time. Since T varies with the computer, the same
simulation performed on different machines produces different FOMs. As
discussed earlier in Section 4.1.1, the FOM should remain relatively
constant (except for fluctuations early in the simulation). For
different variance reduction techniques, the one with the largest FOM is
preferred.

## 5.3.3 Variance of the Variance

The estimation of the relative error R is important to indicate the
precision of the tally mean. However, how accurate is the estimation of
R ? To indicate the accuracy of R , MCNP estimates the relative variance
of R , i.e. a variance of a variance (VOV). The VOV is defined as

<!-- formula-not-decoded -->

where S 2 ( S 2 x ) is the variance of S 2 x ).

The VOV involves the third and fourth moments of the tally distribution
f ( x ) and is much more sensitive to fluctuations in large history
scores than is R , which is based on only the first and second moments
of f ( x ). The proper sampling of infrequent but high scoring events is
vital if reliable tally means are to be obtained, and for this reason
the VOV is an important indicator of a reliable result.

From Eq. (11), it can be shown that the VOV should decrease as 1/N. MCNP
tests for this 1/N behavior in the VOV. Further, the VOV should always
be less than 0.1 for all types of tallies.

## 5.3.4 The Empirical PDF for the Tally

MCNP also constructs the tally PDF f ( x ) to help assess the quality of
the confidence interval estimates for the tally mean. An example is
shown in Fig. 11. Examination of the high-end tail of this distribution
is very important for problems involving infrequent events with very
high score. Three possible outcomes for such problems are possible:

1. Statistically meaningful confidence intervals are produced. This, of course, is always the desired outcome.
2. The sampling of a rare event with a very large score causes the the mean and R to increase and the FOM to decrease significantly. This situation is easily detected by observing the behavior of R and FOM in the tally fluctuation chart (TFC) produced at the end of the MCNP output. See Fig. 12 for a well-behaved example.
3. The third and most troublesome case is one that appears to be converged, based on acceptable statistical behavior of the mean, R , FOM, and the VOV, but in reality the tally mean is substantially underestimated because large scoring histories were inadequately sampled. Detecting this situation of too few large history tallies is difficult. It is for this case that MCNP performs extensive analysis of the high tally tail of the tally PDF.

The main difficulty in detecting case 3 above is knowing when you have
performed enough histories to make a valid estimate of the confidence
interval for the tally mean. The central limit theorem (CLT) guarantees
the tally mean will appear to be sampled from a normal distribution with
a standard deviation σ/N if N is sufficiently large. The confidence
intervals estimated by MCNP for the tally are based on this normality
assumption. The key question is how large must N be for this assumption
to be valid.

For the CLT to hold, the first two moments of the tally PDF f ( x ), E(
x ) = ∫ ∞ 0 xf ( x ) dx and E( x 2 ) = ∫ ∞ 0 x 2 f ( x ) dx , must
exist. 12 For the first two moments to exist, f ( x ) must either have a
12 For the VOV to be finite, the third and fourth moments must also
exist; however, MCNP doesn't enforce this.

§ 2.6.7

§ 2.6.8

Figure 11. An example of the Tally PDF plot prodiced in the MCNP output.

<!-- image -->

Figure 12. Example of a tally fluctuation chart (TFC).

|    nps |       mean |   tally error |   4 vov |   slope |   fom |       mean |   tally error |   14 vov |   slope |   fom |
|--------|------------|---------------|---------|---------|-------|------------|---------------|----------|---------|-------|
|  16000 | 2.5565e-19 |        0.1546 |  0.046  |       0 |    13 | 1.6147e-20 |        0.155  |   0.099  |     0   |    13 |
|  32000 | 2.6267e-19 |        0.1057 |  0.0219 |       0 |    14 | 1.5614e-20 |        0.1098 |   0.0404 |     0   |    13 |
|  48000 | 2.9321e-19 |        0.0822 |  0.0129 |      10 |    15 | 1.5964e-20 |        0.0868 |   0.0228 |     0   |    13 |
|  64000 | 2.9096e-19 |        0.0725 |  0.0108 |      10 |    14 | 1.6062e-20 |        0.076  |   0.0189 |     0   |    13 |
|  80000 | 2.9088e-19 |        0.0655 |  0.0086 |      10 |    14 | 1.6037e-20 |        0.0687 |   0.0161 |     4.9 |    13 |
|  96000 | 2.9487e-19 |        0.0595 |  0.0072 |      10 |    14 | 1.5578e-20 |        0.0631 |   0.013  |     2.7 |    13 |
| 112000 | 2.9758e-19 |        0.0545 |  0.0061 |      10 |    15 | 1.5749e-20 |        0.0571 |   0.0105 |     3   |    13 |
| 128000 | 3.0167e-19 |        0.0509 |  0.0052 |      10 |    15 | 1.597e-20  |        0.0528 |   0.0086 |     2.7 |    14 |
| 144000 | 3.0142e-19 |        0.0483 |  0.005  |      10 |    14 | 1.5824e-20 |        0.0496 |   0.0075 |     2.7 |    14 |
| 160000 | 3.0284e-19 |        0.0461 |  0.0046 |      10 |    14 | 1.6205e-20 |        0.0465 |   0.0064 |     2.8 |    14 |
| 176000 | 3.0391e-19 |        0.0443 |  0.0042 |      10 |    14 | 1.6276e-20 |        0.0441 |   0.0056 |     3.2 |    14 |
| 192000 | 3.0143e-19 |        0.0427 |  0.004  |      10 |    14 | 1.6351e-20 |        0.042  |   0.005  |     3.5 |    14 |
| 200000 | 3.008e-19  |        0.042  |  0.004  |      10 |    14 | 1.6317e-20 |        0.041  |   0.0048 |     3.9 |    14 |

finite upper tally cutoff, or decrease with x faster that 1 /x 3 . It is
this behavior of a proper tally PDF that MCNP tests for by analyzing the
high-tally tail of the empirical PDF.

MCNP uses the highest scoring histories (the 200 largest) to estimate
the slope of the PDF's high-tally tail. This is done by fitting a
generalized Pareto function (with parameters a and k ), namely

<!-- formula-not-decoded -->

to the high tally events. The slope is then estimated from

<!-- formula-not-decoded -->

On the output plot of the PDF, the Pareto fit is shown by string of s
's, and tally mean by a row of m 's (see Fig. 7).

For the high-end tail to be acceptable, a sufficient number of histories
has to have been run so that the CLT is expected to apply, namely, the
SLOPE must be 3 (or greater). If insufficient, rare, high-scoring events
have not been tallied, the SLOPE will generally not satisfy this
criterion. If too few histories have been run to estimate the slope, the
SLOPE is reported as 0; if the PDF falls off faster than 1 /x 10 , the
SLOPE is set to 10 (a 'perfect' value).

## 5.3.5 Confidence Intervals

From the relative error R , MCNP estimates the confidence interval for
the tally. Because the estimated mean and estimated uncertainty in the
mean are correlated, the mid-point of the confidence interval needs to
be shifted slightly from the mean. The amount of this midpoint shift,
SHIFT, is proportional to the third central moment, and should decrease
as 1 /N . MCNP calculates this refinement for the confidence interval.

## 5.3.6 A Conservative Tally Estimate

Sometimes a user wishes to make a conservative tally estimate, just in
case rare high-tally events may not be completely considered. In the
output, MCNP shows what would happen to the mean, R , VOV, confidence
interval, etc., if the next history ( N + 1) were the same as the
largest scoring history encountered in the simulation of N histories. If
large changes occur, then be very suspicious of the result.

§ 2.6.9

§ 2.6.9.2.2

## 5.3.7 The Ten Statistical Tests

- The most valuable tool provided by MCNP for assessing the reliability of results is the suite of § 2.6.9.2.3 10 statistical tests it performs on the tally. If any of the 10 tests are failed, MCNP automatically produces additional output to aid the user in interpreting the seriousness of the failed test(s). The 10 tests are summarized below.

## Tally Mean, x :

1. The mean must exhibit, for the last half of the problem, only random fluctuations as N increases. No up or down trends must be exhibited.

## Relative Error, R :

2. R must be less than 0.1 (0.05 for point/ring detectors).
3. R must decrease monotonically with N for the last half of the problem.
4. R must decrease as 1 / √ N for the last half of the problem.

## Variance of the Variance, VOV:

5. The magnitude of the VOV must be less than 0.1 for all types of tallies.
6. VOV must decrease monotonically for the last half of the problem.
7. VOV must decrease as 1 /N for the last half of the problem.

## Figure of Merit, FOM:

8. FOM must remain statistically constant for the last half of the problem.
9. FOM must exhibit no monotonic up or down trends in the last half of the problem.

## Tally PDF, f ( x ) :

10. The SLOPE determined from the 201 largest scoring events must be greater than 3.

If any of these tests fails, a warning is printed in the output and a
plot of f ( x ) is produced. If all ten tests are passed, MCNP then
calculates asymmetric and symmetric confidence intervals for the mean at
the one-, two-, and three-sigma levels. While these ten statistical
tests provided an excellent indication of the reliability of the result,
they are not foolproof . There is always the possibility that some high-
scoring rare event was not sampled in the histories run and that the
tally is underestimated. Users must rely on their understanding and
insight into the particular problem to avoid such traps.

## 5.3.8 Another Example Problem

Consider a point isotropic source of 7-MeV photons in an infinite medium
of iron. The ambient dose equivalent 30 cm from the source is sought. A
surface F2 detector and a F5 point detector are both used to estimate
this dose. The input file is shown in Fig. 13.

The variation of the tally mean, R , VOV, SLOPE, and FOM with the number
of particle histories is shown in Fig. 14. At 10 7 particle histories,
the F2 tally passed all 10 statistical tests: the mean and FOM are
relatively constant, the relative error R is monotonically decreasing as
1 / √ N (1 y-decade decrease for every 2 x-decades increase), the VOV is
monotonically decreasing as 1 /N (1 y-decade decrease for every 1
x-decade increase), and the SLOPE has a 'perfect' value of 10. This high
slope value is to be expected since there physically is an upper limit
to the tally, namely that produced by an uncollided photon reaching the
scoring surface. The slope of 10 is a strong indicator of such a tally
cutoff.

By contrast, the F5 point detector has not converged. The mean, error,
VOV, and FOM all exhibit sudden changes, a result of an occasional
photon that scatters very near the point detector

and contributes a huge score with the last-flight estimator used by the
F5 tally. The SLOPE remains constant at about 2, an indication of a long
slowly decreasing high-tally tail. In fact, a point detector in a
scattering medium has no tally cutoff. Be very wary of using point/ring
detectors in a strongly scattering medium.

If you had performed this simulation for only 5000 histories and,
unwisely, looked only at the relative errors, the F5 detector would
appear attractive since it has a relative error of about 0.06 (almost
near the acceptable value) while the F2 tally has R &gt; . 2. Recall that
every source particle produces a score with a point detector ( q = 1 , R
eff = 0) and R often starts to decrease properly. The F2 tally, on the
other hand, received scores from only 0.8% ( q = 0 . 0080) of the source
particles leading to R eff = 0 . 0024 and R imp = 0 . 0024 after 10 7
histories. Because of the large fluctuations in the F5 scores, its R imp
is much larger (0.127 after 10 7 histories).

The PDFs for these two tallies are shown in Figs. 15 and 16. As
expected, the PDF for the F5 tally is spread out over a wide range of
scores and has a high-score tail that is poorly defined even after 10 7
histories. The PDF for the F2 tally is much more compact with a well
established upper cutoff.

```
Point isotropic 7-MeV photon sources in infinite iron medium c ********************* BLOCK 1: CELL CARDS ***************************** 1 1 -7.86 -10 imp:p=1 $ iron inside detector shell 2 1 -7.86 10 -20 imp:p=1 $ iron outside detector shell 3 0 20 imp:p=0 $ vacuum outside problem boundary c ********************* BLOCK 2: SURFACE CARDS ************************* 10 so 30.0 $ detector surface 20 so 3000.0 $ outer surface of iron c ********************* BLOCK 3: DATA CARDS **************************** SDEF erg=7.00 par=2 $ pt isotropic 7-MeV photon source mode p $ photon mode only nps 1000000 $ number of histories to be run f2:p 10 $ tally 2: surface detector at 30 cm f15:p 30 0 0 -0.3 $ tally 15: pt det 30 cm on x-axis; Ro=.3mfp c c ---Photon ambient dose equivalent H*(10mm) Sv cm^2; from ICRP [1987] de 0.100E-01 0.150E-01 0.200E-01 0.300E-01 0.400E-01 0.500E-01 0.600E-01 0.800E-01 0.100E+00 0.150E+00 0.200E+00 0.300E+00 0.400E+00 0.500E+00 0.600E+00 0.800E+00 0.100E+01 0.150E+01 0.200E+01 0.300E+01 0.400E+01 0.500E+01 0.600E+01 0.800E+01 0.100E+02 df 0.769E-13 0.846E-12 0.101E-11 0.785E-12 0.614E-12 0.526E-12 0.504E-12 0.532E-12 0.611E-12 0.890E-12 0.118E-11 0.181E-11 0.238E-11 0.289E-11 0.338E-11 0.429E-11 0.511E-11 0.692E-11 0.848E-11 0.111E-10 0.133E-10 0.154E-10 0.174E-10 0.212E-10 0.252E-10 c m1 26000 -1.00000 $ natural iron (density 7.86 g/cm^3)
```

Figure 13. Input file for the example problem

Figure 14. The variation of the various statistics estimated by MCNP for the two tallies of the test problem of Fig. 13.

<!-- image -->

Figure 15. The PDF for the F2 surface tally in the example problem. Heavy line is for 10 6 histories and dotted line for 10 7 .

<!-- image -->

Figure 16. The PDF for the F5 tally in the example problem. Light line is for 10 6 histories and the heavy line for 10 7 .

<!-- image -->

## Useful Web Sites

https://mcnp.lanl.gov/reference collection.html . This is the offical
web site for MCNP. Much MCNP information is available from this site
including the Theory &amp; User's Manual and a large number number of Los
Alamos Technical Reports presenting many different details about the
code.

https://nucleardata.lanl.gov : This site provides the latest cross
section and related data in the ASCII ACE format needed by MCNP. As
errors in the ENDF/B files are corrected or updated, new ACE formatted
files are found here.

https://www.nndc.bnl.gov/ . This is the official site for the national
nuclear data center from which a wealth of nuclear data can be obtained.
In particullar, the latest ENDF/B cross sections are readily available
in ASCII or graphical form.

## REFERENCES

- C ONLIN J.L. (Ed.) AND the LANL Nuclear Data Team, XCP-5, Listing of Available ACE Data Tables , Techical Report LA-UR-17-20709, Oct. 2017, Los Alamos National Laboratory, Los Alamos, NM, USA. Available at https://mcnp.lanl.gov/reference\_collection.html .
- D ETWILER R.S., R.J. M C C ONN , T.F. G RIMES , S.A. U PTON , AND E.J. E NGGEL , Compendium of Material Composition Data for Radiation Transport Modeling , Technical Report 200-DMAMC-128170 PNNL-15870, Rev. 2, April 2021, Pacific Northwest National Laboratory, Richland, WA, USA. Available at https://www.pnnl.gov/main/publications/external/technical\_reports/PNNL-15870Rev2.pdf
- D UNN , W.L. AND J.K. S HULTIS , Exploring Monte Carlo Methods , 2ed, Academic Press, Elsevier, Cambridge, MA, USA, 2023.
- K ULESZA , Joel A. (Ed.) and 28 others, MCNP R © Code Version 6.3.0 Theory &amp; User Manual , Technical Report LA-UR-22-30006, Rev. 1, Sept. 28, 2022, Los Alamos National Laboratory, Los Alamos, NM, USA. Available at https://mcnp.lanl.gov/reference\_collection.html .

S HULTIS , J.K. AND R.E. F AW , Radiation Shielding , Amer. Nucl. Soc.,
LaGrange Park, IL, USA, 2000.
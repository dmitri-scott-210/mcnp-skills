---
title: "Chapter 3 - Introduction to MCNP Usage"
chapter: "3"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/3_Introduction_to_MCNP_Usage.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Chapter 3

## Introduction to MCNP Usage

This part of the MCNP manual, Part II, provides comprehensive
documentation for using the MCNP code, version 6.3.1. This part includes
description of ASCII input file commands (often referred to as input
cards), geometry specifications, and tally plotting details. In addition
to this manual, classes providing detailed instruction for using MCNP6
are held on a regular basis (see http://mcnp.lanl.gov).

The remainder of Chapter 3 presents an overview of MCNP6 applications
and provides a basic primer for MCNP usage with a sample problem. There
are certain limitations in code usage that the user must be made aware
of; these items are listed in §3.4.5. A general description of the MCNP6
input structure can be found in Chapter 4, while Chapter 5 provides
detailed descriptions of each of the available input parameters. Chapter
6 contains basic geometry, cross-section, and tally plotting
instructions. Numerous examples, both simple and complex, are presented
in Chapter 10 as part of Part III.

## 3.1 MCNP6 Versatility

Application areas for the code among the thousands of MCNP users
worldwide are quite broad and constantly developing. Examples include
the following:

- Reactor design
- Nuclear criticality safety
- Nuclear safeguards
- Medical physics, especially proton and neutron therapy
- Design of accelerator spallation targets, particularly for neutron scattering facilities
- Investigations for accelerator isotope production and destruction programs, including the transmutation of nuclear waste
- Research into accelerator-driven energy sources
- Accelerator based imaging technology such as neutron and proton radiography
- Detection technology using charged particles via active interrogation
- Design of shielding in accelerator facilities
- Activation of accelerator components and surrounding groundwater and air
- High-energy dosimetry and neutron detection

- Investigations of cosmic-ray radiation backgrounds and shielding for high altitude aircraft and spacecraft
- Single-event upset in semiconductors from cosmic rays in spacecraft or from the neutron component on the earth's surface
- Analysis of cosmo-chemistry experiments, such as Mars Odyssey
- Charged-particle propulsion concepts for spaceflight
- Investigation of fully coupled neutron and charged-particle transport for lower-energy applications
- Transmutation, activation, and burnup in reactor and other systems
- Nuclear material detection
- Design of neutrino experiments

For all of these applications, the structure of user specification of
the problem and selection of input options are similar. The chapters in
the remainder of Part II provide general guidance for creation of MCNP
input and specific examples of particular problems. The guidance should
be sufficient for a user to simulate radiation transport problems in
their area of interest.

## 3.2 MCNP6 Input for Sample Problem

The MCNP6 code is driven primarily by the main input file, with the
default name inp , that contains a user-specified description of the
problem. Users must specify the geometric properties of the problem of
interest, initial particle state, relevant physics parameters, and
desired tallies.

Problem input consists of a series of structured text commands, where
each command is referred to as a card. We present here only the subset
of cards required to run the simple fixed source demonstration problem.
All input cards are described in Chapter 5.

The MCNP6 code uses consistent units for each dimensional quantity. The
units used in the sample problem that follows are length in centimeters
(cm), energy in MeV, mass density in grams per cubic centimeter (g/cm 3
), and atomic density in atoms/barn-cm. Additional standard MCNP6 units
are provided in Chapter 4. The basic constants used in the MCNP6 code
are printed in an optional PRINT Table 98 in the output file via the
PRINT card.

The simple sample problem is illustrated in Figure 3.1. We wish to start
14-MeV neutrons isotropically as a point source in the center of the
small sphere of oxygen that is embedded in a cube of carbon. A small
sphere of iron is also embedded in the carbon. The carbon is a cube 10
cm on each side; the spheres have a 0.5-cm radius and are centered
between the front and back faces of the cube. We wish to calculate the
total and energy-dependent flux in increments of 1 MeV from 1 to 14 MeV,
where bin 1 will be the tally from 0 to 1 MeV

1. on the surface of the iron sphere, and
2. averaged in the iron sphere volume.

1

2

1

1

<!-- image -->

1

Figure 3.1: A 0.5-cm-radius sphere of oxygen (Cell 1) and a 0.5-cm-
radius sphere of iron (Cell 2) embedded in a carbon cube (Cell 3) with a
side dimension of 10 cm. Cell 4 represents the 'outside world'.

## 3.2.1 Introduction to Geometry Specification

As depicted in Figure 3.1, this geometry has four cells (volumetric
regions) and eight two-dimensional surfaces-six planes and two spheres.
Circled numbers indicates cell numbers and surface numbers are written
next to the appropriate surfaces. Surface 5 comes out from the page in
the + x direction and surface 6 goes back into the page in the -x
direction.

The cell cards for the geometry of our problem are set up using
knowledge of the sense of a surface and the union and intersection
operators (see §3.2.3). To simplify this step, assume the cells are void
for now. The following cards describe cells 1 and 2:

```
1 0 -7 2 0 -8
```

where the first entry on each of these cell cards is the cell number,
the second entry is the material number, with '0' indicating a void, and
the third number provides cell surface information. In this sample
problem, the negative signs denote the regions inside (the negative
sense of) surfaces 7 and 8.

Cell 3 is everything in the problem universe above surface 1 intersected
with everything below surface 2, intersected with everything to the left
of surface 3, and so forth for the remaining three surfaces. The region
in common to all six surfaces is the cube, but we also need to exclude
the two spheres by intersecting everything outside surface 7 and outside
surface 8. By using a blank space to denote the intersection of two
regions of space, the card entries required to describe cell 3 are

```
3 0 1 -2 -3 4 -5 6 7 8
```

Cell 4 requires the use of the union operator, which is denoted by a
colon (:) between two surfaces. Cell 4 is the referred to as the
'outside world' and is defined as everything in the universe below
surface 1, plus everything above surface 2, plus everything to the right
of surface 3, and so forth. The cell card for cell 4 is

```
4 0 -1 : 2 : 3 : -4 : 5 : -6
```

Cell 4, the outside world, would usually have zero importance (not
denoted here). More guidance on cell importance is provided in §3.2.5.2.

Figure 3.2: MCNP Input File Format

<!-- image -->

## 3.2.2 The MCNP Input File

An MCNP6 input file has the form shown in Fig. 3.2.

The input file consists of a series of ASCII text-based, structured
commands, referred to herein as cards. Each card consists of a series of
keywords and data entries, separated by one or more blank spaces, and a
card always starts on a new line. A collection of multiple cards is
referred to as a block. The MCNP input consists of one optional and
three required blocks. A single blank line is used as a delimiter
between blocks and as an optional input-file terminator. Care must be
taken to not include additional blank lines between blocks, as they will
lead to input being ignored and misleading fatal errors.

All input lines are limited to 128 columns. Alphabetic characters can be
upper, lower, or mixed case. Unprintable characters or those outside of
base ASCII found in an input line are converted to blank spaces. Windows
new-line characters are correctly processed in the MCNP code, version
6.2 or newer. MacOS 9-style new-line characters ( CR ) are not
supported. A $ (dollar sign) terminates data entry on a line. Anything
on the line that follows the $ is interpreted as a comment and ignored
by the code.

Tab characters in the input file are converted to one or more blank
spaces, such that the character following the tab will be positioned at
the next tab stop. Tab stops are set every eight characters, i.e., 9,
17, 25, etc. The limit of input lines to 128 columns applies after tabs
are expanded into blank spaces. It is recommended that blank spaces be
used instead of tab characters for this reason.

Comment cards can be used anywhere in the inp file after the problem
title card and before the optional blank terminator card. Comment lines
must have a c somewhere in columns 1-5 followed by at least one space
and can be a total of 128 columns long.

Cell, surface, and data cards must all begin within the first five
columns. Entries are separated by one or more blank spaces. Numbers can
be integer or floating point; the MCNP code makes the appropriate
conversion. A few entries on some cards are allowed to be 8-byte
integers, i.e., integers larger than 2.147 billion but less than ∼ 10 19
. These entries are noted in their respective card description in
Chapter 5. A data entry item, e.g., imp:n or 1.1e2 , must be completed
on one line.

Blank spaces filling the first five columns indicate a continuation of
the data from the last named card. An &amp; (ampersand) ending a line
indicates data will continue on the following card, where data on the
continuation card can be in columns 1-128.

1

The optional message block, discussed in detail in §4.4.1, is used to
change file names and specify running options such as a continue-run. On
most systems these options and files may alternatively be specified with
an execution line (see §3.3.2). If both an execution line and a message
block are present and there is a conflict, the execution line entries
supersede the message block entries. The blank line delimiter signals
the end of the message block.

The first card in the file after the optional message block is the
required problem title card. If there is no message block, this must be
the first card in the INP file. It is limited to one 128-column line and
is used as a title in various places in the MCNP6 output. It can contain
any information you desire but usually contains information describing
the particular problem. Immediately following the title card are three
unlabeled blocks of cards: the cell, surface, and data card blocks,
separated by single blank lines.

Input file checking and error handling is described in §4.7.

## 3.2.3 Cell Cards

After the title card, the next required block is the cell cards. When
populating cell cards, the cell number is the first entry and must begin
in the first five columns. The next entry is the cell material number,
which is arbitrarily assigned by the user. The corresponding material is
described on a material ( M ) card with the same material number
[§3.2.5.5]. If the cell is a void, a zero is entered for the material
number. The cell and material numbers cannot exceed eight digits each.
Following the material number is the cell material density. A positive
entry is interpreted as atom density in units of 10 24 atoms/cm 3 . A
negative entry is interpreted as mass density in units of g/cm 3 . There
is no density entry for a void cell. After the material density, a
complete specification of the geometry of the cell follows. This
specification includes a list of the signed surfaces bounding the cell
where the sign denotes the sense of the regions defined by the surfaces.
The regions are combined with the Boolean intersection and union
operators. A space indicates an intersection and a colon indicates a
union.

Optionally, after the geometry description, cell parameters can be
entered. The form for cell parameters is KEYWORD= value . The following
line illustrates a cell card format:

```
1 1 -0.0014 -7 IMP:N=1
```

Cell 1 contains material 1 with density 0.0014 g/cm 3 , is bounded only
by surface 7, and has a neutron importance of 1. If cell 1 were a void,
the cell card would be

```
1 1 0 -7 IMP:N=1
```

The complete cell input for this problem (with two comment cards) is

```
1 c cell cards for sample problem 2 1 1 -0.0014 -7 3 2 2 -7.86 -8 4 3 3 -1.60 1 -2 -3 4 -5 6 7 8 5 4 0 -1:2:3:-4:5:-6 6 c end of cell cards for sample problem
```

The blank line at the end of the card block terminates the cell-card
section of the MCNP input file. A complete explanation of the cell card
input is found in §5.2.

Table 3.1: Surface Equations for Sample Problem

| Mnemonic   | Equation                                | Card Entries   |
|------------|-----------------------------------------|----------------|
| px         | x - D = 0                               | D              |
| py         | y - D = 0                               | D              |
| pz         | z - D = 0                               | D              |
| s          | ( x x ) 2 +( y y ) 2 +( z z ) 2 R 2 = 0 | x y z R        |

## 3.2.4 Surface Cards

When populating surface cards the surface number is the first entry. The
surface number must begin in columns 1-5 and not exceed eight digits.
The surface number is followed by an alphabetic mnemonic entry that
indicates the surface type. The surface type is followed by the
numerical coefficients of the equation of the surface, in the required
order. This simplified description enables us to proceed with the sample
problem. For a full description of the surface card see §5.3.1.

Our problem uses planes normal to the x -, y -, and z -axes and two
general spheres. The respective mnemonics are px , py , pz , and s .
Table 3.1 shows the equations that determine the sense of the surface
for the cell cards and the entries required for the surface cards. A
complete list of available surface equations is contained in Table 5.1.

For the planes defining the cube, D is the point where the plane
intersects the axis. If we place the origin in the center of the 10-cm
cube shown in Figure 3.1, the planes will be at x = -5 , x = 5 , etc.
The two spheres are not centered at the origin or on an axis, so we must
give the x , y , z -coordinates of their center as well as their radii,
R . The complete surface card input for this problem is shown below. A
blank line terminates the surface card portion of the input.

10

<!-- image -->

| c Beginning of surfaces for cube   | c Beginning of surfaces for cube   |
|------------------------------------|------------------------------------|
| 1 pz                               | -5                                 |
| 2 pz                               | 5                                  |
| 3 py                               | 5                                  |
| 4 py                               | -5                                 |
| 5 px                               | 5                                  |
| 6 px                               | -5                                 |
| c End                              | of cube surfaces                   |
| 7 s 0                              | -4 -2.5 0.5 $ oxygen sphere        |
| 8 s 0                              | 4 4 0.5 $ iron sphere              |

## 3.2.5 Data Cards

The remaining data input for MCNP6 follows the second blank card
delimiter (or third blank card if there is a message block). The data
cards block is where users define additional properties about the
simulation of particle histories. For each data card, the card name is
the first entry and must begin in the first five columns. The required
entries follow, separated by one or more blank spaces.

Some data cards require a particle designator that indicates the
corresponding particle type of that card. The particle designator
consists of the symbol : (colon) and the alphabetic particle symbol (see
Table 4.3) immediately following the name of the card. For example, to
enter neutron importance, use an IMP : n card; enter photon importance
on an IMP : n card; enter positive pion importance on an IMP : / card,
etc.

-

-

-

-

No data card can be used more than once with the same mnemonic, that is,
M 1 and M 2 are acceptable, but two M 1 cards are not allowed. Defaults
have been set for cards in some categories. The sample problem will use
cards in the following categories:

1. physics ( MODE )
2. cell and surface parameters ( IMP :n)
3. source specification ( SDEF )
4. tally specification ( F , E )
5. material specification ( M )
6. problem termination ( NPS )

A complete description of the data cards can be found in §5.4-§5.12.

## 3.2.5.1 MODE Card

The MODE card consists of the mnemonic mode followed by a list of
particles (separated by spaces) to be transported. If the mode card is
omitted, MODE N is assumed (i.e., neutron transport only).

By default, MODE N P does not account for photo-neutrons, but does
account for neutron-induced photons. Photonuclear particle production
can be turned on through an option on the PHYS :p card [§5.7.2]. Photon
production cross sections do not exist for all nuclides. If they are not
available for a MODE n p problem, MCNP6 will print out warning messages.

mode p or mode n p problems generate bremsstrahlung photons with a
thick-target bremsstrahlung approximation. This approximation can be
turned off with the PHYS :e card.

The sample problem is a neutron-only problem, so the MODE card can be
omitted because MODE n is the default.

## 3.2.5.2 Cell and Surface Parameter Cards

Data related to individual cells can be entered either on the cell card
or in the data-card block of the input file. Data related to individual
surfaces can only be entered using the data card format. If entered on a
card in the data block section, entries must be listed in the same order
as the associated cell (or surface) cards that appear earlier in the inp
file. The number of entries on a cell or surface data card must equal
the number of cells or surfaces in the problem, otherwise MCNP6 prints
out a warning or fatal error message. In the case of a warning, MCNP6
allows the problem to continue, but assumes that the value of the
parameter for each cell or surface is zero. Cell parameters also can be
defined on cell cards using the KEYWORD= value format.

## /warning\_sign Caution

If a cell parameter is specified on any cell card, that cell parameter
must be specified only on cell cards and cannot be present in the data
card section.

The IMP : n card is used to specify relative cell importance in the
sample problem. There are four cells in the sample problem, so the IMP :
n card would have four entries. The IMP : n card is used (a) for
terminating the particle's history if the importance is zero and (b) for
geometry splitting and Russian roulette to help particles move more
easily to important regions of the geometry. An IMP : n card for the
sample problem is

1

1

1

IMP:n 1 1 1 0

A listing of available cell parameter cards appears in §5.2. Examples
include importance cards ( IMP : P ) and weight-window cards ( WWE : P ,
WWN i : P ), etc. Each problem requires some method of specifying
relative cell importance. Most of the other cell parameters are used to
specify optional variance reduction techniques. The only surface
parameter card is AREA .

## 3.2.5.3 Source Specification Cards

A source definition ( SDEF ) card is one of four available methods of
defining the properties of starting particles. Section 3.2.5.3 has a
complete discussion of source specification. The SDEF card defines the
basic source parameters, some of which are given in Table 3.2.

The cel entry is only required if cells are used to restrict the domain
of sampled particles; otherwise the code will determine the cell number
of starting particles automatically. The default starting direction for
source particles is isotropic.

For the example problem, a fully specified source card is

```
sdef pos=0.0 -4.0 -2.5 erg=14 wgt=1.0 tme=0 par=n
```

Neutrons will start at the center of the oxygen sphere (0 , -4 , -2 . 5)
, in cell 1 (as determined by the code), with an energy of 14 MeV, and
with weight of 1.0 at time 0. All these source parameters except the
starting position are the default values, so the most concise source
card is sdef pos=0.0 -4.0 -2.5

If all the default conditions applied to the problem, only the mnemonic
SDEF would have been required.

## 3.2.5.4 Tally Specification Cards

The tally cards are used to specify what you want to learn from the
Monte Carlo calculation, such as, current across a surface, flux at a
point, etc. You request this information with one or more tally cards.
Tally specification cards are not required, but if none are supplied, no
tallies will be printed when the problem

Table 3.2: Source Specification Card Entry Summary

| Parameter   |    | Entry Default        | Entry if Unspecified             |
|-------------|----|----------------------|----------------------------------|
| pos         | =  | xyz                  | 0 0 0                            |
| cel         | =  | cell number          | Cell containing sampled location |
| erg         | =  | energy               | 14 MeV                           |
| wgt         | =  | statistical weight   | 1                                |
| tme         | =  | time                 | 0                                |
| par         | =  | source particle type | Lowest-numbered source particle  |

Table 3.3: Tally Specification Card Entry Summary

| Tally Mnemonic                                            | Description                                                                                                                                                                                                                                        |
|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| F1 : P F2 : P F4 : P F5 a:N or F5 a:P F6 : P F7 :n F8 : P | Surface current Surface flux Track length estimate of cell flux Flux at a point (point detector) Track length estimate of energy deposition Track length estimate of fission energy deposition Energy distribution of pulses created in a detector |

is run and a warning message is issued. Many of the tally specification
cards describe tally 'bins.' A few examples are energy ( E ), time ( T
), and cosine ( C ) bin cards.

MCNP6 provides seven different standard tally types, all normalized to
be per starting particle. Some tallies in criticality calculations are
normalized differently. A summary of the tally types is given in Table
3.3, Chapter 2 discusses tallies more completely, and §3.2.5.4 lists all
the tally cards and fully describes each one.

The tallies are identified by tally type and particle type. Tallies are
given the numbers 1, 2, 4, 5, 6, 7, 8, or increments of 10 thereof, and
are given a particle designator indicating the particle type to be
tallied. You may practically have as many of any basic tally as you
need, each with different energy bins, flagging, or any other desired
specification. The tally designations f4: n, f14: n, f104: n, and f234:n
are all legitimate neutron cell-flux type tallies, as indicated by the
last digit of 4; these tallies could all be for the same cell(s) but
with different energy or multiplier bins, for example. Similarly f5:p ,
f15: p, and f305:p are all photon point detector tallies. Having both an
f1:n card and an f1:p card in the same inp file is not allowed.
Limitations on tally numbers and other quantities is given in Table 4.2.

For our sample problem we will use F cards (tally type) and E cards
(tally energy).

## 3.2.5.4.1 Tally (F) Cards

The sample problem has a surface flux tally and a track length cell flux
tally. Thus, the tally cards for the sample problem shown in Figure 3.1
are

```
1 f2:n 8 $ flux across surface 8 2 f4:n 2 $ track length in cell 2
```

Printed out with each tally result is the uncertainty of the tally
corresponding to one estimated standard deviation. Results are not
reliable until they become stable as a function of the number of
histories run. Much information is provided for a specified bin of each
tally in the tally fluctuation charts at the end of the output file to
help determine tally stability. The user is strongly encouraged to look
at this information carefully, with more detail provided in §2.6.9.2.3.

## 3.2.5.4.2 Tally Energy (E) Cards

We wish to calculate neutron flux in increments of 1 MeV from 1 to 14
MeV. Another tally specification card in the sample input file
establishes these energy bins.

The entries on the E n card are the upper bounds in MeV of the energy
bins for tally n . The entries must be given in order of increasing
magnitude. If a particle has an energy greater than the last entry, it
will not be tallied, and a warning is issued. The MCNP code
automatically provides the total over all specified energy bins unless
inhibited by putting the symbol nt as the last entry on the selected E n
card.

The following cards will create energy bins for the sample problem:

```
1 e2 1 2 3 4 5 6 7 8 9 10 11 12 13 14 2 e4 1 12i 14
```

If no E n card exists for tally n , a single bin over all energy will be
used. To change this default, an E 0 (zero) card can be used to set up a
default energy bin structure for all tallies. A specific E n card will
override the default structure for tally n . We could replace the E 2
and E 4 cards with one E 0 card for the sample problem, thus setting up
identical bins for both tallies.

## 3.2.5.5 Materials Specification

The cards in this section specify both the isotopic composition of the
materials and the cross-section evaluations to be used in the cells. For
a comprehensive discussion of materials specification, see §5.6.

## 3.2.5.5.1 Material (M) Card

The following card is used to specify a material for all cells
containing material m , where m cannot exceed five digits:

Mm identifier1 fraction 1 identifier2 fraction 2 ...

The m on a material card corresponds to a material number on a cell card
[§3.2.3]. The consecutive pairs of entries on the material card consist
of the target identifier of the constituent element or nuclide followed
by the atomic fraction (or weight fraction if entered as a negative
number) of that element or nuclide, until all the elements and nuclides
needed to define the material have been listed. These entries are
further described as

1. Nuclide Identifier. This can take any of the possible forms listed in §1.2.3. If a suffix is provided, the code will find the entry with the same Z , A , S , library identifier, and physics identifier as the one input here. This means that U-238.80c can be used to load 92238.80c. If a suffix is not provided, the first Z , A , S match will be used. If atomic data is necessary for the simulation, such as for photoatomic or electron physics, A will be set to zero before searching through the xsdir .

In multi-particle simulations, such as MODE n p , only one suffix can be
specified per identifier inline. To control multiple libraries, one can
use either the xlib= keyword options on the M card to set the value for
the entire material, or specify the full identifier on the corresponding
MX card.

2. Nuclide Fraction. The nuclide fractions may be normalized to 1 or left unnormalized. For example, if the material is H 2 O, the fractions can be entered as 0.667 and 0.333, or as 2 and 1 for H and O, respectively. If the fractions are entered with negative signs, they are weight fractions; otherwise they are atomic fractions. Weight fractions and atomic fractions cannot be mixed on the same M m card.

1

2

3

4

5

6

Appropriate material cards for the sample problem are

```
m1 O-16 1 $ oxygen 16 m2 Fe-54 0.0585 $ Iron Fe-56 0.9175 Fe-57 0.0212 Fe-58 0.0028 m3 C-12 1 $ carbon 12
```

## 3.2.5.6 Problem Termination

Problem termination cards are used to specify parameters for some of the
ways to terminate execution of MCNP6. The full list of available cards
and a complete discussion of problem cutoffs is found in §5.13.1. For
our problem we will use only the history cutoff ( NPS ) card. The card
name NPS is followed by a numeric entry ( npp ) that specifies the
number of histories to transport. MCNP6 will terminate after npp
histories unless it has terminated earlier for some other reason.

## 3.2.6 Sample Problem Input File

The entire input deck for the sample problem is given in Listing 3.1.
Recall that the input text can be upper case, lower case, or mixed case.

Listing 3.1: Complete MCNP Input for Sample Problem

<!-- image -->

1

1

## 3.2.7 Running the Sample Problem

To run the example problem, place the input file in your current
directory. Let's assume the file is called primer.mcnp.inp . In a
terminal (or the equivalent command prompt for Windows installations),
type mcnp6 n=primer.mcnp.inp

where n is an abbreviation for the keyword name . MCNP6 will produce an
output file primer.mcnp.inpo that you can examine at your terminal. To
look at the geometry with the plot module using an interactive graphics
terminal, type mcnp6 ip n=primer.mcnp.inp

After the plot window appears, click anywhere in the picture to get the
default plot. This plot will show an intersection of the surfaces of the
problem by the plane x = 0 with an extent in the x direction of 100 cm
on either side of the origin. If you want to do more with plot , see the
instructions in Chapter 6. Otherwise click end to terminate the session.

## 3.2.8 Checking for Geometry Errors and the VOID Card

The MCNP6 code does extensive input checking but is not foolproof. A
geometry should always be checked by looking at several different views
with the geometry plotting option. Any surfaces that bound an
incorrectly defined volume are indicated as an error in the plotter via
red dotted lines. Additional verification of the geometry can be
performed by simulating particles in a voided geometry using the VOID
card. The VOID card (with no parameters) removes all materials and cross
sections in a problem and sets all non-zero cell importance to unity. It
is very effective for finding errors in the geometry description because
many particles can be run in a short time. Flooding the geometry with
many isotropic particles increases the chance of particles traversing
any invalid regions of the geometry and getting lost. The other uses for
the VOID card and its parameters are discussed in §5.6.10.

The sample input deck could include a VOID card while testing the
geometry for errors. The source in this problem is isotropic, and the
geometry is simple, so a sufficiently large value specified on the NPS
card will find any geometry errors. Run a short simulation with the VOID
card added and study the output to see if you are calculating what you
think you are calculating. When you are satisfied that the geometry is
error-free, remove the VOID card.

For more complicated geometries, it is helpful to surround the entire
voided geometry with a sphere and define a source with an inward cosine
distribution on the bounding spherical surface. The importance of the
cell bounded by the source sphere must be nonzero. For more details on
this procedure, see §4.8.

## 3.3 Executing MCNP6

This section assumes a basic knowledge of command-line interface (CLI)
environments. Lines the user will type and execute are written with a
fixed-width font . Press the Enter key after each input line.

1

1

1

## 3.3.1 The MCNP6 Runtime Environment

A successful installation of the MCNP6 code will automatically include
the location of the executable binary file mcnp6 in the PATH environment
variable. The installation process will also specify the DATAPATH
environment variable, which is read by the code to access nuclear data.
Tabular nuclear data files are indexed by the code through the xsdir
file, which is a listing (i.e., a directory) of cross-section data. The
DATAPATH is the absolute path of the directory containing the latest
xsdir file and additional data library files. If the code is compiled
manually or installation errors have occurred, it may be necessary to
modify these environment variables before executing the mcnp6 binary;
always take care when modifying the PATH variable.

## 3.3.2 Execution Line

The MCNP6 execution line has the following form:

mcnp6 KEYWORD=value ... KEYWORD=value execution \_ option(s) other \_
options where each instance of KEYWORD is an MCNP6 default file name to
which the user may assign a specific value (i.e., file name or path);
execution \_ option (s) provides a character or string of characters that
informs MCNP6 which of five execution module(s) to run; and other \_
option (s) provides the user with additional execution control. The
execute line message may be up to 4096 characters long. The order of the
entries on the MCNP6 execution line is irrelevant. If no changes are
desired to the default names and options, no entries to the MCNP6
execution line are necessary.

The execution-line keywords (i.e., default file names), execution
options, and other options are summarized in Tables 3.4, 3.5, and 3.6,
respectively. Each of these execution-line inputs is detailed in the
following sections.

## 3.3.2.1 Execution KEYWORD=value Entries

The entry KEYWORD is any of the available default MCNP6 file names. The
code uses several files for input and output. User-specified file names
can include full paths to the files (e.g., /mydir/problem-x/jobs/problem
\_ 1a.inp ), but the path cannot be longer than 256 characters. In the
simplest case, in which the MCNP6 execution command has no arguments, a
file named inp must be present in the local directory; then, during
problem execution, MCNP6 will create two output files: outp and runtpe .
Other simulations will require additional files or generate additional
output files.

The default name of any of the files in Table 3.4 can be changed on the
MCNP6 execution line by entering

KEYWORD=newname

For example, if you have an input file called mcin and want the output
file to be mcout and the restart file to be mcrestart , the appropriate
execution line would read mcnp6 inp=mcin outp=mcout runtpe=mcrestart

Only enough letters of the default name are required to identify it
uniquely. For example,

1

1

1

## mcnp6 i=mcin o=mcout ru=mcrestart

also works. If a file in your local file space has the same name as a
file MCNP6 needs to create, the file is created with a different unique
name by changing the last letter of the name of the new file to the next
letter in the alphabet. For example, if you already have a file named
outp in the directory, MCNP6 will create outq . However, if the file
includes an extension, such as .txt or .inp , the last character before
the extension will be checked and changed if necessary.

Sometimes it is useful for all files from one calculation to have
similar names. If your input file is called job1 , the following line
mcnp6 name=job1

will create an output file called job1o and a restart file called job1r
. If these files already exist, the code will not overwrite them or
modify the last letter, but will issue a message that job1o already
exists and terminate.

## 3.3.2.2 Execution Options

MCNP6 provides users control over the execution of six distinct modules:
imcn , plotg , xact , mcrun , mcplot , and partisn \_ input . The xact
and mcrun options are ignored when they are combined with the partisn \_
input option. A description of these modules, including a one-letter
mnemonic assigned to each, appears in Table 3.5.

Given no other instructions, MCNP6 will process the input ( i ), process
the cross-section data ( x ), and then perform the particle transport (
r ). Thus, the default execution input is ixr . Entering the proper
mnemonic on the execution line controls the execution of the modules. If
more than one operation is desired, combine the single characters (in
any order) to form a string. To look for input errors only, specify i ;
to debug a geometry by plotting, use ip ; to plot cross-section data,
enter ixz ; to plot tally results from the runtpe or mctal files,
specify z ; and to create a LNK3DNT geometry file for use in PARTISN,
specify m on the execution line as the execution \_ option .

After a calculation has been run, the print file outp can be examined
with an editor on the computer. Numerous important messages about the
problem execution and statistical quality of the results are displayed
at the terminal; these messages are repeated in the outp file.

The other \_ option entries add additional flexibility when running MCNP6
executables and are shown in Table 3.6.

## 3.3.2.3 Parallel Execution

To take advantage of multi-core computer architecture, MCNP6 provides
two parallel models: task-based threading using the OpenMP model and
distributed processing supported through the use of the MPI model.

The simplest parallel execution of the code is to use theading with the
tasks option on the command line as follows:

mcnp6 i=input tasks &lt;n&gt;

1

MCNP6 will create &lt;n&gt; processes running on separate CPUs.

Because adding OpenMP capability requires extensive modifications to the
source code, some MCNP features cannot run in parallel using threading.
These features include:

- DBCN event logging,
- CINDER for delayed neutrons and/or photons using ACT ,
- LLNL photofission multiplicity,
- FMULT CGMF, FREYA, or LLNL fission multiplicity models,
- SSR surface source write,
- legacy (i.e., non-HDF5) PTRAC ,
- TMESH tallies,
- HISTP file generation,
- model physics for missing cross section data, and
- any particle other than neutrons, photons, or electrons.

If any of these features are used in the problem, MCNP6 will print a
warning message and run the problem with only one thread.

To use MPI parallelization, a separate MPI software package must be
installed that is compatible with the provided MCNP6 MPI binaries. These
MPI packages and associated MCNP6 executable names are:

- Linux
- -OpenMPI: mcnp6.ompi
- -MPICH: mcnp6.mpich
- macOS
- -OpenMPI: mcnp6.mpi
- Windows
- -Microsoft-MPI: mcnp6.mpi.exe

Generally, the MPI execution line using mpiexec program will look like:

```
mpiexec -n <m> mcnp6.mpi i=input ...
```

where mcnp6.mpi refers to the appropriate MCNP6 MPI executable name and
where &lt;m&gt; is the total number of MPI processes, including the manager,
and &lt;m&gt; -1 worker processes that will track the particles. On other
systems, or for other MPI implementations, the syntax of the MPI command
may differ. The MCNP6 MPI executables include OpenMP, allowing each MPI
worker to utilize additional threads; this is accomplished by setting
the tasks option as follows:

1

## mpiexec -n &lt;m&gt; mcnp6.mpi i=input tasks &lt;n&gt;

where &lt;m&gt; -1 × &lt;n&gt; processes are used to track particles. The syntax
required to allocate enough resources for the threading varies by
system. To utilize an MPI-compiled executable in sequential or threads-
only mode (for example, in early testing of a problem or for plotting
geometry), run mcnp6.mpi without mpiexec -n &lt;m&gt; .

Table 3.4: MCNP6 Execution Line Inputs-File Names

| Keyword †           | Description ‡                                                                                                                                                                                                                                                                                   |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| (Default File Name) | (Default File Name)                                                                                                                                                                                                                                                                             |
| COM                 | File from which plot commands will be read.                                                                                                                                                                                                                                                     |
| COMOUT              | File to which all plot requests are written.                                                                                                                                                                                                                                                    |
| DUMN1 and DUMN2     | Command-line-specified file names for FILES card.                                                                                                                                                                                                                                               |
| HISTP               | Command-line-specified HISTP (history tape) file name.                                                                                                                                                                                                                                          |
| INP                 | User-supplied input file name. This is the name of the file that contains the problem input specification and must be present as a local file.                                                                                                                                                  |
| KSENTAL             | Name of ASCII results file for KCODE sensitivity profiles.                                                                                                                                                                                                                                      |
| LINKIN              | Name of LNK3DNT file to input.                                                                                                                                                                                                                                                                  |
| LINKOUT             | Name of LNK3DNT-format geometry file created by MCNP6.                                                                                                                                                                                                                                          |
| MCTAL               | Tally results file (ASCII).                                                                                                                                                                                                                                                                     |
| MDATA               | TMESH mesh tally data (unformatted binary).                                                                                                                                                                                                                                                     |
| MESHTAL             | FMESH tally output file (ASCII).                                                                                                                                                                                                                                                                |
| NAME                | User-supplied input file name. Will automatically generate OUTP , RUNTPE , MDATA files with the user-supplied name appended with a o , r , and d , respectively. Other generated output files will have unique corresponding single character extentions, followed by any file-type extensions. |
| OUTP                | File name to which results are written. This file may be viewed and/or printed. Created by MCNP6 during problem execution.                                                                                                                                                                      |
| PARTINP             | PARTISN input file for MCNP6 to output.                                                                                                                                                                                                                                                         |
| PLOTM               | Name of graphics metafile.                                                                                                                                                                                                                                                                      |
| PTRAC               | Name (without extension) of output file containing user-filtered particle events.                                                                                                                                                                                                               |
| RSSA                | Name of file from which surface and volume source particles are read.                                                                                                                                                                                                                           |
| RUNTPE              | Name of file containing binary start/restart data. Created by MCNP6 during initial problem execution and modified by the code during continued problem execution.                                                                                                                               |
| SRCTP               | Name of file containing fission source data for a KCODE calculation.                                                                                                                                                                                                                            |
| WSSA                | Name of file to which surface and volume source particles are recorded.                                                                                                                                                                                                                         |
| WWINP               | Name of weight-window generator input file containing either cell- or mesh-based lower weight-window bounds.                                                                                                                                                                                    |
| WWONE               | Name of weight-window generator output file containing cell- or mesh-based time- and/or energy-integrated weight windows.                                                                                                                                                                       |
| WWOUT               | Name of weight-window generator output file containing either cell- or mesh-based lower weight-window bounds.                                                                                                                                                                                   |
| XSDIR               | Name of cross-section directory (XSDIR) file. Note: The default name for the XSDIR file is version specific, e.g., xsdir _ mcnp6.3 for MCNP6.3.                                                                                                                                                 |

† Requires only enough letters of the default name to identify it
uniquely.

‡ File names are limited to a maximum of 256 characters. File names may
also include directory paths.

Table 3.5: MCNP6 Execution Line Inputs-Mode Options

| Option †   | Description                                                                                                                |
|------------|----------------------------------------------------------------------------------------------------------------------------|
| -v         | Print build info to screen, if used all other command line input is disregarded. Input file is not needed for this option. |
| i          | Execute module IMCN to process the input file.                                                                             |
| m          | Execute module PARTISN_INPUT to create LNK3DNT-format geometry file.                                                       |
| p          | Execute module PLOTG to plot geometry.                                                                                     |
| r          | Execute module MCRUN to perform the particle transport.                                                                    |
| x          | Execute module XACT to process the cross-section data.                                                                     |
| z          | Execute module MCPLOT to plot tally results or cross-section data.                                                         |

† Default is ixr .

Table 3.6: MCNP6 Execution Line Inputs-Other Options

| Option   | Description                                                                                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BALANCE  | Provides load balancing when used with MPI. Note: When using multiprocessing with KCODE runs, the option for load balancing is not available.                                |
| CN m     | Continue a run, starting with the m th dump and writing the dumps immediately after the fixed part of the RUNTPE , rather than at the end.                                   |
| C m      | Continue a previous run starting with the m th dump. If m is omitted, the last dump is used.                                                                                 |
| DBUG n   | Write debug information every n particles. Note: An 8-byte integer is allowed.                                                                                               |
| DEV-TEST | Delete time-dependent quantities from files for SQA testing. See 3rd entry on the PRDMP card.                                                                                |
| EOL      | Add after all other MCNP6 keywords to distinguish MCNP6 keywords from directives added by MPICH. Only needed if the MPICH implementation of MPI is used.                     |
| FATAL    | Transport particles and calculate volumes even if fatal errors are found. Not applicable to UM calculations.                                                                 |
| NOTEK    | Indicates that the terminal has no graphics capability. PLOT output is in PLOTM.PS . Equivalent to TERM = 0 .                                                                |
| PRINT    | Create the full output file; equivalent to PRINT card in the input file.                                                                                                     |
| TASKS n  | Invokes OpenMP threading on shared memory systems. The parameter n is the number of threads to be used. This keyword may be used in conjunction with MPI on a hybrid system. |

## 3.3.3 Interrupts

For non-MPI versions, MCNP6 allows four types of interactive interrupts
while it is running:

- Ctrl + c , Enter MCNP6 status (Default if no entry is provided)
- Ctrl + c , s MCNP6 status. The Ctrl + c , s interrupt causes MCNP6 to print the computer time used so far, the number of particles run so far, and the number of collisions. If the code is processing in the IMCN module, it prints the input line being processed and if in the XACT module, it prints the cross section being processed.
- Ctrl + c , m Invoke MCPLOT to create interactive plots of tallies or to further invoke PLOT, to plot the geometry
- Ctrl + c , q Quit MCNP6 gracefully after current history. The Ctrl + c , q interrupt has no effect until MCRUN, the particle transport section of the code, is executed. After particle transport simulation has commenced &lt;ctrl-c&gt;q causes the code to stop after the current particle history, to terminate gracefully, and to produce final output and RUNTPE files.
- Ctrl + c , k Kill MCNP6 immediately. The Ctrl + c , k interrupt kills MCNP6 immediately, without normal termination. If Ctrl + c , k fails, enter Ctrl + c three or more times in a row.

Batch calculations, run in sequential or multiprocessing mode, may be
interrupted and stopped with the creation of a file in the directory
where the calculation was started. The name of the file must be 'STOP
inp ' where inp is the name of the original input file that initiated
the run. On a computer system that is case sensitive (e.g., Linux), the
'stop' must be in lower case and 'INP ' must match the case of the input
file name. The contents of this file are meaningless. Once this file is
created, MCNP6 will terminate the calculation during the next output
rendezvous (see 5th entry on PRDMP card) as if a Ctrl + c , q interrupt
had been issued.

## /warning\_sign Caution

If one uses the Ctrl + c , q interrupt during a KCODE multiple-processor
MPI calculation in Linux, MCNP6 does not finish writing the OUTP file
before the code exits. This failure appears to be an MPI error in the
MPI\_FINALIZE call, where the last processor kills all worker and manager
processes. Also, the Ctrl + c interrupt does not function properly when
using the MPI executable on Windows systems.

On some computer systems, MPI versions, even when run sequentially, do
not allow the interactive interrupts because the MPI daemon catches the
signal and aborts the MCNP6 run.

## 3.4 Tips for Correct and Efficient Problems

Provided in this section are checklists of helpful advice that applies
to three phases of your calculation: defining and setting up the
problem, preparing for the long computer runs that you may require, and
executing the runs that will give you results. A fourth checklist is
provided for KCODE calculations. These checklists should be periodically
revisited as you simulate more complicated problems using the techniques
described in the remainder of Part II.

## 3.4.1 Problem Setup

1. Draw a picture of your geometry to help you with geometry setup.
2. Always plot the geometry to see if it is defined correctly and that it is what was intended.

3. Model the geometry and source distribution in enough detail as needed for accurate particle tracking.
4. Use simple cells.
5. Use the simplest surfaces that solve the problem, including macrobodies.
6. Avoid excessive use of the complement operator, #.
7. Do not set up all the geometry at one time.
8. Put commonly used cards in a separate file and add them to your input file via the READ card.
9. Pre-calculate and compare MCNP6-calculated mass, cell volumes, and surface areas.
10. Use the VOID card when checking the geometry.
11. Look at print tables 10, 110, and 170 to check the source.
12. Check your source with a mesh tally.
13. Be aware of physics approximations, problem cutoffs, and default cross sections.
14. Cross-section sets matter! Check the listing of datasets in the output file.
15. Use separate tallies for the fluctuation chart.
16. Use the most conservative variance-reduction techniques.
17. Do not use too many variance-reduction techniques.
18. Balance user time with computer time.
19. Study all warning messages.
20. Generate the best output (consider always using the PRINT card).
21. Recheck the INP file (materials, densities, masses, sources, etc.).
22. Remember that garbage into MCNP6 equals garbage out of MCNP6.

## 3.4.2 Preproduction

1. Do not use MCNP6 as a black box. Become familiar with the theory and methods.
2. Run some short calculations.
3. Examine the outputs carefully.
4. Study the summary tables.
5. Study the statistical checks on tally quality and the sources of variance.
6. Study the trends of the figures of merit and variance of the variance.
7. Consider the collisions per source particle.
8. Examine the track populations by cell.
9. Scan the mean-free-path column.
10. Check detector diagnostic tables.
11. Understand large tally contributions (with event logs).
12. Strive to reduce the number of unimportant tracks.
13. Check secondary particle production.
14. Compare a 'back-of-the-envelope calculation' to MCNP6 results.

## 3.4.3 Production

1. Save RUNTPE file for expanded output printing, continue-run, and tally plotting.
2. Limit the size of the RUNTPE file with the PRDMP card.
3. Look at figure of merit stability.
4. Make sure answers seem reasonable.
5. Examine and understand the 10 statistical checks provided by MCNP6.
6. Form valid confidence intervals.
7. Make continue-runs if necessary.
8. See if stable errors decrease by 1 / √ N .
9. Remember, accuracy is only as good as the nuclear data, modeling, MCNP6 sampling approximations, etc.
10. Adequately sample all cells.

## 3.4.4 Criticality

1. Determine how many inactive cycles are needed by using the MCNP6 plotter to examine the behavior of k eff and the Shannon entropy of the source distribution with cycle number.
2. Run a large number of histories per cycle. For production runs, at least 10000 neutrons per cycle are recommended. More neutrons per cycle are better.
3. Examine the behavior of k eff with cycle number and continue calculations if trends are noticed.
4. Use at least 100 cycles after source convergence.
5. After a production run, use the MCNP6 plotter again to examine the behavior of k eff and the Shannon entropy of the source distribution with cycle number. Ensure that a sufficient number of inactive cycles were used so that k eff and the source distribution are both properly converged.

## 3.4.5 Warnings and Limitations

All computer simulation codes must be validated for specific uses, and
the needs of one project may not overlap completely with the needs of
other projects. It is the responsibility of the user to ensure that his
or her needs are adequately identified and that benchmarking activities
are performed to ascertain how accurately the code will perform. The
benchmarking done by code developers for the MCNP6 sponsors may or may
not be adequate for a user's particular requirements. We make our
benchmarking efforts public as they are completed, but the user must
also develop a rigorous benchmarking program for their own application.
Such benchmarking efforts by the user also ensures that the user
understands how to use MCNP6 for their application.

The following warnings and known bugs apply to the energies and
particles beyond MCNP4C [198]:

1. Perturbation methods used in MCNP4C have not been extended yet to the non-tabular models present in MCNP6. MCNP6 gives a fatal error if it is run for problems that invoke the perturbation capabilities above the MCNP4C energy range or beyond the MCNP4C particle set.

2. KCODE criticality calculations work only with available actinide nuclear data libraries and have not been extended to the model energy regions of the code.
3. Charged-particle reaction products are not generated for some neutron reactions below 20 MeV in the LA150N library. In calculating total particle-production cross sections, the library processing routines include only those reactions for which complete angular and energy information is given for secondary products. Most 150-MeV evaluations are built 'on top' of existing ENDF and JENDL evaluations which typically go to 20 MeV. Although the 150-MeV evaluations do include the detailed secondary information in the 20-150-MeV range, the &lt;20-MeV data typically do not. Therefore secondary production is generally ignored when processing interactions in that energy range. Table 4.3 lists the actual secondary particle-production thresholds in LA150N. Fixing this situation is non-trivial, and involves a re-evaluation of the low-energy data. Improved libraries will be issued, but on an isotope-by-isotope basis.
4. Beware of the results of an F6:P tally in small cells when running a photon or photon/electron problem. Photon heating numbers include the energy deposited by electrons generated during photon collisions, but assume that the electron energy is deposited locally. In a cell where the majority of the electrons lose all of their energy before exiting that cell, this is a good approximation. However, if the cell is thin and/or a large number of electrons are created near the cell boundary, these electrons could carry significant energy into the neighboring cell. For this situation, the F6:P tally for the cell in which the electrons were created would be too large. The user is encouraged to consider use of the F6:E tally instead, which provides an accurate tally of electron energy deposition within a cell.
5. The FLUKA [199] physics module that was in MCNPX is not present in MCNP6. We recommend using the Los Alamos Quark-Gluon String Model (LAQGSM03.03) [200-216] for very high-energy calculations.
6. Specifying different densities for the same material produces a warning. MCNP6 performs a material density correction for charged-particle energy deposition that is not a strict linear function. MCNP6 searches through all cells, finds the first one with the material of interest, and uses the associated material density to determine the correction factor for all cells using that material. For MCNP4C applications the effect is typically small; therefore this is an adequate procedure. For MCNP6 applications that utilize more charged particles and a greatly expanded energy range, this formerly 'small' correction becomes increasingly important, and the usual way of handling it is not sufficient. A suggested practice in such instances is to specify a unique material identifier for each density.
7. 'Next-event estimators,' i.e., point and ring detectors, DXTRAN, and radiography tallies, use an assumption of isotropic scatter for contributions from collisions within the model regime. These estimators require the angular distribution data for particles produced in an interaction to predict the 'next event.' Information on these distributions is available in tabular form in the libraries; however, this information is not available in the required form from physics models used to produce secondary particles above the tabular region.
8. A numerical problem occurs in the straggling routines with densities less than about 10 -9 g/cm 3 for heavier charged particles and with densities less than about 10 -15 g/cm 3 for electrons. Users should avoid such low densities.
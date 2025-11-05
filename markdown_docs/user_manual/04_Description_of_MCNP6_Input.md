---
title: "Chapter 4 - Description of MCNP6 Input"
chapter: "4"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/4_Description_of_MCNP6_Input.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Chapter 4

## Description of MCNP6 Input

The MCNP code processes several input files during execution. These
processed files are either provided as part of the code distribution,
generated during MCNP code execution, or supplied by the user. This
chapter focuses on the user-supplied input file. The input file is the
primary way that users interact with the MCNP code. The input file
contains information about the problem including the geometry
specification, the description of materials and selection of cross-
section evaluations, the location and characteristics of the source, the
type of answers or tallies desired, and other user-controlled properties
of the simulation. The remainder of this chapter provides details on the
structure, requirements, and processing of the input file.

The input file can have two forms: one for an initial calculation and
one for a restarted calculation. The user specifies problem parameters
using various ASCII text-based input cards. All input cards are
described in Chapter 5. The user will provide only a small subset of all
available input cards in a given problem. All features of MCNP6 should
be used with knowledge and caution. Read and understand the relevant
sections of the manual before using them.

Throughout the input file, alphabetic characters can be upper, lower, or
mixed case. Table 4.2 summarizes some of the numerical limitations
within the code on user-specified numeric labels for various features.
Table 4.1 summarizes some additional limitations for certain input
cards. For particular problems, a user may need to increase the size of
the dimensioned arrays associated with some of these parameters by
altering the source code and recompiling. Although not limited by the
code, in some cases a large input may produce an MCNP simulation that
exceeds the available system memory for a particular compute resource.
Total storage requirements in such cases can be significantly reduced by
turning off model physics for neutron problems (see PHYS :N card).

Table 4.1: MCNP Code Option Limitations

| Category                                           | Number Allowed   |
|----------------------------------------------------|------------------|
| Maximum quantity of TMESH tallies                  | 20               |
| Maximum quantity of transformations                | 999              |
| Maximum levels for nested geometry                 | 20               |
| Maximum length of the list for any single cell     | 9,999            |
| Maximum length of file names                       | 256 characters   |
| Maximum file name path length, including file name | 256 characters   |
| Maximum file path lengths for EMBED card           | 80 characters    |
| Maximum quantity of different tallies              | 9,999            |
| Maximum quantity of detector tallies               | 10,000           |
| Quantity of DXTRAN spheres per particle type       | 10               |
| Quantity of URAN universes                         | unlimited        |
| Entries on IDUM and RDUM cards                     | 2,000            |
| Maximum length of an input line (card)             | 128 characters   |

Table 4.2: MCNP Numerical Limitations on Permitted Values for Card Labels

| Category                            | Number Allowed   |
|-------------------------------------|------------------|
| Cell numbers                        | 1-99,999,999     |
| Surface numbers                     | 1-99,999,999     |
| Material numbers                    | 1-99,999,999     |
| Universe numbers                    | 0-99,999,999     |
| Surface numbers for transformations | 1-999            |
| Cell numbers for transformations    | 1-999            |
| Tally numbers                       | 1-99,999,999     |
| Perturbation numbers                | 1-99,999,999     |
| Source distribution numbers         | 1-999            |
| 'Card numbers'                      | 1-99,999,999     |

## 4.1 MCNP Units

The units of measurement used throughout MCNP6 are the following:

- length in centimeters,
- energy in MeV,
- time in shakes ( 10 -8 s),
- temperature in MeV ( kT ),
- atomic density in atoms/barn-cm,
- mass density in g/cm 3 ,
- cross sections in barns ( 10 -24 cm 2 ),
- heating numbers in MeV/collision, and
- atomic weight ratio based on a neutron mass of 1.008664967 amu (as compared to the current NIST value of 1.008664915 amu [217]). In these units, Avogadro's number is 0 . 59703109 × 10 24 per neutron mass in amu. This corresponds to a value of Avogadro's number of 6 . 02204 × 10 23 per mole (as compared to the current NIST value of 6 . 02214 × 10 23 per mole [217, 218]). These details are used by the MCNP code for computing atom densities from mass densities, so these details may become important when modifying existing xsdir files or specifying the XS card.

All numerical entries specified by the user will be processed by MCNP6
using the above units, for the physical parameter corresponding to the
user entry. See PRINT Table 98 for other physical constants used by
MCNP6. Certain outputs have different units, which are noted as
appropriate.

## 4.2 Initiate Calculation

This form of the input file is used to set up a Monte Carlo particle
transport problem (describe geometry, materials, tallies, etc.). Upon
execution, the MCNP code will process the input and simulate the
specified problem, using additional information from either the message
block or the execution line. See §3.3.2.2 for more detail on executing
the initial calculation input file. The initial calculation input file
has the form shown in Fig. 4.1.

Figure 4.1: MCNP Initial-calculation Input File Format

<!-- image -->

In an MCNP6 initial calculation input file, an optional message block
with its blank line delimiter is followed by a required title card.
After the title card appears, three card blocks follow, each separated
by a single blank line. These three blocks provide, respectively,

1. cell descriptions,
2. surface descriptions, and
3. data about everything else in the problem (materials, source, tallies, etc.).

MCNP6 interprets a blank line as the end of the preceding information
block. A final (optional) blank line at the end of the data block
signals the end of the input file. With a valid set of cards, MCNP6 will
run with or without the blank line terminator. However, when MCNP6
encounters the blank line terminator, MCNP6 will stop reading the input
file even if additional lines exist in the file. This region following
the blank line terminator can be used by the user for problem
documentation or to retain cards not used in the current run.

## 4.3 Restarted Calculations

This section describes the form of the input file used to restart a
previously terminated calculation where it left off. Restarted
calculations can also be used to reconstruct the output of a previous
calculation. During MCNP execution of an input file used in an initial
calculation, MCNP6 will generate an HDF5 restart file with default name
runtpe.h5 . See §D.2 for more details on the restart file and §D.1 for
information on binary HDF5 files in general. This self-contained restart
file contains all information necessary to restart the initial
calculation from the beginning. In addition, the problem results at
various stages of the calculation are recorded in a series of dumps that
can be used to restart (i.e., continue) a simulation. For example, a
simulation run for two hours may be restarted and executed for
additional time. Generally, for a restart file to be readable by the
MCNP code during a restarted calculation, its closure must have been
complete without an unexpected crash, error, or file corruption during
the execution of the initial (or previous) calculation.

There are two ways to restart a calculation, which differ depending on
whether previous dumps are preserved or not. The MCNP6 execution line
(or message-block execution information) must contain either a C or CN

Figure 4.2: MCNP Restart-calculation Input File Format

<!-- image -->

entry to restart a calculation. The restarted calculation will start
with the last dump on the specified restart file by default.
Alternatively, it will start execution with the dump numbered m if
either C m or CN m is specified, where m is an integer corresponding to
the 'dump no.' generated by a previous MCNP6 execution. The available
dumps for restarting calculations are sequentially numbered HDF groups
listed in the group variable of the restart file. See the PRDMP card for
a discussion of the selection of the dump frequency.

The MCNP6 code checks the validity of the requested dump's results by
ensuring the simulation that generated the dump did not terminate
unexpectedly from an error (e.g., too many lost particles or a 'bad
trouble' error). These unexpected terminations are more likely to leave
the code and results in an invalid state during MPI execution. If such
an error is detected, the restarted calculation will stop immediately
with a corresponding message. If the error can be corrected through the
restarted calculation's input file, then the restarted calculation can
be executed with a dump number earlier in the simulation to get results.
If not, the original error must be corrected and the initial calculation
repeated from the beginning.

Unlike other execution forms, restarted calculations use the same
restart file. When the C option is specified on the MCNP6 execution
line, the dumps produced during the restarted calculation are appended
to the dumps from which the calculation restarted. However, by
specifying the CN option instead of the C option, all previous dumps are
removed and new dumps are appended. These new dumps overwrite the old
dumps, providing a way for the user to prevent unmanageable growth of
restart files for particularly large simulations. Restart file growth
also can be controlled by the ndmp entry on the PRDMP card. For both
execution options, only the variable group is changed during the
restarted calculation, so all fixed problem data is preserved between
code executions.

## /warning\_sign Caution

A restarted calculation with the CN option will overwrite the dump that
began the restarted calculation. Thus, it is recommended to use the C
option unless disk space is an issue, particularly if the dump may be
revisited, e.g., to compare results with different card changes in the
restarted calculation's input file.

In addition to the C or CN option on the MCNP6 execution line, users can
specify the restart file name and an optional restart-calculation input
file. Specifying the file name to be used by MCNP6 is detailed in
§3.3.2.2. The optional restart-calculation input file must have the word
CONTINUE as the first entry on the first line (title card), or after the
optional message block and its blank line delimiter. This file has the
form shown in Fig. 4.2.

The data cards allowed in the restart-calculation input file are a
subset of the data cards available for an initial-calculation input
file. The allowed restart-calculation data cards include FQ , DD , NPS ,
CTME , IDUM , RDUM , PRDMP , LOST , DBCN , PRINT , KCODE , MPLOT , MESH
, TALNP , ZA , ZB , ZC , FMESH , RAND , STOP , ZD , and EMBED .

Additionally, the number of threads n specified on the execution line (
tasks n ) may be changed between calculations.

If none of the above items is to be changed the restart-calculation
input file is not required; only the restart file and the C option on
the MCNP6 execution line are necessary. For example, with a properly
closed runtpe.h5 file in the current directory the command line sequence
mcnp6 c will pick up the calculation where it stopped and continue until
another stopping condition is reached.

If the initial calculation producing the restart file was stopped
because of particle cutoff ( NPS card), the value of npp on the NPS card
must be increased for a restarted calculation via a restart-calculation
input file. The parameter npp represents the cumulative histories to be
run, i.e., it includes the summation of the initial-calculation and
restart-calculation histories. Contrarily, the tme parameter on the CTME
card in a restarted calculation is the number of minutes more to run,
not the cumulative time. To run more KCODE cycles, only the fourth entry
on the KCODE card, kct , must be changed. Like npp , kct refers to total
cycles to be run, including previous ones.

In a restarted calculation, a negative number entered for npp on the NPS
card produces a print output file at the time of the requested dump. No
more histories will be run. This can be useful when the printed output
has been lost or you want to alter the content of the output with the
PRINT or FQ cards.

Restarted calculations do not produce identical results to initial-runs
for delayed particle calculations (see the ACT card).

Note that restart files are not compatible from one version of MCNP6 to
the next. Therefore, a restarted calculation should use the same code
version as that which created the restart file. Unless explicitly noted
during code execution, restart files can be read independent of whether
MPI and/or task parallelism is used during the initial or restarted
calculations. Be aware that files from the initial calculation will be
overwritten during the restarted calculation if the FILES card was
present in the initial calculation's input file; see the FILES card for
more details.

## 4.4 Card Format

Most text input is entered in a horizontal format as a series of cards,
with individual data entries that are separated by one or more spaces.
Blank lines are used as delimiters between input blocks and as a
terminator after the data block to indicate the end of the input file.
The remainder of this section describes the structure and options for
text entries in the various blocks of the input file.

## 4.4.1 Message Block

The optional message block allows the user to provide MCNP6 with
additional execution information. It is also a convenient way to avoid
retyping an often-repeated message. Both initial- and restart-
calculation input files can contain a message block that replaces or
supplements the MCNP6 execution line information. If used, the message
block is located before the problem title card in the input file. The
message block starts with the string, MESSAGE: . The message block ends
with a blank line delimiter before the title card. The commands may
continue over multiple lines of the message block, up to the blank line
delimiter. The $ symbol (which indicates an end-of-line comment follows)
and the &amp; symbol (which indicates that the information continues on the
next line) are permitted in message blocks and act as end-of-line
markers. The syntax and components of the message are the same as for
the regular execution line entries. Any file name substitution, program
module execution option, or keyword entry on the execution line takes
precedence over conflicting information in the message block. Renaming
of the input file default file name, i.e., INP = filename , is not a
recognized entry in the message block.

```
1
```

1

1

2

3

For example, assume the MCNP6 execution line required to run the input
file, sphere.i , and to assign user-designated names to the output files
is mcnp6 i=sphere.i o=sphere.o r=sphere.r mctal=sphere.m

The following simplified execution line mcnp6

```
i=sphere _ msgblock.i
```

can provide the same file name assignments through the message block
feature:

```
message: o=sphere.o r= sphere.r mctal= sphere.m Title: bare uranium sphere
```

The three lines above show the message block and the input-file title
card separated by a blank line delimiter for an input file sphere \_
msgblock.i .

## 4.4.2 Problem Title Card

The first card in the file after the optional message block is the
required problem title card. If there is no message block, this must be
the first card in the INP file. It is used as a title in various places
in the MCNP6 output. It can contain any information the user desires (or
it can be left blank), but it typically contains information describing
the particular problem. Note that a blank line elsewhere is used as a
delimiter or as a terminator.

## 4.4.3 Comment Cards

General comment cards can be used anywhere in the input file after the
problem title card and before the last blank terminator card. These
comment cards are used, and encouraged, in input files to provide
additional explanation, details, and organization to the often cryptic
input commands. Comment cards must have a c anywhere in columns 1-5
followed by at least one blank. General comment cards are printed only
with the input file listing and not anywhere else in the MCNP6 output
file. Additionally, a comment can be added to any input card: a $
(dollar sign) terminates data entry on a card and anything that follows
the $ is interpreted as a comment. One exception is that you cannot
enter a comment card or a $ terminator within a TMESH tally definition.

Specific comment cards are provided for tallies (the FC n card) and for
sources (the SC n card). User-provided text on these cards are printed
in the output as a tally title and as a heading for a source probability
distribution, n , respectively.

## 4.4.4 Auxiliary Input File Capability

Subsections of the input file may be inserted using the READ card. The
text of these insertions will be expanded in the output file unless
disabled by the NOECHO keyword on the READ card.

## 4.4.5 Cell, Surface, and Data Cards

Detailed specifications for the cell, surface, and data card blocks are
provided in Chapter 5. A general description of the structure of the
cards in each of these blocks is provided in §3.2.2. Although a
horizontal input format for cards is most commonly used, a vertical
format option permitted by MCNP6 for certain data block cards. The
vertical format is particularly useful for some cell parameters and
source distributions. Both formats are described in the sections that
follow.

## 4.4.5.1 Data Card Horizontal Input Format

Like cell and surface cards, data cards all must begin within the first
five columns. The card name or number and particle designator are
followed by data entries separated by one or more blanks. An individual
entry cannot be split between two lines. There can be only one card of
any given type for a given particle designation [§4.5]). Integers must
be entered where integer input is required. Other numerical data can be
entered as integer or floating point and will be read properly by MCNP6.
In fact, non-integer numerical data can be entered in any form
acceptable to a Fortran E-edit descriptor.

MCNP6 allows five shortcuts to facilitate data input:

1. n R means repeat the immediately preceding entry on the card n times. For example, 2 4R is the same as 2 2 2 2 2 .
2. n I means insert n linear interpolates between the entries immediately preceding and following this feature. For example, 1.5 2I 3.0 on a card is the same as 1.5 2.0 2.5 3.0 . In the construct X n I Y, if X and Y are integers, and if Y-X is an exact multiple of n +1 , then correct integer interpolates will be created. Otherwise, only real interpolates will be created, but Y will be stored directly in all cases. In the above example, the 2.0 value may not be exact, but in the example 1 4I 6 , all interpolates are exact and the entry is equivalent to 1 2 3 4 5 6 .
3. x Mmeans multiply the previous entry on the card by the value x . For example, 1 1 2M 2M 2M 2M 4M 2M 2M is equivalent to 1 1 2 4 8 16 64 128 256 .
4. n J means jump over the entry and take the default value. As an example, the following two cards are identical in their effect:

1

1

DD 0.1 1000

DD J 1000

- J J J is also equivalent to 3J . Also using this shortcut, you can jump to a particular entry on a card without having to specify explicitly previous items on the card. This feature is convenient if you know you want to use a default value but cannot remember it. Another example of this capability is DBCN 2J 10 15.
5. n LOG or, equivalently, n ILOG means insert n (base-10) logarithmic interpolates between the entries immediately preceding and following this feature. For example, 0.01 2ILOG 10 is equivalent to 0.01 0.1 1 10 . In the construct X n ILOG Y, X and Y must be non-zero and have the same sign otherwise a fatal error is produced.

These features apply to both integer and floating-point quantities. If n
(an integer) is omitted in the constructs n R, n I, n LOG, n ILOG, and n
J, then n is assumed to be 1. If x (integer or floating point) is
omitted in x M, it is a fatal error. The rules for dealing with adjacent
special input items are as follows:

1. n R must be preceded by a number or by an item created by R or M.
2. n I, n LOG, and n ILOG must be preceded by a number or by an item created by R or M, and must be followed by a number. The preceding number cannot be 0.0 for n LOG or n ILOG.
3. x M must be preceded by a number or by an item created by R or M.
4. n J may be preceded by anything except I and may begin the card input list.

Several examples follow:

- 1 3M 2R is equivalent to 1 3 3 3 · 1 3M I 4 is equivalent to 1 3 3.5 4 · 1 3M 3M is equivalent to 1 3 9 · 1 2R 2I 2.5 is equivalent to 1 1 1 1.5 2.0 2.5 · 1 R 2M is equivalent to 1 1 2 · 1 R R is equivalent to 1 1 1 · 1 2I 4 3M is equivalent to 1 2 3 4 12 · 1 2I 4 2I 10 is equivalent to 1 2 3 4 6 8 10 · 3J 4R is illegal · 1 4I 3M is illegal · 1 4I J is illegal

## 4.4.5.2 Data Card Vertical Input Format

Column input is particularly useful for cell parameters and source
distributions. Cell importance or volumes strung out on horizontal input
lines are not very readable and often lead to errors when users add or
delete cells. In vertical format, all the cell parameters for one cell
can be on a single line, labeled with the name of the cell. If a cell is
deleted, the user deletes just one line of cell parameters instead of
hunting for the data item that belongs to the cell in each of several
multi-line cell-parameter cards. For source distributions, corresponding
SI , SP , and SB values are side by side. Source options, other than
defaults, are on the next line and must all be entered explicitly. The &amp;
continuation symbol is not needed and is ignored if it is present.

In column format, card names are put side by side on one input line and
the data values are listed in columns under the card names. To indicate
that vertical input format is being used, a # is put somewhere in
columns 1-5 on the line with the card names. The card names must be all
cell parameters, all surface parameters, or all something else. If a
card name appears on a # card, there must not be a regular horizontal
card by that name in the same input file. If there are more entries on
data value lines than card names on the # line, the first data entry is
assumed to be a cell or surface number. If any cell names are entered,
all must be entered. If cell names are entered, the cells do not have to
be in the same order as they are in the cell cards block. If cell names
are omitted, the default order is the order of the cells in the cell
card block. The same rules apply

to surface parameters, but because we presently have only one surface
parameter ( AREA ), column input of surface parameters is less useful.

There can be more than one block of column data in an input file.
Typically, there would be one block for cell parameters and one for each
source distribution. If a lot of cell parameter options are being used,
additional blocks of column data would be needed.

We strongly suggest keeping columns reasonably neat for user
readability. The column format is intended for input data that naturally
fit into columns of equal length, but less tidy data are not prohibited.
If a longer column is to the right of a shorter column, the shorter
column must be filled with enough J entries to eliminate any ambiguity
about which columns the data items are in.

Special syntax items ( R , M , I , LOG , ILOG , and J ) are not as
appropriate in column format as they are on horizontal lines, but they
are not prohibited. They are, of course, interpreted vertically instead
of horizontally. Multiple special syntax items, such as 9R , are not
allowed if cell or surface names are present.

The form of a column input block is:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The following rules apply:

1. The # is somewhere in columns 1-5.
2. Each line can be only 128 columns wide.
3. Each column, S i through d li , where l may be less than N , represents a regular input card.
4. The S i must be valid MCNP6 card names. They must be all cell parameters, all surface parameters, or all something else.
5. d li through d Ni must be valid entries for an S i card, except that d l +1 ,i through d Ni may be some J s possibly followed by some blanks.
6. If d ji is non-blank, d j,i -1 must also be non-blank. A J may be used if necessary to make d j,i -1 non-blank.
7. The S i must not appear anywhere else in the input file.
8. The k j are optional integers. If any are non-blank, all must be non-blank.
9. If the S i are cell parameter card names, the k j , if present, must be valid cell names. The same is true with surface parameters.
10. If the k j is present, the d ji must not be multiple special syntax items, such as 9R or 9M .

## 4.4.6 Continuation Lines

If the first five columns of a card are blank, the entries on the card
are interpreted as a continuation of the data from the last named card.
The user also can continue data on the following card by ending the line
with an &amp; (ampersand) preceded by at least one blank space. In this
case, the data on the continuation card can be anywhere from column 1
until the end of the line [Table 4.1]. As before, completely blank cards
are reserved as delimiters between the cell, surface, and data-card
blocks in the input file.

## 4.5 Particle Designators

Numerous input cards require a particle designator to distinguish
between input data for tracked particles. Refer to the pertinent card
information for instructions. The particle designator consists of a
colon ( : ) followed by the particle symbol(s) immediately after the
name of the card. These particle designations are presented in Table
4.3.

## Details:

- 1 'DOP' indicates decayed on production.
- 2 The ' # ' symbol represents all possible heavy-ion types-in other words, any ion that is not one of the four light ions available in MCNP6. A list of heavy ions available for transport is provided in Appendix C.
- 3 Positrons are treated identical to electrons in transport (outside magnetic field effects), and need to be used with the electron transport option (particle e ) enabled. Refer to the MODE card to see the exceptions for positron labels.

At least one blank must follow the particle designator. For example, IMP
: N signifies neutron importance values follow while IMP : P signifies
photon importance values follow. To specify the same value for more than
one kind of particle, a single card can be used instead of several. For
example, if the designation IMP : E,P,N 1 1 0 appears on a cell card,
the electron importance for that cell is 1, the photon importance is 1,
and the neutron importance is 0. With a tally card, the particle
designator follows the card name including tally number. For example, *
F5 : N indicates a neutron point-detector energy tally. In the heating
tally case, two particle designators may appear. The syntax F6 : N,P
indicates the combined heating tally for both neutrons and photons.

## 4.6 Default Values

Many MCNP6 input parameters have default values that are described with
the associated card definitions. Therefore, you do not always have to
specify explicitly every input parameter every time if the defaults
match your needs. If an input card is left out, the default values for
all parameters on the card are used. However, if you want to change a
particular default parameter on a card where others precede that
parameter, you have to specify the others or use the n J jump feature to
jump over the parameters for which you still want the defaults. For
example, the input CUT : p 3 J -0.10 is a convenient way to use the
defaults for the first three parameters on the photon cutoff card but
change the fourth.

Table 4.3: MCNP6 Particle Identifiers and Parameters

| ipt   | Name                                         | Symbol   | Mass [219] (MeV)   | Low Energy Cutoff   | Default Cutoff   | Mean Lifetime [219] (s)   | Mean Lifetime [219] (s)   |
|-------|----------------------------------------------|----------|--------------------|---------------------|------------------|---------------------------|---------------------------|
|       |                                              |          |                    | (MeV)               | (MeV)            | In MCNP6                  | Actual (if different)     |
| 1     | neutron (n)                                  | N        | 939.56563          | 0.0                 | 0.0              | Stable                    | 887.0                     |
| 2     | photon ( γ )                                 | P        | 0.0                | 10 - 6              | 10 - 3           | 10 29                     |                           |
| 3     | electron (e - )                              | E        | 0.511008           | 10 - 5              | 10 - 3           | 10 29                     |                           |
| 4     | negative muon ( µ - )                        | |        | 105.658389         | 10 - 3              | 0.11261          | 2 . 19703 × 10 - 6        |                           |
| 5     | anti neutron (n)                             | Q        | 939.56563          | 0.0                 | 0.0              | Stable                    | 887.0                     |
| 6     | electron neutrino ( ν e )                    | U        | 0.0                | 0.0                 | 0.0              | 10 29                     |                           |
| 7     | muon neutrino ( ν m )                        | V        | 0.0                | 0.0                 | 0.0              | Stable                    |                           |
| 8     | positron (e + ) [ 3 ]                        | F        | 0.511008           | 10 - 3              | 10 - 3           | 10 29                     |                           |
| 9     | proton (p + )                                | H        | 938.27231          | 10 - 3              | 1.0              | 10 29                     |                           |
| 10    | lambda baryon ( Λ 0 )                        | L        | 1115.684           | 10 - 3              | 1.0              | DOP [ 1 ]                 | 2 . 632 × 10 - 10         |
| 11    | positive sigma baryon ( Σ + )                | +        | 1189.37            | 10 - 3              | 1.26760          | DOP [ 1 ]                 | 7 . 99 × 10 - 11          |
| 12    | negative sigma baryon ( Σ - )                | -        | 1197.436           | 10 - 3              | 1.26760          | DOP [ 1 ]                 | 1 . 479 × 10 - 10         |
| 13    | cascade; xi baryon ( Ξ 0 )                   | X        | 1314.9             | 10 - 3              | 1.0              | DOP [ 1 ]                 | 2 . 9 × 10 - 10           |
| 14    | negative cascade; negative xi baryon ( Ξ - ) | Y        | 1321.32            | 10 - 3              | 1.40820          | DOP [ 1                   | 1 . 639 × 10 - 10         |
| 15    | omega baryon ( Ω - )                         | O        | 1672.45            | 10 - 3              | 1.78250          | ] DOP [ 1 ]               | 8 . 22 × 10 - 11          |
| 16    | positive muon ( µ + )                        | !        | 105.658389         | 10 - 3              | 0.11261          | 2 . 19703 × 10 - 6        |                           |
| 17    | anti electron neutrino ( ν e )               | <        | 0.0                | 10 - 3              | 0.0              | 10 29                     |                           |
| 18    | anti muon neutrino ( ν m )                   | >        | 0.0                | 0.0                 | 0.0              | Stable                    |                           |
| 19    | anti proton (p)                              | G        | 938.27231          | 10 - 3              | 1.0              | 10 29                     |                           |
| 20    | positive pion ( π + )                        | /        | 139.56995          | 10 - 3              | 0.14875          | 2 . 603 × 10 - 8          |                           |
| 21    | neutral pion ( π 0 )                         | Z        | 134.9764           | 0.0                 | 0.0              | 8 . 4 × 10 - 17           |                           |
| 22    | positive kaon (K + )                         | K        | 493.677            | 10 - 3              | 0.52614          | 1 . 2371 × 10 - 8         |                           |
| 23    | kaon, short (K 0 S )                         | %        | 497.672            | 0.0                 | 0.0              | 0 . 8926 × 10 - 10        |                           |
| 24    | kaon, long (K 0 L )                          | ˆ        | 497.672            | 0.0                 | 0.0              | 5 . 17 × 10 - 8           |                           |
| 25    | anti lambda baryon ( Λ 0 )                   | B        | 1115.684           | 10 - 3              | 1.0              | DOP [ 1 ]                 | 2 . 632 × 10 - 10         |
| 26    | anti positive sigma baryon ( Σ + )           | _        | 1189.37            | 10 - 3              | 1.26760          | DOP [ 1 ]                 | 7 . 99 × 10 - 11          |
| 27    | anti negative sigma baryon ( Σ - )           | ~        | 1197.436           | 10 - 3              | 1.26760          | DOP [ 1 ]                 | 1 . 479 × 10 - 10         |
| 28    | anti cascade; anti neutral xi baryon ( Ξ 0 ) | C        | 1314.9             | 10 - 3              | 1.0              | DOP [ 1 ]                 | 2 . 9 × 10 - 10           |
| 29    | positive cascade; positive xi baryon ( Ξ + ) | W        | 1321.32            | 10 - 3              | 1.40820          | DOP [ 1 ]                 | 1 . 639 × 10 - 10         |
| 30    | anti omega ( Ω - )                           | @        | 1672.45            | 10 - 3              | 1.78250          | DOP [ 1 ]                 | 8 . 22 × 10 - 11          |
| 31    | deuteron (d)                                 | D        | 1875.627           | 10 - 3              | 2.0              | 10 29                     |                           |
| 32    | triton (t)                                   | T        | 2808.951           | 10 - 3              | 3.0              | 12.3 years                |                           |
| 33    | helion ( 3 He)                               | S        | 2808.421           | 10 - 3              | 3.0              | 10 29                     |                           |
| 34    | alpha particle ( α )                         | A        | 3727.418           | 10 - 3              | 4.0              | 10 29                     |                           |
| 35    | negative pion ( π - )                        | *        | 139.56995          | 10 - 3              | 0.14875          | 2 . 603 × 10 - 8          |                           |
| 36    | negative kaon (K - )                         | ?        | 493.677            | 10 - 3              | 0.52614          | 1 . 2371 10 - 8           |                           |
| 37    | heavy ions [ 2 ]                             | #        | varies             | 10 - 3              | 5.0              | × 10 29                   |                           |

## 4.7 Input Error Messages

MCNP6 makes extensive checks of the input file for user errors. If the
user violates a basic constraint of the input specification, a fatal
error message is printed, both at the terminal and in the OUTP file. If
a fatal input error is detected, MCNP6 will terminate before running any
particles. The first fatal error is real; subsequent error messages may
or may not be real because of the nature of the first fatal message. The
FATAL option on the MCNP6 execution line instructs MCNP6 to ignore fatal
errors and run particles, but the user should be extremely cautious when
doing this. The FATAL does not apply to UM calculations [Chapter 8].

Most MCNP6 error messages are either warnings or comments that are not
fatal. Warnings are intended to inform the user about unconventional
input parameters or running conditions and may need further attention.
Comments relay useful additional information to the user. The user
should not ignore these messages but should understand their
significance before making important calculations.

In addition to fatal, warning, comment, and deprecation messages, MCNP6
issues BAD TROUBLE messages immediately before any impending
catastrophe, such as a divide by zero, which would otherwise cause the
program to 'crash.' MCNP6 terminates as soon as the BAD TROUBLE message
is issued. User input errors in the INP file are the most common reason
for issuing a BAD TROUBLE message. These error messages indicate what
corrective action is required.

Other output messages that may be encountered describe IEEE exception
warnings after a calculation has finished. These usually indicate that
exceptional arithmetic was performed during the calculation relative to
[220] (e.g., invalid operations such as 0 . 0 / 0 . 0 , division by
zero, overflow, underflow, or inexact calculations that cannot be
represented with infinite precision such as 2 . 0 / 3 . 0 or log(1 . 1)
).

## 4.8 Geometry Errors

There is one important kind of input error that MCNP6 will not detect
while processing data from the INP file. MCNP6 cannot detect overlapping
cells or gaps between cells until a particle track actually gets lost.
Even then the precise nature of the error may remain unclear. However,
there is much that you can and should do to check your geometry before
starting a long computer run.

Use the geometry-plotting feature of MCNP6 to look at the system from
several directions and at various scales. Be sure that what you see is
what you intend. Any gaps or overlaps in the geometry will probably show
up as dashed lines. The intersection of a surface with the plot plane is
drawn as a dashed line if there is not exactly one cell on each side of
the surface at each point. Dashed lines can also appear if the plot
plane happens to coincide with a plane of the problem, there are any
cookie-cutter cells in the source, or there are DXTRAN spheres in the
problem.

One way to check your geometry is to set up and run a short problem in
which your system is flooded with particle tracks from an external
source. The changes required in the INP file to perform this test
follow:

1. Add a VOID card to override some of the other specifications in the problem and make all the cells voids, turn heating tallies into flux tallies, and turn off any tally multiplication ( FM ) cards.
2. Add another cell and a large spherical surface to the problem such that the surface surrounds the system and the old outside world cell is split by the new surface into two cells: the space between the system and the new surface, which is the new cell, and the space outside the new surface, which is now the outside world cell. Be sure that the new cell has non-zero importance. Actually, it is best to make all non-zero importance equal. If the system is infinite in one or two dimensions, use one or more planes instead of a sphere.

3. Replace the source specifications by an inward directed surface source to flood the geometry with particles. To do this, you can use the command

1

SDEF SUR=m NRM=-1

where m is the number of the new spherical surface added in Step 2. If
the new surface is a plane, you must specify the portion to be used by
means of POS and RAD or possibly X , Y , and Z source distributions.

Because there are no collisions, a short calculation will generate a
great many tracks through your system. If there are any geometry errors,
they should cause some of the particles to get lost.

When a particle first gets lost, whether in a special run with the VOID
card or in a regular production run, the history is rerun to produce
some special output on the OUTP file. Event-log printing is turned on
during the rerun. The event log will show all surface crossings and will
tell you the path the particle took to the bad spot in the geometry.
When the particle again gets lost, a description of the situation at
that point is printed. You can usually deduce the cause of the lost
particle from this output. It is not possible to rerun lost particles in
a multitasking run.

If the cause of the lost particle is still obscure, try plotting the
geometry with the origin of the plot at the point where the particle got
lost and with the horizontal axis of the plot plane along the direction
the particle was moving. You might also consider turning COLOR OFF using
the interactive geometry plotter. A wire drawing then appears, reducing
the complexity of the visual representation caused by the color. The
cause of the trouble is likely to appear as a dashed line somewhere in
the plot or as some discrepancy between the plot and your idea of what
it should look like.
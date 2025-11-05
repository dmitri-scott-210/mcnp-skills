---
title: "Chapter 5.13 - Problem Termination, Output Control, and Misc"
chapter: "5.13"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.13_Problem_Termination,_Output_Control,_and_Misc.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Details:

- 1 For problems using photon cell importance ( IMP:P ), rather than photon weight windows ( WWN n :P ), a good first guess for PWT card entries is either the default value, w k = -1 , or set w k in every cell to the average source weight.
- 2 For problems with photon weight windows (i.e., WWP:P exists), the PWT card is ignored and the correct numbers of photons are produced within the weight windows.

<!-- image -->

The PWT card controls the production of neutron-induced photons by
comparing the total weight of photons produced with a relative threshold
weight specified on the PWT card. This threshold weight is relative to
the neutron cell importance and, if w k &lt; 0 , to the source neutron
weight. If more neutron-induced photons are desired, the absolute value
of w k should be lowered to reduce the weight and therefore increase the
number of photons. If fewer neutron-induced photons are desired, the
absolute value of w k should be increased.

## 5.13 Problem Termination, Output Control, and Miscellaneous Cards

## 5.13.1 Problem Termination

Six normal ways to terminate an MCNP6 calculation are:

1. the NPS card,
2. the CTME card,
3. the STOP card,
4. the calculation time limit,
5. the end of a surface source file, and
6. the number of cycles on a KCODE card.

If more than one termination condition is in effect, then the one
encountered first will control termination of the MCNP6 calculation.

## 5.13.1.1 NPS: History Cutoff

Terminates the MCNP6 calculation after a requested number of histories
have been transported, unless the calculation is terminated earlier for
some other reason (such as the computer time cutoff, CTME ).

| Data-card Form: NPS npp npsmg n _ per _ batch   | Data-card Form: NPS npp npsmg n _ per _ batch                                                                                                                                         |
|-------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| npp                                             | The total number of histories to be run in the problem. An 8-byte integer is permitted for npp ( 1 , 2 ).                                                                             |
| npsmg                                           | Number of histories for which direct source contributions are to be made to the pixels of an FIR radiography image grid. An 8-byte integer is permitted for npsmg [§2.5.6.3.1]. ( 3 ) |

n \_ per \_ batch

Default: Infinite.

Use: As needed to terminate the calculation. In a criticality
calculation, the NPS card has no meaning and a warning error message is
issued if it is used. Highly recommended for use in multiprocessor
computations.

## Details:

- 1 In a restart calculation, the NPS input values are the total number of particles including those calculations before the current restarted calculation; they are cumulative. A negative npp entry means to print an output file at the time of the last history run and then stop.
- 2 In a surface source problem, either more or fewer than all of the particle histories on the RSSA surface source file will be run, depending on the value of npp entered on the NPS card. Let N 1 represent the number of original histories. If npp &lt; N 1 , Russian roulette with weight adjustment will be played with each history in the file using a survival probability of npp /N 1 . If npp &gt; N 1 , the histories will be split npp /N 1 -to-1 with the fractional part is taken care of by sampling. This can be done equally well for non-spherical sources by cell importance splitting. With a spherical source, each multiple occurrence of the history is sampled for a different starting location on the source sphere, possibly improving the spatial statistics of the results. In either case, the use of the NPS card will not provide additional information about the original source distributions or the transport to the recording surface crossing.
- 3 When the number of source histories exceeds npsmg , the time-consuming process of determining the attenuation of the FIR direct contribution is avoided by adding the average of the previous direct contributions into each of the appropriate tally bins. Depending on the computer time required to calculate the direct image in a particular problem, npsmg can save from a few seconds to upward of ten minutes per history in some cases. For example, a mono-energetic isotropic point source or a monoenergetic mono-directional surface source requires only one history to determine completely the direct image. For this case, npsmg = 1 is adequate.

## 5.13.1.2 CTME: Computer Time Cutoff

Allows the user to specify minutes of computer time after which MCNP6
will terminate the calculation. MCNP6 checks the computer time remaining
in a running problem and will terminate the calculation itself, allowing
enough time to wrap up and terminate gracefully.

## Data-card Form: CTME tme

tme

Default:

Infinite.

Use: As needed.

maximum amount of computer time (in minutes) to be spent in the Monte
Carlo calculation ( 1 , 2 ).

The number of histories to be used per batch for tallies that use batch
statistics. If no tallies use batch statistics, this has no effect. If
npp is not evenly divided by n \_ per \_ batch , npp will be increased to
the nearest value that is. npsmg is not adjusted at this time, as the
FIR tally does not yet support batch statistics. An 8-byte integer is
permitted for n \_ per \_ batch .

1

## Details:

- 1 For a restarted calculation, the time on the CTME card is the time relative to the start of the restarted calculation; it is not cumulative.
- 2 For multiprocessor calculations, it is highly recommended that the NPS card be used to limit the run time.

## 5.13.1.3 STOP: Precision Cutoff

Enables termination of calculations based on the number of particle
histories run, the computer time expended, or the desired precision for
a specified tally.

| Data-card Form: STOP   | keyword= value(s)...                                                                                  |
|------------------------|-------------------------------------------------------------------------------------------------------|
| NPS npp [ npsmg ]      | Stop calculation after npp particle histories ( 1 ). See the NPS card.                                |
| CTME tme               | Stop calculation after tme minutes of computer time ( 2 ). See the CTME card.                         |
| F k e                  | Stop calculation when the tally fluctuation chart of tally k has a relative error less than e . ( 3 ) |

Use: If values for any (or all) of the keywords are supplied, MCNP6 will
terminate the problem at the first met criteria.

## Details:

- 1 For radiography problems, a second NPS keyword entry, npsmg , may be provided to specify how many histories are used for direct radiography tally contributions.
- 2 For multitasking calculations, CTME will be checked only at rendezvous points, where all tasks rendezvous for tally fluctuations and other activities.
- 3 The tally precision stop will be checked only at rendezvous points for the tally bin of the tally fluctuation charts. Thus, the calculation usually will proceed for a short time after the desired error is achieved. See TF card.

## 5.13.1.3.1 Example 1

STOP F111 0.05

MCNP6 will stop at the first rendezvous for which the relative error of
the tally bin for the tally fluctuation chart of tally F111 is less than
0.05. MCNP6 may stop at error=0.048 or other value slightly less than
0.05.

## 5.13.2 RAND: Random Number Generation

Specifies the type of random number generator as well as the seed,
starting history number, and stride (if applicable).

| Data-card Form:   | RAND keyword = value(s) ...                                                                                                                                                                                                                                                         | RAND keyword = value(s) ...                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GEN               | Type of random number generator to be used by MCNP6 ( 3 ). If                                                                                                                                                                                                                       | Type of random number generator to be used by MCNP6 ( 3 ). If                                                                                                                                                                                                                                                                                                                                                                                                     |
|                   |                                                                                                                                                                                                                                                                                     | GEN = 1 then use MCNP6 Lehmer 48-bit Linear Congruential Generator (LCG), which has a period of 7 . 0 × 10 13 numbers. (DEFAULT)                                                                                                                                                                                                                                                                                                                                  |
|                   |                                                                                                                                                                                                                                                                                     | GEN = 2 then use L'Ecuyer 63-bit LCG number 1, which has a period of 9 . 2 × 10 18 numbers.                                                                                                                                                                                                                                                                                                                                                                       |
|                   |                                                                                                                                                                                                                                                                                     | GEN = 3 then use L'Ecuyer 63-bit LCG number 2, which has a period of 9 . 2 × 10 18 numbers.                                                                                                                                                                                                                                                                                                                                                                       |
|                   |                                                                                                                                                                                                                                                                                     | GEN = 4 then use L'Ecuyer 63-bit LCG number 3, which has a period of 9 . 2 × 10 18 numbers.                                                                                                                                                                                                                                                                                                                                                                       |
|                   |                                                                                                                                                                                                                                                                                     | GEN = 5 then use L'Ecuyer 63-bit LCG number 4, which has a period of 2 . 3 × 10 18 numbers.                                                                                                                                                                                                                                                                                                                                                                       |
|                   |                                                                                                                                                                                                                                                                                     | GEN = 6 then use L'Ecuyer 63-bit LCG number 5, which has a period of 2 . 3 × 10 18 numbers.                                                                                                                                                                                                                                                                                                                                                                       |
|                   |                                                                                                                                                                                                                                                                                     | GEN = 7 then use L'Ecuyer 63-bit LCG number 6, which has a period of 2 . 3 × 10 18 numbers.                                                                                                                                                                                                                                                                                                                                                                       |
|                   |                                                                                                                                                                                                                                                                                     | GEN = 8 then use SFC64, which can provide 2 192 ≈ 6 . 2 × 10 57 histories an independent random sequence of length 2 64 ≈ 1 . 8 × 10 19 ( 5 ). This generator is recommended for all use cases.                                                                                                                                                                                                                                                                   |
| SEED              | Random number generator seed for starting the transport of the first particle history in a run. (DEFAULT: SEED = 19073486328125 ) Restriction: For generators 1-7, must end with an odd digit. Note: An 8-byte integer is permitted for keyword SEED (i.e., up to 18 digits). ( 4 ) | Random number generator seed for starting the transport of the first particle history in a run. (DEFAULT: SEED = 19073486328125 ) Restriction: For generators 1-7, must end with an odd digit. Note: An 8-byte integer is permitted for keyword SEED (i.e., up to 18 digits). ( 4 )                                                                                                                                                                               |
| STRIDE            |                                                                                                                                                                                                                                                                                     | Number of random numbers between source particles. This option does not affect generator 8. Note: An 8-byte integer is permitted for keyword STRIDE . (DEFAULT: STRIDE = 152917 )                                                                                                                                                                                                                                                                                 |
| HIST              |                                                                                                                                                                                                                                                                                     | If HIST = n , then causes the starting random number of the problem to be that which would normally start the n th history. That is, causes the n th history to be the first history of a problem for debugging purposes. Setting HIST = n can also be used to select a random number sequence different from that in an identical problem to compare statistical convergence. Note: An 8-byte integer is permitted for keyword HIST . ( 4 ) (DEFAULT: HIST = 1 ) |

## Details:

- 1 RAND entries must be used instead of obsolete DBCN entries 1, 8, 13, and 14.
- 2 The RAND card may be used to change the problem random number seed in a restarted calculation. This capability provides a work-around for avoiding a troublesome particle history. This procedure is not recommended, but is permitted. Be aware that repeatability is very difficult to achieve if this feature is used.
- 3 If the period is exceeded, random numbers will be reused, but the random number sequence used for subsequent histories will differ from the random number sequence used for previous histories. There

should be no impact on results. Generator 8 provides the longest period.
For generators 1-7, decreasing the stride will reduce the chances of
exceeding the period, but may cause reuse of random numbers if the
stride is exceeded. Generally, strides of 4000 or so are reasonable for
criticality problems, while the default stride or greater may be needed
for problems with heavy variance reduction.

- 4 The i th source particle always starts with the same random number; this correlated source sampling enables faster evaluation of small problem differences where the problems have identical source distributions. Caution:
- 5 The SFC64 generator operates differently than the other generator options. In the LCGs, there is a single stream within which each history is started at some equally spaced point based on the STRIDE option. In SFC64, the initial condition for each history is a function of both the history identifier and the user-input SEED . This function is designed such that changing the SEED will change the initial condition for every history to an independent one. Each initial condition provides an independent sequence of length 2 64 . As a result, random number reuse is functionally impossible and there are no pairs of SEED s that can result in correlated simulations [§2.11.2].

<!-- image -->

## 5.13.3 PRINT: Printed Output Tables

Allows selective printing or suppression of optional output tables.

| Data-card Form: PRINT x 1 x 2 . . .   | Data-card Form: PRINT x 1 x 2 . . .                                                                                                                                    |
|---------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x i                                   | List of optional and default table numbers to be included in or excluded from the output file. If there are no entries for x i , the full output print is provided. If |
|                                       | x i > 0 for all i , the tables specified by each positive x i are provided in addition to the 'basic' output tables.                                                   |
|                                       | x i < 0 for any i , the full output applicable to the problem is printed with the exception of those tables identified by negative x i values.                         |

Default: Absence of a PRINT card in the MCNP input file or a PRINT
option on the MCNP6 execution line [§3.3.2] will result in a reduced
output print comprised only of the tables in Table 5.27 marked 'basic,'
'default,' and 'shorten.'

Use: Optional. To get all optional PRINT tables applicable to your
problem use the PRINT card without entries in the MCNP input file or the
PRINT option on the execution line. The execution line takes precedence
over the input card. Entries on the PRINT card can be in any order;
however, no entries may follow the PRINT option on the MCNP6 execution
line.

Table 5.27: MCNP6 Output Tables

| #     | Type        | Table Description                                                                                                                                    | §         |
|-------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| 10    | optional    | Source coefficients and distribution.                                                                                                                | 5.13.3.4  |
| 20    | optional    | Weight-window information.                                                                                                                           |           |
| 30    | optional    | Tally description.                                                                                                                                   |           |
| 32    | optional    | Mesh tally description.                                                                                                                              |           |
| 35    | optional    | Coincident detectors.                                                                                                                                |           |
| 38    | optional    | Fission multiplicity data; controlled by Table 30.                                                                                                   |           |
| 40    | optional    | Material composition.                                                                                                                                |           |
| 41    | default     | LAHET physics options.                                                                                                                               |           |
| 43    | unavailable | LAHET elastic cross sections.                                                                                                                        |           |
| 44    | optional    | Activities of the materials in an SDEF PAR = SP problem.                                                                                             |           |
| 50    | optional    | Cell volumes and masses, surface areas.                                                                                                              | 5.13.3.6  |
| 60    | basic       | Cell importance.                                                                                                                                     | 5.13.3.7  |
| 62    | basic       | Forced collision and exponential transform.                                                                                                          |           |
| 70    | optional    | Surface coefficients.                                                                                                                                | 5.13.3.8  |
| 72    | basic       | Cell temperatures.                                                                                                                                   | 5.13.3.9  |
| 80    | optional    | ESPLT / TSPLT importance ratios.                                                                                                                     |           |
| 85    | optional    | Continuous energy calculation: Charged-particle stopping powers and straggling.Multigroup calculation: flux values for biasing adjoint calculations. | 5.13.3.10 |
| 86    | optional    | Electron bremsstrahlung and secondary production.                                                                                                    |           |
| 87 90 | optional    | Secondary heavy ion stopping powers and straggling ( 1 ). KCODE                                                                                      | 5.13.3.11 |
|       | optional    | source data.                                                                                                                                         |           |
| 95    | default     | GENXS [§5.7.10.1] tally input.                                                                                                                       |           |
| 98    | optional    | Physical constant and compile options.                                                                                                               | 5.13.3.12 |
| 100   | basic       | Cross-section tables.                                                                                                                                | 5.13.3.13 |
| 101   | basic       | Particle and energy limits.                                                                                                                          |           |
| 102   | optional    | Assignment of S ( α,β ) data to nuclides.                                                                                                            |           |
| 110   | optional    | Initial phase-space values for first 50 histories                                                                                                    | 5.13.3.14 |
| 115   | default     | Fission multiplicity summary.                                                                                                                        |           |
| 117   | default     | Spontaneous and induced fission multiplicities and moments.                                                                                          |           |
| 118   | default     | Neutron captures, moments, and multiplicity distributions.                                                                                           |           |
| 120   | optional    | Analysis of the quality of your importance function.                                                                                                 |           |
| 126   | basic       | Particle activity in each cell.                                                                                                                      | 5.13.3.15 |
| 128   | optional    | Universe map.                                                                                                                                        |           |
| 130   | optional    | Neutron/photon/electron weight balance.                                                                                                              | 5.13.3.16 |
| 140   | optional    | Neutron/photon nuclide activity ( 2 ).                                                                                                               | 5.13.3.17 |
| 150   | optional    | DXTRAN diagnostics.                                                                                                                                  |           |
| 160   | default     | TFC bin tally analysis.                                                                                                                              |           |
| 161   | default     | tally empirical history-score probability density function plot.                                                                                     | 5.13.3.18 |
| 162   | default     | tally empirical history-score cumulative density function plots.                                                                                     | 5.13.3.19 |
| 163   | optional    | Receiver-Operator Characterization (ROC) curve data.                                                                                                 |           |
| 170   | optional    | Source distribution frequency tables, surface source.                                                                                                |           |
| 175   | shorten     | Estimated k eff results by cycle.                                                                                                                    | 5.13.3.20 |
| 178   | optional    | Estimated k eff results by batch size.                                                                                                               |           |
| 179   | optional    | ASCII plot of estimated collision/absorption/track-length k eff one-standard-deviation interval versus cycle number.                                 |           |
| 190   | basic       | Weight-window generator summary.                                                                                                                     | 5.13.3.21 |

continued on next page. . .

1

2

3

4

Table 5.27, continued

|   # | Type     | Table Description                               | §         |
|-----|----------|-------------------------------------------------|-----------|
| 198 | optional | Weight windows from multigroup fluxes.          |           |
| 199 | optional | Weight-window diagnostics table.                | 5.13.3.22 |
| 200 | basic    | Weight-window-generated values.                 | 5.13.3.23 |
| 210 | default  | Burnup summary table.                           |           |
| 220 | default  | Burnup summary table summed over all materials. |           |

## Details:

- 1 Table 87 will not be printed unless 85 and 87 are specified explicitly on the PRINT card.
- 2 The DISABLE card will suppress this table even if it is listed on the PRINT card.
- 3 The LNK3DNT embedded geometry information PRINT table has placeholder number 'XX.' This deficiency has been logged in the MCNP issue tracking system for resolution.

The following output will be printed automatically, as applicable:

- a listing of the input file,
- the problem summary of particle creation and loss,
- KCODE cycle summaries,
- tallies,
- tally fluctuation charts,
- the tables listed in Table 5.27 as basic, and
- the tables listed in Table 5.27 as default, provided they are not turned off explicitly with the PRINT card.

In an MCNP6 output file, a table number appears in the upper right-hand
corner of each table, providing a convenient pattern when scanning the
output file with an editor. The pattern is ' print table n ,' where n ,
the table number, is always preceded by one space and is a two- or
three-digit number. The table numbers, titles, and type are summarized
in Table 5.27. 'Basic' tables cannot be controlled by the PRINT card.
'Default' tables are automatically printed but can be turned off.
'Optional' tables with can be turned off and on with the PRINT card or
option.

With two exceptions, the PRINT control can be used in a restarted
calculation to recover all or any applicable PRINT tables, even if they
were not requested in the original calculation. The following example
restartedcalculation input file:

<!-- image -->

| continue   |
|------------|
| nps -1     |
| print      |
| prdmp 2j 1 |

will create the output file for the initial calculation starting with
the Problem Summary (located after PRINT table 110 ) and will also
create a mctal file using the PRDMP card. However, this input may not
always be sufficient; additional information such as an EMBED card may
be needed for calculations that use embedded mesh geometries. Moreover,
note that

1

1

1

- PRINT table 128 can never be printed if it was not requested in the original calculation and
- PRINT table 140 can never be printed if it was disabled in the original calculation using the DISABLE card.

Several of the output tables listed in Table 5.27 have additional
restrictions:

1. If you turn off table 160, then tables 161 and 162 will not appear either. If table 160 is printed, they will all be printed. All three tables are automatically printed if there is no PRINT card or if there is a blank PRINT card. If a PRINT card has a positive entry, tables 160, 161, and 162 will not appear unless table 160 is explicitly requested. If the entry is negative, they will appear unless table 160 is explicitly turned off.
2. Table 175 cannot be turned off completely, but the output can be greatly shortened to every 100 cycles plus the last five cycles. The specification PRINT -175 and PRINT 110 both will produce the short version of table 175.
3. Tables 128 and 140 have unique storage behavior. If table 128 is not turned on in an initial calculation, it cannot be turned on in a subsequent restarted calculation because the (often large) storage arrays have not been set up. If table 140 is disabled in the initial calculation using the DISABLE card, it cannot be turned on in a subsequent restarted calculation. The information in the other tables is always stored, whether or not it is printed. A warning will be printed in a repeated structures problem if the universe map/lattice activity table (table 128) is not requested in the initial calculation. Similarly, a comment will be printed if table 140 is disabled in the initial calculation.
4. PRINT Table 87 does not appear as a result of the standard 'default' convention because stopping powers for all 100 elements for each material results in large output files. To output Table 87, the user must specify 85 and 87 explicitly on the PRINT card.

## 5.13.3.1 Example 1

PRINT 110 40 150

The output file will contain the 'basic' tables plus tables 40, 110,
150, and the shortened version of 175, but not 55, 117, 118, 160, 161,
162, 210, 220 (the 'default' tables).

## 5.13.3.2 Example 2

```
PRINT -170 -70 -110
```

The output file will contain all the 'basic' tables, all the 'default'
tables, the long version of Table 175, and all the optional tables
applicable to your problem, except Tables 70, 110, and 170.

## 5.13.3.3 Example 3

PRINT -1 87

Prints all output including Table 87.

## 5.13.3.4 Table 10

All source variables defined explicitly or by default are printed. The
order of sampling of the source variables is also printed, which is
important for source variables that are dependent on other source
variables.

## 5.13.3.5 Table 43

Output of this table is controlled from within the LAHET Code System but
never enabled.

## 5.13.3.6 Table 50

A cell can be composed of physically separate regions or pieces joined
with the union operator. Improperly defined cells can be composed
unintentionally of more than one piece (for example, a surface is
extended unknowingly and forms a cell). If a cell is composed of more
than one piece, a warning message is given and one should verify that
the number of pieces is correct.

If the mass or volume of a geometry or parts of it are known, one should
compare the known volume or mass with what the MCNP code calculates to
verify the correctness of the geometry. The volumes, masses, and/or
surface areas that the MCNP code cannot calculate (but supplies a
placeholder value such as zero) do not affect the totals. Cell volumes
that are not calculated by the MCNP code can be entered on the VOL card.
Areas that are not calculated by the MCNP code can be entered on the
AREA card.

## 5.13.3.7 Table 60

This table summarizes cell properties. It includes values given in PRINT
Table 50 on density, volume, mass, and number of pieces. However, it
also includes the materials assigned to each cell (and whether they are
modified by an S ( α, β ) treatment shown as an s after the material
number) and the importance(s) assigned to the cell.

## 5.13.3.8 Table 70

The entries in this table are the surface coefficients used by the MCNP
code [§1.3.3.1] and are not necessarily the entries on the surface
cards.

## 5.13.3.9 Table 72

The cell temperature can be controlled using TMP or else a default value
is used ( 2 . 53 × 10 -8 MeV).

## 5.13.3.10 Table 85

The 'Density Effect Data' table contains the material data necessary to
correct the stopping power term for the polarization of the media. If a
fast electron passes through an equal areal density (mass density
multiplied by length) of two materials, it will lose more energy in a
sparse (rather than dense) material. This effect is small for heavier
particles, but for electrons with relativistic velocities transversing
dielectric media, it can be significant. For 1-MeV electrons in water,
this correction can be as large as 5%.

Next, the electron range and straggling table for each material is
listed. Electron energies are listed in in ascending order and gives the
respective stopping powers due to collision and radiation and the range
of the electron in the material. Radiation yield is the fraction of the
electron's kinetic energy that is converted into bremsstrahlung energy.

## 5.13.3.11 Table 86

The 'electron secondary production for. . . ' table contains a list of
electron energies in ascending order and gives the respective stopping
powers due to collision and radiation and the range of the secondary
electron created in the electron in the material.

## 5.13.3.12 Table 98

The physical constants and units used in the MCNP code are listed here.

The compilation options are also listed. Knowing how the code was
compiled is useful if it is slow, runs out of space, does not plot
(usually because the plot option is wrong for the computer being used or
run-time libraries for plotting are located somewhere other than
expected), or cannot find the data libraries (usually because of an
incorrect DATAPATH environment variable).

## 5.13.3.13 Table 100

The cross-section table list shows the nuclear and atomic data used in
the problem. For example, a c appended to the neutron data indicates
continuous energy, a d indicates discrete reaction data, a p indicates
photon data, and an e indicates electron data. A listing of data classes
is given in Table B.1.

Warnings are printed in MODE n p problems if the photon production cross
sections are unavailable or are in the less accurate equiprobable bin
format. Note that electron data may be loaded even though electrons are
not transported because the data may be used for the thick-target
bremsstrahlung model.

Any cross sections outside the energy range of the problem as specified
by the PHYS and CUT cards are deleted.

## 5.13.3.14 Table 110

This table gives starting information about the first 50 source
particles. The columns are as follows:

| nps       | the history number for the source particle,                             |
|-----------|-------------------------------------------------------------------------|
| x , y , z | the initial position of the source particle in ( x, y, z ) coordinates, |

| cell      | the cell ID of the region of space that the particle is started in or directed into,   |
|-----------|----------------------------------------------------------------------------------------|
| surf      | the surface the particle started on, if any,                                           |
| u , v , w | the initial direction of the source particle as Ω ≡ u i + v j + w k ,                  |
| energy    | the initial energy of the particle in MeV,                                             |
| weight    | the initial statistical weight of the particle, and                                    |
| time      | the initial (physical) time of the particle in shakes.                                 |

## 5.13.3.15 Table 126

This table provides cell-by-cell information on particle behaviors.

The tracks entering a cell refers to all tracks entering a cell,
including source particles. If a track leaves a cell and later reenters
that same cell, it is counted again. Tracks entering does not include
particles from the bank (from variance-reduction events at collisions or
physical events at collisions).

The population in a cell is the number of tracks entering a cell plus
source particles plus particles from the bank (from variance-reduction
or physical events at collisions). Population does not include reentrant
tracks. Comparing tracks entering and population for a given cell can
indicate the amount of back scattering in the problem. An often
successful approach for choosing importances is to select them so that
population is kept roughly constant in all cells between the source and
tally regions. Information, carried by histories through phase space,
cannot be regained once lost.

The number of collisions in a cell is important for detectors and
anything involving collision rate. A lack of collisions may indicate a
need to force them. This quantity is not normalized by cell volume. In
some problems, most of the computer time is spent modeling collisions.
Cells with excessive numbers of collisions are possibly oversampled in
this regard. This often happens when many thermal neutrons diffuse and
contribute little of significance to the problem solution. In such
cases, energy-dependent weight windows are most effective, followed by
energy roulette, exponential transform, analog capture, time cutoff,
and/or energy cutoff. Note that the last two methods may introduce a
bias into the problem. Subdividing the cell into smaller cells with
different importances is also effective.

The number of collisions times the weight of the particles having the
collisions is an indication of how important the collisions were.

The number-weighted energy in a cell is computed as

<!-- formula-not-decoded -->

where E is energy, t is time, n = T l /v is the number density of the
particles, T l is distance to next event (i.e., the track length), v is
particle velocity, and w is particle statistical weight. The number-
weighted energy can be useful to understand what energy is dominating a
cell, and if low and unlikely to contribute significantly later, whether
an energy-controlling variance-reduction technique may be useful.

Similarly, the flux-weighted energy in a cell is computed as

<!-- formula-not-decoded -->

It is difficult, and perhaps meaningless, to determine an average energy
in this way because a large spectrum involving several orders of
magnitude is frequently encountered leading to the problem of
representing this

spectrum by one number. That is why an average energy has been
calculated using two methods. If the number-weighted energy is
significantly lower than the flux-weighted energy, it indicates a large
number of low-energy particles with large track time (large T l /v ). As
the energy cutoff is raised, these two weighted energies agree more
closely. Note that the two average energies are identical for constant
velocity photons.

The relative average track weight is computed as

<!-- formula-not-decoded -->

where I c is the importance of the cell under consideration. By making
the average track weight relative to the cell importance, the weight
reduction from importance splitting is removed. For most problems with
consistently assigned cell importances and a source-cell importance of
one, the average track weight is constant from cell to cell and
significant deviations indicate a poor importance function. With weight
windows, the average track weight should be within the weight window
bounds.

The average flux-weighted track mean-free path is computed as

<!-- formula-not-decoded -->

where Σ t is the total macroscopic cross section for the material in the
cell under consideration. The mean-free path is strongly dependent upon
energy, so this average mean-free path may be meaningless. However, an
approach for developing cell-based importances is that importances
should double approximately every mean free path. This is usually a poor
rule, but it is sometimes better than nothing. The average-track mean-
free path is thus useful for making (potentially poor) guesses at cell
importances. It is also useful for determining the fictitious sphere
surrounding point detectors [§5.9.1.2], the outer radius of DXTRAN
spheres [§5.12.10], exponential transform stretching parameters
[§5.12.7], the necessity of forced collisions [§5.12.9], etc.
Occasionally this quantity may even provide physical insight into the
problem.

## 5.13.3.16 Table 130

The tables listed show all possible ways a particle's weight may be
changed in each cell based on external, variance-reduction, and physical
events. In addition to itemizing what is happening to particles and
where, this information can be useful in debugging a problem.

Note that there may be apparent weight discrepancy between PRINT Table
126 and 130, but this is because Table 126 concerns tracks while Table
130 concerns histories. Furthermore, in Table 126 the weight is
relative, whereas it is absolute in Table 130. If the average track
weight is multiplied by the tracks entering cell and then divided by
both the number of source particles and the importance ratio, the two
weights are in close agreement. The overall value of ν in a problem with
fissionable material can be obtained by taking the ratio of fission
neutrons to fission loss in Table 130

## 5.13.3.17 Table 140

The activity of each nuclide per source particle in each cell can tell
one how important various nuclides, such as trace elements, are to the
problem and may aid in selecting cross-section libraries when memory is
limited.

Neutron-induced photon production is also listed for MODE n p problems.
Totals are also given for activity per source particle summed over all
cells in the problem and photoatomic nuclide activity per source
particle summed over all cells in the problem, as applicable.

If applicable, another set of information is provided for how many
photons were produced in each cell and the energy spectrum of the
photons averaged over the problem. Because photons are produced only at
neutron collisions in certain calculations, there is a correlation
between the number of collisions in a cell, the PWT card, and this
output. The earlier output showing the photon activity for the problem
includes isotope-dependent neutron-induced photon-production
information.

## 5.13.3.18 Table 161

This plot is the unnormalized empirical history score probability
density for the tally fluctuation chart bin of the tally under
consideration. The probability density is the number of history scores
(horizontal) plotted against the value of the score (vertical). The
nonzero mean is denoted by the horizontal line of m s. If a problem has
been undersampled, this plot will often show 'holes,' or unsampled
regions of the PDF for relatively high scores. If the slope is less than
10, this plot will also show a curve of s s, which represent the Pareto
curve fit to the PDF at the high scores. This allows the user to
visually compare the fit of the high-weight tally scores to the
calculated distribution.

## 5.13.3.19 Table 162

The first plot is the cumulative number of scores in the tally
fluctuation chart bin of tally under consideration. It is the cumulative
version of PRINT Table 161; i.e., the cumulative probability density
function. The ordinate and abscissa values are printed in the left-hand
columns. A plot then follows that gives the unnormalized cumulative
scores in the tally fluctuation chart bin.

## 5.13.3.20 Table 175

The a minimal set of output is produced that indicates how k eff
iteration is proceeding by cycle if full or optional output of this
table or PRINT Table 179 is not selected. If selected, then a detailed
listing showing seven different estimates of k eff and removal lifetimes
are given versus cycle.

## 5.13.3.21 Table 190

This table lists the lower weight-window bounds generated by the
stochastic weight-window generator [§2.7.2.12.2] using the WWG card.

## 5.13.3.22 Table 199

This table gives a listing of tracks by cell in constant-scaled weight
windows relative to the cell-wise weightwindow lower bound value. The
intent of this table is to communicate the number of tracks above the
local weight window, and by how much, to inform whether the weight
window should be scaled up or otherwise adapted to reduce the frequency
of particle splitting.

Note that this table is only produced if specifically requested using
the PRINT card, e.g., as PRINT 199 .

## 5.13.3.23 Table 200

This table provides weight-window input cards (e.g., WWP and WWN cards)
that can, with some text editing, be used instead of the IMP cards in
subsequent calculations.

Necessary edits may include replacing zero-valued weight-window lower
bounds with a good guess and/or adjusting weight-window lower bounds
that differing significantly from those in neighboring cells. Output is
also given that indicates weight-window lower-bound ratios between
adjacent cells to simplify the aforementioned edits.

## 5.13.4 TALNP: Negate Printing of Tallies

Controls the printing of bin prints for specified tally numbers.

Data-card Form: TALNP t 1 t 2 . . . t i List of tally numbers to be
excluded from output file ( 1 ). If there are no t i entries, then turn
off the bin prints for all tallies in the problem. If there are t i
entries, then turn off the bin prints for the tally numbers that are
listed.

Default: If card is present without entries, then no bin prints are
provided for tallies. If card is absent, bin prints are provided for all
tallies.

## Details:

- 1 If, after the calculation is completed, one would like to see these numbers, the printing of the bin values can be restored with the TALNP card in an MCNP input file used in a restarted calculation. To accomplish this, the tally numbers t i must be entered on the TALNP card as negative numbers. A single entry of zero in a restarted-calculation input file restores the prints of all tally bins.

## 5.13.5 PRDMP: Print and Dump Cycle

The PRDMP card allows the user to control the interval at which tallies
are printed to the MCNP output file and information is dumped to the
runtape file.

For this card, many options have dual meanings, one for a purely
history-based simulation, and one for a batch ( NPS with n \_ per \_ batch
set and a batch-based tally enabled) or cycle ( KCODE ) based
simulation.

Data-card Form: PRDMP ndp ndm mct ndmp dmmp ndp Increment for printing
tallies. An 8-byte integer is permitted for ndp . If ndp &gt; 0 the problem
summary and tallies are printed to the output file after every ndp
histories (or cycles for a KCODE or batch-based problem) ( 1 ).

|      | ndp < 0                                                                                                                                    | the problem summary and tallies are printed to the output file after every ndp minutes of computer time.                                                                                                                                                                                                                    |
|------|--------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ndm  | Increment for dumping to the runtape file. An 8-byte integer is permitted for ndm .                                                        | Increment for dumping to the runtape file. An 8-byte integer is permitted for ndm .                                                                                                                                                                                                                                         |
|      | ndm > 0                                                                                                                                    | a dump is written to the runtape file after every ndm histories (or cycles for a KCODE or batch-based problem) ( 1 ).                                                                                                                                                                                                       |
|      | ndm < 0                                                                                                                                    | a dump is written to the runtape file after every ndm minutes of computer time.                                                                                                                                                                                                                                             |
| mct  | Controls printing of MCTAL file ( 2 ). If                                                                                                  | Controls printing of MCTAL file ( 2 ). If                                                                                                                                                                                                                                                                                   |
|      | mct > 0                                                                                                                                    | write MCTAL file at problem completion.                                                                                                                                                                                                                                                                                     |
|      | mct = 0                                                                                                                                    | do not write MCTAL file.                                                                                                                                                                                                                                                                                                    |
|      | mct = - 1                                                                                                                                  | MCTAL file is written at problem completion, but references to code name, version number, problem ID, figure of merit, and anything else having to do with running time are omitted from MCTAL and MCNP output file. This ensures tracking runs (using identical random walks) yield identical MCTAL and MCNP output files. |
|      | mct = - 2                                                                                                                                  | MCTAL file is written at problem completion, but additional prints in MCNP output file are turned off to assist in comparing multitasking output.                                                                                                                                                                           |
| ndmp | Maximum number of dumps on the runtape file ( 3 ).                                                                                         | Maximum number of dumps on the runtape file ( 3 ).                                                                                                                                                                                                                                                                          |
| dmmp | Controls how frequently tally fluctuation chart (TFC) entries and rendezvous occur ( 4 , 5 ). An 8-byte integer is permitted for dmmp . If | Controls how frequently tally fluctuation chart (TFC) entries and rendezvous occur ( 4 , 5 ). An 8-byte integer is permitted for dmmp . If                                                                                                                                                                                  |
|      | dmmp < 0                                                                                                                                   | write charts every 1000 particles for non- KCODE , non-batch problems or every | dmmp | cycles for KCODE or batch-based problems.                                                                                                                                                                                           |
|      | dmmp = 0                                                                                                                                   | write charts every 1000 particles or, if multiprocessing, 10 times total during the calculation.                                                                                                                                                                                                                            |
|      | dmmp > 0                                                                                                                                   | write charts every dmmp particles for non- KCODE , non-batch problems or every | dmmp | cycles for KCODE or batch-based problems.                                                                                                                                                                                           |

Default: Print only after the calculation has successfully ended. Dump
to the runtape every 60 minutes and at the end of the problem. Do not
write a MCTAL file. Write all dumps to the runtape file. Write charts
and rendezvous for fixed-source problems every 1000 particles or, if
multiprocessing, 10 times total during the calculation ( dmmp=0 ); for
KCODE or batch-based problems, write charts and rendezvous at the end of
each cycle.

Use: Recommended, especially for complex problems. For multiprocessor
problems, it is recommended that the ndp , ndm , and dmmp entries be
provided in number of histories.

## Details:

- 1 If ndp or ndm is set to time in a parallel calculation, it will be time used by one processor, approximately elapsed wall time. The scheduled print or dump will be delayed to the next rendezvous or cycle to assure consistent data. For parallel (i.e., multiprocessor) calculations, is highly recommended that the ndp and ndm values be set in terms of particles or cycles, instead of minutes,
- 2 The MCTAL file is an ASCII file of tallies that can be subsequently plotted with the MCNP6 MCPLOT capability. The MCTAL file is also a convenient way to store tally information in a format that is stable for use in the user's own auxiliary programs. For example, if the user is on a system that cannot use the MCNP6 MCPLOT option, the MCTAL file can be manipulated into whatever format is required by the user's own local plotting algorithms.
- 3 Using the parameter ndmp , the PRDMP card allows the user to control the size of the runtape file. The runtape file will contain the last ndmp dumps that were written. For example, if ndmp =4 , after dump 20 is written only dumps 17, 18, 19, and 20 will be on the runtape file. In all cases, the fixed data and cross-section data at the front of the runtape file are preserved.
- 4 The fifth entry dmmp has several possible meanings. For sequential nonKCODE non-batch MCNP6, a value of dmmp ≤ 0 results in TFC entries every 1000 particles initially. This value doubles to 2000 after 20 TFC entries. A positive value of dmmp produces TFC entries every dmmp particles initially. For nonKCODE non-batch distributed memory multiprocessing, dmmp &lt; 0 produces TFC entries and task rendezvous every 1000 particles initially, the same as does the sequential version. The default value, dmmp = 0 , produces ten TFC entries and task rendezvous, rounded to the nearest 1000 particles, based on other cutoffs such as NPS , CTME , etc. This selection optimizes speedup in conjunction with TFC entries. If detectors/DXTRAN are used with default Russian roulette criteria ( DD card default), the dmmp = 0 entry is changed by MCNP6 to dmmp &lt; 0 , ensuring tracking with the sequential version (i.e., TFC entries and rendezvous every 1000 particles). As with the sequential nonKCODE non-batch version, dmmp &gt; 0 produces TFC entries and task rendezvous every dmmp particles, even with detectors/DXTRAN with default Russian roulette criteria. Setting dmmp to a large positive number minimizes communication time and maximizes speedup. However, the TFC may not have many entries, possibly only one, if dmmp = npp .
- 5 The rendezvous frequency of a multiprocessor calculation is the minimum interval of parameters or ndp , ndm , and dmmp .

## 5.13.6 PTRAC: Particle Track Output

The PTRAC card generates an output file of user-filtered particle events
referred to as a particle track file. Adding a FILE = HDF5 entry will
produce an HDF5 output file [Appendix D.3], but the raw binary format (
FILE = BIN ) is the default for backward compatibility in this release
[DEP-53382]. The HDF5 output file is easier to post process and allows
for parallel execution with MPI, tasks, or both, as detailed in
§5.13.6.1. The default file name ptrac (or ptrac.h5 ) can be changed on
the execution line or within the message block.

Use of one or more card keywords will reduce the particle track file
size significantly. The card keywords are organized into three
categories: output-control keywords, event-filter keywords, and history-
filters keywords. The output-control keywords provide user control of
the output file and I/O. The event-filter keywords filter particle
events on an event-by-event basis, i.e., only events that meet all
event-filter criteria are written to the output file. The history-filter
keywords will filter all particle events for a particular history. That
is, if the entire history meets the filter criteria, all filtered events
for that history are written to file. Restarted calculations that
utilize the PTRAC feature will not change the results in the original
particle track output file and cannot be used to generate additional
PTRAC card results, but other aspects of the simulation will be
completed. Simulations with unique random number seeds (5.13.2) can be
used to generate separate files that can be processed as unique
histories if required.

The output formats for PTRAC and event logs limit the printing of cell,
surface, and material numbers to a maximum of five characters. Users
intending to use the PTRAC card with the ASCII format or event logs
should avoid the use of cell, surface, or material numbers greater than
99,999.

## /\_445 Deprecation Notice

DEP-53382

The FILE keyword options ASC , AOV , BIN , and BOV for the PTRAC card
are deprecated, and the HDF5 option should be preferred. The MAX ,
BUFFER , and WRITE keywords are also deprecated, as they are unused by
the HDF5 option. The ICL and JSU event filter options are deprecated, as
they are replaced with the simpler SUR and CEL event filter options for
HDF5 outputs.

## /\_445 Deprecation Notice

DEP-53383

The COINC keyword and the EVENT=CAP options for the PTRAC card are
deprecated. There is no current plan to support these features with the
HDF5 format in future releases. People interested in continuing to use
these features should send an email to mcnp\_help@lanl.gov.

glyph[negationslash]

| Data-card Form: PTRAC   | keyword=value(s)...                                                                                                                                                                                                                                                        | keyword=value(s)...                                                                                                                                                                                                                                                        |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Output Control Keywords | Output Control Keywords                                                                                                                                                                                                                                                    | Output Control Keywords                                                                                                                                                                                                                                                    |
| BUFFER                  | Except for FILE = HDF5 , determines the amount of storage available for filtered events within each history . Single integer entry. (DEFAULT: BUFFER = 100 ) Restriction: BUFFER > 0 .                                                                                     | Except for FILE = HDF5 , determines the amount of storage available for filtered events within each history . Single integer entry. (DEFAULT: BUFFER = 100 ) Restriction: BUFFER > 0 .                                                                                     |
| FILE                    | Controls file type [DEP-53382]. If                                                                                                                                                                                                                                         | Controls file type [DEP-53382]. If                                                                                                                                                                                                                                         |
|                         | FILE = HDF5                                                                                                                                                                                                                                                                | generates an HDF5 output file (recommended).                                                                                                                                                                                                                               |
|                         | FILE = ASC                                                                                                                                                                                                                                                                 | generates an ASCII output file.                                                                                                                                                                                                                                            |
|                         | FILE = BIN                                                                                                                                                                                                                                                                 | generates a binary output file. (DEFAULT)                                                                                                                                                                                                                                  |
|                         | FILE = AOV                                                                                                                                                                                                                                                                 | generates an ASCII output file by overwriting an existing ASCII particle track file to a named pipe on UNIX systems. Requires a particle track file to exist prior to execution.                                                                                           |
|                         | FILE = BOV                                                                                                                                                                                                                                                                 | generates a binary output file by overwriting an existing binary particle track file to a named pipe on UNIX systems. Requires a particle track file to exist prior to execution.                                                                                          |
| FLUSHNPS                | Controls write frequency for HDF5 output file type. Single integer entry. Restriction: FLUSHNPS > 0 . For non- KCODE simulations ( 3 ), events will be written to the HDF5 particle track file at least every FLUSHNPS histories. See §5.13.6.2 for guidance.              | Controls write frequency for HDF5 output file type. Single integer entry. Restriction: FLUSHNPS > 0 . For non- KCODE simulations ( 3 ), events will be written to the HDF5 particle track file at least every FLUSHNPS histories. See §5.13.6.2 for guidance.              |
| MAX                     | Sets the maximum number of events to write to the particle track file. If FILE = HDF5 , this entry is ignored. Single integer entry. (DEFAULT: MAX = 10000 ) Restrictions: MAX = 0 . The value of | MAX | will be truncated to 2 31 - 1 if it is larger than 2 31 - 1 . If | Sets the maximum number of events to write to the particle track file. If FILE = HDF5 , this entry is ignored. Single integer entry. (DEFAULT: MAX = 10000 ) Restrictions: MAX = 0 . The value of | MAX | will be truncated to 2 31 - 1 if it is larger than 2 31 - 1 . If |
|                         | MAX > 0                                                                                                                                                                                                                                                                    | write MAX events to the particle track file.                                                                                                                                                                                                                               |
|                         | MAX < 0                                                                                                                                                                                                                                                                    | MCNP6 is terminated when | MAX | events have been written to the particle track file.                                                                                                                                                                                      |

MEPH

WRITE

COINC

Determines the maximum number of events per history to write to the

Restriction:

particle track file. Single integer entry. (DEFAULT: write all events)

MEPH

&gt;

0

Controls what particle parameters are written to the particle track
file.

FILE

If

WRITE

WRITE

=

=

=

HDF5

, all parameters are always written.

POS

ALL

1

Otherwise, if write only the

(

x, y, z

)

related cell and material numbers. (DEFAULT)

write the

(

x, y, z

)

related cell and material numbers and the and time.

(

)

location of the particle with location of the particle with

(

u, v, w

)

direction cosines, as well as particle energy, weight,

Activates a particle track file format specifically for coincidence
tally scoring

TALLY

[DEP-53383]. Used in conjunction with

COINC

COINC

=

=

COL

LIN

keyword. (

4

) If a full printing of all specified tally scores is

output is column-based. (DEFAULT)

produced, even if the tally scores were zero. The tally score pairs are
printed for non-zero scores only.

## Event Filter Keywords

| EVENT   | Specifies the type of events written to the particle track file. Up to six mnemonic entries can be specified. (DEFAULT: write all events) If                                                                                                                                                                                                                                                                                                                                                                                                                                          | Specifies the type of events written to the particle track file. Up to six mnemonic entries can be specified. (DEFAULT: write all events) If                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|         | EVENT = SRC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | write initial source events.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|         | EVENT = BNK                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | write bank events. These include secondary sources (e.g., photons produced by neutrons, as well as particles created by variance-reduction techniques such as DXTRAN and energy splitting). See Appendix D.3 for a complete list and more details on bank events.                                                                                                                                                                                                                                                                                                                     |
|         | EVENT = SUR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | write surface events.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|         | EVENT = COL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | write collision events.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|         | EVENT = TER                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | write termination events.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|         | EVENT = CAP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | write coincident capture events [DEP-53383]. ( 5 )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| FILTER  | Specifies additional MCNP6 variables for filtering each event ( 2 ). The parameter values consist of one or two numerical entries and a variable mnemonic that corresponds to a variable in the PBL derived structure or other related quantities. See Table 5.28 for available mnemonics. A single numerical entry requires an exact value; two numerical entries represent a range. When a range is specified, the first entry must be less than or equal to the second. Multiple sets of numerical entries and mnemonics are allowed. (DEFAULT: no additional filtering) Examples: | Specifies additional MCNP6 variables for filtering each event ( 2 ). The parameter values consist of one or two numerical entries and a variable mnemonic that corresponds to a variable in the PBL derived structure or other related quantities. See Table 5.28 for available mnemonics. A single numerical entry requires an exact value; two numerical entries represent a range. When a range is specified, the first entry must be less than or equal to the second. Multiple sets of numerical entries and mnemonics are allowed. (DEFAULT: no additional filtering) Examples: |

- FILTER=2,ICL writes only those events that occur in cell 2.

- FILTER=0,10,X writes only those events in which the particle's x coordinate is between 0 and 10 cm.
- FILTER=0.0,10.0,X 0,1,U 1.0,2,ERG writes only those events in which the particle's x coordinate is between 0 and 10 cm and the particle's x -axis cosine is between 0 and 1 and the particle's energy is between 1 and 2 MeV.

## TYPE

Filters events based on one or more particle types. (DEFAULT: Write
events for all particles.) May specify filtering of a single particle or
multiple particles, where &lt; pl i &gt; is a particle identifier specified in
Table 4.3: TYPE= &lt; pl 1 &gt; , &lt; pl 2 &gt; , . . .

## History Filter Keywords

## NPS

Sets the range of particle histories for which events will be output. A
single value produces filtered events only for the specified history.
Two entries indicate a range and will produce filtered events for all
histories within that range. The first entry must be less than or equal
to the second. (DEFAULT: Events for all histories) Note: An 8-byte
integer is permitted for keyword NPS . Restriction: NPS &gt; 0 . Examples:

- NPS=10 write events only for particle number 10.
- NPS=10,20 writes events for particles 10 through 20.

## CELL

List of cell numbers to be used for filtering histories. If any track
enters a listed cell(s), all filtered events for the history are written
to the particle track file. Note: Number of entries is unlimited
Restriction: CELL &gt; 0 . (DEFAULT: No filtering based on cell entrance.)
Example:

- CELL=1,2 writes all filtered events for those histories that enter cell 1 or 2.

glyph[negationslash]

| SURFACE   | List of surface numbers to be used for filtering histories. If any track crosses a listed surface(s), all filtered events for the history are written to the particle track file. Note: Number of entries is unlimited. Restriction: SURFACE > 0 . (DEFAULT: No filtering based on surface crossing.)                                                                                                                                                                                                                                                                          |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TALLY     | List of tally numbers to be used for filtering histories. If any track contributes to the TFC bin of listed tallies, all filtered events for the history are written to the particle track file. (See the TF n card for specification of the TFC bin for tally n .) Note: A negative TALLY entry indicates that the corresponding VALUE entry is a multiplier rather than an absolute value. Number of entries is unlimited. Restriction: TALLY = 0 . Only positive VALUE entries are allowed when FILE = HDF5 . (DEFAULT: No filtering based on tally contribution.) Example: |

- TALLY=4 writes all filtered events for those histories that contribute to tally 4. (See VALUE keyword for control of filter criteria.)

## VALUE

Specifies the tally cutoff above which history events will be written.
The number of entries must equal the number of entries on the TALLY
keyword. A negative TALLY value indicates that the corresponding VALUE
entry is a multiplier ( 6 ). (DEFAULT: VALUE = 0 . 0 for each tally
associated with the TALLY keyword). Examples:

- TALLY=4 VALUE=2.0 writes all filtered events of any history that contributes 2.0 or more to the TFC bin of tally 4.
- TALLY=-4 VALUE=2.0 writes all filtered events of any history that contributes more than 2 . 0 × T a to tally 4, where T a is the average tally of the TFC bin. The values for T a are updated every dmmp histories (see the PRDMP card).
- TALLY=4 VALUE=0.0 writes all filtered events of every history that scores to tally 4.

Default: Using the PTRAC card without any keywords causes all particle
events to be written to the particle track output file. Caution: If all
particle events are written to the particle track file, an extremely
large file likely will be created unless NPS is small.

Use: Optional.

## Details:

- 1 For the HDF5 particle track file there is a single format, so the WRITE keyword is ignored.
- 2 For FILE = BIN and FILE = ASC , event-based filters specified with the FILTER keyword are not applied to BNK events. For FILE = HDF5 , BNK events are subject to filters listed on the FILTER entry.
- 3 For FILE = HDF5 and KCODE simulations, the FLUSHNPS keyword is not required. Data is written to the particle track file at the end of each cycle.
- 4 The COINC feature only supports the TALLY and VALUE keywords as filter options. When used in conjunction with the COINC keyword, TALLY entries must be positive. The existing VALUE keyword can be used to set threshold scores for the tallies itemized on the TALLY keyword. All scores below that threshold are treated as zero. The COINC keyword will force ASCII file output format ( FILE = ASC or FILE = AOV ).
- 5 For EVENT = CAP , most of the standard PTRAC capabilities are bypassed (for speed) and the data written to each line (or record) of the particle track file are very different from the usual event data. For binary files, the entries on each PTRAC line include the particle history number (' NPS '), the time from source event to analog capture in any FT8 CAP tally ('Time'), and the cell number in which the analog capture occurred ('Cell'). Additionally, for ASCII files, a fourth column, 'Source,' provides the source particle number of a given history. The 5th column of output provides the target identifier of the spontaneous fission nuclide. A value of 0 appears if the source is not spontaneous fission, i.e., PAR = SF . The 6th column contains the target identifier [§1.2.2] of the first induced fission; the 7th, that of the second induced fission; the 8th, that of the third induced fission; and the 9th, that of the last fission before capture, either induced or spontaneous.
- 6 Filtering based on the T a values will occur only when they become non-zero. Thus, when using a multiplier, PTRAC events may not be written for several thousand particles, or at all, if scores are seldom or never made to the TFC bin of the specified tally. In most cases, it is best to enter an absolute value.

Table 5.28: Mnemonic Values for the FILTER Keyword

| Mnemonic   | MCNP6 Variable          | Description                                                 |
|------------|-------------------------|-------------------------------------------------------------|
| X          | pbl%r%x                 | x coordinate of particle position (cm)                      |
| Y          | pbl%r%y                 | y coordinate of particle position (cm)                      |
| Z          | pbl%r%z                 | z coordinate of particle position (cm)                      |
| U          | pbl%r%u                 | Particle x axis direction cosine                            |
| V          | pbl%r%v                 | Particle y axis direction cosine                            |
| W          | pbl%r%w                 | Particle z axis direction cosine                            |
| ERG        | pbl%r%erg               | Particle energy (MeV)                                       |
| WGT        | pbl%r%wgt               | Particle weight                                             |
| TME        | pbl%r%tme               | Time at the particle position (shakes)                      |
| VEL        | pbl%r%vel               | Speed of the particle (cm/shake)                            |
| IMP1       | pbl%r%fiml(1)           | Neutron cell importance                                     |
| IMP2       | pbl%r%fiml(2)           | Photon cell importance                                      |
| IMP3       | pbl%r%fiml(3)           | Electron cell importance                                    |
| SPARE1     | pbl%r%spare(1)          | Spare banked variable                                       |
| SPARE2     | pbl%r%spare(2)          | Spare banked variable                                       |
| SPARE3     | pbl%r%spare(3)          | Spare banked variable                                       |
| ICL        | pbl%i%icl               | Problem number of current cell ( 7 )                        |
| CEL        | ncl(pbl%i%icl)          | User specified number of current cell ( 7 )                 |
| JSU        | pbl%i%jsu               | Problem number of current surface ( 7 )                     |
| SUR        | nsf(pbl%i%icl) + 0.1kfq | User specified number of current surface or macrobody ( 7 ) |
| IDX        | pbl%i%idx               | Number of current DXTRAN sphere                             |
| NCP        | pbl%i%ncp               | Count of collisions for current branch                      |
| LEV        | pbl%i%lev               | Geometry level of particle location                         |
| III        | pbl%i%iii               | 1st lattice index of particle location                      |
| JJJ        | pbl%i%jjj               | 2nd lattice index of particle location                      |
| KKK        | pbl%i%kkk               | 3rd lattice index of particle location                      |

- 7 The filter options for ICL and JSU are the program numbers stored by the MCNP6 program and are numbered by the order the cells and surface appear in the input file, respectively; these options are not allowed if FILE = HDF5 . The options for CEL and SUR are the numbers specified by the user in the input file; these options are only allowed with FILE = HDF5 .

The particle track file will contain the heavy ion particles and their
track information, but not individual heavy ion identities.

## 5.13.6.1 Using PTRAC with Parallel Execution

The HDF5 particle track format can be used with MPI parallelism and
shared-memory parallelism (i.e., the tasks command line option), both
independently and combined. The use of the PTRAC card with multiple MPI
processes requires an MPI-parallel HDF5 installation. Check the MCNP6
build documentation for recommended MPI implementations and versions to
avoid past bugs in the parallel writing features. The tasks option can
be used with any MCNP installation and does not require an MPI
installation.

For optimal performance, the MPI-parallel HDF5 library is intended to be
used on a distributed parallel file system, e.g., a Lustre file system.
Local file systems typically provide acceptable performance as well.

## /warning\_sign Caution

Some network file systems (e.g., NFS) are not compatible with parallel
access and MPI-parallel PTRAC simulations may take a long time to write
and close the file. When using multiple MPI worker processes, it is
recommended to run a simulation with a small value of NPS and ensure
that the simulation is completed and the file written successfully. If
parallel writing is unsuccessful or inefficient for the available file
systems, then the tasks option can be used to achieve parallel
performance, which does not require an MPI-parallel HDF5 distribution or
parallel file system.

When a simulation is performed with tasks greater than 1, there is no
guarantee of the order histories will be written to the output file;
events within a history are always ordered correctly. Because histories
are statistically independent, the history ordering only concerns users
interested in a particular NPS value or in reproducing the exact history
order of an equivalent serial simulation. To reproduce the order of a
serial simulation, the entries in the RecordLog dataset should be sorted
by NPS (i.e., the unique history identifier) with the order of events
within each history preserved [Appendix D.3].

## 5.13.6.2 Guidance for the FLUSHNPS keyword

An important difference from FILE=BIN and FILE=ASC is that HDF5 PTRAC
simulations will buffer event data into memory across multiple histories
and only periodically write to a file, which improves performance. Users
must specify how often the data is written through the FLUSHNPS keyword
if FILE = HDF5 . The buffered data will be written to the output file
and buffers emptied at least every FLUSHNPS histories. If the value is
set too low, then the cost of writing and (optionally) MPI communication
becomes expensive. However, if the value is set too high, memory access
can become slower and the simulation may crash if it runs out of memory.
If the simulation crashes due to an out of memory error, it will print a
message to the terminal that an instance of a ' std::bad \_ alloc ' error
has occurred, followed by additional errors resulting from the
simulation crashing.

To help choose a value for FLUSHNPS , after the first write to the
particle track file during the simulation, an estimate of the peak
memory usage for all MPI processes and shared-memory tasks is printed to
the screen. Data is written to the particle track file at every
rendezvous, including those that can be controlled

1

1

by the PRDMP card, so the peak memory estimate may be written at a value
of NPS that is less than the FLUSHNPS value. For typical simulations and
computer systems currently available, a peak memory usage of 1000 MB
between writes provides a sufficient balance of performance and safety.
As a general rule, try setting a value of FLUSHNPS=1E05 and running a
short test simulation. If the printed peak memory usage is less than
1000 MB, then the FLUSHNPS number is sufficiently low for typical
simulations. Scaling the FLUSHNPS value to use 1000 MB or larger between
writes may increase performance. When in doubt, prefer a smaller value
of FLUSHNPS to avoid ' std::bad \_ alloc ' errors later in the
simulation.

An optimal value of FLUSHNPS depends on many parameters, including the
problem (in particular, the amount of memory used by material and
geometry data), the number of filters active, and the volatile memory
available on the system. As an example of fine-tuning performance, a
simulation with EVENT = SRC can set a value of FLUSHNPS = 5E06 and use
less than 1000 MB between writes. For a neutron simulation of a bare 5
cm sphere of 2.25 g/cm 3 graphite that writes all events from all
histories, a value of FLUSHNPS = 1E06 will use about 1000 MB between
writes. Some problems that write all events with extreme amounts of
particle splitting, multiplication, surface crossings, or collisions,
will require setting a much lower value, such as FLUSHNPS = 1000 or
lower to avoid crashing. In such cases, it is preferable to try to add
additional filtering to reduce the amount of memory used when possible.
The memory usage by particle track buffers between writes is mostly
independent of the number of MPI ranks and shared-memory tasks , for a
particular value of FLUSHNPS . However, using less MPI ranks than
available computational cores on a system reduces the memory used by
geometry and cross section data, which can allow for larger values of
FLUSHNPS and more efficient particle track simulations.

## 5.13.6.3 Example 1

PTRAC FILE=HDF5 EVENT=SUR,COL TYPE=N,P FLUSHNPS=1E05

This input line will generate an HDF5 particle track output file that
contains all surface and collision events that occurred during the
simulation, for photons and electrons. Data is flushed to the output
file at least every 100,000 histories.

## 5.13.6.4 Example 2

PTRAC FILTER=8,9,ERG EVENT=SUR NPS=1,50 TYPE=E CELL=3,4

When multiple keywords are entered on the PTRAC card, the filter
criteria for each keyword must be satisfied to obtain an output event.
This input line will write only surface crossing events for 8-9-MeV
electrons generated by histories 1-50 that have entered cells 3 or 4.

## 5.13.7 MPLOT: Plot Tally While Problem is Running

The MPLOT card specifies a plot of intermediate tally results that is to
be produced periodically during the calculation.

## Data-card Form: MPLOT keyword = value(s) ...

The entries on the MPLOT card are MCPLOT commands [§6.2.4.1] for one
picture.

Default: None.

Use: Optional. The specification of 8-byte integer values is allowed for
FREQ.

During the calculation, as determined by the FREQ n keyword entry, MCRUN
will call MCPLOT to display the current status of one or more of the
tallies in the problem. If a FREQ n command is not included on the MPLOT
card, n will be set to 5000. The following MCPLOT commands cannot appear
on the MPLOT card: RMCTAL , RUNTPE , DUMP , and END . All of the
commands on the MPLOT card are executed for each displayed picture, so
coplots of more than one bin or tally are possible. No output is sent to
a COMOUT file. MCPLOT will not take plot requests from the terminal; it
returns to MCRUN after each plot is displayed. See §6.3.3 for a complete
list of MCPLOT commands available.

A second way to plot intermediate tally results is to use the TTY
interrupt Ctrl + c MCPLOT or Ctrl + c , m that allows interactive
plotting during the calculation. At the end of the history that is
running when the interrupt occurs, MCRUN will call MCPLOT, which will
take plot requests from the terminal. No output is sent to the COMOUT
file. The following commands can not be used: RMCTAL , RUNTPE , DUMP ,
and END .

## 5.13.8 HISTP: Create LAHET-compatible Files

The results of particle transport, and medium- and high-energy physics
interactions from within the LAHET Code System are available through the
LAHET-compatible histp files using the HISTP card in the MCNP input
file. This card controls the writing of information to an external histp
file useful for analysis by the HTAPE3X program distributed with MCNPX
or the HTAPE6 source code distributed with the MCNP6.2 source code.

## /warning\_sign Caution

The HTAPE6 utility code is no longer supported and is thus no longer
distributed with current or future versions of the MCNP6 code.
Furthermore, the HISTP card will be marked for deprecation in a future
version of the MCNP6 code once a suitable alternative capability is
available that provides equivalent history information to that
encapsulated within the histp file. People interested in continuing to
use either the MCNP-generated histp files or the HTAPE6 utility, or
would like to provide input to the development team on the future
direction of the replacement capabilities, should contact the
development team by sending an email to mcnp\_help@lanl.gov.

## Data-card Form: HISTP icl 1 . . . icl K

icl K

List of cell numbers. Only events occurring within these cells will be
written to the histp file. If no icl K values are provided, all events
will be written. Negative values are unused.

Default: All events in all cells written to the histp file.

Use: Optional.

## Limitations:

- No heavy ion transport information is written to the histp file aside from the usual recoils from which the heavy ions are started.
- Writing histp files during multiprocessing is unavailable.

1

## 5.13.8.0.1 Example

histp 11

The histp file will contain only events within cell 11.

## 5.13.9 PIO: Enable Parallel IO

| Data-card Form: PIO value   | Data-card Form: PIO value                                                                                                                     |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| value                       | If                                                                                                                                            |
|                             | value = bl ank or ON , the code is built with parallel HDF5 support, and is run with MPI, features that have parallel IO support will use it. |
|                             | value = NO , then parallel IO is disabled. (DEFAULT)                                                                                          |

Default: NO . This option is not saved in the runtape. It must be
specifically enabled for all runs, continue or otherwise.

Use: Certain components of the code (such as FMESH with the XDMF output
format) can write results using parallel HDF5. This can be extremely
useful on parallel file systems when writing very large results arrays.
Enabling this feature will perform input and output in parallel in these
circumstances.

This feature is not enabled by default as not all file systems will
benefit from parallel IO. Some file systems will even cause the MCNP
code to lock up if parallel IO is used. In testing, NFS partitions would
often cause this. As a result, one should test file systems with short
simulations to see if this will work and provide a benefit to a
simulation before running a large problem.

## 5.13.10 READ: Auxiliary Input File and Encryption

The MCNP6 READ card enables

1. the reading of parts of the input file from other (auxiliary) files,
2. the suppression of the printing of the auxiliary input files to shorten output files and protect proprietary information, and
3. the encryption of auxiliary input files to protect proprietary information.

Unlike most MCNP6 input cards, there may be as many READ cards and
auxiliary input files as desired. The READ card may appear anywhere
after the title card of an MCNP6 input file but not in the middle of a
card continuation. READ cards may appear in auxiliary files, allowing
the nesting of READ cards to multiple levels. The encryption capability
may be applied to any or all of the READ levels. There is no limit to
the number of nested levels.

The encryption capability can be used to protect proprietary designs of
tools and other systems modeled with MCNP6. The encryption capability is
localized in subroutine ENCRYPT. The MCNP6 scheme is very simple;
therefore, it protects nothing. To protect input, the subroutine should
be modified to a more sophisticated scheme known only to those producing
the data and only executable MCNP6 versions should be provided to users
of the encrypted files.

Listing 5.62: example\_histp.mcnp.inp.txt

1

1

1

| Form: READ KEYWORD=value(s) ...   | Form: READ KEYWORD=value(s) ...                                                                                                                                                                                             |
|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FILE= filename                    | Causes input from the file filename to be inserted after the READ card in the MCNP6 input deck.                                                                                                                             |
| NOECHO                            | Suppresses printing in the output file of the input cards that follow the READ card.                                                                                                                                        |
| ECHO                              | Resumes echoing in the output file of the input after a NOECHO keyword was given in a previous READ card. Echoing also will resume when the next READ card is encountered without the NOECHO keyword. (DEFAULT)             |
| DECODE= password                  | Allows reading of an encrypted file. When DECODE is invoked, the encrypted input file is not echoed, and many default print tables are turned off (and cannot be turned back on) to protect the data in the encrypted file. |
| ENCODE= password                  | Allows the writing of an encrypted file.                                                                                                                                                                                    |

## 5.13.10.1 Example 1

## READ FILE=filename NOECHO

Because the echoing of the input cards also is resumed when an 'end of
file' is encountered, this example causes the input from the auxiliary
file, filename , to be suppressed. After the file filename is read,
input transfers back to the input file that contains the READ card and
printing is no longer suppressed.

## 5.13.10.2 Example 2

## READ DECODE password FILE=filename

This example causes the reading of the encrypted file, filename .

## 5.13.10.3 Example 3

## READ ENCODE password FILE=filename

This example causes an encrypted file, filename , to be written.

## 5.13.11 DBCN: Debug Information

## /warning\_sign Caution

Former MCNPX users need to be aware that several DBCN inputs may be
required to invoke MCNPX default behavior. In particular, please see
DBCN parameters x 38 , x 39 , and x 60 .

The entries on this card are used primarily for debugging problems and
the code itself. The first 12 entries can be changed in a restarted
calculation, which is useful for diagnosing troubles that occur late in
a long-running problem.

| ## /warning\_sign Caution   |
|-----------------------------|

The DBCN card is intended for MCNP developers. It should be applied with
extreme caution and a thorough understanding of the side effects.

glyph[negationslash]

| Data-card Form: DBCN   | x 1 x 2 ...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x 1                    | Obsolete - do not use. The random number used for starting the transport of the first particle history in a run. Required: Use the RAND card with the SEED keyword. ( 1 .)                                                                                                                                                                                                                                                                                                                                                              |
| x 2                    | Debug print interval. Print out information about every x 2 th particle. The information consists of a) the particle history number, b) the total number of collisions, c) the total number of random numbers generated, and d) the random number at the beginning of the history. This information is printed at the beginning of the history and is preceded by the letters DBCN in the output to aid in a pattern search. (DEFAULT: x 2 =0)                                                                                          |
| x 3 , x 4              | History number limits for event-log printing. Event-log printing is done for histories x 3 through x 4 , inclusively. The information includes a step-by-step account of each history, such as where and how a particle is born, which surface it crosses and which cell it enters, what happens to it in a cell, etc. (Note: The output formats for event logs limit the printing of cell, surface, and material numbers to a maximum of five characters (i.e., identifying numbers ≤ 99,999). See x 11 . (DEFAULT: x 3 =0 and x 4 =0) |
| x 5                    | Maximum number of events per history in the event log. (DEFAULT: x 5 =600)                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| x 6                    | Detector/DXTRAN underflow limit. (See Note 3.) (DEFAULT: x 6 =80.0) Restriction: 50 ≤ x 6 ≤ 200 If the attenuation factor, λ , to the detector or DXTRAN sphere is >x 6 , then the score is terminated as 'underflow in transmission.'                                                                                                                                                                                                                                                                                                  |
| x 7                    | Useful only to MCNP6 code developers.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| x 7                    | x 7 =0 no print from the volume and surface area calculations is produced. (DEFAULT)                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| x 7                    | x 7 = 0 a detailed print from the volume and surface area calculations is produced.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| x 8                    | Obsolete - do not use. Causes the starting random number of the problem to be that which would normally start the x 8 th history. That is, causes the x 8 th history to be the first history of a problem for debugging purposes; can also be used to select a random number sequence different from that in an identical problem to compare statistical convergence. Required: Use the RAND card with the HIST keyword. (See Note 1.)                                                                                                  |
| x 9                    | Defines the distance allowed between coincident repeated-structures surfaces for them still to be considered coincident. (DEFAULT: 10 - 4 ) A value of 10 - 30 reproduces the earlier treatment where coincident repeated structure surfaces were not allowed. The parameter x 9 should not have to be changed                                                                                                                                                                                                                          |

glyph[negationslash]

glyph[negationslash]

|      | unless geometries have dimensions greater than 10 5 or unless surfaces at different levels are intended to be closer than 10 - 4 .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | unless geometries have dimensions greater than 10 5 or unless surfaces at different levels are intended to be closer than 10 - 4 .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x 10 | Specifies the half-life threshold for stable nuclides (DEFAULT: 1 . 5768 × 10 16 s)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Specifies the half-life threshold for stable nuclides (DEFAULT: 1 . 5768 × 10 16 s)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| x 11 | If                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | If                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|      | x 11 =0,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | collision events are not printed in event logs for lost particles. (DEFAULT)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|      | x 11 = 0,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | the collision lines in the lost-particle event log are printed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| x 12 | Expected number of random numbers for this calculation. Entering x 12 will cause the last line of the output file to print x 12 and the actual number of random numbers used so that a quick comparison can be made to see if two problems tracked each other. DEFAULT: x 12 =0, i.e., test ignored)                                                                                                                                                                                                                                                                                                                                                                                                                    | Expected number of random numbers for this calculation. Entering x 12 will cause the last line of the output file to print x 12 and the actual number of random numbers used so that a quick comparison can be made to see if two problems tracked each other. DEFAULT: x 12 =0, i.e., test ignored)                                                                                                                                                                                                                                                                                                                                                                                                                    |
| x 13 | Obsolete - do not use. Random number stride. Required: Use the RAND card with the STRIDE keyword. ( 1 .)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Obsolete - do not use. Random number stride. Required: Use the RAND card with the STRIDE keyword. ( 1 .)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| x 14 | Obsolete - do not use. Random number multiplier. Required: Use the RAND card with the GEN keyword. ( 1 .)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Obsolete - do not use. Random number multiplier. Required: Use the RAND card with the GEN keyword. ( 1 .)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| x 15 | If                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | If                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|      | x 15 =0,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | the usual selection of statistical quantities is printed (DEFAULT)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|      | x 15 = 0,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | the shifted confidence interval and the variance of the variance for all tally bins are printed. An extra line of tally output is created for each tally that contains non-zero information. The shifted confidence interval center is followed by the estimated VOV. If the tally mean and relative error (RE) are all zeros, the VOV line is not printed because it is all zero also. Changing x 15 from non-zero to zero in a restarted calculation will cause the VOV information not to be printed. The parameter x 15 cannot be changed from zero to non-zero in a restarted calculation.                                                                                                                         |
| x 16 | Scale the history score grid for the accumulation of the empirical f(x) in print table 161 and 162. MCNP6 uses a logarithmically spaced history score grid in print table 161 for f(x), producing a straight line for f(x) on a log-log plot for 1/x n behavior, covering 60 decades of unnormalized tally magnitudes from 1E-30 to 1E30. This range can be multiplied by the x 16 entry when the range is not sufficient. A negative entry means that negative history scores will be accrued in the score grid f(-x) and the absolute value of x 16 will be used as the score grid multiplier. Positive history scores will then be lumped into the lowest bin with this option. This scaling can be done only in the | Scale the history score grid for the accumulation of the empirical f(x) in print table 161 and 162. MCNP6 uses a logarithmically spaced history score grid in print table 161 for f(x), producing a straight line for f(x) on a log-log plot for 1/x n behavior, covering 60 decades of unnormalized tally magnitudes from 1E-30 to 1E30. This range can be multiplied by the x 16 entry when the range is not sufficient. A negative entry means that negative history scores will be accrued in the score grid f(-x) and the absolute value of x 16 will be used as the score grid multiplier. Positive history scores will then be lumped into the lowest bin with this option. This scaling can be done only in the |
| x 17 | If                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | If                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

|      | x 17 =0,                                                                                                           | use default angular treatment for partial sub steps to generation sites of secondary particles. This treatment accounts for the probability of the delta function first, then interpolates in the cosine of the deflection angle. It does not preserve the plane in which the deflection angle will lie at the end of the full sub step. (DEFAULT)                            |
|------|--------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      | x 17 >0,                                                                                                           | use alternate angular treatment for secondary generation. The cosine of the electron angle is interpolated and the end-of-sub step plane is preserved, but the changing probability of the delta function along the sub step is ignored. This option is preserved for further testing of angular algorithms because results have been known to be sensitive to these details. |
|      | x 17 <0,                                                                                                           | use MCNP4A treatment of electron angles at secondary generation sites.                                                                                                                                                                                                                                                                                                        |
| x 18 | Controls the energy-indexing algorithm for electron transport related to bin interpolation.                        | Controls the energy-indexing algorithm for electron transport related to bin interpolation.                                                                                                                                                                                                                                                                                   |
|      | If x 18 =0,                                                                                                        | use 'MCNP-style' energy-indexing algorithm; also called the 'bin-centered' treatment. (Used by MCNPX.)                                                                                                                                                                                                                                                                        |
|      | If x 18 =1,                                                                                                        | use Integrated Tiger Series (ITS)-style energy-indexing algorithm; also called the 'nearest group boundary' treatment.                                                                                                                                                                                                                                                        |
|      | If x 18 =2,                                                                                                        | use detailed Landau straggling sampling logic, also called the 'energy- and step-specific' treatment. Required for single-event electron transport. (DEFAULT)                                                                                                                                                                                                                 |
| x 19 | In use by MCNP6 developer(s) to study quadratic polynomial interpolation. [DEFAULT (x =0) provides current model.] | In use by MCNP6 developer(s) to study quadratic polynomial interpolation. [DEFAULT (x =0) provides current model.]                                                                                                                                                                                                                                                            |
| x 20 | Unused.                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                               |
| x 21 | Unused.                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                               |
| x 22 | Unused.                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                               |
| x 23 | If                                                                                                                 |                                                                                                                                                                                                                                                                                                                                                                               |
|      | x 23 =0,                                                                                                           | use pulse-height tally variance reduction trees if variance reduction is present, otherwise do not use PHT VR trees. (DEFAULT)                                                                                                                                                                                                                                                |
|      | x 23 =1,                                                                                                           | force pulse-height tally variance reduction trees whether they are needed or not.                                                                                                                                                                                                                                                                                             |
|      | x 23 =-1,                                                                                                          | do no use pulse-height tally variance reduction trees.                                                                                                                                                                                                                                                                                                                        |
| x 24 | Controls grazing contribution cut-off for surface flux tallies. If                                                 | Controls grazing contribution cut-off for surface flux tallies. If                                                                                                                                                                                                                                                                                                            |
|      | x 24 =0,                                                                                                           | | mu cut | = 0.001. (DEFAULT)                                                                                                                                                                                                                                                                                                                                                 |

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

<!-- image -->

|      | x 24 = 0,                                                                                                                                                      | | mu cut | = x 24                                                                                                                                                                |
|------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x 25 | Unused.                                                                                                                                                        | Unused.                                                                                                                                                                          |
| x 26 | Unused.                                                                                                                                                        | Unused.                                                                                                                                                                          |
| x 27 | Controls antiparticle promotion. If                                                                                                                            | Controls antiparticle promotion. If                                                                                                                                              |
|      | x 27 =0,                                                                                                                                                       | do not promote antiparticles. (DEFAULT)                                                                                                                                          |
|      | x 27 =1,                                                                                                                                                       | promote antiparticles (affects MODE card and certain tallies); lumps particle and antiparticle pairs under one particle type. (Used in MCNPX.) (Certain restrictions may apply.) |
| x 28 | Bank size. (DEFAULTs vary by application: x 28 =2048 for most fixed-source problems, x 28 =128 for criticality problems, x 28 =16384 for high-energy problems) | Bank size. (DEFAULTs vary by application: x 28 =2048 for most fixed-source problems, x 28 =128 for criticality problems, x 28 =16384 for high-energy problems)                   |
| x 29 | Unused.                                                                                                                                                        | Unused.                                                                                                                                                                          |
| x 30 | Unused.                                                                                                                                                        | Unused.                                                                                                                                                                          |
| x 31 | Unused.                                                                                                                                                        | Unused.                                                                                                                                                                          |
| x 32 | If                                                                                                                                                             | If                                                                                                                                                                               |
|      | x 32 =0,                                                                                                                                                       | normal GENXS behavior. (DEFAULT)                                                                                                                                                 |
|      | x 32 = 0,                                                                                                                                                      | use internal bremsstrahlung spectrum generation with CEM and LAQGSM models for GENXS.                                                                                            |
| x 33 | If                                                                                                                                                             | If                                                                                                                                                                               |
|      | x 33 =0,                                                                                                                                                       | do not apply an additional interpolation/smoothing method to stopping powers for heavy ions. (DEFAULT)                                                                           |
|      | x 33 = 0,                                                                                                                                                      | apply an additional interpolation/smoothing method to stopping powers for heavy ions.                                                                                            |
| x 34 | Used to reproduce a bug in µ - -induced gammas. [DEFAULT (x 34 =0) is to use the corrected code.]                                                              | Used to reproduce a bug in µ - -induced gammas. [DEFAULT (x 34 =0) is to use the corrected code.]                                                                                |
| x 35 | If                                                                                                                                                             | If                                                                                                                                                                               |
|      | x 35 =0,                                                                                                                                                       | causes slight (arbitrary) spreading of nuclear excitation during µ - capture. (DEFAULT)                                                                                          |
|      | x 35 = 0,                                                                                                                                                      | turns off slight (arbitrary) spreading of nuclear excitation during µ - capture.                                                                                                 |
| x 36 | If                                                                                                                                                             | If                                                                                                                                                                               |
|      | x 36 =0,                                                                                                                                                       | use user-provided data for µ - -induced gamma rays, if available. (DEFAULT)                                                                                                      |
|      | x 36 = 0,                                                                                                                                                      | use older data (literature or MUON/RURP) previously hard-coded in MCNPX.                                                                                                         |
| x 37 | Set minimum of internal bremsstrahlung spectrum for CEM and LAQGSM in GENXS when x 32 = 0. (DEFAULT: x 37 =30 MeV)                                             | Set minimum of internal bremsstrahlung spectrum for CEM and LAQGSM in GENXS when x 32 = 0. (DEFAULT: x 37 =30 MeV)                                                               |

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

<!-- image -->

| x 38   | If                                                                                                  |                                                                                                                         |
|--------|-----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
|        | x 38 =0,                                                                                            | use Barashenkov/Polanski data file BARPOL2001.dat. (DEFAULT)                                                            |
|        | x 38 = 0,                                                                                           | use older BARPOL.dat data file from 1996.                                                                               |
| x 39   | Controls the default S( α , β ) smoothing behavior, which was present in MCNPX but not in MCNP5. If | Controls the default S( α , β ) smoothing behavior, which was present in MCNPX but not in MCNP5. If                     |
|        | x 39 =0,                                                                                            | use default S( α , β ) sampling treatment, as in MCNP5 (DEFAULT).                                                       |
|        | x 39 = 0,                                                                                           | use MacFarlane/Little sampling, as in MCNPX.                                                                            |
| x 40   | Controls writing of MCPLIB and xsdir lines                                                          | Controls writing of MCPLIB and xsdir lines                                                                              |
| x 41   | Controls printing printing photon/electron data                                                     | Controls printing printing photon/electron data                                                                         |
| x 42   | If                                                                                                  | If                                                                                                                      |
|        | x 42 =0,                                                                                            | use default method for model cross sections. (DEFAULT)                                                                  |
|        | x 42 >0,                                                                                            | use original MCNPX model cross-section method.                                                                          |
|        | x 42 <0,                                                                                            | use earlier MCNP6 method (MARS coding).                                                                                 |
| x 43   | Control photon form-factor interpolation. If                                                        | Control photon form-factor interpolation. If                                                                            |
|        | x 43 =0,                                                                                            | use linear form-factor interpolation. (Used by MCNPX.)                                                                  |
|        | x 43 =2,                                                                                            | use best method for form-factor interpolation. (DEFAULT) Currently the best method is logarithmic inversion or log-log. |
| x 44   | For developers: to study coherent scattering in isolation. (DEFAULT: x 44 =0, all processes)        | For developers: to study coherent scattering in isolation. (DEFAULT: x 44 =0, all processes)                            |
| x 45   | If                                                                                                  |                                                                                                                         |
|        | x 45 =0,                                                                                            | use MCNP6 elastic scattering method. (DEFAULT)                                                                          |
|        | x 45 = 0,                                                                                           | use earlier MCNPX elastic scattering method.                                                                            |
| x 46   | If                                                                                                  |                                                                                                                         |
|        | x 46 =0,                                                                                            | use default CEM-to-LAQGSM photonuclear energy boundary.                                                                 |
|        | x46>0,                                                                                              | set x 46 as CEM-to-LAQGSM energy boundary.                                                                              |
| x 47   | If                                                                                                  |                                                                                                                         |
|        | x 47 =0,                                                                                            | use CLEM model for cosmic-ray spectra.(DEFAULT)                                                                         |
|        | x 47 = 0,                                                                                           | use Lal model for cosmic-ray spectra.                                                                                   |
| x 48   | If                                                                                                  |                                                                                                                         |
|        | x 48 =0,                                                                                            | allow MCNP6 to forbid threading when not suitable. (DEFAULT)                                                            |

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

|      | x 48 = 0,                                                                                                                                                                                     | insist on threading if requested.                                                                                                                                                             |
|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x 49 | If                                                                                                                                                                                            | If                                                                                                                                                                                            |
|      | x 49 =0,                                                                                                                                                                                      | perform normal input checking. (DEFAULT)                                                                                                                                                      |
|      | x 49 >0,                                                                                                                                                                                      | expert user option to skip some lattice input checking for very large problems to save time in initialization.                                                                                |
| x 50 | Modifies printing the tally fluctuation chart (TFC). Controls printing of the relative fractional uncertainty (i.e., the 'error') and the VOV. If                                             | Modifies printing the tally fluctuation chart (TFC). Controls printing of the relative fractional uncertainty (i.e., the 'error') and the VOV. If                                             |
|      | x 50 =0,                                                                                                                                                                                      | do traditional printing of tally fluctuation charts. (DEFAULT)                                                                                                                                |
|      | x 50 =1,                                                                                                                                                                                      | provide the relative fractional uncertainty and VOV in scientific notation and decrease the printing of three side-by-side TFCs to two side-by-side TFCs.                                     |
|      | x 50 =2,                                                                                                                                                                                      | is the same as x 50 =1 but also prints more digits in the mean column.                                                                                                                        |
| x 51 | Used to turn off all photon-induced fluorescence. (Default is to have photon-induced fluorescence active.)                                                                                    | Used to turn off all photon-induced fluorescence. (Default is to have photon-induced fluorescence active.)                                                                                    |
| x 52 | Used to turn off Compton-induced relaxation. Applies to fluorescence and Auger electrons. (Default is have Compton-induced relaxation active.)                                                | Used to turn off Compton-induced relaxation. Applies to fluorescence and Auger electrons. (Default is have Compton-induced relaxation active.)                                                |
|      | Set                                                                                                                                                                                           | x 52 =1, to invoke MCNPX functionality in emission of Auger electrons.                                                                                                                        |
| x 53 | If                                                                                                                                                                                            | If                                                                                                                                                                                            |
|      | x 53 =0,                                                                                                                                                                                      | use new ENDF photoelectric relaxation data, if available. (DEFAULT)                                                                                                                           |
|      | x 53 = 0,                                                                                                                                                                                     | use traditional photoelectric fluorescence; i.e., use limited pre-ENDF/B VI.8 treatment. Applies to fluorescence and Auger electrons.                                                         |
| x 54 | Controls sampling method for ENDF Law 9. If                                                                                                                                                   | Controls sampling method for ENDF Law 9. If                                                                                                                                                   |
|      | x 54 =0,                                                                                                                                                                                      | use traditional sampling for first 10 8 tries but then use new, improved sampling method. (DEFAULT)                                                                                           |
|      | x 54 = 1,                                                                                                                                                                                     | use new, improved sampling method.                                                                                                                                                            |
| x 55 | Spontaneous decay integration time. Default is 20 s which includes ≈ 20 decay levels, or ≈ 1 s per decay level. Complex decay chains may require an increase in this parameter [§5.8.1, 12 ]. | Spontaneous decay integration time. Default is 20 s which includes ≈ 20 decay levels, or ≈ 1 s per decay level. Complex decay chains may require an increase in this parameter [§5.8.1, 12 ]. |
| x 56 | Unused.                                                                                                                                                                                       | Unused.                                                                                                                                                                                       |
| x 57 | Unused.                                                                                                                                                                                       | Unused.                                                                                                                                                                                       |
| x 58 | Unused.                                                                                                                                                                                       | Unused.                                                                                                                                                                                       |
| x 59 | Unused.                                                                                                                                                                                       | Unused.                                                                                                                                                                                       |
| x 60 | If                                                                                                                                                                                            | If                                                                                                                                                                                            |

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

glyph[negationslash]

|      | x 60 =0,                                                                                                                                                                                                                                                                  | print number of calls to each high-energy model. DEFAULT                                                                                                                                                                                                                  |
|------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      | x 60 = 0,                                                                                                                                                                                                                                                                 | also include successes for each model.                                                                                                                                                                                                                                    |
| x 61 | Models of knock-on electron angles. (DEFAULT=0)                                                                                                                                                                                                                           | Models of knock-on electron angles. (DEFAULT=0)                                                                                                                                                                                                                           |
| x 62 | Used to debug single-event electrons excitation energy loss. (DEFAULT=0)                                                                                                                                                                                                  | Used to debug single-event electrons excitation energy loss. (DEFAULT=0)                                                                                                                                                                                                  |
| x 63 | Unused.                                                                                                                                                                                                                                                                   | Unused.                                                                                                                                                                                                                                                                   |
| x 64 | To debug single-event electrons angular deflection for knock-on electrons. (DEFAULT=0)                                                                                                                                                                                    | To debug single-event electrons angular deflection for knock-on electrons. (DEFAULT=0)                                                                                                                                                                                    |
| x 65 | To debug single-event ionization and treat deflection for incident particles. (DEFAULT=0)                                                                                                                                                                                 | To debug single-event ionization and treat deflection for incident particles. (DEFAULT=0)                                                                                                                                                                                 |
| x 66 | To control single-event bremsstrahlung photon angles. (DEFAULT=0)                                                                                                                                                                                                         | To control single-event bremsstrahlung photon angles. (DEFAULT=0)                                                                                                                                                                                                         |
| x 67 | Controls number of particle histories ( NPS ) for first calculation of the average contribution per history for point detectors and DXTRAN spheres for Russian roulette game. If                                                                                          | Controls number of particle histories ( NPS ) for first calculation of the average contribution per history for point detectors and DXTRAN spheres for Russian roulette game. If                                                                                          |
|      | x 67 =0,                                                                                                                                                                                                                                                                  | use TFC value of NPS for first calculation of detector or DXTRAN average contribution. (DEFAULT)                                                                                                                                                                          |
|      | x 67 >0,                                                                                                                                                                                                                                                                  | use the first x 67 particles to determine the average contribution per history for point detectors and DXTRAN spheres for Russian roulette game.                                                                                                                          |
| x 68 | Unused.                                                                                                                                                                                                                                                                   | Unused.                                                                                                                                                                                                                                                                   |
| x 69 | Used to increase the LJA array size, which stores the surfaces bounding the cells. Only needed when a fatal error occurs and the MCNP code advises the user to 'Set dbcn(69) to increase mlja > [. . . ]'. dbcn(69) sets mlja , which controls the size of the LJA array. | Used to increase the LJA array size, which stores the surfaces bounding the cells. Only needed when a fatal error occurs and the MCNP code advises the user to 'Set dbcn(69) to increase mlja > [. . . ]'. dbcn(69) sets mlja , which controls the size of the LJA array. |
| x 70 | Debug choice of some interaction models. (DEFAULT=0)                                                                                                                                                                                                                      | Debug choice of some interaction models. (DEFAULT=0)                                                                                                                                                                                                                      |
| x 71 | If                                                                                                                                                                                                                                                                        | If                                                                                                                                                                                                                                                                        |
|      | x 71 =0, x 71 = 0,                                                                                                                                                                                                                                                        | allow model photonuclear capability. (DEFAULT) prohibit model photonuclear capability.                                                                                                                                                                                    |
| x 72 | If                                                                                                                                                                                                                                                                        | If                                                                                                                                                                                                                                                                        |
|      | x 72 =0,                                                                                                                                                                                                                                                                  | explicit log-log interpolation in ELXS_MOD. (DEFAULT)                                                                                                                                                                                                                     |
|      | x 72 = 0,                                                                                                                                                                                                                                                                 | random linear interpolation.                                                                                                                                                                                                                                              |
| x 73 | Unused.                                                                                                                                                                                                                                                                   | Unused.                                                                                                                                                                                                                                                                   |
| x 74 | Unused.                                                                                                                                                                                                                                                                   | Unused.                                                                                                                                                                                                                                                                   |
| x 75 | If x 75 = 0, print extra info for F-matrix calculations.                                                                                                                                                                                                                  | If x 75 = 0, print extra info for F-matrix calculations.                                                                                                                                                                                                                  |
| x 76 | If x 76 = 0, print array storage info after setup.                                                                                                                                                                                                                        | If x 76 = 0, print array storage info after setup.                                                                                                                                                                                                                        |
| x 77 | If x 77 = 0, specify number of bins for hash-based cross-section searches. DEFAULT is 8192.                                                                                                                                                                               | If x 77 = 0, specify number of bins for hash-based cross-section searches. DEFAULT is 8192.                                                                                                                                                                               |

glyph[negationslash]

glyph[negationslash]

| x 78   | For developers: 0 for old 6.1 S ( α,β ) method, 1 for new.                                                                                                                                                                                         |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x 79   | If                                                                                                                                                                                                                                                 |
| x 80   | Unused.                                                                                                                                                                                                                                            |
| x 81   | 0 uses linear interpolation of electron elastic scatter and 1 uses log-log interpolation within a data table.                                                                                                                                      |
| x 82   | 0 uses linear interpolation of electron elastic scatter and 1 uses log-log interpolation between data tables.                                                                                                                                      |
| x 83   | 0 uses linear interpolation for electron partial x-s and 1 uses log-log interpolation.                                                                                                                                                             |
| x 84   | 0 uses linear interpolation for electron bremsstrahlung energy and 1 uses log-log interpolation within a data table.                                                                                                                               |
| x 85   | 0 uses linear interpolation for electron bremsstrahlung energy and 1 uses log-log interpolation between data tables.                                                                                                                               |
| x 86   | 0 uses linear interpolation for electron excitation energy and 1 uses log-log interpolation.                                                                                                                                                       |
| x 87   | 0 uses linear interpolation for electron knock-on energy and 1 uses log-log interpolation within a table.                                                                                                                                          |
| x 88   | 0 uses linear interpolation for electron knock-on energy and 1 uses log-log interpolation between tables.                                                                                                                                          |
| x 89   | 0 uses linear interpolation for electron ionization x-s and 1 uses log-log interpolation.                                                                                                                                                          |
| x 90   | If x 90 = 0, set maximum number of terms for the Goudsmit-Saunderson distribution ( 3 ). DEFAULT is 240. If DBCN(90) < 240, the number of terms for the Goudsmit-Saunderson distribution will be set to DEFAULT due to the limitation in the data. |
| x 91   | If x 91 >0, set the minimum ROC curve count value to x 91 .                                                                                                                                                                                        |
| x 92   | If x 92 >0, set the maximum ROC curve count value to x 92 .                                                                                                                                                                                        |
| x 93   | Unused.                                                                                                                                                                                                                                            |
| x 94   | Unused.                                                                                                                                                                                                                                            |
| x 95   | Unused.                                                                                                                                                                                                                                            |
| x 96   | Unused.                                                                                                                                                                                                                                            |
| x 97   | Unused.                                                                                                                                                                                                                                            |
| x 98   | Unused.                                                                                                                                                                                                                                            |
| x 99   | Unused.                                                                                                                                                                                                                                            |
| x 100  | 0 uses new coincident-surface method and 1 uses old method.                                                                                                                                                                                        |

Use: Optional. All DBCN parameters allow 8-byte entries.

## Details:

- 1 Settings for the random-number-generator parameters are now accomplished using the RAND card. The DBCN entries 1, 8, 13, and 14 were used long ago, but are no longer permitted. Setting these entries on the DBCN only (and not the RAND card) is a fatal error.
- 2 The contributions neglected because of underflow are typically insignificant to the final answer. However, in some cases, the underflow contribution is significant and necessary. When DXTRAN spheres for point detectors are used to get tally contributions for generating weight windows, sometimes these underflow contributions cannot be neglected. If DXTRAN or detector underflow is significant in the calculation, generally there are serious problems, such as not sampling enough collisions near the detector. Changing the underflow limit should be done only with extreme caution.
- 3 Setting the number of terms for the Goudsmit-Saunderson distribution can stabilize the underlying angular deflection distributions used in transport, yielding improved simulation results [332]. However, the increase in the number of terms for the Goudsmit-Sauderson distribution is only valid for electron energies greater than 0 . 256 MeV. For electrons with energies less than, the number of terms for the Goudsmit-Sauderson distribution is set to DEFAULT.

## 5.13.12 LOST: Lost Particle Control

The LOST card allows the user to increase the number of lost particles
the code will allow before terminating.

| Data-card Form: LOST lost1 lost2   | Data-card Form: LOST lost1 lost2                                                                                |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| lost1                              | Number of particles that can be lost before the calculation terminates with BAD TROUBLE . (DEFAULT: lost1 =10 ) |
| lost2                              | Maximum number of debug prints that will be made for lost particles. (DEFAULT: lost2 =10 )                      |

Defaults: 10 lost particles and 10 debug prints.

Use: Discouraged. Losing more than 10 particles is rarely justifiable.

The word 'lost' means that a particle gets to an ill-defined section of
the geometry and does not know where to go next. This card should be
used cautiously: the user should know why the particles are being lost
and the number lost should be statistically insignificant out of the
total sample. Even if only one of many particles gets lost, there could
be something seriously wrong with the geometry specification. Geometry
plots in the area where the particles are being lost can be extremely
useful in isolating the reason that particles are being lost.

## 5.13.13 IDUM: Integer Array

The IDUM integer array is in the MCNP \_ DEBUG.F90 module and is
available to the users. IDUM is included in the dumps on the restart
file and therefore can be used for any purpose, including accumulating
information over the entire course of a problem through several
restarted calculations. The array is declared as Fortran integer(4)
type, so it provides 32 bits of precision.

## Data-card Form: IDUM i 1 i 2 . . . i K i k Any user-assigned integer value where 1 ≤ k ≤ K = 2000 .

Default:

All array values zero.

Use: Useful only in user-modified versions of MCNP6.

## Details:

- 1 Up to 2000 entries can be provided to fill the IDUM array with integer numbers. If floating-point numbers are entered, they will be truncated and converted to integers.

## 5.13.14 RDUM: Floating-Point Array

The RDUM floating-point array is in the MCNP \_ DEBUG.F90 module and is
available to the users. RDUM is included in the dumps on the restart
file and therefore can be used for any purpose, including accumulating
information over the entire course of a problem through several
restarted calculations. The array is declared as Fortran real(8) type,
so it provides 64 bits of precision.

```
Data-card Form: RDUM r 1 r 2 . . . r K r k Any user-assigned floating-point value where 1 ≤ k ≤ K = 2000 .
```

Default:

All array values zero.

Use: Useful only in user-modified versions of MCNP6.

## Details:

- 1 Up to 2000 entries can be provided to fill the RDUM array with floating-point (real) numbers.

## 5.13.15 ZA, ZB, ZC, and ZD: Developers Card Placeholders

The ZA , ZB , ZC , and ZD cards are made available to advanced user-
developers who wish to construct their own input cards in MCNP6. Similar
to the use of IDUM and RDUM , source code that is modified by users to
create a modified version of MCNP6 no longer carries the extensive
validation and verification the original LANL-created source and
executables do. Users must perform their own verification and validation
to ensure their modifications have not had adverse effects on existing
capabilities.

## 5.13.16 FILES: File Creation

1

| Data-card Form: FILES unit _ no filename access form record _ length   | Data-card Form: FILES unit _ no filename access form record _ length                                                                                  |
|------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| unit _ no                                                              | Recommendation: unit _ no > 100 . (DEFAULT: none)                                                                                                     |
| filename                                                               | Name of the file. (DEFAULT: none)                                                                                                                     |
| access                                                                 | Options are SEQUENTIAL or DIRECT access. (DEFAULT: SEQUENTIAL )                                                                                       |
| form                                                                   | Options are FORMATTED or UNFORMATTED . (DEFAULT: FORMATTED if SEQUENTIAL access has been specified, UNFORMATTED if DIRECT access has been specified.) |
| record _ length                                                        | Record length in direct access file. (DEFAULT: not required if SEQUENTIAL access has been specified, no default if DIRECT access has been specified.) |

Use: When a user-modified version of MCNP6 needs files whose
characteristics may vary from calculation to calculation. Not allowed in
restarted calculations.

## Details:

- 1 If this card is present, the first two entries are required and must not conflict with existing MCNP6 units and files. Setting unit \_ no greater than 100 and less than 1,000 will likely prevent any conflicts with MCNP6 unit numbers during input reading and output writing. A file unit conflict may occur if the user-defined file is both accessed during particle transport, and the sum of 60 and the number of parallel execution threads requested by the user (e.g. tasks on the command line) are equal to the user-specified file unit number.
- 2 The words SEQUENTIAL , DIRECT , FORMATTED , and UNFORMATTED can be abbreviated. The maximum number of files allowed is six, unless the second dimension of the KUFIL array in FIXCOM.F90 is increased and the UFILES.F90 subroutine is updated appropriately.

## /warning\_sign Caution

The names of any user files in a restarted calculation will be the same
as in the initial calculation. The names are not automatically sequenced
if a file of the same name already exists; therefore, a second output
file from a restarted calculation will overwrite and replace the content
of an existing file of the same name. If you are using the FILES card
for an input file and restart the calculation, you will have to provide
the coding for keeping track of the record number and then positioning
the correct starting location on the file when you continue or MCNP6
will start reading the file at the beginning.

## 5.13.16.1 Example 1

FILES 21 ANDY S F 0 22 MIKE D U 512

## 5.13.16.2 Example 2

1

2

```
FILES 17 DUMN1 MCNP6 INP=TEST3 DUMN1=POST3
```

If the file name is DUMN1 or DUMN2 , the user can optionally use the
execution line message to designate a file whose name might be different
from run to run, for instance in a restarted calculation.

## 5.13.17 DISABLE: Disable MCNP Features

The DISABLE card allows a user to deliberately disable certain features
of the MCNP code that otherwise run by default. This can be useful for
problems approaching the resource limitations of the computer running
it.

## Form: DISABLE [options]

## NUCLIDE \_ ACTIVITY \_ TABLE

If this option is present, this disables the computation of PRINT Table
140 completely. Subsequent restart runs will be unable to print this
table out. This option is useful to reduce the memory usage of problems
with very large numbers of materials and nuclides per material.
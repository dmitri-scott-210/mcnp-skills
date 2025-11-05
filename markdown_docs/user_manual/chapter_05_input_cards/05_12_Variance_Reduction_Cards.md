---
title: "Chapter 5.12 - Variance Reduction-focused Data Cards"
chapter: "5.12"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.12_Variance_Reduction-focused_Data_Cards.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

enhancement is discouraged, since it may result in a program crash,
tally values that are all zeros, or silent wrong answers.

Criteria that must be met for MCNP6 to automatically (and appropriately)
use the lattice speed tally enhancement include the following:

1. A hexagonal lattice must be present in the geometry.
2. All F4 tallies contain a hexahedral lattice.
3. None of the following cards are used: DXT , DXC , F1 , F2 , * F4 , F6 , F7 , F8 , +F8 , PERT , WWG , WWGE , WWGT .
4. None of the following cards are used to modify an F4 tally: FT , E , EM , T , TM , CF , SF , FS , C .
5. All F4 tallies have an associated FM4 card that contains only a single digit multiplier.
6. All F4 tallies have associated DE / DF cards.

The following criteria are not checked by MCNP6. The user must verify
that the input deck meets these criteria:

1. Nested lattices are not tallied over.
2. The entries for a cell's FILL card do not include that cell's own universe number.
3. The full lattice index range is given on every lattice on each F4 tally card.

For more information, see [330].

## 5.12 Variance Reduction-focused Data Cards

Many of these variance-reduction cards require knowledge of both the
Monte Carlo method and the particular variance reduction technique
employed. Section 1.2.7 and its references are a good place to start
learning more about these topics.

Only two variance reduction games in MCNP6 are enabled by default:
implicit capture/weight cutoff and Russian roulette for point detectors
and DXTRAN spheres. All other variance reduction games must be applied
explicitly and therefore are considered optional. In spite of this
statement, the code does require that either (1) the IMP card be present
in the data-card section of the MCNP input file (or, equivalently, an
IMP parameter be specified on each cell card) or (2) weight windows be
supplied through WWN cards (or, equivalently, read from a WWINP file).
Otherwise, a fatal error will occur during the input-checking process.

Some variance reduction cards (e.g., IMP ) in the data section require
the number of entries to equal the number of cells or surfaces in the
problem; otherwise, a fatal error results. For other cards (e.g., EXT )
no fatal error results if the number of entries does not equal the
number of cells or surfaces, but a warning may be issued. The order of
the cells or surfaces on these cards correspond in order to the cell or
surface cards that appear in the MCNP input file. The n R repeat or n J
jump features may help in supplying the desired values. Note that the n
J feature relies on the presence of a default value. Users should refer
to the individual cards to learn about their defaults.

## 5.12.1 IMP: Cell Importance

A cell's importance is used

1. to terminate the particle's history when a particle enters a cell with importance zero,
2. for playing geometry splitting and Russian roulette as a means to control the particle population upon entering a cell, and
3. for scaling the cutoffs in the weight cutoff game. An importance assigned to a cell that is in a universe is interpreted as a multiplier of the importance of the filled cell.

## /warning\_sign Caution

The splitting behavior that takes place as particles enter and exit UM
pseudocells as a result of defining varying pseudocell importances for
adjacent pseudocells may lead to potentially silent wrong answers with
UM geometry or, more clearly, seemingly unrelated issues such as the
code reporting negative emission energy following certain collisions.
Rather than using cell-based importances, it is recommended to use cell-
based weight windows and to set mwhere = -1 on the WWP card to avoid
such issues, which arise because of particle-banking behavior as
particles enter and exit UM pseudocells.

<!-- image -->

| Cell-card Form: IMP: P = or Data-card Form: IMP: P   | x x 1 x 2 . . . x K                                                                                                                                                                                                    |
|------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P                                                    | Any particle symbol from Table 4.3. May also be a list of particle symbols separated by commas as long as the importance are the same for the desired importance are the same for the different listed particle types. |
| x                                                    | Cell importance. One entry must appear on each cell card for each particle type that has non-default values.                                                                                                           |
| x k                                                  | Importance of cell k . Number of entries must equal number of cells in the problem.                                                                                                                                    |

Default: Default IMP values are variable and depend on the presence or
absence of other cards as illustrated below. For this reason, it is
highly recommended that the user explicitly specify IMP values for all
particle types or verify from PRINT Table 60 the values used in the
calculation are those intended.

If no WWN card is present: IMP values are explicitly required for one of
the requested particle types on the MODE card, otherwise a fatal error
occurs. Additionally, if (1) one particle is explicitly assigned IMP
values and (2) IMP values are not supplied for the other particle types,
then the default IMP values for the remaining particles are 1 where the
explicitly assigned importance are greater than 0 and 0 where the
explicitly assigned importance are 0.

If a WWN card is present: IMP values are not required when using cell-
based weight windows. However, one set of IMP values is required when
using mesh-based weight windows. The default IMP values for the
particle(s) on the WWN card are set to 1 where the weight-window lower
bounds are not -1 , otherwise they are set to 0. IMP values for all
other particles not having a WWN card are set to 0. If IMP values are
explicitly provided along with the WWN card(s), they are retained and
IMP values not explicitly provided for any other particles are set to 1
where the explicitly set IMP values are not 0; otherwise, they are set
to 0.

If a cell importance is set to 0 for any particle, all particle
importance for that cell will be set to 0 (default implicit value)
unless specified otherwise. However, if the n J feature is used to
specify importance, the values

1

jumped over are given a default importance value of 0. Particles
entering a cell with an importance value of 0 are immediately terminated
as are contributions to detectors and DXTRAN spheres. The outside world
cell (surrounding the geometry of interest) should be such a cell;
problems without such a cell will experience lost particles.

Use: Use IMP when weight windows are not desired. See details in the
default discussion above.

Different particle types can be split differently by having separate IMP
: P cards. When using the data card entry format, it is a fatal error if
the number of entries on any IMP : P card is not equal to the number of
cells in the problem. Similarly, if an IMP : P parameter appears on one
cell card, a fatal error occurs if a comparable entry does not appear on
all cell cards. The n R repeat and n M multiply features are especially
useful with this card in the data-card section. Be careful when using
these shorthand notations together: R does not duplicate the M , but
rather the value that the M notation creates.

A track will neither be split nor rouletted when it enters a void cell
even if the importance ratio of the adjacent cells would normally call
for a split or roulette. However, the importance of the non-void cell
that a particle exits is remembered and splitting or Russian roulette
will be played when the particle next enters a non-void cell. As an
example of the benefit of not splitting into a void, consider a long
cylindrical void (or pipe) surrounded by a material like concrete where
the importance are decreasing radially away from the pipe. Considerable
computer time can be wasted by tracks bouncing back and forth across the
pipe and doing nothing but splitting, then immediately undergoing
roulette. Splitting into a void increases the time per history but has
no counterbalancing effect on the expected history variance. Thus, the
figure of merit (FOM) is reduced by the increased time per history.

If a superimposed weight-window mesh is used, the IMP card is required.
Cell importance are only used for the weight cutoff game in zero-window
meshes.

## /warning\_sign Caution

The splitting behavior that takes place as particles enter and exit UM
pseudocells as a result of defining varying pseudocell importances for
adjacent pseudocells may lead to potentially silent wrong answers with
UM geometry or, more clearly, seemingly unrelated issues such as the
code reporting negative emission energy following certain collisions. If
one must use weight windows with UM, it is recommended that mwhere = -1
be set to avoid such issues, which arise because of particle-banking
behavior as particles enter and exit UM pseudocells.

## 5.12.1.1 Example 1

## IMP:N 1 2 2M 0 1 20R

The neutron importance of cell 1 is 1, cell 2 is 2, cell 3 is 4, and
cell 4 is 0. The importance for cells 5 through 25 are 1. A track will
be split 2 for 1 going from cell 2 into cell 3, each new track having
half the weight of the original track before splitting. A track moving
in the opposite direction will be terminated in half the cases (that is,
with probability 0.5), but it will be followed in the remaining cases
with twice the weight.

## 5.12.2 VAR: Variance Reduction Control

The VAR card is used to control variance-reduction methods across
several variance-reduction techniques. In particular, it allows the
roulette game for weight windows and cell/energy/time importance to be
turned off. Turning off roulette can be helpful for F8 tallies using
variance reduction ( 1 ).

| Data-card Form: VAR keyword=value   | Data-card Form: VAR keyword=value                                                |
|-------------------------------------|----------------------------------------------------------------------------------|
| RR                                  | controls rouletting game for weight windows and cell/energy/time importances. if |
|                                     | RR = ON the roulette game is turned on.                                          |
|                                     | RR = OFF the roulette game is turned off.                                        |

Default: No modifications of variance reduction methods.

Use: Optional

## Details:

- 1 For a pulse-height tally (that uses the de-branching method), Russian rouletting a particle produces zero tallies for all collections of particles that include the rouletted particle. This procedure results in no bias, but adds computational effort. In this circumstance, roulette is contraindicated.

## 5.12.3 Weight-window Cards

Weight windows can be either cell-based or mesh-based. Mesh-based
windows eliminate the need to subdivide geometries finely enough for
importance functions.

Weight windows provide an alternative means to importance ( IMP values),
energy splitting ( ESPLT cards), and time splitting ( TSPLT cards) for
specifying space-, energy-, and time-dependent importance functions. The
advantages of weight windows are that they

1. provide an importance function in space, time, space-energy, space-time, or space-energy-time;
2. attempt to control particle weights;
3. are more compatible with other variance-reduction features such as the exponential transform ( EXT card);
4. can be applied at surface crossings, collisions, or both;
5. control the severity of splitting or Russian roulette;
6. can be turned off in selected space, time, or energy regions; and
7. can be automatically generated by the weight-window generator.

The disadvantages are that

1. weight windows are not as straightforward as importance and
2. when the source weight is changed, the weight windows may have to be renormalized (see the 7th entry on the WWP card).

The novice weight-window user is strongly advised to read §2.7.2.12.

In repeated structures, an additional difference between cell importance
and weight windows exists. For cell importance ( IMP card), an
importance in a cell that is in a universe is interpreted as a
multiplier of the importance of the filled cell [§5.12.1] and action
(i.e., splitting or roulette) is taken based on the ratio of importance.
The weight-window bounds are absolute bounds, not multipliers. The lower
window bound in cell j and energy bin k is unaffected by the repeated
structures. Mesh based windows are recommended for use with repeated
structures.

A cell-based weight-window lower bound of a cell that is in a universe
is interpreted as a multiplier of the weight-window lower bound of the
filled cell.

## 5.12.3.1 WWE: Weight-window Energies (or Times)

The WWE card defines the energy (or time) intervals for which weight-
window bounds will be specified on the WWN card. The minimum energy is
not entered on the WWE card, but is defined to be zero. Similarly, the
minimum time is -∞ . Whether energy or time is specified is determined
by the 6th entry on the WWP card. For time-dependent weight windows, the
WWT card is now recommended, but times are allowed on the WWE card to
preserve backward compatibility.

<!-- formula-not-decoded -->

Default: If the WWE card is omitted and weight windows are used, one
energy (or time) interval is established corresponding to the energy (or
time) limits of the problem.

Use: Optional. Use only with WWN card. See the WWGE card for use with
the weight-window generator.

## Details:

- 1 Parameter e k accepts time entries to allow backward compatibility. See WWT card for time-dependent weight windows.

## 5.12.3.2 WWT: Weight-window Times

The WWT card defines the time intervals in shakes for which weight-
window bounds will be specified on the WWN card. The minimum time is not
entered on the WWT card, but is defined to be -∞ .

```
Data-card Form: WWT: P t 1 t 2 . . . t K P Particle designator. t k Upper time bound of k th window. Restriction: 1 ≤ k ≤ 99 t k -1 Lower time bound of k th window.
```

Default: One weight-window time interval.

Use: Optional. Use only with WWN card. See WWGT card for use with the
weight-window generator.

## 5.12.3.3 WWN: Cell-based Weight-window Lower Bounds

The WWN card specifies the lower weight bound of the space-, time-, and
energy-dependent weight windows in cells. It must be used with the WWP
card and, if the weight windows are energy and/or time dependent, with
the WWE and/or WWT card. For a particular particle type, both IMP and
WWN cards should not be used with one exception: mesh-based weight
windows require the presence of IMP cards (see the IMP card default
value discussion). The weight-window game turns off the IMP card game
unless the weight-window phase-space region has a lower bound of 0-then
the weight cutoff game, which uses the IMP values to scale the cutoff
values, is played.

In terms of the weight window, particle weight bounds are always
absolute and not relative; the user must explicitly account for weight
changes from any other variance reduction techniques such as source
biasing. The user must specify one lower weight bound per cell per
energy per time interval. There must be no holes in the specification;
that is, if WWN i is specified, WWN k for 1 &lt; k &lt; i must also be
specified.

<!-- image -->

Default: None.

Use: Either cell importance [§5.12.1] or weight windows must be supplied
to MCNP6.

1

2

3

4

## Details:

- 1 If wi j &gt; 0 , particles entering or colliding in the cell are split or rouletted based on the conditions setup by the WWP card parameters.
- 2 If wi j = 0 , the weight-window game is turned off in cell j for energy or time bin i and the weight cutoff game is turned on with a 1-for-2 roulette limit. Sometimes it is useful to specify the weight cutoffs on the CUT card as the lowest permissible weights desired in the problem. Otherwise, too many particles entering cells with wi j = 0 may be killed by the weight cutoff. Usually, the 1-for-2 roulette limitation is sufficient to use the default weight cutoffs, but caution is needed and the problem output file should be examined carefully. The capability to turn the weight-window game off in various phase-space regions is useful when these regions cannot be characterized by a single importance function or set of weight-window bounds.
- 3 Caution should be exercised when one energy (or time) group out of many groups is set to -1 . If the intent is to kill only low-energy particles, this may be okay; otherwise, it may be better to set all groups to -1 .

## 5.12.3.4 Example 1

| WWE:N e1 e2 e3         |
|------------------------|
| WWN1:N w11 w12 w13 w14 |
| WWN2:N w21 w22 w23 w24 |
| WWN3:N w31 w32 w33 w34 |

These cards define three energy intervals and the weight-window bounds
for a four-cell neutron problem.

## 5.12.3.5 Example 2

## WWN1:P w11 w12 w13

This card, without an accompanying WWE card, defines an energy- or time-
independent photon weight window for a three-cell problem.

## 5.12.3.6 WWP: Weight-window Parameters

The WWP card contains parameters that control various aspects of the
weight-window game.

## /warning\_sign Caution

The default mwhere treatment for weight windows has been observed to
lead to potentially silent wrong answers with UM geometry or, more
clearly, seemingly unrelated issues such as the code reporting negative
emission energy following certain collisions. If one must use weight
windows with UM, it is recommended that mwhere = -1 be set to avoid such
issues, which arise because of particle-banking behavior as particles
enter and exit UM pseudocells.

1

| Data-card Form:   | WWP : P wupn wsurvn mxspln mwhere switchn mtime wnorm etsplt wu nfmp                                                                                                                                                                                                                                                                                                             | WWP : P wupn wsurvn mxspln mwhere switchn mtime wnorm etsplt wu nfmp                                                                                                                                                                                                                                                                                                             |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P                 | Particle designator.                                                                                                                                                                                                                                                                                                                                                             | Particle designator.                                                                                                                                                                                                                                                                                                                                                             |
| wupn              | Multiplier to define the weight window upper limit. If the particle weight goes above wupn times the lower weight bound, the particle will be split. Restriction: wupn ≥ 2 (DEFAULT: wupn = 5 )                                                                                                                                                                                  | Multiplier to define the weight window upper limit. If the particle weight goes above wupn times the lower weight bound, the particle will be split. Restriction: wupn ≥ 2 (DEFAULT: wupn = 5 )                                                                                                                                                                                  |
| wsurvn            | Multiplier to define the maximum Russian roulette survival weight within the window. If the particle survives the Russian roulette game, its weight becomes min( wsurvn × w L ,w × mxspln ) , where w L is the lower-weight bound and w is the original weight. Restriction: 1 < wsurvn < wupn . DEFAULT: wsurvn = 0 . 6 × wupn , which defaults to three times the lower bound. | Multiplier to define the maximum Russian roulette survival weight within the window. If the particle survives the Russian roulette game, its weight becomes min( wsurvn × w L ,w × mxspln ) , where w L is the lower-weight bound and w is the original weight. Restriction: 1 < wsurvn < wupn . DEFAULT: wsurvn = 0 . 6 × wupn , which defaults to three times the lower bound. |
| mxspln            | Maximum number of integer splits. No particle will ever be split more than mxspln -for-one or be rouletted more harshly than one-in- mxspln . Restriction: mxspln > 1 (DEFAULT: mxspln = 5 ).                                                                                                                                                                                    | Maximum number of integer splits. No particle will ever be split more than mxspln -for-one or be rouletted more harshly than one-in- mxspln . Restriction: mxspln > 1 (DEFAULT: mxspln = 5 ).                                                                                                                                                                                    |
| mwhere            | Controls where to check a particle's weight ( 5 ). If                                                                                                                                                                                                                                                                                                                            | Controls where to check a particle's weight ( 5 ). If                                                                                                                                                                                                                                                                                                                            |
|                   | mwhere = - 1                                                                                                                                                                                                                                                                                                                                                                     | check the weight at collisions only.                                                                                                                                                                                                                                                                                                                                             |
|                   | mwhere = 0                                                                                                                                                                                                                                                                                                                                                                       | check the weight at surface crossings and collisions. (DEFAULT)                                                                                                                                                                                                                                                                                                                  |
|                   | mwhere = 1                                                                                                                                                                                                                                                                                                                                                                       | check the weight at surface crossings only.                                                                                                                                                                                                                                                                                                                                      |
| switchn           | Controls where to get the lower weight-window bounds. If                                                                                                                                                                                                                                                                                                                         | Controls where to get the lower weight-window bounds. If                                                                                                                                                                                                                                                                                                                         |
|                   | switchn < 0                                                                                                                                                                                                                                                                                                                                                                      | get the lower weight-window bounds from an external WWINP file containing either cell- or mesh-based lower weight-window bounds. Requires an IMP card ( 1 ).                                                                                                                                                                                                                     |
|                   | switchn = 0                                                                                                                                                                                                                                                                                                                                                                      | get the lower weight-window bounds from WWN i cards present in the MCNP input file ( 2 ). (DEFAULT)                                                                                                                                                                                                                                                                              |
|                   | switchn > 0                                                                                                                                                                                                                                                                                                                                                                      | set the lower weight-window bounds equal to switchn divided by the cell importance from the IMP card ( 3 ).                                                                                                                                                                                                                                                                      |
| mtime             | Controls treatment of WWE card. This parameter remains to allow backward compatibility. See WWT card for time-dependent weight windows. If                                                                                                                                                                                                                                       | Controls treatment of WWE card. This parameter remains to allow backward compatibility. See WWT card for time-dependent weight windows. If                                                                                                                                                                                                                                       |
|                   | mtime = 0                                                                                                                                                                                                                                                                                                                                                                        | energy-dependent windows are provided on the WWE card. (DEFAULT)                                                                                                                                                                                                                                                                                                                 |
|                   | mtime = 1                                                                                                                                                                                                                                                                                                                                                                        | time-dependent windows are provided on the WWE card.                                                                                                                                                                                                                                                                                                                             |
| wnorm             | Weight-window normalization factor. If wnorm > 0 , wnorm is a multiplicative constant for all lower weight-window bounds on WWN i: P cards or values in the WWINP file. Applies to particle type P specified by this WWP card. (DEFAULT: wnorm = 1 )                                                                                                                             | Weight-window normalization factor. If wnorm > 0 , wnorm is a multiplicative constant for all lower weight-window bounds on WWN i: P cards or values in the WWINP file. Applies to particle type P specified by this WWP card. (DEFAULT: wnorm = 1 )                                                                                                                             |
| etsplt            | Energy- and time-splitting control. If                                                                                                                                                                                                                                                                                                                                           | Energy- and time-splitting control. If                                                                                                                                                                                                                                                                                                                                           |
|                   | etsplt = 0                                                                                                                                                                                                                                                                                                                                                                       | then any entries on the ESPLT and TSPLT cards are used solely to scale the weight window. (DEFAULT)                                                                                                                                                                                                                                                                              |

```
etsplt = 1 then any entries on the ESPLT and TSPLT cards are used to split/roulette particles as well as scale the weight windows. wu Limits the maximum lower weight-window bound for any particle, energy, or time to wu . If wu = 0 , there is no limit ( 4 ). (DEFAULT: wu = 0 ) nmfp Number of mean-free paths to travel before checking mesh-based weight windows for neutron and photon problems only ( 5 ). (DEFAULT: nmfp = 1 )
```

Default: wupn = 5 ; wsurvn = 3 ; mxspln = 5 ; mwhere = 0 ; switchn = 0 ;
mtime = 0 ; wnorm = 1 . 0 ; etsplt = 0 ; wu = 0 ; nmfp = 1

Use: Weight windows are required unless importance are used.

## Details:

- 1 If switchn &lt; 0 , an external WWINP file with either cell- or mesh-based lower weight-window bounds must exist and an IMP card is required. The WWINP file is a weight-window generator output file, either WWOUT or WWONE , that has been renamed in the local file space or equivalenced on the execution line using WWINP = filename . The different formats of the WWINP file will indicate to the code whether the weight windows are cell or mesh based. For mesh-based weight windows, the mesh geometry will also be read from the WWINP file [Appendix A].
- 2 If switchn is zero, the lower weight-window bounds must be specified with the WWN cards present in the MCNP input file.
- 3 An energy-independent weight window can be specified using existing importance from the IMP card and setting the fifth entry ( switchn ) on the WWP card to a positive constant C . If this option is selected, the lower weight bounds for the cells become C/I , where I is the cell importance. A suggested value for C is one in which source particles start within the weight window, such as 0.25 times the source weight. If that is not possible, the window is probably too narrow or the source should be re-specified. Having switchn &gt; 0 and also having WWN i cards is a fatal error.
- 4 Unreasonably high weight-window bounds can be generated if (1) tracks that pass through a cell score only rarely or score very low, or (2) adjoint Monte Carlo is used. When weight windows with very high bounds are used in a subsequent run, the ultra-high windows will roulette nearly all particles in those phase-space regions. This results in no future estimate in these regions by the weight-window generator and potentially biased results. Use the 9th entry, wu , to limit the maximum lower weight-window bound. A good value of wu is often 1-10 times the maximum source weight.
- 5 Weight window processing is always performed during source emission (though source particles should start with weights consistent with the local window to avoid immediate splitting or rouletting). The mwhere parameter controls weight-window processing during collision or surface-crossing events that take place during particle transport. Similarly, the nmfp parameter controls weight-window processing following free flight for a specified number of mean-free paths when using mesh-based weight windows as long as no other event has taken place (setting nmfp to a high number effectively disables this behavior).

## 5.12.4 Stochastic Weight-window Generator Cards

The weight-window generator estimates the importance of the space-
energy-time regions of phase space specified by the user. The space-
energy-time weight-window lower bounds are then calculated inversely
proportional to the importance.

The cell-based generator estimates the average importance of a phase-
space cell. Inadequately sized (i.e., large) geometry cells often lead
to inappropriate weight windows because of a large variation in the
importance inside the cell. An appropriate user action is to refine the
cell definitions or use the mesh-based weight window. Inadequate
geometry specification for weight-window purposes also results when
there are large importance differences between adjacent cells.
Fortunately, the code provides information about whether the geometry
specification is adequate for sampling purposes by printing to the MCNP
output file a list of neighboring cells that differ by a factor of 4 or
more. If geometries are inadequately subdivided by the geometry cells,
mesh-based weight windows should be used.

The user is advised to become familiar with weight windows [§2.7.2.12],
before trying to use the weight-window generator.

## 5.12.4.1 WWG: Weight-window Generation

The WWG card allows the code to generate an importance function for a
user-specified tally (input parameter i t ). Because the weight-window
bounds are estimated quantities, they should be well converged or else
they can cause more harm than good. When well converged, they can
improve efficiency substantially. Note that the number of histories per
minute is often lower in the more efficient problem because more time is
spent sampling important regions of the problem phase space. Moreover,
in many cases, a window using the adjoint function will not be too far
from optimal.

For the cell-based weight-window generator, the code creates WWE and WWN
i cards that are printed, evaluated, and summarized in the MCNP output
file and written to the weight-window generator output file WWOUT .

For the mesh-based weight-window generator, the code writes the weight-
window lower bounds and a mesh description only to the WWOUT file. The
format of the mesh-based WWOUT file is provided in Appendix A.

In either case, the generated weight-window information can be easily
used in subsequent runs using switchn &lt; 0 on the WWP card. For many
problems, the weight-window generator results are superior to anything
an experienced user can guess and then input on an IMP card. To generate
energy- and/or time-dependent weight windows, use the WWGE and/or WWGT
cards.

<!-- image -->

```
i e = 0 then interpret WWGE card entries as energy bins. (DEFAULT: i e = 0 ) i e = 1 then interpret WWGE card entries as time bins.
```

Default: No weight-window values are generated.

Use: Optional.

## Details:

- 1 Weight-window generation relies on scores being made by the primary source particle to or near (so secondary particles can score) the reference tally, i t . The primary source particle is typically specified by PAR on the SDEF card. If PAR is a distribution or unspecified, then the primary source particle is the particle with the lowest number on the MODE card.
- 2 For mesh-based weight windows, a reference point ( REF ) is required instead of a cell number. See the MESH card.
- 3 The value w g of the lower weight-window bound for reference cell i c or reference mesh location is chosen so that the source weight will start within the weight window, when possible. The reference cell i c is often chosen as the source cell and the reference mesh location is often chosen in or near the source cell.

## 5.12.4.2 WWGE: Weight-window Generation Energies (or Times)

If the WWGE card is present, energy- (or time-) dependent weight windows
are generated and written to the WWOUT file and, for cell-based weight
windows, to the MCNP output file. In addition, single-group energy(or
time-) independent weight windows are written to a separate output file,
WWONE . Energy- (or time-) independent weight windows are sometimes
useful for trouble-shooting the energy- (or time-) dependent weight
windows on the WWOUT file. The WWONE file format is the same as that of
the WWOUT file [Appendix A]. The selection of energy- or time-dependent
weight windows is made with the 8th entry on the WWG card.

<!-- image -->

Default: If the WWGE card is omitted and the weight window is used, a
single energy (time) interval will be established corresponding to the
energy (time) limits of the problem being run. If the card is present
but has no entries, ten energy (time) bins will be generated with
energies (times) of e k = 10 k -8 MeV (or shakes), for i = 1 , 2 , . . .
, 10 . Both the single energy (time) and the energy- (time-) dependent
windows are generated.

Use: Optional.

## Details:

- 1 Although the WWGE card will accept time bins so to be compatible with previous versions of the MCNP code, it is recommended that the user use the WWGT card for time-dependent weight-window generation.

## 5.12.4.3 WWGT: Weight-window Generation Times

If the WWGT card is present, time-dependent weight windows are generated
and written to the WWOUT file and, for cell-based weight windows, to the
MCNP output file. In addition, single-group time-independent weight
windows are written to a separate output file, WWONE . Time-independent
weight windows are sometimes useful for trouble-shooting the time-
dependent weight windows on the WWOUT file. The WWONE file format is the
same as that of the WWOUT file [Appendix A].

```
Data-card Form: WWGT: P t 1 t 2 . . . t K P Particle designator. t k Upper time bound for weight-window group to be generated, t k +1 > t k . Units are shakes. Restriction: k ≤ 15 .
```

Default: If the WWGT card is omitted and the weight window is used, a
single time interval will be established corresponding to the time
limits of the problem being run. If the card is present but has no
entries, ten time bins will be generated with times of t k = 10 k -8
shakes, for i = 1 , 2 , . . . , 10 . Both the single time and the time-
dependent windows are generated.

Use: Optional.

## 5.12.4.4 Example 1

```
1 WWG 111 45 0.25 2 WWGE:p 1 100 3 WWGT:p 1 100 1.e20
```

The cell-based windows generated from the above cards would look like:

```
1 WWP:p 5 3 5 2 WWE:p 1 100 3 WWT:p 1 100 1.e20 4 WWN1:p w1 w2 w3 ... $ energy 1 time 1 5 WWN2:p w1 w2 w3 ... $ energy 2 time 1 6 WWN3:p w1 w2 w3 ... $ energy 1 time 2 7 WWN4:p w1 w2 w3 ... $ energy 2 time 2 8 WWN5:p w1 w2 w3 ... $ energy 1 time 3 9 WWN6:p w1 w2 w3 ... $ energy 2 time 3
```

This example generates a 2-energy group, 3-time group weight window. In
particular, the WWG card would generate weight windows to optimize tally
111. The lowest weight-window bound in any energy-time bin group in cell
45 (the reference cell) would be 0.25. The WWGE and WWGT cards would
generate two energy bins and three time bins for photons.

## 5.12.4.5 MESH: Superimposed Importance Mesh for Mesh-Based Weight-Window Generator

## Data-card Form: MESH keyword = value(s) ...

| GEOM   | Controls mesh geometry type. (DEFAULT: GEOM = XYZ ). If GEOM = XYZ or GEOM = REC mesh geometry is Cartesian.                                                                                                                                                  |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| REF    | x , y , and z coordinates of the reference point; used to create the normalization constant for the mesh-based weight-window generator. (DEFAULT: none) Restriction: Required.                                                                                |
| ORIGIN | x , y , and z coordinates, in MCNP6 cell geometry, of the origin (bottom, left, rear for rectangular; bottom center for cylindrical; center for spherical) of the superimposed mesh. (DEFAULT: ORIGIN = 0 ., 0 ., 0 ., )                                      |
| AXS    | Vector giving the direction of the (polar) axis of the cylindrical ( 1 ) or spherical mesh (DEFAULT: AXS = 0 ., 0 ., 1 ., )                                                                                                                                   |
| VEC    | Vector defining, in conjunction with AXS , the plane for θ = 0 . For spherical geometry, VEC must be orthogonal to φ . (DEFAULT: VEC = 1 ., 0 ., 0 ., )                                                                                                       |
| IMESH  | Locations of the coarse meshes in the x direction for rectangular geometry or in the r direction for cylindrical or spherical geometry ( 2 , 3 , 4 ). (DEFAULT: none)                                                                                         |
| IINTS  | Number of fine meshes within corresponding coarse meshes in the x direction for rectangular geometry or in the r direction for cylindrical or spherical geometry ( 6 , 7 ). (DEFAULT: IINTS = 1 fine mesh in each coarse mesh)                                |
| JMESH  | Locations of the coarse meshes in the y direction for rectangular geometry, in the z direction for cylindrical geometry, or the φ polar angle bounds for spherical geometry ( 2 , 3 , 4 , 5 ). (DEFAULT: none)                                                |
| JINTS  | Number of fine meshes within corresponding coarse meshes in the y direction for rectangular geometry, in the z direction for cylindrical geometry, or in the φ direction for spherical geometry ( 6 , 7 ). (DEFAULT: JINTS = 1 fine mesh in each coarse mesh) |
| KMESH  | Locations of the coarse meshes in the z direction for rectangular geometry or in the θ direction for cylindrical or spherical geometry ( 2 , 3 , 4 , 5 ). (DEFAULT: none)                                                                                     |
| KINTS  | Number of fine meshes within corresponding coarse meshes in the z direction for rectangular geometry or in the θ direction for cylindrical or spherical geometry ( 6 , 7 ). (DEFAULT: KINTS = 1 fine mesh in each coarse mesh)                                |

Use: Required to generate mesh-based weight windows; not required to use
without weight-window generation. This card is also used to generate a
structured discrete-ordinates-style geometry file.

## Details:

- 1 For a cylindrical mesh, the AXS and VEC vectors need not be orthogonal but they must not be parallel; the one half-plane that contains them and the ORIGIN point will define θ = 0 . The AXS vector will remain fixed. The length of the AXS or VEC vectors must not be zero.
- 2 For both the cylindrical and spherical meshes, the lower radial and angular mesh bounds ( r, φ, θ ) are implicitly zero.
- 3 The location of the n th coarse mesh in the u direction ( ru n in what follows) is given in terms of the most positive surface in the u direction. For a rectangular mesh, the coarse mesh locations ( rx n , ry n , rz n ) are given as planes perpendicular to the x , y , and z axes, respectively, in the MCNP6 cell coordinate system; thus, the ORIGIN point ( x 0 , y 0 , z 0 ) is the most negative point of the mesh. For a cylindrical mesh, ORIGIN ( r 0 , z 0 , θ 0 ) corresponds to the bottom center point and, for a spherical mesh, ORIGIN ( r 0 , φ 0 , θ 0 ) corresponds the sphere center. The coarse mesh locations must increase monotonically.
- 4 In the XYZ ( REC ) mesh, the IMESH , JMESH , and KMESH are the actual ( x, y, z ) coordinates. In the RZT ( CYL ) mesh, IMESH (radius) and JMESH (height) are relative to ORIGIN and KMESH ( θ ) is relative to VEC . In the RPT ( SPH ) mesh, IMESH (radius) is relative to ORIGIN , JMESH ( φ ) is relative to AXS , and KMESH ( θ ) is relative to VEC .
- 5 Polar and azimuthal angles may be specified in revolutions ( 0 ≤ φ ≤ 0 . 5 and 0 ≤ θ ≤ 1 ), radians, or degrees. MCNP6 recognizes the appropriate units by looking for 0.5, 3.14, or 180 for the last spherical geometry JMESH entry and for 1, 6.28, or 360 for the last spherical or cylindrical KMESH entry.
- 6 The fine meshes are evenly distributed within the n th coarse mesh in the u direction. The mesh in which the reference point lies becomes the reference mesh cell for the mesh-based weight-window generator; this reference mesh cell is analogous to the reference cell used by the cell-based weight-window generator. The mesh cell containing the REF point will have its (over energy) weight-window lower bound equal to the third entry on the WWG card.
- 7 The code uses a default value of 1 fine mesh per coarse mesh if IINTS , JINTS , or KINTS keywords are omitted. If IINTS , JINTS , or KINTS keywords are present, the number of entries must match the number of entries on the IMESH , JMESH , and KMESH keywords, respectively. Entries on the IINTS , JINTS , and KINTS keywords must be greater than zero.

## 5.12.4.5.1 Using an Existing Superimposed Mesh

A second method of providing a superimposed mesh is to use one that
already exists, written either to the WWOUT file or to the WWONE file.
To implement this method, use the WWG card with i c = 0 in conjunction
with the MESH card where the only keyword is REF . The reference point
must be within the superimposed mesh and must be provided because there
is no reference point in either WWOUT or WWONE . If the mesh-based
weight-window generator is invoked by this method, MCNP6 expects to read
a file called WWINP . The WWINP file is a weight-window generator output
file, either WWOUT or WWONE , that has been renamed in the local file
space or equivalenced on the execution line using WWINP = filename
[Appendix A].

It is not necessary to use mesh-based weight windows from the WWINP file
in order to use the mesh from that file. Furthermore, previously
generated mesh-based weight windows can be used ( WWP card with switchn
&lt; 0 and WWINP file in mesh format) while the mesh-based weight-window
generator is simultaneously generating weight windows for a different
mesh (input on the MESH card). However, it is not possible to read mesh-
based weight windows from one file and a weight-window generation mesh
from a different file.

1

2

3

4

5

6

7

1

2

3

1

2

3

4

5

## 5.12.4.5.2 Hints and Guidelines Regarding Superimposed Mesh Creation

The superimposed mesh should fully cover the problem geometry; i.e., the
outer boundaries of the mesh should lie outside the outer boundaries of
the geometry, rather than being coincident with them. This requirement
guarantees that particles remain within the weight-window mesh. A line
or surface source should not be made coincident with a mesh surface. A
point source should never be coincident with the intersection of mesh
surfaces. In particular, a line or point source should never lie on the
axis of a cylindrical mesh. These guidelines also apply to the WWG
reference point specified using the REF keyword.

If a particle does escape the weight-window mesh, the code prints a
warning message giving the coordinate direction and surface number (in
that direction) from which the particle escaped. The code prints the
total number of particles escaping the mesh (if any) after the tally
fluctuation charts in the standard output file. If a track starts
outside the mesh, the code prints a warning message giving the
coordinate direction that was missed and which side of the mesh the
particle started on. The code prints the total number of particles
starting outside the mesh (if any) after the tally fluctuation charts in
the standard output file.

Specifying i c = 0 on the WWG card with no MESH card is a fatal error.
If AXS or VEC keywords are present and the mesh is rectangular, a
warning message is printed and the keyword is ignored. If there are
fatal errors and the FATAL option is on, weight-window generation is
disabled.

## 5.12.4.5.3 Example 1

```
MESH GEOM=CYL REF=1e-6 1e-7 0 ORIGIN=1 2 3 IMESH 2.55 66.34 IINTS 2 15 $ 2 fine bins from 0 to 2.55, 15 from 2.55 to 66.34 JMESH 33.1 42.1 53.4 139.7 JINTS 6 3 4 13 KMESH 0.5 1 KINTS 5 5
```

## 5.12.4.5.4 Example 2

```
MESH GEOM=REC REF=1e-6 1e-7 0 ORIGIN=-66.34 -38.11 -60 IMESH -16.5 3.8 53.66 IINTS 10 3 8 $ 10 fine bins from -66.34 to -16.5, etc.
```

## 5.12.4.5.5 Example 3

```
MESH GEOM sph ORIGIN 7 -9 -12 REF -23 39 -10 AXS 0.4 -0.5 0.2 VEC 0.1 -0.2 -0.7 IMESH 60. IINTS 3 JMESH 0.1 0.35 0.5 JINTS 1 1 1 KMESH 0.2 0.85 1 KINTS 1 1 1
```

In this example a spherical mesh is located at ORIGIN = 7 -9 -12 . The
reference location in the ( x, y, z ) coordinate system of the problem
is at REF = -23 39 -10 . The weight-window generator lower weight-window
bound will be W for whatever mesh cell contains this location, where W
is half the source weight by default or whatever is the 3rd entry on the
WWG weight-window generator card. The polar ( φ ) axis of the spherical
mesh (as in latitude on the globe) is AXS = 0 . 4 -0 . 5 0 . 2 , which
MCNP6 will normalize to a unit vector. The azimuthal planes (as in
longitude on a globe, or cylindrical mesh theta bins) are measured
relative to the azimuthal vector, theta ( θ ), VEC = 0 . 1 -0 . 2 -0 . 7
. VEC will also be renormalized by MCNP6 and must be orthogonal to φ .
The radial mesh bins have three interpolates between 0 and 60-that is,
the mesh bounds are at 0, 20, 30, and 60 cm. The polar angles ( φ ) are
at 0.1, 0.35, and 0.5 revolutions from the AXS vector. The azimuthal
angles ( θ ) are at 0.2, 0.85, and 1 revolutions from the VEC vector.
Note that 0 ≤ φ ≤ 0 . 5 and 0 ≤ θ ≤ 1 are always required.

Examples that show how to plot superimposed weight-window meshes are
given in §6.4.6.

## 5.12.5 ESPLT: Energy Splitting and Roulette

The ESPLT card allows problem-wide splitting and Russian roulette of
particles in energy, similar to how the IMP card allows splitting and
Russian roulette as a function of geometry for continuous-energy
calculations. The changes to a particle's weight caused by the ESPLT
card will create compensating weight adjustments to the weight cutoff
and weight-window values.

| Data-card Form: ESPLT: P r 1 e 1 . . . r K e K   | Data-card Form: ESPLT: P r 1 e 1 . . . r K e K                                                                                                                                                                                                                                                                                                                                                                                                            | Data-card Form: ESPLT: P r 1 e 1 . . . r K e K                                                                                                                                                                                                                                                                                                                                                                                                            |
|--------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P                                                | Particle designator.                                                                                                                                                                                                                                                                                                                                                                                                                                      | Particle designator.                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| r k                                              | Provides splitting/roulette ratios at each energy boundary, e k , for decreasing energy. The meanings of the r k differ depending on whether or not there is a weight window present for the particle type P . These splitting/roulette ratios are internally converted in the code to an absolute importance function with an r 0 = 1 inserted to set the importance to unity for energies greater than the maximum of the e k . Restriction: 1 ≤ k ≤ 20 | Provides splitting/roulette ratios at each energy boundary, e k , for decreasing energy. The meanings of the r k differ depending on whether or not there is a weight window present for the particle type P . These splitting/roulette ratios are internally converted in the code to an absolute importance function with an r 0 = 1 inserted to set the importance to unity for energies greater than the maximum of the e k . Restriction: 1 ≤ k ≤ 20 |
|                                                  | When weight windows are not used, and if the energy of a particle of type P falls below e k (decreasing energy), then when                                                                                                                                                                                                                                                                                                                                | When weight windows are not used, and if the energy of a particle of type P falls below e k (decreasing energy), then when                                                                                                                                                                                                                                                                                                                                |
|                                                  | r k > 1                                                                                                                                                                                                                                                                                                                                                                                                                                                   | r k is the number of tracks into which a particle will be split.                                                                                                                                                                                                                                                                                                                                                                                          |
|                                                  | 0 < r k < 1                                                                                                                                                                                                                                                                                                                                                                                                                                               | r k is the probability of Russian roulette.                                                                                                                                                                                                                                                                                                                                                                                                               |
|                                                  | r k = 1                                                                                                                                                                                                                                                                                                                                                                                                                                                   | there is no action.                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|                                                  | If the energy of a particle of type P increases in energy above e k , then when                                                                                                                                                                                                                                                                                                                                                                           | If the energy of a particle of type P increases in energy above e k , then when                                                                                                                                                                                                                                                                                                                                                                           |
|                                                  | 1 / r k > 1                                                                                                                                                                                                                                                                                                                                                                                                                                               | 1 / r k is the number of tracks into which a particle will be split.                                                                                                                                                                                                                                                                                                                                                                                      |
|                                                  | 0 < 1 / r k < 1                                                                                                                                                                                                                                                                                                                                                                                                                                           | 1 / r k is the probability of Russian roulette.                                                                                                                                                                                                                                                                                                                                                                                                           |
|                                                  | Exception: if the first r 1 < 0 , then no game is played on energy increases. When weight windows are specified, then the energy splitting is accomplished solely with the weight windows ( 1 ). The r k in this case are energy importance modifications to the weight window. If                                                                                                                                                                        | Exception: if the first r 1 < 0 , then no game is played on energy increases. When weight windows are specified, then the energy splitting is accomplished solely with the weight windows ( 1 ). The r k in this case are energy importance modifications to the weight window. If                                                                                                                                                                        |
|                                                  | • the energy of a particle of type P falls below e k , then the existing weight windows will be adjusted by dividing the windows by r k .                                                                                                                                                                                                                                                                                                                 | • the energy of a particle of type P falls below e k , then the existing weight windows will be adjusted by dividing the windows by r k .                                                                                                                                                                                                                                                                                                                 |

e

k

- the energy of a particle of type P increases above e k , then the weight windows are multiplied by r k .
- more than one energy boundary is crossed, the windows are adjusted by the product of the r k values.

Energy (MeV) at which particles are to undergo splitting or Russian
roulette. Values must be monotonically increasing. Restriction: 1 ≤ k ≤
20

Default: Energy splitting will not occur for a given particle type
unless this card is defined.

## /warning\_sign Caution

The ESPLT card was originally designed with the intent that it be used
with a time-dependent weight window. The ESPLT card is not recommended
for an energy-dependent weight window as these two cards may interfere
with one another (see the discussion in the table above). However, the
code does not prevent the user from invoking both at the same time.
Instead of a single-range weight window and an ESPLT card, consider
using an energy-dependent weight window.

## Details:

- 1 If the eighth entry on the WWP card is 1 (0 is the default), then in addition to the weight-window adjustment, the particle will be explicitly split or rouletted upon crossing e i , just as is the case without a weight window. It is anticipated that the default will be appropriate for almost all problems.

## 5.12.5.1 Additional Information Regarding ESPLT

The entries on the ESPLT card consist of pairs of energy-importance
ratio parameters, r k and e k , with a maximum of twenty pairs allowed.
A warning message is issued if the e k are not monotonically increasing.
The value of r k can be non-integer and also can be between 0 and 1. For
an energy decrease below an e k with an associated r k greater than 1,
particle splitting will occur. For a value of r k between 0 and 1, r k
becomes the survival probability in the Russian roulette game. For an
energy increase above an e k with an associated 1 / r k greater than 1,
particle splitting will occur. For a value of 1 / r k between 0 and 1, 1
/ r k becomes the survival probability in the Russian roulette game. If
a particle's energy becomes less than e k , the specified splitting or
roulette is sampled. If more than one energy boundary is passed during a
particle trajectory, the product of the r k values is used to determine
the outcome.

If the particle's energy falls below e k , the specified splitting or
roulette always occurs. If the particle's energy increases above e k ,
the inverse game is normally played (unless r 1 has been specified as
less than zero). For example, suppose roulette is specified at 0.1 MeV
with a survival probability of 0.5; if a particle's energy increases
above 0.1 MeV, then it is split 2-for-1.

A neutron's energy may increase by fission or from thermal up-
scattering. There are cases when it may not be desirable to have the
splitting or roulette game played on energy increases (particularly in a
fission-dominated problem). If r 1 &lt; 0 , then splitting or roulette will
be played only for energy decreases and not for energy increases.

1

1

2

## 5.12.5.2 Example 1

ESPLT:N 2 0.1 2 0.01 0.25 0.001

This example specifies a 2-for-1 split when the neutron energy falls
below 0.1 MeV, another 2-for-1 split when the energy falls below 0.01
MeV, and Russian roulette when the energy falls below 0.001 MeV with a
25% chance of surviving. Thus, a neutron that enters a collision at 0.5
MeV and exits at 0.005 MeV will be split 4-to-1.

## 5.12.5.3 Example 2

```
1 ESPLT:N 2 0.1 2 0.01 0.25 0.001 2 WWP:N 5 3 5 0 0 0 J J
```

This example divides the weight windows by 2 when the energy falls below
0.1 MeV, divides by 2 again when the energy falls below 0.01 MeV, and
divides by 0.25 when the energy falls below 0.001 MeV.

## 5.12.5.4 Example 3

```
ESPLT:N 2 0.1 2 0.01 0.25 0.001 WWP:N 5 3 5 0 0 0 J 1
```

This example is similar to §5.12.5.3 except that the eighth entry on the
WWP card ( etsplt ) is set to 1. Consequently, in addition to the
weight-window adjustment, the particle will be explicitly split or
rouletted upon crossing e k . For this example, the weight windows will
be divided by 2 when the energy falls below 0.1 MeV, divided by 2 again
when the energy falls below 0.01 MeV, and divided by 0.25 when the
energy falls below 0.001 MeV. In addition, a 2-for-1 split will occur
when the neutron energy falls below 0.1 MeV, another 2-for-1 split will
happen when the neutron energy falls below 0.01 MeV, and Russian
roulette with a survival probability of 0.25 will be played when the
neutron energy falls below 0.001 MeV.

## 5.12.6 TSPLT: Time Splitting and Roulette

The TSPLT card allows problem-wide splitting and Russian roulette of
particles in time, like the IMP card allows splitting and Russian
roulette as a function of geometry. The TSPLT card can be used in all
problems except multigroup problems. The changes to a particle's weight
caused by the TSPLT card will create compensating weight adjustments to
the weight cutoff and weight-window values.

| Data-card Form: TSPLT: P r 1 t 1 . . . r K t K   | Data-card Form: TSPLT: P r 1 t 1 . . . r K t K                                                                                                                                                                                   |
|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P                                                | Particle designator ( 1 ).                                                                                                                                                                                                       |
| r k                                              | Provides splitting/roulette ratios at each time boundary, t k , for increasing time. These splitting/roulette ratios are internally converted in the code to an absolute importance function with an r 0 = 1 inserted to set the |

t k importance to unity for times less than the minimum of the r k .
Restriction: 1 ≤ k ≤ 20

When weight windows are not used, and if

| r k > 1     | r k is the number of tracks into which a particle will be split.   |
|-------------|--------------------------------------------------------------------|
| 0 < r k < 1 | r k is the probability of Russian roulette.                        |
| r = 1       | there is no action.                                                |

k

When weight windows are specified, then the time splitting/roulette is
accomplished solely with the weight windows ( 2 ). The r k in this case
are time importance modifications to the weight window. If

- the particle crosses t k , the existing weight windows will be adjusted by dividing the windows by r k .
- more than one time boundary is crossed, the windows are divided by the product of the r k values.

Time (shakes) at which particles are to undergo splitting or Russian
roulette. Values must be monotonically increasing. Restriction: 1 ≤ k ≤
20

Default: Omission of this card means that time splitting will not take
place for those particles for which the card is omitted.

Use: Optional. Cannot be used in multigroup calculations.

## /warning\_sign Caution

The TSPLT card is intended to be used with an energy-dependent weight
window. The TSPLT card is not recommended for a time-dependent weight
window as these two cards may interfere with one another. However, the
code does not prevent the user from invoking both at the same time.
Instead of a single-range weight window and a TSPLT card, consider using
a time-dependent weight window.

## Details:

- 1 Normally in a coupled mode problem (e.g., MODE N P ), if particle type P is important late in time, then all particles producing particle type P will also be important late in time. For these reasons, it is suggested that the user have a TSPLT card for each relevant particle type. Thus in a MODE N P problem, if a TSPLT:P card is specified then a TSPLT:N card would normally be specified as well.
- 2 If the eighth entry on the WWP card is 1 (0 is the default), then in addition to the weight-window adjustment, the particle will be explicitly time-split or rouletted upon crossing t k , just as is the case without a weight window. It is anticipated that the default will be appropriate for almost all problems.

## 5.12.6.1 Additional Information Regarding TSPLT

The entries on the TSPLT card consist of pairs of time-importance ratio
parameters, r k and t k , with a maximum of twenty pairs allowed. A
warning message is issued if the t k are not monotonically increasing.

1

1

2

1

2

The value of r k can be non-integer and also can be between 0 and 1. For
an r k greater than 1, particle splitting will occur. For a value of r k
between 0 and 1, r k becomes the survival probability in the Russian
roulette game. If a particle's time becomes greater than t k , the
specified splitting or roulette is sampled. If more than one time
boundary is passed during a particle trajectory, the product of the r k
values is used to determine the outcome. The t k are in units of shakes.

## 5.12.6.2 Example 1

TSPLT:N 2 100 2 1000 0.2 10000

This example specifies a 2-for-1 split when the neutron time exceeds 100
shakes, another 2-for-1 split when the time exceeds 1000 shakes, and
Russian roulette with a survival probability of 0.2 when the time
exceeds 10000 shakes. A neutron that crosses both 1000 and 10000 shakes
will have a survival probability of 0.4.

## 5.12.6.3 Example 2

TSPLT:N 2 100 2 1000 0.2 10000

WWP:N 5 3 5 0 0 0 J J

This example divides the weight windows by 2 when the neutron time
exceeds 100 shakes, divides by 2 again when the time exceeds 1000
shakes, and divides by 0.2 when the time exceeds 10000 shakes. Thus the
weight window will be divided by a factor of 4 for a particle whose time
at the start of the transport step was 90 shakes and whose time at the
end of the transport step was 1010 shakes.

## 5.12.6.4 Example 3

TSPLT:N 2 100 2 1000 0.2 10000

WWP:N 5 3 5 0 0 0 J 1

This example is similar to §5.12.6.3 except that the eighth entry on the
WWP card ( etsplt ) is set to 1. Consequently, in addition to the
weight-window adjustment, the particle will be explicitly split or
rouletted when it exceeds t k . For this example the weight windows will
be divided by 2 when the neutron time exceeds 100 shakes, divided by 2
again when the time exceeds 1000 shakes, and divided by 0.2 when the
time exceeds 10000 shakes. In addition, this example specifies a 2-for-1
split when the neutron time exceeds 100 shakes, another 2-for-1 split
when the time exceeds 1000 shakes, and a Russian roulette survival
probability of 0.2 when the time exceeds 10000 shakes.

## 5.12.7 EXT: Exponential Transform

The exponential transform method [§2.7.2.13] stretches the path length
between collisions in a preferred direction by adjusting the total cross
section.

| Cell-Card Form: EXT : P a or Data-card Form: EXT : P a 1 a 2 ...   | Cell-Card Form: EXT : P a or Data-card Form: EXT : P a 1 a 2 ...                                                                                                                                                                                                                  |
|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P                                                                  | Particle designator.                                                                                                                                                                                                                                                              |
| a                                                                  | Each entry a is of the form a = QVm , where Q is the stretching parameter and Vm defines the stretching direction for the cell [Table 5.25].                                                                                                                                      |
| ak                                                                 | Each entry ak is of the form ak = QVm , where Q is the stretching parameter and Vm defines the stretching direction for the cell k [Table 5.25]. The number of entries need not equal the number of cells in the problem, but a warning message is printed if they are not equal. |

## Default: No transform,

ak = 0.

Use: Optional. Use cautiously. Weight windows are strongly recommended.
A warning message is given if weight windows are not present when the
exponential transform is used. The exponential transform should not be
used in the same cell as forced collisions or without good weight
control. The transform works best when the particle flux has an
exponential attenuation, such as in problems with highly absorbing
media.

## 5.12.7.1 The Stretching Parameter

The exponential transform method stretches the path length between
collisions in a preferred direction by adjusting the total cross section
as follows:

<!-- formula-not-decoded -->

where

Σ ∗ t is the artificially adjusted total cross section,

Σ t is the true total cross section,

p

µ

is the stretching parameter, and is the cosine of the angle between the
particle direction and the stretching direction.

The stretching parameter, p , can be specified by the stretching entry,
Q , in three ways. If

Q = 0 p = 0 and the exponential transform is not used.

Q = p 0 &lt; p &lt; 1 and a constant stretching parameter is specified.

Q

=

S

p

= Σ

c

/

Σ

t

where

Σ

c

is the capture cross section (as defined by nuclear engineers).

Letting p = Σ c / Σ t can be used for implicit capture along a flight
path, as described in §2.4.3.4.3 and §2.7.2.14.

The stretching direction is defined by the Vm part of each ak entry on
the EXT card with three available options:

1

2

Table 5.25: Exponential Transform Stretching Parameter

|   Cell | ak     | Q   | Vm   | Stretching Parameter   | Stretching Direction        |
|--------|--------|-----|------|------------------------|-----------------------------|
|      3 | 0.7V2  | 0.7 | V2   | p = 0 . 7              | Toward point (1 , 1 , 1)    |
|      4 | S      | S   |      | p = Σ c / Σ t          | Particle direction          |
|      5 | -SV2   | S   | -V2  | p = Σ c / Σ t          | Away from point (1 , 1 , 1) |
|      6 | -0.6V9 | 0.6 | -V9  | p = 0 . 6              | Away from origin            |
|      8 | 0.5V9  | 0.5 | V9   | p = 0 . 5              | Toward origin               |
|      9 | SZ     | S   | Z    | p = Σ c / Σ t          | Along + z axis              |
|     10 | -0.4X  | 0.4 | -X   | p = 0 . 4              | Along x axis                |

-

1. If the Vm part of the ak entry is omitted (i.e., ak = 0 for a given cell), then the stretching is in the particle direction ( µ = 1 ). This is not recommended unless implicit capture along a flight path is desired, in which case ak = S should be used so that the distance to scatter rather than the distance to collision is sampled.
2. The stretching direction may be specified as Vm , where m is a unique integer that is associated with the vector entry provided on the VECT card. The stretching direction is defined as the line from the collision point to the point ( x m , y m , z m ) , where ( x m , y m , z m ) is provided on the VECT card. The direction cosine µ is now the cosine of the angle between the particle direction and the line drawn from the collision point to point ( x m , y m , z m ) . The sign of ak governs whether stretching is toward or away from ( x m , y m , z m ) .
3. The stretching direction may also be specified as Vm = X or Y or Z , so the direction cosine µ is the cosine of the angle between the particle direction and the x , y , or z axis, respectively. The sign of ak governs whether stretching is toward or away from the x , y , or z axis.

## 5.12.7.2 Example 1

```
EXT:N 0 0 0.7V2 S -SV2 -0.6V9 0 0.5V9 SZ -0.4X VECT V9 0 0 0 V2 1 1 1
```

The 10 entries are for the 10 cells in this problem. Path length
stretching is not turned on for photons or for cells 1, 2, and 7. Table
5.25 is a summary of path length stretching in the other cells.

## 5.12.8 VECT: Vector Input

The entries on the VECT card are quadruplets that may define any number
of vectors for either the exponential transform or user patches. See the
EXT card for a usage example.

Data-card Form:

m,n xm

y m zm

Default: None.

Use: Optional.

VECT

V

m

xm y m

zm

. . .

V

n

xn y n

zn

Any number to uniquely identify vectors

Coordinate triplets to define vector

V

m

.

V

m

,

V

n

,

. . .

## 5.12.9 FCL: Forced Collision

The FCL card controls the forcing of neutron or photon collisions in
each cell. This is particularly useful for generating contributions to
point detectors or DXTRAN spheres. The weight-window game at surfaces is
not played when entering forced-collision cells.

Because the forced-collision variance reduction method can produce
several low-weight particles, the weight cutoff game is turned on by
default when using pulse-height tallies and forced collisions together.
Any of the default settings can be overridden by explicitly setting the
weight cutoffs on the CUT card.

<!-- image -->

| Cell-card Form: FCL: P = x or Data-card Form: FCL: P x 1 x 2 . . .   | Cell-card Form: FCL: P = x or Data-card Form: FCL: P x 1 x 2 . . .                                                               | Cell-card Form: FCL: P = x or Data-card Form: FCL: P x 1 x 2 . . .                                                                    |
|----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| P                                                                    | Particle designator. Restriction: Only neutrons ( N ) and photons ( P ) are permitted.                                           | Particle designator. Restriction: Only neutrons ( N ) and photons ( P ) are permitted.                                                |
| x                                                                    | Forced-collision control for cell ( 1 , 2 , 3 ). Restriction: - 1 ≤ x ≤ 1 . If                                                   | Forced-collision control for cell ( 1 , 2 , 3 ). Restriction: - 1 ≤ x ≤ 1 . If                                                        |
|                                                                      | x > 0                                                                                                                            | forced collision applies to particles entering the cell and to those surviving weight cutoff/weight-window games in the cell ( 4 ).   |
|                                                                      | x < 0                                                                                                                            | forced collision applies only to particles entering the cell ( 5 ).                                                                   |
|                                                                      | x = 0                                                                                                                            | no forced collision in the cell. (DEFAULT)                                                                                            |
| x k                                                                  | Forced-collision control for cell k ( 1 , 2 , 3 ). Restriction: - 1 ≤ x ≤ 1 . If                                                 | Forced-collision control for cell k ( 1 , 2 , 3 ). Restriction: - 1 ≤ x ≤ 1 . If                                                      |
|                                                                      | x k > 0                                                                                                                          | forced collision applies to particles entering the cell k and to those surviving weight cutoff/weight-window games in the cell ( 4 ). |
|                                                                      | x k < 0                                                                                                                          | forced collision applies only to particles entering the cell k ( 5 ).                                                                 |
|                                                                      | x k = 0                                                                                                                          | no forced collision in the cell k . (DEFAULT)                                                                                         |
|                                                                      | The number of entries need not equal the number of cells in the problem, but a warning message is printed if they are not equal. | The number of entries need not equal the number of cells in the problem, but a warning message is printed if they are not equal.      |

Default:

x k = 0 , no forced collisions.

Use: Optional. Exercise caution.

## Details:

- 1 If x k = 0 , all particles entering cell k are split into collided and un-collided parts with the appropriate weight adjustment. If | x k | &lt; 0 , Russian roulette is played on the collided parts with survival probability | x k | to keep the number of collided histories from getting too large. Fractional x k entries, rather than values of -1 or 1, are recommended if a number of forced-collision cells are adjacent to each other.

glyph[negationslash]

- 2 When cell-based weight-window bounds bracket the typical weight entering the cell, choose x k &gt; 0 . When cell-based weight-window bounds bracket the weight typical of forced-collision particles, choose x k &lt; 0 . For mesh-based windows, x k &gt; 0 usually is recommended. When using importance, x k &gt; 0 because x k &lt; 0 turns off the weight cutoff game.

- 3 Let x k = 1 or -1 unless a number of forced collision cells are adjacent to each other or the number of forced collision particles produced is higher than desired. Then fractional values are usually needed.
- 4 If x k &gt; 0 , the forced collision process applies both to particles entering cell k and to the collided particles surviving the weight cutoff or weight-window games. Particles will continue to be split into un-collided and (with probability | x k | ) collided parts until killed by either weight cutoff or weight windows.
- 5 If x k &lt; 0 , the forced collision process applies only to particles entering the cell. After the forced collision, the weight cutoff is ignored and all subsequent collisions are handled in the usual analog manner. Weight windows are not ignored and are applied after contributions are made to detectors and DXTRAN spheres.

## 5.12.10 DXT: DXTRAN Sphere

DXTRAN (which stands for deterministic transport) spheres are used to
improve the particle sampling in a given region of phase-space, a type
of angle biasing, or, conversely, to block high-weight particles from
reaching a given region. Primarily, the DXT card specifies the spheres
needed to define a spherical phase-space region and the special weight-
cutoff game that applies inside the spheres, depending upon the presence
or absence of other variance reduction games specified in the problem.
See §2.7.2.18 for more details about this method.

| Data-card Form:   | P x1 y1 z1 ri1 ro1 x2 y2 z2 ri2 ro2 . . . dwc1 dwc2 dpwt Particle designator. Restriction: Only neutrons ( n ) and photons ( p ) are permitted.                                                                                                                                                       |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| xk yk zk          | Coordinates of the point at the center of the k th pair of spheres ( 1 , 2 ). Restriction: k ≤ 10 .                                                                                                                                                                                                   |
| rik               | Radius of the k th inner sphere in centimeters. The inner sphere is only used to bias placement of the DXTRAN particles on the outer sphere by modifying the probability density function into a two-step histogram [§2.7.2.18]. All particles start on the outer sphere ( 3 ). Restriction: k ≤ 10 . |
| rok               | Radius of the k th outer sphere in centimeters. Restriction: k ≤ 10 .                                                                                                                                                                                                                                 |
| dwc1              | Upper weight cutoff in the spheres for the DXTRAN weight-cutoff game inside the sphere. (DEFAULT: dwc1 = 0 )                                                                                                                                                                                          |
| dwc2              | Lower weight cutoff in the spheres for the DXTRAN weight-cutoff game inside the sphere. (DEFAULT: dwc2 = 0 )                                                                                                                                                                                          |
| dpwt              | Minimum photon weight. Entered on DXT : n card only ( 4 ). (DEFAULT: dpwt = 0 )                                                                                                                                                                                                                       |

Defaults: Zero for dwc1 , dwc2 , and dpwt . No defaults for locations or
radii.

Use: Optional. Consider using DXC : P or DD cards when using DXT .

## Details:

- 1 There can be up to 10 sets of positions and radii per particle type. There is only one set of dwc1 and dwc2 entries for each particle type. The dwc pair is entered after conclusion of the other data and (with DXT : n ) before the one value of dpwt . The weight cutoffs apply to DXTRAN particle tracks inside the outer radii

and have default values of zero. The DXTRAN photon weight cutoffs have
no effect unless the simple physics is used, with one exception: upon
leaving the sphere, track weights (regardless of what physics is used)
are checked against the cutoffs of the CUT : p card. The DXTRAN weight
cutoffs dwc1 and dwc2 are ignored when mesh-based weight windows are
used, but are active for cell-based weight windows because the weight-
window game is turned off inside the spheres.

- 2 DXTRAN spheres can be nested inside one another [331]. The allowed nesting is reasonably general: more than one DXTRAN sphere may be nested inside a larger DXTRAN sphere and the centers of the nested DXTRAN spheres need not be concentric. Also, the spherical surfaces must not intersect. This nesting mitigates weight fluctuation problems as the particles approach the region(s) of interest.
- 3 When the DXTRAN method is used as a means to produce a higher particle population near a tally, the inner radius ri should be at least as large as the tally region. The purpose of the inner sphere is for biasing placement of DXTRAN particles on the outer sphere; there is no problem making the two radii the same.
- 4 The minimum photon weight limit dpwt on the DXT : n card parallels almost exactly the minimum photon weight entries on the PWT card. One slight difference is that in Russian roulette during photon production inside DXTRAN spheres, the factor for relating current cell importance to source cell importance is not applied. Thus, the user must have some knowledge of the weight distribution of the DXTRAN particles (from a short calculation with the DD card, for example) inside the DXTRAN sphere, so the lower weight limit for photon production may be specified intelligently. As in the case of the PWT entries, a negative entry will make the minimum photon weight relative to the source particle starting weight. The default value is zero, which means photon production will occur at each neutron DXTRAN particle collision in a material with non-zero photon production cross section inside the DXTRAN sphere.

## 5.12.10.1 Additional Information Regarding DXTRAN Spheres

One use of DXTRAN is to improve the particle sample in the vicinity of a
tally. It should not be misconstrued as a tally itself, such as a point
detector; it is used in conjunction with tallies as a variance reduction
technique. DXTRAN spheres must not overlap. The spheres should normally
cover the tally region if possible. Specifying a tally cell or surface
partly inside and partly outside a DXTRAN sphere usually will make the
mean of the tally erratic and the variance huge.

The technique is most effective when the geometry inside the spheres is
very simple and can be costly if the inside geometry is complicated,
involving several surfaces. However, the nested DXTRAN treatment should
alleviate some of these complicated geometry issues. The inner sphere is
intended to surround the region of interest. The outer sphere should
surround neighboring regions that may scatter into the region of
interest. In MCNP6, the relative importance of the two regions is five.
That is, the probability density for scattering toward the inner sphere
region is five times as high as the probability density for scattering
between the inner and outer spheres. This position biasing is only one
of several factors that affect the weights of the DXTRAN particles.

All collisions producing neutrons and photons contribute to DXTRAN,
including model physics interactions. When the secondary neutron/photon
angular scattering distribution function is unknown, isotropic
scattering, which may be a poor approximation, is assumed. Although the
extension to higher energies often is approximate, a tally with an
appropriate energy structure can provide the user with insight regarding
the contributions at these energies. This approximation is superior to
neglecting charged-particle and high-energy neutron collisions
altogether.

As mentioned above, DXTRAN uses an assumption of isotropic scatter for
contributions from collisions within the model regime. These estimators
require the angular distribution data for particles produced in an
interaction to predict scattering toward the sphere(s). Information on
these distributions is available in

tabular form in the libraries; however, this information is not
available in the required form from physics models used to produce
secondary particles above the tabular region.

DXTRAN can be used in a problem with the S ( α, β ) thermal treatment
[77], but contributions to the DXTRAN spheres are approximate. DXTRAN
should not be used with reflecting surfaces, white boundaries, or
periodic boundaries [§2.5.6.4.2]. DXTRAN can be used with mono-direction
sources, but the user should understand that no contributions from
sources occur unless the source is directed at the DXTRAN sphere.

DXTRAN spheres can be used around point detectors ( F5 tallies), but the
combination may be very sensitive to reliable sampling.

If more than one set of DXTRAN spheres is used in the same problem, they
can 'talk' to each other in the sense that collisions of DXTRAN
particles in one set of spheres cause contributions to another set of
spheres. The contributions to the second set have, in general, extremely
low weights but can be numerous with an associated large increase in
computer time. In this case the DXTRAN weight cutoffs probably will be
required to kill the very-low-weight particles, provided mesh-based
weight windows are not used. The DD card can give you an indication of
the weight distribution of DXTRAN particles.

Remember that the DD card roulette game is on by default and the
reference weight is a moving average for the first dmmp histories unless
this Russian roulette game is turned off or a fixed level is input (as a
-k i on the DD card). It is highly recommended that the user make a
short calculation to establish a value to input; a value that is 10% of
the average contributed weight to the sphere is a good place to start.
See the DD card input requirements about more details regarding the
number of histories used to find the average contribution. If the user
were to rely on the default behavior, then running a single history
after the first dmmp histories (perhaps for the sake of debugging or
dealing with a lost particle) will not yield the same result as before.

## 5.12.11 DD: Detector Diagnostics

The DD card (1) can speed up calculations significantly by using a
Russian roulette game to limit small contributions that are less than
some fraction k of the average contribution per history to detectors or
DXTRAN spheres and (2) can provide more information about the origin of
large contributions or the lack of a sufficient number of collisions
close to the detector or DXTRAN sphere. The information provided about
large contributions can be useful for setting cell importance or source-
biasing parameters.

The DD card eliminates tracks to DXTRAN spheres, and contributions to
detectors.

| Data-card Form: DD n k 1 m 1 k 2 m 2 . . .   | Data-card Form: DD n k 1 m 1 k 2 m 2 . . .                                                                                                                                 |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                            | Control flag. If n ends in the number 5, then n is the tally number for a specific detector tally to which the card applies. If                                            |
|                                              | n = 0 or is blank, then diagnostic parameters apply to all detector tallies and DXTRAN spheres unless overridden with a separate DD n card.                                |
|                                              | n = 1 provide detector diagnostics for neutron DXTRAN spheres.                                                                                                             |
|                                              | n = 2 provide detector diagnostics for photon DXTRAN spheres.                                                                                                              |
| k k                                          | Criterion for playing Russian roulette for DXTRAN sphere k or detector k in tally n . Let A k be the average score per history for either the sphere or detector ( 1 ). If |

|     | k k < 0                                                                                                                                                                                        | DXTRAN or detector scores greater than | k k | will always be made and contributions less than | k k | are subject to Russian roulette; or                                                                                                                          |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     | 0 < k k ≤ 1                                                                                                                                                                                    | all DXTRAN sphere or detector contributions are made for the first dmmp histories. Thereafter, any contribution to the detector or sphere greater than k k A k will always be made, but any contribution less than k k A k is subject to Russian roulette ( 2 ); or |
|     | k k = 0                                                                                                                                                                                        | no Russian roulette is played on small DXTRAN or detector scores.                                                                                                                                                                                                   |
| m k | Criterion for printing diagnostics for large contributions for DXTRAN sphere k or detector k of tally n . Let A k be the average score per history for either the sphere or detector ( 1 ). If | Criterion for printing diagnostics for large contributions for DXTRAN sphere k or detector k of tally n . Let A k be the average score per history for either the sphere or detector ( 1 ). If                                                                      |
|     | m k = 0                                                                                                                                                                                        | no diagnostic print.                                                                                                                                                                                                                                                |
|     | m k > 0 and k k > 0                                                                                                                                                                            | then no diagnostic print made for the first dmmp histories. Thereafter, the first 100 contributions larger than m k A k will be printed ( 2 ).                                                                                                                      |
|     | m k > 0 and k k < 0                                                                                                                                                                            | then the first 100 contributions larger than m k | k k | will be printed.                                                                                                                                                                                           |

Default: If k k is not specified on a DD n card, k k on the DD card is
used. If that is not specified, k k = 0 . 1 is used. A similar sequence
of defaults defines m k , with a final default of m k = 1000 .

Use: Optional. Remember that Russian roulette will be played for
detectors and DXTRAN unless specifically turned off by use of the DD
card. The value of k k = 0 . 5 is suitable for most problems; the non-
zero default value, k k = 0 . 1 , means that the game is always played
unless explicitly turned off by the user. Consider also using the PD or
DXC cards.

## Details:

- 1 The average contribution per history, A , to a particular DXTRAN sphere or detector is calculated from all contributions to the detector or sphere made by particle histories until the first tally fluctuation chart (TFC) interval is reached (see the dmmp entry on the PRDMP card). The default is 1000 particles per interval for fixed-source problems or one KCODE cycle. The average is then updated at all subsequent tally fluctuation chart intervals.
- 2 Remember that when k k is positive, the Russian roulette game is played on the basis of the estimated average contribution per history, A k . Because the estimate improves from time to time, the game is based on different values for different histories. This can make debugging a problem more complicated, and the variance estimate does not quite obey the Central Limit Theorem.

A procedure worth considering is to determine the average contribution
per history in a preliminary calculation and then use some fraction of
the negative of this value in subsequent longer runs. The Russian
roulette game is played without regard to particle time or energy; thus
time and energy bins for which the ultimate tally is small may lose a
disproportionate share of scores by the roulette game.

1

2

3

4

5

6

7

8

9

## 5.12.11.1 Example 1

| DXT:N   | x1      | y1      | z1   | ri1   | ro1   |
|---------|---------|---------|------|-------|-------|
|         | x2      | y2      | z2   | ri2   | ro2   |
|         | x3      | y3      | z3   | ri3   | ro3   |
| DXT:P   | x4      | y4      | z4   | ri4   | ro4   |
| F15X:P  | a1      | r1      | R1   |       |       |
|         | a2      | r2      | R2   |       |       |
| DD      | 0.2     | 0.2     | 100  | 0.15  | 2000  |
| DD1     | -1.1E25 | -1.1E25 | 3000 | J     | J     |
| DD15    | 0.4     | 0.4     | 10   |       |       |

This input results in the following interpretation for the DD parameters
for the detectors and DXTRAN spheres shown in Table 5.26.

## 5.12.12 PD: Detector Contribution

The PD card reduces the number of contributions to point detector
tallies ( F5 ) from selected cells that are relatively unimportant to a
given detector, thus saving computing time. At each collision in cell j
, the point detector tallies are made with probability 0 ≤ p j ≤ 1 ;
that is, a Russian roulette game is played in which the survival
probability is p j to determine if the contribution should take place.
When the contribution survives the roulette game, the tally is then
increased by the factor 1 /p j to obtain unbiased results for all cells
except those where p j = 0 . This enables the user to decrease the
problem runtime by setting p j &lt; 1 for cells many mean free paths from
the detectors. It also selectively eliminates detector contributions
from cells by setting the p j values for those cells to zero. This card
is analogous to the DXC card, but is used for contributions to point
detector tallies ( F5 ).

## /warning\_sign Caution

Cells should generally never be assigned a value of p j = 0 , because
this will always prevent contribution from a cell to the associated
point detector(s). Unless it can be guaranteed that contributions from
the given cell to the detector are impossible, it is recommended to
assign a small value to have infrequent but high-weight contributions
(by virtue of weight increase following rouletting survival) to give the
MCNP code the opportunity to sample important rare events that will
manifest as notable increases in the point detector tally's variance and
variance of the variance

Table 5.26: DD Card Example k k , m k Parameters

|            | k k             |   m k |
|------------|-----------------|-------|
| sphere 1   | - 1 . 1 × 10 25 |  3000 |
| sphere 2   | 0.15            |  2000 |
| sphere 3   | 0.2             |  3000 |
| sphere 4 1 | 0.2             |   100 |
| detector   | 0.4             |    10 |
| detector 2 | 0.15            |  2000 |

```
Cell-card Form: PD n = p or Data-card Form: PD n p1 p2 . . . n Tally number ( 1 ). Restriction: n ≤ 9999 p Probability of contribution to detector n from cell. (DEFAULT: p = 1 ) pj Probability of contribution to detector n from cell k . (DEFAULT: pj = 1 ) Number of entries is equal to the number of cells in the problem.
```

Default:

pj = 1

Use: Optional. Consider also using the DD card.

## Details:

- 1 A default set of probabilities can be established for all tallies by use of a PD0 card. These default values will be overridden for a specific tally n by values entered on a PD card, where n must end in 5 to apply to a particular point detector.

## 5.12.13 DXC: DXTRAN Contribution

The DXC card is analogous to the PD card for detector contributions
except it is used for contributions to DXTRAN spheres.

| Cell-card Form: DXC n : P = p or Data-card Form: DXC n : P p1 p2 . . .   | Cell-card Form: DXC n : P = p or Data-card Form: DXC n : P p1 p2 . . .                                                                            |
|--------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                                                        | Which DXTRAN sphere the DXC card applies to. If n = 0 or absent, the DXC card applies to all the DXTRAN spheres in the problem. (DEFAULT: n = 0 ) |
| P                                                                        | Particle designator. Restriction: Only allowed particles are neutrons ( N ) and photons ( P ).                                                    |
| p                                                                        | Probability of contribution to DXTRAN sphere n from cell. (DEFAULT: p = 1 )                                                                       |
| pk                                                                       | Probability of contribution to DXTRAN sphere n from cell k . (DEFAULT: pk = 1 ) Number of entries is equal to the number of cells in the problem. |

Use: Optional. Consider also using the DD card.

## 5.12.14 BBREM: Bremsstrahlung Biasing

The bremsstrahlung process generates many low-energy photons, but the
higher-energy photons are often of more interest. One way to generate
more high-energy photon tracks is to bias each sampling of a
bremsstrahlung photon toward a larger fraction of the available electron
energy. Use the BBREM card to specify this biasing toward higher-energy
photons.

1

| Data-card Form: BBREM   | b 1 b 2 . . . b 49 m 1 m 2 . . . m K                  |
|-------------------------|-------------------------------------------------------|
| b 1                     | Any positive value (currently unused).                |
| b 2 . . . b 49          | Bias factors for the bremsstrahlung energy spectrum.  |
| m 1 . . . m K           | List of K materials for which the biasing is invoked. |

Default: None.

Use: Optional.

## 5.12.14.1 Example 1

BBREM 1. 1. 46I 10. 888 999

This specification will create a gradually increasing enhancement (from
the lowest to the highest fraction of the electron energy available to a
given event) of the probability that the sampled bremsstrahlung photon
will carry a particular fraction of the electron energy. This biasing
would apply to each instance of the sampling of a bremsstrahlung photon
in materials 888 and 999. The sampling in other materials would remain
unbiased. The bias factors are normalized by the code in a manner that
depends both on material and on electron energy, so that although the
ratios of the photon weight adjustments among the different groups are
known, the actual number of photons produced in any group is not easily
predictable. For the EL03 treatment, there are more than 49 relative
photon energy ratios so the lower energy bins have a linear
interpolation between b 1 and b 2 for their values.

In most problems the above prescription will increase the total number
of bremsstrahlung photons produced because there will be more photon
tracks generated at higher energies. The secondary electrons created by
these photons will tend to have higher energies as well, and will
therefore be able to create more bremsstrahlung tracks than they would
at lower energies. This increase in the population of the electron-
photon cascade will make the problem run more slowly. The benefits of
better sampling of the high-energy domain must be balanced against this
increase in run time.

## 5.12.15 PIKMT: Photon-production Biasing

For several classes of coupled neutron-photon calculations, the desired
result is the intensity of a small subset of the entire photon energy
spectrum. Two examples are discrete-energy (line) photons and the high-
energy tail of a continuum spectrum. In such cases, it may be beneficial
to bias the spectrum of neutron-induced photons to produce only those
that are of interest.

## /warning\_sign Caution

Use of the PIKMT card can cause non-zero probability events to be
excluded completely, resulting in a biasing game that may not be fair.
While neutron tallies will be unaffected (within statistics), the only
reliable photon tallies will be those with energy bins immediately
around the energies of the discrete photons produced.

To use this feature, users will likely need information about the MT
identifiers of the reactions that produce discrete energy photons. The
user is encouraged to consult [Appendix B of 45] for a list of all MT
identifiers

1

2

3

and look through [Chapters 12 and 13 of 45] (i.e., Files 12 and 13) for
a better understanding of ENDF neutron-induced photon production.

This photon-production biasing feature is also useful for biasing the
neutron-induced photon spectrum to produce very high-energy photons (for
example, E γ ≥ 10 MeV). Without biasing, these high-energy photons are
produced very infrequently; therefore, it is difficult to extract
reliable statistical information about them. An energy cutoff can be
used to terminate a track when it falls below the energy range of
interest.

<!-- formula-not-decoded -->

Default: If the PIKMT card is absent, no biasing of neutron-induced
photons occurs. If the PIKMT card is present, any target identifier not
listed has a default value of ipik k = -1 , and no photons are produced
for these unlisted target identifiers.

Use: Only useful for biasing photon production. Only available for
neutron libraries.

## Details:

- 1 Entries on the mt and pmt pairs need not be normalized. For a target identifier with a positive value of ipik , any reaction that is not identified with its mt on the PIKMT card will not be sampled.

## 5.12.15.1 Example 1

| PIKMT   | Fe-56   | 1 102001   | 1      | N-14   |
|---------|---------|------------|--------|--------|
|         | Cu-63   | 2 3001     | 2 3002 |        |
|         | O-16    | -1         |        |        |

1

This example results in normal sampling of all photon-production
reactions for 14 N. All photons from neutron collisions with 56 Fe are
from the reaction with MT identifier 102001. Two photon-production
reactions with 63 Cu are allowed. Because of the pmt parameters, the
reaction with MT identifier 3001 is sampled twice as frequently relative
to the reaction with MT identifier 3002 than otherwise would be the
case. No photons are produced from 16 O or from any other isotopes in
the problem that are not listed on the PIKMT card.

## 5.12.16 SPABI: Secondary Particle Biasing

Secondary particle biasing allows the user to adjust the number and
weight of secondary particles produced at the time of their creation.
Multiple SPABI cards for different secondary particles are allowed.

| Data-card Form: SPABI: P 1 P 2 e 1 s 1 e 2 s 2 . . .   | Data-card Form: SPABI: P 1 P 2 e 1 s 1 e 2 s 2 . . .                                                                                                                                                                     |
|--------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P 1                                                    | Secondary particle designator [Table 4.3].                                                                                                                                                                               |
| P 2                                                    | List of primary particles to be considered. For example, NPHE represents reactions of neutrons, photons, protons, and electrons. No spaces are allowed. If all particles are to be considered, the entry should be ALL . |
| e k                                                    | The k th upper energy bin limit of secondary particles. The lower bin limit is considered to be zero.                                                                                                                    |
| s k                                                    | Splitting/rouletting control. If                                                                                                                                                                                         |
| s k                                                    | s k > 1 use splitting for secondary particles in the k th bin.                                                                                                                                                           |
| s k                                                    | 0 ≤ s k ≤ 1 use roulette if for secondary particles in the k th bin.                                                                                                                                                     |

## 5.12.16.1 Example 1

SPABI:N NHE 1 0.1 5 1 10 2 20 4

This example specifies that neutron secondaries produced by neutron,
proton, and electron primaries will be biased in the following manner:
below 1 MeV, the secondary neutrons will be rouletted by a factor of
0.1. At energies, 1 to 5 MeV, no biasing is performed. At energies from
5 to 10 MeV, the secondary neutrons will be split 2-for-1, and from 10
to 20 MeV, the secondary neutrons will be split 4-for-1 (with a
corresponding reduction in particle weights).

## 5.12.17 PWT: Photon Weight Control

The PWT card is used in MODE N P or MODE N P E problems. Its purpose is
to control the number and weight of prompt neutron-induced photons
produced at neutron collisions. Use the ACT card to control the number
and weight of delayed photons.

| Cell-card Form: PWT = w or Data-card Form: PWT w 1 w 2 . . .   | Cell-card Form: PWT = w or Data-card Form: PWT w 1 w 2 . . .                                                                                              | Cell-card Form: PWT = w or Data-card Form: PWT w 1 w 2 . . .                                                                                                                                                                                                                                                                                                                       |
|----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| w                                                              | Relative threshold weight of photons produced at neutron collisions in cell ( 1 , 2 ). If                                                                 | Relative threshold weight of photons produced at neutron collisions in cell ( 1 , 2 ). If                                                                                                                                                                                                                                                                                          |
| w                                                              | w > 0                                                                                                                                                     | only neutron-induced photons with weights greater than w × I s /I k are produced, where I s and I k are the neutron importance of the source and collision cells, respectively. Russian roulette is played to determine if a neutron-induced photon with weight below this value survives.                                                                                         |
| w                                                              | w < 0                                                                                                                                                     | only neutron-induced photons with weights greater than - w × w s × I s /I k are produced, where w s is the starting weight of the neutron for the history being followed, and I s and I k are the neutron importance of the source and collision cells, respectively. Russian roulette is played to determine if a neutron-induced photon with weight below this value survives.   |
| w                                                              | w = 0                                                                                                                                                     | exactly one photon will be generated at each neutron collision in the cell, provided that photon production is possible.                                                                                                                                                                                                                                                           |
| w                                                              | w = -1.0e6                                                                                                                                                | photon production in the cell is turned off.                                                                                                                                                                                                                                                                                                                                       |
|                                                                | Relative threshold weight of photons produced at neutron collisions in cell k ( 1 , 2 ). Number of entries is equal to number of cells in the problem. If | Relative threshold weight of photons produced at neutron collisions in cell k ( 1 , 2 ). Number of entries is equal to number of cells in the problem. If                                                                                                                                                                                                                          |
|                                                                | w k > 0                                                                                                                                                   | only neutron-induced photons with weights greater than w k × I s /I k are produced, where I s and I k are the neutron importance of the source and collision cells, respectively. Russian roulette is played to determine if a neutron-induced photon with weight below this value survives.                                                                                       |
|                                                                | w k < 0                                                                                                                                                   | only neutron-induced photons with weights greater than - w k × w s × I s /I k are produced, where w s is the starting weight of the neutron for the history being followed, and I s and I k are the neutron importance of the source and collision cells, respectively. Russian roulette is played to determine if a neutron-induced photon with weight below this value survives. |
|                                                                | w k = 0                                                                                                                                                   | exactly one photon will be generated at each neutron collision in cell k , provided that photon production is possible.                                                                                                                                                                                                                                                            |
|                                                                | w k = -1.0e6                                                                                                                                              | photon production in cell k is turned off.                                                                                                                                                                                                                                                                                                                                         |

Default:

w k = - 1 if neutrons and photons appear on the MODE card.

Use: Recommended for MODE N P and MODE N P E problems without weight
windows.
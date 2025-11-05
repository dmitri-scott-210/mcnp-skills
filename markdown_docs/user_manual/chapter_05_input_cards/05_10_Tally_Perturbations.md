---
title: "Chapter 5.10 - Tally Perturbations and Reactivity Sensitivity"
chapter: "5.10"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.10_Tally_Perturbations_and_Reactivity_Sensitivit.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

1

## 5.9.19.4 Example 3

## TF1 2 j 10-12,13,88 1-2 j 7,8,9 1-99 2 j 1 j j 2 j j j

Note that spaces are not allowed within a comma-delimited list of bins
and/or bin ranges. Spaces continue to be used to delimit the eight bin-
type entries. The first eight entries specify the bins that constitute
the signal component of the tally, while the second eight entries
specify the bins that constitute the noise component of the tally.

## 5.9.20 NOTRN: Direct-only Neutral-particle Point Detector Contributions

## Data-card Form:

Default: None.

Use: This option works with point-detector tallies as well as pinhole or
transmitted image tallies. If the NOTRN card appears in the MCNP input
file, no transport of the neutral particle source particles takes place,
and only the direct neutral particle source contributions are made to
the detectors and the detector grid. This is especially useful for
checking the problem setup or doing a fast calculation to generate the
direct source image. A NOTRN card is not allowed in a restarted
calculation.

## 5.10 Tally Perturbations and Reactivity Sensitivities

MCNP6 offers two flavors of perturbation theory, one based on the
differential operator ( PERT card) and two others based on adjoint
weighting ( KPERT and KSEN cards). Both methods offer advantages and
disadvantages. The differential operator technique is based on a Taylor
series expansion and works very well for generalized responses in fixed-
source problems. In eigenvalue problems, however, the differential
operator methodology may produce inaccurate results because the MCNP6
implementation does not account for the perturbation of the fission
source distribution. The adjoint-based methodology implicitly captures
the perturbation in the fission source; however, it is only capable of
finding the change in reactivity resulting from perturbations in cross
sections and not other responses.

Should a user desire estimates of changes in reactivity for reactor
physics applications or sensitivity coefficients to the k -eigenvalue,
then the adjoint-based methodology is appropriate. An important
limitation of the adjoint-based methods as implemented in MCNP6 is that
they do not consider perturbations that may arise from scattering laws
or from fission emission spectra; this limitation has been shown to lead
to spurious results. For perturbations where the dominant effects are
from absorption or the scattering is mostly isotopic, the results tend
to agree well with those from direct cross-section substitutions and
from the adjoint-methodology code TSUNAMI-3D [318], which employs
multigroup cross-section data rather than continuous-energy data.

## 5.10.1 PERT: Tally Perturbations via Differential Operator

This card allows perturbations in cell material density, composition, or
reaction cross-section data. The perturbation analysis uses the first
and second order differential operator technique. Perturbation estimates

NOTRN

are made without actually changing the input material specifications.
Multiple perturbations can be applied in the same run, each specified by
a separate PERT card.

There is no limit to the number of perturbations because dynamic memory
is used for perturbation storage. The entire tally output is repeated
for each perturbation, giving the estimated difference in the tally, or
this difference can be added to the unperturbed tally (see the METHOD
keyword). For this reason, the number of tallies and perturbations
should be kept to a minimum. However, an entire parameter study can be
done with just two PERT cards [319]. A track length estimate of
perturbations to k eff is automatically estimated and printed for KCODE
problems.

<!-- image -->

| n                        | Unique, user-selected, arbitrary perturbation number. Restriction: 0 < n ≤ 99999999                                                                                                                                                                                                                                                                                                     | Unique, user-selected, arbitrary perturbation number. Restriction: 0 < n ≤ 99999999                                                                                                                                                                                                                                                                                                     |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P                        | Particle designator. Only three options allowed: neutron ( N ); photon ( P ); or combined neutron-photon ( N,P ). Not available for other particles.                                                                                                                                                                                                                                    | Particle designator. Only three options allowed: neutron ( N ); photon ( P ); or combined neutron-photon ( N,P ). Not available for other particles.                                                                                                                                                                                                                                    |
| CELL = c 1 c 2 . . . c K | Comma or space delimited list of cells, c 1 . . . c K , to which to apply the perturbation. Required.                                                                                                                                                                                                                                                                                   | Comma or space delimited list of cells, c 1 . . . c K , to which to apply the perturbation. Required.                                                                                                                                                                                                                                                                                   |
| MAT = m                  | Single material number, m (corresponding to an M m card), with which to fill all cells listed in CELL keyword. Use MAT only if the perturbation changes the material from one cell material to another. Use with caution especially if more than one nuclide in the material is changed. New nuclides cannot be added in the new material card. Must have a corresponding M card ( 1 ). | Single material number, m (corresponding to an M m card), with which to fill all cells listed in CELL keyword. Use MAT only if the perturbation changes the material from one cell material to another. Use with caution especially if more than one nuclide in the material is changed. New nuclides cannot be added in the new material card. Must have a corresponding M card ( 1 ). |
| RHO = r                  | Single value of perturbed density of cells listed after the CELL keyword ( 2 ). If                                                                                                                                                                                                                                                                                                      | Single value of perturbed density of cells listed after the CELL keyword ( 2 ). If                                                                                                                                                                                                                                                                                                      |
| RHO = r                  | RHO > 0                                                                                                                                                                                                                                                                                                                                                                                 | the perturbed density is given in units of atoms/b-cm.                                                                                                                                                                                                                                                                                                                                  |
| RHO = r                  | RHO < 0                                                                                                                                                                                                                                                                                                                                                                                 | the perturbed density is given in units of g/cm 3 .                                                                                                                                                                                                                                                                                                                                     |
| METHOD = j               | Controls tally printing and specifies the number of terms to include in the perturbation estimate ( 3 ). If                                                                                                                                                                                                                                                                             | Controls tally printing and specifies the number of terms to include in the perturbation estimate ( 3 ). If                                                                                                                                                                                                                                                                             |
| METHOD = j               | METHOD = +1                                                                                                                                                                                                                                                                                                                                                                             | perform 1st and 2nd order perturbation calculation and print the difference in the unperturbed tally. (DEFAULT)                                                                                                                                                                                                                                                                         |
| METHOD = j               | METHOD = - 1                                                                                                                                                                                                                                                                                                                                                                            | perform 1st and 2nd order perturbation calculation and print the perturbed tally.                                                                                                                                                                                                                                                                                                       |
| METHOD = j               | METHOD = +2                                                                                                                                                                                                                                                                                                                                                                             | perform 1st order perturbation calculation only and print the difference in the unperturbed tally.                                                                                                                                                                                                                                                                                      |
| METHOD = j               | METHOD = - 2                                                                                                                                                                                                                                                                                                                                                                            | perform 1st order perturbation calculation only and print the perturbed tally.                                                                                                                                                                                                                                                                                                          |
| METHOD = j               | METHOD = +3                                                                                                                                                                                                                                                                                                                                                                             | perform 2nd order perturbation calculation only and print the difference in the unperturbed tally.                                                                                                                                                                                                                                                                                      |
| METHOD = j               | METHOD = - 3                                                                                                                                                                                                                                                                                                                                                                            | perform 2nd order perturbation calculation only and print the perturbed tally.                                                                                                                                                                                                                                                                                                          |
| ERG = e LB e UB          | Two entries, e LB and e UB , that provide the lower and upper bounds of the energy range to which the perturbations are to be applied ( 4 ). (DEFAULT: all energies)                                                                                                                                                                                                                    | Two entries, e LB and e UB , that provide the lower and upper bounds of the energy range to which the perturbations are to be applied ( 4 ). (DEFAULT: all energies)                                                                                                                                                                                                                    |

RXN = r 1 r 2 . . .

ENDF/B reaction number(s) that identify one or more specific reaction
cross sections to perturb ( 5 ). (DEFAULT: RXN = 1 for neutrons and
multigroup, RXN = -5 for photons.) Restriction: RXN reaction numbers
must be identical to FM card reaction numbers.

Default: METHOD=+1 ; ERG =all energies; RXN=1 for neutrons and
multigroup, RXN=-5 for photons.

Use: Optional. The CELL keyword, which identifies one or more perturbed
problem cells, is required. Additionally, either the MAT or RHO keyword
must be specified.

## Details:

- 1 Composition changes can only be made through the use of the MAT keyword. If the RHO keyword is omitted, the MAT keyword is required. Certain composition changes (discussed in §5.10.1.1) are prohibited.
- 2 If the MAT keyword is absent, the RHO keyword is required.
- 3 The ability to produce first- and second-order Taylor series expansion terms separately enables the user to determine the significance of including the second-order estimator for subsequent runs. If the second-order results are a significant fraction (20%-30%) of the total, then higher order (or other) terms are necessary to predict accurately the change in the unperturbed tally. In such cases, the magnitude of the perturbation should be reduced to satisfy this condition. Typically, this technique is accurate to within a few percent for up to 30% changes in the unperturbed tally. It is strongly recommended that the magnitude of the second order term be determined before the user continues with this capability. Classical first-order sensitivity analysis requires only the first-order term, METHOD = +2 ; in this case, the relative magnitude of the second-order term is irrelevant.
- 4 The ERG keyword is usually used with the RXN keyword to perturb a specific cross section over a particular energy range.
- 5 The RXN keyword allows the user to perturb a single reaction cross section of a single nuclide in a material, all reaction types of a single nuclide, a single reaction for all nuclides in a material, and a set of cross sections for all nuclides in a material. Relevant non-standard special R numbers, listed in Table 5.19, can be used. Those that are irrelevant and therefore cannot be used are -4 , -5 , -7 , and -8 for neutrons; -6 for photons; and -3 , -4 , -6 , and -7 for multigroup problems. If these irrelevant R numbers are used, the following fatal error will be printed: ' fatal error. reaction # illegal in perturbation #. '

RXN reaction numbers must be consistent with FM card reaction numbers if
the perturbation affects the tally cross section. The specification RXN
= -6 is most efficient for fission, although MT=18, MT=19, or MT=-2
(multigroup) also work for k eff and F7 tallies.

## 5.10.1.1 PERT Card Limitations/Cautions

1. The perturbation method is limited to the 1st and 2nd order terms of a Taylor series expansion. Examine the 1st and 2nd order terms separately for large ( &gt; 30% ) perturbations to determine the significance of the 2nd order terms. If 2nd order terms are a significant fraction (20%-30%) of the total perturbation, inaccurate tallies can result ( 3 ). A warning message is generated.
2. Nuclide fraction changes ( MAT keyword) are assumed to be independent and, consequently, differential cross terms are ignored. Stated another way, when multiple isotopes are perturbed at once, the perturbation estimate is the sum of the independent nuclide perturbations and does not include the 2nd-order differential term. Therefore, it is very important to change only one isotope density in each PERT card, or to change all isotope densities the same relative amount [319].

1

1

3. FM tallies in perturbed cells can be wrong. Surface tallies and tallies in perturbed cells are safe. A warning message is generated.
4. Detector ( F5 ) and pulse-height tallies ( F8 ) are not compatible with the PERT card. (i.e., give zero perturbation).
5. DXTRAN ( DXT ) is not compatible with the PERT card. A fatal error message is generated.
6. You cannot un-void a region. That is, if you take a region originally specified as void and put in a material in that region with the perturbation technique, a fatal error message is generated. However, you can specify a region as containing a material and use the PERT card to make it void by setting RHO=0 .
7. You cannot introduce a new nuclide into a material composition. A fatal error message is generated. However, you can set up the problem with a mixture of all nuclides of interest and use PERT cards to remove one or more nuclides.
8. Although there is no limit to the number of perturbations, each perturbation may increase running time by 10%-20%, though this value depends on the complexity of the problem and the PERT card(s).
9. Some perturbations (those with small changes) converge slowly.
10. The track length estimate of k eff in criticality calculations assumes the fundamental eigenvector (fission distribution) is unchanged in the perturbed configuration. This approximation can lead to serious errors [197]. For the effect of a perturbation on k eff , use the KPERT card.
11. Use caution when selecting the multiplicative constant and reaction number on FM cards used with F4 tallies in perturbation problems. The track length correction term R 1 j ′ is made only if the multiplicative constant on the FM card is negative (indicating macroscopic cross sections with multiplication by the atom density of the cell). If the multiplicative constant on the FM card is positive, it is assumed that any FM card cross sections are independent of the perturbed cross sections. If there is a reaction ( RXN ) specified on the PERT card, the track length correction term R 1 j is set only if the exact same reaction is specified on the FM card. For example, an entry of RXN=2 (elastic cross section) on the PERT card is not equivalent to the special elastic reaction -3 on the FM card. The user should either enter 2 as the reaction of the FM card and RXN=2 on the PERT card or -3 on FM and -3 on PERT .
12. Limited to N and/or P problems.

## 5.10.1.2 Example 1

```
PERT1:N,P CELL=1 RHO=0.03
```

This perturbation specifies a density change to 0.03 atoms/b-cm in cell
1. This change is applied to both neutron and photon interactions.

## 5.10.1.3 Example 2

```
PERT3:N,P CELL=1 10i 12 RHO=0 METHOD=-1
```

This perturbation makes cells 1 through 12 void for both neutrons and
photons. The estimated changes will be added to the unperturbed tallies.

1

2

3

4

5

6

7

8

9

## 5.10.1.4 Example 3

```
60 13 -2.34 105 -106 -74 73 $ mat 13 at 2.34 g/cm3 . . . M13 1001 -0.2 8016 -0.2 13027 -0.2 26000 -0.2 29000 -0.2 M15 1001 -0.2 8016 -0.2 13027 -0.2 26000 -0.2 29000 -0.4 PERT1:P CELL=60 MAT=15 RHO=-2.808 RXN=51 9i 61,91 ERG=1,20 METHOD=2 PERT2:P CELL=60 RHO=-4.68 RXN=2 METHOD=2
```

This example illustrates first-order sensitivity analysis. The first
PERT card generates the first-order Taylor series terms ∆ c 1 for
changes in tallies caused by a p = 100% increase in the copper cross
section (ENDF/B reaction types 51-61 and 91) above 1 MeV. To effect a p
% change for a specific isotope, set up a perturbed material mimicking
the original material, except multiply the composition fraction of the
perturbed isotope by 1 + p ( -0 . 2 to -0 . 4 ). The density of the
perturbed material is the density of the original material (2.34 g/cm 3
) multiplied by the ratio of the sum of the weight fractions of the
perturbed material (1.2) to the sum of the weight fractions of the
unperturbed material (1.0), or RHO = ( -2 . 34 g/cm 3 × 1 . 2 / 1 . 0 )
= -2 . 808 g/cm 3 . This change must be made to RHO to maintain the
other nuclides in their original amounts. Otherwise, after the MCNP code
normalizes the M15 card and multiplies the constituent weight fractions
by the unperturbed material density, the density of all of the
constituents would be perturbed, which is not the intent. When the MCNP
code normalizes the M 15 card and multiplies the constituent weight
fractions by the correctly modified material density, the density of the
unperturbed isotopes will be unchanged, but the density of the perturbed
isotope will be changed by a factor 1 + p , as intended.

The first-order sensitivity of response c is calculated in post
processing using S = ∆ c 1 / ( c 0 ) p , and p is arbitrary [319].

The second PERT card ( PERT2:p ) gives the first-order Taylor series
terms ∆ c 1 for changes in tallies caused by a 100% increase in the
elastic ( RXN=2 ) cross section of material 13. RHO = -2 . 34 g/cm 3 × 2
= -4 . 68 g/cm 3 .

## 5.10.1.5 Example 4

```
1 M4 6000.60C 0.5 6000.50C 0.5 2 M6 6000.60C 1 3 M8 6000.50C 1 4 PERT1:N CELL=3 MAT=6 METHOD=-1 5 PERT2:N CELL=3 MAT=8 METHOD=-1
```

The perturbation capability can be used to determine the difference
between one cross-section evaluation and another. The difference between
these perturbation tallies will give an estimate of the effect of using
different cross-section evaluations.

## 5.10.1.6 Example 5

10

```
1 1 1 0.05 -1 2 -3 $ mat 1 at 0.05 x 10 atoms/cm 2 . 3 . 4 . 5 M1 1001 0.1 8016 0.2 92235 0.7 6 M9 1001 0.1 8016 0.22 92235 0.7 7 F14:N 1 8 FM14 -1 1 -6 -7 $ keff estimator for cell 1 9 PERT1:N CELL=1 MAT=9 RHO=0.051 METHOD=1 PERT2:N CELL=1 MAT=9 RHO=0.051 METHOD=-1
```

These perturbations involve a 10% increase in the oxygen atom fraction
of material 1 ( RHO = 0 . 05 × (1 . 02 / 1 . 0) = 0 . 051 ). The effect
of this perturbation on tally 14, which is a track-length estimate of k
eff , will be provided as a difference ( PERT1 ) as well as with this
change added to the unperturbed estimate of k eff ( PERT2 ). Note: if
the RHO keyword is omitted from the PERT cards, the 235 U composition
will be perturbed, which can produce invalid results [§5.10.1.1].

## 5.10.1.7 Example 6

The MCNP6 perturbation capability assumes that changes in the relative
abundances of the nuclides in a material are independent and neglects
the cross-differential terms in the second-order perturbation term when
changing two or more cross sections at once. In the case illustrated
below there will be a large false second-order perturbation term.

```
M1 6000.50c 0.5 6012.50c 0.5 M2 6000.50c 0.9 6012.50c 0.1 PERT1:N CELL 1 MAT 2
```

The perturbation should be zero because 6000.50c is exactly the same as
6012.50c, making materials M1 and M2 identical. In fact, the first-order
term will be zero ( METHOD=2 , correct) but the second-order term will
be wrong because of the differential cross term.

## 5.10.1.8 Example 7

There is no problem if all the nuclides have the same density change (
RHO option but no MAT option). There is also no cross term problem if
only one nuclide has a density change, for example:

```
1 cell 1 material 1 density rho=3.0 2 . 3 . 4 . 5 M1 1001 2 8016 1 6 M2 1001 2 8016 2 7 PERT1:N CELL 1 MAT 2 RHO=4.0
```

The cell density times the normalized atom fraction of 1001 is unchanged
( 3 × 2 / 3 = 4 × 2 / 4 ) and only the density of 8016 is changed (from
3 × 1 / 3 to 4 × 2 / 4 ). However, there will be a second-order cross-
differential

1

2

3

term that is neglected when the cell density times nuclide fraction
changes for more than one nuclide in a perturbed material. Therefore, if
the MAT keyword is used for a perturbation, the first- and second-order
terms should be examined. If the second-order perturbation term is small
relative to the first-order term ( METHOD=3 and METHOD=2 ), then
generally the differential cross term is small and the perturbed tally
can be accepted with confidence.

## 5.10.2 KPERT: Reactivity Perturbations via Adjoint Weighting

The adjoint-weighted perturbation methodology invoked by the KPERT card
was designed to investigate changes in k eff as a result of material
substitution. While this method, in theory, allows for more general
perturbations, it introduces an approximation in the handling of
scattering laws that can lead to large and unacceptable deviations in
scattering sensitivities. Additionally, the user interface was designed
with material substitution with mind; using it for sensitivity
coefficient calculations may be cumbersome for some users. For
sensitivity coefficient calculations, see the KSEN card. Multiple KPERT
cards are permitted in a single input file.

| Data-card Form: KPERT n KEYWORD = value(s) ...   | Data-card Form: KPERT n KEYWORD = value(s) ...                                                                                                                                                                                                                                                                                            | Data-card Form: KPERT n KEYWORD = value(s) ...                                                                                                                                                                                                                                                                                            |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                                | Unique, user-selected, arbitrary perturbation number. n has the same limits as regular tallies. See Table 4.2.                                                                                                                                                                                                                            | Unique, user-selected, arbitrary perturbation number. n has the same limits as regular tallies. See Table 4.2.                                                                                                                                                                                                                            |
| CELL = c 1 c 2 . . . c K                         | Comma or space delimited list of cells, c 1 . . . c K , to which to apply the perturbation. Required.                                                                                                                                                                                                                                     | Comma or space delimited list of cells, c 1 . . . c K , to which to apply the perturbation. Required.                                                                                                                                                                                                                                     |
| MAT = m 1 m 2 . . . m K                          | List of materials that are to be substituted in each of the perturbed cells listed in the CELL keyword. Each cell must be associated with exactly one material number and each unique material identifier number must have an associated M card ( 1 ).                                                                                    | List of materials that are to be substituted in each of the perturbed cells listed in the CELL keyword. Each cell must be associated with exactly one material number and each unique material identifier number must have an associated M card ( 1 ).                                                                                    |
| RHO = r 1 r 2 . . . r K                          | List of densities corresponding to each of the perturbed cells listed in the CELL keyword. Each cell specified on the CELL keyword must be associated with exactly one density value specified on the RHO keyword ( 2 ). If                                                                                                               | List of densities corresponding to each of the perturbed cells listed in the CELL keyword. Each cell specified on the CELL keyword must be associated with exactly one density value specified on the RHO keyword ( 2 ). If                                                                                                               |
| RHO = r 1 r 2 . . . r K                          | r k > 0                                                                                                                                                                                                                                                                                                                                   | the perturbed density is given in units of atoms/b-cm 2 .                                                                                                                                                                                                                                                                                 |
| RHO = r 1 r 2 . . . r K                          | r k < 0                                                                                                                                                                                                                                                                                                                                   | the perturbed density is given in units of g/cm 3 .                                                                                                                                                                                                                                                                                       |
| ISO = z 1 z 2 . . . z K                          | List of target identifiers [§1.2.2] or table identifiers [§1.2.3] that the perturbation impacts. All formats supported. The list applies to all cells in the CELL list ( 3 ). (DEFAULT: all isotopes assumed affected)                                                                                                                    | List of target identifiers [§1.2.2] or table identifiers [§1.2.3] that the perturbation impacts. All formats supported. The list applies to all cells in the CELL list ( 3 ). (DEFAULT: all isotopes assumed affected)                                                                                                                    |
| RXN = rx 1 rx 2 . . . rx K                       | List of MT or special reaction numbers that the perturbation impacts. The list applies to all cells in the CELL list ( 4 ). Table 5.23 provides a list of acceptable entries. (DEFAULT: all reactions assumed affected)                                                                                                                   | List of MT or special reaction numbers that the perturbation impacts. The list applies to all cells in the CELL list ( 4 ). Table 5.23 provides a list of acceptable entries. (DEFAULT: all reactions assumed affected)                                                                                                                   |
| ERG = e 1 e 2 . . . e K                          | List of energies (MeV), in ascending order, over which to apply the perturbation ( 5 ). (DEFAULT: all energies)                                                                                                                                                                                                                           | List of energies (MeV), in ascending order, over which to apply the perturbation ( 5 ). (DEFAULT: all energies)                                                                                                                                                                                                                           |
| LINEAR= value                                    | Provides the ability to force an unperturbed fission source, yielding a linear equation to estimate the change in reactivity that arises from a change in cross sections. Many applications, such as the calculation of sensitivity coefficients demand the use of linear-perturbation theory in which the denominator is unperturbed. If | Provides the ability to force an unperturbed fission source, yielding a linear equation to estimate the change in reactivity that arises from a change in cross sections. Many applications, such as the calculation of sensitivity coefficients demand the use of linear-perturbation theory in which the denominator is unperturbed. If |
| LINEAR= value                                    | LINEAR = NO                                                                                                                                                                                                                                                                                                                               | do not use the perturbed fission source in the denominator.                                                                                                                                                                                                                                                                               |

1

1

1

2

LINEAR = YES

use the perturbed fission source in the denominator. (DEFAULT)

Default: ISO =all isotopes; RXN =all reactions; ERG =all energies;
LINEAR=NO

Use: Optional. The CELL keyword, which identifies one or more perturbed
problem cells, is required. Additionally, either the MAT or RHO keyword
must be specified.

## Details:

- 1 If the RHO keyword is absent, the MAT keyword is required. Use the MAT keyword, for example, to test the effect of changing the enrichment of a particular set of cells.
- 2 If the MAT keyword is absent, the RHO keyword is required. This keyword allows the user to perform density perturbations. RHO may be used in addition to the MAT keyword to perturb both the material and the density of the cells specified in the CELL keyword list.
- 3 The ISO keyword is useful for testing the effect of individual nuclides.
- 4 The RXN keyword is useful for testing the effect of individual reactions.
- 5 The ERG keyword is similar to energy binning with tallies, except that there is no implied lower bound of 0 MeV.

## 5.10.2.1 Example 1

```
KPERT5 CELL=1 4 MAT=2 2 RHO=-19.1 -19.1
```

This perturbation takes whatever materials are in cells 1 and 4 and
makes them both material 2 with a mass density of 19.1 g/cm 3 .

## 5.10.2.2 Example 2

KPERT98 CELL=10 RHO=-18.6 RXN=18

This perturbation looks at the effect on the fission reaction (MT=18)
when the mass density of the material in cell 10 is changed to 18.6 g/cm
3 .

## 5.10.2.3 Example 3

```
KPERT1 CELL=22 26 MAT=92 92 ISO=U-238.70c RXN=51 39i 91 ERG=0 2 5 20 LINEAR=YES
```

This perturbation judges the impact of 238 U inelastic scattering in
cells 22 and 26 by a change to material 92. The perturbation is further
broken down by energy, with regions of less than 2 MeV, between 2 and 5
MeV, and between 5 and 20 MeV. The perturbation is also linear.

## 5.10.3 KSEN: k eff Sensitivity Coefficients via Adjoint Weighting

The KSEN card [320, 321] provides the ability to compute sensitivity
coefficients of the effective multiplication k (i.e., k eff ) for
nuclear data. These types of calculations are useful for code validation
and the development of benchmark suites applicable to specific sets of
applications, for the design of critical (integral) experiments, and for
uncertainty quantification. This computation is done in a KCODE
calculation using the KSEN card; fixed-source problems are not
appropriate for KSEN . Multiple KSEN cards are permitted in a single
input file.

MCNP6 has the ability to subdivide sensitivities by spatial zone. These
can be done either as a collection of cells or materials. The keywords
on the KSEN card to do this are CELL = c1 ( c2 c3 ) . . . and MAT = m1 (
m2 m3 ) . . . Each entry defines a spatial zone, and like with tally
specifications, cells or materials may be grouped by parentheses.
Duplicate cells or materials are allowed. A KSEN card may not have both
the CELL and MAT keywords; doing this both ways requires multiple
instances of KSEN .

The methods employed are based upon linear-perturbation theory using
adjoint weighting, the same as those used by TSUNAMI-3D for this purpose
[318]. The adjoint weighting is performed in a single forward
calculation using the Iterated Fission Probability method. The
capability is specifically designed for use in continuous-energy
calculations, and while it is possible to use this option in multigroup
calculations, MCNP6 does not compute the effect of the cross-section
self-shielding on the sensitivity coefficients.

<!-- image -->

| Data-card Form: KSEN n   | sen KEYWORD = value(s) ...                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                        | Unique, user-selected, arbitrary perturbation number. n has the same limits as regular tallies. See Table 4.2. Values greater than 999999 may result in asterisks in the outp file.                                                                                                                                                                                                                                                                                     |
| sen                      | Type of sensitivity. If                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ISO = z1 z2 . . . zK     | List of target identifiers [§1.2.2] or table identifiers [§1.2.3] for which sensitivities are desired. All formats supported. (DEFAULT: all data tables in the problem)                                                                                                                                                                                                                                                                                                 |
| RXN = rx1 rx2 . . . rxK  | List of reaction MT numbers or special reaction numbers. Table 5.23 provides a list of acceptable entries. [DEFAULT: total cross section without S ( α,β ) ]                                                                                                                                                                                                                                                                                                            |
| MT = rx1 rx2 . . . rxK   | Same behavior as RXN .                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ERG = e1 e2 . . . eK     | List of energy bin boundaries, in ascending order, over which to provide the sensitivities. For cross sections and fission ν , the energies are taken to be those entering the collision (incident energy). For secondary distributions of fission χ and scattering laws, the energies are taken to be energies exiting the collision. If used, a minimum of two entries are required to establish at least one lower and upper boundary ( 1 ). (DEFAULT: all energies) |
| EIN = e1 e2 . . . eK     | Specifies a range of incident energy bins ( 1 ). Only used for fission- χ ( - 1018 ) or scattering-law ( - 1002 or - 1004 ) sensitivities. (DEFAULT: all energies)                                                                                                                                                                                                                                                                                                      |
| LEGENDRE                 | The LEGENDRE keyword is followed by a single integer ( > 0 ) stating the order of Legendre moments to calculate sensitivities for (e.g., ' LEGENDRE = 3 ' would give the k eff sensitivity to the P 1 , P 2 , and P 3 Legendre scattering moments) any scattering law sensitivity. If present calculates the scattering law sensitivity to Legendre moments instead of as a function of cosine                                                                          |

1

|           | binning. Note that to do this, the MCNP code needs a background cosine grid that may be provided by the user with the COS keyword. If this is not provided, a default cosine grid of 200 equally spaced cosine bins from - 1 to 1 is used.   |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| COS       | Specifies a range of direction-change cosines for the scattering events. Only used for scattering law ( - 1002 or - 1004 ) sensitivities. (DEFAULT: all angles)                                                                              |
| CONSTRAIN | Only used for fission- χ ( - 1018 ) or scattering-law ( - 1002 or - 1004 ) sensitivities. If                                                                                                                                                 |
| CONSTRAIN | CONSTRAIN = NO do not renormalize the energy (or cosine) sensitivity distribution.                                                                                                                                                           |
| CONSTRAIN | CONSTRAIN = YES renormalize the energy (or cosine) sensitivity distribution ( 2 ). (DEFAULT)                                                                                                                                                 |
| CELL      | List of cell numbers of the problem for spatial zoning. Each entry defines a spatial zone and multiple cells may be grouped into a single spatial zone with parentheses. Duplicate cells are allowed.                                        |
| MAT       | Like the CELL keyword except material numbers are used as opposed to cell numbers. Zones are defined to encompass all cells containing that material.                                                                                        |

Default: ISO =all isotopes in the problem; RXN =total cross section
without S ( α, β ) ; ERG =all energies; EIN =all energies, COS =all
angles; CONSTRAIN = YES

Use: Optional. If the KSEN card is used, the KOPTS card is recommended.

## Details:

- 1 Unlike tallies, there is no implied zero lower-energy-bin boundary.
- 2 Increasing a distribution in one region of energy (or cosine) space needs to be offset by decreases elsewhere to preserve the condition that the distribution be normalized to a constant value, typically one. For most applications, users should use the default, i.e., renormalize the sensitivities. Full normalization [322] is applied.
- 3 For cross sections and fission ν , the energies listed on ERG are taken to be those entering the collision, whereas for secondary distributions of fission χ and scattering laws they are taken to be energies exiting the collision.

## 5.10.3.1 Example 1

## KSEN3 XS

Default behavior. Gives the total cross-section sensitivities
(integrated over all energies) to all isotopes and S ( α, β ) laws in
the problem.

Table 5.23: Allowed Reaction Numbers for KSEN with Continuous-energy Physics

| Nuclear Data                              | MT Number          | Special Reaction Number   |
|-------------------------------------------|--------------------|---------------------------|
| Total                                     | 1                  | -                         |
| Total and S ( α,β )                       | -                  | - 1                       |
| Capture                                   | -                  | - 2                       |
| Elastic                                   | 2                  | -                         |
| Total Inelastic                           | 4                  | -                         |
| Elastic and S ( α,β )                     | -                  | - 3                       |
| Total Fission                             | 18                 | - 6                       |
| First-Chance Fission                      | 19                 | -                         |
| Second-Chance Fission                     | 20                 | -                         |
| Third-Chance Fission                      | 21                 | -                         |
| Fourth-Chance Fission                     | 38                 | -                         |
| Total Fission ν                           | 452                | - 7                       |
| Prompt Fission ν                          | 456                | -                         |
| Delayed Fission ν                         | 455                | -                         |
| (n,2nd)                                   | 11                 | -                         |
| (n,2n)                                    | 16                 | -                         |
| (n,3n)                                    | 17                 | -                         |
| (n, n α )                                 | 22                 | -                         |
| (n, n3 α )                                | 23                 | -                         |
| (n, 2n α )                                | 24                 | -                         |
| (n, np)                                   | 28                 | -                         |
| (n, n2 α )                                | 29                 | -                         |
| (n, 2n2 α )                               | 30                 | -                         |
| (n,nd)                                    | 32                 | -                         |
| (n,nt)                                    | 33                 | -                         |
| (n, n 3 He)                               | 34                 | -                         |
| (n,nd2 α )                                | 35                 | -                         |
| (n,nt2 α )                                | 36                 | -                         |
| (n,4n)                                    | 37                 | -                         |
| (n, 2np)                                  | 41                 | -                         |
| (n, 3np)                                  | 42                 | -                         |
| (n, n2p)                                  | 44                 | -                         |
| (n, np α )                                | 45                 | -                         |
| (n, γ )                                   | 102                | -                         |
| (n,p)                                     | 103                | -                         |
| (n,d)                                     | 104                | -                         |
| (n,t)                                     | 105                | -                         |
| (n, 3 He)                                 | 106                | -                         |
| (n, α )                                   | 107                | -                         |
| Inelastic Levels (1-40)                   | 51, 52, . . . , 90 | -                         |
| Inelastic Continuum                       | 91                 | -                         |
| Total Fission χ                           | -                  | - 1018                    |
| Prompt Fission χ                          | -                  | - 1456                    |
| Delayed Fission χ                         | -                  | - 1455                    |
| Total Scatter Law                         | - -                | - 1001 - 1002             |
| Elastic Scatter Law Inelastic Scatter Law | -                  | - 1004                    |

1

1

1

2

1

1

## 5.10.3.2 Example 2

KSEN14 XS ISO=U-235.70c U-238.70c MT=-1 2 4 -6

Gives total, elastic, inelastic, and fission cross-section sensitivities
for 235 U and 238 U.

## 5.10.3.3 Example 3

KSEN8 XS ISO=H-1.70c lwtr.10t MT=2 4 ERG=0.0 0.625e-6 0.1 20

Gives 1 H elastic scattering and the light-water S ( α, β ) inelastic
scattering kernel sensitivities as a function of energy with bins
between 0 and 0.625 eV, 0.625 eV to 100 keV, and 100 keV to 20 MeV.

## 5.10.3.4 Example 4

KSEN99 XS ISO=Pu-239.70c MT=-1018 ERG=0 0.1 1.0 2.0 5.0 10.0 20.0 EIN=0
2.5 8.0 20.0 CONSTRAIN=NO

Gives 239 Pu fissionχ sensitivities as a function of outgoing and
incident energy. The incident energy bins are 0 to 2.5 MeV, 2.5 to 8
MeV, and 8 to 20 MeV. For each of these, a fissionχ sensitivity is given
for the six energy bins specified by the ERG keyword. The sensitivity is
also not renormalized, which is normally discouraged.

## 5.10.3.5 Example 5

KSEN8016 XS ISO=O-16.70c MT=-1002 ERG=0 19i 20 COS=-1 0 1

Gives 16 O elastic scattering law sensitivities for 1-MeV (outgoing)
energy bins from 0 to 20 MeV. Each outgoing energy bin is subdivided
into two cosine bins for forward and back scattering. The sensitivity
includes neutrons scattering at all possible incident energies.

## 5.10.3.6 Example 6

KSEN101 XS CELL=10 20 (10 20) ERG=SCALE-238

Gives total cross section sensitivities for all isotopes in the problem
with an energy binning defined by SCALE's 238-group library. Three
energy-resolved sensitivity profiles are given: one for cell 10, another
for cell 20, and a third for both (the sum of the sensitivities for
cells 10 and 20).

1

1

1

## 5.10.3.7 Example 7

```
KSEN101 XS RXN=-1002 -1004 LEGENDRE=5 ISO=Fe-56.70c MAT=20
```

Gives the sensitivities for the first five Legendre moments of elastic
and inelastic scattering of 56 Fe, but only for cells with material 20.
The default cosine grid of 200 equally spaced intervals from -1 to 1 is
used for computing the Legendre moment sensitivities because the COS
keyword is not specified.

## 5.10.3.8 Additional Discussion

Other options may be controlled by use of the KOPTS card, which contains
various options for KCODE calculations. The two options are BLOCKSIZE ,
which controls the number of cycles in every outer iteration, and
KSENTAL , which controls output printing of a results file for
sensitivity profiles. The format for these is as follows: KOPTS
BLOCKSIZE = NCY KSENTAL = FILEOPT .

The NCY argument denotes the number of cycles. A greater number leads to
better accuracy of the answer, but the results will be less
statistically resolved. The default is 10 cycles, which has been shown
to be conservative for almost all cases and still preserves a reasonable
about of statistical precision. For small, leakage dominated systems,
this can often be reduced to 5.

The FILEOPT argument gives a file format for printing the sensitivity
profiles. The default is to print no file. In MCNP6, two file formats
are available: MCTAL and TSUNAMI-B. The MCTAL format has the MCNP code
print the sensitivity profiles in a special file called ksental which is
similar to a mctal file for tallies, and can be plotted by MCPLOT. The
TSUNAMI-B format is defined in [Table 6.5.A.2 of 323]. The concepts used
by the MCNP and SCALE codes are not necessarily compatible depending on
the sensitivity profile options in either code, so the TSUNAMI-B format
may not be able to capture everything that the MCNP code can compute. A
description of the formats are given below.

An example illustrating these concepts:

```
KOPTS BLOCKSIZE = 5 KSENTAL = TSUNAMI-B
```

By default the MCNP code prints the sensitivity profiles to the output
file. These are located below 'the box' with the k results with the
heading 'nuclear data sensitivity profiles'. The ordering of results
changes depending upon the requested information. Regardless, the
sensitivities are presented as the sensitivity result (integrated over
an energy bin) and its associated relative uncertainty. Note that
because sensitivities may either be positive or negative, those near
zero may have a very large (greater than one) relative uncertainty, but
the absolute uncertainty may be quite small.

If no energy bins are requested, then the sensitivities will be
presented as:

| ZAID   | REACTION   | SENS   | REL UNC   |
|--------|------------|--------|-----------|

The ZAID is the first 12 characters of the full table identifier. If
energy bins are requested, then the sensitivities will be presented as a
function of energy for each isotope and reaction:

1

| ELOW   | EHIGH   | SENS   | REL UNC   |
|--------|---------|--------|-----------|

Here ELOW and EHIGH denote the energy bin boundaries. These energy-
resolved results may be plotted for visualization in various plotting
programs (Gnuplot, Microsoft Excel, etc.). When doing so, it is usually
recommended to plot the profiles per unit lethargy (divide each
sensitivity by the logarithm of the ratio of EHIGH to ELOW ) on a semi-
log x axis. Doing so makes it visually accurate in that areas under
curves are visually representative of magnitudes of sensitivity
coefficients integrated over energy ranges.

If incident energy grids for secondary distributions are requested, then
an energy-resolved profile in the above format is given for each
incident energy bin. For cosine bins, if an ERG parameter is specified,
then additional grids in the above format is given for each cosine bin.
If no ERG parameter is specified, but COS bins are, then the following
results are given for all outgoing energies:

```
1 CLOW CHIGH SENS REL UNC
```

Here CLOW and CHIGH are the lower and upper cosine bounds.

If the KOPTS option KSENTAL = MCTAL , results will be output in a
special MCTAL-formatted file called ksental . This MCTAL file format is
very much like the standard MCTAL file except that the symbols for bins
have different meanings. These are:

| F   | spatial zones as cells or materials (0 denoting all cells)   |
|-----|--------------------------------------------------------------|
| D   | unused                                                       |
| U   | unused                                                       |
| S   | isotopes                                                     |
| M   | reaction MTs                                                 |
| C   | cosine bins                                                  |
| E   | energy bins                                                  |
| T   | incident energy bins (for fission χ or scattering laws)      |

The MCNP tally plotter, MCPLOT may be loaded to plot these results.
Again, the results should be normalized to be per unit lethargy with the
'lethargy' option and plotted on a semi-log x axis for visually accurate
area plots.

If the KOPTS option KSENTAL = TSUNAMI-B , results will be output in
TSUNAMI-B format. The TSUNAMI-B format is given in the n[Table 6.5.A.2
of 323]. Because the SCALE and MCNP6 sensitivity capabilities are
different, not all concepts in each code perfectly translate. In writing
the TSUNAMI-B file format, the MCNP code will do the following:

- Multiple energy grids, which is possible in the MCNP code by multiple uses of the KSEN card, are not supported by TSUNAMI-B. To handle this, each instance of the KSEN card is listed in the file one after the other. For use in SCALE plotting tools, these will need to be split into multiple files.
- Unlike the MCNP code, energy units in SCALE are in eV, not MeV. The TSUNAMI-B format gives the energies in eV.
- The concept of a unit is not defined in the MCNP code, and the portion of the header that reports a unit number will give a 0 if no spatial zoning is involved, 1 if the zoning is by cell, and 2 if it is by material. The entry that follows (normally the region within the unit) is an enumeration of each spatial zone (the first zone has a '1', the second a '2', and so on).
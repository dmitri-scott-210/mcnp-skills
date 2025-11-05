---
title: "Chapter 2.12 - Perturbations"
chapter: "2.12"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/2_Geometry,_Data,_Physics,_and_Mathematics/2.12_Perturbations.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

where ⊕ is bitwise XOR, glyph[greatermuch] is right shift,
glyph[lessmuch] is left shift, and rotate\_left ( a, b ) rotates the bits
of a over b positions to the left with overflow being placed on the
right. All arithmetic is performed on 64 bit unsigned integers. The
resulting integer t n is converted to a floating point value ξ that
spans (0 , 1) exclusive.

This generator has a few key advantages in comparison to the LCGs [186].
First, due to the use of the counter n within its construction, each
initial ( a 0 , b 0 , c 0 ) configuration will generate an independent
sequence of at least 2 64 values. As such, one does not need to skip
through the sequence to achieve independence. Second, the generator
produces significantly higher quality bits, with no known test at the
time of this writing indicating correlation between bits of the
sequence.

As used within the MCNP code, the value a 0 is the user-provided SEED
value on the RAND card. The upper 32 bits of b 0 is a 'stream type'
identifier. For example, 1 corresponds to the generator used for
particle transport, and 4 corresponds to the generator used for tallies
that need random samples. The lower 32 bits of b 0 are reserved. c 0 is
the history index. Then, prior to use, the generator is iterated 18
times to thoroughly shuffle the state.

When used in this fashion, each history is provided an independent
sequence of at least length 2 64 , effectively preventing random number
reuse. For this reason, sequence overrun does not need to be (and is
not) tracked with SFC64 in the same manner as stride overrun needs to be
tracked for LCGs. In addition, changing the SEED value (even from 1 to
2) changes the stream for every single particle.

## 2.12 Perturbations

The evaluation of response or tally sensitivities to cross-section data
involves finding the ratio of the change in a tally to the infinitesimal
change in the data, as given by the Taylor series expansion. In
deterministic methods, this ratio is approximated by performing two
calculations, one with the original data and one with the perturbed
data. This approach is useful even when the magnitude of the
perturbation becomes very small. In Monte Carlo methods, however, this
approach fails as the magnitude of the perturbation becomes small
because of the uncertainty associated with the response. For this
reason, the differential operator technique was developed.

The differential operator perturbation technique as applied in the Monte
Carlo method was introduced by Olhoeft [187] in the early 1960s. Nearly
a decade after its introduction, this technique was applied to geometric
perturbations by Takahashi [188]. A decade later, the method was
generalized for perturbations in cross-section data by Hall [189, 190]
and later Rief [191]. A rudimentary implementation into the MCNP code
followed shortly thereafter [192]. With an enhancement of the user
interface and the addition of second order effects, this implementation
has evolved into a standard MCNP feature.

## 2.12.1 Derivation of the Operator

In the differential operator approach, a change in the Monte Carlo
response c , due to changes in a related data set (represented by the
parameter v ), is given by a Taylor series expansion

<!-- formula-not-decoded -->

where the n th-order coefficient is

This can be written as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

for the data set where K b ( h ) is some constant, B represents a set of
macroscopic cross sections, and H represents a set of energies or an
energy interval.

For a track-based response estimator where t j is the response estimator
and q j is the probability of path segment j (path segment j is
comprised of segment j -1 plus the current track). This gives

or where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

With some manipulations presented in [193, 194], the path segment
estimator γ nj t j can be converted to a particle history estimator of
the form where p i is the probability of the i th history and V ni is
the n th-order coefficient estimator for history i , given by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Note that this sum involves only those path segments j ′ in particle
history i . The Monte Carlo expected value of u n becomes

<!-- formula-not-decoded -->

for a sample of N particle histories.

The probability of path segment j is the product of the track
probabilities,

<!-- formula-not-decoded -->

where r k is the probability of track k and segment j contains m +1
tracks. If the k th track starts with a neutron undergoing reaction type
'a' at energy E ′ and is scattered from angle θ ′ to angle θ and E ,
continues for a length λ k , and collides, then

<!-- formula-not-decoded -->

where x a ( E ′ ) is the macroscopic reaction cross section at energy E
′ , x T ( E ′ ) is the total cross section at energy E ′ , and P a ( E ′
→ E ; θ ′ → θ )d E d θ is the probability distribution function in phase
space of the emerging neutron. If the track starts with a collision and
ends in a boundary crossing, then

<!-- formula-not-decoded -->

If the track starts with a boundary crossing and ends with a collision,

<!-- formula-not-decoded -->

And finally, if the track starts and ends with boundary crossings

<!-- formula-not-decoded -->

## 2.12.1.1 First Order

For a first-order perturbation, the differential operator becomes

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

whereas,

Then where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

for a track segment k that starts with a particle undergoing reaction
type 'a' at energy E ′ and is scattered to energy E and collides after a
distance λ k . Note that δ hE ′ and δ ba are unity if h = E and b = a ;
otherwise they vanish. For other types of tracks (for which the various
expressions for r k were given in the previous section), that is,
collision to boundary, boundary to collision, and boundary to boundary,
derivatives of r k can be taken leading to one or more of these four
terms for β j ′ k .

The second term of γ 1 j ′ is where the tally response is a linear
function of some combination of reaction cross sections, or

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where c is an element of the tally cross sections, c ∈ C , and may be an
element of the perturbed cross sections, c ∈ B . Then,

<!-- formula-not-decoded -->

R 1 j ′ is the fraction of the reaction rate tally involved in the
perturbation. If none of the nuclides participating in the tally is
involved in the perturbation, then R 1 j ′ = 0 , which is always the
case for F1, F2, and F4 tallies without FM cards. For F4 tallies with an
FM card, if the FM card multiplicative constant is positive (no flag to
multiply by atom density) it is assumed that the FM tally cross sections
are unaffected by the perturbation and R 1 j ′ = 0 . For KCODE k eff
track length estimates, F6 and F7 heating tallies, and F4 tallies with
FM cards with negative multipliers (multiply by atom density to get
macroscopic cross sections), if the tally cross section is affected by
the perturbation, then R 1 j ′ &gt; 0 . For k eff and F6 and F7 tallies in
perturbed cells where all nuclides are perturbed, generally R 1 j ′ = 1
.

Finally, the expected value of the first-order coefficient is

<!-- formula-not-decoded -->

## 2.12.1.2 Second Order

For a second-order perturbation, the differential operator becomes

<!-- formula-not-decoded -->

Whereas t j ′ is a linear function of x b ( h ) , then

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Further, and by taking first and second derivatives of the r k terms of
q j ′ as for the first-order perturbation,

<!-- formula-not-decoded -->

where

<!-- formula-not-decoded -->

The expected value of the second-order coefficient is

<!-- formula-not-decoded -->

where β j ′ k and α j ′ k are given by one or more terms as described
above for track k and R 1 j ′ is again the fraction of the perturbation
with nuclides participating in the tally.

## 2.12.1.3 Implementation in the MCNP Code

The total perturbation printed in the MCNP output file is

<!-- formula-not-decoded -->

For each history i and path j ′ ,

<!-- formula-not-decoded -->

Let the first-order perturbation with R 1 j ′ = 0 be

<!-- formula-not-decoded -->

and let the second-order perturbation with R 1 j ′ = 0 be

<!-- formula-not-decoded -->

Then the Taylor series expansion for R 1 j ′ = 0 is

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

If R 1 j ′ = 0 then glyph[negationslash]

That is, the R 1 j ′ = 0 case is just a correction to the R 1 j ′ = 0
case.

glyph[negationslash]

In the MCNP code, P 1 j ′ and P 2 j ′ are accumulated along every track
length through a perturbed cell. All perturbed tallies are multiplied by
and then if R 1 j ′ = 0 the tally is further corrected by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

R 1 j ′ is the fraction of the reaction rate tally involved in the
perturbation. R 1 j ′ = 0 for F1, F2, F4 tallies without FM cards, and
F4 tallies with FM cards with positive multiplicative constants.

glyph[negationslash]

## 2.12.2 Limitations

Although it is always a high priority to minimize the limitations of any
MCNP feature, the perturbation technique has the limitations:

1. A fatal error is generated if a PERT card attempts to unvoid a region. The simple solution is to include the material in the unperturbed problem and void the region of interest with the PERT card [Appendix B of 195].
2. A fatal error is generated if a PERT card attempts to alter a material composition in such a way as to introduce a new nuclide. The solution is to set up the unperturbed problem with a mixture of both materials and introduce PERT cards to remove each [Appendix B of 195].
3. The track length estimate of k eff in KCODE criticality calculations assumes the fundamental eigenfunction (fission distribution) is unchanged in the perturbed configuration.
4. DXTRAN, point detector tallies, and pulse height tallies are not currently compatible with the PERT card.
5. While there is no limit to the number of perturbations, they should be kept to a minimum, as each perturbation can degrade performance by 10-20%.
6. Use caution in selecting the multiplicative constant and reaction number on FM cards used with F4 tallies in perturbation problems.
7. The METHOD keyword can indicate if a perturbation is so large that higher than second-order terms are needed to prevent inaccurate tallies.
8. If a perturbation changes the relative abundances of nuclides (MAT keyword) it is assumed that the perturbation contribution from each nuclide is independent (that is, second-order differential cross terms are neglected).

## 2.12.3 Accuracy

Analyzing the first- and second-order perturbation results presented in
[196] leads to the following rules of thumb. The first-order
perturbation estimator typically provides sufficient accuracy for
response or tally changes that are less than 5%. The default first- plus
second-order estimator offers acceptable accuracy for response changes
that are less than 20-30%. This upper bound depends on the behavior of
the response as a function of the perturbed parameter. The magnitude of
the second-order estimator is a good measure of the range of
applicability. If this magnitude exceeds 30% of the first-order
estimator, it is likely that higher-order terms are needed for an
accurate prediction. The METHOD keyword on the PERT card allows one to
tally the second-order term separate from the first [§5.10.1].

The MCNP perturbation capability assumes that changes in the relative
concentrations or densities of the nuclides in a material are
independent and neglects the cross-differential terms in the second-
order perturbation term when changing two or more cross sections at
once. In some cases there will be a large FALSE second-order
perturbation term. Reference [196] provides more discussion and a method
for calculating the cross terms.

The MCNP perturbation capability has been shown to be inaccurate for
some large but very localized perturbations in criticality problems. An
alternative implementation that only requires post-processing standard
MCNP tallies has been shown to be much more accurate in some cases
[197].
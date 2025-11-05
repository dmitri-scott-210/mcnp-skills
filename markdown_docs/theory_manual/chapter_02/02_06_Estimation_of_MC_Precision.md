---
title: "Chapter 2.6 - Estimation of the Monte Carlo Precision"
chapter: "2.6"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/2_Geometry,_Data,_Physics,_and_Mathematics/2.6_Estimation_of_the_Monte_Carlo_Precision.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

3. Segregate electrons and positrons into separate bins plus a total bin, with the electron bin scores being all negative to reflect their charge. The bins will be for positrons (positive scores), electrons (negative scores), and total. The total bin will be the same as the single bin with the first ELC option above (usually with negative scores because there are more electrons than positrons).

## 2.5.7.5 User Modification

If the above capabilities do not provide exactly what is desired,
tallies can be modified by a user-supplied TALLYX subroutine ( FU card).
As with a user-supplied SOURCE subroutine, which lets the users provide
their own specialized source, the TALLYX subroutine lets the user modify
any tally, with all the programming changes conveniently located in a
single subroutine.

## 2.5.7.6 Tally Output Format

Not only can users change the contents of MCNP tallies, the output
format can be modified as well. Any desired descriptive comment can be
added to the tally title by the tally comment ( FC ) card. The printing
order can be changed ( FQ card) so that instead of, for instance,
getting the default output blocks in terms of time vs. energy, they
could be printed in blocks of segment vs. cosine. The tally bin that is
monitored for the tally fluctuation chart printed at the problem end and
used in the statistical analysis of the tally can be selected ( TF
card). Detector tally diagnostic prints are controlled with the DD card.
Finally, the PRINT card controls what optional tables are displayed in
the output file.

## 2.6 Estimation of the Monte Carlo Precision

Monte Carlo results represent an average of the contributions from many
histories sampled during the problem. An important quantity equal in
stature to the Monte Carlo answer (or tally) itself is the statistical
error or uncertainty associated with the result. The importance of this
error and its behavior versus the number of histories cannot be
overemphasized because the user not only gains insight into the quality
of the result, but also can determine if a tally appears statistically
well behaved. If a tally is not well behaved, the estimated error
associated with the result generally will not reflect the true
confidence interval of the result and, thus, the answer could be
completely erroneous. The MCNP code contains several quantities that aid
the user in assessing the quality of the confidence interval [146].

The purpose of this section is to educate MCNP users about the proper
interpretation of the MCNP estimated mean, relative error, variance of
the variance, and history score probability density function. Carefully
check tally results and the associated tables in the tally fluctuation
charts to ensure a well-behaved and properly converged tally.

## 2.6.1 Monte Carlo Means, Variances, and Standard Deviations

Monte Carlo results are obtained by sampling possible random walks and
assigning a score x i (for example, x i is the energy deposited by the i
th random walk) to each random walk. Random walks typically will produce
a range of scores depending on the tally selected and the variance
reduction chosen.

Suppose f ( x ) is the history score probability density function for
selecting a random walk that scores x to the tally being estimated. The
true answer (or mean) is the expected value of x , E ( x ) , where

<!-- formula-not-decoded -->

The function f ( x ) is seldom explicitly known; thus, f ( x ) is
implicitly sampled by the Monte Carlo random walk process. The true mean
E ( x ) then is estimated by the sample mean x where

<!-- formula-not-decoded -->

where x i is the value of x selected from f ( x ) for the i th history
and N is the number of histories calculated in the problem. The Monte
Carlo mean x is the average value of the scores x i for all the
histories calculated in the problem. The relationship between E ( x )
and x is given by the Strong Law of Large Numbers [17] that states that
if E ( x ) is finite, x tends to the limit E ( x ) as N approaches
infinity.

The variance of the population of x values is a measure of the spread in
these values and is given by [17]:

<!-- formula-not-decoded -->

The square root of the variance is σ , which is called the standard
deviation of the population of scores. As with E ( x ) , σ is seldom
known but can be estimated by Monte Carlo as S

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

When the number of samples is large, the approximation introduced by
removing Bessel's correction ( N -1 → N ) as done in Eq. (2.212) is
generally valid. This approach is used within the MCNP code for
calculations where

and more generally

Figure 2.16: Inaccuracy caused by systematic error versus statistical precision.

<!-- image -->

that rely on history-based statistics. For components that compute batch
statistics, where N is not expected to be very large, Bessel's
correction is retained.

The quantity S is the estimated standard deviation of the population of
x based on the values of x i that were actually sampled (i.e., S is the
sample standard deviation).

The estimated variance of x is given by

<!-- formula-not-decoded -->

These formulas do not depend on any restriction on the distribution of x
or x (such as normality) beyond requiring that E ( x ) and σ 2 exist and
are finite. The estimated standard deviation of the mean x is given by S
x .

It is important to note that S x is proportional to 1 / √ N , which is
the inherent drawback to the Monte Carlo method. To halve S x , four
times the original number of histories must be calculated, a calculation
that can be computationally expensive. The quantity S x can also be
reduced for a specified N by making S smaller, reducing the inherent
spread of the tally results. This can be accomplished by using variance
reduction techniques such as those discussed in §2.7.

## 2.6.2 Precision and Accuracy

There is an extremely important difference between precision and
accuracy of a Monte Carlo calculation. As illustrated in Figure 2.16,
precision is the uncertainty in x caused by the statistical fluctuations
of the x i s for the portion of physical phase space sampled by the
Monte Carlo process. Important portions of physical phase space might
not be sampled because of problem cutoffs in time or energy,
inappropriate use of variance reduction techniques, or an insufficient
sampling of important low-probability events. Accuracy is a measure of
how close the expected value of x , E ( x ) , is to the true physical
quantity being estimated. The difference between this true value and E (
x ) is called the systematic error, which is seldom known. Error or
uncertainty estimates for the results of Monte Carlo calculations refer
only to the precision of the result and not to the accuracy. It is
possible to calculate a highly precise result that is far from the
physical truth because nature has not been modeled faithfully.

## 2.6.2.1 Factors Affecting Problem Accuracy

Three factors affect the accuracy of a Monte Carlo result: (1) the code
and data, (2) problem modeling, and (3) the user. Code factors
encompass: the physics features included in a calculation as well as the
mathematical models used; uncertainties in the data, such as the
transport and reaction cross sections, Avogadro's number, atomic
weights, etc.; the quality of the representation of the differential
cross sections in energy and angle; and coding errors (bugs). All of the
applicable physics must be included in a calculation to produce accurate
results. Even though the evaluations are not perfect, more faithful
representation of the evaluator's data should produce more accurate
results. The descending order of preference for Monte

Carlo data for calculations is continuous energy, thinned continuous
energy, discrete reaction, and multigroup. Coding errors can always be a
problem because no large code is bug-free. The MCNP code, however, is a
very mature and heavily used production code. With steadily increasing
use over the years, the likelihood of a serious coding error continues
to diminish.

The second area, problem-modeling factors, can quite often contribute to
a decrease in the accuracy of a calculation. Many calculations produce
seemingly poor results because the model of the energy and angular
distribution of the radiation source is not adequate. Two other problem-
modeling factors affecting accuracy are the geometric description and
the physical characteristics of the materials in the problem.

The third general area affecting calculational accuracy involves user
errors in the problem input or in usersupplied subroutines and patches
to the MCNP code. The user can also abuse variance reduction techniques
such that portions of the physical phase space are not allowed to
contribute to the results. Checking the input and output carefully can
help alleviate these difficulties. A last item that is often overlooked
is a user's thorough understanding of the relationship of the Monte
Carlo tallies to any measured quantities being calculated. Factors such
as detector efficiencies, data reduction and interpretation, etc., must
be completely understood and included in the calculation, or the
comparison is not meaningful.

## 2.6.2.2 Factors Affecting Problem Precision

The precision of a Monte Carlo result is affected by four user-
controlled choices: (1) forward vs. adjoint calculation, (2) tally type,
(3) variance reduction techniques, and (4) number of histories run.

The choice of a forward vs. adjoint calculation depends mostly on the
relative sizes of the source and detector regions. Starting particles
from a small region is easy to do, whereas transporting particles to a
small region is generally hard to do. Because forward calculations
transport particles from source to detector regions, forward
calculations are preferable when the detector (or tally) region is large
and the source region is small. Conversely, because adjoint calculations
transport particles backward from the detector region to the source
region, adjoint calculations are preferable when the source (or tally)
region is large and the detector region is small. The MCNP code can be
run in multigroup adjoint mode. There is no continuous-energy adjoint
capability.

As alluded to above, the smaller the tally region, the harder it becomes
to get good tally estimates. An efficient tally will average over as
large a region of phase space as practical. In this connection, tally
dimensionality is extremely important. A one-dimensional tally is
typically 10 to 100 times easier to estimate than a two-dimensional
tally, which is 10 to 100 times easier than a three-dimensional tally.
This fact is illustrated in Fig. 2.22 later in this section.

Variance reduction techniques can be used to improve the precision of a
given tally by increasing the nonzero tallying efficiency and by
decreasing the spread of the nonzero history scores. These two
components are depicted in a hypothetical f ( x ) shown in Fig. 2.17.
See §2.6.8 for more discussion about the empirical f ( x ) for each
tally fluctuation chart bin. A calculation will be more precise when the
history-scoring efficiency is high and the variance of the nonzero
scores is low. The user should strive for these conditions in difficult
Monte Carlo calculations. Examples of these two components of precision
are given in §2.6.6.

More histories can be run to improve precision [§2.6.3]. Because the
precision is proportional to 1 / √ N , running more particles is often
costly in computer time and therefore is viewed as the method of last
resort for difficult problems.

Figure 2.17: Hypothetical history-score probability density function.

<!-- image -->

## 2.6.3 Monte Carlo Confidence Intervals and the Central Limit Theorem

To define confidence intervals for the precision of a Monte Carlo
result, the Central Limit Theorem [17] of probability theory is used,
stating that

<!-- formula-not-decoded -->

where α and β can be any arbitrary values and Pr[ Z ] means the
probability of Z . In terms of the estimated standard deviation of x , S
x , this may be rewritten in the following approximation for large N :

<!-- formula-not-decoded -->

This crucial theorem states that for large values of N (that is, as N
tends to infinity) and identically distributed independent random
variables x i with finite means and variances, the distribution of the x
s approaches a normal distribution. Therefore, for any distribution of
tallies (an example is shown in Figure 2.17), the distribution of
resulting x s will be approximately normally distributed, as shown in
Figure 2.16, with a mean of E ( x ) . If S is approximately equal to σ ,
which is valid for a statistically significant sampling of a tally (that
is, N has tended to infinity), then

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

from standard tables for the normal distribution function. Equation
(2.225a) is a 68% confidence interval and Eq. (2.225b) is a 95%
confidence interval.

The key point about the validity of these confidence intervals is that
the physical phase space must be adequately sampled by the Monte Carlo
process. If an important path in the geometry or a window in the cross
sections, for example, has not been well sampled, both x and S x will be
unknowingly incorrect and the results will be wrong, usually tending to
be too small. The user must take great care to be certain that adequate
sampling of the source, transport, and any tally response functions have
indeed taken place. Additional statistical quantities to aid in the
assessment of proper confidence intervals are described in later
portions of this section beginning in §2.6.9.1.

## 2.6.4 Estimated Relative Errors in the MCNP Code

All standard MCNP tallies are normalized to be per starting particle
history (except for some criticality calculations) and are printed in
the output with a second number, which is the estimated relative error

defined as

<!-- formula-not-decoded -->

| n   |   1 |   4 |   16 |   25 |   100 |   400 |
|-----|-----|-----|------|------|-------|-------|
| R   |   1 | 0.5 | 0.25 |  0.2 |   0.1 |  0.05 |

<!-- formula-not-decoded -->

The relative error is a convenient number because it represents
statistical precision as a fractional result with respect to the
estimated mean.

Combining Eqs. (2.209), (2.219), and (2.220), R can be written (for
large N ) as

<!-- formula-not-decoded -->

Several important observations about the relative error can be made from
Eq. (2.226b). First, if all the x i s are nonzero and equal, then R is
zero. Thus, low-variance solutions should strive to reduce the spread in
the x i s. If the x i s are all zero, then R is defined to be zero. If
only one nonzero score is made, R approaches unity as N becomes large.
Therefore, for x i s of the same sign, S x can never be greater than x
because R never exceeds unity. For positive and negative x i s, R can
exceed unity. The range of R values for x i s of the same sign is
therefore between zero and unity.

To determine what values of R lead to results that can be stated with
confidence, consider Eq. (2.226b) for a difficult problem in which
nonzero scores occur very infrequently. In this case,

<!-- formula-not-decoded -->

For clarity, assume that there are n out of N ( n glyph[lessmuch] N )
nonzero scores that are identical and equal to x . With these two
assumptions, R for 'difficult problems' becomes

<!-- formula-not-decoded -->

This result is expected because the limiting form of a binomial
distribution with infrequent nonzero scores and large N is the Poisson
distribution used in detector 'counting statistics.'

Through use of Eq. (2.227b), a table of R values versus the number of
tallies or 'counts' can be generated as shown in Table 2.5. A relative
error of 0.5 is the equivalent of four counts, which is hardly adequate
for a statistically significant answer. Sixteen counts is an
improvement, reducing R to 0.25, but still is not a large number of
tallies. The same is true for n equals 25. When n is 100, R is 0.10, so
the results should be much improved. With 400 tallies, an R of 0.05
should be quite good indeed, except possibly for point-detector and
ring-detector tallies.

Based on this qualitative analysis and the experience of Monte Carlo
practitioners, Table 2.6 presents the recommended interpretation of the
estimated 1 σ confidence interval x (1 ± R ) for various values of R
associated with an MCNP tally. These guidelines were determined
empirically, based on years of experience using the MCNP code on a wide
variety of problems. Just before the tally fluctuation charts, a 'Status
of Statistical Checks' table prints how many tally bins of each tally
have values of R exceeding these recommended guidelines.

Table 2.6: Guidelines for Interpreting the Relative Error, R ∗ .

| Range of R   | Quality of the Tally                   |
|--------------|----------------------------------------|
| 0.50 to 1.00 | Not meaningful                         |
| 0.20 to 0.50 | Factor of a few                        |
| 0.10 to 0.20 | Questionable                           |
| < 0.10       | Generally reliable                     |
| < 0.05       | Generally reliable for point detectors |

∗ R = S x /x and represents the estimated relative error at the 1 σ
level. These interpretations of R assume that all portions of the
problem phase space are being sampled well by the Monte Carlo process.

Point detector tallies generally require a smaller value of R for valid
confidence interval statements because some contributions, such as those
near the detector point, are usually extremely important and may be
difficult to sample well. Experience has shown that for R less than
0.05, point detector results are generally reliable. For an R of 0.10,
point detector tallies may only be known within a factor of a few and
sometimes not that well (see the pathological example §2.6.10).

The MCNP code calculates the relative error for each tally bin in the
problem using Eq. (2.226b). Each x i is defined as the total
contribution from the i th starting particle and all resulting progeny.
This definition is important in many variance reduction methods,
multiplying physical processes such as fission or (n,xn) neutron
reactions that create additional neutrons, and coupled neutron/photon/
electron problems. The i th source particle and its offspring may thus
contribute many times to a tally and all of these contributions are
correlated because they are from the same source particle. The x i s are
all independent from each other.

Figure 2.18 represents the MCNP process of calculating the first and
second moments of each tally bin and relevant totals using three tally
storage blocks of equal length. The hypothetical grid of tally bins in
the bottom half of Figure 2.18 has 24 tally bins including the time and
energy totals. During the course of the i th history, sums are performed
in the first MCNP tally storage block. Some of the tally bins receive no
contributions and others receive one or more contributions. At the
conclusion of the i th history, the sums are added to the second MCNP
tally storage block. The sums in the first MCNP tally storage block are
squared and added to the third tally storage block. The first tally
storage block is then filled with zeros and history i +1 begins. After
the last history N , the estimated tally means are computed using the
second MCNP tally storage block and Eq. (2.209). The estimated relative
errors are calculated using the second and third MCNP tally storage
blocks and Eq. (2.226b). This method of estimating the statistical
uncertainty of the result produces the best estimate because the batch
size is one, which minimizes the variance of the variance [147-149].

Note that there is no guarantee that the estimated relative error will
decrease inversely proportional to the N as required by the Central
Limit Theorem because of the statistical nature of the tallies. Early in
the problem, R will generally have large statistical fluctuations.
Later, infrequent large contributions may cause fluctuations in S x and
to a lesser extent in x and therefore in R . The MCNP code calculates a
figure of merit for one bin of each numbered tally to aid the user in
determining the statistical behavior as a function of N and the
efficiency of the tally.

## 2.6.5 MCNP Figure of Merit

The estimated relative error squared, R 2 , should be proportional to 1
/N , as shown by Eq. (2.226b). The computer time T used in an MCNP
problem should be directly proportional to N ; therefore, R 2 T should
be approximately a constant within any one Monte Carlo calculation. It
is convenient to define a FOM of a tally to be

<!-- formula-not-decoded -->

<!-- image -->

/ok is the score from the present history

Figure 2.18: Hypothetical energy-time-binned tally scores.

<!-- formula-not-decoded -->

| FOM   |   1 |   10 |   100 |   1000 |   10000 |
|-------|-----|------|-------|--------|---------|
| R     |   1 | 0.32 |   0.1 |  0.032 |    0.01 |

The MCNP code prints the FOM for the Tally Fluctuation Chart (TFC) bin
of each numbered tally as a function of N , where the unit of computer
time T is minutes. The table is printed in particle increments of 1000
up to 20,000 histories. Between 20,000 and 40,000 histories, the
increment is doubled to 2000. This trend continues, producing a table of
up to 20 entries. The default increment can be changed by the 5th entry
on the PRDMP card.

The FOM is a very important statistic about a tally bin and should be
studied by the user. It is a tally reliability indicator in the sense
that if the tally is well behaved, the FOM should be approximately a
constant with the possible exception of statistical fluctuations very
early in the problem. An order-of-magnitude estimate of the expected
fractional statistical fluctuations in the FOM is 2 R . This result
assumes that both the relative statistical uncertainty in the relative
error is of the order of the relative error itself and the relative
error is small compared to unity. The user should always examine the
tally fluctuation charts at the end of the problem to check that the FOM
s are approximately constant as a function of the number of histories
for each tally.

The numerical value of the FOM can be better appreciated by considering
the relation

<!-- formula-not-decoded -->

Table 2.7 shows the expected value of R that would be produced in a one-
minute problem ( T = 1 ) as a function of the value of the FOM . It is
clearly advantageous to have a large FOM for a problem because the
computer time required to reach a desired level of precision is
proportionally reduced. Examination of Eq. (2.228a) shows that doubling
the FOM for a problem will reduce the computer time required to achieve
the same R by a factor of two.

Another interpretation for the FOM involves defining the problem's
particle computation rate t as

<!-- formula-not-decoded -->

where t is the number of particles per minute for a problem on a
specific computer and N is the number of particles run in the problem.
Substituting Eq. (2.228c) into Eq. (2.228a) and using Eqs. (2.209),
(2.222), and (2.226a), the FOM becomes where S is the sample standard
deviation (not the estimated standard deviation of the mean, S x ). The
squared quantity is a ratio of the desired result divided by a measure
of the spread in the sampled values. This ratio is called the tally
signal-to-noise ratio:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The quantity x/S approaches the expected value of the signal-to-noise
ratio for a problem tally bin as N becomes large. Using Eq. (2.228e),
the FOM becomes

<!-- formula-not-decoded -->

The FOM is directly proportional to the particles per minute t (as would
be expected) and the tally bin signal-to-noise ratio squared. The tally
bin signal-to-noise ratio is dependent on the shape of the underlying
history score probability density function f ( x ) for the tally bin
[§2.6.8]. To increase the FOM , t and/or the signal-to-noise ratio can
be increased. Because x should be the same for the problems with
different variance reduction, increasing the FOM is equivalent to
increasing t/S 2 (decreasing S with variance reduction techniques often
decreases t ). It is usually worthwhile to optimize the tally efficiency
by intelligently running various variance reduction methods and using
the largest FOM consistent with good phase-space sampling (good sampling
can often be inferred by examining the cell particle activity in PRINT
Table 126). The MCNP code prints both the empirical f ( x ) and signal-
to-noise ratio for the tally fluctuation chart bin of each tally in
PRINT Table 161.

In summary, the FOM has three uses. One important use is as a tally
reliability indicator. If the FOM is not approximately a constant
(except for statistical fluctuations early in the problem), the
confidence intervals may not overlap the expected score value, E ( x ) ,
the expected fraction of the time (see Eqs. (2.225a) and (2.225b)). A
second use for the FOM is to optimize the efficiency of the Monte Carlo
calculation by making several short test runs with different variance
reduction parameters and then selecting the problem with the largest FOM
. Remember that the statistical behavior of the FOM (that is, R ) for a
small number of histories may cloud the selection of techniques
competing at the same level of efficiency. A third use for the FOM is to
estimate the computer time required to reach a desired value of R by
using T ∼ 1 / ( R 2 FOM ) .

## 2.6.6 Separation of Relative Error into Two Components

Three factors that affect the efficiency of a Monte Carlo calculation
are (1) history-scoring efficiency, (2) dispersions in non-zero history
scores, and (3) computer time per history. All three factors are
included in the FOM . The first two factors control the value of R ; the
third is T .

The relative error can be separated into two components: the non-zero
history-scoring efficiency component R 2 eff and the intrinsic spread of
the nonzero x i scores R 2 int . Defining q to be the fraction of
histories producing nonzero x i s, Eq. (2.220) can be rewritten as
glyph[negationslash]

glyph[negationslash]

<!-- formula-not-decoded -->

glyph[negationslash]

glyph[negationslash]

Table 2.8: Expected Values of R eff as a Function of the Fraction of Histories Producing Non-zero Scores ( q ) and the Number of Histories ( N )

| N    |     q |     q |     q |     q |
|------|-------|-------|-------|-------|
|      | 0.001 | 0.01  | 0.1   | 0.5   |
| 10 3 | 0.999 | 0.315 | 0.095 | 0.032 |
| 10 4 | 0.316 | 0.099 | 0.03  | 0.01  |
| 10 5 | 0.1   | 0.031 | 0.009 | 0.003 |
| 10 6 | 0.032 | 0.01  | 0.003 | 0.001 |

Note by Eq. (2.220) that the first two terms are the relative error of
the qN non-zero scores. Thus defining, glyph[negationslash]

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

glyph[negationslash]

<!-- formula-not-decoded -->

For identical nonzero x i s, R 2 int is zero and for a 100% scoring
efficiency, R 2 eff is zero. It is usually possible to increase q for
most problems using one or more of the MCNP variance reduction
techniques. These techniques alter the random walk sampling to favor
those particles that produce a nonzero tally. The particle weights are
then adjusted appropriately so that the expected tally is preserved.
This topic is described in §2.7. The sum of the two terms of Eq.
(2.229d) produces the same result as Eq. (2.220). Both R 2 int and R 2
eff are printed for the tally fluctuation chart bin of each tally so
that the dominant component of R can be identified as an aid to making
the calculation more efficient.

These equations can be used to better understand the effects of scoring
inefficiency; that is, those histories that do not contribute to a
tally. Table 2.8 shows the expected values of R eff as a function of q
and the number of histories N . This table is appropriate for identical
nonzero scores and represents the theoretical minimum relative error
possible for a specified q and N . It is no surprise that small values
of q require a correspondingly large number of particles to produce
precise results.

A practical example of scoring inefficiency is the case of infrequent
high-energy particles in a down-scatteringonly problem. If only a small
fraction of all source particles has an energy in the highest energy
tally bin, the dominant component of the relative error will probably be
the scoring efficiency because only the high-energy source particles
have a nonzero probability of contributing to the highest energy bin.
For problems of this kind, it is often useful to run a separate problem
starting only high-energy particles from the source and to raise the
energy cutoff. The much improved scoring efficiency will result in a
much larger FOM for the high-energy tally bins.

To further illustrate the components of the relative error, consider the
five examples of selected discrete probability density functions shown
in Fig. 2.19. Cases (a) and (b) have no dispersion in the nonzero
scores, cases (c) and (d) have 100% scoring efficiency, and case (e)
contains both elements contributing to R . The most efficient problem is
case (c). Note that the scoring inefficiency contributes 75% to R in
case (e), the second worst case of the five.

## 2.6.7 Variance of the Variance

Previous sections have discussed the relative error R and figure of
merit FOM as measures of the quality of the mean. A quantity called the
relative variance of the variance (VOV) is another useful tool that can
assist the user in establishing more reliable confidence intervals. The
VOV is the estimated relative variance

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Figure 2.19: Five various distributions with an identical mean of 0.5.

of the estimated R . The VOV involves the estimated third and fourth
moments of the empirical history score PDF f ( x ) and is much more
sensitive to large history score fluctuations than is R . The magnitude
and trend of the VOV versus the number of particle histories are
indicators of tally fluctuation chart (TFC) bin convergence. Early work
was done by Estes and Cashwell [147] and Pederson [150] later
reinvestigated this statistic to determine its usefulness. Pederson
concluded [146] that the VOV is a much better indicator of confidence
interval validity than R .

The VOV is a quantity that is analogous to the square of the R of the
mean, except it is for R instead of the mean. The estimated relative VOV
of the mean is defined as

<!-- formula-not-decoded -->

where S 2 x is the estimated variance of x and S 2 ( S 2 x ) is the
estimated variance in S 2 x . The VOV is a measure of the relative
statistical uncertainty in the estimated R and is important because S
must be a good approximation of σ to use the Central Limit Theorem to
form confidence intervals.

The VOV for a tally bin [150] is

This is the fourth central moment minus the second central moment
squared, normed by the product of N and the second central moment
squared.

<!-- formula-not-decoded -->

When Eq. (2.231) is expanded in terms of sums of powers of x i , it
becomes or

<!-- formula-not-decoded -->

Now consider the truncated Cauchy formula for the following analysis.
The truncated Cauchy is similar in shape to some difficult Monte Carlo
tallies. After numerous statistical experiments on sampling a truncated
positive Cauchy distribution,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

it is concluded that the VOV should be below 0.1 to improve the
probability of forming a reliable confidence interval [146]. The
quantity 0.1 is a convenient value and is why the VOV is used for the
statistical check and not the square root of the VOV. Multiplying
numerator and denominator of Eq. (2.233) by 1 /N converts the terms into
x n , averages, and shows that the VOV is expected to decrease as 1 /N .

It is interesting to examine the VOV for the n identical history scores
x ( n glyph[lessmuch] N ) that were used to analyze R in Table 2.5. The
VOV behaves as 1 /N in this limit. Therefore, ten identical history
scores would be enough to satisfy the VOV criterion, a factor of at
least ten less than the R criterion. There are two reasons for this
phenomenon: (1) the VOV is a squared quantity, so it is naturally
smaller; and (2) the history scores will ordinarily not be identical and
thus the fourth-moment terms in the VOV will increase rapidly over the
second-moment terms in R .

The behavior of the VOV as a function of N for the TFC bin is printed in
the MCNP output file. Because the VOV involves third and fourth moments,
the VOV is a much more sensitive indicator to large history

scores than the R , which is based on first and second moments. The
desired VOV behavior is to decrease inversely with N . This criterion is
deemed to be a necessary, but not sufficient, condition for a
statistically well-behaved tally result. A tally with a VOV that matches
this criteria is NOT guaranteed to produce a high quality confidence
interval because under sampling of high scores will also underestimate
the higher score moments.

To calculate the VOV of every tally bin, put a nonzero 15th entry on the
DBCN card. This option creates two additional history score moment
tables to sum x 3 i and x 4 i (see Fig. 2.18). This option is not the
default because it increases tally storage, which could be prohibitive
for a problem with many tally bins. The magnitude of the VOV in each
tally bin is reported in the 'Status of Statistical Checks' table.
History-dependent checks of the VOV of all tally bins can be done by
printing the tallies to the output file at some frequency using the
first entry on the PRDMP card.

## 2.6.8 Empirical History-score Probability Density Function f ( x )

## 2.6.8.1 Introduction

This section discusses another statistic that is useful in assessing the
quality of confidence intervals from Monte Carlo calculations. Consider
a generic Monte Carlo problem with difficult to sample, but extremely
important, large history scores. This type of problem produces three
possible scenarios [146].

The first, and obviously desired, case is a correctly converged result
that produces a statistically correct confidence interval. The second
case is the sampling of an infrequent, but very large, history score
that causes the mean and R to increase and the FOM to decrease
significantly. This case is easily detectable by observing the behavior
of the FOM and the R in the TFCs.

The third and most troublesome case yields an answer that appears
statistically converged based on the accepted guidelines described
previously, but in fact may be substantially smaller than the correct
result because the large history tallies were not well sampled. This
situation of too few large history tallies is difficult to detect. The
following sections discuss the use of the empirical history score PDF f
( x ) to gain insight into the TFC bin result. A pathological example to
illustrate the third case follows.

## 2.6.8.2 The History-score Probability Density Function f ( x )

A history score posted to a tally bin can be thought of as having been
sampled from an underlying and generally unknown history score PDF f ( x
) , where the random variable x is the score from one complete particle
history to a tally bin. The history score can be either positive or
negative. The quantity f ( x )d x is the probability of selecting a
history score between x and x +d x for the tally bin. Each tally bin
will have its own f ( x ) .

The most general form for expressing f ( x ) mathematically is

<!-- formula-not-decoded -->

where f c ( x ) is the continuous non-zero part and ∑ m i =1 p i δ ( x
-x i ) represents the m different discrete components occurring at x i
with probability p i . An f ( x ) could be composed of either or both
parts of the distribution. A history score of zero is included in f ( x
) as the discrete component δ ( x -0) .

By the definition of a PDF,

<!-- formula-not-decoded -->

As discussed in §2.6.1, f ( x ) is used to estimate the mean, variance,
and higher moment quantities such as the VOV.

## 2.6.8.3 The Central Limit Theorem and f ( x )

As discussed in §2.6.3, the Central Limit Theorem (CLT) states that the
estimated mean will appear to be sampled from a normal distribution with
a known standard deviation σ/ √ N when N approaches infinity. In
practice, σ is NOT known and must be approximated by the estimated
standard deviation S . The major difficulty in applying the CLT
correctly to a Monte Carlo result to form a confidence interval is
knowing when N has approached infinity.

The CLT requires the first two moments of f ( x ) to exist. Nearly all
MCNP tally estimators (except point detectors with zero neighborhoods in
a scattering material and some exponential transform problems) satisfy
this requirement. Therefore, the history score PDF f ( x ) also exists.
One can also examine the behavior of f ( x ) for large history scores to
assess if f ( x ) appears to have been 'completely' sampled. If
'complete' sampling has occurred, the largest values of the sampled x s
should have reached the upper bound (if such a bound exists) or should
decrease faster than 1 / x 3 so that E ( x 2 ) = GLYPH&lt;1&gt; ∞ -∞ x 2 f ( x
)d x exists ( σ is assumed to be finite in the CLT). Otherwise, N is
assumed not to have approached infinity in the sense of the CLT. This is
the basis for the use of the empirical f ( x ) to assess Monte Carlo
tally convergence.

The argument should be made that since S must be a good estimate of σ ,
the expected value of the fourth history score moment E ( x 2 ) =
GLYPH&lt;1&gt; ∞ -∞ x 4 f ( x )d x should exist. It will be assumed that only
the second moment needs to exist so that the f ( x ) convergence
criterion will be relaxed somewhat. Note that [146] states that the VOV
is still a good convergence metric even if four moments do not exist.
Nevertheless, this point should be kept in mind.

## 2.6.8.4 Analytic Study of f ( x ) for Two-state Monte Carlo Problems

Booth [151, 152] examined the distribution of history scores
analytically for both an analog two-state splitting problem and two
exponential transform problems. This work provided the theoretical
foundation for statistical studies [153] on relevant analytic functions
to increase understanding of confidence interval coverage rates for
Monte Carlo calculations.

It was found that the two-state splitting problem f ( x ) decreases
geometrically as the score increases by a constant increment. This is
equivalent to a negative exponential behavior for a continuous f ( x ) .
The f ( x ) for the exponential transform problem decreases
geometrically with geometrically increasing x . Therefore, the splitting
problem produces a linearly decreasing f ( x ) for the history score on
a lin-log plot of the score probability versus score. The exponential
transform problem generates a linearly decreasing score behavior (with
high score negative exponential roll off) on a log-log plot of the score
probability versus score plot. In general, the exponential transform
problem is the more difficult to sample because of the larger impact of
the low-probability high scores.

The analytic shapes were compared with a comparable problem calculated
with a modified version of the MCNP code. These shapes of the analytic
and empirical f ( x ) s were in excellent agreement [153].

## 2.6.8.5 Proposed Uses for the Empirical f ( x ) in Each TFC Bin

Few papers discuss the underlying or empirical f ( x ) for Monte Carlo
transport problems [138, 146, 154]. The MCNP code provides a visual
inspection and analysis of the empirical f ( x ) for the TFC bin of each
tally. This analysis helps to determine if there are any unsampled
regions (holes) or spikes in the empirical history score PDF f ( x ) at
the largest history scores.

The most important use for the empirical f ( x ) is to help determine if
N has approached infinity in the sense of the CLT so that valid
confidence intervals can be formed. It is assumed that the underlying f
( x ) satisfies the CLT requirements; therefore, so should the empirical
f ( x ) . Unless there is a largest possible history score, the
empirical f ( x ) must eventually decrease more steeply than x -3 for
the second moment ( GLYPH&lt;1&gt; ∞ -∞ x 2 f ( x )d x ) to exist. It is
postulated [155] that if such decreasing behavior in the empirical f ( x
) with no upper bound has not been observed, then N is not large enough
to satisfy the CLT because f ( x ) has not been completely sampled.
Therefore, a larger N is required before a confidence interval can be
formed. It is important to note that this convergence criterion is NOT
affected by any correlations that may exist between the estimated mean
and the estimated R [146]. In principle, this lack of correlation should
make the f ( x ) diagnostic robust in assessing 'complete' sampling.

Both the analytic and empirical history score distributions suggest that
large score fill-in and one or more extrapolation schemes for the high
score tail of the f ( x ) could provide an estimate of scores not yet
sampled to help assess the impact of the unsampled tail on the mean. The
magnitude of the unsampled tail will surely affect the quality of the
tally confidence interval.

## 2.6.8.6 Creation of f ( x ) for TFC Bins

The creation of the empirical f ( x ) in the MCNP code automatically
covers nearly all TFC bin tallies that a user might reasonably be
expected to make, including the effect of large and small tally
multipliers. A logarithmically spaced grid is used for accumulating the
empirical f ( x ) because the tail behavior is assumed to be of the form
1 /x n , n &gt; 3 (unless an upper bound for the history scores exists).
This grid produces an equal width histogram straight line for f ( x ) on
a log-log plot that decreases n decades in f ( x ) per decade increase
in x .

Ten bins per x decade are used and cover the unnormalized tally range
from 10 -30 to 10 30 . The term 'unnormalized' indicates that
normalizations that are not performed until the end of the problem, such
as cell volume or surface area, are not included in f ( x ) . The user
can multiply this range at the start of the problem by the 16th entry on
the DBCN card when the range is not sufficient. Both history score
number and history score for the TFC bin are tallied in the x grid.

With this x grid in place, the average empirical f ( x i ) between x i
and x i +1 is defined to be

<!-- formula-not-decoded -->

where x i +1 = 1 . 2589 x i . The quantity 1.2589 is 10 0 . 1 and comes
from 10 equally spaced log bins per decade. The calculated f ( x i ) s
are available on printed plots or by using the 'z' plot option (MCPLOT)
with the TFC command mnemonics. Any history scores that are outside the
x grid are counted as either above or below to provide this information
to the user.

Negative history scores can occur for some electron charge deposition
tallies. The default MCNP behavior is that any negative history score
will be lumped into one bin below the lowest history score in the built-
in grid (the default is 10 -30 ). If the 16th entry on the DBCN card is
negative, f ( -x ) will be created from the negative scores and the
absolute value of the 16th entry on the DBCN card will be used as the
score grid multiplier. Positive history scores then will be lumped into
the lowest bin because of the sign change.

```
1 tally 1
```

runtpe = constant\_sdef\_dist.mcnp.inp.txtr.h5

constant\_sdef\_dist.mcnp.inp.txtr.h5

Figure 2.20: Example empirical history-score PDF for a uniform 0-10 MeV source.

<!-- image -->

Figure 2.20 and Fig. 2.21 show two simple examples of empirical f ( x )
s from the MCNP code for 10 million histories each. Figure 2.20 is from
an energy leakage tally directly from a source that is uniform in energy
from 0 to 10 MeV. The analytic f ( x ) is a constant 0.1 between 0 and
10 MeV. The empirical f ( x ) shows the sampling, which is 0.1 with
statistical noise at the lower x (i.e., E , because the energy of the
particle is the score) bins where fewer samples are made in the smaller-
width energy bins. The MCNP input file for Fig. 2.20 is given in Listing
2.3 and plotting with the command input file given in Listing 2.4.

Listing 2.3: constant\_sdef\_dist.mcnp.inp.txt

<!-- image -->

Listing 2.4: constant\_sdef\_dist.mcnp.comin.txt

runtpe = theory\_manual\_exponential\_track\_len\_dist.mcnp.inpr
theory\_manual\_exponential\_track\_len\_dist.mcnp.inpr.h5

Figure 2.21: Example empirical history-score PDF for the first collision flux.

<!-- image -->

```
2 tfc p 3 end
```

Figure 2.21 shows the sampled distance to first collision in a material
that has a macroscopic cross section of about 0.1 cm -1 . This analytic
function is a negative exponential given by f ( x ) = Σ exp( -Σ x ) (see
§2.4.2) with a mean of 10. The empirical f ( x ) transitions from a
constant 0.1 at values of x less than unity to the expected negative
exponential behavior for larger values of x . The MCNP input file for
Fig. 2.21 is given in Listing 2.5 and plotting with the command input
file given in Listing 2.6.

```
1 Exponential distance-to-collision distribution example 2 10 1 0.005 -1 imp:n=1 3 20 0 1 imp:n=0 4 5 1 so 1e6 6 7 sdef pos= 0 0 0 erg=355e-5 8 m1 1001 1 9 f4:n 10 10 ft4 inc $ Assign user binning by collision. 11 fu4 0 $ Consider only uncollided values. 12 print $ Print all output file tables. 13 prdmp 2j 1 $ Write MCTAL file at conclusion of calculation. 14 cut:n j 350e-5 15 nps 1e7
```

Listing 2.5: exponential\_track\_len\_dist.mcnp.inp.txt

```
1 tally 4 2 tfc p 3 loglog 4 xlims 1e-7 1e3 5 noerrbar 6 end
```

Listing 2.6: exponential\_track\_len\_dist.mcnp.comin.txt

## 2.6.8.7 Pareto Fit to the Largest History Scores for the TFC Bin

The slope n in 1 /x n of the largest history tallies x must be estimated
to determine when the largest history scores decrease faster than 1 /x 3
. The 201 largest history scores for each TFC bin are continuously
updated and saved during the calculation. A generalized Pareto function
[156],

<!-- formula-not-decoded -->

is used to fit the largest x s. This function fits a number of extreme
value distributions including 1 /x n , exponential ( k = 0 ), and
constant ( k = -1 ). The large history score tail fitting technique uses
the robust 'simplex' algorithm [157], which finds the values of a and k
that best fit the largest history scores by maximum likelihood
estimation.

The number of history score tail points used for the Pareto fit is a
maximum of 201 points because this provides about 10% precision [156] in
the slope estimator at n = 3 . The precision increases for smaller
values of n and vice versa. The number of points actually used in the
fit is the lesser of 5% of the nonzero history scores or 201. The
minimum number of points used for a Pareto fit is 25 with at least two
different values,

which requires 500 nonzero history scores with the 5% criterion. If less
than 500 history scores are made in the TFC bin, no Pareto fit is made.

From the Pareto fit, the slope of f ( x large ) is defined to be

<!-- formula-not-decoded -->

A slope value of zero is defined to indicate that not enough f ( x large
) tail information exists for a SLOPE estimate. The SLOPE is not allowed
to exceed a value of 10 (a 'perfect score'), which would indicate an
essentially negative exponential decrease. If the 100 largest history
scores all have values with a spread of less than 1%, an upper limit is
assumed to have been reached and the SLOPE is set to 10. The SLOPE
should be greater than 3 to satisfy the second moment existence
requirement of the CLT. Then, f ( x ) will appear to be 'completely'
sampled and hence N will appear to have approached infinity.

A printed plot of f ( x ) is automatically generated in the MCNP output
file if the SLOPE is less than 3 (or if any of the other statistical
checks described in the next section do not pass). If 0 &lt; SLOPE &lt; 10 ,
several S s appear on the printed plot to indicate the Pareto fit,
allowing the quality of the fit to the largest history scores to be
assessed visually. If the largest scores are not Pareto in shape, the
SLOPE value may not reflect the best estimate of the largest history
score decrease. A new SLOPE can be estimated graphically, as described
in §2.6.8.8. A blank or 162 on the PRINT card also will cause printed
plots of the first two cumulative moments of the empirical f ( x ) to be
made. Graphical plots of various f ( x ) quantities can be made using
the 'z' plot option (MCPLOT) with the TFC plot command. These plots
should be examined for unusual behavior in the empirical f ( x ) ,
including holes or spikes in the tail. The MCNP code tries to assess
both conditions and prints a message if either condition is found.

## 2.6.8.8 Graphical Estimation of the Tally Slope when the Slope Test Fails

When the SLOPE test fails (SLOPE is less than or equal to three), the
calculation should not be rejected without further analysis. Sometimes
the SLOPE test fails because, although the MCNP code uses a Pareto
distribution to fit the tally tail, the tally tail may not be well
represented by a Pareto distribution. In this case, the user can
manually assess the slope using a ruler and MCNP PRINT Table 161.

The slope estimator in the MCNP code is designed to estimate the number
of score moments that exist in a calculation. Note that if for large x
the score density f ( x ) doesn't go down at least as fast as Cx -s for
some x &gt; tail then the r th score moment,

<!-- formula-not-decoded -->

is not finite unless r -s &lt; -1 . That is, s &gt; r +1 .

Thus for the second moment ( r = 2 ) to exist s &gt; 3 (needed to use the
Central Limit Theorem) and for the fourth moment ( r = 4 ) to exist s &gt;
5 (desirable so that the VOV is finite, so that the sample variance is a
good estimate of the true variance in the Central Limit Theorem.) If the
tail score density were f ( x ) &lt; Cx -s , then

<!-- formula-not-decoded -->

This derivative measures the number of decades change in f ( x ) per
decade change in x .

The Pareto fit to the score probability density is

<!-- formula-not-decoded -->

1

10

11

12

13

14

15

16

17

For large enough x , this becomes (essentially the Cx -s mentioned
earlier):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Thus the MCNP slope estimator is a measure of the number of decades
decline in f ( x ) per decade decline in x .

MCNP PRINT Table 161 (see Listing 2.7) is a log-log plot, so the user
can check whether the estimate of the tail slope looks reasonable.
Suppose that the MCNP code tells the user:

the estimated inverse power slope of the 198 largest tallies starting at
2.99875E+00 is 1.4253

so the MCNP estimate of the tail in this case is from the last three
bins in the chart. Note that PRINT Table 161 has the number on each bin.
Note the vertical lines on PRINT Table 161 labeled with a 'd'. Each
vertical line is an additional decade in f ( x ) .

Note that taking a ruler and drawing an extrapolation line through the s
s s on the chart from x = 0 . 501 to x = 5 . 01 gives about 1.5 decades
in f ( x ) . This graphically derived line through the s s s thus has
1.5 decades in f ( x ) per decade in x (i.e. slope = 1.5); this is
roughly consistent with the MCNP code's slope estimate of 1.4.

When a straight line is passed through the tail ( *** ), the
extrapolated line from x = 0 . 501 to x = 5 . 01 is off the chart at x =
0 . 501 . Instead of using a full decade to get the 'ruler' slope
estimate, use the 0.5 decade from x = 1 . 58 to x = 5 . 01 . That is,
extrapolate a straight line through the tail and look at the slope of
this line. The line changes well over 3 decades (perhaps 3.3 decades) in
f ( x ) in a 0.5 decade in x indicating that the slope is at least 6.
Thus the user can conclude that the Pareto fit was not a good fit to f (
x ) and the user can be fairly confident that at least 5 moments of the
score distribution exist. It appears this calculation can thus be
accepted despite the slope estimate warning.

Listing 2.7: Sample MCNP Print Table 161

<!-- image -->

| abscissa ordinate log plot of tally probability density function in tally fluctuation chart bin(d=decade,slope= 1.4)   | abscissa ordinate log plot of tally probability density function in tally fluctuation chart bin(d=decade,slope= 1.4)            | abscissa ordinate log plot of tally probability density function in tally fluctuation chart bin(d=decade,slope= 1.4)            |
|------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                        | 5 6.45-07 -6.190 *************** | | |                                                                                          | 3 2.51-01                                                                                                                       |
|                                                                                                                        | 338 3.46-05 -4.460 ************************* | ************************** | ******** |                                          | 4 3.16-01                                                                                                                       |
|                                                                                                                        | 388 3.16-05 -4.500 ************************* | ************************** | ******* |                                           | 5 3.98-01                                                                                                                       |
|                                                                                                                        | 1345 8.70-05 -4.061 ************************* | ************************** | ****************** |                               | 6 5.01-01                                                                                                                       |
|                                                                                                                        | 629 3.23-05 -4.491 ************************* | ************************** | ******* |                                           | 7 6.31-01                                                                                                                       |
|                                                                                                                        | 1881 7.68-05 -4.115 ************************* | ************************** | ***************** |                                | 8 7.94-01                                                                                                                       |
| 1.00+00                                                                                                                | 32836 1.06-03 -2.973 ************************* | ************************** | ************************* | ********************* | 32836 1.06-03 -2.973 ************************* | ************************** | ************************* | ********************* |
|                                                                                                                        | 2.53-04 -3.597 mmmmmmmmmmmmmmmmmmmmmmmmm|mmmmmmmmmmmmmmmmmmmmmmmmmm|mmmmmmmmmmmmmmmmmmmmmmmmm|mmmm                              | 1.26+00 9820                                                                                                                    |
|                                                                                                                        | 719 1.47-05 -4.833 ************************* | ************************* | |                                                    | 1.58+00                                                                                                                         |
|                                                                                                                        | 4453 7.23-05 -4.141 ************************* | ************************** | **************** |                                 | 2.00+00                                                                                                                         |
|                                                                                                                        | 1412 1.82-05 -4.739 ************************* | ************************** | |                                                  | 2.51+00                                                                                                                         |
|                                                                                                                        | 789 8.09-06 -5.092 ************************* | ****************** |s |                                                          | 3.16+00                                                                                                                         |
|                                                                                                                        | 88 7.17-07 -6.145 **************** | s | |                                                                                      | 3.98+00                                                                                                                         |
|                                                                                                                        | 30 1.94-07 | s | |                                                                                                              | 5.01+00 -6.712 *                                                                                                                |
| total                                                                                                                  | 54733 3.65-04 d------------------------d--------------------------d-------------------------d---------------------              | 54733 3.65-04 d------------------------d--------------------------d-------------------------d---------------------              |

## 2.6.9 Forming Statistically Valid Confidence Intervals

The goal of a Monte Carlo calculation is to produce a valid confidence
interval for each tally bin. Section 2.6 has described different
statistical quantities and the recommended criteria to form a valid
confidence interval. Detailed descriptions of the information available
in the output for all tally bins and the TFC bins are now discussed.

## 2.6.9.1 Information Available for Forming Statistically Valid Confidence

The R is calculated for every user-specified tally bin in the problem.
The VOV and the shifted confidence interval center, discussed below, can
be obtained for all bins with a nonzero entry for the 15th entry on the
DBCN card at problem initiation.

## 2.6.9.1.1 R Magnitude Comparisons with MCNP Guidelines

The quality of MCNP tallies historically has been associated with two
statistical checks that have been the responsibility of the user: (1)
for all tally bins, the estimated relative error magnitude rules-of-
thumb that are shown in Fig. 2.5 (that is, R &lt; 0 . 1 for non-point
detector tallies and R &lt; 0 . 05 for point detector tallies); and (2) a
statistically constant FOM in the user-selectable ( TF n card) TFC bin
so that the estimated R is decreasing by 1 / √ N as required by the CLT.

In an attempt to make the user more aware of the seriousness of checking
these criteria, the MCNP code provides checks of the R magnitude for all
tally bins. A summary of the checks is printed in the 'Status of
Statistical Checks' table. Messages are provided to the user giving the
results of these checks.

## 2.6.9.1.2 Asymmetric Confidence Intervals

A correlation exists between the estimated mean and the estimated
uncertainty in the mean [150]. If the estimated mean is below the
expected value, the estimated uncertainty in the mean S x will most
likely be below its expected value. This correlation is also true for
higher moment quantities such as the VOV. The worst situation for
forming valid confidence intervals is when the estimated mean is much
smaller than the expected value, resulting in smaller than predicted
coverage rates. To correct for this correlation and improve coverage
rates, one can estimate a statistic shift in the midpoint of the
confidence interval to a higher value. The estimated mean is unchanged.

The shifted confidence interval midpoint is the estimated mean plus a
term proportional to the third central moment. The term arises from an
Edgeworth expansion [150] to attempt to correct the confidence interval
for non-normality effects in the estimate of the mean. The adjustment
term is given by

<!-- formula-not-decoded -->

Substituting for the estimated mean and expanding produces

<!-- formula-not-decoded -->

The SHIFT should decrease as 1 /N . This term is added to the estimated
mean to produce the midpoint of the now asymmetric confidence interval
about the mean. This value of the confidence interval midpoint can be
used to form the confidence interval about the estimated mean to improve
coverage rates of the true, but unknown, mean E ( x ) . The estimated
mean plus the SHIFT is printed automatically for the TFC bin for all
tallies. A nonzero entry for the 15th DBCN card entry produces the
shifted value for all tally bins.

This correction approaches zero as N approaches infinity, which is the
condition required for the CLT to be valid. Kalos and Whitlock [158]
uses a slightly modified form of this correction to determine if the
requirements of the CLT are 'substantially satisfied.' Their relation is

<!-- formula-not-decoded -->

which is equivalent to

The user is responsible for applying this check.

SHIFT glyph[lessmuch] S x / 2 .

## 2.6.9.1.3 Forming Valid Confidence Intervals for Non-TFC Bins

The amount of statistical information available for non-TFC bins is
limited to the mean and R . The VOV and the center of the asymmetric
confidence can be obtained for all tally bins with a nonzero 15th entry
on the DBCN card in the initial problem. The magnitude criteria for R
(and the VOV, if available) should be met before forming a confidence
interval. If the shifted confidence interval center is available, it
should be used to form asymmetric confidence intervals about the
estimated mean.

History dependent information about R (and the VOV, if available) for
non-TFC bins can be obtained by printing out the tallies periodically
during a calculation using the first entry on the PRDMP card. The N
-dependent behavior of R can then be assessed. The complete statistical
information available can be obtained by creating a new tally and
selecting the desired TFC bin with the TF n card.

## 2.6.9.2 Information Available for Forming Statistically Valid Confidence Intervals for TFC Bins

Additional information about the statistical behavior of each TFC bin
result is available. A TFC bin table is produced by the MCNP code after
each tally to provide the user with detailed information about the
apparent quality of the TFC bin result. The contents of the table are
discussed in the following subsections, along with recommendations for
forming valid confidence intervals using this information.

## 2.6.9.2.1 TFC Bin Tally Information

The first part of the TFC bin table contains information about the TFC
bin result including the mean, R , scoring efficiency, the zero and
nonzero history score components of R [§2.6.6], and the shifted
confidence interval center. The two components of R can be used to
improve the problem efficiency by either improving the history scoring
efficiency or reducing the range of nonzero history scores.

## 2.6.9.2.2 The Largest TFC Bin History Score Occurs on the Next History

There are occasions when the user needs to make a conservative estimate
of a tally result. Conservative is defined so that the results will not
be less than the expected result. One reasonable way to make such an
estimate is to assume that the largest observed history score would
occur again on the very next history, N +1 .

The MCNP code calculates new estimated values for the mean, R , VOV, FOM
, and shifted confidence interval center for the TFC bin result for this
assumption. The results of this proposed occurrence are summarized in
the TFC bin information table. The user can assess the impact of this
hypothetical happening and act accordingly.

(2.247)

Table 2.9: Summary of MCNP Tally 10 Statistical Checks

| Value   |   Test # | Description                                                                                                                                                                                                                                        |
|---------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Mean    |        1 | a non-monotonic behavior (no up or down trend) in the estimated mean as a function of the number histories N for the last half of the problem                                                                                                      |
| R       |        2 | an acceptable magnitude of the estimated R of the estimated mean ( < 0 . 05 for a point detector tally or < 0 . 10 for a non-point detector tally)                                                                                                 |
|         |        3 | a monotonically decreasing R as a function of the number histories N for the last half of the problem                                                                                                                                              |
|         |        4 | a 1 /N decrease in the R as a function of N for the last half of the problem                                                                                                                                                                       |
| VOV     |        5 | the magnitude of the estimated VOV should be less than 0.10 for all types of tallies                                                                                                                                                               |
|         |        6 | a monotonically decreasing VOV as a function of N for the last half of the problem                                                                                                                                                                 |
|         |        7 | a 1 /N decrease in the VOV as a function of N for the last half of the problem                                                                                                                                                                     |
| FOM     |        8 | a statistically constant value of the FOM as a function of N for the last half of the problem                                                                                                                                                      |
|         |        9 | a non-monotonic behavior in the FOM as a function of N for the last half of the problem                                                                                                                                                            |
| f ( x ) |       10 | the SLOPE [Eq. (2.239)] of the 25 to 201 largest positive (negative with a negative DBCN(16) entry) history scores x should be greater than 3.0 so that the second moment GLYPH<1> xf ( x )d x will exist if the SLOPE is extrapolated to infinity |

## 2.6.9.2.3 Description of the 10 Statistical Checks for the TFC Bin

The MCNP code prints the results of ten statistical checks of the tally
in the TFC bin at each print. In a 'Status of Statistical Checks' table,
the results of these ten checks are summarized at the end of the output
for all TFC bin tallies. The quantities involved in these checks are the
estimated mean, R , VOV, FOM , and the large history score behavior of f
( x ) . Passing all of the checks should provide additional assurance
that any confidence intervals formed for a TFC bin result will cover the
expected result the correct fraction of the time. At a minimum, the
results of these checks provide the user with more information about the
statistical behavior of the result in the TFC bin of each tally.

The 10 statistical checks are made on the TFCs printed at the end of the
output for desirable statistical properties of Monte Carlo solutions as
shown in Table 2.9.

The seven N -dependent checks for the TFC bin are for the last half of
the problem. The last half of the problem should be well behaved in the
sense of the CLT to form the most valid confidence intervals.
'Monotonically decreasing' in checks 3 and 5 allows for some increases
in both R and the VOV. Such increases in adjacent TFC entries are
acceptable and usually do not, by themselves, cause poor confidence
intervals. A TFC bin R that does not pass check 3, by definition in the
MCNP code, does not pass check 4. Similarly, a TFC bin VOV that does not
pass check 6, by definition, does not pass check 7.

A table is printed after each tally for the TFC bin result that
summarizes the results and the pass or no-pass status of the checks.
Both asymmetric and symmetric confidence intervals are printed for the
one, two, and three σ levels when all of the statistical checks are
passed. These intervals can be expected to be correct with improved
probability over historical rules of thumb. This is NOT A GUARANTEE,
however; there is always a possibility that some as-yet-unsampled
portion of the problem would change the confidence interval if more

histories were calculated. A WARNING is printed if one or more of these
ten statistical checks is not passed, and one page of printed plot
information about f ( x ) is produced for the user to examine.

An additional information-only check is made on the largest five f ( x )
score grid bins to determine if there are bins that have no samples or
if there is a spike in an f ( x ) that does not appear to have an upper
limit. The result of the check is included in the TFC summary table for
the user to consider. This check is not a pass or no-pass test because a
hole in the tail may be appropriate for a discrete f ( x ) or an
exceptional sample occurred with so little impact that none of the ten
checks was affected. The empirical f ( x ) should be examined to assess
the likelihood of 'complete' sampling.

## 2.6.9.2.4 Forming Valid TFC Bin Confidence Intervals

For TFC bin results, the highest probability of creating a valid
confidence interval occurs when all of the statistical checks are
passed. Not passing several of the checks is an indication that the
confidence interval is less likely to be correct. A monotonic trend in
the mean for the last half of the problem is a strong indicator that the
confidence interval is likely to produce incorrect coverage rates. The
magnitudes of R and the VOV should be less than the recommended values
to increase the likelihood of a valid confidence interval. Small jumps
in the R , VOV, and/or the FOM as a function of N are not threatening to
the quality of a result. The slope of f ( x ) is an especially strong
indicator that N has not approached infinity in the sense of the CLT. If
the slope appears too shallow ( &lt; 3 ), check the printed plot of f ( x )
to see that the estimated Pareto fit is adequate. The use of the shifted
confidence interval is recommended, although it will be a small effect
for a well-converged problem.

The last half of the problem is determined from the TFC. The more
information available about the last half of the problem, the better the
N -dependent checks will be. Therefore, a problem that has run 40,000
histories will have 20 TFC N entries, which is more N entries than a
50,000 history problem with 13 entries. It is possible that a problem
that passes all tests at 40,000 may not pass all the tests at 40,001. As
is always the case, the user is responsible for deciding when a
confidence interval is valid. These statistical diagnostics are designed
to aid in making this decision.

## 2.6.10 A Statistically Pathological Output Example

A statistically pathological test problem [147] is discussed in this
section. The problem calculates the surface-leakage flux for neutrons
above 12 MeV from an isotropic steady-state 14-MeV neutron point source
of one particle/second at the center of a 30-cm-thick concrete shell
with an outer radius of 390 cm. The input is shown in Listing 10.48 in
§10.6.1. Point and ring detectors are deliberately used to estimate the
surface neutron leakage flux with highly inefficient, long-tailed, f ( x
) s. The largest point detector history scores are those that have many
collisions near the detector, which rarely occurs. A more-efficient
volumetric track-length leakage-flux tally in a thin shell at the outer
surface of the concrete sphere is also used to compare with the detector
results. The variance-reduction methods used are implicit capture with
weight cutoff, low-score point detector Russian roulette, and a
0.5-mean-free-path (approximately 8 cm for 12-14 MeV neutrons)
neighborhood around the detectors to ensure finite tally higher moments.

Figure 2.22 shows MCNP plots of the estimated mean, R , VOV, and slope
of the empirical history score PDF as a function of N for 10 4 (left
column) and 10 8 (right column) histories. The track-length results are
shown as a solid black line, ring-detector results as a dashed blue
line, and the point-detector results as a dotted red line.

The left column shows the results as a function of N for 10 4 histories.
The track-length flux tally appears well converged at 10 4 histories
with a mean of 6 . 40 × 10 -8 neutrons/cm 2 /sec ( R = 0 . 029 , VOV = 0
. 007 , and slope greater than 3). The point-detector result at 6,000
histories is 1 . 48 × 10 -8 ( R = 0 . 023 ), which is

a factor of 4 below the correct result. With no other information, this
result could be accepted by even a careful Monte Carlo practitioner.
However, the VOV never gets close to the recommended 0.1 value and the
slope of f ( x ) is 1.5. This slope could not continue indefinitely
because the mean of f ( x ) would not exist. Therefore, a confidence
interval should not be formed for this tally. The ring detector is much
better at sampling collisions close to the detector. Consequently, the
ring detector tally results do not exhibit the point-detector small-mean
behavior and are not yet converged ( R = 0 . 26 , VOV = 0 . 56 , and
SLOPE = 1 . 7 ).

The right column shows the results as a function of N for 10 8
histories. The R s for this case should be 100 times smaller than the 10
4 -history calculation for converged results. The 10 8 -history track-
length flux is 6 . 16 × 10 -8 ( R = 0 . 0003 , VOV = 0 . 0007 , and
slope greater than 3), the ring-detector result of 6 . 27 × 10 -8 ( R =
0 . 0033 , VOV = 0 . 0005 , and SLOPE greater than 3), and the point-
detector result is 6 . 15 × 10 -8 ( R = 0 . 050 , VOV = 0 . 085 , and
slope is 2.3). Both the track-length and ring-detector tallies appear
well converged, but the point-detector tally needs more sampling to more
completely sample f ( x ) and increase the slope. The ring-detector
result differs from the track-length result slightly because of the
uniform collision approximation in the neighborhood around to the
detector.

The empirical f ( x ) s for the three tallies at 10 4 and 10 8 histories
are shown in Figs. 2.23a and 2.23b. All 3 tally f ( x ) s have larger
sampled history scores, but large scores are most prevalent for the
point-detector tally. When one compares the empirical point detector f (
x ) s for 10 4 and 10 8 histories, the 10 4 history f ( x ) has
unsampled regions in the tail, which indicates incomplete f ( x )
sampling [155]. For the point-detector tally, seven decades of x have
been sampled with 10 8 histories compared to only three decades for 10 4
histories. The point-detector f ( x ) slope is increasing, but it still
does not yet appear to be completely sampled. The most compact (and most
efficient) f ( x ) is the track-length tally, followed by the ring-
detector tally, and then the point-detector tallies. The track-length
tally is 100 times more efficient than the ring-detector tally, which is
4,000 times more efficient than the point-detector tally, as measured
using the FOM.

For difficult-to-sample problems such as this example, it is possible
that an even larger history score could occur that would cause the VOV
and possibly the slope to have unacceptable values. The mean and R will
be much less affected than the VOV. The additional calculation time
required to improve problem sampling and to reach acceptable values for
the VOV and the slope could be prohibitive.

## /warning\_sign Caution

The large history score should NEVER be discarded from the tally result.
It is important that the reason for the large history score be
completely understood.

If the large history score is created by a poorly sampled region of
phase space, the problem should be modified to provide improved phase-
space sampling. If a conservative (large) answer is required, the
printed result that assumes the largest history score occurs on the very
next history can be used; however, there still may be yet unsampled but
important regions of phase space that should be explored further.

## 2.6.11 Batch Statistics

A small number of features in the MCNP code use batch statistics rather
than history statistics for performance reasons. With batch statistics,
the mean value of a number of histories is used as the score for
computing the statistical moments. So long as this number of histories
is constant, the total mean is the same as history statistics.
Additionally, the standard error describes the same value, albeit with
fewer degrees of freedom.

The reduction in degrees of freedom has a few effects. First, the
standard error, as computed as the square root of the unbiased variance,
is itself a biased estimator [159]. Using a small number of batches can
result in a significant bias. However, as one goes beyond 100 batches
this effect quickly becomes negligible. For a normal distribution, five
samples results in an expected bias of 7.9%, and 100 samples results in
an expected

mean leakage fluxes as a function of the number of histories mean
leakage fluxes as a function of the number of histories

<!-- image -->

mcnp6

6

probid:

03/03/20 06:46:05

tally

n

nps

100000000

runtpe = inpdetfofx100mr.h5

dump    2

f   Cell d   Flag/Dir

u   User s   Segment

m   Mult c   Angle

e   Energy

1

1

1

1

1

1

1

t   Time

1

track length ring det

point det mcnp6

6

probid:

03/03/20 06:46:05

tally

n

nps

100000000

runtpe = inpdetfofx100mr.h5

dump    2

f   Cell d   Flag/Dir

u   User s   Segment

m   Mult c   Angle

e   Energy

1

1

1

1

1

1

1

t   Time

1

track length ring detector

point detector mcnp6

6

probid:

03/03/20 06:46:05

tally

n

nps

100000000

runtpe = inpdetfofx100mr.h5

dump    2

f   Cell d   Flag/Dir

u   User s   Segment

m   Mult c   Angle

e   Energy

1

1

1

1

1

1

1

t   Time

1

track length ring detector

point detector mcnp6

6

probid:

03/03/20 06:46:05

tally

n

nps

100000000

runtpe = inpdetfofx100mr.h5

dump    2

f   Cell d   Flag/Dir

u   User s   Segment

m   Mult c   Angle

e   Energy

1

1

1

1

1

1

1

t   Time

1

track length ring detector

point detector

Figure 2.22: Mean, relative error, variance of the variance, and tally
slope for 10,000 histories (left) and 100 million histories (right). The
track length tally is the solid black line, ring detector is the dashed
blue line and the point detector is the dotted red line.

4

4

4

4

empirical f(x)'s for concrete shell leakage flux tallies for 10k histories

<!-- image -->

empirical f(x)'s for concrete shell leakage flux tallies for 100m
histories

Figure 2.23: The empirical f ( x ) s for 3 tallies with 10 4 and 10 8 histories.

<!-- image -->
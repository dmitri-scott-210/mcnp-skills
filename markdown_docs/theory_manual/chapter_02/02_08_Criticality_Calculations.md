---
title: "Chapter 2.8 - Criticality Calculations"
chapter: "2.8"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/2_Geometry,_Data,_Physics,_and_Mathematics/2.8_Criticality_Calculations.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

the tracking to diverge. The sequencing of random numbers is done by
incrementing the random number generator, controlled with the MCNP RAND
card, at the beginning of each history by a stride S of random numbers
from the beginning of the previous history. The stride should be a
quantity greater than would be needed by most histories [§2.11].

The MCNP code does not provide an estimate of the error in the
difference. Reference [160] shows how the error in the difference
between two correlated runs can be estimated. A post-processor code
would have to be written to do this.

Correlated sampling should not be confused with more elaborate Monte
Carlo perturbation schemes that calculate differences and their
variances directly. The MCNP code also has a sophisticated perturbation
capability.

## 2.8 Criticality Calculations

Nuclear criticality, the ability to sustain a chain reaction by fission
neutrons, is characterized by k eff , the eigenvalue to the time-
independent neutron transport equation. In reactor theory, k eff is
thought of as the ratio between the number of neutrons in successive
generations, with the fission process regarded as the birth event that
separates generations of neutrons [78]. For critical systems, k eff = 1
and the chain reaction will just sustain itself. For subcritical
systems, k eff &lt; 1 and the chain reaction will not sustain itself. For
supercritical systems, k eff &gt; 1 and the number of fissions in the chain
reaction will increase with time. In addition to the geometry
description and material cards, all that is required to run a
criticality problem is a KCODE card, described below, and an initial
spatial distribution of fission points using either the KSRC card, the
SDEF card, or a SRCTP file.

Calculating k eff consists of estimating the mean number of fission
neutrons produced in one generation per fission neutron started. A
generation is the life of a neutron from birth in fission to death by
escape, parasitic capture, or absorption leading to fission. In the MCNP
code, the computational equivalent of a fission generation is a k eff
cycle; that is, a cycle is a computed estimate of an actual fission
generation. Processes such as (n,2n) and (n,3n) are considered internal
to a cycle and do not act as termination. Because fission neutrons are
terminated in each cycle to provide the fission source for the next
cycle, a single history can be viewed as continuing from cycle to cycle.
The effect of the delayed neutrons is included by using the total ν when
the data are available. In a MODE N P problem, secondary photon
production from neutrons is turned off during inactive cycles. The MCNP
code uses three different estimators for k eff . We recommend using, for
the final k eff result, the statistical combination of all three [165].

It is extremely important to emphasize that the result from a
criticality calculation is a confidence interval for k eff that is
formed using the final estimated k eff and the estimated standard
deviation. A properly formed confidence interval from a valid
calculation should include the true answer the fraction of time used to
define the confidence interval. For example, 68% of confidence intervals
formed at the 68% confidence level, which corresponds to roughly one
standard deviations of the mean for a normal distribution, will contain
the true answer. There will always be some probability that the true
answer lies outside of a confidence interval.

Reference [166] is an introduction to using the MCNP code for
criticality calculations, focusing on the unique aspects of setting up
and running a criticality problem and interpreting the results. A quick-
start chapter gets the new MCNP user on the computer running a simple
criticality problem as quickly as possible.

## 2.8.1 Criticality Program Flow

Because the calculation of k eff entails running successive fission
cycles, criticality calculations have a different program flow than MCNP
fixed source problems. They require a special criticality source that is
incompatible with the surface source and user-supplied sources. Unlike
fixed source problems, where the source being sampled throughout the
problem never changes, the criticality source changes from cycle to
cycle.

## 2.8.1.1 Criticality Problem Definition

To set up a criticality calculation, the user initially supplies an MCNP
input file that includes the KCODE card with the following information:

1. the nominal number of source histories, N , per k eff cycle;
2. an initial guess of k eff ;
3. the number of source cycles, I c , to skip before k eff accumulation; and
4. the total number of cycles, I t , in the problem.

Other KCODE entries are discussed in §5.8.10. The initial spatial
distribution of fission neutrons can be entered by using (1) the KSRC
card with sets of x, y, z point locations, (2) the SDEF card to define
points uniformly in volume, or (3) a file (SRCTP) from a previous MCNP
criticality calculation. If the SDEF card is used, the default WGT value
should not be changed. Any KSRC points in geometric cells that are void
or have zero importance are rejected. The remaining KSRC points are
duplicated or rejected enough times so the total number of points M in
the source spatial distribution is approximately the nominal source size
N . The energy of each source particle for the first k eff cycle is
selected from a generic Watt thermal fission distribution if it is not
available from the SRCTP file.

## 2.8.1.2 Particle Transport for Each k eff Cycle

In each k eff cycle, M (varying with cycle) source particles are started
isotropically. For the first cycle, these M points come from one of
three user-selected source possibilities. For subsequent cycles, these
points are the ones written at collision sites from neutron transport in
the previous cycle. The total source weight of each cycle is a constant
N . That is, the weight of each source particle is N/M , so all
normalizations occur as if N rather than M particles started in each
cycle.

Source particles are transported through the geometry by the standard
random walk process, except that fission is treated as capture, either
analog or implicit, as defined on the PHYS :N or CUT :N card. At each
collision point the following four steps are performed for the cycle:

1. the three prompt neutron lifetime estimates are accumulated;
2. if fission is possible, the three k eff estimates are accumulated; and
3. if fission is possible, n ≥ 0 fission sites (including the sampled outgoing energy of the fission neutron) at each collision are stored for use as source points in the next cycle,

where

<!-- formula-not-decoded -->

W is the particle weight (before implicit capture weight reduction or
analog capture);

- ν is the average number of neutrons produced per fission at the incident energy of this collision, with either prompt ν or total ν (default) used;
- σ f is the microscopic material fission cross section;
- σ t is the microscopic material total cross section; and

k eff is the estimated collision k eff from previous cycle. For the
first cycle, the second KCODE card entry is used.

M = ∑ n is the number of fission source points to be used in the next
cycle, unless a tally with batch statistics is enabled. In that case,
the fission bank is resampled to be exactly nsrck at the end of each
cycle. The number of fission sites n stored at each collision is rounded
up or down to an integer (including zero) with a probability
proportional to its closeness to that integer. If the initial guess of k
eff is too low or too high, the number of fission sites written as
source points for the next cycle will be, respectively, too high or too
low relative to the desired nominal number N . A bad initial guess of k
eff causes only this consequence.

A very poor initial guess for the spatial distribution of fissions can
cause the first cycle estimate of k eff to be extremely low. This
situation can occur when only a fraction of the fission source points
enter a cell with a fissionable material. As a result, one of two error
messages can be printed: (1) no new source points were generated, or (2)
the new source has overrun the old source. The second message occurs
when the MCNP code's storage for the fission source points is exceeded
because the small k eff that results from a poor initial source causes n
to become very large.

The fission energy of the next-cycle neutron is sampled separately for
each source point and stored for the next cycle. It is sampled from the
same distributions as fissions would be sampled in the random walk based
on the incident neutron energy and fissionable isotope. The geometric
coordinates and cell of the fission site are also stored.

4. The collision nuclide and reaction are sampled (after steps 1, 2, and 3) but the fission reaction is not allowed to occur because fission is treated as capture. The fission neutrons that would have been created are accrued by three different methods to estimate k eff for this cycle. The three estimators are a collision estimator, an absorption estimator and a track-length estimator as discussed in §2.8.2.

## 2.8.1.3 k eff Cycle Termination

At the end of each k eff cycle, a new set of M source particles has been
written from fissions in that cycle. The number M varies from cycle to
cycle but the total starting weight in each cycle is a constant N .
These M particles are written to the SRCTP file at certain cycle
intervals. The SRCTP file can be used as the initial source in a
subsequent criticality calculation with a similar, though not identical,
geometry. Also, k eff quantities are accumulated, as is described below.

## 2.8.1.4 Convergence

The first I c cycles in a criticality calculation are inactive cycles,
where the spatial source changes from the initial definition to the
correct distribution for the problem. No k eff accumulation, summary
table, activity table, or tally information is accrued for inactive
cycles. Photon production, perturbations, and DXTRAN are turned off
during inactive cycles. I c is the third entry on the KCODE card for the
number of k eff cycles to be skipped before k eff and tally
accumulation. After the first I c cycles, the fission source spatial
distribution is assumed to have achieved equilibrium, active cycles
begin, and k eff and tallies are accumulated. Cycles are run until
either a time limit is reached or the total cycles on the KCODE card
have been completed.

Criticality calculations with the MCNP code are based on an iterative
procedure called 'power iteration' [167, 168]. After assuming an initial
guess for the fission source spatial distribution (i.e., first
generation), histories are followed to produce a source for the next
fission neutron generation and to estimate a new value for k eff . The
new fission source distribution is then used to follow histories for the
second generation, producing yet another fission source distribution and
estimate of k eff . These generations (also called cycles or batches)
are repeated until the source spatial distribution has converged. Once
the fission source distribution has converged to its stationary state,
tallies for reaction rates and k eff may be accumulated by running
additional cycles until the statistical uncertainties have become
sufficiently small.

Analysis of the power iteration procedure for solving k eff eigenvalue
calculations [167] shows that the convergence of the fission source
distribution, S , and the estimated eigenvalue, k eff , can be modeled
as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where S 0 and k 0 are the fundamental eigenfunction and eigenvalue of
the exact transport solution, S 1 and k 1 are the eigenfunction and
eigenvalue of the first higher mode, a and b are constants, and n is the
number of cycles performed in the power iteration procedure. Note that k
0 is the expected value of k eff , and that k 0 &gt; k 1 &gt; 0 , so that k 1
/k 0 &lt; 1 . The quantity k 1 /k 0 is called the dominance ratio (DR), and
is the key physical parameter that determines the convergence rate of
the power iteration procedure. The DR is a function of problem geometry
and materials. As the number of cycles n becomes large, the error terms
due to higher modes die off as DR n , and the source distribution and k
eff approach their stationary, equilibrium values. For typical light-
water reactor systems, the DR is often in the range 0.8-0.99, and 50-100
inactive cycles may be required for errors in the initial guess to die
away sufficiently that the source and k eff converge. For some critical
systems (e.g., heavy-water reactors, fuel storage vaults), however, the
DR may be very close to 1 (e.g., 0.99 or higher), and hundreds or
thousands of inactive cycles may be required to attain source
convergence.

It should also be noted that the source distribution S and the
eigenvalue k eff do not converge in the same manner. The expression for
k ( n +1) eff has the additional factor 1 -( k 1 /k 0 ) on the higher-
mode error. For problems where the DR is very close to 1, the source
distribution may take hundreds or thousands of cycles to converge
(because of errors dying out as DR n ), while k eff may converge rapidly
(because its higher-mode error is damped by the additional factor 1 -DR,
which may be very small). That is, k eff will converge more rapidly than
the source distribution. Thus, it is very important to examine the
behavior of both k eff and the source distribution when assessing
problem convergence. Both k eff and the fission source distribution must
converge before starting active cycles for tallies. It is up to the user
to specify the number of inactive cycles I c to run in order to attain
convergence. Most users will make a trial calculation (using a small
number of histories per cycle, such as 1000) to examine the convergence
behavior of k eff and the source distribution, to determine a proper
value for I c , and then make a final calculation using a larger number
of histories per cycle (e.g., 5000 or more) and sufficient active cycles
to attain small uncertainties. To assist users in assessing convergence
of criticality calculations, the MCNP code provides several statistical
checks on k eff , as discussed in the next sections. In addition, the
MCNP code calculates a quantity called the entropy of the source
distribution, H src [169, 170] to assist users in assessing the
convergence of the source distribution.

## 2.8.2 Estimation of k eff Confidence Intervals and Prompt Neutron Lifetimes

The criticality eigenvalue k eff and various prompt neutron lifetimes,
along with their standard deviations, are automatically estimated in
every criticality calculation in addition to any user-requested tallies.
k eff and the lifetimes are estimated for every active cycle, as well as
averaged over all active cycles. k eff and the lifetimes are estimated
in three different ways. These estimates are combined [165] using
observed statistical correlations to provide the optimum final estimate
of k eff and its standard deviation.

It is known [171] that the power iteration method with a fixed source
size produces a very small negative bias ∆ k eff in k eff that is
proportional to 1 /N . This bias is negligible [171] for all practical
problems where N is greater than about 200 neutrons per cycle and as
long as too many active cycles are not used. It has been shown [171]
that this bias is less, probably much less, than one-half of one
standard deviation for 400 active cycles when the ratio of the true k
eff standard deviation to k eff is 0.0025 at the problem end.

In the MCNP code, the definition of k eff is:

<!-- formula-not-decoded -->

where the phase-space variables are t , E , and Ω for time, energy,
direction, and implicitly r for position with incremental volume d V
around r . The denominator is the loss rate, which is the sum of
leakage, capture (n,0n), fission, and multiplicity (n,xn) terms. By
particle balance, the loss rate is also the source rate, which is unity
in a criticality calculation. If the number of fission neutrons produced
in one generation is equal to the number in the previous generation,
then the system is critical. If it is greater, the system is
supercritical. If it is less, then the system is subcritical. The
multiplicity term is:

<!-- formula-not-decoded -->

The above definition of k eff comes directly from the time-integrated
Boltzmann transport equation (without external sources),

<!-- formula-not-decoded -->

which may be rewritten to look more like the definition of k eff as

<!-- formula-not-decoded -->

The loss rate is on the left and the production rate is on the right.

The neutron prompt removal lifetime is the average time from the
emission of a prompt neutron in fission to the removal of the neutron by
some physical process such as escape, capture, or fission. Also, even
with the TOTNU card to produce delayed neutrons as well as prompt
neutrons ( KCODE default), the neutrons are all born at time zero, so
the removal lifetimes calculated in the MCNP code are prompt removal
lifetimes, even if there are delayed neutrons.

The definition of the prompt removal lifetime [172] is

<!-- formula-not-decoded -->

where η is the population per unit volume per unit energy per unit solid
angle. In a multiplying system in which the population is increasing or
decreasing on an asymptotic period, the population changes in accordance
with where τ + r is the adjoint-weighted removal lifetime. The MCNP code
calculates the non-adjoint-weighted prompt removal lifetime τ r that can
be significantly different in a multiplying system. In a non-multiplying
system, k eff = 0 and τ r → τ + r , the population decays as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where the non-adjoint-weighted removal lifetime τ r is also the
relaxation time.

Noting that the flux is defined as

<!-- formula-not-decoded -->

where v is the speed, the non-adjoint-weighted prompt removal lifetime
in the MCNP code, τ r , is defined as

<!-- formula-not-decoded -->

The prompt removal lifetime is a fundamental quantity in the nuclear
engineering point kinetics equation. It is also useful in nuclear well-
logging calculations and other pulsed source problems because it gives
the population time-decay constant.

## 2.8.2.1 Collision Estimators

The collision estimate for k eff for any active cycle is where

<!-- formula-not-decoded -->

| i     | is summed over all collisions in a cycle where fission is possible;                                                     |
|-------|-------------------------------------------------------------------------------------------------------------------------|
| j     | is summed over all nuclides of the material involved in the i th collision;                                             |
| σ t j | is the total microscopic cross section;                                                                                 |
| σ f j | is the microscopic fission cross section;                                                                               |
| ν j   | is the average number of prompt or total neutrons produced per fission by the collision nuclide at the incident energy; |
| f j   | is the atomic fraction for nuclide j ;                                                                                  |
| N     | is the nominal source size for cycle; and                                                                               |
| W i   | is the weight of particle entering collision.                                                                           |

Because W i represents the number of neutrons entering the i th
collision,

<!-- formula-not-decoded -->

is the expected number of neutrons to be produced from all fission
processes in the collision. Thus k C eff is the mean number of fission
neutrons produced per cycle. The collision estimator tends to be best,
sometimes only marginally so, in very large systems.

The collision estimate of the prompt removal lifetime for any active
cycle is the average time required for a fission source neutron to be
removed from the system by either escape, capture (n,0n), or fission.

<!-- formula-not-decoded -->

where T e and T x are the times from the birth of the neutron until
escape or collision. W e is the weight lost at each escape. W c + W f is
the weight lost to (n,0n) and fission at each collision,

<!-- formula-not-decoded -->

where σ c j is the microscopic capture (n,0n) cross section, and W i is
the weight entering the collision.

## 2.8.2.2 Absorption Estimators

The absorption estimator for k eff for any active cycle is made when a
neutron interacts with a fissionable nuclide. The estimator differs for
analog and implicit absorption. For analog absorption,

<!-- formula-not-decoded -->

where i is summed over each analog absorption event in the j th nuclide.
Note that in analog absorption, the weight is the same both before and
after the collision. Because analog absorption includes fission in
criticality calculations, the frequency of analog absorption at each
collision with nuclide j is ( σ c j + σ f j ) /σ t j . The analog
absorption k eff estimate is very similar to the collision estimator of
k eff except that only the j th absorbing nuclide, as sampled in the
collision, is used rather than averaging over all nuclides.

For implicit absorption, the following is accumulated:

<!-- formula-not-decoded -->

where i is summed over all collisions in which fission is possible and

<!-- formula-not-decoded -->

is the weight absorbed in the implicit absorption. The difference
between the implicit absorption estimator k A eff and the collision
estimator k C eff is that only the nuclide involved in the collision is
used for the absorption k eff estimate rather than an average of all
nuclides in the material for the collision k eff estimator.

The absorption estimator with analog absorption is likely to produce the
smallest statistical uncertainty of the three estimators for systems
where the ratio ν j σ f j / ( σ c j + σ f j ) is nearly constant. Such
would be the case for a thermal system with a dominant fissile nuclide
such that the 1/velocity cross-section variation would tend to cancel.

The absorption estimate differs from the collision estimate in that the
collision estimate is based upon the expected value at each collision,
whereas the absorption estimate is based upon the events actually
sampled at a collision. Thus all collisions will contribute to the
collision estimate of k C eff and τ C r by the probability of fission
(or capture for τ C r ) in the material. Contributions to the absorption
estimator will only occur if an actual fission (or capture for τ A r )
event occurs for the sampled nuclide in the case of analog absorption.
For implicit absorption, the contribution to the absorption estimate
will only be made for the nuclide sampled.

The absorption estimate of the prompt removal lifetime for any active
cycle is again the average time required for a fission source neutron to
be removed from the system by either escape, capture (n,0n), or fission.

For implicit absorption, where

For analog absorption, where T e , T c , T f , and T x are the times
from the birth of the neutron until escape, capture (n,0n), fission, or
collision. W e is the weight lost at each escape. W c and W f are the
weights lost to capture (n,0n) and fission at each capture (n,0n) or
fission event with the nuclide sampled for the collision.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## 2.8.2.3 Track-length Estimators

The track length estimator of k eff is accumulated every time the
neutron traverses a distance d in a fissionable material cell:

where

<!-- formula-not-decoded -->

| i   | is summed over all neutron trajectories;            |
|-----|-----------------------------------------------------|
| ρ   | is the atomic density in the cell; and              |
| d   | is the trajectory track length from the last event. |

Because ρd ∑ j f j ν j σ f j is the expected number of fission neutrons
produced along trajectory d , k TL eff is a third estimate of the mean
number of fission neutrons produced in a cycle per nominal fission
source neutron.

The track length estimator tends to display the lowest variance for
optically thin fuel cells (for example, plates) and fast systems where
large cross-section variations because of resonances may cause high
variances in the other two estimators.

The track length estimator for the prompt removal lifetime for each
cycle is accumulated every time the neutron traverses a distance d in
any material in any cell:

<!-- formula-not-decoded -->

where W s is the source weight summed over all histories in the cycle
and v is the velocity. Note that d/v is the time span of the track. Note
further that:

<!-- formula-not-decoded -->

and in criticality problems:

<!-- formula-not-decoded -->

These relationships show how τ TL r is related to the definition of τ r
in Eq. (2.278).

## 2.8.2.4 Other Lifetime Estimators

In addition to the collision, absorption, and track length estimators of
the prompt removal lifetime τ r , The MCNP code provides the escape,
capture (n,0n), and fission prompt lifespans and lifetimes for all KCODE
problems having a sufficient number of settle cycles. Further, the
'average time of' printed in the problem summary table is related to the
lifespans, and track-length estimates of many lifetimes can be computed
using the 1 /v tally multiplier option on the FM card for track-length
tallies.

In KCODE problems, the MCNP code calculates the lifespan of escape l e ,
capture (n,0n) l c , fission l f , and removal l r as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

These sums are taken over all the active histories in the calculation.
If KC8 = 0 on the KCODE card, then the sums are over both active and
inactive cycle histories, but KC8 = 1 , the default, is assumed for the
remainder of this discussion. The capture (n,0n) and fission
contributions are accumulated at each collision with a nuclide, so these
are absorption estimates. Thus,

<!-- formula-not-decoded -->

The difference is that τ A r is the average of the τ A r for each cycle
and l r is the average over all histories. l r = τ A r if there is
precisely one active cycle, but then neither τ A r nor l r is printed
out because there are too few cycles. The cycle average τ A r does not
precisely equal the history-average l r because they are ratios.

l e and l c are the 'average time to' escape and capture (n,0n) that is
printed in the problem summary table for all neutron and photon
problems.

(1 /N ) ∑ W e , (1 /N ) ∑ W c , and (1 /N ) ∑ W f are the weight lost to
escape, capture (n,0n), and fission in the problem summary table.

The 'fractions' F x printed out below the lifespan in the KCODE summary
table are, for x = e , c , f , r ,

<!-- formula-not-decoded -->

The prompt lifetimes [172] for the various reactions τ x are then

<!-- formula-not-decoded -->

Both τ A r and the covariance-weighted combined estimator τ (C / A / T)
r are used. Note again that the slight differences between similar
quantities are because l x and F x are averaged over all active
histories whereas τ A r and τ (C / A / T) r are averaged within each
active cycle, and then the final values are the averages of the cycle
values, i.e., history averages vs. batch averages.

The prompt removal lifetime can also be calculated using the F4 track-
length tally with the 1 /v multiplier option on the FM card and using
the volume divided by the average source weight W s as the
multiplicative constant. The standard track length tally is then
converted from

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

to

Remember to multiply by volume, either by setting the FM card constant
to the volume or overriding the F4 volume divide by using segment
divisors of unity on the SD card. W s should be unity for KCODE
calculations. The only difference between τ TL r and the modified F4
tally will be any variations from unity in W s and the error estimation,
which will be batch-averaged for τ TL r and history-averaged for the F4
tally.

Lifetimes for all other processes also can be estimated by using the FM
multiplier to calculate reaction rates as well (the numerator and
denominator are separate tallies that must be divided by the user-see
the examples in Chapter 10):

<!-- formula-not-decoded -->

Note that the lifetimes are inversely additive as

<!-- formula-not-decoded -->

## 2.8.2.5 Combined k eff and τ r Estimators

The MCNP code provides a number of combined k eff and τ r estimators
that are combinations of the three individual k eff and τ r estimators
using two at a time or all three. The combined k eff and τ r values are
computed by using a maximum likelihood estimate, as outlined by Halperin
[173] and discussed further by Urbatsch [165]. This technique, which is
a generalization of the inverse variance weighting for uncorrelated
estimators, produces the maximum likelihood estimate for the combined
average k eff and τ r , which, for multivariate normality, is the
almost-minimum variance estimate. It is 'almost' because the covariance
matrix is not known exactly and must be estimated. The three-combined k
eff and τ r estimators are the best final estimates from an MCNP
calculation [165].

This method of combining estimators can exhibit one feature that is
disconcerting: sometimes (usually with highly positively correlated
estimators) the combined estimate will lie outside the interval defined
by the

two or three individual average estimates. Statisticians at Los Alamos
have shown [165] that this is the best estimate to use for a final k eff
and τ r value. Reference [165] shows the results of one study of 500
samples from three highly positively correlated normal distributions,
all with a mean of zero. In 319 samples, all three estimators fell on
the same side of the expected value. This type of behavior occurs with
high positive correlation because if one estimator is above or below the
expected value, the others have a good probability of being on the same
side of the expected value. The advantage of the three-combined
estimator is that the Halperin algorithm correctly predicts that the
true value will lie outside of the range.

## 2.8.2.6 Error Estimation and Estimator Combination

After the first I c inactive cycles, during which the fission source
spatial distribution is allowed to come into spatial equilibrium, the
MCNP code begins to accumulate the estimates of k eff and τ r with those
estimates from previous active (after the inactive) cycles. The relative
error R of each quantity is estimated in the usual way as where M is the
number of active cycles,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and x m is a quantity such as k eff from active cycle m . This assumes
that the cycle-to-cycle estimates of each k eff are uncorrelated. This
assumption generally is good for k eff , but not for the eigenfunction
(fluxes) of optically large systems [174].

The MCNP code also combines the three estimators in all possible ways
and determines the covariance and correlations. The simple average of
two estimators is defined as x ij = (1 / 2) ( x i + x j ) , where, for
example, x i may be the collision estimator k C eff and x j may be the
absorption estimator k A eff .

The 'combined average' of two estimators is weighted by the covariances
as

<!-- formula-not-decoded -->

where the covariance C ij is

<!-- formula-not-decoded -->

Note that C ii = x 2 -x 2 for estimator i .

The 'correlation' between two estimators is a function of their
covariances and is given by

<!-- formula-not-decoded -->

The correlation will be between positive one (perfect positive
correlation) and minus one (perfect anti or negative correlation). If
the correlation is one, no new information has been gained by the second
estimator. If the correlation is zero, the two estimators appear
statistically independent and the combined estimated

standard deviation should be significantly less than either. If the
correlation is negative one, even more information is available because
the second estimator will tend to be low, relative to the expected
value, when the first estimator is high and vice versa. Even larger
improvements in the combined standard deviation should occur.

The combined average estimator ( k eff or τ r ) and the estimated
standard deviation of all three estimators are based on the method of
Halperin [173] and is much more complicated than the two-combination
case. The improvements to the standard deviation of the three-combined
estimator will depend on the magnitude and sign of the correlations as
discussed above. The details and analysis of this method are given in
[165].

For many problems, all three estimators are positively correlated. The
correlation will depend on what variance reduction (for example,
implicit or analog capture) is used. Occasionally, the absorption
estimator may be only weakly correlated with either the collision or
track length estimator. It is possible for the absorption estimator to
be significantly anticorrelated with the other two estimators for some
fast reactor compositions and large thermal systems. Except in the most
heterogeneous systems, the collision and track length estimators are
likely to be strongly positively correlated.

There may be a negative bias [171] in the estimated standard deviation
of k eff for systems where the locations of fission sites in one
generation are correlated with the locations of fission sites in
successive generations. The statistical methods used in the MCNP code
for estimating standard deviations in k eff calculations do not account
for the effects of intergenerational correlation, leading to
underprediction of standard deviations. These systems are typically
large with small neutron leakage. The magnitude of this effect can be
estimated by batching the cycle k eff values in batch sizes much greater
than one cycle [171], which the MCNP code provides automatically. For
problems where there is a reason to suspect the results, a more accurate
calculation of this effect can be done by making several independent
calculations of the same problem (using different random number
sequences) and observing the variance of the collection of independent k
eff values. The larger the number of independent calculations that can
be made, the better the distribution of k eff values can be assessed.

## 2.8.2.7 Creating and Interpreting k eff Confidence Intervals

The result of a Monte Carlo criticality calculation (or any other type
of Monte Carlo calculation) is a confidence interval. For criticality,
this means that the result is not just k eff , but k eff plus and minus
some number of estimated standard deviations to form a confidence
interval (based on the Central Limit Theorem) in which the true answer
is expected to lie a certain fraction of the time. The number of
standard deviations used (for example, from a Student's t Table)
determines the fraction of the time that the confidence interval will
include the true answer, for a selected confidence level. For example, a
valid 99% confidence interval should include the true result 99% of the
time. There is always some probability (in this example, 1%) that the
true result will lie outside of the confidence interval. To reduce this
probability to an acceptable level, either the confidence interval must
be increased according to the desired Student's t percentile, or more
histories need to be run to get a smaller estimated standard deviation.

The MCNP code uses three different estimators for k eff . The advantages
of each estimator vary with the problem: no one estimator will be the
best for all problems. All estimators and their estimated standard
deviations are valid under the assumption that they are unbiased and
consistent, therefore representative of the true parameters of the
population. This statement has been validated empirically [165] for all
MCNP estimators for small dominance ratios. The batched k eff results
table should be used to estimate if the calculated batch-size-of-one k
eff standard deviation appears to be adequate.

The confidence interval based on the three-statistically-combined k eff
estimator is the recommended result to use for all final k eff
confidence interval quotations because all of the available information
has been used in the final result. This estimator often has a lower
estimated standard deviation than any of the three individual estimators
and therefore provides the smallest valid confidence

interval as well. The final estimated k eff value, estimated standard
deviation, and the estimated 68%, 95%, and 99% confidence intervals
(using the correct number of degrees of freedom) are presented in the
box on the k eff results summary page of the output. If other confidence
intervals are wanted, they can be formed from the estimated standard
deviation of k eff . At least 30 active cycles need to be run for the
final k eff results box to appear. Thirty cycles are required so that
there are enough degrees of freedom to form confidence intervals using
the well-known estimated standard deviation multipliers. When
constructing a confidence interval using any single k eff estimator, its
standard deviation, and a Student's t Table, there are I t -I c -1
degrees of freedom. For the two- and three-combined k eff estimators,
there are I t -I c -2 and I t -I c -3 degrees of freedom, respectively.

All of the k eff estimators and combinations by two or three are
provided in the MCNP code so that the user can make an alternate choice
of confidence interval if desired. Based on statistical studies, using
the individual k eff estimator with the smallest estimated standard
deviation is not recommended. Its use can lead to confidence intervals
that do not include the true result the correct fraction of the time
[165]. The studies have shown that the standard deviation of the three-
combined k eff estimator provides the correct coverage rates, assuming
that the estimated standard deviations in the individual k eff
estimators are accurate. This accuracy can be verified by checking the
batched k eff results table. When significant anti-correlations occur
among the estimators, the resultant much smaller estimated standard
deviation of the three-combined average has been verified [165] by
analyzing a number of independent criticality calculations.

## 2.8.2.8 Analysis to Assess the Validity of a Criticality Calculation

The two most important requirements for producing a valid criticality
calculation for a specified geometry are sampling all of the fissionable
material well and ensuring that the fundamental spatial mode was
achieved before and maintained during the active k eff cycles. The MCNP
code has checks to assess the fulfillment of both of these conditions.

The MCNP code verifies that at least one fission source point was
generated in each cell containing fissionable material. A WARNING
message is printed on the k eff results summary page that includes a
list of cells that did not have any particles entering, and/or no
collisions, and/or no fission source points. For repeated structure
geometries, a source point in any one cell that is repeated will satisfy
this test. For example, assume a problem with a cylinder and a cube that
are both filled with the same universe, namely a sphere of uranium and
the space outside the sphere. If a source point is placed in the sphere
inside the cylinder but not in the sphere inside the cube, the test will
be satisfied.

One basic assumption that is made for a good criticality calculation is
that the normal spatial mode for the fission source has been achieved
after I c cycles were skipped. The MCNP code attempts to assess this
condition in several ways. The estimated combined k eff and its
estimated standard deviation for the first and second active cycle
halves of the problem are compared. A WARNING message is issued if
either the difference of the two values of combined col/abs/track-length
k eff does not appear to be zero or the ratio of the larger-to-the-
smaller estimated standard deviations of the two col/abs/ track-length k
eff is larger than expected. Failure of either or both checks implies
that the two active halves of the problem do not appear to be the same
and the output from the calculation should be inspected carefully.

The MCNP code checks to determine which number of cycles skipped
produces the minimum estimated standard deviation for the combined k eff
estimator. If this number is larger than I c , it may indicate that not
enough inactive cycles were skipped. The table of combined k eff -by-
number-of-cycles skipped should be examined to determine if enough
inactive cycles were skipped.

It is assumed that N is large enough so that the collection of active
cycle k eff estimates for each estimator will be normally distributed if
the fundamental spatial mode has been achieved in I c cycles and
maintained for the rest of the calculation. To test this assumption, the
MCNP code performs normality checks [175, 176] on each of the three k
eff estimator cycle data at the 95% and 99% confidence levels. A WARNING
message is

issued if an individual k eff data set does not appear to be normally
distributed at the 99% confidence level. This condition will happen to
good data about 1% of the time. Unless there is a high positive
correlation among the three estimators, it is expected to be rare that
all three k eff estimators will not appear normally distributed at the
99% confidence level when the normal spatial mode has been achieved and
maintained. When the condition that all three sets of k eff estimators
do not appear to be normal at the 99% confidence level occurs, the box
with the final k eff will not be printed. The final confidence interval
results are available elsewhere in the output. Examine the calculation
carefully to see if the normal mode was achieved before the active
cycles began. The normality checks are also made for the batchedk eff
and k eff -by-cycles-skipped tables so that normality behavior can be
studied by batch size and I c .

These normality checks test the assumption that the individual cycle k
eff values behave in the assumed way. Even if the underlying individual
cycle k eff values are not normally distributed, the three average k eff
values and the combined k eff estimator will be normally distributed if
the conditions required by the Central Limit Theorem are met for the
average. If required, this assumption can be tested by making several
independent calculations to verify empirically that the collection of
the average k eff values appear to be normally distributed with the same
population variance as estimated by the MCNP code.

The MCNP code tests for a monotonic trend of the three-combined k eff
estimator over the last ten active cycles. This type of behavior is not
expected in a well-converged solution for k eff and could indicate a
problem with achieving or maintaining the normal spatial mode. A WARNING
message is printed if such a monotonic trend is observed.

To assist users in assessing the convergence of the fission source
spatial distribution, the MCNP code computes a quantity called the
Shannon entropy of the fission source distribution, H src [169, 170].
The Shannon entropy is a well-known concept from information theory and
provides a single number for each cycle to help characterize convergence
of the fission source distribution. It has been found that the Shannon
entropy converges to a single steady-state value as the source
distribution approaches stationarity. Line plots of Shannon entropy vs.
cycle are easier to interpret and assess than are 2-D or 3-D plots of
the source distribution vs. cycle.

To compute H src , it is necessary to superimpose a 3-D grid on a
problem encompassing all of the fissionable regions, and then to tally
the number of fission sites in a cycle that fall into each of the grid
boxes. These tallies may then be used to form a discretized estimate of
the source distribution, { P J , J = 1 , N s } , where N s is the number
of grid boxes in the superimposed mesh, and P J is (the number of source
sites in J th grid box)/(total number of source sites). Then, the
Shannon entropy of the discretized source distribution for that cycle is
given by

<!-- formula-not-decoded -->

H src varies between 0 for a point distribution to ln 2 ( N s ) for a
uniform distribution. Also note that as P J approaches 0, P J ln 2 ( P J
) approaches 0. The MCNP code prints H src for each cycle of a KCODE
calculation. Plots of H src vs. cycle can also be obtained during or
after a calculation, using the z option and requesting plots for "kcode
6." The user may specify a particular grid to use in determining H src
using the HSRC input card. If the HSRC card is provided, users should
specify a small number of grid boxes (e.g., 5-10 in each of the x, y, z
directions), chosen according to the symmetry of the problem and layout
of the fuel regions. If the HSRC card is not provided, the MCNP code
will automatically determine a grid that encloses all of the fission
sites for the cycle. The number of grid boxes will be determined by
dividing the number of histories per cycle by 20, and then finding the
nearest integer for each direction that will produce this number of
equal-sized grid boxes, although not fewer than 4 × 4 × 4 will be used.

Upon completion of the problem, the MCNP code will compute the average
value of H src for the last half of the active cycles, as well as the
(estimated population) standard deviation. The MCNP code will then
report the first cycle found (active or inactive) where H src falls
within one standard deviation of its average for the last half of the
cycles, along with a recommendation that at least that many cycles
should be inactive.

Plots of H src vs. cycle should be examined to further verify that the
number of inactive cycles is adequate for fission source convergence.

## /warning\_sign Caution

When running criticality calculations with the MCNP code, it is
essential that users examine the convergence of both k eff and the
fission source distribution (using Shannon entropy). If either k eff or
the fission source distribution is not converged prior to starting the
active cycles, then results from the calculations will not be correct.

## 2.8.2.9 Normalization of Standard Tallies in a Criticality Calculation

Track length fluxes, surface currents, surface fluxes, heating and
detectors-all the standard MCNP talliescan be made during a criticality
calculation. The tallies are for one fission neutron generation. Biases
may exist in these criticality results, but appear to be smaller than
statistical uncertainties [171]. These tallied quantities are
accumulated only after the I c inactive cycles are finished. The tally
normalization is per active source weight w , where w = N · ( I t -I c )
, and N is the nominal source size (from the KCODE card); It is the
total number of cycles in the problem; and I c is the number of inactive
cycles (from KCODE card). The number w is appropriately adjusted if the
last cycle is only partially completed. If the tally normalization flag
(on the KCODE card) is turned on, the tally normalization is the actual
number of starting particles during the active cycles rather than the
nominal weight above. Bear in mind, however, that the source particle
weights are all set to W = N/M so that the source normalization is based
upon the nominal source size N for each cycle.

An MCNP tally in a criticality calculation is for one fission neutron
being born in the system at the start of a cycle. The tally results must
be scaled either by the total number of neutrons in a burst or by the
neutron birth rate to produce, respectively, either the total result or
the result per unit time of the source. The scaling factor is entered on
the FM card.

The statistical errors that are calculated for the tallies assume that
all the neutron histories are independent. They are not independent
because of the cycle-to-cycle correlations that become more significant
for large or loosely coupled systems. For some very large systems, the
estimated standard deviation for a tally that involves only a portion of
the problem has been observed to be underestimated by a factor of five
or more [pages 42-44 of 174]. This value also is a function of the size
of the tally region. In the [174] slab reactor example, the entire
problem (that is, k eff ) standard deviation was not underestimated at
all. An MCNP study [177] of the FFTF fast reactor indicates that 90%
coverage rates for flux tallies are good, but that 2 out of 300 tallies
were beyond four estimated standard deviations. Independent runs can be
made to study the real eigenfunction distribution (that is, tallies) and
the estimated standard deviations for difficult criticality
calculations. This method is the only way to determine accurately these
confidence intervals for large or loosely coupled problems where
intergeneration correlation is significant.

## 2.8.2.10 Neutron Tallies and the MCNP Net Multiplication Factor

The MCNP net multiplication factor M printed out on the problem summary
page differs from the k eff from the criticality code. We will examine a
simple model to illustrate the approximate relationship between these
quantities and compare the tallies between standard and criticality
calculations.

Assume we run a standard MCNP calculation using a fixed neutron source
distribution identical in space and energy to the source distribution
obtained from the solution of an eigenvalue problem with k eff &lt; 1 .
Each generation will have the same space and energy distribution as the
source. The contribution to an estimate of any quantity from one
generation is reduced by a factor of k eff from the contribution in the

preceding generation. The estimate E k of a tally quantity obtained in a
criticality eigenvalue calculation is the contribution for one
generation produced by a unit source of fission neutrons. An estimate
for a standard MCNP fixed source calculation, E s , is the sum of
contributions for all generations starting from a unit source,

<!-- formula-not-decoded -->

Note that 1 / (1 -k eff ) is the true system multiplication, often
called the subcritical multiplication factor. The above result depends
on our assumptions about the unit fission source used in the standard
MCNP run. Usually, E s will vary considerably from the above result,
depending on the difference between the fixed source and the eigenmode
source generated in the eigenvalue problem. E s will be a fairly good
estimate if the fixed source is a distributed source roughly
approximating the eigenmode source. Tallies from a criticality
calculation are appropriate only for a critical system and the tally
results can be scaled to a desired fission neutron source (power) level
or total neutron pulse strength.

In a fixed-source MCNP problem, the net multiplication M is defined to
be unity plus the gain G f in neutrons from fission plus the gain G x
from nonfission multiplicative reactions. Using neutron weight balance
(creation equals loss),

<!-- formula-not-decoded -->

where W e is the weight of neutrons escaped per source neutron and W c
is the weight of neutrons captured per source neutron. In a criticality
calculation, fission is treated as an absorptive process; the
corresponding relationship for the net multiplication is then

<!-- formula-not-decoded -->

where the superscript o designates results from the criticality
calculation and W o f is the weight of neutrons causing fission per
source neutron. Because k eff is the number of fission neutrons produced
in a generation per source neutron, we can also write

<!-- formula-not-decoded -->

where ν is the average number of neutrons emitted per fission for the
entire problem. Making the same assumptions as above for the fixed
source used in the standard MCNP calculation and using Eqs. (2.307),
(2.308), and (2.309), we obtain or, by using (2.309) and (2.310),

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Often, the nonfission multiplicative reactions G o x glyph[lessmuch] 1 .
This implies that k eff can be approximated by k FS eff (from an
appropriate fixed source calculation) as

<!-- formula-not-decoded -->

when the two fission neutron source distributions are nearly the same.
The average value of ν in a problem can be calculated by dividing the
fission neutrons gained by the fission neutrons lost as given in the
totals of the neutron weight balance for physical events. Note, however,
that the above estimate is subject to the same limitations as described
in Eq. (2.307).

## 2.8.3 Recommendations for Making a Good Criticality Calculation

## 2.8.3.1 Problem Setup

As with any calculation, the geometry must be adequately and correctly
specified to represent the true physical situation. Plot the geometry
and check cells, materials, and masses for correctness. Specify the

appropriate nuclear data, including S ( α, β ) thermal data, at the
correct material temperatures. Ensure that initial fission source points
exist in every cell that contains fissionable material. Try running
short problems with both analog and implicit capture (see the PHYS :N
card) to improve the figure of merit for the combined k eff and any
tallies being made. Follow the tips for good calculations listed at the
end of Chapter 1.

## 2.8.3.2 Number of Neutrons per Cycle and Number of Cycles

Criticality calculations can suffer from two potential problems. The
first is the failure to sufficiently converge the spatial distribution
of the fission source from its initial guess to a distribution
fluctuating around the fundamental eigenmode solution. It is recommended
that the user make an initial calculation with a relatively small number
of source particles per generation (perhaps 500 or 1000) and generously
allow a large enough number of cycles so that the eigenvalue appears to
be fluctuating about a constant value. The user should examine the
results and continue the calculation if any trends in the eigenvalue are
noticeable. The SRCTP file from the last k eff cycle of the initial
calculation can then be used as the source for the final production
calculation to be made with a larger number of histories per cycle.

This convergence procedure can be extended for very slowly convergent
problems-typically large, thermal, low-leakage systems, where a
convergence calculation might be made with 500 or 1000 histories per
cycle. Then a second convergence calculation would be made with 1000
histories per cycle, using the SRCTP file from the first run as an
initial fission source guess. If the results from the second calculation
appear satisfactory, then a final calculation might be made using 5000
or 10000 particles per cycle with the SRCTP file from the second
calculation as an initial fission source guess. In the final
calculation, only a few cycles should need to be skipped. The bottom
line is this: skip enough cycles so that the fundamental spatial mode is
achieved.

The second potential problem arises from the fact that the criticality
algorithm produces a very small negative bias in the estimated
eigenvalue. The bias depends upon 1 /N , where N is the number of source
particles per generation. Thus, it is desirable to make N as large as
possible. Any value of N &gt; 500 should be sufficient to reduce the bias
to a small level. The eigenvalue bias ∆ k eff has been shown [171] to be
where

<!-- formula-not-decoded -->

σ k eff is the true standard deviation for the final k eff ,

σ approx is the approximate standard deviation computed assuming the
individual k eff values are statistically independent, and

<!-- formula-not-decoded -->

The standard deviations are computed at the end of the problem. Because
the σ 2 s decrease as 1 / ( I t -I c ) , ∆ k eff is independent of the
number of active cycles. Recall that ∆ k eff is proportional to 1 /N ,
the number of neutrons per k eff cycle.

Eq. (2.314) can be written [171] as the following inequality:

<!-- formula-not-decoded -->

This inequality is useful for determining an upper limit to the number
of active cycles that should be used for a calculation without having ∆
k eff dominate σ k eff . If σ k eff /k eff is 0.0010, which is a
reasonable value for

criticality calculations, and I t -I c is 1000, then k eff /σ k eff &lt; 0
. 5 and ∆ k eff will not dominate the k eff confidence interval. If σ k
eff is reasonably well approximated by the MCNP code's estimated
standard deviation, this ratio will be much less than 0.5.

The total running time for the active cycles is proportional to N · ( I
t -I c ) , and the standard deviation in the estimated eigenvalue is
proportional to 1 / √ N · ( I t -I c ) . From the results of the
convergence calculation, the total number of histories needed to achieve
the desired standard deviation can be estimated.

It is recommended that 200 to 1000 active cycles be used. This large
number of cycles will provide large batch sizes of k eff cycles (for
example, 40 batches of 10 cycles each for 400 active cycles) to compare
estimated standard deviations with those obtained for a batch size of
one k eff cycle. For example, for 400 active cycles, 40 batches of 10 k
eff values are created and analyzed for a new average k eff and a new
estimated standard deviation. The behavior of the average k eff by a
larger number of cycles can also be observed to ensure a good normal
spatial mode. Fewer than 30 active cycles is not recommended because
trends in the average k eff may not have enough cycles to develop.

## 2.8.3.3 Analysis of Criticality Problem Results

The goal of the calculation is to produce a k eff confidence interval
that includes the true result the desired fraction of the time. Check
all WARNING messages. Understand their significance to the calculation.
Study the results of the checks that the MCNP code makes that were
described in §2.8.2.8.

The criticality problem output contains a lot of useful information.
Study it to make sure that:

1. the problem terminated properly;
2. enough cycles were skipped to ensure that the normal spatial mode for fission sources was achieved;
3. all cells with fissionable material were sampled;
4. the average combined k eff appears to be varying randomly about the average value for the active cycles;
5. the average combined k eff -by-cycles-skipped does not exhibit a trend during the latter stages of the calculation;
6. the confidence intervals for the batched (with at least 30 batch values) combined k eff do not differ significantly from the final result;
7. the impact of having the largest of each of the three k eff estimators occurring on the next cycle is not too great on the final confidence interval; and
8. the combined k eff figure of merit should be stable.

The combined k eff figure of merit should be reasonably stable, but not
as stable as a tally figure of merit because the number of histories for
each cycle is not exactly the same, and the combined k eff relative
error may experience some changes because of changes in the estimated
covariance matrix for the three individual estimators.

Plots (using the z option) can be made of the three individual and
average k eff estimators by cycle, as well as the three-estimator-
combined k eff . Use these plots to better understand the results.

If there is concern about a calculation, the k eff -by-cycles-skipped
table presents the results that would be obtained in the final result
box for differing numbers of cycles skipped. This information can
provide insight into fission source spatial convergence, normality of
the k eff data sets, and changes in the 95% and 99%
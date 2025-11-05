---
title: "Chapter 2.7 - Variance Reduction"
chapter: "2.7"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/2_Geometry,_Data,_Physics,_and_Mathematics/2.7_Variance_Reduction.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

bias of 0.25%. The second issue is that the variance of the standard
error will generally increase when one partitions a fixed number of
histories into fewer and fewer batches.

One advantage batch statistics has over history statistics is in KCODE
problems. As discussed in §2.8.2.9, there is correlation between
generations and between histories in an eigenvalue calculation. By
summing together all histories in a generation, the correlation between
histories within a single generation is eliminated. The correlation
between generations, which is typically much larger, is not. This can
yield slightly more conservative tally standard error estimates in KCODE
.

Overall, with batch statistics, users should maximize both batch count
(to avoid standard error bias and variance, with more than 100 batches
recommended) and batch size (to ensure that batch statistics is faster
than history statistics). Further, in KCODE problems, one needs to
ensure the batch size is also sufficiently large to avoid
renormalization bias on the mean as per usual.

## 2.7 Variance Reduction

## 2.7.1 General Considerations

## 2.7.1.1 Variance Reduction and Accuracy

Variance-reducing techniques in Monte Carlo calculations reduce the
computer time required to obtain results of sufficient precision. Note
that precision is only one requirement for a good Monte Carlo
calculation. Even a zero variance calculation cannot accurately predict
natural behavior if other sources of error are not minimized. Factors
affecting accuracy were discussed in §2.6.

## 2.7.1.2 Two Choices that Affect Efficiency

The efficiency of a Monte Carlo calculation is affected by two choices:
tally type and random walk sampling. The tally choice (for example,
point detector flux tally vs. surface crossing flux tally) amounts to
trying to obtain the best results from the random walks sampled. The
chosen random walk sampling amounts to preferentially sampling
'important' random walks at the expense of 'unimportant' random walks. A
random walk is important if it has a large affect on a tally. These two
choices usually affect the time per history and the history variance as
described next in §2.7.1.3. The MCNP code estimates tallies of the form

<!-- formula-not-decoded -->

by sampling particle histories that statistically produce the correct
particle density N ( r , v , t ) . The tally function T ( r , v , t ) is
zero except where a tally is required. For example, for a surface
crossing tally (F1), T will be one on the surface and zero elsewhere.
MCNP variance reduction techniques allow the user to try to produce
better statistical estimates of N where T is large, usually at the
expense of poorer estimates where T is zero or small.

There are many ways to statistically produce N ( r , v , t ) . Analog
Monte Carlo simply samples the events according to their natural
physical probabilities. In this way, an analog Monte Carlo calculation
estimates the number of physical particles executing any given random
walk. Non-analog techniques do not directly simulate nature. Instead,
non-analog techniques are free to do anything if N , hence 〈 T 〉 , is
preserved. This preservation is accomplished by adjusting the weight of
the particles. The weight can be thought of as the number of physical
particles represented by the MCNP particle [§2.4.1]. Every time a
decision is made, the non-analog techniques require that the expected
weight associated with each outcome be the same as in the

analog game. In this way, the expected number of physical particles
executing any given random walk is the same as in the analog game.

For example, if an outcome 'A' is made q times as likely as in the
analog game, when a particle chooses outcome 'A,' its weight must be
multiplied by q -1 to preserve the expected weight for outcome 'A.' Let
p be the analog probability for outcome 'A'; then pq is the non-analog
probability for outcome 'A.' If w 0 is the current weight of the
particle, then the expected weight for outcome 'A' in the analog game is
w 0 · p and the expected weight for outcome 'A' in the non-analog game
is ( w 0 /q ) · pq .

The MCNP code uses three basic types of non-analog games: (1) splitting,
(2) Russian roulette, and (3) sampling from non-analog probability
density functions. The previous paragraph discusses type 3. Splitting
refers to dividing the particle's weight among two or more daughter
particles and following the daughter particles independently. Usually
the weight is simply divided evenly among k identical daughter particles
whose characteristics are identical to the parent except for a factor 1
/k in weight (for example, splitting in the weight window). In this case
the expected weight is clearly conserved because the analog technique
has one particle of weight w 0 at ( r , v , t ) , whereas the splitting
results in k particles of weight w 0 /k at ( r , v , t ) . In both cases
the outcome is weight w 0 at ( r , v , t ) .

Other splitting techniques split the parent particle into k , typically
two, differing daughter particles. The weight of the j th daughter
represents the expected number of physical particles that would select
outcome j from a set of k mutually exclusive outcomes. For example, the
MCNP forced collision technique considers two outcomes: (1) the particle
reaches a cell boundary before collision, or (2) the particle collides
before reaching a cell boundary. The forced collision technique divides
the parent particle representing w 0 physical particles into two
daughter particles, representing w 1 physical particles that are
uncollided and w 2 physical particles that collide. The uncollided
particle of weight w 1 is then put on the cell boundary. The collision
site of the collided particle of weight w 2 is selected from a
conditional distance-to-collision probability density, the condition
being that the particle must collide in the cell. This technique
preserves the expected weight colliding at any point in the cell as well
as the expected weight not colliding. A little simple mathematics is
required to demonstrate this technique.

Russian roulette takes a particle at ( r , v , t ) of weight w 0 and
turns it into a particle of weight w 1 &gt; w 0 with probability w 0 /w 1
and kills it (that is, weight = 0 ) with probability ( 1 -w 0 /w 1 ).
The expected weight at ( r , v , t ) is the same as in the analog game.

<!-- formula-not-decoded -->

Some techniques use a combination of these basic games and DXTRAN
[§2.7.2.18] uses all three.

## 2.7.1.3 Efficiency, Time per History, and History Variance

Recall from §2.6.5 that the measure of efficiency for MCNP calculations
is the FOM : FOM ≡ 1 / ( R 2 T ) , where

R 2 is the sample relative standard deviation of the mean and

T is the computer time for the calculation in minutes.

Recall from Eqs. (2.222) and (2.226a) that R = ( S/ √ N ) /x , where

S 2 is the sample history variance,

## N is the number of particles, and

- x is the sample mean.

Generally we are interested in obtaining the smallest R in a given time
T . The equation above indicates that to decrease R it is desirable to:
(1) decrease S and (2) increase N ; that is, decrease the time per
particle history. Unfortunately, these two goals usually conflict.
Decreasing S normally requires more time because better information is
required. Increasing N normally increases S because there is less time
per history to obtain information. However, the situation is not
hopeless. It is often possible either to decrease S substantially
without decreasing N too much or to increase N substantially without
increasing S too much, so that R decreases.

Many variance reduction techniques in the MCNP code attempt to decrease
R by either producing or destroying particles. Some techniques do both.
In general, techniques that produce tracks work by decreasing S (we hope
much faster than N decreases) and techniques that destroy tracks work by
increasing N (we hope much faster than S increases).

## 2.7.1.4 Strategy

Successful use of MCNP variance reduction techniques is often difficult,
tending to be more art than science. The introduction of the weight
window generator has improved things, but the user is still
fundamentally responsible for the choice and proper use of variance
reducing techniques. Each variance reduction technique has its own
advantages, problems, and peculiarities. However, there are some general
principles to keep in mind while developing a variance reduction
strategy.

Not surprisingly, the general principles all have to do with
understanding both the physical problem and the variance reduction
techniques available to solve the problem. If an analog calculation will
not suffice to calculate the tally, there must be something special
about the particles that tally. The user should understand the special
nature of those particles that tally. Perhaps, for example, only
particles that scatter in particular directions can tally. After the
user understands why the tallying particles are special, MCNP techniques
can be selected (or developed by the user) that will increase the number
of special particles followed.

After the MCNP techniques are selected the user typically has to supply
appropriate parameters to the variance reduction techniques. This is
probably more difficult than is the selection of techniques. The first
guess at appropriate parameters typically comes either from experience
with similar problems or from experience with an analog calculation of
the current problem. It is usually better to err on the conservative
side; that is, too little biasing rather than too much biasing. After
the user has supplied parameters for the variance reduction techniques,
a short Monte Carlo calculation is done so that the effectiveness of the
techniques and parameters can be monitored with the MCNP output.

The MCNP output contains much information to help the user understand
the sampling. This information should be examined to ensure that

1. the variance reduction techniques are improving the sampling of the particles that tally;
2. the variance reduction techniques are working cooperatively; that is, one is not destructively interfering with another;
3. the FOM table is not erratic, which would indicate poor sampling; and
4. there is nothing that looks obviously ridiculous.

Unfortunately, analyzing the output information requires considerable
thought and experience. Reference [160] shows in detail strategies and
analysis for a particular problem.

After ascertaining that the techniques are improving the calculation,
the user makes a few more short calculations to refine the parameters
until the sampling no longer improves. The weight window generator can
also be turned on to supply information about the importance function in
different regions of the phase space. This rather complex subject is
described in §2.7.2.12.2.

## 2.7.1.5 Erratic Error Estimates

Erratic error estimates are sometimes observed in MCNP calculations. In
fact, the primary reason for the Tally Fluctuation Chart (TFC) table in
the MCNP output is to allow the user to monitor the FOM and the relative
error as a function of the number of histories. With few exceptions,
such as an analog point detector embedded in a scattering medium with R
0 = 0 (a practice highly discouraged), MCNP tallies are finite variance
tallies. For finite variance tallies the relative error should decrease
roughly as √ N so the FOM should be roughly constant and the ten
statistical checks of the tallies [§2.6.9.2.3] should all be passed. If
the statistical checks are not passed, the error estimates should be
considered erratic and unreliable, no matter how small the relative
error estimate is.

Erratic error estimates occur typically because a high-weight particle
tallies from an important region of phase space that has not been well
sampled. A high-weight particle in a given region of phase space is a
particle whose weight is some nontrivial fraction of all the weight that
has tallied from that region because of all previous histories. A good
example is a particle that collides very close to a point or ring
detector. If not much particle weight has previously collided that close
to the detector, the relative error estimate will exhibit a jump for
that history. Another example is coherent photon scattering towards a
point detector [§2.4.4.2.5].

To avoid high-weight particles in important regions, the user should try
to ensure that these regions are well sampled by many particles and try
to minimize the weight fluctuation among these particles. Thus the user
should try to use biasing techniques that preferentially push particles
into important regions without introducing large weight fluctuations in
these regions. The weight window can often be very useful in minimizing
weight fluctuations caused by other variance reduction techniques.

If, despite a user's efforts, an erratic error estimate occurs, the user
should obtain event logs for those particles causing the estimate to be
erratic. The event logs should be studied to learn what is special about
these particles. When the special nature of these particles is
understood, the user can adjust the variance reduction techniques to
sample these particles more often. Thus their weight will be smaller and
they will not be as likely to cause erratic estimates.

## /warning\_sign Caution

Under no circumstances should these particles be discarded or ignored!
The fact that these particles contribute very heavily to the tally
indicates that they are important to the calculation and the user should
try to sample more of them.

## 2.7.1.6 Biasing Against Random Walks of Presumed Low Importance

It was mentioned earlier that one should be cautious and conservative
when applying variance reduction techniques. Many more people get into
trouble by overbiasing than by underbiasing. Note that preferentially
sampling some random walks means that some walks will be sampled (for a
given computer time) less frequently than they would have been in an
analog calculation. Sometimes these random walks are so heavily

biased against that very few, or even none, are ever sampled in an
actual calculation because not enough particles are run.

Suppose that (on average) for every million histories only one track
enters cell 23. Further suppose that a typical calculation is 100,000
histories. On any given calculation it is unlikely that a track enters
cell 23. Now suppose that tracks entering cell 23 turn out to be much
more important than a user thought. Maybe 10% of the answer should come
from tracks entering cell 23. The user could run 100,000 particles and
get 90% of the true tally with an estimated error of 1%, with no
indication that anything is amiss. However, suppose the biasing had been
set such that (on average) for every 10,000 particles, one track entered
cell 23, about 10 tracks total. The tally probably will be severely
affected by at least one high weight particle and will hover closer to
the true tally with a larger and perhaps erratic error estimate. The
essential point is this: following ten tracks into cell 23 does not cost
much computer time and it helps ensure that the estimated error cannot
be low when the tally is seriously in error. Always make sure that all
regions of the problem are sampled enough to be certain that they are
unimportant.

## 2.7.2 Variance-reduction Techniques

There are four classes of variance reduction techniques [16] that range
from the trivial to the esoteric.

## 2.7.2.1 Truncation Methods

These are the simplest of variance reduction methods. They speed up
calculations by truncating parts of phase space that do not contribute
significantly to the solution. The simplest example is geometry
truncation in which unimportant parts of the geometry are simply not
modeled. Specific truncation methods available in the MCNP code are
energy cutoff and time cutoff.

## 2.7.2.2 Population Control Methods

These use particle splitting and Russian roulette to control the number
of samples taken in various regions of phase space. In important regions
many samples of low weight are tracked, while in unimportant regions few
samples of high weight are tracked. A weight adjustment is made to
ensure that the problem solution remains unbiased. Specific population
control methods available in the MCNP code are geometry splitting and
Russian roulette, energy splitting/ roulette, time splitting/roulette,
weight cutoff, and weight windows.

## 2.7.2.3 Modified Sampling Methods

These alter the statistical sampling of a problem to increase the number
of tallies per particle. For any Monte Carlo event it is possible to
sample from any arbitrary distribution rather than the physical
probability as long as the particle weights are then adjusted to
compensate. Thus with modified sampling methods, sampling is done from
distributions that send particles in desired directions or into other
desired regions of phase space such as time or energy, or change the
location or type of collisions. Modified sampling methods in the MCNP
code include the exponential transform, implicit capture, forced
collisions, source biasing, and neutron-induced photon production
biasing.

## 2.7.2.4 Partially Deterministic Methods

These are the most complicated class of variance reduction methods. They
circumvent the normal random walk process by using deterministic-like
techniques, such as next-event estimators, or by controlling the random
number sequence. In the MCNP code these methods include point detectors,
DXTRAN, and correlated sampling.

The available MCNP variance reduction techniques are described next.

## 2.7.2.5 Energy Cutoff

The energy cutoff in the MCNP code is either a single user-supplied,
problem-wide energy level or a celldependent energy level. Particles are
terminated when their energy falls below the energy cutoff. The energy
cutoff terminates tracks and thus decreases the time per history. The
energy cutoff should be used only when it is known that low-energy
particles are either of zero or almost zero importance. An energy cutoff
is like a Russian roulette game with zero survival probability. A number
of pitfalls exist.

1. Remember that low-energy particles can often produce high-energy particles (for example, fission or low-energy neutrons inducing high-energy photons). Thus, even if a detector is not sensitive to low-energy particles, the low-energy particles may be important to the tally.
2. The CUT card energy cutoff is the same throughout the problem. Often low-energy particles have zero importance in some regions and high importance in others, and so a cell-dependent energy cutoff is also available with the ELPT card.
3. The answer will be biased (low) if the energy cutoff is killing particles that might otherwise have contributed. Furthermore, as N → ∞ the apparent error will go to zero and therefore mislead the unwary. Serious consideration should be given to two techniques discussed later, energy roulette and space-energy weight window, that are always unbiased.

The energy cutoff has one advantage not directly related to variance
reduction. A lower energy cutoff requires more cross sections so that
computer memory requirements go up and interactive computing with a
time-sharing system is degraded.

## 2.7.2.6 Time Cutoff

The time cutoff in the MCNP code, controlled with the MCNP CUT card, is
a single user-supplied, problemwide time value. Particles are terminated
when their time exceeds the time cutoff. The time cutoff terminates
tracks and thus decreases the computer time per history. A time cutoff
is like a Russian roulette game with zero survival probability. The time
cutoff should only be used in time-dependent problems where the last
time bin will be earlier than the cutoff.

Although the energy and time cutoffs are similar, more caution must be
exercised with the energy cutoff because low energy particles can
produce high energy particles, whereas a late time particle cannot
produce an early time particle.

## 2.7.2.7 Geometry Splitting with Russian Roulette

Geometry splitting/Russian roulette is one of the oldest and most widely
used variance-reducing techniques in Monte Carlo codes. When used
judiciously, it can save substantial computer time. As particles migrate
in an important direction, they are increased in number to provide
better sampling, but if they head in an unimportant direction, they are
killed in an unbiased manner to avoid wasting time on them.
Oversplitting, however, can substantially waste computer time. Splitting
generally decreases the history variance but increases the time per
history, whereas Russian roulette generally increases the history
variance but decreases the time per history.

Each cell in the problem geometry setup is assigned an importance I by
the user on the IMP input card. The number I should be proportional to
the estimated value that particles in the cell have for the quantity
being scored. When a particle of weight W passes from a cell of
importance I to one of higher importance I ′ , the particle is split
into a number of identical particles of lower weight according to the
following recipe. If I ′ /I is an integer n ( n ≥ 2 ), the particle is
split into n identical particles, each weighing W/n . Weight is
preserved in the integer splitting process. If I ′ /I is not an integer
but still greater than 1, splitting is done probabilistically so that
the expected number of splits is equal to the importance ratio. Denoting
n = glyph[floorleft] I ′ /I glyph[floorright] to be the largest integer
in I ′ /I , p = I ′ / I -n is defined. Then with probability p , n +1
particles are used, and with probability 1 -p , n particles are used.
For example, if I ′ /I is 2.75, 75% of the time split 3 for 1 and 25% of
the time split 2 for 1. The weight assigned to each particle is W · I/I
′ , which is the expected weight, to minimize dispersion of weights.

On the other hand, if a particle of weight W passes from a cell of
importance I to one of lower importance I ′ , so that I ′ /I &lt; 1 ,
Russian roulette is played and the particle is killed with probability 1
-( I ′ /I ) , or followed further with probability I ′ /I and weight W ·
I/I ′ .

Geometry splitting with Russian roulette is very reliable. It can be
shown that the weights of all particle tracks are the same in a cell no
matter which geometric path the tracks have taken to get to the cell,
assuming that no other biasing techniques, e.g. implicit capture, are
used. The variance of any tally is reduced when the possible
contributors all have the same weight.

The assigned cell importances can have any value-they are not limited to
integers. However, adjacent cells with greatly different importances
place a greater burden on reliable sampling. Once a sample track
population has deteriorated and lost some of its information, large
splitting ratios (like 20 to 1) can build the population back up, but
nothing can regain the lost information. It is generally better to keep
the ratio of adjacent importances small (for example, a factor of a few)
and have cells with optical thicknesses in the penetration direction
less than about two mean free paths. The MCNP code prints a warning
message if adjacent importances or weight windows have a ratio greater
than 4. PRINT Table 120 in the output file lists the affected cells and
ratios.

Generally, in a deep penetration shielding problem the sample size
(number of particles) diminishes to almost nothing in an analog
simulation, but splitting helps keep the size built up. A good rule is
to keep the population of tracks traveling in the desired direction more
or less constant-that is, approximately equal to the number of particles
started from the source. A good initial approach is to split the
particles 2 for 1 wherever the track population drops by a factor of 2.
Near-optimum splitting usually can be achieved with only a few
iterations and additional iterations show strongly diminishing returns.
Note that in a combined neutron/photon problem, importances will
probably have to be set individually for neutrons and for photons.

The MCNP code never splits into a void, although Russian roulette can be
played entering a void. Splitting into a void accomplishes nothing
except extra tracking because all the split particles must be tracked
across the void and they all make it to the next surface. The split
should be done according to the importance ratio of the last non-void
cell departed and the first non-void cell entered. Note four more items:

1. Geometry splitting/Russian roulette works well only in problems that do not have extreme angular dependence. In the extreme case, splitting/Russian roulette can be useless if no particles ever enter an important cell where the particles can be split.
2. Geometry splitting/Russian roulette will preserve weight variations. The technique is 'dumb' in that it never looks at the particle weight before deciding appropriate action. An example is geometry splitting/Russian roulette used with source biasing.
3. Geometry splitting/Russian roulette are turned on or off together.
4. Particles are killed immediately upon entering a zero importance cell, acting as a geometry cutoff.

## 2.7.2.8 Energy Splitting/Roulette

Energy splitting and roulette is controlled with the MCNP ESPLT card.
Energy splitting/roulette is independent of spatial cell. If the problem
has a space-energy dependence, the space-energy dependent weight window
is normally a better choice.

## 2.7.2.8.1 Energy Splitting

In some cases, particles are more important in some energy ranges than
in others. For example, it may be difficult to calculate the number of
235 U fissions because the thermal neutrons are also being captured and
not enough thermal neutrons are available for a reliable sample. In this
case, once a neutron falls below a certain energy level it can be split
into several neutrons with an appropriate weight adjustment. A second
example involves the effect of fluorescent emission after photoelectric
absorption. With energy splitting, the low-energy photon track
population can be built up rather than rapidly depleted, as would occur
naturally with the high photoelectric absorption cross section.

## 2.7.2.9 Energy Roulette

In many cases the number of tracks increases with decreasing energy,
especially neutrons near the thermal energy range. These tracks can have
many collisions requiring appreciable computer time. They may be
important to the problem and cannot be completely eliminated with an
energy cutoff, but their number can be reduced by playing a Russian
roulette game to reduce their number and computer time.

If a track's energy is below a prescribed energy level, the roulette
game is played, based on the input value of the survival probability. If
the game is won, the track's history is continued, but its weight is
increased by the reciprocal of the survival probability to conserve
weight.

## 2.7.2.10 Time Splitting/Roulette

Time splitting/roulette, controlled with the MCNP TSPLT card, is similar
to the energy splitting and roulette game just discussed, except a
particle's time can only increase, in contrast with a particle's energy
that may increase or decrease. Time splitting/roulette is independent of
spatial cell. If the problem has a space-time dependence, the space-time
dependent weight window is normally a better choice.

1. Splitting: In some cases, particles are more important later in time. For example, if a detector responds primarily to late time particles, then it may be useful to split the particles as time increases.
2. Russian roulette: In some cases there may be too many late time particles for optimal calculational efficiency, and the late time particles can be rouletted.

## 2.7.2.11 Weight Cutoff

In weight cutoff, Russian roulette is played if a particle's weight
drops below a user-specified weight cutoff. The particle is either
killed or its weight is increased to a user-specified level. The weight
cutoff was originally envisioned for use with geometry splitting/Russian
roulette and implicit capture [§2.7.2.14]. Because of this intent,

1. The weight cutoffs in cell j depend not only on w c , 1 and w c , 2 on the CUT card, but also on the cell importances.
2. Implicit capture is always turned on (except in detailed photon physics) whenever a nonzero w c , 1 is specified.

Referring to item 1 above, the weight cutoff is applied when the
particle's weight falls below R j · w c , 2 , where R j is the ratio of
the source cell importance ( IMP card) to cell j 's importance. With
probability W/ ( w c , 1 · R j ) the particle survives with new weight w
c , 1 · R j ; otherwise the particle is killed.

As mentioned earlier, the weight cutoff game was originally envisioned
for use with geometry splitting and implicit capture. To illustrate the
need for a weight cutoff when using implicit capture, consider what can
happen without a weight cutoff. Suppose a particle is in the interior of
a very large medium and there are neither time nor energy cutoffs. The
particle will go from collision to collision, losing a fraction of its
weight at each collision. Without a weight cutoff, a particle's weight
would eventually be too small to be representable in the computer, at
which time an error would occur. If there are other loss mechanisms (for
example, escape, time cutoff, or energy cutoff), the particle's weight
will not decrease indefinitely, but the particle may take an unduly long
time to terminate.

Weight cutoff's dependence on the importance ratio can be easily
understood if one remembers that the weight cutoff game was originally
designed to solve the low-weight problem sometimes produced by implicit
capture. In a high-importance region, the weights are low by design, so
it makes no sense to play the same weight cutoff game in high- and low-
importance regions.

Comments: Many techniques in the MCNP code cause weight change. The
weight cutoff was really designed with geometry splitting and implicit
capture in mind. Care should be taken in the use of other techniques.

Weight cutoff games are unlike time and energy cutoffs. In time and
energy cutoffs, the random walk is always terminated when the threshold
is crossed. Potential bias may result if the particle's importance was
not zero. A weight cutoff (weight roulette would be a better name) does
not bias the game because the weight is increased for those particles
that survive.

Setting the weight cutoff is not typically an easy task, and it requires
thought and experimentation. Essentially, the user must guess what
weight is worth following and start experimenting with weight cutoffs in
that vicinity.

## 2.7.2.12 Weight Window

The weight window, shown qualitatively in Fig. 2.24, is a phase space
splitting and Russian roulette technique. The phase space may be space-
energy, space-time, or space.

For each phase space cell, the user supplies a lower weight bound. The
upper weight bound is a user-specified multiple of the lower weight
bound. These weight bounds define a window of acceptable weights. If a
particle is below the lower weight bound, Russian roulette is played and
the particle's weight is either increased to a

<!-- image -->

Figure 2.24: Qualitative illustration of weight window splitting and
rouletting.

<!-- image -->

Note: Constants C U and C S apply throughout the entire problem.

Figure 2.25: Implementation diagram of MCNP weight window splitting and
rouletting ranges.

value within the window or the particle is terminated. If a particle is
above the upper weight bound, it is split so that all the split
particles are within the window. No action is taken for particles within
the window.

Figure 2.25 is a more detailed picture of the weight window. Three
important weights define the weight window in a phase space cell:

1. W L , the lower weight bound,
2. W S , the survival weight for particles playing roulette, and
3. W U , the upper weight bound.

The user specifies W L for each phase space cell on WWN cards. W S and W
U are calculated using two problemwide constants, C S and C U (entries
on the WWP card), as W S = C S W L and W U = C U W L . Thus all cells
have an upper weight bound C U times the lower weight bound and a
survival weight C S times the lower weight bound.

Although the weight window can be effective when used alone, it was
designed for use with other biasing techniques that introduce a large
variation in particle weight. In particular, a particle may have several
'unpreferred' samplings, each of which will cause the particle weight to
be multiplied by a weight factor substantially larger than one. Any of
these weight multiplications by itself is usually not serious, but the
cumulative weight multiplications can seriously degrade calculational
efficiency. Worse, the error estimates may be misleading until enough
extremely high-weight particles have been sampled. Monte Carlo novices
are prone to be misled because they do not have enough experience
reading and interpreting the summary information on the sampling
supplied by the MCNP code. Hence, a novice may put more faith in an
answer than is justified.

Although it is impossible to eliminate all pathologies in Monte Carlo
calculations, a properly specified weight window goes far toward
eliminating the pathology referred to in the preceding paragraph. As
soon as the weight gets above the weight window, the particle is split
and subsequent weight multiplications will thus be multiplying only a
fraction of the particle's weight (before splitting). Thus, it is hard
for the tally to be severely perturbed by a particle of extremely large
weight. In addition, low-weight particles are rouletted, so time is not
wasted following particles of trivial weight.

One cannot ensure that every history contributes the same score (a zero
variance solution), but by using a window inversely proportional to the
importance, one can ensure that the mean score from any track in the
problem is roughly constant. A weight window generator exists to
estimate these importance reciprocals [§2.7.2.12.2]. In other words, the
window is chosen so that the track weight times the mean score (for unit
track weight) is approximately constant. Under these conditions, the
variance is due mostly to the variation in the number of contributing
tracks rather than the variation in track score.

Thus far, two things remain unspecified about the weight window: the
constant of inverse proportionality and the width of the window. It has
been observed empirically that an upper weight bound five times the
lower weight bound works well, but the results are reasonably
insensitive to this choice anyway. The constant of inverse
proportionality is chosen so that the lower weight bound in some
reference cell is chosen appropriately. In most instances the constant
should be chosen so that the source particles start within the window.

## 2.7.2.12.1 Weight Window Compared to Geometry Splitting

Although both techniques use splitting and Russian roulette, there are
some important differences.

1. The weight window is space-energy dependent or space-time dependent. Geometry splitting is only space dependent.
2. The weight window discriminates on particle weight before deciding appropriate action. Geometry splitting is done regardless of particle weight.
3. The weight window works with absolute weight bounds. Geometry splitting is done on the ratio of the importance across a surface.
4. The weight window can be applied at surface crossings, collisions, or both. In addition, a weight window can be applied after a given distance of travel in a material (e.g., using the nmfp entry on the WWP card). Geometry splitting is applied only at surface crossings.
5. The weight window can control weight fluctuations introduced by other biasing techniques by requiring all particles in a cell to have weight W L ≤ W ≤ W U [161]. The geometry splitting will preserve any weight fluctuations because it is weight independent.
6. In the rare case where no other weight modification schemes are present, importances will cause all particles in a given cell to have the same weight. Weight windows will merely bound the weight.
7. The weight windows can be turned off for a given cell or energy regime by specifying a zero lower bound. This is useful in long or large regions where no single importance function applies. Care should be used because when the weight window is turned off at collisions, the weight cutoff game is turned on, sometimes causing too many particles to be killed.
8. For repeated structures, the geometry splitting uses the product of the importances at the different levels. No product is used for the weight windows.

## 2.7.2.12.2 The Stochastic Weight-window Generator

The generator, controlled with the MCNP WWG card, is a method that
automatically generates weight window importance functions [161]. The
values generated may be thought of as estimates of a forward-calculated
adjoint solution and can provide considerable insight into the physics
of a problem. The task of choosing importances by guessing, intuition,
experience, or trial and error is simplified and insight into the Monte
Carlo calculation is provided.

Low weight-window values indicate important regions. A low weight-window
value near the boundary with the outside world often indicates that the
geometry was truncated and more cells need to be added outside the
present geometry. Weight-window values that differ greatly between
adjacent cells indicate poor weight window convergence and/or a need to
subdivide the geometry into smaller phase space units that will have
different importances.

Although the window generator has proved very useful, two caveats are
appropriate. The generator is not a panacea for all importance sampling
problems and certainly is not a substitute for thinking on the user's
part. In fact, in most instances, the user will have to decide when the
generator's results look reasonable and when they do not. After these
disclaimers, one might wonder what use to make of a generator that
produces both good and bad results. To use the generator effectively, it
is necessary to remember that the generated parameters are only
statistical estimates and that these estimates can be subject to
considerable error. Nonetheless, practical experience indicates that a
user can learn to use the generator effectively to solve some very
difficult transport problems.

Examples of the weight-window generator are given in [160, 161] and
should be examined before using the generator. Note that this importance
estimation scheme works regardless of what other variance reduction
techniques are used in a calculation.

## 2.7.2.12.3 Theory

The importance of a particle at a point P in phase space equals the
expected score a unit weight particle will generate. Imagine dividing
the phase space into a number of phase space 'cells' or regions. The
importance of a cell then can be defined as the expected score generated
by a unit weight particle after entering the cell. Thus, with a little
bookkeeping, the cell's importance can be estimated as

<!-- formula-not-decoded -->

After the importances have been generated, the MCNP code assigns weight
windows inversely proportional to the importances. Then the MCNP code
supplies the weight windows in an output file suitable for use as an
input file in a subsequent calculation. The spatial portion of the phase
space is divided using either standard MCNP cells or a superimposed mesh
grid, which can be either rectangular or cylindrical. The energy portion
of the phase space is divided using the WWGE card. The time portion of
the phase space can be divided also. The constant of proportionality is
specified on the WWG card.

## 2.7.2.12.4 Limitations of the Weight-window Generator

The principal problem encountered when using the generator is bad
estimates of the importance function because of the statistical nature
of the generator. In particular, unless a phase space region is sampled
adequately, there will be either no generator importance estimate or an
unreliable one. The generator often needs a very crude importance guess
just to get any tally; that is, the generator needs an initial
importance function to estimate a (we hope) better one for subsequent
calculations.

Fortunately, in most problems the user can guess some crude importance
function sufficient to get enough tallies for the generator to estimate
a new set of weight windows. Because the weight windows are statistical,
several iterations usually are required before the optimum importance
function is found for a given tally. The first set of generated weight
windows should be used in a subsequent calculation, which generates a
better set of windows, etc.

In addition to iterating on the generated weight windows, the user must
exercise some degree of judgment. Specifically, in a typical generator
calculation, some generated windows will look suspicious and will have
to be reset. In the MCNP code, this task is simplified by an algorithm
that automatically scrutinizes cell-based importance functions, either
input by the user or generated by a generator. By flagging the generated
windows that are more than a factor of 4 different from those in
adjacent spatial regions, often it is easy to determine which generated
weight windows are likely to be statistical flukes that should be
revised before the next generator iteration. For example, suppose the
lower weight bounds in adjacent cells were 0.5, 0.3, 0.9, 0.05, 0.03,
0.02, etc.; here the user would probably want to change the 0.9 to
something like 0.1 to fit the pattern, reducing the 18:1 ratio between
cells 3 and 4.

The weight window generator also will fail when phase space is not
sufficiently subdivided and no single set of weight window bounds is
representative of the whole region. It is necessary to turn off the
weight windows (by setting a lower bound of zero) or to further
subdivide the geometry or energy phase space. Use of a superimposed
importance mesh grid for weight window generation is a good way to
subdivide the spatial portion of the phase space without complicating
the MCNP cell geometry.

On the other hand, the weight window generator will also fail if the
phase space is too finely subdivided and subdivisions are not adequately
sampled. Adequate sampling of the important regions of phase space is
always key to accurate Monte Carlo calculations, and the weight window
generator is a tool to help the user determine the important phase space
regions. When using the mesh-based weight window generator, resist the
temptation to create mesh cells that are too small.

## 2.7.2.13 Exponential Transform

The exponential transform, controlled with the MCNP EXT card, samples
the distance to collision from a non-analog probability density
function. Although many impressive results are claimed for the
exponential transform, it should be remembered that these results are
usually obtained for one-dimensional geometries and quite often for
energy-independent problems. A review article by Clark [162] gives
theoretical background and sample results for the exponential transform.
Sarkar and Prasad [163] have done a purely analytical analysis for the
optimum transform parameter for an infinite slab and one energy group.
The exponential transform allows particle walks to move in a preferred
direction by artificially reducing the macroscopic cross section in the
preferred direction and increasing the cross section in the opposite
direction according to

<!-- formula-not-decoded -->

where

- Σ ∗ t is the fictitious transformed cross section,

Σ t is the true total cross section,

Σ a is the absorption cross section,

- Σ s is the scattering cross section,
- p is the exponential transform parameter used to vary the degree of biasing | p | &lt; 1 can be a constant or p = Σ a / Σ t , in which case Σ ∗ t = Σ s , and
- µ is the cosine of the angle between the preferred direction and the particle's direction with µ ≤ 1 . The preferred direction can be specified on a VECT card.

At a collision a particle's weight is multiplied by a factor w c
(derived below) so that the expected weight colliding at any point is
preserved. The particle's weight is adjusted such that the weight
multiplied by the probability that the next collision is in d s about s
remains constant.

The probability of colliding in d s about s is Σexp( -Σ s )d s where Σ
is either Σ t or Σ ∗ t , so that preserving the expected collided weight
requires

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

or

If the particle reaches a cell surface, time cutoff, DXTRAN sphere, or
tally segment instead of colliding, the particle's weight is adjusted so
that the weight, multiplied by the probability that the particle travels
a distance s to the surface, remains constant. The probability of
traveling a distance s without collision is exp( -Σ s ) so that
preserving the expected uncollided weight requires

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

or

For one-dimensional deep penetration through highly absorbing media, the
variance typically will decrease as p goes from zero to some p ′ , and
then increase as p goes from p ′ to one. For p &lt; p ′ , the solution is
'underbiased' and for p &gt; p ′ , the solution is 'overbiased.'

Choosing p ′ is usually a matter of experience, although some insight
may be gleaned by understanding what happens in severely underbiased and
severely overbiased calculations. For illustration, apply the variance
analysis in §2.6.6 to a deep penetration problem when the exponential
transform is the only non-analog technique used. In a severely
underbiased calculation ( p → 0 ), very few particles will score, but
those that do will all contribute unity. Thus the variance in an
underbiased system is caused by a low scoring efficiency rather than a
large dispersion in the weights of the penetrating particles. In a
severely overbiased system ( p → 1 ) particles will score, but there
will be a large dispersion in the weights of the penetrating particles
with a resulting increase in variance.

Comments: the MCNP code gives a warning message if the exponential
transform is used without a weight window. There are numerous examples
where an exponential transform without a weight window gives unreliable
means and error estimates. However, with a good weight window both the
means and errors are well behaved. The exponential transform works best
on highly absorbing media and very poorly on highly scattering media.
For neutron penetration of concrete or earth, experience indicates that
a transform parameter p = 0 . 7 is about optimal. For photon penetration
of high-Z material, even higher values such as p = 0 . 9 are justified.

The following explains what happens with an exponential transform
without a weight window. For simplicity consider a slab of thickness T
with constant Σ t . Let the tally be a simple count (F1 tally) of the
weight penetrating the slab and let the exponential transform be the
only non-analog technique used. Suppose for a given penetrating history
that there are k flights, m that collide and n that do not collide. The
penetrating weight is thus

<!-- formula-not-decoded -->

However, the particle's penetration of the slab means that

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and hence

The only variation in w p is because of the (1 -pµ ) -1 factors that
arise only from collisions. For a perfectly absorbing medium, every
particle that penetrates scores exactly T exp( -p Σ t ) . If a particle
has only a few collisions, the weight variation will be small compared
to a particle that has many collisions. The weight window splits the
particle whenever the weight gets too large, depriving the particle of
getting a whole series of weight multiplications upon collision that are
substantially greater than one.

By setting p = Σ a / Σ t and µ = 1 so that Σ ∗ = Σ s , we sample
distance to scatter rather than distance to collision. It is preferable
to sample distance to scatter in highly absorbing media-in fact, this is
the standard procedure for astrophysics problems. Sampling distance to
scatter is also equivalent to implicit capture along a flight path
[§2.4.3.4.3]. However, in such highly absorbing media there is usually a
more optimal choice of transform parameter, p , and it is usually
preferable to take advantage of the directional component by not fixing
µ = 1 .

## 2.7.2.14 Implicit Capture

'Implicit capture,' 'survival biasing,' and 'absorption by weight
reduction' are synonymous. Implicit capture, controlled with the MCNP
CUT card, is a variance reduction technique applied in the MCNP code
after the collision nuclide has been selected. Let

σ t i be the total macroscopic cross section for nuclide i and

σ a i be the microscopic absorption cross section for nuclide i .

When implicit capture is used rather than sampling for absorption with
probability σ a i /σ t i , the particle always survives the collision
and is followed with new weight W (1 -σ a i /σ t i ) . Implicit capture
is a splitting process where the particle is split into absorbed weight
(which need not be followed further) and surviving weight.

Implicit capture can also be done along a flight path rather than at
collisions when a special form of the exponential transform is used. See
§2.4.3.4.3 for details.

Two advantages of implicit capture are

1. a particle that has finally, against considerable odds, reached the tally region and is not absorbed just before a tally is made, and
2. the history variance, in general, decreases when the surviving weight (that is, 0 or W ) is not sampled, but an expected surviving weight is used instead (see weight cutoff, §2.7.2.11).

Two disadvantages are

1. a fluctuation in particle weight is introduced, and
2. the time per history is increased (see weight cutoff, §2.7.2.11).

## 2.7.2.15 Forced Collisions

The forced collision method, controlled with the MCNP FCL card, is a
variance reduction scheme that increases sampling of collisions in
specified cells. Because detector contributions and DXTRAN particles
arise only from collisions and at the source, it is often useful in
certain cells to increase the number of collisions that can produce
large detector contributions or large weight DXTRAN particles. Sometimes
we want to sample collisions in a relatively thin cell (a fraction of a
mean free path) to improve the estimate of quantities like a reaction
rate or energy deposition or to cause collisions that are important to
some other part of the problem.

The forced collision method splits particles into collided and
uncollided parts. The collided part is forced to collide within the
current cell. The uncollided part exits the current cell without
collision and is stored in the bank until later when its track is
continued at the cell boundary. Its weight is

<!-- formula-not-decoded -->

where

W 0 is the current particle weight before forced collision, d is the
distance to cell surface in the particle's direction, and

Σ t is the macroscopic total cross section of the cell material.

That is, the uncollided part is the current particle weight multiplied
by the probability of exiting the cell without collision.

The collided part has weight W = W 0 (1 -exp( -Σ t d )) , which is the
current particle weight multiplied by the probability of colliding in
the cell. The uncollided part is always produced. The collided part may
be produced only a fraction f of the time, in which case the collided
weight is W 0 (1 -exp( -Σ t d )) /f . This is useful when several forced
collision cells are adjacent or when too much time is spent producing
and following forced collision particles.

The collision distance is sampled as follows. If P ( x ) is the
unconditional probability of colliding within a distance x , P ( x ) /P
( d ) is the conditional probability of colliding within a distance x
given that a collision is known to occur within a distance d . Thus the
position x of the collision must be sampled on the interval 0 &lt; x &lt; d
within the cell according to ξ = P ( x ) /P ( d ) , where and ξ is a
random number. Solving for x , one obtains

<!-- formula-not-decoded -->

Because a forced collision usually yields a collided particle having a
relatively small weight, care must be taken with the weight-cutoff game
[§2.7.2.11], the weight-window game [§2.7.2.12], and subsequent
collisions of the particle within the cell. The weight window game is
not played on the surface of a forced collision cell that the particle
is entering. For collisions inside the cell the user has two options.

| Option 1   | (negative entry for the cell on the forced collision card) After the forced collision, subsequent collisions of the particle are sampled normally. The weight cutoff game is turned off and detector contributions and DXTRAN particles are made before the weight window game is played. If weight windows are used, they should be set to the weight of the collided particle weight or set to zero if detector contributions or DXTRAN particles are desired.   |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Option 2   | (positive entry for the cell on the forced collision card) After the forced collision, detector contributions or DXTRAN particles are made and either the weight cutoff or weight window game is played. Surviving collided particles undergo subsequent forced collisions. If weight windows are used, they should bracket the weight of particles entering the cell.                                                                                             |

## 2.7.2.16 Source Variable Biasing

Provision is made for biasing the MCNP sources in any or all of the
source variables specified. The MCNP code's source biasing, although not
completely general, allows the production of more source particles, with
suitably reduced weights, in the more important regimes of each
variable. For example, one may start more 'tracks' at high energies and
in strategic directions in a shielding problem while correcting the
distribution by altering the weights assigned to these tracks. Sizable
variance reductions may result from such biasing of the source. Source
biasing samples from a non-analog probability density function.

If negative weight cutoff values are used on the CUT card, the weight
cutoff is made relative to the lowest value of source particle weight
generated by the biasing schemes. Two approaches are available:

1. Biasing by Specifying Explicit Sampling Frequencies: The SB input card determines source biasing for a particular variable by specifying the frequency at which source particles will be produced in the variable regime. If this fictitious frequency does not correspond to the fraction of actual source particles in a variable bin, the corrected weight of the source particles in a particular bin is determined by the ratio of the actual frequency (defined on the SP card) divided by the fictitious frequency (defined on the SB card) except for the lin-lin interpolation where it is defined to be the ratio of the actual to fictitious frequency evaluated at the exact value of the interpolated variable. The total weight of particles started in a given SI bin interval is thus conserved.

2. Biasing by Standard Prescription: Source biasing can use certain built-in prescriptions similar in principle to built-in analytic source distributions. These biasing options are detailed in §2.7.2.16.1, §2.7.2.16.2, §2.7.2.16.3, §2.7.2.16.4 for the appropriate source variables. The SB card input is analogous to that of an SP card for an analytic source distribution; that is, the first entry is a negative prescription number for the type of biasing required, followed by one or more optional user-specified parameters, which are discussed in the following sections.

## 2.7.2.16.1 Direction Biasing

The source direction can be biased (about a reference axis) by sampling
from a continuous exponential function or by using cones of fixed size
and starting a fixed fraction of particles within each cone. The user
can bias particles in any arbitrary direction or combination of
directions. The sampling of the azimuthal angle about the reference axis
is not biased.

In general, continuous biasing is preferable to fixed cone biasing
because cone biasing can cause problems from the discontinuities of
source track weight at the cone boundaries. However, if the cone
parameters (cone size and fraction of particles starting in the cone)
are optimized through a parameter study and the paths that tracks take
to contribute to tallies are understood, fixed cone biasing sometimes
can outperform continuous biasing. Unfortunately, it is usually time
consuming (both human and computer) and difficult to arrive at the
necessary optimization.

Source directional biasing can be sampled from an exponential
probability density function p ( µ ) = C exp( Kµ ) , where C is a
norming constant equal to K/ [exp( K ) -exp( -K )] and µ = cos θ , where
θ is an angle relative to the biasing direction. K is typically about 1;
K = 3 . 5 defines the ratio of weight of tracks starting in the biasing
direction to tracks starting in the opposite direction to be 1 / 1097 .
This ratio is equal to [1 -exp( -2 K )] / [exp(2 K ) -1] .

Table 2.10 may help to give the user a feel for the biasing parameter K
.

From this table for K = 1 , we see that half the tracks start in a cone
of 64 ◦ opening about the axis, and the weight of tracks at 64 ◦ is
0.762 times the unbiased weight of source particles. K = 0 . 01 is
almost equivalent to no biasing, and K = 3 . 5 is very strong.

Cone directional biasing can be invoked by specifying cone cosines on
the SI card, the true distribution on the SP card, and the desired
biasing probabilities on the SB card. Both histogram and linear
interpolation can be used. For example, consider the following case in
which the true distribution is isotropic:

<!-- formula-not-decoded -->

The direction cosine relative to the reference direction, say ν , is
sampled uniformly within the cone ν ′ &lt; ν &lt; 1 with probability p 2 and
within -1 &lt; ν &lt; ν ′ with the complementary probability p 1 . The weights
assigned are w (1 -ν ) / (2 p 2 ) and w (1 + ν ) / (2 p 1 ) ,
respectively. Note that for a very small cone defined by ν ′ and a high
probability p 2 glyph[greatermuch] p 1 for being within the cone, the
few source particles generated outside the cone will have a very high
weight that can severely perturb a tally.

## 2.7.2.16.2 Covering Cylinder Extent Biasing

This biasing prescription for the SDEF EXT variable allows the automatic
spatial biasing of source particles in a cylindrical-source-covering-
volume along the axis of the cylinder. Such biasing can aid in the
escape of source particles from optically thick source regions and thus
represents a variance reduction technique.

1

1

Table 2.10: Exponential Biasing Parameter

| K    |   Cumulative Probability |   θ |   Weight |
|------|--------------------------|-----|----------|
| 0.01 |                     0    |   0 |    0.99  |
|      |                     0.25 |  60 |    0.995 |
|      |                     0.5  |  90 |    1     |
|      |                     0.75 | 120 |    1.005 |
|      |                     1    | 180 |    1.01  |
| 1.0  |                     0    |   0 |    0.432 |
|      |                     0.25 |  42 |    0.552 |
|      |                     0.5  |  64 |    0.762 |
|      |                     0.75 |  93 |    1.23  |
|      |                     1    | 180 |    3.195 |
| 2.0  |                     0    |   0 |    0.245 |
|      |                     0.25 |  31 |    0.325 |
|      |                     0.5  |  48 |    0.482 |
|      |                     0.75 |  70 |    0.931 |
|      |                     1    | 180 |   13.4   |
| 3.5  |                     0    |   0 |    0.143 |
|      |                     0.25 |  23 |    0.19  |
|      |                     0.5  |  37 |    0.285 |
|      |                     0.75 |  53 |    0.569 |
|      |                     1    | 180 |  156.5   |

## 2.7.2.16.3 Covering Cylinder or Sphere Radial Biasing

This biasing prescription for the SDEF RAD variable allows for the
radial spatial biasing of source particles in either a spherical or
cylindrical source covering volume. Like the previous example of extent
biasing, this biasing can be used to aid in the escape of source
particles from optically thick source regions.

## 2.7.2.16.4 Biasing Standard Analytic Source Functions [164]

The preceding examples discuss the biasing of source variables by either
input of specific sampling frequencies corresponding to SP card entries
or by standard analytic biasing functions. A third biasing category can
be used in conjunction with standard analytic source probability
functions (for example, a Watt fission spectrum).

<!-- image -->

A negative entry on an SP card, that is,

SPn -i a b causes the MCNP code to sample source distribution n from
probability function i with input variables a, b, . . . Sampling schemes
cannot typically be biased. For example, for

SPn -5 a the evaporation spectrum f ( E ) = CE exp( -E/a ) is sampled
according to the sampling prescription E = -a log( ξ 1 · ξ 2 ) , where ξ
1 and ξ 2 are random numbers. Biasing this sampling scheme is usually
very difficult

or impossible. Fortunately, there is an approximate method available in
the MCNP code for biasing any arbitrary probability function [164]. The
code approximates the function as a table, then uses the usual SB card
biasing scheme to bias this approximate table function. The user inputs
a coarse bin structure to govern the bias and the code adds up to 300
additional equiprobable bins to assure accuracy. For example, suppose we
wish to sample the function and suppose that we want half the source to
be in the range 0 . 005 &lt; E &lt; 0 . 1 and the other half to be in the
range 0 . 1 &lt; E &lt; 20 . Then the input is

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The MCNP code breaks up the function into 150 equiprobable bins below E
= 0 . 1 and 150 more equiprobable bins above E = 0 . 1 . Half the time E
is chosen from the upper set of bins and half the time it is chosen from
the lower set. Particles starting from the upper bins have a different
weight from that of particles starting from the lower bins in order to
adjust for the bias, and a detailed summary is provided when the PRINT
option is used.

Note that in the above example the probability distribution function is
truncated below E = 0 . 005 and above E = 20 . The MCNP code prints out
how much of the distribution is lost in this manner and reduces the
weight accordingly.

It is possible for the user to choose a foolish biasing scheme. For
example,

<!-- formula-not-decoded -->

causes each of the 299 bins to be chosen with equal probability. This
would be all right except that since there are never more than 300
equiprobable bins, this allocates only 1 equiprobable bin per user-
supplied bin. The single equiprobable bin for 0 . 1 &lt; E &lt; 20 is
inadequate to describe the distribution function over this range. Thus
the table no longer approximates the function and the source will be
sampled erroneously. The MCNP code issues an error message whenever too
much of the source distribution is allocated to a single equiprobable
bin, alerting users to a poor choice of binning which might inadequately
represent the function. The coarse bins used for biasing should be
chosen so that the probability function is roughly equally distributed
among them.

## 2.7.2.17 Point Detector Tally

The point detector is a tally and does not bias random-walk sampling.
Recall from §2.6, however, that the tally choice affects the efficiency
of a Monte Carlo calculation. Thus, a little will be said here in
addition to the discussion in the tally section.

Although flux is a point quantity, flux at a point cannot be estimated
by either a track-length tally (F4) or a surface flux tally (F2) because
the probability of a track entering the volume or crossing the surface
of a point is zero. For very small volumes, a point detector tally can
provide a good estimate of the flux where it would be almost impossible
to get either a track-length or surface-crossing estimate because of the
low probability of crossing into the small volume.

It is interesting that a DXTRAN sphere of vanishingly small size with a
surface-crossing tally across the diameter normal to the particle's
trajectory is equivalent to a point detector. Thus, many of the comments
on DXTRAN are appropriate and the DXC cards essentially are identical to
the PD cards.

For a complete discussion of point detectors, see §2.5.6.1.

## 2.7.2.18 DXTRAN

DXTRAN, controlled with the MCNP DXT card, typically is used when a
small region is being inadequately sampled because particles have a very
small probability of scattering toward that region. To ameliorate this
situation, the user can specify in the input file a DXTRAN sphere that
encloses the small region. Upon collision (or exiting the source)
outside the sphere, DXTRAN creates a special 'DXTRAN particle' and
deterministically scatters it toward the DXTRAN sphere and
deterministically transports it, without collision, to the surface of
the DXTRAN sphere. The collision itself is otherwise treated normally,
producing a non-DXTRAN particle that is sampled in the normal way, with
no reduction in weight. However, the non-DXTRAN particle is killed if it
tries to enter the DXTRAN sphere on its next free flight. DXTRAN uses a
combination of splitting, Russian roulette, and sampling from a non-
analog probability density function.

The subtlety about DXTRAN is how the extra weight created for the DXTRAN
particles is balanced by the weight killed as non-DXTRAN particles cross
the DXTRAN sphere. The non-DXTRAN particle is followed without any
weight correction, so if the DXTRAN technique is to be unbiased, the
extra weight put on the DXTRAN sphere by DXTRAN particles must somehow
(on average) balance the weight of non-DXTRAN particles killed on the
sphere.

## 2.7.2.18.1 DXTRAN Viewpoint 1

One can view DXTRAN as a splitting process (much like the forced
collision technique) wherein each particle is split upon departing a
collision (or source point) into two distinct pieces:

1. the weight that does not enter the DXTRAN sphere on the next flight, either because the particle is not pointed toward the DXTRAN sphere or because the particle collides before reaching the DXTRAN sphere, and
2. the weight that enters the DXTRAN sphere on the next flight.

Let w 0 be the weight of the particle before exiting the collision, let
p 1 be the analog probability that the particle does not enter the
DXTRAN sphere on its next flight, and let p 2 be the analog probability
that the particle does enter the DXTRAN sphere on its next flight. The
particle must undergo one of these mutually exclusive events, thus p 1 +
p 2 = 1 . The expected weight not entering the DXTRAN sphere is w 1 = w
0 p 1 , and the expected weight entering the DXTRAN sphere is w 2 = w 0
p 2 . Think of DXTRAN as deterministically splitting the original
particle with weight w 0 into two particles, a non-DXTRAN (particle 1)
particle of weight w 1 and a DXTRAN (particle 2) particle of weight w 2
. Unfortunately, things are not quite that simple.

Recall that the non-DXTRAN particle is followed with unreduced weight w
0 rather than weight w 1 = w 0 p 1 . The reason for this apparent
discrepancy is that the non-DXTRAN particle (particle 1) plays a Russian
roulette game. Particle 1's weight is increased from w 1 to w 0 by
playing a Russian roulette game with survival probability p 1 = w 1 /w 0
. The reason for playing this Russian roulette game is simply that p 1
is not known, so assigning weight w 1 = p 1 w 0 to particle 1 is
impossible. However, it is possible to play the Russian roulette game
without explicitly knowing p 1 . It is not magic, just slightly subtle.

The Russian roulette game is played by sampling particle 1 normally and
keeping it only if it does not enter (on its next flight) the DXTRAN
sphere; that is, particle 1 survives (by definition of p 1 ) with
probability p 1 . Similarly, the Russian roulette game is lost if
particle 1 enters (on its next flight) the DXTRAN sphere; that is,
particle 1 loses the roulette with probability p 2 . To restate this
idea, with probability p 1 , particle 1 has weight w 0 and does not
enter the DXTRAN sphere and with probability p 2 , the particle enters
the DXTRAN sphere and is killed. Thus, the expected weight not entering
the DXTRAN sphere is w 0 p 1 +0 · p 2 = w 1 , as desired.

So far, this discussion has concentrated on the non-DXTRAN particle and
ignored exactly what happens to the DXTRAN particle. The sampling of the
DXTRAN particle will be discussed after a second viewpoint on the non-
DXTRAN particle.

## 2.7.2.18.2 DXTRAN Viewpoint 2

This second way of viewing DXTRAN does not see DXTRAN as a splitting
process but as an accounting process in which weight is both created and
destroyed on the surface of the DXTRAN sphere. In this view, DXTRAN
estimates the weight that should go to the DXTRAN sphere upon collision
and creates this weight on the sphere as DXTRAN particles. If the non-
DXTRAN particle does not enter the sphere, its next flight will proceed
exactly as it would have without DXTRAN, producing the same tally
contributions and so forth. However, if the non-DXTRAN particle's next
flight attempts to enter the sphere, the particle must be killed or
there would be (on average) twice as much weight crossing the DXTRAN
sphere as there should be because the weight crossing the sphere has
already been accounted for by the DXTRAN particle.

## 2.7.2.18.3 The DXTRAN Particle

Although the DXTRAN particle does not confuse people nearly as much as
the non-DXTRAN particle, the DXTRAN particle is nonetheless subtle.

The most natural approach for scattering particles toward the DXTRAN
sphere would be to sample the scattering angle Ω proportional to the
analog density. This approach is not used because it is too much work to
sample proportional to the analog density and because it is sometimes
useful to bias the sampling.

To sample Ω in an unbiased fashion when it is known that Ω points to the
DXTRAN sphere, one samples the conditional density where S (Ω) is the
set of directions pointed toward the DXTRAN sphere, and multiplies the
weight by GLYPH&lt;1&gt; S (Ω) P (Ω)dΩ , the probability of scattering into
the cone (see Fig. 2.26). However, it is too much work to calculate the
above integral for each collision. Instead, an arbitrary density
function P arb (Ω) is sampled and the weight is multiplied by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The total weight multiplication is the product of the fraction of the
weight scattering into the cone, GLYPH&lt;1&gt; S (Ω) P (Ω)dΩ , and the weight
correction for sampling P arb (Ω) instead of P con (Ω) . Thus, the
weight correction on scattering is

If µ is the cosine of the angle between the scattering direction and the
particle's incoming direction, then P (Ω) = P ( µ ) / 2 π because the
scattering is symmetric in the azimuthal angle. If η is the cosine of
the angle with respect to the cone axis (see Fig. 2.26) and if the
azimuthal angle about the cone axis is uniformly sampled, then P arb (Ω)
= P arb ( η ) / 2 π . Thus

<!-- formula-not-decoded -->

This result can be obtained more directly, but the other derivation does
not explain why P con (Ω) is not sampled.

Because P arb ( η ) is arbitrary, the MCNP code can choose a scheme that
samples η from a two-step density that favors particles within the
larger η interval. In fact, the inner DXTRAN sphere has to do only with
this arbitrary density and is not essential to the DXTRAN concept. The
DXTRAN particles are always created on the outside DXTRAN sphere, with
the inner DXTRAN sphere defining only the boundary between the two steps
in the density function.

After η = cos θ has been chosen, the azimuthal angle ϕ is sampled
uniformly on [0 , 2 π ) ; this completes the scattering. Recall,
however, that the DXTRAN particle arrives at the DXTRAN sphere without
collision. Thus the DXTRAN particle also has its weight multiplied by
the negative exponential of the optical path between the collision site
and the sphere. Thus the DXTRAN weight multiplication is

<!-- formula-not-decoded -->

where λ is the number of mean free paths from the exit site to the
chosen point on the DXTRAN sphere.

## 2.7.2.18.4 Inside the DXTRAN Sphere

So far, only collisions outside the DXTRAN sphere have been discussed.
At collisions inside the DXTRAN sphere, the DXTRAN game is not played
because first, the particle is already in the desired region, and
second, it is impossible to define the angular cone of Fig. 2.26. If
there are several DXTRAN spheres and the collision occurs in sphere i ,
DXTRAN will be played for all spheres except sphere i .

## 2.7.2.18.5 Real Particles vs. Pseudoparticle

Sometimes the DXTRAN particle is called a pseudoparticle and the non-
DXTRAN particle is called the original or real particle. The terms 'real
particle' and 'pseudoparticle' are potentially misleading. Both
particles are equally real: both execute random walks, both carry
nonzero weight, and both contribute to tallies. The only sense in which
the DXTRAN particle should be considered "pseudo" or 'not real' is
during creation. A DXTRAN particle is created on the DXTRAN sphere, but
creation involves determining what weight the DXTRAN particle should
have upon creation. Part of this weight determination requires
calculating the optical path between the collision site and the DXTRAN
sphere. This is done in the same way as point detectors (see point
detector pseudoparticles in §2.5.6.4.1). The MCNP code determines the
optical path by tracking a pseudoparticle from the collision site to the
DXTRAN sphere. This pseudoparticle is deterministically tracked to the
DXTRAN sphere simply to determine the optical path. No distance to
collision is sampled, no tallies are made, and no records of the
pseudoparticle's passage are kept (for example, tracks entering). In
contrast, once the DXTRAN particle is created at the sphere's surface,
the particle is no longer a pseudoparticle. The particle has real
weight, executes random walks, and contributes to tallies.

## 2.7.2.18.6 DXTRAN Details

To explain how the scheme works, consider the neighborhood of interest
to be a spherical region surrounding a designated point in space. In
fact, consider two spheres of arbitrary radii about the point P 0 = ( x
0 , y 0 , z 0 ) . Further, assume that the particle having direction (
u, v, w ) collides at the point P 1 = ( x, y, z ) , as shown in Fig.
2.26. The quantities θ I , θ O , η I , η O , R I , R O are defined in
the figure. Thus L , the distance between the collision point and center
of the spheres, is

<!-- formula-not-decoded -->

and where

Figure 2.26: Diagram of DXTRAN inner and outer spheres.

<!-- image -->

On collision, a DXTRAN particle is placed at a point on the outer sphere
of radius R O as described below. Provision is made for biasing the
contributions of these DXTRAN particles on the outer sphere within the
cone defined by the inner sphere. The weight of the DXTRAN particle is
adjusted to account for the probability of scattering in the direction
of the point on the outer sphere and traversing the distance with no
further collision.

The steps in sampling the DXTRAN particles are outlined next. First,
sample

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Next, sample η = η I + ξ (1 -η I ) uniformly in [ η I , 1) with
probability and with probability

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

sample η = η O + ξ ( η I -η O ) uniformly in [ η O , η I ) . The
quantity Q (equal to 5 in the MCNP code) is a factor that measures the
importance assigned to scattering in the inner cone relative to the
outer cone. Therefore, Q is also the ratio of weights for particles put
in the two different cones.

With η = cos θ chosen, a new direction ( u ′ , v ′ , w ′ ) is computed
by considering the rotation through the polar angle θ (and a uniform
azimuthal angle ϕ ) from the reference direction

<!-- formula-not-decoded -->

The particle is advanced in the direction ( u ′ , v ′ , w ′ ) to the
surface of the sphere of radius R O . The new DXTRAN particle with
appropriate direction and coordinates is banked. The weight of the
DXTRAN particle is determined by multiplying the weight of the particle
at collision by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

| µ                                     | is uu ′ + vv ′ + ww ′ ,                                                                                                                            |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| P ( µ )                               | is the scattering probability density function for scattering through the angle cos - 1 µ in the lab system for the event sampled at ( x, y, z ) , |
| ν                                     | is the number of particles emitted from the event, and                                                                                             |
| exp ( - GLYPH<1> P S P I σ t ( s )d s | is the attenuation along the line between P I ( x, y, z ) and P S , the point on the sphere where the particle is placed.                          |

In arriving at the weight factor, note that the density function for
sampling η is given by

<!-- formula-not-decoded -->

Thus the weight of the DXTRAN particle is the weight of the incoming
particle at P I modified by the ratio of the probability density
function for actually scattering from P I and arriving at P S without
collision to the density function actually sampled in choosing P S .
Therefore, particles in the outer cone have weights Q = 5 times higher
than the weights of similar particles in the inner cone.

The attenuation is calculated at the energy obtained by scattering
through the angle µ . The energy is uniquely determined from µ in
elastic scattering (and also in level scattering), whereas for other
nonelastic events, the energy is sampled from the corresponding
probability density function for energy, and may not depend on µ .

## 2.7.2.18.7 Auxiliary Games for DXTRAN

The major disadvantage to DXTRAN is the extra time consumed following
DXTRAN particles with low weights. Three special games can control this
problem:

1. DXTRAN weight cutoffs,
2. DXC games, and
3. DD game.

Particles inside a DXTRAN sphere are not subject to the normal MCNP
weight cutoff or weight window game. Instead DXTRAN spheres have their
own weight cutoffs, allowing the user to roulette DXTRAN particles that,
for one reason or another, do not have enough weight to be worth
following.

Sometimes low-weighted DXTRAN particles occur because of collisions many
free paths from the DXTRAN sphere. The exponential attenuation causes
these particles to have extremely small weights. The DXTRAN weight
cutoff will roulette these particles only after much effort has been
spent producing them. The DXC cards are cell dependent and allow DXTRAN
contributions to be taken only some fraction of the time. They work just
like the PD cards for detectors [§2.5.6.4.3]. The user specifies a
probability p i that a DXTRAN particle will be produced at a given
collision or source sampling in cell i . The DXTRAN result remains
unbiased because when a DXTRAN particle is produced its weight is
multiplied by p -1 i . The non-DXTRAN particle is treated exactly as
before, unaffected unless it enters the DXTRAN sphere, whereupon it is
killed. To see the utility, suppose that the DXTRAN weight cutoff was
immediately killing 99% of the DXTRAN particles from cell i . Only 1% of
the DXTRAN particles survive anyway, so it might be appropriate to
produce only 1% ( p i = 0 . 01 ) and have these not be killed
immediately by the DXTRAN weight cutoff. Or the p i s can often be set
such that all DXTRAN particles from all cells are created on the DXTRAN
sphere with roughly the same

weight. Choosing the p i s is often difficult and the method works well
typically when the material exponential attenuation is the major source
of the weight fluctuation.

Often the weight fluctuation arises because the probability P ( µ ) of
scattering toward the DXTRAN sphere varies greatly, depending on what
nuclide is hit and what the collision orientation is with respect to the
DXTRAN sphere. For example, consider a highly forward-peaked scattering
probability density. If the DXTRAN sphere were close to the particle's
pre-collision direction, P ( µ ) will be large; if the DXTRAN sphere
were at 105 ◦ to the pre-collision direction, P ( µ ) will be small. The
DD game can be used to reduce the weight fluctuation on the DXTRAN
sphere caused by these geometry effects, as well as the material
exponential attenuation effects.

The DD game selectively roulettes the DXTRAN pseudoparticles during
creation, depending on the DXTRAN particles' weight compared to some
reference weight. This is the same game that is played on detector
contributions, and is described in §2.5.6.4.3. The reference weight can
be either a fraction of the average of previous DXTRAN particle weights
or a user input reference weight. Recall that a DXTRAN particle's weight
is computed by multiplying the exit weight of the non-DXTRAN particle by
a weight factor having to do with the scattering probability and the
negative exponential of the optical path between the collision site and
DXTRAN sphere. The optical path is computed by tracking a pseudoparticle
from collision to the DXTRAN sphere. The weight of the pseudoparticle is
monotonically decreasing, so the DD game compares the pseudoparticle's
weight at the collision site and, upon exiting each cell, against the
reference weight. A roulette game is played when the pseudoparticle's
weight falls below the reference weight. The DD card stops tracking a
pseudoparticle as soon as the weight becomes inconsequential, saving
time by eliminating subsequent tracking.

## 2.7.2.18.8 Final Comments on DXTRAN

1. DXTRAN should be used carefully in optically thick problems. Do not rely on DXTRAN to do penetration.
2. If the source is user supplied, some provision must be made for obtaining the source contribution to particles on the DXTRAN sphere.
3. Extreme care must be taken when more than one DXTRAN sphere is in a problem. Cross-talk between spheres can result in extremely low weights and an excessive growth in the number of particle tracks.
4. Never put a zero on the DXC card. A zero will bias the calculation by not creating DXTRAN particles but still killing the non-DXTRAN particle if it enters the DXTRAN sphere.
5. Usually there should be a rough balance in the summary table of weight created and lost by DXTRAN.
6. DXTRAN cannot be used with reflecting surfaces for the same reasons that point detectors cannot be used with reflecting surfaces. See §2.5.6.4.2 for further explanation.
7. Both DXTRAN and point detectors track pseudoparticles to a point. Therefore, most of the discussion about detectors applies to DXTRAN. Refer to the section on detectors, §2.5.6, for more information.

## 2.7.2.19 Correlated Sampling

Correlated sampling estimates the change in a quantity resulting from a
small alteration of any type in a problem. This technique enables the
evaluation of small quantities that would otherwise be masked by the
statistical errors of uncorrelated calculations. The MCNP code
correlates a pair of runs by providing each new history in the original
and altered problems with the same starting pseudorandom number. The
same sequence of subsequent numbers is used and each history tracks
identically until the alteration causes
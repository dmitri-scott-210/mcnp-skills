---
title: "Chapter 1 - MCNP Code Overview"
chapter: "1"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/1_MCNP_Code_Overview.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Chapter 1

## MCNP Code Overview

This chapter provides an overview of the MCNP code with brief summaries
of the material covered in-depth in later chapters. First, §1.1 briefly
describes the MCNP code and Monte Carlo particle transport method. The
following five features of MCNP code are introduced in §1.2: (1) nuclear
data and reactions, (2) source specifications, (3) tallies and output,
(4) estimation of errors, and (5) variance reduction. Finally, §1.3
explains MCNP geometry setup and the concept of cells and surfaces.

## 1.1 The MCNP Code and the Monte Carlo Method

The MCNP code is a general-purpose, continuous-energy, generalized-
geometry, time-dependent code designed to track 37 particle types over
broad range of energies. The code was first created in 1977 when a
series of special-purpose Monte Carlo codes were combined to create the
first generalized Monte Carlo particle transport code. The worldwide
user community's high confidence in the MCNP code's predictive
capabilities are based on its performance with verification and
validation test suites, comparisons to its predecessor codes, underlying
high quality nuclear and atomic databases, and significant use by its
users across the world in hundreds of applications. The MCNP code has
become a repository for physics knowledge where the knowledge and
expertise contained in the MCNP code is formidable.

The user creates an MCNP input file containing information about the
problem in areas such as:

- the geometry specification,
- the description of materials and selection of cross-section evaluations,
- the location and characteristics of the source,
- the type of answers or tallies desired, and
- any variance reduction techniques used to improve efficiency.

An introduction to each area is given in Chapter 3, with more detailed
discussion in the MCNP primers [Part III].

There are five guiding principles to keep in mind when developing and
running a Monte Carlo particle transport calculation. They will be more
meaningful as you read this manual and gain experience with the MCNP
code, but no matter how sophisticated a user you may become, never
forget the following five points:

1. Define and sample the geometry and source well.
2. You cannot recover lost information.

3. Question the statistical convergence, stability, and reliability of results.
4. Be conservative when applying variance reduction.
5. The number of histories run is not indicative of the quality of the answer.

The following subsections compare Monte Carlo and deterministic methods
and provide a simple description of the Monte Carlo method.

## 1.1.1 Monte Carlo Methods vs. Deterministic Methods

Monte Carlo methods are different from deterministic transport methods.
Deterministic methods, the most common of which is the discrete
ordinates method, solve the transport equation for the average particle
behavior. By contrast, Monte Carlo obtains answers by simulating
individual particles and recording some aspects (tallies) of their
average behavior. The average behavior of particles in the physical
system is then inferred (using the Central Limit Theorem) from the
average behavior of the simulated particles. Not only are Monte Carlo
and deterministic methods very different ways of solving a problem, even
what constitutes a solution is different. Deterministic methods
typically give fairly complete information (for example, flux)
throughout the phase space of the problem. Monte Carlo supplies
information only about specific tallies requested by the user.

When Monte Carlo and discrete ordinates methods are compared, it is
often said that Monte Carlo solves the integral transport equation,
whereas discrete ordinates solves the integro-differential transport
equation. Two things are misleading about this statement. First, the
integral and integro-differential transport equations are two different
forms of the same equation; if one is solved, the other is solved.
Second, Monte Carlo 'solves' a transport problem by simulating particle
histories. A transport equation need not be written to solve a problem
by Monte Carlo. Nonetheless, one can derive an equation that describes
the probability density of particles in phase space; this equation turns
out to be the same as the integral transport equation.

Without deriving the integral transport equation, it is instructive to
investigate why the discrete ordinates method is associated with the
integro-differential equation and Monte Carlo with the integral
equation. The discrete ordinates method visualizes the phase space to be
divided into many small regions, and the particles move from one region
to another. In the limit, as the regions get progressively smaller,
particles moving from region to region take a differential amount of
time to move a differential distance in space. In the limit, this
approaches the integro-differential transport equation, which has
derivatives in space and time. By contrast, Monte Carlo transports
particles between events (for example, collisions) that are separated in
space and time. Neither differential space nor time are inherent
parameters of Monte Carlo transport. The integral equation does not have
terms involving time or space derivatives.

Monte Carlo is well suited to solving complicated three-dimensional,
time-dependent problems. Because the Monte Carlo method does not use
phase space regions, there are no averaging approximations required in
space, energy, and time. This is especially important in allowing
detailed representation of all aspects of physical data.

## 1.1.2 The Monte Carlo Method

Monte Carlo can be used to duplicate theoretically a random walk process
(such as the interaction of nuclear particles with materials) and is
particularly useful for complex problems that cannot be modeled by
computer codes that use deterministic methods. The individual
probabilistic events that comprise a particle history from birth to
death are simulated sequentially, but particle histories can be
simulated in parallel. The probability distributions governing these
events are statistically sampled to describe the total phenomenon.

## Event Log

1. Neutron scatter, photon production
2. Fission, photon production
3. Neutron capture
4. Neutron leakage
5. Photon scatter
6. Photon leakage
7. Photon capture

Figure 1.1: Various particle random walks. The zigzag lines are used to represent the moving of photons in the MCNP user manual, but the MCNP code treats a photon movement as a straight line between collisions.

<!-- image -->

In general, the simulation is performed on a computer because the number
of trials necessary to adequately describe the phenomenon is usually
quite large. The statistical sampling process is based on the selection
of random numbers-analogous to throwing dice in a gambling casino-hence
the name 'Monte Carlo.' In particle transport, the Monte Carlo technique
is pre-eminently realistic (a numerical experiment). It consists of
actually following each of many particles from a source throughout its
life to its death in some terminal category (absorption, escape, etc.).
Probability distributions are randomly sampled using nuclear data to
determine the outcome at each step of its life.

The MCNP code treats neutrons and photons as particles moving in a
straight line between collisions. Figure 1.1 represents the random
history of a neutron incident on a slab of material that can undergo
fission. Numbers between 0 and 1 are selected randomly to determine what
(if any) and where interaction takes place, based on the rules (physics)
and probabilities (nuclear data) governing the processes and materials
involved. In this particular example, a neutron collision occurs at
event 1. The neutron is scattered in the direction shown, which is
selected randomly from the physical scattering distribution. A photon is
also produced and is temporarily stored, or banked, for later analysis.
At event 2, fission occurs, resulting in the termination of the incoming
neutron and the birth of two outgoing neutrons and one photon. One
neutron and the photon are banked for later analysis. The first fission
neutron is captured at event 3 and terminated. The banked neutron is now
retrieved and, by random sampling, leaks out of the slab at event 4. The
fission-produced photon has a collision at event 5 and leaks out at
event 6. The remaining photon generated at event 1 is now followed with
a capture at event 7. Note that the MCNP code retrieves banked particles
such that the last particle stored in the bank is taken out first (i.
e., last-in-first-out stack). This neutron history is now complete. As
more and more such histories are followed, the neutron and photon
distributions become better known. The quantities of interest (whatever
the user requests) are tallied, along with estimates of the statistical
precision (uncertainty) of the results.

## 1.2 Introduction to Features of the MCNP Code

Various features, concepts, and capabilities of the MCNP code are
summarized in this section. More detail concerning each topic is
available in later chapters or appendices.

## 1.2.1 Nuclear Data and Reactions

The MCNP code uses continuous-energy nuclear and atomic data libraries.
The primary sources of nuclear data are evaluations from the Evaluated
Nuclear Data File (ENDF) [4] system, Advanced Computational Technology
Initiative (ACTI) [5], the Evaluated Nuclear Data Library (ENDL) [6],
Evaluated Photon Data Library (EPDL) [7], the Activation Library (ACTL)
[8] compilations from Livermore, and evaluations from the Nuclear
Physics (T-16) Group [9-11] at Los Alamos. Evaluated data are processed
into a format appropriate for the MCNP code by codes such as NJOY
[12-14]. The processed nuclear data libraries retain as much detail from
the original evaluations as is feasible to faithfully reproduce the
evaluator's intent. The ACE nuclear data libraries used by the MCNP code
are publicly available at https://nucleardata.lanl.gov. Note that while
'ACE' is an acronym for 'A Compact ENDF,' a better description of ACE is
that it is the processed data for use in the MCNP code, as these files
are often not compact.

Nuclear data tables exist for neutron interactions, neutron-induced
photons, photon interactions, neutron dosimetry or activation, and
thermal particle scattering S ( α, β ) . Most of the photon and electron
data are atomic rather than nuclear in nature; photonuclear data are
also included. Each data table available to the MCNP code is listed on a
cross-section directory file, typically referred to as the xsdir file.
Users may select specific data tables through unique identifiers for
each table described in §1.2.3. These identifiers generally contain the
atomic number Z, mass number A, and library specifier ID.

Over 836 neutron interaction tables are available for approximately 100
different isotopes and elements. Multiple tables for a single isotope
are provided primarily because data have been derived from different
evaluations, but also because of different temperature regimes and
different processing tolerances. More neutron interaction tables are
constantly being added as new and revised evaluations become available.
Neutron-induced photon production data are given as part of the neutron
interaction tables when such data are included in the evaluations.

Photon interaction tables exist for all elements from Z = 1 through Z =
100 . The data in the photon interaction tables allow the MCNP code to
account for coherent and incoherent scattering, photoelectric absorption
with the possibility of fluorescent emission, and pair production.
Scattering angular distributions are modified by atomic form factors and
incoherent scattering functions. Cross sections for nearly 2,000
dosimetry or activation reactions involving over 400 target nuclei in
ground and excited states are part of the MCNP data package. These cross
sections can be used as energy-dependent response functions in the MCNP
code to determine reaction rates but cannot be used as transport cross
sections.

Thermal data tables are appropriate for use with the S ( α, β )
scattering treatment in the MCNP code. The data include chemical
(molecular) binding and crystalline effects that become important as the
neutron's energy becomes sufficiently low. The thermal scattering
library based on ENDF/B-VIII.0 contains 34 materials and 253 evaluations
[15].

## 1.2.2 Target Identifiers

The MCNP code supports three formats for identifying targets: the ZAID
format, the SZAID format, and the name format. In this section, Z is the
atomic number, A is the mass number, and S is the isomeric state. For
natural materials or atomic data, A can be zero.

The oldest supported format is the ZAID format, which stands for ' Z -A
identifier.' It is a 6-digit number given as

For non-metastable nuclides, this conventionally appears as ZZZAAA. The
first metastable is 400 higher than the non-metastable ZZZAAA.

<!-- formula-not-decoded -->

1

Table 1.1: Examples of Target Identifiers

| Target     |   ZAID |   SZAID | Name (All possibilities, first is recommended)   |
|------------|--------|---------|--------------------------------------------------|
| 1 H        |   1001 |    1001 | H-1 / H1                                         |
| Nat C      |   6000 |    6000 | C-0 / C0                                         |
| 99 Tc      |  43099 |   43099 | Tc-99 / Tc99                                     |
| 99 m Tc    |  43499 | 1043099 | Tc-99m1/ Tc-99m / Tc99m1 / Tc99m                 |
| 177 m 2 Hf |  72677 | 2072177 | Hf-177m2 / Hf177m2                               |
| 238 U      |  92238 |   92238 | U-238 / U238                                     |
| 242 Am     |  95642 | 1095242 | Am-242 / Am242                                   |
| 242 m Am   |  95242 |   95242 | Am-242m1 / Am-242m / Am242m1 / Am242m            |

The second supported format is the SZAID format, which stands for ' S -Z
-A identifier.' It is a 7-digit number given as

In text representation, it is commonly shown as SZZZAAA.

## /warning\_sign Caution

As a historical quirk, 242 m 1 Am and 242 Am are swapped in the ZAID and
SZAID formats, so that the former is 95242 and the latter is 95642 for
ZAID and 1095242 for SZAID. It is important to verify if a data library
follows this convention. To date, all LANL-published libraries do. The
name format does not swap these isomers. As such, Am-242m1 can load a
table labeled 95242 .

The final form is the name format. It takes the form Nn-AAAmS, where Nn
is the one- or two-letter case-insensitive isotopic symbol. Isotopic
symbols for all Z ≤ 118 are available. The hyphen is optional. The
metastable indicator is absent for non-metastables, can be m or m1 for
the first metastable state, and can be as high as m4 . The C++ regular
expression ( std::regex , ECMAScript syntax) used is

```
"^([a-zA-Z]{1,2})-?([0-9]{1,3})(m[1-4]?)?"
```

In general, the MCNP code uses the name format whenever possible. When
not possible, most typically due to breaking compatibility with input
files with previous versions of the code or changing defined file
formats, ZAIDs specifically will be used. Examples of all three formats
can be found in Table 1.1. Input cards list which of these formats they
support.

One can add analytic or otherwise non-physical data tables by using an
identifier with Z = 999 or with an isotopic symbol of Xx. Any A will be
accepted, allowing up to 999 possible data tables. The code will prevent
the use of such data with model physics, which relies on valid Z and A
values.

## 1.2.3 Table Identifiers

Table identifiers are listed in the xsdir file described in Appendix B
and is composed of three parts. The first is the target identifier,
which for single targets are described in §1.2.2. If there are multiple
targets, as is typical of thermal scattering data, the target is simply
a string. The second is the library identifier, which can either be a
2-digit or more integer or an arbitrary string. The third is the physics
identifier [Table B.1] which defines the projectile and the governed
physics.

<!-- formula-not-decoded -->

Table 1.2: Examples of Table Identifiers

| Identifier                                      | Projectile            | Physics                                                    | Target                | Library Identifier          |
|-------------------------------------------------|-----------------------|------------------------------------------------------------|-----------------------|-----------------------------|
| 92238.80c h-h2o.40t                             | Neutron Neutron       | Continuous Energy S ( α,β ) Thermal Scattering             | 238 U H in H 2 O      | 80 40                       |
| U-238.Lib80x-293.6K.c U-0.eprdata14.p 1001.810h | Neutron Photon Proton | Continuous Energy Continuous Photoatomic Continuous Energy | 238 U Elemental U 1 H | Lib80x-293.6K eprdata14 810 |

The table identifier takes the form of

[target identifier] . [library identifier][physics identifier]

if the library identifier is an integer. It takes the form of

## [target identifier] . [library identifier] . [physics identifier]

if the library identifier is a non-integer string. Note that there is a
period required between the library and physics identifiers in this
form. Several examples are shown in Table 1.2 (the last three options
became available in version 6.3.1).

## 1.2.4 Source Specification

The MCNP code's generalized user-input source capability allows the user
to specify a wide variety of source conditions without having to make a
code modification. Independent probability distributions may be
specified for the source variables of energy, time, position, and
direction, and for other parameters such as starting cell(s) or
surface(s). Information about the geometric extent of the source can
also be given. In addition, source variables may depend on other source
variables (for example, energy as a function of angle) thus extending
the built-in source capabilities of the code. The user can bias all
input distributions.

In addition to input probability distributions for source variables,
certain built-in functions are available. These include various analytic
functions for fission and fusion energy spectra such as Watt,
Maxwellian, and Gaussian spectra; Gaussian for time; and isotropic,
cosine, and monodirectional for direction. Biasing may also be
accomplished by special built-in functions.

A surface source allows particles crossing a surface in one problem to
be used as the source for a subsequent problem. The decoupling of a
calculation into several parts allows detailed design or analysis of
certain geometric regions without having to rerun the entire problem
from the beginning each time. The surface source has a fission volume
source option that starts particles from fission sites where they were
written in a previous run.

The MCNP code provides the user three methods to define an initial
criticality source to estimate k eff , the ratio of neutrons produced in
successive generations in fissile systems.

## 1.2.5 Tallies and Output

The user can instruct the MCNP code to make various tallies related to
particle current, particle flux, and energy deposition. MCNP tallies are
normalized to be per starting particle except for a few special cases
with criticality sources. Currents can be tallied as a function of
direction across any set of surfaces, surface segments, or sum of
surfaces in the problem. Charge can be tallied for charged particles.
Fluxes across any set of surfaces, surface segments, sum of surfaces,
and in cells, cell segments, or sum of cells are also available.

Similarly, the fluxes at designated detectors (points or rings) are
standard tallies, as well as radiography detector tallies. Fluxes can
also be tallied on a mesh superimposed on the problem geometry. Heating
and fission tallies give the energy deposition in specified cells. A
pulse height tally provides the energy distribution of pulses created in
a detector by radiation. In addition, particles may be flagged when they
cross specified surfaces or enter designated cells, and the
contributions of these flagged particles to the tallies are listed
separately. Tallies such as the number of fissions, the number of
absorptions, the total helium production, or any product of the flux
times the approximately 100 standard ENDF reactions plus several
nonstandard ones may be calculated with any of the MCNP tallies. In
fact, any quantity of the form

<!-- formula-not-decoded -->

can be tallied, where φ ( E ) is the energy-dependent fluence, and f ( E
) is any product or summation of the quantities in the cross-section
libraries or a response function provided by the user. The tallies may
also be reduced by line-of-sight attenuation. Tallies may be made for
segments of cells and surfaces without having to build the desired
segments into the actual problem geometry. All tallies are functions of
time and energy as specified by the user and are normalized to be per
starting particle. Mesh tallies are functions of energy and are also
normalized to be per starting particle.

In addition to the tally information, the output file contains tables of
standard summary information to give the user a better idea of how the
problem ran. This information can give insight into the physics of the
problem and the adequacy of the Monte Carlo simulation. If errors occur
during the running of a problem, detailed diagnostic prints for
debugging are given. Printed with each tally is also its statistical
relative error corresponding to one standard deviation. Following the
tally is a detailed analysis to aid in determining confidence in the
results. Ten pass/no-pass checks are made for the user-selectable tally
fluctuation chart (TFC) bin of each tally. The quality of the confidence
interval still cannot be guaranteed because portions of the problem
phase space possibly still have not been sampled. Tally fluctuation
charts, described in the following section, are also automatically
printed to show how a tally mean, error, variance of the variance, and
slope of the largest history scores fluctuate as a function of the
number of histories run.

All tally results, except for mesh tallies, can be displayed
graphically, either while the code is running or in a separate post-
processing mode.

## 1.2.6 Estimation of Monte Carlo Errors

MCNP tallies are normalized to be per starting particle and are printed
in the output accompanied by a second number R , which is the estimated
relative error defined to be one estimated standard deviation of the
mean S x divided by the estimated mean x . In the MCNP code, the
quantities required for this error estimate-the tally and its second
moment-are computed after each complete Monte Carlo history, which
accounts for the fact that the various contributions to a tally from the
same history are correlated. For a well-behaved tally, R will be
proportional to 1 / √ N where N is the number of histories. Thus, to
halve R , we must increase the total number of histories fourfold. For a
poorly behaved tally, R may increase as the number of histories
increases.

The estimated relative error can be used to form confidence intervals
about the estimated mean, allowing one to make a statement about what
the true result is. The Central Limit Theorem states that as N
approaches infinity there is a 68% chance that the true result will be
in the range x (1 ± R ) and a 95% chance in the range x (1 ± 2 R ) . It
is extremely important to note that these confidence statements refer
only to the precision of the Monte Carlo calculation itself and not to
the accuracy of the result compared to the true physical value. A
statement regarding accuracy requires a detailed analysis of the
uncertainties in the physical data, modeling, sampling techniques, and
approximations, etc., used in a calculation.

The guidelines for interpreting the quality of the confidence interval
for various values of R are listed in Table 1.3.

Table 1.3: Guidelines for Interpreting the Relative Error, R ∗ .

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

For all tallies except next-event estimators, hereafter referred to as
point detector tallies, the quantity R should be less than 0.10 to
produce generally reliable confidence intervals. Point detector results
tend to have larger third and fourth moments of the individual tally
distributions, so a smaller value of R , &lt; 0 . 05 , is required to
produce generally reliable confidence intervals. The estimated
uncertainty in the Monte Carlo result must be presented with the tally
so that all are aware of the estimated precision of the results.

Keep in mind the footnote to Table 1.3. For example, if an important but
highly unlikely particle path in phase space has not been sampled in a
problem, the Monte Carlo results will not have the correct expected
values and the confidence interval statements may not be correct. The
user can guard against this situation by setting up the problem so as
not to exclude any regions of phase space and by trying to sample all
regions of the problem adequately.

Despite one's best effort, an important path may not be sampled often
enough, causing confidence interval statements to be incorrect. To try
to inform the user about this behavior, the MCNP code calculates a
figure of merit ( FOM ) for one tally bin of each tally as a function of
the number of histories and prints the results in the tally fluctuation
charts at the end of the output. The FOM is defined as

<!-- formula-not-decoded -->

where T is the computer time in minutes. The more efficient a Monte
Carlo calculation is, the larger the FOM will be because less computer
time is required to reach a given value of R .

The FOM should be approximately constant as N increases because R 2 is
proportional to 1 /N and T is proportional to N . Always examine the
tally fluctuation charts to be sure that the tally appears well behaved,
as evidenced by a fairly constant FOM . A sharp decrease in the FOM
indicates that a seldom-sampled particle path has significantly affected
the tally result and relative error estimate. In this case, the
confidence intervals may not be correct for the fraction of the time
that statistical theory would indicate. Examine the problem to determine
what path is causing the large scores and try to redefine the problem to
sample that path much more frequently.

After each tally, an analysis is done and additional useful information
is printed about the TFC tally bin result. The nonzero scoring
efficiency, the zero and nonzero score components of the relative error,
the number and magnitude of negative history scores, if any, and the
effect on the result if the largest observed history score in the TFC
were to occur again on the very next history are given. A table just
before the TFCs summarizes the results of these checks for all tallies
in the problem. Ten statistical checks are made and summarized in Table
160 after each tally, with a pass yes/no criterion. The empirical
history score probability density function (PDF) for the TFC bin of each
tally is calculated and displayed in printed plots.

The TFCs at the end of the problem include the variance of the variance
(an estimate of the error of the relative error), and the slope (the
estimated exponent of the PDF large score behavior) as a function of the
number of particles started.

All this information provides the user with statistical information to
aid in forming valid confidence intervals for Monte Carlo results. There
is no GUARANTEE, however. The possibility always exists that some as yet
unsampled portion of the problem may change the confidence interval if
more histories were calculated. Chapter 2 contains more information
about estimation of Monte Carlo precision.

## 1.2.7 Variance Reduction

As noted in the previous section, R (the estimated relative error) is
proportional to 1 / √ N , where N is the number of histories. For a
given MCNP run, the computer time T consumed is proportional to N . Thus
R = C/ √ T , where C is a positive constant. There are two ways to
reduce R : (1) increase T and/or (2) decrease C . Computer budgets often
limit the utility of the first approach. For example, if it has taken 2
hours to obtain R = 0 . 10 , then 200 hours will be required to obtain R
= 0 . 01 . For this reason the MCNP code has special variance reduction
techniques for decreasing C (variance is the square of the standard
deviation). The constant C depends on the tally choice and/or the
sampling choices.

## 1.2.7.1 Tally Choice

As an example of the tally choice, note that the fluence in a cell can
be estimated either by a collision estimate or a track-length estimate.
The collision estimate is obtained by tallying 1 / Σ t ( Σ t is the
macroscopic total cross section) at each collision in the cell and the
track-length estimate is obtained by tallying the distance the particle
moves while inside the cell. Note that as Σ t gets very small, very few
particles collide but give enormous tallies when they do, producing a
high variance situation [§2.6.6]. In contrast, the track-length estimate
gets a tally from every particle that enters the cell. For this reason
the MCNP code has track length tallies as standard tallies, whereas the
collision tally is not standard in the MCNP code, except for estimating
k eff .

## 1.2.7.2 Non-analog Monte Carlo

Explaining how sampling affects C requires understanding of the non-
analog Monte Carlo model.

The simplest Monte Carlo model for particle transport problems is the
analog model that uses the natural probabilities that various events
occur (for example, collision, fission, capture, etc.). Particles are
followed from event to event by a computer, and the next event is always
sampled (using the random number generator) from a number of possible
next events according to the natural event probabilities. This is called
the analog Monte Carlo model because it is directly analogous to the
naturally occurring transport.

The analog Monte Carlo model works well when a significant fraction of
the particles contribute to the tally estimate and can be compared to
detecting a significant fraction of the particles in the physical
situation. There are many cases for which the fraction of particles
detected is very small, less than 10 -6 . For these problems analog
Monte Carlo fails because few, if any, of the particles tally, and the
statistical uncertainty in the answer is unacceptable.

Although the analog Monte Carlo model is the simplest conceptual
probability model, there are other probability models for particle
transport that estimate the same average value as the analog Monte Carlo
model, while often making the variance (uncertainty) of the estimate
much smaller than the variance for the analog estimate. This means that
problems that would be impossible to solve in days of computer time with
analog methods can be solved in minutes of computer time with non-analog
methods.

A non-analog Monte Carlo model attempts to follow 'interesting'
particles more often than 'uninteresting' ones. An 'interesting'
particle is one that contributes a large amount to the quantity (or
quantities) that

needs to be estimated. There are many non-analog techniques, and all are
meant to increase the odds that a particle scores (contributes). To
ensure that the average score is the same in the non-analog model as in
the analog model, the score is modified to remove the effect of biasing
(changing) the natural odds. Thus, if a particle is artificially made q
times as likely to execute a given random walk, then the particle's
score is weighted by (multiplied by) 1 /q . The average score is thus
preserved because the average score is the sum, over all random walks,
of the probability of a random walk multiplied by the score resulting
from that random walk.

A non-analog Monte Carlo technique will have the same expected tallies
as an analog technique if the expected weight executing any given random
walk is preserved. For example, a particle can be split into two
identical pieces and the tallies of each piece are weighted by 1 / 2 of
what the tallies would have been without the split. Such non-analog, or
variance reduction, techniques can often decrease the relative error by
sampling naturally rare events with an unnaturally high frequency and
weighting the tallies appropriately.

## 1.2.7.3 Variance Reduction Tools in the MCNP Code

There are four categories of variance reduction techniques [16] that
range from the trivial to the esoteric.

## 1.2.7.3.1 Truncation Methods

Truncation methods are the simplest of variance reduction methods. They
speed up calculations by truncating parts of phase space that do not
contribute significantly to the solution. The simplest example is
geometry truncation in which unimportant parts of the geometry are
simply not modeled. Specific truncation methods available in the MCNP
code are the energy cutoff and time cutoff.

## 1.2.7.3.2 Population Control Methods

Population control methods use particle splitting and Russian roulette
to control the number of samples taken in various regions of phase
space. In important regions many samples of low weight are tracked,
while in unimportant regions few samples of high weight are tracked. A
weight adjustment is made to ensure that the problem solution remains
unbiased. Specific population control methods available in the MCNP code
are geometry splitting and Russian roulette, energy splitting/ roulette,
time splitting/roulette, weight cutoff, and weight windows.

## 1.2.7.3.3 Modified Sampling Methods

Modified sampling methods alter the statistical sampling of a problem to
increase the number of tallies per particle. For any Monte Carlo event
it is possible to sample from any arbitrary distribution rather than the
physical probability as long as the particle weights are then adjusted
to compensate. Thus, with modified sampling methods, sampling is done
from distributions that send particles in desired directions or into
other desired regions of phase space such as time or energy, or change
the location or type of collisions. Modified sampling methods in the
MCNP code include the exponential transform, implicit capture, forced
collisions, source biasing, and neutron-induced photon production
biasing.

## 1.2.7.3.4 Partially Deterministic Methods

Partially deterministic methods are the most complicated class of
variance reduction methods. They circumvent the normal random walk
process by using deterministic-like techniques, such as next-event
estimators, or by controlling the random number sequence. In the MCNP
code these methods include point detectors, DXTRAN, and correlated
sampling.

Variance reduction techniques, used correctly, can greatly help the user
produce a more efficient calculation. Used poorly, they can result in a
wrong answer with good statistics and few clues that anything is amiss.
Some variance reduction methods have general application and are not
easily misused. Others are more specialized and attempts to use them
carry high risk. The use of weight windows tends to be more powerful
than the use of importances but typically requires more input data and
more insight into the problem. The exponential transform for thick
shields is not recommended for the inexperienced user; rather, use many
cells with increasing importances (or decreasing weight windows) through
the shield. Forced collisions are used to increase the frequency of
random walk collisions within optically thin cells but should be used
only by an experienced user. The point detector estimator should be used
with caution, as should DXTRAN.

For many problems, variance reduction is not just a way to speed up the
problem but is necessary to get any answer at all. Deep penetration
problems and pipe detector problems, for example, will run too slowly by
factors of trillions without adequate variance reduction. Consequently,
users have to become skilled in using the variance reduction techniques
in the MCNP code.

The following summarizes briefly the main MCNP variance reduction
techniques. Detailed discussion is in §2.7.

1. Energy cutoff: Particles whose energy is out of the range of interest are terminated so that computation time is not spent following them.
2. Time cutoff: Like the energy cutoff but based on time.
3. Geometry splitting with Russian roulette: Particles transported from a region of higher importance to a region of lower importance (where they will probably contribute little to the desired problem result) undergo Russian roulette; that is, some of those particles will be killed a certain fraction of the time, but survivors will be counted more by increasing their weight the remaining fraction of the time. In this way, unimportant particles are followed less often, yet the problem solution remains undistorted. On the other hand, if a particle is transported to a region of higher importance (where it will likely contribute to the desired problem result), it may be split into two or more particles (or tracks), each with less weight and therefore counting less. In this way, important particles are followed more often, yet the solution is undistorted because, on average, total weight is conserved.
4. Energy splitting/Russian roulette: Particles can be split or rouletted upon entering various user-supplied energy ranges. Thus important energy ranges can be sampled more frequently by splitting the weight among several particles and less important energy ranges can be sampled less frequently by rouletting particles.
5. Time splitting/Russian roulette: Like energy splitting/roulette, but based on time.
6. Weight cutoff/Russian roulette: If a particle weight becomes so low that the particle becomes insignificant, it undergoes Russian roulette. Most particles are killed, and some particles survive with increased weight. The solution is unbiased because total weight is conserved, but computer time is not wasted on insignificant particles.
7. Weight window: As a function of energy, geometric location, or both, low-weighted particles are eliminated by Russian roulette and high-weighted particles are split. This technique helps keep the weight dispersion within reasonable bounds throughout the problem. An importance generator is available that estimates the optimal limits for a weight window.

8. Exponential transformation: To transport particles long distances, the distance between collisions in a preferred direction is artificially increased and the weight is correspondingly artificially decreased. Because large weight fluctuations often result, it is highly recommended that the weight window be used with the exponential transform.
9. Implicit absorption: When a particle collides, there is a probability that it is absorbed by the nucleus. In analog absorption, the particle is killed with that probability. In implicit absorption, also known as implicit capture or survival biasing, the particle is never killed by absorption; instead, its weight is reduced by the absorption probability at each collision. Important particles are permitted to survive by not being lost to absorption. On the other hand, if particles are no longer considered useful after undergoing a few collisions, analog absorption efficiently gets rid of them.
10. Forced collisions: A particle can be forced to undergo a collision each time it enters a designated cell that is almost transparent to it. The particle and its weight are appropriately split into two parts, collided and uncollided. Forced collisions are often used to generate contributions to point detectors, ring detectors, and/or DXTRAN spheres.
11. Source variable biasing: Source particles with phase-space variables of more importance are emitted with a higher frequency but with a compensating lower weight than are less important source particles.
12. Point and ring detectors: When the user wishes to tally a flux-related quantity at a point in space, the probability of transporting a particle precisely to that point is vanishingly small. Therefore, pseudoparticles are directed to the point instead. Every time a particle history is born in the source or undergoes a collision, the user may require that a pseudoparticle be tallied at a specified point in space. In this way, many pseudoparticles of low weight reach the detector, which is the point of interest, even though no particle histories could ever reach the detector. For problems with rotational symmetry, the point may be represented by a ring to enhance the efficiency of the calculation.
13. DXTRAN: DXTRAN, which stands for deterministic transport, improves sampling in the vicinity of detectors or other tallies. It involves deterministically transporting particles on collision to some arbitrary, user-defined sphere in the neighborhood of a tally and then calculating contributions to the tally from these particles. Contributions to the detectors or to the DXTRAN spheres can be controlled as a function of a geometric cell or as a function of the relative magnitude of the contribution to the detector or DXTRAN sphere. The DXTRAN method is a way of obtaining large numbers of particles on user-specified 'DXTRAN spheres.' DXTRAN makes it possible to obtain many particles in a small region of interest that would otherwise be difficult to sample. Upon sampling a collision or source density function, DXTRAN estimates the correct weight fraction that should scatter toward, and arrive without collision at, the surface of the sphere. The DXTRAN method then puts this correct weight on the sphere. The source or collision event is sampled in the usual manner, except that the particle is killed if it tries to enter the sphere because all particles entering the sphere have already been accounted for deterministically.
14. Correlated sampling: The sequence of random numbers in the Monte Carlo process is chosen so that statistical fluctuations in the problem solution will not mask small variations in that solution resulting from slight changes in the problem specification. The i th history will always start at the same point in the random number sequence no matter what the previous i -1 particles did in their random walks.

Note: weight cutoff/Russian roulette and implicit absorption are the
only two variance reduction techniques enabled by default in an MCNP
calculation.

## 1.3 MCNP Geometry

We will present here only basic introductory information about geometry
setup, surface specification, and cell and surface card inputs. Areas of
further interest would be the complement operator, use of parentheses,
and

Figure 1.2: Right-handed Cartesian coordinate system.

<!-- image -->

repeated structure and lattice definitions, found in Chapter 2. Chapter
10 contains geometry examples and is recommended as a next step. Chapter
5 has detailed information about the format and entries on cell, surface
(including macrobody), and data cards.

The geometry of the MCNP code treats an arbitrary three-dimensional
configuration of user-defined materials in geometric cells bounded by
first- and second-degree surfaces and fourth-degree elliptical tori. The
cells are defined by the intersections, unions, and complements of the
regions bounded by the surfaces. Surfaces are defined by supplying
coefficients to the analytic surface equations or, for certain types of
surfaces, known points on the surfaces. The MCNP code also provides a
'macrobody' capability, where basic shapes such as spheres, boxes,
cylinders, etc., may be combined using Boolean operators. This
capability is essentially the same as the combinatorial geometry
provided by other codes such as MORSE, KENO, and VIM.

The MCNP code has a more general geometry than is available in most
combinatorial geometry codes. In addition to the capability of combining
several predefined geometric bodies, as in a combinatorial geometry
scheme, the MCNP code gives the user the added flexibility of defining
geometric regions from all the first and second degree surfaces of
analytical geometry and elliptical tori and then of combining them with
Boolean operators. The code does extensive internal checking to find
input errors. In addition, the geometry-plotting capability in the MCNP
code helps the user check for geometry errors.

The MCNP code treats geometric cells in a Cartesian coordinate system.
The surface equations recognized by the MCNP code are listed in Table
5.1. The particular Cartesian coordinate system used is arbitrary and
user defined, but the right-handed system shown in Figure 1.2 is usually
chosen.

Using the bounding surfaces specified on cell cards, the MCNP code
tracks particles through the geometry, calculates the intersection of a
track's trajectory with each bounding surface, and finds the minimum
positive distance to an intersection. If the distance to the next
collision is greater than this minimum distance and there are no DXTRAN
spheres along the track, the particle leaves the current cell. At the
appropriate surface intersection, the MCNP code finds the correct cell
that the particle will enter by checking the sense of the intersection
point for each surface listed for the cell. When a complete match is
found, the MCNP code has found the correct cell on the other side and
the transport continues.

## 1.3.1 Cells

When cells are defined, an important concept is that of the sense of all
points in a cell with respect to a bounding surface. Suppose that s = f
( x, y, z ) = 0 is the equation of a surface in the problem. For any set
of points ( x, y, z ) , if s = 0 the points are on the surface. However,
for points not on the surface, if s &lt; 0 , the points are said to have a
negative sense with respect to that surface and, conversely, a positive
sense if s &gt; 0 . For example, a point at x = 3 has a positive sense with
respect to the plane x -2 = 0 . That is, the equation x -D = 3 -2 = s =
1 is positive for x = 3 (where D is a constant).

Cells are defined on cell cards. Each cell is described by a cell
number, material number, and material density followed by a list of
operators and signed surfaces that bound the cell. If the sense is
positive, the sign can be omitted. The material number and material
density can be replaced by a single zero to indicate a void cell. The
cell number must begin in columns 1-5. The remaining entries follow,
separated by blanks. A complete description of the cell card format can
be found in §5.2. Each surface divides all space into two regions, one

1

2

```
1 0 1 -2 -3 6 2 0 1 -6 -4 5
```

Figure 1.3: Complicated versus simple cell example.

<!-- image -->

with positive sense with respect to the surface and the other with
negative sense. The geometry description defines the cell to be the
intersection, union, and/or complement of the listed regions.

The subdivision of the physical space into cells is not necessarily
governed only by the different material regions, but may be affected by
problems of sampling and variance reduction techniques (such as
splitting and Russian roulette), the need to specify an unambiguous
geometry, and the tally requirements. The tally segmentation feature may
eliminate most of the tally requirements.

Be cautious about making any one cell very complicated. With the union
operator and disjointed regions, a very large geometry can be set up
with just one cell. The problem is that for each track flight between
collisions in a cell, the intersection of the track with each bounding
surface of the cell is calculated, a calculation that can be costly if a
cell has many surfaces. As an example, consider Figure 1.3a. It is just
a lot of parallel cylinders and is easy to set up. However, the cell
containing all the little cylinders is bounded by twelve surfaces
(counting a top and bottom). A much more efficient geometry is seen in
Figure 1.3b, where the large cell has been broken up into a number of
smaller cells.

## 1.3.1.1 Cells Defined by Intersections of Regions of Space

The intersection operator in the MCNP code is implicit; it is simply the
blank space between two surface numbers on the cell card.

If a cell is specified using only intersections, all points in the cell
must have the same sense with respect to a given bounding surface. This
means that, for each bounding surface of a cell, all points in the cell
must remain on only one side of any particular surface. Thus, there can
be no concave corners in a cell specified only by intersections. Figure
1.4, a cell formed by the intersection of five surfaces (ignore surface
6 for the time being), illustrates the problem of concave corners by
allowing a particle (or point) to be on two sides of a surface in one
cell. Surfaces 3 and 4 form a concave corner in the cell such that
points p 1 and p 2 are on the same side of surface 4 (that is, have the
same sense with respect to 4) but point p 3 is on the other side of
surface 4 (opposite sense). Points p 2 and p 3 have the same sense with
respect to surface 3, but p 1 has the opposite sense. One way to remedy
this dilemma (and there are others) is to add surface 6 between the 3/4
corner and surface 1 to divide the original cell into two cells.

With surface 6 added to Figure 1.4, the cell to the right of surface 6
is number 1 (cells indicated by circled numbers); to the left number 2;
and the outside cell number 3. The cell cards (in two dimensions, all
cells void) are given in Listing 1.1.

Listing 1.1: Example cell definitions.

<!-- image -->

1

Figure 1.4: Geometry example, A.

<!-- image -->

Figure 1.5: Cells from unions and intersections.

Cell 1 is a void and is formed by the intersection of the region above
(positive sense) surface 1 with the region to the left (negative sense)
of surface 2, intersected with the region below (negative sense) surface
3, and finally intersected with the region to the right (positive sense)
of surface 6. Cell 2 is described similarly.

Cell 3 cannot be specified with the intersection operator. The following
section about the union operator is needed to describe cell 3.

## 1.3.1.2 Cells Defined by Unions of Regions of Space

The union operator, signified by a colon on the cell cards, allows
concave corners in cells and also cells that are completely disjoint.
The intersection and union operators are binary Boolean operators, so
their use follows Boolean algebra methodology; unions and intersections
can be used in combination in any cell description.

Spaces on either side of the union operator are irrelevant, but remember
that a space without the colon signifies an intersection. In the
hierarchy of operations, intersections are performed first and then
unions. There is no left to right ordering. Parentheses can be used to
clarify operations and in some cases are required to force a certain
order of operations. Innermost parentheses are cleared first. Spaces are
optional on either side of a parenthesis. A parenthesis is equivalent to
a space and signifies an intersection.

For example, let A and B be two regions of space. The region containing
points that belong to both A and B is called the intersection of A and
B. The region containing points that belong to A alone or to B alone or
to both A and B is called the union of A and B. The shaded area in
Figure 1.5a represents the union of A and B (or A : B), and the shaded
area in Figure 1.5b represents the intersection of A and B (or A B). The
only way regions of space can be added is with the union operator. An
intersection of two spaces always results in a region no larger than
either of the two spaces. Conversely, the union of two spaces always
results in a region no smaller than either of the two spaces.

A simple example will further illustrate the concept of Figure 1.5 and
the union operator to solidify the concept of adding and intersecting
regions of space to define a cell. See also the second example in
§10.1.1.2. In Figure 1.6 we have two infinite planes that meet to form
two cells. Cell 1 is easy to define; it is everything in the universe to
the right of surface 1 (that is, a positive sense) that is also in
common with (or intersected

Figure 1.6: More complicated cells from unions and intersections.

<!-- image -->

with) everything in the universe below surface 2 (that is, a negative
sense). Therefore, the surface relation of cell 1 is 1 -2.

Cell 2 is everything in the universe to the left (negative sense) of
surface 1 plus everything in the universe above (positive sense) surface
2, or -1 : 2, illustrated in Figure 1.6b by all the shaded regions of
space. If cell 2 were specified as -1 2, that would represent the region
of space common to -1 and 2, which is only the cross-hatched region in
the figure and is obviously an improper specification for cell 2.

Returning to Figure 1.4, if cell 1 is inside the solid black line and
cell 2 is the entire region outside the solid line, then the MCNP cell
cards in two dimensions are (assuming both cells are voids) given in
Listing 1.2.

```
1 1 0 1 -2 (-3 : -4) 5 2 2 0 -5 : -1 : 2 : 3 4
```

Listing 1.2: Example cell definitions with intersections.

Cell 1 is defined as the region above surface 1 intersected with the
region to the left of surface 2, intersected with the union of regions
below surfaces 3 and 4, and finally intersected with the region to the
right of surface 5. Cell 2 contains four concave corners (all except
between surfaces 3 and 4), and its specification is just the converse
(or complement) of cell 1. Cell 2 is the space defined by the region to
the left of surface 5 plus the region below 1 plus the region to the
right of 2 plus the space defined by the intersections of the regions
above surfaces 3 and 4.

A simple consistency check can be noted with the two cell cards in
Listing 1.2. All intersections for cell 1 become unions for cell 2 and
vice versa. The senses are also reversed.

Note that in this example, all corners less than 180 degrees in a cell
are handled by intersections, and all corners greater than 180 degrees
are handled by unions.

To illustrate some of the concepts about parentheses, assume an
intersection is thought of mathematically as multiplication and a union
is thought of mathematically as addition. Parentheses are removed first,
with multiplication being performed before addition. The cell cards for
the example cards from Figure 1.4 may be written as shown in Listing
1.3.

```
1 1 a · b · ( c + d ) · e 2 2 e + a + b + c · d
```

Note that parentheses are required for the first cell but not for the
second, although the second could have been written as e + a + b +( c ·
d ) , ( e + a + b ) + ( c · d ) , ( e ) + ( a ) + ( b ) + ( c · d ) ,
etc.

Several more examples using the union operator are given in §10.1.1.
Study them to get a better understanding of this powerful operator that
can greatly simplify geometry setups.

## 1.3.2 Surface Type Specification

The first- and second-degree surfaces plus the fourth-degree elliptical
and degenerate tori of analytical geometry are all available in the MCNP
code. The surfaces are designated by mnemonics such as C/Z for a
cylinder parallel to the z-axis. A cylinder at an arbitrary orientation
is designated by the general quadratic (GQ) mnemonic. A paraboloid
parallel to a coordinate axis is designated by the special quadratic
(SQ) mnemonic. The 29 mnemonics representing various types of surfaces
are listed in Table 5.1.

## 1.3.3 Surface Parameter Specification

There are two ways to specify surface parameters in the MCNP code: (1)
by supplying the appropriate coefficients needed to satisfy the surface
equation, and (2) by specifying known geometric points on a surface that
is rotationally symmetric about a coordinate axis.

## 1.3.3.1 Coefficients for the Surface Equations

The first way to define a surface is to use one of the surface-type
mnemonics from Table 5.1 and to calculate the appropriate coefficients
needed to satisfy the surface equation.

For example, a sphere of radius 3.62 cm with the center located at the
point (4 , 1 , -3) is specified by

S 4 1 -3 3.62

An ellipsoid whose axes are not parallel to the coordinate axes is
defined by the GQ mnemonic plus up to 10 coefficients of the general
quadratic equation. Calculating the coefficients can be (and frequently
is) nontrivial, but the task is greatly simplified by defining an
auxiliary coordinate system whose axes coincide with the axes of the
ellipsoid. The ellipsoid is easily defined in terms of the auxiliary
coordinate system, and the relationship between the auxiliary coordinate
system and the main coordinate system is specified on a TR n card,
described in §5.5.3.

The use of the SQ and GQ surfaces is determined by the orientation of
the axes. One should always use the simplest possible surface in
describing geometries; for example, using a GQ surface instead of an S
to specify a sphere will require more computational effort for the MCNP
code.

1

Listing 1.3: Example cell definitions mathematical rendition.

## 1.3.3.2 Points that Define a Surface

The second way to define a surface is to supply known points on the
surface. This method is convenient if you are setting up a geometry from
something like a blueprint where you know the coordinates of
intersections of surfaces or points on the surfaces. When three or more
surfaces intersect at a point, this second method also produces a more
nearly perfect point of intersection if the common point is used in the
surface specification. It is frequently difficult to get complicated
surfaces to meet at one point if the surfaces are specified by the
equation coefficients. Failure to achieve such a meeting can result in
the unwanted loss of particles.

There are, however, restrictions that must be observed when specifying
surfaces by points that do not exist when specifying surfaces by
coefficients. Surfaces described by points must be either skew planes or
surfaces rotationally symmetric about the x , y , or z axes. They must
be unique, real, and continuous. For example, points specified on both
sheets of a hyperboloid are not allowed because the surface is not
continuous. However, it is valid to specify points that are all on one
sheet of the hyperboloid. See the X , Y , Z , and P input card
descriptions in §5.3.2 for additional explanation.
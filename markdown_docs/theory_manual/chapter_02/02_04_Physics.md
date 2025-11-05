---
title: "Chapter 2.4 - Physics"
chapter: "2.4"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/2_Geometry,_Data,_Physics,_and_Mathematics/2.4_Physics.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

sections are unavailable; and (6) charged particle transport using the
Boltzmann-Fokker-Planck algorithm in which charged particles masquerade
as neutrons.

Multigroup cross sections are very problem dependent. Some multigroup
libraries are available from the Transport Methods Group at Los Alamos
but must be used with caution. Users are encouraged to generate or get
their own multigroup libraries and then use the supplementary code CRSRD
[59] to convert them to the MCNP code format. Reference [59] describes
the conversion procedure. This report also describes how to use both the
multigroup and adjoint methods in the MCNP code and presents several
benchmark calculations demonstrating the validity and effectiveness of
the multigroup/adjoint method.

To generate cross-section tables for electron/photon transport problems
that will use the multigroup BoltzmannFokker-Planck algorithm [60], the
CEPXS [61-63] code developed by Sandia National Laboratory and available
from RSICC can be used. The CEPXS manuals describe the algorithms and
physics database upon which the code is based; the physics package is
essentially the same as ITS version 2.1. The keyword 'MONTE-CARLO' is
needed in the CEPXS input file to generate a cross-section library
suitable for input into CRSRD; this undocumented feature of the CEPXS
code should be approached with caution.

## 2.4 Physics

The physics of neutron, photon, and electron interactions is the very
essence of the MCNP code. A review of charged particle transport
capabilities in the MCNP code can be found in [42]. For a description of
all high-energy event generators used by the MCNP code, see [64]. This
section may be considered a software requirements document in that it
describes the equations the MCNP code is intended to solve. All the
sampling schemes essential to the random walk are presented or
referenced. But first, particle weight and particle tracks, two concepts
that are important for setting up the input and for understanding the
output, are discussed in the following sections.

## 2.4.1 Statistical Weight

At the most fundamental level, weight is a tally multiplier. That is,
the tally contribution for a weight w is the unit weight tally
contribution multiplied by w . Weight is an adjustment for deviating
from a direct physical simulation of the transport process. Note that if
a Monte Carlo code always sampled from the same distributions as nature
does, then the Monte Carlo code would have the same mean and variance as
seen in nature. Quite often, the natural variance is unacceptably high
and the Monte Carlo code modifies the sampling using some form of
'variance reduction' [§2.7]. The variance reduction methods use
weighting schemes to produce the same mean as the natural transport
process, but with lower calculational variance than the natural variance
of the transport process.

With the exception of the pulse height tally ( F8 ), all tallies in the
MCNP code are made by individual particles. In this case, weight is
assigned to the individual particles as a 'particle weight.' The manual
discusses the 'particle weight' cases first and afterward discusses the
weight associated with the F8 tally.

## 2.4.1.1 Particle Weight

If the MCNP code were used only to simulate exactly physical transport,
then each MCNP particle would represent one physical particle and would
have unit weight. However, for computational efficiency, the MCNP code
allows many techniques that do not exactly simulate physical transport.
For instance, each MCNP particle might represent a number w of particles
emitted from a source. This number w is the initial weight of the MCNP
particle. The w physical particles all would have different random
walks, but the one MCNP

particle representing these w physical particles will only have one
random walk. Clearly this is not an exact simulation; however, the true
number of physical particles is preserved in the MCNP code in the sense
of statistical averages and therefore in the limit of a large number of
MCNP source particles (of course including particle production or loss
if they occur). Each MCNP particle result is multiplied by the weight so
that the full results of the w physical particles represented by each
MCNP particle are exhibited in the final results (tallies). This
procedure allows users to normalize their calculations to whatever
source strength they desire. The default normalization is a weight of
one per MCNP source particle. A second normalization to the number of
Monte Carlo histories is made in the results so that the expected means
will be independent of the number of source particles actually initiated
in the MCNP calculation.

The utility of particle weight, however, goes far beyond simply
normalizing the source. Every Monte Carlo biasing technique alters the
probabilities of random walks executed by the particles. The purpose of
such biasing techniques is to increase the number of particles that
sample some part of the problem of special interest (1) without
increasing (and sometimes actually decreasing) the sampling of less
interesting parts of the problem, and (2) without erroneously affecting
the expected mean physical result (tally). This procedure, properly
applied, increases precision in the desired result compared to an
unbiased calculation taking the same computing time. For example, if an
event is made √ 2 times as likely to occur (as it would occur without
biasing), the tally ought to be multiplied by 1 / √ 2 so that the
expected average tally is unaffected. This tally multiplication can be
accomplished by multiplying the particle weight by 1 / √ 2 because the
tally contribution by a particle is always multiplied by the particle
weight in the MCNP code. Note that weights need not be integers.

In short, particle weight is a number carried along with each MCNP
particle, representing that particle's relative contribution to the
final tallies. Its magnitude is determined to ensure that whenever the
MCNP code deviates from an exact simulation of the physics, the expected
physical result nonetheless is preserved in the sense of statistical
averages, and therefore in the limit of large MCNP particle numbers. Its
utility is in the manipulation of the number of particles, sampling just
a part of the problem to achieve the same results and precision,
obviating a full unbiased calculation which has a longer computing time.

## 2.4.1.2 Pulse-height Tally ( F8 ) Weight

Unlike other tallies in the MCNP code, the pulse height tally depends on
a collection of particles instead of just individual particles. Because
of this, a weight is assigned to each collection of tallying particles.
It is this 'collective weight' that multiplies the F8 tally, not the
particle weight.

When variance reduction is used, a 'collective weight' is assigned to
every collection of particles. If variance reduction techniques have
made a collection's random walk q times as likely as without variance
reduction, then the collective weight is multiplied by 1 /q so that the
expected F8 tally of the collection is preserved. The interested reader
should consult [65, 66] for more details.

## 2.4.2 Particle Tracks

When a particle starts out from a source, a particle track is created.
If that track is split 2 for 1 at a splitting surface or collision, a
second track is created and there are now two tracks from the original
source particle, each with half the single track weight. If one of the
tracks has an (n,2n) reaction, one more track is started for a total of
three. A track refers to each component of a source particle during its
history. Track length tallies use the length of a track in a given cell
to determine a quantity of interest, such as fluence, flux, or energy
deposition. Tracks crossing surfaces are used to calculate fluence,
flux, or pulse-height energy deposition (surface estimators). Tracks
undergoing collisions are used to calculate multiplication and
criticality (collision estimators).

Within a given cell of fixed composition, the method of sampling a
collision along the track is determined using the following theory. The
probability of a first collision for a particle between l and l +d l
along its line of flight is given by where Σ t is the macroscopic total
cross section of the medium and is interpreted as the probability per
unit length of a collision. Setting ξ the random number on [0 , 1) , to
be

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

it follows that

However, because 1 -ξ is distributed in the same manner as ξ and hence
may be replaced by ξ , we obtain the well-known expression for the
distance to collision,

<!-- formula-not-decoded -->

## 2.4.3 Neutron Interactions

When a particle (representing any number of neutrons, depending upon the
particle weight) collides with a nucleus, the following sequence occurs:

1. the collision nuclide is identified;
2. either the S ( α, β ) treatment is used or the velocity of the target nucleus is sampled for low-energy neutrons;
3. photons are optionally generated for later transport;
4. neutron capture (that is, neutron disappearance by any process) is modeled;
5. if the energy of the neutron is low enough and an appropriate S ( α, β ) table is present, the collision is modeled by the S ( α, β ) treatment;
6. otherwise, either elastic scattering or an inelastic reaction (including fission) is selected, and the new energy and direction of the outgoing track(s) are determined.

## 2.4.3.1 Selection of Collision Nuclide

If there are n different nuclides forming the material in which the
collision occurred, and if ξ is a random number on the unit interval [0
, 1) , then the k th nuclide is chosen as the collision nuclide if

<!-- formula-not-decoded -->

where Σ t ,i is the macroscopic total cross section of nuclide i . If
the energy of the neutron is low enough (below about 4 eV) and the
appropriate S ( α, β ) table is present, the total cross section is the
sum of the capture cross section from the regular cross-section table
and the elastic and inelastic scattering cross sections from the S ( α,
β ) table. Otherwise, the total cross section is taken from the regular
cross-section table and is adjusted for thermal effects [§2.4.3.2].

## 2.4.3.2 Free Gas Thermal Treatment

A collision between a neutron and an atom is affected by the thermal
motion of the atom, and in most cases, the collision is also affected by
the presence of other atoms nearby. The thermal motion cannot be ignored
in many applications of the MCNP code without serious error. The effects
of nearby atoms are also important in some applications. The MCNP code
uses a thermal treatment based on the free gas approximation to account
for the thermal motion. It also has an explicit S ( α, β ) capability
that takes into account the effects of chemical binding and crystal
structure for incident neutron energies below about 4 eV, but is
available for only a limited number of substances and temperatures. The
S ( α, β ) capability is described in §2.4.3.6.

The free gas thermal treatment in the MCNP code assumes that the medium
is a free gas and also that, in the range of atomic weight and neutron
energy where thermal effects are significant, the elastic scattering
cross section at zero temperature is nearly independent of the energy of
the neutron and that the reaction cross sections are nearly independent
of temperature. These assumptions allow the MCNP code to have a thermal
treatment of neutron collisions that runs almost as fast as a completely
non-thermal treatment and that is adequate for most practical problems.

With the above assumptions, the free gas thermal treatment consists of
adjusting the elastic cross section and taking into account the velocity
of the target nucleus when the kinematics of a collision are being
calculated. The MCNP free gas thermal treatment effectively applies to
elastic scattering only.

Cross-section libraries processed by NJOY already include Doppler
broadening of elastic, capture, fission, and other low-threshold
absorption cross-sections ( &lt; 1 eV). Inelastic cross sections are never
broadened by NJOY.

## 2.4.3.2.1 Adjusting the Elastic Cross Section

The first aspect of the free gas thermal treatment is to adjust the
zero-temperature elastic cross section by raising it by the factor where
a = √ AE/kT , A is the atomic weight of the nucleus, E is the incident
neutron energy, and T is the material temperature. For speed, F is
approximated by F = 1+0 . 5 /a 2 when a ≥ 2 and by linear interpolation
in a table of 51 values of aF when a &lt; 2 . Both approximations have
relative errors less than 0.0001. The total cross section also is
increased by the amount of the increase in the elastic cross section.

<!-- formula-not-decoded -->

The adjustment to the elastic and total cross sections is done partly in
the setup of a problem and partly during the actual transport
calculation. No adjustment is made if the elastic cross section in the
data library was already processed to the temperature that is needed in
the problem. If all of the cells that contain a particular nuclide have
the same temperature, which is constant in time, that is different from
the temperature of the library, the elastic and total cross sections for
that nuclide are adjusted to that temperature during the setup so that
the transport will run a little faster. Otherwise, these cross sections
are reduced, if necessary, to zero temperature during the setup and the
thermal adjustment is made when the cross sections are used. For speed,
the thermal adjustment is omitted if the neutron energy is greater than
500 kT/A . At that energy the adjustment of the elastic cross section
would be less than 0.1%.

Note that this adjustment of the nuclear data is less accurate than the
one used within NJOY, as NJOY will handle more reactions and does not
assume constant data. As such, it is recommended to use datasets
Doppler-broadened to the temperature of interest, rather than relying on
this adjustment. See the discussion in the TMP card for more
information.

## 2.4.3.2.2 Sampling the Velocity of the Target Nucleus

The second aspect of the free gas thermal treatment takes into account
the velocity of the target nucleus when the kinematics of a collision
are being calculated. The target velocity is sampled and subtracted from
the velocity of the neutron to get the relative velocity. The collision
is sampled in the target-at-rest frame and the outgoing velocities are
transformed to the laboratory frame by adding the target velocity.

There are different schools of thought as to whether the relative energy
between the neutron and target, E r , or the laboratory frame incident
neutron energy (target-at-rest), E o , should be used for all the
kinematics of the collision. E o is used in the MCNP code to obtain the
distance-to-collision, select the collision nuclide, determine energy
cutoffs, generate photons, generate fission sites for the next
generation of a KCODE criticality problem, for S ( α, β ) scattering,
and for capture. E r is used for everything else in the collision
process, namely elastic and inelastic scattering, including fission and
( n , x n ) reactions. It is shown in Eq. (2.8) that E r is based upon v
rel . that is based upon the elastic scattering cross section, and,
therefore, E r is truly valid only for elastic scatter. However, the
only significant thermal reactions for stable isotopes are absorption,
elastic scattering, and fission. 181 Ta has a 6 keV threshold inelastic
reaction; all other stable isotopes have higher inelastic thresholds.
Metastable nuclides like 242m Am have inelastic reactions all the way
down to zero, but these inelastic reaction cross sections are neither
constant nor 1 /v cross sections and these nuclides are generally too
massive to be affected by the thermal treatment anyway. Furthermore,
fission is very insensitive to incident neutron energy at low energies.
The fission secondary energy and angle distributions are nearly flat or
constant for incident energies below about 500 keV. Therefore, it makes
no significant difference if E r is used only for elastic scatter or for
other inelastic collisions as well. At thermal energies, whether E r or
E o is used only makes a difference for elastic scattering.

If the energy of the neutron is greater than 400 kT and the target is
not 1 H, the velocity of the target is set to zero. Otherwise, the
target velocity is sampled as follows. The free-gas kernel is a thermal
interaction model that results in a good approximation to the thermal
flux spectrum in a variety of applications and can be sampled without
tables. The effective scattering cross section in the laboratory system
for a neutron of kinetic energy E is

<!-- formula-not-decoded -->

Here, v rel . is the relative velocity between a neutron moving with a
scalar velocity v n and a target nucleus moving with a scalar velocity V
, and µ t is the cosine of the angle between the neutron and the target
direction-of-flight vectors. The equation for v rel . is

<!-- formula-not-decoded -->

The scattering cross section at the relative velocity is denoted by σ s
( v rel . ) , and p ( V ) is the probability density function for the
Maxwellian distribution of target velocities, with β defined as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where A is the mass of a target nucleus in units of the neutron mass, M
n is the neutron mass in MeV-sh 2 /cm 2 , and kT is the equilibrium
temperature of the target nuclei in MeV.

The most probable scalar velocity V of the target nuclei is 1 /β , which
corresponds to a kinetic energy of kT for the target nuclei. This is not
the average kinetic energy of the nuclei, which is 3 kT/ 2 . The
quantity that the MCNP code expects on the TMPn input card is kT and not
just T [§5.7.5]. Note that kT is not a function of the particle mass and
is therefore the kinetic energy at the most probable velocity for
particles of any mass.

Equation (2.8) implies that the probability distribution for a target
velocity V and cosine µ t is

<!-- formula-not-decoded -->

It is assumed that the variation of σ s ( v ) with target velocity can
be ignored. The justification for this approximation is that (1) for
light nuclei, σ s ( v rel . ) is slowly varying with velocity, and (2)
for heavy nuclei, where σ s ( v rel . ) can vary rapidly, the moderating
effect of scattering is small so that the consequences of the
approximation will be negligible. As a result of the approximation, the
probability distribution actually used is

Note that the above expression can be written as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

As a consequence, the following algorithm is used to sample the target
velocity.

1. With probability α = 1 / (1 + ( √ πβv n / 2)) , the target velocity V is sampled from the distribution

<!-- formula-not-decoded -->

The transformation V = √ y/β reduces this distribution to the sampling
distribution P ( y ) = y exp( -y ) . The MCNP code actually codes 1 -α .

2. With probability 1 -α , the target velocity is sampled from the distribution

Substituting V = y/β reduces the distribution to the sampling
distribution for y to

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

3. The cosine of the angle between the neutron velocity and the target velocity is sampled uniformly on the interval 1 ≤ µ t ≤ 1 .
4. The rejection function R ( V, µ t ) is computed using

<!-- formula-not-decoded -->

With probability R ( V, µ t ) , the sampling is accepted; otherwise, the
sampling is rejected and the procedure is repeated. The minimum
efficiency of this rejection algorithm corresponding to assuming V = v n
= v rel . averaged over µ t is

<!-- formula-not-decoded -->

which approaches 100% as either the incident neutron energy approaches
zero or becomes much larger than kT .

For more accuracy, the probability distribution in Equation 2.12 can be
directly sampled without the constant cross-section approximation. This
is enabled through the DBRC card. This is not enabled by default.

## 2.4.3.3 Optional Generation of Photons

Photons are generated if the problem is a combined neutron/photon run
and if the collision nuclide has a nonzero photon production cross
section. The number of photons produced is a function of neutron weight,
neutron source weight, photon weight limits (entries on the PWT card),
photon production cross section, neutron total cross section, cell
importance, and the importance of the neutron source cell. No more than
10 photons may be born from any neutron collision. In a KCODE
calculation, secondary photon production from neutrons is turned off
during the inactive cycles.

Because of the many low-weight photons typically created by neutron
collisions, Russian roulette is played for particles with weight below
the bounds specified on the PWT card, resulting in fewer particles, each
having a larger weight. The created photon weight before Russian
roulette is

<!-- formula-not-decoded -->

where

W p is the photon weight,

W n is the neutron weight,

σ γ is the photon production cross section, and

σ t is the total neutron cross section.

Both σ γ and σ t are evaluated at the incoming neutron energy without
the effects of the thermal free gas treatment because nonelastic cross
sections are assumed independent of temperature.

The Russian roulette game is played according to neutron cell
importances for the collision and source cell. For a photon produced in
cell i where the minimum weight set on the PWT card is W min . i , let I
i be the neutron importance in cell i and let I s be the neutron
importance in the source cell. If W p &gt; W min . i I s /I i , one or more
photons will be produced. The number of photons created is N p , where

<!-- formula-not-decoded -->

Each photon is stored in the bank with weight W p /N p . If W p &lt; W min
. i I s /I i , Russian roulette is played and the photon survives with
probability W p I i / ( W min . i I s ) and is given the weight W min .
i I s /I i .

If weight windows are not used and if the weight of the starting
neutrons is not unity, setting all the W min . i on the PWT card to
negative values will make the photon minimum weight relative to the
neutron source weight. This will make the number of photons being
created roughly proportional to the biased collision rate of neutrons.
It is recommended for most applications that negative numbers be used
and be chosen to produce from one to four photons per source neutron.
The default values for W min . i on the PWT card are -1 , which should
be adequate for most problems using cell importances.

If energy-independent weight windows are used, the entries on the PWT
card should be the same as on the WWN1 : p card. If energy-dependent
photon weight windows are used, the entries on the PWT card should be
the minimum WWN n : p entry for each cell, where n refers to the photon
weight window energy group. This will cause most photons to be born
within the weight window bounds.

Any photons generated at neutron collision sites are temporarily stored
in the bank. There are two methods for determining the exiting energies
and directions, depending on the form in which the processed photon
production data are stored in a library. The first method has the
evaluated photon production data processed

into an 'expanded format' [67]. In this format, energy-dependent cross
sections, energy distributions, and angular distributions are explicitly
provided for every photon-producing neutron interaction. In the second
method, used with data processed from older evaluations, the evaluated
photon production data have been collapsed so that the only information
about secondary photons is in a matrix of 20 equally probable photon
energies for each of 30 incident neutron energy groups. The sampling
techniques used in each method are now described.

## 2.4.3.3.1 Expanded Photon Production Method

In the expanded photon production method, the reaction n responsible for
producing the photon is sampled from where ξ is a random number on the
interval [0 , 1) , N is the number of photon production reactions, and σ
i is the photon production cross section for reaction i at the incident
neutron energy. Note that there is no correlation between the sampling
of the type of photon production reaction and the sampling of the type
of neutron reaction described in §2.4.3.5.

<!-- formula-not-decoded -->

Just as every neutron reaction (for example, ( n , 2 n ) ) has
associated energy-dependent angular and energy distributions for the
secondary neutrons, every photon production reaction (for example, ( n ,
p γ ) ) has associated energy-dependent angular and energy distributions
for the secondary photons. The photon distributions are sampled in much
the same manner as their counterpart neutron distributions.

All non-isotropic secondary photon angular distributions are represented
by either 32 equiprobable cosine bins or by a tabulated angular
distribution. The distributions are given at a number of incident
neutron energies. All photon-scattering cosines are sampled in the
laboratory system. The sampling procedure is identical to that described
for secondary neutrons in §2.4.3.5.1.

Secondary photon energy distributions are also a function of incident
neutron energy. There are two representations of secondary photon energy
distributions allowed in ENDF-6 format: tabulated spectra and discrete
(line) photons. Correspondingly, there are two laws used in the MCNP
code for the determination of secondary photon energies. Law 4 provides
for representation of a tabulated photon spectra possibly including
discrete lines. Law 2 is used solely for discrete photons. These laws
are described in more detail beginning in §2.4.3.5.4.1.

The expanded photon production method has clear advantages over the
original 30 × 20 matrix method [§2.4.3.3.2]. In coupled neutron/photon
problems, users should attempt to specify data sets that contain photon
production data in expanded format. Such data sets are identified by
'yes' entries in the GPD column in [46]. However, it should be noted
that the evaluations from which these data are processed may not include
all discrete lines of interest; evaluators may have binned sets of
photons into average spectra that simply preserve the energy
distribution.

## 2.4.3.3.2 30 × 20 Photon Production Method

For lack of better terminology, we will refer to the photon production
data contained in older libraries as ' 30 × 20 photon production' data.
In contrast to expanded photon production data, there is no information
about individual photon production reactions in the 30 × 20 data. This
method is not used in modern tables and is only included to maintain
backwards compatibility for very old data libraries.

The only secondary photon data are a 30 × 20 matrix of photon energies;
that is, for each of 30 incident neutron energy groups there are 20
equally probable exiting photon energies. There is no information
regarding secondary photon angular distributions; therefore, all photons
are taken to be produced isotropically in the laboratory system.

There are several problems associated with 30 × 20 photon production
data. The 30 × 20 matrix is an inadequate representation of the actual
spectrum of photons produced. In particular, discrete photon lines are
not well represented, and the high-energy tail of a photon continuum
energy distribution is not well sampled. Also, the multigroup
representation is not consistent with the continuous-energy nature of
the MCNP code. Finally, not all photons should be produced
isotropically. None of these problems exists for data processed into the
expanded photon production format.

## 2.4.3.4 Absorption

Absorption is treated in one of two ways: analog or implicit. Either
way, the incident incoming neutron energy does not include the relative
velocity of the target nucleus from the free gas thermal treatment
because nonelastic reaction cross sections are assumed to be nearly
independent of temperature. That is, only the scattering cross section
is affected by the free gas thermal treatment. The terms 'absorption'
and 'capture' are used interchangeably for non-fissile nuclides, both
meaning ( n , 0 n ) . For fissile nuclides, 'absorption' includes both
capture and fission reactions.

## 2.4.3.4.1 Analog Absorption

In analog absorption, the particle is killed with probability σ a /σ t ,
where σ a and σ t are the absorption and total cross sections,
respectively, of the collision nuclide at the incoming neutron energy.
The absorption cross section is specially defined for the MCNP code as
the sum of all ( n , x ) cross sections, where x is anything except
neutrons. Thus σ a is the sum of σ n , g , σ n , a , σ n , d , σ f ,
etc. For all particles killed by analog absorption, the entire particle
energy and weight are deposited in the collision cell.

## 2.4.3.4.2 Implicit Absorption

For implicit absorption, also called survival biasing, the neutron
weight W n is reduced to W ′ n as

<!-- formula-not-decoded -->

If the new weight W ′ n is below the problem weight cutoff (specified on
the CUT card), Russian roulette is played, resulting overall in fewer
particles with larger weight.

For implicit absorption, a fraction σ a /σ t of the incident particle
weight and energy is deposited in the collision cell corresponding to
that portion of the particle that was absorbed. Implicit absorption is
the default method of neutron absorption in the MCNP code.

## 2.4.3.4.3 Implicit Absorption Along a Flight Path

Implicit absorption also can be done continuously along the flight path
of a particle trajectory as is the common practice in astrophysics. In
this case, the distance to scatter, rather than the distance to
collision, is sampled. The distance to scatter is

<!-- formula-not-decoded -->

The particle weight at the scattering point is reduced to account for
the expected absorption along the flight path, where

<!-- formula-not-decoded -->

W ′ is the reduced weight after expected absorption along flight path,

W is the weight at the start of the flight path,

σ a is the absorption cross section,

σ s is the scattering cross section,

σ t is the total cross section ( σ a + σ s ), l is the distance to
scatter, and

ξ is a uniformly sampled random number.

Implicit absorption along a flight path is a special form of the
exponential transformation coupled with implicit absorption at
collisions. See the description of the exponential transform in §5.12.7.
The path length is stretched in the direction of the particle, µ = 1 ,
and the stretching parameter is p = Σ a / Σ t . Using these values the
exponential transform and implicit absorption at collisions yield the
identical equations as does implicit absorption along a flight path.

Implicit absorption along a flight path is invoked in the MCNP code as a
special option of the exponential transform variance reduction method.
It is most useful in highly absorbing media, that is, Σ a / Σ t → 1 .
When almost every collision results in absorption, it is very
inefficient to sample distance to collision. However, implicit
absorption along a flight path is discouraged. In highly absorbing
media, there is usually a superior set of exponential transform
parameters. In relatively non-absorbing media, it is better to sample
the distance to collision than the distance to scatter.

## 2.4.3.5 Elastic and Inelastic Scattering

If the conditions for the S ( α, β ) treatment are not met, the particle
undergoes either an elastic or inelastic collision. The selection of an
elastic collision is made with the probability

<!-- formula-not-decoded -->

where

σ el is the elastic scattering cross section.

σ in is the inelastic cross section, including any neutron-out process
such as (n,n'), (n,f), (n,np), etc.

σ a is the absorption cross section; Σ a ( n, x ) , where x = n , that
is, all neutron disappearing reactions.

σ t is the total cross section, σ t = σ el + σ in + σ a .

glyph[negationslash]

Both σ el and σ t are adjusted for the free gas thermal treatment at
thermal energies.

The selection of an inelastic collision is made with the remaining
probability,

<!-- formula-not-decoded -->

If the collision is determined to be inelastic, the type of inelastic
reaction, n , is sampled from

<!-- formula-not-decoded -->

where ξ is a random number on the interval [0 , 1) , N is the number of
inelastic reactions, and σ i is the i th inelastic reaction cross
section at the incident neutron energy.

Directions and energies of all outgoing particles from neutron
collisions are determined by sampling data from the appropriate cross-
section table. Angular distributions are provided and sampled for
scattered neutrons resulting from either elastic or discrete-level
inelastic events; the scattered neutron energy is then calculated from
two-body kinematics. For other reaction types, a variety of data
representations is possible. These representations may be divided into
two types: (a) the outgoing energy and outgoing angle are sampled
independently of each other, or (b) the outgoing energy and outgoing
angle are correlated. In the latter case, the outgoing energy may be
specified as a function of the sampled outgoing angle, or the outgoing
angle may be specified as a function of the sampled outgoing energy.
Details of the possible data representations and sampling schemes are
provided in the following sections.

## 2.4.3.5.1 Sampling of Angular and Energy Distributions

The cosine of the angle between incident and exiting particle
directions, µ , is sampled from angular distribution tables in the
collision nuclide's cross-section library. The cosines are either in the
center-of-mass or target-atrest system, depending on the type of
reaction. Data are provided at a number of incident neutron energies. If
E is the incident neutron energy, if E n is the energy of table n , and
if E n +1 is the energy of table n +1 , then a value of µ is sampled
from table n +1 with probability ( E -E n ) / ( E n +1 -E n ) and from
table n with probability ( E n +1 -E ) / ( E n +1 -E n ) . There are two
options in the MCNP code for representing and sampling a non-isotropic
scattering cosine. The first method involves the use of 32 equally
probable cosine bins. The second method is to sample a tabulated
distribution as a function of µ .

When the method with 32 equiprobable cosine bins is employed, a random
number ξ on the interval [0 , 1) is used to select the i th cosine bin
such that I = 32 + 1 . The value of µ is then computed as

<!-- formula-not-decoded -->

The method of 32 equiprobable cosine bins accurately represents high-
probability regions of the scattering probability; however, it can be a
very crude approximation in low-probability regions. For example, it
accurately represents the forward scattering in a highly forward-peaked
distribution, but may represent all the back angle scattering using only
one or a few bins.

A new, more rigorous angular distribution representation was implemented
in MCNP4C. This new representation features a tabulation of the
probability density function (PDF) as a function of the cosine of the
scattering angle. Interpolation of the PDF between cosine values may be
either by histogram or linear-linear interpolation. The new tabulated
angular distribution allows more accurate representations of original
evaluated distributions (typically given as a set of Legendre
polynomials) in both high-probability and low-probability regions.

Tabular angular distributions are equivalent to tabular energy
distribution (as defined using ENDF Law 4) except that the sampled value
is the cosine of the scattering angle, and discrete lines are not
allowed. For

each incident neutron energy E i there is a pointer to a table of
cosines µ i,k , probability density functions p i,k , and cumulative
density functions c i,k . The index i and the interpolation fraction r
are found on the incident energy grid for the incident energy E in such
that

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and

A random number, ξ 1 , on the unit interval [0 , 1) is used to sample a
cosine bin k from the cumulative density function where l = i if ξ 2 &gt; r
and l = i +1 if ξ 2 &lt; r , and ξ 2 is a random number on the unit
interval. For histogram interpolation the sampled cosine is

<!-- formula-not-decoded -->

For linear-linear interpolation the sampled cosine is

If the emitted angular distribution for some incident neutron energy is
isotropic, µ is chosen from µ = ξ ′ , where ξ ′ is a random number on
the interval [ -1 , 1) . Strictly, in the MCNP code, random numbers are
always furnished on the interval (0 , 1) . Thus, to compute ξ ′ on ( -1
, 1) we calculate ξ ′ = 2 ξ -1 , where ξ is a random number on (0 , 1) .

<!-- formula-not-decoded -->

The ENDF-6 format also has various formalisms to describe correlated
secondary energy-angle spectra. These are discussed later in this
chapter.

For elastic scattering, inelastic level scattering, and some ENDF-6
inelastic reactions, the scattering cosine is chosen in the center-of-
mass system. Conversion must then be made to µ lab , the cosine in the
target-at-rest system. For other inelastic reactions, the scattering
cosine is sampled directly in the target-at-rest system.

The incident particle direction cosines ( u o , v o , w o ) are rotated
to new outgoing target-at-rest system cosines ( u, v, w ) through a
polar angle whose cosine is µ lab , and through an azimuthal angle
sampled uniformly. For random numbers ξ 1 and ξ 2 on the interval [ -1 ,
1) with rejection criterion ξ 1 ξ 2 ≤ 1 , the rotation scheme is [page
54 of 18]

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

If 1 -w 2 o ∼ 0 , then

If the scattering distribution is isotropic in the target-at-rest
system, it is possible to use an even simpler formulation that takes
advantage of the exiting direction cosines, ( u, v, w ) , being
independent of the incident direction cosines, ( u o , v o , w o ) . In
this case,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where ξ 1 and ξ 2 are rejected if ξ 2 1 + ξ 2 2 &gt; 1 .

## 2.4.3.5.2 Energy from Elastic Scattering

Once the particle direction is sampled from the appropriate angular
distribution tables, then the exiting energy, E out , is dictated by
two-body kinematics,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where E in is the incident neutron energy, µ cm is the center-of-mass
cosine of the angle between incident and exiting particle directions,

<!-- formula-not-decoded -->

and A is the mass of nuclide nucleus in units of the mass of a neutron
(atomic weight ratio).

In the case of point detectors, Equation (2.36) is solved for a fixed
cosine scattering angle in the laboratory frame, µ lab .

<!-- formula-not-decoded -->

If the nuclear data is in the center-of-mass frame, then for point
detectors it is necessary to convert

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where and

In the case of the free gas thermal treatment, the kinematics for the
point detector must take into account the velocity of the target nucleus
as described in [68].

## 2.4.3.5.3 Inelastic Reactions

The treatment of inelastic scattering depends upon the particular
inelastic reaction chosen. Inelastic reactions are defined as ( n , y )
reactions such as ( n , n ′ ) , ( n , 2 n ) , ( n , f ) , ( n , n ′ α )
in which y includes at least one neutron.

For many inelastic reactions, such as ( n , 2 n ) , more than one
neutron can be emitted for each incident neutron. The weight of each
exiting particle is always the same as the weight of the incident
particle minus any implicit capture. The energy of exiting particles is
governed by various scattering laws that are sampled independently from
the cross-section files for each exiting particle. Which law is used is
prescribed by the particular cross-section evaluation used. In fact,
more than one law can be specified, and the particular one used at a
particular time is decided with a random number. In an ( n , 2 n )
reaction, for example, the first particle emitted may have an energy
sampled from one or more laws, but the second particle emitted may have
an energy sampled from one or more different laws, depending upon
specifications in the nuclear data library. Because emerging energy and
scattering angle is sampled independently for each particle, there is no
correlation between the emerging particles. Hence energy is not
conserved in an individual reaction because, for example, a 14-MeV
particle could conceivably produce two 12-MeV particles in a single
reaction. The net effect of many particle histories is unbiased because
on the average the correct amount of energy is emitted. Results are
biased only when quantities that depend upon the correlation between the
emerging particles are being estimated.

Users should note that the MCNP code follows a very particular
convention. The exiting particle energy and direction are always given
in the target-at-rest (laboratory) coordinate system. For the
kinematical calculations in the MCNP code to be performed correctly, the
angular distributions for elastic, discrete inelastic level scattering,
and some ENDF-6 inelastic reactions must be given in the center-of-mass
system, and the angular distributions for all other reactions must be
given in the target-at-rest system. The MCNP code does not stop if this
convention is not adhered to, but the results will be erroneous. In the
checking of the cross-section libraries prepared for the MCNP code at
Los Alamos, however, careful attention has been paid to ensure that
these conventions are followed.

The exiting particle energy and direction in the target-at-rest
(laboratory) coordinate system are related to the center-of-mass energy
and direction as [17]:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and where

E ′ is the exiting particle energy (laboratory),

E ′ cm is the exiting particle energy (center-of-mass),

E is the incident particle energy (laboratory),

µ cm is the cosine of center-of-mass scattering angle,

µ lab is the cosine of laboratory scattering angle, and

A is the atomic weight ratio (mass of nucleus divided by mass of
incident particle).

For point detectors, Equation (2.43) is solved for a fixed µ lab
resulting in a quadratic equation with two possible solutions for the
exiting particle energy [69],

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The existence of the roots of the quadratic are subject to the following
conditions:

1. If E ′ cm ≤ 0 , no roots are valid.
2. If E ′ cm &gt; E/ ( A +1) 2 , only the root with the + sign is valid.
3. If 0 &lt; E ′ cm &lt; E/ ( A +1) 2 and √ 1 -( A +1) 2 E ′ cm /E &lt; µ lab &lt; 1 , both roots are valid.

If the nuclear data is in the center-of-mass frame, then for point
detectors it is necessary to convert

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where and

## 2.4.3.5.4 Non-fission Inelastic Scattering and Emission Laws

Non-fission inelastic reactions are handled differently from fission
inelastic reactions. For each non-fission reaction N p particles are
emitted, where N p is an integer quantity specified for each reaction in
the crosssection data library of the collision nuclide. The direction of
each emitted particle is independently sampled from the appropriate
angular distribution table, as was described earlier. The energy of each
emitted particle is independently sampled from one of the following
scattering or emission laws. Energy and angle are correlated only for
ENDF-6 Laws 44 and 67. For completeness and convenience, all the laws
are listed together, regardless of whether the law is appropriate for
non-fission inelastic scattering (for example, Law 3), fission spectra
(for example, Law 11), both (for example, Law 9), or neutron-induced
photon production (for example, Law 2). The conversion from center-of-
mass to target-at-rest (laboratory) coordinate systems is given in the
above equations.

where

## 2.4.3.5.4.1 Law 1 (ENDF Law 1): Equiprobable Energy Bins

The index i and the interpolation fraction r are found on the incident
energy grid for the incident energy E in such that and

A random number on the unit interval ξ 1 is used to select an
equiprobable energy bin k from the K equiprobable outgoing energies E
i,k where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Then scaled interpolation is used with random numbers ξ 2 and ξ 3 on the
unit interval. Let

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and and

and then

## 2.4.3.5.4.2 Law 2: Discrete Photon Energy

The value provided in the library is E g . The secondary photon energy E
out is either

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

for non-primary photons or for primary photons, where A is the atomic
weight to neutron weight ratio of the target and E in is the incident
neutron energy.

## 2.4.3.5.4.3 Law 3 (ENDF Law 3): Inelastic Scattering ( n , n ′ ) From Nuclear Levels

The value provided in the library is Q and as a result

<!-- formula-not-decoded -->

## 2.4.3.5.4.4 Law 4 (ENDF Law 4): Tabular Distribution

For each incident neutron energy E i there is a pointer to a table of
secondary energies E i,k , probability density functions p i,k , and
cumulative density functions c i,k . The index i and the interpolation
fraction r are found on the incident energy grid for the incident energy
E in such that

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and

The tabular distribution at each E i may be composed of discrete lines,
a continuous spectra, or a mixture of discrete lines superimposed on a
continuous background. If discrete lines are present, there must be the
same number of lines (given one per bin) in each table. The sampling of
the emission energy for the discrete lines (if present) is handled
separately from the sampling for the continuous spectrum (if present). A
random number, ξ 1 , on the unit interval [0 , 1) is used to sample a
second energy bin k from the cumulative density function.

If discrete lines are present, the algorithm first checks to see if the
sampled bin is within the discrete line portion of the table as
determined by

<!-- formula-not-decoded -->

If this condition is met, then the sampled energy E ′ for the discrete
line is interpolated between incident energy grids as

<!-- formula-not-decoded -->

If a discrete line has been sampled, the energy sampling is finished. If
a discrete line has not been sampled, the secondary energy is sampled
from the remaining continuous background.

For continuous distributions, the secondary energy bin k is sampled from

<!-- formula-not-decoded -->

where l = i if ξ 2 &gt; r and l = i +1 if ξ 2 &lt; r , and ξ 2 is a random
number on the unit interval. For histogram interpolation the sampled
energy is

<!-- formula-not-decoded -->

For linear-linear interpolation the sampled energy is

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The secondary energy is then interpolated between the incident energy
bins i and i +1 to properly preserve thresholds. Let

and then

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The final step is to adjust the energy from the center-of-mass system to
the laboratory system, if the energies were given in the center-of-mass
system.

Law 4 is an independent distribution, i.e. the emission energy and angle
are not correlated. The outgoing angle is selected from the angular
distribution as described in §2.4.3.5.1. Data tables built using this
methodology are designed to sample the distribution correctly in a
statistical sense and will not necessarily sample the exact distribution
for any specific collision.

## 2.4.3.5.4.5 Law 5 (ENDF Law 5): General Evaporation Spectrum

The function g ( x ) is tabulated versus χ and the energy is tabulated
versus incident energy E in . The law is then

This density function is sampled by E out = χ ( ξ ) T ( E in ) , where T
( E in ) is a tabulated function of the incident energy and c ( ξ ) is a
table of equiprobable χ values.

<!-- formula-not-decoded -->

## 2.4.3.5.4.6 Law 7 (ENDF Law 7): Simple Maxwell Fission Spectrum

The law is

<!-- formula-not-decoded -->

The nuclear temperature T ( E in ) is a tabulated function of the
incident energy. The normalization constant C is given by

<!-- formula-not-decoded -->

where U is a constant provided in the library and limits E out to 0 ≤ E
out ≤ E -U . In the MCNP code this density function is sampled by the
rejection scheme

<!-- formula-not-decoded -->

where ξ 1 , ξ 2 , ξ 3 , and ξ 4 are random numbers on the unit interval.
ξ 1 and ξ 2 are rejected if ξ 2 1 + ξ 2 2 &gt; 1 .

## 2.4.3.5.4.7 Law 9 (ENDF Law 9): Evaporation Spectrum

The law is where the nuclear temperature T ( E in ) is a tabulated
function of the incident energy. The energy U is provided in the library
and is assigned so that E out is limited by 0 ≤ E out ≤ E in -U . The
normalization constant C is given by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

In the MCNP code this density function is sampled by

<!-- formula-not-decoded -->

where ξ 1 and ξ 2 are random numbers on the unit interval, and ξ 1 and ξ
2 are rejected if E out &gt; E in -U .

## 2.4.3.5.4.8 Law 11 (ENDF Law 11): Energy Dependent Watt Spectrum

The law is

The constants a and b are tabulated functions of incident energy and U
is a constant from the library. The normalization constant C is given by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where the constant U limits the range of outgoing energy so that 0 ≤ E
out ≤ E in -U . This density function is sampled as follows. Let

Then E out = -ag ln( ξ 1 ) . E out is rejected if where ξ 1 and ξ 2 are
random numbers on the unit interval.

<!-- formula-not-decoded -->

## 2.4.3.5.4.9 Law 22 (UK Law 2): Tabular Linear Functions of Incident Energy Out

Tables of P i,j , C i,j , and T i,j are given at a number of incident
energies E i . If E i ≤ E in &lt; E i +1 then the i th P i,j , C i,j , and
T i,j tables are used and where k is chosen according to

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where ξ is a random number on the unit interval [0 , 1) .

## 2.4.3.5.4.10 Law 24 (UK Law 6): Equiprobable Energy Multipliers

The law is

<!-- formula-not-decoded -->

The library provides a table of K equiprobable energy multipliers T i,k
for a grid of incident neutron energies E i . For incident energy E in
such that

<!-- formula-not-decoded -->

The random numbers ξ 1 and ξ 2 on the unit interval are used to find T
with

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and so

## 2.4.3.5.4.11 Law 44 Tabular Distribution (ENDF Law=1 Lang=2): Kalbach-87 Correlated Energy-angle Scattering)

Law 44 is an extension of Law 4. For each incident energy E i there is a
pointer to a table of secondary energies E i,k , probability density
functions p i,k , cumulative density functions c i,k , pre-compound
fractions R i,k , and angular distribution slope values A i,k . The
secondary emission energy is found exactly as stated in the Law 4
description in §2.4.3.5.4.4. Unlike Law 4, Law 44 includes a correlated
angular distribution associated with each incident energy E i as given
by the Kalbach parameters R i,k , and A i,k . Thus, the sampled emission
angle is dependent on the sampled emission energy.

The sampled values for R and A are interpolated on both the incident and
outgoing energy grids. For discrete spectra, and

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

For continuous spectra with histogram interpolation,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and

For continuous spectra with linear-linear interpolation,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and

The outgoing neutron center-of-mass scattering angle µ is sampled from
the Kalbach density function

<!-- formula-not-decoded -->

using the random numbers ξ 3 and ξ 4 on the unit interval as follows. If
ξ 3 &gt; R , then let and

or if ξ 3 &lt; R , then

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

As with Law 4, the emission energy and angle are transformed from the
center-of-mass to the laboratory system as necessary.

## 2.4.3.5.4.12 Law 61 Tabular Distribution (ENDF Law=1 Lang=0, 12, or 14): Correlated Energy-angle Scattering

Law 61 is an extension of Law 4. For each incident energy E i there is a
pointer to a table of secondary energies E i,k , probability density
functions p i,k , cumulative density functions c i,k , and pointers to
tabulated angular distributions L i,k . The secondary emission energy is
found exactly as stated in the Law 4 description in §2.4.3.5.4.4. Unlike
Law 4, Law 61 includes a correlated angular distribution associated with
each incident energy E i as given by the tabular angular distribution
located using the pointers L i,k . Thus, the sampled emission angle is
dependent on the sampled emission energy.

If the secondary distribution is given using histogram interpolation,
the angular distribution located at L i,k is used to sample the emission
angle. If the secondary distribution is specified as linear
interpolation between energy points, L i,k is chosen by selecting the
bin closest to the randomly sampled cumulative distribution function
(CDF) point. If the value of L i,k is zero, the angle is sampled from an
isotropic distribution as described on page 81. If the value of L i,k is
positive, it points to a tabular angular distribution which is then
sampled as described on page 81.

As with Law 4, the emission energy and angle are transformed from the
center-of-mass to the laboratory system as necessary.

## 2.4.3.5.4.13 Law 66 (ENDF Law 6): N-body Phase Space Distribution

The phase space distribution for particle i in the center-of-mass
coordinate system is:

where all energies and angles are also in the center-of-mass system and
E max i is the maximum possible energy for particle i , µ , and T . T is
used for calculating E out . The C n normalization constants for n = 3 ,
4 , 5 are:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

E max i is a fraction of the energy available, E avail , given as

<!-- formula-not-decoded -->

where M is the total mass of the n particles being treated, m i is the
mass of particle i , and

<!-- formula-not-decoded -->

where m t is the target mass and m p is the projectile mass. For
neutrons,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and for a total mass ratio A p = M/m i ,

Thus,

<!-- formula-not-decoded -->

The total mass A p and the number of particles in the reaction n are
provided in the data library. The outgoing energy is sampled as follows.

Let ξ i , i = 1 , 10 be random numbers on the unit interval. Then from
rejection technique R28 from the Monte Carlo Sampler [70], accept ξ 1
and ξ 2 if ξ 2 1 + ξ 2 2 ≤ 1 and accept ξ 3 and ξ 4 if ξ 2 3 + ξ 2 4 ≤ 1
.

Then let and

Then

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The cosine of the scattering angle is always sampled isotropically in
the center-of-mass system using another random number ξ 10 on the unit
interval as

<!-- formula-not-decoded -->

## 2.4.3.5.4.14 Law 67 (ENDF Law 7): Correlated Energy-angle Scattering

For each incident neutron energy, first the exiting particle direction µ
is sampled as described in §2.4.3.5.1. In other law data, first the
exiting particle energy is sampled and then the angle is sampled. The
index i and the interpolation fraction r are found on the incident
energy grid for the incident energy E in such that

<!-- formula-not-decoded -->

and

For each incident energy E i there is a table of exiting particle
direction cosines µ i,j and locators L i,j . This table is searched to
find which ones bracket µ , namely,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Then the secondary energy tables at L i,j and L i,j +1 are sampled for
the outgoing particle energy. The secondary energy tables consist of a
secondary energy grid E i,j,k , probability density functions p i,j,k ,
and cumulative density functions c i,j,k . A random number ξ 1 on the
unit interval is used to pick between incident energy indices: if ξ 1 &lt;
r then l = i +1 ; otherwise, l = i . Two more random numbers ξ 2 and ξ 3
on the unit interval are used to determine interpolation energies. As
such,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Similarly,

A random number ξ 4 on the unit interval is used to sample a secondary
energy bin k from the cumulative density function

<!-- formula-not-decoded -->

For histogram interpolation the sampled energy is

<!-- formula-not-decoded -->

For linear-linear interpolation the sampled energy is

<!-- formula-not-decoded -->

The final outgoing energy E out uses scaled interpolation. Let

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and then

## 2.4.3.5.5 Emission from Fission

For any fission reaction a number of neutrons, n , is emitted according
to the value of ν ( E in ) . Depending on the type of problem (fixed
source or KCODE ) and on user input ( TOTNU card), the MCNP code may use
either

prompt ν p ( E in ) or total ν t ( E in ) . For either case, the average
number of neutrons per fission, ν ( E in ) , may be a tabulated function
of energy or a polynomial function of energy.

If DATA entry on the FMULT card is zero (default), then n is sampled
between I (the largest integer less than ν ( E in ) ) and I +1 by where
ξ is a random number drawn from the unit interval.

<!-- formula-not-decoded -->

If more microscopically correct fission neutron multiplicities are
desired for fixed source problems, the DATA entry on the FMULT card can
be used to select which set of Gaussian widths are used to sample the
actual number of neutrons from fission that typically range from 0 to 7
or 8 [71]. For a given fission event, there is a probability P n that n
neutrons are emitted. This distribution is generally called the neutron
multiplicity distribution. Fission neutron multiplicity distributions
are known to be well reproduced by simple Gaussian distributions [72],
and

<!-- formula-not-decoded -->

glyph[negationslash]

<!-- formula-not-decoded -->

where ν is the mean multiplicity, b is a small adjustment to make the
mean equal to ν , and σ is the Gaussian width. For the range of
realistic widths, the adjustment b can be accurately expressed as a
single smooth function of ( ν +0 . 5) /σ [73]. To determine the value of
σ from experimental data, many authors have minimized the chi-squared
where ∆ P exp n is the uncertainty in the experimentally measured
multiplicity distribution P exp n . The factorial moments of the neutron
multiplicity distribution ( ν i = ∑ P n n ! / ( n -i )! ) emitted by a
multiplying sample can be expressed as a function of the factorial
moments for spontaneous and induced fission [74]. Therefore, for many
applications it is not necessary to know the details of the neutron
multiplicity distribution, but it is more important to know the
corresponding first three factorial moments. A reevaluation of the
existing spontaneous fission and neutron induced fission data has been
performed [73] where the widths of Gaussians are adjusted to fit the
measured second and third factorial moments. This reevaluation was done
by minimizing the chi-squared

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

These results are summarized in Table 2.1. Despite the change in
emphasis from the detailed shape to the moments of the distributions,
the inferred widths are little changed from those obtained by others.
However, by minimizing the chi-squared in Eq. (2.122) the inferred
widths are guaranteed to be in reasonable agreement with the measured
second and third factorial moments. The widths obtained using Eq.
(2.122) give Gaussian distributions that reproduce the experimental
second and third factorial moments to better than 0.6%. The adjustment
parameter b ensures that the first moment ( ν ) is accurately
reproduced. If the chi-squared in Eq. (2.121) is used, then the second
and third factorial moments can differ from the experimental values by
as much as 10%.

Assuming that the widths of the multiplicity distributions are
independent of the initial excitation energy of the fissioning system
[73], the relationship between different factorial moments is easily
calculated as a function of ν . The corresponding calculated
relationships between the first three factorial moments are in

Table 2.1: Recommended Gaussian Widths [73] from Eq. (2.122)

| Reaction    |     σ |
|-------------|-------|
| 233 U(n,f)  | 1.07  |
| 235 U(n,f)  | 1.088 |
| 238 U(n,f)  | 1.116 |
| 239 Pu(n,f) | 1.14  |
| 241 Pu(n,f) | 1.15  |
| 238 Pu SF ∗ | 1.135 |
| 240 Pu SF   | 1.151 |
| 242 Pu SF   | 1.161 |
| 242 Cm SF   | 1.091 |
| 244 Cm SF   | 1.103 |
| 246 Cm SF   | 1.098 |
| 248 Cm SF   | 1.108 |
| 250 Cf SF   | 1.22  |
| 252 Cf SF   | 1.245 |
| 254 Cf SF   | 1.215 |
| 254 Fm SF   | 1.246 |

∗ SF: Spontaneous Fission

good agreement with experimental neutron induced fission data up to an
incoming neutron energy of 10 MeV [73]. This implies that an energy
independent width can be used with confidence up to an incoming neutron
energy of at least 10 MeV. The Gaussian widths in Table 2.1 are used for
fission multiplicity sampling in the MCNP code when the DATA entry on
the FMULT card is 1. Induced fission multiplicities for isotopes not
listed in Table 2.1 use a Gaussian width that is linearly dependent on
the mass number of the fissioning system [73].

The direction of each emitted neutron is sampled independently from the
appropriate angular distribution table by the procedure described in
§2.4.3.5.1.

The energy of each fission neutron is determined from the appropriate
emission law. These laws are discussed in the preceding section. The
MCNP code then models the transport of the first neutron out after
storing all other neutrons in the bank.

## 2.4.3.5.6 Prompt and Delayed Neutron Emission

If (1) the MCNP code is using ν t , (2) the data for the collision
isotope includes delayed-neutron spectra, and (3) the use of detailed
delayed-neutron data has not been preempted (on the PHYS : n card), then
each fission neutron is first determined by the MCNP code to be either a
prompt fission neutron or a delayed fission neutron. Assuming analog
sampling, the type of emitted neutron is determined from the ratio of
delayed ν ( E in ) to total ν t ( E in ) where a delayed neutron is
produced if

<!-- formula-not-decoded -->

and a prompt neutron is produced if

<!-- formula-not-decoded -->

where ν d is the expected number of delayed neutrons.

If the neutron is determined to be a prompt fission neutron, it is
emitted instantaneously, and the emission laws (angle and energy)
specified for prompt fission are sampled.

If the neutron is determined to be a delayed fission neutron, then the
MCNP code first samples for the decay group by using the specified
abundances. Then, the time delay is sampled from the exponential density
with decay constant specified for the sampled decay group.

Finally, the emission laws (angle and energy) specified for that decay
group are then sampled. Since the functionality in the MCNP code to
produce delayed neutrons using appropriate emission data is new, we
include next a somewhat more expanded description.

A small but important fraction ( ≈ 1% ) of the neutrons emitted in
fission events are delayed neutrons emitted as a result of fission-
product decay at times later than prompt fission neutrons. the MCNP code
users have always been able to specify whether or not to include delayed
fission neutrons by using either ν t (prompt plus delayed) or ν p
(prompt only). However, in versions of the MCNP code up through and
including 4B, all fission neutrons (whether prompt or delayed) were
produced instantaneously and with an energy sampled from the spectra
specified for prompt fission neutrons.

For many applications this approach is adequate. However, it is another
example of a data approximation that is unnecessary. Therefore, Versions
4C and later of the MCNP code allow delayed fission neutrons to be
sampled (either analog or biased) from time and energy spectra as
specified in nuclear data evaluations. The libraries with detailed
delayed fission neutron data are listed in [46] with a 'yes' in the 'DN'
column.

The explicit sampling of a delayed-neutron spectrum implemented in
MCNP4C has two effects. One is that the delayed neutron spectra have the
correct energy distribution; they tend to be softer than the prompt
spectra. The second is that experiments measuring neutron decay after a
pulsed source can now be modeled with the MCNP code because the delay in
neutron emission following fission is properly accounted for. In this
treatment, a natural sampling of prompt and delayed neutrons is
implemented as the default and an additional delayed neutron biasing
control is available to the user via the PHYS : n card. The biasing
allows the number of delayed neutrons produced to be increased
artificially because of the low probability of a delayed neutron
occurrence. The delayed neutron treatment is intended to be used with
the TOTNU card in the MCNP code, giving the user the flexibility to use
the time-dependent treatment of delayed neutrons whenever the delayed
data are available.

The impact of sampling delayed-neutron energy spectra on reactivity
calculations has been studied [75]. As expected, most of the reactivity
impacts are very small, although changes of 0.1-0.2% in k eff were
observed for certain cases. Overall, inclusion of delayed-neutron
spectra can be expected to produce small positive reactivity changes for
systems with significant fast neutron leakage and small negative changes
for some systems in which a significant fraction of the fissions occurs
in isotopes with an effective fission threshold (e.g., 238 U and 240
Pu).

## 2.4.3.6 The S ( α, β ) Treatment

The S ( α, β ) thermal scattering treatment is a complete representation
of thermal neutron scattering by molecules and crystalline solids. Two
processes are allowed: (1) inelastic scattering with cross section σ in
and a coupled energy-angle representation derived from an ENDF S ( α, β
) scattering law, and (2) elastic scattering with no change in the
outgoing neutron energy for solids with cross section σ el and an
angular treatment derived from lattice parameters. The elastic
scattering treatment is chosen with probability σ el / ( σ el + σ in ) .
This thermal scattering treatment also allows the representation of
scattering by multi-atomic molecules (for example, BeO).

For the inelastic treatment, the distribution of secondary energies is
represented by a set of equally probable final energies (typically 16 or
32) for each member of a grid of initial energies from an upper limit of
typically 4 eV down to 10 -5 eV, along with a set of angular data for
each initial and final energy. The selection of a final energy E ′ given
an initial energy E can be characterized by sampling from the
distribution

<!-- formula-not-decoded -->

where E i and E i +1 are adjacent elements on the initial energy grid,

<!-- formula-not-decoded -->

N is the number of equally probable final energies, and E i,j is the j
th discrete final energy for incident energy E i .

There are two allowed schemes for the selection of a scattering cosine
following selection of a final energy and final energy index j . In each
case, the ( i, j ) th set of angular data is associated with the energy
transition E = E i → E ′ = E i,j .

In the first scheme, the data consist of sets of equally probable
discrete cosines µ i,j,k for k = 1 , . . . , ν with ν typically 4 or 8.
An index k is selected with probability 1 /ν , and µ is obtained by the
relation

<!-- formula-not-decoded -->

In the second scheme, the data consist of bin boundaries of equally
probable cosine bins. In this case, random linear interpolation is used
to select one set or the other, with ρ being the probability of
selecting the set corresponding to incident energy E i . The subsequent
procedure consists of sampling for one of the equally probable bins and
then choosing µ uniformly in the bin.

For elastic scattering, the above two angular representations are
allowed for data derived by an incoherent approximation. In this case,
one set of angular data appears for each incident energy and is used
with the interpolation procedures on incident energy described above.
For elastic scattering, when the data have been derived in the coherent
approximation, a completely different representation occurs. In this
case, the data actually stored are the set of parameters D k , where

<!-- formula-not-decoded -->

and E Bk are Bragg energies derived from the lattice parameters. For
incident energy E such that E Bk ≤ E ≤ E Bk +1 ,

<!-- formula-not-decoded -->

represents a discrete cumulative probability distribution that is
sampled to obtain index i , representing scattering from the i th Bragg
edge. The scattering cosine is then obtained from the relationship

<!-- formula-not-decoded -->

Using next-event estimators such as point detectors with S ( α, β ) ,
scattering cannot be done exactly because of the discrete scattering
angles. The MCNP code uses an approximate scheme [76, 77] that in the
next-event estimation calculation replaces discrete lines with
histograms of width δµ &lt; 0 . 1 .

See also §2.5.6.4.7.

## 2.4.3.7 Probability Tables for the Unresolved Resonance Range

Within the unresolved resonance range (e.g., in ENDF/B-VI, 2.25-25 keV
for 235 U, 10-149.03 keV for 238 U, and 2.5-30 keV for 239 Pu),
continuous-energy neutron cross sections appear to be smooth functions
of energy. This behavior occurs not because of the absence of
resonances, but rather because the resonances are so close together that
they are unresolved. Furthermore, the smoothly varying cross sections do
not account

for resonance self-shielding effects, which may be significant for
systems whose spectra peak in or near the unresolved resonance range.

Fortunately, the resonance self-shielding effects can be represented
accurately in terms of probabilities based on a stratified sampling
technique. This technique produces tables of probabilities for the cross
sections in the unresolved resonance range. Sampling the cross section
in a random walk from these probability tables is a valid physics
approximation so long as the average energy loss in a single collision
is much greater than the average width of a resonance; that is, if the
narrow resonance approximation [78] is valid. Then the detail in the
resonance structure following a collision is statistically independent
of the magnitude of the cross sections prior to the collision.

The utilization of probability tables is not a new idea in Monte Carlo
applications. A code [79] to calculate such tables for Monte Carlo fast
reactor applications was utilized in the early 1970s. Temperature-
difference Monte Carlo calculations [80] and a summary of the VIM Monte
Carlo code [81] that uses probability tables are pertinent early
examples. Versions of the MCNP code up through and including 4B did not
take full advantage of the unresolved resonance data provided by
evaluators. Instead, smoothly varying average cross sections were used
in the unresolved range. As a result, any neutron self-shielding effects
in this energy range were unaccounted for. Better utilizations of
unresolved data have been known and demonstrated for some time, and the
probability table treatment has been incorporated [82] into MCNP4C and
its successors. The column 'UR' in [46] lists whether unresolved
resonance probability table data is available for each nuclide library.

Sampling cross sections from probability tables is straightforward. At
each of a number of incident energies there is a table of cumulative
probabilities (typically 20) and the value of the near-total, elastic,
fission, and radiative capture cross sections and heat deposition
numbers corresponding to those probabilities. These data supplement the
usual continuous data; if probability tables are turned off ( PHYS : n
card), then the usual smooth cross section is used. But if the
probability tables are turned on (default), if they exist for the
nuclide of a collision, and if the energy of the collision is in the
unresolved resonance energy range of the probability tables, then the
cross sections are sampled from the tables. The near-total is the total
of the elastic, fission, and radiative capture cross sections; it is not
the total cross section, which may include other absorption or inelastic
scatter in addition to the near-total. The radiative capture cross
section is not the same as the usual MCNP capture cross section, which
is more properly called 'destruction' or absorption and includes not
only radiative capture but all other reactions not emitting a neutron.
Sometimes the probability tables are provided as factors (multipliers of
the average or underlying smooth cross section) which adds computational
complexity but now includes any structure in the underlying smooth cross
section.

It is essential to maintain correlations in the random walk when using
probability tables to properly model resonance self-shielding. Suppose
we sample the 17 th level (probability) from the table for a given
collision. This position in the probability table must be maintained for
the neutron trajectory until the next collision, regardless of particle
splitting for variance reduction or surface crossings into various other
materials whose nuclides may or may not have probability table data.
Correlation must also be retained in the unresolved energy range when
two or more cross-section sets for an isotope that utilize probability
tables are at different temperatures.

The impact of the probability-table approach has been studied [83] and
found to have negligible impact for most fast and thermal systems. Small
but significant changes in reactivity may be observed for plutonium and
233 U systems, depending upon the detailed shape of the spectrum.
However, the probability-table method can produce substantial increases
in reactivity for systems that include large amounts of 238 U and have
high fluxes within the unresolved resonance region. Calculations for
such systems will produce significantly nonconservative results unless
the probability-table method is employed.

## 2.4.4 Photon Interactions

Sampling of a collision nuclide, analog capture, implicit capture, and
many other aspects of photon interactions such as variance reduction,
are the same as for neutrons. The collision physics are completely
different.

The MCNP code has two photon interaction models: simple and detailed.

The simple physics treatment ignores coherent (Thomson) scattering and
fluorescent photons from photoelectric absorption. It is intended for
high-energy photon problems or problems where electrons are free and is
also important for next-event estimators such as point detectors, where
scattering can be nearly straight ahead with coherent scatter. The
simple physics treatment uses implicit capture unless overridden with
the CUT : p card, in which case it uses analog capture.

The detailed physics treatment includes coherent (Thomson) scattering
and accounts for fluorescent photons after photoelectric absorption.
Form factors and Compton profiles are used to account for electron
binding effects. Analog capture is always used. The detailed physics
treatment is used below energy EMCPF on the PHYS : p card, and because
the default value of EMCPF is 100 MeV, that means it is almost always
used by default. It is the best treatment for most applications,
particularly for highZ nuclides or deep penetration problems.

The generation of electrons from photons is handled three ways. These
three ways are the same for both the simple and detailed photon physics
treatments.

1. If electron transport is turned on ( MODE P E ), then all photon collisions except coherent scatter can create electrons that are banked for later transport.
2. If electron transport is turned off (no E on the MODE card), then a thick-target bremsstrahlung model (TTB) is used. This model generates electrons, but assumes that they are locally slowed to rest. Any bremsstrahlung photons produced by the non-transported electrons are then banked for later transport. Thus electron-induced photons are not neglected, but the expensive electron transport step is omitted. The TTB production model contains many approximations compared to models used in actual electron transport. In particular, the bremsstrahlung photons inherit the direction of the parent electron.
3. If IDES = 1 on the PHYS : p card, then all electron production is turned off, no electron-induced photons are created, and all electron energy is assumed to be locally deposited.

The TTB approximation is the default for MODE P problems. In MODE P E
problems, it plays a role when the energy cutoff for electrons is
greater than that for photons. In this case, the TTB model is used in
the terminal processing of the electrons to account for the few low-
energy bremsstrahlung photons that would be produced at the end of the
electrons' range.

## 2.4.4.1 Simple Physics Treatment

The simple physics treatment is intended primarily for higher energy
photons. It is inadequate for highZ nuclides or deep penetration
problems. The physical processes treated are photoelectric effect, pair
production, Compton scattering from free electrons, and (optionally)
photonuclear interactions (described in §2.4.4.3). The photoelectric
effect is regarded as an absorption (without fluorescence). The
kinematics of Compton scattering is assumed to be with free electrons
(without the use of form factors or Compton profiles). The total
scattering cross section, however, includes the incoherent scattering
factor regardless of the use of simple or detailed physics. Thus, strict
comparisons with codes using only the Klein-Nishina differential cross
section are not valid. Highly forward coherent Thomson scattering is
ignored. Thus the total cross section σ t is regarded as the sum of
three components:

<!-- formula-not-decoded -->

## 2.4.4.1.1 Photoelectric Effect

This is treated as a pure absorption by implicit capture with a
corresponding reduction in the photon weight WGT, and hence does not
result in the loss of a particle history except for Russian roulette
played on the weight cutoff. The non-captured weight WGT (1 -σ pe /σ s )
is then forced to undergo either pair production or Compton scattering.
The captured weight either is assumed to be locally deposited or becomes
a photoelectron for electron transport or for the TTB approximation.

## 2.4.4.1.2 Pair Production

In a collision resulting in pair production [probability σ pp / ( σ t -σ
pe ) ], either an electron-positron pair is created for further
transport (or the TTB treatment) and the photon disappears, or it is
assumed that the kinetic energy WGT ( E -1 . 022) MeV of the electron-
positron pair produced is deposited as thermal energy at the time and
point of collision, with isotropic production of one photon of energy
0.511 MeV headed in one direction and another photon of energy 0.511 MeV
headed in the opposite direction. The rare single 1.022-MeV annihilation
photon is ignored. The relatively unimportant triplet production process
is also ignored. The simple physics treatment for pair production is the
same as the detailed physics treatment that is described in §2.4.4.2.4.

## 2.4.4.1.3 Compton Scattering

The alternative to pair production is Compton scattering on a free
electron, with probability σ s / ( σ t -σ pe ) . In the event of such a
collision, the objective is to determine the energy E ′ of the scattered
photon, and µ = cos( θ ) for the angle θ of deflection from the line of
flight. This yields at once the energy WGT ( E -E ′ ) deposited at the
point of collision and the new direction of the scattered photon. The
energy deposited at the point of collision can then be used to make a
Compton recoil electron for further transport or for the TTB
approximation. The differential cross section for the process is given
by the Klein-Nishina formula [17]

<!-- formula-not-decoded -->

where r o is the classical electron radius 2 . 817938 × 10 -13 cm , α
and α ′ are the incident and final photon energies in units of 0.511 MeV
[ α = E/ ( mc 2 ) , where m is the mass of the electron and c is the
speed of light], and α ′ = α/ [1 + α (1 -µ )] .

The Compton scattering process is sampled exactly by Kahn's method [35]
below 1.5 MeV and by Koblinger's method [84] above 1.5 MeV as analyzed
and recommended by Blomquist and Gelbard [85].

## 2.4.4.2 Detailed Physics Treatment

The detailed physics treatment includes coherent (Thomson) scattering
and accounts for fluorescent photons after photoelectric absorption.
Again, photonuclear interactions may (optionally) be included
[§2.4.4.3]. Form factors are used with coherent and incoherent
scattering to account for electron binding effects. Photo-neutron
reactions can also be included for select isotopes. Analog capture is
always used, as described in §2.4.4.2.3. The detailed physics treatment
is used below energy EMCPF on the PHYS : p card, and because the default
value of EMCPF is 100 MeV, that means it is almost always used by
default. It is the best treatment for most applications, particularly
for highZ nuclides or deep penetration problems.

Figure 2.5: Scattering factor modifying the Klein-Nishina cross section from [86].

<!-- image -->

When using next-event estimators (point detectors, ring detectors, or
image detectors) with detailed physics treatment, one should enable one
of two options, as explained in §2.4.4.2.5. That is, one can turn off
coherent scattering with the NOCOH = 1 option on the PHYS : p card. Or,
one can prevent large scores from rare coherent scattering contributions
by enabling next-event estimator contributions from all possible photon
reactions at each collision by setting the PDS = 1 option on the FT
card.

## 2.4.4.2.1 Incoherent (Compton) Scattering

To model Compton scattering it is necessary to determine the angle θ of
scattering from the incident line of flight (and thus the new
direction), the new energy E ′ of the photon, and the recoil kinetic
energy of the electron, E -E ′ . The recoil kinetic energy can be
deposited locally, can be transported in MODE P E problems, or (default)
can be treated with the TTB approximation.

Incoherent scattering is assumed to have the differential cross section

<!-- formula-not-decoded -->

where I ( Z, v ) is an appropriate scattering factor modifying the
Klein-Nishina cross section in Eq. (2.119).

Qualitatively, the effect of I ( Z, v ) is to decrease the Klein-Nishina
cross section (per electron) more extremely in the forward direction,
for low E and for highZ independently. For any Z , I ( Z, v ) increases
from I ( Z, 0) = 0 to I ( Z, ∞ ) = Z . The parameter v is the inverse
length v = sin( θ/ 2) /λ = κα √ 1 -µ , where κ = m o c/ ( h √ 2 ) = 29 .
1434 Å -1 . The maximum value of v is v max = κα √ 2 = 41 . 2149 α Å -1
at µ = -1 . The essential features of I ( Z, v ) are indicated in Figure
2.5. These parameters are calculated using MCNP internal variables,
which may not match the current best values.

For hydrogen, an exact expression for the form factor is used [86, 87],
which is

<!-- formula-not-decoded -->

where f is the inverse fine structure constant, f = 137 . 0393 , and f /
√ 2 = 96 . 9014 .

The Klein-Nishina formula is sampled exactly by Kahn's method [35] below
1.5 MeV and by Koblinger's method [84] above 1.5 MeV as analyzed and
recommended by Blomquist and Gelbard [85]. The outgoing energy E ′ and
angle µ are rejected according to the form factors.

For next-event estimators such as detectors and DXTRAN, the probability
density for scattering toward the detector point must be calculated as

<!-- formula-not-decoded -->

where πr o = 0 . 2494351 and σ 1 ( Z, α ) and I ( Z, v ) are looked up
in the data library.

The new energy, E ′ , of the photon accounts for the effects of a bound
electron. The electron binding effect on the scattered photon's energy
distribution appears as a broadening of the energy spectrum due to the
pre-collision momentum of the electron. This effect on the energy
distribution of the incoherently scattered photon is called Doppler
broadening.

The Hartree-Fock Compton profiles, J ( p z ) , are used to account for
the effects of a bound electron on the energy distribution of the
scattered photon. These Compton profiles are a collection of orbital and
total atom data tabulated as a function of the projected pre-collision
momentum of the electron. Values of the Compton profiles for the
elements are published in tabular form by Biggs et al. [52] as a
function of p z .

The scattered energy of a Doppler broadened photon can be calculated by
selecting an orbital shell, sampling the projected momentum from the
Compton profile, and calculating the scattered photon energy, E ′ , from

<!-- formula-not-decoded -->

The Compton profiles are related to the incoherent scattering function,
I ( Z, v ) , by

<!-- formula-not-decoded -->

where k refers to the particular electron subshell, J k ( p z , Z ) is
the Compton profile of the k th shell for a given element, and p max z
is the maximum momentum transferred and is calculated using E ′ = E -E
binding .

## 2.4.4.2.2 Coherent (Thomson) Scattering

Thomson scattering involves no energy loss, and thus is the only photon
process that cannot produce electrons for further transport and that
cannot use the TTB approximation. Only the scattering angle θ is
computed, and then the transport of the photon continues.

The differential cross section is σ 2 ( Z, α, µ )d µ = C 2 ( Z, v ) T (
µ )d µ , where C ( Z, v ) is a form factor modifying the energy-
independent Thomson cross section T ( µ ) = πr 2 o ( 1 + µ 2 ) d µ .

Figure 2.6: Form factor modifying the energy-dependent Thomson cross section from [86].

<!-- image -->

The general effect of C 2 ( Z, v ) /Z 2 is to decrease the Thomson cross
section more extremely for backward scattering, for high E , and low Z .
This effect is opposite in these respects to the effect of I ( Z, v ) /Z
on K ( α, µ ) in incoherent (Compton) scattering. For a given Z , C ( Z,
v ) decreases from C ( Z, 0) = Z to C ( Z, ∞ ) = 0 . For example, C ( Z,
v ) is a rapidly decreasing function of µ as µ varies from +1 to -1 ,
and therefore the coherent cross section is peaked in the forward
direction. At high energies of the incoming photon, coherent scattering
is strongly forward and can be ignored. The parameter v is the inverse
length v = sin( θ/ 2) /λ = κα √ 1 -µ , where κ = m o c/ ( h √ 2 ) = 29 .
1434 Å -1 . The maximum value of v is v max = κα √ 2 = 41 . 2149 α Å -1
at µ = -1 . The square of the maximum value is v 2 max = 1698 . 6679 α 2
Å -2 . The qualitative features of C ( Z, v ) are shown in Figure 2.6.
These parameters are calculated using MCNP internal variables, which may
not match the current best values.

For next-event estimators, one must evaluate the probability density
function

<!-- formula-not-decoded -->

for a given µ . Here σ 2 ( Z, α ) is the integrated coherent cross
section. The value of C ( Z, v ) at v = κα √ 1 -µ must be interpolated
in the original C 2 ( Z, v i ) tables separately stored on the cross-
section library for this purpose.

Note that at high energies, coherent scattering is virtually straight
ahead with no energy loss; thus, it appears from a transport viewpoint
that no scattering took place. For a point detector to sample this
scattering, the point must lie on the original track ( µ ∼ = 1 ), which
is seldom the case. Thus, photon point detector variances generally will
be much greater with detailed photon physics than with simple physics
unless coherent scattering is turned off with NOCOH = 1 on the PHYS : p
card or by enabling next-event estimator contributions from all possible
photon reactions at each collision by setting the PDS option on the FT
card, as explained in §2.4.4.2.5.

## 2.4.4.2.3 Photoelectric Effect

The photoelectric effect consists of the absorption of the incident
photon of energy E , with the consequent emission of several fluorescent
photons and the ejection (or excitation) of an orbital electron of
binding energy e &lt; E , giving the electron a kinetic energy of E -e .
Zero, one, or two fluorescent photons are emitted. These three cases are
now described.

- (1) Zero photons greater than 1 keV are emitted. In this event, the cascade of electrons that fills up the orbital vacancy left by the photoelectric ejection produces electrons and low-energy photons (Auger effect). These particles can be followed in MODE P E problems, or be treated with the TTB approximation, or be assumed to deposit energy locally. Because no photons are emitted by fluorescence (some may be produced by electron transport or the TTB model), the photon track is terminated. This photoelectric 'capture' of the photon is scored like analog capture in the summary table of the output file. Implicit capture is not possible.
- (2) One fluorescent photon of energy greater than 1 keV is emitted. The photon energy E ′ is the difference in incident photon energy E , less the ejected electron kinetic energy E -e , less a residual excitation energy e ′ that is ultimately dissipated by further Auger processes. This dissipation leads to additional electrons or photons of still lower energy. The ejected electron and any Auger electrons can be transported or treated with the TTB approximation. In general,

<!-- formula-not-decoded -->

These primary transactions are taken to have the full fluorescent yield
from all possible upper levels e ′ , but are apportioned among the x-ray
lines Kα 1 , ( L 3 → K ) ; Kα 2 , ( L 2 → K ) ; Kβ ′ 1 , ( mean M → K )
; and kβ ′ 2 , ( mean N → K ) .

- (3) Two fluorescence photons can occur if the residual excitation e ′ of process (2) exceeds 1 keV. An electron of binding energy e ′′ can fill the orbit of binding energy e ′ , emitting a second fluorescent photon of energy E ′′ = e ′ -e ′′ . As before, the residual excitation e ′′ is dissipated by further Auger events and electron production that can be modeled with electron transport in MODE P E calculations, approximated with the TTB model, or assumed to deposit all energy locally. These secondary transitions come from all upper shells and go to L shells. Thus the primary transitions must be Kα 1 or Kα 2 to leave an L shell vacancy.

Each fluorescent photon born as discussed above is assumed to be emitted
isotropically and can be transported, provided that E ′ , E ′′ &gt; 1 keV.
The binding energies e , e ′ , and e ′′ are very nearly the x-ray
absorption edges because the x-ray absorption cross section takes an
abrupt jump as it becomes energetically possible to eject (or excite)
the electron of energy E ∼ = e ′′ , then e ′ , then e , etc. The jump
can be as much as a factor of 20 (for example, K-carbon).

A photoelectric event is terminal for elements Z &lt; 12 because the
possible fluorescence energy is below 1 keV. The event is only a single
fluorescence of energy above 1 keV for 31 &gt; Z ≥ 12 , but double
fluorescence (each above 1 keV) is possible for Z ≥ 31 . For Z ≥ 31 ,
primary lines Kα 1 , Kα 2 , and Kβ ′ 1 are possible and, in addition,
for Z ≥ 37 , the Kβ ′ 2 line is possible.

In all photoelectric cases where the photon track is terminated because
either no fluorescent photons are emitted or the ones emitted are below
the energy cutoff, the termination is considered to be caused by analog
capture in the output file summary table (and not energy cutoff).

## 2.4.4.2.4 Pair Production

This process is considered only in the field of a nucleus. The threshold
is 2 mc 2 [1 + ( m/M )] ∼ = 1 . 022 MeV, where M is the nuclear mass and
m is the mass of the electron. There are three cases:

1. In the case of electron transport ( MODE P E ), the electron and positron are created and banked and the photon track terminates.
2. For MODE P problems with the TTB approximation, both an electron and positron are produced but not transported. Both particles can make TTB approximation photons. The positron is then considered to be annihilated locally and a photon pair is created as in case (3).
3. For MODE P problems when positrons are not created by the TTB approximation, the incident photon of energy E vanishes. The kinetic energy of the created positron/electron pair, assumed to be E -2 mc 2 , is deposited locally at the collision point. The positron is considered to be annihilated with an electron at the point of collision, resulting in a pair of photons, each with the incoming photon weight, and each with an energy of mc 2 = 0 . 511 MeV. The first photon is emitted isotropically, and the second is emitted in the opposite direction. The very rare single-annihilation photon of 1.022 MeV is ignored.

## 2.4.4.2.5 Caution for Detectors and Coherent Scattering

Users should understand the implications of using detailed photon
physics with either next-event estimators or DXTRAN. The user should
take care to enable either one of three possible solutions when using
the detailed physics treatment with photon next-event estimators (such
as point detector, ring detectors, and image detectors). The user can
use two of these options for photon simulations with DXTRAN. For both
next-event estimators and DXTRAN, one can turn off coherent scattering
with the NOCOH = 1 option on the PHYS : p card or enable the simple
physics treatment ( EMCPF &lt; 0 . 001 on the PHYS : p card).
Alternatively, for next-event estimators only, one can enable sampling
all reactions at each collision event with the FT PDS option for each
tally.

Turning off coherent scattering can improve the figure of merit (FOM)
[§2.6.5] by more than a factor of 10 for tallies with small relative
errors because coherent scattering is highly peaked in the forward
direction. Consequently, coherent scattering becomes undersampled
because the photon must be traveling directly at the detector point and
undergo a coherent scattering event. When the photon is traveling nearly
in the direction of the point detector or the chosen point on a ring
detector or DXTRAN sphere, the p ( µ ) term (called 'PSC' in the MCNP
code) of the point detector [§2.5.6.1] becomes large, which causes a
large score for the event and may significantly increase the variance of
the tally.

The reason that a large score can occur is that p ( µ ) is a probability
density function, not a probability ( p ( µ )d µ , which can be no
larger than unity), and can approach infinity for highly forward-peaked
scattering. Thus, the under-sampled coherent scattering event is
characterized by many low contributions to the detector when the photon
trajectory is directed away from the detector (when p ( µ ) is small)
and a few large contributions when the trajectory is nearly pointed
toward the detector (and p ( µ ) is large). Such under-sampled events
cause a large score and commensurate increase in both the tally mean and
the variance, a decrease in the FOM, and likely a failure to pass the
statistical checks for the tally as described in §2.6.9.2.3. One way to
improve sampling for point-detector tallies of these forward-peaked
behaviors is with the FT PDS option. The FT PDS option enables
contributions from all possible reaction types (and optionally all
isotopes as well) at each collision. With this option, the statistical
weight of each reaction contribution is based on the reaction
probability, which results in many small contributions from coherent
scattering instead of a few large contributions.

## 2.4.4.3 Photonuclear Physics Treatment

Photonuclear physics may be included when handling a photon collision. A
photonuclear interaction begins with the absorption of a photon by a
nucleus. There are several mechanisms by which this can occur. The
nuclear data files currently available focus on the energy range up to
150 MeV incident photon energy. The

value of 150 MeV was chosen as this energy is just below the threshold
for the production of pions and the subsequent need for much more
complicated nuclear modeling. Below 150 MeV, the primary mechanisms for
photoabsorption are the excitation of either the giant dipole resonance
or a quasi-deuteron nucleon pair.

The giant dipole resonance (GDR) absorption mechanism can be
conceptualized as the electromagnetic wave, the photon, interacting with
the dipole moment of the nucleus as a whole. This results in a
collective excitation of the nucleus. It is the most likely process
(that is, the largest cross section) by which photons interact with the
nucleus. Expected peak cross sections of 6-10 millibarns are seen for
the light isotopes and 600-800 millibarns are not uncommon for the heavy
elements. Thus, photonuclear collisions may account for a theoretical
maximum of 5-6% of the photon collisions. The GDR occurs with highest
probability when the wavelength of the photon is comparable to the size
of the nucleus. This typically occurs for photon energies in the range
of 5-20 MeV and has a resonance width of a few MeV. For deformed nuclei,
a double peak is seen due to the variation of the nuclear radius.
Outside of this resonance region, the cross section for a GDR reaction
becomes negligible. A complete description of this process can be found
in the text by Bohr and Mottelson [88].

The quasi-deuteron (QD) absorption mechanism can be conceptualized as
the electromagnetic wave interacting with the dipole moment of a
correlated neutron-proton pair. In this case, the neutron-proton pair
can be thought of as a QD having a dipole moment with which the photon
can interact. This mechanism is not as intense as the GDR but it
provides a significant background cross section for all incident photon
energies above the relevant particle separation threshold. The seminal
work describing this process was published by Levinger [89, 90]. Recent
efforts to model this process include the work of Chadwick et al. [91].

Once the photon has been absorbed by the nucleus, one or more secondary
particle emissions can occur. For the energy range in question (that is,
below 150 MeV) these reactions may produce a combination of gamma rays,
neutrons, protons, deuterons, tritons, helium-3 particles, alphas, and
fission fragments. The threshold for the production of a given secondary
particle is governed by the separation energy of that particle,
typically a few MeV to as much as a few 10s of MeV. Most of the these
particles are emitted via pre-equilibrium and equilibrium mechanisms
though it is possible, but rare, to have a direct emission.

Pre-equilibrium emission can be conceptualized as a particle within the
nucleus that receives a large amount of energy from the absorption
mechanism and escapes the binding force of the nucleus after at least
one but very few interactions with other nuclei. This is in contrast to
a direct emission where the emission particle escapes the nucleus
without any interactions. Typically this occurs from QD absorption of
the photon where the incident energy is initially split between the
neutron-proton pair. Particles emitted by this process tend to be
characterized by higher emission energies and forward-peaked angular
distributions.

Equilibrium emission can be conceptualized as particle evaporation. This
process typically occurs after the available energy has been generally
distributed among the nucleons. In the classical sense, particles boil
out of the nucleus as they penetrate the nuclear potential barrier. The
barrier may contain contributions from coulomb potential (for charged
particles) and effects of angular momentum conservation. It should be
noted that for heavy elements, evaporation neutrons are emitted
preferentially as they are not subject to the coulomb barrier. Particles
emitted by this process tend to be characterized by isotropic angular
emission and evaporation energy spectra. Several references are
available on the general emission process after photoabsorption [92-94].

For all of the emission reactions discussed thus far, the nucleus will
most probably be left in an excited state. It will subsequently relax to
the ground state by the emission of one or more gamma rays. The gamma-
ray energies follow the well known patterns for relaxation. The only
reactions that do not produce gamma-rays are direct reactions where the
photon is absorbed and all available energy is transferred to a single
emission particle leaving the nucleus in the ground state.

Reactions at higher energies (above the pion production threshold)
require more thorough descriptions of the underlying nuclear physics.
The delta resonance and other absorption mechanisms become significant
and the

amount of energy involved in the reaction presents the opportunity for
the production of more fundamental particles. While beyond the scope of
this current work, descriptions of the relevant physics may be found in
the paper by Fasso et al. [95].

New photonuclear data tables are used to extend the traditional photon
collision routines. Because of the sparsity of photonuclear data, the
user is allowed to toggle photonuclear physics on or off (with the
fourth entry on the PHYS : p card) and the code defaults to off. Once
turned on, the total photon cross section, photoatomic plus photonuclear
(i.e. the photonuclear cross section is absent from this calculation
when photonuclear physics is off), is used to determine the distance to
the next photon collision. For simple physics, this implies the sum of
the photoelectric, pair production, incoherent and photonuclear cross
sections. Detailed physics includes the additional coherent cross
section in this sum.

The toggle for turning on and off photonuclear physics is also used to
select biased or unbiased photonuclear collisions. For the unbiased
option, the type of collision is sampled as either photonuclear or
photoatomic based on the ratio of the partial cross sections. The biased
option is similar to forced collisions. At the collision site, the
particle is split into two parts, one forced to undergo photoatomic
interaction and the other photonuclear. The weight of each particle is
adjusted by the ratio of their actual collision probability. The
photoatomic sampling routines (as described in §2.4.4.1 and §2.4.4.2)
are used to sample the emission characteristics for secondary electrons
and photons from a photoatomic collision. The emission characteristics
for secondary particles from photonuclear collisions are handled
independently.

Once it has been determined that a photon will undergo a photonuclear
collision, the emission particles are sampled as follows. First, the
appropriate collision isotope is selected based on the ratio of the
total photonuclear cross section from each relevant table. Note that
photoatomic collisions are sampled from a set of elemental tables
whereas photonuclear collisions are sampled from a set of isotopic
tables. Next, the code computes the ratio of the production cross
section to the total cross section for each secondary particle
undergoing transport. Based on this ratio, an integer number of emission
particles are sampled. If weight games (i.e. weight cutoffs or weight
windows) are being used, these secondary particles are subjected to
splitting or roulette to ensure that the sampled particles will be of an
appropriate weight. The emission parameters for each secondary particle
are then sampled independently from the reaction laws provided in the
data. Last, tallies and summary information are appropriately updated,
applicable variance reduction games are performed, and the emitted
particle is banked for further transport.

Note that photonuclear physics was implemented in the traditional Monte
Carlo style as a purely statistical based process. This means that
photons undergoing a photonuclear interaction produce an average number
of emission particles. For multiple particle emission, the particles may
not be sampled from the same reaction; for example, if two neutrons are
sampled, one may be from the ( γ, 2 n ) distributions and the second
from the ( γ, np ) distributions. Note that the photonuclear data use
the same energy/angle distributions that have been used for neutrons and
the same internal coding for sampling. See §2.4.3.5.4. This generalized
particle production method is statistically correct for large sampling
populations and lends itself to uncomplicated biasing schemes. It is
(obviously) not microscopically correct. It is not possible to perform
microscopically correct sampling given the current set of data tables.

Because of the low probability of a photon undergoing a photonuclear
interaction, the use of biased photonuclear collisions may be necessary.
However, caution should be exercised when using this option as it can
lead to large variations in particle weights. It is important to check
the summary tables to determine if appropriate weight cutoff or weight
windows have been set. That is, check to see if weight cutoffs or weight
windows are causing more particle creation and destruction than
expected. It is almost always necessary to adjust the default neutron
weight cutoff (when using only weight cutoffs with photonuclear biasing)
as it will roulette a large fraction of the attempts to create secondary
photoneutrons.

More information about the photonuclear physics included in the MCNP
code can be found in White [96, 97].

## 2.4.5 Electron Interactions

The transport of electrons and other charged particles is fundamentally
different from that of neutrons and photons. The interaction of neutral
particles is characterized by relatively infrequent isolated collisions,
with simple free flight between collisions. By contrast, the transport
of electrons is dominated by the long-range Coulomb force, resulting in
large numbers of small interactions. As an example, a neutron in
aluminum slowing down from 0.5 MeV to 0.0625 MeV will have about 30
collisions, while a photon in the same circumstances will experience
fewer than ten. An electron accomplishing the same energy loss will
undergo about 105 individual interactions. This great increase in
computational complexity makes a single-collision Monte Carlo approach
to electron transport infeasible for most situations of practical
interest.

Considerable theoretical work has been done to develop a variety of
analytic and semi-analytic multiplescattering theories for the transport
of charged particles. These theories attempt to use the fundamental
cross sections and the statistical nature of the transport process to
predict probability distributions for significant quantities, such as
energy loss and angular deflection. The most important of these theories
for the algorithms in the MCNP code are the Goudsmit-Saunderson [98]
theory for angular deflections, the Landau [99] theory of energy-loss
fluctuations, and the Blunck-Leisegang [100] enhancements of the Landau
theory. These theories rely on a variety of approximations that restrict
their applicability, so that they cannot solve the entire transport
problem. In particular, it is assumed that the energy loss is small
compared to the kinetic energy of the electron.

In order to follow an electron through a significant energy loss, it is
necessary to break the electron's path into many steps. These steps are
chosen to be long enough to encompass many collisions (so that multiple-
scattering theories are valid) but short enough that the mean energy
loss in any one step is small (so that the approximations necessary for
the multiple-scattering theories are satisfied). The energy loss and
angular deflection of the electron during each of the steps can then be
sampled from probability distributions based on the appropriate
multiple-scattering theories. This accumulation of the effects of many
individual collisions into single steps that are sampled
probabilistically constitutes the 'condensed history' Monte Carlo
method.

The most influential reference for the condensed history method is the
1963 paper by Berger [101]. Based on the techniques described in that
work, Berger and Seltzer developed the ETRAN series of electron/photon
transport codes [102]. These codes have been maintained and enhanced for
many years at the National Bureau of Standards (now the National
Institute of Standards and Technology). The ETRAN codes are also the
basis for the Integrated TIGER Series [103], a system of general-
purpose, application-oriented electron/photon transport codes developed
and maintained by Halbleib and his collaborators at Sandia National
Laboratories in Albuquerque, New Mexico. The electron physics in the
MCNP code is essentially that of the Integrated TIGER Series, Version
3.0. The ITS radiative and collisional stopping power and bremsstrahlung
production models were integrated into MCNP4C.

## 2.4.5.1 Electron Steps and Substeps

The condensed random walk for electrons can be considered in terms of a
sequence of sets of values

<!-- formula-not-decoded -->

where s n , E n , t n , u n , and r n are the total path length, energy,
time, direction, and position of the electron at the end of n steps. On
the average, the energy and path length are related by

<!-- formula-not-decoded -->

where -d E/ d s is the total stopping power in energy per unit length.
This quantity depends on energy and on the material in which the
electron is moving. ETRAN-based codes customarily choose the sequence of
path lengths { s n } such that

<!-- formula-not-decoded -->

for a constant k . The most commonly used value is k = 2 -1 / 8 , which
results in an average energy loss per step of 8.3%.

Electron steps with (energy-dependent) path lengths s = s n -s n -1
determined by Eqs. (2.140)-(2.141) are called major steps or energy
steps. The condensed random walk for electrons is structured in terms of
these energy steps. For example, all pre-calculated and tabulated data
for electrons are stored on an energy grid whose consecutive energy
values obey the ratio in Eq. (2.141). In addition, the Landau and
Blunck-Leisegang theories for energy straggling are applied once per
energy step. See §2.4.5.6 for a more detailed option. For a single step,
the angular scattering could also be calculated with satisfactory
accuracy, since the Goudsmit-Saunderson theory is valid for arbitrary
angular deflections. However, the representation of the electron's
trajectory as the result of many small steps will be more accurate if
the angular deflections are also required to be small. Therefore, the
ETRAN codes and the MCNP code further break the electron steps into
smaller substeps. A major step of path length s is divided into m
substeps, each of path length s/m . Angular deflections and the
production of secondary particles are sampled at the level of these
substeps. The integer m depends only on material (average atomic number
Z ). Appropriate values for m have been determined empirically, and
range from m = 2 for Z &lt; 6 to m = 15 for Z &gt; 91 .

In some circumstances, it may be desirable to increase the value of m
for a given material. In particular, a very small material region may
not accommodate enough substeps for an accurate simulation of the
electron's trajectory. In such cases, the user can increase the value of
m with the ESTEP option on the material card M . The user can gain some
insight into the selection of m by consulting PRINT Table 85 in the MCNP
output. Among other information, this table presents a quantity called
DRANGE as a function of energy. DRANGE is the size of an energy step in
g/cm 2 . Therefore, DRANGE/ m is the size of a substep in the same
units, and if ρ is the material density in g/cm 3 , then DRANGE/ ( mρ )
is the length of a substep in centimeters. This quantity can be compared
with the smallest dimension of a material region. A reasonable rule of
thumb is that an electron should make at least ten substeps in any
material of importance to the transport problem.

## 2.4.5.2 Condensed Random Walk

In the initiation phase of a transport calculation involving electrons,
all relevant data are either precalculated or read from the electron
data file and processed. These data include the electron energy grid,
stopping powers, electron ranges, energy step ranges, substep lengths,
and probability distributions for angular deflections and the production
of secondary particles. Although the energy grid and electron steps are
selected according to Eqs. (2.140)-(2.141), energy straggling, the
analog production of bremsstrahlung, and the intervention of geometric
boundaries and the problem time cutoff will cause the electron's energy
to depart from a simple sequence s n satisfying Eq. (2.141). Therefore,
the necessary parameters for sampling the random walk will be
interpolated from the points on the energy grid.

At the beginning of each major step, the collisional energy loss rate is
sampled (unless the logic described in §2.4.5.6 is being used). In the
absence of energy straggling, this will be a simple average value based
on the nonradiative stopping power described in the next section. In
general, however, fluctuations in the energy loss rate will occur. The
number of substeps m per energy step will have been preset, either from
the empirically determined default values, or by the user, based on
geometric considerations. At most m substeps will be taken in the
current major step with the current value for the energy loss rate. The
number of substeps may be reduced if the electron's energy falls below
the boundary of the current major step, or if the electron reaches a
geometric boundary. In these circumstances, or upon the completion of m
substeps, a new major step is begun, and the energy loss rate is
resampled.

With the possible exception of the energy loss and straggling
calculations, the detailed simulation of the electron history takes
place in the sampling of the substeps. The Goudsmit-Saunderson [98]
theory is used to sample from the distribution of angular deflections,
so that the direction of the electron can change at the end of each
substep. Based on the current energy loss rate and the substep length,
the projected energy for the electron at the end of the substep is
calculated. Finally, appropriate probability distributions are sampled
for the production of secondary particles. These include electron-
induced fluorescent X-rays, 'knock-on' electrons (from electron-impact
ionization), and bremsstrahlung photons.

Note that the length of the substep ultimately derives from the total
stopping power used in Eq. 2.140, but the projected energy loss for the
substep is based on the nonradiative stopping power. The reason for this
difference is that the sampling of bremsstrahlung photons is treated as
an essentially analog process. When a bremsstrahlung photon is generated
during a substep, the photon energy is subtracted from the projected
electron energy at the end of the substep. Thus the radiative energy
loss is explicitly taken into account, in contrast to the collisional
(nonradiative) energy loss, which is treated probabilistically and is
not correlated with the energetics of the substep. Two biasing
techniques are available to modify the sampling of bremsstrahlung
photons for subsequent transport. However, these biasing methods do not
alter the linkage between the analog bremsstrahlung energy and the
energetics of the substep.

The MCNP code uses identical physics for the transport of electrons and
positrons, but distinguishes between them for tallying purposes, and for
terminal processing. Electron and positron tracks are subject to the
usual collection of terminal conditions, including escape (entering a
region of zero importance), loss to time cutoff, loss to a variety of
variance-reduction processes, and loss to energy cutoff. The case of
energy cutoff requires special processing for positrons, which will
annihilate at rest to produce two photons, each with energy mc 2 = 0 .
511008 MeV.

## 2.4.5.3 Collisional Stopping Power

Berger [101] gives the restricted electron collisional stopping power,
i.e., the energy loss per unit path length to collisions resulting in
fractional energy transfers glyph[epsilon1] less than an arbitrary
maximum value glyph[epsilon1] m , in the form

<!-- formula-not-decoded -->

where

<!-- formula-not-decoded -->

Here glyph[epsilon1] and glyph[epsilon1] m represent energy transfers as
fractions of the electron kinetic energy E ; I is the mean ionization
potential in the same units as E ; β is v/c ; τ is the electron kinetic
energy in units of the electron rest mass; δ is the density effect
correction (related to the polarization of the medium); Z is the average
atomic number of the medium; N is the atom density of the medium in cm
-3 ; and the coefficient C is given by

<!-- formula-not-decoded -->

where m , e , and v are the rest mass, charge, and speed of the
electron, respectively. The density effect correction δ is calculated
using the prescriptions of Sternheimer, Berger and Seltzer [104] when
using data from the el03 library and using the method of Sternheimer and
Peierls [105] when using data from the el library.

The ETRAN codes and the MCNP code do not make use of restricted stopping
powers, but rather treat all collisional events in an uncorrelated,
probabilistic way. Thus, only the total energy loss to collisions is

needed, and Eqs. (2.142)-(2.143) can be evaluated for the special value
glyph[epsilon1] m = 1 / 2 . The reason for the 1 / 2 is the
indistinguishability of the two outgoing electrons. The electron with
the larger energy is, by definition, the primary. Therefore, only the
range glyph[epsilon1] &lt; 1 / 2 is of interest. With glyph[epsilon1] m = 1
/ 2 , Eq. (2.143) becomes

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

On the right side of Eq. (2.142), we can express both E and I in units
of the electron rest mass. Then E can be replaced by τ on the right side
of the equation. We also introduce supplementary constants

<!-- formula-not-decoded -->

so that Eq. (2.142) becomes

<!-- formula-not-decoded -->

This is the collisional energy loss rate in MeV/cm in a particular
medium. In the MCNP code, we are actually interested in the energy loss
rate in units of MeV barns (so that different cells containing the same
material need not have the same density). Therefore, we divide Eq.
(2.147) by N and multiply by the conversion factor 10 24 barns/cm 2 . We
also use the definition of the fine structure constant

<!-- formula-not-decoded -->

where h is Planck's constant, to eliminate the electronic charge e from
Eq. (2.147). The result is as follows:

This is the form actually used in the MCNP code to preset the
collisional stopping powers at the energy boundaries of the major energy
steps.

<!-- formula-not-decoded -->

The mean ionization potential and density effect correction depend upon
the state of the material, either gas or solid. In the fit of
Sternheimer and Peierls [105] the physical state of the material also
modifies the density effect calculation. In the Sternheimer, Berger and
Seltzer [104] treatment, the calculation of the density effect uses the
conduction state of the material to determine the contribution of the
outermost conduction electron to the ionization potential. The
occupation numbers and atomic binding energies used in the calculation
are from Carlson [106].

## 2.4.5.4 Radiative Stopping Power

The radiative stopping power is

∣ where Φ ( n ) rad is the scaled electron-nucleus radiative energy-loss
cross section based upon evaluations by Berger and Seltzer for data from
either the el or the el03 library (details of the numerical values of
the data on the el03 library can be found in [107-109]); η is a
parameter to account for the effect of electron-electron bremsstrahlung
(it is unity when using data from the el library and, when using data
from the el03 library, it is based upon the work of Seltzer and Berger
[107-109] and can be different from unity); α is the fine structure
constant; mc 2 is the mass energy of an electron; and r e is the
classical electron radius. The dimensions of the radiative stopping
power are the same as the collisional stopping power.

<!-- formula-not-decoded -->

## 2.4.5.5 Energy Straggling

Because an energy step represents the cumulative effect of many
individual random collisions, fluctuations in the energy loss rate will
occur. Thus the energy loss will not be a simple average ∆ ; rather
there will be a probability distribution f ( s, ∆)d∆ from which the
energy loss ∆ for the step of length s can be sampled. Landau [99]
studied this situation under the simplifying assumptions that the mean
energy loss for a step is small compared with the electron's energy,
that the energy parameter ξ defined below is large compared with the
mean excitation energy of the medium, that the energy loss can be
adequately computed from the Rutherford [110] cross section, and that
the formal upper limit of energy loss can be extended to infinity. With
these simplifications, Landau found that the energy loss distribution
can be expressed as

<!-- formula-not-decoded -->

in terms of φ ( λ ) , a universal function of a single scaled variable

<!-- formula-not-decoded -->

Here m and v are the mass and speed of the electron, δ is the density
effect correction, β is v/c , I is the mean excitation energy of the
medium, and γ is Euler's constant ( γ = 0 . 5772157 . . . ) . The
parameter ξ is defined by

<!-- formula-not-decoded -->

where e is the charge of the electron and NZ is the number density of
atomic electrons, and the universal function is where x is a positive
real number specifying the line of integration.

<!-- formula-not-decoded -->

For purposes of sampling, φ ( λ ) is negligible for λ &lt; -4 , so that
this range is ignored. Börsch-Supan [111] originally tabulated φ ( λ )
in the range 4 ≤ λ ≤ 100 , and derived for the range λ &gt; 100 the
asymptotic form

<!-- formula-not-decoded -->

in terms of the auxiliary variable w , where

<!-- formula-not-decoded -->

Recent extensions [57] of Börsch-Supan's tabulation have provided a
representation of the function in the range 4 ≤ λ ≤ 100 in the form of
five thousand equally probable bins in λ . In the MCNP code, the
boundaries of these bins are saved in the array eqlm(mlam) , where mlam
= 5001 . Sampling from this tabular distribution accounts for
approximately 98.96% of the cumulative probability for φ ( λ ) . For the
remaining largeλ tail of the distribution, the MCNP code uses the
approximate form φ ( λ ) ≈ w , which is easier to sample than ( w 2 + π
2 ) -1 , but is still quite accurate for λ &gt; 100 .

Blunck and Leisegang [100] have extended Landau's result to include the
second moment of the expansion of the cross section. Their result can be
expressed as a convolution of Landau's distribution with a Gaussian
distribution:

<!-- formula-not-decoded -->

Blunck and Westphal [112] provided a simple form for the variance of the
Gaussian:

<!-- formula-not-decoded -->

Subsequently, Chechin and Ermilova [113] investigated the Landau/Blunck-
Leisegang theory, and derived an estimate for the relative error

<!-- formula-not-decoded -->

caused by the neglect of higher-order moments. Based on this work,
Seltzer [114] describes and recommends a correction to the Blunck-
Westphal variance as

<!-- formula-not-decoded -->

This value for the variance of the Gaussian is used in the MCNP code.

Examination of the asymptotic form for φ ( λ ) shows that unrestricted
sampling of λ will not result in a finite mean energy loss. Therefore, a
material- and energy-dependent cutoff λ c is imposed on the sampling of
λ . In the initiation phase of an MCNP calculation, the code makes use
of two preset arrays, flam(mlanc) and avlm(mlanc) , with mlanc = 1591 .
The array flam contains candidate values for λ c in the range -4 ≤ λ c ≤
50000 ; the array avlm contains the corresponding expected mean values
for the sampling of λ . For each material and electron energy, the code
uses the known mean collisional energy loss ∆ , interpolating in this
tabular function to select a suitable value for λ c , which is then
stored in the dynamically allocated array flc . During the transport
phase of the calculation, the value of flc applicable to the current
material and electron energy is used as an upper limit, and any sampled
value of λ greater than the limit is rejected. In this way, the correct
mean energy loss is preserved.

## 2.4.5.6 Logic for Sampling Energy Straggling

The Landau theory described in the previous section provides an energy-
loss distribution determined by the energy E of the electron, the path-
length s to be traversed, and the properties of the material. Let us
symbolize a sampling of this distribution as an application of a
straggling operator L ( E,s, ∆) that provides a sampled value of the
energy loss ∆ . In the MCNP code earlier than version 5.1.40, all
parameters needed for sampling straggling were precomputed and
associated with the standard energy boundaries E n and the corresponding
ranges s n . In effect the code was restricted to calculations based on
discrete arguments of the operator L ( E n , s n , ∆ n ) . As a result,
the proper assignment of an electron transport step to an energy group n
required a rather subtle logic. Eventually, two algorithms for
apportioning straggled energy loss to electron substeps were made
available. With MCNP code version 5.1.40, a third algorithm is provided,
as discussed in §2.4.5.6.3.

## 2.4.5.6.1 Energy Indexing Algorithm in the MCNP Code

The first energy indexing algorithm (also called the 'bin-centered'
treatment) developed for the MCNP code is arguably the less successful
of the two existing algorithms, but for historical reasons remains the
default option. It was an attempt to keep the electron substeps aligned
as closely as possible with the energy groups that were used for their
straggling samples. A simplified description of the MCNP algorithm is as
follows. An electron of energy E is assigned to the group n such that E
n &gt; E ≥ E n +1 . A straggled energy loss ∆ is sampled from L ( E n , s n
, ∆ n ) . The electron attempts to traverse m substeps, each of which is
assigned the energy loss ∆ /m . If m substeps are completed, the process
starts over with the assignment of a new energy group. However, if the
electron crosses a cell boundary, or if the electron energy falls below
the current group,

the loop over m is abandoned, even if fewer than m substeps have been
completed, and the energy group is reassigned.

Since the straggling parameters are pre-computed at the midpoints of the
energy groups, this algorithm does succeed in assigning to each substep
a straggled energy loss based on parameters that are as close as
possible to the beginning energy of the substep. However, there are two
problems with the current MCNP approach. First, there is a high
probability that the electron will not actually complete the expected
range s n for which the energy loss was sampled, in which case the
energy loss relies on a linear interpolation in a theory that is clearly
nonlinear. Second, the final substep of each sequence using the sampled
energy loss from L ( E n , s n , ∆ n ) will frequently fall partially in
the next-lower energy group n +1 , but no substep using the sample from
L ( E n , s n , ∆ n ) will ever be partially in the higher group n -1 .

## /warning\_sign Caution

This results in a small, but potentially significant, systematic error.

See for example the investigations of Schaart et al. [115] and
references therein.

## 2.4.5.6.2 Energy Indexing Algorithm in the ITS Code

Developed for the ITS codes earlier than the MCNP algorithm, this method
(also called the 'nearest-groupboundary' treatment) was added to the
MCNP code in order to explore some of the energy-dependent artifacts of
the condensed history approach, and in order to offer more consistency
with the TIGER Series codes. This algorithm differs from the default
treatment in two ways. First, the electron is initially assigned to a
group n such that

In other words, the electron is assigned to the group whose upper limit
is closest to the electron's energy. Second, although the electron will
be reassigned when it enters a new geometric cell, it will not be
reassigned merely for falling out of the current energy group. These
differences serve to reduce the number of times that unwanted imposition
of linear interpolation on partial steps occurs, and to allow more equal
numbers of excursions above and below the energy group from which the
Landau sampling was made. As [115] shows, these advantages make the ITS
algorithm a more accurate representation of the energy loss process, as
indicated in comparisons with reference calculations and experiments.
Nevertheless, although the reliance on linear interpolation and the
systematic errors are reduced, neither is completely eliminated. It is
straightforward to create example calculations that show unphysical
artifacts in the ITS algorithm as well as in the MCNP logic.

<!-- formula-not-decoded -->

The 'nearest-group-boundary' treatment is selected by setting the 18th
entry of the DBCN card to 1. For example, the card ' DBCN 17J 1 '
selects this straggling logic without affecting any of the other DBCN
options.

## 2.4.5.6.3 New Energy- and Step-specific Method

It is easy to express what we would like to see in the straggling logic.
For an electron with energy E about to traverse a step of length s , we
would like to sample the straggling from the operator L ( E,s, ∆ )
without regard to the prearranged energy boundaries E n . In the MCNP
code, version 5.1.40, we have now brought this situation about. A new
Fortran 90 module has been installed to deal with straggling data. Those
parameters that are separate from the individual straggling events are
still precomputed, but each electron transport step can now sample its
energy loss separately from adjacent steps, and specifically for its
current energy and planned step length. Using this approach, we largely
eliminate the linear interpolations and energy misalignments of the
earlier algorithms and obviate the need for a choice of energy group. As
of the MCNP

code, version 5.1.40, the new straggling logic is included in the code,
but is still being tested. Preliminary results [116] indicate that a
more accurate and stable estimate of the straggling is obtained, and a
variety of unphysical artifacts are eliminated.

The new logic is selected by setting the 18th entry of the DBCN card to
2, for example with the card ' DBCN 17J 2 '.

## 2.4.5.7 Angular Deflections

The ETRAN codes and the MCNP code rely on the Goudsmit-Saunderson [98]
theory for the probability distribution of angular deflections. The
angular deflection of the electron is sampled once per substep according
to the distribution where s is the length of the substep, µ = cos( θ )
is the angular deflection from the direction at the beginning of the
substep, P l ( µ ) is the l th Legendre polynomial, and G l is

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

in terms of the microscopic cross section d σ/ dΩ , and the atom density
N of the medium.

For electrons with energies below 0.256 MeV, the microscopic cross
section is taken from numerical tabulations developed from the work of
Riley [117]. For higher-energy electrons, the microscopic cross section
is approximated as a combination of the Mott [118] and Rutherford [110]
cross sections, with a screening correction. Seltzer [102] presents this
'factored cross section' in the form

<!-- formula-not-decoded -->

where e , p , and v are the charge, momentum, and speed of the electron,
respectively. The screening correction η was originally given by Molière
[119] as

<!-- formula-not-decoded -->

where α is the fine structure constant, m is the rest mass of the
electron, and β = v/c . The MCNP code now follows the recommendation of
Seltzer [102], and the implementation in the Integrated TIGER Series, by
using the slightly modified form

<!-- formula-not-decoded -->

where τ is the electron energy in units of electron rest mass. The
multiplicative factor in the final term is an empirical correction which
improves the agreement at low energies between the factored cross
section and the more accurate partial-wave cross sections of Riley.

## 2.4.5.8 Bremsstrahlung

When using data from the el library, for the sampling of bremsstrahlung
photons, the MCNP code relies primarily on the Bethe-Heitler [120] Born-
approximation results that have been used until rather recently [107] in
ETRAN. A comprehensive review of bremsstrahlung formulas and
approximations relevant to the present level of the theory in the MCNP
code can be found in the paper of Koch and Motz [121]. Particular
prescriptions appropriate to Monte Carlo calculations have been
developed by Berger and Seltzer [122]. For the ETRAN-based codes, this
body of data has been converted to tables including bremsstrahlung
production probabilities, photon energy distributions, and photon
angular distributions.

For data tables on the el03 library, the production cross section for
bremsstrahlung photons and energy spectra are from the evaluation by
Seltzer and Berger [107-109]. The evaluation uses detailed calculations
of the electron-nucleus bremsstrahlung cross section for electrons with
energies below 2 MeV and above 50 MeV. The evaluation below 2 MeV uses
the results of Pratt, Tseng, and collaborators, based on numerical
phase-shift calculations [123-126]. For 50 MeV and above, the analytical
theory of Davies, Bethe, Maximom, and Olsen [127, 128] is used and is
supplemented by the Elwert-Coulomb [129] correction factor and the
theory of the high-frequency limit or tip region given by Jabbur and
Pratt [130, 131]. Screening effects are accounted for by the use of
Hartree-Fock atomic form factors [86, 132]. The values between these
firmly grounded theoretical limits are found by a cubic-spline
interpolation as described in [107, 108]. Seltzer reports good agreement
between interpolated values and those calculated by Tseng and Pratt
[133] for 5- and 10-MeV electrons in aluminum and uranium. Electron-
electron bremsstrahlung is also included in the cross-section evaluation
based on the theory of Haug [134] with screening corrections derived
from Hartree-Fock incoherent scattering factors [86, 132]. The energy
spectra for the bremsstrahlung photons are provided in the evaluation.
No major changes were made to the tabular angular distributions, which
are internally calculated when using the el library, except to make
finer energy bins over which the distribution is calculated.

The MCNP code addresses the sampling of bremsstrahlung photons at each
electron substep. The tables of production probabilities are used to
determine whether a bremsstrahlung photon will be created. For data from
the el03 library, the bremsstrahlung production is sampled according to
a Poisson distribution along the step so that none, one or more photons
could be produced; the el library allows for either none or one
bremsstrahlung photon in a substep. If a photon is produced, the new
photon energy is sampled from the energy distribution tables. By
default, the angular deflection of the photon from the direction of the
electron is also sampled from the tabular data. The direction of the
electron is unaffected by the generation of the photon because the
angular deflection of the electron is controlled by the multiple
scattering theory. However, the energy of the electron at the end of the
substep is reduced by the energy of the sampled photon because the
treatment of electron energy loss, with or without straggling, is based
only on non-radiative processes.

There is an alternative to the use of tabular data for the angular
distribution of bremsstrahlung photons. If the fourth entry on the PHYS
: e card is 1, then the simple, material-independent probability
distribution

<!-- formula-not-decoded -->

where µ = cos( θ ) and β = v/c , will be used to sample for the angle of
the photon relative to the direction of the electron according to the
formula where ξ is a random number drawn from the unit interval. This
sampling method is of interest only in the context of detectors and
DXTRAN spheres. A set of source contribution probabilities p ( µ )
consistent with the tabular data is not available. Therefore, detector
and DXTRAN source contributions are made using Eq. (2.167). Specifying
that the generation of bremsstrahlung photons rely on Eq. (2.167) allows
the user to force the actual transport to be consistent with the source
contributions to detectors and DXTRAN.

<!-- formula-not-decoded -->

## 2.4.5.9 K-shell Electron Impact Ionization and Auger Transitions

Data tables in the el03 library use the same K-shell impact ionization
calculation (based upon ITS1.0) as data tables on the el library, except
for how the emission of relaxation photons is treated; the el03
evaluation model has been modified to be consistent with the photo-
ionization relaxation model. In the el evaluation, a K-shell impact
ionization event generated a photon with the average K-shell energy. The
el03 evaluation generates photons with energies given by Everett and
Cashwell [50]. Both el03 and el treatments only take into account the
highest Z component of a material. Thus inclusion of trace high Z
impurities could mask K-shell impact ionization from other dominant
components.

Auger transitions are handled the same for data tables from the el03 and
el libraries. If an atom has undergone an ionizing transition and can
undergo a relaxation, if it does not emit a photon it will emit an Auger
electron. The difference between el and el03 is the energy with which an
Auger electron is emitted, given by E A = E K or E A = E K -2 E L for el
or el03 , respectively. The el value is that of the highest energy Auger
electron while the el03 value is the energy of the most probable Auger
electron. It should be noted that both models are somewhat crude.

## 2.4.5.10 Knock-on Electrons

The Møller cross section [135] for scattering of an electron by an
electron is

<!-- formula-not-decoded -->

where glyph[epsilon1] , τ , E , and C have the same meanings as in Eqs.
(2.142)-(2.145). When calculating stopping powers, one is interested in
all possible energy transfers. However, for the sampling of
transportable secondary particles, one wants the probability of energy
transfers greater than some glyph[epsilon1] c representing an energy
cutoff, below which secondary particles will not be followed. This
probability can be written

<!-- formula-not-decoded -->

The reason for the upper limit of 1 / 2 is the same as in the discussion
of Eq. (2.145). Explicit integration of Eq. (2.169) leads to

<!-- formula-not-decoded -->

Then the normalized probability distribution for the generation of
secondary electrons with glyph[epsilon1] &gt; glyph[epsilon1] c is given by

<!-- formula-not-decoded -->

At each electron substep, the MCNP code uses σ ( glyph[epsilon1] c ) to
determine randomly whether knock-on electrons will be generated. If so,
the distribution of Eq. (2.172) is used to sample the energy of each
secondary electron. Once an energy has been sampled, the angle between
the primary direction and the direction of the newly generated secondary
particle is determined by momentum conservation. This angular deflection
is used for the subsequent transport of the secondary electron. However,
neither the energy nor the direction of the primary electron is altered
by the sampling of the secondary particle. On the average, both the
energy loss and the angular deflection of the primary electron have been
taken into account by the multiple scattering theories.
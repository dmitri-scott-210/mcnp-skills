---
title: "Chapter 2.5 - Tallies"
chapter: "2.5"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/2_Geometry,_Data,_Physics,_and_Mathematics/2.5_Tallies.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

Table 2.2: Tally Quantities Scored.

| Tally   | Description               | Score                        | Physical Quantity                                                                                 | Units          |
|---------|---------------------------|------------------------------|---------------------------------------------------------------------------------------------------|----------------|
| F1      | surface current           | W                            | J = GLYPH<1> d E GLYPH<1> d t GLYPH<1> d A GLYPH<1> dΩ | Ω · n | ψ ( r , Ω ,E,t )                 | particles      |
| F2      | surface fluence           | W | µ | A                    | φ S = 1 A GLYPH<1> d E GLYPH<1> d t GLYPH<1> d A GLYPH<1> dΩ ψ ( r , Ω ,E,t )                     | particles/cm 2 |
| F4      | cell fluence              | W T l V                      | φ V = 1 V GLYPH<1> d E GLYPH<1> d t GLYPH<1> d V GLYPH<1> dΩ ψ ( r , Ω ,E,t )                     | particles/cm 2 |
| F5      | detector fluence          | W · p ( Ω P ) exp( - λ ) L 2 | φ P = GLYPH<1> d E GLYPH<1> d t GLYPH<1> dΩ ψ ( r P , Ω ,E,t )                                    | particles/cm 2 |
| F6      | energy deposition         | WT l σ t ( E ) H ( E ) ρ a m | H t = ρ a m GLYPH<1> d E GLYPH<1> d t GLYPH<1> d V GLYPH<1> dΩ σ t ( E ) H ( E ) ψ ( r , Ω ,E,t ) | MeV/g          |
| F7      | fission-energy deposition | WT l σ f ( E ) Q ρ a m       | H f = ρ a m Q GLYPH<1> d E GLYPH<1> d t GLYPH<1> d V GLYPH<1> dΩ σ f ( E ) ψ ( r , Ω ,E,t )       | MeV/g          |
| F8      | pulse-height tally        | W C put in bin E D           | pulses                                                                                            | pulses         |

## 2.4.5.11 Multigroup Boltzmann-Fokker-Planck Electron Transport

The electron physics described above can be implemented into a
multigroup form using a hybrid multigroup and continuous-energy method
for solving the Boltzmann-Fokker-Planck equation as described by Morel
[60]. The multigroup formalism for performing charged particle transport
was pioneered by Morel and Lorence [61-63] for use in deterministic
transport codes. With a first-order treatment for the continuous slowing
down approximation (CSDA) operator, this formalism is equally applicable
to a standard Monte Carlo multigroup transport code as discussed by
Sloan [136]. Unfortunately, a first-order treatment is not adequate for
many applications. Morel, et al. have addressed this difficulty by
developing a hybrid multigroup/continuous energy algorithm for charged
particles that retains the standard multigroup treatment for large-angle
scattering, but treats exactly the CSDA operator. As with standard
multigroup algorithms, adjoint calculations are performed readily with
the hybrid scheme.

The process for performing an MCNP/MGBFP calculation for electron/photon
transport problems involves executing three codes. First the CEPXS
[61-63] code is used to generate coupled electron-photon multigroup
cross sections. Next the CRSRD code casts these cross sections into a
form suitable for use in the MCNP code by adjusting the discrete
ordinate moments into a Radau quadrature form that can be used by a
Monte Carlo code. CRSRD also generates a set of multigroup response
functions for dose or charge deposition that can be used for response
estimates for a forward calculation or for sources in an adjoint
calculation. Finally, the MCNP code is executed using these adjusted
multigroup cross sections. Some applications of this capability for
electron/photon transport have been presented in [137].

## 2.5 Tallies

The MCNP code automatically creates standard summary information that
gives the user a better insight into the physics of the problem and the
adequacy of the Monte Carlo simulation including: a complete accounting
of the creation and loss of all tracks and their energy; the number of
tracks entering and reentering a cell plus the track population in the
cell; the number of collisions in a cell; the average weight, mean free
path, and energy of tracks in a cell; the activity of each nuclide in a
cell (that is, how particles interacted with each nuclide, not the
radioactivity); and a complete weight balance for each cell.

The MCNP code also provides seven standard tally types that can be
specified in an MCNP input file by using F cards (see §5.9 for the tally
type specification). These tallies are normalized to be per source
particle unless a different normalization has been specified with the
WGT keyword on the SDEF card, changed by the user with a TALLYX
subroutine, and by weight in a criticality ( KCODE ) calculation. The
MCNP tally plotter provides graphical displays of the results (see
§6.3). The seven standard tally quantities actually scored in the MCNP
code before the final normalization are presented in Table 2.2. The
table also gives the physical quantity that corresponds to each tally,
and it defines much of the notation used in the remainder of this
section. The F2 , F4 , and F5 tallies in Table 2.2 are described as
fluence tallies with the associated units. However, depending

on the source units, these may also be fluence rate (i.e., flux) tallies
with units of particles / ( cm 2 · s ) . For Table 2.2, the variables
used are

- W particle weight,
- W C collective weight from a history for pulse-height tally [§2.5.5],
- r , Ω , E, t particle position vector (cm), direction unit vector, energy (MeV), and time (shakes, sh; 1 sh = 10 -8 s),
- µ Ω · n , cosine of angle between surface normal n and particle trajectory Ω ,
- A,V surface area (cm 2 ) and volume (cm 3 ), calculated by the code or input by the user,
- T l track length (cm), event transit time multiplied by the particle velocity,
- p ( Ω P ) probability density function for scattering (or starting) in the direction Ω P towards the point detector (azimuthal symmetry is assumed),
- λ total number of mean free paths from particle location to detector (i.e., the optical distance),
- L distance to detector from the source or collision event (cm),
- σ t ( E ) microscopic total cross section (barns),
- σ f ( E ) microscopic fission cross section (barns),
- H ( E ) heating number (MeV/collision),
- E D total energy deposited by a history in a detector (MeV); see [§2.5.5],
- ρ a atom density (atoms/barn-cm),
- ρ g mass density (g/cm 3 ); not used in Table 2.2 but used later in this chapter,
- m cell mass (g),
- Q total prompt energy release per fission (MeV),
- ψ angular flux as typically defined in nuclear reactor theory [78, 138]; ψ ( r , Ω , E, t ) = vn ( r , Ω , E, t ) , where n is the particle density (particles/cm 3 /MeV/steradian) and v is the velocity (cm/sh), so the units of ψ are particles/cm 2 /sh/MeV/steradian,
- J total (not net) current crossing a surface,
- φ S average flux on a surface,
- φ V average flux in a cell (i.e., in a volume),
- φ P flux at a point,
- r P point at which φ P is estimated (i.e., the location of the point detector),
- H t total energy deposition in a cell (MeV/g),
- H f total fission energy deposition in a cell (MeV/g).

Table 2.3: Tallies Modified with an Asterisk or Plus.

| Tally   | Scores                                                     | Units    |
|---------|------------------------------------------------------------|----------|
| *F1     | WE                                                         | MeV      |
| *F2     | WE | µ | A                                                 | MeV/cm 2 |
| *F4     | W T l E V                                                  | MeV/cm 2 |
| *F5     | W · p ( Ω P ) exp( - λ ) E L 2                             | MeV/cm 2 |
| *F6     | 1 . 60219 × 10 - 22 jerks MeV WT l σ t ( E ) H ( E ) ρ a m | jerks/g  |
| +F6     | total energy deposition from all particles                 | MeV/g    |
| *F7     | 1 . 60219 × 10 - 22 jerks MeV WT l σ f ( E ) Q ρ a m       | jerks/g  |
| *F8     | E D × W C put in bin E D                                   | MeV      |
| +F8     | ± W C put in bin E D                                       | charge   |

The units of each tally are derived from the units of the source. If the
source has units of particles per unit time, current tallies are
particles per unit time and flux tallies are particles per unit time per
unit area. When the source has units of particles, current tallies have
units of particles and flux tallies actually represent fluences with
units of particles per unit area. A steady-state flux solution can be
obtained by having a source with units of particles per unit time and
integrating the tally over all time (that is, omitting the T n card).
The average flux in a time bin can be obtained from the fluence tally
for a time-dependent source by dividing the tally by the time bin width
in shakes. These tallies can all be made per unit energy by dividing
each energy bin by the energy bin width.

Adding an asterisk ( * F n ) changes the units into an energy tally and
multiplies each tally as indicated in Table 2.3. For an F8 pulse height
tally, the asterisk changes the tally from deposition of pulses to an
energy deposition tally. A plus sign can only be used with F6 and F8
cards. A +F6 tally is a total energy position tally from all particles
(2.5.3) and a +F8 tally is a charge deposition tally.

Extensive statistical analysis of tally convergence is applied to the
tally fluctuation bin of each tally [§5.9.19]. Ten statistical checks
are made, including the variance of the variance and the Pareto slope of
the history score probability density function. These checks are
described in §2.6.

In addition to the standard tallies, the MCNP code has superimposed mesh
tallies. This feature allows the user to tally particles on a mesh
independent of the problem geometry. Track-length quantities such as
fluence, heating, energy deposition, point-detector and DXTRAN sphere
contribution rays or other data such as source points can be calculated.
Mesh tallies are invoked by using the FMESH and TMESH cards. When a
track-length quantity is computed over the mesh tally cells, it is
typically normalized to be per starting particle, except in KCODE
criticality calculations.

Not all features of the standard tallies have been implemented in the
mesh tallies. For example, no tally fluctuation statistics are given for
mesh tallies; the only error information provided is the relative error
for each mesh cell. Features that can be used with the mesh tallies are
multiplying the result by the particle energy ( * FMESH card), dose
functions, and tally multipliers. Time binning is not a feature of the
TMESH tally.

The definitions of the current and flux in the sections that follow come
from nuclear reactor theory [78, 138] but are related to similar
quantities in radiative transfer theory [139, 140]. The MCNP angular
flux multiplied by the particle energy is the same as the intensity in
radiative transfer theory. The MCNP total flux at energy E multiplied by
the particle energy E equals the integrated energy density times the
speed of light in radiative transfer theory. The MCNP current multiplied
by the particle energy is analogous to the radiative flux crossing an
area in radiative transfer theory. The MCNP particle fluence multiplied
by the particle energy is the same as the fluence in radiative transfer
theory.

<!-- image -->

|

·

|

Figure 2.7: Diagram for description of the surface current tally.

Nuclear reactor theory has given the terms flux and current quite
different meanings [78, 138] than they have in other branches of
physics; terminology from other fields should not be confused with that
used in this manual.

Rigorous mathematical derivations of the basic tallies are given in
[141]. Somewhat heuristic derivations follow. Note that the surface
current is a total but the cell and surface fluxes are averages.

## 2.5.1 Surface Current Tally

The surface current ( F1 ) tally is a simple count of the number of
particles, represented by the Monte Carlo weight, crossing a surface in
specified bins as illustrated in Figure 2.7. The number of particles at
time t , in a volume element d r , with directions within dΩ , and
energies within d E is n ( r , Ω , E, t )d r dΩd E . Let the volume
element d r contain the surface element d A (with surface normal n ) and
along Ω for a distance v d t , as depicted in Figure 2.7. Then the
differential volume element is d r = v d t | Ω · n | d A . All the
particles within this volume element (with directions within dΩ and
energies within d E ) will cross surface d A in time d t . Thus, the
number of particles crossing surface d A in time d t is | Ω · n | vn ( r
, Ω , E, t )dΩd E d t d A . The number of particles crossing surface A
in energy bin i , time bin j , and angle bin k is thus

<!-- formula-not-decoded -->

The range of integration over energy, time, and angle (cosine) is
controlled by E , T , and C cards. If the range of integration is over
all angles (no C card), then the surface current tally is a count of the
number of particles with any trajectory crossing the surface (in each
energy and time bin) and thus has no direction associated with it.

Note that the MCNP current J of Table 2.2 is the total current and not
the net current. It is the total number of particles crossing a surface.
Frequently, the net current, rather than the total current, is desired.
Defining the partial currents crossing in the positive and negative
directions ('right' and 'left' or 'up' and 'down') as [138]

<!-- formula-not-decoded -->

where the net current across the surface is J net = J + -J -. The total
current of Table 2.2 is J net = J + + J -. The partial currents J ±
across a surface can be calculated in the MCNP code using the surface
current tally with two cosine bins, one each for 1 ≤ µ &lt; 0 and 0 &lt; µ ≤ 1
.

The units of the surface current tally are those of the source. If the
source has units of particles per unit time, the tally has units of
particles per unit time. When the source has units of particles, the
tally has units of particles. The SD card can be used to input a
constant that divides the tally. In other words, if x is input on the SD
card, the tally will be divided by x .

## 2.5.2 Flux Tallies

Defining the scalar flux as φ ( r , E, t ) ≡ GLYPH&lt;1&gt; dΩ ψ ( r , Ω , E,
t ) where φ ( r , E, t )d r d E is the total scalar flux in volume
element d r about r and energy element d E about E and, introducing
energy and time bins, the integrals of Table 2.2 for the surface flux (
F2 ), cell flux ( F4 ), and detector flux ( F5 ) tallies can be recast
as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The range of integration over energy and time can be tailored by E and T
cards. If no E card is present, the integration limits are the same as
the limits for the corresponding cross sections used. The cell flux and
surface flux tallies are discussed in this section. The detector flux
tally is discussed in §2.5.6.

## 2.5.2.1 Track-length Estimate of Cell Flux

The average particle flux in a cell (from Table 2.2) can be written

<!-- formula-not-decoded -->

where N ( r , E, t ) = GLYPH&lt;1&gt; dΩ n ( r , Ω , E, t ) is the density of
particles, regardless of their trajectories, at a point. Defining d s to
be the differential unit of track length and noting that d s = v d t
yields

<!-- formula-not-decoded -->

The quantity N ( r , E, t )d s may be thought of as a track-length
density; thus, the average flux can be estimated by summing track
lengths. The MCNP code estimates φ V by summing WT l /V for all particle
tracks in the cell. Time- and energy-dependent subdivisions of φ V are
made by binning the track lengths in appropriate time and energy bins.
The track length estimator is generally quite reliable because there are
frequently many tracks in a cell (compared to the number of collisions),
leading to many contributions to this tally.

The SD card can be used to input a new volume that divides the tally. In
other words, if V ′ is input on the SD card, the tally will be divided
by V ′ instead of V . See the SD card information on how the MCNP code
can handle the volumes used to compute the tallies.

n

Figure 2.8: Diagram for description of the surface flux tally.

<!-- image -->

## 2.5.2.2 Surface Flux

The average particle scalar flux on a surface ( φ S of Table 2.2) is
estimated using a surface crossing estimator that may be thought of as
the limiting case of the cell flux or track length estimator when the
cell becomes infinitely thin, as illustrated in Figure 2.8.

As the cell thickness δ approaches zero, the cell volume approaches Aδ
and the track length through the cell approaches δ/ | Ω · n | . Thus,

<!-- formula-not-decoded -->

A more formal derivation of the surface flux estimator may be found in
[141].

For particles grazing the surface, 1 / | µ | is very large and the MCNP
code approximates the surface flux estimator in order to ensuring a
finite variance for the sampled population.

## /warning\_sign Caution

An unmodified surface flux estimator has an infinite variance when 1 / |
µ | is very large, and thus confidence intervals could not be formed via
the central limit theorem because the central limit theorem requires a
finite variance. For this reason, the MCNP code sets µ = 0 . 0005 when µ
&lt; 0 . 001 ; because of this approximation, the F2 surface flux tally is
not an exact estimate of the surface flux. This value can be adjusted
with the 24th entry on the DBCN card.

The SD card can be used to input a new area that divides the tally. In
other words, if A ′ is input on the SD card, the tally will be divided
by A ′ instead of A . See information in the SD card section on how the
MCNP code handles the areas used by the tallies.

The surface flux tally is essential for stochastic calculation of
surface areas when the normal analytic procedure fails [§2.9.2].

## 2.5.3 Energy Deposition Tally

The energy-deposition family of tallies are used to estimate cell
heating. The F6 and TMESH cards can be used to tally energy deposition;
the F6 card is for a cell-based tally and the TMESH card is for a mesh-
based

tally. The F6 card provides the energy deposition for a single particle
type in units of MeV/g per source particle. The * F6 card is equivalent
to the F6 card except in units of jerks/g per source particle (1 MeV = 1
. 60219 × 10 -22 jerks). The +F6 card provides an estimate of the total
energy deposition from all particles. These tallies are implemented as
hybrid track-length and collision tallies. The mass normalization of the
cell-based energy deposition tally can be adjusted by the SD card.
Multiple particles can be listed as follows: F6 : p , n .

These tallies operate slightly differently depending on the incident
particle, the MODE card, and if model physics are used. An overview is
listed in Table 2.4. The heating numbers, which are the probability of a
reaction multiplied by all kinetic energy carried away by the secondary
particles, are generated by NJOY [12].

## /warning\_sign Caution

The use of heating numbers can result in negative energy deposition
tallies in two cases. First, in the case in which collision tallies are
used to subtract energies of secondary particles, this can result in
negative +F6 tallies when the tally is undersampled. Second, older data
may have poor separation of neutron and photon heating resulting in one
of the two having negative values. The total energy deposition is still
consistent in this second case.

## /warning\_sign Caution

The way the MCNP code handles F6 tallies results in double counting in a
variety of cases, such as with a combination of photons and electrons,
or with light ion recoil. As such, the sum of F6 tallies should not be
used, with the exception of F6 : n + F6 : p which are designed to be
compatible. For total energy deposition, +F6 should be considered
instead.

This hybrid tallying approach was designed to minimize the cost of
computing energy deposition for neutral particle problems. As the
charged-particle contribution is contained within the neutral particle
components, one does not need to simulate charged particles to get
reasonable estimates. However, the use of heating numbers results in a
number of caveats that one should be aware of:

1. The energy from non-transported secondary charged particles is deposited along the track (for projectiles with heating numbers) or at the point of collision (for everything else). If the mean free path of these secondary products would have been larger than the geometry of interest and as a result would have been deposited elsewhere, this can result in incorrect energy deposition.
2. Heating numbers ignore the energy deposition from secondary particles undergoing further reactions beyond slowing down.
3. Photonuclear reactions are not included in the photon data.
4. Heating from radioactive decay is not included.

The first three caveats can be remedied by adjusting the MODE and PHYS
cards to include the necessary particles and physics. The more
comprehensive both are, the more accurate energy deposition will be.

Radioactive decay is partially handled by the MCNP code in a variety of
ways. Using TOTNU on (default), delayed neutrons from fission will be
produced and transported, and will deposit energy in the same fashion as
prompt neutrons. The generation of delayed neutrons from capture, as
well as generation of other particles, is done via the ACT card.

With these caveats and remedies in mind, there are a few rules of thumb
for computing accurate energy deposition:

Table 2.4: Physics-dependent Energy Deposition Methods

| Neutrons                |                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                         | Table Physics                                                                                                                                                                                                                                                                                                                                                                          | Track-length tallies are performed using heating numbers. These heating numbers include the kinetic energy for all secondary particles except photons. If available, the partial heating numbers of particles on the MODE card are removed to ensure consistency. If not, the energy of the secondary particle is subtracted out from only the +F6 tally at the point of collision. This second case typically occurs during light ion recoil.                                                                                                  |
|                         | Model Physics                                                                                                                                                                                                                                                                                                                                                                          | Kinematics are tallied using collision tallies.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Photons                 |                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|                         | Table Physics                                                                                                                                                                                                                                                                                                                                                                          | Track-length tallies are performed using heating numbers. These heating numbers include the kinetic energy for all secondary particles except neutrons. For secondary parti- cles other than neutrons and electrons, energy balance is achieved using the same approach as for tabular neutrons above. Electron heating is never removed from the heating number. As such, F6 : p and F6 : e will double count the elec- tron contribution. For +F6 tallies, kinematic collision tallies are used for photons instead to guarantee consistency. |
|                         | Model Physics                                                                                                                                                                                                                                                                                                                                                                          | Kinematics are tallied using collision tallies.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Charged Particles       | The slowing down energy deposition is tallied by taking the start energy and end energy of a track and performing a track-length tally assuming a constant dE/dx . For cell-based tallies, this results in no approximation as particles will always stop at a surface crossing. For mesh-based tallies, this can lead to localized inconsistencies between neighboring mesh elements. | The slowing down energy deposition is tallied by taking the start energy and end energy of a track and performing a track-length tally assuming a constant dE/dx . For cell-based tallies, this results in no approximation as particles will always stop at a surface crossing. For mesh-based tallies, this can lead to localized inconsistencies between neighboring mesh elements.                                                                                                                                                          |
|                         | Table Physics (proton only)                                                                                                                                                                                                                                                                                                                                                            | Table Physics (proton only)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                         |                                                                                                                                                                                                                                                                                                                                                                                        | Track-length tallies are performed using heating numbers. These heating numbers include the kinetic energy for all secondary particles. Energy balance is achieved using the same approach as for tabular neutrons above.                                                                                                                                                                                                                                                                                                                       |
|                         | Model Physics                                                                                                                                                                                                                                                                                                                                                                          | Kinematics are tallied using collision tallies. If neutral daughter products (which includes neutrons, photons, neu- trinos, π 0 , and neutral kaons) are not on the MODE card, their energy will not be deposited.                                                                                                                                                                                                                                                                                                                             |
| Other Neutral Particles |                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|                         | Kinematics are tallied using collision tallies. If neutral daughter products (which includes neutrons, photons, neutrinos, π 0 , and neutral kaons) are not on the MODE card, their energy will not be deposited.                                                                                                                                                                      | Kinematics are tallied using collision tallies. If neutral daughter products (which includes neutrons, photons, neutrinos, π 0 , and neutral kaons) are not on the MODE card, their energy will not be deposited.                                                                                                                                                                                                                                                                                                                               |

1

2

3

4

5

6

7

8

9

10

11

12

1. For low energy neutron sources and k -eigenvalue problems, a MODE n p , F6 : n + F6 : p or +F6 tally will provide reasonably accurate prompt total + fission delay neutron energy deposition values.
2. For low energy photon fixed-source problems, MODE p , F6 : p or +F6 will provide reasonably accurate energy deposition. One should enable photofission if necessary.
3. The ACT card can allow computing non-fission delayed neutrons and other delayed particles. It can only be used for fixed-source simulations.
4. If the geometry is thin relative to the mean free path of generated secondary particles (such as electrons from photons, or recoil nuclei from any nuclear reaction), and the energy deposition in this component is important, one should add those particles to the simulation and use +F6 tallies to prevent doublecounting energy deposition. In addition, light ion recoil may need to be enabled (see the PHYS : n and PHYS : h cards) for some problems.
5. If a given particle type is expected to undergo important reactions beyond slowing down, it should be added to the simulation.
6. If neutral particles can be generated, they should be included on the MODE card or the energy will not be tracked.

## 2.5.4 Track-length Fission Energy Deposition

The fission-energy deposition ( F7 ) tally is a track-length estimate of
neutron-induced fission energy deposition, and is given in units of
MeV/g per source particle. The * F7 tally is identical to the F7 tally,
but converted to jerks/g per source particle (see Table 2.2 and Table
2.3). The Q values used to compute F7 tallies are printed in PRINT Table
98 in an MCNP output file.

## 2.5.4.1 Equivalence of F4, F6, and F7 Tallies

For neutrons and photons, the F6 and F7 heating tallies are special
cases of the F4 track length estimate of cell flux with energy-dependent
multipliers. The tally combinations given in Listing give equivalent
results.

Listing 2.2: tally\_equivalence.mcnp.inp.txt

<!-- image -->

| c Tally Definitions    |
|------------------------|
| f14:n 1                |
| fm14 0.0025621 9 1 -4  |
| f16:n 1                |
| c                      |
| f24:n 1                |
| fm24 0.0025621 9 -6 -8 |
| f27:n 1                |
| c                      |
| f34:p 1                |
| fm34 0.0025621 9 -5 -6 |
| f36:p 1                |

That is, the F14 / FM14 and F16 tallies are equivalent, the F24 / FM24
and F27 tallies are equivalent, and the F34 / FM34 and F36 tallies are
equivalent. In this example, material 9 in cell 1 is 235 U with an atom
density ( ρ a ) of 0.02 atoms/barn-cm and a mass density ( ρ g ) of
7.80612 g/cm 3 for an atom/gram ratio of 0.0025621. Note that using -1
/ρ g will give the same result as using ρ a /ρ g and is a better choice
if perturbations are used. For more information on perturbations see
§2.12.

1

For the photon results to be identical, both electron transport and the
thick-target bremsstrahlung approximation ( PHYS : p j 1 must be turned
off. In the F6 : p tally, if a photon produces an electron that produces
a photon, the second photon is not counted again. It is already tallied
in the first photon heating. In the F 4 : p tally, the second photon
track is counted, so the F4 tally will slightly overpredict the tally.

The photon heating tally also can be checked against the * F8 energy
deposition tally by dividing the F6 tally by a unit mass with the SD
card. Results will only be statistically identical because the tallies
are totally independent and use different estimators. The FM card can
also be used to make the surface flux tally ( F2 ) and point and ring
detector tallies ( F5 ) calculate heating, on a surface or at a point,
respectively.

## 2.5.5 Pulse-height Tallies

The pulse height tally provides the energy distribution of pulses
created in a cell that models a physical detector. It also can provide
the energy deposition in a cell. Although the entries on the F8 card are
cells, this is not a track length cell tally. The pulse-height tallies
are made at source points and at surface crossings. The * F8 card
changes the tally from deposition of pulses to an energy deposition
tally and the +F8 card changes the tally to a charge deposition tally.
The pulse height tally is analogous to a physical detector. The F8
energy bins ( E D ) correspond to the total energy deposited in a
detector in the specified channels by each computational particle
(history). All the other MCNP tallies record the energy of a scoring
track in the energy bin.

In an experimental configuration, suppose a source emits 100 photons at
10 MeV, and ten of these get to the detector cell. Further, suppose that
the first photon (and any of its progeny created in the cell) deposits 1
keV in the detector before escaping, the second deposits 2 keV, and so
on up to the tenth photon which deposits 10 keV. Then the pulse height
measurement at the detector would be one pulse in the 1-keV energy bin,
1 pulse in the 2-keV energy bin, and so on up to 1 pulse in the 10-keV
bin.

In the analogous MCNP pulse height tally, the source cell is credited
with the energy times the weight of the source particle. When a particle
crosses a surface, the energy times the weight of the particle is
subtracted from the account of the cell that it is leaving and is added
to the account of the cell that it is entering. The energy is the
kinetic energy of the particle plus 2 m o c 2 = 1 . 022016 MeV if the
particle is a positron. At the end of the history, the account in each
tally cell is divided by the source weight. The resulting energy
determines which energy bin the score is put in. The value of the score
is the source weight ( W C ) for an F8 tally and the source weight times
the energy in the account for a * F8 tally. The value of the score is
zero if no track entered the cell during the history. Another aspect of
the pulse height tally that is different from other MCNP tallies is that
F 8 : p , F 8 : e and F8 : p , e are all equivalent. All the energy from
both photons and electrons, if present, will be deposited in the cell,
no matter which tally is specified.

When the pulse height tally is used with energy bins, care must be taken
because of negative scores from non-analog processes and zero scores
caused by particles passing through the pulse height cell without
depositing energy. In some codes, like the Integrated TIGER Series,
these events cause large contributions to the lowest energy bin pulse
height score. In other codes no contribution is made. The MCNP code
compromises by counting these events in a zero bin and an epsilon bin so
that these scores can be segregated out. It is recommended that energy
binning for an F8 tally be something like

## E8 0 1.e-5 1.0 2.0 3.0 4.0 5.0 ...

Knock-on electrons in the MCNP code are non-analog in that the energy
loss is included in the multiple scattering energy loss rate rather than
subtracted out at each knock-on event. Thus knock-ons can cause negative
energy pulse height scores. These scores will be caught in the 0 energy
bin. If they are a large fraction of the total F8 tally, then the tally
is invalid because of non-analog events. Another situation is

Figure 2.9: Illustration of point detector contributions.

<!-- image -->

differentiating zero contributions from particles not entering the cell
and particles entering the cell but not depositing any energy. These are
differentiated in the MCNP code by causing an arbitrary 1.e-12 energy
loss for particles just passing through the cell. These will appear in
the 0-epsilon bin.

## 2.5.6 Flux at a Detector

The neutral particle flux can be estimated at a point (or ring) using
the point (or ring) detector next-event estimator. Neutral particle flux
images using an array of point detectors-one detector for each pixel-can
also be estimated. Detectors can yield anomalous statistics and must be
used with caution. Detectors also have special variance reduction
features, such as a highly advantageous DD card Russian roulette game.
Whenever a user-supplied source is specified, a user-supplied source
angle probability density function must also be provided.

## 2.5.6.1 Point Detector

A point detector is a deterministic estimate (from the current event
point) of the flux at a point in space. Contributions to the point
detector tally are made at source and collision events throughout the
random walk. The point detector tally ( F5 ) may be considered a
limiting case of a surface flux tally ( F2 ), as shown in Figure 2.9.

Consider the point detector to be a sphere whose radius is shrinking to
zero. Let Ω P be in the direction to the center of the sphere, i.e., in
the direction r P -r . Let dΩ P be the solid angle subtended by the
sphere from r , and let d A be defined by the intersection of an
arbitrary plane (passing through the detector point) and the collapsing
cone.

In order to contribute to a flux tally upon crossing d A , the particle
has to do two things. First, the particle must scatter toward d A (i.e.
into solid angle dΩ P ); this occurs with probability p ( Ω P )dΩ P .
Second, the particle must have a collision-less free flight for the
distance L = | r P -r | (along Ω P ) to the sphere; this occurs with
probability exp ( -GLYPH&lt;1&gt; L 0 Σ t ( s )d s ) , where Σ t ( s ) is the
total macroscopic cross section at a distance s (along Ω P ) from the
source or collision point. The probability that these two events both
occur is

<!-- formula-not-decoded -->

Define η to be the cosine of the angle between the particle direction
and the unit normal ( n ) to area d A as

<!-- formula-not-decoded -->

If a particle of weight w reaches d A , it will contribute w/ | η | d A
to the flux (compare to the F2 tally in §2.5.2.2).

As the sphere shrinks to a point, the solid angle subtended by d A is dΩ
P = | η | d A/L 2 . The sides of the cone in the figure become parallel
and the cone resembles a cylinder near the shrinking sphere. Thus the
tally becomes or

<!-- formula-not-decoded -->

In all the scattering distributions and in the standard sources, the
MCNP code assumes azimuthal symmetry. This provides some simplification.
The vector Ω P can be expressed in spherical coordinates with respect to
the particle's direction of travel, Ω , being the polar axis. The
azimuthal angle is φ and the cosine of the polar angle is µ . The
probability of scattering into dΩ P can then be written in terms of a
probability in µ , φ . That is,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Defining the probability density function for scattering about µ as

<!-- formula-not-decoded -->

and, recalling that p ( µ, φ ) is independent of φ , yields

<!-- formula-not-decoded -->

Substituting this into Eq. (2.179) yields

<!-- formula-not-decoded -->

A point detector tally is known as a 'next-event estimator' because it
is a tally of the flux at a point as if the 'next event' were a particle
trajectory directly to the detector point without further collision.

A contribution to the point detector is made at every source or
collision event. The free-flight probability term, exp [ -GLYPH&lt;1&gt; L 0 Σ
t ( s )d s ] , term accounts for attenuation between the present event
and the detector point. The 1 / 2 πL 2 term accounts for the solid angle
effect. The p ( µ ) term accounts for the probability of scattering
toward the detector instead of the direction selected in the random
walk. For an isotropic source or scatter, p ( µ ) = 0 . 5 , and the
solid-angle terms reduce to the expected 1 / 4 πL 2 . Note that p ( µ )
can be larger than unity because it is the value of a density function
and not a probability. Each contribution to the detector can be thought
of as the transport of a pseudoparticle to the detector.

The L 2 term in the denominator of the point detector causes a
singularity that makes the theoretical variance of this estimator
infinite. That is, if a source or collision event occurs near the
detector point, L approaches zero and the flux approaches infinity. The
technique is still valid and unbiased, but convergence is slower and
often impractical. If the detector is not in a source or scattering
medium, a source or collision close to the detector is impossible. For
problems where there are many scattering events near the detector, a
cell or surface estimator should be used instead of a point detector
tally. If there are so few scattering events near the detector that cell
and surface tallies are impossible, a point detector can still be used
with a specified average flux region close to the detector. This region
is defined by a fictitious sphere of radius R o surrounding the point
detector. R o can be specified either in centimeters or in mean free
paths. If R o is specified in centimeters and if L &lt; R o , the point
detector estimation inside R o is assumed to be the average flux
uniformly distributed in volume. That is

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where we can assume that the total cross section is constant within the
sphere, so

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

If Σ t = 0 , the detector is not in a scattering medium, no collision
can occur, and

<!-- formula-not-decoded -->

If the fictitious sphere radius is specified in mean free paths λ 0 ,
then λ 0 = Σ t R o and

<!-- formula-not-decoded -->

The choice of R o may require some experimentation. For a detector in a
void region R o can be set to zero. However, one is cautioned against
using R o = 0 in regions with very few collisions (such as air), because
this can cause rare scattering events near the detector that result in
large scores. For a typical problem, setting R o to a mean free path or
some fraction thereof is usually adequate. If R o is specified in
centimeters, it should correspond to the mean free path for some average
energy in the sphere.

## /warning\_sign Caution

Be certain when defining R o that the sphere it defines does not
encompass more than one material unless you understand the consequences.
This is especially true when defining R o in terms of mean free path
because R o becomes a function of energy and can vary widely. If the
sphere does contain multiple materials, the total cross section used
corresponds to the material at the center of the sphere.

In particular, if R o is defined in terms of mean free paths and if a
detector is on a surface that bounds a void on one side and a material
on the other, the contribution to the detector from the direction of the
void

will be zero even though the importance of the void is nonzero. The
reason is simply that the volume of the artificial sphere is infinite in
a void. Contributions to the detector from the other direction (that is,
across the material) will be accounted for.

Detectors differing only in R o are coincident detectors [§2.5.6.4.4],
and there is little cost incurred by experimenting with several
detectors that differ only by R o in a single problem.

## 2.5.6.2 Ring Detector

A ring detector [142] tally is a point detector tally in which the point
detector location is not fixed but rather sampled from some location on
a ring. Most of the previous section on point detectors applies to ring
detectors as well. In the MCNP code, three ring detector tallies ( Fx ,
Fy , and Fz ) correspond to rings located rotationally symmetric about
the x -, y -, and z -coordinate axes. A ring detector usually enhances
the efficiency of point detectors for problems that are rotationally
symmetric about a coordinate axis. Ring detectors also can be used for
problems where the user is interested in the average flux at a point on
a ring about a coordinate axis.

Although the ring detector is based on the point detector that has a 1
/L 2 singularity and an unbounded variance, the ring detector has a
finite variance and only a 1 /L min singularity, where L min is the
minimum distance between the contributing point and the detector ring
[143].

In a cylindrically symmetric system, the flux is constant on a ring
about the axis of symmetry. Hence, one can sample uniformly for
positions on the ring to determine the flux at any point on the ring.
The ring detector efficiency is improved by biasing the selection of
point detector locations to favor those near the contributing collision
or source point. This bias results in the same total number of detector
contributions, but the large contributions are sampled more frequently,
reducing the relative error.

For isotropic scattering in the lab system, experience has shown that a
good biasing function is proportional to exp( -P ) L -2 , where P is the
number of mean free paths and L is the distance from the collision point
to the detector point. For most practical applications, using a biasing
function involving P presents prohibitive computational complexity
except for homogeneous medium problems. For air transport problems, a
biasing function resembling exp( -P ) has been used with good results. A
biasing function was desired that would be applicable to problems
involving dissimilar scattering media and would be effective in reducing
variance. The function L -2 meets these requirements.

In Figure 2.10, consider a collision point, ( x o , y o , z o ) at a
distance L from a point detector location ( x, y, z ) . The point ( x,
y, z ) is to be selected from points on a ring of radius r that is
symmetric about the y -axis in this case.

To sample a position ( x, y, z ) on the ring with a 1 /L 2 bias, we pick
ϕ from the density function p ( ϕ ) = C/ ( 2 πL 2 ) , where C is a
normalization constant. To pick ϕ from p ( ϕ ) , let ξ be a random
number on the unit interval. Then

<!-- formula-not-decoded -->

where

<!-- formula-not-decoded -->

The above equation is valid if a 2 &gt; b 2 + c 2 , which is true except
for collisions exactly on the ring.

Solving for tan( ϕ / 2 ) , one obtains

Letting t = tan( ϕ / 2 ) , then

Figure 2.10: Illustration of ring detector contributions.

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

For ring detectors, the 1 /L 2 biasing has been supplemented when it is
weak to include a biasing based on angle to select the point on the
ring. This angle is in the plane of the ring and is relative to the
shortest line from the collision point to the detector ring. The angle
that would most likely be selected would pick the same point on the ring
as a straight line through the axis of the problem, the collision point,
and the ring. The angle least likely to be picked would choose the point
on the opposite side of the ring. This approach will thus make scores
with smaller attenuations more often. This supplemental biasing is
achieved by requiring that a ≤ 3 / 2 ( b 2 + c 2 ) 1 / 2 in Eq. (2.193).

If the radius of the ring is very large compared to the dimensions of
the scattering media (such that the detector sees essentially a point
source in a vacuum), the ring detector is still more efficient than a
point detector. The reason for this unexpected behavior is that the
individual scores to the ring detector for a

specific history have a mean closer to the true mean than to the regular
point detector contributions. That is, the point detector contributions
from one history will tend to cluster about the wrong mean because the
history will not have collisions uniformly in volume throughout the
problem, whereas the ring detector will sample many paths through the
problem geometry to get to different points on the ring.

## 2.5.6.3 Flux Image Detectors

Flux image detector tallies are an array of point detectors close enough
to one another to generate an image based on the point detector fluxes.
Each detector point represents one pixel of the flux image. The source
need not be embedded in the object. The particle creating the image does
not have to be the source particle type. Three types of neutral particle
flux image tallies can be made [144, 145]:

- Flux Image Radiograph ( FIR ), a flux image radiograph on a planar image surface;
- Flux Image on a Cylinder ( FIC ), a flux image on a cylindrical image surface; and
- Flux Image by Pinhole ( FIP ), a flux image by pinhole on a planar image surface.

When these flux image tallies are used with FS n and C n cards to
construct a virtual image grid, millions of point detectors can be
created-one detector for each pixel-to produce a flux image. The FS n
card is used to define the image pixels along the s -axis. The C n card
defines the pixels along the t -axis. The relationship of the s -axis, t
-axis, and reference direction for the planar image grid is calculated
by the MCNP code and follows the right-hand rule. Since the orientation
of the s -axis and the t -axis is dependent on the reference direction
in the geometry coordinate system, the MCNP tally output should be
examined to see the direction cosines of these two planar image grid
axes.

## /warning\_sign Caution

The image grid SHOULD NOT be in a scattering material because the point
detector average flux neighborhood is not used for flux image tallies.

## 2.5.6.3.1 Radiograph Image Tallies

Both the Flux Image Radiograph ( FIR ) and Flux Image on a Cylinder (
FIC ) tallies act like film for an x-ray type image (that is, a
transmitted image for neutrons or photons). The diagram in Figure 2.11
shows how the FIR planar rectangular grid image is defined for a source
particle passing through an object and scattering in an object. An FIC
cylindrical surface grid generates an image on a cylinder as shown in
Figure 2.12 for the particles generated inside the object.

In both cases, a ray-trace point-detector flux contribution is made to
every image grid bin (pixel) from each source and scatter event.
Allowing each event to contribute to all pixels reduces statistical
fluctuations across the grid that would occur if the grid location for
the contribution were selected randomly. For each source and scatter
event, the direction cosines to a pixel detector point are determined.
The option exists to select a random position in the pixel. The same
relative random offset is used for all pixels for a source or scatter
event. The random detector location in a pixel changes from event to
event. The option also exists to select the point detector location at
the center of each pixel when the center flux is desired.

A standard point detector attenuated ray-trace flux contribution to the
image pixel is then made. A new direction cosine is determined for each
pixel followed by the new ray-trace flux calculation. These tallies
automatically create a source-only contribution and a total for each
pixel. Standard point detector tally modifications can be made to the
image tally, for example, by using the FM , PD , and FT cards.

Figure 2.11: Diagram of an FIR (Flux Image Radiograph) tally for a source external to the object. The directions of the orthogonal S - and T -axes depend on the reference-direction vector in the geometry coordinate system.

<!-- image -->

Figure 2.12: Diagram of an FIC (Flux Image on a Cylinder) tally for a source internal to the object.

<!-- image -->

Figure 2.13: Diagram of an FIP (Flux Image by Pinhole) tally for a source internal to the object. The directions of the orthogonal S - and T -axes depend on the reference-direction vector in the geometry coordinate system.

<!-- image -->

## 2.5.6.3.2 Pinhole Image Tally

The Flux Image by Pinhole ( FIP ) tally uses a pinhole (as in a pinhole
camera) to create a neutron or photon image onto a planar rectangular
grid that acts much like photographic film. Figure 2.13 is a diagram of
the FIP image tally. Each source and scatter event contributes to one
point detector on the image grid pixel intersected by the particle
trajectory through the pinhole.

The particle event point and the virtual pinhole point (sampled
uniformly in area if a radius is specified) are used to define the
direction cosines of the contribution to be made from the source or
scatter location through the pinhole to one image grid element (pixel).
Once this direction is established, a ray-trace point detector flux
contribution is made to the intersected pixel including attenuation by
any material along that path. No source or scattering events on the
image grid side of the pinhole will contribute to the image.

The pinhole and associated grid will image both direct source
contributions and the direct plus any scattered contributions. Standard
tally modifications can be made to the image tally, for example, by
using the FM , PD , and FT cards.

The magnitude of the flux contribution through the pinhole to a pixel is
calculated as follows. The flux at a pinhole point P is φ P ( Ω ) ,
where Ω is the direction that intersects the pinhole at point P . Define
µ to be the cosine of the angle between the detector trajectory and the
reference direction, which is perpendicular to the plane of the pinhole.
The particle weight per unit pinhole area (or the particle current per
unit pinhole area) is φ P ( Ω ) µ . The weight in a small area d A in
the pinhole is φ P ( Ω ) µ d A . The total particle weight W integrated
over the pinhole area A P is

<!-- formula-not-decoded -->

The FIP tally selects one particle trajectory to carry this weight. This
trajectory should be sampled in d A from

Instead, the pinhole point P sampling is biased to be uniform in the
pinhole area A P ; that is,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

To account for this biased sampling, the weight W of the sample must be
multiplied by

<!-- formula-not-decoded -->

Thus, an unbiased estimate of the sampled weight going through d A at
the pinhole is W P ( Ω ) = Ww m ( Ω ) or

<!-- formula-not-decoded -->

Now that an unbiased estimate of the weight through d A is obtained, an
unbiased estimate of the weight arriving on the image plane can also be
obtained. If λ ( Ω ) is the optical path along Ω from the sampled
pinhole point to the image plane, then the weight W pixel ( Ω ) arriving
at the pixel in the image plane is

<!-- formula-not-decoded -->

The surface flux at the image plane is estimated by the W pixel ( Ω )
divided by µ (note that the pinhole plane and image plane are parallel)
divided by pixel area A pixel . Therefore, the surface flux at the
intersected pixel is

<!-- formula-not-decoded -->

Thus, the flux at the pixel is just the exp[ -λ ( Ω )] -attenuated flux
at the pinhole scaled by the ratio of A P (where the weight W passes
through) to the A pixel (the pixel where the flux φ pixel ( Ω ) is
scored). If a perfect pinhole with no pinhole area is used, then A P is
defined to be unity.

## 2.5.6.4 General Considerations of Point Detector Estimators

## 2.5.6.4.1 Pseudoparticles and Detector Reliability

Point and ring detectors are Monte Carlo methods wherein the simulation
of particle transport from one place to another is deterministically
short-circuited. Transport from the source or collision point to the
detector is replaced by a deterministic estimate of the potential
contribution to the detector. This transport between the source or
collision point and the detector can be thought of as being via
'pseudoparticles.' Pseudoparticles undergo no further collisions. These
particles do not reduce the weight or otherwise affect the random walk
of the particles that produced them. They are merely estimates of a
potential contribution. The only resemblance to Monte Carlo particles is
that the quantity they estimate requires an attenuation term that must
be summed over the trajectory from the source or collision to the
detector. Thus most of the machinery for transporting particles can also
be used for the pseudoparticles. No records (for example, tracks
entering) are kept about pseudoparticle passage.

## /warning\_sign Caution

Because detectors rely on pseudoparticles rather than particle
simulation by random walk, they should be considered only as a very
useful last resort. Detectors are unbiased estimators, but their use can
be tricky, misleading, and occasionally unreliable.

Consider the problem illustrated in Figure 2.14. The monoenergetic
isotropic point source always will make the same contribution to the
point detector, so the variance of that contribution will be zero. If no
particles have yet collided in the scattering region, the detector tally
will be converged to the source contribution, which is wrong and
misleading. But as soon as a particle collides in the scattering region,
the detector tally

Figure 2.14: Demonstration of inappropriate source-point detector-scatterer configuration.

<!-- image -->

and its variance will jump. Then the detector tally and variance will
steadily decrease until the next particle collides in the scattering
region, at which time there will be another jump.

These jumps in the detector score and variance are characteristic of
undersampling important regions. Nextevent estimators are prone to
undersampling as already described in §2.4.4.2.5 for the p ( µ ) term of
photon coherent scattering. The jump discussed here is from the sudden
change in the L and possibly λ terms. Jumps in the tally caused by
undersampling can be eliminated only by better sampling of the
undersampled scattering region that caused them.

Biasing Monte Carlo particles toward the tally region would cause the
scattering region to be sampled better, thus eliminating the jump
problem. It is recommended that detectors be used with caution and with
a complete understanding of the nature of next-event estimators. When
detectors are used, the tally fluctuation charts printed in the output
file should be examined closely to see the degree of the fluctuations.
Also the detector diagnostic tables in the MCNP output file should be
examined to see if any one pseudoparticle trajectory made an unusually
large contribution to the tally. Detector results should be viewed
suspiciously if the relative error is greater than 5%. Close attention
should be paid to the tally statistical analysis and the ten statistical
checks described in §2.6.9.2.3.

## 2.5.6.4.2 Detectors and Reflecting, White, or Periodic Surfaces

## /warning\_sign Caution

Detectors used with reflecting, white, or periodic surfaces give wrong
answers because pseudoparticles travel only in straight lines.

Consider Figure 2.15, with a point detector and six source cells. The
imaginary cells and point detector are also shown on the other side of
the mirror. The solid line shows the source contribution from the
indicated cell. The MCNP code does not allow for the dashed-line
contribution on the other side of the reflecting surface. The result is
that contributions to the detector will always be from the solid path
instead of from a mixture of solid and dashed contributions. This same
situation occurs at every collision. Therefore, the detector tally will
be lower (with the same starting weight) than the correct answer and
should not be used with reflecting, white, or periodic surfaces. The
effect is even worse for problems with multiple reflecting, white, or
periodic surfaces.

## 2.5.6.4.3 Variance-reduction Schemes for Detectors

Pseudoparticles of point detectors are not subject to the variance
reduction schemes applied to particles of the random walk. They do not
split according to importances, weight windows, etc., although they are

Figure 2.15: Demonstration of inappropriate source-point detector-reflecting boundary scenario.

<!-- image -->

terminated by entering zero importance cells. However, two Russian
roulette games are available specifically for detector pseudoparticles.

The PD card can be used to specify the pseudoparticle generation
probability for each cell. The entry for each cell i is p i where 0 ≤ p
i ≤ 1 . Pseudoparticles are created with probability p i and weight 1 /p
i . If p i = 1 , which is the default, every source or collision event
produces a pseudoparticle. If p i = 0 , no pseudoparticle is produced.

## /warning\_sign Caution

Setting p i = 0 in a cell that can actually contribute to a detector
erroneously biases the detector tally by eliminating such contributions.

Thus p i = 0 should be used only if the true probability of scoring is
zero or if the score from cell i is unwanted for some legitimate reason
such as problem diagnostics. Fractional entries of p i should be used
with caution because the PD card applies equally to all pseudoparticles.
The DD card can be used to Russian roulette just the unimportant
pseudoparticles. However, the DD card roulette game often requires
particles to travel some distance along their trajectory before being
killed. When cells are many mean-free paths from the detector, the PD
card may be preferable.

The DD card controls both the detector diagnostic printing and a Russian
roulette game played on pseudoparticles in transit to detectors. The
Russian roulette game is governed by the input parameter k that controls
a comparison weight w c internal to the MCNP code, such that where

<!-- formula-not-decoded -->

N is the number of histories run thus far,

I is the number of pseudoparticles started so far,

<!-- formula-not-decoded -->

I is the contribution from the i th pseudoparticle to the detector
tally.

When each pseudoparticle is generated, W , p ( µ ) , and L are already
known before the expensive tracking process is undertaken to determine λ
. If Wp ( µ ) / ( 2 πL 2 ) &lt; w c , the pseudoparticle contribution to
the detector ϕ i will be less than the comparison weight. Playing
Russian roulette on all pseudoparticles with ϕ i &lt; w c avoids the
expensive tracking of unimportant pseudoparticles. Most are never
started. Some are started but are rouletted as soon as λ has increased
to the point where Wp ( µ ) e -λ / ( 2 πL 2 ) &lt; w c . Rouletting
pseudoparticles whose expected detector contribution is small also has
the added benefit that those pseudoparticles surviving Russian roulette
now have larger weights, so the disparity in particle weights reaching
the detector is reduced. Typically, using the DD card will increase the
efficiency of detector problems by a factor of ten. This Russian
roulette is so powerful that it is one of two MCNP variance reduction
options that is turned on by default. The default value of k is 0.1. The
other default variance reduction option is implicit capture.

The DD card Russian roulette game is almost foolproof. Performance is
relatively insensitive to the input value of k . For most applications
the default value of k = 0 . 1 is adequate. Usually, choose k so that
there are 1-5 transmissions (pseudoparticle contributions) per source
history. If k is too large, too few pseudoparticles are sampled; thus k
≥ 1 is a fatal error.

## /warning\_sign Caution

Because a random number is used for the Russian roulette game invoked by
k &gt; 0 , the addition of a detector tally affects the random walk
tracking processes.

Detectors are the only tallies that affect results. If any other tally
type is added to a problem, the original problem tallies remain
unchanged. Because detectors use the default DD card Russian roulette
game, and that game affects the random number sequence, the whole
problem will track differently and the original tallies will agree only
to within statistics. Because of this tracking difference, it is
recommended that k &lt; 0 be used once a good guess at w c can be made.
This is especially important if a problem needs to be debugged by
starting at some history past the first one. Also, k &lt; 0 makes the first
200 histories run faster.

There are two cases when it is beneficial to turn off the DD card
Russian roulette game by setting k = 0 . First, when looking at the tail
of a spectrum or some other low probability event, the DD card roulette
game will preferentially eliminate small scores and thus eliminate the
very phenomenon of interest. For example, if energy bias is used to
preferentially produce high energy particles, these biased particles
will have a lower weight and thus preferentially will be rouletted by
the DD card game. Second, in very deep penetration problems,
pseudoparticles will sometimes go a long way before being rouletted. In
this rare case it is wasteful to roulette a pseudoparticle after a great
deal of time has been spent following it and perhaps a fractional PD
card should be used or, if possible, a cell or surface tally.

## 2.5.6.4.4 Coincident Detectors

Because tracking pseudoparticles is very expensive, the MCNP code uses a
single pseudoparticle for multiple detectors, known as coincident
detectors, that must be identical in:

- geometric location,
- particle type (that is, neutron or photon),
- upper time bin limit,

- DD card Russian Roulette control parameter, k , and
- PD card entries, if any.

Energy bins, time bins, tally multipliers, response functions,
fictitious sphere radii, user-supplied modifications ( TALLYX ), etc.,
can all be different. Coincident detectors require little additional
computational effort because most detector time is spent in tracking a
pseudoparticle. Multiple detectors using the same pseudoparticle are
almost 'free.'

## 2.5.6.4.5 Direct vs. Total Contribution

Unless specifically turned off by the user, the MCNP code automatically
prints out both the direct and total detector contribution. Recall that
pseudoparticles are generated at source and collision events. The direct
contribution is that portion of the tally from pseudoparticles born at
source events. The total contribution is the total tally from both
source and collision events. For MODE N P problems with photon
detectors, the direct contribution is from pseudophotons born in neutron
collisions. The direct contributions for detailed photon physics will be
smaller than the simple physics direct results because coherent
scattering is included in the detailed physics total cross section and
omitted in the simple physics treatment.

## 2.5.6.4.6 Angular Distribution Functions for Point Detectors

All detector estimates require knowledge of the p ( µ ) term, the value
of the probability density function at an angle θ , where µ = cos( θ ) .
This quantity is available to the MCNP code for the standard source and
for all kinds of collisions. For user-supplied source subroutines, the
MCNP code assumes an isotropic distribution,

<!-- formula-not-decoded -->

Therefore, the variable PSC = p ( µ ) = 1 / 2 . If the source
distribution is not isotropic in a user-supplied source subroutine, the
user must also supply a subroutine SRCDX if there are any detectors or
DXTRAN spheres in the problem. In subroutine SRCDX , the variable PSC
must be set for each detector and DXTRAN sphere. An example of how this
is done and also a description of several other source angular
distribution functions is in §10.3.5.

## 2.5.6.4.7 Detectors and the S ( α, β ) Thermal Treatment

The S ( α, β ) thermal treatment poses special challenges to next-event
estimators because the probability density function for angle has
discrete lines to model Bragg scattering and other molecular effects.
Therefore, the MCNP code has an approximate model [76] that, for the PSC
calculation (not the transport calculation), replaces the discrete lines
with finite histograms of width µ &lt; 0 . 1 .

This approximation has been demonstrated to accurately model the
discrete line S ( α, β ) data. In cases where continuous data is
approximated with discrete lines, the approximate scheme cancels the
errors and models the scattering better than the random walk [77]. Thus
the S ( α, β ) thermal treatment can be used with confidence with next-
event estimators like detectors and DXTRAN.

## 2.5.7 Additional Tally Features

The standard MCNP tally types can be controlled, modified, and
beautified by other tally cards. These cards are described in detail in
§3.2.5.4; an overview is given here.

## 2.5.7.1 Bin Limit Control

The integration limits of the various tally types can be controlled by E
, T , C , and FS cards. The E card establishes energy bin ranges; the T
card establishes time bin ranges; the C card establishes cosine bin
ranges; and the FS card segments the surface or cell of a tally into
subsurface or subcell bins.

## 2.5.7.2 Flagging

Cell and surface flagging cards, CF and SF , determine where the
different portions of a tally originate. For example:

```
1 F4 1 2 CF4 2 3 4
```

The flux tally for cell 1 is output twice: first, the total flux in cell
1; and second, the flagged tally, or that portion of the flux caused by
particles having passed through cells 2, 3, or 4.

## 2.5.7.3 Multipliers and Modification

MCNP tallies can be modified in many different ways. The EM , TM , and
CM cards multiply the quantities in each energy, time, or cosine bin by
a different constant. This capability is useful for modeling response
functions or changing units. For example, a surface current tally can
have its units changed to per steradian by entering the inverse
steradian bin sizes on the CM card.

The DE and DF cards allow modeling of an energy-dependent dose function
that is a continuous function of energy from a table whose data points
need not coincide with the tally energy bin structure ( E card).

The FM card multiplies the F1 , F2 , F4 , and F5 tally cards by any
continuous-energy quantity available in the data libraries. For example,
average heating numbers H avg ( E ) and total cross section σ t ( E )
are stored on the MCNP data libraries. An F4 tally multiplied by σ t H
avg ( E ) ρ a /ρ g converts it to an F6 tally, or an F5 detector tally
multiplied by the same quantity calculates heating at a point
[§2.5.6.1]. The FM card can modify any flux or current tally of the form
GLYPH&lt;1&gt; ϕ ( E )d E into GLYPH&lt;1&gt; R ( E ) ϕ ( E )d E , where R ( E ) is
any combination of sums and products of energy-dependent quantities
known to the MCNP code.

The FM card can also model attenuation. Here the tally is converted to
GLYPH&lt;1&gt; ϕ ( E ) exp[ -σ t ( E ) ρ a x ]d E , where x is the thickness
of the attenuator, ρ a is its atom density, and σ t is its total cross
section. Double parentheses allow the calculation of GLYPH&lt;1&gt; ϕ ( E )
exp[ -σ t ( E ) ρ a x ] R ( E )d E . More complex expressions of σ t ( E
) ρ a x are allowed so that many attenuators may be stacked. This is
useful for calculating attenuation in line-of-sight pipes and through
thin foils and detector coatings, particularly when done in conjunction
with point and ring detector tallies. Beware, however, that attenuation
assumes that the attenuated portion of the tally is lost from the system
by capture or escape and cannot be scattered back in.

Two special FM card options are available. The first option sets R ( E )
= 1 /ϕ ( E ) to score tracks or collisions. The second option sets R ( E
) = 1 /v (where v is scalar velocity) to score population or prompt
removal lifetime.

## 2.5.7.4 Special Treatments

A number of special tally treatments are available using the FT card. A
brief description of each one follows.

## 2.5.7.4.1 Change Current Tally Reference Vector

F1 current tallies measure bin angles relative to the surface normal.
They can be binned relative to any arbitrary vector defined with the FRV
option.

## 2.5.7.4.2 Gaussian Energy Broadening

The GEB option can be used to better simulate a physical radiation
detector in which energy peaks exhibit Gaussian energy broadening. The
tallied energy is broadened by sampling from the Gaussian, where

E is the broadened energy,

E 0 is the unbroadened energy of the tally,

C is a normalization constant, and

A is the Gaussian width.

The Gaussian width is related to the full width half maximum (FWHM) by

<!-- formula-not-decoded -->

The desired FWHM is specified by the user-provided constants, a , b ,
and c , where

The FWHM is defined as FWHM = 2( E FWHM -E 0 ) , where E FWHM is such
that f ( E FWHM ) = 1 / 2 f ( E 0 ) and f ( E 0 ) is the maximum value
of f ( E ) .

<!-- formula-not-decoded -->

## 2.5.7.4.3 Time Convolution

Because the geometry and material compositions are independent of time,
except in the case of time-dependent temperatures, the expected tally T
( t, t + τ ) at time t + τ from a source particle emitted at time t is
identical to the expected tally T (0 , τ ) from a source particle
emitted at time 0. Thus, if a calculation is performed with all source
particles started at t = 0 , one has an estimate of T (0 , τ ) and the
tallies T Q i from a number of time-distributed sources. Q i ( t ) can
be calculated at time η as

<!-- formula-not-decoded -->

by sampling t from Q i ( t ) and recording each particle's tally
(shifted by t ), or after the calculation by integrating Q i ( t )
multiplied by the histogram estimate of T (0 , η -t ) . The latter
method is used in the MCNP code to simulate a source as a square pulse
starting at time a and ending at time b , where a and b are supplied by
the TMC option.

<!-- formula-not-decoded -->

## 2.5.7.4.4 Binning by the Number of Collisions

Tallies can be binned by the number of collisions that caused them with
the INC option and an FU card. A current tally, for example, can be
subdivided into the portions of the total current coming from particles
that have undergone zero, one, two, three, . . . collisions before
crossing the surface. In a point detector tally, the user can determine
what portion of the score came from particles having their 1st, 2nd,
3rd, . . . collision. Collision binning is particularly useful with the
exponential transform because the transform reduces variance by reducing
the number of collisions.

## /warning\_sign Caution

If particles undergoing many collisions are the major contributor to a
tally, then the exponential transform is ill-advised. When the
exponential transform is used, the portion of the tally coming from
particles having undergone many collisions should be small.

## 2.5.7.4.5 Binning by Detector Cell

The ICD option with an FU card is used to determine what portion of a
detector tally comes from what cells. This information is similar to the
detector diagnostics print, but the FT card can be combined with energy
and other binning cards. The contribution to the normalized rather than
unnormalized tally is printed.

## 2.5.7.4.6 Binning by Source Distribution

The SCX and SCD options are used to bin a tally score according to what
source distribution caused it.

## 2.5.7.4.7 Binning by Multigroup Particle Type

The PTT option with an FU card is used to bin multigroup tallies by
particle type. The MCNP multigroup treatment is available for neutron,
coupled neutron/photon, and photon problems. However, charged particles
or any other combinations of particles can be run with the various
particles masquerading as neutrons and are printed out in the MCNP
output file as if they were neutrons. With the PTT option, the tallies
can be segregated into particle types by entering atomic weights in
units of MeV on the FU card. The FU atomic weights must be specified to
within 0.1% of the true atomic weight in MeV units; thus FU 0.511
specifies an electron, but 0.510 is not recognized.

## 2.5.7.4.8 Binning by Particle Charge

The ELC option allows binning F1 current tallies by particle charge.
There are three ELC options:

1. Cause negative electrons to make negative scores and positrons to make positive scores. Note that by tallying positive and negative numbers the relative error is unbounded and this tally may be difficult to converge.
2. Segregate electrons and positrons into separate bins plus a total bin. There will be three bins (positron, electron, and total) all with positive scores. The total bin will be the same as the single tally bin without the ELC option.
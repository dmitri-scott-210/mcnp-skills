---
title: "Chapter 5.9 - Tally Specification-focused Data Cards"
chapter: "5.9"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.9_Tally_Specification-focused_Data_Cards.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## 5.8.15.1 Example 1

The source.F90 subroutine given in Listing 5.48 is used to represent the
SDEF card:

```
1 SDEF par=n erg=8 vec=1 0 0 dir 1 wgt=1 tme=0 pos 2 3 4
```

Listing 5.48: example\_source\_subroutine.f90.txt

```
1 subroutine source 2 ! dummy subroutine. Aborts job if source subroutine is 3 ! missing. If nsr==USER _ DEFINED _ SOURCE, a subroutine 4 ! source must be furnished by the user. 5 6 ! At entrance, a random set of direction cosines, pbl%r%u, 7 ! pbl%r%v, pbl%r%w has been defined 8 9 ! .. Use Statements .. 10 use mcnp _ interfaces _ mod, only : expirx 11 use mcnp _ debug 12 use pblcom 13 14 implicit none 15 16 pbl%i%ipt = 1 17 pbl%i%jsu = 0 18 pbl%i%icl = 1 19 pbl%r%x = 2 20 pbl%r%y = 3 21 pbl%r%z = 4 22 pbl%r%u = 1 23 pbl%r%v = 0 24 pbl%r%w = 0 25 pbl%r%erg = 8 26 pbl%r%tme = 0 27 pbl%r%wgt = 1 28 29 ! call expirx(0,'source','you need a source subroutine.') 30 return 31 end subroutine source
```

It is assumed that the source is in cell 6, which is the 1st cell number
listed in the input. The expirx call must be commented out; otherwise
the compiled source will still result in a message to the terminal of
'bad trouble in subroutine source of mcrun you need a source
subroutine.'

## 5.9 Tally Specification-focused Data Cards

Tally cards are used to specify what type of information the user wants
to gain from the Monte Carlo calculation. Options include such tallies
as current across a surface, flux at a point, heating in a region, etc.
This information is requested by the user by using a combination of
cards described in this section. To obtain tally results, only the F
card is required; the other tally cards provide various optional
features.

The n associated with the tally-type specification is a user-chosen
tally number n ≤ 99999999 ; choices of n are discussed in the following
section. When a choice of n is made for a particular tally type, any
other input card used to refine that tally description (such as E n for
energy bins) is given the same value of n by the user.

Table 5.18: Tally Designators &amp; Units

| Mnemonic   | Tally Description                                                 | F n units      | * F n units   |
|------------|-------------------------------------------------------------------|----------------|---------------|
| F 1 : P    | Current integrated over a surface                                 | particles      | MeV           |
| F 2 : P    | Fluence averaged over a surface                                   | particles/cm 2 | MeV/cm 2      |
| F 4 : P    | Fluence averaged over a cell                                      | particles/cm 2 | MeV/cm 2      |
| F 5a : P   | Fluence at a point or ring detector                               | particles/cm 2 | MeV/cm 2      |
| FIP 5 : P  | Array of point detectors for pinhole fluence image                | particles/cm 2 | MeV/cm 2      |
| FIR 5 : P  | Array of point detectors for planar radiograph fluence image      | particles/cm 2 | MeV/cm 2      |
| FIC 5 : P  | Array of point detectors for cylindrical radiograph fluence image | particles/cm 2 | MeV/cm 2      |
| F 6 : P    | Energy deposition averaged over a cell                            | MeV/g          | jerks/g       |
| +F 6       | Collision heating                                                 | MeV/g N/A      |               |
| F 7 : P    | Fission energy deposition averaged over a cell                    | MeV/g          | jerks/g       |
| F 8 : P    | Energy distribution of pulses created in a detector by radiation  | pulses MeV     |               |
| +F 8 : P   | Charge deposition                                                 | charge N/A     |               |

Much of the information on these cards is used to describe tally 'bins,'
or subdivisions, of the tally space into discrete and contiguous
increments such as cosine, energy, or time. Usually when the user
subdivides a tally into bins, MCNP6 also can provide the total tally
summed over appropriate bins (such as over all energy bins). Absence of
any bin specification card results in one unbounded bin rather than one
bin with a default bound. No information is printed about the limits on
the unbounded bin.

If there are reflecting surfaces or periodic boundaries in the problem,
the user may have to normalize the tallies in some special way. This can
be done by setting the weight of the source particles or by using the FM
or SD cards.

Printed with each tally bin is the relative error of the tally
corresponding to one standard deviation. These errors cannot be believed
reliable (hence neither can the tally itself) unless the error is fairly
low. Results with errors greater than 50% are useless, those with errors
between 20% and 50% can be believed to within a factor of a few, those
with errors between 10% and 20% are questionable, and results with
errors less than 10% are generally (but not always) reliable, except for
point detectors. Detector results are generally reliable if their
associated relative errors are below 5%. The tally fluctuation charts at
the end of the output file base their results on the information from
one specified bin of every tally. See the TF card. This bin also is used
for the weight-window generator and is subject to ten statistical checks
for tally convergence, including calculation of the variance of the
variance (VOV). The VOV can be printed for all bins in a tally by using
the DBCN card. A tally is considered to be converged with high
confidence only when it passes all ten statistical checks.

## 5.9.1 F: Standard Tallies

MCNP6 offers an array of standard tallies to the user. These include
particle current, particle flux (across a surface, in a cell, at a
detector point), energy deposition, collision heating, fission energy
deposition, pulse height, and charge deposition. All tallies are
normalized to be per source particle unless a different normalization
has been specified with the WGT keyword on the SDEF card, changed by the
user with a TALLYX subroutine, or normalized by weight in a criticality
( KCODE ) calculation.

The tallies are identified by tally type and particle type as follows.
Tallies are given the numbers 1, 2, 4, 5, 6, 7, 8 or increments of 10
thereof, and are given a particle designator P , where P is chosen from
Table 4.3. Thus you may have as many of any basic tally as you need,
each with different energy bins, or flagging bins, or anything else. The
designations F4 : n , F14 : n , F104 : n , and F234 : n are all
legitimate neutron cell flux tallies; they could all be for the same
cell(s) but with different energy or multiplier bins, for example.
Similarly F5 : p ,

F15 : p , and * F 305 : p are all photon point detector tallies. Having
both an F1 : n card and an F1 : p card in the same MCNP input file is
not allowed. The tally number may not exceed 99,999,999.

Several tally types allow multiple particles. For example, an energy
deposition tally for both neutrons and gammas, F6 : n , p , may be
specified. In the case of collision heating, +F6 always applies to all
particles in a problem; therefore this tally has no particle designator.
For pulse-height tallies photons/electrons are a special case: F8 : p ,
e is the same as F8 : p and F8 : e . Also, F8 tallies may have particle
combinations such as F8 : n , h .

Tally types 2, 4, and 5 are described as fluence tallies with the
associated units. However, depending on the source units, these may also
be fluence rate (i.e., flux) tallies with units of particles / ( cm 2 ·
s ) .

Tally types 1, 2, 4, and 5 are normally weight tallies; however, if the
F card is flagged with an asterisk (for example, * F1 : n ), energy
times weight will be tallied. The asterisk flagging also can be used on
tally types 6 and 7 to change the units from MeV/g to jerks/g. No
asterisk can be used in combination with the + on the +F8 or +F8
tallies. The asterisk on a tally type 8 converts from a pulse-height
tally to an energy deposition tally. All of the units are shown in the
Table 5.18.

Tally type 8 has many options. The standard F8 tally is a pulse-height
tally and the energy bins are no longer the energies of scoring events,
but rather the energy balance of all events in a history. In conjunction
with the FT 8 card, the F8 tally can be an anti-coincidence pulse-height
tally, a neutron coincidence capture tally, or a residual nuclei
production tally. When flagged with an asterisk, * F8 becomes an energy
deposition tally. In addition, F8 can be flagged with a plus ( + ) to
convert it from an energy deposition tally (flagged with an asterisk) to
a charge deposition tally. The +F8 tally is the negative particle weight
for electrons and the positive weight for positrons. The +F8 : e tally
can be checked against an F1 : e type surface tally with the FT 1 : e
ELC option to tally charge.

Only the F2 surface flux tally requires the surface area. The area
calculated is the total area of the surface that may bound several
cells, not a portion of the surface that bounds only a particular cell.
An exception to this statement occurs if one uses a repeated structures
format to describe the tally bin [§5.9.1.5]. If you need only the
segment of a surface, you might segment the full surface with the FS
card and use the SD card to enter the appropriate values. You can also
redefine the geometry as another solution to the problem. Similarly,
tally types 4, 6, and 7 require the cell volume, which can be
automatically calculated or supplied by the user via the VOL or SD
cards. The limit on the total number of detectors and different tallies
is given in Table 4.1. Note that a single type 5 tally may create more
than one detector.

For any tally, if the tally label of the surface or cells in a given bin
exceeds eleven characters, including spaces, an alphabetical or
numerical designator is defined for printing convenience. The
MCNP6-supplied designator will be printed with the tally output, e.g., '
G is (1 2 3 4 5 6) '. This labeling scheme is usually required for
tallies over the union of a long list of surfaces or cells or with
repeated structure tallies.

## 5.9.1.1 Surface and Cell Tallies (Tally Types 1, 2, 4, 6, and 7)

```
Simple Data-card Form: F n : P s1 . . . sK or General Data-card Form: F n : P s1 ( s2 . . . s3 ) ( s4 . . . s5 ) s6 s7 . . . [ T ] n Tally number. Restriction: n ≤ 99999999 P Particle designator ( 1 ). sk Problem number of surface or cell for tallying ( 2 ). T Total over specified surfaces for F1 tallies; average over specified surfaces or
```

<!-- formula-not-decoded -->

Use: In the simple form above, MCNP6 creates K surface or cell bins for
the requested tally, listing the results separately for each surface or
cell. In the more general form, a bin is created for each surface or
cell listed separately and for each collection of surfaces or cells
enclosed within a set of parentheses. Entries within parentheses also
can appear separately or in other combinations. Parentheses indicate
that the tally is for the union of the items within the parentheses. For
unnormalized tallies (tally type 1), the union of tallies is a sum, but
for normalized tallies (types 2, 4, 6, and 7), the union results in an
average. See §5.9.1.5 for an explanation of the repeated structure and
lattice tally format.

## Details:

- 1 Tally type 7 allows P = n only.
- 2 Only surfaces that define cell boundaries and that are listed in a cell card description can be used on F1 and F2 tallies.
- 3 The symbol T entered on surface or cell F cards is shorthand for a region that is the union of all of the other entries on the card. A tally is made for the individual entries on the F card plus the union of all the entries. The entry is optional.
- 4 Surface flux tallies require an approximation when counting grazing contributions, that is, for contributions where the dot product of the particle direction and the surface normal are between -0 . 001 and 0.001 (the current default, new in MCNP6.2). The grazing angle cutoff can be reset using the 24th entry on the DBCN card; i.e., ' DBCN 23 J 0 . 1 ' changes the grazing angle cutoff from the MCNP6.2 value of ± 0 . 001 to the historic MCNP value of ± 0 . 1 .

## 5.9.1.1.1 Aside: Surface Flux Tally (F2)

For particles grazing the surface, 1 / | µ | (where µ is the cosine of
the angle that the particle track makes with the surface normal) is very
large and the MCNP code approximates the surface flux estimator in order
to satisfy the requirement of one central limit theorem. An unmodified
surface flux estimator has an infinite variance, and thus confidence
intervals could not be formed via the central limit theorem, because the
central limit theorem requires a finite variance. For this reason, the
MCNP code sets | µ | = 0 . 0005 when | µ | &lt; 0 . 001 ; because of this
approximation, the F2 tally is not an exact estimate of the surface
flux. The grazing angle cutoff cosine can be changed using the 24th
entry on the DBCN card.

While the numeric values may vary, this is the standard approximation
used in Monte Carlo codes. This approximation is accurate when the
angular flux is isotropic or linearly anisotropic with respect to µ on
the surface and the limits of the flux integral with respect to µ are
symmetric. However, these assumptions may become invalid on external
surfaces or in other cases of one-way surface crossings; when exactly
tangent crossing is not possible because of the geometry of the problem;
or when cosine bins are used. Users should be especially careful in
these cases. More details may be found in [303, 304].

## 5.9.1.1.2 Aside: Energy Deposition Tally (F6)

The energy deposition tallies in the MCNP code are fairly complicated,
and require some explanation in order to ensure the correct result is
extracted. See §2.5.3 for further details, as well as some rules of
thumb for how to ensure the accuracy of your simulation.

1

1

1

1

## 5.9.1.1.3 Example 1

## F2:N 1 3 6 T

This card specifies four neutron flux tallies, one across each of the
surfaces 1, 3, and 6 and one which is the average of the flux across all
three of the surfaces.

## 5.9.1.1.4 Example 2

## F1:P (1 2) (3 4 5) 6

This card provides three photon current tallies, one for the sum over
surfaces 1 and 2; one for the sum over surfaces 3, 4, and 5; and one for
surface 6 alone.

## 5.9.1.1.5 Example 3

## F371:N (1 2 3) (1 4) T

This card provides three neutron current tallies, one for the sum over
surfaces 1, 2, and 3; one for the sum over surfaces 1 and 4; and one for
the sum over surfaces 1, 2, 3, and 4. The point of this example is that
the T bin is not confused by the repetition of surface 1.

## 5.9.1.1.6 Example 4

## +F6 2

This card produces energy deposition (MeV/g) from all particles averaged
over cell 2. This will include heating values and/or d E/ d x energy
from particles undergoing library interactions (e.g., neutrons, photons,
electrons, protons) and d E/ d x , recoil, and non-tracked secondary
particle energy from all model interactions.

## 5.9.1.2 Detector Tallies (Tally Type 5)

Point detectors, ring detectors, and radiography tallies use an
assumption of isotropic scatter for contributions from collisions within
the model regime (i.e., generally E &gt; 150 MeV). These estimators require
the angular distribution data for particles produced in an interaction
to predict the 'next event.' Information on these distributions is
available in tabular form in the libraries; however, this information is
not available in the required form from physics models used to produce
secondary particles above the tabular region. The limit on the number of
detectors is given in Table 4.1.

The user is encouraged to read about detectors before implementing them
because they are susceptible to unreliable results if used improperly.
Here are a few hints:

1. Remember that contributions to a detector are not made through a region of zero importance.
2. Ring (rather than point) detectors should be used in all problems with axial symmetry.
3. Flux image detectors should be located in a void because the constant flux neighborhood ro is not used. Such a neighborhood would have to enclose the entire image grid.
4. A detector located right on a surface will probably cause trouble.
5. Detectors and DXTRAN can be used in problems with the S ( α, β ) thermal treatment, but the S ( α, β ) contributions are approximate [77].
6. Detectors used with reflecting, white, or periodic surfaces give wrong answers.
7. Consider using the PD n and DD n cards.

## 5.9.1.2.1 Point Detectors

| Data-card Form: F n : P x1 y1 z1 ro1 . . . xK yK zK roK [ ND ]   | Data-card Form: F n : P x1 y1 z1 ro1 . . . xK yK zK roK [ ND ]                                                                                                                                                    |
|------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                                                | User-supplied tally number ending in the numeral 5. Restriction: n ≤ 99999999                                                                                                                                     |
| P                                                                | Particle designator: Restriction: n for neutrons or p for photons only.                                                                                                                                           |
| xk yk zk                                                         | Coordinates of the k th detector point ( 2 ).                                                                                                                                                                     |
| rok                                                              | Radius of the sphere of exclusion for the k th detector where a positive entry is interpreted as centimeters and a negative entry is interpreted as mean free paths. A negative entry is illegal in a void ( 3 ). |
| ND                                                               | Optional keyword to inhibit the separate printing of the direct contribution for that detector tally ( 4 ).                                                                                                       |

## 5.9.1.2.2 Ring Detectors

| Data-card Form: F na : P ao1 r1 ro1 . . . aoK rK roK [ ND ]   | Data-card Form: F na : P ao1 r1 ro1 . . . aoK rK roK [ ND ]                                                           |
|---------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| n                                                             | User-supplied tally number ending in the numeral 5. Restriction: n ≤ 99999999                                         |
| a                                                             | The letter x , y , or z , which indicates the axis of the ring.                                                       |
| P                                                             | Particle designator: Restriction: n for neutrons or p for photons only.                                               |
| aok                                                           | Distance along axis ' a ' where the ring plane of the k th detector intersects the axis ( 2 ).                        |
| rk                                                            | Radius of the ring of the k th detector in centimeters.                                                               |
| rok                                                           | Same meaning as for point detectors, but describes a sphere about the point selected on the k th ring detector ( 3 ). |

ND

Default: None.

## Details:

- 1 For more than one detector with the same n or na designation, sets of the input parameters (quadruplets for F n or triplets for F na ) are simply continued on the same F n or F na card.
- 2 If more than one detector of the same type (an F5 : n and an F15 : n , for example) are at the same location, the time-consuming contribution calculation upon collision is made only once and not independently for each detector. Thus it is inexpensive to add more than one detector (each with a different response function, for example) at the same location.
- 3 The radius of the sphere of exclusion, ± rok , should be about 1/8 to 1/2 mean free path for particles of average energy at the sphere and zero in a void. Supplying rok in terms of mean free path will increase the variance and is not recommended unless you have no idea how to specify it in centimeters.

## /warning\_sign Caution

The exclusion sphere should not encompass more than one material. MCNP6
cannot verify this and the consequences may be wrong answers.

- 4 The printout for detectors is normally in two parts: (1) the total of all contributions to the detector (as a function of any defined bins such as energy) and (2) the direct (or un-collided) contribution to the detector from the source. The direct contribution is always included in the total of all contributions. Adding the symbol ND at the end of a type 5 detector tally card inhibits the separate printing of the direct contribution for that tally. In coupled neutron/photon problems, the direct contribution in photon tallies is from photons created at neutron collisions.

## 5.9.1.3 The Radiography Tally

MCNP6 can generate simulated radiography images as one would expect to
see from an x-ray or pinhole projection of an object containing the
particle source. This allows the recording of both the direct (source)
image as well as that due to background (scatter). This tool is an
invaluable aid to the problem of image enhancement, or extracting the
source image from a background of clutter. MCNP6 includes two types of
image capability; the pinhole image projection and the transmitted image
projection.

The radiography capability is based on point detector techniques, and is
extensively described in [305, 306]. In essence, the radiography focal
plane grid is an array of point detectors.

## 5.9.1.3.1 FIP: Pinhole Image Projection

## /\_445 Deprecation Notice

DEP-53484

The PI card formerly used by MCNPX for pinhole image projection is
replaced by the FIP card. The input format is identical.

Optional keyword to inhibit the separate printing of the direct
contribution for that detector tally ( 4 ).

FIP establishes a flux image through a pinhole to a planar grid. In the
pinhole image projection case, a point is defined in space that acts
much like the hole in a pinhole camera and is used to focus an image
onto a grid which acts much like the photographic film. The pinhole is
actually a point detector and is used to define the direction cosines of
the contribution that is to be made to the grid. The pinhole position
relative to the grid is also used to define the element of the grid into
which this contribution is scored. Once the direction is established, a
ray-trace contribution is made to the grid bin with attenuation being
determined for the material regions along that path. The source need not
be within the object being imaged, nor does it need to produce the same
type of particles that the detector grid has been programmed to score.
The grid and pinhole will image either source or scattered events
produced within the object (see NOTRN card) for either photons or
neutrons. These event-type contributions can be binned within the grid
tallies by binning as source only, total, or by using special binning
relative to the number of collisions contributing cells, etc. Steps to
define the image grid for a pinhole image are provided later in this
section.

| n        | Tally number, tally type 5. Restriction: n ≤ 99999999                                                                                                                                                                          | Tally number, tally type 5. Restriction: n ≤ 99999999                                                                                                                                                                          |
|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P        | Particle designator: Restriction: n for neutrons or p for photons only.                                                                                                                                                        | Particle designator: Restriction: n for neutrons or p for photons only.                                                                                                                                                        |
| x1 y1 z1 | The coordinates of the pinhole center.                                                                                                                                                                                         | The coordinates of the pinhole center.                                                                                                                                                                                         |
| r0       | Always 0 (zero) for this application. Note: neither the pinhole nor the grid should be located within a highly scattering media.                                                                                               | Always 0 (zero) for this application. Note: neither the pinhole nor the grid should be located within a highly scattering media.                                                                                               |
| x2 y2 z2 | The reference coordinates (center of object) that establish the reference direction cosines for the normal to the detector grid. This direction is defined as being from ( x2 , y2 , z2 ) to the pinhole at ( x1 , y1 , z1 ) . | The reference coordinates (center of object) that establish the reference direction cosines for the normal to the detector grid. This direction is defined as being from ( x2 , y2 , z2 ) to the pinhole at ( x1 , y1 , z1 ) . |
| f1       | If                                                                                                                                                                                                                             | If                                                                                                                                                                                                                             |
| f1       | f1 > 0                                                                                                                                                                                                                         | this value is the radius of a cylindrical collimator, centered on and parallel to the reference direction, which establishes a radial field of view through the object and surrounding materials and onto the image grid.      |
| f1       | f1 = 0                                                                                                                                                                                                                         | the value of the radius is 'large.' (DEFAULT)                                                                                                                                                                                  |
| f2       | The radius of the pinhole perpendicular to the reference direction. If                                                                                                                                                         | The radius of the pinhole perpendicular to the reference direction. If                                                                                                                                                         |
| f2       | f2 = 0                                                                                                                                                                                                                         | this represents a perfect pinhole.                                                                                                                                                                                             |
| f2       | f2 > 0                                                                                                                                                                                                                         | the point within the pinhole through which the particle flux contribution will pass is picked randomly (i.e., uniformly in area) for each source and scatter event. This simulates a less-than-perfect pinhole.                |
| f3       | The distance from the pinhole at ( x1 , y1 , z1 ) to the center of the detector grid along the direction established from ( x2 , y2 , z2 ) to ( x1 , y1 , z1 ) . The image grid is perpendicular to this reference vector.     | The distance from the pinhole at ( x1 , y1 , z1 ) to the center of the detector grid along the direction established from ( x2 , y2 , z2 ) to ( x1 , y1 , z1 ) . The image grid is perpendicular to this reference vector.     |

## Details:

- 1 Only one pinhole image tally per FIP card is allowed. The point detector Russian roulette game is not used with the FIP tally. Consider use of the NOTRN card for only direct contributions and the TALNP card

to reduce the size of the MCNP output file for large-image grids. The
image grid should not be in a scattering material because the point
detector average flux neighborhood is not used for flux image tallies.

## 5.9.1.3.2 FIR and FIC Transmitted Image Projection

## /\_445 Deprecation Notice

DEP-53482

The TIR and TIC cards formerly used by MCNPX for pinhole image
projection are replaced by the FIR and FIC cards, respectively. The
input format is identical.

FIR establishes a flux image on a rectangular radiograph planar grid,
and FIC establishes a flux image on a cylindrical radiograph grid.

In the transmitted image projection case, the grid acts like a film pack
in an x-ray type image, or transmitted image projection. In both cases,
for every source or scatter event a ray-trace contribution is made to
every bin in the detector grid. This eliminates statistical fluctuations
across the grid that would occur if the grid location of the
contribution from each event were to be picked randomly, as would be the
case if one used a DXTRAN sphere and a segmented surface tally. For each
event, source or scatter, the direction to each of the grid points is
determined, and an attenuated ray-trace contribution is made. As in
pinhole image projection, there are no restrictions as to location or
type of source used. These tallies automatically bin in a source-only
and a total contribution. Steps to define the image grid for transmitted
images are provided later in this section.

When this type of detector is being used in a problem, if a contribution
is required from a source or scatter event, an attenuated contribution
is made to each and every detector grid bin. Because for some types of
source distributions very few histories are required to image the direct
or source contributions, an additional entry has been added to the NPS
card to eliminate unwanted duplication of information from the source.

<!-- image -->

| Rectangular-grid Data-card Form: FIR n : P x1 y1 z1 r0 x2 y2 z2 f1 f2 f3 or Cylindrical-grid Data-card Form: FIC n : P x1 y1 z1 r0 x2 y2 z2 f1 f2 f3   | Rectangular-grid Data-card Form: FIR n : P x1 y1 z1 r0 x2 y2 z2 f1 f2 f3 or Cylindrical-grid Data-card Form: FIC n : P x1 y1 z1 r0 x2 y2 z2 f1 f2 f3                                                                                                                                                                                                                        |
|--------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                                                                                                                                      | Tally number, tally type 5. Restriction: n ≤ 99999999                                                                                                                                                                                                                                                                                                                       |
| P                                                                                                                                                      | Particle designator: Restriction: n for neutrons or p for photons only.                                                                                                                                                                                                                                                                                                     |
| x1 y1 z1                                                                                                                                               | The coordinates of the center of the detector flux image grid, the extent and spacing of which are defined by the entries on the tally segment ( FS ) and cosine ( C ) cards. In the planar rectangular grid case, this point defines the center of the grid. In the cylindrical grid case, this point defines the center of the cylinder on which the grid is established. |
| r0                                                                                                                                                     | Always 0 (zero) in this application. Do not locate the image grid in a scattering material.                                                                                                                                                                                                                                                                                 |
| x2 y2 z2                                                                                                                                               | The reference coordinates (center of object) that establish the reference direction cosines for the outward normal to the detector grid plane, as from ( x2 , y2 , z2 ) to ( x1 , y1 , z1 ) . This direction is used as the outward normal to the detector grid plane for the FIR case, and as the centerline of the cylinder for the FIC case.                             |
| f1                                                                                                                                                     | If                                                                                                                                                                                                                                                                                                                                                                          |

|    | f1 > 0                                                                                                                                                                                                                                                                                                                                    | only the scattered contributions will be scored. (See Note 2.)                                                                                                                                                                                                                                                                            |
|----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| f2 | Radial field of view. Planar grid case: Radial restriction relative to the center of the grid to define a radial field of view on the grid for contributions to be made. If f2 = 0 , no radial restriction exists. (DEFAULT) Cylindrical grid case: Radius of the cylindrical surface of the image grid. If f2 = 0 , it is a fatal error. | Radial field of view. Planar grid case: Radial restriction relative to the center of the grid to define a radial field of view on the grid for contributions to be made. If f2 = 0 , no radial restriction exists. (DEFAULT) Cylindrical grid case: Radius of the cylindrical surface of the image grid. If f2 = 0 , it is a fatal error. |
| f3 | If                                                                                                                                                                                                                                                                                                                                        | If                                                                                                                                                                                                                                                                                                                                        |
|    | f3 = 0                                                                                                                                                                                                                                                                                                                                    | all flux contributions are directed to the center of each grid bin.                                                                                                                                                                                                                                                                       |
|    | f3 = 1                                                                                                                                                                                                                                                                                                                                    | contributions are made with a random offset from the center of the image grid bin. This offset remains fixed and is used as the offset for contributions to all of the grid bins for this event.                                                                                                                                          |

## Details:

- 1 Only one flux image detector is allowed on each FIC or FIR card. The point detector Russian roulette game is not used with FIC or FIR tallies. Consider use of the NOTRN card for only direct contributions, the second entry on the NPS card for limiting the direct FIR contributions, and the TALNP card to reduce size of the MCNP output file for large-image grids.
- 2 The scattered contributions can often be made on a much coarser image grid because there is much less structure to the scattered image. Use f1 = -1 in this case. The NOTRN card can be used to obtain only the direct image with f1 = 0 .

## 5.9.1.3.3 Defining an FIP, FIR, or FIC Image Grid Using Space and Cosine Segmenting Cards

The grid plane is in the two-dimensional ( s, t ) coordinate system
where the s and t axes are orthogonal to the reference direction. The s
and t dimensions are established from entries on tally segment ( FS n )
and cosine ( C n ) cards, where the tally number n matches the flux
image tally number.

In the case of FIP and FIR , the image-plane rectangular grid dimensions
are defined by setting the first entry on the FS n and C n cards to the
lower limit (in centimeters) of the first image bin for the s axis and t
axis, respectively. The other entries on the FS n and C n cards set the
upper limit of each of the bins. These limits are set relative to the
intersection of the reference direction and the grid plane.

In the cylindrical ( FIC ) grid case, the entries on the FS n card are
the distances along the symmetry axis of the cylinder from ( x1 , y1 ,
z1 ) , and the entries on the C n card are the angles in degrees as
measured counterclockwise from the positive t axis.

The relationship of the s axis, t axis, and reference direction for the
planar image grid is calculated by MCNP6 and follows the right-hand
rule. Since the orientation of the s axis and the t axis is dependent on
the

1

2

reference direction in the geometry coordinate system, the MCNP6 tally
output should be examined to see the direction cosines of these two
planar image grid axes. These limits should be defined taking into
account any image size change at the grid caused by magnification. The
image grid should not be in a scattering material because the point
detector average flux neighborhood is not used for flux image tallies.

There is no limit to the number of image grid bins that can be defined
by FS n and C n . However, it is easy to define a tally with a huge
number of point detectors. For example, a 1000 × 1000 grid is the
equivalent of 1-million point detectors, which could take a long time to
run. Fatal errors will result if the FS n and C n card bin
specifications are not each monotonically increasing. The default tally
fluctuation chart bin is the last FS n and C n bin in the total (direct
plus scattered) detector tally. FS0 and C0 cards for these image tallies
are not allowed. The T (total) and C (cumulative) options for the FS n
and C n cards are not available for flux image tallies.

The directions of the t axis and s axis of the grid are set up such that
if the reference direction (the outward normal to the grid plane) is not
parallel to the z axis of the geometry, the t axis of the grid is
defined by the intersection of the grid plane and plane formed by the z
axis and the point where the reference direction would intersect the
grid plane. If the reference direction is parallel to the z axis of the
geometry, then the t axis of the grid is defined to be parallel to the y
axis of the geometry. The s axis of the grid is defined as the cross
product of a unit vector in the ' t ' direction and a unit vector in the
reference direction. If the reference direction is not parallel to the z
axis, MCNP6 calculates the orthogonal axes. The s and t image axes
direction cosines are printed in the MCNP output file.

## Example 1

| FSn   |   -20. | 99i   |   15. |
|-------|--------|-------|-------|
| Cn    |    -25 | 99i   |    10 |

These two cards set up a 100 × 100 grid that extends from -20 cm to 15
cm along the s axis, from -25 cm to 10 cm along the t axis, and has
10,000 equal sized bins. These bins need not be equal in size nor do
they need to be symmetric about the reference direction.

## 5.9.1.3.4 Reading or Plotting the Radiography Tally Output

Pinhole and radiography tallies can be plotted directly in the MCNP6
tally plotter from the runtape or mctal files. To create a 2-D contour
plot of the s and t axes enter FREE SC . The MCNPTools mctal2rad utility
[307] can also plot radiograph tallies. In addition, the gridconv
utility [Appendix E.4] can format radiograph tallies results for
external graphics programs.

## 5.9.1.4 Pulse-height Tally (Tally Type 8)

The pulse-height tally is a radical departure from other MCNP6 tallies.
All other tallies are estimates of macroscopic variables, such as flux,
whose values are determined by very large numbers of microscopic events.
The pulse-height tally records the energy or charge deposited in a cell
by each source particle and its secondary particles. For other tallies
it is not necessary to model microscopic events realistically as long as
the expectation values of macroscopic variables are correct. For the
pulse-height tally, microscopic events must be modeled much more
realistically.

The departures from microscopic realism in MCNP6 are everywhere. The
number, energies, and directions of the secondary neutrons and photons
from a neutron collision are sampled without any correlation between

1

the particles and with no regard for the conservation of energy. The
fluctuations in the energy loss rate of an electron are not correlated
with the production of knock-on electrons and x-rays. The variance-
reduction schemes in MCNP6 distort the natural random walk process in
various ways; nevertheless, they give correct results for macroscopic
tallies when appropriate weighting factors are used.

Problems that give correct pulse height tallies are severely limited.
For example, the pulse-height tally does not work well with neutrons
because of the non-analog nature of neutron transport that departs from
microscopic realism at every turn. One can have a neutron source in a
MODE n p or n p e problem, but only the photons and electrons can be
tallied on the F8 card. The F8 tally can be used effectively in photon
problems. Electron problems may give correct results as long as the
tally cells are thick enough for the errors in the energy loss rate to
average out. Combining F8 tallies with a photonuclear bias is a fatal
error. MCNP6 tries to detect conditions in a problem that would
invalidate pulse height tallies, but it is not able to catch all of
them. The user must ascertain that his problem does not violate the
necessary conditions for obtaining correct answers.

Scoring the pulse-height tally is done at the end of each history. In
the absence of variance reduction, the scoring is reasonably easy to
describe. For example, consider a unit weight source and an F8 tally in
cell 7. Suppose that on a given particle history that there are K
entries into cell 7 and L departures from cell 7. The tally energy
associated with an F8 tally is the kinetic energy of the particle plus
1.022016 MeV if it is a positron. Particles can enter cell 7 either by
crossing a boundary into cell 7 or entering cell 7 as a source event.
Particles depart cell 7 either by capture in cell 7 or by crossing a
boundary out of cell 7. Let E i be the i th tally energy of a particle
entering cell 7 and let D j be the j th tally energy of a particle
departing cell 7. The total energy deposited in cell 7 is

<!-- formula-not-decoded -->

Suppose the pulse height bins are specified on the E8 card as:

## E8 T1 T2 T3 T4 T5

If T m -1 &lt; T &lt; T m , then MCNP6 will post a unit tally in the m th bin.
If the problem is analog but the source weight is w s , then w s would
be posted in the m th bin. If there is an asterisk on the F8 card (i.e.,
* F8 ), then MCNP6 tallies w s T in the m th bin. If there is a plus on
the F8 card (i.e., +F8 ), then MCNP6 posts the net charge change times
the w s into the m th bin. That is, an entering electron or a departing
positron constitutes a charge change of -1 , whereas a departing
electron or an entering positron constitutes a charge change of +1 .

The scoring details are more complex with pulse-height tally variance
reduction [66].

One common application of the F8 tally is simulation of the energy
distribution of pulses created in a detector by radiation. The union of
tallies produces a tally sum, not an average. Cell, user, and energy bin
cards are allowed. Flagging and multiplier bins are not allowed.
Segment, time, and cosine bins are permitted with certain FT options.
Use of the dose energy ( DE ) and dose function ( DF ) cards is also
disallowed with the F8 tally.

The energy bins in the F8 pulse-height tally are different from those of
all other tallies. Rather than tally the particle energy at the time of
scoring, the number of pulses depositing energy within the bins are
tallied. That is, the meaning of the energy bins of a pulse-height tally
is the energy deposited in a cell bin by all the physically associated
tracks of a history. Care must be taken when selecting energy bins for a
pulse-height tally. It is recommended that a zero bin and an epsilon bin
be included such as

1

```
E8 0 1E-5 1E-3 1E-1 ...
```

The zero bin will catch non-analog knock-on electron negative scores.
The epsilon ( 10 -5 ) bin will catch scores from particles that travel
through the cell without depositing energy.

With the FT8 special tally treatments card the F8 tally can become an
anti-coincidence pulse-height tally ( FT8 PHL ) or a different kind of
tally altogether. For example, FT8 CAP is a neutron coincidence capture
tally, and FT8 RES tallies the residual nuclides from physics-model
evaporation and fission models. These variations have special rules
regarding possible variance reduction, time bins, and other issues.

## 5.9.1.4.1 Pulse-height Tally Variance Reduction

Variance reduction for F8 tallies is implemented for electrons and
photons; however, not a lot of experience exists to guide the user.
Experience suggests that weight windows be used instead of geometry
splitting for F8 tallies. Many of the variance-reduction techniques that
were designed for lowering the variance on other tally types may be used
with the F8 tally. Allowed variance reduction techniques include

- Splitting/roulette ( IMP card)
- Implicit capture and weight cutoff ( CUT card)
- Weight window ( WWN card)
- Forced collisions ( FCL card)
- Exponential transform ( EXT card)
- DXTRAN ( DXT card)
- Weight roulette on DXTRAN particle ( DD card)
- DXTRAN cell probabilities ( DXC card)
- Source biasing ( SB card)
- Energy splitting ( ESPLT card)
- Time splitting ( TSPLT card)

The roulette associated with splitting/roulette ( IMP card) and weight
windows ( WWN card) may be less useful than it is for nonF8 tallies;
roulette may be turned off by setting the keyword RR = off on the VAR
card. Although implicit capture and weight cutoff have been implemented,
in most cases these games are turned off by default if an F8 tally is in
the problem. An exception occurs if forced collisions also are used in
the problem.

Note that the weight-window generator was designed for nonF8 tallies;
the generator should not be used for F8 tallies. The generator estimates
the importance of a single particle at a phase-space point p . The
generator cannot estimate the importance of a collection of K particles
at phase-space points p 1 , p 2 , . . . , p k . To see what is involved
with making a generator work with F8 , see [308]. Instead, a useful
weight window often can be generated using a tally such as an F4 tally
in the same cell as the F8 tally.

Figure 5.12: Example of exponential transform applied to both branches of a pair annihilation event.

<!-- image -->

## 5.9.1.4.2 Pulse-height Tally Variance Reduction: Discussion Using Examples

The MCNP6 pulse height variance-reduction theory is described in detail
in [65, 66]. Two simple examples are given in this manual to give the
reader an idea of how MCNP6 does variance reduction with pulse height
tallies. The essential idea is that MCNP6's deconvolution method
reconstructs physically possible random walks and assigns an appropriate
tally weight based on how much the variance reduction has distorted the
frequency of obtaining the walks. For example, if a random walk has been
made twice as likely to occur in the simulation as it would naturally,
then this random walk will be assigned at weight of 1 / 2 so that the
expected tallies are preserved.

Let's suppose, as depicted in Fig. 5.12, that there is a pair
annihilation event and an exponential transform is applied to both
0.511-MeV branches. Assume this is the only variance reduction used.
Because the exponential transform samples a non-analog density, there
will be a weight multiplication to account for this. The left branch has
a track weight of 1 / 5 indicating that the left branch's random walk
was made 5 times more likely to occur as it would have without applying
the exponential transform. Similarly, the right branch has a track
weight of 1 / 3 indicating that the right branch's random walk was made
3 times more likely to occur as it would have without applying the
exponential transform. Assuming that none of the E i is in the same bin,
the tally for the total current into the cell is tallied as

- 1 / 5 in the energy bin around E 5
- 1 / 5 in the energy bin around E 7
- 1 / 3 in the energy bin around E 1
- 1 / 3 in the energy bin around E 3

and the total current leaving the cell is tallied as

- 1 / 5 in the energy bin around E 6
- 1 / 5 in the energy bin around E 7

Figure 5.13: F8 Tally Splitting example.

<!-- image -->

- 1 / 3 in the energy bin around E 2
- 1 / 3 in the energy bin around E 4

By contrast, as explained below, the F8 tally for this history is (1 /
5)(1 / 3) in the energy bin around E 5 -E 6 + E 7 -E 7 + E 1 -E 2 + E 3
-E 4 . Note that the F8 tally depends on the energy deposited
collectively by both branches of the pair annihilation event. If the
history above had been sampled without the exponential transforms, then
the F8 tally would have been 1 in the energy bin around E 5 -E 6 + E 7
-E 7 + E 1 -E 2 + E 3 -E 4 .

Note that the physical walk contributes E 5 -E 6 + E 7 -E 7 + E 1 -E 2 +
E 3 -E 4 regardless of how often the walk is sampled. With the variance
reduction applied here, the particular walk sampled occurred 5 × 3 = 15
times as often as it would in an analog calculation. Thus, the F8 tally
credits the physical energy bin with a weight factor of 1 / 15 ,
correcting for the fact that the annihilation pair has been made 15
times as likely to execute the walk that contributes E 5 -E 6 + E 7 -E 7
+ E 1 -E 2 + E 3 -E 4 as it should have. Note that it is a physical
collection of particles that now carries the tally modification weight
because it is the physical collection that tallies to the F8 tally
rather than just the individual tracks as with other tallies in MCNP6.

The second example, illustrated by Fig. 5.13, considers a 2:1 splitting
event and no other variance reduction methods. Note that splitting is a
mathematical artifice; only one physical particle exists after crossing
the splitting surface. What the splitting does is give two (usually)
different samples of the random walk after crossing the splitting
surface. Both of these random walks do not physically occur at the same
time. If the left split branch occurs then the right split branch does
not and vice versa. Because the splitting represents a doubling of the
sampling frequency for either branch, the branches are each assigned a
weight of 1 / 2 . The energy bins associated with taking the left split
branch or the right split branch are, respectively, E 5 -E 6 + E 7 -E 7
+ E 1 -E 8 or E 5 -E 6 + E 7 -E 7 + E 1 -E 2 + E 3 -E 4 . The pulse-
height tally is thus 1 / 2 in the energy bin around E 5 -E 6 + E 7 -E 7
+ E 1 -E 8 and 1 / 2 in the energy bin around E 5 -E 6 + E 7 -E 7 + E 1
-E 2 + E 3 -E 4 .

```
Simple Data-card Form: F n : P s1 . . . sK or General Data-card Form: F n : P s1 ( s2 . . . s3 ) ( s4 . . . s5 ) s6 s7 . . . T n User-supplied tally number, ending in the numeral 8. Restriction: n ≤ 99999999
```

1

| P   | Particle designator. Standard F8 tallies support only ' p , e ' (if only one of these is specified, it is expanded to include both). Other particle types should only be specified with the FT PHL or CAP options ( 2 ).   |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| sk  | Problem number of cell for tallying, or T for the total across all listed cells.                                                                                                                                           |
| T   | Provide average of tally over specified cells. (Optional)                                                                                                                                                                  |

## Details:

- 1 An asterisk on the F8 card converts the tally from a pulse-height tally to an energy deposition tally. A plus on the F8 card converts the tally from a pulse-height tally to a charge deposition tally in units of charge. Energy binning is not recommended with the +F8 tally.
- 2 Both photons and electrons will be tallied if present, even if only e or only p is on the F8 card. In other words, F8 : p , F8 : e , and F8 : p , e are all equivalent tallies.

## 5.9.1.4.3 Example 1

```
F8:E 1
```

or

```
1 F1:E 2 2 FT1 ELC 1 3 C1 0 1
```

The +F8 charge deposition tally can be checked against an electron F1 :
e surface tally with the FT ELC option if the volume of the +F8 is
exactly enclosed by the surfaces on the F1 : e card. For example, if
cell 1 is enclosed by spherical surface 2, then the above tallies give
the same result provided the two F1 current tally bins (in minus out)
are properly subtracted.

## 5.9.1.5 Repeated Structures Tallies (Tally Types 1, 2, 4, 6, 7, and 8)

```
Simple Data-card Form: F n : P s1 . . . sK or General Data-card Form: F n : P s1 ( s2 . . . s3 ) (( s4 s5 ) < ( c1 c2 [ i1 . . . i2 ]) < U = # ( c3 c4 c5 )) . . . T n Tally number. Restriction: n ≤ 99999999 P Particle designator. sk Problem number of a surface or cell for tallying or U = # . ck Problem number of a cell filled with a universe or U = # .
```

| T     | Average or total over specified surfaces or cells, depending on type of tally. (Optional)                                        |
|-------|----------------------------------------------------------------------------------------------------------------------------------|
| U = # | Problem number of a universe used on a FILL card.                                                                                |
| ik    | Index data for a lattice cell element, with three possible formats (always in brackets). If                                      |
| ik    | ik = i1 then ik indicates the 1st lattice element of the given cell, as defined by the FILL array.                               |
| ik    | ik = i1 : i2 i3 : i4 i5 : i6 then ik indicates a range of one or more lattice elements. Use the same format as on the FILL card. |
| ik    | ik = i1 i2 i3 , i4 i5 i6 then ik indicates individual lattice elements [ i1 , i2 , i3 ] , [ i4 , i5 , i6 ] , etc.                |

Use: Consider using the SPDTL card.

In the simple repeated-structure tally form, MCNP6 creates k surface or
cell bins for the requested tally, listing the results separately for
each surface or cell. In the more general form, a bin is created for
each surface or cell listed separately and for each collection of
surfaces or cells enclosed within a set of parentheses. A tally bin can
involve a single tally level or multiple tally levels. Tallies involving
repeated structure and lattice geometries can use either form.

Some operators and nomenclature need to be introduced before the
explanation of repeated structures and lattice tallies. The left arrow
or less than symbol &lt; is used to identify surfaces or cells within
levels of repeated structures. See §5.5.5.1 for an explanation of
geometry levels. A tally bin that includes one or more left arrows
implies multiple levels, called a chain. Multiple entries enclosed by
parentheses at any level of a tally chain indicate the union of the
items. Brackets [ . . . ] immediately following a filled lattice cell
identify one or more elements of that lattice.

## 5.9.1.5.1 Multiple Bin Format

In addition to multiple levels, multiple entries can be used in each
level of the tally chain resulting in multiple output bins. Within the
parentheses required around the tally bin chain, other sets of
parentheses can be used to indicate the union of cells as in a simple
tally description, resulting in fewer output tally bins. For example,

<!-- formula-not-decoded -->

results in one output tally bin and will be the union of the tally in s4
plus s5 that fill c1 or c2 elements [ i1 . . . i2 ] and when c1 or c2
fills cells c3 , c4 , or c5 . Removing the first and third inner
parentheses, i.e.,

<!-- formula-not-decoded -->

1

2

3

4

5

results in the creation of 2 × 1 × 3 = 6 bins as follows:

```
( s4 < ( c1 c2 [ i1 . . . i2 ]) < c3 ) , ( s4 < ( c1 c2 [ i1 . . . i2 ]) < c4 ) , ( s4 < ( c1 c2 [ i1 . . . i2 ]) < c5 ) , ( s5 < ( c1 c2 [ i1 . . . i2 ]) < c3 ) , ( s5 < ( c1 c2 [ i1 . . . i2 ]) < c4 ) , ( s5 < ( c1 c2 [ i1 . . . i2 ]) < c5 ) .
```

The repeated structure/lattice input tally bin format with levels that
have multiple entries automatically creates multiple output tally bins.
The total number of bins generated is the product of the number of
entries at each level. If parentheses enclose all entries at a level,
the number of entries at that level is one and results in the union of
all those entries. For unnormalized tallies (types 1, 8), the union is a
sum. For normalized tallies (types 2, 4, 6, 7), the union is an average.
A symbol T on the tally line creates an additional tally bin that is the
union or total of all the other tally bins.

## 5.9.1.5.2 Brackets

Brackets [ . . . ] enclose index data for lattice cell elements.
Brackets make it possible to tally on a cell or surface only when it is
within the specified lattice elements. The brackets must immediately
follow a filled lattice cell. Listing a lattice cell without brackets
will produce a tally when the tally cell or surface is in any element of
the lattice, provided the tally cell or surface fills an entry at all
other levels in the chain. The use of brackets is limited to levels
after the first ' &lt; ' symbol in the tally specification.

To tally within lattice elements of a real world (level zero) lattice
cell, use the special syntax that follows. Cell 3 contains material 1
and is bounded by four surfaces. The F4 card specifies a tally only in
lattice element [0 , 0 , 0] . This syntax is required because brackets
can only follow a &lt; symbol:

```
3 1 -1.0 -1234 lat=1 . . . F4:N (3 < 3 [0 0 0])
```

## 5.9.1.5.3 Universe Format

The universe format, U = # , is a shorthand method of including all
cells and lattice elements filled by universe # . The example shown in
Listing 5.49 demonstrates this universe-expansion capability with the
tally definition and comments representing the expanded form.

```
1 f214:n ((1000 1100) < 2000 < 3000) $ ((1000 1100) < 2000 < 3000) 2 f224:n ((1000 1100) < 2000 < 3100) $ ((1000 1100) < 2000 < 3100) 3 f234:n ((1000 1100) < (u = 1) < 3000) $ ((1000 1100) < (2000) < 3000)) 4 f244:n ((1000 1100) < (u = 1) < 3100) $ ((1000 1100) < (2000) < 3100)) 5 f254:n ((1000 1100) < 2000 < (u = 2)) $ ((1000 1100) < 2000 < (3000 3100)) 6 f264:n ((1000 1100) < (u = 1) < (u = 2)) $ ((1000 1100) < (2000) < (3000 3100)) 7 f274:n ((1000 1100) < (u = 1) < u = 2) $ ((1000 1100) < (2000) < 3000 3100) 8 f284:n ((1000 1100) < u = 1 < (u = 2)) $ ((1000 1100) < 2000 < (3000 3100))
```

Listing 5.49: example\_tally\_universe\_expansion\_stochastic\_volume.mcnp.inp.txt

```
9 f294:n ((1000 1100) < u = 1 < u = 2) $ ((1000 1100) < 2000 < 3000 3100) 10 f204:n ((1000 1100) < u = 2) $ ((1000 1100) < 3000 3100) 11 f314:n ( 1000 1100 < u = 1 < u = 2) $ ( 1000 1100 < 2000 < 3000 3100)
```

Note that inner parentheses are used to indicate unions of cells in the
expansion, which can lead to fewer bins than otherwise. Accordingly, in
complex geometries, the U = # format should be used sparingly,
especially with the multiple bin format. If 100 cells are filled by
universe 1 and 10 cells are filled by universe 2 (which contains
universe 1), then 1000 tally bins will be created if unions are not
used.

Further, note that if contained cells in interstitial universes (not the
highest or lowest level) are defined at varying levels of universe
nesting in the same calculation, this universe expansion may be expanded
incorrectly. As such, one should verify that the expansion has been
performed correctly and to provide explicit input if it is found to be
incorrect. A way to induce this incorrect behavior is to create a third
box as cell 3200 below the current two boxes using the input in Listing
5.49 and to fill it with universe 1 (skipping universe 2). In this
example, because universe 1 is now contained in both universes 2 and 3,
an incorrect universe expansion may appear in the MCNP output file as
cell (1000 1100&lt;2000 3200&lt;3000) (expanded from f034:n ((1000 1100) &lt; (u
= 1) &lt; 3000) ) or similar where the new cell 3200 is contained in cells
at the same universe nesting level (cells 3000 and/or 3100), which is
incorrect.

## 5.9.1.5.4 Example

This example shown in Listing 5.50 runs significantly faster with MCNP6
than with MCNP4C.

```
1 21x21x21 void lattice of spheres 2 11 0 -31 u=1 imp:p=1 3 12 0 31 u=1 imp:p=1 4 16 0 -32 u=2 imp:p=1 lat=1 fill= -10:10 -10:10 -10:10 1 9260R 5 17 0 -33 fill=2 imp:p=1 6 18 0 33 imp:p=0 7 8 31 so 0.5 9 32 rpp -1 1 -1 1 -1 1 10 33 rpp -21 21 -21 21 -21 21 11 12 mode p 13 sdef 14 f4:p (11<16[-10:10 -10:10 -10:10]<17) 15 print 16 nps 10000
```

Listing 5.50: example\_repeated\_structure\_tally.mcnp.inp.txt

Larger lattices and nested lattices offer even more dramatic speedups.

## 5.9.1.5.5 Use of SD Card for Repeated Structures Tallies

MCNP6 may be unable to calculate required volumes or areas for tallies
involving repeated-structure and lattice geometries. For example, a
universe can be repeated a different number of times in different cells
and the code has no way to determine this.

There are two distinct options for entries on the SD card relating to
repeated structures and they cannot be mixed within a single tally.

The first option is to enter a value for each first level entry on the
related F card. If the entry on the F card is the union of cells, the SD
card value will be the volume of the union of the cells. An example of
this is shown in Listing 5.51.

```
1 f114:n (1000 < 2000 < 3000) (1100 < 2000 < 3000) 2 f124:n ((1000 1100 1200) < 2000 < 3000) 3 f134:n (1200 < 2000 < 3000) 4 f144:n ((1000 1100 1200) < 2000 < 3000) (2100 < 3000) t 5 f154:n (2100 < 3000) 6 f164:n ((1000 1100 1200) < 2000 < 3000) ((1000 1100 1200) < 2000 < 3100) 7 (2100 < 3000) (2100 < 3100) 4000 t 8 f174:n 4000 9 c 10 sd114 1 1 11 sd124 1 12 sd134 1 13 sd144 1 1 1 14 sd154 1 15 sd164 1 1 1 1 1 1 16 sd174 1
```

Listing 5.51: example\_tally\_universe\_expansion\_stochastic\_volume.mcnp.inp.txt

The second option is to enter a value for each bin generated by the F
card. An example of this is shown in Listing 5.52 (which correspond to
the tallies shown in Listing 5.13).

```
1 sd214 1 2 sd224 1 3 sd234 1 4 sd244 1 5 sd254 1 6 sd264 1 7 sd274 1 8 sd284 1 9 sd294 1 10 sd204 1 11 sd314 1 1 1 1
```

Listing 5.52: example\_tally\_universe\_expansion\_stochastic\_volume.mcnp.inp.txt

## 5.9.2 FC: Tally Comment

```
Data-card Form: FC n info n Tally number. Restriction: n ≤ 99999999 info Provides title for tally in MCNP output and MCTAL files ( 1 ).
```

Default: No comment.

Use: Encouraged, especially when using a modified or non-standard tally.

1

## Details:

- 1 The FC card can be continued only by blanks in columns 1-5 on succeeding lines. The &amp; continuation symbol is considered part of the comment and not recognized as a continuation command. Like other cards, the line-length limit given in Table 4.1 applies.

## 5.9.3 E: Tally Energy Bins

This card is used to assign energy-bin boundaries for tallies to
accumulate results into. If it is not present, the results are
accumulated into a single 'total' bin regardless of the particle energy.

| Data-card Form: E n e1 . . . eK [ NT ] [ C ]   | Data-card Form: E n e1 . . . eK [ NT ] [ C ]                                                                                                          |
|------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                              | Tally number. Restriction: n ≤ 99999999                                                                                                               |
| ek                                             | Upper bound (in MeV) of the k th energy bin for tally n ( 2 ).                                                                                        |
| NT                                             | Optional notation at the end of the input line to inhibit the automatic total over all specified energy bins.                                         |
| C                                              | Optional notation at the end of the input line to cause the bin values to be cumulative and the last energy bin to be the total over all energy bins. |

Default: If the E card is absent, there will be one bin over all
energies unless this default has been changed by an E0 card.

Use: Required if EM card is used.

## Details:

- 1 An E0 card can be used to set up a default energy-bin structure for all tallies. A specific E n card will override the default structure for tally n .
- 2 The energies on the E card must be entered in the order of increasing magnitude. If a particle has energy greater than the last entry, it is not tallied and a warning is issued. A comment is printed if the last energy bin is greater than the upper limit specified on the PHYS card.

## 5.9.3.1 Example 1

```
E11 0.1 1 20
```

This card will separate an F11 current tally into four energy bins:

1. from the lower energy cutoff to 0.1 MeV,
2. from 0.1 to 1.0 MeV,
3. from 1.0 to 20.0 MeV, and
4. a total over all energy.

## 5.9.4 T: Tally Time Bins

This card is used to assign time-bin boundaries for tallies to
accumulate results into. If it is not present, the results are
accumulated into a single 'total' bin regardless of the particle time.

```
Data-card Form: T n t1 . . . tK [ NT ] [ C ] or Data-card Form: T n keyword = values(s) n Tally number. Restriction: n ≤ 99999999 tk Upper bound (in shakes) of the k th time bin for tally n ( 2 ). NT Optional notation at the end of the input line to inhibit the automatic total over all specified time bins. C Optional notation at the end of the input line to cause the bin values to be cumulative and the last time bin to be the total over all time. CBEG = value Reference starting time in shakes (sh) (DEFAULT: CBEG = 0 ) CFRQ = value Frequency of cycling in 1/sh or 1/time width COFI = value Dead time interval in shakes CONI = value Alive time interval in shakes CSUB = value Number of subdivisions to use within alive time (DEFAULT: CSUB = 1 ) CEND = value Reference ending time in shakes (optional)
```

Default: If the T card is absent, there will be one bin over all times
unless this default has been changed by a T0 card; CBEG = 0 ; CSUB = 1 .

Use: Required if TM card is used. Consider FQ card.

## /warning\_sign Caution

One shake is equal to 10 -8 seconds, which is equal to 10 nanoseconds.

## Details:

- 1 A T0 card can be used to set up a default time-bin structure for all tallies. A specific T n card will override the default structure for tally n .
- 2 For the first form of the tally-time card, the times on the T card must be entered in the order of increasing magnitude. If a particle has a time greater than the last entry, it is not be tallied and a warning is issued. A comment is printed if the last time bin is greater than the time cutoff specified on the CUT card. For point detector tallies, time bins can exceed the time cutoff so that particles will score at detectors remote from the main body of the system. Setting the time cutoff lower than the last time bin will inhibit unproductive transport of slow neutrons in the system and will increase the efficiency of the problem.
- 3 The the second form of the tally-time card, keyword entries allow for automatic creation of cyclic time bins. The standard time entries and keyword entries are mutually exclusive within a given T card. If CEND is specified, all cyclic time bins are generated for the first cycle and these are repeated out to the CEND time. Keyword entries can be in any order.

1

## 5.9.4.1 Example 1

```
1 T2 -1 1 1.0+37 NT
```

This will separate an F2 flux surface tally into three time bins:

1. from -∞ to -1.0 shake,
2. from -1.0 shake to 1.0 shake, and
3. from 1.0 shake to 10 37 shakes, which is effectively infinity.

No total bin will be printed in this example.

## 5.9.4.2 Example 2

```
T1 CBEG=0.0 CFRQ=1000e-8 COFI=0.000005e8 CONI=0.0005e8 CSUB=5
```

This example specifies a reference starting time of 0 sh with a
frequency of 1000 Hz ( 10 -5 sh -1 ). The dead time of 5 µ s ( COFI )
results in a time bin from 0-500 sh that includes missed tally scores
during the dead time. The alive time of 0.5 ms ( CONI ), with the
specified five subdivisions ( CSUB ), results in five time bins equally
spaced from 500-50500 sh. A final time bin from 50500-100000 sh will be
provided for tally scores made after the alive time. Note that using the
' e8 ' and ' e-8 ' form shown here makes it easy to express the entries
in seconds and Hertz rather than using the native unit of shakes.

## 5.9.5 C: Tally Cosine Bins (Tally Type 1 and 2)

This card is used to assign cosine-bin boundaries for surface tallies to
accumulate results into. If it is not present, the results are
accumulated into a single 'total' bin regardless of the direction that
the particle has relative to the tally surface when it crosses the
surface.

<!-- image -->

| Data-card Form: C n c1 . . . cK [ T ] [ C ] or Data-card Form: * C n ϕ 1 . . . ϕ K [ T ] [ C ]   | Data-card Form: C n c1 . . . cK [ T ] [ C ] or Data-card Form: * C n ϕ 1 . . . ϕ K [ T ] [ C ]                                                                                      |
|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                                                                                | Tally number. Restriction: n ≤ 99999999                                                                                                                                             |
| ck                                                                                               | Upper cosine limit of the k th angular bin for surface current or flux tally n (See Notes 3 and 4.). Restrictions: c1 > - 1 and cK = 1 , where cK is the entry for the last bin     |
| ϕ k                                                                                              | Upper angular limit of the k th angular bin for surface current or flux tally n (See Notes 3 and 4.). Restrictions: ϕ 1 < 180 and ϕ K = 0 , where ϕ K is the entry for the last bin |
| T                                                                                                | Optional notation at the end of the input line to provide the total over all specified angular bins.                                                                                |

1

1

- C Optional notation at the end of the input line to cause the bin values to be cumulative and the last angular bin to be the total over all angles.

Default: If the C card is absent, there will be one bin over all angles
unless this default has been changed by a C0 card.

Use: For use with tally types 1 and 2 only. Required if CM card is used.
Consider FQ card.

## Details:

- 1 A C 0 card can be used to set up a default angular bin structure for all tallies. A specific C n card will override the default structure for tally n . The selection of a single cosine bin for an F1 tally gives the total and not the net current crossing a surface.
- 2 The asterisk ( * ) on the C n card causes the entries to be interpreted as degrees.
- 3 Whether entered as degrees or cosines, the entries on the C card must be such that the cosine is monotonically increasing, beginning with the cosine of the largest angle less than 180 ◦ to the normal and ending with the normal (i.e., cos θ = 1 ). A lower cosine bound of -1 is set in the code and should not be entered on the card.
- 4 The angular limits described by the C card are defined with respect to the positive normal to the surface at the particle point of entry. An FT card with an FRV v1 v2 v3 option can be used to make the cosine bins relative to the vector ( u, v, w ) = ( v1 , v2 , v3 ) . The positive normal to the surface is always in the direction of a cell that has positive sense with respect to that surface.
- 5 Due to the grazing angle approximation made for F2 tallies, some cosine bins may be inaccurate and the code prints a warning when a C n is used with an F2 tally. Details on this approximation can be found in §2.5.2.2.

## 5.9.5.1 Example 1

C1 -0.866 -0.5 0 0.5 0.866 1

* C1 150 120 90 60 30 0

Either card will tally currents within the following angular limits

1. 180 ◦ to 150 ◦ ,
2. 150 ◦ to 120 ◦ ,
3. 120 ◦ to 90 ◦ ,
4. 90 ◦ to 60 ◦ ,
5. 60 ◦ to 30 ◦ , and
6. 30 ◦ to 0 ◦ with respect to the positive normal.

No total will be provided.

## 5.9.5.2 Example 2

As an example of the relationship between a surface normal and sense for
the C1 card, consider a source at the origin of a coordinate system and
a plane ( PY ) intersecting the + y axis. An entry of 0 and 1 on the C1
card will tally all source particles transmitted through the plane in
the 0 to 1 cosine bin ( 0 ◦ to 90 ◦ ) and all particles scattered back
across the plane in the -1 to 0 cosine bin ( 90 ◦ to 180 ◦ ). A plane (
PY ) intersecting the -y axis will result in a tally of all source
particles transmitted through the second plane in the -1 to 0 bin ( 90 ◦
to 180 ◦ ) and all particles scattered back across the plane in the 0 to
1 bin ( 0 ◦ to 90 ◦ ). Note that the positive normal direction for both
planes is the same, the + y axis.

## 5.9.6 FQ: Print Hierarchy

This card can be used to change the order in which the output is printed
for the tallies. For a given tally, the default order is changed by
entering a different ordering of the letters, space delimited.

| Data-card Form: FQ n a1 . . . a8   | Data-card Form: FQ n a1 . . . a8                                              |
|------------------------------------|-------------------------------------------------------------------------------|
| n                                  | Tally number. Restriction: n ≤ 99999999                                       |
| ak                                 | Letters representing all eight possible types of tally bins: 1 ≤ k ≤ 8 ( 2 ). |
|                                    | F cell, surface, or detector bins                                             |
|                                    | D direct or flagged bins                                                      |
|                                    | U user bins                                                                   |
|                                    | S segment bins                                                                |
|                                    | M multiplier bins                                                             |
|                                    | C cosine bins                                                                 |
|                                    | E energy bins                                                                 |
|                                    | T time bins                                                                   |

Default: Order as given above. The tally will be printed in the output
file in blocks of time (rows) and energy (columns). Any other bins in a
tally will be listed vertically down the output page.

Use: Highly recommended. Prints tallies in more easily readable blocks
in the output file without affecting answers.

## Details:

- 1 An FQ0 card can be used to change the default order for all tallies. A specific FQ card will then override that order for tally n .
- 2 A subset of the letters can be used, in which case MCNP6 places them at the end of the FQ card and precedes them with the unspecified letters in the default order. The first letter is for the outermost loop of the nest in the tally printout coding. The last two sets of bins make a table-the next to last set goes vertically, and the last set of bins goes horizontally in the table. Default order is a table in E and T ; any other bins in a tally will be listed vertically down the output page.

## 5.9.6.1 Example 1

```
1 FQ4 E S M
```

The output file printout will be tables with multiplier bins across the
top, segments listed vertically, and these segment-multiplier blocks
printed for each energy.

## 5.9.7 FM: Tally Multiplier

The FM card basically multiplies any tallied quantity (flux, current) by
any cross section to give nearly all reaction rates plus heating,
criticality, etc. That is, the FM card is used to calculation any
quantity of the form

<!-- formula-not-decoded -->

where ϕ ( E ) is the energy-dependent fluence (particles/cm 2 ) and R m
( E ) is an operator of additive and/or multiplicative response
functions from the MCNP6 cross-section libraries or specially designated
quantities. Note that some MCNP6 cross-section-library reaction numbers
( R ) are different from ENDF/B (MT) reaction numbers. The constant C is
any arbitrary scalar quantity that can be used for normalization. The
material number m must appear on an M m card, but need not be used in a
geometric cell of the problem.

<!-- image -->

k = -3 the tally will be multiplied by the microscopic cross section of
the first interaction. This option can be used with the LCA NOACT = -2
option to convert multiplicities into secondary production cross
sections with units of barns ( 3 ). ( reaction list i ) Sums and
products of ENDF or special reaction numbers ( 4 ). T Optional notation
at the end of the input line to provide the total over all specified
bins. If absent, a total over all bins is not provided. C Optional
notation at the end of the input line to cause the bin values to be
cumulative and the last bin to be the total over all bins.

Use: Optional. Use the attenuators only when they are thin. When used
with tally types 6 and 7, only the multiplicative constant can be
specified. Disallowed for tally type 8. When used with mesh tallies,
only one multiplier set and reaction list per mesh tally is permitted.
If m = 0 for a multiplier set, the reaction cross sections for the
material in which the particle is traveling are used (for FMESH tallies
only).

## Details:

- 1 An attenuator set of the form c -1 m px includes one layer and allows the tally to be modified by the factor exp( -σ t p x ) representing an exponential line-of-sight attenuator. This capability makes it possible to have attenuators without actually modeling them in the problem geometry.

## /warning\_sign Caution

The assumption is made that the attenuator is thin, so that simple
exponential attenuation without buildup from scattering is valid.

The attenuator set can include more than one layer, in which case the
factor is exp( -σ 1 p 1 -σ 2 p 2 ) . The attenuator set can also be part
of a bin set, for example,

```
(( c1 m1 R1 ) ( c2 m2 R2 ) ( c3 -1 m3 px3 ))
```

in which case the attenuation factor is applied to every bin created by
the multiplier sets. Note that both the inner and the outer parentheses
are required for this application.

- 2 If the c entry is negative (for type 4 tally only), c is replaced by | c | times the atom density of the cell where the tally is made.
- 3 The special multiplier option with k = -3 works for all incident particle types except electrons; however, for charged particles, caution should be exercised because for some charged particles maximum cross sections are used instead of actual cross sections.
- 4 A reaction list consists of one or more reaction numbers delimited by spaces, colons, and/or pound symbols ( # ). A space between reaction numbers means multiply the reactions. A colon means to add the reactions and a pound symbol means to subtract the reactions. The hierarchy of operation is multiply first and then add or subtract. One bin is created for each reaction list. No parentheses are allowed within the reaction list.

The reaction cross sections are microscopic (with units of barns) and
not macroscopic. Therefore, if the constant c is the atomic density (in
atoms/barn-cm), the results will include the normalization 'per cm 3 .'

Any number of ENDF/B (MT) or special ( R ) reactions can be used in a
multiplier set as long as they are present in the MCNP6 cross-section
libraries, or in special libraries of dosimetry data. If neither a
material number nor any reactions are given, the tally simply is
multiplied by the constant c .

## 5.9.7.1 Use of Parentheses

1. If a given multiplier set contains only one reaction list, the parentheses surrounding the reaction list can be omitted. Parentheses within a reaction list are forbidden.
2. If a given bin set consists of more than a single multiplier or attenuator set, each multiplier or attenuator set must be surrounded by parentheses, and the combination must also be surrounded by parentheses.
3. If the FM card consists only of a single bin set, and that bin set consists only of a single multiplier or attenuator bin, surrounding parentheses can be omitted.

## 5.9.7.2 Special Reaction Numbers

In addition to the standard ENDF reaction numbers (e.g., MT=1, 2, and
16, representing σ t , σ el , and σ n,2n , respectively from the ENDF-6
manual(s) [45, 309, 310]), Table 5.19 lists the non-standard special R
numbers that may be used.

Table 5.19: ENDF/B Special Reaction Numbers, R

<!-- image -->

| Reaction Type               | R   | Microscopic Cross-Section Description          |
|-----------------------------|-----|------------------------------------------------|
| Neutron                     | - 1 | Total cross section without thermal            |
| Neutron                     | - 2 | Absorption cross section                       |
| Neutron                     | - 3 | Elastic cross section without thermal          |
| Neutron                     | - 4 | Average neutron heating number (MeV/collision) |
| Neutron                     | - 5 | Gamma-ray production cross section , barns     |
| Neutron                     | - 6 | Total fission cross section                    |
| Neutron                     | - 7 | Fission ν , prompt or total                    |
| Neutron                     | - 8 | Fission Q (MeV/fission)                        |
| Neutron                     | - 9 | Fission ν , delayed                            |
| Many Nuclides               | - 4 | Average heating numbers (MeV/collision)        |
| Many Nuclides               | - 5 | Gamma-ray production cross section, barns      |
| Many Nuclides               | - 7 | Fission ν (prompt or total)                    |
| Many Nuclides               | - 8 | Fission Q (MeV/fission)                        |
| Photoatomic                 | - 1 | Incoherent scattering cross section            |
| Photoatomic                 | - 2 | Coherent scattering cross section              |
| Photoatomic                 | - 3 | Photoelectric cross section, with fluorescence |
| Photoatomic                 | - 4 | Pair production cross section                  |
| Photoatomic                 | - 5 | Total cross section                            |
| Photoatomic                 | - 6 | Average photon heating number                  |
| Proton ( 1 )                | ± 1 | Total cross section                            |
| Proton ( 1 )                | ± 2 | Non-elastic cross section                      |
| Proton ( 1 )                | ± 3 | Elastic cross section                          |
| Proton ( 1 )                | ± 4 | Average proton heating number                  |
| Photonuclear ( 2 )          | 1   | Total cross section                            |
| Photonuclear ( 2 )          | 2   | Non-elastic cross section                      |
| Photonuclear ( 2 )          | 3   | Elastic cross section                          |
| Photonuclear ( 2 )          | 4   | Average photonuclear heating number            |
| Multigroup Neutron & Photon | - 1 | Total cross section                            |
| Multigroup Neutron & Photon | - 2 | Fission cross section                          |
| Multigroup Neutron & Photon | - 3 | Fission ν data                                 |
| Multigroup Neutron & Photon | - 4 | Fission χ data                                 |
| Multigroup Neutron & Photon | 5   | Absorption cross section                       |

continued on next page. . .

-

## Details:

- 1 On the LA150H proton library, the only available reaction (beyond ± 1 , 2 , 3 , 4 ) is MT=5 and its multiplicities, 1005, 9005, 31005, etc. The multiplicity reaction numbers are specified by adding 1000 times the secondary particle number to the reaction number. For interaction reaction MT=5, the multiplicities are 1005 for neutrons, 9005 for protons, 31005 for deuterons, etc. The proton multiplicity, MT=9001, 9004, 9005, etc., is generally available, along with the total cross section and heating number, MT=1, MT=4.
- 2 The principal photonuclear cross sections are the following: 1=total, 2=non-elastic, 3=elastic, 4=heating, and &gt; 4 =various reactions such as 18=( γ ,f). The photonuclear yields (multiplicities) for various secondary particles are specified by adding 1000 times the secondary particle number to the reaction number. For example, 31001 is the total yield of deuterons (particle type D=31), 34001 is the total yield of alphas (particle type a=34), and 1018 is the total number of neutrons (particle type n = 1 ) from fission.

The total and elastic cross sections, MT=1 and MT=2, are adjusted for
temperature dependence. All other reactions are interpolated directly
from the library data tables. Note that for tritium production, the R
number differs from one nuclide to another. Note also that tally types 6
and 7 already include reactions, so the FM n card makes little sense for
n = 6 or 7. Generally only the constant-multiplier feature should be
used for these tally types.

Photon production reactions are characterized by multiple MT numbers
because more than one photon can be produced by a particular neutron
reaction that is itself specified by a single MT number. Each of these
photons is produced with an individual energy-dependent cross section.
For example, MT 102 (radiative capture) might produce 40 photons, each
with its own cross section, angular distribution, and energy
distribution. Accordingly, 40 MT numbers are needed to represent the
data; the MT numbers are 102001, 102002, . . . , 102040.

Photonuclear and proton cross sections may be used in tally multipliers
on the FM card, however the applicability of the tally is limited to the
upper energy included in the related cross-section library.

glyph[negationslash]

In perturbed problems, the PERT card keyword RXN can affect the cross
sections used with the FM card tally multipliers. If a tally in a cell
is dependent on a cross section that is perturbed, then R ij ′ = 0 and a
correction is made to the R 1 j ′ = 0 case. For this required R 1 j ′
correction to be made, the user must ensure

Table 5.19, continued

| Reaction Type   | R   | Microscopic Cross-Section Description   |
|-----------------|-----|-----------------------------------------|
|                 | - 6 | Stopping powers                         |
|                 | - 7 | Momentum transfers                      |
| Electrons       | 1   | de/dx electron collision stopping power |
|                 | 2   | de/dx electron radiative stopping power |
|                 | 3   | de/dx total electron stopping power     |
|                 | 4   | Electron range                          |
|                 | 5   | Electron radiation yield                |
|                 | 6   | Relativistic β 2                        |
|                 | 7   | Stopping power density correction       |
|                 | 8   | Ratio of rad/col stopping powers        |
|                 | 9   | Drange                                  |
|                 | 10  | dyield                                  |
|                 | 11  | MG array values                         |
|                 | 12  | QAV array values                        |
|                 | 13  | EAR array values                        |

1

1

1

1

2

that the R reactions on the FM card are the same as the RXN reactions on
the PERT card and that the FM card multiplicative constant c is
negative, indicating multiplication by the atom density to get
macroscopic cross sections. For example, if R = -6 for fission on the FM
card, you should not use RXN = 18 for fission on the PERT card. If c &gt; 0
, the cross sections are not macroscopic; it is assumed that there is no
tally dependence on a perturbed cross section, R 1 j ′ = 0 , and no
correction is made. The same correction is automatically made for the F6
tally and the KCODE k eff calculation, and for an F7 tally if the
perturbation reaction is fission because these three tallies all have
implicit associated FM cards.

It is always wise to plot the desired cross sections first to see if
they are available with the expected reaction numbers in the data
library. The tally multipliers treat the data the same as the data are
treated in transport: the cross section at the lowest energy is extended
down to E = 0 for protons with reaction identifier MT &lt; 0 ; the cross
section at the highest energy of the table is extended to E = ∞ for
proton interaction cross sections with MT &lt; 0 ; and for photonuclear
interaction cross sections, MT &lt; 1000 . These extrapolations can be seen
in the cross-section plots. Examples below include total energy
deposition (Example 3), track length criticality estimate (Example 4),
total energy deposited for materials not present in geometry (Example
5), and lifetime calculation/reaction rates (Example 6).

## 5.9.7.3 Example 1

Case 1:

FMn c m r1 r2 : r3

Case 2:

```
FMn c m r1 r2 : r1 r3
```

Case 3:

FMn c m r1 (r2 : r3)

These cases reiterate that parentheses cannot be used for algebraic
hierarchy within a reaction list. The first case represents one reaction
list (i.e., one bin) calling for reaction r3 to be added to the product
of reactions r1 and r2 . The second case produces a single bin with the
product of reaction r1 with the sum of reactions r2 and r3 . The third
case creates two bins, the first of which is reaction r1 alone; the
second is the sum of r2 and r3 , without reference to r1 .

## 5.9.7.4 Example 2

Case 1:

```
F2:N 1 2 3 4 FM2 (c1) (c2) (c3) (c4) T
```

Case 2:

1

2

```
F12:N 1 2 3 4 FM12 c1
```

Case 3:

```
1 F22:N (1 2 3) 4 T 2 FM22 (c1) (c2) (c3) (c4)
```

These three cases illustrate the syntax when only the constant-
multiplier feature is used. All parentheses are required in these
examples. Tally F2 creates 20 bins: the flux across each of surfaces 1,
2, 3, and 4 with each multiplied by each constant c1 , c2 , c3 , c4 ,
and the sum of the four constants. Tally F12 creates 4 bins: the flux
across each of surfaces 1, 2, 3, and 4 with each multiplied by the
constant c1 . Tally F22 creates 12 bins: the flux across surface 1 plus
surface 2 plus surface 3, the flux across surface 4, and the flux across
all four surfaces with each multiplied by each constant c1 , c2 , c3 ,
and c4 . An FQ card with an entry of F M or M F would print these bins
of the tallies in an easy-to-read table rather than vertically down the
output file.

## 5.9.7.5 Example 3 (Total Energy Deposition)

| F4:P   | 1          |
|--------|------------|
| FM4    | -1 2 -5 -6 |
| SD4    | 1          |
| F6:P   | 1          |
| SD6    | 1          |

Multiplying the photon flux by volume ( SD4 1) times the atom density (
-1 ) for material 2 times the photon total cross section ( -5 ) times
the photon heating number ( -6 ) is the same as the F6 : p photon
heating tally multiplied by mass ( SD6 1), namely the total energy
deposition in cell 1. Note that positive photon reaction numbers are
photonuclear reactions. Note also that the SD card replaces the normal
divisor (volume for F4 and mass for F6 ) with new values (both 1 in this
example). By overriding the MCNP6-computed cell volume and mass with
values of 1, you effectively multiply the unmodified F4 and F6 tallies
by the volume and mass, respectively, yielding the score for the entire
cell.

## 5.9.7.6 Example 4 (Track Length Criticality Estimate)

```
1 F4:n 1 2 FM4 -1 3 -6 -7 3 SD4 1
```

Multiplying the neutron flux by volume ( SD4 1) times the atom density (
-1 ) for material 3 times the fission multiplicity, ν ( -7 ), times the
fission cross section ( -6 ) gives the track-length estimate of
criticality for cell 1.

1

2

3

4

5

6

7

## 5.9.7.7 Example 5 (Total Energy Deposited for Materials Not Present in Geometry)

Using MCNP6 tallies, there are two ways to obtain the energy deposited
in a material in terms of rads ( 1 rad = 100 ergs/g). When the actual
material of interest is present in the MCNP6 model, the simplest way is
to use the heating tally with units MeV/g in conjunction with c = 1 .
602 × 10 -8 on the companion FM card, where c = (1 . 602 × 10 -6
ergs/MeV ) / (100 ergs/g ) . When the material is not present in the
model, rads can be obtained from type 1, 2, 4, and 5 tallies by using an
FM card where c is equal to the factor above times N 0 η × 10 -24 /A ,
where N 0 is Avogadro's number, η is the number of atoms per molecule,
and A is the atomic weight of the material of interest. This value of c
equals ρ a /ρ g as discussed in §2.5.4.1. The implicit assumption when
the material is not present is that it does not affect the radiation
transport significantly. In the reaction list on the FM card, you must
enter -4 1 for neutron heating and -5 -6 for photon heating. For both F4
and F6 , if a heating number from the data library is negative, it is
set to zero by the code.

## 5.9.7.8 Example 6 (Lifetime Calculation/Reaction Rates)

```
F4:N 1 SD4 1 FM4 (-1 1 16:17) $ bin 1 = (n,xn) reaction rate (-1 1 -2) $ bin 2 = capture (n,0n) reaction rate (-1 1 -6) $ bin 3 = fission reaction rate (1 -2) $ bin 4 = prompt removal lifetime=flux/velocity M1 92235 -94.73 92238 -5.27
```

This F4 neutron flux tally from a Godiva criticality problem is
multiplied by four FM bins and will generate four separate tally
quantities. The user can divide bin 4 by bins 1, 2, and 3 to obtain the
(n,xn) lifetime, the (n,0n) lifetime, and the (n,f) lifetime,
respectively. The FM4 card entries are:

```
c = -1 multiply by atomic density of material 1 m = 1 material number on material card r1 = 16:17 reaction number for (n,2n) cross section plus reaction number for (n,3n) cross section r2 = -2 reaction number for capture cross section r3 = -6 reaction number for total fission cross section r4 = 1 -2 prompt removal lifetime = flux/velocity = time integral of population
```

## 5.9.8 DE and DF: Dose Energy and Dose Function

## /warning\_sign Caution

Due to copyright concerns the built-in flux-to-dose conversion factors
have been removed. They are available in Appendix F.1 formatted as MCNP
input for DE / DF cards.

This feature allows you to enter a point wise response function (such as
flux-to-dose conversion factors) as a function of energy to modify a
regular tally, or apply a built-in conversion/response function.

```
Data-card Form either: DE n a e1 . . . eK and DF n b f1 . . . fK or DF n IU = value FAC = value IC = value n Tally number ( 3 ). Restriction: n ≤ 99999999 ek The k th energy value (in MeV) ( 1 ). fk The value of the dose function corresponding to ek ( 1 , 2 ). a Interpolation method for energy table ( 4 , 5 ). If a = LOG logarithmic interpolation. (DEFAULT) a = LIN linear interpolation. b Interpolation method for dose function table ( 5 ). If b = LOG logarithmic interpolation. (DEFAULT) b = LIN linear interpolation. IC = value Apply a response function. If IC = 99 ICRP-60 equivalent dose function (neutrons) or dose equivalent (charged particles) for energy deposition tallies ( 6 , 7 ). IC = name detector response function listed in Table 5.21. (DEFAULT: None)
```

The following keywords can only be used with IC = 99 .

```
IU = value Controls units. If IU = 1 US units (rem/h/source particle). IU = 2 International units (Sv/h/source particle). (DEFAULT) FAC = value Normalization factor for dose. If FAC = -3 Use ICRP-60 dose conversion factors for energy deposition tallies. (DEFAULT) ( 6 , 7 ). FAC > 0 User-supplied normalization factor ( 7 ).
```

Default:

If a or b is missing, LOG interpolation is used.

Use: Optional. Tally comment card recommended.

## Details:

- 1 When both the DE and DF cards provide a user-specified dose table, they must have the same number of numerical entries. The DE card entries must increase monotonically. Particle energies outside the energy

1

2

3

4

1

2

3

range defined on these cards use either the highest or the lowest value,
as appropriate.

- 2 In addition to allowing user-supplied response functions, the dose conversion capability provides several built-in response functions. These are invoked by omitting the DE card and using keywords on the DF card.
- 3 If n is zero on the DE and DF cards, the function will be applied to all tallies that do not have DE and DF cards specifically associated with them.
- 4 By default MCNP6 uses logarithmic-logarithmic interpolation between the points rather than a histogram function as is done for the EM card. The energy points specified on the DE card do not have to equal the tally energy bins specified with the E card for the F tally.
- 5 LIN or LOG can be chosen independently for either table. Thus any combination of interpolation (logarithmiclogarithmic, linear-linear, linear-logarithmic, or logarithmic-linear) is possible. The default logarithmiclogarithmic interpolation is generally appropriate for the ANSI/ANS flux-to-dose rate conversion factors; kermas for air, water, and tissue; and energy absorption coefficients.
- 6 The IC = 99 and FAC = -3 keyword options apply dose conversion factors recommended in ICRP-60 [311] to energy deposition tallies. For neutrons, radiation weighting factors, w R , are used to convert absorbed dose to ambient dose equivalent. Theses factors are calculated as

<!-- formula-not-decoded -->

Charged particle energy deposition tallies use quality factors, Q , to
calculate dose equivalent. The stopping power, S ( E,p ) of the charged
particles are used to calculate the quality factors based on the
following formula:.

where the stopping power is in keV/ µ m.

<!-- formula-not-decoded -->

- 7 If FAC &gt; 0 and IC = 99 , the tally results will be in absorbed dose (rad or Sv, depending the value of IU ) /h/source particle, provided that the source strength is weighted by source particles/sec.

## 5.9.8.1 Example 1

```
fc5 Point detector tally modified by an arbitrary user-supplied response function f5:p 0. 0. 5. 1. de5 0.01 0.1 0.2 0.5 1.0 df5 lin 0.062 0.533 1.03 2.54 4.6
```

Listing 5.53: example\_de-df.cards.inp.txt

In this example, a point detector tally is modified by a user-supplied
dose function using logarithmic interpolation on the energy table and
linear interpolation on the dose function table.

## 5.9.8.2 Example 2

```
fc6 Helium-4 (alpha) dose equivalent (Sv) f6:a 77 df6 IC=99 IU=2 FAC=-3
```

Listing 5.54: example\_de-df.cards.inp.txt

In this example, the ICRP-60 dose function is used to calculate the
alpha particle dose equivalent in cell 77 in units of Sv/h/source
particle. Note that the source strength must be weighted by source
particles/sec.

1

2

3

## 5.9.8.3 Example 3

```
fc26 Helium-3 detector response for tritium. f26:t 6 df26 IC=he3-1
```

Listing 5.55: example\_de-df.cards.inp.txt

This example applies the He-3 detector response function to a tritium
energy deposition tally.

## 5.9.9 EM: Energy Multiplier

The EM n card can be used with any tally (specified by n ) to scale the
usual current, flux, etc. by a response function. There should be one
entry for each energy entry on the corresponding E n card. When a tally
is being recorded within a certain energy bin, the regular contribution
is multiplied by the entry on the EM n card corresponding to that bin.
For example, a dose rate can be tallied with the appropriate response
function entries. Tallies can also be changed to be per unit energy if
the entries are 1 / ∆ E for each bin, where ∆ E is the width of the
corresponding energy bin. Note that this card modifies the tally by an
energy-dependent function that has the form of a histogram and not a
continuous function. It also requires the tally to have as many energy
bins as there are histograms on the EM n card. If neither of these two
effects is desired, see the DE and DF cards.

```
Data-card Form: EM n m1 . . . mK n Tally number. Restriction: n ≤ 99999999 mk Multiplier to be applied to the k th energy bin.
```

Default: None.

Use: Requires E card. Tally comment recommended.

## Details:

- 1 A set of energy multipliers can be specified on an EM0 card that will be used for all tallies for which there is not a specific EM card.

## 5.9.10 TM: Time Multiplier

The TM card can be used with any tally to scale the usual current, flux,
etc. by a response function. There should be one entry for each time
entry on the corresponding T card. Note that this card modifies the
tally by a time-dependent function that has the form of a histogram and
not a continuous function. For example, tallies can be changed to be per
unit time if the entries are 1 / ∆ T for each bin, where ∆ T is the
width or the corresponding time bin.

```
Data-card Form: TM n m1 . . . mK n Tally number. Restriction: n ≤ 99999999 mk Multiplier to be applied to the k th time bin.
```

Default: None.

Use: Requires T card. Tally comment recommended.

## Details:

- 1 A set of time multipliers can be specified on a TM0 card that will be used for all tallies for which there is not a specific TM card.

## 5.9.11 CM: Cosine Multiplier (tally types 1 and 2 only)

The CM card can be used with an F1 or F2 tally to scale the usual
current by a response function. There should be one entry for each
cosine entry on the corresponding C card. Note that this card modifies
the tally by an angular-dependent function that has the form of a
histogram and not a continuous function. For example, To get the
directionally dependent F1 tally results to be per steradian, the k th
entry on the CM1 card is 1 / [2 π (cos θ i -cos θ i -1 )] where θ 0 is
180 ◦ .

```
Data-card Form: CM n m1 . . . mK n Tally number. Restriction: n ≤ 99999999 mk Multiplier to be applied to the k th cosine bin.
```

Default: None.

Use: Tally types 1 and 2. Requires C n card. Tally comment recommended.

## Details:

- 1 A set of cosine multipliers can be specified on a CM 0 card that will be used for all F1 or F2 tallies for which there is not a specific CM card.

## 5.9.12 CF: Cell Flagging (Tally Types 1, 2, 4, 6, 7)

Particle tracks can be 'flagged' when they leave designated cells and
the contributions of these flagged tracks to a tally are listed
separately in addition to the normal total tally. This method can
determine the tally contribution from tracks that have passed through an
area of interest.

The cell flag is turned on only upon leaving a cell. A source particle
born in a flagged cell does not turn the flag on until it leaves the
cell.

1

2

The flagged tallies are the contribution to the tally made by a particle
or its progeny that ever had its cell flag set by leaving the flagged
cell or cells designated on the CF card. For example, a flagged photon
tally can be scored in by either a photon leaving the flagged cell or a
neutron leaving a flagged cell, which leads to a photon that is tallied.

## /warning\_sign Caution

A particle that is killed on a surface will have its surface flag set
but not have its cell flag.

Both a CF and an SF card can be used for the same tally. The tally is
flagged if the track leaves one or more of the specified cells or
crosses one or more of the surfaces. Only one flagged output for a tally
is produced from the combined CF and SF card use.

| Data-card Form: CF n c1 . . . cK   | Data-card Form: CF n c1 . . . cK                                                                                                                                                                |
|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                  | Tally number. Restriction: n ≤ 99999999                                                                                                                                                         |
| ck                                 | Problem cell numbers whose tally contributions are to be flagged. A negative cell number requires that a collision occurs in that cell in order for the flag to be set upon exit from the cell. |

Default: None.

Use: Not with detector ( F5 ) tallies, DXTRAN ( DXT ) spheres, or pulse-
height ( F8 ) tallies; instead consider the FT card with the ICD
keyword. Consider FQ card.

## 5.9.12.1 Example 1

| F4:N   | 6 10   |
|--------|--------|
| CF4    | 3 4    |

In this example the flag is turned on when a neutron leaves cell 3 or 4.
The print of Tally 4 is doubled. The first print is the total track
length flux tally in cells 6, 10, and 13. The second print is the tally
in these cells for only those neutrons that have left cell 3 or 4 at
some time before making their contribution to the cell 6, 10, or 13
tally.

## 5.9.13 SF: Surface Flagging (Tally Types 1, 2, 4, 6, 7)

Particle tracks can be 'flagged' when they cross designated surfaces and
the contributions of these flagged tracks to a tally are listed
separately in addition to the normal total tally. This method can
determine the tally contribution from tracks that have crossed a surface
of interest.

The flagged tallies are the contribution to the tally made by a particle
or its progeny that ever had its surface flag set by crossing the
flagged surface or surfaces designated on the SF card. For example, a
flagged photon tally can be scored in by either a photon crossing the
flagged surface or a neutron crossing the flagged surface, which leads
to a photon that is tallied.

Both a CF and an SF card can be used for the same tally. The tally is
flagged if the track leaves one or more of the specified cells or
crosses one or more of the surfaces. Only one flagged output for a tally
is produced from the combined CF and SF card use.

```
Data-card Form: SF n s1 . . . sK n Tally number. Restriction: n ≤ 99999999 sk Problem surface numbers whose tally contributions are to be flagged.
```

Default: None.

Use: Not with detector ( F5 ) tallies or DXTRAN ( DXT ) spheres; instead
consider the FT card with the ICD keyword. Not with pulse-height ( F8 )
tallies. Consider FQ card.

## 5.9.13.1 Example 1

```
1 F4:N 6 10 2 SF4 30
```

In this example, the flag is turned on when a neutron leaves surface 30.
The print of Tally 4 is doubled. The first print is the total track
length flux tally in cells 6 and 10. The second print is the tally in
these cells for only those neutrons that have crossed surface 30 at some
time before making their contribution to cells 6 or 10.

## 5.9.14 FS: Tally Segment (Tally Types 1, 2, 4, 6, 7)

This card allows you to subdivide a cell or a surface of the problem
geometry into segments for tallying purposes without having to specify
extra cells just for tallying. The segmenting surfaces specified on the
FS card are listed with the regular problem surfaces, but they need not
be part of the actual geometry and hence do not complicate the
cell/surface relationships. The cell or surface to be segmented,
however, must be part of the problem geometry.

<!-- image -->

Default: No segmenting.

Use: Not with detector ( F5 ) tallies or DXTRAN ( DXT ) spheres. Not
with pulse-height ( F8 ) tallies. May require SD card. Consider FQ card.

## Details:

- 1 If K surfaces are entered on the FS n card, K +1 surface or volume segments (and tally bins) are created. If the symbol T is on the FS n card, there will be an additional total bin. Tally n is subdivided into K +1 segment bins according to the order and sense of the segmenting surfaces listed on the FS n card as follows:

| Bin #1   | The portion of tally n with the same sense with respect to surface s1 as the sign given to s1 ;                                                                   |
|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Bin #2   | The portion of tally n with the same sense with respect to surface s2 as the sign given to s2 , but excluding that already scored in a previously listed segment. |
| Bin K    | The portion of tally n with the same sense with respect to surface sK as the sign given to sK , but excluding that already scored in a previously listed segment. |
| Bin K +1 | The remaining portion of tally n not yet tallied, i.e., everything else.                                                                                          |
| Bin K +2 | The total tally for the entire surface or cell if T is present on the FS n card.                                                                                  |

If the symbol T is absent from the FS n card, MCNP6 calculates the tally
only for each segment (including the K +1 'everything else' segment). If
multiple entries are on the F n card, each cell or surface in the tally
is segmented according to the above rules. For tally types 1 or 2, the
segmenting surfaces divide a problem surface into segments for the
current or flux tallies. For tally types 4, 6, or 7, the segmenting
surfaces divide a problem cell into segments. For normalized tallies,
the segment areas (for type 2), volumes (for type 4), or masses (for
types 6 and 7) may have to be provided. See the discussion under the SD
n card.

## 5.9.14.1 Example 1

```
F2:N 1
```

```
1 2 FS2 -3 -4
```

This example subdivides surface 1 into three sections and calculates the
neutron flux across each of them. There are three prints for the F2
tally:

1. the flux across that part of surface 1 that has negative sense with respect to surface 3;
2. the flux across that part of surface 1 that has negative sense with respect to surface 4, but that has not already been scored (and so must have positive sense with respect to surface 3); and
3. everything else (that is, the flux across surface 1 with positive sense with respect to both surfaces 3 and 4).

It is possible to get a zero score in some tally segments if the
segmenting surfaces and their senses are not properly specified. In this
example, if all tallies that are positive with respect to surface 3 are
also all positive with respect to surface 4, the third segment bin will
have no scores.

## 5.9.14.2 Example 2

```
F2:N 1
```

```
1 2 FS2 -3 4
```

The order and sense of the surfaces on the FS 2 card are important. This
example produces the same numbers as does the example in §5.9.14.1 but
changes the order of the printed flux. Bins two and three are
interchanged.

## 5.9.14.3 Example 3

| F1:N   | 1 2 T   |
|--------|---------|
| FS1    | -3 T    |

This example produces three current tallies:

1. across surface 1,
2. across surface 2, and
3. the sum across surfaces 1 and 2.

Each tally will be subdivided into three parts:

1. that with a negative sense with respect to surface 3,
2. that with a positive sense with respect to surface 3, and
3. a total independent of surface 3.

## 5.9.15 SD: Segment Divisor (Tally Types 1, 2, 4, 6, 7)

For segmented cell volumes or surface areas defined by the FS card that
are not automatically calculated by MCNP6, the user can provide volumes
(tally type 4), areas (tally type 2), or masses (tally types 6 and 7) on
this segment divisor card to be used by tally n . Tally type 1 (the
current tally) is not normally divided by anything, but with the SD 1
card the user can introduce any desired divisor, for example, area to
tally surface current density. This card is similar to the VOL and AREA
cards but is used for specific tallies, whereas VOL and AREA used for
the entire problem geometry.

| Data-card Form: SD n ( d11 d12 . . . d1M ) ( d21 d22 . . . d2M ) . . . ( dK1 dK2 . . . dKM )   | Data-card Form: SD n ( d11 d12 . . . d1M ) ( d21 d22 . . . d2M ) . . . ( dK1 dK2 . . . dKM )                     |
|------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| n                                                                                              | Tally number. Restriction: n ≤ 99999999                                                                          |
| K                                                                                              | Number of cells or surfaces on F card, including T if present.                                                   |
| M                                                                                              | Number of segmenting bins on the FS card, including the remainder segment, and the total segment if FS has a T . |
| dkm                                                                                            | Area, volume, or mass of k th segment of the m th surface or cell bin for tally n .                              |

Use: Not with detector ( F5 ) tallies or DXTRAN ( DXT ) spheres. The
parentheses are optional. May be required with FS card. Can be used
without FS card.

MCNP6 uses the following hierarchy for determining the volume, area, or
mass:

For cell or surface without segmenting (tally types 2, 4, 6, and 7):

<!-- image -->

- non-zero entry on SD card

- non-zero entry on VOL or AREA card
- volume, area, or mass calculated by MCNP6
- fatal error

For cell or surface with segmenting (tally types 2, 4, 6, and 7):

- non-zero entry on SD card
- volume, area, or mass calculated by MCNP6
- fatal error

For surface in a type 1 tally:

- non-zero entry on SD card
- no divisor

## 5.9.15.1 Example 1

```
F4:N 1 2 3 T
```

```
1 2 SD4 1 1 1 1
```

Note that the SD card can be used to define tally divisors even if the
tally is not segmented. In this example the tally calculates the flux in
the three cells plus the union of the three cells. The VOL card can be
used to set the volume divisor of the three cells (to unity, for
example), but it cannot do anything about the divisor for the union. Its
divisor is the sum of the volumes (whether MCNP6-calculated or user-
entered) of the three cells. However, the divisors for all four of the
cell bins can be set to unity by means of the SD card. These entries
override entries on the VOL and AREA cards. See §5.9.1.5 for use with
repeated structure tallies.

## 5.9.16 FU: Special Tally or TALLYX Input

This card is used with a user-supplied tally modification subroutine
TALLYX and some cases of the FT card. If the FU card has no input
parameters, TALLYX will be called but no user bins will be created. The
k entries on the FU card serve three purposes:

1. each entry establishes a separate user tally bin for tally n ,
2. each entry can be used as an input parameter for TALLYX to define the user bin it establishes, and
3. the entries appear in the output as labels for the user bins.

| Data-card Form: FU n [ x1 . . . xK ] [ NT ] [ C ]   | Data-card Form: FU n [ x1 . . . xK ] [ NT ] [ C ]                                               |
|-----------------------------------------------------|-------------------------------------------------------------------------------------------------|
| n                                                   | Tally number. Restriction: n ≤ 99999999                                                         |
| xk                                                  | Input parameter establishing user bin k .                                                       |
| NT                                                  | Optional entry to inhibit MCNP6 from automatically providing the total over all specified bins. |
| C                                                   | Optional entry that causes the bin values to be cumulative.                                     |

Default: If the FU card is absent, subroutine TALLYX is not called.

Use: Used with a user-supplied TALLYX subroutine or FT card.

## 5.9.16.1 Programming Hint

iptal(3,1,tally \_ p \_ thread%ital) is the pointer to the location in the
tds array of the word preceding the location of the data entries from
the FU card. Thus if the FU card has the form shown above,

```
1 tds(L+1) = x1 2 tds(L+2) = x2 3 . 4 . 5 . 6 tds(L+k) = xk
```

where

```
L = iptal(3,1,tally _ p _ thread%ital) (5.41) k = iptal(3,4,tally _ p _ thread%ital) -1 = iptal(3,3,tally _ p _ thread%ital) -1 (5.42) n = jptal(1,tally _ p _ thread%ital) (5.43)
```

and tally \_ p \_ thread%ital is the program number of the tally.

MCNP6 automatically provides the total over all specified user bins. The
total can be inhibited for a tally by putting the symbol NT at the end
of the FU card, which changes the variables such that:

<!-- formula-not-decoded -->

The symbol C at the end of the FU card causes the bin values to be
cumulative, in which case

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The discussion of the iptal and jptal arrays in the MCNP5 Volume III:
Developer's Guide [312] and the following description of TALLYX may be
useful.

## 5.9.17 TALLYX: User-supplied Tally Subroutine

TALLYX is called whenever a tally with an associated FU card but no FT
card is scored. It is called for tally n only if an FU card is in the
MCNP input file.

## 5.9.17.1 Programming Hint

The locations of the calls to TALLYX are such that TALLYX is the very
last thing to modify a score before it is posted in the tally. TALLYX
calls can be initiated by more than one FU n card for different values
of n ; a branch must be constructed inside the subroutine based on which
tally F n is calling TALLYX , where n = jptal(1,tally \_ p \_ thread%ital)
. TALLYX has the form shown in Listing 5.56.

```
1 subroutine tallyx(t,ib) 2 ! dummy for user-supplied tallyx subroutine. 3 ! t is the input and output tally score value. 4 ! ib controls scoring. see the user's manual. 5 6 ! .. Use Statements .. 7 use mcnp _ params, only : dknd, zero 8 use fixcom, only : jtlx 9 use errprn _ mod, only : errprn 10 use mcnp _ debug 11 12 implicit none 13 14 ! .. Scalar Arguments .. 15 real(dknd), intent(inout) :: t 16 integer, intent(inout) :: ib 17 18 ! print a warning the first time this dummy tallyx is called. 19 if(jtlx == 0)call errprn(jtlx,0,zero,zero,' ',' ',& 20 & 'a tallyx subroutine is ordinarily needed with fu cards.') 21 return 22 end subroutine tallyx
```

Listing 5.56: example\_default\_tallyx.f90.txt

The quantity t (first argument of TALLYX ) that is scored in a standard
tally can be multiplied or replaced by anything. The modified score t is
then put into one of the k user bins established by the FU card.

In TALLYX(t,ib) the second argument ib is defined to allow for more than
one pass through TALLYX per tally score. By default, ib = 0 , which
means make one pass through the MCNP6 coding where user bin tally scores
are posted. If the user sets ib &lt; 0 in TALLYX , no score will be made.
If the user sets ib &gt; 0 , passes through the user bin loop including
TALLYX will be made until ib is reset to zero. This scheme allows for
tally modification and posting in more than one user bin. The variable
tally \_ p \_ thread%ibu is the variable designating the particular user
bin established by the FU card. Its value is 1 before the first pass
through the user bin loop. The indices of the current user, segment,
cosine, energy, and time bins ( tally \_ p \_ thread%ibu , tally \_ p \_
thread%ibs , tally \_ p \_ thread%ibc , tally \_ p \_ thread%ibe , and tally
\_ p \_ thread%ibt , respectively) and the flag tally \_ p \_ thread%jbd
that indicates flagged- or direct-versus-not are in the module TSKCOM
for optional modification by TALLYX . Note that the index of the
multiplier bin is not available and cannot be modified. The variable
tally \_ p \_ thread%ntx is from the module TSKCOM . It is set equal to nx
just before the CALL TALLYX in TALLYD , TALLY , and TALPH . The variable
nx is set to unity just before the start of the user bins loop and is
incremented after the CALL TALLYX , so tally \_ p \_ thread%ntx contains
the number of the TALLYX call. An example of using tally \_ p \_
thread%ntx to tally in every user bin before leaving the user bin loop
is shown in Listing 5.57.

```
1 subroutine tallyx(t, ib) 2 use mcnp _ params 3 use mcnp _ global 4 use mcnp _ debug
```

Listing 5.57: example\_tallyx\_ubin\_score.f90.txt

```
5 use tskcom, only: tally _ p _ thread 6 use basic _ tally, only: iptal 7 8 implicit none 9 10 ! .. Scalar Arguments .. 11 real(dknd), intent(inout) :: t 12 integer, intent(inout) :: ib 13 14 t = 1d0 ! Whatever you want. 15 tally _ p _ thread%ibu = tally _ p _ thread%ntx 16 ib = 1 17 if (tally _ p _ thread%ntx > iptal(3, 4, tally _ p _ thread%ital) -1) ib = 0 18 return 19 end subroutine tallyx
```

If tally \_ p \_ thread%ibu is out of range, no score is made and a count
of out-of-range scores is incremented. If excessive loops through TALLYX
are made, MCNP6 assumes ib has been incorrectly set and terminates the
calculation with a BAD TROUBLE error (excessive means greater than the
product of the numbers of bins of all kinds in the tally). Several
examples of the FU card and TALLYX appear in Section 10.2.8. The
procedure for implementing a TALLYX subroutine is the same as for the
user-provided SOURCE subroutine.

## 5.9.18 FT: Special Treatments for Tallies

| Data-card Form: FT n id1 p11 p12 p13 . . . idK pK1 pK2 pK3 . . .   | Data-card Form: FT n id1 p11 p12 p13 . . . idK pK1 pK2 pK3 . . .                                                |
|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| n                                                                  | Tally number. Restriction: n ≤ 99999999                                                                         |
| idk                                                                | The alphabetic keyword identifier for a special treatment (see Table 5.20)                                      |
| pkj                                                                | Input parameters for the special treatment specified by idk : either a number, a parenthesis, or a colon ( 1 ). |

Default: If the FT card is absent, there is no special treatment for
tally n .

Use: Optional; as needed.

## Details:

- 1 The syntax and meaning of the pkj is different for each idk . A special treatment may cause a set of user bins or possibly a set of some other kind of bins to be created. The information in the pkj allows the number and kind of those bins to be inferred easily. More than one special treatment can be specified by a given tally except for combinations of INC , ICD , SCD , PTT , PHL , RES , TAG , and FFT . Only one of these special treatments can be used by a tally at one time because all require user bins making them mutually exclusive.
- 2 Some FT treatments require an FU card; treatments that require or allow an FU card are not compatible with each other.
- 3 The SPM , FNS , and LCS treatments are incompatible with other FT options.

Descriptions of the available special treatments follow with an
explanation of the allowed parameters for each.

Table 5.20: Special Treatment for Tallies Card ( FT )

| Keyword   | §         | Description                                                           |
|-----------|-----------|-----------------------------------------------------------------------|
| FRV       | 5.9.18.1  | Fixed arbitrary reference direction for tally 1 or 2 cosine binning.  |
| GEB       | 5.9.18.2  | Gaussian energy broadening.                                           |
| TMC       | 5.9.18.3  | Time convolution.                                                     |
| INC       | 5.9.18.4  | Identify the number of collisions ( 2 ).                              |
| ICD       | 5.9.18.5  | Identify the cell from which each detector score is made ( 2 ).       |
| SCX       | 5.9.18.6  | Identify the sampled index of a specified source distribution.        |
| SCD       | 5.9.18.7  | Identify which of the specified source distributions was used ( 2 ).  |
| ELC       | 5.9.18.8  | Electron current tally.                                               |
| PTT       | 5.9.18.9  | Put different multigroup particle types in different user bins ( 2 ). |
| PHL       | 5.9.18.10 | Pulse-height light tally with anticoincidence ( 2 ).                  |
| CAP       | 5.9.18.11 | Coincidence capture.                                                  |
| RES       | 5.9.18.12 | Heavy-ion and residual isotopes ( 2 ).                                |
| TAG       | 5.9.18.13 | Tally tagging ( 2 ).                                                  |
| LET       | 5.9.18.14 | Linear energy transfer. Energies as stopping powers.                  |
| ROC       | 5.9.18.15 | Receiver Operator Characteristic (ROC) curve generation.              |
| PDS       | 5.9.18.16 | Point detector sampling.                                              |
| FFT       | 5.9.18.17 | First fission tally ( 2 ).                                            |
| COM       | 5.9.18.18 | Compton image tally.                                                  |
| SPM       | 5.9.18.19 | Scatter probability matrix ( 3 ).                                     |
| MGC       | 5.9.18.20 | Flux weighted multigroup cross sections.                              |
| FNS       | 5.9.18.21 | Induced fission neutron spectra ( 3 ).                                |
| LCS       | 5.9.18.22 | Legendre coefficients for scatter reactions ( 3 ).                    |

## 5.9.18.1 FRV v1 v2 v3

The vi are the ( x, y, z ) components of vector v , not necessarily
normalized. If the FRV special treatment is in effect for a type 1 or 2
tally, the direction v is used in place of the vector normal to the
surface as the reference direction for getting the cosine for binning.

## 5.9.18.2 GEB a b c

The parameters specify the full width at half maximum (FWHM) of the
observed energy broadening in a physical radiation detector, where E is
the energy of the particle. The units of a , b , and c are MeV, MeV 1 /
2 , and MeV -1 , respectively. The energy actually scored is sampled
from a Gaussian with that FWHM.

## 5.9.18.3 TMC a b

All particles should be started at time zero. The tally scores are made
as if the source was actually a square pulse starting at time a and
ending at time b .

## 5.9.18.4 INC

No parameters follow the INC keyword but an FU card is required. Its bin
boundaries are the number of collisions that have occurred in the track.
The user can control if secondary particles are considered

<!-- formula-not-decoded -->

un-collided (default) or collided at their creation with use of the UNC
card. If the INC special treatment is in effect, the call to TALLYX that
the presence of the FU card would normally trigger does not occur.
Instead ibu is set by calling JBIN with the number of collisions as the
argument. To capture all particles, the last FU bin value should be a
very large number.

## 5.9.18.5 ICD

No parameters follow the keyword ICD but an FU card is required. Its
bins are the names of some or all of the cells in the problem. If the
cell from which a detector score is about to be made is not in the list
on the FU card, the score is not made. The result is that the detector
tally is subdivided into bins according to which cell had the source or
collision resulting in the detector score. TALLYX is not called. The
selection of the user bin is done in TALLYD .

## 5.9.18.6 SCX k

The parameter k is the name of one of the source distributions and is
the k that appears on the SI k card. One user bin is created for each
bin of source distribution k plus a total bin. The scores for tally n
are then binned according to which bin of source distribution k the
source particle came from. The score of the total bin is the score you
would see for tally n without the special treatment, if source
distribution k is not a dependent distribution.

## /warning\_sign Caution

For a dependent distribution, the score in the total bin is the subtotal
portion of the score from dependent distribution k .

## 5.9.18.7 SCD

No parameters follow the keyword SCD but an FU card is required. Its
bins are a list of source distribution numbers from SI k cards. The
scores for tally n are then binned according to which distribution
listed on the FU card was sampled. This feature might be used to
identify which of several source nuclides emitted the source particle.
In this case, the source distributions listed on the FU card would
presumably be energy distributions. Each energy distribution is the
correct energy distribution for some nuclide known to the user and the
probability of that distribution being sampled from is proportional to
the activity of that nuclide in the source. The user might want to
include an FC card that tells to what nuclide each energy distribution
number corresponds.

## /warning\_sign Caution

If more than one of the source distributions listed on the FU card is
used for a given history, only the first one used will score.

## 5.9.18.8 ELC c

The single parameter c of ELC specifies how the charge of a particle is
to affect the scoring of an F1 tally. Normally, an F1 tally gives
particle current without regard for the charge of the particles.
Additionally, this treatment can create separate bins for particles and
antiparticles. There are three possible values for c :

```
c = 1 to cause negatively charged particles to make negative scores, c = 2 to put charged particles and antiparticles into separate user bins, and c = 3 for the effect of both c = 1 and c = 2 .
```

If c = 2 or 3, three user bins (e.g., positrons, electrons, and total)
are created.

## 5.9.18.9 PTT

No parameters follow the keyword PTT but an FU card is required. Its
bins are a list of atomic weights in units of MeV of particles
masquerading as neutrons in a multigroup data library. The scores for
tally n are then binned according to the particle type as differentiated
from the masses in the multigroup data library. For example, 0.511 0
would be for electrons and photons masquerading as neutrons.

## 5.9.18.10 PHL

The PHL keyword has the form:

```
PHL [ N ta1 ba1 ta2 ba2 . . . taN baN ] [ det1 ] [ M tb1 bb1 tb2 bb2 . . . tbM bbM ] [ det2 ] [ J tc1 bc1 tc2 bc2 . . . tcJ bcJ ] [ det3 ] [ K td1 bd1 td2 bd2 . . . tdK bdK ] [ det4 ] [ 0 ] [ TDEP tg tt ]
```

The PHL option models a pulse-height tally with anti coincidence. This
option allows the F8 tally to be based on energy/light deposition in up
to four regions as specified via F6 tallies. Requires an FU card.

The parameters for keyword PHL are the following:

| N       | is the number of F6 tallies for the first detector region,                                                         |
|---------|--------------------------------------------------------------------------------------------------------------------|
| taN baN | are the pairings of tally number and F -bin number (see 5.9.19) for the N F6 tallies of the first detector region, |
| det1    | is an optional detector descriptor chosen from Table 5.21 for the first detector region,                           |
| M       | is the number of F6 tallies for the second detector region,                                                        |
| tbM bbM | are the pairings of tally number and F -bin number for the M F6 tallies of the second detector region,             |
| det2    | is an optional detector descriptor chosen from Table 5.21 for the second detector region,                          |
| J       | is the number of F6 tallies for the third detector region,                                                         |
| tcJ bcJ | are the pairings of tally number and F -bin number for the J F6 tallies of the third detector region,              |
| det3    | is an optional detector descriptor chosen from Table 5.21 for the third detector region,                           |
| K       | is the number of F6 tallies for the fourth detector region,                                                        |

Table 5.21: Detector Descriptors for the FT PHL Option

| Detector Type   | Detector Name   | Primary Particle Type(s)   | Response Parameter   | Default Value         | Notes            |
|-----------------|-----------------|----------------------------|----------------------|-----------------------|------------------|
| 3 He            | HE3-1           | Proton, Triton, Helion     | Multiplication       | 100                   | 42.3 eV/ion pair |
| BF 3            | BF3-1           | Alpha, Lithium             | Multiplication       | 100                   | 36.0 eV/ion pair |
| Li Glass        | LIG-1           | Triton, Alpha              | Quenching Factor     | 5 . 0 × 10 - 4 cm/MeV | Generic value    |
| LiI             | LII-1           | Triton, Alpha              | Quenching Factor     | 5 . 0 × 10 - 4 cm/MeV | Generic value    |
| ZnS+LiF         | ZNS-1           | Triton, Alpha              | Quenching Factor     | 5 . 0 × 10 - 4 cm/MeV | Generic value    |
| NaI             | NAI-1           | Electron                   | Quenching Factor     | 3 . 4 × 10 - 4 cm/MeV | [313]            |
| BGO             | BGO-1           | Electron                   | Quenching Factor     | 6 . 5 × 10 - 4 cm/MeV | [314]            |
| CsI             | CSI-1           | Electron                   | Quenching Factor     | 1 . 5 × 10 - 4 cm/MeV | [314]            |
| BC-400          | BC4-1           | Electron                   | Quenching Factor     | 4 . 6 × 10 - 3 cm/MeV | [315]            |
| HPGe            | HPG-1           | Electron                   | Gain                 | 1.0                   | 3.0 eV/ion pair  |

| tdK bdK    | are the pairings of tally number and F -bin number for the K F6 tallies of the fourth detector region,                                                                                                                                                    |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| det4       | is an optional detector descriptor chosen from Table 5.21 for the fourth detector region,                                                                                                                                                                 |
| 0          | a zero entry terminates input for PHL detectors entries and allows for other FT options to follow,                                                                                                                                                        |
| TDEP tg tt | is a keyword option that specifies a tally that will be used as a trigger for the related T8 card. The first optional TDEP entry ( tg ) specifies the trigger tally number and the second optional TDEP entry ( tt ) specifies an energy threshold (MeV). |

The F -bin descriptor specified after each tally, bai or bbi , may be
'0', indicating that the referenced tally includes a lattice description
of multiple lattice elements. When this option is specified, all tallies
within that PHL region must also include the '0' descriptor for bai or
bbi and all tallies must be over the same lattice cell and elements.
When this option is used in both PHL regions, the related F8 F -bins are
modified, with an appropriate warning message, to include J × K bins,
where J is the number of lattice elements included in PHL Region 1 and K
is the number of lattice elements included in PHL Region 2. The output
of Tally 8 will include coincidence results for all J × K bins, along
with appropriate cell labels (e.g., 1[0 1 1] + 2[0 0 0] , which is the
combination of lattice cell 1, element [0 1 1] , with lattice cell 2,
element [0 0 0] ). This special F -bin descriptor is typically used with
the FT COM option to create a Compton image of a radiation source.

When a detector descriptor is specified, built-in particle-dependent
response functions are automatically applied to all listed tallies
(e.g., ta1 , ta2 , . . . for det1 ). For photon detectors, these include
materialdependent electron response functions (light output, current,
etc.). For neutron detectors, these include material-dependent electron
or light-ion response functions. Additional details on references
regarding these parameters can be found in the source code (
Source/src/fluence \_ to \_ dose.F90 ).

The gas detectors are treated by multiplying the charged-particle energy
deposition by the inverse of the gas work function (see Details in
§5.9.18) and the detector E -field multiplication (response parameter).
The units for this response function are pico-Coulombs (pC) per source
particle, thus this detector response is further multiplied by the
electron charge per ion pair ( 1 . 6 × 10 -7 pC). The user can override
the default multiplication by appending an underscore and a
multiplication value to the detector name (e.g., HE3-1 \_ 25.0 ).

The scintillation detectors are treated by Birks's Law [316], which is
generally in good agreement with measured data for Z &lt; 6 and particle
energies less than ≈ 50 MeV/amu. The stopping powers used in Birks's Law
are the total stopping powers calculated by the MCNP code for each
particle type. The units for this response function are 1-MeVee photons
per source particle (an MeVee is MeV electron-equivalent). For absolute
visible light photons per source particle, one must multiply this
response by the number of visible light photons produced by a 1-MeV
electron (which is typically given by the detector manufacturer or can
be found in the literature). The default Birks's quenching factors (QF)
are given in Table 5.21, however

the user may override these values by appending an underscore and a QF
value to the detector name (e.g., LIG-1 \_ 2.5e-3 ).

The semi-conductor detector is treated similarly to a gas detector,
except the work function is typically much lower ( ≈ 3 eV/ion pair) and
the multiplication is replaced by the gain. The units for this response
are also pC per source particle. The user can override the default gain
by appending an underscore and new gain value to the detector name
(e.g., HPG-1 \_ 2.5 ).

When M is non-zero, indicating the use of two or more detector regions,
an FU card is required for the F8 tally. The entries on the FU card are
presented in units of MeV (unless modified by DE / DF cards associated
with the specified F6 tallies) and must increase monotonically.
Similarly, if J or K is non-zero, the energy bins must be specified with
C (tally cosine) and FS (tally segment) cards, respectively. The
particle type indicated on the F8 tally does not matter because this
tally allows a combination of light output from various particle types.
If baN is zero, then the number of cell bins on the F8 card must match
that on the corresponding taN tally card, which is useful for a lattice
pulse-height PHL tally.

The TDEP keyword allows the T8 values to be relative to the first
contribution to any FT8 PHL tally. Invoking TDEP allows pulse
distributions from different histories to be relative to the same start
time rather than distributed in absolute time with significant variation
based on when a particle reaches the detector. TDEP can also be followed
by one or two entries, where the first entry ( tg ) is a tally number
and the second ( tt ) is an energy threshold. If an energy threshold
value is provided, the reference time on the T8 card is whenever the
specified tally has a value greater than the specified threshold. The
specified tally can be the same number as the F8 tally, in which case
TDEP depends on the sum of the PHL F6 tallies, or it can be a single F6
tally that is specified in any region of the FT PHL option. If the tally
number has a format of 8.3 (e.g., F8.3 ), for example, then the trigger
tally is the sum of all F6 tallies that are specified for region 3 of
the FT PHL option. The default TDEP tally number is the corresponding F8
tally number and the default energy threshold is 0 MeV.

## 5.9.18.10.1 Time-dependent F8 Tallies Using the Pulse-height Light (PHL) Option

The T (time bin) card is allowed with pulse-height tallies ( F8 ), but
only when used in conjunction with the FT PHL option. In this case, the
time-dependent energy deposition is taken from the associated F6
tally(s). If the time entries on the F8 card do not match those provided
for the various F6 tallies, a fatal error is issued. If the associated
F6 tallies do not have T cards, then one matching the F8 tally will be
created automatically.

## 5.9.18.10.2 Example 1

Case 1

```
1 F8:N 5 2 FT8 PHL 1 6 1 0 3 GEB a b c 4 E8 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 5 F6:E 5 6 DE6 LIN 1.0 1.5 2.0 2.5 3.0 3.5 10.0 7 DF6 LIN 1.0 0.99 0.98 0.97 0.96 0.95 0.92
```

Case 2

```
1 F8:N 5 2 FT8 PHL 1 6 1 1 16 1 0 3 GEB a b c 4 E8 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 5 FU8 1.5 2.5 3.5 4.5 5.5 6.5 7.5 8.5 6 F6:E 5 7 DE6 LIN 1.0 1.5 2.0 2.5 3.0 3.5 10.0 8 DF6 LIN 1.0 0.99 0.98 0.97 0.96 0.95 0.92 9 F16:E 6 10 DE16 LIN 1.0 1.5 2.0 2.5 3.0 3.5 10.0 11 DF16 LIN 1.0 0.99 0.98 0.97 0.96 0.95 0.92
```

In both cases, the F6 tallies convert energy deposition to equivalent
light (units of MeV, photons, or MeVee, depending on the units of the
associated DF card). SD cards are not required with the F6 tallies
because these divisors renormalize only the printed output for the F6
tallies and not the values stored in the tally arrays (thus, the F8
tally will result in the same value, regardless of whether the F6 tally
has an SD card). The DE / DF conversion is based on the incident
particle energy, and the values on the DF card should be the d L/ d E
for that incident particle energy. Thus, the F6 tally will multiply the
d L/ d E values by the energy deposition to give the light output ( ∆ L
) summed over each track. Also, no energy bins exist for the F6 tallies.
The F8 tally uses the total light output. Energy bins ( E 6 card) can be
added, but the F8 tally will use the value from the total bin.
Similarly, for other bins associated with the F6 tally, in each case,
the tally fluctuation chart bin is used to extract the value for the F8
tally (see the TF card to alter this). The FT GEB cards are used to
perform Gaussian broadening on these tally values; however, this is done
only at the end of the particle history to determine the light output
value used in the pulse-height tally.

In Case 1, the electron light output from only one region (cell 5) is
used to subdivide the pulse-height tally. In this case, a pulse of 1
(input source weight) is put into the first E 8 bin when the light
output in cell 5 is &lt; 1 MeV. It is placed in the second E8 bin when the
light output is between 1 and 2 MeV, etc. A zero F6 tally will result in
no F8 tally.

In Case 2, the light output from two regions (cells 5 and 6) is used to
subdivide the pulse-height tally. This case is useful for
coincidence/anti-coincidence applications. A pulse of 1 (input source
weight) is put into the second E8 bin and into the second FU8 bin when
the light output in cell 5 is 0 &lt; L &lt; 1 . 0 MeV and the light output in
cell 6 is 0 &lt; L &lt; 1 . 5 MeV. This pulse is put into the second E 8 bin
and into the third FU 8 bin when the light output in cell 5 is 0 &lt; L &lt; 1
. 0 MeV and the light output in cell 6 is between 1.5 and 2.5 MeV. A
zero light output in both cells will result in no F8 tally. A zero light
output in cell 5 (tally 6) with a non-zero light output in cell 6 (tally
16) will result in a pulse in the first E8 bin and the corresponding FU8
bin. Similarly, for a zero light output in cell 6 and a non-zero light
output in cell 5, a pulse will be put into the first FU8 bin and the
corresponding E8 bin. Note that the E8 and FU8 bins do not have to be
the same and typically would not be unless the detector regions were of
similar material and size. Separate F6 tallies (as in Case 2, F6 and F16
) are needed only when the two regions have different light conversion
functions. If the two regions are of the same material, then a single F6
tally can be used as follows:

## 5.9.18.10.3 Example 2

```
1 F8:N 5 2 FT8 PHL 2 6 1 6 2 0 3 E8 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 4 FU8 1.5 2.5 3.5 4.5 5.5 6.5 7.5 8.5 5 F6:E 5 6 6 DE6 LIN 1.0 1.5 2.0 2.5 3.0 3.5 10.0
```

```
7 DF6 LIN 1.0 1.1 1.2 1.3 1.4 1.5 1.6
```

In this example, the light output from the two regions (cells 5 and 6),
which are included on the same F6 tally, is used to subdivide the pulse-
height tally.

Currently, it is not important what cell is listed on the F8 card
because this tally is made only at the end of a particle history and
depends only on the tally results of the listed F6 tallies. Having
multiple cells listed on the F8 card is meaningful only when the F -bin
parameter (i.e., baN or bbN ) of the FT PHL option is zero, indicating a
lattice grid of detector regions. Otherwise, each additional F8 cell bin
simply will be a duplicate of the first cell bin.

## 5.9.18.10.4 Example 3

```
1 F6:H 1 2 F16:T 1 3 F8:h,t 1 4 FT8 PHL 2 6 1 16 1 0 5 T8 10 20 30 40 50 60 70 80 90 100 1e37
```

In this example, the proton ( F6 ) and triton ( F16 ) energy depositions
in cell 1 are combined into a pulse-height tally ( F8 ) using the FT PHL
option. The time-dependent behavior of these pulses is segregated into
11 time bins: 0-10 shakes, 10-20 shakes, etc. To obtain the time-
dependent pulse shape, time-dependent energy depositions are obtained
from the tallies identified by the PHL option. To accomplish this, the
11 specified T8 bins are applied to the associated F6 and F16 tallies
with the automatic creation of matching T6 and T16 cards. A warning
message is generated when these cards are created.

## 5.9.18.11 CAP [ -mc ] [ -mo ] i1 i2 [ GATE td tw ] [ EDEP tg tt ]

The FT8 capture tally scores the number of captures in specified
combinations of nuclides at the end of each history. Time gating with
pre-delay and gate width treatments is optional [317]. It is
particularly useful for neutron coincidence detectors. In addition,
captures may be written to an auxiliary output file, PTRAC . Section
5.13.6 describes the PTRAC capture file.

The FT8 CAP option converts the pulse-height tally to a neutron capture
tally. Variance reduction is no longer allowed, time bins are allowed
(unlike other F8 tallies), cosine bins are used to store capture
frequencies and moments, and PRINT table 118 is created in the MCNP
output file.

The parameters for keyword CAP are described as follows:

| mc   | is the optional maximum number of captures (Default is 21),              |
|------|--------------------------------------------------------------------------|
| mo   | is the optional maximum number of moments (Default is 12), and           |
| in   | are the capture nuclide identifiers [§1.2.2]. All formats are supported. |

In addition, the time-gate keyword GATE may appear with its parameters,
td and tw , where

```
td is the pre-delay time and
```

1

2

3

```
tw is the gate width;
```

and the energy deposition keyword EDEP may appear with its parameters,
tg and tt , where

| tg   | is the trigger tally number and                        |
|------|--------------------------------------------------------|
| tt   | is the trigger tally threshold (MeV) (Default is 0.0). |

The EDEP keyword specifies to record a capture whenever tally tg
produces an energy deposition greater than tt . Tally tg can be any F6
or F8 tally, but is usually the related F8 tally of the FT CAP option
(which is the default).

## 5.9.18.11.1 Example 1

| F8:N   |     | 2 (5   | 6) 7 T   |
|--------|-----|--------|----------|
| FT8    | CAP | Li-6   | B-10     |
| T8     |     | 1 7LOG | 1E8      |

In this example, captures and moments are tallied in cells 2, 7, in the
combination of 5 and 6 and in the total over cells 2, 5, 6, 7. The
captures by either 6 Li or 10 B are tallied. Results are tabulated in
time bins at 1, 10, 100, 1000, 10 4 , 10 5 , 10 6 , 10 7 , and 10 8
shakes-that is, in the range of 10 nanoseconds to 1 second.

## 5.9.18.11.2 Example 2

| F8:N    | 4                 |
|---------|-------------------|
| FT8 CAP | He-3 GATE 0.5 0.4 |

In this example, 3 He captures and moments are tallied in cell 4. There
is a time gate with a pre-delay treatment of 0.5 shakes ( 5 × 10 -9
seconds) and a width of 0.4 shakes ( 4 × 10 -9 seconds).

## 5.9.18.11.3 Example 3

| * F8:H,T   | 999   |      |         |
|------------|-------|------|---------|
| F18:N      | 999   |      |         |
| FT18       | CAP   | EDEP | 8 0.001 |

1

2

3

In this example, a capture is scored in Tally 18 whenever there is an F8
tally that exceeds 0.001 MeV.

The addition of the pre-delay and time gate width changes the capture
tally scoring. When a neutron is captured at time t 0 in the specified
cell by the specified nuclide, the gate is 'turned on.' If the pre-delay
duration is t 1 and the gate width is t 2 , then all captures between t
0 + t 1 and t 0 + t 1 + t 2 are counted. For a history with no captures,
no events are scored. With one capture, zero events are scored. With two
captures,

the first turns on the time gate at time t 0 and scores 0; the second
will score one event if it is captured between t 0 + t 1 and t 0 + t 1 +
t 2 , or score another 0 if outside the gate.

## /warning\_sign Caution

Coincidence counting of capture multiplicities and moments requires
analog capture: CUT : n 2J 0 0 . Calculations must be totally analog
with no variance reduction. Fission multiplicity also is required: PHYS
: n J 100 3J -1 . An FT 8 CAP tally in an input file will automatically
set analog capture, fission multiplicity, and exit with error messages
if variance reduction is used.

The capture tallies may be written to a PTRAC file for further analysis
by auxiliary codes. See §5.13.6 on the PTRAC card extensions.

## 5.9.18.12 RES [ z1 z2 ] or RES [ za1 za2 . . . ]

The interaction of high-energy particles with target nuclei causes the
production of many residual nuclei. The generated residual nuclei can be
recorded to an F8 tally if used with an FT8 RES special treatment
option. The residuals are recorded at each physics model interaction as
well as each neutron library interaction. The residual data can be
accumulated for the entire geometry (when no cells are listed) or for
specific cells listed on the F8 : # card. A specific list of targets may
also be requested on the FT RES card. Requires an FU card.

The FT8 RES capability can also be used with type 1, 2, 4, and 6 heavy-
ion tallies ( F n : # ) to segregate the score into bins according to
the heavy ion that produced the score.

By default, the FT RES card with no entries causes the corresponding
tally to create a user bin for each of the 2200+ possible residual
nucleus ion types. A range of bins may be selected by specifying lower
and upper proton numbers, z 1 and z 2 , which correspond to a range of
possible Z values. If z 1 and z 2 are specified and a residual is
generated with a higher or lower Z , the residual will not be scored in
the tally. To specify an explicit list of heavy ions to be tallied,
provide target identifiers [§1.2.2] after the RES keyword. All formats
are supported. Specifying an elemental identifier, such as Fe-0 for
iron, will include all nuclides of that element into a single bin.
Metastable residuals will be included with non-metastable counterparts.
A metastable input is not allowed.

When used with the F8 : # tally, the FT RES card yields a list of
residual nuclides produced by all neutroninduced reactions and model
reactions of all incident particle types (photon and proton library
reactions do not yet produce residuals). The residual tallies can be
obtained either with or without the emission of delayed neutrons and/or
delayed gammas. Residual tallies can be obtained for analog or non-
analog (implicit capture) neutron transport. The residuals are just the
residuals of the nuclear reactions and not their decay products.

For models that include light-ion recoil and the neutron capture ion
algorithm (NCIA) (activated using the 7th entry on the PHYS : n card),
reaction residuals are included in the FT 8 RES tally. In most
instances, reaction residuals are determined using the ENDF reaction
specifications for simple-multi-particle reactions. In rare instances,
e.g., neutron bombardment of 6 Li(n,t) α , the ENDF reaction
specifications can result in only light-ion production. In such cases,
the heaviest light-ion residual is selected.

## 5.9.18.12.1 Example 1

```
F4:# 6
```

```
1 2 FT4 RES O-16 Ca-40 Fe-0 U-238
```

This combination of tally cards creates a track-length tally in cell 6
and then creates three user bins for the nuclides 16 O, 20 Ca, and 238
U. It also creates one bin for all iron nuclides.

## 5.9.18.12.2 Example 2

| F8:#   | 1 100   |    |   T |
|--------|---------|----|-----|
| FT8    | RES     | 25 |  27 |

The entries on the F8 tally card are cell numbers for which residuals
are to be tallied. In this example, residual tallies are requested for
cell 1, cell 100, and for cells 1 and 100 combined. The entries on the
FT8 RES card specify the range of possible Z values for which to tally
the residuals. Here, residuals with atomic numbers between (and
including) Z = 25 and Z = 27 will be scored.

## 5.9.18.12.3 Example 3

```
1 F8:# 1 100 T 2 FT8 RES Mn-54 Mn-55 Mn-56 Fe-55 Fe-56 Fe-57 Co-56 Co-57 Co-58
```

The entries on the F8 tally card are cell numbers for which residuals
are to be tallied. In this example, residual tallies are requested for
cell 1, cell 100, and for cells 1 and 100 combined. The entries on the
FT8 RES card specify a list of isotopes for scoring residuals.
Production for specific isotopes of manganese, iron, and cobalt will be
included for this F8 tally.

The FT8 RES capability is particularly useful with the eighth LCA card
entry, noact . When noact = -2 on the LCA card, the source particle
immediately collides in the source material. All subsequent daughter
particles then are transported without further collision, as if in a
vacuum. The F8 tally with an FT8 RES special tally treatment is then
simply the distribution of nuclides resulting from a single collision.

For additional information involving fission multiplicity see the
discussion presented in §5.7.9. More capture tally information and
examples appear in §10.2.5.5 and §10.2.5.6. To inspect a residual nuclei
tally example, see §10.2.5.8.

## 5.9.18.13 TAG a

Tally tagging allows the user to separate a tally into components based
on how and where the scoring particle was produced. This feature is
available for both standard ( F1 , F2 , F4 , F6 , F7 ) and detector ( F5
) tallies. Requires an FU card.

The single required parameter a of the keyword TAG specifies how scatter
is to be treated (i.e., whether the creation tag on a particle should be
retained or a separate scatter tag be invoked). More specifically, if

| a = 1   | particles undergoing elastic scattering will lose their tag and bremsstrahlung and annihilation photons will be included in the 'scatter' bin (i.e., FU '0' bin);                                                                                                                                                                                                       |
|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| a = 2   | particles undergoing elastic scattering will lose their tag, but bremsstrahlung and annihilation photons will be segregated (see appropriate FU bins below);                                                                                                                                                                                                            |
| a = 3   | particles undergoing elastic scattering will retain their production tag. If a particle has multiple production events, the tag will be for the last production event. For example, a neutron undergoing fission followed by (n,2n) would have the (n,2n) tag. If a particle undergoes an elastic scatter, its previous tag is retained (i.e., no need for FU '0' bin); |

a = 4 same conditions as a = 3 except Compton photoatomic interactions
retain their tag. Neutron interactions behave identically as a = 3 .

Binning specifications for the tagged tally must be provided on the FU
special tally card. Each bini entry on the card requests three distinct
pieces of tagging information:

1. a cell of interest where particles are produced;
2. a target nuclide from which the particle is emitted; and
3. a reaction MT identifier, or, in the case of spallation, a residual nuclide of interest, or a special designator (see below).

The format on the FU card when used in association with the tagging
treatment is FU n bin1 bin2 . . . binN [ NT ] where each tagging bini
has the form CCCCCZZAAA.RRRRR and

| CCCCC   | represents a user cell number. Note: leading zeros are not required.                                                                                                                                                                                                             |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ZZAAA   | represents a 5-digit target identifier [§1.2.2] in the ZAID form for a target nuclide where ZZ is the atomic number and AAA is the atomic mass number. Note: ZZ is limited to two characters, therefore nuclides with Z > 99 cannot be tagged.                                   |
| RRRRR   | specifies a reaction identifier for library interactions or a residual nuclide ZZAAA identifier for high-energy model interactions or a special designator. Some MCNP reaction numbers ( RRRRR ) of special designators have different meanings from ENDF reaction (MT) numbers. |

By default, a total over all specified bins is provided for the FU
special tally; add the NT parameter after the last specified bin to
suppress this total. A list of special cases for the CCCCCZZAAA.RRRRR FU
card entries appears later in this section.

If cell tagging is not desired, the CCCCC portion of the tag should be
omitted or, alternatively, set to ' 00000 '. In either case, tally
contributions will be accumulated for all cells for that FU bin,
provided the ZZAAA.RRRRR portion of the tag is satisfied. In the case of
particle production from electrons, which are material based (not
nuclide specific), the CCCCC input should be used to identify the cell
and the ZZAAA input should be set to ' 00000 '. The suffix RRRRR refers
to a standard or special ENDF reaction (MT) number for library
interactions. For example, ' 00102 ' stipulates (n, γ ) or, in the case
of high-energy model interactions, RRRRR refers to a residual nuclide
ZZAAA identifier (e.g., ' 06012 ' for 12 C).

In general, a zero input for any portion of the tag results in the sum
of all contributions related to the entry. For example, the tag '
0000092000.00000 ' will collect all tally contributions for which any
isotope of uranium ( Z = 92 ) produced the particle making the tally.
However, the tag ' 0000000000.00000 ' is reserved for elastic-scattered
particles. Note that each tally contribution is made only to the first
FU bin that satisfies the tag description (i.e., those that have not
already been tallied). If no appropriate FU bin is found, the tally
contribution is not made; however a special 'everything else' bini
(i.e., ' 1e10 ') can be specified to collect any portion of the tally
that falls into no other bin. When the 'everything else' bin is used,
then the user is assured that the 'user-bin total' bin will reproduce
the original tally as if the FTn TAG option had not been used.

Special designations for CCCCCZZAAA :

- -0000000001 or -1 source particle tag for all cells

| - CCCCC 00001       | source (i.e., un-collided) particle tag for cell CCCCC   |
|---------------------|----------------------------------------------------------|
| 0000000000 or 0     | elastic-scattered particle tag                           |
| 10000000000 or 1e10 | everything else tag                                      |

Photon tally special designations for ZZAAA.RRRRR :

| 00000.00001   | bremsstrahlung from electrons                            |
|---------------|----------------------------------------------------------|
| ZZ 000.00003  | fluorescence from nuclide ZZ                             |
| 00000.00003   | K x-rays from electrons                                  |
| 00000.00004   | annihilation photons from electron-positron interactions |
| ZZ 000.00005  | Compton photons from nuclide ZZ                          |
| ZZAAA .00006  | muonic x-rays from nuclide ZZAAA                         |
| 00000.00007   | Cerenkov photons                                         |

Electron tally special designations for ZZAAA.RRRRR :

| ZZ 000.00001   | photoelectric from nuclide ZZ   |
|----------------|---------------------------------|
| ZZ 000.00003   | Compton recoil from nuclide ZZ  |
| ZZ 000.00004   | pair production from nuclide ZZ |
| ZZ 000.00005   | Auger electron from nuclide ZZ  |
| 00000.00005    | Auger electron from electrons   |
| 00000.00006    | knock-on electrons              |

Neutron and photon tally special designations for ZZAAA.RRRRR :

ZZAAA .99999

delayed particles from fission of ZZAAA

The RRRRR reaction tag also includes all the MT reactions listed for
neutrons, but selecting RRRRR is complicated by the inconsistencies of
ENDF and other table data evaluations. For fission, RRRRR = 18 will not
always catch all fission reactions. For example, in 239 Pu RRRRR = 18 ,
but in 240 Pu RRRRR = 19 , 20, 21 and all three must be listed to catch
240 Pu fission. Likewise, RRRRR = 16 only tags (n,2n) reactions; RRRRR =
17 must be used to get (n,3n) reactions. And then there are the
exceptions. For example, photons from fission in 235 U have the tag
RRRRR = 3 , which is inelastic, and is also the tag of photons created
by (n,xn).

1

2

3

4

5

6

## 5.9.18.13.1 Example 1

```
1 F1:N 10 2 FT1 TAG 1 3 FU1 0000092235.00016 0000092235.00000 1e10
```

If an (n,2n) neutron that is produced from an interaction with 235 U
contributes to the F1 tally, then its contribution will be included only
in the first FU bin even though its tag also will satisfy the criteria
for the 2nd FU bin. Thus, the order of the FU bin tags is important for
segregating the tally. Note that neutrons produced by some other
reaction with 235 U will be placed in the 2nd FU bin and neutrons
produced by reactions with other target nuclides will be placed in the
last ('everything else') bin. The sum of these three bins should
preserve the value of the original F1 : n tally.

## 5.9.18.13.2 Example 2

| F1:P   | 1   |       1 | 1           | 1           |
|--------|-----|---------|-------------|-------------|
| FT1    | TAG |     1   | 1           | 1           |
| FU1    | 0.0 |  1001   | 01001.00000 |             |
|        |     | 26056   | 26056.00051 | 26056.00052 |
|        |     | 26056.2 | 26056.26053 | 26056.26054 |
|        |     | 26056   |             |             |

All elastic-scattered photons (i.e., coherent) will be put into the FU
'0.0' bin. All capture gammas from 1 H will be put into the 01001.00102
bin; all remaining gammas from 1 H interactions will be put into the
01001.00000 bin. All capture gammas from 56 Fe will go into the
26056.00102 bin; all (n,n ′ ) 1st level gammas will go into the
26056.00051 bin; all (n,n ′ ) 2nd level gammas will go into the
26056.00052 bin; all de-excitation gammas from the spallation of 56 Fe
into 52 Cr will go into the 26056.24052 bin; etc. All remaining gammas
produced from 56 Fe interactions will go into the 26056.00000 bin.

## 5.9.18.13.3 Example 3

```
F5:P 0 0 0 1 FT5 TAG 3 FU5 -1.0 0000106012.00005 0000106012.00000 0000026056.00102 0000026056.00000 0000000000.00051 10000000000.00000
```

In this case, all collided photons will retain their original creation
tag. All source photons will go into the -1 . 0 bin. All Compton photons
from 12 C in cell 1 will be put into the 2nd bin; all remaining photons
produced from interactions with 12 C in cell 1 will go into the 3rd bin.
All capture gammas from 56 Fe will go into the 4th bin; all remaining
photons/gammas produced from interactions with 56 Fe will go into the
5th bin. All (n,n ′ ) 1st level gammas will be put into the 6th bin, and
all remaining photons/gammas that were not included in any of the
previous bins will be placed in the last bin.

1

2

3

4

## 5.9.18.14 LET

The linear energy transfer ( LET ) special tally option allows track
length tallies to record flux as a function of stopping power instead of
energy. When the FTn LET option is specified, the values provided in the
energy bins are interpreted as stopping power values with units of
MeV/cm. This option can only be applied to charged particle tallies.

## 5.9.18.14.1 Example 1

| fc4   | Proton flux LET   |
|-------|-------------------|
| f4:h  | 77                |
| e4    | 1e-2 99ilog 6e4   |
| ft4   | LET               |

This example is a tally that records the proton flux in cell 77 for a
LET tally. The tally results are recorded in 100 bins of stopping power
from 0.01 to 60000 MeV/cm.

## 5.9.18.15 ROC nhb [ m ]

The ROC special tally option separates tallies into two components,
signal and noise. During a calculation, the signal and noise tally
values are saved for each specified batch of histories. These
distributions of tally values are formed into signal and noise
probability distribution functions (PDFs). Integration of the signal PDF
(labeled as the Probability of Detection, PD) is plotted as a function
of the integral of the noise PDF (labeled as the Probability of False
Alarm, PFA), resulting in the printed Receiver-Operator Characteristic
(ROC) curve. A table of the PDF values is provided in PRINT table 163 of
the MCNP output file.

To specify the 'signal' portion of a tally, use entries 1-8 on an
associated TF card; to specify the 'noise' portion, use TF entries 9-16.
The ROC keyword parameter nhb sets the number of histories per batch.
This parameter sets the 5th entry (the tally fluctuation chart
frequency) on the PRDMP card. The nhb value should represent the total
number of source particles emitted over the time interval of interest.
The npp value on the NPS card should be set to a multiple of nhb ; the
npp value will then be used to determine the number of sampled batches.
We recommend that npp should be 50-100 times the value of nhb . The
optional parameter m specifies the maximum number of batches that will
be kept and analyzed. The default value is 100. We recommend m be
greater than 50 and perhaps two times the number of batches planned,
even considering possible restarted calculations. This value cannot be
increased in a restarted-calculation input file. If there are multiple
tallies with ROC entries, the maximum m value is used. The WGT keyword
on the SDEF card should be set to the default value of unity.

## 5.9.18.15.1 Example 1

```
f1:n 1 t1 1e8 1e37 tf1 j j j j j j j 2 j j j j j j j 1 ft1 ROC 1000
```

1

2

3

4

In this example, tally F1 scores the current of neutrons crossing
surface 1. This tally is divided into two time bins, neutrons arriving
before 1 second (i.e., 10 8 shakes) and those arriving after 1 second
(i.e., 10 37 shakes). The TF card associates the second time bin as the
'signal' and the first as the 'noise.' The signal and noise currents are
accumulated for each batch of 1000 particle histories. The resulting
tally values are formed into signal and noise PDFs that are integrated
and plotted in PRINT table 163 as a ROC curve for this tally.

Another ROC curve example is provided in §10.2.5.9.

## 5.9.18.16 PDS c

This pre-collision estimator augments the post-collision next-event
estimator that has historically been used for point flux estimation in
MCNP6. The pre-collision next-event estimator includes the contribution
of all possible reactions before the collision isotope and resulting
reaction are sampled. This procedure has the advantage of providing an
improved expected estimate per collision, but with a significant
increase in computational costs per collision. This improved sampling
technique removes the requirement to suppress coherent scattering for
photon transport problems that include photon next-event estimators
[§2.4.4.2.5]. The sampling of all possible scattering reactions
generally provides an increase in the Figure of Merit (FOM) for most
photon problems. This increase in the FOM can be significant when the
contribution to a photon next-event estimator is primarily from forward
scattering. For most neutron problems there is not typically a large
increase in the FOM. However, for both photons and neutrons the pre-
collision next-event estimator increases the convergence rate as
measured by the time to pass MCNP6's ten statistical checks.

The single parameter, c , specifies how the sampling of the collision is
performed for the next-event estimator. If

| c = - 1   | Next-event estimator sampling is performed post-collision; only a single reaction and isotope is sampled (historic MCNP4 and MCNP5 behavior)                                      |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| c = 0     | Same as c = - 1 (DEFAULT)                                                                                                                                                         |
| c = 1     | Next-event estimator sampling is performed using post-collision sampling of the collision isotope and pre-collision sampling of all reaction channels. (Recommended for photons.) |
| c = 2     | Next-event estimator sampling is performed using pre-collision sampling of all collision isotopes and pre-collision sampling of all reaction channels.                            |

Recommendation: Using either PDS 1 or PDS 2 allows the user to perform
next-event estimator tallies with photon coherent scattering enabled.

For neutron next-event estimator tallies the user should perform scoping
calculations with PDS = -1 , 1 , and 2 . The user should check the 10
statistical tests of the three runs to assess which parameter provides
the best compromise between convergence and FOM. Using a pre-collision
estimator for neutrons will typically reduce the computational time
needed to pass the 10 statistical checks but result in a lower FOM.

## 5.9.18.16.1 Example 1

| f5p    | 100.0 50.0 25.0 0.0   | $ post-collision next-event estimator   |
|--------|-----------------------|-----------------------------------------|
| ft5    | pds -1                | $ F5 tally is post-collision            |
| c f15p | 100.0 50.0 25.0 0.0   | $ pre-collision next-event estimator    |
| ft15   | pds 1                 | $ F15 tally is pre-collision            |

1

2

In this example the pre-collision next-event estimator and the post-
collision next-event estimator are compared for a photon tally located
at x = 100 cm, y = 50 cm, and z = 25 cm.

## 5.9.18.17 FFT [ LKJI ]

A single parameter may follow the FFT keyword and an FU card is
required. The optional LKJI parameter toggles on/off the first-fission
treatment for the various physics packages, as explained below. The
related FU card segregates the tally into contributions according to
which fission occurred first. FU entries must be target identifiers
[§1.2.2] in ZAID form of fissionable nuclides. Additionally, an FU entry
of '0' should be included to score all contributions that are not
associated with any other FU bin, an FU entry of '16' will score (n,xn)
reactions instead of fission if they occur before any fission, and an
entry of '18' will score first fissions from any nuclide that is not
listed on the FU card. The bins may be entered in any order. The LKJI
parameter combines four binary toggles that specify which physics
packages should be included with the FFT treatment, such that:

| L = 0 / 1   | Omit/include neutron and photon-induced fissions treated by model physics      |
|-------------|--------------------------------------------------------------------------------|
| K = 0 / 1   | Omit/include neutron spontaneous fissions ( PAR = SF source particles)         |
| J = 0 / 1   | Omit/include photon-induced fissions treated by library physics                |
| I = 0 / 1   | Omit/include neutron-induced fissions treated by library physics ( E < 20 MeV) |

The default value for LKJI is 0001 , which is equivalent to 1 and is the
default action if LKJI is omitted. To turn on the full FFT treatment,
one would specify LKJI = 1111 .

Cell flagging ( CF card) and surface tally segmenting ( FS card) have
somewhat different meanings when the FFT special tally treatment is
used. Unlike the standard tally segmenting, in which the segment
identifies where the score is made, FFT tally segmenting identifies
where the first fission occurs. Unlike the standard tally flagging,
which flags cells through which the track has passed before scoring, FFT
cell flagging flags cells in which the first fission occurred. Cell
flagging and surface segmenting work for cells and surfaces at the
lowest level so when FFT is specified, these lowest-level cells/surfaces
will be the location of the first fission. If a CF card is used with the
FFT option on any tally, then the use of a CF card without the FFT
option is prohibited on any other tally, and the related CF card is
ignored and a warning is issued.

## 5.9.18.17.1 Example 1

| FT1   |   FFT |
|-------|-------|
| FU1   | 92238 |

If an (n,xn) reaction occurs before a fission, then the 16 bin records a
score. If the particle has its first fission in a listed nuclide (U-235,
U-238, Pu-239, Pu-241), then that nuclide bin records a score provided
16 has no score. If the first fission is not a listed nuclide, the 18
bin records a score provided 16 has no score. The 0 bin records a score
if no other bin has a score.

## 5.9.18.18 COM t a

The FT8 COM tally option produces a Compton image stored in an
associated FIR radiography tally t using algorithm a (optional,
currently there is one algorithm so a = 1 ). The Compton image is formed
from a FT8 PHL specification of dual-region coincidences of planar
lattice tallies. At the end of each particle history,
Compton/photoelectric energy deposition in the front/back of these dual-
panel detectors is used to create a circular 'image' of the incident
photon on a specified image plane. The FT8 PHL enhancement is used to
obtain coincidences of front-panel energy deposition with back-panel
energy deposition, on a voxel-by-voxel (or element-by-element) basis.
For example, if the front-panel detector consists of a 5 × 5 lattice and
the back-panel detector consists of a 10 × 10 lattice, then the FT 8 PHL
option produces coincident pulses for 25 × 100 = 2500 voxel
combinations. The Compton electron energy deposition scored in a front-
panel voxel ( E f ) is correlated to the photoelectric energy deposition
in a back-panel voxel ( E b ), via the Compton equation, to produce the
Compton angle of scatter and thus determine a conical angle of
incidence. The form of the Compton equation that is used to obtain the
conical angle of incidence is

<!-- formula-not-decoded -->

where m e is taken as 0.511 MeV.

Restrictions on E f and E b include: (1) E f &lt; E b , and (2) E f &gt; E ft
and E b &lt; E bt , where E ft and E bt are threshold energies set by the
user on the corresponding E8 and FU8 cards. The first of these is
required to formulate a backward conical image (and helps ensure a
Compton/photoelectric reaction occurred), while the latter is needed to
reduce image clutter from voxel leakage (electron escape,
bremsstrahlung, etc.). The FT8 COM processing algorithm is currently
quite simple in that it takes the center-point of the front-panel voxel
and that of the back-panel voxel to form a line which is then
intersected with the image plane (at point P ). Using the equation
above, a radial distance from point P is determined and scores are made
to various grid elements intersected by the circle about P (see Fig.
5.14). A simple algorithm is used, based on the size of the grid
elements, to determine the number of sample points to score around the
circle. A pulse of the source weight is scored in each image-plane grid
element that overlaps a circular sample point.

An associated FIR radiography tally will be used to set up the image
grid, with corresponding tally segment ( FS card) and cosine ( C card)
bins.

The COM option is allowed only on F8 tallies and must be used with a
corresponding dual-region PHL option. The tallies specified with the PHL
option must involve multi-element lattices and use the special F-bin
descriptor of '0'. While the lattices in the two regions can differ in
size and number of elements, tallies specified within a region must
tally over the same lattice cell and elements (but can include
contributions from different particle types). This feature fully
supports repeated-structures geometries.

## 5.9.18.18.1 Example 1

The example shown in Listing 5.58 has a 2-MeV isotropic photon source
located at ( -5 , 3 , 3) , which is approximately 4 cm from two 1 × 5 ×
5 silicon panels, with the back panel 3 cm behind the front with the
front panel centered at ( -1 , 0 , 0) . This arrangement is shown in
Fig. 5.15.

The silicon voxels are 2 × 2 × 2 cm, making the panels 2 × 10 × 10 cm
overall in size. The image plane is coincident with the source location,
so it is also approximately 4 cm from the front panel detector. The size
of the image plane is 20 cm in each direction, with 10 grid elements
along these s and t axes [§5.9.1.3.3]. The energy thresholds are set to
0.2 MeV on the E8 and FU8 cards. The TF8 card uses the 2nd user and
energy bins for the TFC, and it is the values in these bins that are
used in solving the Compton image equation, Eq. (5.48).

Figure 5.14: Diagram of a Compton imaging detector, along with a circular sample on the image plane.

<!-- image -->

Figure 5.15: Geometry plot of Compton Imaging Tally Example, showing lattice indices for the front and back detector panels.

<!-- image -->

1

2

3

4

```
1 2-MeV photons into Si grid 2 1 1 -2.3 -1 lat=1 u=1 imp:p=1 3 fill=0:0 -2:2 -2:2 1 24r 4 2 1 -2.3 -2 lat=1 u=2 imp:p=1 5 fill=0:0 -2:2 -2:2 2 24r 6 3 0 -3 fill=1 imp:p=1 7 4 0 -4 fill=2 imp:p=1 8 5 0 -5 4 3 imp:p=1 9 6 0 5 imp:p=0 10 11 1 rpp -1 1 -1 1 -1 1 12 2 rpp 4 6 -1 1 -1 1 13 3 rpp -1 1 -5 5 -5 5 14 4 rpp 4 6 -5 5 -5 5 15 5 so 100 16 17 mode p e 18 sdef par=p pos=-5 3 3 erg=2 19 m1 14028 1 20 phys:e 2j 1 $ Turn off bremsstrahlung 21 cut:p,e 2j 0 0 $ Analog capture 22 c 23 fir5:p -5 0 0 0 0 0 0 1 1 1 24 fs5 -10 9i 10 25 c5 -10 9i 10 26 c 27 f16:e (1<1[0:0 -2:2 -2:2]<3) 28 f26:e (2<2[0:0 -2:2 -2:2]<4) 29 c 30 f8:e 1 31 ft8 PHL 1 16 0 $ Region 1 32 1 26 0 $ Region 2 33 0 34 COM 5 1 35 e8 0.2 100 NT 36 fu8 0.2 100 NT 37 tf8 j j 2 j j j 2 j 38 print 39 rand gen=2 seed=12345 40 nps 1e6 41 prdmp 2j 1
```

Listing 5.58: example\_compton\_img.mcnp.inp.txt

Figure 5.16 presents the corresponding Compton image, which can be
produced using the commands shown in Listing 5.59.

```
tally 5 free sc contour noline file end end
```

Listing 5.59: example\_compton\_img.mcnp.comin.txt

## 5.9.18.19 SPM na

The SPM special tally option generates collision exit energy-angle
scatter probability matrices ( SPM ) averaged over particle interactions
within each incident FU energy bin. The FU bins are automatically
created from,

Figure 5.16: Compton image for Compton Imaging Tally Example, using a 20 × 20 -cm image plane with 10 × 10 grid elements.

<!-- image -->

Table 5.22: Description of the Multiplier Bins for the MGC FT Option.

|   Bin # | Units            | Values                                                 |
|---------|------------------|--------------------------------------------------------|
|       1 | n / ( cm 2 · s ) | Flux (used as a divisor for the other bins)            |
|       2 | sh/cm            | Inverse velocity                                       |
|       3 | barns            | Total cross section                                    |
|       4 | barns            | Absorption cross section                               |
|       5 | barns            | Fission cross section                                  |
|       6 | barns            | Total or prompt fission production cross section       |
|       7 | barns            | Delayed fission production cross section               |
|       8 | barns            | Fission heat production cross section                  |
|       9 | barns            | Capture cross section (Absorption + Fission)           |
|      10 | barns            | Scatter cross section [Total - (Absorption + Fission)] |

and are identical to, the bins specified on a related E card. This tally
option can only be used with F4 tallies. The required na entry specifies
the number of uniform cosine bins that will be generated on the related
C card (from -1 to 1). This option requires analog transport, and the
SPM s are tallied for each cell listed on the related F4 card. Fission
neutrons are omitted from the SPM, however, subsequent collisions after
fission are included. The SPMs are normalized to the number of
collisions contributing to that exit energy-angle SPM , thus the sum of
the E bins and C bins of each FU bin equals 1. Consider using the FQ
card with ' E C ' to get exit cosine bins listed horizontally in the
MCNP output file and exit energy bins listed vertically down the MCNP
output file for each SPM . SPM s are independent of the source
specification, although a poor choice in the source energy distribution
may result in poor SPM convergence or no SPM results for some incident
energies.

## 5.9.18.20 MGC fg

The MGC special tally option automatically generates ten FM multiplier
bins that tally the flux and nine flux-weighted quantities useful to
multigroup transport, using the energy bin structure specified on a
related E card. This tally option can only be used with F4 tallies. The
optional fg entry specifies microscopic cross-section units (barns) by
default (i.e., when unspecified or set to '0') or macroscopic units
(1/cm) when non-zero. For the tally results, the flux-weighted
quantities are divided by the flux values to produce multigroup cross
sections or other transport parameters. These FM bins are tallied for
each cell listed on the related F4 card, and a full description of each
bin is provided, as usual, in PRINT Table 30 of the MCNP output file,
along with a condensed description in the tally output tables.

The ten multiplier bins are listed in Table 5.22.

## 5.9.18.21 FNS nt

The FNS special tally option generates fission neutron spectra (FNS)
averaged over neutron induced fissions within each incident FU energy
bin. The FU user bins are automatically created from, and are identical
to, the bins specified on a related E card. This tally option can only
be used with F4 tallies. The optional nt entry specifies the number of
uniform half-life bins (from 100 to 10 11 sh) that will be generated on
the related T card for prompt (1st bin) and delayed (remaining nt bins)
fission neutrons. A value of nt = 6 results in a prompt bin (100 sh) and
the standard six ENDF delayed half-life bins (with midpoints of 0 . 179
× 10 8 , 0 . 496 × 10 8 , 2 . 230 × 10 8 , 6 . 000 × 10 8 , 21 . 840 ×
10 8 , and 54 . 510 × 10 8 sh). If nt is not specified, a T card must be
used to list the prompt and delayed bin boundaries. This tally option
requires analog transport, and the FNS are tallied for each cell listed
on the related F4 card. For fixed-source problems, libraries and/or
models can be specified to generate the delayed neutrons (see ACT card),
while criticality problems only use libraries for delayed neutron
production.

## 5.9.18.22 LCS lo

The LCS special tally option generates Legendre coefficients for exit
energy-angle scatter probabilities over collisions within each incident
FU energy bin. The FU user bins are automatically created from, and are
identical to, the bins specified on a related E card. This tally option
can only be used with F4 tallies. The required lo entry specifies the
maximum Legendre order and thus the number of coefficients that will be
generated on the associated C card. Included in this tally are the
scatter bins' normalization factors (i.e., fraction of collisions
contributing to the related coefficients). The C bins are labeled as
0.00 (normalization factor), 1.00 (1st coeff.), 2.00 (2nd coeff.), etc.
These coefficients can be used in a Legendre polynomial expansion to
mathematically estimate, subject to truncation error, the scatter
distributions produced by the FT SPM option. This tally option requires
analog transport, and the Legendre coefficients are tallied for each
cell listed on the related F4 card. Fissions are not included as a
scatter event.

## 5.9.19 TF: Tally Fluctuation

This card specifies the bin for which the tally fluctuation chart
statistical information is calculated and the weight-window generator
results are optimized. In addition, two separate tally bins can be
specified to distinguish the 'signal' vs. 'noise' portions of a tally
for ROC curve generation (see special tally treatment FT ROC in
§5.9.18.15).

The TF card allows you to change the default bin for a given tally and
specify for which tally bin the chart and all the statistical analysis
output will be printed. The set of eight entries on a TF card correspond
(in order) to the list of bin indices for the eight dimensions of the
tally bins array. The order is fixed and not affected by an FQ card.

A helpful mnemonic suggested by Dr. Kris Ogren to remember the default
bin ordering is Fred Died Under Some Mysterious Circumstances Editing
Tallies-thanks Kris!

<!-- image -->

| Data-card Form 1: TF n if id iu is im ic ie it or Data-card Form 2: TF n if 1 id 1 iu 1 is 1 im 1 ic 1 ie 1 it 1 if 2 id 2 iu 2 is 2 im 2 ic 2 ie 2 it 2   | Data-card Form 1: TF n if id iu is im ic ie it or Data-card Form 2: TF n if 1 id 1 iu 1 is 1 im 1 ic 1 ie 1 it 1 if 2 id 2 iu 2 is 2 im 2 ic 2 ie 2 it 2   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                                                                                                                                          | Tally number. Restriction: n ≤ 99999999                                                                                                                    |
| if                                                                                                                                                         | The bin number of the cell, surface, or detector bin ( F -bin) on F card. (DEFAULT: if = 1 , first bin)                                                    |
| id                                                                                                                                                         | The bin number of the total, flagged, or un-collided flux ( D -bin). (DEFAULT: id = 1 , total flux)                                                        |
| iu                                                                                                                                                         | The bin number of the user bin ( U -bin). (DEFAULT: iu = last bin) ( 2 )                                                                                   |
| is                                                                                                                                                         | The bin number of the segment bin ( S -bin). (DEFAULT: is = last bin)                                                                                      |
| im                                                                                                                                                         | The bin number of the multiplier bin on FM card ( M -bin). DEFAULT: im = 1 , first bin)                                                                    |
| ic                                                                                                                                                         | The bin number of the cosine bin ( C -bin). (DEFAULT: ic = last bin)                                                                                       |
| ie                                                                                                                                                         | The bin number of the energy bin ( E -bin). (DEFAULT: ie = last bin)                                                                                       |
| it                                                                                                                                                         | The bin number of the time bin ( T -bin). (DEFAULT: it = last bin)                                                                                         |

Use: Whenever a particular tally bin is more important than the default
bin. Particularly useful in conjunction with the weight-window
generator. Also used to specify signal versus noise components of a ROC
curve.

1

1

## Details:

- 1 The second input format is used only with the FT n ROC tally option. In this case, the first 8 entries represent bins associated with the signal component while the second 8 entries identify the noise component [§5.9.18.15]. To support ROC curve generation, the entry format allows multiple bins to be specified for each entry: a single bin (e.g., 10), a range of bins (e.g., 10-12), a list of bins (e.g., 10, 11, 12), or a combination of these formats (e.g., 10-12,13,14). However, only the first bin listed in each entry is used for generating the TFC output, weight-window generation, and statistical analysis.
- 2 You may find the J feature useful to jump over last entries. Remember that totals are calculated for energy, time, and user bins (unless inhibited by using NT ), so that last for eight energy bins is 9. If one segmenting surface divides a cell or surface into two segments, last in that case is 2, unless T is used on the FS card, in which case last is 3. If there are no user bins or cosine bins, for example, last is 1 for each; last is never less than 1.

## 5.9.19.1 The Tally Fluctuation Chart

At the end of the output, one chart for each tally is printed to give an
indication of tally fluctuations; that is, how well the tally has
converged. The tally mean, relative error, variance of the variance,
Pareto slope [§2.6.8.7], and figure of merit (FOM = R -2 T -1 ) , where
R is the relative error printed with the tally and T is computer time in
minutes) are printed as functions of the number of histories run. The
FOM should be roughly constant. The TF n card determines for which bin
in tally n the fluctuations are printed. It also determines which tally
bin is optimized by the weight-window generator ( WWE or WWT and WWG or
WWGT cards).

The mean printed in a chart will correspond to some number in the
regular tally print. If you have more than one surface listed on an F2
card, for example, the default chart will be for the first surface only;
charts can be obtained for all surfaces by having a separate tally for
each surface.

## 5.9.19.2 Example 1

Suppose an F2 tally has four surface entries, is segmented into two
segments (the segment plus everything else) by one segmenting surface,
and has eight energy bins. By default one chart will be produced for the
first surface listed, for the part outside the segment, and totaled over
energy. If we wish a chart for the fifth energy bin of the third surface
in the first segment, we would use

TF2 3 2J 1 2J 5

## 5.9.19.3 Example 2

TF2 3 2J 1 2J 5 J

In this example, statistics will be calculated based on the 3rd surface,
1st segment, and 5th energy bin provided in tally 2. Without this card,
statistics will be performed on the 1st surface, 1st segment, and the
total of all energy bins.
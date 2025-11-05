---
title: "Chapter 5.8 - Source Specification-focused Data Cards"
chapter: "5.8"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.8_Source_Specification-focused_Data_Cards.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

1

## 5.7.13 FIELD: Gravitational Field

The FIELD card was historically an undocumented feature in earlier MCNP
releases that allowed the user to model planetary gravitational effects
on neutrons, which results in their orbiting the planet. The theory and
equations used for this feature are documented in a paper by Feldman, et
al. [288]. This can be an important effect for low-energy (e.g.,
thermal) neutron detectors aboard orbiting spacecraft.

## /warning\_sign Caution

The gravitational field capability is not tested, has known issues, and
is being considered for deprecation for future versions of the MCNP6
code if there is no user interest in this capability. People interested
in this capability should send an email to mcnp\_help@lanl.gov.

| Data-card Form: FIELD KEYWORD = value(s)   | Data-card Form: FIELD KEYWORD = value(s)                                                                                                                                                                         |
|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| gcut = e                                   | Gravitational binding energy (eV) threshold. Below this energy, the gravitational field treatment is applied (DEFAULT: gcut = 0 . 653 ).                                                                         |
| gpar = p                                   | Particle type (limited to neutrons) (DEFAULT: gpar = 1 ).                                                                                                                                                        |
| grad = r                                   | Radius of planetary object (km) (DEFAULT: grad = 6 , 371 ).                                                                                                                                                      |
| gsur = s                                   | Required list of one or more surface numbers. When the gpar particle crosses the surface, it is assumed to orbit the planetary object and reenter the gsur surface at a later time, unless terminated via decay. |

Default: Applied to neutrons ( gpar = 1 ) with respect to the Earth's
radius ( grad = 6 , 371 ), and below Earth's gravitational binding
energy ( gcut = 0 . 653 ). The list of one or more surfaces ( gsur ) is
required.

Use: Optional.

## Details:

- 1 The orbiting particle reenters at the same location as they exit, thus this is really a partial reflection at surface gsur . Even though the particle would reenter at a different location, it is assumed that there is a uniform distribution of such reentering particles.

## 5.7.13.1 Example

The input card shown in Listing 5.39 contains the default keyword-value
options applied to neutrons as they cross surface gsur = 2 .

Listing 5.39: example\_field.mcnp.inp.txt

field gcut=0.653 gpar=1 grad=6371.0

```
gsur=2
```

## 5.8 Source Specification-focused Data Cards

Every MCNP problem has one of four sources:

1. General source ( SDEF card),
2. Surface source ( SSR card),
3. Criticality source ( KCODE card), or
4. User-supplied source.

All can use source distribution functions, specified on SI , SP , SB ,
and DS cards.

## 5.8.1 SDEF: General Source Definition

The specification of a source variable has one of the following three
forms:

1. A scalar or vector, in which a single, explicit value is given for the specified variable (e.g., CEL = 1 or POS = 0 0 6 ).
2. A distribution number, n , prefixed by a D , in which the specified source variable may have multiple values that will be sampled from distribution SI n . For example, CEL = D1 indicates that multiple cell numbers will appear on the SI1 card and will be sampled using probabilities entered on the associated SP1 card.
3. The name of another variable prefixed by an F , followed by a distribution number prefixed by a D . (For example., POS = FCEL = D1 indicates that the position specification will depend on the cell(s) specified on the SI1 card.) Only one level of dependence is allowed. Each distribution may be used for only one source variable. None of the position-related keywords (i.e., CEL , SUR , RAD , AXS , EXT , X , Y , Z , and CCC ) can be a dependent distribution of POS .

The above scheme translates into three levels of source description. The
first level exists when a source variable has an explicit or default
value (for example, a single energy) or a default distribution (for
example, an isotropic angular distribution). The second level occurs
when a source variable is given by a probability distribution. This
level requires the SI and/or SP cards. The third level occurs when a
variable depends on another variable. This level requires the DS card.

The MCNP code samples the source variables in an order set up according
to the needs of the particular problem. Each dependent variable must be
sampled after the variable it depends on has been sampled. If the value
of one variable influences the default value of another variable or the
way it is sampled, as SUR influences DIR , they need to be sampled in
the right order. The scheme used in the MCNP code to set up the order of
sampling is complicated and may not always work. If it fails, a message
will be printed. The fix in such instances may be to use explicit values
or distributions instead of depending on defaults.

The source variables SUR , VEC , NRM , and DIR are used to determine the
initial direction of source-particle flight. The direction of flight is
sampled with respect to the reference vector VEC , which can itself be
sampled from a distribution. The polar angle is the sampled value of the
variable DIR . The azimuthal angle is sampled uniformly in the range
from 0 ◦ to 360 ◦ . If VEC and DIR are not specified for a volume
distribution of position ( SUR = 0 ), an isotropic distribution of
direction is produced by default. If VEC is not specified for a
distribution on a surface ( SUR = 0 ), the vector normal to the surface,
with the sign determined by the

sign of NRM , is used by default. If DIR is not specified for a
distribution on a surface, the cosine distribution ( p ( DIR ) = 2 × DIR
, 0 &lt; DIR &lt; 1 ) is used by default. A biased distribution of DIR can be
used to make more source particles start in a direction toward the
tallying regions of the geometry. The exponential distribution function
( -31 , Table 5.15) is usually most appropriate for this.

The source variables SUR , POS , RAD , EXT , AXS , X , Y , Z , and CCC
are used in various combinations to determine the coordinates ( x, y, z
) of the starting positions of the source particles. With them you can
specify three different kinds of volume distributions and three
different kinds of distributions on surfaces. Degenerate versions of
those distributions provide line and point sources. More elaborate
distributions can be approximated by combining several simple
distributions, using the S option of the SI and DS cards.

A description of each SDEF keyword appears below. Following the card
description and its notes are more detailed discussions of volume and
surface source specification. Examples of the general source follow
discussion of the SI , SP , SB , and DS cards.

<!-- image -->

| Data-card Form:   | KEYWORD=value(s)                                                                                                                                                                                    |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CEL               | Cell number. DEFAULT: Determined from the position of the particle, and possibly the direction of the flight of the particle if the position is on a surface of a cell.                             |
| SUR               | Surface number ( 1 ). DEFAULT: SUR = 0 , which indicates a cell (volume) source. Always required when source points lie on the boundary (surface) of a cell.                                        |
| ERG               | Kinetic energy (MeV). ( 16 ) DEFAULT: ERG = 14                                                                                                                                                      |
| TME               | Time (shakes) ( 2 ). DEFAULT: TME = 0                                                                                                                                                               |
| DIR               | µ , the cosine of the angle between VEC and the particle's direction of flight. Azimuthal angle is always sampled uniformly in 0 ◦ to 360 ◦ ( 3 ). Defaults are                                     |
| DIR               | volume source µ is sampled uniformly in - 1 to 1 , i.e., the source is isotropic.                                                                                                                   |
| DIR               | surface source p ( µ ) = 2 µ in 0 to 1 , i.e., cosine distribution.)                                                                                                                                |
| VEC               | Reference vector for DIR in vector notation. DEFAULT for volume source: Required unless source is isotropic. DEFAULT for surface source: Vector normal to the surface with sign determined by NRM . |
| NRM               | Sign of the surface normal. DEFAULT: NRM = +1                                                                                                                                                       |
| POS               | Reference point for position sampling in vector notation. DEFAULT: POS = 0,0,0                                                                                                                      |
| RAD               | Radial distance of the position from POS or AXS . DEFAULT: RAD = 0                                                                                                                                  |
| EXT               | For a volume source is the distance from POS along AXS . For a surface source is the cosine of angle from AXS . DEFAULT: EXT = 0                                                                    |
| AXS               | Reference vector for EXT and RAD in vector notation. DEFAULT: No direction.                                                                                                                         |
| X                 | x coordinate of position. DEFAULT: X = 0                                                                                                                                                            |
| Y                 | y coordinate of position. DEFAULT: Y = 0                                                                                                                                                            |
| Z                 | z coordinate of position. DEFAULT: Z = 0                                                                                                                                                            |

CCC

ARA

WGT

TR

EFF

PAR

Cookie-cutter cell number. (

Area of surface.

,

) DEFAULT: no cookie-cutter cell.

4

5

Required only for direct contributions to point detectors from plane
surface source. DEFAULT: none

Particle weight (input as explicit value only). DEFAULT:

Source particle transformation number (

TR

=

DEFAULT: none.

)

(

transformations (

,

n

card(s) is required.

TR

). Corresponding

Rejection efficiency criterion for position sampling (input as explicit
value

8

) DEFAULT:

only).

(

=

0.01

EFF

Source particle type(s) by symbol or number (e.g.,

=

=

9

PAR

PAR

H

For a complete list of particle types, see Table 4.3.

sampling multiple particle types.

15

Use a distribution for

To specify a particular heavy ion as a source particle, set or

PAR

identifier [§1.2.2]. All formats supported. Metastable states are
ignored.

To sample cosmic particles, if

PAR

[-]CR

PAR

PAR

PAR

PAR

PAR

the source is a combination of all cosmic particles

C1001

the source contains cosmic protons only

C2004

the source contains cosmic alphas only the source contains cosmic
nitrogen only

the source contains cosmic silicon only the source contains cosmic iron
only

=

=

=

=

=

=

or

[-]CH

[-]CA

or

PAR

PAR

[-]C7014

[-]C14028

[-]C26056

When the negative sign is omitted from these options, the SDEF WGT
keyword (i.e., source normalization) is set to the integral 2 π flux
obtained from the Castagnoli and Lal analytic equation ([289], as
corrected by [290]). If the cosmic particle designator is preceded by a
negative sign, then the particle weight normalization only considers the
SDEF WGT information provided by the user.

To sample background particles ( 9 ), if

```
PAR = [-]BG the background is a combination of all background particles (currently limited to neutrons and gammas) PAR = [-]BN the background contains neutrons only PAR = [-]BP the background contains gammas only
```

If the negative sign is omitted, the SDEF WGT keyword (i.e., source
normalization) is multiplied by values contained in the BACKGROUND.dat
file. If the negative sign is included, then the source normalization is
taken only from the SDEF WGT keyword.

To sample spontaneous fission [§5.8.1.7] if

PAR

=

SF

normalize summary and tally information by the number of spontaneous-
fission neutrons.

=

=

to a target

D

n

=

TR

=

WGT

1

) or distribution of

6

).

7

(

)

|           | PAR = -SF                                                                                                                                                                                                                                                                                                                                                                            | normalize summary and tally information by the number of histories (generally, the number of spontaneous fissions).                                                                                                                                                                                                                                                                  |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|           | To sample spontaneous neutrons:                                                                                                                                                                                                                                                                                                                                                      | To sample spontaneous neutrons:                                                                                                                                                                                                                                                                                                                                                      |
|           | PAR = SN                                                                                                                                                                                                                                                                                                                                                                             | decay neutrons will be created based on the relative activities of the unstable isotopes in the material(s) located at the source location(s).                                                                                                                                                                                                                                       |
|           | To sample spontaneous photons:                                                                                                                                                                                                                                                                                                                                                       | To sample spontaneous photons:                                                                                                                                                                                                                                                                                                                                                       |
|           | PAR = SP                                                                                                                                                                                                                                                                                                                                                                             | decay gammas will be created based on the relative activities of the unstable isotopes in the material(s) located at the source location(s).                                                                                                                                                                                                                                         |
|           | To sample spontaneous betas:                                                                                                                                                                                                                                                                                                                                                         | To sample spontaneous betas:                                                                                                                                                                                                                                                                                                                                                         |
|           | PAR = SB                                                                                                                                                                                                                                                                                                                                                                             | decay betas will be created based on the relative activities of the unstable isotopes in the material(s) located at the source location(s).                                                                                                                                                                                                                                          |
|           | To sample spontaneous positrons:                                                                                                                                                                                                                                                                                                                                                     | To sample spontaneous positrons:                                                                                                                                                                                                                                                                                                                                                     |
|           | PAR = ST                                                                                                                                                                                                                                                                                                                                                                             | decay betas will be created based on the relative activities of the unstable isotopes in the material(s) located at the source location(s).                                                                                                                                                                                                                                          |
|           | To sample spontaneous alphas:                                                                                                                                                                                                                                                                                                                                                        | To sample spontaneous alphas:                                                                                                                                                                                                                                                                                                                                                        |
|           | PAR = SA                                                                                                                                                                                                                                                                                                                                                                             | decay alphas will be created based on the relative activities of the unstable isotopes in the material(s) located at the source location(s).                                                                                                                                                                                                                                         |
|           | To sample all-particle spontaneous decay:                                                                                                                                                                                                                                                                                                                                            | To sample all-particle spontaneous decay:                                                                                                                                                                                                                                                                                                                                            |
|           | PAR = SD                                                                                                                                                                                                                                                                                                                                                                             | all decay particles ( SN , SP , SB , SA , ST ) will be created based on the relative activities of the unstable isotopes in the material(s) located at the source location(s). Decay particle types that are missing from the MODE card will be omitted (with a related warning message)                                                                                             |
|           | To specify the decay particles from a particular heavy ion as the source, set PAR to a target identifier corresponding to the ion, and set the energy of the ion to zero ( ERG = 0 . 0 ). Requires that heavy ions ( # ) be specified on the MODE card. DEFAULT: If no MODE card, PAR = N . DEFAULT: If MODE card in INP file, lowest IPT number or symbol represented on MODE card. | To specify the decay particles from a particular heavy ion as the source, set PAR to a target identifier corresponding to the ion, and set the energy of the ion to zero ( ERG = 0 . 0 ). Requires that heavy ions ( # ) be specified on the MODE card. DEFAULT: If no MODE card, PAR = N . DEFAULT: If MODE card in INP file, lowest IPT number or symbol represented on MODE card. |
| DAT m d y | Date to use for cosmic-ray ( PAR = CR , CH , CA ) and background ( PAR = BG , BN , BP ) sources ( 10 ):                                                                                                                                                                                                                                                                              | Date to use for cosmic-ray ( PAR = CR , CH , CA ) and background ( PAR = BG , BN , BP ) sources ( 10 ):                                                                                                                                                                                                                                                                              |
|           | m                                                                                                                                                                                                                                                                                                                                                                                    | An integer value representing the month of the year ( 1 ≤ m ≤ 12 )                                                                                                                                                                                                                                                                                                                   |
|           | d                                                                                                                                                                                                                                                                                                                                                                                    | An integer value representing the day of the month ( 1 ≤ d ≤ 31 )                                                                                                                                                                                                                                                                                                                    |
|           | y                                                                                                                                                                                                                                                                                                                                                                                    | A 4-digit integer representing the year                                                                                                                                                                                                                                                                                                                                              |

| LOC lat lng alt   | Location of cosmic particle source ( 11 ):   | Location of cosmic particle source ( 11 ):                                                                                                                               |
|-------------------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                   | lat                                          | latitude ( - 90 ≤ lat ≤ 90 , relative to equator; negative values are south of the equator and positive values are north of the equator)                                 |
|                   | lng                                          | longitude ( - 180 ≤ lat ≤ 180 , relative to Greenwich, UK; negative values are west longitude and positive values are east longitude)                                    |
|                   | alt                                          | altitude in km of cosmic particles when PAR = CR , CH , CA (DEFAULT: alt = 65 . 0 km), or elevation in km of the background source when PAR = BG , BN , BP (no default). |
| BEM exn eyn bml   | Beam emittance parameters ( 12 ):            | Beam emittance parameters ( 12 ):                                                                                                                                        |
|                   | exn                                          | normalized beam emittance parameter, ε nx , for phase-plane coordinates x,x ′ ( π -cm-radians)                                                                           |
|                   | eyn                                          | normalized beam emittance parameter, ε ny , for phase-plane coordinates y, y ′ ( π -cm-radians)                                                                          |
|                   | bml                                          | distance from the aperture to the spot, L (cm)                                                                                                                           |
|                   | DEFAULT: none                                | DEFAULT: none                                                                                                                                                            |
| BAP ba1 ba2 u     | Beam aperture parameters ( 13 ):             | Beam aperture parameters ( 13 ):                                                                                                                                         |
|                   | ba1                                          | beam aperture half-width in the x transverse direction, x 0 (cm)                                                                                                         |
|                   | ba2                                          | beam aperture half-width in the y transverse direction, y 0 (cm)                                                                                                         |
|                   | u                                            | unused, but must be set to an arbitrary value                                                                                                                            |
|                   | DEFAULT: none                                | DEFAULT: none                                                                                                                                                            |

Default: Isotropic point source at position = (0 , 0 , 0) , time = 0 ,
energy = 14 MeV, and particle weight = 1 .

Use: Required for problems using the general source. Optional for
problems using the criticality source. Reminder: an equals sign ( = )
following a keyword is optional.

## Details:

- 1 If the source location is on any surface (including 'extended' surfaces of macrobodies) used to describe the cell that contains that source, the SUR keyword must be used. A source can lie on an extended surface used to describe any other cell of the problem.
- 2 Emitted source decay gammas are assumed to arise from instantaneous activity of a large pool of decaying isotopes; time behavior is defined by the TME keyword. If an isotope emits multiple gamma lines, the emissions will not necessarily be correlated. Isotopes with half-lives longer than 10 18 seconds ( ∼ 3 . 17 × 10 10 years) are treated as stable. When the decay gammas of a heavy ion are specified as the source, PRINT Table 110 of the output file will list the sampled heavy-ion isotopes but not the created gamma lines.

- 3 Discrete values of DIR are allowed. DIR = 1 gives a mono-directional source in the direction of VEC . This is sometimes useful as an approximation to an actual source that is at a large distance from the geometry of the problem. In most cases discrete values of DIR will prevent direct contributions to point detectors from being scored. The direct contribution will be scored only if the source is on a plane surface, is sampled uniformly in area within a circle (using RAD sampled from SP -21 1 ), VEC is perpendicular to the surface (the default), and DIR = 1 . A cookie-cutter cell is allowed and a value of ARA is necessary. Discrete values of DIR with DXTRAN are generally wrong because p ( µ ) = 0 . 5 is assumed.
- 4 Cookie-cutter rejection is available for both cell and surface sources. If CCC is present, the sampled position is accepted if it is within cell CCC and is resampled if it is not. It is recommended that cookie-cutter cells be bounded by surfaces used for no other purpose in the problem and that the cookie-cutter cell cards appear at the end of the list of cell cards. Also, keep the cookie-cutter cell as simple as possible. For example, for a surface source, the intersection of the cookie-cutter cell with the source surface is what matters. For a plane surface source, an infinitely long cell of uniform cross section bounded by planes and cylinders is usually adequate.

## 5 /warning\_sign Caution

The combination of either CEL or CCC rejection with biased sampling of
the position is nearly always an unfair game. If the user employs this
combination, they must ensure that the game is fair; the MCNP code
cannot detect this error. To accomplish this, the source weight needs to
be multiplied by the ratio of the biased acceptance probability to the
unbiased acceptance probability (discussed in [291]).

- 6 A general transformation of the generated source may be specified with a single transformation TR = n or with a distribution of transformations TR = D m . In either case, all SDEF parameters relating to particle position or direction are interpreted as being in an auxiliary coordinate system in which the source specification is simpler. A general transformation is applied to a source particle after its coordinates and direction cosines have been determined in the auxiliary coordinate system. Particle coordinates are modified by both rotation and translation, while direction cosines are modified only by rotation. The source after transformation is treated as a volume source (i.e., surface number not defined); the cell for the source particle is determined after transformation. ( SUR and CEL are used only in the initial generation procedure). To avoid the possibility of lost particles, do not place the transformed source exactly on a surface of the physical geometry. With the form TR = n , a transformation card TR n must be specified. With the form TR = D m , in addition to the TR cards, the user must provide SI m , SP m , and possibly SB m cards. If a distribution of transformations is specified, the option parameter on the corresponding SI m card must be L . The option parameter on the SP m and SB m cards may be blank, D , or C .
- 7 Sources may be translated to different locations with the TR option. For example, the source transformation capability allows the user to rotate the direction of an accelerator beam or move the entire beam of particles in space. In addition, this capability is useful for setting up the source as an accelerator beam and then using the translation as a distribution to repeat the accelerator source at different locations and orientations. The TR option can be dependent on other source variables. For example, the particle type can depend on the translated source location:

1

1

SDEF CEL=FTR=D3 PAR=FTR=D1 TR=D2

or the translated source location can be a dependent distribution
function of cell:

| SDEF   | CEL=D2   | TR=FCEL=D5   |
|--------|----------|--------------|

- 8 The efficiency criterion EFF applies to both CCC and CEL rejection. If in any source cell or cookie-cutter cell the acceptance rate is too low (the default value of EFF is 0 . 01 ), the problem is terminated for inefficiency. To increase efficiency, the user is encouraged to revise the source description. If a source efficiency lower than 0.01 is unavoidable, specify a lower value for EFF .
- 9 The BG , BN , and BP options require that the user:
- (a) properly normalize the source in a spherical volume ( WGT = sphere surface area / 3 . 0 ), cylindrical volume ( WGT = cylindrical surface area / 3 . 4 ), cube volume ( WGT = cube surface area / 3 . 7 ), spherical surface ( WGT = πr 2 ), or some other enclosed surface ( WGT set to a central cell tally that has unit flux);
- (b) use the appropriate SDEF keywords to specify an isotropic uniform spatial distribution within these volumes or a cosine-weighted uniform distribution on any enclosing surface;
- (c) ensure that the background source volume is large compared to the geometry of interest (i.e., a radius or diameter that is 10 times that of the interior geometry); and
- (d) ensure that the BACKGROUND.dat file is in the local directory or in the DATAPATH directory. When the ' -' sign is omitted from these options, the WGT normalization will be further modified by the neutron and/or gamma flux normalization provided in the BACKGROUND.dat file, as well as being multiplied by the neutron/cosmic-photon elevation scaling factor [292]. The elevation scaling is only performed when the LOC elevation (3rd entry) differs from that of the selected BACKGROUND.dat grid-point elevation. This scaling will be omitted when the LOC elevation is specified as ' -1 ' or when the grid-point location is over seawater. These background source options require use of the LOC keyword and the sampling of this source ignores any specification for the ERG keyword. The LOC keyword identifies the normalization and energy spectrum to be sampled from the BACKGROUND.dat file.
- 10 The DAT keyword is used with the PAR = BG , BN , BP option to scale the background fluxes from the date specified in the BACKGROUND.dat file to the date specified by the DAT keyword. It can be used with the PAR = BG , BN , BP option when the cosmic source is intended for use within the Earth's atmosphere (in which case solar modulation effects are included). When the keyword DAT specifies a date between 1936 and 2014, linear interpolation of the yearly solar modulation values determines the appropriate modulation. Specified dates prior to 1936 or after 2014 use a sine-wave fit to approximate the solar modulation based on the measured data available for 1936-2014.
- 11 The keyword LOC is used only the PAR = CR , CH , CA , BG , BN , or BP options and should be specified when the cosmic or background source is intended for use within the Earth's atmosphere. Omission of the LOC keyword with the PAR = CR , CH , or CA option provides a cosmic source appropriate for interplanetary analysis. The 47th entry on the DBCN card can be used to switch between the default Clem formulation [293] and the Lal formation [289]. When the LOC keyword is used, the SKYMAP.dat file must be available in the local directory or in the DATAPATH directory. The sky map data file contains rigidity data on an approximate 5 ◦ latitude resolution (non-uniform spacing) and 20 ◦ longitude resolution (uniform spacing). Based on the LOC keyword, the algorithm uses a closest-match approach, first finding the closest longitude match followed by the closest latitude match. Fractional values are allowed after the LOC keyword-however, these are converted to the nearest integer degree for comparison to the sky map data. The PAR = CR , CH , CA option will automatically include heavy ions if they are included on the MODE card, unless the Lal source is specified.
- 12 The PAR = SD , SN , SP , SB , ST , SA , and target identifier (with ERG = 0 ) options require time integration of daughter production at each level within a decay chain. This is facilitated by setting all decay constants to unity and uniformly spacing all time bins within 20 s (or ≈ 20 decay levels), which will include all decay particle production within most decay chains (i.e., an equilibrium production). The user can adjust the integration time, and thus the number of decay levels, by modifying the 55th entry on the DBCN card. For example, setting this to ≈ 1 . 0 s will result in daughter production and related decay particle production from just the precursor. If long-lived radionuclides are included (half life &lt; 1 . 5768 × 10 16 s) the user must increase the 10th entry on the DBCN card to obtain related decay particle production. This will also increase the fidelity of the time integration by increasing the number of time steps from 99 to 234.

<!-- image -->

x

Figure 5.7: Locating and aiming a beam in the MCNP code involves a
transformation from local ( x, y, z ) to global ( x G , y G , z G )
coordinates. The beam aperture is located in the local-coordinate x, y
plane at the entrance to the drift region ( z = 0 ) at position P (' POS
'). The beam envelope is aligned in the direction A (' AXS ') parallel
to the + z local-coordinate direction with the azimuthal orientation
given by V (' VEC '). Particle emission is in the direction Ω at the
local-coordinate position r (the global position R ) as determined by
beam parameters and Monte Carlo sampling.

- 13 In a multiple-source-particle problem, the 'energy per source particle' given in the summary tables is normalized to the source particle weight for each source particle type. If the particle type is not a source particle (listed on the MODE card, but not on SDEF ), then the 'energy per source particle' is normalized to the source particle weight of the lowest particle type.
- 14 To simplify the description of the beam parameters BEM and BAP , the beam is referenced to the z axis and the aperture is described as if it lies in the x, y plane. Other SDEF keywords, namely POS , AXS , and VEC , are employed to describe the location and orientation of the beam. These three keywords specify the center of the aperture, the beam direction, and the azimuthal orientation of the beam, respectively. The Fig. 5.7 caption explains further the keyword relationships.
- 15 In the MCNP code, version 5, the specification of PAR = 4 would result in a positron. However, in the MCNP code, version 6, PAR = 4 indicates a negative muon.
- 16 If there is a negative igm on the MGOPT card, which indicates a special electron-photon multigroup problem, ERG on the SDEF card is interpreted as an energy group number, which is an integer.

## 5.8.1.1 Volume Source Specification

The three volume distributions are Cartesian, spherical, and
cylindrical. A volume distribution can be used in combination with the
CEL or CCC keywords to sample uniformly throughout the interior of a
cell. A Cartesian, spherical, or cylindrical region that completely
contains a cell is specified and is sampled uniformly in volume. If the
sampled point is found to be inside the cell, it is accepted. Otherwise
it is rejected and another point is sampled. If you use this technique,
you must make sure that the sampling region really does contain every
part of the cell because the MCNP code has no way of checking for this.
Cookie-cutter ( CCC ) rejection can be used instead of or in combination
with CEL rejection.

A Cartesian volume distribution is specified with the keywords X , Y ,
and Z . A degenerate case of the Cartesian distribution, in which the
three variables are constants, defines a point source. A single point
source can be specified easily by providing values of X , Y , and Z on
the SDEF card. If several source points need to be specified, it is
usually easier to use a degenerate spherical distribution for each
point. Other degenerate cases of the Cartesian distribution are a line
source and a rectangular plane source.

Figure 5.8: Volumetric Sampling Source-parameter Arrangements

<!-- image -->

A Cartesian distribution is an efficient shape for the CEL rejection
technique when the cell is approximately rectangular. It is much better
than a cylindrical distribution when the cell is a long thin slab. The
Cartesian distribution is limited in that the faces can only be
perpendicular to the coordinate axes.

A spherical volume distribution is specified with the keywords POS and
RAD as shown in Fig. 5.8a. The keywords X , Y , Z , and AXS must not be
specified or the distribution will be assumed to be Cartesian or
cylindrical. The sampled value of the vector POS defines the center of
the sphere. The sampled value of RAD defines the distance from the
center of the sphere to the position of the particle. The position is
then sampled uniformly on the surface of the sphere of radius RAD .
Uniform sampling in volume is obtained if the distribution of RAD is a
power law with a = 2 , which is the default case. If RAD is not
specified, the default is zero. This is useful because it specifies a
point source at the position POS . A distribution for POS , with an L on
the SI card, is the easiest way to specify a set of point sources in a
problem.

A common use of the spherical volume distribution is to sample uniformly
in the volume between two concentric spherical surfaces. The two radii
are specified on the SI card for RAD and the effect of an SP n -21 2
card is obtained by default.

A cylindrical volume distribution is specified with the keywords POS ,
AXS , RAD , and EXT as shown in Fig. 5.8b. The axis of the cylinder
passes through the point POS in the direction AXS . The position of the
particles is sampled uniformly on a circle whose radius is the sampled
value of RAD , centered on the axis of the cylinder. The circle lies in
a plane perpendicular to AXS at a distance from POS which is the sampled
value of EXT . A useful degenerate case is EXT = 0 , which provides a
source with circular symmetry on a plane (i.e., a thin disk source).

A common use of the cylindrical distribution is to sample uniformly in
volume within a cylindrical shell. The distances of the ends of the
cylinder from POS are entered on the SI n card for EXT and the inner and
outer radii are entered on the SI n card for RAD . Uniform sampling
between the two values of EXT and power law sampling between the two
values of RAD , with a = 1 which gives sampling uniform in volume, are
provided by default.

The reason for using the a = 2 and a = 1 as the power-law parameters on
the radial SP cards for spheres and cylinders, respectively, leading to
quadratic and linear radial sampling is because of the need to sample
the radial position proportional to differential volume. That is, for a
sphere, the volume is defined as V = 4 πr 3 / 3 so dV / d r = 4 πr 2 ∝ r
2 . Similarly, for cylinders, the volume is V = πr 2 h so d V/ d r = 2
πrh ∝ r , where the sampling along the extent of the cylinder based on
its height, h , is constant (i.e., d V/ d h = πr 2 , which

Figure 5.9: Volumetrically nonuniform (top) versus volumetrically uniform (bottom) radial sampling for spheres (left) and cylinders (right).

<!-- image -->

is height invariant). The effect of incorrectly and correctly specifying
radial sampling is demonstrated in Fig. 5.9, which is generated from the
MCNP input file shown in Listing 5.40. Note that the shading in the
volumes in the (volumetrically uniform and generally correctly
specified) lower half of Fig. 5.9 is constant when neglecting the noise
that arises from uneven source sampling versus the uneven radial
profiles visible in the (generally incorrectly specified) top half.

Listing 5.40: example\_radial\_source\_sampling.mcnp.inp.txt

<!-- image -->

```
15 200 s 0 -50 -50 35 16 300 rcc -0.5 50 50 1 0 0 35 17 400 rcc -0.5 50 -50 1 0 0 35 18 500 rpp -100 100 -100 100 -100 100 19 20 mode n 21 c 22 sdef cel = d1 pos = fcel = d2 rad = fcel = d3 axs = fcel = d4 ext = fcel = d5 23 si1 l 1000 2000 3000 4000 $ cel 24 sp1 0.25 0.25 0.25 0.25 25 ds2 s 20 21 22 23 $ pos 26 ds3 s 30 31 32 33 $ rad 27 ds4 s 40 41 42 43 $ axs 28 ds5 s 50 51 52 53 $ ext 29 c 30 si20 l 0 -50 50 31 sp20 1 32 si21 l 0 -50 -50 33 sp21 1 34 si22 l 0 50 50 35 sp22 1 36 si23 l 0 50 -50 37 sp23 1 38 c 39 si30 h 0 35 40 sp30 -21 1 $ Sphere, Linear Radial Sampling, Volumetrically Nonuniform - TYPICALLY WRONG 41 si31 h 0 35 42 sp31 -21 2 $ Sphere, Quadratic Radial Sampling, Volumetrically Uniform 43 si32 h 0 35 44 sp32 -21 0 $ Cylinder, Constant Radial Sampling, Volumetrically Nonuniform - TYPICALLY WRONG 45 si33 h 0 35 46 sp33 -21 1 $ Cylinder, Linear Radial Sampling, Volumetrically Uniform 47 c 48 si40 l 0 0 0 49 sp40 1 50 si41 l 0 0 0 51 sp41 1 52 si42 l 1 0 0 53 sp42 1 54 si43 l 1 0 0 55 sp43 1 56 c 57 si50 l 0 58 sp50 1 59 si51 l 0 60 sp51 1 61 si52 h -0.5 0.5 62 sp52 0 1 63 si53 h -0.5 0.5 64 sp53 0 1 65 c 66 fmesh14:n geom=xyz origin=-35 -85 -85 imesh=35 iints=70 67 jmesh=85 jints=170 68 kmesh=85 kints=170 69 out=none type=source 70 rand gen=2 seed=12345 71 print 72 nps 1e7
```

## /warning\_sign Caution

Never position any kind of degenerate volume distribution so that it
lies on a defined surface of the problem geometry. Even a bounding
surface that extends into the interior of a cell can cause trouble. If
possible, use one of the surface distributions instead. Else, move to a
position a small distance from the surface. This positioning will make
no detectable difference in the answers, but will prevent particles from
getting lost.

## 5.8.1.2 Surface Source Specification

The value of the keyword SUR is non-zero for a distribution on a
surface. The shape of the surface can be a spheroid, sphere, cylinder,
or plane. A spheroid is an ellipse revolved around one of its axes. If X
, Y , and Z are specified, their sampled values determine the position.
The user must in this case make sure that the point really is on the
surface because the MCNP code does not check. If X , Y , and Z are not
specified, the position is sampled on the surface SUR . With the
exception of a spherical surface, the SUR keyword does not automatically
provide source points on the listed surface. The user must still use the
X , Y , Z , POS , AXS , RAD , and EXT keywords to ensure the source
points actually lay on the prescribed surface. For a surface source,
sampling using CEL rejection is not an option; however, cookie-cutter
rejection can be used.

If the value of SUR is the name of a spheroidal surface, the position of
the particle is sampled uniformly in area on the surface. A spheroid for
this purpose must have its axis parallel to one of the coordinate axes.
Although there is no provision for easy non-uniform or biased sampling
on a spheroidal surface, a distribution of cookie-cutter cells could be
used to produce a crude non-uniform distribution of position.

If the value of SUR is the name of a spherical surface, the position of
the particle is sampled on that surface. A spherical surface source does
not have to be on a cell-bounding problem surface. If the vector AXS is
not specified, the position is sampled uniformly in area on the surface.
If AXS is specified, the sampled value of EXT is used for the cosine of
the angle between the direction AXS and the vector from the center of
the sphere to the position point. The azimuthal angle is sampled
uniformly in the range from 0 ◦ to 360 ◦ . A non-uniform distribution of
position, in polar angle only, is available through a non-uniform
distribution of EXT . A biased distribution of EXT can be used to start
more particles from the side of the sphere nearest the tallying regions
of the geometry. The exponential distribution function ( -31 , Table
5.15) usually is the most appropriate way to specify this behavior. The
keyword DIR may be specified without VEC , allowing VEC to default to
the outward surface normal.

Cylindrical surface sources must be specified as degenerate volume
sources. For a cylindrical surface source, the cylindrical surface can
be, but does not have to be, a cell-bounding problem surface specified
by the keyword SUR . If the cylindrical surface is a problem surface,
then the surface number must be specified on the SDEF card with the SUR
keyword. The default of VEC is the surface normal. If both DIR and VEC
are specified, then particle directions are relative to VEC rather than
to the cylindrical surface normal. DIR may be specified without VEC ,
causing VEC to default to the outward surface normal.

If the value of SUR is the name of a plane, the position is sampled on
that plane. The sampled value of POS must be a point on the plane. The
user must make sure that POS really is on the plane because the MCNP
code does not check. The sampled position of the particle is at a
distance from POS equal to the sampled value of RAD . The position is
sampled uniformly on the circle of radius RAD centered on POS . Uniform
sampling in area is obtained if the distribution of RAD is a power law
with a = 1 , which is the default in this case.

## 5.8.1.3 Unstructured Mesh Source Specification

The VOLUMER option is a new option for the POS parameter on the SDEF
card. More information about describing volume sources for the MCNP
unstructured mesh calculation can be found in the source keyword

discussion in §8.3.1.1 for a mesh model formatted as an Abaqus input
file and in the source group discussion in §D.6.2.4for a mesh model
formatted as an HDF5 file. The VOLUMER value is for unstructured mesh
volume source(s) so that x , y , z may be sampled from the volume source
description. Note that the last character ' R ' stands for sampling by
rejection. This section describes how the user can select among multiple
volume sources defined in the pseudo-cells.

First, if volume sources have been defined in the mesh model and you do
not wish to sample from them, don't use the VOLUMER value anywhere in
describing the source on the SDEF card. A fatal error is thrown if the
VOLUMER value is used in describing the source on the SDEF card but the
volume sources are not defined in the mesh model, or if the VOLUMER
value is associated with a pseudo-cell that does not use source
elements.

Second, to sample uniformly over all volume source regions defined in a
model, simply set the POS parameter to VOLUMER :

1

| SDEF POS=VOLUMER   |
|--------------------|

Next, if the volume sources appear in different pseudo-cells and you
desire to sample non-uniformly among the pseudo-cells, use a dependent
distribution where POS is a function of CEL . Only uniform sampling
within a cell is possible:

1

2

3

4

| SDEF CEL=D1 POS=FCEL=D2   |
|---------------------------|
| SI1 L 101 103             |
| SP1 0.4 0.6               |
| DS2 L VOLUMER VOLUMER     |

In this example, the MCNP code will first select proportionally from
cells 101 (40%) and 103 (60%). With the cell selected, the code will
select uniformly over that cell proportional to each element's volume to
find an element from which it will uniformly sample a position.

Finally, it is possible to combine volume sources with point sources
(and other legacy source descriptions) with a dependent distribution of
distributions.

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

13

14

15

<!-- image -->

| SDEF CEL=D1 POS=FCEL=D2 C   |
|-----------------------------|
| SI1 L 101 102 103           |
| SP2 0.4 0.2 0.4             |
| C                           |
| DS2 S 4 5 6                 |
| C                           |
| SI4 L VOLUMER               |
| SP4 1                       |
| C                           |
| SI5 L .1 .2 .3              |
| SP5 1                       |
| C                           |
| SI6 L VOLUMER               |
| SP6 1                       |

As before, the cell is selected first, then the position from the
appropriate distribution. In this example, the point source is selected
20% of the time.

1

## 5.8.1.4 Guidance: Defining Embedded Source Distribution Information

Source distributions may be embedded within each other to describe
accelerator micro-pulses and other phenomena. The format to specify an
embedded source is

```
SDEF TME=( D11 < D12 < D13 )
```

or, for distributions of distributions, the following form may be used:

```
SDEF TME=D41
```

```
1 2 SI41 S 51 ( D11 < D12 < D13 ) 52
```

In both cases, distributions 11, 12, 13 are all for the same variable,
time. Distribution 11 covers a small time range that is repeated as
often as needed to fill exactly the larger time range of distribution
12. Similarly, distribution 12 is repeated as often as needed to fill
exactly the even larger time range of distribution 13. See [§5.8.6.21]
for an example.

Note that the parentheses are optional and that the designator ' D ' on
the SI card with ' S ' option is also optional. Thus

```
SDEF TME=( D11 < D12 < D13 )
```

and

```
SDEF TME= D11 < D12 < D13
```

are equivalent.

Also,

```
SI41 S 51 ( D11 < D12 < D13 ) 52
```

and

```
SI41 S 51 D11 < D12 < D13 52
```

and

```
SI41 S 51 ( 11 < 12 < 13 ) 52
```

and

1

1

1

1

1

1

<!-- formula-not-decoded -->

are all equivalent.

The embedded distributions must start at zero or a fatal error message
is issued. For ( D11 &lt; D12 &lt; D13 ) the lowest value on the SI11 and SI12
cards must be zero. The embedding distribution, D13 , can have any
range.

## /warning\_sign Caution

The -21 entry on an SP card for a power-law distribution cannot be used
with the embedded distributions; it will lead to incorrect results.

The embedded distributions should fit within each other (nearly)
exactly. If they do not there the fatal error message, ' embedded
distribution nn has improper range ' is issued and the distribution will
spill into the next bin and have a strange normalization for values in
its last bin.

Only continuous source distributions such as ERG , TME , X , Y , Z , DIR
, RAD and EXT may use embedded distributions.

## 5.8.1.5 Guidance: Defining a Source in a Repeated Structures or Lattice Geometry

Hint: Carefully study PRINT Table 110 in the MCNP output file to ensure
that the proper source path and position are being sampled when repeated
structures are used in a source description.

When the source is specified in a repeated structure part of the
geometry, the CEL parameter on the SDEF card must have a value that is a
path, enclosed in parentheses, from level n to level 0 (i.e., the
highest level), where n is not necessarily the bottom level:

<!-- formula-not-decoded -->

In this specification c i is either zero or a cell in the universe that
fills cell c i -1 , or is D m for a distribution of cells in the
repeated structure case. A distribution of cells (i.e., D m ) is not
valid for a lattice; however, a range of lattice elements may be
specified. Cell designator c i can have a minus sign, but D m cannot.
This is discussed below. If c i = 0 , the cell at that level is searched
for. If c i is one specific element in a lattice, it is indicated as

<!-- formula-not-decoded -->

The coordinate system for position and direction sampling (PDS) is the
coordinate system of the first negative or zero c i in the source path
starting from the right and proceeding left. Each entry in the source
path represents a geometry level, where level zero is the last specified
source path entry, level one is the second entry to the left, and so
forth. Level zero is above level one and level two is below level one.
The PDS level is the level associated with the PDS cell or PDS
coordinate system. All levels above the PDS level must be included in
the source path. Levels below the PDS level need not be specified, and
when given, may include one or more zero entries. When the path has no
negative or zero entry, the default PDS level is the first (i.e.,
lowest) entry in the source path.

glyph[negationslash]

Position rejection is done in cells at all levels where c i = 0 , but if
any c i has a negative universe number on its cell card and is at or
above the PDS level, higher level cells are not checked.

1

Table 5.13: Cell Path versus PDS Level

| CEL Source Path                        | Cell of PDS Level   |   PDS Level |
|----------------------------------------|---------------------|-------------|
| ( 5 < 6 < 7 < 8 )                      | 5                   |           3 |
| ( 6 < -7 < 8 )                         | 7                   |           1 |
| ( 0 < 4 < 0 < -6 < 7 < 8 )             | 6                   |           2 |
| ( 0 < 6 [ 0 0 0 ] < -7 [ 1 0 0 ] < 8 ) | 7                   |           1 |
| ( 0 < 6 [ 0 0 0 ] < 7 [ 1 0 0 ] < 8 )  | Will be determined  |           3 |

Table 5.14: Cell Path versus Accepted/rejected Lattice Elements

Table 5.13 illustrates the concept of the PDS level.

| CEL Source Path   | Accepted     | Rejected              |
|-------------------|--------------|-----------------------|
| 7                 | All elements | None                  |
| ( 0 < 7 )         | All elements | None                  |
| ( 8 < 7 )         | [ 1 0 0 ]    | [ 0 0 0 ] , [ 2 0 0 ] |
| ( 10 < 7 )        | [ 2 0 0 ]    | [ 0 0 0 ] , [ 1 0 0 ] |

A range of lattice indices may be specified to produce a uniform
sampling among those lattice elements. The ability to sample source
points from a range of lattice indices requires the use of a fully
specified FILL card for the listed lattice cell. The sampling is
accomplished using rejection on all possible lattice elements. Note that
the SDEF keyword EFF may need to be decreased to accommodate sampling of
a small portion of a large lattice. A lattice cell without indices
results in uniform sampling in all elements if a fully specified FILL
card is provided. Uniform sampling is applied to lattice cell entries in
the source path that lack an explicit lattice index and that are at or
above the PDS level. Lattice cells not defined by the expanded FILL card
must include an explicit lattice index when at or above the PDS level.
Rejection of automatically sampled lattice elements depends on the entry
before the lattice cell number in the source path.

Assume the following cell descriptions where cell 7 is a 3-element
lattice defined using the following data entries:

lat=1 u=1 fill=0:2 0:0 0:0 1 2 3

Cells 8 and 9 are members of universe 2, and cells 10 and 11 are members
of universe 3.

Cell 7 is a lattice with three existing elements: [ 0 0 0 ] , which is
filled by itself [ u=1 ] ; [ 1 0 0 ] , which is filled by cells 8 and 9
[ u=2 ] ; and [ 2 0 0 ] , which is filled by cells 10 and 11 [ u=3 ] .
Table 5.14 show which elements are accepted and which are rejected.

The sampling efficiency for cell 7 in the MCNP output file will reflect
the element rejections. Lattice cell entries that lack an explicit
lattice index and are below the PDS level are not sampled. Instead, the
appropriate lattice element is determined by the input source position.

Lattice element sampling is independent from position sampling. First a
lattice element is chosen, then a position is chosen. If the sampled
position is not in the sampled lattice element, the position is
resampled until it is in the specified source path and in the lattice
element chosen or until an efficiency error occurs. The lattice elements
will not be resampled to accommodate the sampled position. Lattice
element rejection is done only as described above.

Using the previous description of lattice cell 7, add that cell 6 is
filled by cell 7. The source path becomes ( 0 &lt; 7 &lt; 6 ) . Three elements
of the lattice exist ( fill = 0 : 2 0 : 0 0 : 0 ) but element [ 0 0 0 ]
now is cut off

by cell 6. Lattice element [ 0 0 0 ] still will be sampled one-third of
the time. The first time element [ 0 0 0 ] is sampled a fatal error will
occur because the sampled position, no matter what it is, will be
rejected because element [ 0 0 0 ] does not exist.

## /warning\_sign Caution

Implement automatic lattice sampling carefully and ensure that all of
the lattice elements specified on the expanded FILL card really do
exist.

Note that the format of the CEL source path is the same as for tally
cards. See [§5.9.1.5] for more information about specifying the path for
repeated structures or lattices for tallies.

## 5.8.1.6 Shorthand: Specifying Multiple Cell Paths for Repeated Structures or Lattices

The source cell path input format also allows a shorthand notation for
one source cell path to represent a number of source paths, similar to
the way that one 'tally 4' path sequence enclosed in parentheses can
represent a number of separate tallies. For example, the input source
path ( 5 &lt; 7 8 9 10 11 &lt; 1 ) is interpreted by the MCNP code as the
following five paths: ( 5 &lt; 7 &lt; 1 ) , ( 5 &lt; 8 &lt; 1 ) , ( 5 &lt; 9 &lt; 1 ) , (
5 &lt; 10 &lt; 1 ) , and ( 5 &lt; 11 &lt; 1 ) . The sequence order of these paths is
determined from left to right in the original input master path.
Similarly, single or multiple lattice indexes within the square brackets
of path ( 5 &lt; 3 [ . . . ] &lt; 2 ) can have the following four optional
input forms for the [ i , j , k ] index data for lattice cell element(s)
with the FILL array defined on the cell 3 card:

| i         |                 | Indicates the i th lattice element of cell 3 as defined by the FILL array using only one count index; e.g., i = 1 is the first element.                           |
|-----------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| i j k     |                 | Indicates a lattice element from the FILL array using the three indexes.                                                                                          |
| i 1 : i 2 | : j 2 k 1 : k 2 | Indicates a range of one or more lattice elements, where the ' : ' and last entry of any of the three pairs can be omitted if that lattice element does not vary. |
| U = m     |                 | Specifies all of the lattice elements that have universe ' m '.                                                                                                   |

For the third specification form listed above, the MCNP code will create
' n ' source paths, where

<!-- formula-not-decoded -->

with the order of these n paths being the order of the indexes changing
from left to right with the left index varying most rapidly. For the
fourth specification, the n source paths are the number of lattice
elements with universe m , where the order of the source paths is the
order in the FILL matrix for cell 3. Since the SP card must specify the
corresponding probabilities, this sequence order may be important. This
sequence of the split paths is shown in the 'cell' column of PRINT Table
10 of the MCNP output file.

When more than one cell (or lattice cell) is specified on more than one
level in the source input path, the MCNP code splits into multiple paths
with the variation most rapid from the left. However, the first level
(level n ) and the last level (level 0) entered in the source input path
can only have one entry. The path in this new format must always be
enclosed in parentheses, but there must not be any inner parentheses in
the path.

## 5.8.1.7 Spontaneous Fission Sources: Physics and Tally Normalization

Eighteen nuclides are available for a spontaneous fission source ( PAR =
SF ): 232 Th, 232 U, 233 U, 234 U, 235 U, 236 U, 238 U, 237 Np, 238 Pu,
239 Pu, 240 Pu, 241 Pu, 242 Pu, 241 Am, 242 Cm, 244 Cm, 249 Bk, and 252
Cf.

If more than one spontaneous-fission nuclide is present in a source
cell, the fissioning nuclide will be chosen proportionately to the
product of its atom fraction and the spontaneous-fission yield for each
nuclide. If no spontaneous-fission nuclide is found in a specified
source cell, the code exits with a 'BAD TROUBLE' error: 'spontaneous
fission impossible.'

The number of spontaneous-fission neutrons then is sampled. The
spontaneous-fission multiplicity data of Santi [272] and references
cited by him are used by default. Alternatively, the LLNL FREYA or CGMF
fission model can be used (see the FMULT card for more details). The
energies are sampled from a Watt spectrum with appropriate spontaneous-
fission parameters for the selected nuclide. Only the first spontaneous-
fission neutron from each history is printed. If the spontaneous fission
samples a multiplicity of zero-that is, no neutrons for a given
spontaneous fission-then the history is omitted from the first 50
history lists of PRINT Table 110. The number of source particles is the
number of spontaneous-fission neutrons, which will be ν times the
requested number of source histories on the NPS card.

The spontaneous fission source is different from most other SDEF fixed
sources. Let

- N be the number of source-particle histories run in the problem,
- W be the average source particle weight, and
- ν be the average number of spontaneous fission neutrons per fission.

For most other fixed-source ( SDEF ) problems,

- N is the summary table source tracks,
- W is the summary table source weight, and
- summary tables and tallies are normalized by N .

For the spontaneous fission source, SDEF PAR = SF ,

- summary table source tracks = ν · N ,
- summary table source weight = W , and
- summary tables and tallies are normalized by ν · N , the number of spontaneous fission neutrons.

For the spontaneous fission source, SDEF PAR = -SF ,

- summary table source tracks = ν · N
- summary table source weight = ν · W , and
- summary tables and tallies are normalized by N , the number of spontaneous fissions.

## 5.8.2 SI: Source Information

| Data-card Form: SI n option i 1 . . . i K   | Data-card Form: SI n option i 1 . . . i K                                                         | Data-card Form: SI n option i 1 . . . i K                                                                                                                                          |
|---------------------------------------------|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                           | Distribution number from corresponding distribution number on SDEF card. Restriction: 1 ≤ n ≤ 999 | Distribution number from corresponding distribution number on SDEF card. Restriction: 1 ≤ n ≤ 999                                                                                  |
| option                                      | Determines how the i values are interpreted. If                                                   | Determines how the i values are interpreted. If                                                                                                                                    |
|                                             | option = H or absent                                                                              | i values are monotonically increasing histogram bin upper boundaries (scalar only) ( 1 ). (DEFAULT)                                                                                |
|                                             | option = L                                                                                        | i values are discrete source variable values (e.g., cell numbers or energies of photon spectrum lines).                                                                            |
|                                             | option = A                                                                                        | i values are points where a probability density is defined. Entries must be monotonically increasing, with the lowest and highest values defining the range of the variable ( 2 ). |
|                                             | option = S                                                                                        | i values are distribution numbers ( 3 ).                                                                                                                                           |

Default:

## Details:

- 1 The H option is an integral, bin-wise method for describing a source distribution. It is integral in the sense that the fundamental differential distribution (e.g., particles/MeV for energy) must be integrated over an interval and its integration value placed on the SP card, corresponding to the upper bin value listed on the SI card. For example, if an energy differential distribution is integrated from E 1 to E 2 (and these are the first two entries ( i 1 and i 2 ) on the SI card), then the integration value over this interval is listed as the 2nd entry ( p 1 ) on the corresponding SP card.
- 2 When the A option is used, the entries on the SI card are values of the source variable at which the probability density is defined. The A option is a differential, point-wise method for describing a source distribution. The fundamental differential distribution is placed directly on the SP card, in a point-wise fashion. For each point listed on the SI card, the corresponding value of the differential distribution is listed on the SP card. For example, if an energy differential distribution has a value of V 1 at E 1 and V 2 at E 2 , then the SI entries i 1 and i 2 become E 1 , E 2 and the SP entries p 1 and p 2 become V 1 and V 2 . Typically, the first entry on the SP card would not be zero (although it can be). To sample this description of a source variable, the code must integrate the point-wise distribution and formulate an integral, bin-wise cumulative distribution for sampling (i.e., basically do what the user had to do when using the H option). To accomplish this, the code uses a corrected trapezoidal (i.e., linear) integration scheme, along with linear interpolation for intra-bin sampling. While this integration scheme is fairly accurate, users are encouraged to increase the number of points on their SI / SP cards and note effects to tallies to ensure this linear integration scheme is adequate for their specified differential distribution. Included in PRINT Table 10 are the integral, bin-wise cumulative distribution that will be used when sampling the associated source variable and the renormalized input differential distribution.
- 3 The S option on the SI card allows sampling among distributions, one of which is chosen for further sampling. This feature makes it unnecessary to fold distributions together and is essential if some of the distributions are discrete and others are linearly interpolated. The distributions listed on an SI card with the S option can themselves have the S option. Each distribution number on the SI card can be prefixed with a D , or the D can be omitted. If a distribution number is zero, the default value for the variable is

SI n H i 1 . . . i K

used. A distribution can appear in more than one place with an S option,
but a distribution cannot be used for more than one source variable.

## 5.8.3 SP: Source Probability

| Data-card Form: SP n option p 1 . . . p K or Data-card Form: SP n -f a b   | Data-card Form: SP n option p 1 . . . p K or Data-card Form: SP n -f a b                                  | Data-card Form: SP n option p 1 . . . p K or Data-card Form: SP n -f a b                                                                                                                                         |
|----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n                                                                          | Distribution number from corresponding distribution number on SDEF and SI cards. Restriction: 1 ≤ n ≤ 999 | Distribution number from corresponding distribution number on SDEF and SI cards. Restriction: 1 ≤ n ≤ 999                                                                                                        |
|                                                                            | Determines how the p values are interpreted ( 1 ). If                                                     | Determines how the p values are interpreted ( 1 ). If                                                                                                                                                            |
|                                                                            | option absent                                                                                             | it is the same as D for an H or L distribution on the SI card or probability density for an A distribution on the SI card ( 2 ).                                                                                 |
|                                                                            | option = D                                                                                                | p values are bin probabilities for an H or L distribution on the SI card ( 3 , 4 ). (DEFAULT)                                                                                                                    |
|                                                                            | option = C                                                                                                | p values are cumulative bin probabilities for an H or L distribution on the SI card ( 5 , 6 ).                                                                                                                   |
|                                                                            | option = V                                                                                                | p values are for cell distributions; probability is proportional to cell volume ( × p i if p i are present) ( 5 ).                                                                                               |
|                                                                            | option = W                                                                                                | p values are intensities for a mix of particle sources. Negative p values corresponding to SF or SP sources indicate cell numbers, the volumes of which will be used for the computation of the intensity ( 6 ). |
| p 1 . . . p K                                                              | Source variable probabilities. Restriction: Must be zero for 1st histogram bin                            | Source variable probabilities. Restriction: Must be zero for 1st histogram bin                                                                                                                                   |
| -f                                                                         | Designator (negative number) for a built-in function.                                                     | Designator (negative number) for a built-in function.                                                                                                                                                            |
| a b                                                                        | Parameters for the built-in function (Refer to Table 5.15).                                               | Parameters for the built-in function (Refer to Table 5.15).                                                                                                                                                      |

Default: . . .

SP n D p 1 p K

The first form of the SP card, where the first entry is positive or non-
numeric, indicates that it and its SI card define a probability
distribution function. The entries on the SI card are either values of
the source variable or, when the S option is used, distribution numbers.
The entries on the SP card are probabilities that correspond to the
entries on the SI card.

The second form of the SP card, where the first entry is negative,
indicates that a built-in analytic function is to be used to generate a
continuous probability density function for the source variable. Built-
in functions can be used only for scalar variables.

## Details:

- 1 Probabilities on the SP card need not be normalized.

Table 5.15: Special Source Probability Functions

| Keyword            |   Function ID and Input |    |    | Description                                                                                  |
|--------------------|-------------------------|----|----|----------------------------------------------------------------------------------------------|
| ERG                |                      -2 |    | a  | Maxwell fission spectrum                                                                     |
| ERG                |                      -3 | a  | b  | Watt fission spectrum                                                                        |
| ERG                |                      -4 | a  | b  | Gaussian fusion spectrum                                                                     |
| ERG                |                      -5 |    | a  | Evaporation spectrum                                                                         |
| ERG                |                      -6 | a  | b  | Muir velocity Gaussian fusion spectrum                                                       |
| TME                |                      -7 |    | a  | Exponential decay                                                                            |
| DIR , RAD , or EXT |                     -21 |    | a  | Power law: p ( x ) = c | x | a                                                               |
| DIR or EXT         |                     -31 |    | a  | Exponential: p ( µ ) = c exp( aµ )                                                           |
| TME or X , Y , Z   |                     -41 | a  | b  | Gaussian distribution of time, t , or of position coordinates ( x, y, z ) (for beam sources) |

- 2 When the A option is used on the SI card, the numerical entries on the associated SP card are values of the probability density corresponding to the values of the variable on the SI card. This set of SI and SP values creates a curve from which intermediate values are linearly interpolated. The first and last entries on the SP card will typically be zero, but non-zero values are allowed.
- 3 When the H option is used on the SI card, the first numerical entry on the corresponding SP card must be zero and the following entries are bin probabilities or cumulative bin probabilities, depending on whether the D or C option on the SP card is selected. The variable is sampled by first sampling a bin according to the bin probabilities and then sampling uniformly within the chosen bin.
- 4 When the L option is used on the SI card, the entries on the associated SP card are either probabilities of those discrete values or cumulative probabilities, depending on whether the D or C option is selected.
- 5 The V option on the SP card is a special case used only when the source variable is CEL . This option is useful when the cell volume is a factor in the probability of particle emission. If the MCNP code cannot calculate the volume of such a cell and the volume is not provided on a VOL card, a fatal error results.
- 6 The W option of the SP card allows the user to specify intensities for a mix of particle sources. The intensities will be normalized, as is done for all MCNP source distributions; however the factor used to renormalize the intensities will be applied to the source weight to give the tallies the correct magnitude. The SP n W distribution specification can only be applied to particle distributions.

## 5.8.3.1 Description of Built-in Probability Density and Bias Functions

The special (i.e., built-in) source probability functions are summarized
in Table 5.15 and described in detail next.

<!-- formula-not-decoded -->

f = -31

See Listing 5.29 for the default parameters used with the FMULT card for
spontaneous fission.

Default: a = 0 . 965 MeV, b = 2 . 29 MeV - 1 .

f = -4 Gaussian fusion energy spectrum:

<!-- formula-not-decoded -->

where a is the width in MeV and b is the average energy in MeV. Width
here is defined as the ∆ E above b where the value of the exponential is
equal to e -1 . If a &lt; 0 , it is interpreted as a temperature in MeV and
b must also be negative. If b = -1 , the D-T fusion energy is calculated
and used for b . If b = -2 , the D-D fusion energy is calculated and
used for b . Note that a is not the full-width-at-half-maximum (FWHM)
but is related to it by FWHM = 2 a √ ln(2) .

Default: a = -0 . 01 MeV, b = -1 (DT fusion at 10 keV).

f = -5 Evaporation energy spectrum:

<!-- formula-not-decoded -->

Default: a = 1 . 2895 MeV.

f = -6 Muir velocity Gaussian fusion energy spectrum:

<!-- formula-not-decoded -->

where a is the width in MeV 1 / 2 , and b is the energy in MeV
corresponding to the average speed. Width here is defined as the change
in velocity above the average velocity b 1 / 2 , where the value of the
exponential is equal to e -1 . To get a spectrum somewhat comparable to
f = -4 , the width can be determined by a = √ b + a 4 -b 1 / 2 , where a
4 is the width used with the Gaussian fusion energy spectrum. If a &lt; 0 ,
it is interpreted as a temperature in MeV. If b = -1 , the D-T fusion
energy is calculated and used for b . If b = -2 , the D-D fusion energy
is calculated and used for b .

Default: a = -0 . 01 MeV, b = -1 (D-T fusion at 10 keV).

f = -7 Exponential decay:

<!-- formula-not-decoded -->

Allows the creation of a source with an exponential decay shape. The
activity at TME = 0 is given by α 0 . The parameter a is the half-life
in shakes.

Default: a = 1 .

<!-- formula-not-decoded -->

The default depends on the variable. For DIR , a = 1 . For RAD , a = 2 ,
unless AXS is defined or SUR = 0 , in which case a = 1 . For EXT , a = 0
.

glyph[negationslash]

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

f = -41 Gaussian distribution of time or position coordinates t x, y, z
:

<!-- formula-not-decoded -->

where a is the width at half maximum and b is the mean. For time, a and
b are in shakes, while for position variables, the units are
centimeters. Note: This distribution may be written in normal form as

<!-- formula-not-decoded -->

The FWHM is thus a = √ 8 ln 2 σ .

Default: no default,

a = b = 0 .

The built-in functions can be used only for the variables shown in Table
5.15. Any of the built-in functions can be used on SP cards, but only
-21 and -31 can be used on SB cards. If a function is used on an SB
card, only that same function can be used on the corresponding SP card.
The combination of a regular table on the SI and SP cards with a
function on the SB card is not allowed.

A built-in function on an SP card can be biased or truncated or both by
a table on SI and SB cards. The biasing affects only the probabilities
of the bins, not the shape of the function within each bin. If it is
biased, the function is approximated within each bin by n equally
probable groups such that the product of n and the number of bins is as
large as possible but not over 300. Unless the function is -21 or -31 ,
the weight of the source particle is adjusted to compensate for
truncation of the function by the entries on the SI card.

Special defaults are available for distributions that use built-in
functions:

- If SB f is present and SP f is not, an SP f with default input parameters is, in effect, provided by the MCNP code.
- If only an SI card is present for RAD or EXT , an SP -21 with default input parameters is, in effect, provided.
- If only SP -21 or SP -31 is present for DIR or EXT , an SI 0 1 for -21 , or SI -1 1 for -31 , is, in effect, provided.
- If SI x and SP -21 are present for RAD , the SI is treated as if it were SI 0 x .
- If SI x and SP -21 or SP -31 are present for EXT , the SI is treated as if it were SI -x x .

## 5.8.4 SB: Source Bias

The SB card is used to provide a probability distribution for sampling
that is different from the true probability distribution on the SP card.
Its purpose is to bias the sampling of its source variable to improve
the convergence rate of the problem. The weight of each source particle
is adjusted to compensate for the bias. All rules that apply to the
first form of the SP card apply to the SB card.

```
Data-card Form: SB n option b 1 . . . b K or Data-card Form: SB n -f a b n same as for the SP card. option same as for the SP card. b 1 . . . b K source-variable-biased probabilities. -f same as for the SP card, except that the only values allowed for -f are -21 and -31 . a b same as for the SP card.
```

Default: SB n D b 1 . . . b K

## 5.8.5 DS: Dependent Source Distribution

The DS card is used instead of the SI card for a variable that depends
on another source variable, as indicated on the SDEF card. No SP or SB
card is used. The MCNP code first determines the value of the
independent variable as usual by sampling the probability function of
the independent variable. Then the value of the dependent variable is
determined according to the form of the DS card.

The first form of the DS card has several possibilities. If the SI card
of the independent variable has a histogram distribution of m bins ( m
+1 entries) and the DS card has the blank or H option, the DS card must
have m +1 entries to specify m bins. The first entry need not be zero.
If the sampled value of the independent variable is i k +[ f ( i k +1 -i
k )] , then the value of the dependent variable is j k +[ f ( j k +1 -j
k )] , where the terms in f are used only for continuous distributions.
The interpolation factor f always exists whether or not it is needed for
the independent distribution.

The second form of the DS card specifies the T option. When the T option
is selected, the sampled value of the independent variable is sought
among the i k , and if a match is found, the independent variable gets
the value j k . If no match is found, the dependent variable gets its
default value. The purpose of the T option is to shorten the input when
a dependent variable should usually get the default value.

When the Q option is used on a DS card, as it is in the third form, the
v k define a set of bins for the independent variable. The sampled value
of the independent variable is compared with the v k , starting with v 1
, and if the sampled value is less than or equal to v k , the
distribution s k is sampled for the value of the dependent variable. The
value of v k must be greater than or equal to any possible value of the
independent variable. If a distribution number s k is zero, the default
value for the variable is used. The Q option is the only form of the DS
card that can be used when the distribution of the independent variable
is a built-in function.

```
Data-card Form: DS n option j 1 . . . j K or Data-card Form: DS n T i 1 j 1 . . . i K j K or Data-card Form: DS n Q v 1 s 1 . . . v K s K n Distribution number. Restriction: 1 ≤ n ≤ 999 option Determines how the j values are interpreted. If option = H or absent source variable values in continuous distribution, for
```

1

<!-- image -->

Default:

DS n H j 1 . . . j K

## Details:

- 1 If the L or S option is used on the DS card, m entries are required to specify m discrete values (for all options on the independent variable except H ). See 2 for an independent variable that is represented by a histogram. It is not necessary for the distributions of the independent and dependent variables to be both discrete or both continuous. All combinations work correctly.
- 2 If the S option is used on the DS card and the independent variable has a histogram defined by m +1 SI entries, then m numbers must appear on the DS card. Recall that the first bin of a histogram distribution must have an SP value of 0.0. The code will assume that the first independent histogram bin is ignored. A fatal error will result if a dependent source value is assigned to the first histogram bin.
- 3 The DS Q option does not support using cells, surfaces, or transforms as the independent variable, as the sort order of these variables is not maintained internally in the code. The T option is more appropriate for these variables.

## 5.8.6 Examples of the General Source Card and Distribution Cards

## 5.8.6.1 Example 1

SDEF

This card specifies a 14-MeV isotropic point source at position (0 , 0 ,
0) at time 0 with weight 1 (all defaults).

1

2

3

4

1

2

3

4

5

6

## 5.8.6.2 Example 2

| SDEF   | ERG=D1   | POS=x y z WGT=w   |
|--------|----------|-------------------|
| SI1    | H e1     | e2 ... ek         |
| SP1    | D        | 0 p2 ... pk       |
| SB1    | D        | 0 b2 ... bk       |

This is a point isotropic source at ( x, y, z ) with a biased histogram
energy distribution and average source particle weight w . The starting
cell is not specified. The MCNP code will determine it from the value of
( x, y, z ) .

## 5.8.6.3 Example 3

| SDEF   |   SUR=m AXS=i j k |   EXT=D6 |
|--------|-------------------|----------|
| SB6    |               -31 |      1.5 |

This is a source on surface m . The presence of AXS and EXT implies that
surface m is a sphere because AXS and EXT are not otherwise used
together for sources on a surface. By default, the particles are emitted
in a cosine distribution. They are emitted outward if the positive
normal to the sphere is outward, which it is for all the spherical
surface types but might not be if the sphere is specified as type SQ .
The position on the surface is biased toward the direction ( i, j, k )
by an exponential bias (specified by -31 ). Table 2.10 shows the effect
of the biasing parameter on the maximum and minimum source particle
weights and the cumulative probability distribution. By default, the
MCNP code provides the effect of two cards: SI6 -1 1 and SP6 -31 0 .

## 5.8.6.4 Example 4

| SDEF   | SUR=999   | NRM=-1 DIR=D1   | WGT=1.13097e6   |
|--------|-----------|-----------------|-----------------|
| SB1    | -21 2     |                 |                 |
| void   |           |                 |                 |
| f4:n   | 1 2 3 4   |                 |                 |
| vol    | 1 5r      |                 |                 |
| imp:n  | 1.0 4r    | 0.0             |                 |

These data cards illustrate how an inward-directed ( NRM = -1 ), biased
cosine source on a spherical surface can be used to stochastically
calculate the volume of MCNP cells. All materials are voided in the
problem ( VOID card) and all non-zero importance are set to 1 ( IMP :N
card). In this example, the surface source is placed on the surface of a
600-cm-radius sphere ( SUR = 999 ) that surrounds the cells of interest
and the source weight ( WGT ) is set to 1 . 13097 × 10 6 cm 2 ( πr 2 ).
All volumes are forced to unity ( VOL card). Type 2 and type 4 flux
tallies will provide estimates of the areas and volumes of the cells,
respectively. By default, the MCNP code provides the effect of two
cards: SI1 0 1 and SP1 -21 1 . The directional bias by the SB1 card
causes higher track density toward the center of the sphere, where
presumably the cells of greatest interest lie, than it would be if the
unbiased cosine distribution were used. This bias, incidentally,
provides a zero-variance estimate of the (known) volume of the sphere
999.

1

2

3

1

1

## 5.8.6.5 Example 5

```
SDEF CEL=D3 POS=0 6 0 EXT=D1 RAD=D2 AXS= 0 1 0 SI3 L (1<10[0 0 0]<11) (1<10[1 0 0]<11) (1<10[2 0 0]<11) (1<10[0 1 0]<11) (1<10[1 1 0]<11) (1<10[2 1 0]<11)
```

The SDEF card creates a cylindrical volume source oriented along the y
axis with radius specified by the SI2 source information and SP 2 source
probability cards and extent given by SI 1 and SP 1 . This CEL source
specification for repeated-structures geometries is consistent with the
repeated-structures tally format. The old-style format (listing cells in
the opposite order separated by ' : ') is no longer recognized and will
produce a fatal error.

## 5.8.6.6 Example 6

```
SDEF POS=0 0 0 RAD=1 EXT=D1 AXS=1 0 0 SUR=5
```

```
SDEF POS=0 0 0 RAD=1 EXT=D1 AXS=1 0 0 SUR=5 DIR=D2
```

```
1 SDEF POS=0 0 0 RAD=1 EXT=D1 AXS=1 0 0 DIR=D2
```

The first SDEF card specifies a cylindrical source on surface 5 with
default cosine distribution relative to the surface normal. The second
SDEF card specifies a cylindrical source on surface 5 with a specified
angular distribution that is relative to the cylindrical surface normal.
The third SDEF source specification is similar except that a degenerate
volume source is used to specify the cylindrical surface source (i.e.,
omitting the SUR keyword) with a specified angular distribution relative
to the surface normal.

## 5.8.6.7 Example 7

```
1 SDEF DIR=1 VEC=0 0 1 X=D1 Y=D2 Z=0 CCC=99 TR=1 2 SP1 -41 fx 0 3 SP2 -41 fy 0 4 TR1 x0 y0 z0 cos(theta) -sin(theta) 0 sin(theta) cos(theta) 0 0 0 1
```

The SDEF card sets up an initial beam of particles traveling along the z
axis ( DIR = 1 , VEC = 0 0 1 ). Information on the x and y coordinates
of particle position is detailed in the two SP cards. The z coordinate
is left unchanged. The first entry on the SP cards is -41 , indicating
sampling from a built-in Gaussian distribution. The second SP card entry
is the full width half maximum (FWHM) of the Gaussian in either the x or
y direction. This value must be computed for the x and y axes by the
user as follows: f x = √ 8 ln 2 a ≈ 2 . 35482 a and f y = √ 8 ln 2 b ≈ 2
. 35482 b , where a and b are the standard deviations of the Gaussian in
the x and y directions, respectively. More details are provided in
[§10.3.2]. The third entry represents the centroid of the Gaussian in
either the x or y direction. It is recommended the user input zero for
this third entry and handle any transformations of the source with a TR
card. The specification of the cookie-cutter cell 99 for source
rejection prevents the beam Gaussian from extending infinitely. The TR
card performs a rotation of the major axis of the source distribution.
Other beam examples appear in [§10.3.2].

1

2

3

## 5.8.6.8 Example 8

```
1 SDEF ERG=D1 POS=x y z CEL=m RAD=D2 2 EXT=D3 AXS=i j k 3 SP1 -3 4 SI2 r1 r2 5 SI3 l
```

This source is distributed uniformly in volume throughout cell m , which
presumably approximates a cylinder. The cell is enclosed by a sampling
volume centered at ( x, y, z ) . The axis of the sampling volume is the
line through ( x, y, z ) in the direction ( i, j, k ) . The inner and
outer radii of the sampling volume are r1 and r2 , and it extends along
( i, j, k ) for a distance from ( x, y, z ) . The user has to make sure
that the sampling volume totally encloses cell m . The energies of the
source particles are sampled from the Watt fission spectrum using the
default values of the two parameters, making it a Cranberg spectrum. By
default, the MCNP code interprets SI3 l as if it was actually SI3 -l +l
and provides the effect of two cards: SP2 -21 1 and SP3 -21 0 .

## 5.8.6.9 Example 9

```
1 SDEF SUR=m POS=x y z RAD=D1 DIR=1 CCC=n 2 SI1 r
```

This is a mono-directional source emitted from surface m in the
direction of the positive normal to the surface. The presence of POS and
RAD implies that surface m is a plane because POS and RAD are not
otherwise used together for sources on a surface. The position is
sampled uniformly in area on the surface within radius r of point ( x,
y, z ) . The user must make sure that point ( x, y, z ) actually lies on
surface m . The sampled position is rejected and resampled if it is not
within cookie-cutter cell n . The starting cell is found from the
position and the direction of the particle. By default, the MCNP code
interprets SI1 r as if it were actually SI1 0 r and provides the effect
of card SP1 -21 1 .

## 5.8.6.10 Example 10

```
1 SDEF PAR=SF CEL=D1 POS=D2 RAD=FPOS=D3
```

This is a spontaneous-fission source in which source points will be
started from within defined spheres ( POS , RAD ) and limited to fission
cells by CEL . Each sampled source point will be a spontaneous-fission
site ( PAR = SF ) producing the appropriate number of spontaneous-
fission neutrons per fission at the appropriate energy with isotropic
direction.

## 5.8.6.11 Example 11

| SDEF   | PAR=D1           |
|--------|------------------|
| SI1    | L 1 9 Li-6 Fe-56 |
| SP1    | 1 1 0.1 0.3      |

Five different source particles are sampled in this example: neutrons;
protons; and the three heavy ions: 6 Li, 56 Fe, and 238 U. The relative
sampling frequency is given by the probability parameters on the SP1
card.

## 5.8.6.12 An Aside on PAR = D n

Note the following when using a distribution specification for the SDEF
PAR keyword:

1. The characters L , A , H , S , Q , and T are reserved as SI and DS card options. L means discrete source variables, S means distribution numbers, etc. If the first entry on the SI or DS card is L , A , H , S , Q , or T , it will be interpreted as a distribution option. To list source particles types L , A , H , S , Q , or T , either the corresponding particle numbers ( 10 , 34 , 9 , 33 , 5 , 32 ) must be used or L , A , H , S , Q , or T must appear as the second or later particle type. Generally, it is best to specify the discrete source variable option; therefore, L will be the first entry, followed by the particle types. A second L will be interpreted correctly as particle type L . For example,

1

SI99 L -H N L Q F T S

2. Antiparticles may be designated, as usual, with negative entries:

1

SI77 L -E N -H

3. Either characters ( N , P , E , H , D , T , S , A , etc.) or numbers ( 1 , 2 , 3 , 9 , 31 , 32 , 33 , 34 , etc.) may be used. For example,

1

SI98 L -H 3 -32 N

4. Spontaneous fission may be used as a particle type. For example,

1

SI87 L SF N

5. Particle types may be listed multiple times to give them different energy distributions, angular distributions, etc., in different parts of the problem. For example:

1

SI23 L N n 1 n N

6. Heavy ions may be specified using the appropriate target identifier for individual ions. Multiple heavy ions may be specified for the source using a distribution. Dependent distributions can be used to specify different energies for different heavy ions. Heavy ion particle energy should be input as total energy, not energy/nucleon.
7. Tallies are normalized by dividing the total source weight by the number of source histories. Note that weight ( WGT on the SDEF card) cannot be a source distribution (either independent or dependent). The weight of particles in the summary tables is controlled by the SI , SP , SB , and DS cards for the particle distribution. This normalization procedure is described in [§5.8.6.13].

1

2

3

4

5

6

## 5.8.6.13 Example 12

| SDEF   | PAR=D1 POS=FPAR=D2 ERG=FPAR=D3   |
|--------|----------------------------------|
| SI1    | L H N                            |
| SP1    | 2 1                              |
| SB1    | 1 2                              |
| DS2    | L 0 0 0 15 0 0                   |
| DS3    | L 2 3                            |

1

2

3

4

5

6

| SDEF   | PAR=FPOS=D2 POS=D1 ERG=FPOS=D3   |
|--------|----------------------------------|
| SI1    | L 0 0 0 15 0 0                   |
| SP1    | 2 1                              |
| SB1    | 1 2                              |
| DS2    | L h n                            |
| DS3    | L 2 3                            |

The first source definition above defines the source particle type, PAR
, as the independent variable; while in the second source definition,
the source particles specified by PAR depend on the source positions (
POS ). Both approaches result in the same source distributions.

The total source weight is WGT = 1.0 by default. From the SP 1 card, the
weight of the neutrons that are produced is 1 / 3 and the weight of
protons that are produced is 2 / 3 . From the SB1 card, the total number
of neutron tracks is 2 / 3 × N for neutrons and 1 / 3 × N for protons
(where N is the number of source histories actually run). The energy per
source particle is normalized to the source particle weight for each
source particle type. If the particle type is not a source particle
(e.g., photons in the above problem), then the energy per source
particle is normalized to the source particle weight of the lowest
particle type. In this example, photon source energy would be normalized
in the photon creation-and-loss table by 1 / 3 , which is the weight of
the source neutrons produced.

## 5.8.6.14 Example 13

Listing 5.41: example\_source\_fpos\_ds\_1.mcnp.inp.txt

| sdef pos = d1 erg = fpos = d2   |          |        |
|---------------------------------|----------|--------|
| si1 0                           | l -51 0  | 51 0 0 |
| sp1                             | 0.3      | 0.7    |
| ds2                             | s 3      | 4      |
| si3                             | h 2 10   | 14     |
| sp3                             | d 0 1    | 2      |
| sp4                             | -3 0.965 | 2.29   |

The example shown in Listing 5.41 is a point isotropic source in two
locations, shown by two ( x, y, z ) s on the SI1 card. The code will
determine the starting cell. With probability 0.3 the first location
will be picked, and with probability 0.7 the second location will be
chosen. Each location has a different energy spectrum pointed to by the
DS2 card. All other needed source variables will use their default
values.

## 5.8.6.15 Example 14

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

4

```
SDEF DIR=1 VEC=0 0 1 X=D1 Y=0 Z=-2 TR=1 SI1 0.0 0.5 SP1 0.0 1.0 TR1 0.5 0.5 0.0 0.4 0.3 0.0 -0.3 0.4 0.0
```

This example generates a source uniform on a straight line from ( x, y,
z ) = (0 . 5 , 0 . 5 , -2 . 0) to ( x, y, z ) = (0 . 9 , 0 . 8 , -2 . 0)
in the + z direction. In the auxiliary coordinate system, the source is
easily created as uniform from (0 . 0 , 0 . 0 , -2 . 0) to (0 . 5 , 0 .
0 , -2 . 0) and then transformed.

## 5.8.6.16 Example 15

```
1 SDEF TR=D1 2 SI1 L 1 3 5 3 SP1 D 1.0 1.0 1.0 4 SB1 C 0.2 0.5 1.0
```

In this example, a distribution of transformations is specified using TR
= D1 on the SDEF card. Three transformations are assigned: TR1 , TR3 ,
and TR5 . The L option on the SI card is required so that the MCNP code
interprets the values as discrete transformation numbers. The option on
the SP and SB cards may be blank, D , or C . For this problem, the
transformations are equally probable, but are biased to sample TR1 20%
of the time, TR3 30% of the time, and TR5 50% of the time.

## 5.8.6.17 Example 16

| SDEF   | TME=D1   |                        |
|--------|----------|------------------------|
| SP1    | -7 2e8   | $ 2e8 shakes=2 seconds |

The source shape will be represented by exponential decay with a half-
life of 2 s.

## 5.8.6.18 Example 17

```
1 999 0 -999 $ cookie cutter cell CCC 2 ... 3 999 SQ 25 100 0 0 0 0 -4 0 0 0 $ surface for cell CCC 4 ... 5 SDEF DIR=1 VEC=0 0 1 X=D1 Y=D2 Z=0 CCC=999 TR=D3 6 SP1 -41 0.470964 0 7 SP2 -41 0.235482 0 8 SI3 L 11 22 33 9 SP3 1 2 3 10 SB3 1 1 1 11 TR11 0 0 -2 1 0 0 0 1 0 0 0 1 12 TR22 -2 0 0 0 1 0 0 0 1 1 0 0 13 TR33 0 -2 0 0.707107 0 0.707107 0.707107 0 -0.707107 0 1 0
```

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

In this example, the source particle coordinates are generated in an
auxiliary coordinate system in the ( x ′ , y ′ , 0) plane around the
origin with a Gaussian profile (FWHM = 0 . 470964 ) in the x ′
coordinate and a Gaussian profile (FWHM = 0 . 235482 ) in the y ′
coordinate. The beam is truncated by 'cookie cutter cell' CCC , which
restricts the source to an ellipse corresponding to two standard
deviations of the Gaussian distributions in the x ′ and y ′ coordinates.
The subsequent application of the transformation TR = D3 results in
three intersecting beams with the following characteristics:

- Beam 1 is centered at (0 , 0 , -2) with the major axis of the beam distribution along the x axis, emitted in the + z direction, with relative intensity 1;
- Beam 2 is centered at ( -2 , 0 , 0) with the major axis of the beam distribution along the y axis, emitted in the + x direction, with relative intensity 2; and
- Beam 3 is centered at (0 , -2 , 0) with the major axis of the beam distribution along the line x = z , emitted in the + y direction, with relative intensity 3.

## 5.8.6.19 Example 18

```
m1 1001 1 8016 1 7016 1e-4 $ Unstable isotope N-16 25054 1e-2 $ Unstable isotope Mn-54 c sdef par=sp pos= 0 0 0 $ Location of material 1 ACT DG=LINES
```

The source is defined as decay gammas from the unstable isotopes 16 N
and 54 Mn in material 1, which is the material located at the user-
provided source position coordinates (0 , 0 , 0) . The two unstable
isotopes will be sampled based on their relative activities within
material 1. The default time ( TME = 0 ) is assumed.

## 5.8.6.20 Example 19

```
mode p # sdef par=N-16 erg=0 pos= 0 0 0 ACT DG=LINES
```

Setting the source particle to the heavy ion 16 N ( PAR = N-16 ) and
specifying the energy of the ion as zero ( ERG = 0 ) defines the source
as the decay gammas of 16 N. The heavy ions will not be transported.
Notice that the heavy-ion symbol, # , appears on the MODE card.

## 5.8.6.21 Example 20

```
adapted from mcnpx _ extended/test27a/inp07/inp07.inp 1 0 -1 imp:n=1 2 0 1 imp:n=0
```

Listing 5.42: example\_embedded\_dist.mcnp.inp.txt

| 1 so          | 0.001                   |
|---------------|-------------------------|
| sdef          | erg 1 cel=1 tme=d41     |
| si41          | S 52<51 (D31<32<d33) 61 |
| sp41          | .1 .8 .1                |
| si51          | A -26 -16               |
| sp51          | 0 1                     |
| si52          | H 0 1 2                 |
| sp52          | 0 1 0                   |
| si61          | A 32 40                 |
| sp61          | 1 0                     |
| si31          | 0 1 2                   |
| sp31          | 0 1 0                   |
| si32          | 0 16                    |
| sp32          | -41 8 8                 |
| si33          | -16 32                  |
| sp33          | 0 1                     |
| f1:n 1        | f1:n 1                  |
| t0 -30 79i 50 | t0 -30 79i 50           |
| nps 1e7       | nps 1e7                 |

The example given in Listing 5.42 illustrates how embedded distributions
can reside within distributions of distributions ( D41 ), and can use
built-in functions ( D32 uses a Gaussian centered at t = 8 with FWHM = 8
) and interpolated distributions ( D51 and D61 use the SI A option).
Distribution D52 is embedded in distribution D51 ; distribution D31 is
embedded in distribution D32 , which is embedded in distribution D33 . A
tally plot of this embedded distribution appears in Fig. 5.10. The tally
plot is created with the MCNP interactive plotter command input file
given in Listing 5.43.

Listing 5.43: example\_embedded\_dist.mcnp.comin.txt

| tfc m   |
|---------|
| free t  |
| end     |
| end     |

## 5.8.6.22 Example 21

```
1 sdef cel=d1 2 si1 L (4<2[-1:1 -2:2 -3:3]<1) 3 sp1 1 104r
```

This source definition creates source particles in a subset of a lattice
using ranges specified for the lattice elements. The lattice must have
been defined using a fully specified FILL card.

## 5.8.6.23 Example 22

| si1 L   |     n | p h     |
|---------|-------|---------|
| sp1 W   | 3e+09 | 5e9 2e9 |

1

2

The source shown here mixes contributions from three source particles
and samples them according to their relative magnitudes (neutrons 30%,
photons 50%, and protons 20%). The weight assigned to each particle will
be the sum of the non-normalized values, 3 × 10 9 +5 × 10 9 +2 × 10 9 =
1 × 10 10 .

1

2

3

4

runtpe = example\_embedded\_dist.mcnp.inp.txtr.h
example\_embedded\_dist.mcnp.inp.txtr.h5

Figure 5.10: MCPLOT plot of tally from -30 to 50 shakes.

<!-- image -->

1

2

## 5.8.6.24 Example 23

| si1   | L   |   sp |   sf |     n |
|-------|-----|------|------|-------|
| sp1   | W   |  -10 |  -15 | 3e+09 |

The spontaneous photon source will look to cell 10 and use the material
and volume to calculate the overall activity that will be substituted
into the SP1 distribution. Correspondingly, the SF source will look to
the material and volume in cell 15 for the intensity of the spontaneous
fission source. Note that a +SF normalizes per spontaneous fission
neutron, a -SF normalizes per spontaneous fission. The neutron source is
unchanged. After the overall activity is computed, the source
distribution normalization will be done as described above and the
weight adjustment value passed into the weight parameter.

## 5.8.6.25 Example 24

| sdef   | par=d1 wgt=264   |
|--------|------------------|
| si1    | L sf             |
| sp1    | w -35            |

1

2

3

If the cell specified in the SP n W option is a lattice cell, then the
code may not know the correct volume for this cell. If the user does not
wish to correct the volume using the VOL card or cell keyword, a WGT
keyword can be used with the source as a multiplicative factor. In this
example, the spontaneous fission source is weighted by the activity from
cell 35, which has been duplicated 264 times in the geometry. The final
source weight will be the activity from cell 35 multiplied by 264.

## 5.8.7 SC: Source Comment

| Data-card Form: SC n comment                      |
|---------------------------------------------------|
| n the distribution number such that 1 ≤ n ≤ 999   |
| comment user-supplied text describing the source. |

Default: No comment.

## Details:

- 1 The comment is printed as part of the header of distribution n in the source distribution table and in the source distribution frequency table. The &amp; continuation symbol is considered to be part of the comment, not a continuation command.

## 5.8.8 SSW: Surface Source Write

This card is used to write a surface source file or KCODE fission volume
source file for use in a subsequent MCNP calculation. Include enough
geometry beyond the specified surfaces to account for albedo effects.

During execution, surface source information is written to the scratch
file WXXA . Upon normal completion, WXXA becomes WSSA . If the
calculation terminates abnormally, the WXXA file will appear instead of
WSSA and must be saved along with the runtape file. The calculation must
be continued for at least one more history. At the subsequent normal
termination, WXXA disappears and the correct surface source file WSSA is
properly written.

<!-- image -->

| Data-card Form: SSW   | s 1 s 2 ( c 1 . . . c J ) s 3 . . . s K keyword = value(s) ...                                                                                                                                                                                    |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| s k                   | Problem surface number, with the appropriate sign to indicate sense of inward or outward particle direction, for which particle-crossing information is to be written to the surface source file WSSA . Macrobody facets are allowed.             |
| c j                   | Problem cell number. A positive entry denotes a cell the particle is entering. A negative entry specifies a cell that particle is leaving. This option provides a means to include only a portion of tracks crossing a certain surface ( 1 , 2 ). |
| SYM = value           | Symmetry option flag. If                                                                                                                                                                                                                          |
| SYM = value           | SYM = 0 no symmetry assumed. (DEFAULT)                                                                                                                                                                                                            |
| SYM = value           | SYM = 1 spherical symmetry assumed. The list of problem surface numbers must contain only one surface and it must be a sphere ( ).                                                                                                                |
| SYM = value           | SYM = 2 write particles to a surface bidirectionally. Otherwise, only particles going out of a positive surface and into a negative surface are recorded.                                                                                         |
| PTY = P 1 P 2 . . .   | Controls tracks to record. If PTY is absent, record all tracks for all particle types. (DEFAULT) Each P i entry is a particle type selected from those listed in Table 4.3.                                                                       |
| CEL = cf 1 cf 2 . . . | List of names of all the cells from which KCODE fission source neutrons are to be written, active cycles only ( 4 , 5 ).                                                                                                                          |

Default:

SYM = 0 ; no PTY keyword (record tracks for all particle types)

Use: Optional.

## Details:

- 1 The SSW card allows a list of one or more cell names, positive or negative, after any of the surface names. The list of cell names must be enclosed in parentheses. If the list of cells is absent, any track that crosses the surface in the 'correct direction' (as specified by the positive or negative sign on the surface number) will be recorded. If the list of cells is present, a track will be recorded if it crosses the surface in the correct direction and is either entering a cell in the list whose entry is positive or leaving a cell in the list whose entry is negative.

1

1

- 2 Problem cell numbers, c j , cannot include chain information; i.e., all cells listed must be at the lowest level. Lattice cells should not be listed because in most cases other cells are filled into a lattice cell. In the rare case that a lattice cell is filled with itself, simply list the lattice cell without any reference to a specific element.
- 3 If the SYM = 1 option is used, the geometry inside the surface must be spherically symmetric and the materials must be symmetric. This symmetric situation only occurs rarely and it is the responsibility of the user to determine whether SYM = 1 is appropriate for the problem. If the SYM = 1 option is invoked, fewer words per particle need to be written to the surface source file and certain biasing options become available when reading the surface source file. The SYM = 1 option cannot be used if CEL is specified.
- 4 Fission volume sources from a KCODE calculation can be written from active cycles only. The fission neutrons and prompt photons can then be transported in a subsequent calculation using the SSR surface source read fixed-source capability. In a KCODE criticality calculation the fission neutron sources and prompt photons produced from fission during each cycle are written to the WSSA surface source file if the SSW card has the CEL keyword followed by the names of all the cells from which fission source neutrons are to be written. Particles crossing specified surfaces can also be written by specifying s k .
- 5 Fission neutrons and photons written to the surface source file in a KCODE calculation can be used as a volume-distributed source in a subsequent calculation. A NONU card should be used so that fission neutrons and photons are not counted twice. Generally a TOTNU card is not required. Total ν is the default for both KCODE and nonKCODE sources. Prompt ν may be invoked by specifying TOTNU NO .

## 5.8.8.1 Example 1

SSW 4 -7 19 (45 -46) 16 -83 (49)

A track that crosses surface 19 in the correct direction will be
recorded only if it is either entering cell 45 or leaving cell 46. A
track that crosses surface 83 in the correct direction will be recorded
only if it is entering cell 49. A track that crosses surface 4, 7, or 16
in the correct direction will be recorded regardless of what cells it
happens to be leaving or entering.

## 5.8.8.2 Example 2

SSW 1 2 (3 4) CEL 8 9

A track that crosses surface 2 in the correct direction will be recorded
only if it enters cell 3 or 4. A track crossing surface 1 in the correct
direction always will be recorded. Particles created from fission events
in cells 8 and 9 will be recorded.

## 5.8.9 SSR: Surface Source Read

This card is used to read a surface source file or KCODE fission volume
source file that was created in a previous MCNP calculation. The file
WSSA must have previously been created using the SSW card; the file must
be renamed to RSSA before it can be read by the SSR feature.

```
1 2
```

The number of particle histories reported in the output file for an SSR
calculation is related to the number written to the WSSA file during the
SSW procedure, so that proper normalization is preserved. However, a
user may specify a different value on the NPS card in the SSR input file
than that used in the initial SSW calculation. If the value of the npp
parameter of the NPS card is smaller than that used in the initial
calculation, an appropriate ratio of tracks will be rejected. If the npp
value is larger than that of the initial calculation, an appropriate
duplication of tracks will be sampled. For example, if the SSW
calculation used an npp value of 100 and the SSR calculation uses an npp
of 200, then every track is duplicated, each with a different random
number seed and each with half the original weight. Note that a larger
value of npp on the SSR calculation will indeed lower the tally errors
until the weight variance contained on the RSSA file dominates.
Therefore, a user should maximize the number of tracks on the RSSA file.
Because the npp value can readjust particle weights as described above,
some variance reduction parameters (e.g., weight-window bounds) may need
to be renormalized for SSR applications.

The problem summary tables for a surface source problem represent the
weights of the particles read from the RSSA file, not the weights in the
original problem that wrote the surface source. To understand the
resultant Problem Summary Tables for an SSR problem, consider the
following example with two calculations in sequence, first:

```
1 MODE N E 2 SSW $ neutrons and electrons written to WSSA file
```

followed by

```
MODE N P E SSR $ no photons available on RSSA to read
```

The weight creation and loss columns for all particles are normalized by
the number of histories run in the problem. For this example, the
neutron and electron average energies are determined by normalizing by
the respective starting source weights from the RSSA file. Because no
photons were available to be read, the photon summary table average
energies will be normalized by the first particle source weight from
RSSA in the problem, where neutrons have first priority (as in this
example), then photons, then electrons, etc.

For the general SSR problem, one or more particle types will have source
weights. The average energies in a particle Problem Summary Table are
obtained in the following order: 1) if source particles are read from
the RSSA file, then the average energies are determined by normalizing
by the starting source weight; else 2) the first particle type with
source weight will be used for obtaining average summary table energies.

Any variance-reduction technique that requires the input of normalized
weight parameters (e.g., weightwindow bounds, negative entries on the DD
card, etc.) may need to be renormalized for SSW / SSR applications.
Consider the following observations and comments:

1. In general, weight-window bounds generated in a SSW calculation are not useful in the SSR calculation, unless the tally identified on the WWG card of the SSW calculation is the same as that desired for the SSR calculation and plenty of tracks contributed to that tally during the SSW calculation.
2. A window generated in an SSR calculation will likely have to be renormalized in subsequent runs that use those windows, unless the value on the NPS card remains unchanged. If the value on the NPS card is changed, the WGT keyword on the SSR card can be used to renormalize the source weights to ensure weights are within the window in the source region. Whenever the WGT keyword is used in this fashion, tallies must be properly normalized by using this value on the SD card or the inverse of this value as a multiplier on the FM card.

| Data-card Form: SSR      | keyword= value(s) ...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | keyword= value(s) ...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| OLD = s 1 s 2 . . . s K  | List of K problem surface numbers that are a subset of the surfaces on the SSW card that created the file WSSA , now called RSSA . Negative entries are not allowed as filtering is not available based on crossing direction. A positive value (as on the SSW card) simply means to accept all tracks that have crossed that surface regardless of direction. (DEFAULT: All surfaces in the original calculation.) Restriction: Macrobody surfaces are allowed.                                                        | List of K problem surface numbers that are a subset of the surfaces on the SSW card that created the file WSSA , now called RSSA . Negative entries are not allowed as filtering is not available based on crossing direction. A positive value (as on the SSW card) simply means to accept all tracks that have crossed that surface regardless of direction. (DEFAULT: All surfaces in the original calculation.) Restriction: Macrobody surfaces are allowed.                                                        |
| CEL = c 1 c 2 . . . c K  | List of K cells numbers that represent a subset of the cells on the SSW card that created the file WSSA , now called RSSA . This subset specifies which fission cells to accept of those from the KCODE calculation that wrote the RSSA file ( 1 ), (DEFAULT: All cells in the original calculation.)                                                                                                                                                                                                                   | List of K cells numbers that represent a subset of the cells on the SSW card that created the file WSSA , now called RSSA . This subset specifies which fission cells to accept of those from the KCODE calculation that wrote the RSSA file ( 1 ), (DEFAULT: All cells in the original calculation.)                                                                                                                                                                                                                   |
| NEW = sa 1 sa 2 . . . sa | K sb 1 sb 2 . . . sb K sm 1 sm 2 . . . sm K Problem surface numbers on which the surface source is to start particles in this run. The K entries may be repeated to start the surface source in multiple ( m ) transformed locations. In other words, for m = 1 , each particle written from surface s k in the OLD list will start on surface s1 k . For m = 2 , each particle written on surface s k in the OLD list will start on surface s2 k , etc. See the TR keyword below. (DEFAULT: Surfaces in the OLD list.) | K sb 1 sb 2 . . . sb K sm 1 sm 2 . . . sm K Problem surface numbers on which the surface source is to start particles in this run. The K entries may be repeated to start the surface source in multiple ( m ) transformed locations. In other words, for m = 1 , each particle written from surface s k in the OLD list will start on surface s1 k . For m = 2 , each particle written on surface s k in the OLD list will start on surface s2 k , etc. See the TR keyword below. (DEFAULT: Surfaces in the OLD list.) |
| PTY = P 1 P 2 . . .      | A blank-delimited list of particle types for which the tracks are to be read. If the PTY keyword is absent, read all tracks for all particle types in the problem ( 2 , 3 ). (DEFAULT: PTY absent.)                                                                                                                                                                                                                                                                                                                     | A blank-delimited list of particle types for which the tracks are to be read. If the PTY keyword is absent, read all tracks for all particle types in the problem ( 2 , 3 ). (DEFAULT: PTY absent.)                                                                                                                                                                                                                                                                                                                     |
| COL                      | Collision option flag. If                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Collision option flag. If                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | COL = -1 start from the surface source file only those particles that came directly from the source without a collision.                                                                                                                                                                                                                                                                                                                                                                                                |
|                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | COL = 1 start from the surface source file only those particles that had collisions before crossing the recording surface.                                                                                                                                                                                                                                                                                                                                                                                              |
|                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | COL = 0 start particles without regard to collisions. (DEFAULT)                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| WGT                      | Each particle weight is multiplied by the constant WGT as it is accepted for transport. (DEFAULT: = )                                                                                                                                                                                                                                                                                                                                                                                                                   | Each particle weight is multiplied by the constant WGT as it is accepted for transport. (DEFAULT: = )                                                                                                                                                                                                                                                                                                                                                                                                                   |
| TR = n or TR = D n       | Transformation number, n . Track positions and velocities are transformed from the auxiliary coordinate system (the coordinate system of the problem that wrote the surface source file) into the coordinate system of the current problem, using the transformation on the TR card, which must be present in the MCNP input file of the current problem ( 4 ).                                                                                                                                                         | Transformation number, n . Track positions and velocities are transformed from the auxiliary coordinate system (the coordinate system of the problem that wrote the surface source file) into the coordinate system of the current problem, using the transformation on the TR card, which must be present in the MCNP input file of the current problem ( 4 ).                                                                                                                                                         |
|                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Distribution number, D n , where 1 ≤ n ≤ 999 . Distribution number for a set of SI , SP , and SB cards. If the surface source is transformed into several locations, the SI card lists the transformation numbers and the SP and SB cards give the probabilities and bias of each transformation, respectively ( 5 ). (DEFAULT: no transformation)                                                                                                                                                                      |
| PSC = c                  | A non-negative constant that is used in an approximation to the PSC evaluation for the probability of the surface source emitting a particle into a specified angle relative to the surface normal ( 6 ).                                                                                                                                                                                                                                                                                                               | A non-negative constant that is used in an approximation to the PSC evaluation for the probability of the surface source emitting a particle into a specified angle relative to the surface normal ( 6 ).                                                                                                                                                                                                                                                                                                               |

The following four keywords are used only with spherically symmetric
surface sources, that is, sources generates with SYM = 1 on the SSW
card.

| AXS = u v w   | Direction cosines that define an axis through the center of the surface sphere in the auxiliary (original) coordinate system. This is the reference vector for EXT . (DEFAULT: No axis)                                                                                                                                                                                                                                                                                                                                                                         |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EXT = D n     | Distribution number ( 1 ≤ n ≤ 999 ) ( SI , SP , and SB cards) that will bias the sampling of the cosine of the angle between the direction AXS and the vector from the center of the sphere to the starting point on the sphere surface. (DEFAULT: No position bias)                                                                                                                                                                                                                                                                                            |
| POA = c       | Particles with a polar angle cosine relative to the source surface normal that falls between 1 and c will be accepted for transport. All others are disregarded and no weight adjustment is made. (DEFAULT: POA = 0 )                                                                                                                                                                                                                                                                                                                                           |
| BCW = r zb ze | All particles with acceptable polar angles relative to the surface normal are started so that they will pass through a cylindrical window of radius r , starting at zb from the center of the source sphere and ending at ze from the center. The axis of the cylinder is parallel to the z axis of the auxiliary (original) coordinate system and contains the center of the source sphere. The weight of each source particle is adjusted to compensate for this biasing of position and direction. (DEFAULT: No cylindrical window) Restriction: 0 < zb < ze |

Use: Required for surface source problems.

## Details:

- 1 Problem cell numbers, c k , cannot include chain information; i.e., all cells listed must be at the lowest level. When a source point is kept for transport, the code determines the cell(s) for all higher levels in the geometry, based on its absolute location (i.e., ( x, y, z ) position).
- 2 By default, all particle types defined with the MODE card are read from the RSSA file if available. Particle types not defined with the MODE card are rejected without weight adjustment. Particle types can be selected from the RSSA file using the PTY keyword.
- 3 When heavy ions are specified in the problem, the charge and mass for each heavy ion are stored in the surface source file, WSSA , and will be read back to reconstruct the proper source distribution.
- 4 For each surface s k in the OLD list, a corresponding surface s1 k must appear in the NEW list such that TR n transforms the coordinates of a particle written from s k to be on surface s1 k in the current problem. However, if the surfaces s1 k are 'dummy' surfaces not used in constructing the real geometry, then the transformed source will effectively be treated as a volume source not specifically defined to be on any surface.
- 5 If NEW is present with multiple ( m&gt; 1 ) transformed locations, then the distribution must specify exactly m transformations that properly represent the relationship of the m × K surfaces on the NEW list to the K surfaces on the OLD list. Otherwise, the NEW specification is ignored (if present) and the application of TR = D n is analogous to its use on the SDEF card. The source after transformation is treated as a volume source (surface number not defined); the cell for the source particle is determined after transformation. It may be wise not to place the transformed source exactly on a surface of the physical geometry (to avoid lost particles in some cases).

1

- 6 An exact treatment of point detectors or DXTRAN spheres with a surface source is not possible because the p (cos θ ) values required for the source contribution are not readily available. To use detectors or DXTRAN with a surface source, an approximate p (cos θ ) must be specified on the SSR card. The most common azimuthally symmetric approximation for an angular emission probability density function is given by

<!-- formula-not-decoded -->

The PSC value entered is c , the power to which p (cos θ ) is raised. C
c is a normalization constant calculated in the MCNP code and θ is the
angle between the direction vector to the point detector and the surface
normal at the point where the particle is to be started. Because surface
crossings are recorded in only one direction specified on the SSW card,
the limits on µ = cos( θ ) are always between 1 and 0. A PSC entry of
zero specifies an isotropic angular distribution on the surface. An
entry of 1 specifies a cosine angular distribution that produces an
isotropic angular flux on the surface. In the case of a 1-D spherical
surface source of radius R , a cosine distribution is adequate if the
point detector or DXTRAN sphere is more than 4 R away from the source.

## /warning\_sign Caution

Remember that the value entered for PSC is only an approximation. If the
point detector or DXTRAN sphere is close to the source sphere and the
approximation is poor, the answers will be wrong.

## 5.8.9.1 Example 1

Original calculation:

```
SSW 1 2 3
```

Current calculation:

```
1 SSR OLD 3 2 NEW 6 7 12 13 TR D5 COL 1 2 SI5 L 4 5 3 SP5 0.4 0.6 4 SB5 0.3 0.7
```

Particles starting on surface 1 in the original calculation will not be
started in the current calculation because surface 1 is absent from the
list of OLD surface numbers. Particles recorded on surface 2 in the
original calculation will be started on surfaces 7 and 13, and particles
recorded on surface 3 in the original calculation will be started on
surfaces 6 and 12, as prescribed by the mapping from the OLD to the NEW
surface numbers. The COL keyword causes only particles that crossed
surfaces 2 and 3 in the original problem after having undergone
collisions to be started in the current problem. The TR entry indicates
that distribution function 5 describes the required surface
transformations. According to the SI 5 card, surfaces 6 and 7 are
related to surfaces 3 and 2, respectively, by transformation TR4 ;
surfaces 12 and 13 are related to 3 and 2 by TR5 . The physical
probability of starting on surfaces 6 and 7 is 40% according to the SP5
card, and the physical probability of starting on surfaces 12 and 13 is
60%. The SB5 card causes the particles from surfaces 3 and 2 to be
started on surfaces 6 and 7 30% of the time with weight multiplier 4 / 3
and to be started on surfaces 12 and 13 70% of the time with weight
multiplier 6 / 7 .

## 5.8.9.2 Example 2

Original calculation:

```
1 SSW 3 SYM 1
```

Current calculation:

| SSR   |   AXS |   0 0 1 | EXT D99   |
|-------|-------|---------|-----------|
| SI99  | -1    |     0.5 | 1         |
| SP99  |  0.75 |     1   |           |
| SB99  |  0.5  |     0.5 |           |

All particles written to surface 3 in the original problem will be
started on surface 3 in the new problem, which must be exactly the same
because no OLD , NEW , COL , or TR keywords are present. Because this is
a spherically symmetric problem, indicated by the SYM 1 flag in the
original calculation, the position on the sphere can be biased. It is
biased in the z direction with a cone bias described by distribution 99.

## 5.8.9.3 Example 3

Original calculation:

```
1 SSW 2 4 6
```

Current calculation:

```
1 SSR OLD 2 TR=D1 WGT 6.0 2 SI1 L 11 22 33 3 SP1 1 2 3 4 SB1 1 1 1 5 TR11 0 0 -3 1 0 0 0 1 0 0 0 1 6 TR22 -3 0 0 0 1 0 0 0 1 1 0 0 7 TR33 0 -3 0 0.707 0 0.707 0.707 0 -0.707 0 1 0
```

All particles written from surface 2 in the original problem will be
accepted; those written from surfaces 4 and 6 will be rejected. The
distribution D1 will be sampled for each accepted particle and one of
the transformations TR11 , TR22 , or TR33 will be applied. In this case,
the particle current across surface 2 in the original problem will be
applied as three intersecting beams in the x , y , and z directions. The
relative intensities are 2 : 3 : 1 respectively, but the sampling rate
is the same in all three directions through use of the SB card.

## 5.8.10 KCODE: Criticality Source

The KCODE card specifies the MCNP criticality source that is used for
determining k eff . The criticality source uses total fission ν values
unless overridden by a TOTNU NO card and applies only to neutron
problems.

In a MODE N P problem, secondary photon production from neutrons is
turned off during inactive cycles. SSW particles are not written during
inactive cycles.

Fission sites for each cycle are those points generated by the previous
cycle. For the initial cycle, fission sites can come from an SRCTP file
from a similar geometry, from a KSRC card, or from a volume distribution
specified by an SDEF card.

Since the mid-2000s, there have been many detailed studies on the theory
and practice of performing Monte Carlo criticality calculations. These
studies have resulted in a set of 'best practices' for performing KCODE
calculations with the MCNP code. Best practices are discussed in
[294-300] and in older documents including [295-300]. To summarize these
reports:

Convergence of the fission source shape should be assessed with plots of
the Shannon entropy vs. cycle. To avoid bias from the renormalization of
the fission source each cycle, it is very strongly recommended that at
least 10,000 neutrons/cycle should be specified on the KCODE card, with
even larger numbers for large reactor problems. The initial guess for
the source distribution (via KSRC , SRCTP , or SDEF ) should be a
reasonable representation covering the fissionable regions of a problem.

<!-- image -->

| Data-card Form: KCODE   | nsrck rkk ikz kct msrk knrm mrkp kc8                                                                                                                  |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| nsrck                   | Number of source histories per cycle ( 1 ). (DEFAULT: nsrck = 1000 )                                                                                  |
| rkk                     | Initial guess for k eff ( 2 ). (DEFAULT: rkk = 1.0 )                                                                                                  |
| ikz                     | Number of cycles to be skipped before beginning tally accumulation. (DEFAULT: ikz = 30 )                                                              |
| kct                     | Total number of cycles to be done. If kct = 0 , never terminate on the number of cycles, but terminate on time [§3.2.5.6]. (DEFAULT: kct = ikz +100 ) |
| msrk                    | Number of source points for which to allocate storage ( 3 ). (DEFAULT: msrk = maximum of 4500 or 2 × nsrck )                                          |
| knrm                    | Controls normalization of tallies. If                                                                                                                 |
| mrkp                    | Maximum number of cycle values on MCTAL or RUNTPE files. (DEFAULT: mrkp = 6500 )                                                                      |
| kc8                     | Controls the number of cycles over which summary and tally information are averaged. If                                                               |
| kc8                     | kc8 = 0 average over all cycles. ( 4 )                                                                                                                |
| kc8                     | kc8 = 1 average over active cycles only. (DEFAULT)                                                                                                    |

Use: Required for criticality calculations.

## Details:

- 1 The default approach is to allow the histories per cycle to fluctuate around this value from generation to generation. If any tallies are performed with batch statistics (such as FMESH with the tally = batch option), the number of source particles in the fission bank will be resampled at each generation to precisely

nsrck particles to ensure the validity of the statistics. This will
change the random number sequence but will yield statistically
equivalent results.

- 2 If in the first cycle the source being generated overruns the current source, the initial guess ( rkk ) is probably too low. The code then proceeds to print a comment, continues without writing a new source, calculates k ′ eff , reads the initial source back in, and begins the problem using k ′ eff instead of rkk . If the generated source again overruns the current source after the first cycle, the calculation terminates and either a better initial guess ( rkk ) or more source space ( msrk ) should be specified on the next try.
- 3 If an SRCTP file with a larger value of msrk is read for the initial source, the larger value is used.
- 4 Setting the parameter kc8 to zero causes tallies and summary table information to be for both active and inactive cycles and should not be used. Setting kc8 = 0 also results in strange MCTAL file normalization, as these are normalized by active cycles.

## 5.8.11 KSRC: Criticality Source Points

This card contains up to nsrck ( x, y, z ) triplets that are locations
of initial source points for a KCODE calculation. At least one point
must be in a cell containing fissile material and points must be away
from cell boundaries. It is not necessary to input all nsrck coordinate
points. The MCNP code will start approximately nsrck / ( number of
points ) particles at each point. Usually one point in each fissile
region is adequate, because the MCNP code will quickly calculate and use
the new fission source distribution. The energy of each particle in the
initial source is sampled from a Watt fission spectrum hardwired into
the MCNP code, with a = 0 . 965 MeV, b = 2 . 29 MeV -1 .

A SRCTP file from a previous criticality calculation can be used instead
of a KSRC card. If the current problem has a lot in common with the
previous problem, using the SRCTP file may save some computer time. Even
if the problems are quite different, the SRCTP file may still be usable
if some of the points in the SRCTP file are in cells containing fissile
material in the current problem. Points in void or zero importance cells
will be deleted. The number of particles actually started at each point
will be such as to produce approximately nsrck initial source particles.

An SDEF card also can be used to sample initial source points in fissile
material regions. The SDEF card parameters applicable to volume sampling
can be used: CEL , POS , RAD , EXT , AXS , X , Y , Z ; and CCC , ERG ,
and EFF . If a uniform volume distribution is chosen, the early values
of k eff will likely be low because too many particles are put near
where they can escape, just the opposite of the usual situation with the
KSRC card. Do not change the default value of WGT for a KCODE
calculation.

```
Data-card Form: KSRC x 1 y 1 z 1 x 2 y 2 z 2 . . . x K y K z K x k y k z k the locations of the initial source points.
```

Default: None. If this card is absent, an SRCTP source file or SDEF card
must be supplied to provide initial source points for a criticality
calculation.

Use: Optional card for use with criticality calculations.

## 5.8.12 KOPTS: Criticality Calculations Options

By invoking options on the KOPTS card, a number of features can be
enabled. These mainly cluster into point-kinetics calculations and
fission matrix acceleration.

For the point-kinetics parameters, the MCNP code can calculate the
following parameters for criticality: the neutron generation time ( Λ ),
the effective delayed neutron fraction ( β eff ), and Rossiα . The MCNP
code computes the point-kinetics parameters in a forward calculation
with only the existing random walks by breaking the active cycles of a
KCODE calculation into sequential blocks of fission generations. For
best results of the KOPTS card, the system should be as near critical (
k eff = 1 ) as possible.

For the fission matrix acceleration, k -eigenvalue problems can be
accelerated by computing the eigenvalues of the fission matrix and
weighting the inactive cycle source distribution by these eigenvalues.
This can substantially improve the rate of convergence on a wide variety
of problems [301]. In addition, it can be used to determine if a k
-eigenvalue problem is poorly converged using a variety of statistical
comparisons.

The fission matrix requires a mesh in order to operate. In addition, the
statistical tests require the Shannon entropy mesh to match as well.
There are three ways to give the MCNP code a mesh for this purpose. The
first is to explicitly specify one on the HSRC card. The second is to
set the FMATNX , FMATNY , and FMATNZ values, in which the extent of the
bounding box is computed from the end-of-first-batch fission source
distribution and subdivided using these values. Finally, if neither the
HSRC card or the FMATN * values are specified, the MCNP code will
generate a mesh by finding the bounding box from the end-of-first-batch
fission source distribution and subdividing it by the fission-to-fission
mean free path in each direction. In all cases, if source particles are
found outside this mesh, it will be automatically expanded.

| Data-card Form: KOPTS   | keyword = value(s) ...                                                                                                                                                 | keyword = value(s) ...                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BLOCKSIZE = ncy         | Controls the number of cycles in every outer iteration. Number of cycles, ncy , in blocks for adjoint weighting ( 1 , 2 , 3 ). (DEFAULT: ncy = 10 ) Restriction: n ≥ 2 | Controls the number of cycles in every outer iteration. Number of cycles, ncy , in blocks for adjoint weighting ( 1 , 2 , 3 ). (DEFAULT: ncy = 10 ) Restriction: n ≥ 2                                                                                                                                                                                                                                                                                                   |
| KINETICS = value        | If                                                                                                                                                                     | If                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|                         | KINETICS = YES                                                                                                                                                         | calculate point-kinetics parameters.                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                         | KINETICS = NO                                                                                                                                                          | do not calculate point-kinetics parameters. (DEFAULT)                                                                                                                                                                                                                                                                                                                                                                                                                    |
| PRECURSOR = value       | If                                                                                                                                                                     | If                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|                         | PRECURSOR = YES                                                                                                                                                        | calculate detailed precursor information.                                                                                                                                                                                                                                                                                                                                                                                                                                |
|                         | PRECURSOR = NO                                                                                                                                                         | do not calculate detailed precursor information ( 4 ). (DEFAULT)                                                                                                                                                                                                                                                                                                                                                                                                         |
| KSENTAL = fileopt       | Select format of sensitivity profiles output file, KSENTAL ( 5 ). If                                                                                                   | Select format of sensitivity profiles output file, KSENTAL ( 5 ). If                                                                                                                                                                                                                                                                                                                                                                                                     |
|                         | KSENTAL = MCTAL                                                                                                                                                        | write the sensitivity profiles in a MCTAL -like file, from which the profiles may be plotted using MCPLOT ( 6 ).                                                                                                                                                                                                                                                                                                                                                         |
|                         | no format is specified                                                                                                                                                 | print no file. (DEFAULT)                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| FMAT = value            |                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|                         | FMAT = YES                                                                                                                                                             | compute the fission matrix. Statistical tests on the convergence of the fission matrix, the convergence of the Shannon entropy, and the distributions of both relative to each other will be performed and reported to the user. This will include information on whether or not the statistical tests indicate that the problem is converged, as well as possible undersampling issues. For those interested in analyzing the resulting fission matrix, it is available |

|                          |                                                                                                                                                                                                                                | as a 0-indexed compressed-sparse-row (CSR) matrix in the results section of the runtape (see §D.5).                                                                                                                                                                                                                         |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                          | FMAT = NO                                                                                                                                                                                                                      | do not compute the fission matrix. (DEFAULT)                                                                                                                                                                                                                                                                                |
| FMATCONVRG = value       |                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                             |
|                          | FMATCONVRG = YES                                                                                                                                                                                                               | the ikz option of KCODE will be ignored and instead, the statistical tests described above will be used to determine when to enable active cycles.                                                                                                                                                                          |
|                          | FMATCONVRG = NO                                                                                                                                                                                                                | do not use the fission matrix to determine convergence. (DEFAULT)                                                                                                                                                                                                                                                           |
| FMATACCEL = value        |                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                             |
|                          | FMATACCEL = YES                                                                                                                                                                                                                | the eigenvalues of the fission matrix will be used to weight the importances of the fission sources in the problem during inactive cycles. This can be used to converge difficult problems more quickly. This option operates better with more particles per batch, as the matrix fills out quicker and has lower variance. |
|                          | FMATACCEL = NO                                                                                                                                                                                                                 | do not use the fission matrix to determine convergence. (DEFAULT)                                                                                                                                                                                                                                                           |
| FMATSRC = value          |                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                             |
|                          | FMATSRC = YES or AUTO                                                                                                                                                                                                          | FMATSRC = YES or AUTO                                                                                                                                                                                                                                                                                                       |
|                          |                                                                                                                                                                                                                                | sample source particles uniformly from within the fission matrix mesh. KSRC and SDEF are ignored. Requires a mesh to be explicitly input on an HSRC card.                                                                                                                                                                   |
|                          | FMATSRC = NO                                                                                                                                                                                                                   | do not automatically generate a source. (DEFAULT)                                                                                                                                                                                                                                                                           |
| FMATSKIP = fmat _ skip   |                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                             |
|                          | Skips this many batches before accumulating fission matrix tallies. (DEFAULT )                                                                                                                                                 | Skips this many batches before accumulating fission matrix tallies. (DEFAULT )                                                                                                                                                                                                                                              |
| FMATNCYC = fmat _ ncyc   |                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                             |
|                          | Batches between fission matrix solves. Larger values allow more fission matrix tallies to occur, improving stability, whereas smaller values can allow a problem to converge faster when used in acceleration. (DEFAULT = 10 ) | Batches between fission matrix solves. Larger values allow more fission matrix tallies to occur, improving stability, whereas smaller values can allow a problem to converge faster when used in acceleration. (DEFAULT = 10 )                                                                                              |
| FMATSPACE = fmat _ space | FMATSPACE = fmat _ space                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                             |
|                          | Initial number of nonzero elements to allocate the fission matrix to store. If exceeded, the MCNP code will dynamically reallocate the arrays. (DEFAULT = 100000000 )                                                          | Initial number of nonzero elements to allocate the fission matrix to store. If exceeded, the MCNP code will dynamically reallocate the arrays. (DEFAULT = 100000000 )                                                                                                                                                       |
| FMATNX = fmat _ nx       | Ignored with an HSRC card. If not zero, compute the x -axis mesh spacing by subdividing the end-of-first-batch fission source extent by this number. (DEFAULT )                                                                | Ignored with an HSRC card. If not zero, compute the x -axis mesh spacing by subdividing the end-of-first-batch fission source extent by this number. (DEFAULT )                                                                                                                                                             |
| FMATNY = fmat _ ny       | Ignored with an HSRC card. If not zero, compute the y -axis mesh spacing by subdividing the end-of-first-batch fission source extent by this number. (DEFAULT = 0 )                                                            | Ignored with an HSRC card. If not zero, compute the y -axis mesh spacing by subdividing the end-of-first-batch fission source extent by this number. (DEFAULT = 0 )                                                                                                                                                         |

1

1

FMATNZ = fmat \_ nz

## Details:

- 1 Specification of BLOCKSIZE without setting KINETICS = YES is allowed, but the MCNP code will try to do adjoint weighting without tallying anything.
- 2 The default block size of 10 cycles produces results with sufficient accuracy for most problems of interest. Using fewer cycles per block introduces greater bias from truncation, but provides a more statistically efficient calculation. Larger blocks are more accurate, but the accuracy gained for larger block sizes is often small relative to the increased computer time required to preserve the statistical precision. Users are encouraged to check whether the selected block size is sufficient for their application by running a larger block size and comparing the results. For small, leakage-dominated systems, the block size can often be reduced to 5.
- 3 Because sensitivity coefficients (see the KSEN card) are adjoint weighted, they theoretically require infinitely many cycles before a tally may be performed. In practice, the default BLOCKSIZE value of 10 generations is usually more than sufficient to get accurate results.
- 4 If PRECURSOR = YES , then KINETICS must be set to YES .
- 5 The KSENTAL keyword requires there be at least one KSEN card specified in the MCNP input file.
- 6 The MCTAL format of the sensitivity profiles is much like the standard MCTAL file except that the symbols for bins have different meanings: F = cells (with 0 denoting all cells); D = unused; U = unused ; S = isotopes; M = reaction numbers; C = cosine bins; E = energy bins; and T = incident energy bins (for fission χ or scattering laws). The tally plotter, MCPLOT , may be loaded to plot these results. The results should be normalized to be per unit lethargy with the ' LETHARGY ' option and plotted on a semi log-x scale for visually accurate area plots [§6.5].

## 5.8.12.1 Example 1

## KOPTS BLOCKSIZE=15 KINETICS=YES PRECURSOR=YES

Both standard kinetics parameters and detailed precursor information are
requested. Because the BLOCKSIZE value is not the default, we assume the
user determined from empirical studies that 15 generations per block are
needed for the application.

## 5.8.12.2 Example 2

KOPTS FMAT=YES FMATCONVRG=YES

This will compute the fission matrix and use it to determine when to
enable active cycles. The fission matrix mesh will be determined either
from an HSRC card if present or from the first batch if not present.

Ignored with an HSRC card. If not zero, compute the z -axis mesh spacing
by subdividing the end-of-first-batch fission source extent by this
number. (DEFAULT = 0 )

1

1

## 5.8.12.3 Example 3

KOPTS FMAT=YES FMATCONVRG=YES FMATACCEL=YES

This is identical to the previous example, except the fission matrix is
used to accelerate the convergence of the problem.

## 5.8.12.4 Example 4

KOPTS FMAT=YES FMATNX=5 FMATNY=5 FMATNZ=5

If there is no HSRC card, the fission matrix will be computed on a mesh
that is initially 5 × 5 × 5 . The extent of the mesh is computed from
the fission source distribution at the end of the first batch. The mesh
will be extended as necessary throughout simulation.

## 5.8.13 HSRC: Mesh for Shannon Entropy of Fission Source Distribution

To assist users in assessing the convergence of the fission source
distribution, the MCNP code computes a quantity called the Shannon
entropy of the fission source distribution, H src . To compute H src ,
it is necessary to superimpose a 3-D grid on a problem encompassing all
of the fissionable regions, and then to tally the number of fission
sites in a cycle that fall into each of the grid boxes. The user may
specify a particular grid to use in determining H src by means of the
HSRC input card. If the HSRC card is provided, users should use a small
number of grid boxes (e.g., 5-10 in each of the x , y , and z
directions), chosen according to the symmetry of the problem and layout
of the fuel regions.

If the HSRC card is not provided, the MCNP code will automatically
generate a mesh for use with Shannon entropy. The fission matrix
capability on the KOPTS card will generate a mesh as described there
that is usable for both the fission matrix and for entropy calculations.
If the fission matrix capability is not enabled, the number of grid
boxes will be determined by dividing the number of histories per cycle
by 20 and then finding the nearest integer for each direction that will
produce this number of equal-sized grid boxes, although not fewer than 4
× 4 × 4 will be used. If the grid is automatically determined by the
MCNP code, it will be expanded as necessary if fission source sites for
a cycle fall outside of the grid. The grid size will not be reduced. If
the grid is provided by the user using the HSRC card, then the MCNP code
will issue warning messages either if 90% of the grid-boxes have zero
scores for a cycle or if 25% of the fission source is located outside of
the grid. Either of these messages is an indication that the user-
supplied grid was poorly chosen for computing H src . While H src may
not be computed reliably, there is no effect on k eff or other tallies.

| Data-card Form:   | HSRC n x x min x max n y y min y max n z z min z max   |
|-------------------|--------------------------------------------------------|
| x min             | Minimum x value for mesh.                              |
| x max             | Maximum x value for mesh.                              |
| n y               | Number of mesh intervals in y direction, n y > 0 .     |
| y min             | Minimum y value for mesh.                              |

```
y max Maximum y value for mesh. n z Number of mesh intervals in z direction, n z > 0 . z min Minimum z value for mesh. z max Maximum z value for mesh.
```

Default: None. If this card is absent, if fewer than nine entries are
supplied, or if n x × n y × n z ≤ 0 , the MCNP code will automatically
create a mesh that encloses all of the fission source sites in a cycle.
This automatic mesh will be expanded if necessary on later cycles. The
minimum number of mesh cells for the automatic mesh is 4 × 4 × 4 . If
the HSRC card is supplied, one or more intervals may be specified for
each of the x , y , and z directions.

Use: Optional card to specify the mesh for computing Shannon entropy of
the fission source distribution in criticality calculations.

## 5.8.14 BURN: Depletion/Burnup (KCODE Problems Only)

Requirement: The CINDER.dat library file contains decay, fission yield,
and 63-group cross-section data not calculated by the MCNP code. This
library file must be present and accessible by the MCNP code for the
burnup capability to work properly. To be accessible, the CINDER.dat
file must reside in either the working directory or the DATAPATH .

MCNP depletion is a linked process involving steady-state flux
calculations in the MCNP code and nuclide depletion calculations in
CINDER90. The MCNP code runs a steady-state calculation to determine the
system eigenvalue, 63-group fluxes, energy-integrated reaction rates,
fission multiplicity ( ν ), and recoverable energy per fission ( Q
values). CINDER90 then takes those MCNP-generated values and performs
the depletion calculation to generate new atom densities for the next
time step. The MCNP code takes these new atom densities and generates
another set of fluxes and reaction rates. The process repeats itself
until after the final time step specified by the user.

Steady-state particle transport in the MCNP code includes only those
isotopes listed on the material cards, selected from a fission product
tier (presented in Table 5.16), or produced by the isotope generator
algorithm. This algorithm captures only the daughter reactions and a few
other residual reactions of the isotopes specified on the materials
card; not the entire isotope decay chain. These daughter products are
depicted in Fig. 5.11, which provides the relative locations of the
products of various nuclear processes on the Chart of the Nuclides. To
track the buildup of additional decay-chain isotopes in the transport
calculation, the code adds the isotopes must be listed on the material (
M ) card. If decay-chain isotopes of interest are not initially present,
the user must add these nuclides to the material card ( M ) with low
atomic/weight fraction values ( f i ) (e.g., 10 -36 ).

Table 5.16: Fission Product Content Within Each Burnup Tier

|   Tier 1 | Tier 2                                    | Tier 3                                                                                          |
|----------|-------------------------------------------|-------------------------------------------------------------------------------------------------|
|       74 | As 75 As                                  | 69 Ga 71 Ga 70 Ge 72 Ge 73 Ge 74 Ge 76 Ge 74 As 75 As 74 Se 76 Se 77 Se 78 Se 79 Se 80 Se 82 Se |
|       78 | 79 Br 81 Br 80 Kr 82 Kr 83 Kr 84 Kr 86 Kr | 79 Br 81 Br 78 Kr 80 Kr 82 Kr 83 Kr 84 Kr 85 Kr 86 Kr                                           |

continued on next page. . .

Table 5.16, continued

| Tier 1                   | Tier 2                                                                                                                                                                                               | Tier 3                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 93 Zr 95 Mo 99 Tc 101 Ru | 85 Rb 87 Rb 89 Y 90 Zr 91 Zr 92 Zr 93 Zr 94 Zr 96 Zr 93 Nb 95 Mo 99 Tc 101 Ru 103 Ru 103 Rh 102 Pd 104 Pd 105 Pd 106 Pd 108 Pd 110 Pd 107 Ag 109 Ag 106 Cd 108 Cd 110 Cd 111 Cd 112 Cd 113 Cd 120 Sn | 85 Rb 86 Rb 87 Rb 84 Sr 86 Sr 87 Sr 88 Sr 89 Sr 90 Sr 89 Y 90 Y 91 Y 90 Zr 91 Zr 92 Zr 93 Zr 94 Zr 95 Zr 96 Zr 93 Nb 94 Nb 95 Nb 92 Mo 94 Mo 95 Mo 96 Mo 97 Mo 98 Mo 99 Mo 100 Mo 99 Tc 96 Ru 98 Ru 99 Ru 100 Ru 101 Ru Ru 103 Ru 104 Ru 105 Ru 106 Ru 103 Rh 105 Rh 102 Pd 104 Pd 105 Pd 106 Pd 107 Pd 108 Pd 110 Pd 107 Ag 109 Ag 111 Ag 106 Cd 108 Cd 110 Cd 111 Cd 112 Cd 113 Cd 114 Cd 116 Cd 113 In 115 In 112 Sn 113 Sn 114 Sn 115 Sn 116 Sn |
| 131 Xe 134 Xe            | I I I 124 Xe 126 Xe 128 Xe 129 Xe 130 Xe 131 Xe 132 Xe 134 Xe 135 Xe 136 Xe                                                                                                                          | 102 117 Sn 118 Sn 119 Sn 120 Sn 122 Sn                                                                                                                                                                                                                                                                                                                                                                                                              |
|                          | 127 129 135 141 Pr 143 Nd 145 Nd 147 Nd 148 Nd                                                                                                                                                       | 123 Sn 124 Sn 125 Sn 126 Sn 121 Sb 123 Sb 124 Sb 125 Sb 126 Sb 120 Te 122 Te 123 Te 124 Te 125 Te 126 Te 128 Te 130 Te 132 Te 127 I 129 I 130 I 131 I 135 I 123 Xe 124 Xe 126 Xe 129 Xe 130 Xe                                                                                                                                                                                                                                                      |
| Nd 145 Nd                | 147 Pm 148 Pm 149 Pm                                                                                                                                                                                 | 142 Nd 143 Nd 144 Nd 145 Nd 146 147 Nd 148 Nd 150 147 Pm 148 Pm 149 Pm 151 144 Sm 147 Sm 148 Sm 149 Sm 150 151 Sm 152 Sm 153 Sm 154 151 Eu 152 Eu 153 Eu 154 Eu 155                                                                                                                                                                                                                                                                                 |
| 133 Cs 137 Cs 138 Ba     | 133 Cs 134 Cs 135 Cs 136 Cs 137 Cs 138 Ba                                                                                                                                                            | 131 Xe 132 Xe 133 Xe 134 Xe 135 Xe 136 Xe 133 Cs 134 Cs 135 Cs 136 Cs 137 Cs 130 Ba 132 Ba 133 Ba 134 Ba 135 Ba 136 Ba 137 Ba 138 Ba 140 Ba                                                                                                                                                                                                                                                                                                         |
| 141 Pr 143               | 147 Sm 149 Sm 150 Sm 151 Sm 152 Sm                                                                                                                                                                   | 138 La 139 La 140 La 136 Ce 138 Ce 139 Ce 140 Ce 141 Ce 142 Ce 143 Ce 144 Ce 141 Pr 142 Pr 143 Pr Nd Nd                                                                                                                                                                                                                                                                                                                                             |
|                          | 151 Eu 152 154 155 156 157                                                                                                                                                                           | Pm Sm Sm Eu                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|                          | Gd Gd Gd Gd Gd 158 Gd 160 Gd                                                                                                                                                                         | 156 Eu 157 Eu 152 Gd 153 Gd 154 Gd 155 Gd 156 157 Gd 158 Gd 160                                                                                                                                                                                                                                                                                                                                                                                     |
|                          |                                                                                                                                                                                                      | Gd Gd 159 160                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|                          |                                                                                                                                                                                                      | Tb Tb 156 Dy 158 Dy 160 Dy 161 Dy 162 Dy 163 Dy 164 Dy                                                                                                                                                                                                                                                                                                                                                                                              |
|                          | 165 Ho                                                                                                                                                                                               | 165 Ho 162 Er 164 Er 166 Er 167 Er 168 Er                                                                                                                                                                                                                                                                                                                                                                                                           |

n: neutron

p: proton

d: deuteron

t: triton

γ

: gamma ray

α :

alpha particle

β - :

electron

β +

: positron

ε

:

electron capture

Figure 5.11: Nuclides selected for inclusion by the Isotope Generator Algorithm

<!-- image -->

When the information is not specified by the MCNP code, CINDER90 uses
inherent intrinsic cross-section and decay data to track the time-
dependent reactions of 3400 nuclides. The MCNP code can only track
energy-integrated reaction-rate information for isotopes containing
transport cross sections. For isotopes not containing transport cross-
section information, the MCNP code calculates a 63-group flux that is
sent to CINDER90. This flux data then is matched with a 63-group cross-
section set inherent within CINDER90 to generate 63-group reaction
rates. These resultant reaction rates are then energy integrated to
determine the total reactions occurring.

Burnup is given in units of gigawatt days (GWD) per metric tons of
uranium (MTU), where MTU is the sum of masses of isotopes containing ≥
90 protons.

```
Data-card Form: BURN keyword = value(s) ... TIME = t 1 t 2 . . . Incremental time duration t i for each successive burn step. Time unit is days. ( 1 ) (DEFAULT: A single one-day time step) PFRAC = f 1 f 2 . . . Fraction f i of total system power to be applied to the corresponding time step t i . A power fraction of zero will perform decay without computing the corresponding reaction rates. Caution: If the number of entries in the PFRAC keyword is less than in the TIME keyword, the missing entries will be given a power fraction of zero. (DEFAULT: f i = 1 for all t i ) POWER = pwr Total recoverable fission system power in MW. (DEFAULT: pwr = 1 ) MAT = m 1 m 2 . . . List of materials to participate in the burnup calculation. Each ID corresponds to the ID on an M card. Positive m i will be transmuted during the simulation and used to compute heating for power normalization. Negative m i will be used only to compute heating for power normalization and will not be transmuted. ( 2 , 9 ) OMIT = m 1 n 1 [omitted targets] 1 m 2 n 2 [omitted targets] 2 . . . For material m i , omit n i targets [§1.2.2] as listed in [omitted targets] i from the transport calculation. All formats are supported. This is primarily used to remove nuclides that are part of the decay chain but do not have cross sections available. If m i is -1 , then this applies to all materials listed in the MAT keyword. AFMIN = af 1 af 2 Atom fraction controls. af 1 is the atom fraction below which nuclides are not tracked. If a nuclide atom fraction goes below this limit, the atom fraction is set to zero. (DEFAULT: af 1 = 10 -10 ) af 2 is the transmutation chain convergence criteria used in CINDER90. (DEFAULT: af 2 = 10 -10 ) BOPT = b 1 b 2 b 3 Burnup options. b 1 is the Q value multiplier. (DEFAULT: b 1 = 1 , ) b 2 is used to control the ordering and content of the output. It is the additive result of two integer values: b 2 = I 1 + I 2 . The first value, I 1 , selects among three tiers (see Table 5.16) of fission product content: If I 1 = 0 , include only Tier 1 fission products (DEFAULT).
```

b

3

- If I 1 = 10 , include Tier 2 fission products, which is more comprehensive than Tier 1.

If I 1 = 20 , include Tier 3 fission products, which is more
comprehensive than Tier 2. Tier 3 includes all fission products in the
ENDF/B-VII.0 library that have CINDER90 yield information.

The second value I 2 selects among four ordering options:

If I 2 = 1 , sort output inventory by decreasing mass (DEFAULT).

If I 2 = 2 , sort output inventory by decreasing total activity.

If I 2 = 3 , sort output inventory by decreasing specific activity.

If I 2 = 4 , sort output inventory by increasing Z , followed by A ,
followed by S .

The sign of b 2 controls when to print. If positive, the output will be
printed at the end of the calculation (DEFAULT). If negative, it will be
printed at the end of each burn step.

allows the user to allow or disallow the use of high energy physics
models.

If

3

-

,

b

=

1

a fatal error will be printed if tabular data is unavailable for any
nuclide (DEFAULT).

If b 3 = 0 , the atom fraction of any data using a model is set to zero.

If b 3 = 1 , use cross section models for nuclides not containing
tabular data and then allow CINDER90 to calculate the 1-group cross
section for these nuclides by convolving a 63-group flux tally with the
CINDER90 63-group cross section data.

MATVOL = v 1 v 2 . . .

Used to provide the volume of all cells containing a burn material in a
repeated structure or lattice geometry ( 3 ). Each v i entry is the
volume of all cells containing burn material m i . If MATVOL is used,
all materials m i must have a corresponding volume v i .

MATMOD = n t ts 1 [material list] 1 ts 2 [material list] 2 . . .

Allows a user to make adjustments to the material abundances as a
function of time. The input for this option is nested 3 layers deep. The
three layers are time, material, and nuclide.

MATMOD = n t ts 1 [material list] 1 ts 2 [material list] 2 . . .

n t The number of time steps in which abundance changes are specified.

ts j = i The ordinate of the time step, corresponding to the TIME
keyword. If positive, the new abundances are used at times t i and t i
+1 / 2 . If negative, the new abundances are used at t i and t i +1 .
The value at t i +1 / 2 is linearly interpolated.

[material list] 1 = n m 1 [material info] 1 m 2 [material info] 2 . . .

n m The number of materials to adjust during this time step. m i The
material to adjust.

[material info] 1 = n z target 1 c 1 target 2 c 2 . . .

n z The number of targets to adjust.

target i The target identifier [§1.2.2] to change the abundance of. All
target formats are supported.

c i The new abundance of the target. If it is positive, it is
interpreted as atom fractions or atom densities. If negative, it is
interpreted as weight fractions or gram densities.

Note that if a nuclide is not listed, its abundance is not changed. As a
result, all nuclides must be listed to reset a material. SWAPB is more
practical for inserting fresh fuel into a problem.

SWAPB = n t ts 1 [universe list] 1 ts 2 [universe list] 2 . . .

Allows a user to swap the contents of universes at the end of a given
time step ts . This is useful for moving fresh fuel in and swapping
assemblies during a refuel, for example ( 7 , 8 ). Like MATMOD , this is
a nested input, with layers of time and universe.

SWAPB = n t ts 1 [universe list] 1 ts 2 [universe list] 2 . . .

n t The number of time steps in which universe fill changes are
specified.

ts j = i The ordinate of the time step to make changes, corresponding to
the TIME keyword. Changes are only made after a corrector step.

[universe list] 1 = n u u 1 [fill spec] 1 u 2 [fill spec] 2 . . .

n u The number of universes to adjust during this time step. u i The
universe to adjust.

[fill spec] i

The revised, fully specified, FILL card input, listing the universe
numbers for each cell of the finite lattice, but omitting the range
specification ( 6 ).

NOSTATS If present, this option will disable the computation and output
of statistical parameters for reaction rates during depletion. In
addition, only a single reaction-rate array is created per MPI rank, as
opposed to the default duplication of the arrays for each OpenMP task.
This will generally reduce performance but substantially reduce memory
usage on large depletion problems. Without statistical information,
users should take care to ensure their problem is converged. One should
also consider using this option in concert with DISABLE NUCLIDE \_
ACTIVITY \_ TABLE for further memory reduction.

This feature will be eliminated in the next public release of the code
in lieu of transparent and less-memory-intensive approaches, but it is
provided here as a stop-gap measure in case memory overconsumption is
encountered.

Use: The depletion/burnup capability is limited to criticality ( KCODE )
problems.

## Details:

- 1 Burning with large time steps that encounter large flux-shape changes during the time step will lead to inaccurate calculations. Use time steps small enough to capture the flux-shape change accurately over time.

- 2 For negative material numbers, m i , specified on the MAT keyword, the recoverable energy per fission and neutrons per fission are computed for use in the power normalization procedure and the calculation of fission power fractions. A fatal error results if every material number is negative.
- 3 To compute correctly isotopic masses and fluxes for burn materials, the volume of these materials must be either calculated by the MCNP code or provided by the user (on the VOL card or MATVOL keyword). For lattices or repeated structures, the MCNP code calculates the volume of each cell, but does not account for multiple occurrences of cell volumes. Therefore, if cells containing a burn material are repeated, then the volume calculated by the MCNP code will not represent the total volume of burn material and the user must provide the correct information on the MATVOL keyword.
- 4 When using the MATMOD keyword, if ts j is negative at t i and the abundances of any of the altered isotopes at t i +1 is equal to the abundance set at t i , then the abundances of the altered isotopes will be set to the value at t i for t i , t i + 1 / 2 and t i +1 . At t i + 3 / 2 , the isotopes will undergo a normal depletion and the abundances will not be set to the value at t i +1 .
- 5 When using the MATMOD keyword of the BURN card, if a burn material is set to have an abundance change at t 1 , then the atom density of that isotope at t 1 / 2 is set to the initial value specified at t 0 . This is only set for the initial midpoint time step; the rest of the calculation will follow the procedure described for the ts j parameter.
- 6 The ability to 'swap' or redefine universes is limited to universes of the same level. The universe need not be actively in the geometry (i.e. the universe may be truncated out of view by the bounding surfaces and still be able to be swapped). Also, you cannot swap a universe that does not pre-exist in the geometry.
- 7 At the beginning of the simulation, the code inserts a tiny quantity (an atom fraction of 10 -37 ) of nuclides the code expects to need transport reaction rates for into the transport material. These reaction rates are then used during the depletion process to compute transmutation as these nuclides are generated, which generally improves the initial predictor step accuracy. When one uses the SWAPB option to move material into the geometry after the first time step, the AFMIN option will truncate nuclide abundances below af 1 , which by default will remove these nuclides from the material and prevent initial computation of these reaction rates. One can set af 1 to 10 -38 or make the first step after fuel shuffling particularly short if this accuracy loss is a concern.
- 8 As one shuffles material in the geometry, one must always ensure the volume of each material being irradiated is constant and corresponds to the val (individual cells) or MATVAL (lattices of cells) values. Otherwise, the normalization of tallies will be performed incorrectly. One can remove and insert a material throughout a simulation using SWAPB , but all of the material must be removed or inserted at the same time.
- 9 Burnup is performed on a per-material basis. As a result, if one material is in multiple locations in the geometry, burnup will be performed based on the average irradiation of all locations. It is recommended to have unique materials whenever the neutron flux is expected to vary from location to location, even if the initial configuration is the same. For example, in a reactor with fuel rods, the following list is sorted in increasing accuracy: all fuel is given by one material, each assembly has a unique fuel material, each fuel rod has a unique material, each axial and radial discretization of the fuel rod has a unique material. This applies to all material being burned. Having many unique regions, however, increases the variance per region and the memory requirements for the simulation.
- 10 Energy deposition in BURN is computed as 1 . 111 b 1 Q Σ f φ . The factor 1 . 111 is a default estimate of the ratio of total recoverable energy from all reactions to the prompt fission energy and comes from [page 98 of 302]. This additionally includes delayed photon, delayed beta, and capture photons. This factor is not perfectly applicable to all problems due to compositional and spectral effects. One can adjust the value b 1 as necessary to help correct for these effects, but one should note that the factor 1 . 111 is still included.

The value of Q is hardcoded for 22 fissionable nuclides and includes
fission fragment recoil, prompt neutron, and prompt photon energies. The
fissionable nuclides with Q values are 232 Th, 233 Pa, 233 U through 240
U, 237 Np, 238 Pu through 243 Pu, 241 Am through 243 Am, 242 Cm, and 244
Cm. The Q values used

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

13

14

15

16

17

18

19

20

21

1

2

by the MCNP code are shown in PRINT Table 98 and come from a variety of
sources such as ENDF/B-VI, ENDF/B-VII, JEFF 3.1, and expert evaluation
(only in the case of those isotopes with no other source of data). The
incoming neutron energy spectrum used for Q is thermal.

## 5.8.14.1 Example 1

Listing 5.44 gives an infinite pincell example, where materials 10, 30,
and 40 are burned at 5 kW for 100 days and then 70 more days. Only
material 10 contains fissionable actinides; therefore materials 30 and
40 experience transmutation only. The 2nd entry on the BOPT keyword sets
the ordering of the output and selection of the fission product tier.
Because the 1st digit of the 2nd entry is '1', the 2nd fission product
tier will be used. Because the 2nd digit of the 2nd entry is '2', the
order of the output isotope inventory will be based on high to low total
activity. Because the 2nd BOPT keyword is negative, output will be given
at the end of each burn step. Isotope inventories will be given for each
individual burn material as well as the sum over all burn materials.

The nlib = 80c option is used to ensure that all neutron transport cross
sections, including those brought in by the burnup process, are from one
library. Since ENDF/B-VII.1 does not include all of the nuclides the
code tries to add to transport, the OMIT option removes 14 nuclides that
are not available.

Listing 5.44: example\_burn\_1.mcnp.inp.txt

<!-- image -->

| BURN   | TIME = 100 70 MAT = 10 30 40 POWER = 0.005   |
|--------|----------------------------------------------|
| M10    | O-16 2.0 U-235 0.0455                        |
| M20    | He-4 -1.0                                    |
| M30    | Zr-90 -1.0                                   |
| M40    | H-1 4.7716e-2 O-16 2.3858e-2                 |

## 5.8.14.2 Example 2

Listing 5.45 is identical to Listing 5.44 but with three exceptions.
First, after running at full power, a single decay step of 365 days is
performed. Second, the second entry of BOPT is changed to '-22',
indicating that Tier 3 fission products will be used instead of Tier 2.
Finally, from material 4, 1 H and 16 O have been omitted so that only
boron is transmuted.

Listing 5.45: example\_burn\_2.mcnp.inp.txt

| BURN   | TIME = 100 70 365   |
|--------|---------------------|
|        | MAT = 10 30 40      |

```
3 POWER = 0.005 4 PFRAC = 1.0 1.0 0.0 5 BOPT = 1.0 -22 1 6 OMIT = -1 14 C-12 C-13 C-14 N-16 O-18 F-18 Ne-20 7 Y-87 Y-88 Zr-89 Nb-91 Nb-92 Mo-91 Mo-93
```

## 5.8.14.3 Example 3

Listing 5.46 has three changes relative to Listing 5.44. First, the time
steps have been changed to 15, 30, and 30 days. Second, the AFMIN
keyword is used to set the minimum nuclide density to 10 -20 and the
convergence criteria to 10 -12 . Third, the MATMOD keyword is used to
adjust the boron abundance at time step 2. Here, 10 B is updated with a
6 × 10 -5 atom fraction and 11 B is updated to a 24 × 10 -5 atom
fraction. All other materials and nuclides are untouched. Note that
although material 40 has unnormalized nuclide fractions, the input to
MATMOD is a relative fraction.

```
1 BURN TIME = 15 30 30 2 MAT = 10 30 40 3 POWER = 0.005 4 PFRAC = 1.0 1.0 1.0 5 BOPT = 1.0 -12 1 6 AFMIN = 1e-20 1e-12 7 OMIT = -1 14 C-12 C-13 C-14 N-16 O-18 F-18 Ne-20 8 Y-87 Y-88 Zr-89 Nb-91 Nb-92 Mo-91 Mo-93 9 MATMOD = 1 10 2 1 11 40 2 B-10 0.00006
```

Listing 5.46: example\_burn\_3.mcnp.inp.txt

## 5.8.14.4 Example 4

Listing 5.47 gives a 3 × 3 lattice of fuel pins where universes 1, 2,
and 3 each contain a fuel rod, differing only in the material in the
fuel. The fuel used is material 10, 20, and 30 respectively. Initially,
only universe 1 and 2 are in the problem, in a checkerboard pattern with
universe 1 in the top left corner. Material 3 is not present in the
problem and is not initially being irradiated.

Using the SWAPB keyword at the end of time step 2, universe 2 is removed
from the geometry and replaced with the fresh fuel in universe 3.
Material 20 is now no longer being irradiated and decay calculations
will be performed. At the end of time step 4, universe 3 is removed and
replaced with universe 2 again. Material 30 is now no longer irradiated
and will now decay.

The MATVOL keyword is required in this example order to provide the
correct volumes to CINDER90. If MATVOL is missing, the vol option on the
cell will be used, regardless of how many times that cell appears in the
geometry. One must ensure the quantity of each material is constant as
noted in 8 .

```
BURN TIME = 10 10 10 10 10 MAT = 10 20 30 MATVOL = 50.2655 40.2124 40.2124 POWER = 0.030 BOPT = 1.0 -12 1 OMIT = -1 14 C-12 C-13 C-14 N-16 O-18 F-18 Ne-20
```

Listing 5.47: example\_burn\_4.mcnp.inp.txt

1

2

3

4

5

6

Table 5.17: Source Variables Required for each Source Particle

| Code Source Variable                                                                                                        | Variable Description                                                                                                                                                                                                                                                                                                                              |
|-----------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pbl%r%erg pbl%r%tme pbl%r%x , pbl%r%y , and pbl%r%z pbl%r%u , pbl%r%v , and pbl%r%w pbl%i%ipt pbl%r%wgt pbl%i%icl pbl%i%jsu | the energy of the particle (MeV) the time when the particle started (shakes) the position of the particle the direction of the flight of the particle the type of particle the statistical weight of the particle the cell where the particle started the surface where the particle started, or zero if the starting point is not on any surface |

10

11

12

13

14

15

<!-- image -->

| Y-87      | Y-88      |
|-----------|-----------|
| SWAPB = 2 | SWAPB = 2 |
| 2 1       | 2 1       |
| 4 1 3 1   | 4 1 3 1   |
| 3 1 3     | 3 1 3     |
| 1 3 1     | 1 3 1     |
| 4 1       | 4 1       |
| 4 1 2 1   | 4 1 2 1   |
| 2 1 2     | 2 1 2     |

## 5.8.15 Subroutines SOURCE and SRCDX

Users may write their own source subroutines to bypass the standard
source capabilities. If no SDEF , SSR , or KCODE card is provided in the
MCNP input file, then the MCNP code will look for a subroutine called
SOURCE . This subroutine must be supplied by the user. In addition, if
there are detectors or DXTRAN, the MCNP code also will require a SRCDX
routine. [§10.3.4] contains an example of a SOURCE subroutine and
[§10.3.5] discusses the SRCDX subroutine. The parameters that must be
specified within the SOURCE subroutine are listed and defined in Table
5.17. Prior to calling subroutine SOURCE , isotropic direction cosines (
u, v, w ) ( pbl%r%u , pbl%r%v , and pbl%r%w ) are calculated and need
not be specified if an isotropic distribution is desired.

Note that additional variables may have to be defined if there are point
detectors or DXTRAN spheres in the problem. Also, pbl%r%erg has a
different meaning in a special case. If there is a negative igm on the
MGOPT card, which indicates a special electron-photon multigroup
problem, ERG on the SDEF card is interpreted as an energy group number,
an integer.

The SI , SP , and SB cards also can be used with the SOURCE subroutine,
although modifications to other parts of the MCNP code may be required
for proper initialization and to set up storage. A random number
generator RANG() is available for use by SOURCE for generating random
numbers between 0 and 1. Up to 200 numerical entries can be entered on
each of the IDUM and RDUM cards for use by SOURCE . The IDUM entries
must be integers and the RDUM entries floating point numbers.

If you are using a detector or DXTRAN and your source has an anisotropic
angular distribution, you will need to supply an SRCDX subroutine to
specify PSCs (i.e., probability of the surface source emitting a
particle into a specified angle relative to the surface normal) for each
detector or DXTRAN sphere.

There are unused variables stored in the particle bank that are reserved
for the user. These are called SPARE(M), M=1, MSPARE , where MSPARE = 7
. Depending on the application, you may need to reset them to 0 in
SOURCE for each history; the MCNP code does not reset them.
---
title: "Chapter 10.3 - Source Examples"
chapter: "10.3"
source_pdf: "mcnp631_theory_user-manual/mcnp-primers-examples/10.3_Source_Examples.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

```
11 real(dknd), intent(inout) :: t 12 integer, intent(inout) :: ib 13 14 t=t * exp(tds(iptal(3,1,tally _ p _ thread%ital)+1) * pbl%r%tme) 15 return 16 end subroutine tallyx
```

The FU 4 card establishes a single user bin, and the value of α is
stored in tds(iptal(3,1,tally \_ p \_ thread%ital)+1) and used for the
tally label.

## 10.2.8.5 Example 50

Tally the number of neutrons passing through cell 16 that have had 0, 1,
2, 3, or 4 collisions. The input cards are

```
1 F4:N 16 2 FU4 0 1 2 3 4 3 SD4 1
```

and TALLYX is shown in Listing 10.33.

```
1 subroutine tallyx(t,ib) 2 use mcnp _ params 3 use mcnp _ global 4 use tskcom, only: tally _ p _ thread 5 use pblcom, only: pbl 6 use mcnp _ debug 7 8 implicit none 9 real(dknd), intent(inout) :: t integer, intent(inout) :: ib tally _ p _ thread%ibu = pbl%i%ncp if(tally _ p _ thread%ibu > 5 ) ib=-1 t=pbl%r%wgt return end subroutine tallyx
```

Listing 10.33: example\_tallyx\_collision\_bins.f90.txt

10

11

12

13

14

15

16

17

If the IF statement in this TALLYX is omitted, a count will be made of
the cases of five or more collisions, and in these cases no score will
be tallied but a count will be printed of the times that the tally was
unable to be made because tally \_ p \_ thread%ibu was a value where no
bin existed.

In the five user bins, t is the number of neutrons per source neutron
passing through cell 16 that have undergone 0, 1, 2, 3, or 4 collisions,
respectively. Note that the FU 4 card has five entries to establish the
five user bins and provide labels. Note also that in this example, the
neutrons are calculated so that t = t × renormalization factor (which
preserves the weight associated with the tracks), where in TALLYX
subroutine Listing 10.30 the neutron tracks are calculated so that t=1 .
Finally, note that if pbl%i%ncp &gt; 5 (six or more collisions) no tally is
made because ib is set to be less than zero. If an E 4 card was added,
the neutrons would be tallied as a function of energy for each user bin.

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

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

## 10.3 Source Examples

## 10.3.1 General Source

Some examples of the general source are given here to illustrate the
power and complexity of this feature. Refer to §5.8 for a complete
explanation and other examples.

The following example is of the general source that illustrates two
levels of dependency. Let us assume a duct streaming problem where the
source at the duct opening has been obtained from a reactor calculation.
Energies above 13.5 MeV have one angular distribution and energies below
13.5 MeV have a different angular distribution. The source has a uniform
spatial distribution on a circular disk of radius 37 cm centered at ( x,
y, z ) on planar surface 1 going into cell 2.

## 10.3.1.1 Example 51

```
1 SDEF ERG = D1 DIR FERG D2 SUR = 1 CEL = 2 2 POS = x y z RAD D5 AXS u v w VEC u v w 3 c Source Definition Card. 4 c In this example, AXS is needed to define a vector which 5 c defines the source plane of a disk source. 6 c In this example, POS defines the location of the center 7 c of the disk. 8 c VEC is the direction that source particles will be 9 c travelling once created. c AXS and VEC can be different. c For this duct streaming problem, they should be the same. c SI1 H 1E-7 1E-5 ... 13.5 14 ... 20 c Source Information 1 (SI1) corresponds to D1. c H indicates histogram values follow. c SP1 D 0 10E-4 ... 10E-2 10E-1 ... 0.3 c Source Probability 1 (SP1) augments SI1. c D indicates discrete values. c Probability of each bin on SI1. c The probability a source particle will be between 10E-7 c and 10E-5 MeV is 10E-4. c DS2 S 3 3 ... 3 4 ... 4 c Dependent Source 2 (Depends as a function of ERG). c S indicates numbers following are themselves other c distributions. c In this example, if a particle has an energy in bin 10E-7 to c 10E-5, then it will have a direction associated with source c distribution 3. c SI3 0 0.2 ... 1 c Source Information 3 (Second Level) c Default is histogram values. c SP3 D 0 1E-4 ... 0.1 c Source Probability 3 (Second Level). c Probability of each bin on SI3.
```

```
39 c 40 SI4 0 0.1 ... 1 41 c Source Information 4 (Second Level). 42 c Default is histogram values. 43 c 44 SP4 D 0 1E-2 ... 0.1 45 c Source Probability 4 (Second Level). 46 c Probability of each bin on SI4. 47 c 48 SI5 37 49 c Source Information 5. 50 c Default is histogram values. 51 c There is one bin from 0 to 37. 52 c When used with the RAD keyword on the SDEF card, it indicates 53 c a circular distribution from 0 to 37 cm. 54 c 55 SP5 -21 1 56 c Source Probability 5. 57 c The -21 indicates a sampling scheme based on a power of the 58 c variable. 59 c In this case, the sampling is a function of radius^1, 60 c which results in a uniform spatial distribution over the disk. 61 c Since a uniform spatial distribution is the default for disk 62 c sources, this card is optional. 63 c
```

This example can be expanded by having the source in two ducts instead
of one (with the same energy and angular distribution as before). The SI
1, SP 1, DS 2, SI 3, SP 3, SI 4, and SP 4 cards remain unchanged, but
the SI 5 and SP 5 cards are no longer valid. The SDEF card is changed as
shown, and the other cards are added.

```
1 SDEF ERG = D1 DIR FERG D2 SUR = D6 CEL FSUR D7 2 POS FSUR D8 RAD FSUR D9 AXS FSUR D10 VEC FSUR D10 3 SI6 L 1 7 4 c Source Information 6. 5 c L indicates discrete values, in this case surface 1 or 7 6 c 7 SP6 D 0.6 0.4 8 c Source Probability 6. 9 c Probability of each value on SI6. 10 c 11 DS7 L 2 8 12 c Dependent Source 7 (Depends as a function of SUR). 13 c L indicates discrete value, in this case cell 2 or 8, 14 c depending on whether surface 1 or 7, respectively, was chosen. 15 c 16 DS8 L x1 y1 z1 x2 y2 z2 17 c Dependent Source 8 (Depends as a function of SUR). 18 c L indicates discrete values, in this case the respective centers, 19 c of two disks, depending on whether surface 1 or 7 was chosen. 20 c 21 DS9 S 11 12 22 c Dependent Source 9 (Depends as a function of SUR). 23 c S indicates other distributions, in this case the respective radii, 24 c of two disks, depending on whether surface 1 or 7 was chosen. 25 c 26 DS10 L u1 v1 w1 u2 v2 w2 27 c Dependent Source 10 (Depends as a function of SUR).
```

```
28 c L indicates discrete values, in this case the vectors that define a 29 c plane that the disk is on and the vector from which DIR is measured. 30 c In this streaming problem, AXS=VEC, and both depend on whether 31 c surface 1 or 7 was chosen. 32 33 SI11 0 37 34 SP11 -21 1 35 SI12 0 25 36 SP12 -21 1 37 c In this problem, the radius of the duct depends on which 38 c duct was chosen.
```

## 10.3.1.2 Example 52

This example is a two-source-cell problem where the material in one cell
is uranium and in the other is thorium. The uranium cell has two
isotopes, 235 U and 238 U, and the thorium has one, 232 Th. Each isotope
has many photon lines from radioactive decay. The following input cards
describe this source.

```
1 SDEF CEL D1 ERG FCEL D2 POS FCEL D3 2 c 3 SC1 Source Cells 4 c Source Comment 1 5 c 6 SI1 L 1 2 7 c Source Information 1 8 c L indicates discrete values, in this case cell 1 or 2. 9 c The cell also determines the element in this problem. 10 c 11 SP1 D 2 1 12 c Source Probability 1 13 c Probability of each value on SI1. Here the cell with 14 c uranium is twice as likely as the thorium cell. 15 c Other distributions based on volume or decay rate, 16 c for example, are also possible. 17 c 18 SC2 source "spectra" 19 DS2 S 4 5 20 c Dependent Source 2 (Depends as a function of CEL). 21 c S indicates numbers following are themselves other 22 c distributions. 23 c In this example, if a particle starts in cell 1, then the 24 c ERG is defined by source distribution 4. 25 c 26 DS3 L 0 0 0 10.5 0 0 27 c 28 SC4 uranium nuclides 29 SI4 S 6 7 30 SP4 D 1 3 31 c Source Distribution and Probability 4. 32 c Here the specific uranium isotope is chosen, 238U is 33 c three times more likely than 235U. 34 c 35 SC5 thorium nuclide 36 SI5 S 8 37 SP5 D 1
```

```
38 c Source Distribution and Probability 5. 39 c Only one isotope of thorium is possible. 40 c 41 SC6 235U photon lines 42 SI6 L 1.0 2.0 $ E1 ... EI 43 SP6 D 1 2 $ I1 ... II 44 SC7 238U photon lines 45 SI7 L 0.1 0.2 $ E1 ... EI 46 SP7 D 2 1 $ I1 ... II 47 SC8 232Th photon lines 48 S 49 L 0.01 0.02 $ E1 ... EI 50 SP8 D 1 1 $ I1 ... II
```

## 10.3.1.3 Example 53

```
1 SDEF SUR=D1 CEL FSUR D2 ERG FSUR D6 2 X FSUR D3 Y FSUR D4 Z FSUR D5 3 c 4 SI1 L 11 0 5 c Source Information 1 6 c L indicates discrete values, in this case surface 11 or 0 7 c (meaning the source point is not on a surface). 8 c 9 SP1 0.8 0.2 10 DS2 L 0 88 11 c Dependent Source 2 (Depends as a function of FSUR). 12 c L indicates discrete values, in this case cell 0, 13 c (meaning the point may not be within a cell), or cell 88. 14 c Note that with Distribution 1, the source point may either be 15 c on surface 11 (80% probability) or within cell 88 16 c (20% probability). 17 c 18 DS6 S 61 62 19 SP61 -3 0.98 2.2 20 SP62 -3 1.05 2.7 21 c Source Probabilities 61 and 62. 22 c The -3 indicates the energy is sampled from the Watt Fission 23 c Spectrum. 24 c 25 DS3 S 0 31 26 SI31 20 30 27 SP31 0 1 28 c Source Information and Probabilities for Distribution 3. 29 c In this case, the 0 on the DS3 card indicates that no 30 c distribution is given; the default variable will be selected. 31 c For this case, if surface 11 was selected, the variable 32 c POS will default to the coordinates 0 0 0. 33 c If surface 11 was not selected, the source point must be 34 c within cell 88,and the x coordinate is sampled from a single 35 c bin histogram with values between 20 and 30. 36 c Since this value corresponds to a position, the units are cm. 37 c 38 DS4 S 0 41 39 SI41 -17 36
```

| SP41   | 0 1    |
|--------|--------|
| DS5    | S 0 51 |
| SI51   | -10 10 |
| SP51   | 0 1    |

Of the particles from this source, 80% start on surface 11, and the rest
start in cell 88. When a particle starts in cell 88, its position is
sampled, with rejection, in the rectangular polyhedron bounded by 20 &lt; x
&lt; 30 , -17 &lt; y &lt; 36 , and -10 &lt; z &lt; 10 . When a particle starts on
surface 11, its cell is found from its position and direction. The
energy spectrum of the particles from surface 11 is different from the
energy spectrum of the particles from cell 88. A zero after the S option
invokes the default variable value.

## 10.3.1.4 Example 54

The following is an example of using the Q option. The low-energy
particles from surface m come out with a cosine distribution of
direction, but the higher-energy particles have a more nearly radial
distribution. The energy values on the DS 2 card need not be the same as
any of the e i on the SI 1 card.

| SDEF   | ERG=D1   | DIR FERG D2   | SUR=m   |
|--------|----------|---------------|---------|
| SI1    | e1 e2    | ... ek        |         |
| SP1    | 0 p2     | ... pk        |         |
| DS2    | Q        | 0.3 21 0.8 22 | 1.7 23  |
| SP21   | -21      | 1             |         |
| SP22   | -21      | 1.1           |         |
| SP23   | -21      | 1.3           |         |
| SP24   | -21      | 1.8           |         |

## 10.3.2 Beam Sources

By implementing a general transformation on the SDEF card in one of two
forms; TR = n or TR = Dn , a user can point a particle beam in space. In
either case a general transformation is applied to a source particle
after its coordinates and direction cosines have been determined using
the other parameters on the SDEF card. Particle coordinates are modified
by both rotation and translation; direction cosines are modified by
rotation only. This allows the user to rotate the direction of the beam
or move the entire beam of particles in space. The TR = Dn option is
particularly powerful because it allows the specification of more than
one beam at a time.

## 10.3.2.1 Example 55: A Single Beam Source

An example of specifying a Gaussian beam follows:

<!-- image -->

```
8 c Surface Cards 9 . 10 . 11 . 12 nnn SQ a^-2 b^-2 0 0 0 0 -c^2 0 0 0 $ cookie cutter surface 13 14 c Control Cards 15 SDEF DIR=1 VEC=0 0 1 X=D1 Y=D2 Z=0 CCC=ccc TR=n 16 SP1 -41 fx 0 17 SP2 -41 fy 0 18 TRn x0 y0 z0 cos(phi) -sin(phi) 0 sin cos 0 0 0 1
```

The SDEF card sets up an initial beam of particles traveling along the z
axis ( DIR = 1 , VEC = 0 0 1 ). Information on the x and y coordinates
of particle position is detailed in the two SP cards. On the SDEF card,
the specifications X = D1 and Y = D2 indicate that MCNP6 must look for
distributions 1 and 2, here given by source probability distributions,
SP1 and SP2 . The z coordinate is left unchanged ( z = 0 ).

Because there is no PAR option in this example, the particle generated
by this source will be the one with the lowest ipt number in Table 4.3
(i.e., neutron).

The SP cards have three entries. The first entry is -41 , which
indicates sampling is to be done from a built-in Gaussian distribution.
This position Gaussian distribution has the form

<!-- formula-not-decoded -->

The parameters a and b are the standard deviations of the Gaussian in x
and y .

The second entry ( fx or fy ) on the SP cards is the full-width at half-
maximum (FWHM) of the Gaussian in either the x or y direction. These
must be computed from a and b by the user as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The third entry on the SP cards represents the centroid of the Gaussian
in either the x or y direction. We recommend that the user input 0 here,
and handle any transformations of the source with a TR card. Using a
non-zero value will interfere with the rejection function as specified
by the 'cookie cutter' option.

Note that in PRINT Table 10 in the MCNP6 output file, the definitions of
a , b , and c are different from those discussed above; however, FWHM
will be the same as the third entry on the SP cards. The parameter a in
PRINT Table 10 differs from the parameter a above by a factor of the
square root of two. This is a legacy item from the conversion of the -41
function from time to space.

The user generally does not want the beam Gaussian to extend infinitely
in x and y , therefore a cookie cutter option has been included to keep
the distribution to a reasonable size. CCC = ccc tells MCNP6 to look at
the card labeled ccc ( ccc is a user-specified cell number) to define
the cutoff volume. The first entry on the ccc card is 0 , which
indicates a void cell. The second number, -nnn ( nnn again is a user-
specified number), indicates a surface card within which to accept
particles. In the example, this is a SQ surface (a 2-sheet hyperboloid)
that is defined as

<!-- formula-not-decoded -->

Any particle generated within this cell is accepted; any outside of the
cell is rejected. Any well defined surface may be selected, and it is
common to use a simple cylinder to represent the extent of a beam pipe.

In this example, a source is generated in an ( x ′ , y ′ ) -coordinate
system with the distribution centered at the origin and the particles
traveling in the z ′ direction. The particle coordinates can be modified
to an ( x, y ) -coordinate system by translation and rotation according
to the following equations, where 0 ≤ φ L ≤ π :

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Thus the angle φ L is the angle of rotation of the major axis of the
source distribution from the positive y direction in the laboratory
coordinate system. If cos φ L = 0 . 0 , the angle is 90 ◦ and the major
axis lies along the x axis. The TR n card in the example above
implements this rotation matrix, however the user should note that φ L
in the TR n card is equal to φ L -π/ 2 .

## 10.3.2.2 Example 56: Defining Multiple Beams

The opportunity to specify a probability distribution of transformations
on the SDEF card allows the formation of multiple beams which differ
only in orientation and intensity. This feature may have applications in
radiography or in the distribution of point sources of arbitrary
intensity.

The use of a distribution of transformations is invoked by specifying TR
= Dn on the SDEF card. The cards SI , SP , and, optionally, SB are used
as specified for the SSR card.

1

2

3

| SIn   | L      | i1 ... ik   |
|-------|--------|-------------|
| SPn   | option | p1 ... pk   |
| SBn   | option | b1 ... bk   |

The L option on the SI card is required; input checking ensures this
usage for both the SDEF and SSR applications. The 'option' on the SP and
SB cards may be blank, D , or C . The values i1 ... ik identify k
transformations that must be supplied. The content of the SP and SB
cards then follows the general MCNP6 rules.

The following example shows a case of three intersecting Gaussian
parallel beams, each defined with the parameters a = 0 . 2 cm, b = 0 . 1
cm and c = 2 in the notation used previously [§10.3.2.1]. Each beam is
normal to the plane of definition.

| Beam 1   | is centered at (0 , 0 , - 2) . The major axis of the beam distribution is along the x axis. The beam is emitted in the + z direction and has relative intensity 1.                 |
|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Beam 2   | is centered at ( - 2 , 0 , 0) . The major axis of the beam distribution is along the y axis. The beam is emitted in the + x direction and has relative intensity 2.                |
| Beam 3   | is centered at (0 , - 2 , 0) . The major axis of the beam distribution is along the line defined by x = z . The beam is emitted in the + y direction and has relative intensity 3. |

The card SB n is used to provide equal sampling from each of the three
beams, independent of the relative intensities. The input cards are as
follows:

```
1 Title 2 c Cell cards 3 . 4 . 5 . 6 999 0 -999 $ cookie cutter cell 7 8 c Surface Cards 9 . 10 . 11 . 12 999 SQ 25 100 0 0 0 0 -4 0 0 0 $ cookie cutter surface 13 14 c Control Cards 15 SDEF DIR=1 VEC=0 0 1 X=D1 Y=D2 Z=0 CCC=999 TR=D3 16 SP1 -41 0.4709640 17 SP2 -41 0.23584820 18 SI3 L 1 2 3 19 SP3 1 2 3 20 SB3 1 1 1 21 TR1 0 0 -2 1 0 0 0 1 0 0 0 1 22 TR2 -2 0 0 0 1 0 0 0 1 1 0 0 23 TR3 0 -2 0 0.707 0 0.707 0.707 0 -0.707 0 1 0
```

## 10.3.3 Burning Multiple Materials In a Repeated Structure with Specified Abundance Changes

## 10.3.3.1 Example 57

In the following example, a 4 × 4 fuel pin array (created using repeated
structures) is burned while material abundance changes are made at
various time steps. Portions of the input and output files provided in
this example illustrate various BURN card features:

```
1 burn example 2 1 1 6.87812e-2 -1 u=2 imp:n=1 vol=192.287 $ fuel 3 3 2 4.5854e-2 1 -2 u=2 imp:n=1 vol=66.43 $ clad 4 4 3 7.1594e-2 2 u=2 imp:n=1 vol=370.82 $ water 5 6 4 6.87812e-2 -1 u=3 imp:n=1 vol=192.287 $ fuel 6 7 5 4.5854e-2 1 -2 u=3 imp:n=1 vol=66.43 $ clad 7 8 6 7.1594e-2 2 u=3 imp:n=1 vol=370.82 $ water 8 10 0 -3 4 -5 6 u=1 imp:n=1 lat=1 fill=0:1 0:1 0:0 9 2 3 2 3 10 ... 11 12 ... 13 BURN TIME=50,10,500 14 MAT=1 4 15 POWER=1.0 16 PFRAC=1.0 0 0.2 17 OMIT= 1,8,6014,7016,8018,9018,90234,91232,95240,95244 18 4,8,6014,7016,8018,9018,90234,91232,95240,95244 19 BOPT= 1.0, -4
```

<!-- image -->

A 4 × 4 lattice contains universes 2 and 3, which are both repeated
twice in the lattice. Universe 2 comprises cells 1, 3, and 4, where cell
1 contains material 1; universe 3 comprises cells 6, 7, and 8, where
cell 6 contains material 4. The MAT keyword specifies that both
materials 1 and 4 will be burned. The combination of the TIME , POWER
and PFRAC keywords specify that these materials will be burned first for
50 days at 100% of 1 MW, then decayed for 10 days, and then finally
burned for 500 days at 20% of 1 MW.

The BOPT keyword specifies that the following options will be invoked:
the Q -value multiplier will be set to a value of 1.0, only Tier 1
fission products will be included, the output will be ordered by ZAID
and printed at the end of each KCODE run, and only tabular transport
cross sections will be used. Because tabular transport cross sections do
not exist for every isotope that is generated, an OMIT keyword is
required to omit these isotopes from the transport process. The
transmutation of these isotopes is accounted for by sending a 63-group
flux from MCNP6 to be matched to a 63-group cross-section set within
CINDER90. These are energy integrated to determine a total collision
rate. The OMIT keyword in the example omits eight isotopes from material
1 and eight isotopes from material 4. The AFMIN keyword states that only
isotopes possessing an atom fraction below 10 -32 will be omitted from
the transport calculation.

Because there are repeated structures in the example a MATVOL keyword is
required to calculate the tracklength-estimated reaction rates in each
repeated structure. Because material 1 and 4 are repeated twice and each
material possesses a volume of 192.287 cm 3 , MATVOL keyword entries of
192 . 287 × 2 = 384 . 57 are required for each material being burned.

A MATMOD keyword is used to manually change the abundance of certain
isotopes at specified time steps. In this example, manual isotope
abundance changes are to be completed at two time steps. At time step 1,
material 4 will have the atom density of isotope 94238 changed to 10 -6
atoms/b-cm. At time step 2, the atom densities of isotopes 94238 and
94241 in material 1 both will be revised to 10 -6 atoms/b-cm. Also in
step 2, the atom density of isotope 94238 in material 4 will be set to
10 -6 atoms/b-cm.

PRINT Table 210 contains the burnup summary table:

<!-- image -->

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

The burnup summary table contains information regarding the entire burn
system. Each time step is listed with the corresponding time duration
and actual specified time. The next six columns list the power used for

the flux normalization, k eff , energy integrated system averaged flux,
system averaged neutrons per fission and recoverable energy per fission,
and burnup. Finally, the production rate is listed in the source column.

Since both materials 1 and 4 were burned in the example, individual burn
material burnup information is also available. The available information
includes: time step, time duration, actual time, fission power fraction,
and individual material burnup:

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

<!-- image -->

| Individual Material Burnup   | Individual Material Burnup   | Individual Material Burnup   | Individual Material Burnup   | Individual Material Burnup   |
|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
| Material #: 1                | Material #: 1                | Material #: 1                | Material #: 1                | Material #: 1                |
| step                         | duration (days)              | time (days)                  | power fraction               | burnup (GWd/MTU)             |
| 0                            | 0.000E+00                    | 0.000E+00                    | 5.015E-01                    | 0.000E+00                    |
| 1                            | 5.000E+01                    | 5.000E+01                    | 5.016E-01                    | 7.205E+00                    |
| 2                            | 1.000E+01                    | 6.000E+01                    | 5.002E-01                    | 7.205E+00                    |
| 3                            | 5.000E+02                    | 5.600E+02                    | 5.002E-01                    | 2.158E+01                    |
| Material #: 4                | Material #: 4                | Material #: 4                | Material #: 4                | Material #: 4                |
| step                         | duration (days)              | time (days)                  | power fraction               | burnup (GWd/MTU)             |
| 0                            | 0.000E+00                    | 0.000E+00                    | 4.985E-01                    | 0.000E+00                    |
| 1                            | 5.000E+01                    | 5.000E+01                    | 4.984E-01                    | 7.161E+00                    |
| 2                            | 1.000E+01                    | 6.000E+01                    | 4.998E-01                    | 7.161E+00                    |
| 3                            | 5.000E+02                    | 5.600E+02                    | 4.998E-01                    | 2.152E+01                    |
| ...                          | ...                          | ...                          | ...                          | ...                          |

The fission power fraction is calculated by taking the ratio of the
fission power in a particular material to the sum of all burn materials.
Fission power fractions are only related to fissions in burn materials
as

<!-- formula-not-decoded -->

The individual material burnup is calculated by

<!-- formula-not-decoded -->

The time-dependent isotope buildup/depletion is listed after the burnup
summary information. The isotope buildup/depletion for each individual
material is given at each time step. The information is further
subdivided into actinide and non-actinide categories:

10

11

12

```
1 nuclide data are sorted by increasing zaid for material 1 volume 3.8457E+02 (cm ** 3) 2 3 actinide inventory for material 1 at end of step 0, time 0.000E+00 (days), power 1.000E+00 (MW) 4 5 no. zaid mass activity spec.act. atom den. atom fr. mass fr. 6 (gm) (Ci) (Ci/gm) (a/b-cm) 7 1 90231 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 8 2 90232 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 9 3 90233 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 4 91233 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 5 92234 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 6 92235 3.441E+02 0.000E+00 0.000E+00 2.293E-03 1.000E-01 9.886E-02
```

```
13 ... 14 ... 15 actinide inventory for material 1 at end of step 1, time 5.000E+01 (days), power 1.000E+00 (MW) 16 17 no. zaid mass activity spec.act. atom den. atom fr. mass fr. 18 (gm) (Ci) (Ci/gm) (a/b-cm) 19 1 90231 1.286E-09 6.837E-04 5.315E+05 8.718E-15 3.832E-13 3.723E-13 20 2 90232 2.394E-08 2.625E-15 1.097E-07 1.616E-13 7.100E-12 6.929E-12 21 3 90233 1.235E-13 4.468E-06 3.618E+07 8.298E-19 3.647E-17 3.574E-17 22 4 91233 1.345E-09 2.792E-05 2.075E+04 9.039E-15 3.973E-13 3.894E-13 23 ...
```

At the end of each subdivision there is an accumulation total of the
isotope information for that subdivision. Atom and weight fractions
calculations are based on the fractions of that specific subdivision.

```
1 ... 2 totals 3.455E+03 2.584E+05 7.479E+01 2.275E-02 1.000E+00 1.000E+00 3 ... 4 ... 5 nonactinide inventory for material 1 at end of step 0, time 0.000E+00 (days), power 1.000E+00 (MW) 6 7 no. zaid mass activity spec.act. atom den. atom fr. mass fr. 8 (gm) (Ci) (Ci/gm) (a/b-cm) 9 1 6012 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 10 2 6013 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 11 3 7014 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 12 4 7015 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 13 5 8016 4.684E+02 0.000E+00 0.000E+00 4.585E-02 1.000E+00 1.000E+00 14 ...
```

After isotope information for each individual material is given, PRINT
Table 220 lists the total build/up of all actinides and non-actinides
from all materials combined at each of the time steps.

```
1 ... 2 1burnup summary table summed over all materials print table 220 3 4 nuclides with atom fractions below 1.000E-32 for a material are zeroed and deleted from print tables after t=0 5 6 nuclide data are sorted by increasing zaid summed over all materials volume 7.6914E+02 (cm ** 3) 7 8 actinide inventory for sum of materials at end of step 0, time 0.000E+00 (days), power 1.000E+00 (MW) 9 10 no. zaid mass activity spec.act. atom den. atom fr. mass fr. 11 (gm) (Ci) (Ci/gm) (a/b-cm) 12 1 90231 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 13 2 90232 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 14 3 90233 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 15 4 91233 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 16 5 92234 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 0.000E+00 17 6 92235 6.883E+02 0.000E+00 0.000E+00 4.585E-03 1.000E-01 9.886E-02 18 ...
```

## 10.3.4 Source Subroutine

When possible, you should take advantage of the standard sources
provided by the code rather than write a source subroutine. When you
write your own source subroutine, you lose features such as sampling
from multiple distributions, using dependent distributions, and having
frequency prints for each tabular distribution. Additionally, if using
next-event estimators ( F5 tallies) or DXTRAN spheres, subroutine SRCDX
is needed.

The standard sources, however, cannot handle all problems. If the
general source ( SDEF card), surface source ( SSR ), or criticality
source ( KCODE card) is unsuitable for a particular application, MCNP6
provides a mechanism to furnish your own source-modeling capability. The
absence of SDEF , SSR , or KCODE cards causes MCNP6 to call subroutine
SOURCE , which you must supply. Subroutine SOURCE specifies the
coordinates, direction, weight, energy, and time of source particles as
listed and defined in §5.8.15. If the value of PBL%I%IPT (particle type)
set by STARTP , which calls SOURCE , is not satisfactory, SOURCE must
also specify PBL%I%IPT . STARTP sets IPT = 1 (neutron) for MODE n , n p
, and n p e ; sets IPT = 2 (photon) for MODE p and p e ; and sets IPT =
3 (electron) for MODE e . MCNP6 checks the user's source for consistency
of cell, surface, direction, and position. If the source direction is
anisotropic and there are point detectors or DXTRAN spheres, a SRCDX
subroutine is also required [§5.8.15].

The following example of a subroutine SOURCE uses SI n , SP n , and SB n
cards and demonstrates the use of MCNP6 subroutines SMPSRC , ROTAS ,
CHKCEL , and the function NAMCHG . The geometry is a 5-cm-long cylinder
centered about the y axis, divided into 5 cells by PY planes at 1-cm
intervals. The 1-MeV mono-energetic source is a biased isotropic
distribution that is also biased along the y axis. The input
distribution cards are

```
1 SI1 -1 0 1 $ These 3 cards 2 SP1 0 1 1 $ represent a biased 3 SB1 0 1 2 $ isotropic distribution. 4 SI2 0 1 2 3 4 5 $ These 3 cards 5 SP2 0 4 2 2 1 1 $ represent a biased 6 SB2 0 1 1 2 2 4 $ distribution in y. 7 RDUM 1 $ cylindrical radius 8 IDUM 2 4 6 8 10 $ source cells
```

This problem can be run with the general source by removing the RDUM and
IDUM cards and adding:

1

2

3

```
SDEF ERG=1 VEC=0 1 0 AXS=0 1 0 DIR=D1 EXT=D2 RAD=D3 SI3 0 1 $ represents a covering surface of radius 1 SP3 -21 1 $ samples from the power law with k=1
```

The example source subroutine is shown in Listing 10.34, which would
replace the generic subroutine SOURCE that is provided with the MCNP
source code.

```
1 subroutine source 2 ! dummy subroutine. aborts job if source subroutine is missing. 3 ! if nsr=0, subroutine source must be furnished by the user. 4 ! at entrance, a random set of uuu,vvv,www has been defined. the 5 ! following variables must be defined within the subroutine: 6 ! pbl%r%x, pbl%r%y, pbl%r%z, pbl%r%icl, pbl%r%jsu, pbl%r%erg, 7 ! pbl%r%wgt, pbl%r%tme and possibly pbl%i%ipt, pbl%r%u, pbl%r%v, 8 ! pbl%r%w. 9 ! subroutine srcdx may also be needed. 10
```

Listing 10.34: example\_source\_cylinder.f90.txt

```
11 use mcnp _ params 12 use mcnp _ global 13 use mcnp _ interfaces _ mod, only: chkcel, namchg, rotas, smpsrc 14 use mcnp _ debug 15 use mcnp _ random 16 use tskcom, only: uold 17 use pblcom, only: pbl 18 19 implicit none 20 21 real(dknd) :: a(3), c, fi, r, th 22 23 ! smpsrc requires an array as the first argument. 24 ! create dummy one dimensional array 25 real(dknd) :: array(1) 26 27 integer :: i, ib, imax, itr, j, lev 28 29 intrinsic cos, sin 30 31 pbl%r%wgt=1.0 _ dknd 32 33 ! rdum(1)--Radius of Source Cylinder 34 ! sample radius uniform in area. 35 36 r=rdum(1) * sqrt(rang()) 37 38 ! Y coordinate position, probability and bias are 39 ! defined in distribution 2 by the SI2, SP2, SB2 cards. 40 ! sample for y. 41 ! IB returns the index sampled and FI the interpolated fraction. 42 ! neither is used in this example. 43 44 call smpsrc(array,2,ib,fi) 45 pbl%r%y = array(1) 46 47 ! Sample for X and Z. 48 49 th = 2.0 _ dknd * pie * rang() 50 pbl%r%x = -r * sin(th) 51 pbl%r%z = r * cos(th) 52 53 ! Direction is isotropic but biased in cone along Y axis 54 ! Defined as distribution 1 by the SI1, SP1, SB1 cards. 55 ! Sample for cone opening C=cos(NU) 56 ! Rotas samples a direction U,V,W at an angle ARCCOS(C) 57 ! From the reference vector UOLD(3) 58 ! and at an azimuthal angle sampled uniformly. 59 60 call smpsrc(array,1,ib,fi) 61 c = array(1) 62 uold(1) = 0.0 _ dknd 63 uold(2) = 1.0 _ dknd 64 uold(3) = 0.0 _ dknd 65 66 call rotas(c,uold,a,lev,itr) 67 pbl%r%u = a(1) 68 pbl%r%v = a(2) 69 pbl%r%w = a(3)
```

```
70 71 ! Cell source -find starting cell. 72 ! IDUM(1) IDUM(5) --list of source cells on IDUM card. 73 pbl%i%jsu=0 74 j = 1 75 i = 1 76 imax = 5 77 do while ((J /= 0) .and. (i /= imax)) 78 pbl%i%icl=namchg(1,idum(I)) 79 call chkcel(pbl%i%icl,2,J) 80 i=i+1 81 enddo 82 if (j /= 0) call expire(1,'Source', & 83 & 'Source is not in any cells on the idum card.') 84 pbl%r%erg = 1.0 _ dknd 85 pbl%r%tme = 0.0 _ dknd 86 return 87 end subroutine source
```

## 10.3.5 SRCDX Subroutine

If a user has supplied a subroutine SOURCE that does not emit particles
isotropically (uniform emission in all directions) and is using either a
detector tally or DXTRAN in the calculations, then subroutine SRCDX must
also be supplied to MCNP6. The structure of this subroutine is the same
as for subroutine SOURCE , except that usually only a single parameter,
PSC, needs to be specified for each detector or set of DXTRAN spheres.
PSC as defined in SRCDX is used to calculate the direct contribution
from the source to a point detector, to the point selected for the ring
detector or DXTRAN sphere. Other parameters may also be specified in
SRCDX . For example, if a quantity such as particle energy and/or weight
is directionally dependent, its value must be specified in both
subroutines SOURCE and SRCDX . When using detectors and a subroutine
SOURCE with an anisotropic distribution, check the direct source
contribution to the detectors carefully to see if it is close to the
expected result.

In general, it is best to have as few directionally dependent parameters
as possible in subroutine SOURCE . Directionally dependent parameters
must also be dealt with in subroutine SRCDX .

The most general function for emitting a particle from the source in the
laboratory system can be expressed as p ( µ, ϕ ) , where µ is the cosine
of the polar angle and ϕ is the azimuthal angle in the coordinate system
of the problem. Most anisotropic sources are azimuthally symmetric and p
( µ, ϕ ) = p ( µ ) / 2 π . The quantity p ( µ ) is the probability
density function for the µ variable only (i.e., GLYPH&lt;1&gt; p ( µ )d µ = 1
, p ( µ &gt; 0) ). PSC is p ( µ 0 ) , where µ 0 is the cosine of the angle
between the direction defining the polar angle for the source and the
direction to a detector or DXTRAN sphere point in the laboratory system.
MCNP6 includes the 2 π in the calculation automatically. Note that p ( µ
0 ) and hence PSC may have a value greater than unity and must be non-
negative. It is valuable to point out that every source must have a
cumulative distribution function based on p ( µ, ϕ ) from which to
sample angular dependence. The probability density function p ( µ, ϕ )
needs only to be considered explicitly for those problems with detectors
or DXTRAN.

Table 10.2 gives the equations for PSC for six continuous source
probability density functions. More discussion of probability density
functions is given in §2.5.6.4.6. The isotropic case is assumed in
MCNP6; therefore SRCDX is required only for the anisotropic case.

As an example of calculating µ 0 , consider a spherical surface cosine
source (type 2 in Table 10.2) with several point detectors in the
problem. Assume that a point on the spherical surface has been selected
at which to

1 The quantities a and b must have values such that PSC is always non-
negative and finite over the range of µ 0 .

Table 10.2: Continuous Source Distributions and Their Associated PSCs

glyph[negationslash]

| Source Description   | Source Distribution   | PSC & Range of µ 0                                                                                                        |
|----------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------|
| Isotropic            | Uniform               | { 0 . 5 - 1 ≤ µ 0 ≤ 1                                                                                                     |
| Surface Cosine       | µ                     | { 2 | µ 0 | 0 ≤ µ 0 ≤ 1 ( or - 1 ≤ µ 0 ≤ 0) 0 - 1 ≤ µ 0 < 0 ( or 0 < µ 0 ≤ 1)                                             |
| Point Cosine         | | µ |                 | { | µ 0 | - 1 ≤ µ 0 ≤ 1                                                                                                   |
| Point Cosine 1       | a + bµ                |          2( a + bµ 0 ) 2 a + b 0 ≤ µ 0 ≤ 1 2( a + bµ 0 ) 2 a - b - 1 ≤ µ 0 < 0 0 - 1 ≤ µ 0 < 0 ( or 0 < µ 0 ≤ 1) |
| Point Cosine 1       | a + bµ, a = 0         | { a + bµ 0 2 a - 1 ≤ µ 0 ≤ 1                                                                                              |
| Point Cosine 1       | a + b | µ |           | { a + bµ 0 2 a + b - 1 ≤ µ 0 ≤ 1                                                                                          |

start a particle. The value of µ 0 for a detector is given by the scalar
(or dot) product of the two directions; that is,

<!-- formula-not-decoded -->

where u , v , and w are the direction cosines of the line from the
source point to the point detector location and u ′ , v ′ , and w ′ are
the direction cosines for either the outward normal if the surface
source is outward or the inward normal if the source is inward.

If u = u ′ , v = v ′ , and w = w ′ , then µ 0 = 1 , indicating that the
point detector lies on the normal line. The value of PSC for the
detector point is

<!-- formula-not-decoded -->

where the parenthetical values of µ 0 are for the inward-directed cosine
distribution.

For | µ 0 | &lt; 0 . 25 in case 2 of Table 10.2, PSC is less than 0.5,
which is the value for an isotropic source. This means that source
emissions for these values of | µ 0 | are less probable than the
isotropic case for this source distribution. The converse is also true.
Note that if | µ 0 | &gt; 0 . 5 , PSC is greater than one, which is
perfectly valid.

An example of a subroutine SRCDX for a surface outward cosine
distribution is shown in Listing 10.35.

```
1 subroutine srcdx 2 ! dummy subroutine for use with user-defined sources 3 4 use mcnp _ global 5 use mcnp _ params 6 use tskcom, only: psc 7 use pblcom, only: pbl 8 use mcnp _ debug 9 10 implicit none
```

Listing 10.35: example\_srcdx\_outward\_cosine.f90.txt

```
11 12 real(dknd) :: up, vp, wp 13 14 ! Calculate PSC for a surface (Sphere) outward cosine distribution. 15 ! Find the direction cosines for this example based on the source 16 ! point on the sphere (X,Y,Z). 17 18 up=(pbl%r%x-rdum(1))/rdum(4) 19 vp=(pbl%r%y-rdum(2))/rdum(4) 20 wp=(pbl%r%z-rdum(3))/rdum(4) 21 22 ! (RDUM(1),RDUM(2),RDUM(3)) are the coordinates of the center 23 ! of the sphere from the RDUM card. RDUM(4) is the radius. 24 ! U,V, and W have been calculated for the current point detector 25 ! in subroutine DDDET. 26 27 psc = 2.0 _ dknd * max(ZERO,pbl%r%u * up + pbl%r%v * vp + pbl%r%w * wp) 28 return 29 end subroutine srcdx
```

This is basically the technique that is used in MCNP6 to calculate PSC
for a spherical surface source in a cosine distribution; the only
difference is that MCNP6 uses the cosines of the direction from the
center of the sphere that selected the source point because this is
normal to the spherical surface. The primed direction cosines were
calculated in Listing 10.35 to aid in illustrating this example. The
direction cosines u , v , and w as defined in Eq. (10.14) have already
been calculated in subroutine DDDET when SRCDX is called and are
available through the pbl (particle) object.

For many sources, a discrete probability density function will be used.
In this situation, a cumulative distribution function P ( µ ) is
available and is defined as

<!-- formula-not-decoded -->

where p j is an average value of the probability density function in the
interval ∆ µ j . Thus, the probability density function is a constant p
j in the interval ∆ µ j . For this case, there are N values of P i with
P 1 = 0 , P N +1 = 1 . 0 and P i -1 &lt; P i . Each value of P i has an
associated value of µ i . Because PSC is the derivative of P ( µ 0 ) ,
then

This is an average PSC between µ i -1 and µ i and is also an average
value of p ( µ ) in the specified range of µ .

<!-- formula-not-decoded -->

Frequently, the cumulative distribution function is divided into N
equally probable intervals. For this case,

<!-- formula-not-decoded -->

This is precisely the form used in MCNP6 for calculating contributions
to the point detector for elastic scattering with N = 32 .

An example of a subroutine SRCDX for a discrete probability density
function is given in the example that follows. This subroutine would
work with the subroutine SOURCE example in §10.3.4, and would calculate
PSC = 1 / 2 for the isotropic distribution.

A biased anisotropic distribution can also be represented by

```
1 SIn -1 ... 1 2 SPn 0 p1 ... pN 3 SBn 0 q1 ... qN
```

A reference vector u ′ , v ′ , w ′ for this distribution is also needed.

The subroutine SOURCE input cards can be modified for this case by
changing the SI 1, SP 1, SB 1, and RDUM cards as follows:

```
1 SI1 -1 0 1 $ These 3 cards 2 SP1 0 2 1 $ represent a biased 3 SB1 0 1 2 $ anisotropic distribution. 4 RDUM 1 0 1 0 $ cylindrical radius and reference vector
```

SOURCE would sample this anisotropic distribution and SRCDX would
calculate the appropriate PSC is shown in Listing 10.36.

```
1 subroutine srcdx 2 ! dummy subroutine for use with user-defined sources 3 4 use mcnp _ params 5 use mcnp _ global 6 use tskcom, only: psc 7 use pblcom, only: pbl 8 use mcnp _ debug 9 10 implicit none 11 12 real(dknd) :: am 13 integer :: i 14 15 ! The variably dimensioned block SPF holds the SI, SP, SB arrays. 16 17 ! RDUM(2), RDUM(3),RDUM(4) --Directional cosines for the source reference 18 ! direction. 19 20 am = pbl%r%u * rdum(2) + pbl%r%v * rdum(3) + pbl%r%w * rdum(4) 21 22 ! KSD(4,1) is the length of the distribution. 23 ! KSD(13,1) is the offset into the SPF block. 24 25 do i=1,ksd(4,1)-1 26 if ( spf(i,ksd(13,1)+1) <= am .and. spf(i+1,ksd(13,1)+1) >= am) then 27 psc = (spf(i+1,ksd(13,1)+2)-spf(i,ksd(13,1)+2))/ & 28 & (spf(i+1,ksd(13,1)+1)-spf(i,ksd(13,1)+1)) 29 psc = psc * spf(i+1,ksd(13,1)+3) 30 exit 31 else 32 psc = ZERO 33 endif 34 enddo 35 36 return 37 end subroutine srcdx
```

Listing 10.36: example\_srcdx\_biased\_anisotropic.f90.txt

## /warning\_sign Caution

It is important to note that the case in Listing 10.36 applies only when
the source is anisotropic with azimuthal symmetry.

For the general case,

<!-- formula-not-decoded -->

The 2 π factor must be applied by the user because MCNP6 assumes
azimuthal symmetry and, in effect, divides the user-defined PSC by 2 π .

For a continuous p ( µ, ϕ ) function, PSC is calculated as above. In the
case of a discrete probability density function,

<!-- formula-not-decoded -->

where µ i -1 ≤ µ 0 &lt; µ i , ϕ i -1 ≤ ϕ 0 &lt; ϕ i , and p ( µ 0 , ϕ 0 ) is
an average probability density function in the specified values of µ 0
and ϕ 0 and P i -P i -1 is the probability of selecting µ 0 and ϕ 0 in
these intervals. For N equally probable bins and n equally spaced ∆ ϕ s,
each 2 π/n wide,

<!-- formula-not-decoded -->

Another way to view this general case is by considering solid angles on
the unit sphere. For an isotropic source, the probability ( P i -P i -1
) of being emitted into a specified solid angle is the ratio of the
total solid angle ( 4 π ) to the specified solid angle ( ∆ µ ∆ ϕ ).
Then, PSC ≡ 0 . 5 . Thus, for the general case (normalized to PSC ≡ 0 .
5 for an isotropic source)

<!-- formula-not-decoded -->

Note that PSC is greater than 0.5 if the specified solid angle ∆ µ ∆ ϕ i
is less than ( P i -P i -1 )4 π . This is the same as the previous
general expression.

## /warning\_sign Caution

Be careful when using your own subroutine SOURCE with either detectors
or DXTRAN. This caution applies to the calculation of the direct
contribution from the source to a point detector, point on a ring, or
point on a DXTRAN sphere. Not only is there the calculation of the
correct value of PSC for an anisotropic source, but there may also be
problems with a biased source.

For example, if an isotropic source is biased to start only in a cone of
a specified angle (for example, Ψ ), the starting weight of each
particle should be WGT × (1 -cos Ψ ) / 2 , where WGT is the weight of
the unbiased source (that is, WGT is the expected weight from a total
source). The weight in SRCDX must be changed to the expected weight WGT
to calculate the direct contribution to a point detector correctly if
PSC is defined to be 0.5.

This example can be viewed in a different way. The probability density
function for the above biased source is

<!-- formula-not-decoded -->
---
title: "Chapter 10.2 - Tally Examples"
chapter: "10.2"
source_pdf: "mcnp631_theory_user-manual/mcnp-primers-examples/10.2_Tally_Examples.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

<!-- image -->

Figure 10.39: Two MCNP6 geometry plots of a cylindrical ( r, z, θ )
embedded geometry. In each plot, the remaining axis points toward the
reader.

<!-- image -->

Figure 10.40: (Cropped) MCNP6 geometry plot of an embedded structured
mesh placed in two unique containers. The left instance is rotated 45 ◦
in addition to being translated 20 cm in the -x direction.

```
1 RZT Test of two checkerboard cylinders with lnk3dnt 2 11 3 -18.7 0 u=e10 imp:n=1 $ inferred geometry cell 3 12 4 -0.001 0 u=e10 imp:n=1 $ inferred geometry cell 4 13 0 0 u=e10 imp:n=1 $ inferred background cell 5 20 0 -1 fill=e10 (20 0 0) imp:n=1 $ fill cell 1 6 21 0 -2 fill=e10 (-20 0 0 -1 1 0 1 1 0)imp:n=1 $ fill cell 2
```

For this example, we assume that surfaces 1 and 2 are off-center spheres
and the transformations shift the embedded geometry universes to be
aligned with the spheres' geometric centers ( x = ± 20 cm). With the
addition of a 45 ◦ counter-clockwise rotation applied to one of the
embedded meshes, we get the geometry displayed in Figure 4-40.

## 10.2 Tally Examples

This section contains examples of the FM , FS , and FT tally cards, a
complicated repeated structures/lattice example, and the TALLYX
subroutine. Refer also to §5.9.1.5 for the basic repeated
structure/lattice tally, and §5.9.17 for TALLYX before trying to
understand these examples.

1

## 10.2.1 FM Card Examples (Simple Form)

## 10.2.1.1 Example 26

Consider input file shown in Listing 10.13.

Listing 10.13: example\_tally\_multiplier\_1.mcnp.inp.txt

| Tally Multiplier (FM)   | Tally Multiplier (FM)   | Tally Multiplier (FM)   | Tally Multiplier (FM)   | Tally Multiplier (FM)   |
|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|
| 10                      | 999                     | -7.0 -1                 | imp:n=1                 |                         |
| 11                      | 0                       |                         | 1 -2 imp:n=1            |                         |
| 12                      | 0                       |                         | 2 imp:n=0               |                         |
| 1                       |                         |                         | 6 so 5                  |                         |
| 2                       |                         |                         | 7 so 6                  |                         |
| sdef                    |                         |                         | 9                       |                         |
| f1:n                    |                         | 1                       |                         |                         |
| nps                     |                         |                         | 2000                    |                         |
| f4:n                    |                         | 10                      |                         |                         |
| fm4                     |                         | 0.04786                 | 999 102                 |                         |
| m999                    |                         |                         | 92238.80c 1.0           |                         |

The F4 neutron tally is the track length estimate of the average fluence
in cell 10. Material 999 is 238 U with an atomic fraction of 100%.

| c=0.04786   | is a normalization factor (such as atom/barn-cm),                                                                    |
|-------------|----------------------------------------------------------------------------------------------------------------------|
| m=999       | is the material number for 238 U as defined on the material card (with an atom density of 0.04786 atom/barn-cm), and |
| r 1 =102    | is the ENDF reaction number for radiative capture cross-section (microscopic).                                       |

The average fluence is multiplied by the microscopic (n, γ ) cross
section of 238 U (with an atomic fraction of 1.0) and then by the
constant 0.04786 (atom/barn-cm). Thus the tally 4 printout will indicate
the number of 239 U atoms/cm 3 produced as a result of (n, γ ) capture
with 238 U.

Standard F6 and F7 tallies can be duplicated by F4 tallies with
appropriate FM 4 cards. The FM 4 card to duplicate F6 is

```
FM4 c m 1 -4
```

where

```
c is 10 -24 × number of atoms per gram, r 1 =1 is the ENDF reaction number for total cross section (barns), and r 2 =-4 is the reaction number for average heating number (MeV/collision)
```

```
and for F7 it is
```

1

10

11

12

13

14

15

```
FM4 c m -6 -8
```

where

```
c is 10 -24 × number of atoms per gram, r 1 =-6 is the reaction number for total fission cross section (barns), and r 2 =-8 is the reaction number for fission Q (MeV/fission).
```

This technique applied to F2 tallies can be used to estimate the average
heating over a surface rather than over a volume. It provides the
surface equivalents of F6 and F7 tallies, which are not available as
standard tallies in MCNP6.

## 10.2.1.2 Example 27

Consider the MCNP input in Listing 10.14, which contains a point
detector.

```
1 Point Detector Tally 2 10 999 -1.0 -1 imp:n=1 3 11 1001 -5.0 1 -2 imp:n=1 4 12 0 2 imp:n=0 5 6 1 so 5 7 2 so 6 8 9 sdef f1:n 1 nps 2000 m999 1001.80c 2 8016.80c 1 F25:N 0 0 0 0 FM25 0.00253 1001 -6 -8 M1001 92238.80c 0.9 92235.80c 0.1
```

Listing 10.14: example\_point\_detector\_1.mcnp.inp.txt

This F25 neutron tally is the fission heating per unit volume of
material 1001 at the origin. Material 1001 does not actually have to be
in a cell at the origin. The FM25 card constants are:

```
c = 0 . 00253 atoms per barn-cm (atomic density) of material 1001, m = 1001 is the material number for material being heated, r1 = -6 is the reaction number for total fission cross section (barn), and r2 = -8 is the reaction number for fission Q (MeV/fission).
```

Other frequently used FM card examples are shown in Listing 10.15.

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

1

2

3

Listing 10.15: example\_fm.mcnp.inp.txt

| f05:n 6 1 0 1               | $ Neutron heating per cm^3 of silicon with an atom          |
|-----------------------------|-------------------------------------------------------------|
| fm05 4.28836E-02 20 1 -4 c  | $ density of 4.28836E-02 bn^-1 * cm^-1 at a point detector. |
| f15x:p 6 1 1                | $ Photon heating per cm^3 of silicon with an atom           |
| fm15 4.28836E-02 20 -5 -6 c | $ density of 4.28836E-02 bn^-1 * cm^-1 at a ring detector.  |
| f1:n 1 2 3                  | $ Number of neutron ** tracks ** crossing surfaces 1, 2,    |
| fm1 1 0                     | $ and 3 per neutron started.                                |
| c                           | c                                                           |
| f35:p 6 1 0 1               | $ Number of photon collisions per source particle that      |
| fm35 1 0                    | $ contribute to the associated point detector.              |
| c                           | c                                                           |
| m99 5011 1                  | $ Number of (n,p) reactions in B-11 per cm^3 in cell 200.   |
| f4:n 200                    | $ Atom density assumed based on a mass density of 1 g/cm^3. |
| fm4 5.570369e-02 99 103     | fm4 5.570369e-02 99 103                                     |
| f104:p 200                  | $ Number of pair-production reactions (mt=516) in           |
| fm104 -1 10 516             | $ iron per cm^3 in cell 100.                                |
| c                           | c                                                           |
| m10 26056 1.0 c             | $ Pure Fe-56 for transport; density: 8 g/cm^3 assumed.      |
| m20 14028 9.222300e-01      | $ Natural silicon for tallying.                             |
| 14029 4.685000e-02          | $ Composition from 'mattool -a 14000 1'.                    |
| 14030 3.092000e-02          | $ Density: 2 g/cm^3 assumed.                                |

## 10.2.2 FM Examples (General Form)

Remember that the hierarchy of operation is multiply first and then add,
and that this hierarchy can not be superseded by the use of parentheses.

## 10.2.2.1 Example 28

```
F4:N 1 FM4 ( 1 (1 -4)(-2)) ( 1 1) $ where c==atomic density (atom/barn-cm) M1 6012.10 1
```

In this example there are three different tallies, namely

1. ρ 1 1 -4
2. ρ 1 -2
3. ρ 1 1

Thus tally (1) will yield the neutron heating in MeV/cm 3 from 12 C in
cell 11. The advantage in performing the multiplication 1 -4 in tally
(1) is that the correct statistics are determined for the desired
product. This would not be true if tally (1) were to be done as two
separate tallies and the product formed by hand after the calculation.

## 10.2.2.2 Example 29

In the example shown in Listing 10.16, one can obtain the total tritium
production per cm 3 from natural lithium (ENDF/B-VII.1 evaluation) in
cell 11.

```
1 Tally Multiplier (FM): Total Tritium Production 2 10 999 -1.0 -1 imp:n=1 $ Water 3 11 1001 -1. 1 -2 imp:n=1 $ Li 4 12 0 2 imp:n=0 5 6 1 so 5 7 2 so 6 8 9 sdef 10 nps 2000 11 M999 1001.80c 2 8016.80c 1 12 M1001 3006.80c 0.0742 3007.80c 0.9258 13 F4:N 11 14 FM4 0.04635 1001 205
```

Listing 10.16: example\_tally\_multiplier\_2.mcnp.inp.txt

The constant c on the FM 4 card is the atomic density of natural
lithium. The reaction number 205 specifies the total tritium production
cross section.

Using older ENDF/B-V evaluated data such as in [343, p. 4-41], one could
specify this reaction as the sum of reactions 105 and 91. Reaction 105
gives tritium production from 6 Li while reaction 91 in ENDF/B-V
represents 7 Li(n,n')t, which in modern data would be the sum of
reaction numbers 52 through 82.

## 10.2.2.3 Example 30

Suppose we have three reactions: r1 , r2 , and r3 , and we wish to add
r2 and r3 and multiply the result by r1 . The following would not be
valid: FM n (C m r 1 (r 2 :r 3 )). The correct card is: FM n (C m (r 1 r
2 :r 1 r 3 )).

## 10.2.3 FMESH Isotopic Reaction Rate Tally Examples

The FMESH card allows the user to calculate isotopic reaction rates on
an arbitrary, user-specified mesh that is independent of the actual
problem geometry [§5.11.2.2].

## 10.2.3.1 Example 31

In the input file shown in Listing 10.17, there are two cells: one
composed of natural uranium and the other as depleted uranium.

```
1 FMESH tally example 2 c Cells 3 900 100 -19.1 -1 imp:n=1 $ Natural Uranium 4 901 200 -19.1 -2 imp:n=1 $ Depleted Uranium 5 902 300 -0.001 1 2 -3 imp:n=1 $ air 6 903 0 3 imp:n=0 $ Void, kill n
```

Listing 10.17: example\_fmesh\_tally\_1.mcnp.inp.txt

```
7 8 c Surfaces 9 1 sx 4 3 10 2 sx -4 3 11 3 so 10 12 13 sdef erg=2 14 mode n 15 nps 500000 16 c 17 c Problem materials 18 c Natural Uranium 19 m100 92238 0.992745 20 92235 0.007200 21 c Hypothetical Depleted Uranium 22 m200 92238 0.9999 23 92235 0.0001 24 c Air 25 m300 7014 -0.755 8016 -0.231 18000 -0.013 26 c Dummy materials for FM mesh tallies 27 m238 92238 1.0 28 m235 92235 1.0 29 c 30 fmesh04:n geom=xyz origin -10 -10 -10 31 imesh 10 iints 100 32 jmesh 10 jints 100 33 kmesh 10 kints 100 34 out=none 35 fmesh14:n geom=xyz origin -10 -10 -10 36 imesh 10 iints 100 37 jmesh 10 jints 100 38 kmesh 10 kints 100 39 out=none 40 fmesh24:n geom=xyz origin -10 -10 -10 41 imesh 10 iints 100 42 jmesh 10 jints 100 43 kmesh 10 kints 100 44 out=none 45 c Tally multipliers 46 +fm04 -1 235 -6 $ fission rate per cm3 from U235 47 +fm14 -1 238 -6 $ fission rate per cm3 from U238 48 +fm24 -1 100 -6 $ total fission rate from both U235 and U238
```

To calculate the fission rates for each isotope in both cells, a mesh
tally is used. The default units of the results are the (number of
fissions) · cm -3 (or cm -3 · shake -1 ) in each mesh cell. For tally
24, material 200 could be used instead of material 100 because both
materials contain the same isotopes.

## 10.2.3.2 Example 32

The input file shown in Listing 10.18 contains a single cell composed of
concrete.

```
1 FMESH tally example 2 c Cells 3 900 10 -2.5 -1 imp:n=1 $ Concrete
```

Listing 10.18: example\_fmesh\_tally\_2.mcnp.inp.txt

```
4 901 11 -7.86 -2 imp:n=1 $ Stainless Steel -202 5 902 12 -0.0012 1 2 -3 imp:n=1 $ Void, transport 6 903 0 3 imp:n=0 $ Void, kill n 7 8 c Surfaces 9 1 sx 6 3 10 2 sx -6 3 11 3 so 10 12 13 sdef erg=2 14 mode n 15 nps 500000 16 c 17 c Problem materials 18 c Ordinary Concrete (rho = 2.35 g/cc) 19 m10 1001 -0.00600 8016 -0.50000 11023 -0.01700 20 13027 -0.04800 14028 -0.28940 14029 -0.01518 21 14030 -0.01042 19000 -0.01900 20000 -0.08300 22 26054 -0.00068 26056 -0.01106 26057 -0.00026 23 c Stainless Steel -202 24 m11 6000 -0.00075 7014 -0.00125 14000 -0.00500 25 15031 -0.00030 16000 -0.00015 24000 -0.18000 26 25055 -0.08750 26000 -0.67505 28000 -0.05000 27 m12 7014 -0.755 8016 -0.232 18000 -0.013 28 m20 11023 1 29 m21 26054 1 30 m22 25055 1 31 c 32 fmesh04:n geom=xyz origin -10 -10 -10 33 imesh 10 iints 50 34 jmesh 10 jints 50 35 kmesh 10 kints 50 36 out=none 37 fmesh14:n geom=xyz origin -10 -10 -10 38 imesh 10 iints 50 39 jmesh 10 jints 50 40 kmesh 10 kints 50 41 out=none 42 fmesh24:n geom=xyz origin -10 -10 -10 43 imesh 10 iints 50 44 jmesh 10 jints 50 45 kmesh 10 kints 50 46 out=none 47 c 48 C 102 = (n,gamma) reaction 49 +fm4 -1 20 102 $ Na-24 production (not in material 11) 50 +fm14 -1 21 102 $ Fe-55 production (2600 in material 11) 51 +fm24 -1 22 102 $ Mn-56 production (not in material 10)
```

We want to calculate the production rate of 24 Na and 55 Fe in the
material. The 23 Na and 54 Fe isotopes are specified on the dummy
material cards because an (n, γ ) reaction on these isotopes produce 24
Na and 55 Fe, respectively. The production rate is calculated by
multiplying the (n, γ ) reaction cross section times the atomic fraction
of the isotope in material 10.

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

## 10.2.4 FS Card Examples

The FS card allows you to subdivide your tally into geometry segments,
avoiding over-specifying the problem geometry with unnecessary cells.

The entries on the FS card are the names and senses of surfaces that
define how to segment any surface or cell tally.

## 10.2.4.1 Example 33

Consider a 1-MeV point isotropic source at the center of a 2-cm cube of
carbon as shown in Listing 10.19.

Listing 10.19: example\_tally\_segment\_1.mcnp.inp.txt

<!-- image -->

| Tally segmenting example   | Tally segmenting example   | Tally segmenting example   | Tally segmenting example   | Tally segmenting example   |
|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|
| 1                          | 1 -2.22                    | 1                          | 2 -3 -4 -5                 | 6 imp:n=1                  |
| 2                          | 0                          |                            | #1                         | imp:n=0                    |
| 1                          | py                         | 0                          |                            |                            |
| 2                          | pz                         | -1                         |                            |                            |
| 3                          | py                         | 2                          |                            |                            |
| 4                          | pz                         | 1                          |                            |                            |
| 5                          | px                         | 1                          |                            |                            |
| 6                          | px                         | -1                         |                            |                            |
| sdef                       |                            | pos =                      | 0 1 0 erg =                | 1                          |
| m1                         |                            | 6012 -1                    |                            |                            |
| f2:n                       |                            | 3                          |                            |                            |
| nps                        | 100                        |                            |                            |                            |

We wish to calculate the flux through a 1-cm 2 window in the center of
one face on the cube. The input file calculating the flux across one
entire face is shown in Fig. 10.41.

The FS card retains the simple cube geometry and four more surface cards
are required,

Figure 10.41: Example 33

|   7 | PX   |   0.5 |
|-----|------|-------|
|   8 | PX   |  -0.5 |

<!-- image -->

1

1

<!-- image -->

Figure 10.42: Example 33

<!-- image -->

The four segmenting surface cards are listed with the other surface
cards, but they are not part of the actual geometry and hence do not
complicate the cell-surface relationships.

The F2 tally is subdivided into five separate tallies as shown in Fig.
10.42: 1) the first is the flux of particles crossing surface 3 but with
a positive sense to surface 7; 2) the second is the remaining flux with
negative sense to surface 7 crossing surface 3 but with a negative sense
to surface 10; 3) the third is the remaining flux (negative sense to 7
and positive sense to 10) crossing 3 but with a negative sense to 8; 4)
the remaining flux with positive sense to 9; and 5) everything else. In
this example, the desired flux in the window is in the fifth sub-tally-
the 'everything else' portion.

The FS segmenting card could have been set up other ways. For example:

```
FS2 -10 7 9 -8
```

and

```
FS2 -8 9 -10 7
```

Each works, but the order of the sub-tallies is changed. A way to avoid
the five sub-tallies and to get only the window of interest is to use
the TALLYX subroutine [§5.9.17, §10.2.8].

## 10.2.4.2 Example 34

Consider a source at the center of a 10-cm-radius sphere called cell 1.
We want to determine the fission heating in a segment of the sphere
defined by the intersection of the 10-cm sphere, an 8-cm inner sphere,
and a 20-degree cone (i.e., the angle between the axis and surface of
the cone is 20 ◦ ) whose vertex is at the source and is about the y
axis. This is accomplished by using

```
1 F7:N 1 2 FS7 -2 -3
```

where surface 2 is the 8-cm sphere and surface 3 is the cone. This
breaks the F7 tally up into three portions:

1. the heating inside the 8-cm sphere;
2. the heating outside the 8-cm sphere but within the cone-this is the desired portion; and
3. everything else, which is a 2-cm shell just inside the 10-cm sphere but outside the cone.

## 10.2.5 FT Examples

## 10.2.5.1 Example 35

Consider the following input cards.

| F1:N   | 2            |
|--------|--------------|
| FT1    | FRV v1 v2 v3 |

The FT n card is the special treatment for tallies card. Various tally
treatments are available for certain specific tally requirements. The FT
n tally with the FRV keyword used in conjunction with tally type 1 will
redefine the vector normal to the tally surface. In this case, the
current over surface 2 (tally type 1) uses the vector ( v 1 , v 2 , v 3)
as its reference vector for getting the cosine for binning.

## 10.2.5.2 Example 36

| F5:P   | 4 5 6   |
|--------|---------|
| FT5    | ICD     |
| FU5    | 1 3     |

In this example the photon flux at detector 5 is being tallied. However,
only the contributions to the detector tally from cells 1 and 3 are of
interest. The ICD keyword allows the user to create a separate bin for
each cell, and only contributions from one of the specified cells are
scored. The FU n card specifies the cells from which tallies are to be
made, but TALLYX is not called.

## 10.2.5.3 Example 37

When keeping track of charged particle current across a surface, it is
sometimes desirable to track both positive and negative score
contributions, applicable in cases that include charged particles.
Consider a photon source that is enclosed in a spherical shell of lead
as shown in Listing 10.20.

```
1 electron current example 2 1 1 -0.001124 -11 imp:e=1 imp:p=1 3 2 2 -11.0 11 -21 imp:e=1 imp:p=1 4 3 0 21 imp:e=0 imp:p=0 5 6 11 so 30 7 21 so 32 8 9 m1 6012 0.000125 7014 0.6869 8016 0.301248 18040 0.011717 10 m2 82000 1. 11 mode p e 12 sdef pos = 0. 0. 0. erg = 2.5 13 f1:e 21 14 ft1 elc 2 15 f2:p 21 16 e2 1e-3 1e-2 0.1 0.5 1.0 1.5 2.0 2.5 C 17 nps 10000
```

Listing 10.20: example\_tally\_electron\_current.mcnp.inp.txt

If a surface current tally is taken over the sphere and it is desirable
to tally both the positron and electron current separately, then the
special treatment card option is invoked.

The input deck shown in Listing 10.20 models a sphere filled with dry
air surrounded by a spherical shell of lead. The centrally located
source emits 2.5-MeV photons that travel through the air into the lead
shell. The F1 surface current tally has been modified with the ELC
special tally option. The parameter value of 2 that follows the ELC
keyword specifies that positrons and electrons be placed into separate
tally user bins. Once this option has been invoked, the user can inspect
the output tally bins for the respective scoring of either particle.

The F2 tally scores photon flux crossing surface 21, scored into energy
bins defined on the E 2 card. The C at the end of the energy bin card
indicates that the bins are cumulative. For instance, the bin with an
upper limit of 1 MeV would contain scores from particles that cross
surface 21 with energy less than or equal to 1 MeV.

## 10.2.5.4 Example 38

Consider the following two point sources, each with a different energy
distribution:

<!-- image -->

| sdef   | pos=d1   | erg=fpos d2   |
|--------|----------|---------------|
| si1    | L 5 3    | 6 75 3 6      |
| sp1    | 0.3      | 0.7           |
| ds2    | S 3 4    |               |
| si3    | H 2 10   | 14            |
| sp3    | D 0      | 1 2           |
| si4    | H 5      | 2 8           |
| sp4    | D 0      | 3 1           |
| f2:n   | 2        |               |
| ft2    |          | scd           |
| fu2    |          | 3 4           |

The SCD option causes tallies to be binned according to which source
distribution was sampled. The FU n card is used to list the distribution
numbers of interest. Thus, the tallies in this example are placed in one
of

two bins, depending on which of the two sources emitted the particle.
The two sources may represent two nuclides with different energy
distributions. In this case use of the SCD option allows the user to
determine each nuclide's contribution to the final tally.

## 10.2.5.5 Example 39: Capture Tallies: Interpreting Capture Tally Output

The FT8 CAP coincidence capture tally option produces both a standard tally, which is generally unreadable, and a coincidence capture table, PRINT Table 118. An example is provided to help in the interpretation of this table:

<!-- image -->

The capture tally input for this problem was

| F8:n    | 999 $ input F8 card             |
|---------|---------------------------------|
| FT8 CAP | -8 -8 2003 $ input FT8 CAP card |

Note that the line ' captures &gt; 7 ' indicates that nine histories had
eight or more neutrons captured. This implies that 8 histories had 8 × 8
= 64 neutrons captured and 1 history had 1 × 9 neutrons captured, for a
total of 73 neutrons captured. The table of captures evidently was too
short, and the problem should have been run with FT8 CAP -9 -9 or even
more captures and moments. Not specifying enough capture rows affects
only the captures &gt; 7 lines and the error estimate on the totals capture
line; all other information is correct as if more captures and moments
were listed.

As an interpretation of the neutron captures on 3he portion of the
table, Column 1 is the number of histories according to the number of
captures by the designated material (2003 = 3 He) in the designated cell
(999). This number sums to the total number of source histories for the
problem, NPS 10000 .

Column 2 is the number of captures by 3 He in cell 999=21794. Because
analog capture is the default for F8 tallies, the total weight captured
is also 21794.

Column 3 is the total weight captured divided by the tally
normalization. In this problem, SDEF PAR = SF , and the tally
normalization is the source particles = spontaneous fission neutrons =
21512. Thus, captures by weight are 21794 . 0 / 21512 = 1 . 01311 .

Column 4 is the multiplicity fraction by number, which is Column 1
divided by the number of source histories. The total is always 1.00000.

Column 5 is the multiplicity fraction by weight, which is the weight of
histories undergoing capture divided by the tally normalization. In this
problem, SDEF PAR = SF and the multiplicity fraction by weight is 10000
. 0 / 21512 = 0 . 464857 .

Note that for SDEF PAR = -SF , the tally normalization is the number of
source histories = number of spontaneous fissions = 10000. Therefore,
for SDEF PAR = -SF , all of the columns that are labeled by weight would
be consistent with the values reported in the columns labeled by number
in both the neutron capture on 3he and factorial moments sections of
PRINT Table 118. For example, if SDEF PAR = -SF , then column 3 would be
21794 . 0 / 10000 = 2 . 17940 , and column 5 would be 10000 . 0 / 10000
= 1 . 00000 in the neutron capture on 3he portion of the table.

The interpretation of the factorial moments portion of the table now
follows.

The first moment by number is the number of captures divided by the
number of source histories = 21794 / 10000 = 2 . 17940 .

The first moment by weight is the total weight of capture divided by the
tally normalization. In this problem, SDEF PAR = SF and the first moment
by weight is 21794 . 0 / 21512 = 1 . 01311 .

The second moment is N × ( N -1) / 2 , where N is the number of
captures. In this problem,

| N     | N × ( N - 1) / 2   |    | histories   |    |       |
|-------|--------------------|----|-------------|----|-------|
| 1     | 0                  | ×  | 2285        | =  |     0 |
| 2     | 1                  | ×  | 3223        | =  |  3223 |
| 3     | 3                  | ×  | 2489        | =  |  7467 |
| 4     | 6                  | ×  | 1022        | =  |  6132 |
| 5     | 10                 | ×  | 209         | =  |  2090 |
| 6     | 15                 | ×  | 51          | =  |   765 |
| 7     | 21                 | ×  | 12          | =  |   252 |
| 8     | 28                 | ×  | 8           | =  |   224 |
| 9     | 36                 | ×  | 1           | =  |    36 |
| Total |                    |    |             |    | 20189 |

and the second moment by number is divided by the number of histories,
20189 / 10000 = 2 . 01890 .

Because of analog capture, the second moment weight is 20189.0. The
second moment by weight is divided by the tally normalization. In this
problem, SDEF PAR = SF , and the second moment by weight is 20189 . 0 /
21512 = 0 . 938499 .

The seventh moment is

thus, 17 / 10000 = 0 . 0017 .

And the ninth moment is thus, 1 / 10000 = 0 . 0001 .

## 10.2.5.6 Example 40: Capture Tallies with Time Gating

The coincidence capture tally optionally allows specification of
predelay and gate width [317] with the GATE keyword on the FT8 card. The
GATE keyword may appear anywhere after the CAP keyword and is part of
the CAP command. Immediately following, the GATE keyword must be the
predelay time and the total gate width, both in units of shakes ( 10 -8
s).

The addition of the predelay and time gate width changes the capture
tally scoring. When a neutron is captured at time t 0 in the specified
cell by the specified nuclide (22 and 3 He in this example), the gate is
'turned on.' If the predelay is t 1 and the gate width is t 2 , then all
captures between t 0 + t 1 and t 0 + t 1 + t 2 are counted. For a
history with no captures, no events are scored. With one capture, 0
events are scored. With two captures, the first turns on the time gate
are at time t 0 and scores 0; the second will score one event if it is
captured between t 0 + t 1 and t 0 + t 1 + t 2 or score another 0 if
outside the gate.

Other entries after the CAP keyword may be placed in any order, as shown
in the following examples. The negative entries change the allowed
number of captures and moments (defaults 21 and 12 are changed to 40 and
40 in F78 in this example). The list of capture nuclides may be placed
anywhere after CAP .

Examples for three capture tallies now follow. The capture tally without
gating ( F18 ) is shown for reference. An infinite gate ( F38 ) results
in a very different PRINT Table 118: the number of captures is the same,
but the moments are offset by one. A finite gate ( F78 ) has fewer
captures, as expected.

| 7 × 6 × 5 × 4 × 3 × 2 × 1 / 7!   | =   | 1   | ×   | 12   |   12 |
|----------------------------------|-----|-----|-----|------|------|
| 8 × 7 × 6 × 5 × 4 × 3 × 2 / 7!   | =   | 8   | ×   | 8    |   64 |
| 9 × 8 × 7 × 6 × 5 × 4 × 3 / 7!   | =   | 36  | ×   | 1    |   36 |
| Total                            |     |     |     |      |  112 |

thus, 112 / 10000 = 0 . 0112 .

The eighth moment is

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

1

2

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

39

## 10.2.5.6.1 Case A: Capture Tally without Gate

## Input:

| f18:n 22      |
|---------------|
| ft18 cap 2003 |

## Output:

<!-- image -->

## 10.2.5.6.2 Case B: Infinite Gate

Input:

1

2

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

39

40

41

42

43

44

45

46

| f38:n 22                  |
|---------------------------|
| ft38 cap 2003 gate 0 1e11 |

## Output:

<!-- image -->

## 10.2.5.7 Case C: Finite Gate

## Input:

```
1 f78:n 22 2 ft78 cap gate .5 .4 -40 -40 2003
```

## Output:

```
1 1 neutron captures, moments and multiplicity distributions. tally 78 print table 118 2 3 weight normalization by source histories = 20000 4 5 cell: 22 6 7 neutron captures on 3he 8 9 time gate: predelay = 5.0000E-01 gate width = 4.0000E-01 10 11 pulses occurrences occurrences pulse fraction 12 in gate histogram by number by weight by number by weight error 13 14 captures = 0 7837 0 0.00000E+00 3.91850E-01 3.91850E-01 0.0118 15 captures = 1 394 394 1.97000E-02 1.97000E-02 1.97000E-02 0.0666 16 captures = 2 67 134 6.70000E-03 3.35000E-03 3.35000E-03 0.1542 17 captures = 3 6 18 9.00000E-04 3.00000E-04 3.00000E-04 0.4082 18 captures = 4 1 4 2.00000E-04 5.00000E-05 5.00000E-05 1.0000 19 20 total 8305 550 2.75000E-02 4.15250E-01 4.15250E-01 0.0624 21 22 factorial moments by number by weight 23 24 n 2.75000E-02 0.0717 2.75000E-02 0.0716 25 n(n-1)/2! 4.55000E-03 0.1654 4.55000E-03 0.1654 26 n(n-1)(n-2)/3! 5.00000E-04 0.4690 5.00000E-04 0.4690 27 n(n-1)(n-2) ... (n-3)/4! 5.00000E-05 1.0000 5.00000E-05 1.0000
```

Scratch space is needed to save capture times during the course of a
history. The times are stored temporarily in the capture and moment bins
of the tally. If sufficient bins are unavailable, then the number of
allowed captures and moments must be increased using the negative
entries after the CAP keyword. The message *** warning *** dimension
overflow. Some pulses not counted. is written in PRINT Table 118 if the
space needs to be increased.

## 10.2.5.8 Example 41: Residual Nuclei Tally

The input file shown in Listing 10.21 models a 1.2-GeV proton source
having a single collision with 208 Pb.

```
1 Test of p(1.2GeV)+Pb(208) 2 1 1 -11. -1 imp:h 1 3 2 0 1 imp:h 0
```

Listing 10.21: example\_residual\_nuclei\_tally.mcnp.inp.txt

<!-- image -->

Figure 10.43: Residuals for 81 Tl isotopes 189 to 201 from 1.3-GeV
protons on 208 82 Pb.

<!-- image -->

These data are plotted in Fig. 10.43, with MCNP6 using the tally plotter
and the execute line command

1

```
mcnp6 z com=com91
```

where the command file, com91 , is

```
1 rmctal=mctl91 2 tally 8 free u xlim 81189 8120 ylim .0001 .01
```

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

## 10.2.5.9 Example 42: ROC Curve Generation

The input file in Listing 10.22 models a 15-MeV photon source incident
on a 238 U sphere (10 kg). This source is represented as a single 10 µ s
pulse of 10 7 photons ( S i ). A 1 /E background source is specified in
the surrounding cube (200 cm each side), and the FT card PHL option is
used to generate a receiver operating characteristic (ROC) curve from
the signal and noise components tallied in a Ge detector for 60 s. The
Ge detector is surrounded by 2 cm of Pb. The flux of the background
photons was taken as 10 γ /cm 2 /min. The background source strength ( S
b ) to produce this flux is given by A · F/ 3 . 7 , where A is the
surface area of the cube and F is the flux (the factor of 3.7 comes from
the shape of the cube-for a sphere this factor is 1.0). This results in
S b = 6 · 200 · 200 · 10 / 3 . 7 , or 648648 photons. The probability of
sampling each source component becomes

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

or P i = 0 . 9391 and P b = 0 . 0609 , as seen on the SP1 card. The NHB
parameter of the ROC option is set to the sum of these sources, or
10648648. In this example, we ran 10 batches to formulate the signal and
noise PDFs and the related ROC curve.

Listing 10.22: example\_tally\_roc\_1.mcnp.inp.txt

|               | Generate   | ROC           | curve     |               | for      | 15-MeV photons   | into U-238                                        |
|---------------|------------|---------------|-----------|---------------|----------|------------------|---------------------------------------------------|
| 1             | 0          |               | -1        |               | 2        | 6 4              | imp:n,p=1                                         |
| 2             | 0          |               | -2        |               |          |                  | imp:n,p=1                                         |
| 4             | 1          | -5.16         |           | -3            |          |                  | imp:n,p=1                                         |
| 5             | 2          | -19.0         |           | -4            |          |                  | imp:n,p=1                                         |
| 6             | 0          |               |           | -5            |          |                  | imp:n,p=1                                         |
| 7             | 3          | -11.3         |           | -6            | 3        | 5                | imp:n,p=1                                         |
| 8             | 0          |               |           | 1             |          |                  | imp:n,p=0                                         |
| 1             | rpp so     | -100 5.0      | 100       | 25            | -100 10  | 100 -100         | 100                                               |
| 2 3           | rcc        | 20            | 0         | 0 0           |          | 4.0              |                                                   |
| 4             | sph        | 20            | 0         | 0 5.0         | 5        | 4.0              |                                                   |
| 5             | rcc        | 20            | 0 20      | 0 0           | 0 17     | 6.0              |                                                   |
| 6             | rcc        |               | 0         | 0             |          |                  |                                                   |
| mode          | p          | 20 n          | 20        |               |          |                  |                                                   |
| m1 m2         |            |               | 92238.70c | 32074.70c 1 1 |          |                  |                                                   |
| m3            |            |               | 82208.70c |               | 1        |                  |                                                   |
|               | mphys      | on            |           |               |          |                  |                                                   |
| mx2:p         |            |               | model     |               |          |                  |                                                   |
| cut:n         |            | 60e8          | 60e8      |               |          |                  |                                                   |
| phys:p act    | cut:p      | j 1 fission=p | j -1      | nonfiss=p     | x=ferg   |                  |                                                   |
| sdef          |            | par=p vec=1   | 0         | erg=d1 0      | dir=ferg | d2 d8            | dg=mg y=ferg d3 z=ferg d4 tme=ferg d7 cel=1 wgt=1 |
| si1 s sp1 ds2 | s          | 15            | 5 16      | 0.9391        | 6 0.0609 |                  |                                                   |
| ds3           | s          | 25            |           | 26            |          |                  |                                                   |
|               | s          |               | 35        | 36            |          |                  |                                                   |
| ds4           |            |               |           |               |          |                  |                                                   |
| ds7           | s          |               | 45        | 46            |          |                  |                                                   |
|               | s          |               | 55        | 56            |          |                  |                                                   |
| ds8           |            |               |           |               |          |                  |                                                   |

<!-- image -->

The ROC output for Tally 1 is provided in PRINT Table 163, shown in
Listing 10.23. The first printed plot is the ROC curve itself, plotting
the noise PDF (usually referred to as the probability of false alarm)
versus the signal PDF (usually referred to as the probability of
detection). The data for the signal and noise PDFs is provided in the
subsequent table. The jagged behavior of the ROC curve can be
significantly refined by increasing the number of batches (say from 10
to 100, or by running 1064864800 particle histories).

<!-- image -->

|                      | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            | Listing 10.23: example_tally_roc_1.mcnp.outp.txt                                                            |
|----------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| 1roc curve for tally | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  | 1 10 batches, signal mean= 3.029E+01 noise mean= 2.960E+01 nps = 106486480 print table 163                  |
| abscissa             | ordinate                                                                                                    | 2 3 LA-UR-24-24602,                                                                                         | plot of                                                                                                     | probability                                                                                                 | of detection                                                                                                | versus                                                                                                      | probability                                                                                                 | of false                                                                                                    | alarm - 0                                                                                                   | to 100                                                                                                      | percent                                                                                                     | 2 3 LA-UR-24-24602,                                                                                         |
| noise                | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | signal:--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 |
| 1.000                | 0.000|x                                                                                                     | |                                                                                                           | |                                                                                                           | |                                                                                                           | | |                                                                                                         |                                                                                                             | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 2.000                | 0.000|x                                                                                                     | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 3.000                | 0.000|x                                                                                                     | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 4.000                | 0.000|x                                                                                                     | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 5.000                | 0.000|x                                                                                                     | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 6.000                | 0.000|x                                                                                                     | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 7.000                | 0.000|x                                                                                                     | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 8.000                | 0.000|x                                                                                                     | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 9.000                | 0.000|x                                                                                                     | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 10.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 11.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 12.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 13.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 14.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 15.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 16.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 17.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 18.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 19.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 20.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 21.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 22.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 23.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 24.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 25.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 26.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 27.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 28.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 29.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 30.000               | 10.000|                                                                                                     | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 31.000               | 12.000|                                                                                                     | | x                                                                                                         | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 32.000               | 14.000|                                                                                                     | | x                                                                                                         | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 33.000               | 16.000|                                                                                                     | |                                                                                                           | x |                                                                                                         | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 34.000               | 18.000|                                                                                                     | |                                                                                                           | x |                                                                                                         | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 35.000               | 20.000|                                                                                                     | |                                                                                                           | x                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 36.000               | 22.000|                                                                                                     | |                                                                                                           | | x                                                                                                         | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |
| 37.000               | 24.000|                                                                                                     | |                                                                                                           | | x                                                                                                         | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           | |                                                                                                           |                                                                                                             |

|                      | 38.000   | 26.000| |   | | x   | |   | |   | | |     | |     | | | |         |
|----------------------|----------|-------------|-------|-----|-----|---------|-------|---------------|
| 39.000               | 28.000|  | |           | |     | |   | |   | | |     | |     | x | | |       |
| 40.000               | 40.000|  | |           | |     | x   | |   | | |     | |     | | | |         |
| 41.000               | 40.000|  | |           | |     | x   | |   | | |     | |     | | | |         |
| 42.000               | 40.000|  | |           | |     | x   | |   | | |     | |     | | | |         |
| 43.000               | 40.000|  | |           | |     | x   | |   | | |     | |     | | | |         |
| 44.000               | 40.000|  | |           | |     | x   | |   | | |     | |     | | | |         |
| 45.000               | 40.000|  | |           | |     | x   | |   | | |     | |     | | | |         |
| 46.000               | 40.000|  | |           | |     | x   | |   | | |     | |     | | | |         |
| 47.000               | 40.000|  | |           | |     | x   | |   | | |     | |     | | | |         |
| 48.000               | 40.000|  | |           | |     | x   | |   | | |     | |     | | | |         |
| 49.000               | 40.000|  | |           | |     | x   | |   | | |     | |     | | | |         |
| 50.000               | 50.000|  | |           | |     | |   | x   | | |     | |     | | | |         |
| 51.000               | 50.000|  | |           | |     | |   | x   | | |     | |     | | | |         |
| 52.000               | 50.000|  | |           | |     | |   | x   | | |     | |     | | | |         |
| 53.000               | 50.000|  | |           | |     | |   | x   | | |     | |     | | | |         |
| 54.000               | 50.000|  | |           | |     | |   | x   | | |     | |     | | | |         |
| 55.000               | 50.000|  | |           | |     | |   | x   | | |     | |     | | | |         |
| 56.000               | 50.000|  | |           | |     | |   | x   | | |     | |     | | | |         |
| 57.000               | 50.000|  | |           | |     | |   | x   | | |     | |     | | | |         |
| 58.000               | 50.000|  | |           | |     | |   | x   | | |     | |     | | |           |
| 59.000               | 50.000|  | |           | |     | |   | x   | | |     | |     | | | | |       |
| 60.000               | 70.000|  | |           | |     | |   | |   | | x     | |     | | | |         |
| 61.000               | 71.000|  | |           | |     | |   | |   | | |x    | |     | | | |         |
| 62.000               | 72.000|  | |           | |     | |   | |   | | | x   | |     | | | |         |
| 63.000               | 73.000|  | |           | |     | |   | |   | | | x   | |     | | | |         |
| 64.000               | 74.000|  | |           | |     | |   | |   | | |     | x |   | | | |         |
| 65.000               | 75.000|  | |           | |     | |   | |   | | |     | x |   | | | |         |
| 66.000               | 76.000|  | |           | |     | |   | |   | | |     | x | x | | | |         |
| 67.000               |          | |           | |     | |   | |   | | |     | |     | 77.000| | | | |
| 68.000               | 78.000|  | |           | |     | |   | |   | | | x   | |     | | | |         |
| 69.000               | 79.000|  | |           | |     | |   | |   | | |     | x|    | | | |         |
| 70.000               | 80.000|  | |           | |     | |   | |   | | |     | x     | | | |         |
| 71.000               | 80.000|  | |           |       | |   | |   | | |     | x     | | | |         |
| 72.000               | 80.000|  | |           | | |   |     |     | | |     |       | | | |         |
| 73.000               | 80.000|  | |           | |     | |   | |   | | |     | x     | | | |         |
| 74.000               | 80.000|  | |           | |     | |   | | | | | |     | x x   | | | |         |
| 75.000               | 80.000|  | |           | |     | | | | |   | | |     | x     | | | | |       |
| 76.000 77.000 78.000 | 80.000|  | 80.000| | | | | |   | | | | |   | | | | | | x x   | | | | |       |
|                      | 80.000|  | |           | |     | |   | |   | |       | x     | |             |
| 79.000               |          |             |       | |   | |   | |       |       | |             |
|                      |          |             |       |     |     | |       |       | | |           |
|                      | 80.000|  | |           | |     |     | |   | |       | x     | | | |         |

10.2.

Tally Examples

<!-- image -->

| 80.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
|---------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| 81.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 82.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 83.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 84.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 85.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 86.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 87.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 88.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 89.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 90.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 91.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 92.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 93.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 94.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 95.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 96.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 97.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | |                                                                                                   | x                                                                                                     |
| 98.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | | | |                                                                                                 | x                                                                                                     |
| 99.000              | 100.000|                                                                                              | 100.000|                                                                                              | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | |                                                                                                     | x                                                                                                     |
|                     | |--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | |--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | |--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | |--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | |--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | |--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | |--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | |--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | |--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 | |--------10--------20--------30--------40--------50--------60--------70--------80--------90-------100 |
| tally               | signal                                                                                                | signal                                                                                                | noise                                                                                                 | noise                                                                                                 | noise                                                                                                 | noise                                                                                                 | noise                                                                                                 | noise                                                                                                 | noise                                                                                                 | noise                                                                                                 |
| upper bin           | pdf                                                                                                   | cum.                                                                                                  | pdf                                                                                                   | cum.                                                                                                  |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 1.819E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 1.000E-01                                                                                             | 1.000E+00                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 1.838E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 1.857E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 1.876E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 1.895E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 1.914E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 1.933E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 1.952E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 1.971E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 1.990E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 2.009E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 2.028E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 2.047E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 2.066E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 2.085E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 2.104E+01           | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 1.000E-01                                                                                             | 9.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
|                     | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 8.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |
| 2.123E+01 2.142E+01 | 0.000E+00                                                                                             | 1.000E+00                                                                                             | 0.000E+00                                                                                             | 8.000E-01                                                                                             |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |                                                                                                       |

10.2.

Tally Examples

|   2.161E+01 |     |   0.000E+00 |   1.000E+00 |   0.000E+00 | 8.000E-01   |
|-------------|-----|-------------|-------------|-------------|-------------|
|       21.8  | 0   |         1   |         0   |         0.8 | Chapter     |
|       21.99 | 0   |         1   |         0   |         0.8 |             |
|       22.18 | 0   |         1   |         0   |         0.8 | 10.         |
|       22.37 | 0   |         1   |         0   |         0.8 |             |
|       22.56 | 0   |         1   |         0   |         0.8 | Examples    |
|       22.75 | 0   |         1   |         0   |         0.8 |             |
|       22.94 | 0   |         1   |         0   |         0.8 |             |
|       23.13 | 0   |         1   |         0   |         0.8 |             |
|       23.32 | 0   |         1   |         0   |         0.8 |             |
|       23.51 | 0   |         1   |         0   |         0.8 |             |
|       23.7  | 0   |         1   |         0   |         0.8 |             |
|       23.89 | 0   |         1   |         0   |         0.8 |             |
|       24.08 | 0.1 |         1   |         0   |         0.8 |             |
|       24.27 | 0   |         0.9 |         0   |         0.8 |             |
|       24.46 | 0   |         0.9 |         0   |         0.8 |             |
|       24.65 | 0   |         0.9 |         0   |         0.8 |             |
|       24.84 | 0   |         0.9 |         0   |         0.8 |             |
|       25.03 | 0   |         0.9 |         0   |         0.8 |             |
|       25.22 | 0   |         0.9 |         0   |         0.8 |             |
|       25.41 | 0   |         0.9 |         0   |         0.8 |             |
|       25.6  | 0   |         0.9 |         0   |         0.8 |             |
|       25.79 | 0   |         0.9 |         0   |         0.8 |             |
|       25.98 | 0   |         0.9 |         0   |         0.8 |             |
|       26.17 | 0   |         0.9 |         0   |         0.8 |             |
|       26.36 | 0   |         0.9 |         0   |         0.8 |             |
|       26.55 | 0   |         0.9 |         0   |         0.8 |             |
|       26.74 | 0   |         0.9 |         0   |         0.8 |             |
|       26.93 | 0   |         0.9 |         0   |         0.8 |             |
|       27.12 | 0.1 |         0.9 |         0   |         0.8 |             |
|       27.31 | 0   |         0.8 |         0   |         0.8 |             |
|       27.5  | 0   |         0.8 |         0   |         0.8 |             |
|       27.69 | 0   |         0.8 |         0   |         0.8 |             |
|       27.88 | 0   |         0.8 |         0   |         0.8 |             |
|       28.07 | 0   |         0.8 |         0.1 |         0.8 |             |
|       28.26 | 0   |         0.8 |         0   |         0.7 | 10.2.       |
|       28.45 | 0   |         0.8 |         0   |         0.7 |             |
|       28.64 | 0   |         0.8 |         0   |         0.7 |             |
|       28.83 | 0   |         0.8 |         0   |         0.7 | Tally       |
|       29.02 | 0.1 |         0.8 |         0.1 |         0.7 |             |
|       29.21 | 0   |         0.7 |         0   |         0.6 |             |
|       29.4  | 0   |         0.7 |         0   |         0.6 | Examples    |

|   2.959E+01 |   0.000E+00 |   7.000E-01 |   0.000E+00 |   6.000E-01 |
|-------------|-------------|-------------|-------------|-------------|
|       29.78 |         0   |         0.7 |         0   |         0.6 |
|       29.97 |         0.2 |         0.7 |         0   |         0.6 |
|       30.16 |         0   |         0.5 |         0.1 |         0.6 |
|       30.35 |         0   |         0.5 |         0   |         0.5 |
|       30.54 |         0   |         0.5 |         0   |         0.5 |
|       30.73 |         0   |         0.5 |         0   |         0.5 |
|       30.92 |         0.1 |         0.5 |         0   |         0.5 |
|       31.11 |         0   |         0.4 |         0.1 |         0.5 |
|       31.3  |         0   |         0.4 |         0   |         0.4 |
|       31.49 |         0   |         0.4 |         0   |         0.4 |
|       31.68 |         0   |         0.4 |         0   |         0.4 |
|       31.87 |         0.1 |         0.4 |         0   |         0.4 |
|       32.06 |         0.2 |         0.3 |         0.1 |         0.4 |
|       32.25 |         0   |         0.1 |         0   |         0.3 |
|       32.44 |         0   |         0.1 |         0   |         0.3 |
|       32.63 |         0   |         0.1 |         0   |         0.3 |
|       32.82 |         0   |         0.1 |         0   |         0.3 |
|       33.01 |         0   |         0.1 |         0   |         0.3 |
|       33.2  |         0   |         0.1 |         0   |         0.3 |
|       33.39 |         0   |         0.1 |         0   |         0.3 |
|       33.58 |         0   |         0.1 |         0   |         0.3 |
|       33.77 |         0   |         0.1 |         0   |         0.3 |
|       33.96 |         0   |         0.1 |         0   |         0.3 |
|       34.15 |         0   |         0.1 |         0   |         0.3 |
|       34.34 |         0   |         0.1 |         0   |         0.3 |
|       34.53 |         0   |         0.1 |         0   |         0.3 |
|       34.72 |         0   |         0.1 |         0   |         0.3 |
|       34.91 |         0   |         0.1 |         0   |         0.3 |
|       35.1  |         0   |         0.1 |         0.2 |         0.3 |
|       35.29 |         0   |         0.1 |         0   |         0.1 |
|       35.48 |         0   |         0.1 |         0   |         0.1 |
|       35.67 |         0   |         0.1 |         0   |         0.1 |
|       35.86 |         0   |         0.1 |         0   |         0.1 |
|       36.05 |         0   |         0.1 |         0   |         0.1 |
|       36.24 |         0   |         0.1 |         0   |         0.1 |
|       36.43 |         0   |         0.1 |         0   |         0.1 |
|       36.62 |         0   |         0.1 |         0   |         0.1 |
|       36.81 |         0.1 |         0.1 |         0   |         0.1 |
|       37    |         0   |         0   |         0.1 |         0.1 |

## 10.2.6 Repeated Structure/Lattice Tally Example

An explanation of the basic repeated structure/lattice tally format can
be found in §5.9.1.5. The example shown here illustrates more complex
uses.

## 10.2.6.1 Example 43: Repeated-structure Lattice-tally Example

An example repeated structure lattice tally with a complicated track-
length tally is shown in Listing 10.24.

```
1 Repeated structure lattice tally example 2 1 0 -1 -2 3 13 fill=4 3 2 0 -1 -2 3 -13 fill=1 4 3 0 -4 5 -6 7 u=1 lat=1 5 fill=-2:2 -2:0 0:0 1 1 3 1 1 1 3 2 3 1 3 2 3 2 3 6 4 0 -8 9 -10 11 u=2 fill=3 lat=1 7 5 0 -12 u=3 8 6 0 12 u=3 9 7 0 -14 -2 3 u=4 fill=3 trcl=(-60 40 0) 10 8 like 7 but trcl=(-30 40 0) 11 9 like 7 but trcl=(0 40 0) 12 10 like 7 but trcl=(30 40 0) 13 11 like 7 but trcl=(60 40 0) 14 12 0 #7 #8 #9 #10 #11 u=4 15 13 0 1:2:-3 16 17 1 cz 100 18 2 pz 100 19 3 pz -100 20 4 px 20 21 5 px -20 22 6 py 20 23 7 py -20 24 8 px 10 25 9 px -10 26 10 py 10 27 11 py -10 28 12 cz 5 29 13 py 19.9 30 14 cz 10 31 32 sdef 33 f4:n 5 6 (5 6 3) $ a: 3 bins 34 (5<3) (5<(3[-2:2 -2:0 0:0])) $ b: 2 bins 35 (5<(7 8 9 10 11)) (5<7 8 9 10 11<1) (5<1) $ c: 7 bins 36 ((5 6)<3[0 -1 0]) ((5 6)<3[0:0 -1:-1 0:0]) ((5 6)<3[8]) $ d: 3 bins 37 (5<(4[0 0 0]3[8]))(5<4[0 0 0]<3[8]) 38 (3<(3[1]3[2]3[4]3[5]3[6]3[10])) $ e: 3 bins 39 (5<u=3) $ f: 12 bins 40 sd4 1 29r 41 print 42 nps 100 43 imp:n 1 11r 0
```

Listing 10.24: example\_repeated\_structure\_tally\_2.mcnp.inp.txt

## Tally Line

<!-- image -->

Figure 10.44: Example 33 Tally Regions by F4 Line. (a-f) indicates the
tally regions for each tally line. The number of bins generated by MCNP6
is shown at the end of each tally line following the $ in-line comment
symbol.

## 10.2.6.1.1 Tally Line 1

This first line creates three tally output bins: cell 5, cell 6, and the
union of cells 5, 6, and 3, as indicated in Fig. 10.44a. Because cell 3
is filled entirely by cells 5 and 6, a tally over cell 5 plus cell 6 is
the same as a tally over cell 3. If a particle is tallied in cell 5 and
tallied in cell 3, it will be tallied twice in the bin (5 6 3).

## /warning\_sign Caution

A true union is performed when first level cells overlap (or fill)
another cell. This is not a tally that is normally desired. If an
average of cell 3 and region (5 6) outside cell 3 is desired, separate
bins must be defined and properly combined using correct volume
weighting.

## 10.2.6.1.2 Tally Line 2

These two input tally bins result in identical output tallies, as shown
in Fig. 10.44b. The use of lattice index brackets that include all
existing lattice elements makes the two tallies equivalent. The simpler
format will execute faster.

## 10.2.6.1.3 Tally Line 3

This line illustrates omission of geometry levels and a single output
bin versus multiple bins. All three input bins tally cell 5 within cells
7 through 11. The second bin specifies the entire path explicitly.
Because the only place cell 5 exists within cell 1 is in cells 7-11, the
7-11 specification can be omitted, as in the third input bin. In the
second input bin, the parentheses around cells 7-11 are omitted,
creating multiple output bins. Five tally bins are produced: (5&lt;7&lt;1),
(5&lt;8&lt;1), (5&lt;9&lt;1), (5&lt;10&lt;1), and (5&lt;11&lt;1). The sum of these five bins
should equal the tally in the first and last output bins on this line.
The tally regions are shown in Fig. 10.44c.

## 10.2.6.1.4 Tally Line 4

This line illustrates the union of multiple tally cells, (5 6), and
various ways of specifying lattice index data. The three input tally
bins create three output tally bins with identical values because the
three different lattice descriptions refer to the same lattice element,
the eighth entry on the FILL array. If the parentheses around (5 6) were
removed, two output bins would be created for each input bin, namely (5&lt;
3[0 , -1 , 0] ) and (6&lt; 3[0 , -1 , 0] ), etc. The tally regions are
shown in Fig. 10.44d.

## 10.2.6.1.5 Tally Line 5

This line illustrates tallies in overlapping regions in repeated
structures in a lattice and a tally in lattice elements filled with
themselves. Three tally output bins are produced. In the first input
bin, a particle is tallied only once when it is in cell 5 and in 4 [0 ,
0 , 0] or when it is in cell 5 and in 3 [0 , -1 , 0] . Fig. 10.44e shows
all the cell 5 instances included in this tally bin. This tally is
probably more useful than the overlapping regions in tally line 1. Input
bin 2 demonstrates a tally for a nested lattice. A tally is made when a
particle is in cell 5 and in cell 4, element [0 , 0 , 0] and in cell 3,
element [0 , -1 , 0] . Note that 3[0 , -1 , 0] is indeed filled with
cell 4 (u=2). If that were not true, a zero tally would result in this
bin. The final input tally bin demonstrated a tally in lattice elements
that are filled with their own universe number. This method is the only
way to tally in these elements separate from the rest of cell 3.

Figure 10.45: Light ion recoil.

<!-- image -->

## 10.2.6.1.6 Tally Line 6

This line illustrates the universe format. The single input bin includes
all possible chains involving cell 5. Because u=3 is not within
parentheses, the input is expanded into twelve output bins: (5&lt; 3[3] ,
etc.). The format 3[3] indicates the third lattice element of cell 3 as
entered on the cell 3 FILL array. Note that the third element is filled
by universe 3, consisting of cells 5 and 6. The tally regions are shown
in Fig. 10.44f.

## 10.2.7 Miscellaneous Tally Examples

## 10.2.7.1 Example 44: Light Ion Recoil (RECL)

MCNP6 can produce and track ions created by elastic recoil from neutrons
or protons. Neutrons and protons undergoing elastic scatter with light
nuclei (H, D, T, 3 He, and 4 He) can create ions (protons, deuterons,
tritons, 3 He, and α ) that are banked for subsequent transport.

Figure 10.45 shows the energy-angle production of alphas created from 15
MeV neutrons striking 4 He. Note that in the forward bin, cosine 0 . 8 &lt;
µ &lt; 1 , the α energy goes up to the theoretical maximum of 9.6 MeV. The
theoretical maxima in the other cosine bins (0.8, 0.6, 0.4, and 0.2) are
6.144, 3.456, 1.536, and 0.384.

The input file for this example is shown in Listing 10.25 and the plot
command input file is shown in Listing 10.26.

```
1 Test of light ion recoil 2 1 1 1e-5 -1 3 2 0 1 4 5 1 so 1.e-5 6 7 prdmp 2j 1 8 mode n a 9 imp:n,a 1 0 10 phys:n 6j 1 11 sdef erg=15 12 print -161 -162 13 tmp1 1e-20 0 14 fcl:n 1 0 15 m1 2004.00c 0.2 16 cut:a j 0 17 nps 1000000 18 f51:a 1 19 e51 0.1 100log 20 20 c51 -0.8 8i 1 t 21 fq51 e c
```

Listing 10.25: example\_light\_ion\_recoil\_1.mcnp.inp.txt

```
1 rmct mctal tal 51 & 2 xlims 0.1 15 ylims 1e-14 1e-10 loglog & 3 title 1 "Light Ion Recoil: 15 MeV Neutrons on 4He" & 4 title 2 "Alpha Energy vs Cosine" & 5 fix c 11 label 1 "cos total" cop fix c 6 label 2 "cos -1-.2" & 6 cop fix c 7 label 3 "cos .2-.4" cop fix c 8 label 4 "cos .4-.6" & 7 cop fix c 9 label 5 "cos .6-.8" cop fix c 10 label 6 "cos .8-1." 8 end
```

Listing 10.26: example\_light\_ion\_recoil\_1.mcnp.comin.txt

The MCNP commands to produce Fig. 10.45 are mcnp6 i= example \_ light \_
ion \_ recoil \_ 1.mcnp.inp.txt followed by mcnp6 z com= example \_ light \_
ion \_ recoil \_ 1.comin.inp.txt notek .

## 10.2.7.2 Inline Generation of Double Differential Cross Sections and Residual Nuclei

The double differential cross sections and distributions of residual
nuclei for a single nuclear interaction thus may be calculated directly
in MCNP6. Tallying of the residual nuclei is discussed in the FT8 RES
tally description. Tallying of the differential cross section can be
done with standard F1 surface tallies, as shown in the following
example. The input file shown in Listing 10.27 models a 1.2 GeV proton
source having a single collision with 208 Pb.

```
Test of p(1.2GeV)+Pb(208) 1 1 -11. -1 imp:h 1 2 0 1 imp:h 0 1 so .01
```

Listing 10.27: example\_double\_diff\_xs\_1.mcnp.inp.txt

1

2

3

4

5

6

```
7 prdmp 2j 1 8 mode h n 9 sdef par h erg=1200 vec 0 0 1 dir 1 10 m1 82208 1 11 phys:h 1300 j 0 12 phys:n 1300 13 fmult data=0 14 nps 10000 15 fc1 *** neutron angle spectra tally *** 16 f1:n 1 17 ft1 frv 0 0 1 18 fq1 e c 19 * c1 167.5 9i 17.5 0 T 20 e1 1 50log 1300 T 21 lca 2 1 1 23 1 1 0 -2 0
```

Listing 10.28: example\_double\_diff\_xs\_1.mcnp.comin.txt

```
1 rmctal mctal 2 file all loglog xlim 1 1300 ylim 1e-6 1 & 3 fix c 13 label 1 "all angles" & 4 cop fix c 1 label 2 "180 deg" & 5 cop fix c 6 label 3 "100 deg" & 6 cop fix c 12 label 4 "0 deg" 7 end
```

The differential production for neutron production is tallied in the F1
current tally with energy and time bins. This tally is simply the
neutrons that are created from the single proton collision with lead and
then escape.

In Fig. 10.46, the first line (solid black) is the energy spectrum over
all angles, the second (blue dashed) is the 180 ◦ output, the third (red
dotted) is the 100 ◦ output, and the fourth (green broken) is the 0 ◦
output. Use of the FM -3 option for Tally 1 in this example will convert
these production results into differential cross sections (units of
barns).

The MCNP commands to produce Fig. 10.46 are mcnp6 i= example \_ double \_
diff \_ xs \_ 1.mcnp.inp.txt followed by mcnp6 z com= example \_ double \_
diff \_ xs \_ 1.mcnp.comin.txt notek .

## 10.2.8 TALLYX Subroutine Examples

An explanation of the TALLYX subroutine arguments can be found in
§5.9.17. Only examples illustrating some uses of TALLYX will be found
here.

## 10.2.8.1 Example 46

In §10.2.4.1, the FS n card is used to get the flux through a window on
the face of a cube. Instead of using the FS 2 card, which established
five sub tallies, TALLYX could have been used to get only the desired
window tally. Two input cards are used:

```
FU2 1 RDUM -0.5 0.5 -0.5 0.5
```

1

2

Figure 10.46: Differential production at all angles (black), 180 ◦ (blue), 100 ◦ (red), 0 ◦ (green), for 1.3 GeV protons on 208 82 Pb.

<!-- image -->

The subroutine shown in Listing 10.29 performs the work of extracting
the desired window tally. The subroutine is implemented just like a
user-provided SOURCE subroutine by replacing the file TALLYX.F90 . Note
that ib=0 and tally \_ p \_ thread%ibu=1 upon entry into TALLYX .

```
1 subroutine tallyx(t,ib) 2 use mcnp _ params 3 use mcnp _ global 4 use pblcom, only: pbl 5 use mcnp _ debug 6 7 implicit none 8 9 real(dknd), intent(inout) :: t 10 integer, intent(inout) :: ib 11 12 if( (pbl%r%x < rdum(1)) .or. (pbl%r%x > rdum(2)) ) ib=-1 13 if( (pbl%r%z < rdum(3)) .or. (pbl%r%z > rdum(4)) ) ib=-1 14 return 15 end subroutine tallyx
```

Listing 10.29: example\_tallyx\_rdum.f90.txt

The subroutine was generalized a bit by using the RDUM input card,
although the card could have been avoided by directly encoding the
values of the dimensions of the window into TALLYX .

## 10.2.8.2 Example 47

Calculate the number of neutron tracks exiting cell 20 per source
neutron. The input cards are

```
1 F4:N 20 2 FU4 1 3 SD4 1
```

and the tallyx.f90 file is given in Listing 10.30.

```
1 subroutine tallyx(t,ib) 2 use mcnp _ params 3 use mcnp _ global 4 use pblcom, only: pbl 5 use mcnp _ debug 6 7 implicit none 8 9 real(dknd), intent(inout) :: t 10 integer, intent(inout) :: ib 11 12 t=1.0 _ dknd 13 if (pbl%r%dcs < pbl%r%dls) ib = -1 14 return 15 end subroutine tallyx
```

Listing 10.30: example\_tallyx\_exiting\_tracks.f90.txt

The quantity t=1.0 is scored every time a track exits cell 20. The
variables used in this subroutine, pbl%r%dcs (the distance to collision)
and pbl%r%dls (distance to the boundary), are available to TALLYX from
the module PBLCOM.

10

11

12

13

14

15

## 10.2.8.3 Example 48

Divide the point detector scores into separate tallies (that is, user
bins) depending on which of the 20 cells in a problem geometry caused
the contributions. The input cards are

```
1 F5:N 0 0 0 0 2 FU5 1 18I 20
```

and TALLYX subroutine is shown in Listing 10.31.

```
1 subroutine tallyx(t,ib) 2 use mcnp _ params 3 use mcnp _ global 4 use tskcom, only: tally _ p _ thread 5 use pblcom, only: pbl 6 use mcnp _ debug 7 8 implicit none 9 real(dknd), intent(inout) :: t integer, intent(inout) :: ib tally _ p _ thread%ibu=pbl%i%icl return end subroutine tallyx
```

Listing 10.31: example\_tallyx\_f5\_contributing\_cells.f90.txt

The FU 5 card establishes 20 separate user bins, one for each cell in
the problem. Note the use of the ' n I ' input format [§4.4.5.1], which
creates 18 linear interpolates between 1 and 20.

## 10.2.8.4 Example 49

Determine the quantity GLYPH&lt;1&gt; ϕ ( E ) f ( E )d E in cell 14 where f (
E ) = exp( αt ) . The input cards are

```
1 F4:N 14 2 FU4 alpha
```

where alpha is a numerical value and TALLYX is shown in Listing 10.32.

```
1 subroutine tallyx(t,ib) 2 use mcnp _ params 3 use mcnp _ global 4 use tskcom, only: tally _ p _ thread 5 use pblcom, only: pbl 6 use basic _ tally, only: tds, iptal 7 use mcnp _ debug 8 9 implicit none 10
```

Listing 10.32: example\_tallyx\_time\_response.f90.txt
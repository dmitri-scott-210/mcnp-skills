---
title: "Chapter 5.3 - Surface Cards"
chapter: "5.3"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.3_Surface_Cards.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

```
1 3 0 -1 2 -4 $ definition of cell 3 2 5 0 #3 $ equivalent to each of the next 2 lines
```

or

```
5 0 #(-1 2 -4)
```

1

or

```
1 5 0 (+1 : -2 : +4)
```

Cell 3 is defined as the region in space with negative sense with
respect to surface 1, positive sense with respect to surface 2, and
negative sense with respect to surface 4. Cell 5 is the region of space
not including cell 3. In the second and third lines of the example, it
is specified using the complement operator; in the fourth line, the same
region is specified using the union operator.

## Example 2

```
1 2 3 -3.7 -1 IMP:N=2 IMP:P=4 2 3 LIKE 2 BUT IMP:N=10 TRCL=1
```

This second example says that cell 3 is the same as cell 2 in every
respect except that cell 3 has a different location ( TRCL = 1 ) and a
different neutron importance. The material in cell 3, the density, and
the definition are the same as cell 2 and the photon importance is the
same.

## Example 3

```
1 10 16 -4.2 1 -2 3 IMP:N=4 IMP:P=8 EXT:N=-0.4X
```

This says that cell 10 is to be filled with material 16 at a density of
4.2 g/cm 3 . The cell consists of the intersections of the regions on
the positive side of surface 1, the negative side of surface 2, and the
positive side of surface 3. The neutron importance in cell 10 is 4 and
the photon importance is 8. Neutrons in cell 10 are subject to an
exponential transform in the -x direction with stretching parameter 0.4.

## 5.3 Surface Cards

## 5.3.1 Surfaces Cards, Defined by Equations

The available surface types, equations, mnemonics, and the order of the
card entries are given in Table 5.1. To specify a surface by this
method, find the surface in Table 5.1 and determine the coefficients for
the equation. The information is entered on the surface card according
to the following format:

| Form: j n A list   | Form: j n A list                                                                                                                                                                                      |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| j                  | Surface number assigned by the user. Restriction: 1 ≤ j ≤ 99 , 999 , 999 Restriction: If the surface is affected by a TR transformation, then j must be in the range 1 ≤ j ≤ 999 [§5.5.3 and §5.5.4]. |
| * j                | Reflecting surface number. A particle track that hits a reflecting surface is reflected specularly ( 1 )                                                                                              |
| + j                | White boundary surface number. A particle hitting a white boundary is reflected with a cosine distribution relative to the surface normal ( 1 )                                                       |
| n                  | Transformation number. If n is absent then no coordinate transformation is specified.                                                                                                                 |
| n                  | n > 0 the value specifies a transformation number n of a TR n card.                                                                                                                                   |
| n                  | n < 0 the value specifies that surface j is periodic with surface n ( 2 ).                                                                                                                            |
| A                  | Equation mnemonic from Table 5.1 that specifies the type of surface.                                                                                                                                  |
| list               | One to ten numerical entries, as required to define the selected surface.                                                                                                                             |

In addition, using the X , Y , Z , and P mnemonics a surface can be
defined based on points [§5.3.2 and §5.3.3]. Finally, macrobodies can be
used to conveniently define surfaces [§5.3.4].

## Details:

- 1 Detectors and DXTRAN (next-event estimators) usually should not be used in problems that have reflecting surfaces or white boundaries. Also, tallies in problems with reflecting surfaces will need to be normalized differently as discussed in §2.2.3.3 and §2.5.6.4.2.
- 2 If periodic boundaries are specified (i.e., n &lt; 0 ) such that surface j is periodic with surface n , the following restrictions apply:
- (a) Surfaces j and n must be planes.
- (b) No surface transformation is allowed for the periodic planes.
- (c) The periodic cell(s) can be infinite or bounded by planes on the top and bottom that can be reflecting or white, but cannot be periodic.
- (d) Periodic planes can bound only other periodic planes or top and bottom planes.
- (e) A single zero-importance cell must be on one side of each periodic plane.
- (f) All periodic planes must have a common rotational vector normal to the geometry top and bottom.
- (g) Next-event estimators such as detectors and DXTRAN should not be used.
- 3 The quadratic equation for a cone describes a cone of two sheets-one sheet is a cone of positive slope, and the other has a negative slope. MCNP6 provides the option to select either of the two sheets. The +1 or the -1 entry on the cone surface card causes the one sheet cone treatment to be used (and is only used for single-sheet cones). If the sign of the entry is positive, the specified sheet is the one that extends to infinity in the positive direction of the coordinate axis to which the cone axis is parallel. The converse is true for a negative entry. A cell whose description contains a two-sheeted cone may require an additional

Table 5.1: MCNP6 Surface Cards

| Type                                           | Mnemonic   | Description                            | Equation                                                                                           | Card Entries                        |
|------------------------------------------------|------------|----------------------------------------|----------------------------------------------------------------------------------------------------|-------------------------------------|
| Plane                                          | P PX       | General Normal to x axis               | Ax + By + Cz - D = 0 x - D = 0                                                                     | A,B,C,D D                           |
| Plane                                          | PY         | Normal to y axis                       | y - D = 0                                                                                          | D                                   |
| Plane                                          | PZ         | Normal to z axis                       | z - D = 0                                                                                          | D                                   |
| Sphere                                         | SO         | Centered at Origin                     | x 2 + y 2 + z 2 - R = 0                                                                            | R                                   |
| Sphere                                         | S          | General                                | ( x - x ) 2 +( y - y ) 2 +( z - z ) 2 - R 2 = 0                                                    | x,y,z,R                             |
| Sphere                                         | SX         | Centered on x axis                     | ( x - x ) 2 + y 2 + z 2 - R 2 = 0                                                                  | x,R                                 |
| Sphere                                         | SY         | Centered on y axis                     | x 2 +( y - y ) 2 + z 2 - R 2 = 0                                                                   | y,R                                 |
| Sphere                                         | SZ         | Centered on z axis                     | x 2 + y 2 +( z - z ) 2 - R 2 = 0                                                                   | z,R                                 |
| Cylinder                                       | C/X        | Parallel to x axis                     | ( y - y ) 2 +( z - z ) 2 - R 2 = 0                                                                 | y,z,R                               |
| Cylinder                                       | C/Y        | Parallel to y axis                     | ( x - x ) 2 +( z - z ) 2 - R 2 = 0                                                                 | x,z,R                               |
| Cylinder                                       | C/Z        | Parallel to z axis                     | ( x - x ) 2 +( y - y ) 2 - R 2 = 0                                                                 | x,y,R                               |
| Cylinder                                       | CX         | On x axis                              | y 2 + z 2 - R 2 = 0                                                                                | R                                   |
| Cylinder                                       | CY         | On y axis                              | x 2 + z 2 - R 2 = 0                                                                                | R                                   |
| Cylinder                                       | CZ         | On z axis                              | x 2 + y 2 - R 2 = 0                                                                                | R                                   |
| Cone ( 3 , 4 )                                 | K/X        | Parallel to x axis                     | √ ( y - y 2 ) + ( z - z 2 ) - t ( x - x ) = 0                                                      | x, y, z, t 2 , ± 1                  |
| Cone ( 3 , 4 )                                 | K/Y        | Parallel to y axis                     | √ x - x 2 + z - z 2 - t ( y - y ) = 0                                                              | x, y, z, t 2 , ± 1                  |
| Cone ( 3 , 4 )                                 | K/Z        | Parallel to z axis                     | ( ) ( ) √ ( x - x 2 ) + ( y - y 2 ) - t ( z - z ) = 0                                              | x, y, z, t 2 , ± 1                  |
| Cone ( 3 , 4 )                                 | KX         | On x axis                              | y 2 + z 2 - t ( x - x ) = 0                                                                        | x, t 2 , ± 1                        |
| Cone ( 3 , 4 )                                 | KY         | On y axis                              | √ √ x 2 + z 2 - t ( y - y ) = 0                                                                    | y, t 2 , ± 1                        |
| Cone ( 3 , 4 )                                 | KZ         | On z axis                              | x 2 + y 2 - t ( z - z ) = 0                                                                        | z, t 2 , ± 1                        |
| Ellipsoid Hyperboloid Paraboloid               | SQ         | Axes parallel to x , y , or z axis     | √ A ( x - x ) 2 + B ( y - y ) 2 + C ( z - z ) 2 +2 D ( x - x )+2 E ( y - y ) +2 F ( z - z )+ G = 0 | A , B , C , D , E , F G , x , y , z |
| Cylinder Cone Ellipsoid Hyperboloid Paraboloid | GQ         | Axes not parallel to x , y , or z axis | Ax 2 + By 2 + Cz 2 + Dxy + Eyz + Fzx + Gx + Hy + Jz + K = 0                                        | A , B , C , D , E , F G , H , J , K |
| Torus ( 5 )                                    | TX         | Axis parallel to x , y , or axis       | x - x ) 2 B + (√ ( y - y ) 2 +( z - z ) 2 - A ) 2 C 2 - 1 = 2                                      | x,y,z,A,B,C                         |
| Torus ( 5 )                                    | TY         | z                                      | y - y ) 2 B + (√ ( x - x ) 2 +( z - z ) 2 - A ) C 2 - 1 = 2                                        | x,y,z,A,B,C                         |
| Torus ( 5 )                                    | TZ         |                                        | z - z ) 2 B + (√ ( x - x ) 2 +( y - y ) 2 - A ) C 2 - 1 =                                          | x,y,z,A,B,C                         |

x

z

x

z

r

C

B

y

(a) Ring Torus

A

s

y

Figure 5.1: Elliptical Tori

<!-- image -->

surface specification to help distinguish between the two sheets. This
ambiguity surface helps to eliminate any ambiguities as to which region
of space is included in the cell.

- 4 The value t 2 entered to define the angle of the surface relative to the axis of the cone is t 2 = tan 2 ( θ ) = ( r/h ) 2 where θ is the angle in radians and r is the radius of the cone at distance h along the axis of the cone from its apex. The relationship among these parameters is shown in Fig. 5.2.
- 5 The TX , TY , and TZ mnemonics represent elliptical tori (fourth degree surfaces) rotationally symmetric about axes parallel to the x , y , and z axes, respectively. A TY torus is illustrated in Fig. 5.1a. Note that the input parameters x, y, z, A, B, C specify the ellipse

<!-- formula-not-decoded -->

rotated about the s axis in the ( r, s ) cylindrical coordinate system
(Fig. 5.1a) whose origin is at in the ( x, y, z ) system. In the case of
a TY torus, and

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

A torus is degenerate if | A | &lt; C where 0 &lt; A &lt; C produces the outer
surface (Fig. 5.1b), and -C &lt; A &lt; 0 produces the inner surface (Fig.
5.1c).

Coordinate transformations for tori are limited to those in which each
axis of the auxiliary coordinate system is parallel to an axis of the
main system.

## /warning\_sign Caution

MCNP6 may incorrectly compute the internal volume of tori that exhibit a
large ratio of major to minor axes. A warning message is printed when
the ratio of the major to minor axes exceeds 2000.

x

x

z

y

z

(c) Degenerate Torus,

A &lt;

0

&lt; C

r

-

A

s

y

1

1

1

2

1

2

3

## 5.3.1.1 Example 1

1 PY 3

Surface 1 describes a plane normal to the y axis at y = 3 with positive
sense for all points with y &gt; 3 .

## 5.3.1.2 Example 2

## 3 K/Y 0 0 2 0.25 1

Surface 3 is a cone whose vertex is at ( x, y, z ) = (0 , 0 , 2) and
whose axis is parallel to the y axis. The cone has height h = 100 and
radius r = 50 leading to t 2 = tan 2 ( θ ) = ( r/h ) 2 = 0 . 25 (where θ
is the angle between the surface and the cone's axis) and only the
positive (right hand) sheet of the cone is used. Points outside the cone
have a positive sense.

## 5.3.1.3 Example 3

| 11   | GQ   | 1 0.25   |   0.75 | 0 -0.866   |
|------|------|----------|--------|------------|
|      |      | 0 -12    |     -2 | 3.464 39   |

This is a cylinder of radius 1 cm whose axis is in a plane normal to the
x axis at x = 6 , displaced 2 cm from the x axis and rotated 30 degrees
about the x axis off the y axis toward the z axis. The sense is positive
for points outside the cylinder. Such a cylinder would be much easier to
specify by first defining it in an auxiliary coordinate system where it
is symmetric about a coordinate axis and then using the TR n card to
define the relationship between the basic and auxiliary coordinate
systems. The input would then be

```
11 7 CX 1
```

```
* TR7 6 1 -1.732 0 30 60
```

Figure 5.2: Cone Parameters

<!-- image -->

1

## 5.3.2 Axisymmetric Surfaces Defined by Points

Surface cards of the type X , Y , Z , and P can be used to describe
surfaces by coordinate points rather than by equation coefficients as in
the previous section. The surfaces described by these cards must be
symmetric about the x , y , or z axis, respectively, and, if the surface
consists of more than one sheet, the specified coordinate points must
all be on the same sheet.

Each of the coordinate pairs defines a geometric point on the surface.
On the Y card, for example, the entries may be j Y y1 r1 y2 r2 where ri
= √ xi 2 + zi and yi is the coordinate of point i . If one coordinate
pair is used, a plane ( PX , PY , or PZ ) is defined. If two coordinate
pairs are used, a linear surface ( PX , PY , PZ , CX , CY , CZ , KX , KY
, or KZ ) is defined. If three coordinate pairs are used, a quadratic
surface ( PX , PY , PZ , SO , SX , SY , SZ , CX , CY , CZ , KX , KY , KZ
, or SQ ) is defined. Note that planes and linear surfaces are
degenerate quadratic surfaces, which is why they are listed multiple
times.

When a cone is specified by two points, a cone of only one sheet is
generated.

The senses of these surfaces (except SQ ) are determined by the code to
be identical to the senses one would obtain by specifying the surface by
equations. For SQ , the sense is defined so that points sufficiently far
from the axis of symmetry have positive sense. Note that this is
different from the equation-defined SQ , where the user could choose the
sense freely through the sign of the coefficient G .

| Form: j n A list   | Form: j n A list                                                                                                                                                                                                                 |
|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| j                  | Surface number assigned by the user. Restriction: 1 ≤ j ≤ 99 , 999 , 999 Restriction: If the surface is affected by a TR transformation or in a repeated structure, then j must be in the range 1 ≤ j ≤ 999 [§5.5.3 and §5.5.4]. |
| n                  | Transformation number. If n is absent then no coordinate transformation is specified.                                                                                                                                            |
|                    | n > 0 the value specifies a transformation number n of a TR n card.                                                                                                                                                              |
| A                  | The letter X , Y , or Z .                                                                                                                                                                                                        |
| list               | One to three coordinate pairs.                                                                                                                                                                                                   |

## 5.3.2.1 Example 1

| 12   | 7 5   | 3 2   | 4 3   |
|------|-------|-------|-------|

This input describes a surface symmetric about the x axis, which passes
through the three ( x, r ) points (7 , 5) , (3 , 2) , and (4 , 3) . This
surface is a hyperboloid of two sheets, converted in MCNP6 to its
equivalent

1

| 12   | SQ   | -0.083333333 1 1 0 0 0 68.52083 -26.5 0 0   |
|------|------|---------------------------------------------|

1

1

1

1

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

## 5.3.2.2 Example 2

## 12 Y 1 2 1 3 3 4

These data describe two parallel planes at y = 1 and y = 3 and is a
fatal error because the requirement that all points be on the same sheet
is not met.

## 5.3.2.3 Example 3

## 12 Y 3 0 4 1 5 0

This input describes a 1-cm-radius sphere with center at ( x, y, z ) =
(0 , 4 , 0) .

## 5.3.2.4 Example 4

## 12 Z 1 0 2 1 3 4

This surface is rejected because the points are on two different sheets
of the hyperboloid

<!-- formula-not-decoded -->

However, the surface

## 12 Z 2 1 3 4 5 9.380832

which has the same surface equation as above is accepted because all
coordinates lie on a single surface: the right sheet of the hyperboloid.

## 5.3.2.5 Example 5

Listing 5.1: example\_axisym\_surf.mcnp.inp.txt

<!-- image -->

## 02/23/20 21:04:54 example 5

Figure 5.3: A geometry plot of Cell 1 of Example 5.

<!-- image -->

1

1

The final example in Listing 5.1 defines a cell bounded by a cone,
hyperboloid, and an ellipsoid. The three surfaces define the donut-like
cell that is symmetric about the y axis. A cross section of this cell is
seen in Fig. 5.3. To plot this view, use the interactive plotter command
input file in Listing 5.2.

Listing 5.2: example\_axisym\_surf.mcnp.comin.txt

label 1 1 cel or 0 2 0 ex 3.5 scale 1

One surface goes through the points ( -3 , 2) and (2 , 1) . The second
surface goes through (2 , 3) , (3 , 3) , and (4 , 2) . The last surface
is defined by the points (2 , 1) , (3 , 1) , and (4 , 2) . These
coordinate points are in the form ( y, r ) . Using these cards, MCNP6
indicates that surface 1 is a cone of one sheet, surface 2 is an
ellipsoid, and surface 3 is a hyperboloid of one sheet. The equation
coefficients for the standard surface equations are printed out for the
various surfaces when the PRINT input card or execution option is used.
For example, an SQ surface defining surface 3 is

```
3 SQ 1 -1.5 1 0 0 0 -0.625 0 2.5 0
```

## 5.3.3 General Plane Defined by Three Points

If there are four entries on a surface card with a P mnemonic, they are
assumed to be the general plane equation coefficients as in Table 5.1.
If there are more than four entries, they give the coordinates of three
points lying in the desired plane. The code uses the coordinate points
to determine the required surface coefficients to produce the plane

The sense of the plane is determined by requiring the origin to have
negative sense. If the plane passes through the origin ( D = 0 ), the
point (0 , 0 , ∞ ) has positive sense. If this fails ( D = C = 0 ), the
point (0 , ∞ , 0) has positive sense. If this fails ( D = C = B = 0 ),
the point ( ∞ , 0 , 0) has positive sense. If this fails, the three
points lie in a line and a fatal error is issued.

<!-- formula-not-decoded -->

## Form: j n P x1 y1 z1 x2 y2 z2 x3 y3 z3

j

n

P

xi yi

zi

Surface number assigned by the user.

Restriction: 1 ≤ j ≤ 99 , 999 , 999

Restriction: 1 ≤ j ≤ 999 if j is the surface number of a repeated
structure or if surface j defines a surface transformed with TR .

If n is absent, then no coordinate transformation is specified.

n

n

&gt;

&lt;

0

0

specifies transformation number specifies surface

j

n

of a

TR

is periodic with surface

Mnemonic that indicates this is a planar surface [Table 5.1].

Coordinates of three points that define the plane.

## 5.3.4 Surfaces Defined by Macrobodies

Using a combinatorial-geometry-like macrobody capability is an
alternative method of defining cells and surfaces. The combinatorial
geometry bodies available are similar to those in the Integrated Tiger
Series

n

n

card.

.

(ITS) [57] codes. The macrobodies can be mixed with the standard cells
and surfaces. The macrobody surface is decomposed internally by MCNP6
into surface equations and the facets are assigned individual numbers
according to a predetermined sequence. The assigned numbers are the
number selected by the user followed by a decimal point and 1 , 2 , . .
. . The facets can be used for tallying, tally segmentation, other cell
definitions, SDEF sources, etc. They cannot be used on the surface
source read and write cards ( SSR / SSW ), the surface flagging card (
SF ), non-HDF5 PTRAC files, or MCTAL files.

The space inside a macrobody has a negative sense with respect to the
macrobody surface and all its facets. The space outside a body has a
positive sense. The sense of a facet is the sense assigned to it by the
macrobody 'master' cell and the facet retains that assigned sense if it
appears in other cell descriptions and must be properly annotated. More
information regarding facets is provided in §5.3.4.11.

## 5.3.4.1 BOX: Arbitrarily Oriented Orthogonal Box

| BOX vx vy vz a1x a1y a1z a2x a2y a2z a3x a3y a3z   | BOX vx vy vz a1x a1y a1z a2x a2y a2z a3x a3y a3z             |
|----------------------------------------------------|--------------------------------------------------------------|
| vx vy vz                                           | The ( x, y, z ) coordinates of a corner of the box.          |
| a1x a1y a1z                                        | Vector of first side from the specified corner coordinates.  |
| a2x a2y a2z                                        | Vector of second side from the specified corner coordinates. |
| a3x a3y a3z                                        | Vector of third side from the specified corner coordinates.  |

## Details:

- 1 All corner angles are 90 ◦ .
- 2 If ( a3x , a3y , a3z ) is not specified, the box will be infinite along the vector normal to the plane specified by ( a1x , a1y , a1z ) and ( a2x , a2y , a2z ) .

An example 1 × 2 × 3 -cm box, centered about (0 , 0 , 0) with sides
normal to the x , y , and z axes, is given in Listing 5.3.

```
1 1010 box -0.5 -1 -1.5 1 0 0 0 2 0 0 0 3
```

Listing 5.3: example\_macrobodies.mcnp.inp.txt

## 5.3.4.2 RPP: Rectangular Parallelepiped

| RPP xmin xmax ymin ymax zmin zmax   | RPP xmin xmax ymin ymax zmin zmax          |
|-------------------------------------|--------------------------------------------|
| xmin xmax                           | Termini of box sides normal to the x axis. |
| ymin ymax                           | Termini of box sides normal to the y axis. |
| zmin zmax                           | Termini of box sides normal to the z axis. |

1

1

1

## Details:

- 1 RPP surfaces will only be normal to the x , y , and z axes.
- 2 The x , y , and z values are relative to the origin.
- 3 If xmin = xmax , ymin = ymax , or zmin = zmax , the rectangular parallelepiped will be infinite in that dimension. Only one dimension may be infinite at a time.

An example 1 × 2 × 3 -cm rectangular parallelepiped, centered about (1 .
5 , 0 , 0) with sides normal to the x , y , and z axes, is given in
Listing 5.4. This RPP specification is comparable (other than absolute
position) to the BOX example in Listing 5.3.

```
1020 rpp 1 2 -1 1 -1.5 1.5
```

Listing 5.4: example\_macrobodies.mcnp.inp.txt

## 5.3.4.3 SPH: Sphere

## SPH vx vy vz r

```
vx vy vz The ( x, y, z ) coordinates of the center of the sphere. r Radius of sphere.
```

An example 20-cm radius sphere, centered about (0 , 0 , 0) , is given in
Listing 5.5.

```
1030 sph 0 0 0 20
```

Listing 5.5: example\_macrobodies.mcnp.inp.txt

## 5.3.4.4 RCC: Right Circular Cylinder

| RCC vx vy vz h1 h2 h3 r   | RCC vx vy vz h1 h2 h3 r                                                                                  |
|---------------------------|----------------------------------------------------------------------------------------------------------|
| vx vy vz                  | The ( x, y, z ) coordinates at the center of the base for the right circular cylinder.                   |
| h1 h2 h3                  | Right circular cylinder axis vector, which provides both the orientation and the height of the cylinder. |
| r                         | Radius of cylinder.                                                                                      |

An example 0.5-cm radius right-circular cylinder aligned parallel to the
z axis, centered about (3 , 0 , 0) and with a length of 3 cm, is given
in Listing 5.6.

```
1040 rcc 3.0 0 -1.5 0 0 3 0.50
```

Listing 5.6: example\_macrobodies.mcnp.inp.txt

## 5.3.4.5 RHP or HEX: Right Hexagonal Prism

1

2

3

4

| RHP vx vy vz h1 h2 h3 r1 r2 r3 s1 s2 s3 t1 t2 t3 or HEX vx vy vz h1 h2 h3 r1 r2 r3 s1 s2 s3 t1 t2 t3   | RHP vx vy vz h1 h2 h3 r1 r2 r3 s1 s2 s3 t1 t2 t3 or HEX vx vy vz h1 h2 h3 r1 r2 r3 s1 s2 s3 t1 t2 t3                           |
|--------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| vx vy vz                                                                                               | The ( x, y, z ) coordinates at the center of the bottom of the hexagonal prism.                                                |
| h1 h2 h3                                                                                               | Vector from the bottom to the top of the hexagonal prism. For a z hex with height h , ( h1 , h2 , h3 ) = (0 , 0 ,h ) .         |
| r1 r2 r3                                                                                               | Vector from the axis to the center of the first facet. For a pitch 2 p facet normal to y axis, ( r1 , r2 , r3 ) = (0 , p, 0) . |
| s1 s2 s3                                                                                               | Vector to center of the second facet. This is optional for a regular hexagon but required for an irregular hexagon.            |
| t1 t2 t3                                                                                               | Vector to center of the third facet. This is optional for a regular hexagon but required for an irregular hexagon.             |

## Details:

1 The right-hexagonal prism in the MCNP code differs from the ITS-ACCEPT
[57] format.

2 One can make an infinite right-hexagonal prism by setting the length
of the vector ( h1 , h2 , h3 ) greater than or equal to 10 6 cm.
Surfaces 7 and 8 in Table 5.2 will then not be created.

An example regular right-hexagonal prism using the RHP keyword aligned
parallel to the z axis, centered about (4 . 5 , 0 , 0) with a length of
3 cm and first-facet offset of 0.5-cm normal to the y axis, is given in
Listing 5.7. An example regular right hexagonal prism using the HEX
keyword aligned parallel to the z axis, centered about (6 , 0 , 0) with
a length of 3 cm and first-facet offset of 0.5-cm normal to the x axis,
is also given. Two examples of irregular hexagons are also given.

Listing 5.7: example\_macrobodies.mcnp.inp.txt

| 1050 rhp   | 4.5 0 -1.5 0   | 0 3   | 0 0.5 0                                  |
|------------|----------------|-------|------------------------------------------|
| 1051 hex   | 6.0 0 -1.5     | 0 0 3 | 0.5 0 0                                  |
| 1052 hex   | 6.0 2 -1.5     | 0 0 3 | 0.5 0 0 0.4 0.69282 0.0 -0.4 0.69282 0.0 |
| 1053 hex   | 6.0 4 -1.5     | 0 0 3 | 0.5 0 0 0.4 0.69282 0.0 -0.5 0.85 0.0    |

## 5.3.4.6 REC: Right Elliptical Cylinder

| REC vx vy vz h1 h2 h3 v1x v1y v1z v2x v2y v2z   | REC vx vy vz h1 h2 h3 v1x v1y v1z v2x v2y v2z                                                        |
|-------------------------------------------------|------------------------------------------------------------------------------------------------------|
| vx vy vz                                        | The ( x, y, z ) coordinates of the cylinder bottom.                                                  |
| h1 h2 h3                                        | Cylinder axis height vector.                                                                         |
| v1x v1y v1z                                     | Ellipse minor axis vector, which is normal to ( h1 , h2 , h3 ) .                                     |
| v2x v2y v2z                                     | Ellipse major axis vector, which is orthogonal to vectors ( h1 , h2 , h3 ) and ( v1x , v1y , v1z ) . |

1

1

2

## Details:

- 1 If there are 10 entries instead of 12, the 10th entry is the minor axis radius, where the direction is determined from the cross product of ( h1 , h2 , h3 ) and ( v1x , v1y , v1z ) .

An example right-elliptical cylinder aligned parallel to the z axis,
centered about (7 . 5 , 0 , 0) with an axial length of 3 cm and 0.25-
and 0.5-cm minor and major axes along the x and y axes, respectively, is
given in Listing 5.8.

Listing 5.8: example\_macrobodies.mcnp.inp.txt

| 1060 rec   | 7.5 0 -1.5   | 0 0 3   | 0.25 0 0 0 0.5   |
|------------|--------------|---------|------------------|

## 5.3.4.7 TRC: Truncated Right-angle Cone

| TRC vx vy vz h1 h2 h3 r1 r2   | TRC vx vy vz h1 h2 h3 r1 r2                     |
|-------------------------------|-------------------------------------------------|
| vx vy vz                      | The ( x, y, z ) coordinates of the cone bottom. |
| h1 h2 h3                      | Cone axis height vector.                        |
| r1                            | Radius of lower cone base.                      |
| r2                            | Radius of upper cone base.                      |

An example truncated cone aligned parallel to the z axis, with its base
centered at (9 , -1 , 0) with a length of 2 cm, lower-base radius of
0.15 cm, and upper-base radius of 0.5 cm, is given in Listing 5.9. An
example truncated cone aligned parallel to the z axis, with its base
centered at (10 . 5 , -1 , 0) with a length of 2 cm, lower-base radius
of 0.5 cm, and upper-base radius of 0.15 cm, is also given.

Listing 5.9: example\_macrobodies.mcnp.inp.txt

| 1070 trc   | 9.0 -1 0   | 0 2 0   |   0.15 |   0.5 |
|------------|------------|---------|--------|-------|
| 1071 trc   | 10.5 -1 0  | 0 2 0   |    0.5 |  0.15 |

## 5.3.4.8 ELL: Ellipsoid

| v1x v1y v1z   | Coordinates determined by sign of r : r > 0 the coordinates of the first focus. r < 0 the coordinates of the center of the ellipsoid.                                                                                            |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| v2x v2y v2z   | Coordinates determined by sign of r : r > 0 the coordinates of the second focus. r < 0 major axis vector (vector from the center of the ellipsoid through a focus to the vertex, where the length is equal to the major radius). |

## Details:

- 1 The major and minor radii are half the lengths of the major and minor axes, respectively.
- 2 The ellipsoid macrobody is a surface of revolution about the major axis, but the major radius may be smaller than the minor radius.

An example ellipsoid aligned parallel to the y axis, centered about (12
, 0 , 0) with a major-axis distance of 2 cm and 0.5-cm minor radius
length, is given in Listing 5.10. An example ellipsoid aligned parallel
to the y axis, centered about (13 . 5 , 0 , 0) with a distance of 1 cm
between foci and 0.75-cm major radius length, is also given.

Listing 5.10: example\_macrobodies.mcnp.inp.txt

| 1080 ell   | 12.0 0 0 0 1 0 -0.5   |      |        |      |      |
|------------|-----------------------|------|--------|------|------|
| 1081 ell   | 0.5 0                 | 13.5 | -0.5 0 | 13.5 | 0.75 |

## 5.3.4.9 WED: Wedge

## WED vx vy vz v1x v1y v1z v2x v2y v2z v3x v3y v3z

```
vx vy vz The ( x, y, z ) coordinates of wedge vertex. v1x v1y v1z Vector of first side of triangular base. v2x v2y v2z Vector of second side of triangular base. v3x v3y v3z Height vector.
```

## Details:

- 1 A right-angle wedge has a right triangle for a base defined by ( v1x , v1y , v1z ) and ( v2x , v2y , v2z ) and a height ( v3x , v3y , v3z ) .
- 2 The vectors ( v1x , v1y , v1z ) , ( v2x , v2y , v2z ) , and ( v3x , v3y , v3z ) are orthogonal to each other.

An example right-angle wedge aligned parallel to the z axis, about (15 ,
0 , 0) with an axial length of 3 cm, a first-side length of 2 cm and a
second-side length of 0.5-cm, is given in Listing 5.11.

```
1 1090 wed 14.75 -1 -1.5 0 2 0 0.5 0 0 0 0 3
```

Listing 5.11: example\_macrobodies.mcnp.inp.txt

LA-UR-24-24602, Rev. 1

r

r

```
> 0 major radius length. < 0 minor radius length.
```

1

2

3

## 5.3.4.10 ARB: Arbitrary Polyhedron

There must be eight triplets of entries input for the ARB to describe
the ( x, y, z ) coordinates of the corners, although some may not be
used (just use triplets of zeros). These are followed by six more
entries, n i , which follow a prescribed convention: each entry is a
four-digit integer that defines a side of the ARB in terms of the
corners for the side.

For example, the entry 1278 would define this plane surface to be
bounded by the first, second, seventh, and eighth triplets (or
equivalently, corners). Because three points are sufficient to determine
the plane, only the first, second, and seventh corners would be used in
this example to determine the plane. The distance from the plane to the
fourth corner (corner 8 in the example) is determined by MCNP6. If the
absolute value of this distance is greater than 10 -6 cm, an error
message is given and the distance is printed in the MCNP output file
along with the ( x, y, z ) that would lie on the plane. If the fourth
digit is zero, the fourth point is ignored. For a four-sided ARB , four
non-zero four-digit integers (last digit is zero for four-sided since
there are only three corners for each side) are required to define the
sides. For a five-sided ARB , five non-zero four-digit integers are
required, and six non-zero four-digit integers are required for a six-
sided ARB . Since there must be 30 entries altogether for an ARB (or
MCNP6 gives an error message), the last two integers are zero for the
four-sided ARB and the last integer is zero for a five-sided ARB .

| ARB ax ay az ax ay az   | . . . n1 n2 n3 n4 n5 n6 The ( x, y, z ) coordinates of first corner of the polyhedron.                                                                                                              |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| bx by bz                | The ( x, y, z ) coordinates of second corner of the polyhedron.                                                                                                                                     |
| cx cy cz                | The ( x, y, z ) coordinates of third corner of the polyhedron.                                                                                                                                      |
| dx dy dz                | The ( x, y, z ) coordinates of fourth corner of the polyhedron.                                                                                                                                     |
| ex ey ez                | The ( x, y, z ) coordinates of fifth corner of the polyhedron.                                                                                                                                      |
| fx fy fz                | The ( x, y, z ) coordinates of sixth corner of the polyhedron.                                                                                                                                      |
| gx gy gz                | The ( x, y, z ) coordinates of seventh corner of the polyhedron.                                                                                                                                    |
| hx hy hz                | The ( x, y, z ) coordinates of eighth corner of the polyhedron.                                                                                                                                     |
| ni                      | Four-digit numbers describing a side of the polyhedron in terms of its corresponding corners. For example, n1 = 1278 is a plane/side bounded by corners 1, 2, 7, and 8 (points a , b , g , and h ). |

## Details:

- 1 There must be eight ( x, y, z ) triplets to describe the eight corners of the polyhedron.

An example 1 × 2 × 3 -cm rectangular parallelepiped, centered about (16
, 0 , 0) with sides normal to the x , y , and z axes, is given in
Listing 5.12. This ARB specification is equivalent to the BOX and RPP
examples in Listings 5.3 and 5.4, respectively.

Listing 5.12: example\_macrobodies.mcnp.inp.txt

| 1100 arb   | 15.5 -1 -1 16.5 -1   | -1   | 16.5 1 -1 15.5 1 -1   |
|------------|----------------------|------|-----------------------|

Table 5.2: Macrobody Facet Descriptions

| Macrobody Type   | Facet Number   | Facet Description                                                                                                         |
|------------------|----------------|---------------------------------------------------------------------------------------------------------------------------|
| BOX              | 1              | Plane normal to end of ( a1x , a1y                                                                                        |
| BOX              | 2              | , a1z ) Plane normal to beginning of ( a1x , a1y , a1z )                                                                  |
| BOX              | 3              | Plane normal to end of ( a2x , a2y , a2z )                                                                                |
| BOX              | 4              | Plane normal to beginning of ( a2x , a2y , a2z )                                                                          |
| BOX              | 5              | Plane normal to end of ( a3x , a3y , a3z )                                                                                |
| BOX              | 6              | Plane normal to beginning of ( a3x , a3y , a3z )                                                                          |
| RPP              | 1              | Plane xmax                                                                                                                |
| RPP              | 2              | Plane xmin                                                                                                                |
| RPP              | 3              | Plane ymax                                                                                                                |
| RPP              | 4              | Plane ymin                                                                                                                |
| RPP              | 5              | Plane zmax                                                                                                                |
| RPP              | 6              | Plane zmin                                                                                                                |
| SPH              |                | Treated as a regular surface so no facet                                                                                  |
| RCC              | 1              | Cylindrical surface of radius r                                                                                           |
| RCC              | 2              | Plane normal to end of ( h1 , h2 , h3 )                                                                                   |
| RCC              | 3              | Plane normal to beginning of ( h1 , h2 , h3 )                                                                             |
| RHP or HEX       | 1              | Plane normal to end of ( r1 , r2 , r3 )                                                                                   |
| RHP or HEX       | 2              | Plane opposite facet 1                                                                                                    |
| RHP or HEX       | 3              | Plane normal to end of ( s1 , s2 , s3 )                                                                                   |
| RHP or HEX       | 4              | Plane opposite facet 3                                                                                                    |
| RHP or HEX       | 5              | Plane normal to end of ( t1 , t2 , t3 )                                                                                   |
| RHP or HEX       | 6              | Plane opposite facet 5                                                                                                    |
| RHP or HEX       | 7              | Plane normal to end of ( h1 , h2 , h3 )                                                                                   |
| RHP or HEX       | 8              | ( h1 , h2 , h3 )                                                                                                          |
| RHP or HEX       |                | Plane normal to beginning of                                                                                              |
| REC              | 1              | Elliptical cylinder                                                                                                       |
| REC              | 2              | Plane normal to end of ( h1 , h2 , h3 )                                                                                   |
| REC              | 3              | Plane normal to beginning of ( h1 , h2 , h3 )                                                                             |
| TRC              | 1              | Conical surface                                                                                                           |
| TRC              | 2              | Plane normal to end of ( h1 , h2 , h3 )                                                                                   |
| TRC              | 3              | Plane normal to beginning of ( h1 , h2 , h3 )                                                                             |
| ELL              |                | Treated as a regular surface so no facet                                                                                  |
| WED              | 1              | Slant plane including top and bottom hypotenuses                                                                          |
| WED              | 2              | Plane including vectors ( v2x , v2y , v2z ) and ( v3x , v3y , v3z )                                                       |
| WED              | 3              | Plane including vectors ( v1x , v1y , v1z ) and ( v3x , v3y , v3z )                                                       |
| WED              | 4              | Plane including vectors ( v1x , v1y , v1z ) and ( v2x , v2y , v2z ) at end of ( v3x , v3y , v3z ) (top triangle)          |
| WED              | 5              | Plane including vectors ( v1x , v1y , v1z ) and ( v2x , v2y , v2z ) at beginning of ( v3x , v3y , v3z ) (bottom triangle) |
| ARB              | 1              | Plane defined by corners n1                                                                                               |
| ARB              | 2              | Plane defined by corners n2                                                                                               |
| ARB              | 3              | Plane defined by corners n3                                                                                               |
| ARB              | 4              | Plane defined by corners n4                                                                                               |
| ARB              | 5              | Plane defined by corners n5                                                                                               |
| ARB              | 6              | Plane defined by corners n6                                                                                               |

## 5.3.4.11 Macrobody Facets

The facets of the macrobodies are numbered sequentially and can be used
on other MCNP6 cards. BOX and RPP can be infinite in a dimension, in
which case those two facets are skipped and the numbers of the remaining
facets are decreased by two. RHP can be infinite in the axial dimension
in which case facets 7 and 8 do not exist. Facet numbering can be
displayed graphically with MBODY = OFF in the geometry plotter. The
order of the facet numbering presented by macrobody type, is provided in
Table 5.2.

## 5.3.4.11.1 Example 1

The following input file describes five cells and illustrates a
combination of the various body and cell/surface descriptions. In Fig.
5.4, surface numbers are in given within the planes they define and cell
numbers are given within circles. Note that the cell and surface numbers
do not have to start with 1 or be consecutive.
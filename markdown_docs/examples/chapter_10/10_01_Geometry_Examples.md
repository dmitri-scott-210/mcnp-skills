---
title: "Chapter 10.1 - Geometry Examples"
chapter: "10.1"
source_pdf: "mcnp631_theory_user-manual/mcnp-primers-examples/10.1_Geometry_Examples.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Chapter 10

## Examples

Instructive examples of several topics are included in this chapter.
Some of the examples are simplistic while others illustrate more complex
features of the MCNP6 code. They should be studied in conjunction with
the theory, instructions, and previous examples provided in Chapters 3,
4, and 5 of this manual.

Following the simple geometry specification examples are related
geometry examples that exercise coordinate transformations, repeated
structure and lattice geometries, and embedded meshes. After the
geometry-related examples are those related to tally options, including
the FM , FMESH , FS , and FT cards as well as the TALLYX subroutine for
user-defined tallies using the FU card. Next are source specification
examples for the generalized source, beam sources, and a burnup case
followed by example SOURCE and SRCDX subroutines for point detectors
and/or DXTRAN spheres. Finally, a materials example of table and model-
data mix-and-match and a physics model example complete the section.

## 10.1 Geometry Examples

The geometry discussions in Chapters 3 and 4 must be understood before
studying the following examples. The concept of combining regions of
space bounded by surfaces to make a cell must be fully appreciated; the
following examples should help solidify this concept. The use of
macrobodies will simplify many geometry definition situations.

## 10.1.1 Geometry Specification

Several examples of the union and complement operators follow. These
should help you better understand how cells are defined. In the
illustrations, cell numbers will be circled; surface numbers will not be
circled but will appear next to the surface they represent. For
simplicity, all cells are void of material.

The next several examples become progressively more difficult and
usually take advantage of what you learned in the preceding ones.
Remember that unless altered by parentheses, the hierarchy of operations
is that intersections are performed first and then unions.

## 10.1.1.1 Example 1

Figure 10.1, surfaces 2 and 4 are cylinders and the others are planes
with their positive sides to the right. The figure includes a
perspective view to make it clearer what is being defined. The surfaces
used in this example are:

<!-- image -->

Figure 10.1: Example 1 sample geometry-two Stacked Cylinders: The XZ
cross section (at left) shows the three cells and defining surface
indices.

```
1 1 PX 0 $ plane perpendicular to the X axis at x=0 2 2 CX 2 $ cylinder on the X axis of radius 2 3 3 PX 2 $ plane perpendicular to the X axis at x=2 4 4 CX 3 $ cylinder on the X axis of radius 3 5 5 PX 6 $ plane perpendicular to the X axis at x=6
```

Cells 1 and 2 are easy to specify:

```
1 1 0 -2 1 -3 $ inside cylinder 2, right of plane 1, left of plane 3 2 2 0 -4 3 -5 $ inside cylinder 4, right of plane 3, left of plane 5
```

Cell 3 is more complex: There are multiple ways it can be defined. Here
are some definitions of cell 3, each of which is described in more
detail:

```
1 3 0 (2 3): 1:4:5 $ parentheses used for clarity; not required 2 3 0 4: 1:5:(2 3) $ parentheses not required 3 3 0 ( 1:2) (-3:4):5 $ parentheses are required for correctness 4 3 0 #1 #2 $ everything that is "not" cell 1 or 2
```

It may be helpful to refer to Fig. 2.3 and its explanation. Remember
that a union adds regions and an intersection gives you only the areas
that overlap or are common to both regions. In addition, intersections
take precedence over unions. Regions can be added together more than
once-or duplicated-with the union operator.

Let us arbitrarily start with the definition of cell 3 at cylindrical
surface 2. The expression 2 -3 defines the following region: everything
in the world outside surface 2 intersected with everything to the left
of plane surface 3. This region is hatched in Fig. 10.2. Let us examine
in detail how Fig. 10.2 was derived. First look at each region
separately. The area with a positive sense with respect to surface 2 is
shown in Fig. 10.3. It includes everything outside surface 2 extending
to infinity in all directions. The area with negative sense with respect
to surface 2 is undefined so far. The area with negative sense with
respect to surface 3 is shown in Fig. 10.4. It includes everything to
the left of surface 3 extending to infinity, or half the universe.
Recall

<!-- image -->

Figure 10.2: Outside (i.e., positive sense) of cylindrical surface 2
intersected with region to left (i.e., negative sense) of plane surface
3.

Figure 10.3: Region with positive sense with respect to cylindrical surface 2

<!-- image -->

Figure 10.4: Region with negative sense with respect to plane surface 3.

<!-- image -->

Figure 10.5: Figure 4-3 and Figure 4-4 overlaid creating a cross-hatched region that is identical to the hatched region in Figure 4-2.

<!-- image -->

Figure 10.6: Region shown in Figure 4-2 superimposed with region negative with respect to (i.e., left of) plane surface 1.

<!-- image -->

that an intersection of two regions gives only the area common to both
regions or the areas that overlap. Superimposing Fig. 10.3 and Fig. 10.4
results in Fig. 10.5. The cross-hatched regions show the space common to
both regions. This is the same area hatched in Fig. 10.2.

Let us now deal with surface 1. To the quantity 2 -3 we will add
everything with a negative sense with respect to plane surface 1 as
indicated by the expression 2 -3:-1, or (2 -3):-1 if you prefer. First,
recall that in the hierarchy of operations, intersections are performed
first and then unions. Consequently, the parentheses are unnecessary in
the previous expression. Second, recall that a union of two regions
results in a space containing everything in the first region plus
everything in the second region. This union also includes everything
common to both regions. Superimposing the region shown in Fig. 10.2 and
the region to the left of surface 1 results in Fig. 10.6. Our geometry
now includes everything hatched plus everything crosshatched and has
added part of the tunnel that is interior to cylindrical surface 2.

By the same method we will deal with cylindrical surface 4. To the
quantity 2 -3:-1 we will add everything with a positive sense with
respect to surface 4, written as 2 -3:-1:4. Figure 10.7 shows our new
geometry. It includes everything in Fig. 10.6 plus everything outside
surface 4.

Our final step is to block off the large tunnel extending to positive
infinity (i.e., to the right) by adding the region with a positive sense
with respect to plane surface 5 to the region shown in Fig. 10.7. The
final expression that defines cell 3 of Fig. 10.1 is 2 -3:-1:4:5.

There is more than one way to define cell 3. Starting with plane surface
1, we can add the region to the left of 1 to the region outside
cylindrical surface 2 or -1:2. This newly defined region is illustrated
in Fig. 10.8. We wish to intersect this space with the space having a
negative sense with respect to plane surface 3. Superimposing Fig. 10.8
and the region to the left of surface 3 results in Fig. 10.9. The cross-
hatched area

<!-- image -->

Figure 10.7: Region outside of surface 4 added to the region shown in
Figure 4-6.

Figure 10.8: Union of regions to the left of surface 1 and outside of surface 2.

<!-- image -->

Figure 10.9: Region of Figure 4-8 superimposed with the region to the left of surface 3.

<!-- image -->

Figure 10.10: A starting point for defining cell 3.

<!-- image -->

Figure 10.11: Union of the space block defined using outer boundaries of model and the left corner regions.

<!-- image -->

indicates the area common to both regions and is the result of the
intersection. Note that the cross-hatched area of Fig. 10.9 is identical
to the entire hatched plus crosshatched area of Fig. 10.6. Therefore, we
have defined the same geometry in both figures but have used two
different approaches to the problem. To ensure that the intersection of
-3 is with the quantity -1:2 as we have illustrated, we must use
parentheses giving the expression (-1:2) -3. Remember the order in which
the operations are performed. Intersections are done before unions
unless parentheses alter the order. The final expression is (-1:2)
-3:4:5.

Another tactic to define cell 3 uses a somewhat different approach.
Rather than defining a small region of the geometry as a starting point
and adding other regions until we get the final product, we shall start
by defining a block of space and adding to or subtracting from that
block as necessary. We arbitrarily choose our initial block to be
represented by 4: 1:5, illustrated in Fig. 10.10. Notice that the
boundaries of this block are the outermost surfaces of our model:
cylindrical surface 4 and planar surfaces 1 and 5.

To this block we need to add the space in the upper and lower left
corners that belong to cell 3. The expression 2 -3 isolates the space we
need to add. Adding 2 -3 to our original block, we have 4:-1:5:(2 -3).
The parentheses are not required for correctness in this case but help
to illustrate the path our reasoning has followed.

Figure 10.11 depicts the union of 2 -3 with the block of space we
originally chose.

Now let us arbitrarily choose a different initial block, 4:5:-3, all the
world except cell 2. From this region we need to subtract cell 1. If we
intersect the region (2:-1) with (4:5:-3), as shown in Fig. 10.12, we
will have introduced an undefined tunnel to the right of surface 5. To
correct this error, define an area (2:-1:3) or (2:-1:5) and intersect
this region with the initial block.

Yet another approach is to intersect the two regions -1:2 and -3:4, then
add that to the region to the right of surface 5 by (-1:2) (-3:4):5. In
the above paragraph the expression (4:5:-3) (2:-1:5) can have the common
quantity 5 factored out, also resulting in (-1:2) (-3:4):5.

Figure 10.12: Region (2:-1) intersected with region (4:5:-3), creating an undefined region.

<!-- image -->

Figure 10.13: Simple two-cell model.

<!-- image -->

Finally, another approach is to forget about the reality of the geometry
and to define cell 3 take the inverse (or complement) of all the cells
bounding cell 3-cells 1 and 2. This says that cell 3 is the entire world
excluding that which has already been defined to be in cells 1 and 2.
The advantage of this method is that cells 1 and 2 are easy to specify
and you do not get bogged down in details for cell 3. Cell 3 thus
becomes (-1:2:3) (-3:4:5). Note that the specifications for cells 1 and
2 are reversed. Intersections become unions. Positive senses become
negative. Then each piece is intersected with the other. There is a
complement operator in MCNP6 that is a shorthand notation for the above
expression; it is the symbol #, which can be thought of as meaning 'not
in.' Therefore, cell 3, when specified as #1 #2, is translated as
everything in the world that is not in cell 1 and not in cell 2.

## 10.1.1.2 Example 2

In this example (Fig. 10.13), cell 1 includes everything interior to
both surfaces 1 and 2. It is simple enough that the answer is provided
without explanation.

<!-- image -->

## 10.1.1.3 Example 3

In this geometry (Fig. 10.14) of four cells defined by three spheres,
cell 3 is disconnected, consisting of two disjoint volumes. Cell 3 is
the region inside surface 3 but outside surfaces 1 and 2 (-3 1 2) plus
the region enclosed between surfaces 1 and 2 (-2 -1):

```
1 1 0 -1 2 2 2 0 -2 1 3 3 0 (-3 1 2):(-2 -1) $ parentheses not required 4 4 0 3
```

## 10.1.1.4 Example 4

In this example (Fig. 10.15), all vertical lines are planes with their
positive sides to the right and all horizontal lines are cylinders. The
surface list (with notional dimensions) is:

```
1 1 PX -3
```

Figure 10.14: Illustration of disconnected cell 3.

<!-- image -->

Figure 10.15: Horizontal cylinders internal to a sphere.

<!-- image -->

2

3

4

5

6

7

8

|   2 | CX   |    2 |
|-----|------|------|
|   3 | PX   | -1   |
|   4 | CX   |  5   |
|   5 | PX   |  1   |
|   6 | CX   |  3.5 |
|   7 | PX   |  3   |
|   8 | SO   |  8   |

Cells 1, 2, and 3 are simple right-circular cylinders. Cell 4 is also
simple to define with the complement operator. Cell 5 is also simple,
everything in the world with a positive sense with respect to the outer
sphere, surface 8.

<!-- image -->

|   1 | 0 1 -2 -3                                 |
|-----|-------------------------------------------|
|   2 | 0 3 -4 -5                                 |
|   3 | 0 5 -6 -7                                 |
|   4 | 0 #1 #2 #3 -8 $ or (-1:4:7:2 -3:5 6) -8   |
|   5 | 0 8 $ everything outside the outer sphere |

Some users might try defining cell 5 simply as #4 (i.e., not cell 4).
However, that would be incorrect. That syntax says cell 5 is everything
in the universe not in cell 4, which includes cells 1, 2, and 3. The
specification #4 #1 #2 #3 would be correct but should not be used
because it is computationally inefficient. It tells MCNP6 that cell 5 is
bounded by surfaces 1 through 7 in addition to surface 8. The lesson
here is that extra, irrelevant surfaces in cell definitions-implicit or
explicit-can cause MCNP6 to run significantly more slowly than it should
because any time a particle enters a cell or has a collision in it, the
intersection of the particle's trajectory with each bounding surface has
to be calculated.

Specifying cell 4 exclusively with the complement operator is very
convenient and computationally efficient in this case. However, it will
be instructive to set up cell 4 explicitly without complements. There
are many different ways to specify cell 4, The following approach should
not be considered to be the way.

First consider cell 4 to be everything outside the big cylinder of
surface 4 that is bounded on each end by surfaces 1 and 7. This is
specified by (-1:4:7). The parentheses are not necessary but may add
clarity. Now all that remains is to add the corners outside cylinders 2
and 6. The corner outside cylinder 2 is (2 -3), whereas it is (5 6)
outside cylinder 6. Again the parentheses are optional. These corners
are then added to what we already have outside cylinder 4 to get

(-1:4:7):(2 -3):(5 6)

The region described so far does not include cells 1, 2, or 3 but
extends to infinity in all directions. This region needs to be
terminated at the spherical surface 8. In other words, cell 4 is
everything we have defined so far that is also common with everything
inside surface 8 (that is, everything so far intersected with -8). So as
a final result,

((-1:4:7):(2 -3):(5 6)) -8

1

```
1
```

The inner parentheses can be removed, but the outer ones are necessary
(remember the hierarchy of operations) to give us

1

| (-1:4:7:2 -3:5 6) -8   |
|------------------------|

Figure 10.16: Horizontal and vertical cylinders in a sphere.

<!-- image -->

If the outer parentheses are removed, the intersection of -8 will occur
only with 5 and 6, an event that is clearly incorrect.

## 10.1.1.5 Example 5

This example (Fig. 10.16) is similar to the previous one except that a
vertical cylinder (surface 4) is added to one side of the horizontal
cylinder (surface 3).

Cell 1 is (1 -3 -2), cell 3 is #1 #2 #4, and cell 4 is just 6.

Cell 2 is more than might initially meet the eye. The description of
cell 2 might appear to be simply (-5 -4 3), but this definition causes
two images of cell 2 to be created: one we desire above the y axis and
one we do not want below the y axis. This undesired mirror image of cell
2 resides in the bottom half of cell 1 and is depicted by the dashed
lines in Fig. 10.16. We need to add an ambiguity surface to keep cell 2
above the y axis. Let surface 7 be an ambiguity surface that is a plane
at z = 0 . This surface is defined in the MCNP6 input file like any
other surface. Then cell 2 becomes (-5 -4 3 7) for the final result. You
should convince yourself that the region above surface 7 intersected
with the region defined by -5 -4 3 is cell 2. Do not even think of
surface 7 as an ambiguity surface but just another surface defining some
region in space. The mirror problem can also be avoided by defining
cells 1 and 2 as right-circular-cylinder ( RCC ) macrobodies. The
necessary cards for defining cells 1 and 2 as macrobodies could be, for
example,

```
1 1 rcc 0 -2 0 0 4 0 4 2 2 rcc 0 0 0 0 0 7 1
```

In this case cells 1, 2 and 3 would simply be (-1), (-2 1), and (1 2 -6)
respectively. Notice that to get the interface between the cylinders
correct, macrobody 2 extends into cell 1 and is then truncated by the
definition of cell 1.

## 10.1.1.6 Example 6

Figure 10.17 contains three concentric spheres with a box cut out of
cell 3. Surface 8 is the front of the box and surface 9 is the back of
the box. The cell cards are

<!-- image -->

Figure 10.17: A box located within a concentric sphere.

```
1 1 0 -1 2 2 0 -2 1 3 3 0 -3 2 (-4:5:-6:7:8:-9) $ These parentheses are required. 4 4 0 3 5 5 0 4 -5 6 -7 -8 9
```

Cell 3 is everything inside surface 3 intersected with everything
outside surface 2 but not in cell 5. Therefore, cell 3 could be written
as

1

```
3 0 -3 2 #(4 -5 6 -7 -8 9)
```

or

```
1 3 0 -3 2 #5
```

or

1

1

2

```
3 0 -3 2 (-4:5:-6:7:8:-9)
```

Cell 5 could also be specified using a RPP macrobody. The correct cell
and surface cards for this would be

```
5 0 -4 $ Cell card 4 rrp 2 4 7.5 8.5 -2 2 $ Surface card
```

1

2

3

4

5

6

## 10.1.1.7 Example 7

Figure 10.18 contains three concentric boxes, a geometry that is very
challenging to set up using only intersections, easier with unions, and
almost trivial with the BOX macrobody. Surfaces 5, 11, and 17 are the
back sides of the boxes (smaller to larger, respectively); 6, 12, and 18
are the fronts:

```
1 0 -2 -3 4 1 5 -6 2 0 -7 -8 9 10 11 -12 (2 : 3 : -4 : -1 : -5 : 6) 3 0 -13 -14 15 16 17 -18 (7 : 8 : -9 : -10 : -11 : 12) 4 0 13 : 14 : -15: -16 : -17: 18
```

## 10.1.1.8 Example 8

Figure 10.19 contains two concentric spheres with a torus attached to
cell 2 and cut out of cell 1:

```
1 1 0 -1 4 2 2 0 -2 (1 : -4) 3 3 0 2
```

If the torus were attached to cell 1 and cut out of cell 2, this bug-
eyed geometry would be:

1

2

3

```
1 0 -1 : -4 2 0 -2 1 4 3 0 2
```

Figure 10.18: Concentric boxes.

<!-- image -->

1

2

3

## 10.1.1.9 Example 9

Notice that cell 17 is disconnected, having two pieces. Cell 9 in Fig.
10.20 is a box cut out of the left part of spherical cell 17; surface 9
is the front of the box and surface 8 is the rear. The right part of
cell 17 is the space interior to spheres 6 and 7. An F4 tally in cell 17
would be the average flux in all parts of cell 17. An F2 surface tally
on surface 7 would be the flux across only the solid portion of surface
7 in the figure. The cell specifications are:

```
9 0 -3 -2 4 1 8 -9 17 0 -5 (3 : -4 : -1 : 2 : 9 : -8) : -6 : -7 22 0 5 6 7
```

A variation on this problem is for the right portion of cell 17 to be
the intersection of the interiors of surfaces 6 and 7 (the region
bounded by the dashed lines in Fig. 10.20):

```
1 9 0 -3 -2 4 1 8 -9 2 17 0 -5 (3 : -4 : -1 : 2 : 9 : -8) : -6 -7
```

Figure 10.19: Torus attached to a concentric sphere.

<!-- image -->

Figure 10.20: Disconnected cell.

<!-- image -->

```
3 22 0 5 (6 : 7)
```

## 10.1.1.10 Example 10

Figure 10.21 contains a box with a cone sitting on top of it. Surface 6
is the front of the box and 7 is the rear. You should understand this
example before going on to the next one.

```
1 1 0 1 2 -3 (-4 : -5) -6 7 2 2 0 -1 : -2 : 3 : 4 5 : 6 : -7
```

This problem could be simplified by replacing surfaces 1-6 with a BOX
macrobody. To specify individual macrobody surfaces, the resulting cell
and surface definitions must use macrobody facet notation. Typical cell
and surface cards would look like

```
1 c cell cards 2 1 0 -8:(-5 8.5) 3 2 0 #1 $ or -8.4:-8.6:8.3:(8.5 5):8.1:-8.2 4 5 c surface cards 6 5 kz 8 0.25 -1 7 8 box -2.5 -2.5 0 5 0 0 0 5 0 0 0 5
```

## 10.1.1.11 Example 11

Two views of this example appear in Figure 10.22. Surfaces 15 and 16 are
cones, surface 17 is a sphere, and cell 2 is disconnected.

```
1 1 0 -1 2 3 (-4 : -16) 5 -6 (12 : 13 : -14) 2 (10 : -9 : -11 : -7 : 8) 15 3 2 0 -10 9 11 7 -8 -1 : 2 -12 14 -6 -13 3 4 3 0 -17 (1 : -2 : -5 : 6 : -3 : -15 : 16 4) 5 4 0 17
```

Figure 10.21: Box with an upside-down cone.

<!-- image -->

1

2

3

Figure 10.22: Views from two different perspectives of a complicated four-cell model.

<!-- image -->

Figure 10.23: Two intersecting cylinders.

<!-- image -->

## 10.1.1.12 Example 12

In Figure 10.23, cell 1 consists of two cylinders joined at a 45-degree
angle. Cell 2 is a disk consisting of a cylinder (surface 8) bounded by
two planes. Surface 5 is a diagonal plane representing the intersection
of the two cylinders. The problem is to specify the disk (cell 2) in one
cell formed by the two cylinders (cell 1). A conflict arises in
specifying cell 1 since, from the outside of cell 3, corner a between
surfaces 1 and 3 is convex, but on the other side of the cell the same
two surfaces form a concave corner at b. The dilemma is solved by
composing cell 1 of two disconnected cells, each bounded by surface 5
between corners a and b. Surface 5 must be included in the list of
surface cards in the MCNP6 input file. When the two parts are joined to
make cell 1, surface 5 does not appear. Convince yourself by plotting it
using an origin of 0 0 24 and basis vectors 0 1 1 0 -1 1. See Chapter 6
for an explanation of plotting commands.

```
1 0 (2 -1 -5 (7:8:-6)):(4 -3 5(-6:8:7)) 2 0 -8 6 -7 3 0 (-2:1:5) (-4:3:-5)
```

A more efficient expression for cell 1 is

1

Figure 10.24: More complicated, yet straightforward to define.

<!-- image -->

## 1 0 (2 -1 -5:4 -3 5) (-6:8:7)

## 10.1.1.13 Example 13

This example (Figure 10.24) has the most complicated geometry so far,
but it can be described very simply.

You can see that this example is similar to §10.1.1.1. There is just a
lot more of it. It is possible to set this geometry up by any of the
ways mentioned in §10.1.1.1. However, going around the outer surfaces of
the cells inside cell 10 is tedious. There is a problem of visualization
and also the problem of coming up with undefined tunnels going off to
infinity as in §10.1.1.1.

The way to handle this geometry is by the last method in §10.1.1.1. Set
up the cell/surface relations for each interior cell, then just take the
complement for cell 10. For the interior cells,

|   1 | 0   | 1 -2 -23     |         |
|-----|-----|--------------|---------|
|   2 |     | 25 -24       | 0 -3 2  |
|   3 | 0   | 3 -5 12 -15  | 16 -11  |
|   4 | 0   | 5 -6 12 -17  | 18 -11  |
|   5 | 0   | 6 -8 12 -13  | -19 20  |
|   6 |     | -9           | 0 8 -26 |
|   7 | 0   | 4 -7         | -12 -27 |
|   8 | 0   | -12 7 -10 14 | -21 22  |
|   9 |     | -3           | 0 2 -25 |

Figure 10.25: Sphere in a box in a box.

<!-- image -->

Cell 10 is surrounded by the spherical surface 28. Considering cell 10
to be everything outside cells 1 through 9 but inside surface 28, one
can reverse the senses and replace all intersections with unions to
produce

1

2

3

4

5

6

7

1

1

| 10   | 0 (-1:2:23) (3:-25:24:-2)   |
|------|-----------------------------|
|      | (-3:5:-12:15:-16:11)        |
|      | (-5:6:-12:17:-18:11)        |
|      | (-6:8:-12:13:19:-20)        |
|      | (-8:9:26) (12:-4:7:27)      |
|      | (12:-7:10:-14:21:-22)       |
|      | (-2:3:25) -28               |

Note how easy cell 10 becomes when the complement operator is used:

## 10 0 #1 #2 #3 #4 #5 #6 #7 #8 #9 -28

Once again this example can be greatly simplified by replacing all but
cell 7 with macrobodies. However the definition of cell 7 must then be
changed to use the facets of the surrounding macrobodies instead of
surfaces 12 and 7. The facets of macrobodies can be visualized using the
MBODY OFF option of the geometry plotter [§6.2.4.1.4].

## 10.1.1.14 Example 14

Figure 10.25 illustrates some necessary conditions for volume and area
calculations. The geometry has three cells, an outer cube, an inner
cube, and a sphere at the center. If cell 3 is described as

```
3 0 8 -9 -10 11 -12 13 #2 #1
```

(and #1 must be included to be correct), the volume of cell 3 cannot be
calculated. As described, it is not bounded by all planes so it is not a
polyhedron, nor is it rotationally symmetric. If cell 3 is described by
listing all 12 bounding surfaces explicitly, the volume can be
calculated.

Figure 10.26: Tilted can in the y -z plane showing the main and auxiliary coordinate systems.

<!-- image -->

## 10.1.2 Coordinate Transformations

In most problems, the surface transformation feature of the TR card will
be used with the default setting, m = 1 . When m = 1 applies, most of
the geometry can be set up easily in an ( x, y, z ) coordinate system
and only a small part of the total geometry will be difficult to
specify. For example, a box with sides parallel to the ( x, y, z )
coordinate system is simple to describe, but inside might be a tilted
object consisting of a cylinder bounded by two planes. Since the axis of
the cylinder is neither parallel to nor on the x , y , or z axis, a
general quadratic must be used to describe the surface of the cylinder.
The GQ surface card has ten entries that are usually difficult to
determine. On the other hand, it is simple to specify the entries for
the surface card for a cylinder centered on the y axis. Therefore, we
define an auxiliary coordinate system ( x ′ , y ′ , z ′ ) so the axis of
the cylinder is one of the primed axes, y ′ for example. Now we will use
the TR card to describe the relationship between one coordinate system
and the other. The m = 1 specification on the TR card requires that the
coordinates of a vector from the ( x, y, z ) origin to the ( x ′ , y ′ ,
z ′ ) origin be given in terms of ( x, y, z ) .

Only in rare instances will m = -1 be needed. Some unusual circumstances
may require that a small item of the geometry be described in a certain
system which we will call ( x, y, z ) , and the remainder of the
surfaces would be easily described in an auxiliary system ( x ′ , y ′ ,
z ′ ) . The o i displacement entries on the TR card are then the
coordinates of a vector from the ( x ′ , y ′ , z ′ ) origin to the ( x,
y, z ) origin given in terms of the primed system.

## 10.1.2.1 Example 15

The following example consists of a can whose axis is in the y -z plane
but tilted 30 ◦ from the y axis and whose center is at (0 , 10 , 15) in
the ( x, y, z ) coordinate system. The can is bounded by two planes and
a cylinder, as shown in Fig. 10.26.

The surface cards that describe the can in the simple ( x ′ , y ′ , z ′
) system are the following:

1

2

3

|   1 | 1 CY   |   4 |
|-----|--------|-----|
|   2 | 1 PY   |  -7 |
|   3 | 1 PY   |   7 |

The 1 before the surface mnemonics on the cards is the n that identifies
to which TRn card these surface cards are associated. TRn card indicates
the relationship of the primed coordinate system to the basic coordinate
system.

We will specify the origin vector as the location of the origin of the (
x ′ , y ′ , z ′ ) coordinate system with respect to the ( x, y, z )
system; therefore, m = 1 . Since we wanted the center of the cylinder at
(0 , 10 , 15) , the o i

1

10

11

12

entries are simply 0 10 15 . If, however, we had wanted surface 2 to be
located at ( x, y, z ) = (0 , 10 , 15) , a different set of surface
cards would accomplish it. If surface 2 were at y ′ = 0 and surface 3 at
y ′ = 14 , the o i entries would remain the same. The significant fact
to remember about the origin vector entries is that they describe one
origin with respect to the other origin. The user must locate the
surfaces about the auxiliary origin so that they will be properly
located in the main coordinate system.

The rotation matrix entries on the TRn card are the cosines of the
angles between the axes as listed in §5.5.3. In this example, the x axis
is parallel to the x ′ axis. Therefore, the cosine of the angle between
them is 1. The angle between y and x ′ is 90 ◦ with a cosine of 0. The
angle between z and x ′ , and also between x and y ′ , is 90 ◦ with a
cosine of 0. The angle between y and y ′ is 30 ◦ with a cosine of 0.866.
The angle between z and y ′ is 60 ◦ with a cosine of 0.5. Similarly, 90
◦ is between x and z ′ ; 120 ◦ is between y and z ′ ; and 30 ◦ is
between z and z ′ . The complete TRn card is

```
1 TR1 0 10 15 1 0 0 0 0.866 0.5 0 -0.5 0.866
```

An asterisk preceding TRn indicates that the rotation matrix entries are
the angles given in degrees between the appropriate axes. The entries
using the * TR n mnemonic become

```
1 * TR1 0 10 15 0 90 90 90 30 60 90 120 30
```

The default value of 1 for m , the thirteenth entry, has been used and
is not explicitly specified.

The user need not enter values for all of the rotation matrix entries.
As shown in §5.5.3, the rotation matrix may be specified in any of five
patterns. Pattern 3(a) was used above, but the simplest form for this
example is pattern 3(d) because all the skew surfaces are surfaces of
revolution about some axis. The complete input card then becomes

```
* TR1 0 10 15 3J 90 30 60
```

## 10.1.2.2 Example 16

The following example illustrates another use of the TR n card. The
first part of the example uses the TR card and the default m =1
transformation; the second part uses the TR card with m = -1 . Both
parts and transformations are used in the following input file.

```
1 EXAMPLE OF SURFACE TRANSFORMATIONS 2 2 0 -4 3 -5 3 6 0 -14 -13 : -15 41 -42 4 998 0 #2 #6 -999 5 999 0 999 $ outside world 6 7 C Cell 2 surfaces 8 3 1 PX -14 9 4 1 X -14 10 0 12 14 10 5 1 PX 14 C C Cell 6 surfaces
```

Listing 10.1: example\_tr.card.mcnp.inp.txt

<!-- image -->

Figure 10.27: A tilted barrel as seen from three views.

```
13 13 2 SX -15 70 14 14 2 CX 30 15 15 2 KY 75 1.2641975E-01 16 41 2 PY 0 17 42 2 PY 75 18 C 19 C Surface defining outside world 20 999 so 500 21 22 TR1 20 31 37 0.223954 0.358401 0.906308 23 TR2 -250 -100 -65 0.675849 0.669131 0.309017 24 J J 0.918650 J J -0.246152 -1 25 C 26 IMP:N 1 1 1 0 27 SDEF 28 PRINT 29 NPS 5000
```

## 10.1.2.2.1 Case 1: TR and m =1

Cell 2 is bounded by the planar surfaces 3 and 5 and the spheroid
surface 4, which is a surface of revolution about the skew axis x ′ in
Fig. 10.27.

To get the coefficients of surfaces 3, 4, and 5, define the x ′ axis as
shown in the drawings. Because the surfaces are surfaces of revolution
about the x ′ axis, the orientation of the y ′ and z ′ axes does not
matter. Then set up cell 2 and its surfaces with coefficients defined in
the ( x ′ , y ′ , z ′ ) coordinate system.

On the TR 1 card, the origin vector is the location of the origin of the
( x ′ , y ′ , z ′ ) coordinate system with respect to the main ( x, y, z
) system of the problem. The rotation matrix pattern 3(d) in §5.5.3 is
appropriate

Figure 10.28: Angles between the x ′ axis and the main ( x, y, z ) coordinate system of Case 1.

<!-- image -->

since the surfaces are all surfaces of revolution about the x ′ axis.
The components of one vector of the transformation matrix are the
cosines of the angles between x ′ and the x , y , and z axes. They are
obtained from spherical trigonometry as shown in Fig. 10.28 and by
calculating

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## 10.1.2.2.2 Case 2: TR and m = -1

Cell 6 is the union of a can bounded by spherical surface 13,
cylindrical surface 14, conical surface 15, and two ambiguity surfaces
[§2.2.3.2] 41 and 42, which are planes. Surface 42 is required because
when surface 15 is transformed into the ( x, y, z ) system it becomes a
type GQ surface, which in this case is a cone of two sheets [Note 5 of
§5.5.3]. Surfaces 13 and 14 are surfaces of revolution about one axis,
and surfaces 15, 41, and 42 are surfaces of revolution about an axis
perpendicular to the first axis. Both axes are skewed with respect to
the ( x, y, z ) coordinate system of the rest of the geometry.

Define the auxiliary ( x ′ , y ′ , z ′ ) coordinate system as shown in
Fig. 10.29. Set up cell 6 with its surfaces specified in the ( x ′ , y ′
, z ′ ) coordinate system as part of the input file and add a second
transformation card, TR2 .

Because the location of the origin of the ( x, y, z ) coordinate system
is known relative to the ( x ′ , y ′ , z ′ ) system (rather than the
other way around, as in Case 1), it is necessary to use the reverse
mapping. This is indicated by setting m = -1 . In this reverse mapping,
the origin vector ( -250 , -100 , -65) is the location of the origin of
the ( x, y, z ) system with respect to the ( x ′ , y ′ , z ′ ) system.
For the components of the transformation matrix, pattern 3(c) out of the
five possible choices from §5.5.3 is most convenient here. The ( x, y, z
) components of z ′ and the ( x ′ , y ′ , z ′ ) components of z are easy
to get, while the components of x and of y are not. The whole
transformation matrix with the components that are obtained from Fig.
10.29 is given in Table 10.1.

The signs of the zz ′ and xx ′ components are determined by inspection
of the figure.

Figure 10.29: Case 2 geometry.

<!-- image -->

Table 10.1: Case 2 Transformation Matrix

<!-- image -->

| x                                                    | y                       | z                                              |
|------------------------------------------------------|-------------------------|------------------------------------------------|
| √ 1 . 0 - 0 . 669131 2 - 0 . 309017 2 ) = 0 . 675849 | cos(48 ◦ ) = 0 . 669131 | cos(72 ◦ ) = 0 . 309017                        |
| J                                                    | J                       | cos(15 ◦ ) cos(18 ◦ ) = 0 . 918650             |
| J                                                    | J                       | √ 1 . 0 0 . 669131 2 0 . 309017 2 = 0 . 675849 |

-

-

-

## 10.1.3 Repeated Structure and Lattice Examples

## 10.1.3.1 Example 17

The example shown in Listing 10.2 illustrates the use of transformations
with simple repeated structures.

Listing 10.2: example\_lattice\_geometry\_1.mcnp.inp.txt

| simple repeated structures   | simple repeated structures   | simple repeated structures   | simple repeated structures   | simple repeated structures   | simple repeated structures   | simple repeated structures   | simple repeated structures   | simple repeated structures   | simple repeated structures   |
|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
| 1                            | 0                            | -27                          | #2 #5                        |                              |                              |                              | imp:n=1                      | 2                            |                              |
| 2                            | 0                            | 1                            | -2 -3                        | 4                            | -5                           | 6 fill=1                     | imp:n=1                      | 3                            |                              |
| 3                            | 0                            | -10                          | -11                          | 12                           |                              | u=1                          | imp:n=1                      | 4                            |                              |
| 4                            | 0                            | #3                           |                              |                              |                              | u=1                          | imp:n=1                      |                              |                              |
| 5                            | like                         | 2                            | but                          | trcl=3                       |                              |                              |                              | 6                            |                              |
| 7                            | 0                            | 27                           |                              |                              |                              |                              | imp:n=0                      | 7                            |                              |
| 1                            | px                           |                              |                              |                              |                              |                              |                              | 9 -3                         |                              |
| 2                            |                              |                              | 3                            |                              |                              |                              |                              | px                           |                              |
| 3                            |                              |                              | 3                            |                              |                              |                              |                              | py                           |                              |
| 4                            |                              | -3                           |                              |                              |                              |                              |                              | py                           |                              |
| 5                            | pz                           |                              | 4.7                          |                              |                              |                              |                              |                              |                              |
| 6                            |                              |                              | -4.7                         |                              |                              |                              |                              | pz                           |                              |
|                              | cz                           |                              | 1                            |                              |                              |                              |                              | 10                           |                              |
| 11                           | pz                           |                              | 4.5                          |                              |                              |                              |                              |                              |                              |
| 12                           | pz                           | -4.5                         |                              |                              |                              |                              |                              |                              |                              |
| 27                           | s                            | 3.5                          | 3.5                          | 0 11                         |                              |                              |                              |                              |                              |
| sdef                         |                              | pos                          | 3.5 3.5                      | 0                            |                              |                              |                              |                              |                              |
| f2:n                         |                              | 1                            |                              |                              |                              |                              |                              |                              |                              |
| * tr3                        |                              | 7 7 0                        | 40 130                       | 90                           | 50 40                        | 90                           | 90 90 0                      |                              |                              |
| nps                          |                              |                              |                              |                              |                              |                              |                              | 10000                        |                              |

The geometry consists of a sphere enclosing two boxes that each contains
a cylindrical can.

The geometric structure of this example can be displayed using the plot
feature in MCNP6. Specifically, Fig. 10.30 can be obtained by launching
the plotter:

```
1 mcnp6 ip i= example _ lattice _ geometry _ 1.mcnp.inp.txt
```

clicking the lower left hand corner of the plot window ( click here or
picture or window ) and entering the following three settings:

1

2

3

| b 1 0 0 0 1 0   |
|-----------------|
| ex 11           |
| or 3.5 3.5 0    |

Cell 2 is filled by universe 1. Two cells are in universe 1-the
cylindrical can, cell 3, and the space outside the can, cell 4. Cell 2
is defined and the LIKE n BUT card duplicates the structure at another
location. The TRCL entry identifies a TR card that defines the
displacement and rotational axis transformation for cell 5.

Figure 10.30: Geometry of Example 1: a sphere enclosing two boxes that each contains a cylindrical can.

<!-- image -->

## 10.1.3.2 Example 18

The example shown in Listing 10.3 illustrates the LIKE n BUT construct,
the FILL card, the U card, two forms of the TRCL card, and a multiple
source-cell definition.

```
1 lattice example 18 2 1 1 -0.5 -7 #2 #3 #4 #5 #6 imp:n=1 3 2 0 1 -2 -3 4 5 -6 imp:n=2 trcl=2 fill=1 4 3 like 2 but trcl=3 5 4 like 2 but trcl=4 6 5 like 2 but trcl=5 imp:n=1 7 6 like 2 but trcl=6 8 7 0 7 imp:n=0 9 8 0 8 -9 -10 11 imp:n=1 trcl=(-.9 .9 0) fill=2 u=1 10 9 like 8 but trcl=(.9 .9 0) 11 10 like 8 but trcl=(.1 -.9 0) 12 11 2 -18 #8 #9 #10 imp:n=1 u=1 13 12 2 -18 -12 imp:n=1 trcl=(-.3 .3 0) u=2 14 13 like 12 but trcl=( .3 .3 0) 15 14 like 12 but trcl=( .3 -.3 0) 16 15 like 12 but trcl=(-.3 -.3 0) 17 16 1 -0.5 #12 #13 #14 #15 u=2 imp:n=1 18 19 1 px -2 20 2 py 2 21 3 px 2 22 4 py -2 23 5 pz -2 24 6 pz 2 25 7 so 15 26 8 px -0.7
```

Listing 10.3: example\_lattice\_geometry\_2.mcnp.inp.txt

<!-- image -->

| 9           | py                                        | 0.7                              | 27       |    |
|-------------|-------------------------------------------|----------------------------------|----------|----|
| 10 px       | 0.7                                       |                                  | 28       |    |
| 11          | py -0.7                                   |                                  | 29       |    |
| 12          | cz 0.1                                    |                                  | 30       |    |
| sdef #      | erg=d1 cel=d2 rad=d5 ext=d6 axs=0 si1 sp1 | 0 1 pos=d7 sb1                   | 32 33    |    |
| si7 sp7     | 1 0 L 8 9 8 9 2 0 1 0                     | 0                                | 34 43    |    |
|             | 3 0.22 4 0.08                             | 0.05                             | 35       |    |
|             | 0.25                                      | 0.05                             | 36       |    |
|             | 5 6                                       | 0.1                              | 37       |    |
|             | 0.18 7 0.07                               | 0.1                              | 38       |    |
|             | 8 0.1                                     | 0.2 0.2                          | 39 40    |    |
|             | 0.05                                      | 0.1                              | 41       |    |
|             | 9 11                                      | 0.05 0.2                         | 42       |    |
| si2         | (12 <                                     | 10 < 2 3 4 5 6 ) 10 )            |          |    |
|             | (13 < (14 < 8 9                           | < 2 3 4 5 6 10 < 2 3 4 5 6 )     | 44 45    |    |
| si5         | (15 < 8 9                                 | 10 < 2 3 4 5 6                   | 46 47    |    |
| sp2         |                                           |                                  |          |    |
|             | 59r                                       |                                  |          |    |
|             | 1 0 0.1                                   |                                  |          |    |
| sp5 si6     | -21 1 -2                                  | )                                | 48 49 50 |    |
| sp6         | 0.3 0.3                                   | 0.3 -0.3 0 -0.3 0.3 0 -0.3 1 1 1 | 51 52    |    |
| L           | 1                                         | -0.3                             | 53       |    |
| c           |                                           |                                  | 54       |    |
| m1          | 6000 1                                    |                                  | 55       |    |
| m2          | 92235 1                                   | 1.2 1.1                          | 56 57 58 |    |
| c drxs tr2  | -6 7                                      | 1.4                              | 59       |    |
| tr3 tr4 tr5 | 7 6 8 -5 -1 -4 1                          | 90 90 90 0                       | 60 61    |    |
| * tr6       | -9 -2 1.3 2 3                             | 40 130 90 50 40                  | 62 63    |    |
| f4:n e4     | 4 5 1 3 5                                 | 12 13 14 15                      | 64       |    |
|             | 7 5j                                      | 6 9 11 13 1.8849555921 3r        | 65       |    |
| sd4 fq      | f e 1e20                                  | 0.1                              | 66 67    |    |
| cut:n       |                                           |                                  | 68       |    |
| print       |                                           |                                  |          |    |
| nps         |                                           |                                  |          |    |
|             | 100000                                    |                                  |          |    |
|             |                                           |                                  | 70       | 69 |

Cell 2 could be replaced with an RPP macrobody that can then be
replicated and translated identically to cell 2 above.

Figure 10.31 can be displayed using the geometry plotter in command-
prompt mode [§6.2.4] and entering:

basis 1 0 0 0 1 0 extent 21 label 0 0

Figure 10.31 shows five cells, numbers 2 through 6, identical except for
their locations. Cell 2 is described fully and the other four are
declared to be like cell 2 but in different locations. Cell 2 is defined
in an auxiliary coordinate system that is centered in the cell for
convenience. That coordinate system is related to the main

1

Figure 10.31: Repeated structures located at different positions and orientations.

<!-- image -->

coordinate system of the problem by transformation number 2, as declared
by the TRCL=2 entry and the TR2 card. Cells 2 through 6 are all filled
with universe number 1. Because no transformation is indicated for that
filling, universe 1 inherits the transformation of each cell that it
fills, thereby establishing its origin in the center of each of those
five cells.

As shown in Fig. 10.32, universe 1 contains three infinitely long square
tubes embedded in cell 11, which is unbounded. All four of these
infinitely large cells are truncated by the bounding surfaces of each
cell that is filled by universe 1, thus making them effectively finite.
To illustrate the two possible ways of performing transformations, the
transformations that define the locations of cells 8, 9 and 10 are
entered directly on the cell cards after the TRCL symbol rather than
indirectly through TR cards as was done for cells 2 through 6. Cells 8,
9 and 10 are each filled with universe 2, which consists of five
infinite cells truncated by the boundaries of higher level cells. The
simplicity and lack of repetition in this example were achieved by
careful choice of the auxiliary coordinate systems at all levels. All of
the location information is contained in just a few TRCL entries, some
direct and some pointing to a few TR cards.

The source definition is given on the SDEF , SIn , and SPn cards. The
source desired is a cylindrical volume distribution, equally probable in
all the cylindrical rods. The energies are given by distribution 1. On
the CEL entry, source distribution 2 includes all 60 of the cylindrical
rod cells, using the shorthand method described in §5.8.1.6. A
cylindrical volume distribution is specified by the source distributions
on the RAD , EXT , AXS , and POS entries. The cylinder is centered about
the origin, with a radius of 0.1 ( SI5 ) and a length of 4 ( SI6 , from
-2 to 2). The four sets of entries on the SI7 card are the origins of
the four cylinders of cells 12-15. These parameters describe exactly the
four cells 12-15.

## 10.1.3.3 Example 19

The example shown in Listing 10.4 illustrates the use of the FILL , U ,
and LAT cards to create an object within several cells of a lattice. A
cylinder contains a square lattice and the cells in the inner 3 × 3
array of that lattice each contain a small cylinder.

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

Figure 10.32: Close up of the repeated structure defined by universe 1 in Fig. 10.31.

<!-- image -->

Listing 10.4: example\_lattice\_geometry\_3.mcnp.inp.txt

<!-- image -->

The resulting geometry is shown in Fig. 10.33. Cell 1 is the interior of
the cylinder, and cell 5 is everything outside (all surfaces are
infinite in the z direction). Cell 1 is filled by universe 1. Cell 2 is
defined to be in universe 1. Surfaces 301-304 define the dimensions of
the square lattice.

When filling the cells of a lattice, all visible cells, even those only
partially visible, must be specified by the FILL card. In this case, the
'window' created by the cylinder reveals portions of 25 cells ( 5 × 5
array). A FILL card with indices of -2 to 2 in the x and y directions
will place the [0 , 0 , 0] element at the center of the array. Universe
2, described by cells 3 and 4, is the interior and exterior,
respectively, of an infinite cylinder of radius 8 cm. The cells in
universe 1 not filled by universe 2 are filled by universe 1, so in
effect they are filled by themselves.

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

Figure 10.33: The simple lattice defined by Example 3.

<!-- image -->

## 10.1.3.4 Example 20

The example shown in Listing 10.5 illustrates a lattice geometry and
uses the FILL entries followed by transformations, universes, and
lattices.

Listing 10.5: example\_lattice\_geometry\_4.mcnp.inp.txt

<!-- image -->

| Lattice example   |        |         |        |          |       |      |        |     |       |    |       |         |
|-------------------|--------|---------|--------|----------|-------|------|--------|-----|-------|----|-------|---------|
| 1                 | 1 -0.6 | -1      |        |          |       |      |        |     |       |    |       | imp:n=1 |
| c                 | 2 0    | 1       | 2 -4   |          |       |      |        |     |       |    |       | imp:n=1 |
| 2                 | 0      | 1 -2    | -4     | fill=1   | (-6   | -6.5 | 0)     |     |       |    |       | imp:n=1 |
| 3                 | 0      | 2 -3    | -4 *   | fill=2   | (-7 5 | 0    | 30     | 60  | 90    | 30 | 120   | imp:n=1 |
| 4                 | 0      | 2       | 3 -4   | * fill=2 | ( 4   | 8    | 0 15   | 105 | 90    | 15 | 75    | imp:n=1 |
| 5                 | 0      | 4       |        |          |       |      |        |     |       |    |       | imp:n=0 |
| 6                 | 0      | -5      | 6 -7   | 8        | -9 10 |      | fill=3 | u=1 |       |    | lat=1 | imp:n=1 |
| 7                 | 0      | -11     | 12 -13 | 14 -15   | 16    |      | fill=5 | u=2 | lat=1 |    |       | imp:n=1 |
| 18                | 3 -2.7 | -18     |        |          |       |      |        | u=5 |       |    |       | imp:n=1 |
| 8 -0.8            | 2      | -17 u=3 |        |          |       |      |        |     |       |    |       | imp:n=1 |
| 9                 | 0      | 17      | u=3    |          |       |      |        |     |       |    |       | imp:n=1 |
| 10                | 0      | -18     | u=4    |          |       |      |        |     |       |    |       | imp:n=1 |
| 1 -5              | sy     | 3       |        |          |       |      |        |     |       |    |       |         |
| 2                 | py     | 0       |        |          |       |      |        |     |       |    |       |         |
| 3                 | px     | 0       |        |          |       |      |        |     |       |    |       |         |
| 4                 | so     | 15      |        |          |       |      |        |     |       |    |       |         |
| 5                 | px     | 1.5     |        |          |       |      |        |     |       |    |       |         |
| 6 -1.5            | px     |         |        |          |       |      |        |     |       |    |       |         |
| 7 1               | py     |         |        |          |       |      |        |     |       |    |       |         |
| 8 -1              | py     |         |        |          |       |      |        |     |       |    |       |         |
| 9 3               | pz     |         |        |          |       |      |        |     |       |    |       |         |
| 10 -3             | pz     |         |        |          |       |      |        |     |       |    |       |         |
| 11 1              | p      | -0.5 0  | 1.3    |          |       |      |        |     |       |    |       |         |

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

47

48

49

<!-- image -->

Figure 10.34: Lattices with universes and coordinate transformation.

<!-- image -->

| 12 p   | 1 -0.5 0 -1.3           |
|--------|-------------------------|
| 13 py  | 0.5                     |
| 14 py  | -0.5                    |
| 15 pz  | 3                       |
| 16 pz  | -3                      |
| 17 sq  | 1 2 0 0 0 0 -1 0.2      |
| 18 so  | 10                      |
| sdef   | pos 0 -5 0 erg d1 rad   |
| si1    | 0 10                    |
| sp1    | 0 1                     |
| si2    | 3                       |
| sp2    | -21                     |
| e0     | 1 2 3 4 5 6 7 8 9 10 11 |
| f2:n   | 3                       |
| sd2    | 1                       |
| f4:n   | 8 9                     |
| sd4    | 1 1                     |
| m1     | 4009 1                  |
| m2     | 6000 1                  |
| m3     | 13027 1                 |
| nps    | 100000                  |
| print  | print                   |
| dbcn   | 0 0 1 4                 |

The geometry for this example is shown in Fig. 10.34.

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

Cell 2 is the bottom half of the large sphere outside the small sphere
(cell 1) and is filled by universe 1. The transformation between the
filled cell and the filling universe immediately follows in parentheses.

Cell 6 describes a hexahedral lattice cell ( LAT = 1 ) and, by the order
of specification of its surfaces, also describes the order of the
lattice elements. The [0 , 0 , 0] element has its center at ( -6 , -6 .
5 , 0) , according to the transformation information on the card for
cell 2. Element [1 , 0 , 0] is beyond surface 5, element [ -1 , 0 , 0]
is beyond surface 6, element [0 , 1 , 0] is beyond surface 7, etc. Cell
6 is filled by universe 3, which consists of two cells: cell 8 inside
the ellipsoid and cell 9 outside it.

Alternatively, cell 6 could have been defined using a macrobody, either
RPP or BOX . When a lattice cell is defined with a macrobody, some of
the lattice-element indexing is predetermined. For example, the first,
third and fifth facets are used to define the direction of increasing
indices. For the RPP , the second index increases in the positive y
direction and the third index increases in the positive z direction. For
the BOX , the order of defining the three vectors will determine the
axis each index will increase in a positive direction.

Cell 3 is the top left-hand quarter of the sphere; cell 4 is the top
right-hand quarter. Both are filled by universe 2. Both FILL entries are
followed by a transformation. The inter-origin vector portion of the
transformation is between the origin of the filled cell and the origin
of the filling universe, with the universe considered to be in the
auxiliary coordinate system. The [0 , 0 , 0] lattice element is located
around the auxiliary origin and the lattice elements are identified by
the ordering of the surfaces describing cell 7. The skewed appearance is
caused by the rotation part of the transformation.

The source is centered at (0 , -5 , 0) (i.e., at the center of cell 1).
It is a volumetric source filling cell 1, and the probability of a
particle being emitted at a given radius is given by the power-law
function. For RAD the exponent defaults to 2, so the probability
increases as the square of the radius, resulting in a uniform volumetric
distribution.

## 10.1.3.5 Example 21

The example in Listing 10.6 illustrates a more complicated lattice
geometry and uses the FILL card followed by the array specification. It
builds on the expertise from §10.1.3.4.

Listing 10.6: example\_lattice\_geometry\_9.mcnp.inp.txt

<!-- image -->

| 5         | s            | 7 2.1 0 3.5           |
|-----------|--------------|-----------------------|
| 6         | px           | 4                     |
| 7         | px           | -5                    |
| 8         | py           | 2                     |
| 9         | py           | -2                    |
| 10        | p 0.7        | -0.7 0 -2.5           |
| 11        | p 0.6        | 0.8 0 0.5             |
| 12        | py -1        |                       |
| 13        | x -4.5       | 0 -0.5 1.7 3.5 0      |
| 14        | px           | 1.6                   |
| 15        | px           | -1.4                  |
| 16        | py           | 1                     |
| 17        | py           | -1.2                  |
| 18        | px           | 3                     |
| 19        | px           | -3                    |
| 20        | py           | 0.5                   |
| 21        | py           | -0.6                  |
| 22        | pz           | 6                     |
| 23        | pz           | -7                    |
| 24        | so           | 10                    |
| sdef      | erg d1       | pos 7 2 0 cel=1       |
| si1       | si2 3.6 0    | 10                    |
| sp1       | 0            | 1                     |
| e4        | 1 3 5        | 7 9 11                |
| f4:n      | 10           |                       |
| m1        | 4009         | 1                     |
| m2        | 6000         | 1                     |
| m3 m4     | 13027 1001   | 1 2 8016 1            |
| nps       |              |                       |
| dbcn      | 0 0 1        | 4                     |
| * tr1     | 100000 0 0 0 | 10 80 90 100 10 90 88 |
| * tr2 tr3 | 1 0 0 3 0    | 90 92 2 90            |
| print     |              | 2                     |
|           |              | 0                     |

This example has three 'main' cells: cell 1 is inside surface 5, cell 3
is the outside world, and cell 2 is the large square (excluding cell 1)
that is filled with a lattice, some of whose elements are filled with
three different universes. A schematic of the geometry is given in Fig.
10.35.

Universe 1 is a hexahedral lattice cell infinite in the z direction.
Based on the FILL parameters, it can be seen that the lattice has five
elements in the first direction numbered from -2 to 2, nine elements in
the second direction numbered from -4 to 4, and one element in the third
direction. The remaining entries on the card are the array that
identifies which universe is in each element, starting in the lower
left-hand corner with [ -2 , -4 , 0] , [ -1 , -4 , 0] , [0 , -4 , 0] ,
etc. An array entry (in this case 1) that is the same as the number of
the universe of the lattice itself means that element is filled by the
material specified for the lattice cell. Element [1 , -3 , 0] is filled
by universe 2, which is located within the element in accordance with
the transformation defined on the TR 3 card. Element [ -1 , -2 , 0] is
filled by universe 3. Cell 7, part of universe 3, is filled by universe
5, which is also a lattice. Note the use of the X parameter to describe
surface 13. The quadratic surface, which is symmetric about the x axis,
is defined by specifying three coordinate pairs on the surface.

The source is a volumetric source of radius 3.6 cm which is centered in
and completely surrounds cell 1. The CEL keyword causes a cell rejection
technique to be used to sample uniformly throughout the cell. That is,
the source is sampled uniformly in volume and any points outside cell 1
are rejected. The same effect is

Figure 10.35: Example 21

<!-- image -->

achieved by using cookie-cutter rejection. The PRINT card results in a
full output print, and the VOL card sets the volumes of all the cells to
unity.

## 10.1.3.6 Example 22

The example shown in Listing 10.7 primarily illustrates a fairly complex
source description in a lattice geometry.

Listing 10.7: example\_lattice\_geometry\_5.mcnp.inp.txt

<!-- image -->

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

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

| 15 2 -18 -31 32 33 -34 imp:n=1 u=5                                                                                             |
|--------------------------------------------------------------------------------------------------------------------------------|
| 1 px 50                                                                                                                        |
| 2 px 0                                                                                                                         |
| 3 px -50                                                                                                                       |
| 4 py -20                                                                                                                       |
| 5 py 20                                                                                                                        |
| 6 pz 60                                                                                                                        |
| 7 pz -60                                                                                                                       |
| 11 px 8.334                                                                                                                    |
| 12 px -8.334                                                                                                                   |
| 13 py -6.67                                                                                                                    |
| 14 py 6.67                                                                                                                     |
| 15 px 25                                                                                                                       |
| 17 py 0                                                                                                                        |
| 18 py 10                                                                                                                       |
| 19 c/z 10 5 3                                                                                                                  |
| 20 c/z 10 5 3                                                                                                                  |
| 21 px 4                                                                                                                        |
| 22 px -4                                                                                                                       |
| 23 py -3                                                                                                                       |
| 24 py 3                                                                                                                        |
| 31 px 20                                                                                                                       |
| 32 px 16 33 py 3                                                                                                               |
| 34 py 6                                                                                                                        |
| m2 92238 0.98 92235 0.02 m3 1001 1                                                                                             |
| sdef erg fcel d1 x fcel d11 y fcel d13 z fcel d15 cel d6 rad fcel d17 ext fcel d19 pos fcel d21 axs fcel d23 ds1 s d2 d3 d4 d5 |
| sp2 -2 1.2 sp3 -2 1.3 sp4 -2 1.4                                                                                               |
| sp5 -2 1.42 si6 s d7 d8                                                                                                        |
| d9 d10 sp6 0.65 0.2 0.1 0.05 si7 l 2:4:8                                                                                       |
| sp7 1 si8 l 3:5(0 0 0):11                                                                                                      |
| 3:5(1 0 0):11 3:5(0 1 0):11 3:5(1 1 3:5(0 2 0):11 3:5(0 3 0):11 3:5(1 3 0):11                                                  |
| 0):11 sp8 1 1 1 1 1 1 1 si9 l 3:5(1 2 0):13                                                                                    |
| sp9 1 si10 l 3:5(1 2 0):15                                                                                                     |
| sp10 1 ds11 s d12 0 0 d25 si12 -4 4                                                                                            |
| sp12 0 1                                                                                                                       |
| ds13 s d14 0 0 d26 si14 -3 3                                                                                                   |
| sp14 0 1                                                                                                                       |
| ds15 s d16 0 0 d16                                                                                                             |
| si16 -60 60 sp16 0 1                                                                                                           |
| ds17 s 0 d18 d18                                                                                                               |
| 0                                                                                                                              |
| si18 0 3                                                                                                                       |

<!-- image -->

Figure 10.36: Example 22

<!-- image -->

The geometry consists of two 'main' cells, each filled with a different
lattice.

The geometry for this example is shown in Fig. 10.36.

Cell 2, the left half of Fig. 10.36, is filled with a hexahedral
lattice, which is in turn filled with a universe consisting of a
rectangular cell and a surrounding cell. The relationship of the origin
of the filling universe, universe 1, to the filled cell, cell 2, is
given by the transformation in parentheses following FILL = 1 . The
right half of Fig. 10.36, Cell 3, is filled with a different hexahedral
lattice, which in turn is filled by universes 4 and 5. Lattice cells
must be completely specified by an expanded FILL card if the lattice
contains a source (cell 5) or by selecting a coordinate system of a
higher level universe ( SI7 1 -2:4:8 ). PRINT Table 110 lists the
lattice elements that are being sampled.

The reader is cautioned to become familiar with the geometry before
continuing with the source description that follows. In this example, a
distributed volumetric source located in each of the ten boxes and eight
circles (in two dimensions) is desired. The cells involved are given by
distribution 6. The S on the SI 6

1

2

3

4

card indicates distribution numbers will follow. The four distributions
will describe the cells further. The probabilities for choosing each
distribution of cells are given by the SP 6 card.

The SI 7 card shows the entire path from level 0 to level n for the nine
boxes on the left. The expanded FILL notation is used on the cell 4 card
to describe which elements of the lattice exist and which universe fills
each one. All nine are filled by universe 3. The source information card
SI 12 indicates that x is sampled from -4 to 4; similarly, SI 14
indicates that y is sampled from -3 to 3. Used together with the
expanded FILL notation, source points will be sampled from all nine
lattice elements. Without the expanded FILL notation, only the [0 , 0 ,
0] element would have source points.

Alternatively, one could use the following input cards:

```
4 0 -11 12 -14 13 imp:n=1 lat=1 u=1 fill=3 si7 l -2:4:8 si12 -46 -4 si14 -17 17
```

The minus sign in front of the second entry on the SI 7 card means that
the sampled position and direction will be in the coordinate system of
the level preceding that entry. In this case, however, there is no
preceding entry, so the position and direction will be in the coordinate
system of cell 2. If a point is chosen that is not is cell 8, it is
rejected and the variable is resampled.

The SI 8 card describes a path from cell 3 through element [0 , 0 , 0]
of cell 5 to cell 11, from cell 3 through element [1 , 0 , 0] of cell 5
to cell 11, and so on. Element [1 , 2 , 0] is skipped and will be
treated differently. The SI 9 entries provide the path to cell 13, the
circle in element [1 , 2 , 0] , while SI 10 provides the path to cell
15, the box in element [1 , 2 , 0] . All the other source variables are
given as a function of the cell and follow explanations given in §5.8.

## 10.1.3.7 Example 23

The example shown in Listing 10.8 illustrates a hexagonal prism lattice
and shows how the order of specification of the surfaces on a cell card
identifies the lattice elements beyond each surface.

```
1 hexagonal prism lattice 2 1 0 -11 -19 29 fill=1 imp:n=1 3 2 0 -10 u=3 imp:n=1 4 3 0 -301 302 -303 305 -304 306 fill=3 lat=2 u=1 imp:n=1 5 4 0 11:19:-29 imp:n=0 6 7 11 cz 20 8 10 so 40 9 19 pz 31.75 10 29 pz -31.75 11 301 px 1 12 302 px -1 13 303 p 1 1.7320508076 0 2 14 304 p -1 1.7320508076 0 2 15 305 p 1 1.7320508076 0 -2 16 306 p -1 1.7320508076 0 -2 17 18 sdef 19 f1:n 11 20 nps 2000
```

Listing 10.8: example\_lattice\_geometry\_6.mcnp.inp.txt

Figure 10.37: Hexagonal prism lattice.

<!-- image -->

The geometry for this example is shown in Fig. 10.37.

The [0 , 0 , 0] element is the space described by the surfaces on the
cell card, perhaps influenced by a TRCL entry. The user chooses where
the [0 , 0 , 0] element will be. The user chooses the location of the [1
, 0 , 0] element-it is beyond the first surface entered on the cell
card. The [ -1 , 0 , 0] element must be in the opposite direction from
[1 , 0 , 0] and must be beyond the second surface listed. The user then
chooses where the [0 , 1 , 0] element will be-it must be adjacent to the
[1 , 0 , 0] element-and that surface is listed next. The [0 , -1 , 0]
element must be diagonally opposite from [0 , 1 , 0] and is listed
fourth. The fifth and sixth elements are defined based on the other four
and must be listed in the correct order: [ -1 , 1 , 0] and [1 , -1 , 0]
. Pairs can be picked in any order, but once set the pattern must be
followed. The example illustrates one pattern that could be selected and
shows how the numbering of elements progresses outward from the center.

One of the most powerful uses of macrobodies is for the specification of
hexagonal prisms. The example in Figure 10.37 can be simplified by using
the RHP (also called HEX ) macrobody as shown in Listing 10.9.

Listing 10.9: example\_lattice\_geometry\_7.mcnp.inp.txt

<!-- image -->

| 14 f1:n   |   2.1 |
|-----------|-------|
| 15 nps    |  2000 |

## 10.1.3.8 Example 24

The example shown in Listing 10.10 demonstrates how the LIKE n BUT and
TRCL cards can be used to create an array of non-identical objects
within each cell of a lattice.

Listing 10.10: example\_lattice\_geometry\_8.mcnp.inp.txt

<!-- image -->

<!-- image -->

Figure 10.38: Example 24

<!-- image -->

A horizontal slice through this configuration is shown in Fig. 10.38.

Only one lattice element is shown in Fig. 10.38. A lattice of hexahedral
subassemblies, each holding an array of 25 cylindrical rods, is
contained within a cylindrical cell. Cell 1, the space inside the large
cylinder, is filled with universe 1. Cell 2 is the only cell in universe
1 and is the hexahedral lattice that fills cell 1. The lattice is a 7 ×
7 × 1 array, indicated by the array indices on the FILL card, and it is
filled either by universe 2 or by itself (that is, universe 1). Cell 3,
a fuel rod, is in universe 2 and is the space inside the cylindrical
rod. The other fuel cells, 5-24, are like cell 3 but at different x, y
locations. The material in these 21 fuel cells is slightly enriched
uranium. Cells 25-28 are control rods. Cell 25 is like 3 but the
material is changed to cadmium, and the density and the x, y location
are different. Cells 26-28 are like cell 25 but at different x, y
locations. Cell 4 is also in universe 2 and is the space outside all 25
rods. To describe cell 4, each cell number is complemented. All the
surfaces in Fig. 10.38 except for the center one have a new predictable
surface number equal to 1000 × ( cell number ) + ( surface number ) .
These numbers could be used in the description of cell 4 if desired.

The KCODE and KSRC cards appear because this example is a criticality
calculation. The KCODE card specifies that there are 1000 particles per
cycle, the initial guess for k eff is 1, 5 cycles are skipped before the
tally accumulation begins, and a total of 10 cycles will be run. The
KSRC indicates that the neutron source for the first cycle will be a
point source at the origin.

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

## 10.1.4 Embedded Meshes: Structured and Unstructured

In the following example, we first create a structured PARTISN-style
geometry mesh and save it in LNK3DNT format. The cylindrical mesh
consists of two materials in a checkerboard pattern that appears
radially, axially, and azimuthally. After the LNK3DNT-format mesh file
is created, we then embed the mesh in a new MCNP6 file.

## 10.1.4.1 Example 25 (Part 1)

In the example shown in Listing 10.11, the MESH and DAWWG cards specify
a cylindrical geometry with diameter and length of 20 cm.

Listing 10.11: example\_structured\_mesh\_generate\_2.mcnp.inp.txt

<!-- image -->

| 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   | 1 Generate a LNK3DNT rzt mesh w/ multiple materials   |
|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|
| c upper-inner                                         | c upper-inner                                         | c upper-inner                                         | c upper-inner                                         | c upper-inner                                         | c upper-inner                                         | c upper-inner                                         | c upper-inner                                         | c upper-inner                                         | c upper-inner                                         | c upper-inner                                         | c upper-inner                                         | c upper-inner                                         |
| 1                                                     | 1                                                     | -18.7                                                 |                                                       |                                                       | -11                                                   | 1                                                     | 2                                                     | 3 imp:n=1                                             | 3                                                     |                                                       |                                                       |                                                       |
| 2                                                     | 2                                                     | -0.001                                                |                                                       |                                                       | -11                                                   | 1                                                     | -2                                                    | 3 imp:n=1                                             | 4                                                     |                                                       |                                                       |                                                       |
| 3                                                     | 1                                                     | -18.7                                                 |                                                       |                                                       | -11                                                   | -1                                                    | -2                                                    | 3 imp:n=1                                             | 5                                                     |                                                       |                                                       |                                                       |
| 4                                                     | 2                                                     | -0.001                                                |                                                       | -11                                                   |                                                       | -1                                                    | 2                                                     | 3 imp:n=1                                             | 6                                                     |                                                       |                                                       |                                                       |
| c upper-outer                                         | c upper-outer                                         | c upper-outer                                         | c upper-outer                                         | c upper-outer                                         | c upper-outer                                         | c upper-outer                                         | c upper-outer                                         | c upper-outer                                         | c upper-outer                                         | c upper-outer                                         | c upper-outer                                         | c upper-outer                                         |
| 6                                                     | 2                                                     | -0.001                                                |                                                       | -10                                                   | 11                                                    | 1                                                     | 2                                                     | 3 imp:n=1                                             | 8                                                     |                                                       |                                                       |                                                       |
| 7                                                     | 1                                                     | -18.7                                                 |                                                       | -10                                                   | 11                                                    | 1                                                     | -2 3                                                  | imp:n=1                                               | 9                                                     |                                                       |                                                       |                                                       |
| 8                                                     | 2                                                     | -0.001                                                |                                                       | -10                                                   | 11                                                    | -1                                                    | -2 3                                                  | imp:n=1                                               |                                                       |                                                       |                                                       |                                                       |
| 9                                                     | 1                                                     | -18.7                                                 |                                                       | -10 11                                                |                                                       | -1                                                    | 2                                                     | imp:n=1                                               |                                                       |                                                       |                                                       |                                                       |
| 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       | 3 c lower-inner                                       |
| 11                                                    | 2                                                     |                                                       |                                                       | -11                                                   | 1                                                     |                                                       | 2 -3                                                  | imp:n=1                                               | -0.001                                                |                                                       |                                                       |                                                       |
| 12                                                    | 1                                                     |                                                       |                                                       | -11                                                   | 1                                                     |                                                       | -3                                                    | imp:n=1                                               | -18.7                                                 |                                                       |                                                       |                                                       |
| 13                                                    | 2                                                     | -0.001                                                |                                                       | -11                                                   | -1                                                    | -2 -2                                                 | -3                                                    | imp:n=1                                               |                                                       |                                                       |                                                       |                                                       |
| 14                                                    | 1                                                     | -18.7                                                 |                                                       | -11                                                   | -1                                                    | 2                                                     |                                                       | imp:n=1                                               |                                                       |                                                       |                                                       |                                                       |
| -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      | -3 c lower-outer                                      |
| 16                                                    | 1                                                     | -18.7                                                 |                                                       | -10 11                                                |                                                       | 1                                                     | -3                                                    | imp:n=1                                               |                                                       |                                                       |                                                       |                                                       |
| 17                                                    | 2                                                     |                                                       |                                                       | -10                                                   | 11                                                    | 2 1 -2                                                | -3                                                    | imp:n=1                                               | -0.001                                                |                                                       |                                                       |                                                       |
| 18                                                    | 1                                                     | -18.7                                                 |                                                       | -10                                                   | 11 -1                                                 | -2                                                    | imp:n=1                                               | -3                                                    |                                                       |                                                       |                                                       |                                                       |
| 19                                                    |                                                       | -0.001                                                |                                                       | -10 11                                                | -1                                                    | 2                                                     | -3                                                    | imp:n=1                                               | 2                                                     |                                                       |                                                       |                                                       |
| c                                                     | c                                                     | c                                                     | c                                                     | c                                                     | c                                                     | c                                                     | c                                                     | c                                                     | c                                                     | c                                                     | c                                                     | c                                                     |
| c outer void                                          | c outer void                                          | c outer void                                          | c outer void                                          | c outer void                                          | c outer void                                          | c outer void                                          | c outer void                                          | c outer void                                          | c outer void                                          | c outer void                                          | c outer void                                          | c outer void                                          |
| 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       | 20 0 10 imp:n=0                                       |
| 10                                                    | rcc                                                   | 0.                                                    | 0.                                                    | -10.                                                  | 0.                                                    | 0.                                                    | 10.                                                   | $ outer                                               | 20.                                                   |                                                       |                                                       |                                                       |
| 11                                                    |                                                       | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 20                                                    | 5                                                     | $ inner                                               | rcc -10                                               |                                                       |                                                       |                                                       |
| 1                                                     |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       | py 0.0                                                |                                                       |                                                       |                                                       |
| 2                                                     | px                                                    |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       | 0.0                                                   |                                                       |                                                       |                                                       |
| 3                                                     | pz                                                    |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       | 0.0                                                   |                                                       |                                                       |                                                       |
| kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 | kcode 5000 1.0 50 250                                 |
| ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      | ksrc 0.0 0.0 0.0                                      |
| m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       | m1 92235.69c 1.0 m2 6012 1.0 dm1 92235 92235.50       |
| mesh                                                  | ref                                                   | geom cyl                                              |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       | 0.0 0.0 0.0                                           |                                                       |                                                       |                                                       |
| origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        | origin 0.0 0.0 -10.0 bottom center of cylinder        |
| axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       | axs 0.0 0.0 1.0                                       |
|                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       | $                                                     |                                                       |                                                       |                                                       |                                                       |                                                       |
|                                                       | vec                                                   |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       | 1.0 0.0 0.0                                           |                                                       |                                                       |                                                       |
| imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            | imesh 10 $ cylinder radius                            |
|                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       | iints 2 $ 2 radial divisions                          |                                                       |                                                       |                                                       |

```
44 jmesh 20 $ axial (z) length 45 jints 2 $ 2 axial divisions 46 kmesh 1 $ azimuth-single rotation (0-2pi) 47 kints 4 $ 4 azimuthal divisions (0, pi/2, pi, 3pi/2, 2pi) 48 dawwg xsec=ndilib points=10
```

The cylinder mesh has two radial, two axial, and four azimuthal
divisions, creating a total of eight mesh elements. The materials in
each of the elements alternate, creating a checkerboard-like pattern
throughout the cylinder. The use of the MESH keywords ORIGIN , AXS , and
VEC ensure that the mesh aligns with the geometry-the bottom center of
the mesh at (0 , 0 , -10) , the cylinder oriented along the z axis, and
the azimuthal plane along the positive x axis. To create the LNK3DNT
file, run MCNP6 with the M execution-line option using Listing 10.11 as
the MCNP6 input and assign the LINKOUT file the arbitrary name
cyl.linkout .

## 10.1.4.2 Example 25 (Part 2)

Now we embed the mesh geometry into the MCNP6 input in Listing 10.12
using inferred geometry cells (one for each material in the cyl.linkout
file) and one inferred background cell.

```
1 RZT Test of checkerboard cylinder with lnk3dnt 2 11 3 -18.7 0 u=e10 imp:n=1 $ inferred geometry cell 3 12 4 -0.001 0 u=e10 imp:n=1 $ inferred geometry cell 4 13 0 0 u=e10 imp:n=1 $ inferred background cell 5 20 0 -1 fill=e10 imp:n=1 $ embedded mesh fill cell 6 99 0 1 imp:n=0 $ outside world 7 8 1 so 20 9 10 kcode 500 1.0 50 100 11 ksrc 1 1 5 1 -1 5 -1 -1 5 -1 1 5 12 5 5 5 5 -5 5 -5 -5 5 -5 5 5 13 1 1 -5 1 -1 -5 -1 -1 -5 -1 1 -5 14 5 5 -5 5 -5 -5 -5 -5 -5 -5 5 -5 15 m3 92235.69c 1.0 16 m4 6012 1.0 17 dm1 92235 92235.50 18 embed10 meshgeo=lnk3dnt mgeoin=cyl.linkout debug=echomesh 19 matcell= 1 11 2 12 20 background=13
```

Listing 10.12: example\_structured\_mesh\_read\_2.mcnp.inp.txt

Note that inferred geometry cell 11 maps to mesh material 1, inferred
geometry cell 12 maps to mesh material 2, and the inferred background
cell 13 completes the embedded mesh universe by defining the space
surrounding the mesh. The embedded mesh universe then fills cell 20 of
the MCNP6 model. Recall that the ' e ' is optional for the U and FILL
keywords to denote an embedded mesh.

Figure 10.39 shows two views of the resulting geometry with the embedded
geometry shaded by material, which in this case alternates between
geometry elements.

## 10.1.4.3 Example 25 (Part 3)

Now let's assume we want two copies of this mesh geometry embedded into
our MCNP6 model, each having a different placement and orientation. We
need to rotate/translate the two mesh geometry universes appropriately
as we fill two distinct MCNP6 cells.
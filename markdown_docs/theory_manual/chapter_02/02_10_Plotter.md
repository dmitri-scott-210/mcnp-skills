---
title: "Chapter 2.10 - Plotter"
chapter: "2.10"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/2_Geometry,_Data,_Physics,_and_Mathematics/2.10_Plotter.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

When applied to the calculation of arbitrary volumes, the function that
defines the volume may not be known. Thus, selecting an effective
biasing function can be difficult. However, as described in §5.5.1.1,
using an inwardly directed spherical source with a biased cosine
distribution is considered the best source setup [179]. While a simple
inwardly directed spherical source with rays coming off the surface
tangent to the point they are born ( DIR = -1 ) may be used, some shapes
may benefit from sampling a non-tangent angle which allows more of the
unknown volume to be interrogated. Higher track lengths are important to
reduce variance in the calculation of this volume. The WGT entry on the
SDEF card should be πr 2 , where r is the radius of the sphere, to
account for the spherical surface area that defines the source. This is
similar to multiplying the area of the bounding box in the naive example
described previously.

## 2.10 Plotter

The MCNP plotter draws cross-sectional views of the problem geometry
according to commands entered by the user. See Chapter 6 for the command
vocabulary and examples of use. The pictures can be drawn on the screen
of a terminal or to a postscript file as directed by the user. The
pictures are drawn in a square viewport on the graphics device. The
mapping between the viewport and the portion of the problem space to be
plotted, called the window, is user-defined. A plane in problem space,
the plot plane, is defined by specifying an origin r 0 and two
perpendicular basis vectors a and b . The size of the window in the plot
plane is defined by specifying two extents. The picture appears in the
viewport with the origin at the center, the first basis vector pointing
to the right and the second basis vector pointing up. The width of the
picture is twice the first extent and the height is twice the second
extent. If the extents are unequal, the picture is distorted. The
central task of the plotter is to plot curves representing the
intersections of the surfaces of the geometry with the plot plane within
the window.

All plotted curves are conics, defined here to include straight lines.
The intersection of a plane with any MCNP surface that is not a torus is
always a conic. A torus is plotted only if the plot plane contains the
torus axis or is perpendicular to it, in which case the intersection
curves are conics. The first step in plotting the curves is to find
equations for them, starting from the equations for the surfaces of the
problem. Equations are needed in two forms for each curve: a quadratic
equation and a pair of parametric equations. The quadratic equations are
needed to solve for the intersections of the curves. The parametric
equations are needed for defining the points on the portions of the
curves that are actually plotted.

The equation of a conic is

<!-- formula-not-decoded -->

where s and t are coordinates in the plot plane. They are related to
problem coordinates ( x, y, z ) by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

or in matrix form

Table 2.11: Useful Conic Parametric Equations

| Type          | Variable   |     | Equation                                                    |
|---------------|------------|-----|-------------------------------------------------------------|
| Straight Line | s t        | = = | C 1 + C 2 p C 4 + C 5 p                                     |
| Parabola      | s t        | = = | C 1 + C 2 p + C 3 p 2 C 4 + C 5 p + C 6 p 2                 |
| Ellipse       | s t        | = = | C 1 + C 2 sin p + C 3 cos p C 4 + C 5 sin p + C 6 cos p     |
| Hyperbola     | s t        | = = | C 1 + C 2 sinh p + C 3 cosh p C 4 + C 5 sinh p + C 6 cosh p |

In matrix form the conic equation is

<!-- formula-not-decoded -->

Thus, finding the equation of a curve to be plotted is a matter of
finding the QM matrix, given the PL matrix and the coefficients of the
surface.

<!-- formula-not-decoded -->

Any surface in the MCNP code, except for tori, can be readily written as

<!-- formula-not-decoded -->

or in matrix form as

<!-- formula-not-decoded -->

The transpose of the transformation between ( s, t ) and ( x, y, z ) is

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where PL T is the transpose of the PL matrix. Substitution in the
surface equation gives

Therefore, QM = PL T AMPL .

<!-- formula-not-decoded -->

A convenient set of parametric equations for conics is given in Table
2.11.

The type of a conic is determined by examination of the conic invariants
[180], which are simple functions of the elements of QM . Some of the
surfaces produce two curves, such as the two branches of a hyperbola or
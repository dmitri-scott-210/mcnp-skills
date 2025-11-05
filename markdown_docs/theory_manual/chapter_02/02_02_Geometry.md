---
title: "Chapter 2.2 - Geometry"
chapter: "2.2"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/2_Geometry,_Data,_Physics,_and_Mathematics/2.2_Geometry.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

the free gas thermal treatment, generates and banks any photons, handles
analog capture or capture by weight reduction, plays the weight cutoff
game, and handles S ( α, β ) thermal collisions and elastic or inelastic
scattering. For criticality problems, fission sites are stored for
subsequent generations. Any additional tracks generated in the collision
are put in the bank. The energies and directions of particles exiting
the collision are determined. Multigroup and multigroup/adjoint
collisions are treated separately. The collision process and thermal
treatments are described in more detail in §2.4.3.1.

The collision analysis for photons is similar to that for neutrons, but
includes either the simple or the detailed physics treatments. See
§5.7.2.3 for a discussion of turning photonuclear physics on. The simple
physics treatment is valid only for photon interactions with free
electrons, i.e. it does not account for electron binding effects when
sampling emission distributions; the detailed treatment is the default
and includes form factors and Compton profiles for electron binding
effects, coherent (Thomson) scatter, and fluorescence from photoelectric
capture [§2.4.4]. There may also be photonuclear physics (if
photonuclear physics is in use). Additionally, photonuclear biasing is
available (similar to forced collisions) to split the photon (updating
the weight by the interaction probabilities) and force one part to
undergo a photoatomic collision and the second part to undergo a
photonuclear collision. The collision analysis samples for the collision
nuclide, treats photonuclear collisions, treats photoelectric
absorption, or capture (with fluorescence in the detailed physics
treatment), incoherent (Compton) scatter (with Compton profiles and
incoherent scattering factors in the detailed physics treatment to
account for electron binding), coherent (Thomson) scatter for the
detailed physics treatment only (again with form factors), and pair
production. Secondary particles from photonuclear collisions (either
photons or neutrons) are sampled using the same routines as for
inelastic neutron collisions [§2.4.3.5]. Electrons are generated for
incoherent scatter, pair production, and photoelectric absorption. These
electrons may be assumed to deposit all their energy instantly if ides =
1 on the PHYS : p card, or they may produce electrons with the thick-
target bremsstrahlung approximation (default for MODE p problems, ides =
0 on the PHYS : p card), or they may undergo full electron transport
(default for MODE p e problems, ides = 0 on the PHYS : p card.)
Multigroup or multigroup/adjoint photons are treated separately.

After the surface crossing or collision is processed, transport
continues by calculating the distance to cell boundary, and so on. Or if
the particle involved in the collision was killed by capture or variance
reduction, the bank is checked for any remaining progeny, and if none
exists, the history is terminated. Appropriate summary information is
incremented, the tallies of this particular history are added to the
total tally data, the history is terminated, and a return is made.

After each history, several checks are made to see if other actions need
to be performed before additional histories can be run. For
continuation, the subroutine is called again. Otherwise a return is made
and the summary information and tally data are printed.

## 2.2 Geometry

The basic MCNP geometry concepts, discussed in Chapter 1, include the
sense of a cell, the intersection and union operators, and surface
specification. Covered in this section are the complement operator; the
repeated structure capability; an explanation of two surfaces, the cone
and the torus; and a description of ambiguity, reflecting, white, and
periodic boundary surfaces.

## 2.2.1 Complement Operator

The complement operator provides no new capability over the intersection
and union operators. It is just a shorthand cell-specifying method that
implicitly uses the intersection and union operators.

The complement operator is the # symbol. The complement operator can be
thought of as standing for not in. There are two basic uses of the
operator:

1

Figure 2.1: Illustration of poor use of complement operator.

<!-- image -->

1. # n means that the description of the current cell is the complement of the description of cell n .
2. #(. . . ) means complement the portion of the cell description in the parentheses (usually just a list of surfaces describing another cell).

In the first of the two above forms, the MCNP code performs five
operations: (1) the symbol # is removed, (2) parentheses are placed
around n , (3) any intersections in n become unions, (4) any unions in n
are replaced by back-to-back parentheses, ')(', which is an
intersection, and (5) the senses of the surfaces defining n are
reversed.

A simple example is a cube. We define a two-cell geometry with six
surfaces, where cell 1 is the cube and cell 2 is the outside world:

```
1 1 0 -1 2 -3 4 -5 6 2 2 0 1:-2: 3:-4: 5:-6
```

Note that cell 2 is everything in the universe that is not in cell 1, or

```
1 2 0 #1
```

The form #( n) is not allowed; it is functionally available as the
equivalent of -n .

## /warning\_sign Caution

Using the complement operator can destroy some of the necessary
conditions for some cell volume and surface area calculations by the
MCNP code. See §10.1.1.14 for an example.

The complement operator can be easily abused if it is used
indiscriminately. A simple example can best illustrate the problems.
Figure 2.1 consists of two concentric spheres inside a box. Cell 4 can
be described using the complement operator as

4 0 #3 #2 #1

Although cells 1 and 2 do not touch cell 4, to omit them would be
incorrect. If they were omitted, the description of cell 4 would be
everything in the universe that is not in cell 3. Since cells 1 and 2
are not part of cell 3, they would be included in cell 4. Even though
surfaces 1 and 2 do not physically bound cell 4, using the complement
operator as in this example causes the MCNP code to think that all
surfaces involved with the complement do bound the cell. Even though
this specification is correct and required by the MCNP code, the
disadvantage is that when a particle enters cell 4 or has a collision in
cell 4, the MCNP code must calculate the intersection of the particle's
trajectory with all real bounding surfaces of cell 4 plus any extraneous
ones brought in by the complement operator. This intersection
calculation is very expensive and can add significantly to the required
computer time.

A better description of cell 4 would be to complement the description of
cell 3 (omitting surface 2) by reversing the senses and interchanging
union and intersection operators as illustrated in the cell cards that
describe the simple cube in the preceding paragraphs.

## 2.2.2 Repeated Structure Geometry

The repeated structure geometry feature is explained in detail starting
on §5.5.5. The capabilities are only introduced here. Examples are shown
in Chapter 10. The cards associated with the repeated structure feature
are U (universe), FILL , TRCL , URAN , and LAT (lattice) and cell cards
with LIKE m BUT.

The repeated structure feature makes it possible to describe only once
the cells and surfaces of any structure that appears more than once in a
geometry. This unit then can be replicated at other locations by using
the 'LIKE m BUT' construct on a cell card. The user specifies that a
cell is filled with something called a universe. The U card identifies
the universe, if any, to which a cell belongs. The FILL card specifies
with which universe a cell is to be filled. A universe is either a
lattice or an arbitrary collection of cells. The two types of lattice
shapes, hexagonal prisms and hexahedra, need not be rectangular nor
regular, but they must fill space exactly. Several concepts and cards
combine in order to use this capability.

## 2.2.3 Surfaces

## 2.2.3.1 Explanation of Cone and Torus

Two surfaces, the cone and torus, require more explanation. The
quadratic equation for a cone describes a cone of two sheets (just like
a hyperboloid of two sheets): one sheet is a cone of positive slope, and
the other has a negative slope. A cell whose description contains a two-
sheeted cone may require an ambiguity surface to distinguish between the
two sheets. The MCNP code provides the option to select either of the
two sheets; this option frequently simplifies geometry setups and
eliminates any ambiguity. The +1 or the -1 entry on the cone surface
card causes the one sheet cone treatment to be used. If the sign of the
entry is positive, the specified sheet is the one that extends to
infinity in the positive direction of the coordinate axis to which the
cone axis is parallel. The converse is true for a negative entry. This
feature is available only for cones whose axes are parallel to the
coordinate axes of the problem.

The treatment of fourth degree surfaces in Monte Carlo calculations has
always been difficult because of the resulting fourth order polynomial
('quartic') equations. These equations must be solved to find the
intersection of a particle's line of flight with a toroidal surface. In
the MCNP code these equations must also be solved to find the
intersection of surfaces in order to compute the volumes and surface
areas of geometric regions of a given problem. In either case, the
quartic equation,

<!-- formula-not-decoded -->

is difficult to solve on a computer because of roundoff errors. For many
years the MCNP toroidal treatment required 30 decimal digits (CDC
double-precision) accuracy to solve quartic equations. Even then there
were

Figure 2.2: Cell demonstrating two different senses.

<!-- image -->

round-off errors that had to be corrected by Newton-Raphson iterations.
Schemes using a single-precision quartic formula solver followed by a
Newton-Raphson iteration were inadequate because if the initial guess of
roots supplied to the Newton-Raphson iteration is too inaccurate, the
iteration will often diverge when the roots are close together.

The single-precision quartic algorithm in the MCNP code basically
follows the quartic solution of Cashwell and Everett [43]. When roots of
the quartic equation are well separated, a modified Newton-Raphson
iteration quickly achieves convergence. But the key to this method is
that if the roots are double roots or very close together, they are
simply thrown out because a double root corresponds to a particle's
trajectory being tangent to a toroidal surface, and it is a very good
approximation to assume that the particle then has no contact with the
toroidal surface. In extraordinarily rare cases where this is not a good
assumption, the particle would become 'lost.' Additional refinements to
the quartic solver include a carefully selected finite size of zero, the
use of a cubic rather than a quartic equation solver whenever a particle
is transported from the surface of a torus, and a gross quartic
coefficient check to ascertain the existence of any real positive roots.
As a result, the single-precision quartic solver is substantially faster
than double-precision schemes, portable, and also somewhat more
accurate.

In the MCNP code, elliptical tori symmetric about any axis parallel to a
coordinate axis may be specified. The volume and surface area of various
tallying segments of a torus usually will be calculated automatically.

## 2.2.3.2 Ambiguity Surfaces

The description of the geometry of a cell must eliminate any ambiguities
as to which region of space is included in the cell. That is, a particle
entering a cell should be able to determine uniquely which cell it is in
from the senses of the bounding surfaces. This is not possible in a
geometry such as shown in Figure 2.2 unless an ambiguity surface is
specified. Suppose the figure is rotationally symmetric about the y
-axis.

A particle entering cell 2 from the inner spherical region might think
it was entering cell 1 because a test of the senses of its coordinates
would satisfy the description of cell 1 as well as that of cell 2. In
such cases, an ambiguity surface is introduced such as plane a . An
ambiguity surface need not be a bounding surface of a cell, but it may
be and frequently is. It can also be the bounding surface of some cell
other than the one in question. However, the surface must be listed
among those in the problem and must not be a reflecting surface
[§2.2.3.3]. The description of cells 1 and 2 in Figure 2.2 is augmented
by listing for each its sense relative to surface a as well as that of
each of its other bounding surfaces. A particle in cell 1 cannot have
the same sense relative to surface a as does a particle in cell 2. More
than one ambiguity surface may be required to define a particular cell.

A second example may help to clarify the significance of ambiguity
surfaces. We would like to describe the geometry of Figure 2.3a. Without
the use of an ambiguity surface, the result will be Figure 2.3b.
Surfaces 1 and 3 are spheres about the origin, and surface 2 is a
cylinder around the y -axis. Cell 1 is both the center and outside world
of the geometry connected by the region interior to surface 2.

Figure 2.3: Example geometry demonstrating ambiguity surface.

<!-- image -->

At first glance it may appear that cell 1 can easily be specified by -1
: -2 : 3 whereas cell 2 is simply #1. This results in Figure 2.3b, in
which cell 1 is everything in the universe interior to surface 1 plus
everything in the universe interior to surface 2 (remember the cylinder
goes to plus and minus infinity) plus everything in the universe
exterior to surface 3.

An ambiguity surface (plane 4 at y = 0 ) will solve the problem.
Everything in the universe to the right of the ambiguity surface
intersected with everything in the universe interior to the cylinder is
a cylindrical region that goes to plus infinity but terminates at y = 0
. Therefore, -1 : (4 -2) : 3 defines cell 1 as desired in Figure 2.3a.
The parentheses in this last expression are not required because
intersections are done before unions. Another expression for cell 2
rather than #1 is 1 -3 #(4 -2).

For the user, ambiguity surfaces are specified the same way as any other
surface-simply list the signed surface number as an entry on the cell
card. For the MCNP code, if a particular ambiguity surface appears on
cell cards with only one sense, it is treated as a true ambiguity
surface. Otherwise, it still functions as an ambiguity surface but the
TRACK subroutine will try to find intersections with it, thereby using a
little more computer time.

## 2.2.3.3 Reflecting Surfaces

A surface can be designated a reflecting surface by preceding its number
on the surface card with an asterisk. Any particle hitting a reflecting
surface is specularly (mirror) reflected. Reflecting planes are valuable
because they can simplify a geometry setup (and also tracking) in a
problem. They can, however, make it difficult (or even impossible) to
get the correct answer. The user is cautioned to check the source weight
and tallies to ensure that the desired result is achieved. Any tally in
a problem with reflecting planes should have the same expected result as
the tally in the same problem without reflecting planes.

## /warning\_sign Caution

Point detectors or DXTRAN regions used with reflecting surfaces give
wrong answers [§2.5.6.4.2].

The following example illustrates the above points and should make MCNP
users very cautious in the use of reflecting surfaces. Reflecting
surfaces should never be used in any situation without a lot of thought.

Consider a cube of carbon 10 cm on a side sitting on top of a 5-MeV
neutron source distributed uniformly in volume. The source cell is a
1-cm-thick void completely covering the bottom of the carbon cube and no

1

2

3

4

5

more. The average neutron flux across any one of the sides (but not top
or bottom) is calculated to be 0.150 ( ± 0.5%) per cm 2 per starting
neutron from an MCNP F2 tally, and the flux at a point at the center of
the same side is 1 . 55 × 10 -03 n/cm 2 ( ± 1%) from an MCNP F5 tally.
The cube can be modeled by half a cube and a reflecting surface. All
dimensions remain the same except the distance from the tally surface to
the opposite surface (which becomes the reflecting surface) is 5 cm. The
source cell is cut in half also. Without any source normalization, the
flux across the surface is now 0.302 ( ± 0.5%), which is twice the flux
in the nonreflecting geometry. The detector flux is 2 . 58 × 10 -03 ( ±
1%), which is less than twice the point detector flux in the
nonreflecting problem.

The problem is that for the surface tally to be correct, the starting
weight of the source particles has to be normalized; it should be half
the weight of the non-reflected source particles. The detector results
will always be wrong (and lower) for the reason discussed in §2.5.6.4.2.

In this particular example, the normalization factor for the starting
weight of source particles should be 0.5 because the source volume is
half of the original volume. Without the normalization, the full weight
of source particles is started in only half the volume. These
normalization factors are problem dependent and should be derived very
carefully.

Another way to view this problem is that the tally surface has doubled
because of the reflecting surface; two scores are being made across the
tally surface when one is made across each of two opposite surfaces in
the nonreflecting problem. The detector has doubled too, except that the
contributions to it from beyond the reflecting surface are not being
made [§2.5.6.4.2].

## 2.2.3.4 White Boundaries

A surface can be designated a white boundary surface by preceding its
number on the surface card with a plus. A particle hitting a white
boundary is reflected with a cosine distribution, p ( µ ) = µ , relative
to the surface normal; that is, µ = √ ξ , where ξ is a random number.
White boundary surfaces are useful for comparing MCNP results with other
codes that have white boundary conditions. They also can be used to
approximate a boundary with an infinite scatterer. They make no sense in
problems with next-event estimators such as detectors or DXTRAN
[§2.5.6.4.2] and should always be used with caution.

## 2.2.3.5 Periodic Boundaries

Periodic boundary conditions can be applied to pairs of planes to
simulate an infinite lattice. Although the same effect can be achieved
with an infinite lattice, the periodic boundary is easier to use,
simplifies comparison with other codes having periodic boundaries, and
can save considerable computation time. There is approximately a 55%
run-time penalty associated with repeated structures and lattices that
can be avoided with periodic boundaries. However, collisions and other
aspects of the Monte Carlo random walk usually dominate running time, so
the savings realized by using periodic boundaries are usually much
smaller. A simple periodic boundary problem is illustrated in Figure
2.4.

It consists of a square reactor lattice infinite in the z direction and
4 cm on a side in the x and y directions with an off-center 0.5 cm
radius cylindrical fuel pin. The MCNP surface cards are given in Listing
2.1.

Listing 2.1: periodic\_boundary.mcnp.inp.txt

| 1 -2 px   | -2            |
|-----------|---------------|
| 2 -1 px   | 2             |
| 3 -4 py   | -2            |
| 4 -3 py   | 2             |
| 5 c/z     | 0.75 0.75 0.5 |
---
title: "Chapter 5.1 - Geometry Specification Card Introduction"
chapter: "5.1"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.1_Geometry_Specification_Card_Introduction.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Chapter 5

## Input Cards

The MCNP input file contains entries that are commonly referred to as
cards. Cards are usually structured to take a list of numbers or
keyword-value pairs. This chapter describes each of the MCNP6 input
cards. The overall file format is discussed in Chapter 4.

## 5.1 Geometry Specification Card Introduction

The geometry of MCNP6 treats an arbitrary three-dimensional
configuration of user-defined materials in geometric cells bounded by
first- and second-degree surfaces and fourth-degree elliptical tori. See
Table 5.1. The cells are defined by the intersections, unions, and
complements of the regions bounded by the surfaces. Surfaces are defined
by supplying coefficients to the analytic surface equations or, for
certain types of surfaces, known points on the surfaces. MCNP6 also
provides a 'macrobody' capability, where basic shapes such as spheres,
boxes, cylinders, etc., may be combined using Boolean operators.

Each surface divides all space into two regions, one with positive sense
with respect to the surface and the other with negative sense. Define S
= f ( x, y, z ) = 0 as the equation of a surface in the problem. For any
set of points ( x, y, z ) if S = 0 , the points are on the surface; if S
is negative, the points are said to have a negative sense with respect
to that surface, and if S is positive, the points have a positive sense.
The expression for a surface is the left side of the equation for the
surface in Table 5.1. For the sphere, cylinder, cone, and torus, this
definition is identical to defining the sense to be positive outside the
figure. With planes normal to axes ( PX , PY , or PZ ), the definition
gives positive sense for points with x , y , or z values exceeding the
intercept of the plane. For the P , SQ , and GQ surfaces, the user
supplies all of the coefficients for the expression and thus can
determine the sense of the surface at will. This is different from the
other cases where the sense, though arbitrary, is uniquely determined by
the form of the expression. Therefore, in a surface transformation (see
the TR n card) a PX , PY , or PZ surface will sometimes be replaced by a
P surface just to prevent the sense of the surface from getting
reversed.

The geometry of each cell is described on a cell card by a list of
operators and signed surfaces that bound the cell. If the sense is
positive, the '+' sign can be omitted. This geometry description defines
the cell to be the intersection, union, and/or complement of the listed
regions. The intersection operator in MCNP6 is implicit; it is simply
the blank space between two signed surface numbers on the cell card. The
union operator, signified by a colon ( : ), allows concave corners in
cells and also cells that are completely disjoint. Because the
intersection and union operators are binary Boolean operators, their use
follows Boolean algebra methodology; unions and intersections can be
used in combination in any cell description. Spaces on either side of
the union operator are irrelevant, but a space without the colon
signifies an intersection.

The complement operator, signified by the # symbol, provides no new
capability over the intersection and union operators. It is just a
shorthand cell-specifying method that implicitly uses the intersection
and union operators. The complement operator can be thought of as
standing for 'not in.' The notation # n , where n is a previously
defined cell number, means that the description of the current cell is
the complement of the
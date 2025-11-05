---
title: "Chapter 8 - Unstructured Mesh"
chapter: "8"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/8_Unstructured_Mesh.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## 8.1 Introduction

The MCNP code has a general geometry specification capability by using a
constructive solid geometry (CSG) approach. This approach consists of
using first- and second-order implicit surfaces (plane, sphere, etc.,)
and fourth-order elliptical tori with Boolean operations to define
regions of space [§1.3, §2.2]. This CSG capability has been well-tested
and verified. However, it has long been recognized that as the model
complexity increases, creating a CSG model is difficult, tedious, and
error prone [336-338]. Consequently, innovators have taken on the task
of developing a better way to construct geometries in the MCNP code. The
MCNP code addresses this issue by permitting the user to embed an
unstructured mesh (UM) representation of a geometry in its CSG cells to
create a hybrid geometry using universe ( U ) keywords on cell cards.
Particle tracking methods for CSG and UM models are different. The code
implementation for the MCNP UM input processing and particle tracking is
known as 'REGL,' which stands for Revised Extended Grid Library. This
library is also called the UM library in the MCNP manual.

The UM capability was originally designed to work with an unstructured
mesh created with the Abaqus/CAE [339] software and the ASCII input file
that it generates. Many other mesh generation tools have the ability to
generate a mesh from a solid model that can be exported as the Abaqus
input file format. It is the user's responsibility to verify that these
meshing tools are generating the Abaqus input file format that meets the
MCNP specification; see §8.7. In addition, the information in the Abaqus
input file can be converted to the MCNP code-friendly MCNPUM file type
(now deprecated, [DEP-53424]). Version 6.3 of the MCNP code introduces
the new capability of tracking particles on a UM model formatted as an
HDF5 file; the details of the HDF5 UM mesh format can be found in §D.6.

## 8.2 Terminology

The MCNP code can only process an Abaqus input file organized into parts
that are instanced into an assembly. An overview of an Abaqus input file
format is given in §8.7. Tracking particles on a UM geometry is a
combination of two fields: particle transport and finite element
analysis (FEA). One of the problems of merging two capabilities that
have long, independent development paths is dealing with the distinct
and sometimes contradictory terminology that has evolved with each. For
example, the term 'cell' is often used to generically denote the
smallest building block in a UM geometry. However, an MCNP cell is quite
different from a UM cell, which will be referred to as a 'finite
element'. Note that element, mesh, part, elset, instance, and assembly
terminology described in this section are used in FEA and Abaqus. The
purpose of this section is to introduce the terminology and more
information will be discussed later in this chapter. MCNP users who do
not have an FEA background should consult the information in §8.7.

elements (or finite elements)

The smallest building blocks into which the mesh geometry is broken.
Nodal data (i.e., node numbers and node coordinates) are used to define

## Chapter 8

## Unstructured Mesh

Figure 8.1: Finite element types (second-order elements with planar faces).

<!-- image -->

an element. The number of nodes per element depends on an element type.
The element types are unstructured polyhedra with 4, 5, or 6 sides or
faces, Fig. 8.1. First-order elements have nodes only at the vertices.
When a face has 4 nodes, all 4 nodes are not guaranteed to lie in the
same plane. This face has a degree of curvature and is known as
bilinear. Thus, first-order elements may have either planar or bilinear
faces. First-order elements with bilinear faces have trilinear volumes.

Second-order elements have nodes at the vertices and at the midpoints
between the vertices. When 4 or more nodes define a face, they are not
guaranteed to lie in the same plane. With 6 or 8 nodes defining a face,
the degree of curvature can be greater than with 4 nodes and the faces
are known as biquadratic. Thus, second-order elements may have either
planar, bilinear, or biquadratic faces. Second-order elements with
biquadratic faces have triquadratic volumes.

| mesh     | The collection of elements comprising the entire model. The mesh geometry can be structured or unstructured and is a representation of the geometry described by the solid model.                                                                                                                                                                                                                                            |
|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| part     | A part is defined by a collection of elements and nodes. In an Abaqus input file, it is possible to further subdivide a part into multiple sets of elements. This is done by grouping the elements in a part into sets where each element set is assigned a different name.                                                                                                                                                  |
| elsets   | Elsets is short for element sets. An elset is a collection of elements that is associated with a specific tag, label, or name. The MCNP code requires that each part in an Abaqus input file must have an elset with 'material' and 'statistic' in its name. These elsets are referred to as a 'material elsets' or 'statistic elsets', respectively. This term is only used for a UM model defined in an Abaqus input file. |
| instance | An instance is a copy of a part used in constructing an assembly. Thus, each part may be used multiple times, giving rise to multiple instances of that part. This term is only used for a UM model defined in an Abaqus input file.                                                                                                                                                                                         |

<!-- image -->

Figure 8.2: Constructing an assembly from parts.

| assembly        | An assembly consists of one or more instances. It can be viewed as a composite object. From this assembly, the MCNP code will create a global mesh model. This term is only defined for a UM model defined in an Abaqus input file.                                                                                                                                                                                                                                                                                                                                                         |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pseudo-cell     | In the MCNP input file, a pseudo-cell is a specialized cell definition, defined with a null or zero surface, that is used to associate normal MCNP cell features with the set of elements placed in the cell (e.g., a cell for an F4 tally). The MCNP code uses instances and associated parts in an Abaqus input file to construct pseudo-cells. The elsets with distinct statistic elset names in the part are used to form the pseudo-cells when each part is instanced to form an assembly. For an HDF5 mesh input file, a pseudo-cell is created from a cell group.                    |
| background cell | An MCNP cell defined with a null surface. It serves as the background medium into which the UM model is placed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| mesh universe   | This is the MCNP universe composed of the UM geometry (i.e., pseudo- cells) and the background cell. This universe may not contain any other lower universes or cells. The UM geometry must not be clipped by the boundaries of the fill cell that define this universe. This clipping requirement is not enforced by the code at this point, but is the user's responsibility to ensure that it doesn't occur. If clipping does occur, the user will experience lost particles in these regions of phase space. Particle tracking takes place on the pseudo-cells and the background cell. |

## 8.3 Constructing an Unstructured Mesh Geometry

The MCNP UM calculations require two input file types: an MCNP input
file and one or more UM geometry input files. The MCNP code can process
a UM model formatted as either an Abaqus input file, or an HDF5 mesh
input file. This section focuses on how to create a UM model formatted
as an Abaqus input file. The first step in creating a UM model for use
in the MCNP code is to create a part or series of parts. Each part can
consist of a single element set of one homogeneous material or multiple
element sets of different homogeneous materials. Once each part is
created and meshed, element sets must be assigned in a part. The parts
are then instanced to form an assembly, Fig. 8.2. The final step is to
define material names. Other mesh generation tools may promote a
different workflow, but the resulting file ultimately must meet the MCNP
mesh format requirements. See §8.7 for more information on an Abaqus
input file format.

## /warning\_sign Caution

The mesh geometry input files used on the EMBED card must have a
filename that is all lowercase.

## 8.3.1 Naming Elsets and Materials

## 8.3.1.1 Elset Naming Guidance

The MCNP code requires that each part must has one or more elset keyword
lines; see §8.7.2.4. Each elset in a part must be tagged with a name.
The MCNP code requires the elset name to be in a specific format:

## ???AAA???%ZZZ

where:

| AAA   | Is one of the keywords: material , statistic , tally , source ( 1 ).                                             |
|-------|------------------------------------------------------------------------------------------------------------------|
| ZZZ   | The set number following an underscore, '_', or a hyphen, '-', and ZZZ can be from 1 to 12 digits in length.     |
| ???   | Any other characters or strings that may be used to describe the set, but should NOT repeat any of the keywords. |
| %     | Indicates either a hyphen or an underscore.                                                                      |

## Details:

- 1 The keywords statistic and tally are interchangeable; use one or the other, but not both to describe the elset in a part.

If a part is made up of more than one elset, the ZZZ number must be
unique within the part. The ZZZ number must be unique within the
assembly for the material elsets and material names in order for the
legacy EEOUT file [DEP-53294] to be fully functional with auxiliary
programs such as GMV [228]. This material elset number is assigned
internally to the elements by the MCNP code and is output in the EEOUT
file [§D.7] for each element. For best results, the user should make
each ZZZ of the material element sets to be the same material number
that appears on the MCNP material card.

As a convenience, it is possible to construct one elset that has
multiple functions by specifying more than one keyword in the elset
name. The naming format is:

## ???AAA???%???BBB???%???CCC???%ZZZ

where AAA , BBB , and CCC are the keywords defined above. Examples of
legal elset names are material-tally001, material\_statistic\_source\_002,
material\_001, or statistic\_001. Examples of illegal elset names are
material\_tally\_statistic\_001 or HEU-5.

In each part, the material and statistic (or tally ) elset keywords are
required, and the number of statistic elsets must be greater than or
equal to the number of material elsets. The MCNP code will use the
statistic elset numbers in each part to construct the corresponding
pseudo-cells. If a part has only one statistic elset, then all elements
in the part are assigned into one pseudo-cell. If a part has two
statistic elsets and one material elset, then elements in this part are
divided into two pseudo-cells with the same material number. The MCNP
code checks that the number of statistic elsets must be greater or equal
to the number of material

elsets in each part. If this requirement is not met, a fatal error is
thrown. The intended use of the statistic (or tally ) keyword is to
collect individual elements in the elset into a pseudo-cell for the
purpose of volume tallies ( F4 , F6 , or F7 ). Basically, the elements
in the same statistic elset share the same cell-like properties; hence
coining of the term pseudo-cell.

## /warning\_sign Caution

The MCNP code requires its CSG cells to be associated with only one
material and this must be upheld through the UM pseudo-cells. The MCNP
code does not check the material and statistic elsets to ensure this
requirement. Thus it is user's responsibility to make sure that only one
material is assigned to each statistic elset.

All elements in each part must be assigned to material and statistic
elsets. If not, a fatal error will be thrown.

The source elset keyword is optional in each part. This keyword should
only be used to describe a volume source region in the UM model. The
MCNP code will sample the source starting position ( x , y , z )
uniformly over the elements associated with the volume source; multiple
volume sources are permitted, but see §5.8.1.3 on how to select among
various volume sources. That is, a source element is selected from the
source elset(s) with a probability proportional to the fractional volume
of the source element in the total source volume. The source coordinates
( x , y , z ) are uniformly selected by rejection sampling over the
selected element. No source biasing of position within a source elset
(or pseudo-cell) is permitted with this capability. All other, non-
positional fixed source ( SDEF ) options should work in conjunction with
this capability, but extensive testing has not been performed. Volume
source elsets may be defined but will not be used unless requested on
the SDEF card.

## 8.3.1.2 Material Naming Guidance

The material names are independently created and are placed outside the
assembly block near the end of the Abaqus input file. The material names
must have the following format

## ???%ZZZ

where ZZZ is a material number that corresponds to those numbers used in
the material elset and ??? are any other characters or strings, except
the keywords reserved for elset naming. The % indicates either a hyphen
or underscore. In other words, the material name can be a description
like 'BoronCarbide' followed by ZZZ ; a valid material number in the
MCNP input file.

Material names appear in the pseudo-cell cross reference table, which is
written to the MCNP output file after the MCNP code processes the mesh
description and creates the global tracking model. This table is
intended to help users understand how the pseudo-cells should be
specified. When searching for material names to insert into this table,
the code tries to match the material number for the pseudo-cell to the
material number in the material name. If that fails, the code assumes
that the material names have been entered sequentially from 1 to the
maximum number of material numbers and uses the pseudo-cell material
number to select one of these. If both of these rules fail to produce a
defined name, a message is inserted into the table to the effect that
the material name does not exist.

The material properties may be assigned within the material name block
in the Abaqus input file; however, the MCNP code does not use any
material property presented in the Abaqus input file for the MCNP
calculations. The isotopic (or mass) ratios are defined on a standard M
card in the MCNP input. Likewise, the material densities are defined in
the MCNP input on the pseudo-cells. The density information may be added
to an Abaqus input file when an Abaqus input file is preprocessed to
generate an MCNP UM input file.

Figure 8.3: Example mesh universe with unstructured mesh.

<!-- image -->

## 8.3.2 Pseudo-Cell Creation

The MCNP code uses instances and statistic element sets to define the
internal pseudo-cells. The pseudo-cells internally created by the code
are numbered consecutively starting at 1, in the order the parts are
instanced into the assembly. If part #2 is instanced ahead of part #1 in
the Abaqus input file and each part has only one statistic elset, then
an internal pseudo-cell #1 contains the elements in part #2 and an
internal pseudo-cell #2 contains the elements in part #1. If only one
part is instanced in an assembly and this part has 3 tally elsets
(tally-10, tally-3, and tally-5), then an internal pseudo-cell #1
contains the elements in the tally-3 elset, an internal pseudo-cell #2
contains the elements in the tally-5 elset, and an internal pseudo-cell
#3 contains the elements in tally-10 elsets. The internal pseudo-cells
are matched to the pseudo-cell numbers in an MCNP input by the MATCELL
keyword on the EMBED card, where the first and second entries of the
MATCELL keyword are respectively the internal pseudo-cell numbers
created from an Abaqus input file and the pseudo-cell numbers in an MCNP
input file. The internal pseudo-cells are also known as (unstructured)
mesh cells. The user should examine the pseudo-cell cross-reference
table in the MCNP output file to make sure that the global model built
by the MCNP code is the model that the user intends to study.

## 8.3.3 Mesh Universe

A simplified MCNP hybrid geometry arrangement with a UM geometry model
embedded in the CSG model (i.e., mesh universe) is shown in Fig. 8.3.
The mesh universe is everything contained within the fill cell where the
fill cell's outer boundary is the heavy black rectangle. Note, 'fill
cell' means the traditional MCNP cell card that contains the ' FILL '
parameter and a collection of defined surfaces that crop the universe
which it contains. These surfaces that define the fill cell must not
intersect the pseudo-cells.

A background cell is needed to make the mesh universe infinite in extent
and is the region outside of the blue unstructured mesh region in Fig.
8.3; it is cropped by the surface(s) that defines the fill cell.
Specifying the background cell in the MCNP input file is a 2-step
process: First, a background cell defined by the null surface must be
specified in the MCNP cell block. Second, the background keyword must
appear on the EMBED data card. The material specified for the background
cell is also the material used in all gaps within the UM model.

Figure 8.4: Illustration of the three critical points for the overlap models.

<!-- image -->

## 8.3.4 Overlaps

One of the initial requirements for the MCNP UM implementation was to
permit multiple, non-contiguous, meshed parts instead of requiring one
contiguous mesh. This naturally leads to the possibility of overlapping
parts, particularly when two parts attempt to share a curved surface. If
it is crucial to the model that the integrity of any curved surface be
maintained, the user should then consider merging the two separate parts
into a single part, using second-order elements, and/or refining the
mesh. Significant overlapping regions are never a good idea. Users
should never rely on any of the following models to correctly produce
the same results as a model where the boundary between two regions is
defined so that there is no overlap.

The MCNP code can accommodate a small amount of overlap in one of
several ways. For the initial implementation, there was no correction
for tracking through overlapping elements. A particle tracks in an
element until it finds a definite transition point in phase space (i.e.,
another element, gap, or background cell). Of the three overlap models
currently in place (see the OVERLAP keyword on the EMBED card and Fig.
8.4), the initial implementation is known as the EXIT model, meaning
that in an overlap situation, the exit point of the overlap is used and
a path-length is accumulated by ignoring an overlap region.

The second overlap model, ENTRY , is the one that uses the entry point
of the overlap in an overlap situation and the results are accumulated
accordingly. If the entry point is behind the particle's current
position, the current position is used; the particle never moves
backwards. The third and last overlap model is called AVERAGE and
results in averaging the entry and exit points in an attempt to find the
midpoint of the overlap in the direction the particle is tracking; the
particle's path length in the overlap is then divided between the two
parts instead of being assigned to one or the other.

Although the code defaults to the EXIT model, ultimately the choice of
which model to use is left to the user. If both parts are important and
the particle flux through this region is fairly isotropic, the AVERAGE
model is probably the best choice. If the flux is somewhat more
directional and one part is deemed more significant than the other, a
better choice might be ENTRY or EXIT , depending on the problem. The
user also has the ability to select the model to use by the part, with
the decision based upon the current part in which the particle resides.
For example, if the particle is currently in a part that specifies the
EXIT model and the part into which it will travel specifies the ENTRY
model, the EXIT model is used.

Note that testing has been performed with the EXIT model but not the
other two.

## 8.4 Output: Elemental Edits

To obtain results at the element level, a path length estimate of the
flux is accumulated as particles track from one element face to another,
Fig. 8.5.

Figure 8.5: Illustration of element-to-element tracking on a 12-element part.

<!-- image -->

To differentiate the mesh results from the traditional MCNP tally
treatment, those results accumulated on the unstructured mesh are
referred to as 'elemental edits.' There is no current intention to
duplicate all of the tally features with the edits. The elemental edits,
along with a generic description of the unstructured mesh model, are
output in a special file known as the EEOUT (Elemental Edit OUTput)
file. See §D.7 and DEP-53294 for a description of the legacy EEOUT file
and §D.6 for a description of the HDF5 EEOUT file.

At this time, relative errors are optional for the results on any
element. Specifying errors can result in large EEOUT files. If the
traditional MCNP statistical analysis (e.g., tally fluctuation chart,
empirical history score pdf) is desired for the results, set up a tally
for an appropriate pseudo-cell. More information on estimation of the
Monte Carlo precision can be found in §2.6.4.

## 8.5 MCNP Geometry Plotter

Plotting of the UM geometry with the MCNP plotter is very limited. It is
only possible to produce shaded plots of the pseudo-cells by material,
atom density, or mass density so the user may see that the UM geometry
is positioned correctly relative to the CSG cells. No cell outlines or
UM lines are possible. Labels may appear but may not be correct. See
Figs. 8.6-8.10 for several examples. Overlaps may make regions appear
distorted, Fig. 8.9. Gaps may give rise to extended regions of the
background material, Fig. 8.10.

Caution should be exercised with large UM files. While the plotter
should be able to plot large UM geometries, it may take a long time to
build the model. The MCNP plotter is an old technology and thus cannot
be used to view a UM model in 3-dimensions. Many modern software
packages can be utilized to view UM models in 3-dimensions. A UM model
formatted as an Abaqus input file can be visualized by the Abaqus and
Cubit codes; Cubit is a mesh generation tool kit developed by Sandia
National Laboratories ( https://cubit.sandia.gov ). A UM model formatted
as an HDF5 mesh file can be visualized by modern visualization software
packages such as ParaView ( https://www.paraview.org ) and VisIt (
https://visit-dav.github.io/visit-website/index.html ).

## 8.6 Limitations and Restrictions

The UM capability is currently not fully integrated with all of the pre-
existing MCNP features. This section highlights known limitations and
restrictions of the MCNP UM feature.

Figure 8.6: Pseudo-cells shaded by material in the mesh universe.

<!-- image -->

Figure 8.7: Pseudo-cells shaded by material density.

<!-- image -->

Figure 8.8: Model demonstrating correct plotting of a gap.

<!-- image -->

Figure 8.9: Model demonstrating overlaps.

<!-- image -->

Figure 8.10: Model demonstrating gaps.

<!-- image -->

- Limited to neutrons, photons, electrons with the default physics options, protons, and charged particles heavier than protons. Testing for other particle transport problems, except neutrons and photons, is limited.
- Cannot be used with magnetic fields.
- A UM model can not be placed inside a lattice.
- A universe can not be placed within a mesh universe.
- CSG surfaces must not clip or intersect the UM model.
- The MCNP plotter may be used to plot limited aspects of the UM geometry for the purpose of seeing its position in the hybrid geometry.
- Mesh surfaces can not be used for surface sources; normal surface source reads and writes have under gone limited testing with the UM feature and are not guaranteed to work with it.
- Reflecting and periodic boundary conditions are not guaranteed to work with the pseudo-cells but should work with CSG cells/surfaces that have these conditions.
- Source particles may not be started in mesh gaps.
- Surface tallies are not permitted in the background cell and pseudo-cells, but can still be used with CSG surfaces.
- Only pentahedra and hexahedra elements may appear together in a part; otherwise a part must contain only a single mesh type.
- Overlapping parts must not be severe; any single element may not be wholly contained within another element.
- Testing for multiple UM models embedded into multiple CSG cells is very limited.
- Forced collision ( FCL ) variance reduction cannot be used with the UM feature.

- Testing for embedding both UM and LNK3DNT geometries in a problem is very limited.
- Splitting particles as they enter and exit pseudo-cells as a result of weight windows or pseudo-cell importances may lead to potentially silent wrong answers with a UM geometry or, more clearly, seemingly unrelated issues, such as the code reporting negative emission energy following certain collisions (see the WWP and IMP entries for more information).
- It is unknown whether a PTRAC file will contain all surface related information.
- Not all combinations of parameters associated with the SDEF card have been tested in conjunction with the UM volume sources.

## 8.7 Abaqus-formatted Mesh Input File

## 8.7.1 Creating an Abaqus Input File

The Abaqus input files needed for MCNP UM calculations must have the
correct Abaqus syntax and meet the additional requirements by the MCNP
code. A mesh model is a representation of a solid geometry model, and
several software packages can generate a UM model formatted as an Abaqus
input file. Typically, a computer aided design (CAD) software is used to
construct a solid geometry model, which is then imported into a mesh
generation software to prepare and mesh the solid model. Finally, the
mesh model is exported into a file formatted as an Abaqus input file.
When creating Abaqus input files for MCNP UM calculations, users should
be aware of these two points:

1. Depending upon the purpose of the model creation and who is generating it, there may be extraneous information in the input file that could cause problems with the MCNP input file parser. What is shown in this section is the basic information that the MCNP code needs. For best results only include the data types discussed here.
2. Other meshing tools may be used to export an Abaqus input file. It is the user's responsibility to ensure that the Abaqus input files generated by other meshing tools meet the requirements outlined in this section.

## 8.7.2 Abaqus Input File Format

An Abaqus input file is an ASCII file that contains a series of lines.
Each line in the file cannot exceed 256 characters. If required data
cannot be fit on a single 256-character line, then a comma is placed at
the end of the line to indicate that the next line is a continuation
line. Three types of input lines are used in an Abaqus input file:
comment lines, keyword lines, and data lines.

| Comments   | Begin with double asterisks in columns 1 and 2 (**). The comment lines are not used by the MCNP code.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Keywords   | Must begin with an asterisk (*) in column 1. The keyword lines may have parameters that appear as words or phrases separated by commas. The keyword must be followed by a comma if it has parameters. The parameters in a keyword line can stand alone or have values. If a parameter has a value, an equal sign and a double quotation mark are respectively used to assign and group the value. Some keywords occur in pairs, meaning that there is a keyword that starts a block of data and another keyword that ends a block of data. Other keywords are singular in that they start a block of data and an unrelated keyword or comment ends the block. Most keyword lines require one or more data lines. If the data lines are required, they must immediately follow the keyword line. |

Data lines

Are generally used to provide entry values for the associated keyword
options. Data lines have no special characters preceding them and data
items are separated by commas. If there is only one item on a data line,
it must be followed by a comma.

The MCNP code reads and processes Abaqus input files that make use of
part and assembly definitions. An Abaqus UM model is created by defining
parts and then assembling instances of each part. Each part can be used
(instanced) one or more times, where each instance has its own position
within the assembly. Only one assembly can be defined in a model. A
component defined within a part, instance, or the assembly is local to
that part, instance, or the assembly. A part definition must appear
outside the assembly definition. Multiple parts can be defined in a
model and each part must have a unique name. An instance definition must
appear within the assembly definition, where each instance must have a
unique name and refer to a part name defined in the part data block.
Data lines may be used to position the instance within the assembly.
These positioning data lines include a translation and rotation for the
instance relative to the origin of the assembly coordinate system. Other
components must be categorized and fall within the proper level: part,
assembly, instance, or model. Material definitions are model-level data.
The part-level data definitions required by the MCNP code are node,
element, and element sets. All part definition blocks must be defined
before the assembly material definition blocks. The assembly material
blocks may appear in any order after the part blocks. Greater detail on
the Abaqus file format can be found in the Abaqus documentation released
with the Abaqus software package ( https://www.3ds.com/products-
services/simulia/products/abaqus/).

The MCNP code reads and processes the following keywords and associated
data lines: * Heading , * Part and * End Part , * Node , * Element , *
Elset , * Assembly and * End Assembly , * Instance and * End Instance ,
* Material , and * Density . The ' * Heading ' keyword is optional. The
sample input file in Section 8.7.2.10 is color-coded for ease of
reading. The keywords of interest to the unstructured mesh parser are
shown in blue. Several special tags, also of interest to the parser, are
shown in red and are discussed below. The model present in this sample
file is simple and consists of one part that has been instanced four
times in the assembly; this is discussed in more detail in Section
8.7.2.7. Each of the keywords of interest to the unstructured mesh
parser are discussed in the order that they usually appear in the sample
input file. In the following, keywords are shown in mixed case, but the
input parser is case-insensitive.

## 8.7.2.1 Part

The ' * Part ' keyword signifies the beginning of the information for a
particular part. The required parameter is the name after the ' name= '
characters on the keyword line. The label of the name parameter must be
unique since it will be used to refer to the part. The UM library parser
retrieves everything after the equals sign up to and including 256
characters in the name. This name is used by the UM library in locating
the correct part when it is instanced in the assembly. The part name is
also used when the UM library outputs information about the mesh model.
Do not use any of the element set keywords (§8.3.1.1) in the name of the
part.

## 8.7.2.2 Node

The ' * Node ' keyword appears in the part-level block and signifies the
beginning of the node data specific to the part. The MCNP code does not
use other parameters (such as input , nset , system ) on this keyword
line. The ' * Node ' keyword must have data lines follow that specify
the node numbers and their coordinates. Each data line contains four
numbers: the first entry is a positive integer and the other entries are
three real numbers. The positive integer is the node number and the
three real numbers are the x -, y -, and z -locations of the given node.

## 8.7.2.3 Element

The ' * Element ' keyword appears in the part-level block and marks the
beginning of the element connectivity data. The required parameter is '
type= '. Other parameters (such as elset , input , etc.) should not be
in the ' * Element ' keyword line since they are not used by the MCNP
code. The parameter value on this keyword line after ' type= ' is a
description of the type of elements in this part. The element type codes
appearing on this line that the UM library can handle are presented in
Table 8.1. The MCNP code treats a continuum shell element as a linear
hexahedron; it is included as a convenience for users that must rely on
the SC8 element type. In the example input file in Section 8.7.2.10, the
type code is presented in red-lettered characters on the ' * Element '
keyword line.

Table 8.1: Element Type Codes

| Element Type            | Type Code   |
|-------------------------|-------------|
| First-order tetrahedra  | C3D4        |
| First-order pentahedra  | C3D6        |
| First-order hexahedra   | C3D8        |
| Second-order tetrahedra | C3D10       |
| Second-order pentahedra | C3D15       |
| Second-order hexahedra  | C3D20       |
| Continuum shell element | SC8         |

Each line following this keyword contains a variable number of integers
depending upon the number of nodes that define the element. In the type
code given in Table 8.1, the number of nodes for a particular element
type appears as the number following the tag ' D ' or ' SC '. The first
integer on the data line is the element number; the remainder are the
node numbers that define the element. The exception to this is second
order hexahedra, where two lines are required for each element. For
these, the first line contains the element number plus 15 node numbers;
the second line contains the remaining 5 node numbers and is generally
indented.

The MCNP code can handle a part with two mixed element types. When two
element types appear in a part, Abaqus places two ' * Element ' keyword
sets in the ' * Part ' block. Currently, the UM library can only handle
mixed element parts containing pentahedra and hexahedra elements or
continuum shell and hexahedra elements. If tetrahedra elements are
needed in the model, a tetrahedra part must not contains other element
types. Other element type codes are used by the Abaqus code; it is the
user's responsibility to ensure use of the type codes from Table 8.1 to
specify the element types. The ' * Element ' keyword and data lines must
be defined after the ' * Node ' block.

## 8.7.2.4 Element Set

In Abaqus parlance, element sets are referred to as 'elsets' and the ' *
Elset ' keyword signifies the beginning of the elset data. The elset
mechanism permits the grouping of elements in order to assign various
properties. The MCNP code uses the elset definition blocks defined in
the part-level data. The elset keyword and data lines must be defined
after the ' * Element ' block(s). The elset parameter is required for
this keyword line; the parameter value after ' elset= ' is the name of
the element set to which the elements will be assigned. The ' elset= '
parameter must be the first parameter on the keyword line. Each part may
have more than one elset and each elset name must be unique. At least
material and tally elsets (see Section 8.3.1.1) must be defined in each
part. These elset names are easy to find in the example input file in
Section 8.7.2.10; they are in the red-lettered characters after the '*
Elset ' keyword that is in a blue font. The other parameters allowed in
the ' * Elset ' keyword line is generate . Other parameters (such as
instance , unsorted , etc.) should not be used on this keyword line.

The first elset is the material elset and is required. All of the
elements in a part must be assigned a material number. The name or tag
for this elset must contain the word ' material ' and the material
number. The material number must be the last part of the tag and it must
be separated from the rest of the tag by an underscore or hyphen. In
addition to the material elset tag presented in the example in Section
8.7.2.10, the following tag is also acceptable:

## Set-my \_ material \_ uranium \_ 02

Note that any number of characters can appear between the word
'material' and the material number, but the total length of the line
containing the keyword and the tag is limited to 256.

The second elset is the statistic (or tally) elset. This elset is also
required. The name or tag for this elset must contain the word '
statistic ' or ' tally ' (but not both) and the statistic set number.
The same rules and conventions apply to this elset tag as for material
elsets. All elements in a statistic elset must have the same material
number; there is no mixing of materials in the statistic set. The UM
library will enforce this.

For each of these keyword types, the data lines following them may be
one of two forms. The first of which is just an integer list of element
numbers, on the order of 16 integers or fewer per line. The second form
is in compact notation where the word ' generate ' appears on the ' *
Elset ' keyword line and the data line consists of 3 integers. The first
integer is the starting element number. The second integer is the ending
element number. The third integer is the stride from the starting to the
ending element numbers. For example, to specify all of the odd element
numbers from 1 to 27, use the following:

## 1, 27, 2

The MCNP code uses these two elsets (material and statistic) and
instance data to define the internal pseudo-cells that must be mapped
back to the pseudo-cell cells in the MCNP input file; this mapping is
done with the MATCELL keyword on an EMBED card. The MCNP code outputs a
'Pseudo-Cell Cross-Reference' table that shows how the internal pseudo-
cell numbers match the pseudo-cell numbers defined in the MCNP input
file, the instance numbers, the part numbers, the material numbers, and
the material names.

## 8.7.2.5 End Part

The ' * End Part ' keyword marks the end of a part's input. Another part
description may follow, in which case there will be another ' * Part '
keyword to signify its beginning, or the assembly description may
follow.

## 8.7.2.6 Assembly

The ' * Assembly ' keyword appears after all of the parts are defined. A
look at the sample file shows that an assembly name appears after this
keyword much like what appeared for the part. The UM library does not
use the assembly name; it only uses the ' * Assembly ' keyword to
determine the end of the part data

There is also an ' * End Assembly ' keyword that signifies the end of a
particular assembly. Between these two keywords is the important
information that the UM library needs in order to construct the mesh
model from the parts.

## 8.7.2.7 Instance

Appearing in the assembly-level block are the ' * Instance ' keywords.
The numbers that appear here correspond to the parts used to form the
Assembly for each instance. Each part may be instanced many times. There
are two parameters appearing on the ' * Instance ' keyword line: ' name=
' and ' part= '. The parameter value after ' name= ' is the name of the
instance and, unless changed by the user in the meshing tool, is just
the part name appended with an instance number. The parameter value
after ' part= ' is the part name as one of those used with the ' * Part
' keyword. The ' name ' parameter must be defined before the ' part '
parameter. The UM library uses this ' part ' parameter name to match
with the ' * Part ' keyword name in order to locate the right one to
use.

The ' * End Instance ' keyword marks the end of the information block
for a particular instance. From the example in Section 8.7.2.10, there
are four instances of the same part. The last instance in this example
has no additional lines between the ' * Instance ' and ' * End Instance
' keyword lines while the other three have one or two data lines present
that describe the translation or rotation of the part as it was
instanced into the assembly.

The first data line appearing between the keywords is the translation
information. The three real values given here are the values of the
translation applied in the x -, y -, and z -directions, respectively.
These translation values have the same unit used to define node
positions in parts.

If the part is rotated as it is instanced into the assembly, two lines
appear between the instance keyword lines. The first line is the
translation information as discussed previously. If there is a pure
rotation the values for the three real numbers on the translation line
are all zero. If there is both a translation and rotation, the
translation is applied before the rotation.

There are seven real numbers that appear on the rotation line. The first
six real numbers define an axis of rotation. The first three numbers are
the x -, y -, and z -locations of the first point that defines the axis.
The second three numbers are the x -, y -, and z -locations of the
second point that defines the axis. The seventh number is the angle of
rotation in degrees about the axis.

In the sample input file, the first and third instances have just a
translation while the second instance has a rotation but no translation.
The fourth instance is neither translated or rotated.

## 8.7.2.8 Material

The ' * Material ' keyword has one parameter, which is a material name.
The parameter value after ' name= ' is the name of material which must
end with a number. The UM library parser retrieves everything after the
equals sign up to and including 256 characters in the name and extract
the ending number. This ending material number is then used to match
with an elset material number in a part. See Section 8.3.1 for the
recommendations in naming materials. The material properties present in
an Abaqus input file are not used for MCNP calculations. The MCNP code
uses the material properties defined in the MCNP input file.

## 8.7.2.9 Density

The ' * Density ' keyword is the material sub-keyword of interest to the
UM library. The data line following this keyword has one data item. This
keyword and associated value are only used by the um \_ pre \_ op program,
[§E.12, DEP-53422]. The ' * Density ' keyword and data line are not
required by the UM library. If this keyword and data line are not in an
Abaqus input file, the MCNP skeleton input file written by the um \_ pre
\_ op program will be zero density (void) and the user must manually edit
the densities in the MCNP input file. Mass densities used in Abaqus
calculations must be positive, but mass densities in an MCNP file must
be

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

entered as negative numbers. The um \_ pre \_ op writes the density values
read from an Abaqus input file into an MCNP input file without adjusting
the sign, and it is user's responsibility to edit the mass densities in
an MCNP input if they are positive in an Abaqus input file. A negative
density value is not a correct Abaqus input format, but the UM library
will read the negative density value without any warning. The density
values in an Abaqus input file are not used in MCNP calculations, and it
is not required that the material density in the Abaqus input file be
the same as the density in the MCNP input file.

## 8.7.2.10 Example Abaqus Input File

<!-- image -->

| * Heading an example of an Abaqus input file ** Job name: job _ block _ demo _ 01 Model name: Model-1 ** Generated by: Abaqus/CAE 6.10-1 * Preprint, echo=NO, model=NO, history=NO, contact=NO **   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

```
47 * Nset, nset=Set-material _ 01, generate 48 1, 27, 1 49 * Elset, elset=Set-material _ 01, generate 50 1, 8, 1 51 * Nset, nset=Set-statistic _ 01, generate 52 1, 27, 1 53 * Elset, elset=Set-statistic _ 01, generate 54 1, 8, 1 55 * End Part 56 ** 57 ** 58 ** ASSEMBLY 59 ** 60 * Assembly, name=Assembly 61 ** 62 * Instance, name=Part-block _ 01-1, part=Part-block _ 01 63 4., 0., 0. 64 * End Instance 65 ** 66 * Instance, name=Part-block _ 01-2, part=Part-block _ 01 67 0., 0., 0. 68 0., 0., 0., 0., 1., 0., 90. 69 * End Instance 70 ** 71 * Instance, name=Part-block _ 01-3, part=Part-block _ 01 72 4., 0., -4. 73 * End Instance 74 ** 75 * Instance, name=Part-block _ 01-4, part=Part-block _ 01 76 * End Instance 77 ** 78 * End Assembly 79 ** 80 ** MATERIALS 81 ** 82 * Material, name=Material-part1 _ 01 83 * Density 84 18.74,
```

## 8.8 HDF5-based Mesh Input and Output Files

In addition to the Abaqus-formatted mesh input file described in §8.7,
an HDF5-formatted [340] mesh input file can be used. The format of this
file is described in §D.6. The HDF5-formatted UM output can also be
requested and has the format described in §D.6. Advantages provided by
HDF5 include hierarchical organization, binary representation of data
with compression, and many options for software and programming language
interoperability.

The legacy EEOUT file [§D.7, DEP-53294] provides comprehensive output
for MCNP UM calculations, which includes providing the ability to
restart calculations. However, the EEOUT file uses a non-standard mesh
file format, so it requires custom post-processing parsers that often
rely heavily on regular expressions. Accordingly, it can be burdensome
for end users to convert the EEOUT file into a format for downstream
analysis and/or visualization. The GMV file [§8.9.1] also prevents easy
interrogation except by select visualization applications or custom
post-processing applications. Because of the GMV format, post-processing
is usually limited to serial execution.

As such, an output file option is available that produces an HDF5 binary
file containing the UM geometry and edit results and an accompanying
XDMF version 2 file [324, 325] that permits direct visualization in
applications such as ParaView [326] and VisIt [327]. The HDF5 file
itself can be processed in parallel. In this way, the XDMF file can be
immediately used to visualize UM results and the HDF5 file can be
interrogated and/or manipulated to enable downstream analysis using
standard HDF5 utilities, which are available in a variety of programming
languages (such as with Python's h5py package).

When HDF5 output is enabled, data necessary for restart calculations are
also written (and used, as applicable). For the MCNP code, these data
are written to the /restart/unstructured \_ mesh group in the HDF5-format
runtape file [§D.2]. As such, MCNP calculations can be performed using
the legacy EEOUT output [DEP-53294] or HDF5 output for results and
restart purposes. This provides a means to compare behavior and permits
deprecating the legacy EEOUT output. Note that during comparison with
ASCII EEOUT files, some differences are expected because the ASCII
output stores only five decimal places.

To enable the HDF5 output, the hdf5file parameter on the EMBED card
specifies the name for (and enables writing) a binary HDF5 file
containing UM geometry structure and data as well as an accompanying
XDMF version 2 file. The hdf5file option and the MCNP input command line
option can be used to create the HDF5/XDMF files containing the mesh
model.

The accompanying XDMF version 2 file is an ASCII XML file. Because of
its standard format, the XDMF file format is not described here. The
XDMF file does not contain the mesh model data nor the edit results.
This XDMF file points at the appropriate data in the HDF5 binary file so
that the mesh model and edit output can be visualized. Note that the
XDMF and HDF5 files must remain together in the same directory to permit
a utility reading the XDMF file to find the HDF5 file. If a Python
script is developed to post-process the mesh data and edit results, then
only the HDF5 file is needed since the mesh data and edits are contained
in this file.

## 8.9 Other Files

## 8.9.1 GMV File

## /\_445 Deprecation Notice

DEP-53519

The GMV file output capability using the EMBED card is deprecated.
Because of the new HDF5formatted output file that can be trivially
visualized and/or post-processed, this output file format is no longer
necessary. As such, the GMV keyword on the EMBED card is deprecated.

Often times it is beneficial to have an independent and easy to use
program for mesh geometry visualization. The General Mesh Viewer, GMV,
program [228] is such a program. For this reason, it is possible to
generate a GMV input file (see embed card, parameter gmvfile ). Note
that if during model creation in the CAE tool, the material elsets don't
have unique numbers, it will be difficult to differentiate parts in GMV.
That is, if each part has one material and the number assigned to that
material is the same one in all of the parts, then all elements in GMV
will have the same color. Also, GMV limits material names to 8
characters.

This GMV file capability is primarily for LANL use.

## 8.9.2 MCNPUM File

## /\_445 Deprecation Notice

DEP-53424

The MCNPUM file (as both input and output) specified on the EMBED card
for unstructured mesh (UM) calculations is deprecated. Because of
algorithmic improvements during UM input processing, the need for this
file to accelerate that process is no longer necessary. Furthermore, the
historic guidance that suggests limiting components to 30,000-50,000
elements is no longer necessary.

As such, the MCNPUMFILE keyword on the EMBED card and the mcnpum option
for the MESHGEO keyword are also deprecated.

The Abaqus input file contains some basic information about the
unstructured mesh, but does not contain everything that MCNP6 needs.
Once MCNP6 reads this file, it uses the Abaqus data to generate other
information that it needs in its tracking routines, such as nearest
neighbor lists. Even with the parallel input processing, discussed
elsewhere in this document, significant computer time can be required to
regenerate this data and create other internal data structures for every
MCNP6 calculation that uses the Abaqus unstructured mesh file.

The MCNPUM file-type [341] was created to contain all of the
unstructured mesh data structures that MCNP6 needs, thus eliminating the
need to 'input process' the Abaqus input file every time the code is
run, including restarted calculations. MCNP6 can generate this file
(primarily after processing the Abaqus input file) by simply including
the MCNPUMFILE option on the EMBED card. MCNP6 can use the MCNPUM file
when MESHGEO=MCNPUM on the EMBED card.

The um \_ convert utility [§E.10, DEP-53421] is a highly parallelized
program that can convert the Abaqus mesh input file to the MCNPUM file
type. This file type is highly recommended when a complex geometry will
be used more than once.
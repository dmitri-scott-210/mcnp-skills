---
title: "Chapter 5.6 - Material-focused Data Cards"
chapter: "5.6"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.6_Material-focused_Data_Cards.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

```
16 m2 1001.60c 1.0 17 prdmp j 275 18 print 19 rand gen=2 seed=12345 20 embed10 meshgeo=lnk3dnt mgeoin=linkout debug=echomesh 21 calc _ vols=yes background=12 matcell= 1 11
```

## 5.5.6.13.2 Example 2

Similar to the last example's geometry, an unstructured mesh using
first-order hexahedra can be defined and used in the MCNP input file
shown in Listing 5.19. The Abaqus-formatted mesh input file is
electronically attached to this document as example \_ unstructured \_
mesh.abaq.inp.txt .

Listing 5.19: example\_unstructured\_mesh.mcnp.inp.txt

<!-- image -->

The EMBED card is allowed in a restarted embedded unstructured mesh
problem. This allows for the previous elemental edit output file to be
read in as the elemental edit input file (now deprecated functionality)
or from the MCNP runtape file and for a new name to be assigned to the
newly created elemental edit output file, as shown in Listing 5.20 and
is executed with the command (depending on the runtape name): mcnp6 c r=
runtpe.h5 i= example \_ unstructured \_ mesh \_ continue.mcnp.inp.txt .

```
continue c kcode 5000 1.0 50 300 embed2 meshgeo=abaqus mgeoin=example _ unstructured _ mesh.abaq.inp.txt meeout=example _ unstructured _ mesh _ continue.eeout hdf5file=example _ unstructured _ mesh _ continue.eeout.h5 background= 12 matcell= 1 11
```

Listing 5.20: example\_unstructured\_mesh\_continue.mcnp.inp.txt

1

2

3

4

5

6

7

## 5.6 Material-focused Data Cards

Material cards within the MCNP code serve two purposes. The first is to
specify the composition of the materials. The second is to select the
data libraries to use during simulation. The M card is used to create a
material and define its composition. It also has a few options to define
material-specific properties to use during transport. The MT card allows
one to attach a neutron thermal scattering S ( α, β ) table to a
material. Finally, the MX card allows one to alter targets and tables on
a per-physics basis.

## 5.6.1 M: Material Specification

The material card allows a user to input the composition of a given
material. The main input consists of pairs of targets and
concentrations. Targets can be specified using target identifiers
[§1.2.2], or using table identifiers [§1.2.3]. Concentrations can be
specified by either mass or weight fraction. Additionally, there are
key-value pairs on this card that set specific material properties.

## /warning\_sign Caution

M card keywords may appear anywhere among the target-fraction pairs, but
must not separate a pair.

The M card also doubles as a mechanism for selecting data tables. The
MCNP code loads data using a process described in §2.3.1. Each target
listed on the M card is added to the data search list. The necessary
physics identifiers are inferred from the MODE and PHYS cards. The
library identifiers can be input on the M card in three ways. The first
is by using a full table identifier instead of a target identifier. This
library identifier will only be used for the corresponding physics.
Second, to select libraries for each physics, the x LIB ( NLIB , PLIB ,
PNLIB , ELIB , HLIB , ALIB , SLIB TLIB , DLIB ) key-value options can be
used. When set, the value will be used for every target in the material.
Third, a special material card, M 0 , can be used to set the default for
all materials.

The methods one can use to select the library, in decreasing priority,
are:

1. Setting a full table identifier on the MX card for a given physics.
2. Setting a full table identifier on an M card.
3. Setting the x LIB key-value options on an M card.
4. Setting the x LIB key-value options on an M0 card.

The x LIB options are the only way to specify which data libraries to
use for the nuclides that are implicitly added to the simulation through
transmutation during BURN calculations. Without x LIB , the first
library listed in the xsdir is always used for those nuclides.

It is recommended to always specify compositions by nuclide or isomer
rather than by element (in which A is set to zero) for two reasons.
First, in simulations with nuclear interactions, inputting elemental
identifiers results in using older data because current practices are to
provide only isotopic data files, so elemental data files are generally
out of date and less accurate. Second, atom densities are computed using
the elemental atomic mass listed in the xsdir file. For elements in
which there exists a natural composition, this value is computed using
that composition. For elements for which no natural composition exists,
the elemental mass is specified, but no pedigree is available. This can
result in unexpected behavior.

| Data-card Form: M m z1 f1 z2 f2 . . . zK fK keyword = values(s)   | Data-card Form: M m z1 f1 z2 f2 . . . zK fK keyword = values(s)                                                                                                                                                                                                                                                                                                                                   | Data-card Form: M m z1 f1 z2 f2 . . . zK fK keyword = values(s)                                                                                                                                                                                                                                                                                                                                   |
|-------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| m                                                                 | Arbitrary material number; same as material number, m , on a cell card [§5.2]. When m = 0 , keyword entries on that card are applied to all other M cards. Restriction: 0 ≤ m ≤ 99 , 999 , 999 .                                                                                                                                                                                                  | Arbitrary material number; same as material number, m , on a cell card [§5.2]. When m = 0 , keyword entries on that card are applied to all other M cards. Restriction: 0 ≤ m ≤ 99 , 999 , 999 .                                                                                                                                                                                                  |
| zk                                                                | Either a target identifier [§1.2.2] or a table identifier [§1.2.3] for constituent k . All forms of target identifier are supported.                                                                                                                                                                                                                                                              | Either a target identifier [§1.2.2] or a table identifier [§1.2.3] for constituent k . All forms of target identifier are supported.                                                                                                                                                                                                                                                              |
| fk                                                                | Fraction of the k th constituent in the material ( 1 , 2 ), where                                                                                                                                                                                                                                                                                                                                 | Fraction of the k th constituent in the material ( 1 , 2 ), where                                                                                                                                                                                                                                                                                                                                 |
| fk                                                                | fk > 0                                                                                                                                                                                                                                                                                                                                                                                            | indicates that the value is interpreted as an atomic fraction and                                                                                                                                                                                                                                                                                                                                 |
| fk                                                                | fk < 0                                                                                                                                                                                                                                                                                                                                                                                            | indicates that the value is interpreted as the weight fraction.                                                                                                                                                                                                                                                                                                                                   |
| fk                                                                | Atomic and weight fractions may not both appear on a single M card.                                                                                                                                                                                                                                                                                                                               | Atomic and weight fractions may not both appear on a single M card.                                                                                                                                                                                                                                                                                                                               |
| GAS = value                                                       | Optional, flag for density-effect correction to electron stopping power. If                                                                                                                                                                                                                                                                                                                       | Optional, flag for density-effect correction to electron stopping power. If                                                                                                                                                                                                                                                                                                                       |
| GAS = value                                                       | GAS = 0                                                                                                                                                                                                                                                                                                                                                                                           | the code calculates a density-effect correction appropriate for material in the condensed (solid or liquid) state (DEFAULT), or                                                                                                                                                                                                                                                                   |
| GAS = value                                                       | GAS = 1                                                                                                                                                                                                                                                                                                                                                                                           | the code calculates a density-effect correction appropriate for material in the gaseous state.                                                                                                                                                                                                                                                                                                    |
| ESTEP = n                                                         | Causes the number of electron sub-steps per energy step to be increased to n for the material. If n is smaller than the built-in default found for this material, the entry is ignored. Both the default value and the ESTEP value actually used are available in PRINT Table 85 of the output file. (DEFAULT: internally set)                                                                    | Causes the number of electron sub-steps per energy step to be increased to n for the material. If n is smaller than the built-in default found for this material, the entry is ignored. Both the default value and the ESTEP value actually used are available in PRINT Table 85 of the output file. (DEFAULT: internally set)                                                                    |
| HSTEP = n                                                         | Causes the number of proton or other charged-particle sub-steps (exclusive of electrons, but including heavy ions) per energy step to be increased to n for the material. If ESTEP is specified and HSTEP is not, then the ESTEP value is used for HSTEP . Both the default value and the HSTEP value actually used are available in PRINT table 85 of the output file. (DEFAULT: internally set) | Causes the number of proton or other charged-particle sub-steps (exclusive of electrons, but including heavy ions) per energy step to be increased to n for the material. If ESTEP is specified and HSTEP is not, then the ESTEP value is used for HSTEP . Both the default value and the HSTEP value actually used are available in PRINT table 85 of the output file. (DEFAULT: internally set) |
| NLIB = x                                                          | Changes the default neutron table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                    | Changes the default neutron table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                    |
| PLIB = x                                                          | Changes the default photoatomic table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                | Changes the default photoatomic table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                |
| PNLIB = x                                                         | Changes the default photonuclear table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                               | Changes the default photonuclear table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                               |
| ELIB = x                                                          | Changes the default electron table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                   | Changes the default electron table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                   |
| HLIB = x                                                          | Changes the default proton table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                     | Changes the default proton table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                     |
| ALIB = x                                                          | Changes the default alpha table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                      | Changes the default alpha table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                      |
| SLIB = x                                                          | Changes the default helion table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                     | Changes the default helion table identifier to the string x (DEFAULT: blank string, which selects the first matching entry in the xsdir file)                                                                                                                                                                                                                                                     |

1

Changes the default triton table identifier to the string x (DEFAULT:
blank xsdir

- TLIB = x string, which selects the first matching entry in the file)

DLIB = x

Changes the default deuteron table identifier to the string x (DEFAULT:
blank string, which selects the first matching entry in the xsdir file)

COND = value Sets conduction state of a material only for the EL03
electron-transport evaluation. If

COND &lt; 0 then the material is a non-conductor.

COND = 0

COND &gt; 0

then the material is a non-conductor if there is at least one non-
conducting component; otherwise it is a conductor (DEFAULT)

then the material is a conductor if there is at least one conducting
component.

REFI = A Constant refractive index

REFI = A B C D Cauchy coefficients (units are micrometers) for
refractive index that are used

<!-- formula-not-decoded -->

to calculate

REFS = B1 C1 B2 C2 B3 C3

Sellmeier coefficients for refractive index that are used to calculate

<!-- formula-not-decoded -->

Use: Required if you want materials in cells. Recall that an equals sign
(=) following a keyword, such as the x LIB keywords, is optional.
Inclusion of the decimal point or the physics identifier in the library
x designation (e.g., .70c as opposed to 70) is permitted, but not
required.

## Details:

- 1 The nuclide fractions can be normalized to 1.0 or left unnormalized, in which case the code performs the normalization.
- 2 The code uses the atomic weight ratio values from the transport table to convert mass fractions to atom fractions. To avoid this conversion and therefore ensure the most accurate material representation, it is recommended that atom fractions be specified.

## 5.6.1.1 Example 1

<!-- formula-not-decoded -->

In this example, there are two components to this material, one part 12
C and two parts 16 O by atom fraction. For 12 C, the neutron library
identifier 00 is explicitly set. For 16 O, the photoatomic library
identifier 12 is

1

1

1

Table 5.7: M Card Example 1 Table Listing

| Physics      | 12 C                                        | 16 O                                        |
|--------------|---------------------------------------------|---------------------------------------------|
| Neutron      | 6012.00c                                    | 8016.80c                                    |
| Photoatomic  | 6000.14p                                    | 8000.12p                                    |
| Photonuclear | 6012.24u                                    | 8016.24u                                    |
| Electron     | First e dataset with Z = 6 , A = 0          | First e dataset with Z = 8 , A = 0          |
| Proton       | First h dataset with Z = 6 , A = 12 , S = 0 | First h dataset with Z = 8 , A = 16 , S = 0 |

explicitly set. The neutron default library identifier is set to 80 ,
the photonuclear default library identifier is set to 24, and the
photoatomic default library identifier is set to 14 .

Given a simulation with neutron, photon, electron, and proton physics,
the tables shown in Table 5.7 will be loaded. There are several notes
here. First, most tables are historically identified in ZAID format
[§1.2.2]. The MCNP code converts between target identifier formats to
load 6012 for C-12 and 8016 for O-16. Second, for atomic data, A is
automatically set to zero. Photoatomic and electron data search for C-0
and O-0 instead of C-12 and O-16. Third, the library identifier attached
to the target identifier overrides the x LIB options. This occurs for 12
C neutron data and 16 O photoatomic data. Finally, as neither electrons
nor protons have their library specified, the first value in the xsdir
will be used based on the listed rules.

## 5.6.1.2 Example 2

M1 NLIB=50D H-1 2 O-16.50C 1 C-12 1

This material consists of three isotopes. Hydrogen (H-1) and carbon
(C-12) are not fully specified and will use the default neutron table
that has been defined by the NLIB entry to be 50d, the discrete-reaction
library. Oxygen (O-16.50c) is fully specified and will use the
continuous-energy library 8016.50c. The same default override hierarchy
applies to proton, photonuclear, photon, and electron specifications.

## 5.6.1.3 Example 3

## M1 Ag-110m 1

In this example, the material consists of 110m Ag. In older files, this
may be represented by the ZAID 47510, where Z = 47 , A = 110 , and the
identifier is incremented by 300 + 100 S = 400 to indicate the first
metastable state.

## 5.6.1.4 Example 4

M1 H-1 2 O-16 1 REFI=1.3199

Water with a constant refractive index of 1.3199.

1

## 5.6.1.5 Example 5

```
M1 H-1 2 O-16 1 REFC=1.3119 6.878e-2 1.132e-3 1.11e-4
```

Water with a refractive index specified by coefficients for a 4th-order
Cauchy expression. The coefficients are in units of micrometers.

## 5.6.1.6 Example 6

```
M1 Si-28 1 O-16 2
```

```
1 2 REFS = 1.0396 6e-3 0.2318 2.0018e-2 1.0104 1.0356e2
```

Approximate borosilicate crown glass (cf. [material 156 of 229]) with a
refractive index specified by coefficients for Sellmeier's equation.
Sellmeier coefficients are applied directly; they are not squared.

## 5.6.2 MT: S ( α, β ) Thermal Neutron Scattering

It is possible to treat nuclides within a material as if they were a
molecule or crystalline solid by applying S ( α, β ) neutron thermal
scattering data. This data, described in more detail in §2.3.6, replaces
portions of the neutron physics at low energies, below approximately 10
eV depending on library, with those altered by molecular binding forces.

The MT card is specified for each material as needed. The input is a
list of S ( α, β ) table identifiers [§1.2.3]. S ( α, β ) table
identifiers are slightly different from typical identifiers, in that the
target is an arbitrary string due to the many possible molecules or
crystals that can be represented. Modern libraries use a 'target-
molecule' format for the target identifiers. As an example, H-H2O would
alter the hydrogen physics to correspond to molecular interactions in
water. The physics identifier is t for this type of data.

The MT card will override the physics of all nuclides marked as a
target. In the case of H-H2O , all hydrogen tables will be altered to
include water binding energy. It is not possible for two tables to alter
a single target or to alter only a fraction of a material. If multiple
tables for a given target are loaded, the MT0 card can be used to match
a specific S ( α, β ) table to a specific target table such as when
stochastic temperature mixing is used.

## Data-card Form: MT m sabid1 sabid2 . . . sabidK

m

sabidk

Default: None.

Use: Essential for problems with thermal neutron scattering.

Material identifier, same as m on the corresponding material ( M m )
card.

S ( α, β ) identifier [§1.2.3] corresponding to a particular target on
the M m card. S ( α, β ) contributions to detectors ( F5 tallies) and
DXTRAN spheres ( DXT card) are approximate.

1

2

## 5.6.2.1 Example 1

```
M1 H-1 2 O-16 1 $ light water MT1 H-H2O.40t
```

In this example, all hydrogen in material 1 will be altered with the
H-H2O.40t table.

## 5.6.2.2 Example 2

| M8   | C-12 1   | $ graphite   |
|------|----------|--------------|
| MT8  | GRPH.47t |              |

In this example, all carbon in material 8 will be altered with the
GRPH.47t table.

## 5.6.2.3 Example 3

When a particle is within the energy regime at which the S ( α, β )
treatment applies, the specification

```
1 M1 H-1 2 O-16 1 Be-9 1e-3 $ light water w/ small amt of Be 2 MT1 H-H2O.40t BE-MET.40t
```

will substitute the light-water S ( α, β ) library for the hydrogen and
the beryllium metal library for the beryllium.

However, the specification

```
1 M1 Be-9 2 O-16 1 $ Be oxide 2 MT1 BE-MET.40t BE-BEO.40t
```

will not work as desired because both libraries will try to substitute
for the beryllium in the problem. Only the first S ( α, β )
specification (for BE-MET.40t ) will be used.

## 5.6.2.4 MT0 Card: S ( α, β ) Special Treatment for Specific Isotopes

Some MCNP input files make use of an old, traditional method for dealing
with material temperatures called 'stochastic mixing.' When a material
is used in a cell that has a temperature in-between the temperatures
used by NJOY in producing the ACE files, users can approximate the
temperature effects on cross-section data by including both a 'hot'
version and a 'cold' version of the ACE data used for each isotope in
the material. For example, if there are ACE files available at 293.6K
and 600K, and a cell has a temperature of 446.8K (halfway between the
available ACE files), then an approximate way to model the material is
to include each isotope twice - once using a target at the lower ACE
file temperature and once using a target for the ACE file at the higher
temperature, with 50% of the atom or weight fractions used for each of
the

bounding targets. During transport, the MCNP code will select the 'hot'
target half the time and the 'cold' target the other half,
stochastically, so that the average for the mixture matches the cell
temperature. This approach is approximate, because it is not
interpolation based on physics, just a stochastic mixing of the bounding
data.

The use of stochastic mixing for ordinary cross-section data is routine
and straightforward. For the S ( α, β ) ACE datasets, however, there is
the complication that the 'hot' S ( α, β ) data must be specifically
associated with the 'hot' identifier and the 'cold' S ( α, β ) data must
be specifically associated with the 'cold' identifier. To make the
correct association of S ( α, β ) data tables to nuclear data tables,
the MT0 card can be used to fully specify the S ( α, β ) assignments.

The format of the MT0 card is:

| Data-card Form: MT0 sabid1 identifier _ 1 . . . sabidK identifier _ k   | Data-card Form: MT0 sabid1 identifier _ 1 . . . sabidK identifier _ k                                             |
|-------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| sabidk                                                                  | S ( α,β ) dataset identifier [§1.2.3]. The library identifier and physics identifier must be explicitly included. |
| identifier _ k                                                          | material target identifier. The library identifier and physics identifier must be explicitly included.            |

Default: None.

Use: Essential for problems with thermal neutron scattering where S ( α,
β ) datasets and nuclear datasets are specified at more than 1
temperature for a single material.

The entries in MT0 consist of pairs of S ( α, β ) dataset identifiers
and nuclear data identifiers. Whenever the S ( α, β ) dataset is
requested on an MT card, it will only be used to alter the physics for
the data in the corresponding nuclear data library. Libraries listed on
this card must also be fully specified on their corresponding M and MT
cards. Users should check PRINT Table 102 to verify the correct
assignments in the materials.

## 5.6.2.5 Example 4

A material is at 446.8K, halfway between ACE files available at 293.6K
and 600K. Water may be represented in the following approximate manner
using stochastic mixing:

| mt0   | h-h2o.40t H-1.00c        | $ S(a,b)-table matching at 293.6K   |
|-------|--------------------------|-------------------------------------|
|       | h-h2o.54t H-1.01c        | $ S(a,b)-table matching at 600K     |
| c     |                          |                                     |
| m100  | H-1.00c 1.0 O-16.00c 0.5 | $ at 293.6K                         |
|       | H-1.01c 1.0 O-16.01c 0.5 | $ at 600K                           |
| mt100 | h-h2o.40t h-h2o.54t      |                                     |

Each nuclide is included twice, with half the required fraction for
each, and both S ( α, β ) datasets are included on the MT100 card. The
pairs of identifiers from the MT0 card are used to provide the proper
assignments for the material. The h-h2o.40t data is associated with the
H-1.00c nuclide, and the h-h2o.54t data is associated with the H-1.01c
nuclide. PRINT Table 102 is used to verify that these assignments were
made.

## 5.6.3 MX: Material Card Nuclide Substitution

The MCNP nuclide substitution capability [230] enables mixing of physics
models and data tables for individual isotopes. Different nuclides can
be substituted for different particle types. For example, natural carbon
and calcium can be used for neutrons, whereas 12 C and 40 Ca can be used
for protons and photonuclear reactions.

Above tabular data limits, models are automatically called in the MCNP
code. The model to be used depends on values set on the LCA card. The
physics models can be disabled by the MPHYS card. The sole exception is
photonuclear interactions, for which CEM03.03 [201, 207, 208, 212, 216]
is always used regardless of whether CEM03.03 is used for other
particles (see the LCA card). Using the term MODEL on an MX card will
substitute model physics for the entire energy range of a particle-no
tabular data will be used. This option should be carefully considered
before use. The parameter 0 on an MX card eliminates all interaction
physics, whether model or table-based. This makes sense in the case of
photonuclear interactions on hydrogen, which do not exist in nature, but
should be avoided for other cases.

| Data-card Form: MX m : P z1 z2 . . . zK   | Data-card Form: MX m : P z1 z2 . . . zK                                                                                                                                                             |
|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| m                                         | Material identifier, same as m on the corresponding material ( M m ) card. The MX m card must appear after its associated ( M m ) material card.                                                    |
| P                                         | Particle designator [Table 4.3]; allowed values are neutron ( n ), photonuclear ( p ), proton ( h ), deuteron ( d ), triton ( t ), hellion ( s ), and alpha ( a ).                                  |
| zk                                        | Varies behavior such that if = _                                                                                                                                                                    |
| zk                                        | zk table identifier [§1.2.3], then substitute the specified library for the k th nuclide identifier on the M card. All target formats are supported.                                                |
| zk                                        | zk = target _ identifier [§1.2.2] then substitute the k th nuclide on the                                                                                                                           |
| zk                                        | M card with the nuclide listed. zk = MODEL then substitute model physics for the k th nuclide on the M card. A mixture of models and tabular data may be specified for nuclides on a single M card. |
| zk                                        | zk = 0 for a photonuclear substitution card ( MX m : P ), then omit photonuclear reactions for zk . This option is only available for photonuclear particles.                                       |
| zk                                        | No substitutions are allowed for photoatomic ( P ) and electron ( E ) data because these data depend only on Z and are not isotope-specific.                                                        |

Use: The MX m card enables nuclide substitution for different particle
types. The nuclide replacement capability is particularly useful for
photonuclear and proton calculations when few data tables are available.
Libraries are used when available and models are used otherwise.

## 5.6.3.1 Example 1

| MODE   | n h p                      |
|--------|----------------------------|
| M3     | H-2 1 H-3 1 C-12 1 Ca-40 1 |

3

4

5

| MX3:N   | j     | MODEL   | C-0   | Ca-0   |
|---------|-------|---------|-------|--------|
| MX3:H   | MODEL | H-1     | j     | j      |
| MX3:P   | C-12  | 0       | j     | j      |

In this example, models will be used for neutrons on tritium and protons
on deuterium. Natural libraries will be used for neutron interactions on
carbon and calcium. A model will be used for proton interactions for
deuterium, and protons on tritium will substitute the hydrogen cross
section. For photonuclear, 12 C substitutes for deuterium and the cross
section for tritium interactions will be set to 0.0.

## 5.6.3.2 Example 2

| m1    | O-16         | 1.0          |
|-------|--------------|--------------|
|       | Pb-206       | 10.0         |
|       | nlib=.60c    | nlib=.60c    |
|       | hlib=.24h    | hlib=.24h    |
|       | pnlib=.24u   | pnlib=.24u   |
| mx1:h | j Fe-56.70h  | j Fe-56.70h  |
| mx1:n | j Ra-223.70c | j Ra-223.70c |
| mx1:p | j Pu-239.70u | j Pu-239.70u |

1

2

3

4

5

6

7

8

For 16 O of material 1, the MCNP code will use the neutron, proton, and
photonuclear cross-section data files, O-16.60c , O-16.24h and O-16.24u
, respectively. For 206 Pb of material 1, the MX cards specify that data
file Ra-223.70c will be substituted for Pb-206.60c , Fe-56.70h for
Pb-206.24h , and Pu-239.70u for Pb-206.24u .

## 5.6.4 MPN: Photonuclear Nuclide Selector

## /\_445 Deprecation Notice

DEP-53483

This feature has been replaced by the material card nuclide substitution
( MX ) capability. To control the selection of photonuclear nuclide
data, use the MX card.

## 5.6.5 OTFDB: On-the-fly Doppler Broadening

The MCNP code has a capability for on-the-fly (OTF) Doppler broadening
of neutron cross sections. Background, theory and methodology, and
implementation details are provided in several references [231234].

To use the OTF Doppler broadening, data tables with temperature-fitting
coefficients must first be prepared using the fit \_ otf code. This code
is included in the MCNP distribution in the MCNP \_ CODE/Utilities/FIT \_
OTF directory. Input specifications and examples for running fit \_ otf
are available in §E.3. Running the fit \_ otf code will produce a file of
OTF coefficients in either a binary or a text file format. These files
have names of the form

- Binary: otf \_ 92235.70c.binary , otf \_ 8016.70c.binary , etc.

- Text: otf \_ 92235.70c.txt , otf \_ 8016.70c.txt , etc.

1

The identifier (with suffix) that is part of the file name refers to the
original identifier for the base dataset used as input to fit \_ otf (not
necessarily to the identifier used in an MCNP input file). The files
generated by fit \_ otf for various nuclides should be placed in the
DATAPATH directory or in the working directory. Alternatively, symbolic
links to the files could be placed in the DATAPATH directory, with the
actual files located elsewhere.

The OTFDB card is used to provide the MCNP code with the list of OTF
data files that should be used in a calculation. The table identifier
portion of the file names should be supplied, including the suffix.

## Data-card Form: OTFDB z1 z2 . . . zK

zk are the identifiers for OTF Doppler broadening data tables. These
identifiers may use any format listed in [§1.2.3], so long as they match
the OTF database filename.

In the MCNP input processing, identifiers specified on the material
input ( M ) cards are matched with available identifiers from the OTFDB
card. This is done by decomposing the Z , A , and S of both the M card
input and the OTFDB input. If they match, the OTFDB data replaces the
low-energy portion of the corresponding dataset. Library identifiers are
ignored. The OTFDB data is broadened to the value provided on the TMP
card for each cell that contains the affected material. The TMP value
must be higher than the minimum temperature of the library for all
cells, including void cells and cells with zero importance.

## 5.6.5.1 Example 1

OTFDB

U-235.70c O-16.70c

This input loads the files otf \_ U-235.70c.txt and otf \_ O-16.70c.txt or
their binary equivalent. For all 235 U and 16 O in the problem, the
loaded OTF data will be used to provide temperature dependence.

## 5.6.6 TOTNU: Total Fission

## /warning\_sign Caution

Former MCNP5 users need to be aware that the default behavior of this
card has changed to total ν .

| Data-card Form: TOTNU value   | Data-card Form: TOTNU value   | Data-card Form: TOTNU value                                                                                                                                |
|-------------------------------|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| value                         | If                            | If                                                                                                                                                         |
|                               | value = bl ank                | then use total ν , which samples both prompt and delayed fission neutrons, for all fissionable nuclides for which prompt and delayed values are available. |
|                               | value = NO                    | then use only prompt ν for all fissionable nuclides for which prompt values are available.                                                                 |

Default: If the TOTNU card is absent or if a TOTNU card is present but
has no entry after it ( value is not specified), total ν , which samples
both prompt and delayed fission neutrons, is used for all fissionable
nuclides

for which prompt and delayed values are available. Thus, the TOTNU card
is not needed unless only prompt ν is desired.

Use: Needed to specify use of only prompt ν . A TOTNU card with NO as
the value causes prompt ν to be used for all fissionable nuclides for
which prompt values are available, ignoring delayed neutrons from
fission.

## 5.6.7 NONU: Disable Fission

The NONU card provides the ability to disable fission in a cell. The
fission is then treated as simple capture and is accounted for on the
loss side of the problem summary as the 'Loss to fission' entry. The
NONU card is not allowed in a restarted calculation.

| Cell-card Form: NONU = a or Data-card Form: NONU a1 a2 . . . aJ   | Cell-card Form: NONU = a or Data-card Form: NONU a1 a2 . . . aJ          | Cell-card Form: NONU = a or Data-card Form: NONU a1 a2 . . . aJ                           |
|-------------------------------------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| a                                                                 | If                                                                       | If                                                                                        |
|                                                                   |                                                                          | a = 0 then fission in cell treated as capture; gammas produced.                           |
|                                                                   |                                                                          | a = 1 then fission in cell treated as real; gammas produced.                              |
|                                                                   |                                                                          | a = 2 then fission in cell treated as capture; gammas not produced ( 1 ).                 |
|                                                                   |                                                                          | blank then fission in the cells is treated like capture; gammas produced (i.e., a = 0 ).  |
| aj                                                                | Number of entries equals the number of cells unless no entry appears. If | Number of entries equals the number of cells unless no entry appears. If                  |
|                                                                   |                                                                          | aj = 0 then fission in cell treated as capture; gammas produced.                          |
|                                                                   |                                                                          | aj = 1 then fission in cell treated as real; gammas produced.                             |
|                                                                   |                                                                          | aj = 2 then fission in cell treated as capture; gammas not produced ( 1 ).                |
|                                                                   |                                                                          | blank then fission in the cells is treated like capture; gammas produced (i.e., aj = 0 ). |

Default: If the NONU card is absent, fission is treated as real fission
( aj = 1 ). If the card is present but without entries, fission is
treated as capture with gammas produced ( aj = 0 ).

Use: Needed with SSR for fissioning neutron problems only. When fission
is already modeled in the source, such as SSR , it should not be
duplicated in transport and should be turned off with NONU . Use aj = 2
.

## Details:

- 1 Note 1: An aj value of 2 treats fission as capture and, in addition, no fission gamma rays are produced. This option should be used with KCODE fission source problems written to surface source files. Suppressing the creation of new fission neutrons and photons is necessary because they are already accounted for in

the source. Consider a problem with a fixed source in a multiplying
medium. For example, an operating reactor power distribution could be
specified as a function of position in the core either by an SDEF source
description or by writing the fission source from a KCODE calculation to
a WSSA file with a CEL option on an SSW card. Without the ability to
turn off fission, the nonKCODE calculation would be impossible to run
because of the criticality of the system and because fission neutrons
have already been accounted for. Using the NONU card in the nonKCODE
mode allows this problem to run correctly by treating fission as simple
capture.

## 5.6.8 AWTAB: Atomic Weight

Entries on this card override the existing atomic weight ratios as
contained in both the xsdir file and the cross-section tables. The AWTAB
card is needed when atomic weights are not available in an xsdir file.

```
Data-card Form: AWTAB z1 a1 z2 a2 . . . zK aK zk Nuclide or element identifier [§1.2.2]. ak Atomic weight ratios.
```

Default: If the AWTAB card is absent, the atomic weight ratios from the
xsdir file and cross-section tables are used.

Use: Discouraged. Occasionally useful when XS card introduces rare
isotopes.

## /warning\_sign Caution

Using atomic weight ratios different from the ones in the cross-section
tables in a neutron problem can lead to negative neutron energies that
will cause the problem to terminate prematurely.

## 5.6.9 XS: Cross-Section File

The XS n card can be used to load cross-section evaluations not listed
in the xsdir file. The XS n cards can be used in addition to the xsdir
file. Each XS n card describes one cross-section table. The entries for
the XS n card are identical to those that appear in the default cross-
section directory file (i.e., xsdir \_ mcnp6.3 , see Appendix B), except
that the ' + ' is not used for continuation.

| Data-card Form: XS n z1 a1 z2 a2 . . .   | Data-card Form: XS n z1 a1 z2 a2 . . .                                                             |
|------------------------------------------|----------------------------------------------------------------------------------------------------|
| n                                        | Arbitrary cross-section identification number. Restriction: 1 ≤ n ≤ 99 , 999 , 999 .               |
| zk                                       | Full table identifier [§1.2.3] used on the M material card. All target formats are allowed.        |
| ak                                       | Atomic weight ratio associated with nuclide k .                                                    |
| . . .                                    | Remaining xsdir file entries for the user-provided cross-section table as described in Appendix B. |

Use: Add an xsdir -type entry for nuclides not represented in the xsdir
file.

## 5.6.10 VOID: Material Void

## Data-card Form: VOID c1 c2 . . .

cj

The list of cells to treat as void.

Default: Use problem materials.

Use: Debugging geometry and calculating volumes stochastically.

## Details:

<!-- image -->

- 1 When the VOID card is blank, the material number and density is set to zero for all cells, FM cards are turned off, heating tallies are turned into flux tallies, and, if there is no NPS card, the effect of an NPS 100000 card is created. If there is a TALLYX subroutine, it may need to be changed, too.
- 2 Entries on the VOID card selectively set the material number and density to zero for the specified cells. Can be used to check whether the presence of some object in your geometry makes a significant difference in the results.

<!-- image -->

## 5.6.11 MGOPT: Multigroup Adjoint Transport Option

- ' J ' is not an acceptable value for any of the MGOPT card parameters. Further, mcal and igm must be specified.

| Data-card Form: MGOPT mcal igm iplt isb icw fnw rim   | Data-card Form: MGOPT mcal igm iplt isb icw fnw rim                                                                                              | Data-card Form: MGOPT mcal igm iplt isb icw fnw rim                                                                                                                                                                    |
|-------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| mcal                                                  | Setting mcal to F specifies a forward problem and setting mcal to A specifies an adjoint problem ( 2 ).                                          | Setting mcal to F specifies a forward problem and setting mcal to A specifies an adjoint problem ( 2 ).                                                                                                                |
| igm                                                   | The total number of energy groups for all kinds of particles in the problem. A negative total indicates a special electron-photon problem ( 3 ). | The total number of energy groups for all kinds of particles in the problem. A negative total indicates a special electron-photon problem ( 3 ).                                                                       |
| iplt                                                  | Indicator of how weight windows are to be used. If                                                                                               | Indicator of how weight windows are to be used. If                                                                                                                                                                     |
| iplt                                                  | iplt = 0                                                                                                                                         | then IMP values set cell importance. Weight windows, if any, are ignored for cell importance splitting and Russian roulette. (DEFAULT)                                                                                 |
| iplt                                                  | iplt = 1                                                                                                                                         | then weight windows must be provided and are transformed into energy-dependent cell importance. A zero weight-window lower bound produces an importance equal to the lowest non-zero importance for that energy group. |
| iplt                                                  | iplt = 2                                                                                                                                         | then weight windows do what they normally do.                                                                                                                                                                          |
| isb                                                   | Controls adjoint biasing for adjoint problems; valid only for mcal is A . If                                                                     | Controls adjoint biasing for adjoint problems; valid only for mcal is A . If                                                                                                                                           |
| isb                                                   | isb = 0                                                                                                                                          | then collisions are biased by infinite-medium fluxes. (DEFAULT)                                                                                                                                                        |
| isb                                                   | isb = 1                                                                                                                                          | then collisions are biased by functions derived from weight windows, which must be supplied.                                                                                                                           |

glyph[negationslash]

<!-- image -->

|     | isb = 2                                                                                                                                                                                                                                                                            | then collisions are not biased.                                                                                                                                                                                                                                                    |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| icw | Name of the reference cell for generated weight windows. If                                                                                                                                                                                                                        | Name of the reference cell for generated weight windows. If                                                                                                                                                                                                                        |
|     | icw = 0                                                                                                                                                                                                                                                                            | then weight windows are not generated. (DEFAULT)                                                                                                                                                                                                                                   |
|     | icw = 0                                                                                                                                                                                                                                                                            | then volumes must be supplied or calculated for all cells of non-zero importance.                                                                                                                                                                                                  |
| fnw | Normalization value for generated weight windows. The value of the weight-window lower bound in the most important energy group in cell icw is set to fnw . (DEFAULT: fnw = 1 )                                                                                                    | Normalization value for generated weight windows. The value of the weight-window lower bound in the most important energy group in cell icw is set to fnw . (DEFAULT: fnw = 1 )                                                                                                    |
| rim | Compression limit for generated weight windows. Before generated weight windows are printed out, the weight windows in each group separately are checked to see that the ratio of the highest to the lowest is less than rim . If not, they are compressed. (DEFAULT: rim = 1000 ) | Compression limit for generated weight windows. Before generated weight windows are printed out, the weight windows in each group separately are checked to see that the ratio of the highest to the lowest is less than rim . If not, they are compressed. (DEFAULT: rim = 1000 ) |

Use: Required for neutron multigroup calculations.

## Details:

- 1 Presently, the standard MCNP6 multigroup neutron cross sections are given in 30 groups and photons are given in 12 groups. Thus, an existing continuous-energy input file can be converted to a multi-group input file simply by adding one of the following cards:

1

2

3

<!-- image -->

- 2 An input file for an adjoint problem can have both an IMP card and weight-window cards ( iplt = 0 and isb = 1 ). The entries on the weight-window cards are not weight windows in the normal sense but biasing functions. If iplt = 1 , the values on a weight-window card become energy-dependent cell importance.
- 3 A negative igm value allows a single cross-section table to include data for more than one sort of particle. This feature applies currently to electron/photon multigroup calculations only. A problem with 50 electron groups followed by 30 photon groups in one table would have igm = -80 . Also, all tables must have the same group structure. A negative igm value will use the energy variable on the source or tally card as groups index unless it is associated with a distribution. For an energy distribution on the source card, there should be igm increasing integer entries for each group on the SI card. On a tally energy card, if there are fewer than igm entries, they will be taken as energies in MeV; otherwise, the bins will be according to group index. The particles can be separated in tallies by using the PTT keyword on the FT n tally special treatment card.

## 5.6.12 DRXS: Discrete-Reaction Cross Section

If the necessary discrete data are available, nuclides listed on the
optional DRXS card are given a discrete energy treatment instead of the
regular fully continuous-energy cross-section treatment.
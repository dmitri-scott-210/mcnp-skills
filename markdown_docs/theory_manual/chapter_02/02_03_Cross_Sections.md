---
title: "Chapter 2.3 - Cross Sections"
chapter: "2.3"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/2_Geometry,_Data,_Physics,_and_Mathematics/2.3_Cross_Sections.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

<!-- image -->

3

Figure 2.4: Demonstration of periodic boundary conditions.

The negative entries before the surface mnemonics specify periodic
boundaries. Card one says that surface 1 is periodic with surface 2 and
is a px plane. Card two says that surface 2 is periodic with surface 1
and is a px plane. Card three says that surface 3 is periodic with
surface 4 and is a py plane. Card four says that surface 4 is periodic
with surface 3 and is a py plane. Card five says that surface 5 is an
infinite cylinder parallel to the z axis. A particle leaving the lattice
out the left side (surface 1) reenters on the right side (surface 2). If
the surfaces were reflecting, the reentering particle would miss the
cylinder, shown by the dotted line. In a fully specified lattice and in
the periodic geometry, the re-entering particle will hit the cylinder as
it should.

Much more complicated examples are possible, particularly hexagonal
prism lattices. In all cases, the MCNP code checks that the periodic
surface pair matches properly and performs all the necessary surface
rotations and translations to put the particle in the proper place on
the corresponding periodic plane.

The following limitations apply:

- Periodic boundaries cannot be used with next-event estimators such as detectors or DXTRAN [§2.5.6.4.2];
- All periodic surfaces must be planes;
- Periodic planes cannot also have a surface transformation;
- The periodic cells may be infinite or bounded by planes on the top or bottom that must be reflecting or white boundaries but not periodic;
- Periodic planes can only bound other periodic planes or top and bottom planes;
- A single zero-importance cell must be on one side of each periodic plane; and
- All periodic planes must have a common rotational vector normal to the geometry top and bottom.

## 2.3 Cross Sections

The MCNP code package is incomplete without the associated nuclear data
tables. The kinds of tables available and their general features are
outlined in this section. The manner in which information contained on
nuclear data tables is used in the MCNP code is described in §2.4.

There are two broad objectives in preparing nuclear data tables for the
MCNP code. First, the data available to the MCNP code should reproduce
the original evaluated data as much as is practical. Second, new data
should be brought into the MCNP package in a timely fashion, thereby
giving users access to the most recent evaluations. The nuclear data
needed by the MCNP code are available at the LANL nuclear data website
https://nucleardata.lanl.gov .

Ten classes of data tables exist for the MCNP code. They are:

1. continuous-energy neutron interaction data;
2. discrete reaction neutron interaction data;
3. continuous-energy photoatomic interaction data;
4. continuous-energy photonuclear interaction data;
5. neutron dosimetry cross sections;
6. neutron S ( α, β ) thermal data;
7. multigroup neutron, coupled neutron/photon, and charged particles masquerading as neutrons;
8. multigroup photon;
9. electron interaction data; and
10. charged particle interaction data.

In a given simulation, one typically needs data for every projectile-
target pair. For nuclear reactions, targets need to be specified at the
nuclide or isomer level. This is the case for neutron interactions,
charged particle interactions, and photonuclear interactions. For atomic
reactions such as electron or photoatomic, targets need to be specified
on the atomic level. The code can convert a nuclide specification to
atomic automatically. Finally, for neutron thermal scattering, the
target is the atom within the molecule of interest. For example, water
can have 1 H, 2 H, 3 H, 16 O, 17 O, and 18 O as nuclear targets, H and O
as atomic targets, and H within H 2 O and O within H 2 O as thermal
scattering targets.

## /warning\_sign Caution

Some historical data libraries provide 'elemental' nuclear data, in
which each nuclide is not cleanly separated out. In general, these
datasets are of lower quality than using separate nuclear data for each
target and should be avoided.

The means of selecting each class of data through MCNP input is
described next. In the remainder of this section, the characteristics of
each class of data such as evaluated sources, processing tools,
differences between data on the original evaluation and on the MCNP data
tables, are described and some hints are provided on how to select the
appropriate data tables.

## 2.3.1 Dataset Selection

The MCNP code needs data tables for a wide variety of physics within the
simulation. Most of the data available to the MCNP code is listed in a
file called the xsdir ('cross section directory'). This file contains a
list of table identifiers [§1.2.3], information on where they are stored
on disk, and a few physical parameters the code needs to work. Further
information on the xsdir file can be found in Appendix B.

Through the combination of material specification cards ( M , MT , MX )
and physics options ( MODE , PHYS ), the code builds up a list of
datasets it needs to load. This list contains target information,
physics identifiers, and library identifiers if provided. It then scans
through the xsdir for tables that match all input information. The first
match in the xsdir is used. If a dataset is not found, the code will
report an error.

The target information is not quite the target identifier described in
§1.2.2. When loading nuclear data, the target is decomposed into its
constituent Z , A , and S values and comparisons are performed with
these. When loading atomic data, the target is also decomposed into Z ,
A , and S , but when searching, A and S are

set to zero. All currently known available data follows this convention
for atomic data. Finally, for neutron thermal scattering, the precise
target identifier string is searched for (case insensitive).

This approach has a notable property in that target identifier formats
are interchangeable. For example, U-238 will match the table 92238 and
vice versa. This was done to allow the more modern formats to be used to
access data provided in older formats.

By convention, only one dataset with a given combination of target
information ( Z , A , S for nuclear/atomic data, name for S ( α, β ) ),
physics identifier, and library identifier should be present in the
xsdir so that the combination is unique. There may be multiple libraries
with a given set of target information and physics identifier made
distinct by the library identifier.

## 2.3.2 Neutron Interaction Data: Continuous-energy and Discrete-reaction

In neutron problems, one neutron interaction table is required for each
isotope (or element if using the older 'elemental' tables) in the
problem. Continuous-energy tables use a physics identifier of c , and
the discrete reaction tables use d .

For most materials, there are many cross-section sets available
(represented by different library identifiers) because of multiple
sources of evaluated data and different parameters used in processing
the data. An evaluated nuclear data set is produced by analyzing
experimentally measured cross sections and combining those data with the
predictions of nuclear model calculations in an attempt to extract the
most accurate interaction description. Preparing evaluated cross-section
sets has become a discipline in itself and has developed since the early
1960s. In the US, researchers at many of the national laboratories as
well as several industrial firms are involved in such work. The American
evaluators joined forces in the mid-1960s to create the national ENDF
system [44].

There has been some confusion due to the use of the term ENDF to refer
to both a library and a format. The US effort to create a national
evaluated nuclear data library led to formation of the Cross Section
Evaluation Working Group (CSEWG) in the 1960s. This body standardized
the ENDF format, which is used to store evaluated nuclear data files,
and created the US ENDF/B library that contains the set of data
evaluations currently recommended by CSEWG. Each update of the ENDF/B
library receives a unique identifier (discussed below). While ENDF began
as a US effort, over time other data centers have adopted the ENDF
storage format for their own use (this international standardization has
encouraged and facilitated many collaborations). The ENDF-6 format [45]
(note that the Arabic number 6 indicates the ENDF format version) has
become the international standard for storing evaluated nuclear data and
is used by data centers in Europe, Japan, China, Russia, Korea and
elsewhere. The user should be aware that there are many evaluated
nuclear data libraries of which ENDF/B is only one.

It is worth discussing the ENDF/B library for a moment. The US-based
CSEWG meets once a year to discuss and approve changes to the ENDF/B
library. In order to track the updates to the ENDF/B library, the
following notation has been adopted. The '/B' in ENDF/B is used to
indicate the US data library as recommended by CSEWG. There was at one
time an ENDF/A that was a repository for other, possibly useful, data.
However, this is no longer used. The major version of the library is
indicated by a Roman numeral, e.g. ENDF/B-V or ENDF/B-VI. Changes in the
major version are generally tied to changes in the standard cross
sections. Many cross-section measurements are made relative to the
standard cross sections, e.g. elastic scattering off hydrogen or the 235
U(n,f) cross section. When one of the standard cross sections is
changed, the evaluated data that were based on that standard must be
updated. Within a major release, revisions are generally indicated as
ENDF/B-VI.2 or ENDF/B-VI.6 where the '.2' and '.6' indicate release 2
and release 6, respectively. A release indicates that some evaluations
have been revised, added or deleted. Users should note that neither a
major release nor an interim release guarantee that a particular
evaluation has been updated. In fact, only a few evaluations change in
each release and often the change is limited to a certain energy region.
This numbering scheme simply indicates that something within the data
library

has changed. It is up to the user to read the accompanying documentation
to determine exactly what, if anything, changed. Each ACE table provided
with the MCNP package is listed in [46] where its lineage (e.g.
ENDF/B-V.0 or ENDF/B-VI.2) is given. The ENDF/B evaluations are
available through the National Nuclear Data Center at Brookhaven
National Laboratory [http://www.nndc.bnl.gov/].

In addition to the ENDF/B library, many other data centers provide
libraries of evaluated data. These include the Japanese Atomic Energy
Research Institute's (JAERI) JENDL library, the European JEFF library
maintained by the Nuclear Energy Agency (NEA), the Chinese Nuclear Data
Center's (CNDC) CENDL library, and the Russian BOFOD library. Other
libraries also exist. These centers may provide processed versions of
their library in MCNP ACE format. Contact the appropriate center for
more information.

In recent years the primary evaluated source of neutron interaction data
provided as part of the MCNP code package has been the ENDF/B library
(i.e. ENDF/B-V and ENDF/B-VI). However, these have been supplemented
with evaluated neutron interaction data tables from other sources, in
particular data from Lawrence Livermore National Laboratory's Evaluated
Nuclear Data Library (ENDL) library [6] and supplemental evaluations
performed in the Nuclear Physics Group in the Theoretical Division at
Los Alamos [9-11]. The package also includes older evaluations from
previous versions of ENDF/B, ENDL, the Los Alamos Master Data File [47],
and the Atomic Weapons Research Establishment in Great Britain.

The MCNP code does not access evaluated data directly from the ENDF
format; these data must first be processed into ACE format. The very
complex processing codes used for this purpose include NJOY [13, 14] for
evaluated data in ENDF format and MCPOINT [48] for evaluated data in the
ENDL format.

Data on the MCNP neutron interaction tables include cross sections and
emission distributions for secondary particles. Cross sections for all
reactions given in the evaluated data are specified. For a particular
table, the cross sections for each reaction are given on one energy grid
that is sufficiently dense that linear-linear interpolation between
points reproduces the evaluated cross sections within a specified
tolerance. Over the years this tolerance has been tightened as computer
memory has increased. In general, the tables currently available have
cross sections that are reproduced to a tolerance of 1% or less,
although many recent tables have been created with tolerances of 0.1%.
Depending primarily on the number of resolved resonances for each
isotope, the resulting energy grid may contain up to ≈ 100,000 points
(see [46] for information about specific tables).

Angular distributions for neutron (and photonuclear) collisions are
given in each table for all reactions emitting neutrons or photons (note
that older neutron tables may not include photon distributions). The
distributions are typically given in the center-of-mass system for
elastic scattering and discrete-level inelastic scattering. Other
distributions may be given in either the center-of-mass or laboratory
system as specified by the ENDF-6 scattering law from which they are
derived. Angular distributions are given on a reaction-dependent grid of
incident energies.

The sampled angle of scattering uniquely determines the secondary energy
for elastic scattering and discretelevel inelastic scattering. For other
inelastic reactions, energy distributions of the scattered particles are
provided in each table. As with angular distributions, the energy
distributions are given on a reactiondependent grid of incident
energies. The energy and angle of particles scattered by inelastic
collisions is sampled in a stochastic manner such that the overall
emission distribution and energy are preserved for many collisions but
not necessarily for any single collision.

When neutron evaluations contain data about secondary photon production,
that information appears in the MCNP neutron interaction tables. Many
processed data sets contain photon production cross sections, photon
angular distributions, and photon energy distributions for each neutron
reaction that produces secondary photons. However, the user should be
aware that not all evaluations include this information and the
information is sometimes approximate, e.g. individual gamma lines may be
lumped into average photon emission bins.

Other miscellaneous information on the neutron (and photonuclear)
interaction tables includes the atomic weight ratio of the target
nucleus, the Q -values of each reaction, and ν data (the average number
of neutrons per fission) for fissionable isotopes. In many cases both
prompt and total ν are given. Total ν is the default and the TOTNU card
can be used to change the default.

Approximations must be made when processing an evaluated data set into
ACE format. As mentioned above, cross sections are reproduced to within
a certain tolerance, generally less than 1%. Until recently, evaluated
angular distributions for non-isotropic secondary particles could only
be approximated on ACE tables by 32 equally probable cosine bins. This
approximation is extremely fast to use but may not adequately represent
a distribution originally given as a 20 th -order Legendre polynomial.
Starting with the MCNP code, version 4C, tabular angular distributions
may be used to represent the scattering angle with a tolerance generally
between 0.1% to 1% or better. On the whole, the approximations within
more recent ACE tables are small, and MCNP interaction data tables for
neutron (and photonuclear) collisions are extremely faithful
representations of the original evaluated data.

Discrete-reaction tables are identical to continuous-energy tables
except that in the discrete reaction tables all cross sections have been
averaged into 262 groups. The averaging is done with a flat weighting
function. This is not a multigroup representation; the cross sections
are simply given as histograms rather than as continuous curves. The
remaining data (angular distributions, energy distributions, ν , etc.)
are identical in discrete-reaction and continuous-energy neutron tables.
Discrete-reaction tables have been provided in the past as a method of
shrinking the required data storage to enhance the ability to run the
MCNP code on small machines or in a time-sharing environment. Given the
advances in computing speed and storage, they are no longer necessary
and should not be used. There original purpose was for preliminary
scoping studies. They were never recommended as a substitute for the
continuous-energy tables when performing final calculations.

Careful users will want to think about what neutron interaction tables
to choose. There is, unfortunately, no strict formula for choosing the
tables. The following guidelines and observations are the best that can
be offered:

1. Users should, in general, use the most recent data available. The nuclear data evaluation community works hard to continually update these libraries with the most faithful representations of the cross sections and emission distributions.
2. Consider checking the sensitivity of the results to various sets of nuclear data. Try, for example, a calculation with ENDF/B cross sections, and then another with ENDL cross sections. If the results of a problem are extremely sensitive to the choice of nuclear data, it is advisable to find out why.
3. Consider differences in evaluators' philosophies. The Physical Data Group at Livermore is justly proud of its extensive cross-section efforts; their evaluations manifest a philosophy of reproducing the data with the fewest number of points. Livermore evaluations are available mainly in the '.40C' series. We at Los Alamos are particularly proud of the evaluation work being carried out in the Nuclear Data team; generally, these evaluations are the most complex because they are the most thorough.
4. Be aware of the neutron energy spectrum in your problem. For high-energy problems, the 'thinned' and discrete reaction data are probably not bad approximations. Conversely, it is essential to use the most detailed continuous-energy set available for problems influenced strongly by transport through the resonance region.
5. Check the temperature at which various data tables have been processed. Do not use a set that is Doppler broadened to 3,000 K for a room temperature calculation.
6. For a coupled neutron/photon problem, be careful that the tables you choose have photon production data available. If possible, use the more-recent sets that have been processed into expanded photon production format.

7. Users should be aware of the differences between the '.50C' series of data tables and the '.51C' series. Both are derived from ENDF/B-V. The '.50C' series is the most faithful reproduction of the evaluated data. The '.51C' series, also called the 'thinned' series, has been processed with a less rigid tolerance than the '.50C' series. As with discrete reaction data tables, although not to the same extent, users should be careful when using the 'thinned' data for transport through the resonance region.
8. In general, use the best data available. It is understood that the latest evaluations tend to be more complex and therefore require more memory and longer execution times. If you are limited by available memory, try to use smaller data tables such as thinned or discrete-reaction for the minor isotopes in the calculation. Discrete reaction data tables might be used for a parameter study, followed by a calculation with the full continuous-energy data tables for confirmation.

In conclusion, the additional time necessary to choose appropriate
neutron interaction data tables rather than simply to accept the
defaults often will be rewarded by increased understanding of your
calculation.

## 2.3.3 Photon Interaction Data

Photon interaction cross sections are required for all photon problems.
Photon interactions can now account for both photoatomic and
photonuclear events. Because these events are different in nature, i.e.
elemental versus isotopic, the data are stored on separate tables.
Photoatomic data are stored on ACE tables that use the physics
identifier p .

The '01p' ACE tables were introduced in 1982 and combine data from
several sources. The incoherent, coherent, photoelectric and pair
production cross sections, the coherent form factors, and incoherent
scattering function for this data set come from two sources. For Z equal
to 84, 85, 87, 88, 89, 91, and 93, these values are based on the
compilation of Storm and Israel [49] and include data for incident
photon energies from 1 keV to 15 MeV. For all other elements from Z
equal to 1 through 94, the data are based on ENDF/B-IV33 and include
data for incident photon energies from 1 keV to 100 MeV. Fluorescence
data for Z equal to 1 through 94 are taken from work by Everett and
Cashwell [50] as derived from multiple sources.

The '02p' ACE tables were introduced in 1993 and are an extension of the
'01p' to higher incident energies [51]. Below 10 MeV the data are
identical to the '01p' data (i.e. the cross sections, form factors,
scattering function, and fluorescence data in this region are
identical). From 10 MeV to the top of the table (either 15 or 100 MeV,
depending on the table) the cross-section values are smoothly
transitioned from the '01p' values to the values from the Livermore
Evaluated Photon Data Library (EPDL89) [7]. Above this transition
region, the cross section values are derived from the EPDL89 data and
are given for incident energies up to 100 GeV. The pair production
threshold was also corrected for some tables.

The '03p' ACE tables were introduced in 2002 and are an extension of the
'02p' tables to include additional data. The energy of a photon after an
incoherent (Compton) collision is a function of the momentum of the
bound electron involved in the collision. To calculate this effect
(which is seen as a broadening of the Compton peak), it is necessary to
know the probability with which a photon interacts with an electron from
a particular shell and the momentum profile for the electrons of each
shell. The probabilities and momentum profile data of Biggs et al. [52]
are included in the '03p' tables. All other data in the '03p' are
identical to the '02p' data. The ability to use the new data for
broadening of the Compton scattering energy requires MCNP5 or later;
however, these tables are compatible with older versions of the code
(you simply will not access or use the new data).

The '04p' ACE tables were introduced in 2002 and contain the first
completely new data set since 1982. These tables were processed from the
ENDF/B-VI.8 library. The ENDF/B-VI.8 photoatomic and atomic relaxation
data are in turn based upon the EPDL97 [53] library. They include
incoherent, coherent, photoelectric and pair production cross sections
for incident energies from 1 keV to 100 GeV and Z equal to 1 to 100.
They

also include coherent form factors, incoherent scattering functions, and
fluorescence data derived from the ENDF/B-VI.8 data. It should be noted
that the form factor and scattering data have been evaluated and are
hard-coded in the MCNP code (in the GETXST subroutine). The fluorescence
data use the traditional scheme defined by Everett and Cashwell [50] but
updated and consistent with the new data. Also included are the bound
electron momenta of Biggs et al. [52] (i.e. identical to those data in
the '03p' tables). This is the recommended data set. More information on
the '04p' ACE tables can be found in [54].

For each element the photoatomic interaction libraries contain an energy
grid-explicitly including the photoelectric edges and the pair
production threshold-the incoherent, coherent, photoelectric and pair
production cross sections (all stored as the logarithm of the value to
facilitate log-log interpolation). The total cross section is not
stored; instead it is calculated from the partial cross sections as
needed. The energy grid for each table is tailored specifically for that
element. The average material heating due to photon scattering is
calculated by the processing code and included as a tabulation on the
main energy grid. The incoherent scattering function and coherent form
factors are tabulated as a function of momentum transfer on a
predefined, fixed-momenta grid. Average fluorescence data (according to
the scheme of Everett and Cashwell [50]) are also included. The most
recent data (on the 03p and 04p libraries) also include momentum profile
data for broadening of the photon energy from Compton scattering from
bound electrons.

The determination of directions and energies of atomically scattered
photons requires information different from the sets of angular and
energy distributions found on neutron interaction tables. The angular
distribution for fluorescence x-rays from the relaxation cascade after a
photoelectric event is isotropic. The angular distributions for coherent
and incoherent scattering come from sampling the well-known Thomson and
Klein-Nishina formulas, respectively. By default, this sampling accounts
for the form factor and scattering function data at incident energies
below 100 MeV. Above, 100 MeV (or at the user's request) the form factor
and scattering function data are ignored (a reasonable approximation for
high-energy photons). The energy of an incoherently scattered photon is
calculated from the sampled scattering angle. If available, this energy
is modified to account for the momentum of the bound electron.

Very few approximations are made in the various processing codes used to
transfer photon data from ENDF into the format of MCNP photon
interaction tables. Cross sections are reproduced exactly as given
(except as the logarithm of the value). Form factors and scattering
functions are reproduced as given; however, the momentum transfer grid
on which they are tabulated may be different from that of the original
evaluation. Heating numbers are calculated values, not given in
evaluated sets, but inferred from them. Fluorescence data are calculated
using the scheme developed by Everett and Cashwell [50].

Photonuclear data tables use the physics identifier u . Photon
interactions can include photonuclear events. Early data distribution
included tables for only 13 nuclides. Because of this, photonuclear
physics must be explicitly turned on. If on, a table must be provided
for each nuclide of every material or a fatal error will occur and the
simulation will not run. Around 2000, more than 150 other photonuclear
data evaluations were created as part of an IAEA collaboration [55].
Around 2020, evaluations for 219 nuclides became available through the
IAEA's Nuclear Data Services website (https://www-
nds.iaea.org/photonuclear) [56].

Photonuclear interaction data describe nuclear events with specific
isotopes. The reaction descriptions use the same ENDF-6 format as used
for neutron data. Their processing, storage as ACE tables, and sampling
in a simulation are completely analogous to what is done for neutrons.
See the previous discussion of the neutron data for more details. Note
that the photonuclear data available so far are complete in the sense
that they provide secondary particle distributions for all light-
particles, i.e. photons, neutrons, protons, alphas, etc. At this time,
the MCNP code makes use of the photon and neutron emission
distributions.

The selection of photon interaction data has become more complicated.
Let us first examine the simple cases. Photon or photon/electron
problems where photonuclear events are to be ignored (i.e. photonuclear
physics is explicitly off) should specify the material composition on
the M n card by mass or weight fraction of each element, i.e. setting A
= 0 as shown in §1.2.2. The next most simple case is a coupled neutron-
photon problem that will explicitly ignore photonuclear events. In this
case, one should specify the material composition

according to the rules discussed in the previous section on neutron data
tables. Given an isotopic material component, e.g. Al-27, the
appropriate elemental photoatomic table will be selected, e.g. Al-0. If
no evaluation identifier is given, the default (first) table from the
xsdir file will be used. If a particular evaluation set is desired, the
PLIB option on the M n card may be used to select all photoatomic tables
from a given library. It is recommended in all cases that the
photoatomic tables for any given problem all be from the same library
(these data sets are created in masse and thus are self-consistent
across a library).

The most complicated case for material definition is the selection of
tables for coupled neutron-photon problems where photonuclear events are
not ignored. In such a case, the composition must be chosen based on the
availability of most appropriate isotopic neutron and photonuclear
tables as needed for the specific problem at hand. The MX n card may be
used to accommodate mismatches in the availability of specific isotopes
[§5.6.3]. As always, a fully specified identifier, e.g. Al-27.24u , will
ensure that a specific table is selected. The PNLIB option on the
material card may be used to select all photonuclear tables from a
specific library. Otherwise, the code will select the first match in the
xsdir file. Note that if no photonuclear table is available for the
given target, the problem will report the error and will not run. See
the discussion in the description of the MX n card for more information
[§5.6.3].

## 2.3.4 Electron Interaction Data

Electron interaction data tables are required both for problems in which
electrons are actually transported, and for photon problems in which the
thick-target bremsstrahlung model is used. Electron data tables use the
physics identifier e , and are selected by default when the problem mode
requires them. There are two electron interaction data libraries: el
(data suffix of .01e) and el03 (data suffix of .03e).

The electron libraries contain data on an element-by-element basis for
atomic numbers from Z equal 1 to 94. The library data contain energies
for tabulation, radiative stopping power parameters, bremsstrahlung
production cross sections, bremsstrahlung energy distributions, K-edge
energies, Auger electron production energies, parameters for the
evaluation of the Goudsmit-Saunderson theory for angular deflections
based on the Riley cross-section calculation, and Mott correction
factors to the Rutherford cross sections also used in the Goudsmit-
Saunderson theory. The el03 library also includes the atomic data of
Carlson used in the density effect calculation. Internal to the code at
run-time, data are calculated for electron stopping powers and ranges, K
x-ray production probabilities, knock-on probabilities, bremsstrahlung
angular distributions, and the Landau-Blunck-Leisegang theory of energy-
loss fluctuations. The el03 library is derived from the ITS3.0 code
system [57]. Discussions of the theoretical basis for these data and
references to the relevant literature are presented in [§2.4.5].

The hierarchy rules for electron cross sections require that each
material must use the same electron library. If a specific library
identifier is selected on a material card, that choice of library will
be used as the default for all elements in that material. Alternatively,
the default electron library for a given material can be chosen by
specifying the ELIB option on the M card. In the absence of any
specification, the MCNP code will use the first electron data table
listed in the xsdir file for the relevant element.

## /warning\_sign Caution

Under no circumstances should data tables from different libraries be
specified for use in the same material (e.g., "m6 12000.01e 1 20000.03e
1" should not be used). This will result in a fatal error as reported at
run time. Overriding this error with a FATAL option [Table 3.6] will
result in unreliable results.

## 2.3.5 Neutron Dosimetry Cross Sections

Dosimetry cross-section tables cannot be used for transport through
material. These incomplete cross-section sets provide energy-dependent
neutron cross sections to the MCNP code for use as response functions
with

the FM tally feature, e.g. they may be used in the calculation of a
reaction rate. Identifiers for dosimetry tables have the physics
identifier y . Remember, dosimetry cross-section tables have no effect
on the particle transport of a problem.

The available dosimetry cross sections are from three sources: ENDF/B-V
Dosimetry Tape 531, ENDF/B-V Activation Tape 532, and ACTL [8]-an
evaluated neutron activation cross-section library from the Lawrence
Livermore National Laboratory. Various codes have been used to process
evaluated dosimetry data into the format of MCNP dosimetry tables.

Data on dosimetry tables are simply energy-cross-section pairs for one
or more reactions. The energy grids for all reactions are independent of
each other. Interpolation between adjacent energy points can be
specified as histogram, linear-linear, linear-log, log-linear, or log-
log. With the exception of the tolerance involved in any reconstruction
of point-wise cross sections from resonance parameters, evaluated
dosimetry cross sections can be reproduced on the MCNP data tables with
no approximation.

When specifying a dosimetry dataset on a material card, the full
specifier must be used including the library identifier. There are no
defaults for dosimetry tables. The code will prevent materials with
dosimetry data from being used in the geometry. These materials can only
be used as the multiplier in FM cards.

## 2.3.6 Neutron Thermal S ( α, β ) Tables

Thermal S ( α, β ) tables are not required, but they are essential to
get correct answers in problems involving neutron thermalization. The
thermal scattering library based on ENDF/V-VIII.0 provides the material
identifiers for use on the MT n card(s). The data on these material
identifier tables encompass those required for a complete representation
of thermal neutron scattering by molecules and crystalline solids. The
source of S ( α, β ) data is a special set of ENDF tapes [58]. The
THERMR and ACER modules of the NJOY [13, 14] system have been used to
process the evaluated thermal data into a format appropriate for the
MCNP code.

Data are for neutron energies generally less than 4 eV. Cross sections
are tabulated on table-dependent energy grids; inelastic scattering
cross sections are always given and elastic scattering cross sections
are sometimes given. Correlated energy-angle distributions are provided
for inelastically scattered neutrons. A set of equally probable final
energies is tabulated for each of several initial energies. Further, a
set of equally probable cosines or cosine bins is tabulated for each
combination of initial and final energies. Elastic scattering data can
be derived from either an incoherent or a coherent approximation. In the
incoherent case, equally probable cosines or cosine bins are tabulated
for each of several incident neutron energies. In the coherent case,
scattering cosines are determined from a set of Bragg energies derived
from the lattice parameters. During processing, approximations to the
evaluated data are made when constructing equally probable energy and
cosine distributions.

## 2.3.7 Multigroup Tables

Multigroup cross-section libraries are the only libraries allowed in
multi-group/adjoint problems. Neutron multigroup problems cannot be
supplemented with S ( α, β ) thermal libraries; the thermal effects must
be included in the multigroup neutron library. Photon problems cannot be
supplemented with electron libraries; the electrons must be part of the
multigroup photon library. Neutron multigroup data has the m physics
suffix, and photons use g .

Although continuous-energy data are more accurate than multigroup data,
the multigroup option is useful for a number of important applications:
(1) comparison of deterministic ( S N ) transport codes to Monte Carlo;
(2) use of adjoint calculations in problems where the adjoint method is
more efficient; (3) generation of adjoint importance functions; (4)
cross-section sensitivity studies; (5) solution of problems for which
continuous-cross
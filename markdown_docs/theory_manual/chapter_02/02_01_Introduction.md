---
title: "Chapter 2.1 - Introduction"
chapter: "2.1"
source_pdf: "mcnp631_theory_user-manual/mcnp-theory-manual-chapters/2_Geometry,_Data,_Physics,_and_Mathematics/2.1_Introduction.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## 2.1 Introduction

This chapter discusses the mathematics and physics of the MCNP code,
including geometry, cross-section libraries, sources, variance reduction
schemes, Monte Carlo simulation of particle transport, and tallies. This
discussion is not meant to be exhaustive; many details of the particular
techniques and of the Monte Carlo method itself will be found elsewhere.
Carter and Cashwell's book [17], a good general reference on radiation
transport by Monte Carlo, is based upon what is in the MCNP code.
Another reference is Lux and Koblinger's book [18]. Methods of sampling
from standard probability densities are discussed in the Monte Carlo
samplers by Everett and Cashwell [19].

The MCNP code is currently developed by Monte Carlo Codes Group (XCP-3)
in X-Computational Physics Division (XCP) at Los Alamos National
Laboratory (LANL). The MCNP code development team maintains and improves
the MCNP code, supports and deploys it at LANL and at other Department
of Energy (DOE) laboratories and government agencies where we have
collaborators or sponsors, offers online and in-person MCNP training
classes, and provides limited free consulting and support for MCNP
users. The MCNP code is typically distributed to other users through the
Radiation Safety Information Computational Center (RSICC) at Oak Ridge
National Laboratory ( https://rsicc.ornl.gov ).

The MCNP code is comprised of hundreds of subroutines written in
Fortran, C, and C++. The source code has been made as system independent
as possible to enhance its portability, and follows the Fortran 2018
[20], C 99 [21], and C++ 14 [22] standards. The MCNP code takes
advantage of parallel computer architectures using two parallel models:
task-based threading using the OpenMP model and distributed processing
is supported through the use of the Message Passing Interface (MPI)
model. The MCNP code also combines threading with MPI, but some features
of the code are only available with MPI-based parallelism.

## 2.1.1 History of the Monte Carlo Method and the MCNP Code

The Monte Carlo method is generally attributed to scientists working on
the development of nuclear weapons in Los Alamos during the 1940s.
However, its roots go back much farther.

Perhaps the earliest documented use of random sampling to solve a
mathematical problem was that of Comte de Buffon in 1772 [23]. A century
later people performed experiments in which they threw a needle in a
haphazard manner onto a board ruled with parallel straight lines and
inferred the value of π from observations of the number of intersections
between needle and lines [24, 25]. Laplace suggested in 1786 that π
could be evaluated by random sampling [26]. Lord Kelvin appears to have
used random sampling to aid in evaluating some time integrals of the
kinetic energy that appear in the kinetic theory of gasses [27] and
acknowledged his secretary for performing calculations for more than
5000 collisions [28].

## Chapter 2

## Geometry, Data, Physics, and Mathematics

According to Emilio Segrè, Enrico Fermi's student and collaborator,
Fermi invented a form of the Monte Carlo method when he was studying the
moderation of neutrons in Rome [28, 29]. Though Fermi did not publish
anything, he amazed his colleagues with his predictions of experimental
results. After indulging himself, he would reveal that his 'guesses'
were really derived from the statistical sampling techniques that he
performed in his head when he couldn't fall asleep.

During World War II at Los Alamos, Fermi joined many other eminent
scientists to develop the first atomic bomb. It was here that Stan Ulam
became impressed with electromechanical computers used for implosion
studies. Ulam realized that statistical sampling techniques were
considered impractical because they were long and tedious, but with the
development of computers they could become practical. Ulam discussed his
ideas with others like John von Neumann and Nicholas Metropolis.
Statistical sampling techniques reminded everyone of games of chance,
where randomness would statistically become resolved in predictable
probabilities. It was Nicholas Metropolis who noted that Stan had an
uncle who would borrow money from relatives because he 'just had to go
to Monte Carlo' and thus named the mathematical method 'Monte Carlo'
[29].

Meanwhile, a team of wartime scientists headed by John Mauchly was
working to develop the first electronic computer at the University of
Pennsylvania in Philadelphia. Mauchly realized that if Geiger counters
in physics laboratories could count, then they could also do arithmetic
and solve mathematical problems. When he saw a seemingly limitless array
of women cranking out firing tables with desk calculators at the
Ballistic Research Laboratory at Aberdeen, he proposed [29] that an
electronic computer be built to deal with these calculations. The result
was ENIAC (Electronic Numerical Integrator and Computer), the world's
first computer, built for Aberdeen at the University of Pennsylvania. It
had 18,000 double triode vacuum tubes in a system with 500,000 solder
joints [29].

John von Neumann was a consultant to both Aberdeen and Los Alamos. When
he heard about ENIAC, he convinced the authorities at Aberdeen that he
could provide a more exhaustive test of the computer than mere firing-
table computations. In 1945 John von Neumann, Stan Frankel, and Nicholas
Metropolis visited the Moore School of Electrical Engineering at the
University of Pennsylvania to explore using ENIAC for thermonuclear
weapon calculations with Edward Teller at Los Alamos [29]. After the
successful testing and dropping of the first atomic bombs a few months
later, work began in earnest to calculate a thermonuclear weapon. On
March 11, 1947, John von Neumann sent a letter to Robert Richtmyer,
leader of the Theoretical Division at Los Alamos, proposing use of the
statistical method to solve neutron diffusion and multiplication
problems in fission devices [29]. His letter was the first formulation
of a Monte Carlo computation for an electronic computing machine. In
1947, while in Los Alamos, Fermi invented a mechanical device called
FERMIAC [30] to trace neutron movements through fissionable materials by
the Monte Carlo Method.

By 1948 Stan Ulam was able to report to the Atomic Energy Commission
that not only was the Monte Carlo method being successfully used on
problems pertaining to thermonuclear as well as fission devices, but
also it was being applied to cosmic ray showers and the study of partial
differential equations [29]. In the late 1940s and early 1950s, there
was a surge of papers describing the Monte Carlo method and how it could
solve problems in radiation or particle transport and other areas
[31-33]. Many of the methods described in these papers are still used in
Monte Carlo today, including the method of generating random numbers
[34] used in the MCNP code. Much of the interest was based on continued
development of computers such as the Los Alamos MANIAC (Mechanical
Analyzer, Numerical Integrator, and Computer) in March 1952.

The Atomic Energy Act of 1946 created the Atomic Energy Commission to
succeed the Manhattan Project. In 1953 the United States embarked upon
the 'Atoms for Peace' program with the intent of developing nuclear
energy for peaceful applications such as nuclear power generation.
Meanwhile, computers were advancing rapidly. These factors led to
greater interest in the Monte Carlo method. In 1954 the first
comprehensive review of the Monte Carlo method was published by Herman
Kahn [35] and the first book was published by Cashwell and Everett [19]
in 1959.

At Los Alamos, Monte Carlo computer codes developed along with
computers. The first Monte Carlo code was the simple 19-step computing
sheet in John von Neumann's letter to Richtmyer. But as computers became

more sophisticated, so did the codes. At first the codes were written in
machine language and each code would solve a specific problem. In the
early 1960s, better computers and the standardization of programming
languages such as Fortran made possible more general codes. The first
Los Alamos general-purpose particle transport Monte Carlo code was MCS
[36], written in 1963. Scientists who were not necessarily experts in
computers and Monte Carlo mathematical techniques now could take
advantage of the Monte Carlo method for radiation transport. They could
run the MCS code to solve modest problems without having to do either
the programming or the mathematical analysis themselves. MCS was
followed by MCN [37] in 1965. MCN could solve the problem of neutrons
interacting with matter in a three-dimensional geometry and used physics
data stored in separate, highly developed, libraries.

In 1973 MCN was merged with MCG [38], a Monte Carlo gamma code that
treated higher energy photons, to form MCNG, a coupled neutron-gamma
code. In 1977 MCNG was merged with MCP [38], a Monte Carlo Photon code
with detailed physics treatment down to 1 keV, to accurately model
neutron-photon interactions. The code has been known as the MCNP code
(often referred to, incorrectly, as just 'MCNP') ever since. Though at
first 'MCNP' stood for Monte Carlo Neutron Photon, now it stands for
Monte Carlo N-Particle. Other major advances in the 1970s included the
present generalized tally structure, automatic calculation of volumes,
and a Monte Carlo eigenvalue algorithm to determine k eff for nuclear
criticality ( KCODE ).

In 1983 MCNP3 was released, entirely rewritten in ANSI standard Fortran
77. MCNP3 was the first MCNP code version internationally distributed
through the Radiation Shielding and Information Center at Oak Ridge,
Tennessee. Other 1980s versions of the MCNP code were MCNP3A (1986) and
MCNP3B (1988), that included tally plotting graphics (MCPLOT), the
present generalized source, surface sources, repeated structures/lattice
geometries, and multi-group/adjoint transport. MCNP4 was released in
1990 and was the first UNIX version of the code. It accommodated
N-particle transport and multitasking on parallel computer
architectures. MCNP4 added electron transport (patterned after the
Integrated TIGER Series (ITS) electron physics) [39], the pulse height
tally (F8), a thick-target bremsstrahlung approximation for photon
transport, enabled detectors and DXTRAN with the S ( α, β ) thermal
treatment, provided greater random number control, and allowed plotting
of tally results while the code was running.

MCNP4A, released in 1993, featured enhanced statistical analysis,
distributed processor multitasking for running in parallel on a cluster
of scientific workstations, new photon libraries, ENDF-6 capabilities,
color X-Windows graphics, dynamic memory allocation, expanded
criticality output, periodic boundaries, plotting of particle tracks via
SABRINA, improved tallies in repeated structures, and many smaller
improvements.

MCNP4B, released in 1997, featured differential operator perturbations,
enhanced photon physics equivalent to ITS3.0, PVM load balance and fault
tolerance, cross-section plotting, postscript file plotting, 64-bit
workstation upgrades, PC X-windows, inclusion of LAHET HMCNP, lattice
universe mapping, enhanced neutron lifetimes, coincident-surface lattice
capability, and many smaller features and improvements.

MCNP4C, released in 2000, featured an unresolved resonance treatment,
macrobodies, superimposed importance mesh, perturbation enhancements,
electron physics enhancements, plotter upgrades, cumulative tallies,
parallel enhancements and other small features and improvements.

MCNP5, released in 2003, is rewritten in ANSI standard Fortran 90. It
includes the addition of photonuclear collision physics, superimposed
mesh tallies, time splitting, and plotter upgrades. MCNP5 also includes
parallel computing enhancements with the addition of support for OpenMP
and MPI.

The MCNPX program began in 1994 as an extension of MCNP4B and LAHET 2.8,
extending the MCNP code to 34 particle types at nearly all energies. The
INCL, CEM, and LAQGSM physics models were added along with heavy ion
transport. New sources, tallies, output, graphics and variance reduction
capabilities were developed and added.

The merger of MCNP5 and MCNPX began in 2006 and the first version of the
merged code, MCNP6.1 (i.e., the MCNP code, version 6.1.0), was released
in 2013 (which followed a release of the MCNP code, version 6 beta 2, in
2012 and was later followed by a release of the MCNP code, version
6.1.1, in 2014).

The MCNP code, version 6.2, that released in 2018, contains 39 new
features in addition to 172 bug fixes and code enhancements. Two new
utility tools, Whisper and MCNPTools, were released with the MCNP6.2
code. Details of MCNP6.2 features and bug fixes are in the release notes
[40].

MCNP6.3, released in January 2023 and available to the public in August
2023, transitioned to the CMake build system, added numerous
HDF5-formatted output files (several with complementary XDMF files to
permit immediate open source and cross platform visualization), an
internal fission matrix to accelerate k -eigenvalue calculations, and
other new features, resources, and bug fixes described in the release
notes [41]. In addition, a cross-platform Qt-based plotter built upon
MCNP6.3 was released as a technology preview and to solicit user
feedback.

Large production codes such as the MCNP code have revolutionized
science-not only in the way it is done, but also by becoming the
repositories for physics knowledge. The knowledge and expertise
contained in the MCNP code is formidable. Current MCNP development is
characterized by a strong emphasis on quality control, documentation,
and research. New features continue to be added to the MCNP code to
reflect new advances in computer architectures, improvements in Monte
Carlo methodology, and better physics models. The MCNP code has a proud
history and a promising future.

## 2.1.2 Structure of the MCNP Code

The MCNP code is currently written using a mixed Fortran/C/C++
programming paradigm. It can be built with any Fortran compiler
supporting the Fortran 2018 standard [20] and any C++ compiler
supporting the C++14 standard [22]. Fortran global data is shared via
modules. The general internal structure of the MCNP code is as follows:

Initiation (IMCN):

- Initialize global variables to default values;
- Read input two times to get user inputs;
- Set up variable dimensions or dynamically allocated storage;
- Read input file to load input;
- Initialize random number generator;
- Process geometry;
- Process source;
- Process tallies;
- Process materials specifications including masses without loading the data files;
- Calculate cell volumes and surface areas.

Interactive Geometry Plot (PLOTG).

Cross-section Processing (XACT):

- Load libraries;
- Eliminate excess nuclear data outside problem energy range;

- Doppler broaden elastic and total cross sections to the proper temperature if the problem temperature is higher than the library temperature;
- Process multigroup libraries if requested;
- Process electron libraries including calculation of range tables, straggling tables, scattering angle distributions, and bremsstrahlung.

MCRUN sets up multitasking and multiprocessing, runs histories, and
returns to print, write

RUNTPE dumps, or process another criticality cycle.

Under MCRUN, the MCNP code runs particle histories. The following
procedures are for neutron and/or photon transport

- Start a source particle;
- Find the distance to the next boundary, cross the surface and enter the next cell;
- Find the total neutron cross section and process neutron collisions producing photons as appropriate;
- Find the total photon cross section and process photon collisions producing electrons as appropriate;
- Use the optional thick-target bremsstrahlung approximation if no electron transport;
- Follow electron tracks;
- Process optional multigroup collisions;
- Process detector tallies or DXTRAN;
- Process surface, cell, and pulse height tallies.

Periodically write output file, restart dumps, update to next
criticality cycle, rendezvous for multitasking and updating detector and
DXTRAN Russian roulette criteria, etc.:

- Go to the next criticality cycle;
- Print output file summary tables;
- Print tallies;
- Generate weight windows.

Plot tallies, cross sections, and other data (MCPLOT).

MPI distributed processor multiprocessing routines.

Random number generator and control.

Mathematics, character manipulation, and other routines.

## 2.1.2.1 History Flow

The history flow of heavy charged particles is described in [42]. The
basic flow of a particle history for a coupled neutron/photon/electron
problem is handled as follows:

For a given history, the random number sequence is set up and the number
of the history is incremented. The particle-state arrays are reset.
Then, the particle identifier ( ipt ) is set for the type of particle
being run: 1 for a neutron, 2 for a photon, etc. (with the full set of
integer identifiers given in Table 4.3). The branch of the history is
set to 1.

Next, the appropriate source routine is called. Source options are the
standard fixed sources, the surface source, the criticality source, or a
user-provided source. All of the parameters describing the particle are
set in these source routines, including position, direction of flight,
energy, weight, time, and starting cell (and possibly surface), by
sampling the various distributions described on the source input control
cards. Several checks are made at this time to verify that the particle
is in the correct cell or on the correct surface, and directed toward
the correct cell.

Next, the initial parameters of the first fifty particle histories are
printed. Then some of the summary information is incremented. Energy,
time, and weight are checked against cutoffs. A number of error checks
are made. Detector contributions are scored, and then the DXTRAN
subroutine is called (if used in the problem) to create particles on the
spheres. The particles are saved in the bank for later tracking.
Bookkeeping is started for the pulse height cell tally energy balance.
The weight window game is played, with any additional particles from
splitting put into the bank and any losses to Russian roulette
terminated.

Then the actual particle transport is started. For an electron source,
electrons are run separately. For a neutron or photon source, the
intersection of the particle trajectory with each bounding surface of
the cell is calculated. The minimum positive distance to the cell
boundary indicates the next surface the particle is heading toward. The
distance to the nearest DXTRAN sphere is calculated, as is the distance
to time cutoff, and energy boundary for multigroup charged particles.
The cross sections for a current cell are calculated using a binary
table lookup in data tables for neutrons or photons. The total photon
cross section may include the photonuclear portion of the cross section
if photonuclear physics is in use. See §5.7.2.3 for a discussion of
turning photonuclear physics on. The total cross section is modified by
the exponential transformation if necessary. The distance to the next
collision is determined (if a forced collision is required, the
uncollided part is banked). The track length of the particle in the cell
is found as the minimum of the distance to collision, the distance to
the cell surface, one mean free path (in the case of a mesh-based weight
window), the distance to a DXTRAN sphere, the distance to time cutoff,
or the distance to energy boundary. Track length cell tallies are then
incremented. Some summary information is incremented. The particle's
parameters (time, position, and energy) are then updated. If the
particle's distance to a DXTRAN sphere (of the same type as the current
particle) is equal to the minimum track length, the particle is
terminated because particles reaching the DXTRAN sphere are already
accounted for by the DXTRAN particles from each collision. If the
particle exceeds the time cutoff, the track is terminated. If the
particle was detected leaving a DXTRAN sphere, the DXTRAN flag is set to
zero and the weight cutoff game is played. The particle is either
terminated to weight cutoff or survives with an increased weight. Weight
adjustments then are made for the exponential transformation.

If the minimum track length is equal to the distance-to-surface
crossing, the particle is transported to the cell surface, any surface
tallies are processed, and the particle is processed for entering the
next cell. Reflecting surfaces, periodic boundaries, geometry splitting,
Russian roulette from importance sampling, and loss to escape are
treated. The bank entries or retrievals are made on a last-in, first-out
basis. The history is continued by going back to the previous paragraph
and repeating the steps.

If the distance to collision is less than the distance to surface, or if
a multigroup charged particle reaches the distance to energy boundary,
the particle undergoes a collision. For neutrons, the collision analysis
determines which nuclide is involved in the collision, samples the
target velocity of the collision nuclide for
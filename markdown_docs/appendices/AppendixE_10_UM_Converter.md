---
title: "Appendix E.10 - Unstructured Mesh Format Converter (um_converter)"
chapter: "E.10"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.10_Unstructured_Mesh_Format_Converter_(um_conver.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## E.10 Unstructured Mesh Format Converter ( um \_ convert )

## /\_445 Deprecation Notice

DEP-53421

The um \_ convert application is deprecated because of the deprecation of
the MCNPUM file format [DEP-53424].

The um\_convert (unstructured mesh convertor) program is a command-line
utility program that takes the information in the Abaqus mesh input file
and processes it with the UM input processing routines from REGL to
produce the internal data structures that MCNP6 needs. The data from
these internal data structures are written to a new file type, MCNPUM
[DEP-53424], that MCNP6 can quickly read before launching into
calculations. With the MCNPUM file type the UM input processing start up
penalty need not happen every time the UM geometry is required. This can
save substantial time for large mesh geometries that are used
repeatedly. Details on the structure of this file and its contents are
best learned from looking at the source code.

## E.10.1 Command Line Options

To be reminded of um\_convert 's functionality and to see the command
line options, enter the following at the command line prompt:

```
um _ convert _ op --help
```

Note, your path must include the path to the program. A message similar
to the following should appear in the command window:

```
** UNSTRUCTURED MESH CONVERSION PROGRAM ** Functions: 1) Convert ABAQUS inp file to mcnpum file Command Line Arguments: -h, --help summary of features & arguments -b, --binary create mcnpum in binary format -a, --abaqus ABAQUS input file --(1) -l, --length length conversion factor -o, --output um _ convert output file name -t, --threads number of threads -um, --mcnpum mcnpum output file name
```

## The -b Option

This argument ( -b, --binary ) requests that the MCNPUM file be created
as a binary file instead of ASCII. ASCII is default and results if this
option is not specified.

## The -a Option

This argument ( -a, --abaqus ) followed by the file name of the Abaqus
mesh input file communicates this information to the utility program.
This information is required.

## The -l Option

This argument ( -l, --length ) followed by a value provides a conversion
factor for all dimensions in a similar fashion to the length parameter
on the EMBED card.

## The -o Option

This argument ( -o, --output ) followed by a file name tells the utility
program where to write messages and information from the file conversion
process. The information that MCNP6 would normally print to its outp
file when building the unstructured mesh model is written to this file.
This argument is optional. If no name is specified, the information is
written to the um \_ convert.out file.

## The -t Option

This argument ( -t, --threads ) followed by a number sets the number of
OpenMP threads for use in the conversion process. The user should be
careful and not oversubscribe threads by requesting too large of a
number. (See Section E.10.2). This is an optional argument. The default
value is 1.

## The -um Option

This argument ( -um, --mcnpum ) followed by a file name tells the
utility program what to call the MCNPUM file [DEP-53424] that it
generates. If no name is specified, the information is written to the um
\_ convert.mcnpum file.

## E.10.2 Program Execution and Example

The um\_convert utility is a highly parallelized program that can be
compiled to use MPI processes, OpenMP threads, and vectorized loops. As
a note to those wishing to build the code on their systems from the
source, the following is the appropriate command line (using the
traditional MCNP6 make system) that will build the code with MPI
processes, OpenMP threads, and vectorized loops once the mainline MCNP6
code has been built:

make depends build CONFI='intel openmpi omp' FC \_ OPT='-O3' GNUJ=4

Normal execution of um\_convert from the command line will result in
messages similar to the following appearing in the command window:

UM \_ CONVERT input processing begins.

119-2015 @ 9:46:31

```
Max threads available: 16 Global Tracking Model Complete Element Neighbors Found Part Cell Surfaces Complete SKD-Trees Build Complete Element Connectivity Complete um _ convert execution time 19.6 sec UM _ CONVERT input processing ends. 119-2015 @ 9:46:50
```

Note that the program provides the user with the maximum number of
available threads. The product of the number of MPI processes and the
number of threads, specified with the -t Option, should not exceed the
number of cpu cores present or performance will be degraded.

A combination of MPI processes and OpenMP threads should produce the
shortest execution times on most systems. If the user doesn't have MPI
available (e.g., a desktop Windows machine), executing with the maximum
number of available threads should still produce acceptable execution
times. The utility will process one part / instance at a time, using all
of the requested threads as it needs them.

If the user is running on a Linux cluster where MPI has been installed,
a combination of MPI processes and OpenMP threads is recommended. As
always, performance is contingent on the number of parts / instances in
the Abaqus mesh input file. If there are more cpu cores available than
parts / instances, then specifying one MPI process for each part /
instance with several threads per process is recommended. If fewer MPI
processes are specified than parts / instances, then um\_convert will
give each process a number of parts / instances to work on in a
sequential fashion much like MCNP6 does with its parallel processing of
parts / instances. In this later scenario where there are more parts /
instances than cpu cores, it may be beneficial to reduce the number of
MPI processes so that each process has two threads. This should help
when one or a few parts have substantially more elements than the other
parts.

Unlike MCNP6 where the manager MPI process basically functions as a
controller during the calculational phase, all MPI processes in the
um\_convert utility have a chunk of the parts / instances with which to
work.

As a reminder when using MPI processes and OpenMP threads together on
certain Linux clusters, the mpi \_ paffinity \_ alone and bynode switches
(or their equivalent) may be necessary when using mpirun to ensure that
threads are assigned to the correct hardware.
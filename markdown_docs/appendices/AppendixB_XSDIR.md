---
title: "Appendix B - XSDIR Data Directory File"
chapter: "B"
source_pdf: "mcnp631_theory_user-manual/appendecies/B_XSDIR_Data_Directory_File.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Appendix B

## XSDIR Data Directory File

A cross-section directory file, commonly referred to as the xsdir file,
is used to locate and read the ACEformatted data files. The xsdir file
is a sequentially formatted ASCII file containing free-field entries
delimited by blanks. The default xsdir file provided with the MCNP code,
version 6.3, is named xsdir \_ mcnp6.3 . MCNP6 uses two types and fifteen
classes of data. These data are kept in individual tables that are often
organized into libraries. These terms and tables are described in this
appendix.

MCNP6 reads fifteen classes of data from two types of data tables. The
two types of data tables are the following:

- Type 1 standard formatted tables (sequential, up to 128 characters per record). These portable libraries are used to transmit data from one installation to another. They are bulky and slower to read. Often installations generate Type 2 tables from Type 1 tables using the makxsf code [344]. See §E.5 for more information on the the makxsf code.
- Type 2 standard unformatted tables (direct-access, binary) locally generated from Type 1 tables. They are generally not portable between different systems. Type 2 tables are used mostly because they are more compact and faster to read than Type 1 tables.

Data tables exist for fifteen classes of data. These classes are
identified by the last letter of the table identifier in Table B.1.

A user should think of a data table as an entity that contains
evaluation-dependent information about one of the fifteen classes of
data for a specific target isotope, isomer, element, or material. For
how the data are used in the MCNP code, a user does not need to know
whether a particular table is Type 1 or Type 2. For a given table
identifier [§1.2.3], the data contained on Type 1 and Type 2 tables are
identical. Problems run with one data type will track problems run with
the same data in another format type.

When we refer to data libraries, we are talking about a series of data
tables concatenated into one file. All tables on a single library must
be of the same type but not necessarily of the same class. There is no
reason, other than convenience, for having data libraries; the MCNP code
could read exclusively from individual data tables not in libraries. The
MCNP code determines where to find data tables for each target
identifier in a problem based on information contained in a version-
dependent xsdir file, following the rules in [§2.3.1].

The xsdir file has three sections. In the first section, the first line
is an optional entry of the form DATAPATH = datapath where the word
DATAPATH (case insensitive) must start in columns 1-5. The '=' sign is
optional. The directory where the data libraries are stored is named
datapath . The xsdir file can be renamed on the MCNP execution line
[Table 3.4]. The search hierarchy to find xsdir and/or the data
libraries is the following:

1. xsdir = filename on the MCNP6 execution line, where filename is the name of a cross-section directory file,

Table B.1: MCNP6 Data Classes

|    | Class description                                      | Physics identifier   |
|----|--------------------------------------------------------|----------------------|
|  1 | S( α , β ) data tables                                 | t                    |
|  2 | Continuous-energy neutron data libraries               | c                    |
|  3 | Discrete-energy neutron data libraries                 | d                    |
|  4 | Coupled neutron-photon data multigroup library-neutron | m                    |
|  5 | Coupled neutron-photon data multigroup library-photon  | g                    |
|  6 | Photoatomic data libraries                             | p                    |
|  7 | Photonuclear data libraries                            | u                    |
|  8 | Dosimetry data libraries                               | y                    |
|  9 | Electron data libraries                                | e                    |
| 10 | Proton data libraries                                  | h                    |
| 11 | Photoatomic data libraries with atomic relaxation data | p                    |
| 12 | Deuteron data libraries                                | o                    |
| 13 | Triton data libraries                                  | r                    |
| 14 | Helion data libraries                                  | s                    |
| 15 | Alpha data libraries                                   | a                    |

2. DATAPATH= datapath in the MCNP input file message block,
3. the current working directory,
4. the DATAPATH entry on the first line of the xsdir file,
5. the system environment variable DATAPATH , or
6. the individual data table in the xsdir file (see below under Access Route).

The second section of the xsdir file is the atomic weight ratios. This
section starts with the words 'ATOMIC WEIGHT RATIOS' (case insensitive)
beginning in columns 1-5. The following lines are free-format pairs of
target identifiers and AWRs, where the target identifier is any form in
[§1.2.2] and AWR is the atomic weight ratio. These atomic weight ratios
are used for converting from weight fractions to atom fractions and for
getting the average Z in computing electron stopping powers. If the
atomic weight ratio is missing for any nuclide requested on an Mm card,
it must be provided on the AWTAB card.

The third section of the xsdir file is the listing of available data
tables. This section starts with the word 'DIRECTORY' (case insensitive)
beginning in columns 1-5. The lines following consist of the seven- to
eleven-entry description of each table. The table identifier of each
table must be the first entry. If a table requires more than one line,
the continuation is indicated by a '+' at the end of the line. A zero
indicates the entry is not applicable. Unneeded entries at the end of
the line can be omitted.

The directory file has seven to eleven entries for each table. They are
the following:

1. Name of the Table, character
2. Atomic Weight Ratio, real
3. File Name, character
4. Access Route, character
5. File Type, integer
6. Address, integer

7. Table Length, integer
8. Record Length, integer
9. Number of Entries per Record, integer
10. Temperature, real
11. Probability Table Flag, character

which are

1. Name of the Table, in the form of §1.2.3. The target identifier cannot be '0', 'model', or 'none' and may be up to 32 characters in length.
2. Atomic Weight Ratio. This is the atomic mass divided by the mass of a neutron. The atomic weight ratio here is used only for neutron kinematics and should be the same as it appears in the cross-section table so that threshold reactions are correct. It is the quantity A used in all the neutron interaction equations of Section 2 of the xsdir file. This entry is used only for neutron tables.
3. File Name. The file name is the name of the library that contains the table. The file name can include a directory path. It cannot include spaces.
4. Access Route. The access route is a string that tells how to access the file if it is not already accessible, such as a directory path. If there is no access route, this entry is zero. It cannot include spaces.
5. File Type. Either 1 for Type 1 files or 2 for Type 2.
6. Address. For Type 1 files, the address is the line number in the file where the table starts. For Type 2 files, it is the record number of the first record of the table.
7. Table Length. A data table consists of two blocks of information. The first block is a collection of pointers, counters, and character information. The second block is a solid sequence of numbers. For Type 1 and Type 2 tables, the table length is the length (total number of words) of the second block.
8. Record Length. This entry is unused for Type 1 files and therefore is zero. For Type 2 direct access files, it is a compiler-dependent attribute.
9. Number of Entries per Record. This is unused for Type 1 files and therefore is zero. For Type 2 files it is the number of entries per record. Usually this entry is set to 512.
10. Temperature. This is the temperature in MeV at which a neutron table is processed. This entry is used only for neutron data.
11. Probability Table Flag. The character word 'ptable' indicates a continuous-energy neutron nuclide has unresolved resonance range probability tables.
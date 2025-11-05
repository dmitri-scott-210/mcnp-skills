---
title: "Appendix E.9 - Simple ACE File Generation Tools (simple_ace.pl)"
chapter: "E.9"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.9_Simple_ACE_File_Generation_Tools_(simple_ace.p.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## E.9 Simple ACE File Generation Tools ( simple \_ ace.pl and simple \_ ace \_ mg.pl )

The simple \_ ace.pl and simple \_ ace \_ mg.pl scripts have been developed
to support the generation of simplified continuous-energy and multigroup
nuclear data files in A Compact ENDF (ACE) format [357, 358]. In
general, these scripts are used to generate nuclear data for use in
analytic or semi-analytic verification testing that is useful to ensure
that the code implementation is consistent with the underlying particle
transport theory.

To run either the simple \_ ace.pl or the simple \_ ace \_ mg.pl script,
the user must have Perl available on their system. All interactions with
the scripts are performed in a command-line interface.

## E.9.1 Continuous-energy Cross Sections with simple \_ ace.pl

The simple \_ ace.pl script generates continuous-energy nuclear data ACE-
formatted datasets. It only considers capture, fission, and elastic
scattering, prompt fission neutrons (no delayed fission), and a discrete
delta function for the prompt fission neutron spectrum, χ ( E ) .

## User Interface Command Line Options

| -zaid ZAID       | String name for dataset, following §1.2.3, typically of the form ZZAAA.nnc . Default 99999.99c .                                                                                                                               |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -file FILE       | String filename for output ACE dataset. Default ZAID (see above).                                                                                                                                                              |
| -awr AWR         | Atomic weight ratio, mass/neutron-mass. Default 1000000.0 .                                                                                                                                                                    |
| -tmp TMP         | Temperature. In units of MeV if TMP<1 . In units of Kelvin if TMP>1 . Default is room temperature 2.5301E-8 MeV.                                                                                                               |
| -comment COMMENT | Comment to include in ACEfile header. Default is ACE file created by simple _ ace.pl                                                                                                                                           |
| -e ENERGIES      | List of energy points (MeV). Must include ≥ 2 values, provided in increasing order. Default is 1.E-11 100 MeV.                                                                                                                 |
| -t T _ XS        | Ignored. Total cross section, σ t , constructed from -s , -c , and -f values below ( 1 ).                                                                                                                                      |
| -s S _ XS        | List of scattering cross section values, σ s , elastic only ( 1 ).                                                                                                                                                             |
| -mu MU           | List of average cosine scattering angles, ¯ µ ( 1 , 2 ).                                                                                                                                                                       |
| -s1 S1           | List of P 1 scattering cross sections ( 1 ). May be used instead of ¯ µ with same restrictions of the MU values above ( 2 ).                                                                                                   |
| -c C _ XS        | List of capture cross section values, σ c , not including fission ( 1 ).                                                                                                                                                       |
| -f F _ XS        | List of fission cross section values, σ f ( 1 ).                                                                                                                                                                               |
| -echi ECHI       | Single energy (MeV) value for prompt fission spectrum delta function, χ ( E ) = δ ( E - ECHI ) .                                                                                                                               |
| -nu NU           | List of average fission multiplicity values, ¯ ν ( 1 ).                                                                                                                                                                        |
| -nloge NLOGE     | List of energy intervals to expand -e energy list into equally spaced bins in log ( e ) . Number of values in list must be 1 less than the number of values in the -e list. Use linear interpolation for cross section values. |

.

1

-broaden Flag to Doppler broaden cross sections. Assumes each input
scatter cross section is at 0 K, and then Doppler broadens each cross
section to TMP value, assuming constant cross section approximation.
Default is False.

## Details:

- 1 If 0 values supplied, set to 0. If 1 value supplied, use it for all energies. Otherwise, number of values must match the number of values given in the -e list of energies.
- 2 For P 1 scattering, | µ | ≤ 1 / 3 . For scattering angles of | µ | &gt; 1 / 3 , results can be seriously incorrect because the scattering probability density function is negative over portions of the scattering angle domain [358].

## Example

To create a continuous-energy ACE dataset covering the incident neutron
energy range from 10 -11 to 100 MeV, with uniform capture ( σ c ),
scattering ( σ s ), and fission ( σ f ) cross sections, an uniform
prompt fission neutron multiplicity ( ¯ ν ), and a 1 MeV discrete delta
function for prompt neutrons born from fission, the following command
line options can be used:

```
simple _ ace.pl -c .019584 -s .225216 -f .0816 -nu 3.24 -e 1e-11 100 -echi 1
```

Information from simple \_ ace.pl is provided to the standard output:

```
1 =====> simple _ ace.pl -create special purpose ACE file 2 3 zaid = 99999.99c 4 za = 99999 5 file = 99999.99c 6 awr = 1000000 7 tmp = 2.5301e-08 8 echi = 1 9 energy pts = 2 10 xss size = 60 11 12 e sigt sigc sigs nu sigf 13 1.0000e-11 3.2640e-01 1.9584e-02 2.2522e-01 3.24 8.1600e-02 14 1.0000e+02 3.2640e-01 1.9584e-02 2.2522e-01 3.24 8.1600e-02 15 16 XSDIR Info, to use on XSn card:: 17 18 XSn 99999.99c 1e+06 99999.99c 0 1 1 60 0 0 2.5301e-08 19 20 21 Creating ACE file: 99999.99c
```

To utilize this ACE file within an MCNP calculation, the screen output
provides the necessary XS n cross section input card. If the user
provides a unique n value for this particular XS input card, the
99999.99c identifier can be used within a M material specification input
card. The generated ACE file for this example can be found in Listing
E.12.

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

22

23

24

25

26

27

Listing E.12: Simple ACE File 99999.99c

| 99999.99c        | 1e+06 2.53010e-08 2022-06-20   | 1e+06 2.53010e-08 2022-06-20   | 1e+06 2.53010e-08 2022-06-20   | 1e+06 2.53010e-08 2022-06-20   | 1e+06 2.53010e-08 2022-06-20   | 1e+06 2.53010e-08 2022-06-20   |
|------------------|--------------------------------|--------------------------------|--------------------------------|--------------------------------|--------------------------------|--------------------------------|
| ACE file created | by simple _ ace.pl             | by simple _ ace.pl             | by simple _ ace.pl             |                                |                                | 2022-06-20                     |
| 0                | 0.000000                       | 0                              | 0.000000                       | 0 0.000000                     | 0                              | 0.000000                       |
| 0                | 0.000000                       | 0                              | 0.000000                       | 0 0.000000                     | 0                              | 0.000000                       |
| 0                | 0.000000                       | 0                              | 0.000000                       | 0 0.000000                     | 0                              | 0.000000                       |
| 0                | 0.000000                       | 0                              | 0.000000                       | 0 0.000000                     | 0                              | 0.000000                       |
| 60               | 99999                          | 2                              | 1                              | 1 0                            | 0                              | 0                              |
| 0                | 0                              | 0                              | 0                              | 0 0                            | 0                              | 0                              |
| 1                | 11                             | 18                             | 19                             | 20 21                          | 22                             | 26                             |
| 28               | 38                             | 39                             | 0                              | 0 0                            | 0                              | 0                              |
| 0                | 0                              | 0                              | 0                              | 57 60                          | 0                              | 0                              |
| 0                | 0                              | 0                              | 0                              | 0 0                            | 0                              | 0                              |
| 1e-11            | 1e-11                          | 100                            | 100                            | 100                            | 0.3264                         | 0.3264                         |
|                  | 0.019584                       |                                | 0.019584                       | 0.225216                       | 0.3264                         | 0.225216                       |
|                  | 0                              |                                | 0                              |                                | 2                              | 0                              |
|                  | 2                              |                                | 1e-11                          |                                | 100                            | 3.24                           |
|                  | 3.24                           |                                | 18                             |                                | 0                              | 19                             |
|                  | 1                              |                                | 1                              |                                | 2                              | 0.0816                         |
|                  | 0.0816                         |                                | 1                              |                                | 6                              | 2                              |
|                  | 1e-11                          |                                | 100                            |                                | 0                              | 0                              |
|                  | 2                              |                                | 1e-11                          |                                | 100                            | 0                              |
|                  | 0                              |                                | 1                              |                                | 0                              | 1                              |
|                  | 10                             |                                | 0                              |                                | 2                              | 1e-11                          |
|                  | 100                            |                                | 1                              |                                | 1                              | 0                              |
|                  | 2                              |                                | 1e-11                          |                                |                                | 2                              |
|                  | 0.999999                       |                                | 1.000001                       |                                | 100                            |                                |
|                  |                                |                                |                                |                                | 0.999999                       | 1.000001                       |
|                  | 1                              |                                | 2                              |                                |                                |                                |
|                  |                                |                                |                                |                                | 0.0816                         | 0.0816                         |

## E.9.2 Multigroup Cross Sections with simple \_ ace \_ mg.pl

The simple \_ ace \_ mg.pl script generates multigroup nuclear data ACE-
formatted datasets. It only considers capture, fission, and elastic
scattering, prompt fission neutrons (no delayed fission), and isotropic
or P 1 scattering distributions.

## User Interface Command Line Options

| -zaid ZAID       | String name for dataset, following §1.2.3, typically of the form ZZAAA.nnm . Default 99999.99m .                           |
|------------------|----------------------------------------------------------------------------------------------------------------------------|
| -file FILE       | String filename for output ACE dataset. Default ZAID (see above).                                                          |
| -awr AWR         | Atomic weight ratio, mass/neutron-mass. Default 1000000.0 .                                                                |
| -tmp TMP         | Temperature. In units of MeV if TMP<1 . In units of Kelvin if TMP>1 . Default is room temperature 2.5301E-8 MeV.           |
| -comment COMMENT | Comment to include in ACE file header. Default is multigroup ACE file .                                                    |
| -groups NG       | Number of energy groups. Default is 1 .                                                                                    |
| -e ENERGIES      | List of energy group boundaries (MeV). Must include NG+1 values, provided in decreasing order. Default is 100 0 MeV ( 1 ). |

1

2

3

- -t T \_ XS List of total cross section values, σ t ( 2 ). -s S \_ XS List of scattering cross section values, σ s , elastic only ( 3 , 4 ). -s1 S1 List of P 1 scattering cross section values ( 3 , 4 , 5 ). -c C \_ XS List of capture cross section values, σ c , not including fission ( 2 ). -f F \_ XS List of fission cross section values, σ f ( 2 ). -chi CHI List of prompt fission spectrum, χ , values for each energy group ( 2 ). -nu NU List of average fission multiplicity values, ¯ ν ( 2 ). -bins NBINS Number of bins to expand P 1 scattering into equiprobable scattering angular distribution. Default 1000 .

## Details:

- 1 If NG=1 , default energy group structure is 100 0 MeV. If NG=2 , default energy group structure is 100 0.625E-6 0 MeV. For any other NG value, no default group structure provided.
- 2 If 0 values supplied, set to 0. If 1 value supplied, use it for all energy groups. Otherwise, the number of values entered must match the number of NG groups.
- 3 If 0 values supplied, set to 0. If 1 value supplied, use it for all scattering transition groups. Otherwise, the number of values entered must match the number of scattering transition groups, NS = NG × NG .
- 4 The group-to-group scatter cross sections must be provided in this order: 1 → 1 , 1 → 2 , . . . , 1 → NG , 2 → 1 , 2 → 2 , . . . , 2 → NG , . . . NG → 1 , NG → 2 , . . . , NG → NG , with group 1 being the highest-energy group and group NG being the lowest-energy group.
- 5 For P 1 scattering, | S1 / S \_ XS | ≤ 1 / 3 . For scattering angles of | S1 / S \_ XS | &gt; 1 / 3 , results can be seriously incorrect because the scattering probability density function is negative over portions of the scattering angle domain [358].

## Example

To create a 2-group multigroup ACE dataset with energy group 1 from
10-100 MeV and energy group 2 from 0-10 MeV, with total ( σ t ), capture
( σ c ), and fission ( σ f ) cross sections, a prompt fission neutron
multiplicity ( ¯ ν ) and emission spectrum ( χ ), and an isotropic
group-to-group scattering matrix ( σ s,g → g ′ ), the following command
line options can be used:

```
simple _ ace.pl -zaid 22089.01m -comment 'la-ur-12-22089 analytic problem 1' \ -groups 2 -e 100. 10. 0. -t 2. 3. -c .5 1. -f .5 1. \ -nu .75 4.5 -chi 1. 0. -s .5 .5 0. 1.
```

Information from simple \_ ace \_ mg.pl is provided to the standard screen
output:

```
1 =====> simple _ ace _ mg.pl -create simple multigroup ACE file 2 3 zaid = 22089.01m
```

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

<!-- image -->

| za = 22089 file = 22089.01m awr = 1000000              | za = 22089 file = 22089.01m awr = 1000000              | za = 22089 file = 22089.01m awr = 1000000              | za = 22089 file = 22089.01m awr = 1000000              | za = 22089 file = 22089.01m awr = 1000000              | za = 22089 file = 22089.01m awr = 1000000              | za = 22089 file = 22089.01m awr = 1000000              | za = 22089 file = 22089.01m awr = 1000000              | za = 22089 file = 22089.01m awr = 1000000              |
|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|
| group                                                  | Ehi                                                    | Elow                                                   | total                                                  | capture                                                | scatter                                                | fission                                                | nu                                                     | chi                                                    |
| 1                                                      | 100                                                    | 10                                                     | 2                                                      | 0.5                                                    | 1                                                      | 0.5                                                    | 0.75                                                   | 1                                                      |
| 2                                                      | 10                                                     | 0                                                      | 3                                                      | 1                                                      | 1                                                      | 1                                                      | 4.5                                                    | 0                                                      |
| scattering matrix, group-I (down) --> group-J (across) | scattering matrix, group-I (down) --> group-J (across) | scattering matrix, group-I (down) --> group-J (across) | scattering matrix, group-I (down) --> group-J (across) | scattering matrix, group-I (down) --> group-J (across) | scattering matrix, group-I (down) --> group-J (across) | scattering matrix, group-I (down) --> group-J (across) | scattering matrix, group-I (down) --> group-J (across) | scattering matrix, group-I (down) --> group-J (across) |
| J -->                                                  | 1                                                      |                                                        | 2                                                      |                                                        |                                                        |                                                        |                                                        |                                                        |
| I --v                                                  | I --v                                                  | I --v                                                  | I --v                                                  | I --v                                                  | I --v                                                  | I --v                                                  | I --v                                                  | I --v                                                  |
| 1                                                      | 0.5                                                    |                                                        | 0.5                                                    |                                                        |                                                        |                                                        |                                                        |                                                        |
| 2                                                      |                                                        | 0                                                      | 1                                                      |                                                        |                                                        |                                                        |                                                        |                                                        |
| XSDIR Info, XSn                                        | to use 22089.01m                                       | on XSn card: 1e+06                                     | 22089.01m                                              | 0 1 1 21                                               | 0 0                                                    | 2.5301e-08                                             |                                                        |                                                        |
| Creating ACE                                           | file:                                                  | 22089.01m                                              |                                                        |                                                        |                                                        |                                                        |                                                        |                                                        |

To utilize this ACE file within an MCNP calculation, the screen output
provides the necessary XS n cross section input card. If the user
provides a unique n value for this particular XS input card, the
22089.01m identifier can be used within a M material specification input
card. The generated ACE file for this example can be found in Listing
E.13.

Listing E.13: Simple ACE Multigroup File 22089.01m

| 22089.01m 1e+06 2.53010e-08 2022-06-20   | 22089.01m 1e+06 2.53010e-08 2022-06-20   | 22089.01m 1e+06 2.53010e-08 2022-06-20   | 22089.01m 1e+06 2.53010e-08 2022-06-20   | 22089.01m 1e+06 2.53010e-08 2022-06-20   | 22089.01m 1e+06 2.53010e-08 2022-06-20   |
|------------------------------------------|------------------------------------------|------------------------------------------|------------------------------------------|------------------------------------------|------------------------------------------|
| la-ur-12-22089 analytic problem 1        | la-ur-12-22089 analytic problem 1        | la-ur-12-22089 analytic problem 1        | la-ur-12-22089 analytic problem 1        | la-ur-12-22089 analytic problem 1        | 2022-06-20                               |
| 0                                        | 0.000000                                 | 0                                        | 0.000000                                 | 0 0.000000                               | 0 0.000000                               |
| 0                                        | 0.000000                                 | 0                                        | 0.000000                                 | 0 0.000000                               | 0 0.000000                               |
| 0                                        | 0.000000                                 | 0                                        | 0.000000                                 | 0 0.000000                               | 0 0.000000                               |
| 0                                        | 0.000000                                 | 0                                        | 0.000000                                 | 0 0.000000                               | 0 0.000000                               |
| 21                                       | 22089                                    | 0                                        | 0                                        | 2 1                                      | 1 0                                      |
| 0                                        | 1                                        | 0                                        | 1                                        | 0 0                                      | 0 0                                      |
| 1                                        | 5                                        | 7                                        | 9                                        | 11 13                                    | 0 0                                      |
| 0                                        | 0                                        | 0                                        | 0                                        | 15 0                                     | 0 20                                     |
| 21                                       | 0                                        | 0                                        | 0                                        | 0 0                                      | 0 0                                      |
| 0                                        | 0                                        | 0                                        | 0                                        | 0 0                                      | 0 0                                      |
|                                          | 55                                       |                                          | 5                                        |                                          | 90 10                                    |
|                                          | 2                                        |                                          | 3                                        |                                          | 0.5 1                                    |
|                                          | 0.75                                     |                                          | 4.5                                      |                                          | 0                                        |
|                                          | 0.5                                      |                                          | 1                                        |                                          | 0.5                                      |
|                                          | 0.5                                      |                                          | 0                                        |                                          | 0                                        |
|                                          | 0                                        |                                          |                                          |                                          |                                          |

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
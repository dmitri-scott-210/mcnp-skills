---
title: "Appendix F.1 - Biological Conversion Factors"
chapter: "F.1"
source_pdf: "mcnp631_theory_user-manual/appendecies/F.1_Biological_Conversion_Factors.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Appendix F

## Response Functions

This appendix presents response functions that are appropriate for use
on the DE and DF tally cards to convert from calculated particle flux to
quantities of interest. Section F.1 provides several biological dose
equivalent rates and Section F.2 provides data on material damage.

These sets of conversion factors are not the only ones in existence, nor
are they recommended by this publication. Rather, they are presented
only for convenience. The original publication cited and other sources
of this information should be consulted to determine if they are
appropriate for your application.

Be aware that conversion factor sets are subject to change based on the
actions of various national and international organizations such as the
National Council on Radiation Protection and Measurements (NCRP), the
International Commission on Radiological Protection (ICRP), the
International Commission on Radiation Units and Measurements (ICRU), the
American National Standards Institute (ANSI), and the American Nuclear
Society (ANS). Changes may be based on the reevaluation of existing data
and calculations or on the availability of new information.

In addition to biological dose factors, a reference is given for silicon
displacement kerma factors for potential use in radiation-effects
assessment of electronic semiconductor devices. The use of these factors
is subject to the same caveats stated above for biological dose rates.

For these response functions, ASCII files containing DE / DF cards that
can be used with the READ card are electronically attached to this
document for convenience to ease data retrieval, subsequent processing,
and eventual use. Tabulated values and representative plots of the
response functions given in the attachments are also provided here.
Instructions on how to extract the response functions from this document
can be found in the Preface (page 23).

## /warning\_sign Caution

The attached DE / DF cards cannot be directly used in an MCNP input. A
tally number must be added. The omission of a tally number and therefore
invalid attached input is intentional to ensure the person using the
values has interacted with (and thought about) them and is not using
them blindly.

## F.1 Biological Conversion Factors

In the following discussions, dose rate will be used interchangeably
with biological dose equivalent rate. The neutron quality factors
implicit in the conversion factors are also tabulated for reference. For
consistency with the original publication and to enable direct
comparison with original sources, all conversion factors are given in
the units they are published as. The interpolation mode chosen should
correspond to that recommended

by the reference. For example, the ANSI/ANS publication recommends log-
log interpolation; significant differences at interpolated energies can
result if a different interpolation scheme is used (e.g., Figs. F.1 and
F.26).

## F.1.1 Incident Neutron

The ANSI/ANS-6.1.1-1977 neutron flux-to-dose conversion and quality
factors are given in Listing F.1, which can be directly used as MCNP
input for DE / DF cards. These flux-to-dose conversion factors are also
plotted in Figure F.1 showing both linear and logarithmic interpolation.
These values are extracted from [360] with permission of the publisher,
the American Nuclear Society.

The ANSI/ANS-6.1.1-1991 standard provides a variety of neutron fluence-
to-dose conversion factors assuming four irradiation-phantom
orientations: anterior-posterior (AP), posterior-anterior (PA), lateral
(LAT), and rotational (ROT). More details on these factors, and how to
use them, are available in [361]. The AP, PA, LAT, and ROT responses are
given in Listings F.2, F.3, F.4, and F.5, respectively, which can be
directly used as MCNP input for DE / DF cards. In addition, the
conversion factors are plotted in Figures F.2, F.3, F.4, and F.5.

The ICRP/21-1973 neutron fluence-to-dose conversion and quality factors
are given in Listing F.6, which can be directly used as MCNP input for
DE / DF cards. These values are modified from the original values in
[362]. The values in Listing F.6 are the inverse of the original values.
In addition, Listing F.6 includes extra significant figures in order to
reconstruct the original values in [362].

These fluence-to-dose conversion factors are plotted in Figure F.6
showing both linear and logarithmic interpolation.

Similar to ANSI/ANS-6.1.1-1991, the ICRP/74-1996 standard provides a
variety of neutron fluence-to-dose conversion factors assuming six
irradiation-phantom orientations: anterior-posterior (AP), posterior-
anterior (PA), left-lateral (LLAT), right-lateral (RLAT), rotational
(ROT), and isotropic (ISO). For more information, please see [363]. The
AP, PA, LLAT, RLAT, ROT, and ISO responses are given in Listings F.7,
F.8, F.9, F.10, F.11, F.12, respectively. Similarly to before, these can
be directly used as MCNP input for DE / DF cards. These conversion
factors are plotted in Figures F.7, F.8, F.9, F.10, F.11, and F.12
respectively.

In addition, ICRP/74-1996 provides ambient and personal dose equivalent
fluence-to-dose conversion factors assuming different orientations
relative to an ICRU sphere and slab [363]. These are given in Listings
F.13, F.14, F.15, F.16, F.17, F.18, and F.19, which are shown in Figures
F.13, F.14, F.15, F.16, F.17, F.18, and F.19, respectively.

Similar to ICRP/74-1996, the ICRP/116-2010 standard provides a variety
of neutron fluence-to-dose conversion factors assuming six irradiation-
phantom orientations: anterior-posterior (AP), posterior-anterior (PA),
leftlateral (LLAT), right-lateral (RLAT), rotational (ROT), and
isotropic (ISO). For more information, please see [364]. The AP, PA,
LLAT, RLAT, ROT, and ISO responses are given in Listings F.20, F.21,
F.22, F.23, F.24, F.25, respectively. Similarly to before, these can be
directly used as MCNP input for DE / DF cards. These conversion factors
are plotted in Figures F.20, F.21, F.22, F.23, F.24, and F.25
respectively.

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

Listing F.1: Neutron\_ANSIANS-611-1977\_dedf.txt

| c c ANSI/ANS-6.1.1-1977, from Table 1: c             | c c ANSI/ANS-6.1.1-1977, from Table 1: c             | c c ANSI/ANS-6.1.1-1977, from Table 1: c             |
|------------------------------------------------------|------------------------------------------------------|------------------------------------------------------|
| c Energy Flux-to-dose Conversion Factor              | c Energy Flux-to-dose Conversion Factor              | Quality Factor                                       |
| c [MeV] [(rem/hr)/(cm$^{-2}\cdot$s$^{-1}$)] [None] # | c [MeV] [(rem/hr)/(cm$^{-2}\cdot$s$^{-1}$)] [None] # | c [MeV] [(rem/hr)/(cm$^{-2}\cdot$s$^{-1}$)] [None] # |
| de:n                                                 | df:n                                                 |                                                      |
| log                                                  | log                                                  |                                                      |
| 2.5e-8                                               | 3.67e-6                                              | $ 2.0                                                |
| 1.0e-7                                               | 3.67e-6                                              | $ 2.0                                                |
| 1.0e-6                                               | 4.46e-6                                              | $ 2.0                                                |
| 1.0e-5                                               | 4.54e-6                                              | $ 2.0                                                |
| 1.0e-4                                               | 4.18e-6                                              | $ 2.0                                                |
| 1.0e-3                                               | 3.76e-6                                              | $ 2.0                                                |
| 0.01                                                 | 3.56e-6                                              | $ 2.5                                                |
| 0.1                                                  | 2.17e-5                                              | $ 7.5                                                |
| 0.5                                                  | 9.26e-5                                              | $ 11.0                                               |
| 1.0                                                  | 1.32e-4                                              | $ 11.0                                               |
| 2.5                                                  | 1.25e-4                                              | $ 9.0                                                |
| 5.0                                                  | 1.56e-4                                              | $ 8.0                                                |
| 7.0                                                  | 1.47e-4                                              | $ 7.0                                                |
| 10.0                                                 | 1.47e-4                                              | $ 6.5                                                |
| 14.0                                                 | 2.08e-4                                              | $ 7.5                                                |
| 20.0                                                 | 2.27e-4                                              | $ 8.0                                                |
| c                                                    |                                                      |                                                      |

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

28

29

30

31

Listing F.2: Neutron\_ANSIANS-611-1991\_Anterior-Posterior\_AP\_dedf.txt

| c c ANSI/ANS-6.1.1-1991, Anterior-Posterior (AP), from Table 4: c   | c c ANSI/ANS-6.1.1-1991, Anterior-Posterior (AP), from Table 4: c   |
|---------------------------------------------------------------------|---------------------------------------------------------------------|
| c Energy c [MeV]                                                    | Fluence-to-dose Conversion Factor [pSv$\cdot$cm$^{2}$]              |
| # de:n                                                              | df:n                                                                |
| log                                                                 | log                                                                 |
| 2.5e-8                                                              | 4.0                                                                 |
| 1.0e-7                                                              | 4.4                                                                 |
| 1.0e-6                                                              | 4.82                                                                |
| 1.0e-5                                                              | 4.46                                                                |
| 1.0e-4                                                              | 4.14                                                                |
| 1.0e-3                                                              | 3.83                                                                |
| 0.01                                                                | 4.53                                                                |
| 0.02                                                                | 5.87                                                                |
| 0.05                                                                | 10.9                                                                |
| 0.1                                                                 | 19.8                                                                |
| 0.2                                                                 | 38.6                                                                |
| 0.5                                                                 | 87.0                                                                |
| 1.0                                                                 | 143.0                                                               |
| 1.5                                                                 | 183.0                                                               |
| 2.0                                                                 | 214.0                                                               |
| 3.0                                                                 | 264.0                                                               |
| 4.0                                                                 | 300.0                                                               |
| 5.0                                                                 | 327.0                                                               |
| 6.0                                                                 | 347.0                                                               |
| 7.0                                                                 | 365.0                                                               |
| 8.0                                                                 | 380.0                                                               |
| 10.0                                                                | 410.0                                                               |
| 14.0                                                                | 480.0                                                               |

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

28

29

30

31

Listing F.3: Neutron\_ANSIANS-611-1991\_Posterior-Anterior\_PA\_dedf.txt

| c c ANSI/ANS-6.1.1-1991, Posterior-Anterior (PA), from Table 4: c   | c c ANSI/ANS-6.1.1-1991, Posterior-Anterior (PA), from Table 4: c   |
|---------------------------------------------------------------------|---------------------------------------------------------------------|
| c Energy c [MeV]                                                    | Fluence-to-dose Conversion Factor [pSv$\cdot$cm$^{2}$]              |
| # de:n                                                              | df:n                                                                |
| log                                                                 | log                                                                 |
| 2.5e-8                                                              | 2.6                                                                 |
| 1.0e-7                                                              | 2.7                                                                 |
| 1.0e-6                                                              | 2.81                                                                |
| 1.0e-5                                                              | 2.78                                                                |
| 1.0e-4                                                              | 2.63                                                                |
| 1.0e-3                                                              | 2.49                                                                |
| 0.01                                                                | 2.58                                                                |
| 0.02                                                                | 2.79                                                                |
| 0.05                                                                | 3.64                                                                |
| 0.1                                                                 | 5.69                                                                |
| 0.2                                                                 | 8.6                                                                 |
| 0.5                                                                 | 30.8                                                                |
| 1.0                                                                 | 53.5                                                                |
| 1.5                                                                 | 85.8                                                                |
| 2.0                                                                 | 120.0                                                               |
| 3.0                                                                 | 174.0                                                               |
| 4.0                                                                 | 215.0                                                               |
| 5.0                                                                 | 244.0                                                               |
| 6.0                                                                 | 265.0                                                               |
| 7.0                                                                 | 283.0                                                               |
| 8.0                                                                 | 296.0                                                               |
| 10.0                                                                | 321.0                                                               |
| 14.0                                                                | 415.0                                                               |

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

28

29

30

31

Listing F.4: Neutron\_ANSIANS-611-1991\_Lateral\_LAT\_dedf.txt

| c c ANSI/ANS-6.1.1-1991, Lateral (LAT), from Table 4: c   | c c ANSI/ANS-6.1.1-1991, Lateral (LAT), from Table 4: c   |
|-----------------------------------------------------------|-----------------------------------------------------------|
| c Energy c [MeV]                                          | Fluence-to-dose Conversion Factor [pSv$\cdot$cm$^{2}$]    |
| # de:n                                                    | df:n                                                      |
| log                                                       | log                                                       |
| 2.5e-8                                                    | 1.3                                                       |
| 1.0e-7                                                    | 1.4                                                       |
| 1.0e-6                                                    | 1.43                                                      |
| 1.0e-5                                                    | 1.33                                                      |
| 1.0e-4                                                    | 1.27                                                      |
| 1.0e-3                                                    | 1.19                                                      |
| 0.01                                                      | 1.27                                                      |
| 0.02                                                      | 1.46                                                      |
| 0.05                                                      | 2.14                                                      |
| 0.1                                                       | 3.57                                                      |
| 0.2                                                       | 6.94                                                      |
| 0.5                                                       | 18.7                                                      |
| 1.0                                                       | 33.3                                                      |
| 1.5                                                       | 52.1                                                      |
| 2.0                                                       | 71.8                                                      |
| 3.0                                                       | 105.0                                                     |
| 4.0                                                       | 131.0                                                     |
| 5.0                                                       | 151.0                                                     |
| 6.0                                                       | 167.0                                                     |
| 7.0                                                       | 181.0                                                     |
| 8.0                                                       | 194.0                                                     |
| 10.0                                                      | 218.0                                                     |
| 14.0                                                      | 280.0                                                     |

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

28

29

30

31

Listing F.5: Neutron\_ANSIANS-611-1991\_Rotational\_ROT\_dedf.txt

| c c ANSI/ANS-6.1.1-1991, Rotational (ROT), from Table 4:   | c c ANSI/ANS-6.1.1-1991, Rotational (ROT), from Table 4:   |
|------------------------------------------------------------|------------------------------------------------------------|
| c Energy c [MeV]                                           | Fluence-to-dose Conversion Factor [pSv$\cdot$cm$^{2}$]     |
| # de:n                                                     | df:n                                                       |
| log                                                        | log                                                        |
| 2.5e-8                                                     | 2.3                                                        |
| 1.0e-7                                                     | 2.4                                                        |
| 1.0e-6                                                     | 2.63                                                       |
| 1.0e-5                                                     | 2.48                                                       |
| 1.0e-4                                                     | 2.33                                                       |
| 1.0e-3                                                     | 2.18                                                       |
| 0.01                                                       | 2.41                                                       |
| 0.02                                                       | 2.89                                                       |
| 0.05                                                       | 4.7                                                        |
| 0.1                                                        | 8.15                                                       |
| 0.2                                                        | 15.3                                                       |
| 0.5                                                        | 38.8                                                       |
| 1.0                                                        | 65.7                                                       |
| 1.5                                                        | 93.7                                                       |
| 2.0                                                        | 120.0                                                      |
| 3.0                                                        | 162.0                                                      |
| 4.0                                                        | 195.0                                                      |
| 5.0                                                        | 219.0                                                      |
| 6.0                                                        | 237.0                                                      |
| 7.0                                                        | 253.0                                                      |
| 8.0                                                        | 266.0                                                      |
| 10.0                                                       | 292.0                                                      |
| 14.0                                                       | 365.0                                                      |
| c                                                          | c                                                          |

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

28

29

Listing F.6: Neutron\_ICRP21-1973\_dedf.txt

<!-- image -->

| c c ICRP/21-1973, from Table 4, with Modifications: c                                            | c c ICRP/21-1973, from Table 4, with Modifications: c   |
|--------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| c Energy Flux-to-dose Conversion Factor c [MeV] [(mrem/hr)/(cm$^{-2}\cdot$s$^{-1}$)] # de:n df:n | Quality Factor [None]                                   |
| 2.5e-8                                                                                           | 3.846e-3 $ 2.3                                          |
| 1.0e-7                                                                                           | 4.167e-3 $ 2.0                                          |
| 1.0e-6 4.546e-3                                                                                  | $ 2.0                                                   |
| 1.0e-5                                                                                           | 4.348e-3 $ 2.0                                          |
| 1.0e-4                                                                                           | 4.167e-3 $ 2.0                                          |
| 1.0e-3                                                                                           | 3.704e-3 $ 2.0                                          |
| 0.01                                                                                             | 3.571e-3 $ 2.0                                          |
| 0.1                                                                                              | 0.02083 $ 7.4                                           |
| 0.5                                                                                              | 0.07143 $ 11.0                                          |
| 1.0                                                                                              | 0.1176 $ 10.6                                           |
| 2.0                                                                                              | 0.1429 $ 9.3                                            |
| 5.0                                                                                              | 0.1471 $ 7.8                                            |
| 10.0                                                                                             | 0.1471 $ 6.8                                            |
| 20.0                                                                                             | 0.1538 $ 6.0                                            |
| 50.0                                                                                             | 0.1639 $ 5.0                                            |
| 100.0 0.1786                                                                                     | $ 4.4                                                   |
| 500.0                                                                                            | 0.2778 $ 3.2                                            |
| 1.0e3 0.4545                                                                                     | $ 2.8                                                   |
| 2.0e3                                                                                            | $ 2.6                                                   |
| 0.625                                                                                            |                                                         |
| 3.0e3                                                                                            | 0.7143 $ 2.5                                            |

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

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

Listing F.7: Neutron\_ICRP74-1996\_Anterior-Posterior\_AP\_dedf.txt

| ICRP/74-1996, Anterior-Posterior (AP), from Table A.41:   | ICRP/74-1996, Anterior-Posterior (AP), from Table A.41:   |
|-----------------------------------------------------------|-----------------------------------------------------------|
| Energy Fluence-to-dose [MeV]                              | [pSv$\cdot$cm$^{2}$]                                      |
| de:n                                                      | df:n                                                      |
| log                                                       | log                                                       |
| 1.0e-9 1.0e-8                                             | 5.24 6.55                                                 |
| 2.5e-8                                                    |                                                           |
|                                                           | 7.6                                                       |
| 1.0e-7                                                    | 9.95                                                      |
| 2.0e-7                                                    | 11.2                                                      |
| 5.0e-7                                                    | 12.8                                                      |
| 1.0e-6                                                    | 13.8                                                      |
| 2.0e-6                                                    | 14.5                                                      |
| 5.0e-6                                                    | 15.0                                                      |
| 1.0e-5                                                    | 15.1                                                      |
| 2.0e-5                                                    | 15.1                                                      |
| 5.0e-5                                                    | 14.8                                                      |
| 1.0e-4                                                    | 14.6                                                      |
| 2.0e-4                                                    | 14.4                                                      |
| 5.0e-4                                                    | 14.2                                                      |
| 1.0e-3                                                    | 14.2                                                      |
| 2.0e-3                                                    | 14.4                                                      |
| 5.0e-3                                                    | 15.7                                                      |
| 0.01                                                      | 18.3                                                      |
| 0.02                                                      | 23.8                                                      |
| 0.03                                                      | 29.0                                                      |
| 0.05                                                      | 38.5                                                      |
| 0.07 0.1                                                  | 47.2 59.8                                                 |
| 0.15                                                      | 80.2                                                      |
| 0.2                                                       | 99.0                                                      |
| 0.3                                                       | 133.0 188.0                                               |
| 0.5 0.7                                                   | 231.0                                                     |
| 0.9                                                       | 267.0                                                     |
| 1.0                                                       | 282.0                                                     |
| 1.2                                                       | 310.0                                                     |
| 2.0                                                       | 383.0                                                     |
| 3.0                                                       | 432.0                                                     |
| 5.0                                                       | 458.0                                                     |
| 4.0                                                       | 474.0                                                     |
| 6.0                                                       | 483.0                                                     |
| 7.0                                                       | 490.0                                                     |
| 8.0                                                       | 494.0                                                     |
| 9.0                                                       | 497.0                                                     |
| 10.0                                                      | 499.0                                                     |
| 12.0                                                      | 499.0                                                     |
| 14.0                                                      | 496.0                                                     |
| 15.0                                                      | 494.0                                                     |
| 16.0                                                      | 491.0 486.0                                               |
| 18.0                                                      |                                                           |
| 20.0 30.0                                                 | 480.0 458.0                                               |
|                                                           | 437.0                                                     |
| 50.0 75.0                                                 | 429.0                                                     |
| 100.0                                                     | 429.0                                                     |
| 130.0 150.0                                               | 432.0 438.0                                               |
| 180.0                                                     | 445.0                                                     |

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

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

Listing F.8: Neutron\_ICRP74-1996\_Posterior-Anterior\_PA\_dedf.txt

| ICRP/74-1996, Posterior-Anterior (PA), from Table A.41:   | ICRP/74-1996, Posterior-Anterior (PA), from Table A.41:   |
|-----------------------------------------------------------|-----------------------------------------------------------|
| Energy Fluence-to-dose [MeV]                              | [pSv$\cdot$cm$^{2}$]                                      |
| de:n                                                      | df:n                                                      |
| log                                                       | log                                                       |
| 1.0e-9 1.0e-8                                             | 3.52 4.39                                                 |
| 2.5e-8                                                    |                                                           |
|                                                           | 5.16                                                      |
| 1.0e-7                                                    | 6.77                                                      |
| 2.0e-7                                                    | 7.63                                                      |
| 5.0e-7                                                    | 8.76                                                      |
| 1.0e-6                                                    | 9.55                                                      |
| 2.0e-6                                                    | 10.2                                                      |
| 5.0e-6                                                    | 10.7                                                      |
| 1.0e-5                                                    | 11.0                                                      |
| 2.0e-5                                                    | 11.1                                                      |
| 5.0e-5                                                    | 11.1                                                      |
| 1.0e-4                                                    | 11.0                                                      |
| 2.0e-4                                                    | 10.9                                                      |
| 5.0e-4                                                    | 10.7                                                      |
| 1.0e-3                                                    | 10.7                                                      |
| 2.0e-3                                                    | 10.8                                                      |
| 5.0e-3                                                    | 11.6                                                      |
| 0.01                                                      | 13.5                                                      |
| 0.02                                                      | 17.3                                                      |
| 0.03                                                      | 21.0                                                      |
| 0.05                                                      | 27.6                                                      |
| 0.07                                                      | 33.5                                                      |
| 0.1                                                       | 41.3                                                      |
| 0.15                                                      | 77.1                                                      |
| 0.2                                                       | 52.2 61.5                                                 |
| 0.3                                                       | 103.0                                                     |
| 0.5 0.7                                                   | 124.0                                                     |
| 0.9                                                       | 144.0                                                     |
| 1.0                                                       | 154.0                                                     |
| 1.2                                                       | 175.0                                                     |
| 2.0                                                       | 247.0                                                     |
| 3.0                                                       | 308.0                                                     |
|                                                           | 366.0                                                     |
| 4.0 5.0                                                   | 345.0                                                     |
| 6.0                                                       | 380.0                                                     |
| 7.0                                                       | 391.0                                                     |
| 8.0                                                       | 399.0                                                     |
| 9.0                                                       | 406.0                                                     |
| 10.0                                                      | 412.0                                                     |
| 12.0                                                      | 422.0                                                     |
| 14.0                                                      | 429.0                                                     |
| 15.0                                                      | 431.0 433.0                                               |
| 16.0                                                      | 435.0 436.0                                               |
| 18.0                                                      |                                                           |
| 20.0 30.0                                                 | 437.0                                                     |
|                                                           | 444.0                                                     |
| 50.0 75.0                                                 | 459.0                                                     |
|                                                           | 477.0                                                     |
| 100.0                                                     | 495.0                                                     |
| 130.0 150.0                                               | 514.0                                                     |
| 180.0                                                     | 535.0                                                     |

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

47

48

49

50

51

52

53

54

55

Listing F.9: Neutron\_ICRP74-1996\_L-Lateral\_LLAT\_dedf.txt

| c c ICRP/74-1996, L-Lateral (LLAT), from Table A.41:   | c c ICRP/74-1996, L-Lateral (LLAT), from Table A.41:   |
|--------------------------------------------------------|--------------------------------------------------------|
| c c Fluence-to-dose Conversion Factor                  | c c Fluence-to-dose Conversion Factor                  |
| Energy c [MeV]                                         | [pSv$\cdot$cm$^{2}$]                                   |
| # de:n                                                 | df:n                                                   |
| log                                                    | log                                                    |
| 1.0e-9                                                 | 1.68                                                   |
| 1.0e-8                                                 | 2.04                                                   |
| 2.5e-8                                                 | 2.31                                                   |
| 1.0e-7                                                 | 2.86                                                   |
| 2.0e-7                                                 | 3.21                                                   |
| 5.0e-7                                                 | 3.72                                                   |
| 1.0e-6                                                 | 4.12                                                   |
| 2.0e-6                                                 | 4.39                                                   |
| 5.0e-6                                                 | 4.66                                                   |
| 1.0e-5                                                 | 4.8                                                    |
| 2.0e-5                                                 | 4.89                                                   |
| 5.0e-5                                                 | 4.95                                                   |
| 1.0e-4                                                 | 4.95                                                   |
| 2.0e-4                                                 | 4.92                                                   |
| 5.0e-4                                                 | 4.86                                                   |
| 1.0e-3                                                 | 4.84                                                   |
| 2.0e-3                                                 | 4.87                                                   |
| 5.0e-3                                                 | 5.25                                                   |
| 0.01                                                   | 6.14                                                   |
| 0.02                                                   | 7.95                                                   |
| 0.03                                                   | 9.74                                                   |
| 0.05                                                   | 13.1                                                   |
| 0.07                                                   | 16.1                                                   |
| 0.1                                                    | 20.1                                                   |
| 0.15                                                   | 25.5                                                   |
| 0.2                                                    | 30.3                                                   |
| 0.3                                                    | 38.6                                                   |
| 0.5                                                    | 53.2                                                   |
| 0.7                                                    | 66.6                                                   |
| 0.9                                                    | 79.6                                                   |
| 1.0                                                    | 86.0                                                   |
| 1.2                                                    | 99.8                                                   |
| 2.0                                                    | 153.0                                                  |
| 3.0                                                    | 195.0                                                  |
| 4.0 5.0                                                | 224.0 244.0                                            |
| 6.0                                                    |                                                        |
|                                                        | 261.0                                                  |
| 7.0                                                    | 274.0                                                  |
| 8.0 9.0                                                | 285.0 294.0                                            |
| 10.0                                                   |                                                        |
|                                                        | 302.0                                                  |
| 12.0                                                   | 315.0                                                  |
| 14.0                                                   | 324.0                                                  |
| 15.0 16.0                                              | 328.0 331.0                                            |
| 18.0                                                   | 335.0                                                  |
| 20.0                                                   | 338.0                                                  |

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

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

Listing F.10: Neutron\_ICRP74-1996\_R-Lateral\_RLAT\_dedf.txt

| ICRP/74-1996, R-Lateral (RLAT), from Table A.41:   | ICRP/74-1996, R-Lateral (RLAT), from Table A.41:   |
|----------------------------------------------------|----------------------------------------------------|
| Energy Fluence-to-dose [MeV]                       | Conversion Factor [pSv$\cdot$cm$^{2}$]             |
| de:n                                               | df:n                                               |
| log                                                | log                                                |
| 1.0e-9                                             | 1.36                                               |
| 1.0e-8                                             | 1.7                                                |
| 2.5e-8                                             | 1.99                                               |
| 1.0e-7                                             | 2.58                                               |
| 2.0e-7                                             | 2.92                                               |
| 5.0e-7                                             | 3.35                                               |
| 1.0e-6                                             | 3.67                                               |
| 2.0e-6                                             | 3.89                                               |
| 5.0e-6                                             | 4.08                                               |
| 1.0e-5                                             | 4.16                                               |
| 2.0e-5                                             | 4.2                                                |
| 5.0e-5                                             | 4.19                                               |
| 1.0e-4                                             | 4.15                                               |
| 2.0e-4                                             | 4.1                                                |
| 5.0e-4                                             | 4.03                                               |
| 1.0e-3                                             | 4.0                                                |
| 2.0e-3                                             | 4.0                                                |
| 5.0e-3                                             | 4.29                                               |
| 0.01                                               | 5.02                                               |
| 0.02                                               | 6.48                                               |
| 0.03                                               | 7.93                                               |
| 0.05                                               | 10.6                                               |
| 0.07                                               | 13.1                                               |
| 0.1                                                | 16.4                                               |
| 0.15 0.2                                           | 21.2 25.6                                          |
|                                                    | 33.4                                               |
| 0.3                                                | 46.8                                               |
| 0.5 0.7                                            | 58.3                                               |
| 0.9                                                | 69.1                                               |
| 1.0                                                | 74.5                                               |
| 1.2                                                | 85.8                                               |
| 2.0                                                | 129.0                                              |
| 3.0                                                | 171.0                                              |
| 6.0                                                |                                                    |
| 5.0                                                | 217.0                                              |
|                                                    | 232.0                                              |
| 7.0                                                | 244.0                                              |
| 8.0                                                | 253.0                                              |
| 9.0                                                | 261.0                                              |
| 10.0 12.0                                          | 268.0 278.0                                        |
| 14.0                                               | 286.0                                              |
| 15.0                                               | 290.0                                              |
| 16.0                                               | 293.0                                              |
| 18.0                                               | 299.0                                              |
| 20.0 30.0                                          | 305.0 324.0                                        |
|                                                    | 358.0                                              |
| 50.0 75.0                                          | 397.0                                              |
|                                                    | 433.0                                              |
| 100.0                                              | 467.0                                              |
| 130.0 150.0                                        | 501.0                                              |
| 180.0                                              | 542.0                                              |

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

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

Listing F.11: Neutron\_ICRP74-1996\_Rotational\_ROT\_dedf.txt

| c c ICRP/74-1996, Rotational (ROT), from Table A.41: c   | c c ICRP/74-1996, Rotational (ROT), from Table A.41: c   |
|----------------------------------------------------------|----------------------------------------------------------|
| Energy Fluence-to-dose [MeV]                             | Conversion Factor [pSv$\cdot$cm$^{2}$]                   |
| de:n                                                     | df:n                                                     |
| log                                                      | log                                                      |
| 1.0e-9 1.0e-8                                            | 2.99                                                     |
| 2.5e-8                                                   | 3.72 4.4                                                 |
| 1.0e-7                                                   | 5.75                                                     |
| 2.0e-7 5.0e-7                                            | 6.43                                                     |
|                                                          | 7.27                                                     |
| 1.0e-6                                                   | 7.84                                                     |
| 2.0e-6                                                   | 8.31                                                     |
| 5.0e-6                                                   | 8.72                                                     |
| 1.0e-5                                                   | 8.9                                                      |
| 2.0e-5                                                   | 8.92                                                     |
| 5.0e-5                                                   | 8.82                                                     |
| 1.0e-4                                                   | 8.69                                                     |
| 2.0e-4                                                   | 8.56                                                     |
| 5.0e-4                                                   | 8.4                                                      |
| 1.0e-3                                                   | 8.34                                                     |
| 2.0e-3                                                   | 8.39                                                     |
| 5.0e-3                                                   | 9.06                                                     |
| 0.01                                                     | 10.6                                                     |
| 0.02                                                     | 13.8                                                     |
| 0.03                                                     | 16.9 22.7                                                |
| 0.05 0.07                                                | 27.8                                                     |
| 0.1 0.15                                                 | 34.8 45.4                                                |
| 0.2                                                      | 71.6                                                     |
| 0.3                                                      | 54.8                                                     |
| 0.5                                                      | 99.4 123.0                                               |
| 0.7                                                      |                                                          |
| 0.9                                                      | 144.0                                                    |
| 1.0                                                      | 154.0                                                    |
| 1.2                                                      | 173.0 234.0                                              |
| 2.0                                                      | 283.0                                                    |
| 3.0 4.0                                                  | 315.0                                                    |
| 6.0                                                      | 335.0                                                    |
| 5.0                                                      | 348.0                                                    |
| 7.0                                                      | 358.0                                                    |
| 8.0                                                      | 366.0                                                    |
| 10.0                                                     | 378.0                                                    |
| 9.0                                                      | 373.0                                                    |
| 12.0                                                     | 385.0                                                    |
|                                                          | 390.0                                                    |
| 14.0 15.0                                                | 391.0 393.0                                              |
| 16.0                                                     | 394.0                                                    |
| 18.0 20.0                                                | 395.0                                                    |
| 30.0                                                     | 395.0                                                    |
| 50.0                                                     | 404.0 422.0                                              |
| 75.0                                                     |                                                          |
| 100.0                                                    | 443.0                                                    |
| 130.0                                                    | 465.0 489.0                                              |
| 150.0                                                    |                                                          |
| 180.0                                                    | 517.0                                                    |

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

47

48

49

50

51

52

53

54

55

Listing F.12: Neutron\_ICRP74-1996\_Isotropic\_ISO\_dedf.txt

| c c ICRP/74-1996, Isotropic (ISO), from Table A.41:   | c c ICRP/74-1996, Isotropic (ISO), from Table A.41:   |
|-------------------------------------------------------|-------------------------------------------------------|
| c c Fluence-to-dose Conversion Factor                 | c c Fluence-to-dose Conversion Factor                 |
| Energy c [MeV]                                        | [pSv$\cdot$cm$^{2}$]                                  |
| # de:n                                                | df:n                                                  |
| log                                                   | log                                                   |
| 1.0e-9                                                | 2.4                                                   |
| 1.0e-8                                                | 2.89                                                  |
| 2.5e-8                                                | 3.3                                                   |
| 1.0e-7                                                | 4.13                                                  |
| 2.0e-7                                                | 4.59                                                  |
| 5.0e-7                                                | 5.2                                                   |
| 1.0e-6                                                | 5.63                                                  |
| 2.0e-6                                                | 5.96                                                  |
| 5.0e-6                                                | 6.28                                                  |
| 1.0e-5                                                | 6.44                                                  |
| 2.0e-5                                                | 6.51                                                  |
| 5.0e-5                                                | 6.51                                                  |
| 1.0e-4                                                | 6.45                                                  |
| 2.0e-4                                                | 6.32                                                  |
| 5.0e-4                                                | 6.14                                                  |
| 1.0e-3                                                | 6.04                                                  |
| 2.0e-3                                                | 6.05                                                  |
| 5.0e-3                                                | 6.52                                                  |
| 0.01                                                  | 7.7                                                   |
| 0.02                                                  | 10.2                                                  |
| 0.03                                                  | 12.7                                                  |
| 0.05                                                  | 17.3                                                  |
| 0.07                                                  | 21.5                                                  |
| 0.1                                                   | 27.2                                                  |
| 0.15                                                  | 35.2                                                  |
| 0.2                                                   | 42.4                                                  |
| 0.3                                                   | 54.7                                                  |
| 0.5                                                   | 75.0                                                  |
| 0.7                                                   | 92.8                                                  |
| 0.9                                                   | 108.0                                                 |
| 1.0                                                   | 116.0                                                 |
| 1.2                                                   | 130.0                                                 |
| 2.0 3.0                                               | 178.0                                                 |
|                                                       | 220.0                                                 |
| 4.0                                                   | 250.0 272.0                                           |
| 5.0                                                   | 282.0                                                 |
| 6.0                                                   |                                                       |
| 7.0                                                   | 290.0                                                 |
| 8.0 9.0                                               | 297.0 303.0                                           |
| 10.0                                                  | 309.0                                                 |
| 12.0                                                  |                                                       |
|                                                       | 322.0                                                 |
| 14.0                                                  | 333.0                                                 |
| 15.0 16.0                                             | 338.0 342.0                                           |
| 18.0                                                  | 345.0                                                 |
| 20.0                                                  | 343.0                                                 |

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

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

Listing F.13: Neutron\_ICRP74-1996\_H10Phi\_dedf.txt

| c c ICRP/74-1996, $H^{ * }(10)/Phi$, from Table A.42:   | c c ICRP/74-1996, $H^{ * }(10)/Phi$, from Table A.42:   |
|---------------------------------------------------------|---------------------------------------------------------|
| Energy Fluence-to-dose [MeV]                            | [pSv$\cdot$cm$^{2}$]                                    |
| de:n                                                    | df:n                                                    |
| log                                                     | log                                                     |
| 1.0e-9                                                  | 6.6                                                     |
| 1.0e-8                                                  | 9.0                                                     |
| 2.53e-8                                                 | 10.6                                                    |
| 1.0e-7                                                  | 12.9                                                    |
| 2.0e-7                                                  | 13.5                                                    |
| 5.0e-7                                                  | 13.6                                                    |
| 1.0e-6                                                  | 13.3                                                    |
| 2.0e-6                                                  | 12.9                                                    |
| 5.0e-6                                                  | 12.0                                                    |
| 1.0e-5                                                  | 11.3                                                    |
| 2.0e-5                                                  | 10.6                                                    |
| 5.0e-5                                                  | 9.9                                                     |
| 1.0e-4                                                  | 9.4                                                     |
| 2.0e-4                                                  | 8.9                                                     |
| 5.0e-4                                                  | 8.3                                                     |
| 1.0e-3                                                  | 7.9                                                     |
| 2.0e-3                                                  | 7.7                                                     |
| 5.0e-3                                                  | 8.0                                                     |
| 0.01 0.02                                               | 10.5 16.6                                               |
| 0.03                                                    | 23.7 41.1                                               |
| 0.05 0.07                                               | 60.0                                                    |
| 0.1                                                     | 88.0                                                    |
| 0.15                                                    | 132.0                                                   |
| 0.2                                                     | 170.0                                                   |
| 0.3                                                     | 233.0                                                   |
| 0.5                                                     | 322.0                                                   |
| 0.7                                                     | 375.0                                                   |
| 0.9                                                     | 400.0                                                   |
| 1.0                                                     | 416.0                                                   |
| 1.2                                                     | 425.0                                                   |
| 2.0                                                     | 420.0                                                   |
| 3.0                                                     | 412.0                                                   |
| 4.0                                                     | 408.0                                                   |
| 5.0 6.0                                                 | 405.0 400.0                                             |
| 7.0                                                     | 405.0                                                   |
| 8.0                                                     | 409.0                                                   |
| 9.0                                                     | 420.0                                                   |
| 10.0                                                    | 440.0                                                   |
| 12.0                                                    | 480.0                                                   |
| 14.0                                                    | 520.0                                                   |
| 15.0                                                    | 540.0                                                   |
| 16.0                                                    | 555.0                                                   |
| 18.0                                                    | 570.0                                                   |
| 20.0                                                    | 600.0                                                   |
| 30.0                                                    | 515.0                                                   |
| 50.0                                                    | 400.0 330.0                                             |
| 75.0                                                    |                                                         |
| 100.0                                                   | 285.0                                                   |
| 130.0                                                   | 260.0                                                   |
| 150.0 175.0                                             | 245.0 250.0                                             |
|                                                         | 260.0                                                   |
| 201.0                                                   |                                                         |

63

c

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

47

48

49

50

51

52

53

54

55

Listing F.14: Neutron\_ICRP74-1996\_H\_textrmpslab100circPhi\_dedf.txt

| c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,0^{\circ})/Phi$, from Table A.42:   | c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,0^{\circ})/Phi$, from Table A.42:   |
|---------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor                                    | c c Energy Fluence-to-dose Conversion Factor                                    |
| [MeV]                                                                           | [pSv$\cdot$cm$^{2}$]                                                            |
| de:n log                                                                        | df:n log                                                                        |
| 1.0e-9                                                                          | 8.19                                                                            |
| 1.0e-8                                                                          | 9.97                                                                            |
| 2.53e-8                                                                         | 11.4                                                                            |
| 1.0e-7                                                                          | 12.6                                                                            |
| 2.0e-7                                                                          | 13.5                                                                            |
| 5.0e-7                                                                          | 14.2                                                                            |
| 1.0e-6                                                                          | 14.4                                                                            |
|                                                                                 | 14.3                                                                            |
| 2.0e-6                                                                          |                                                                                 |
| 5.0e-6                                                                          | 13.8                                                                            |
| 1.0e-5                                                                          | 13.2                                                                            |
| 2.0e-5                                                                          | 12.4                                                                            |
| 5.0e-5                                                                          |                                                                                 |
|                                                                                 | 11.2                                                                            |
| 1.0e-4                                                                          | 10.3                                                                            |
| 2.0e-4                                                                          | 9.84                                                                            |
| 1.0e-3                                                                          | 8.78                                                                            |
| 2.0e-3                                                                          | 8.72                                                                            |
| 5.0e-3                                                                          | 9.36 11.2                                                                       |
| 0.01                                                                            | 17.1                                                                            |
| 0.02 0.03                                                                       | 24.9                                                                            |
| 0.05                                                                            | 39.0                                                                            |
|                                                                                 | 59.0                                                                            |
| 0.07                                                                            | 90.6                                                                            |
| 0.1                                                                             | 139.0                                                                           |
| 0.15 0.2                                                                        | 180.0                                                                           |
| 0.3                                                                             | 246.0                                                                           |
| 0.5                                                                             | 335.0                                                                           |
| 0.7                                                                             | 386.0                                                                           |
| 0.9                                                                             | 414.0                                                                           |
| 1.0                                                                             | 422.0                                                                           |
| 1.2                                                                             | 433.0                                                                           |
| 2.0                                                                             | 442.0                                                                           |
| 3.0                                                                             | 431.0                                                                           |
| 4.0                                                                             | 422.0                                                                           |
| 5.0                                                                             | 420.0                                                                           |
| 6.0                                                                             | 423.0                                                                           |
| 7.0                                                                             | 432.0                                                                           |
| 8.0                                                                             | 445.0                                                                           |
| 9.0                                                                             | 461.0                                                                           |
| 10.0                                                                            | 480.0                                                                           |
| 12.0                                                                            | 517.0                                                                           |
|                                                                                 | 550.0                                                                           |
| 14.0 15.0                                                                       | 564.0                                                                           |
| 16.0                                                                            | 576.0                                                                           |
| 18.0                                                                            | 595.0                                                                           |
| 20.0                                                                            | 600.0                                                                           |

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

47

48

49

50

51

52

53

54

55

Listing F.15: Neutron\_ICRP74-1996\_H\_textrmpslab1015circPhi\_dedf.txt

| c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,15^{\circ})/Phi$, from Table A.42:   | c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,15^{\circ})/Phi$, from Table A.42:   |
|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor                                     | c c Energy Fluence-to-dose Conversion Factor                                     |
| [MeV]                                                                            | [pSv$\cdot$cm$^{2}$]                                                             |
| de:n                                                                             | df:n                                                                             |
| log                                                                              | log                                                                              |
| 1.0e-9                                                                           | 7.64                                                                             |
| 1.0e-8                                                                           | 9.35                                                                             |
| 2.53e-8                                                                          | 10.6                                                                             |
| 1.0e-7                                                                           | 11.7                                                                             |
| 2.0e-7                                                                           | 12.6                                                                             |
| 5.0e-7                                                                           | 13.5                                                                             |
| 1.0e-6                                                                           | 13.9                                                                             |
| 2.0e-6                                                                           | 14.0                                                                             |
| 5.0e-6                                                                           | 13.9                                                                             |
| 1.0e-5                                                                           | 13.4                                                                             |
| 2.0e-5                                                                           | 12.6                                                                             |
| 5.0e-5                                                                           | 11.2                                                                             |
| 1.0e-4                                                                           | 9.85                                                                             |
| 2.0e-4                                                                           | 9.41                                                                             |
| 5.0e-4                                                                           | 8.66                                                                             |
| 1.0e-3                                                                           | 8.2                                                                              |
| 2.0e-3                                                                           | 8.22                                                                             |
| 5.0e-3                                                                           | 8.79                                                                             |
| 0.01                                                                             | 10.8                                                                             |
| 0.02                                                                             | 17.0                                                                             |
| 0.03 0.05                                                                        | 24.1                                                                             |
|                                                                                  | 36.0                                                                             |
| 0.07                                                                             | 55.8                                                                             |
| 0.1                                                                              | 87.8                                                                             |
| 0.15 0.2                                                                         | 137.0 179.0                                                                      |
| 0.3                                                                              | 244.0                                                                            |
| 0.5                                                                              | 330.0                                                                            |
| 0.7                                                                              | 379.0                                                                            |
| 0.9                                                                              | 407.0                                                                            |
| 1.0                                                                              | 416.0                                                                            |
| 1.2                                                                              | 427.0                                                                            |
| 2.0                                                                              | 438.0                                                                            |
| 3.0                                                                              | 429.0                                                                            |
| 4.0                                                                              | 421.0                                                                            |
| 5.0                                                                              | 418.0                                                                            |
| 6.0                                                                              |                                                                                  |
| 7.0                                                                              | 422.0 432.0                                                                      |
| 8.0                                                                              | 445.0                                                                            |
| 9.0                                                                              | 462.0                                                                            |
| 10.0                                                                             | 481.0                                                                            |
| 12.0                                                                             | 519.0                                                                            |
| 14.0                                                                             | 552.0                                                                            |
| 15.0                                                                             | 565.0                                                                            |
| 16.0 18.0                                                                        | 577.0 593.0                                                                      |
| 20.0                                                                             | 595.0                                                                            |

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

47

48

49

50

51

52

53

54

55

Listing F.16: Neutron\_ICRP74-1996\_H\_textrmpslab1030circPhi\_dedf.txt

| c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,30^{\circ})/Phi$, from Table A.42:   | c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,30^{\circ})/Phi$, from Table A.42:   |
|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor                                     | c c Energy Fluence-to-dose Conversion Factor                                     |
| [MeV]                                                                            | [pSv$\cdot$cm$^{2}$]                                                             |
| de:n                                                                             | df:n                                                                             |
| log                                                                              | log                                                                              |
| 1.0e-9                                                                           | 6.57                                                                             |
| 1.0e-8                                                                           | 7.9                                                                              |
| 2.53e-8                                                                          | 9.11                                                                             |
| 1.0e-7                                                                           | 10.3                                                                             |
| 2.0e-7                                                                           | 11.1                                                                             |
| 5.0e-7                                                                           | 11.8                                                                             |
| 1.0e-6                                                                           | 12.0                                                                             |
| 2.0e-6                                                                           | 11.9                                                                             |
| 5.0e-6                                                                           | 11.5                                                                             |
| 1.0e-5                                                                           | 11.0                                                                             |
| 2.0e-5                                                                           | 10.4                                                                             |
| 5.0e-5                                                                           | 9.42                                                                             |
| 1.0e-4                                                                           | 8.64                                                                             |
| 2.0e-4                                                                           | 8.22                                                                             |
| 5.0e-4                                                                           | 7.66                                                                             |
| 1.0e-3                                                                           | 7.29                                                                             |
| 2.0e-3                                                                           | 7.27                                                                             |
| 5.0e-3                                                                           | 7.46                                                                             |
| 0.01                                                                             | 9.18                                                                             |
| 0.02                                                                             | 14.6                                                                             |
| 0.03                                                                             | 21.3                                                                             |
| 0.05                                                                             | 34.4                                                                             |
| 0.07                                                                             | 52.6                                                                             |
| 0.1                                                                              | 81.3                                                                             |
| 0.15                                                                             | 126.0                                                                            |
| 0.2                                                                              | 166.0                                                                            |
| 0.3                                                                              | 232.0                                                                            |
| 0.5                                                                              | 326.0                                                                            |
| 0.7                                                                              | 382.0                                                                            |
| 0.9                                                                              | 415.0                                                                            |
| 1.0                                                                              | 426.0                                                                            |
| 1.2                                                                              | 440.0                                                                            |
| 2.0                                                                              | 457.0                                                                            |
| 3.0                                                                              | 449.0                                                                            |
| 4.0                                                                              | 440.0                                                                            |
| 5.0                                                                              | 437.0                                                                            |
| 6.0                                                                              | 440.0                                                                            |
| 7.0                                                                              | 449.0                                                                            |
| 8.0                                                                              | 462.0                                                                            |
| 9.0                                                                              | 478.0                                                                            |
| 10.0                                                                             | 497.0                                                                            |
| 12.0                                                                             | 536.0                                                                            |
| 14.0                                                                             | 570.0                                                                            |
| 15.0                                                                             | 584.0                                                                            |
| 16.0 18.0                                                                        | 597.0 617.0                                                                      |
| 20.0                                                                             |                                                                                  |
|                                                                                  | 619.0                                                                            |

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

47

48

49

50

51

52

53

54

55

Listing F.17: Neutron\_ICRP74-1996\_H\_textrmpslab1045circPhi\_dedf.txt

| c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,45^{\circ})/Phi$, from Table A.42:   | c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,45^{\circ})/Phi$, from Table A.42:   |
|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor                                     | c c Energy Fluence-to-dose Conversion Factor                                     |
| [MeV]                                                                            | [pSv$\cdot$cm$^{2}$]                                                             |
| de:n log                                                                         | df:n log                                                                         |
| 1.0e-9                                                                           | 4.23                                                                             |
| 1.0e-8 2.53e-8                                                                   | 5.38 6.61                                                                        |
| 1.0e-7                                                                           | 7.84                                                                             |
| 2.0e-7                                                                           | 8.73                                                                             |
| 5.0e-7                                                                           | 9.4                                                                              |
| 1.0e-6                                                                           | 9.56                                                                             |
|                                                                                  | 9.49                                                                             |
| 2.0e-6                                                                           |                                                                                  |
| 5.0e-6                                                                           | 9.11 8.65                                                                        |
| 1.0e-5                                                                           |                                                                                  |
| 5.0e-5                                                                           | 7.32                                                                             |
| 2.0e-5                                                                           | 8.1                                                                              |
| 1.0e-4                                                                           | 6.74                                                                             |
| 2.0e-4                                                                           | 6.21                                                                             |
| 1.0e-3                                                                           | 5.43                                                                             |
| 2.0e-3                                                                           | 5.43                                                                             |
| 5.0e-3                                                                           | 5.71                                                                             |
| 0.01                                                                             | 7.09                                                                             |
| 0.02                                                                             | 11.6 16.7                                                                        |
| 0.03                                                                             | 27.5                                                                             |
| 0.05                                                                             | 42.9                                                                             |
| 0.07 0.1                                                                         | 67.1                                                                             |
| 0.15                                                                             | 106.0                                                                            |
| 0.2                                                                              | 141.0                                                                            |
| 0.3                                                                              | 201.0                                                                            |
| 0.5                                                                              | 291.0                                                                            |
| 0.7                                                                              | 348.0                                                                            |
| 0.9                                                                              | 383.0                                                                            |
| 1.0                                                                              | 395.0                                                                            |
| 1.2                                                                              | 412.0                                                                            |
| 2.0                                                                              | 439.0                                                                            |
| 3.0                                                                              | 440.0                                                                            |
| 4.0                                                                              | 435.0                                                                            |
| 5.0                                                                              | 435.0                                                                            |
| 6.0                                                                              | 439.0                                                                            |
| 7.0                                                                              | 448.0                                                                            |
| 8.0                                                                              | 460.0                                                                            |
| 9.0                                                                              | 476.0                                                                            |
| 10.0                                                                             | 493.0                                                                            |
| 12.0                                                                             | 529.0                                                                            |
| 14.0                                                                             |                                                                                  |
| 15.0                                                                             | 561.0 575.0                                                                      |
| 16.0                                                                             | 588.0                                                                            |
| 18.0                                                                             | 609.0                                                                            |
| 20.0                                                                             | 615.0                                                                            |

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

47

48

49

50

51

52

53

54

55

Listing F.18: Neutron\_ICRP74-1996\_H\_textrmpslab1060circPhi\_dedf.txt

| c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,60^{\circ})/Phi$, from Table A.42:   | c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,60^{\circ})/Phi$, from Table A.42:   |
|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor                                     | c c Energy Fluence-to-dose Conversion Factor                                     |
| [MeV]                                                                            | [pSv$\cdot$cm$^{2}$]                                                             |
| de:n                                                                             | df:n                                                                             |
| log                                                                              | log                                                                              |
| 1.0e-9                                                                           | 2.61                                                                             |
| 1.0e-8                                                                           | 3.37                                                                             |
| 2.53e-8                                                                          | 4.04                                                                             |
| 1.0e-7                                                                           | 4.7                                                                              |
| 2.0e-7                                                                           | 5.21                                                                             |
| 5.0e-7                                                                           | 5.65                                                                             |
| 1.0e-6                                                                           | 5.82                                                                             |
| 2.0e-6                                                                           | 5.85                                                                             |
| 5.0e-6                                                                           | 5.71                                                                             |
| 1.0e-5                                                                           | 5.47                                                                             |
| 2.0e-5                                                                           | 5.14                                                                             |
| 5.0e-5                                                                           | 4.57                                                                             |
| 1.0e-4                                                                           | 4.1                                                                              |
| 2.0e-4                                                                           | 3.91                                                                             |
| 5.0e-4                                                                           | 3.58                                                                             |
| 1.0e-3                                                                           | 3.46                                                                             |
| 2.0e-3                                                                           | 3.46                                                                             |
| 5.0e-3                                                                           | 3.59                                                                             |
| 0.01                                                                             | 4.32                                                                             |
| 0.02                                                                             | 6.64                                                                             |
| 0.03                                                                             | 9.81                                                                             |
| 0.05                                                                             | 16.7                                                                             |
| 0.07                                                                             | 27.3                                                                             |
| 0.1                                                                              | 44.6                                                                             |
| 0.15                                                                             | 73.3                                                                             |
| 0.2                                                                              | 100.0                                                                            |
| 0.3                                                                              | 149.0                                                                            |
| 0.5                                                                              | 226.0                                                                            |
| 0.7                                                                              | 279.0                                                                            |
| 0.9                                                                              | 317.0                                                                            |
| 1.0                                                                              | 332.0                                                                            |
| 1.2                                                                              | 355.0                                                                            |
| 2.0 3.0                                                                          | 402.0                                                                            |
|                                                                                  | 412.0                                                                            |
| 4.0                                                                              | 409.0                                                                            |
| 5.0                                                                              | 409.0                                                                            |
| 6.0                                                                              | 414.0                                                                            |
| 7.0                                                                              | 425.0                                                                            |
| 8.0 9.0                                                                          | 440.0 458.0                                                                      |
| 10.0                                                                             |                                                                                  |
|                                                                                  | 480.0                                                                            |
| 12.0                                                                             | 523.0                                                                            |
| 14.0                                                                             | 562.0                                                                            |
| 15.0                                                                             | 579.0                                                                            |
| 16.0 18.0                                                                        | 593.0 615.0                                                                      |
| 20.0                                                                             | 619.0                                                                            |

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

47

48

49

50

51

52

53

54

55

Listing F.19: Neutron\_ICRP74-1996\_H\_textrmpslab1075circPhi\_dedf.txt

| c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,75^{\circ})/Phi$, from Table A.42:   | c c ICRP/74-1996, $H _ {\textrm{p,slab}}(10,75^{\circ})/Phi$, from Table A.42:   |
|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor                                     | c c Energy Fluence-to-dose Conversion Factor                                     |
| [MeV]                                                                            | [pSv$\cdot$cm$^{2}$]                                                             |
| de:n                                                                             | df:n                                                                             |
| log                                                                              | log                                                                              |
| 1.0e-9                                                                           | 1.13                                                                             |
| 1.0e-8                                                                           | 1.5                                                                              |
| 2.53e-8                                                                          | 1.73                                                                             |
| 1.0e-7                                                                           | 1.94                                                                             |
| 2.0e-7                                                                           | 2.12                                                                             |
| 5.0e-7                                                                           | 2.31                                                                             |
| 1.0e-6                                                                           | 2.4                                                                              |
| 2.0e-6                                                                           | 2.46                                                                             |
| 5.0e-6                                                                           | 2.48                                                                             |
| 1.0e-5                                                                           | 2.44                                                                             |
| 2.0e-5                                                                           | 2.35                                                                             |
| 5.0e-5                                                                           | 2.16                                                                             |
| 1.0e-4                                                                           | 1.99                                                                             |
| 2.0e-4                                                                           | 1.83                                                                             |
| 5.0e-4                                                                           | 1.68                                                                             |
| 1.0e-3                                                                           | 1.66                                                                             |
| 2.0e-3                                                                           | 1.67                                                                             |
| 5.0e-3                                                                           | 1.69                                                                             |
| 0.01                                                                             | 1.77                                                                             |
| 0.02                                                                             | 2.11                                                                             |
| 0.03                                                                             | 2.85                                                                             |
| 0.05                                                                             | 4.78                                                                             |
| 0.07                                                                             | 8.1                                                                              |
| 0.1                                                                              | 13.7                                                                             |
| 0.15                                                                             | 24.2                                                                             |
| 0.2                                                                              | 35.5                                                                             |
| 0.3                                                                              | 58.5                                                                             |
| 0.5                                                                              | 102.0                                                                            |
| 0.7                                                                              | 139.0                                                                            |
| 0.9                                                                              | 171.0                                                                            |
| 1.0                                                                              | 180.0                                                                            |
| 1.2                                                                              | 210.0                                                                            |
| 2.0                                                                              | 274.0                                                                            |
| 3.0                                                                              | 306.0                                                                            |
| 4.0                                                                              | 320.0                                                                            |
| 5.0                                                                              | 331.0                                                                            |
| 6.0                                                                              | 345.0                                                                            |
| 7.0                                                                              | 361.0                                                                            |
| 8.0                                                                              | 379.0                                                                            |
| 9.0                                                                              | 399.0                                                                            |
| 10.0                                                                             | 421.0                                                                            |
| 12.0                                                                             | 464.0                                                                            |
| 14.0                                                                             | 503.0                                                                            |
| 15.0                                                                             | 520.0                                                                            |
| 16.0 18.0                                                                        | 535.0 561.0                                                                      |
| 20.0                                                                             | 570.0                                                                            |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.20: Neutron\_ICRP116-2010\_Anterior-Posterior\_AP\_dedf.txt

| c c ICRP/116-2010, Anterior-Posterior (AP), from Table A.5:   | c c ICRP/116-2010, Anterior-Posterior (AP), from Table A.5:   |
|---------------------------------------------------------------|---------------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor                  | c c Energy Fluence-to-dose Conversion Factor                  |
| [MeV]                                                         | [pSv$\cdot$cm$^{2}$]                                          |
| de:n                                                          | df:n                                                          |
| log                                                           | log                                                           |
| 1.0e-9                                                        | 3.09                                                          |
| 1.0e-8                                                        | 3.55                                                          |
| 2.5e-8                                                        | 4.0                                                           |
| 1.0e-7                                                        | 5.2                                                           |
| 2.0e-7                                                        | 5.87                                                          |
| 5.0e-7                                                        | 6.59                                                          |
| 1.0e-6                                                        | 7.03                                                          |
| 2.0e-6                                                        | 7.39                                                          |
| 5.0e-6                                                        | 7.71                                                          |
| 1.0e-5                                                        | 7.82                                                          |
| 2.0e-5                                                        | 7.84                                                          |
| 5.0e-5                                                        | 7.82                                                          |
| 1.0e-4                                                        | 7.79                                                          |
| 2.0e-4                                                        | 7.73                                                          |
| 5.0e-4                                                        | 7.54                                                          |
| 1.0e-3                                                        |                                                               |
|                                                               | 7.54                                                          |
| 5.0e-3                                                        | 7.97                                                          |
| 0.01                                                          | 9.11                                                          |
| 0.02                                                          | 12.2                                                          |
| 0.03                                                          | 15.7 23.0                                                     |
| 0.05                                                          |                                                               |
| 0.07                                                          | 30.6                                                          |
| 0.1                                                           | 41.9                                                          |
| 0.15                                                          | 60.6 78.8                                                     |
| 0.2                                                           |                                                               |
| 0.3                                                           | 114.0                                                         |
| 0.5                                                           | 177.0                                                         |
| 0.7                                                           | 232.0                                                         |
| 0.9                                                           | 279.0                                                         |
| 1.0                                                           | 301.0                                                         |
| 1.2                                                           | 330.0                                                         |
| 1.5                                                           | 365.0                                                         |
| 2.0                                                           | 407.0                                                         |
| 3.0                                                           | 458.0                                                         |
| 4.0                                                           | 483.0                                                         |
| 5.0                                                           | 494.0                                                         |
| 6.0                                                           | 498.0                                                         |
| 7.0                                                           | 499.0                                                         |
| 8.0                                                           | 499.0                                                         |
| 9.0                                                           | 500.0                                                         |
| 10.0                                                          | 500.0                                                         |
| 12.0                                                          | 499.0                                                         |
| 14.0                                                          | 495.0                                                         |
| 15.0                                                          | 493.0                                                         |
| 16.0                                                          | 490.0                                                         |
| 18.0                                                          | 484.0                                                         |
| 20.0 21.0                                                     | 477.0 474.0                                                   |
| 30.0                                                          | 453.0                                                         |

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

| 50.0   | 433.0   |
|--------|---------|
| 75.0   | 420.0   |
| 100.0  | 402.0   |
| 130.0  | 382.0   |
| 150.0  | 373.0   |
| 180.0  | 363.0   |
| 200.0  | 359.0   |
| 300.0  | 363.0   |
| 400.0  | 389.0   |
| 500.0  | 422.0   |
| 600.0  | 457.0   |
| 700.0  | 486.0   |
| 800.0  | 508.0   |
| 900.0  | 524.0   |
| 1.0e3  | 537.0   |
| 2.0e3  | 612.0   |
| 5.0e3  | 716.0   |
| 1.0e4  | 933.0   |
| c      | c       |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.21: Neutron\_ICRP116-2010\_Posterior-Anterior\_PA\_dedf.txt

| c c ICRP/116-2010, Posterior-Anterior (PA), from Table A.5:   | c c ICRP/116-2010, Posterior-Anterior (PA), from Table A.5:   |
|---------------------------------------------------------------|---------------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor                  | c c Energy Fluence-to-dose Conversion Factor                  |
| [MeV] de:n                                                    | [pSv$\cdot$cm$^{2}$] df:n                                     |
| log                                                           | log                                                           |
| 1.0e-9                                                        | 1.85                                                          |
| 1.0e-8                                                        | 2.11                                                          |
| 2.5e-8                                                        | 2.44                                                          |
| 1.0e-7                                                        | 3.25                                                          |
| 2.0e-7                                                        | 3.72                                                          |
| 5.0e-7                                                        | 4.33                                                          |
| 1.0e-6                                                        | 4.73                                                          |
| 2.0e-6                                                        | 5.02                                                          |
| 5.0e-6                                                        | 5.3                                                           |
| 1.0e-5                                                        | 5.44                                                          |
| 2.0e-5                                                        | 5.51                                                          |
| 5.0e-5 1.0e-4                                                 | 5.55                                                          |
|                                                               | 5.57                                                          |
| 2.0e-4                                                        | 5.59                                                          |
| 5.0e-4                                                        | 5.6                                                           |
| 1.0e-3                                                        | 5.6                                                           |
| 5.0e-3 0.01                                                   | 5.95 6.81                                                     |
| 0.02                                                          | 8.93                                                          |
| 0.03                                                          | 11.2                                                          |
| 0.05                                                          | 15.7                                                          |
| 0.07                                                          | 20.0                                                          |
| 0.1                                                           | 25.9                                                          |
| 0.15                                                          | 34.9                                                          |
| 0.2                                                           | 43.1                                                          |
| 0.3                                                           | 58.1                                                          |
| 0.5                                                           | 85.9                                                          |
| 0.7                                                           | 112.0                                                         |
| 0.9                                                           | 136.0                                                         |
| 1.0                                                           | 148.0                                                         |
| 1.2                                                           | 167.0                                                         |
| 1.5                                                           | 195.0                                                         |
| 2.0                                                           | 235.0                                                         |
| 3.0                                                           | 292.0                                                         |
| 5.0                                                           |                                                               |
| 4.0                                                           | 330.0                                                         |
|                                                               | 354.0                                                         |
| 6.0 7.0                                                       | 371.0 383.0                                                   |
|                                                               | 392.0                                                         |
| 8.0                                                           |                                                               |
| 9.0                                                           | 398.0                                                         |
| 10.0 12.0                                                     | 404.0 412.0                                                   |
|                                                               | 417.0                                                         |
| 14.0                                                          |                                                               |
| 15.0 16.0                                                     | 419.0 420.0                                                   |
| 18.0                                                          | 422.0                                                         |
| 20.0                                                          | 423.0                                                         |
| 21.0                                                          | 423.0                                                         |
| 30.0                                                          | 422.0                                                         |

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

| 50.0   | 428.0   |
|--------|---------|
| 75.0   | 439.0   |
| 100.0  | 444.0   |
| 130.0  | 446.0   |
| 150.0  | 446.0   |
| 180.0  | 447.0   |
| 200.0  | 448.0   |
| 300.0  | 464.0   |
| 400.0  | 496.0   |
| 500.0  | 533.0   |
| 600.0  | 569.0   |
| 700.0  | 599.0   |
| 800.0  | 623.0   |
| 900.0  | 640.0   |
| 1.0e3  | 654.0   |
| 2.0e3  | 740.0   |
| 5.0e3  | 924.0   |
| 1.0e4  | 1.17e3  |
| c      |         |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.22: Neutron\_ICRP116-2010\_Left\_Lateral\_LLAT\_dedf.txt

| c c ICRP/116-2010, Left Lateral (LLAT), from Table A.5:   | c c ICRP/116-2010, Left Lateral (LLAT), from Table A.5:   |
|-----------------------------------------------------------|-----------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor              | c c Energy Fluence-to-dose Conversion Factor              |
| [MeV]                                                     | [pSv$\cdot$cm$^{2}$]                                      |
| de:n                                                      | df:n                                                      |
| log                                                       | log                                                       |
| 1.0e-9                                                    | 1.04                                                      |
| 1.0e-8                                                    | 1.15                                                      |
| 2.5e-8                                                    | 1.32                                                      |
| 1.0e-7                                                    | 1.7                                                       |
| 2.0e-7                                                    | 1.94                                                      |
| 5.0e-7                                                    | 2.21                                                      |
| 1.0e-6                                                    | 2.4                                                       |
| 2.0e-6                                                    | 2.52                                                      |
| 5.0e-6                                                    | 2.64                                                      |
| 1.0e-5                                                    | 2.65                                                      |
| 2.0e-5                                                    | 2.68                                                      |
| 5.0e-5                                                    | 2.66                                                      |
| 1.0e-4                                                    | 2.65                                                      |
| 2.0e-4                                                    | 2.66                                                      |
| 5.0e-4                                                    | 2.62                                                      |
| 1.0e-3                                                    | 2.61                                                      |
| 2.0e-3                                                    | 2.6                                                       |
| 5.0e-3                                                    | 2.74                                                      |
| 0.01                                                      | 3.13                                                      |
| 0.02                                                      | 4.21                                                      |
| 0.03                                                      | 5.4                                                       |
| 0.05                                                      | 7.91                                                      |
| 0.07                                                      | 10.5                                                      |
| 0.1                                                       | 14.4                                                      |
| 0.15                                                      | 20.8                                                      |
| 0.2                                                       | 27.2                                                      |
| 0.3                                                       | 39.7                                                      |
| 0.5                                                       | 63.7                                                      |
| 0.7                                                       | 85.5                                                      |
| 0.9                                                       | 105.0                                                     |
| 1.0                                                       | 115.0                                                     |
| 1.2                                                       | 130.0                                                     |
| 1.5                                                       | 150.0                                                     |
| 2.0                                                       | 179.0                                                     |
| 3.0                                                       | 221.0                                                     |
| 4.0                                                       | 249.0                                                     |
| 5.0                                                       | 269.0                                                     |
| 6.0                                                       | 284.0                                                     |
| 7.0                                                       | 295.0                                                     |
| 8.0                                                       | 303.0                                                     |
| 9.0                                                       | 310.0                                                     |
| 10.0                                                      | 316.0                                                     |
| 12.0                                                      | 325.0                                                     |
| 14.0                                                      | 333.0                                                     |
| 15.0                                                      | 336.0                                                     |
| 16.0                                                      | 338.0                                                     |
| 18.0 20.0                                                 | 343.0                                                     |
| 21.0                                                      | 347.0 348.0                                               |
| 30.0                                                      | 360.0                                                     |

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

| 50.0   | 380.0   |
|--------|---------|
| 75.0   | 399.0   |
| 100.0  | 409.0   |
| 130.0  | 416.0   |
| 150.0  | 420.0   |
| 180.0  | 425.0   |
| 200.0  | 427.0   |
| 300.0  | 441.0   |
| 400.0  | 472.0   |
| 500.0  | 510.0   |
| 600.0  | 547.0   |
| 700.0  | 579.0   |
| 800.0  | 603.0   |
| 900.0  | 621.0   |
| 1.0e3  | 635.0   |
| 2.0e3  | 730.0   |
| 5.0e3  | 963.0   |
| 1.0e4  | 1.23e3  |
| c      |         |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.23: Neutron\_ICRP116-2010\_Right\_Lateral\_RLAT\_dedf.txt

| c c ICRP/116-2010, Right Lateral (RLAT), from Table A.5:   | c c ICRP/116-2010, Right Lateral (RLAT), from Table A.5:   |
|------------------------------------------------------------|------------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor               | c c Energy Fluence-to-dose Conversion Factor               |
| [MeV] de:n                                                 | [pSv$\cdot$cm$^{2}$] df:n                                  |
| log                                                        | log                                                        |
| 1.0e-9                                                     | 0.893                                                      |
| 1.0e-8                                                     | 0.978                                                      |
| 2.5e-8                                                     | 1.12                                                       |
| 1.0e-7                                                     | 1.42                                                       |
| 2.0e-7                                                     | 1.63                                                       |
| 5.0e-7                                                     | 1.86                                                       |
| 1.0e-6                                                     | 2.02                                                       |
| 2.0e-6                                                     | 2.11                                                       |
| 5.0e-6                                                     | 2.21                                                       |
| 1.0e-5                                                     | 2.24                                                       |
| 2.0e-5                                                     | 2.26                                                       |
| 5.0e-5                                                     | 2.24                                                       |
| 1.0e-4                                                     | 2.23                                                       |
| 2.0e-4                                                     | 2.24                                                       |
| 5.0e-4                                                     | 2.21                                                       |
| 1.0e-3                                                     | 2.21                                                       |
| 2.0e-3                                                     | 2.2                                                        |
| 5.0e-3                                                     | 2.33                                                       |
| 0.01                                                       | 2.67                                                       |
| 0.02                                                       | 3.6                                                        |
| 0.03 0.05                                                  | 4.62                                                       |
|                                                            | 6.78                                                       |
| 0.07                                                       | 8.95                                                       |
| 0.1 0.15                                                   | 12.3                                                       |
| 0.2                                                        | 17.9                                                       |
|                                                            | 23.4                                                       |
| 0.3                                                        | 34.2                                                       |
| 0.5                                                        | 54.4                                                       |
| 0.7 0.9                                                    | 72.6 89.3                                                  |
| 1.0                                                        | 97.4                                                       |
|                                                            | 110.0                                                      |
| 1.2                                                        |                                                            |
| 1.5                                                        | 128.0                                                      |
| 3.0                                                        | 192.0                                                      |
| 4.0                                                        | 220.0                                                      |
| 5.0                                                        | 240.0                                                      |
| 6.0 7.0                                                    | 255.0 267.0                                                |
| 8.0                                                        | 276.0                                                      |
| 9.0                                                        | 284.0                                                      |
| 10.0 12.0                                                  | 290.0 301.0                                                |
| 14.0                                                       | 310.0                                                      |
| 15.0                                                       | 313.0                                                      |
| 16.0 18.0                                                  | 317.0 323.0                                                |
| 20.0                                                       | 328.0                                                      |
| 21.0                                                       | 330.0                                                      |
| 30.0                                                       | 345.0                                                      |

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

| 50.0   | 370.0   |
|--------|---------|
| 75.0   | 392.0   |
| 100.0  | 404.0   |
| 130.0  | 413.0   |
| 150.0  | 418.0   |
| 180.0  | 425.0   |
| 200.0  | 429.0   |
| 300.0  | 451.0   |
| 400.0  | 483.0   |
| 500.0  | 523.0   |
| 600.0  | 563.0   |
| 700.0  | 597.0   |
| 800.0  | 620.0   |
| 900.0  | 638.0   |
| 1.0e3  | 651.0   |
| 2.0e3  | 747.0   |
| 5.0e3  | 979.0   |
| 1.0e4  | 1.26e3  |
| c      |         |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.24: Neutron\_ICRP116-2010\_Rotational\_ROT\_dedf.txt

| c c ICRP/116-2010, Rotational (ROT), from Table A.5:   | c c ICRP/116-2010, Rotational (ROT), from Table A.5:   |
|--------------------------------------------------------|--------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor           | c c Energy Fluence-to-dose Conversion Factor           |
| [MeV] de:n                                             | [pSv$\cdot$cm$^{2}$] df:n                              |
| log                                                    | log                                                    |
| 1.0e-9                                                 | 1.7                                                    |
| 1.0e-8                                                 | 2.03                                                   |
| 2.5e-8                                                 | 2.31                                                   |
| 1.0e-7                                                 | 2.98                                                   |
| 2.0e-7                                                 | 3.36                                                   |
| 5.0e-7                                                 | 3.86                                                   |
| 1.0e-6                                                 | 4.17                                                   |
| 2.0e-6                                                 | 4.4                                                    |
| 5.0e-6                                                 | 4.59                                                   |
| 1.0e-5                                                 | 4.68                                                   |
| 2.0e-5                                                 | 4.72                                                   |
| 5.0e-5                                                 | 4.73                                                   |
| 1.0e-4                                                 | 4.72                                                   |
| 2.0e-4                                                 | 4.67                                                   |
| 5.0e-4                                                 | 4.6                                                    |
| 1.0e-3                                                 | 4.58                                                   |
| 2.0e-3                                                 | 4.61                                                   |
| 5.0e-3                                                 | 4.86                                                   |
| 0.01 0.02                                              | 5.57 7.41                                              |
| 0.03                                                   | 9.46                                                   |
| 0.05                                                   | 13.7                                                   |
| 0.07                                                   | 18.0                                                   |
|                                                        | 24.3                                                   |
| 0.1 0.15                                               | 34.7                                                   |
| 0.2                                                    | 44.7                                                   |
| 0.3                                                    | 63.8                                                   |
| 0.5                                                    | 99.1                                                   |
| 0.7                                                    | 131.0                                                  |
| 0.9                                                    | 160.0                                                  |
| 1.0                                                    | 174.0                                                  |
| 1.2                                                    | 193.0                                                  |
| 1.5                                                    | 219.0                                                  |
| 2.0                                                    | 254.0                                                  |
| 3.0                                                    | 301.0                                                  |
| 4.0                                                    | 331.0                                                  |
| 5.0                                                    | 351.0                                                  |
| 6.0                                                    | 365.0                                                  |
| 7.0                                                    | 374.0                                                  |
| 8.0                                                    | 381.0                                                  |
| 9.0                                                    | 386.0                                                  |
| 10.0                                                   | 390.0                                                  |
| 12.0                                                   | 395.0                                                  |
| 14.0                                                   | 398.0                                                  |
| 15.0                                                   | 398.0                                                  |
| 16.0                                                   | 399.0                                                  |
| 18.0                                                   | 399.0                                                  |
| 20.0                                                   | 398.0                                                  |
| 21.0                                                   | 398.0                                                  |
| 30.0                                                   | 395.0                                                  |

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

| 50.0   | 395.0   |
|--------|---------|
| 75.0   | 402.0   |
| 100.0  | 406.0   |
| 130.0  | 411.0   |
| 150.0  | 414.0   |
| 180.0  | 418.0   |
| 200.0  | 422.0   |
| 300.0  | 443.0   |
| 400.0  | 472.0   |
| 500.0  | 503.0   |
| 600.0  | 532.0   |
| 700.0  | 558.0   |
| 800.0  | 580.0   |
| 900.0  | 598.0   |
| 1.0e3  | 614.0   |
| 2.0e3  | 718.0   |
| 5.0e3  | 906.0   |
| 1.0e4  | 1.14e3  |
| c      |         |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.25: Neutron\_ICRP116-2010\_Isotropic\_ISO\_dedf.txt

| c c ICRP/116-2010, Isotropic (ISO), from Table A.5:   | c c ICRP/116-2010, Isotropic (ISO), from Table A.5:   |
|-------------------------------------------------------|-------------------------------------------------------|
| c c Energy Fluence-to-dose Conversion Factor          | c c Energy Fluence-to-dose Conversion Factor          |
| [MeV] de:n                                            | [pSv$\cdot$cm$^{2}$] df:n                             |
| log                                                   | log                                                   |
| 1.0e-9                                                | 1.29                                                  |
| 1.0e-8                                                | 1.56                                                  |
| 2.5e-8                                                | 1.76                                                  |
| 1.0e-7                                                | 2.26                                                  |
| 2.0e-7                                                | 2.54                                                  |
| 5.0e-7                                                | 2.92                                                  |
| 1.0e-6                                                | 3.15                                                  |
| 2.0e-6                                                | 3.32                                                  |
| 5.0e-6                                                | 3.47                                                  |
| 1.0e-5                                                | 3.52                                                  |
| 2.0e-5                                                | 3.54                                                  |
| 5.0e-5                                                | 3.55                                                  |
| 1.0e-4                                                | 3.54                                                  |
| 2.0e-4                                                | 3.52                                                  |
| 5.0e-4                                                | 3.47                                                  |
| 1.0e-3                                                | 3.46                                                  |
| 2.0e-3                                                | 3.48                                                  |
| 5.0e-3                                                | 3.66                                                  |
| 0.01                                                  | 4.19                                                  |
| 0.02 0.03                                             | 5.61                                                  |
| 0.05                                                  | 7.18 10.4                                             |
| 0.07                                                  | 13.7                                                  |
| 0.1                                                   | 18.6                                                  |
| 0.15                                                  |                                                       |
| 0.2                                                   | 26.6 34.4                                             |
| 0.3                                                   | 49.4                                                  |
|                                                       | 77.1                                                  |
| 0.5 0.7                                               | 102.0                                                 |
| 0.9                                                   | 126.0                                                 |
| 1.0                                                   | 137.0                                                 |
| 1.2                                                   | 153.0                                                 |
| 1.5                                                   | 174.0                                                 |
| 2.0                                                   | 203.0                                                 |
| 3.0                                                   | 244.0                                                 |
| 4.0                                                   | 271.0                                                 |
| 5.0                                                   | 290.0                                                 |
| 6.0                                                   | 303.0                                                 |
| 7.0                                                   | 313.0                                                 |
| 8.0                                                   | 321.0                                                 |
| 9.0                                                   | 327.0                                                 |
| 10.0                                                  | 332.0                                                 |
| 12.0                                                  | 339.0                                                 |
| 14.0                                                  | 344.0                                                 |
| 15.0                                                  | 346.0                                                 |
| 16.0                                                  | 347.0                                                 |
| 18.0                                                  | 350.0                                                 |
| 20.0                                                  | 352.0                                                 |
| 21.0                                                  | 353.0                                                 |
| 30.0                                                  | 358.0                                                 |

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

| 50.0   | 371.0   |
|--------|---------|
| 75.0   | 387.0   |
| 100.0  | 397.0   |
| 130.0  | 407.0   |
| 150.0  | 412.0   |
| 180.0  | 421.0   |
| 200.0  | 426.0   |
| 300.0  | 455.0   |
| 400.0  | 488.0   |
| 500.0  | 521.0   |
| 600.0  | 553.0   |
| 700.0  | 580.0   |
| 800.0  | 604.0   |
| 900.0  | 624.0   |
| 1.0e3  | 642.0   |
| 2.0e3  | 767.0   |
| 5.0e3  | 1.01e3  |
| 1.0e4  | 1.32e3  |
| c      | c       |

Figure F.1: ANSI/ANS-6.1.1-1977 Neutron Flux-to-dose Conversion Factors

<!-- image -->

Figure F.2: ANSI/ANS-6.1.1-1991 Anterior-Posterior (AP) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.3: ANSI/ANS-6.1.1-1991 Posterior-Anterior (PA) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.4: ANSI/ANS-6.1.1-1991 Lateral (LAT) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.5: ANSI/ANS-6.1.1-1991 Rotational (ROT) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.6: ICRP/21-1973 Neutron Flux-to-dose Conversion Factors.

<!-- image -->

Figure F.7: ICRP/74-1996 Anterior-Posterior (AP) Neutron Fluence-to-dose Conversion Factors.

<!-- image -->

Figure F.8: ICRP/74-1996 Posterior-Anterior (PA) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.9: ICRP/74-1996 Left Lateral (LLAT) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.10: ICRP/74-1996 Right Lateral (RLAT) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.11: ICRP/74-1996 Rotational (ROT) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.12: ICRP/74-1996 Isotropic (ISO) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

<!-- image -->

Figure F.13: ICRP/74-1996 Ambient Dose Equivalent ( H ∗ (10) /φ )
Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.14: ICRP/74-1996 Personal Dose Equivalent ( H p,slab (10 , 0 ◦
) /φ ) Neutron Fluenceto-dose Conversion Factors

Figure F.15: ICRP/74-1996 Personal Dose Equivalent ( H p,slab (10 , 15 ◦ ) /φ ) Neutron Fluenceto-dose Conversion Factors

<!-- image -->

Figure F.16: ICRP/74-1996 Personal Dose Equivalent ( H p,slab (10 , 30 ◦ ) /φ ) Neutron Fluenceto-dose Conversion Factors

<!-- image -->

<!-- image -->

Figure F.17: ICRP/74-1996 Personal Dose Equivalent ( H p,slab (10 , 45 ◦
) /φ ) Neutron Fluenceto-dose Conversion Factors

<!-- image -->

Figure F.18: ICRP/74-1996 Personal Dose Equivalent ( H p,slab (10 , 60 ◦
) /φ ) Neutron Fluenceto-dose Conversion Factors

Figure F.19: ICRP/74-1996 Personal Dose Equivalent ( H p,slab (10 , 75 ◦ ) /φ ) Neutron Fluenceto-dose Conversion Factors

<!-- image -->

Figure F.20: ICRP/116-2010 Anterior-Posterior (AP) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.21: ICRP/116-2010 Posterior-Anterior (PA) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.22: ICRP/116-2010 Left Lateral (LLAT) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.23: ICRP/116-2010 Right Lateral (RLAT) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.24: ICRP/116-2010 Rotational (ROT) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.25: ICRP/116-2010 Isotropic (ISO) Neutron Fluence-to-dose Conversion Factors

<!-- image -->

## F.1.2 Incident Photon

The ANSI/ANS-6.1.1-1977 photon flux-to-dose conversion factors are given
in Listing F.26 which can be directly used as MCNP input for DE / DF
cards. The flux-to-dose conversion factors are also plotted in Figure
F.26 showing both linear and logarithmic interpolation. These values are
extracted from [360] with permission of the publisher, the American
Nuclear Society.

The ANSI/ANS-6.1.1-1991 standard provides a variety of photon fluence-
to-dose conversion factors assuming five irradiation-phantom
orientations: anterior-posterior (AP), posterior-anterior (PA), lateral
(LAT), rotational (ROT), and isotropic (ISO). More details on these
factors, and how to use them, are available in [361]. The AP, PA, LAT,
ROT, and ISO responses are given in Listings F.27, F.28, F.29, F.30, and
F.31, respectively, which can be directly used as MCNP input for DE / DF
cards. In addition, the conversion factors are plotted in Figures F.27,
F.28, F.29, and F.30.

The ICRP/21-1973 photon fluence-to-dose conversion factors are given in
Listing F.32, which can be directly used as MCNP input for DE / DF
cards. These values are modified from the original values in [362]. The
values in Listing F.32 are the inverse of the original values. In
addition, Listing F.32 includes extra significant figures in order to
reconstruct the original values in [362]. In addition, a duplicate entry
for 10 MeV in [362] has been removed to provide a monotonic progression
in energy, which is required by the DE card.

The fluence-to-dose conversion factors are also plotted in Figure F.32
showing both linear and logarithmic interpolation.

The ICRP/116-2010 standard provides a variety of photon fluence-to-dose
conversion factors assuming six irradiation-phantom orientations:
anterior-posterior (AP), posterior-anterior (PA), left lateral (LLAT),
right lateral (RLAT), rotational (ROT), and isotropic (ISO). More
details on these factors, and how to use them, are available in [364].
The AP, PA, LLAT, RLAT, ROT, and ISO responses are given in Listings
F.33, F.34, F.35, F.36, F.37, and F.38, respectively, which can be
directly used as MCNP input for DE / DF cards. In addition, the
conversion factors are plotted in Figures F.33, F.34, F.35, F.36, F.37,
and F.38.

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

Listing F.26: Photon\_ANSIANS-611-1977\_dedf.txt

| c c ANSI/ANS-6.1.1-1977, from Table 3:   | c c ANSI/ANS-6.1.1-1977, from Table 3:                             |
|------------------------------------------|--------------------------------------------------------------------|
| c c Energy c [MeV]                       | Flux-to-dose Conversion Factor [(rem/hr)/(cm$^{-2}\cdot$s$^{-1}$)] |
| # de:p                                   | df:p                                                               |
| log                                      | log                                                                |
| 0.01                                     | 3.96e-6                                                            |
| 0.03                                     | 5.82e-7                                                            |
| 0.05                                     | 2.9e-7                                                             |
| 0.07                                     | 2.58e-7                                                            |
| 0.1                                      | 2.83e-7                                                            |
| 0.15                                     | 3.79e-7                                                            |
| 0.2                                      | 5.01e-7                                                            |
| 0.25                                     | 6.31e-7                                                            |
| 0.3                                      | 7.59e-7                                                            |
| 0.35                                     | 8.78e-7                                                            |
| 0.4                                      | 9.85e-7                                                            |
| 0.45                                     | 1.08e-6                                                            |
| 0.5                                      | 1.17e-6                                                            |
| 0.55                                     | 1.27e-6                                                            |
| 0.6                                      | 1.36e-6                                                            |
| 0.65                                     | 1.44e-6                                                            |
| 0.7                                      | 1.52e-6                                                            |
| 0.8                                      | 1.68e-6                                                            |
| 1.0                                      | 1.98e-6                                                            |
| 1.4                                      | 2.51e-6                                                            |
| 1.8                                      | 2.99e-6                                                            |
| 2.2                                      | 3.42e-6                                                            |
| 2.6                                      | 3.82e-6                                                            |
| 2.8                                      | 4.01e-6                                                            |
| 3.25                                     | 4.41e-6                                                            |
| 3.75                                     | 4.83e-6                                                            |
| 4.25                                     | 5.23e-6                                                            |
| 4.75                                     | 5.6e-6                                                             |
| 5.0                                      | 5.8e-6                                                             |
| 5.25                                     | 6.01e-6                                                            |
| 5.75                                     | 6.37e-6                                                            |
| 6.25                                     | 6.74e-6                                                            |
| 6.75                                     | 7.11e-6                                                            |
| 7.5                                      | 7.66e-6                                                            |
| 9.0                                      | 8.77e-6                                                            |
| 11.0                                     | 1.03e-5                                                            |
| 13.0                                     | 1.18e-5                                                            |

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

28

29

30

31

32

33

34

Listing F.27: Photon\_ANSIANS-611-1991\_Anterior-Posterior\_AP\_dedf.txt

| c c ANSI/ANS-6.1.1-1991, Anterior-Posterior (AP), from Table 3:   | c c ANSI/ANS-6.1.1-1991, Anterior-Posterior (AP), from Table 3:   |
|-------------------------------------------------------------------|-------------------------------------------------------------------|
| c Energy c [MeV]                                                  | Fluence-to-dose Conversion Factor [pSv$\cdot$cm$^{2}$]            |
| # de:p                                                            | df:p                                                              |
| log                                                               | log                                                               |
| 0.01                                                              | 0.062                                                             |
| 0.015                                                             | 0.157                                                             |
| 0.02                                                              | 0.238                                                             |
| 0.03                                                              | 0.329                                                             |
| 0.04                                                              | 0.365                                                             |
| 0.05                                                              | 0.384                                                             |
| 0.06                                                              | 0.4                                                               |
| 0.08                                                              | 0.451                                                             |
| 0.1                                                               | 0.533                                                             |
| 0.15                                                              | 0.777                                                             |
| 0.2                                                               | 1.03                                                              |
| 0.3                                                               | 1.56                                                              |
| 0.4                                                               | 2.06                                                              |
| 0.5                                                               | 2.54                                                              |
| 0.6                                                               | 2.99                                                              |
| 0.8                                                               | 3.83                                                              |
| 1.0                                                               | 4.6                                                               |
| 1.5                                                               | 6.24                                                              |
| 2.0                                                               | 7.66                                                              |
| 3.0                                                               | 10.2                                                              |
| 4.0                                                               | 12.5                                                              |
| 5.0                                                               | 14.7                                                              |
| 6.0                                                               | 16.7                                                              |
| 8.0                                                               | 20.8                                                              |
| 10.0                                                              | 24.7                                                              |
| 12.0                                                              | 28.9                                                              |
| c                                                                 | c                                                                 |

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

28

29

30

31

32

33

34

Listing F.28: Photon\_ANSIANS-611-1991\_Posterior-Anterior\_PA\_dedf.txt

| c c ANSI/ANS-6.1.1-1991, Posterior-Anterior (PA), from Table 3:   | c c ANSI/ANS-6.1.1-1991, Posterior-Anterior (PA), from Table 3:   |
|-------------------------------------------------------------------|-------------------------------------------------------------------|
| c Energy c [MeV]                                                  | Fluence-to-dose Conversion Factor [pSv$\cdot$cm$^{2}$]            |
| # de:p                                                            | df:p                                                              |
| log                                                               | log                                                               |
| 0.01                                                              | 1.0e-4                                                            |
| 0.015                                                             | 0.031                                                             |
| 0.02                                                              | 0.0868                                                            |
| 0.03                                                              | 0.161                                                             |
| 0.04                                                              | 0.222                                                             |
| 0.05                                                              | 0.26                                                              |
| 0.06                                                              | 0.286                                                             |
| 0.08                                                              | 0.344                                                             |
| 0.1                                                               | 0.418                                                             |
| 0.15                                                              | 0.624                                                             |
| 0.2                                                               | 0.844                                                             |
| 0.3                                                               | 1.3                                                               |
| 0.4                                                               | 1.76                                                              |
| 0.5                                                               | 2.2                                                               |
| 0.6                                                               | 2.62                                                              |
| 0.8                                                               | 3.43                                                              |
| 1.0                                                               | 4.18                                                              |
| 1.5                                                               | 5.8                                                               |
| 2.0                                                               | 7.21                                                              |
| 3.0                                                               | 9.71                                                              |
| 4.0                                                               | 12.0                                                              |
| 5.0                                                               | 14.1                                                              |
| 6.0                                                               | 16.2                                                              |
| 8.0                                                               | 20.2                                                              |
| 10.0                                                              | 24.2                                                              |
| 12.0                                                              | 28.8                                                              |
| c                                                                 | c                                                                 |

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

28

29

30

31

32

33

34

Listing F.29: Photon\_ANSIANS-611-1991\_Lateral\_LAT\_dedf.txt

| c c ANSI/ANS-6.1.1-1991, Lateral (LAT), from Table 3: c   | c c ANSI/ANS-6.1.1-1991, Lateral (LAT), from Table 3: c   |
|-----------------------------------------------------------|-----------------------------------------------------------|
| c Energy c [MeV]                                          | Fluence-to-dose Conversion Factor [pSv$\cdot$cm$^{2}$]    |
| # de:p                                                    | df:p                                                      |
| log                                                       | log                                                       |
| 0.01                                                      | 0.02                                                      |
| 0.015                                                     | 0.033                                                     |
| 0.02                                                      | 0.0491                                                    |
| 0.03                                                      | 0.0863                                                    |
| 0.04                                                      | 0.123                                                     |
| 0.05                                                      | 0.152                                                     |
| 0.06                                                      | 0.17                                                      |
| 0.08                                                      | 0.212                                                     |
| 0.1                                                       | 0.258                                                     |
| 0.15                                                      | 0.396                                                     |
| 0.2                                                       | 0.557                                                     |
| 0.3                                                       | 0.891                                                     |
| 0.4                                                       | 1.24                                                      |
| 0.5                                                       | 1.58                                                      |
| 0.6                                                       | 1.92                                                      |
| 0.8                                                       | 2.6                                                       |
| 1.0                                                       | 3.24                                                      |
| 1.5                                                       | 4.7                                                       |
| 2.0                                                       | 6.02                                                      |
| 3.0                                                       | 8.4                                                       |
| 4.0                                                       | 10.6                                                      |
| 5.0                                                       | 12.6                                                      |
| 6.0                                                       | 14.6                                                      |
| 8.0                                                       | 18.5                                                      |
| 10.0                                                      | 22.3                                                      |
| 12.0                                                      | 26.4                                                      |
| c                                                         | c                                                         |

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

28

29

30

31

32

33

34

Listing F.30: Photon\_ANSIANS-611-1991\_Rotational\_ROT\_dedf.txt

| c c ANSI/ANS-6.1.1-1991, Rotational (ROT), from Table 3:   | c c ANSI/ANS-6.1.1-1991, Rotational (ROT), from Table 3:   |
|------------------------------------------------------------|------------------------------------------------------------|
| c Energy c [MeV]                                           | Fluence-to-dose Conversion Factor [pSv$\cdot$cm$^{2}$]     |
| # de:p                                                     | df:p                                                       |
| log                                                        | log                                                        |
| 0.01                                                       | 0.029                                                      |
| 0.015                                                      | 0.071                                                      |
| 0.02                                                       | 0.11                                                       |
| 0.03                                                       | 0.166                                                      |
| 0.04                                                       | 0.199                                                      |
| 0.05                                                       | 0.222                                                      |
| 0.06                                                       | 0.24                                                       |
| 0.08                                                       | 0.293                                                      |
| 0.1                                                        | 0.357                                                      |
| 0.15                                                       | 0.534                                                      |
| 0.2                                                        | 0.731                                                      |
| 0.3                                                        | 1.14                                                       |
| 0.4                                                        | 1.55                                                       |
| 0.5                                                        | 1.96                                                       |
| 0.6                                                        | 2.34                                                       |
| 0.8                                                        | 3.07                                                       |
| 1.0                                                        | 3.75                                                       |
| 1.5                                                        | 5.24                                                       |
| 2.0                                                        | 6.56                                                       |
| 3.0                                                        | 8.9                                                        |
| 4.0                                                        | 11.0                                                       |
| 5.0                                                        | 13.0                                                       |
| 6.0                                                        | 14.9                                                       |
| 8.0                                                        | 18.9                                                       |
| 10.0                                                       | 22.9                                                       |
| 12.0                                                       | 27.6                                                       |
| c                                                          | c                                                          |

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

28

29

30

31

32

33

34

Listing F.31: Photon\_ANSIANS-611-1991\_Isotropic\_ISO\_dedf.txt

| c c ANSI/ANS-6.1.1-1991, Isotropic (ISO), from Table 3:   | c c ANSI/ANS-6.1.1-1991, Isotropic (ISO), from Table 3:   |
|-----------------------------------------------------------|-----------------------------------------------------------|
| c Energy c [MeV]                                          | Fluence-to-dose Conversion Factor [pSv$\cdot$cm$^{2}$]    |
| # de:p                                                    | df:p                                                      |
| log                                                       | log                                                       |
| 0.01                                                      | 0.022                                                     |
| 0.015                                                     | 0.057                                                     |
| 0.02                                                      | 0.0912                                                    |
| 0.03                                                      | 0.138                                                     |
| 0.04                                                      | 0.163                                                     |
| 0.05                                                      | 0.18                                                      |
| 0.06                                                      | 0.196                                                     |
| 0.08                                                      | 0.237                                                     |
| 0.1                                                       | 0.284                                                     |
| 0.15                                                      | 0.436                                                     |
| 0.2                                                       | 0.602                                                     |
| 0.3                                                       | 0.949                                                     |
| 0.4                                                       | 1.3                                                       |
| 0.5                                                       | 1.64                                                      |
| 0.6                                                       | 1.98                                                      |
| 0.8                                                       | 2.64                                                      |
| 1.0                                                       | 3.27                                                      |
| 1.5                                                       | 4.68                                                      |
| 2.0                                                       | 5.93                                                      |
| 3.0                                                       | 8.19                                                      |
| 4.0                                                       | 10.2                                                      |
| 5.0                                                       | 12.1                                                      |
| 6.0                                                       | 14.0                                                      |
| 8.0                                                       | 17.8                                                      |
| 10.0                                                      | 21.6                                                      |
| 12.0                                                      | 25.8                                                      |
| c                                                         | c                                                         |

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

47

Listing F.32: Photon\_ICRP21-1973\_dedf.txt

| c                                                | c                                                                   |
|--------------------------------------------------|---------------------------------------------------------------------|
| c ICRP/21-1973, from Table 6, with Modification: | c ICRP/21-1973, from Table 6, with Modification:                    |
| c Energy c [MeV]                                 | Flux-to-dose Conversion Factor [(mrem/hr)/(cm$^{-2}\cdot$s$^{-1}$)] |
| # de:p                                           | df:p                                                                |
| log                                              | log                                                                 |
| 0.01                                             | 2.778e-3                                                            |
| 0.015                                            | 1.111e-3                                                            |
| 0.02                                             | 5.882e-4                                                            |
| 0.03                                             | 2.564e-4                                                            |
| 0.04                                             | 1.563e-4                                                            |
| 0.05                                             | 1.205e-4                                                            |
| 0.06                                             | 1.111e-4                                                            |
| 0.08                                             | 1.205e-4                                                            |
| 0.1                                              | 1.471e-4                                                            |
| 0.15                                             | 2.381e-4                                                            |
| 0.2                                              | 3.448e-4                                                            |
| 0.3                                              | 5.556e-4                                                            |
| 0.4                                              | 7.692e-4                                                            |
| 0.5                                              | 9.091e-4                                                            |
| 0.6                                              | 1.136e-3                                                            |
| 0.8                                              | 1.47e-3                                                             |
| 1.0                                              | 1.786e-3                                                            |
| 1.5                                              | 2.439e-3                                                            |
| 2.0                                              | 3.03e-3                                                             |
| 3.0                                              | 4.0e-3                                                              |
| 4.0                                              | 4.762e-3                                                            |
| 5.0                                              | 5.556e-3                                                            |
| 6.0                                              | 6.25e-3                                                             |
| 8.0                                              | 7.692e-3                                                            |
| 10.0                                             | 9.091e-3                                                            |
| 20.0                                             | 0.01563                                                             |
| 30.0                                             | 0.02273                                                             |
| 40.0                                             | 0.02941                                                             |
| 50.0                                             | 0.03571                                                             |
| 60.0                                             | 0.04348                                                             |
| 80.0                                             | 0.05882                                                             |
| 100.0                                            | 0.07143                                                             |
| 200.0                                            | 0.1087                                                              |
| 500.0                                            | 0.1724                                                              |
| 1.0e3                                            | 0.2041                                                              |
| 2.0e3                                            | 0.2326                                                              |
| 5.2e3                                            | 0.2703                                                              |
| 1.0e4                                            | 0.2941                                                              |
| 2.0e4                                            | 0.3125                                                              |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.33: Photon\_ICRP116-2010\_Anterior-Posterior\_AP\_dedf.txt

| c c ICRP/116-2010, Anterior-Posterior (AP), from Table A.1:   | c c ICRP/116-2010, Anterior-Posterior (AP), from Table A.1:   |
|---------------------------------------------------------------|---------------------------------------------------------------|
| Energy Fluence-to-dose Conversion Factor                      | Energy Fluence-to-dose Conversion Factor                      |
| [MeV]                                                         | [pSv$\cdot$cm$^{2}$]                                          |
| de:p                                                          | df:p                                                          |
| log                                                           | log                                                           |
| 0.01                                                          | 0.0685                                                        |
| 0.015                                                         | 0.156                                                         |
| 0.02                                                          | 0.225                                                         |
| 0.03                                                          | 0.313                                                         |
| 0.04                                                          | 0.351                                                         |
| 0.05                                                          | 0.37                                                          |
| 0.06                                                          | 0.39                                                          |
| 0.07                                                          | 0.413                                                         |
| 0.08                                                          | 0.444                                                         |
| 0.1                                                           | 0.519                                                         |
| 0.15                                                          | 0.748                                                         |
| 0.2                                                           | 1.0                                                           |
| 0.3                                                           | 1.51                                                          |
| 0.4                                                           | 2.0                                                           |
| 0.5                                                           | 2.47                                                          |
| 0.511                                                         | 2.52                                                          |
| 0.6                                                           | 2.91                                                          |
| 0.662                                                         | 3.17                                                          |
| 0.8                                                           | 3.73                                                          |
| 1.0                                                           | 4.49                                                          |
| 1.117                                                         | 4.9                                                           |
| 1.33                                                          | 5.59                                                          |
| 1.5                                                           | 6.12                                                          |
| 2.0                                                           | 7.48                                                          |
| 3.0                                                           | 9.75                                                          |
| 4.0                                                           | 11.7                                                          |
| 5.0                                                           | 13.4                                                          |
| 6.0                                                           | 15.0                                                          |
| 6.129                                                         | 15.1                                                          |
| 8.0                                                           | 17.8                                                          |
| 10.0                                                          | 20.5                                                          |
| 15.0                                                          | 26.1 30.8                                                     |
| 20.0                                                          |                                                               |
| 30.0                                                          | 37.9                                                          |
| 40.0 50.0                                                     | 43.1                                                          |
| 60.0                                                          | 47.1 50.1                                                     |
| 80.0                                                          | 54.5                                                          |
| 100.0                                                         | 57.8                                                          |
| 150.0                                                         | 63.3                                                          |
| 200.0                                                         | 67.3 72.3                                                     |
| 300.0                                                         |                                                               |
| 400.0                                                         | 75.5                                                          |
| 500.0                                                         | 77.5                                                          |
| 600.0                                                         | 78.9                                                          |
| 800.0                                                         | 80.5                                                          |
| 1.0e3 1.5e3                                                   | 81.7                                                          |
| 2.0e3                                                         | 83.8 85.2                                                     |
| 3.0e3                                                         | 86.9                                                          |

58

59

60

61

62

63

| 4.0e3   | 88.1   |
|---------|--------|
| 5.0e3   | 88.9   |
| 6.0e3   | 89.5   |
| 8.0e3   | 90.2   |
| 1.0e4   | 90.7   |
| c       | c      |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.34: Photon\_ICRP116-2010\_Posterior-Anterior\_PA\_dedf.txt

| c c ICRP/116-2010, Posterior-Anterior (PA), from Table A.1:   | c c ICRP/116-2010, Posterior-Anterior (PA), from Table A.1:   |
|---------------------------------------------------------------|---------------------------------------------------------------|
| Energy Fluence-to-dose Conversion Factor                      | Energy Fluence-to-dose Conversion Factor                      |
| [MeV]                                                         | [pSv$\cdot$cm$^{2}$]                                          |
| de:p                                                          | df:p                                                          |
| log                                                           | log                                                           |
| 0.01                                                          | 0.0184                                                        |
| 0.015                                                         | 0.0155                                                        |
| 0.02                                                          | 0.026                                                         |
| 0.03                                                          | 0.094                                                         |
| 0.04                                                          | 0.161                                                         |
| 0.05                                                          | 0.208                                                         |
| 0.06                                                          | 0.242                                                         |
| 0.07                                                          | 0.271                                                         |
| 0.08                                                          | 0.301                                                         |
| 0.1                                                           | 0.361                                                         |
| 0.15                                                          | 0.541                                                         |
| 0.2                                                           | 0.741                                                         |
| 0.3                                                           | 1.16                                                          |
| 0.4                                                           | 1.57                                                          |
| 0.5                                                           | 1.98                                                          |
| 0.511                                                         | 2.03                                                          |
| 0.6                                                           | 2.38                                                          |
| 0.662                                                         | 2.62                                                          |
| 0.8                                                           | 3.13                                                          |
| 1.0                                                           | 3.83                                                          |
| 1.117                                                         | 4.22                                                          |
| 1.33                                                          | 4.89                                                          |
| 1.5                                                           | 5.39                                                          |
| 2.0                                                           | 6.75                                                          |
| 3.0                                                           | 9.12                                                          |
| 4.0                                                           | 11.2                                                          |
| 5.0                                                           | 13.1                                                          |
| 6.0                                                           | 15.0                                                          |
| 6.129                                                         | 15.2                                                          |
| 8.0 10.0                                                      | 18.6 22.0                                                     |
| 15.0                                                          |                                                               |
| 20.0                                                          | 30.3 38.2                                                     |
| 30.0 40.0                                                     | 51.4                                                          |
| 50.0                                                          | 62.0 70.4                                                     |
| 60.0                                                          | 76.9                                                          |
| 80.0                                                          |                                                               |
|                                                               | 86.6                                                          |
| 100.0                                                         | 93.2                                                          |
| 150.0 200.0                                                   | 104.0                                                         |
|                                                               | 111.0                                                         |
| 300.0                                                         | 119.0                                                         |
| 400.0                                                         | 124.0                                                         |
| 500.0                                                         | 128.0                                                         |
| 600.0                                                         | 131.0                                                         |
| 800.0                                                         | 135.0                                                         |
| 1.0e3 1.5e3                                                   | 138.0 142.0                                                   |
| 2.0e3                                                         | 145.0                                                         |
| 3.0e3                                                         | 148.0                                                         |

58

59

60

61

62

63

| 4.0e3   | 150.0   |
|---------|---------|
| 5.0e3   | 152.0   |
| 6.0e3   | 153.0   |
| 8.0e3   | 155.0   |
| 1.0e4   | 155.0   |
| c       | c       |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.35: Photon\_ICRP116-2010\_Left\_Lateral\_LLAT\_dedf.txt

| c c ICRP/116-2010, Left Lateral (LLAT), from Table A.1:   | c c ICRP/116-2010, Left Lateral (LLAT), from Table A.1:   |
|-----------------------------------------------------------|-----------------------------------------------------------|
| Energy Fluence-to-dose Conversion Factor                  | Energy Fluence-to-dose Conversion Factor                  |
| [MeV]                                                     | [pSv$\cdot$cm$^{2}$]                                      |
| de:p                                                      | df:p                                                      |
| log                                                       | log                                                       |
| 0.01                                                      | 0.0189                                                    |
| 0.015                                                     | 0.0416                                                    |
| 0.02                                                      | 0.0655                                                    |
| 0.03                                                      | 0.11                                                      |
| 0.04                                                      | 0.14                                                      |
| 0.05                                                      | 0.16                                                      |
| 0.06                                                      | 0.177                                                     |
| 0.07                                                      | 0.194                                                     |
| 0.08                                                      | 0.214                                                     |
| 0.1                                                       | 0.259                                                     |
| 0.15                                                      | 0.395                                                     |
| 0.2                                                       | 0.552                                                     |
| 0.3                                                       | 0.888                                                     |
| 0.4                                                       | 1.24                                                      |
| 0.5                                                       | 1.58                                                      |
| 0.511                                                     | 1.62                                                      |
| 0.6                                                       | 1.93                                                      |
| 0.662                                                     | 2.14                                                      |
| 0.8                                                       | 2.59                                                      |
| 1.0                                                       | 3.23                                                      |
| 1.117                                                     | 3.58                                                      |
| 1.33                                                      | 4.2                                                       |
| 1.5                                                       | 4.68                                                      |
| 2.0                                                       | 5.96                                                      |
| 3.0                                                       | 8.21                                                      |
| 4.0                                                       | 10.2                                                      |
| 5.0                                                       | 12.0                                                      |
| 6.0                                                       | 13.7                                                      |
| 6.129                                                     | 13.9                                                      |
| 8.0                                                       | 17.0                                                      |
| 10.0                                                      | 20.1                                                      |
| 15.0                                                      | 27.4                                                      |
| 20.0                                                      | 34.4                                                      |
| 30.0                                                      | 47.4                                                      |
| 40.0                                                      | 59.2                                                      |
| 50.0 60.0                                                 | 69.5                                                      |
|                                                           | 78.3                                                      |
| 80.0                                                      | 92.4                                                      |
| 100.0                                                     | 103.0                                                     |
| 150.0                                                     | 121.0                                                     |
| 200.0                                                     | 133.0                                                     |
| 300.0                                                     | 148.0                                                     |
| 400.0                                                     | 158.0                                                     |
| 500.0                                                     | 165.0                                                     |
| 600.0                                                     | 170.0                                                     |
| 800.0                                                     | 178.0                                                     |
| 1.0e3 1.5e3                                               | 183.0                                                     |
| 2.0e3                                                     | 193.0 198.0                                               |
| 3.0e3                                                     | 206.0                                                     |

58

59

60

61

62

63

| 4.0e3   | 212.0   |
|---------|---------|
| 5.0e3   | 216.0   |
| 6.0e3   | 219.0   |
| 8.0e3   | 224.0   |
| 1.0e4   | 228.0   |
| c       | c       |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.36: Photon\_ICRP116-2010\_Right\_Lateral\_RLAT\_dedf.txt

| c c ICRP/116-2010, Right Lateral (RLAT), from Table A.1:   | c c ICRP/116-2010, Right Lateral (RLAT), from Table A.1:   |
|------------------------------------------------------------|------------------------------------------------------------|
| Energy Fluence-to-dose Conversion Factor                   | Energy Fluence-to-dose Conversion Factor                   |
| [MeV]                                                      | [pSv$\cdot$cm$^{2}$]                                       |
| de:p                                                       | df:p                                                       |
| log                                                        | log                                                        |
| 0.01                                                       | 0.0182                                                     |
| 0.015                                                      | 0.039                                                      |
| 0.02                                                       | 0.0573                                                     |
| 0.03                                                       | 0.0891                                                     |
| 0.04                                                       | 0.114                                                      |
| 0.05                                                       | 0.133                                                      |
| 0.06                                                       | 0.15                                                       |
| 0.07                                                       | 0.167                                                      |
| 0.08                                                       | 0.185                                                      |
| 0.1                                                        | 0.225                                                      |
| 0.15                                                       | 0.348                                                      |
| 0.2                                                        | 0.492                                                      |
| 0.3                                                        | 0.802                                                      |
| 0.4                                                        | 1.13                                                       |
| 0.5                                                        | 1.45                                                       |
| 0.511                                                      | 1.49                                                       |
| 0.6                                                        | 1.78                                                       |
| 0.662                                                      | 1.98                                                       |
| 0.8                                                        | 2.41                                                       |
| 1.0                                                        | 3.03                                                       |
| 1.117                                                      | 3.37                                                       |
| 1.33                                                       | 3.98                                                       |
| 1.5                                                        | 4.45                                                       |
| 2.0                                                        | 5.7                                                        |
| 3.0                                                        | 7.9                                                        |
| 4.0                                                        | 9.86                                                       |
| 5.0                                                        | 11.7                                                       |
| 6.0                                                        | 13.4                                                       |
| 6.129                                                      | 13.6                                                       |
| 8.0                                                        | 16.6                                                       |
| 10.0                                                       | 19.7                                                       |
| 15.0 20.0                                                  | 27.1 34.4                                                  |
| 30.0                                                       | 48.1                                                       |
| 40.0 50.0                                                  | 60.9                                                       |
| 60.0                                                       | 72.2 82.0                                                  |
| 80.0                                                       |                                                            |
|                                                            | 97.9                                                       |
| 100.0                                                      | 110.0                                                      |
| 150.0                                                      | 130.0                                                      |
| 200.0                                                      | 143.0                                                      |
| 300.0                                                      | 161.0                                                      |
| 400.0                                                      | 172.0                                                      |
| 500.0                                                      | 180.0                                                      |
| 600.0                                                      | 186.0                                                      |
| 800.0                                                      | 195.0                                                      |
| 1.0e3 1.5e3                                                | 201.0 212.0                                                |
| 2.0e3                                                      | 220.0                                                      |
| 3.0e3                                                      | 229.0                                                      |

58

59

60

61

62

63

| 4.0e3   | 235.0   |
|---------|---------|
| 5.0e3   | 240.0   |
| 6.0e3   | 244.0   |
| 8.0e3   | 251.0   |
| 1.0e4   | 255.0   |
| c       | c       |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.37: Photon\_ICRP116-2010\_Rotational\_ROT\_dedf.txt

| c c ICRP/116-2010, Rotational (ROT), from Table A.1:   | c c ICRP/116-2010, Rotational (ROT), from Table A.1:   |
|--------------------------------------------------------|--------------------------------------------------------|
| Energy Fluence-to-dose Conversion Factor               | Energy Fluence-to-dose Conversion Factor               |
| [MeV]                                                  | [pSv$\cdot$cm$^{2}$]                                   |
| de:p                                                   | df:p                                                   |
| log                                                    | log                                                    |
| 0.01                                                   | 0.0337                                                 |
| 0.015                                                  | 0.0664                                                 |
| 0.02                                                   | 0.0986                                                 |
| 0.03                                                   | 0.158                                                  |
| 0.04                                                   | 0.199                                                  |
| 0.05                                                   | 0.226                                                  |
| 0.06                                                   | 0.248                                                  |
| 0.07                                                   | 0.273                                                  |
| 0.08                                                   | 0.297                                                  |
| 0.1                                                    | 0.355                                                  |
| 0.15                                                   |                                                        |
|                                                        | 0.528                                                  |
| 0.2 0.3                                                | 0.721 1.12                                             |
| 0.4                                                    | 1.52                                                   |
| 0.5                                                    | 1.92                                                   |
| 0.511                                                  | 1.96                                                   |
| 0.6                                                    | 2.3                                                    |
| 0.662                                                  | 2.54                                                   |
| 0.8                                                    | 3.04                                                   |
| 1.0                                                    | 3.72                                                   |
| 1.117                                                  | 4.1                                                    |
| 1.33                                                   | 4.75                                                   |
| 1.5                                                    | 5.24                                                   |
| 2.0                                                    | 6.55                                                   |
| 3.0                                                    | 8.84                                                   |
| 4.0                                                    | 10.8                                                   |
| 5.0                                                    | 12.7                                                   |
| 6.0                                                    | 14.4                                                   |
| 6.129                                                  | 14.6                                                   |
| 8.0                                                    | 17.6                                                   |
| 10.0                                                   | 20.6                                                   |
| 15.0                                                   | 27.7                                                   |
| 20.0                                                   | 34.4                                                   |
| 30.0                                                   | 46.1                                                   |
| 40.0                                                   | 56.0                                                   |
| 50.0                                                   | 64.4                                                   |
| 60.0                                                   | 71.2                                                   |
| 80.0                                                   | 82.0                                                   |
| 100.0                                                  | 89.7                                                   |
| 150.0                                                  | 102.0                                                  |
| 200.0                                                  | 111.0                                                  |
| 300.0                                                  | 121.0                                                  |
| 400.0                                                  | 128.0                                                  |
| 500.0                                                  | 133.0                                                  |
| 600.0                                                  | 136.0                                                  |
| 800.0                                                  | 142.0                                                  |
| 1.0e3                                                  | 145.0                                                  |
| 1.5e3                                                  | 152.0 156.0                                            |
| 2.0e3                                                  |                                                        |
| 3.0e3                                                  | 161.0                                                  |

58

59

60

61

62

63

| 4.0e3   | 165.0   |
|---------|---------|
| 5.0e3   | 168.0   |
| 6.0e3   | 170.0   |
| 8.0e3   | 172.0   |
| 1.0e4   | 175.0   |
| c       | c       |

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

47

48

49

50

51

52

53

54

55

56

57

Listing F.38: Photon\_ICRP116-2010\_Isotropic\_ISO\_dedf.txt

| c c ICRP/116-2010, Isotropic (ISO), from Table A.1:   | c c ICRP/116-2010, Isotropic (ISO), from Table A.1:   |
|-------------------------------------------------------|-------------------------------------------------------|
| Energy Fluence-to-dose Conversion Factor              | Energy Fluence-to-dose Conversion Factor              |
| [MeV]                                                 | [pSv$\cdot$cm$^{2}$]                                  |
| de:p                                                  | df:p                                                  |
| log                                                   | log                                                   |
| 0.01                                                  | 0.0288                                                |
| 0.015                                                 | 0.056                                                 |
| 0.02                                                  | 0.0812                                                |
| 0.03                                                  | 0.127                                                 |
| 0.04                                                  | 0.158                                                 |
| 0.05                                                  | 0.18                                                  |
| 0.06                                                  | 0.199                                                 |
| 0.07                                                  | 0.218                                                 |
| 0.08                                                  | 0.239                                                 |
| 0.1                                                   | 0.287                                                 |
| 0.15                                                  | 0.429                                                 |
| 0.2                                                   | 0.589                                                 |
| 0.3                                                   | 0.932                                                 |
| 0.4                                                   | 1.28                                                  |
| 0.5                                                   | 1.63                                                  |
| 0.511                                                 | 1.67                                                  |
| 0.6                                                   | 1.97                                                  |
| 0.662                                                 | 2.17                                                  |
| 0.8                                                   | 2.62                                                  |
| 1.0                                                   | 3.25                                                  |
| 1.117                                                 | 3.6                                                   |
| 1.33                                                  | 4.2                                                   |
| 1.5                                                   | 4.66                                                  |
| 2.0                                                   | 5.9                                                   |
| 3.0                                                   | 8.08                                                  |
| 4.0                                                   | 10.0                                                  |
| 5.0                                                   | 11.8                                                  |
| 6.0                                                   | 13.5                                                  |
| 6.129                                                 | 13.7                                                  |
| 8.0                                                   | 16.6                                                  |
| 10.0                                                  | 19.6                                                  |
| 15.0                                                  | 26.8                                                  |
| 20.0                                                  | 33.8                                                  |
| 30.0                                                  | 46.1                                                  |
| 40.0 50.0                                             | 56.9                                                  |
| 60.0                                                  | 66.2                                                  |
|                                                       | 74.1                                                  |
| 80.0                                                  | 87.2                                                  |
| 100.0                                                 | 97.5                                                  |
| 150.0                                                 | 116.0                                                 |
| 200.0                                                 | 130.0                                                 |
| 300.0                                                 | 147.0                                                 |
| 400.0                                                 | 159.0                                                 |
| 500.0                                                 | 168.0                                                 |
| 600.0                                                 | 174.0                                                 |
| 800.0                                                 | 185.0                                                 |
| 1.0e3 1.5e3                                           | 193.0                                                 |
| 2.0e3                                                 | 208.0 218.0                                           |
| 3.0e3                                                 | 232.0                                                 |

58

59

60

61

62

63

| 4.0e3   | 243.0   |
|---------|---------|
| 5.0e3   | 251.0   |
| 6.0e3   | 258.0   |
| 8.0e3   | 268.0   |
| 1.0e4   | 276.0   |
| c       | c       |

Figure F.26: ANSI/ANS-6.1.1-1977 Photon Flux-to-dose Conversion Factors

<!-- image -->

Figure F.27: ANSI/ANS-6.1.1-1991 Anterior-Posterior (AP) Photon Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.28: ANSI/ANS-6.1.1-1991 Posterior-Anterior (PA) Photon Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.29: ANSI/ANS-6.1.1-1991 Lateral (LAT) Photon Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.30: ANSI/ANS-6.1.1-1991 Rotational (ROT) Photon Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.31: ANSI/ANS-6.1.1-1991 Isotropic (ISO) Photon Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.32: ICRP/21-1973 Photon Flux-to-dose Conversion Factors

<!-- image -->

Figure F.33: ICRP/116-2010 Anterior-Posterior (AP) Photon Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.34: ICRP/116-2010 Posterior-Anterior (PA) Photon Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.35: ICRP/116-2010 Left Lateral (LLAT) Photon Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.36: ICRP/116-2010 Right Lateral (RLAT) Photon Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.37: ICRP/116-2010 Rotational (ROT) Photon Fluence-to-dose Conversion Factors

<!-- image -->

Figure F.38: ICRP/116-2010 Isotropic (ISO) Photon Fluence-to-dose Conversion Factors

<!-- image -->
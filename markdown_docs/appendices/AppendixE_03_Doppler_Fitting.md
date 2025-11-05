---
title: "Appendix E.3 - On-the-fly Doppler Broadened Data Fitting"
chapter: "E.3"
source_pdf: "mcnp631_theory_user-manual/appendecies/E.3_On-the-fly_Doppler_Broadened_Data_Fitting_(fit.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## E.3 On-the-fly Doppler Broadened Data Fitting ( fit \_ otf )

This tool generates data for the on-the-fly temperature dependent
nuclear data capability (see card OTFDB ). Generating a library is a
two-stage process. First, the nuclear data library is scanned to
generate a temperatureunionized energy grid in -ugrid mode. Then, in
-fit mode, at each point in the unionized grid, a polynomial curve fit
is generated as a function of temperature.

## E.3.1 User Interface

## Modes (one must be selected)

| -fit   | Enables fitting the nuclear data. This is the second stage to generating a library. Enables fit -specific arguments below.         |
|--------|------------------------------------------------------------------------------------------------------------------------------------|
| -test  | Tests the fitting procedure over a defined energy range. Mainly used for debugging. Enables fit and test specific arguments below. |
| -ugrid | Generates the unionized grid. This is the first stage to generating a library. Enables ugrid -specific arguments below.            |

## Arguments valid in all modes

| -ace _ file   | The ACE file to extract the nuclear data from. (OPTIONAL, DEFAULT: finds the table identifier set on -zaid in xsdir _ mcnp6.3 in the DATAPATH )                                                                                                                      |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -tol _ err    | The target relative error to process the library to. During the ugrid stage, this is used to determine how fine the energy grid is. During the fit stage, this is used to determine what order of polynomial is necessary in temperature. (OPTIONAL, DEFAULT: 0.001) |
| -ugrid _ file | The name of the file for the unionized grid. It is generated with -ugrid , and used with -fit . (REQUIRED)                                                                                                                                                           |
| -zaid         | The table identifier to perform the operation on. This must exactly match the value in the xsdir file. (REQUIRED)                                                                                                                                                    |

## ugrid (unionized energy grid generation)-specific arguments

| -ugrid _ ace _ zaid   | Which table identifier to process into a unionized energy grid. Should match -zaid . (REQUIRED)                                                                                            |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -ugrid _ tmin         | The lower temperature bound to use in Kelvin. If this value is lower than the temperature of the nuclear data, the nuclear data temperature will be used instead. (OPTIONAL, DEFAULT: 250) |
| -ugrid _ tmax         | The upper temperature bound to use in Kelvin. (OPTIONAL, DEFAULT: 3200)                                                                                                                    |
| -ugrid _ tinc         | The spacing between temperatures used during processing in Kelvin. Finer values can generate higher quality data at the cost of greater processing time. (OPTIONAL, DEFAULT: 50)           |

1

2

3

1

2

## fit -specific arguments

| -otf _ file   | The output filename for the coefficients. (OPTIONAL, DEFAULT: otf _ file.txt )                                                                                                                                                       |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -order        | If present, both -order _ min and -order _ max are set to this value. (OPTIONAL, DEFAULT: unset)                                                                                                                                     |
| -order _ min  | The minimum curve-fit order used to fit the temperature data. (OPTIONAL, DEFAULT: 1)                                                                                                                                                 |
| -order _ max  | The maximum curve-fit order used to fit the temperature data. In general, increasing this value will provide no benefit, as the numerical stability of the fitting algorithm gets worse beyond an order of 8. (OPTIONAL, DEFAULT: 8) |
| -tmin         | The lower temperature bound to use in Kelvin. If this value is lower than the temperature of the nuclear data, the nuclear data temperature will be used instead. (OPTIONAL, DEFAULT: 250)                                           |
| -tmax         | The upper temperature bound to use in Kelvin. (OPTIONAL, DEFAULT: 3200)                                                                                                                                                              |
| -tinc         | The spacing between temperatures used during processing in Kelvin. Finer values can generate higher quality data at the cost of greater processing time. (OPTIONAL, DEFAULT: 50)                                                     |

## test -specific arguments

| -test _ emin   | Lower energy bound to test fitting approach in MeV. (REQUIRED)   |
|----------------|------------------------------------------------------------------|
| -test _ emax   | Upper energy bound to test fitting approach in MeV. (REQUIRED)   |

## E.3.2 Examples

In this example, the ENDF/B-VII.1 library for 238 U will be processed
from 250 K to 3000 K with a target tolerance of 0.1%. A temperature step
of 25 K will be used. In order to get to 250 K, a nuclear data library
that is at or below this energy must be provided. Here, 92238.86c has a
temperature of 250 K. The first step is to generate the unionized energy
grid:

```
fit _ otf -zaid 92238.86c -ugrid -ugrid _ ace _ zaid 92238.86c \ -ugrid _ tmin 250 -ugrid _ tmax 3000 -ugrid _ tinc 25 \ -ugrid _ file ugrid _ 92238.86c
```

Once this process is completed, the file ugrid \_ 92238.86c will contain
the necessary unionized energy grid for phase two:

```
fit _ otf -zaid 92238.86c -fit -tmin 250 -tmax 3000 -tinc 25 \ -ugrid _ file ugrid _ 92238.86c -otf _ file otf _ 92238.86c.txt
```

This process will generate the necessary otf \_ 92238.86c.txt file. This
file can be added to the DATAPATH , or stored alongside the input file
in the working directory. At the end of processing, the output will
describe the quality of the library, including the number of energy
points that had errors exceeding -tol \_ err , and by how much this error
was exceeded:

```
1 Overall error checks: 2 mt= 1 max-err= 0.100% for e= 10589.2 eV, t= 275.0 K 3 mt=101 max-err= 0.103% for e= 4266.55 eV, t= 350.0 K 4 mt= 2 max-err= 0.433% for e= 20.2818 eV, t= 350.0 K 5 mt=301 max-err= 0.232% for e= 718.922 eV, t= 350.0 K 6 mt=202 max-err= 0.108% for e= 4266.81 eV, t= 350.0 K 7 mt= 18 max-err= 0.041% for e= 723.763 eV, t= 625.0 K 8 mt=102 max-err= 0.108% for e= 4266.81 eV, t= 350.0 K 9 mt=444 max-err= 0.002% for e= 20.6298 eV, t= 350.0 K 10 11 Overall maximum error = 0.433% 12 13 Number of energies with err > 0.10% = 101
```

If these error values are acceptable, the file is ready for use with the
OTFDB card. If it is not, one can tune the parameters using the testing
mode prior to re-evaluating the whole library. In the example below, the
0.433% error at 20.2818 eV is re-examined with a maximum fit order of
10.

1

2

3

```
fit _ otf -zaid 92238.86c -test -fit -tmin 250 -tmax 3000 -tinc 25 \ -ugrid _ file ugrid _ 92238.86c -order _ max 10 \ -test _ emin 2.0e-5 -test _ emax 2.1e-5
```

With this data, the new maximum error is 1.528%, indicating that
increasing the order will not improve the result past 0.433% due to
numerical instability.
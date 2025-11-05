# MCNP6 ROSSI Validation

The MCNP Rossi Validation Suite is a collection of 14 benchmarks in which the `KOPTS kinetics` computed Rossi-alpha is compared against experimental values.
It must be noted that the MCNP input decks in this suite are ICSBEP benchmark models, while the Rossi-alpha values compared against are the raw experimental values.
This is unlike the criticality validation suites, in which the reference value has been modified to incorporate corrections due to the benchmark model simplification process.

The description of this suite can be found in R.D. Mosteller, B.C. Kiedrowski, "A Rossi Alpha Validation Suite for MCNP", International Conference on Nuclear Criticality 2011, Edinburgh, Scotland, September 19-22, 2011. LA-UR-11-01162.

This directory contains the *experiments* subdirectory, the *references* subdirectory, this *README.md*, and a few supporting python scripts to be used to run, process and analyze results.  Instructions on the use of these python scripts will be updated in due time.

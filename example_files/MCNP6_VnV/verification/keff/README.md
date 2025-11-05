# MCNP6 k-effective Verification

This verification test suite is a series of input and data files for the MCNP code for a series of analytic k-eigenvalue benchmarks. 
These benchmarks are from the paper "Analytical Benchmark Test Set for Criticality Code Verification", by Avneet Sood, Arthur R. Forster, and Kent D. Parsons (LA-UR-01-3082), and include continuous energy and multigroup problems.

Several problems have been excluded from this verification set.
First, continuous energy solutions are not available for any multigroup problem (44 onwards).
Second, any problem with P2 Legendre moments are excluded (33, 35).
Finally, problems with negative scattering probability are excluded (34, 35, 37, 42, 43, 71).

Due to limitations in the MCNP MCTAL file format, the precision of the output is limited to five digits.
Several of the analytic solutions are given with more than five significant figures.
As a result, comparisons (and the resulting discrepancies) past the first five digits are not meaningful due to rounding.



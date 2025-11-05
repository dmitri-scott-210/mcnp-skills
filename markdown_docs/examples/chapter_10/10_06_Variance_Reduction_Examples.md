---
title: "Chapter 10.6 - Variance Reduction Examples"
chapter: "10.6"
source_pdf: "mcnp631_theory_user-manual/mcnp-primers-examples/10.6_Variance_Reduction_Examples.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

Table 10.4: Results Compiled for Summary Cases

| Case   | Variation from base case                                |    n/p |
|--------|---------------------------------------------------------|--------|
| Base   | N/A                                                     | 17.369 |
| 1      | Bertini INC and light ion transport                     | 17.398 |
| 2      | ISABEL INC for nucleons and pions                       | 16.371 |
| 3      | CEM INC for nucleons and pions                          | 18.33  |
| 4      | INCL INC for nucleons and pions; ABLA evaporation model | 16.649 |

Net neutron production for this case is 16.649 n/p, which is 4.14% less
than the base case value.

## 10.5.1.6 Summary

Results compiled for each case of this example are shown in Table 10.4.
Runtimes between the model physics options do vary. In general, the
Bertini and ISABEL models have comparable runtimes for the cases within
this exercise. The CEM model was the most computationally efficient
while the INCL/ABLA model was roughly double the computational time of
CEM.

This example demonstrates how to calculate neutron production from a
spallation target. When the quantity of interest depends only on
neutrons and one starts with a proton beam, there is no need to
transport any particles other than protons, neutrons, and charged pions,
as neutron production by other particles is negligible compared to
production by these three particle types. All particles should be
included for energy deposition calculations, as discussed in §5.9.1.1.
Use of the various physics model options, such as the CEM03.03. Bertini,
and INCL modules, within MCNP6 is encouraged-this ability allows the
user to test the sensitivity of the quantity of interest to the
different physics models. If significant differences are observed, the
user should evaluate which physics model is most appropriate for their
particular application. For example, total neutron production from
actinide targets is known to be more accurate if the multi-step pre-
equilibrium model (MPM) is turned off while using Bertini INC and/or
ISABEL INC.

## 10.6 Variance Reduction Examples

## 10.6.1 Pathological Concrete Shell Example

This simple, but pathological, problem illustrates how to use and
interpret results from point and ring detectors that is discussed in
greater detail in §2.6.10. It also shows how the statistical checks can
reveal deficiencies in the tallies of an otherwise seemingly well-
behaved problem.

The problem consists of a spherical shell of concrete with a 390 cm
outer radius and a 360 cm inner radius [147]. A 14 MeV point isotropic
neutron source is at (0 , 0 , 0) , the center of the void region. It is
a neutron-only problem ( MODE n ; this is the default mode and thus the
MODE card does not appear in the input file), with a neutron lower-
energy cutoff at 12 MeV. A surface-flux and track-length tally is used
in addition to point and ring detectors.

Even though this is a simple problem, it is difficult, and even
inappropriate, for the F5 -type point detector. Detectors are usually
inappropriate when particles can be transported readily to the region of
interest and another type of tally, such as the F2 surface flux tally,
or even better (because there is no grazing-angle approximation), the F4
track-length tally can be used. Also, detectors do not generally work
well close to or in scattering regions. This problem is especially
difficult for point detectors because the largest history scores occur
for neutrons that not only have several collisions near the detector
point but also stay above the

12-MeV energy cutoff. These histories are extremely rare, important, and
generally undersampled (leading to the long tail in the high-score
region of the EHSPDF).

To demonstrate the long-tail behavior, two calculations are used with 10
4 and 10 8 histories, shown in Listings 10.47 and 10.48, respectively.
Interactive-plotter command-input files [§6.2.1] to generate the figures
shown in §2.6.10 are given in Listings 10.49, 10.50, and 10.51.

Listing 10.47: example\_vr\_conc\_shell\_ehspdf\_10k.mcnp.inp.txt

<!-- image -->

Listing 10.48: example\_vr\_conc\_shell\_ehspdf\_100m.mcnp.inp.txt

<!-- image -->

```
23 print 24 prdmp 4j 5e6 25 nps 1e8
```

10

11

12

13

14

15

16

17

```
1 run=example _ vr _ conc _ shell _ ehspdf _ 10k.mcnp.inp.txtr.h5 file all & 2 tfc m xlims 0 10000 ylims 0 1.4-7 & 3 title 2 "mean leakage fluxes as a function of the number of histories" & 4 noerr tal 4 lab "track length" cop tal 15 lab "ring detector" cop 5 tal 5 lab "point detector" 6 tfc e linlog ylims 1-3 1 & 7 title 2 "relative errors as a function of the number of histories" & 8 tal 4 lab "track length" cop tal 15 lab "ring detector" cop 9 tal 5 lab "point detector" tfc v title 2 "variance of the variance as a function of the number of histories" & tal 4 lab "track length" cop tal 15 lab "ring detector" cop tal 5 lab "point detector" tfc s linlin ylims 0 4 & title 2 "slope of f(x) for large scores as a function of the number of histories" & tal 4 lab "track length" cop tal 15 lab "ring detector" cop tal 5 lab "point detector" end
```

Listing 10.49: example\_vr\_conc\_shell\_tallies\_10k.mcnp.comin.txt

```
1 run=example _ vr _ conc _ shell _ ehspdf _ 100m.mcnp.inp.txtr.h5 file all & 2 tfc m xlims 0 1+8 ylims 5.5-8 7.5-8 & 3 title 2 "mean leakage fluxes as a function of the number of histories" & 4 noerr tal 4 lab "track length" cop tal 15 lab "ring detector" cop 5 tal 5 lab "point detector" 6 tfc e linlog ylims 1-4 0.2 & 7 title 2 "relative errors as a function of the number of histories" & 8 tal 4 lab "track length" cop tal 15 lab "ring detector" cop 9 tal 5 lab "point detector" 10 tfc v ylims 1-4 1 & 11 title 2 "variance of the variance as a function of the number of histories" & 12 tal 4 lab "track length" cop tal 15 lab "ring detector" cop 13 tal 5 lab "point detector" 14 tfc s linlin ylims 0 10.1 & 15 title 2 "slope of f(x) for large scores as a function of the number of histories" & 16 tal 4 lab "track length" cop tal 15 lab "ring detector" cop 17 tal 5 lab "point detector" 18 end
```

Listing 10.50: example\_vr\_conc\_shell\_tallies\_100m.mcnp.comin.txt

Listing 10.51: example\_vr\_conc\_shell\_ehspdf.mcnp.comin.txt

```
run=example _ vr _ conc _ shell _ ehspdf _ 10k.mcnp.inp.txtr.h5 file all tfc p xlims 1-8 .2 ylims 1-7 1+9 & title 2 "empirical f(x)'s for concrete shell leakage flux tallies for 10k histories" & tal 4 fac x 5.23-3 0 fac y 191.135 0 lab "track length" cop tal 15 lab "ring detector" cop tal 5 lab "point detector" run=example _ vr _ conc _ shell _ ehspdf _ 100m.mcnp.inp.txtr.h5 & title 2 "empirical f(x)'s for concrete shell leakage flux tallies for 100m histories" & tfc p tal 4 fac x 5.23-3 0 fac y 191.135 0 lab "track length" cop tal 15 lab "ring detector" cop tal 5 lab "point detector" end
```

1

2

3

4

5

6

7

8

9
---
title: "Source Primer Chapter 4 - Advanced Sources"
chapter: "Source-4"
source_pdf: "mcnp6-primer-docs/mcnp6-source-primer/4.Advanced_Sources.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## 4.1 Surface Source Write/Read

## 4.1.1 Single Particle Coupling

Example of a Cs-137 photon source incased in a Tungsten shell creating a
beam that strikes a Lead target.

## Full calculation

This portion of the example includes the full calculation without the
surface write/read cards.

```
Cs-137 example c c Cell Cards c 10 0 -1 IMP:P=1 20 0 +1 -2 +3 -4 IMP:P=1 30 100 -19.25 +1 -2 -3 -4 IMP:P=1 40 100 -19.25 +1 -2 +4 IMP:P=1 50 200 -7.874 -6 IMP:P=1 60 0 -5 +2 -9 IMP:P=1 70 0 +5 +6 -9 IMP:P=1 99 0 +9 IMP:P=0 c c Surface Cards c 1 SO 5 2 SO 10 3 PZ 0 4 CZ 0.5 5 PZ 12.5 6 RPP -10 10 -10 10 15 18 9 SO 50 c c Data Cards c MODE P NPS 1e6 c
```

Listing 4.1: MCNP6 Input File

## ADVANCED SOURCES

```
SDEF PAR=P ERG=0.662 c c Materials c M100 74184 1.0 M200 26056 1.0 c FMESH4:P GEOM=XYZ ORIGIN=-20 -20 -30 IMESH=20 IINTS=100 JMESH=20 JINTS=100 KMESH=30 KINTS=150 OUT=NONE
```

Below is the plot of the photon flux from the source throughout the
geometry including reflecting off the exterior Lead target.

<!-- image -->

```
fmesh 4 file end end
```

## Surface Source Write

Example using the surface source write (SSW) option for Cs-137 exiting
Tungsten shell.

```
Cs-137 example SSW c c Cell Cards c 10 0 -1 IMP:P=1 20 0 +1 -2 +3 -4 IMP:P=1 30 100 -19.25 +1 -2 -3 -4 IMP:P=1 40 100 -19.25 +1 -2 +4 IMP:P=1 50 0 -6 IMP:P=0 60 0 -5 +2 -9 IMP:P=1 70 0 +5 +6 -9 IMP:P=0 99 0 +9 IMP:P=0 c c Surface Cards c 1 SO 5 2 SO 10 3 PZ 0 4 CZ 0.5 5 PZ 12.5 6 RPP -10 10 -10 10 15 18 9 SO 50 c c Data Cards c MODE P NPS 1e6 SSW 5 c SDEF PAR=P ERG=0.662 c c Materials c M100 74184 1.0 M200 26056 1.0 c FMESH4:P GEOM=XYZ ORIGIN=-20 -20 -30 IMESH=20 IINTS=100 JMESH=20 JINTS=100 KMESH=30 KINTS=150 OUT=NONE
```

Listing 4.3: MCNP6 Input File

Listing 4.2: MCNP6 Plotting Commands

Below, a plot shows the Cs-137 inside sphere case creating a beam. The
SSW cuts off the beam when it intersects surface 5 so the source at this
point can be used in further problems and applications using the surface
source read (SSR) option.

<!-- image -->

Listing 4.4: MCNP6 Plotting Commands

<!-- image -->

## Surface Source Read

Continuation of the SSW for the Cs-137 beam where the surface source
read (SSR) continues the calculation and has the beam hitting the Lead
target. Note that seperating the two calculations can save computing
time and make the code more efficient especially if you are planning to
use the source created in your SSW calculations for multiple SSR
applications.

```
Cs-137 example SSR c c Cell Cards c 10 0 -1 IMP:P=1 20 0 +1 -2 +3 -4 IMP:P=1 30 100 -19.25 +1 -2 -3 -4 IMP:P=1 40 100 -19.25 +1 -2 +4 IMP:P=1 50 200 -7.874 -6 IMP:P=1 60 0 -5 +2 -9 IMP:P=1 70 0 +5 +6 -9 IMP:P=1 99 0 +9 IMP:P=0 c c Surface Cards c 1 SO 5 2 SO 10 3 PZ 0 4 CZ 0.5 5 PZ 12.5 6 RPP -10 10 -10 10 15 18 9 SO 50 c c Data Cards c MODE P NPS 1e6 SSR c c Materials c M100 74184 1.0 M200 26056 1.0 c FMESH4:P GEOM=XYZ ORIGIN=-20 -20 -30 IMESH=20 IINTS=100 JMESH=20 JINTS=100 KMESH=30 KINTS=150 OUT=NONE
```

Listing 4.5: MCNP6 Input File

The plot below shows the continuation of the source at surface 5 and
calculates the outcome of the source hitting the Lead target.

<!-- image -->

Listing 4.6: MCNP6 Plotting Commands

```
fmesh 4 file end end
```

## 4.1.2 Multiple Particle Coupling

## Surface Source Write

Example of a surface source write input file with a proton beam incident
on a Tungsten target. Ultimately, the neutron spallation source from
this proton beam is desired to model various configurations.

```
Proton source on Tungsten target c c Cell Cards c 10 0 +1 -9 IMP:H,N=1 20 0 -1 +2 -9 IMP:H,N=1 30 100 -19.25 -2 IMP:H,N=1 99 0 +9 IMP:H,N=0
```

Listing 4.7: MCNP6 Input File

```
c c Surface Cards c 1 PX 10 2 RPP 2.5 5 -2.5 2.5 -2.5 2.5 9 RPP -15 15 -15 15 -15 15 c c Data Cards c MODE H N NPS 1e5 SSW 1 PTY=N c PHYS:H 150 SDEF PAR=H ERG=150 VEC=1 0 0 DIR=1 c c Materials c M100 74184 1.0 c FMESH4:H GEOM=XYZ ORIGIN=-5 -5 -5 IMESH= 5 IINTS=150 JMESH= 5 JINTS=150 KMESH= 5 KINTS=150 OUT=NONE c FMESH14:N GEOM=XYZ ORIGIN=-15 -15 -15 IMESH=15 IINTS=150 JMESH=15 JINTS=150 KMESH=15 KINTS=150 OUT=NONE
```

A flux mesh plot of the proton beam as it interacts with the Tungsten on
the XY plane.

The flux mesh plot of the spallation neutrons created from the proton beam source on the XY plane.

<!-- image -->

<!-- image -->

Listing 4.8: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 fmesh 14 file end end
```

## Surface Source Read

Surface source read file that tests neutrons produced from the high-
energy proton source incident on the Tungsten spallation target.

```
Neutron spallation source read c c Cell Cards c 10 0 -11 -9 IMP:N=1 20 0 +11 -2 -9 IMP:N=1 30 100 -1.0 +2 +4 -5 -9 IMP:N=1 40 200 -7.874 +2 +3 -4 -5 IMP:N=1 50 0 +2 -3 -5 IMP:N=1
```

Listing 4.9: MCNP6 Input File

```
60 0 +5 -9 IMP:N=1 99 0 +9 IMP:N=0 c c Surface Cards c 11 PX 5 2 PX 10 3 CX 2.5 4 CX 7.5 5 PX 60 9 RPP 0 100 -25 25 -25 25 c c Data Cards c MODE N NPS 5e6 SSR NEW 11 TR=1 TR1 -5 0 0 c c Materials c M100 1001 2 8016 1 5010 2 MT100 lwtr M200 26056 1.0 c F4:N 60 E4 1E-6 99ilog 30 c FMESH14:N GEOM=XYZ ORIGIN= 0 -25 -25 IMESH=100 IINTS=200 JMESH=25 JINTS=50 KMESH=25 KINTS=50 OUT=NONE c PRINT
```

The following plot shows the energy spectrum of neutrons reaching the
void cell beyond the borated water surrounded collimator.

<!-- image -->

The mesh plot of the flux of neutrons as they travel down the
collimator.

<!-- image -->

The mesh plot at the end of the collimator showing the peak of neutrons
traveling through the collimator.

<!-- image -->

Listing 4.10: MCNP6 Plotting Commands

```
tal 4 loglog xlims 1.e-6 3.e+1 fmesh 14 basis 1 0 0 0 1 0 basis 0 1 0 0 0 1 origin 61 0 0 file end end
```

## 4.1.3 Criticality Fission Source Coupling

## Surface Source Write

This example is a neutron-only criticality calculation, where the
fission source points are saved in the SSW cell location.

```
Simplified CAAS --surface soure write c ### cells c c >>>>> accident tank c 100 1 9.9270e-2 -10 -12 imp:n=1 101 3 4.8333e-5 -10 +12 imp:n=1 102 2 8.6360e-2 +10 -11 imp:n=1 c c >>>>> facility rooms: nw. -> ne., sw. -> se.
```

Listing 4.11: MCNP6 Input File

```
c 200 3 4.8333e-5 -20 imp:n=1 210 3 4.8333e-5 -21 +11 imp:n=1 220 3 4.8333e-5 -22 imp:n=1 c c >>>>> doorways c 260 3 4.8333e-5 -30 imp:n=1 261 3 4.8333e-5 -31 imp:n=1 262 3 4.8333e-5 -32 imp:n=1 c c >>>>> facility and rest of world c 900 4 0.0764 -99 +20 +21 +22 +30 +31 +32 imp:n=1 999 0 +99 imp:n=0 c ### surfaces c c >>>>> critical experiment tank 10 rcc 0 0 1 0 0 100 50 11 rcc 0 0 0 0 0 101 50.5 12 pz 13.6 c c >>>>> rpp's for the empty space in the rooms 20 rpp -1100 -500 -300 300 0 300 21 rpp -300 300 -300 300 0 300 22 rpp -450 -350 -300 300 0 300 c c >>>>> doorways 30 rpp -350 -300 -300 -200 0 250 31 rpp 300 350 200 300 0 250 32 rpp -500 -450 200 300 0 250 c c >>>>> building structure 99 rpp -1150 350 -350 350 -50 310 mode n kcode 10000 1.0 25 125 ksrc 0 0 7 c ssw cel = 100 c fmesh4:n geom=xyz origin=-1150 -350 -50 imesh=350 iints=150 jmesh=350 jints=70 kmesh=310 kints=36 type=source c fmesh14:n geom=xyz origin=-1150 -350 -50 imesh=350 iints=150 jmesh=350 jints=70 kmesh=310 kints=36 c c ### materials c plutonium nitrate solution m1 1001 6.0070e-2 8016 3.6540e-2
```

```
7014 2.3699e-3 94239 2.7682e-4 94240 1.2214e-5 94241 8.3390e-7 94242 4.5800e-8 mt1 lwtr c stainless steel m2 24050 7.1866e-4 $ Cr-50 4.345% 24052 1.3859e-2 $ Cr-52 83.789% 24053 1.5715e-3 $ Cr-53 9.501% 24054 3.9117e-4 $ Cr-54 2.365% 26054 3.7005e-3 $ Fe-54 5.845% 26056 5.8090e-2 $ Fe-56 91.754% 26057 1.3415e-3 $ Fe-57 2.119% 26058 1.7853e-4 $ Fe-58 0.282% 28058 4.4318e-3 $ Ni-58 68.0769% 28060 1.7071e-3 $ Ni-60 26.2231% 28061 7.4207e-5 $ Ni-61 1.1399% 28062 2.3661e-4 $ Ni-62 3.6345% 28064 6.0256e-5 $ Ni-64 0.9256% c dry air (typical of American Southwest) m3 1001 1.7404E-10 1002 1.3065E-14 2003 8.3540E-16 2004 4.5549E-10 6000 1.11008E-08 7014 3.8981E-05 7015 1.3515E-07 8016 9.1205E-06 8017 3.4348E-09 18036 3.0439E-10 18038 5.3915E-11 18040 8.0974E-08 36078 1.7811E-14 36080 1.1164E-13 36082 5.6154E-13 36083 5.49985E-13 36084 2.69359E-12 36086 7.98498E-13 54124 2.30549E-13 mt3 lwtr c los alamos concrete m4 1001 0.00842 8016 0.04423 13027 0.00252 14028 0.014690958 14029 0.000718176 14030 0.000460866 11023 0.00105 20040 2.84037E-03 20042 1.89571E-05 20043 3.95550E-06 20044 6.11198E-05 20046 1.17200E-07 20048 5.47910E-06 26054 0.000041788 26056 0.000632003 26057 0.000014347
```

```
26058 0.000001862 19039 6.43481E-04 19040 8.07300E-08 19041 4.64384E-05 mt4 lwtr
```

The following mesh plot contains the fission source locations over all
of the active cycles.

<!-- image -->

Below is the flux mesh plot on the XY plane.

<!-- image -->

And the flux mesh plot now shown on the XZ plane.

<!-- image -->

Listing 4.12: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 origin -381.62 -9 6.25 ex 1000 fmesh 14 basis 1 0 0 0 1 0 origin -381.62 -9 6.25 ex 1000 basis 1 0 0 0 0 1 origin -381.62 -9 6.25 ex 1000 file end end
```

## Surface Source Read

This surface source read example continues the neutron-only criticality
fission source. This SSR calculation is a fixedsource neutron-photon
problem where the fission reactions are treated as capture reactions and
photons are produced from the fission source locations.

```
Simplified CAAS --surface soure read c ### cells c c >>>>> accident tank c 100 1 9.9270e-2 -10 -12 imp:n=1 101 3 4.8333e-5 -10 +12 imp:n=1 102 2 8.6360e-2 +10 -11 imp:n=1 c c >>>>> facility rooms: nw. -> ne., sw. -> se. c 200 3 4.8333e-5 -20 imp:n=1 210 3 4.8333e-5 -21 +11 imp:n=1 220 3 4.8333e-5 -22 imp:n=1 c c >>>>> doorways c 260 3 4.8333e-5 -30 imp:n=1 261 3 4.8333e-5 -31 imp:n=1 262 3 4.8333e-5 -32 imp:n=1 c c >>>>> facility and rest of world c 900 4 0.0764 -99 +20 +21 +22 +30 +31 +32 imp:n=1 999 0 +99 imp:n=0 c ### surfaces c c >>>>> critical experiment tank 10 rcc 0 0 1 0 0 100 50 11 rcc 0 0 0 0 0 101 50.5 12 pz 13.6 c c >>>>> rpp's for the empty space in the rooms 20 rpp -1100 -500 -300 300 0 300 21 rpp -300 300 -300 300 0 300 22 rpp -450 -350 -300 300 0 300 c c >>>>> doorways 30 rpp -350 -300 -300 -200 0 250 31 rpp 300 350 200 300 0 250 32 rpp -500 -450 200 300 0 250 c c >>>>> building structure 99 rpp -1150 350 -350 350 -50 310 nps 1E6 mode n p nonu 0 10r
```

Listing 4.13: MCNP6 Input File

```
c ssr cel = 100 psc = 0.5 c fmesh4:n geom=xyz origin=-1150 -350 -50 imesh=350 iints=150 jmesh=350 jints=70 kmesh=310 kints=36 type=source out=none c fmesh14:n geom=xyz origin=-1150 -350 -50 imesh=350 iints=150 jmesh=350 jints=70 kmesh=310 kints=36 out=none c fmesh24:p geom=xyz origin=-1150 -350 -50 imesh=350 iints=150 jmesh=350 jints=70 kmesh=310 kints=36 out=none c print c ### materials c plutonium nitrate solution m1 1001 6.0070e-2 8016 3.6540e-2 7014 2.3699e-3 94239 2.7682e-4 94240 1.2214e-5 94241 8.3390e-7 94242 4.5800e-8 mt1 lwtr c stainless steel m2 24050 7.1866e-4 $ Cr-50 4.345% 24052 1.3859e-2 $ Cr-52 83.789% 24053 1.5715e-3 $ Cr-53 9.501% 24054 3.9117e-4 $ Cr-54 2.365% 26054 3.7005e-3 $ Fe-54 5.845% 26056 5.8090e-2 $ Fe-56 91.754% 26057 1.3415e-3 $ Fe-57 2.119% 26058 1.7853e-4 $ Fe-58 0.282% 28058 4.4318e-3 $ Ni-58 68.0769% 28060 1.7071e-3 $ Ni-60 26.2231% 28061 7.4207e-5 $ Ni-61 1.1399% 28062 2.3661e-4 $ Ni-62 3.6345% 28064 6.0256e-5 $ Ni-64 0.9256% c dry air (typical of American Southwest) m3 1001 1.7404E-10 1002 1.3065E-14 2003 8.3540E-16 2004 4.5549E-10 6000 1.11008E-08 7014 3.8981E-05 7015 1.3515E-07 8016 9.1205E-06 8017 3.4348E-09 18036 3.0439E-10
```

```
18038 5.3915E-11 18040 8.0974E-08 36078 1.7811E-14 36080 1.1164E-13 36082 5.6154E-13 36083 5.49985E-13 36084 2.69359E-12 36086 7.98498E-13 54124 2.30549E-13 mt3 lwtr c los alamos concrete m4 1001 0.00842 8016 0.04423 13027 0.00252 14028 0.014690958 14029 0.000718176 14030 0.000460866 11023 0.00105 20040 2.84037E-03 20042 1.89571E-05 20043 3.95550E-06 20044 6.11198E-05 20046 1.17200E-07 20048 5.47910E-06 26054 0.000041788 26056 0.000632003 26057 0.000014347 26058 0.000001862 19039 6.43481E-04 19040 8.07300E-08 19041 4.64384E-05 mt4 lwtr
```

Below is a plot of the neutron source from the SSR file on the XY plane.

<!-- image -->

The neutron flux is now shown on the XY plane.

<!-- image -->

The photon flux is now shown on the XY plane.

<!-- image -->

The photon flux is now shown on the XZ plane.

<!-- image -->

Listing 4.14: MCNP6 Plotting Commands

```
fmesh 4 basis 1 0 0 0 1 0 origin -381.62 -9 6.25 ex 1000 fmesh 14 fmesh 24 basis 1 0 0 0 0 1 origin -381.62 -9 6.25 ex 1000 file end
```

end

## 4.2 Repeated Structure Lattices

## 4.2.1 Repeated Structures with Lattice

Repeated structure lattice with uniform (in radius, not volume)
spherical source in each sphere.

```
Repeated Structures with Lattices 1 0 -20 FILL=1 IMP:N=1 2 0 -30 U=1 FILL=2 LAT=1 IMP:N=1 3 0 -11 U=-2 IMP:N=1 4 0 11 U=2 IMP:N=1 5 0 20 IMP:N=0 20 RPP 0 50 -10 10 -5 5 30 RPP 0 10 0 10 0 0 11 S 5 5 0 4 NPS 1e6 SDEF RAD=D1 POS=D2 SI1 0 4 SP1 0 1 SI2 L 5 5 0 15 5 0 25 5 0 35 5 0 45 5 0 5 -5 0 15 -5 0 25 -5 0 35 -5 0 45 -5 0 SP2 1 1 1 1 1 1 1 1 1 1 c FMESH4:N GEOM= xyz ORIGIN= -50.0 -50.0 -50.0 IMESH= 50.0 IINTS= 200 JMESH= 50.0 JINTS= 200 KMESH= 50.0 KINTS= 200 TYPE=SOURCE OUT=NONE
```

Listing 4.15: MCNP6 Input File

Point sources seen inside of spheres of repeated structure on XY plane.

<!-- image -->

## View from YZ plane.

<!-- image -->

```
fmesh 4 basis 1 0 0 0 1 0 origin 25 0 0 basis 0 0 1 0 1 0 origin 25 0 0 file end end
```

Listing 4.16: MCNP6 Plotting Commands

## 4.2.2 Displacement and Rotational Transformations

This example contains several LIKE n BUT repeated structures. The
sampling of the cells indicated on the cel keyword shows how to obtain
uniform sampling in each of the cylindrical pins within the geometry in
a shorthand way. This example also contains source energy biasing (SB
card) and a VOID card. Taken from the MCNP6 User's Manual, page 5-22
(see Helpful Links ).

```
Repeated Structure 1 1 -0.5 -7 #2 #3 #4 #5 #6 IMP:N=1 2 0 1 -2 -3 4 5 -6 IMP:N=2 TRCL=2 FILL=1 3 LIKE 2 BUT TRCL=3 4 LIKE 2 BUT TRCL=4 5 LIKE 2 BUT TRCL=5 IMP:N=1 6 LIKE 2 BUT TRCL=6 7 0 7 IMP:N=0 8 0 8 -9 -10 11 IMP:N=1 TRCL=(-.9 .9 0) FILL=2 U=1 9 LIKE 8 BUT TRCL=(.9 .9 0) 10 LIKE 8 BUT TRCL=(.1 -.9 0) 11 2 -18 #8 #9 #10 IMP:N=1 u=1 12 2 -18 -12 IMP:N=1 TRCL=(-.3 .3 0) U=2 13 LIKE 12 BUT TRCL=( .3 .3 0) 14 LIKE 12 BUT TRCL=( .3 -.3 0) 15 LIKE 12 BUT TRCL=(-.3 -.3 0) 16 1 -0.5 #12 #13 #14 #15 U=2 IMP:N=1 1 PX -2 2 PY 2 3 PX 2 4 PY -2 5 PZ -2 6 PZ 2 7 SO 15 8 PX -0.7 9 PY 0.7 10 PX 0.7 11 PY -0.7 12 CZ 0.1 VOID SDEF ERG=D1 CEL=D2:D3:0 RAD=D5 EXT=D6 AXS=0 0 1 POS=D7 SI1 1 3 4 5 6 7 8 9 11 SP1 0 0.22 0.08 0.25 0.18 0.07 0.1 0.05 0.05 SB1 0 0.05 0.05 0.1 0.1 0.2 0.2 0.1 0.2 SI2 L 2 3 4 5 6 SP2 1 1 1 1 1
```

Listing 4.17: MCNP6 Input File

```
SI3 L 8 9 10 SP3 1 1 1 SI5 0 0.1 SP5 -21 1 SI6 -2 2 SP6 0 1 SI7 L 0.3 0.3 0 0.3 -0.3 0 -0.3 0.3 0 -0.3 -0.3 0 SP7 1 1 1 1 M1 6000 1 M2 92235 1 TR2 -6 7 1.2 TR3 7 6 1.1 TR4 8 -5 1.4 TR5* -1 -4 1 40 130 90 50 40 90 90 90 0 TR6 -9 -2 1.3 F4:N (2 3 4 5 6) E4 1 3 4 5 6 7 8 9 11 FQ F E CUT:N 1E20 0.1 NPS 1000000 FMESH14:N GEOM= xyz ORIGIN= -10.0 -10.0 -10.0 IMESH= 10.0 IINTS= 400 JMESH= 10.0 JINTS= 400 KMESH= 10.0 KINTS= 1 TYPE=SOURCE OUT=NONE PRINT
```

## Energy distribution of the cells can be seen below.

<!-- image -->

The source mesh plot in the XY plane of the five level 0 cells 2-6 each
with three level 1 cells 8-10 each containing four level 2 cells 12-15.

<!-- image -->

Closer view of the source mesh plot in the XY plane of cell 3.

<!-- image -->

Listing 4.18: MCNP6 Plotting Commands

```
tal 4 linlin fmesh 14 basis 1 0 0 0 1 0 ex 15 la 0 basis 1 0 0 0 1 0 origin 7 6.5 0 ex 3 file end end
```

## 4.2.3 Lattices with Dependence on Sampled Cell

This example, modified from the example in the MCNP6 User's Manual, page
5-33 (see Helpful Links ), consists of several source variables
dependent on the selected cell. The selected cell is sampled from 4
separate distributions, all with lattice descriptions and some specific
elements given.

```
Lattice Example 6 1 0 1:-3:-4:5:6:-7 imp:n=0 2 0 -2 3 4 -5 -6 7 imp:n=1 fill=1 (-25 0 0) 3 0 -1 2 4 -5 -6 7 imp:n=1 fill=2 (0 -20 0) 4 0 -11 12 -14 13 imp:n=1 lat=1 u=1 fill=-1:1 -1:1 0:0 3 8r 5 3 -1.0 -15 2 -18 17 imp:n=1 lat=1 u=2
```

Listing 4.19: MCNP6 Input File

```
fill=0:1 0:3 0:0 4 4 4(5 0 0) 4 4 5 4 4 6 1 -0.9 21:-22:-23:24 imp:n=1 u=3 7 1 -0.9 19 imp:n=1 u=4 8 2 -18 -21 22 23 -24 imp:n=1 u=3 9 1 -0.9 20(31:-32:-33:34) imp:n=1 u=5 11 2 -18 -19 imp:n=1 u=4 13 2 -18 -20 imp:n=1 u=5 15 2 -18 -31 32 33 -34 imp:n=1 u=5 1 px 50 2 px 0 3 px -50 4 py -20 5 py 20 6 pz 60 7 pz -60 11 px 8.334 12 px -8.334 13 py -6.67 14 py 6.67 15 px 25 17 py 0 18 py 10 19 c/z 10 5 3 20 c/z 10 5 3 21 px 4 22 px -4 23 py -3 24 py 3 31 px 20 32 px 16 33 py 3 34 py 6 m1 6000 0.4 8016 0.2 11023 0.2 29000 0.2 m2 92238 0.98 92235 0.02 m3 1001 1 sdef erg fcel d1 x fcel d11 y fcel d13 z fcel d15 cel d6 rad fcel d17 ext fcel d19 pos fcel d21 axs fcel d23 ds1 s d2 d3 d4 d5 sp2 -2 1.2 sp3 -2 1.3 sp4 -2 1.4 sp5 -2 1.42 si6 s d7 d8 d9 d10 sp6 0.65 0.2 0.1 0.05 si7 l 2:4:8 sp7 1 si8 l 3:5(0 0 0):11 3:5(1 0 0):11 3:5(0 1 0):11 3:5(1 1 0):11 3:5(0 2 0):11 3:5(0 3 0):11 3:5(1 3 0):11 sp8 1 2 3 4 5 6 7 si9 l 3:5(1 2 0):13 sp9 1 si10 l 3:5(1 2 0):15 sp10 1 ds11 s d12 0 0 d25 si12 -4 4 sp12 0 1
```

```
ds13 s d14 0 0 d26 si14 -3 3 sp14 0 1 ds15 s d16 0 0 d16 si16 -60 60 sp16 0 1 ds17 s 0 d18 d18 0 si18 0 3 sp18 -21 1 ds19 s 0 d20 d20 0 si20 -60 60 sp20 0 1 ds21 s 0 d22 d22 0 si22 l 10 5 0 sp22 1 ds23 s 0 d24 d24 0 si24 l 0 0 1 sp24 1 si25 16 20 sp25 0 1 si26 3 6 sp26 0 1 f2:n 1 e2 0.1 1 20 f6:n 2 4 6 8 3 5 7 9 11 13 15 sd6 1 1 1 1 1 1 1 1 1 1 1 print nps 1E6 c tallies FMESH14:N GEOM= xyz ORIGIN= -50.0 -20.0 -60.0 IMESH= 50.0 IINTS= 200 JMESH= 20.0 JINTS= 80 KMESH= 60.0 KINTS= 1 OUT=NONE FMESH24:N GEOM= xyz ORIGIN= -50.0 -20.0 -60.0 IMESH= 50.0 IINTS= 200 JMESH= 20.0 JINTS= 80 KMESH= 60.0 KINTS= 1 TYPE=SOURCE OUT=NONE FMESH34:N GEOM= xyz ORIGIN= -50.0 -20.0 -60.0 IMESH= 50.0 IINTS= 200 JMESH= 20.0 JINTS= 1 KMESH= 60.0 KINTS= 200 TYPE=SOURCE OUT=NONE
```

Below is a plot of the flux in the XY plane.

<!-- image -->

Below is a plot of the source in the XY plane.

<!-- image -->

Below is a plot of the source in the XZ plane.

<!-- image -->

Listing 4.20: MCNP6 Plotting Commands

```
fmesh 14 basis 1 0 0 0 1 0 fmesh 24 fmesh 34 basis 1 0 0 0 0 1 file end end
```
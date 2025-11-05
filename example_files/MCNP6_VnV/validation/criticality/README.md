# MCNP6 Criticality Validation

The MCNP Criticality Validation Suite is a collection of 31 benchmark models taken from the International Handbook of Evaluation Criticality Safety Benchmark Experiments. MCNP6-calculated Keff values can be compared to benchmark measurements. These benchmark models include systems with fast, intermediate, and thermal spectra; light, heavy, or no reflectors; lattices of fuel pins; and liquid solutions. This modest suite of benchmarks is meant to be used and tested frequently when changes to the nuclear data or code are made.

See Reference: R. Mosteller, "Comparison of Results from the MCNP Criticality Validation Suite Using ENDF B-VI and Preliminary ENDF B-VII Nuclear Data", International Conference on Nuclear Data for Science and Technology, Santa Fe, Sept 26 - Oct 1 2004. LA-UR-04-6489.

This directory contains this `README.md`, the `experiments` subdirectory, which contains the benchmark MCNP input decks, the `references` subdirectory, which contains reference MCNP calculations for various nuclear data libraries and MCNP code versions, and `VnV.py`, which is the Python script used to run, process, and analyze results.

Informational table of the 31 cases from ICSBEP Handbook
--------------------------------------------------------
Name         |  Spectrum     |  ICSBEP Name            |  Description
------------ | ------------- | ----------------------- | ------------
Jezebel-233  |	Fast 	     |	U233-MET-FAST-001      |	Bare sphere of 233U
Flattop-23   |	Fast 	     |	U233-MET-FAST-006      |	Sphere of 233U reflected by normal U
U233-MF-05   |	Fast 	     |	U233-MET-FAST-005,c2   |	Sphere of 233U reflected by beryllium
Falstaff-1   |	Intermediate |	U233-SOL-INTER-001,c1  |	Sphere of uranyl fluoride solution enriched in 233U
SB-2 1/2     |	Thermal      |	U233-COMP-THERM-001,c3 |	Lattice of 233U fuel pins in water
ORNL-11	     |	Thermal      |	U233-SOL-THERM-008     |	Large sphere of uranyl nitrate solution enriched in 233U
Godiva 	     |	Fast 	     |	HEU-MET-FAST-001       |	Bare HEU sphere
Tinkertoy-2  |	Fast 	     |	HEU-MET-FAST-026,c21   |	3 x 3 x 3 array of HEU cylinders in paraffin box
Flattop-25   |	Fast 	     |	HEU-MET-FAST-028       |	HEU sphere reflected by normal U
Godiver      |	Fast 	     |	HEU-MET-FAST-004       |	HEU sphere reflected by water
Zeus-2 	     |	Intermediate |	HEU-MET-INTER-006,c2   |	HEU platters moderated by graphite and reflected by copper
UH3 	     |	Intermediate |	HEU-COMP-INTER-003,c6  |	UH3 cylinders reflected by depleted uranium
SB-5 	     |	Thermal	     |	U233-COMP-THERM-001,c6 |	Lattice of HEU fuel pins in water, with blanket of ThO2 pins
ORNL-10      |	Thermal	     |	HEU-SOL-THERM-032      |	Large sphere of HEU nitrate solution
IEU-MF-03    |	Fast 	     |	IEU-MET-FAST-003       |	Bare sphere of IEU (36 wt.%)
BIG TEN	     |	Fast 	     |	IEU-MET-FAST-007       |	Cylinder of IEU (10 wt.%) reflected by normal uranium
IEU-MF-04    |	Fast 	     |	IEU-MET-FAST-004       | 	Sphere of IEU (36 wt.%) reflected by graphite
Zebra-8H     |	Intermediate |	MIX-MET-FAST-008,c7    |	IEU (37.5 wt.%) reflected by normal U and steel
IEU-CT-02    |	Thermal      |	IEU-COMP-THERM-002,c3  |	Lattice of IEU (17 wt.%) fuel rods in water
STACY-36     |	Thermal      |	LEU-SOL-THERM-007,c36  |	Cylinder of IEU (9.97 wt.%) uranyl nitrate solution
B&W XI-2     |	Thermal      |	LEU-COMP-THERM-008,c2  |	Large lattice of LEU (2.46 wt.%) fuel pins in borated water
LEU-ST-02    |	Thermal      |	LEU-SOL-THERM-002,c2   |	Sphere of LEU (4.9 wt.%) uranyl fluoride solution
Jezebel      |	Fast 	     |	PU-MET-FAST-001        |	Bare sphere of plutonium
Jezebel-240  |	Fast 	     |	PU-MET-FAST-002        |	Bare sphere of plutonium (20.1 at.% 240Pu)
Pu Buttons   |	Fast 	     |	PU-MET-FAST-003,c103   |	3 x 3 x 3 array of small cylinders of plutonium
Flattop-Pu   |	Fast 	     |	PU-MET-FAST-006        |	Plutonium sphere reflected by normal U
THOR 	     |	Fast 	     |	PU-MET-FAST-008        |	Plutonium sphere reflected by thorium
PU-MF-11     |	Fast 	     |	PU-MET-FAST-011        |	Plutonium sphere reflected by water
HISS/HPG     |	Intermediate |	PU-COMP-INTER-001      |	Infinite, homog. mixture of plutonium, hydrogen, & graphite
PNL-33 	     |	Thermal	     |	MIX-COMP-THERM-002,c4  |	Lattice of mixed-oxide fuel pins in borated water
PNL-2 	     |	Thermal      |	PU-SOL-THERM-021,c3    |	Sphere of plutonium nitrate solution

This benchmark suite has available material card descriptions for the following nuclear data libraries:
* ENDF/B-VI.6
* ENDF/B-VII.0
* ENDF/B-VII.1
* ENDF/B-VIII.0
* JEFF3.3
The user is responsible for ensuring that the `DATAPATH` environment variable includes the desired nuclear data and associated cross-section directory (`xsdir`) file(s).

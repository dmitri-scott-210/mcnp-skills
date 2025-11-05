# MCNP6 Pulsed Sphere Time-Dependent Transport Validation 

The Pulsed Sphere Time-Dependent Transport Validation Suite is a collection of
12 calculations using spherical targets of 6 materials bombarded with a
centered, nominal 14-MeV neutron source. The neutron time-of-flight values
calculated by MCNP6 are compared with experimental values measured during the
Livermore Pulsed Sphere Program.

Each sphere material is simulated with both a simplistic legacy constructive
solid geometry (CSG) modeling only the pulsed sphere and a more detailed CSG
additionally modeling the neutron source and geometry outside of the sphere. As
such, input files follow the naming convention: `ps_{CSG Type}_{Material}.inp`.

This directory contains the `experiments` subdirectory, which contains a folder
for each calculation with the input file, experimental values, and a
`description.json` file with metadata about the calculation; this `README.md`
file; and a Python script to run, process, and analyze results.

See references:  
C. Wong et al., "Livermore Pulsed Sphere Program: Program Summary
through July 1971," UCRL-51144 Rev. 1, Lawrence Livermore National Laboratory
(1972). Available: <https://mcnp.lanl.gov/pdf_files/ucrl-51144.pdf>

J. A. Bucholz et al., "Improving the LLNL Pulsed Sphere Experiments
Database and MCNP Models," Proc. of the American Nucl. Soc. Annual Meet., June
1–5, 2003, San Diego, CA. Available:
<https://mcnp.lanl.gov/pdf_files/la-ur-03-0609.pdf>

J. A. Bucholz & S. C. Frankle, "Improving the LLNL Pulsed Sphere Experiments
Database and MCNP Models," LA-UR-03-3537, Los Alamos National Laboratory
(2003). Available:
<https://permalink.lanl.gov/object/tr?what=info:lanl-repo/lareport/LA-UR-03-3537>

J. A. Kulesza & R. L. Martz, "Evaluation of Pulsed Sphere Time-of-Flight
and Neutron Attenuation Experimental Benchmarks Using MCNP6's Unstructured Mesh
Capabilities," Nuclear Technology, 195:1, 44-54 (2016), DOI:10.13182/NT15-121.
Available: <https://doi.org/10.13182/NT15-121>.

J. D. Court, R. C. Brockhoff, and J. S. Hendricks, "Lawrence Livermore
Pulsed Sphere Benchmark Analysis of MCNP ENDF/B-VI," LA-12885, Los Alamos
National Laboratory (1994). Available:
<https://mcnp.lanl.gov/pdf_files/la-12885.pdf>

R. D. Mosteller, S. C. Frankle, and P. G. Young, “Data Testing of ENDF/B-VI
with MCNP: Critical Experiments, Thermal-Reactor Lattices, and Time-of-Flight
Measurements,” LA-UR-96-2143, Los Alamos National Laboratory (1996).

S. C. Frankle, "Possible Impact of Additional Collimators on the LLNL Pulsed
Sphere Experiments (U)," LA-UR-05-5877, Los Alamos National Laboratory (2005).

S. C. Frankle, "LLNL Pulsed Sphere Measurements and Detector Response Functions
(U)," LA-UR-05-5878, Los Alamos National Laboratory (2005).

S. C. Frankle, "README file for Running a LLNL Pulsed-Sphere
Benchmark," LA-UR-05-5879, Los Alamos National Laboratory (2005).

A note on data representation in `description.json` files: experimental data
are reported as an average value at a flight time and MCNP results are reported
as an average value with flight-time bin-edge values. Additionally, MCNP
reports the value of the bin from negative infinity to the lowest specified bin
edge. For consistent comparison, a value of zero is assigned to this first MCNP
bin and a value of zero is prepended to the list of experimental values.
Consequently, the i-th experimental flight time corresponds to the i+1-th
average value with the final experimental flight time being artificial and
neglected. This representation is accounted for during data processing.

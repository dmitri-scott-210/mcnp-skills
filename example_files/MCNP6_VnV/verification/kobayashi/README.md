# MCNP6 Kobayashi verification

This problem set contains 6 benchmarks that were designed by Kobayashi
[1] to test how 3D discrete ordinates codes deal with ray effects in problems
with void and shield regions. The problem set contains 3 distinct geometries
that are each composed of a cubic monoenergetic, isotropic neutron source
bounded by void and shield material regions. In each problem, the shield
material is either a pure absorber (designated “i”) or one in which the
scattering cross section is half of the total cross section (designated “ii”).

The first problem is a nested set of the three cubic regions. The second
problem contains a central cubic neutron source, a rectangular void duct along
one axis adjacent to the neutron source, and shield material encompassing them.
The third problem contains a central cubic neutron source, a rectangular void
duct with two 90-degree bends, and shield material encompassing them.

In discrete ordinates calculations, an octant of the geometry is simulated with
reflective boundary conditions for computational efficiency. In MCNP
calculations, however, the entire geometry is simulated. Despite the symmetry
of each problem, point detector tallies produce erroneous results when using
reflective boundary conditions.

Prior work by Kulesza et al. [2] investigated this problem set using continuous
energy (CE) and multigroup nuclear data, constructive solid geometry (CSG) and
unstructured mesh (UM) treatment, and importance splitting turned on or off.
This problem set, however, contains only the CE nuclear data, CSG treatment,
and importance splitting turned on, with importance splitting parameters given
in [3].

This problem set uses fictitious nuclear data files provided in the "MCNP_DATA"
folder. "99001.00c" is the pure absorber and "99002.00c" is such that the
scattering cross section is half of the total cross section. Reference [3]
gives a more detailed discussion.

The "MCNP_DATA" directory contains several XSDIR files that follow the naming
and format conventions required by different MCNP versions.

[1] K. Kobayashi, N. Sugimura, and Y. Nagaya, "3D radiation transport benchmark
    problems and results for simple geometries with void region",
    Progress in Nuclear Energy, vol. 39, no. 2, pg. 119-144 (2001).
    DOI: 10.1016/S0149-1970(01)00007-5
[2] J. A. Kulesza and R. L. Martz, "Evaluation of the Kobayashi Analytical
    Benchmark Using MCNP6's Unstructured Mesh Capabilities", Nuclear Technology,
    vo. 195, no. 1, pg. 55-70, (2016). DOI: 10.13182/NT15-122
[3] B. E. Toth And F. B. Brown, "MCNP5 Benchmark Calculations For 3-D Radiation
    Transport In Simple Geometries With Void Regions", Los Alamos National
    Laboratory Report Number LA-UR-03-5974, Aug. 2003.
    URL: http://permalink.lanl.gov/object/tr?what=info:lanl-repo/lareport/LA-UR-03-5974
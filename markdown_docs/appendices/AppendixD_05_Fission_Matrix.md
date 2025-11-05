---
title: "Appendix D.5 - Fission Matrix Format"
chapter: "D.5"
source_pdf: "mcnp631_theory_user-manual/appendecies/D.5_Fission_Matrix_Format.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## D.5 Fission Matrix Format

The MCNP fission matrix is added to the runtape whenever the KOPTS
option FMAT is set to yes . The contents of the /results/fission \_
matrix group in the restart file [§D.2] are:

```
fission _ matrix................ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .(group) data............ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .(dataset) delta _ xyz.... . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .(dataset) indices.................. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .(dataset) indptr................. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .(dataset) n..... . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .(dataset) n _ xyz. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . (dataset) origin................. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .(dataset)
```

The variables indptr , indices , and data represent a 0-indexed
compressed-sparse-row (CSR) matrix, which can be readily loaded by many
sparse linear algebra packages. As an example, the Python [347] code in
Listing D.12 can be used to load a fission matrix into the SciPy [348]
sparse capability. The eigenvalues of the matrix can be computed using
scipy.sparse.linalg.eigs .

```
1 #!/usr/bin/env python3 2 3 import h5py 4 import scipy.sparse as sparse 5 import scipy.sparse.linalg as sla 6 7 SUPPORTED _ RUNTAPE = [1, 0, 0] 8 9 10 def extract _ fmat(runtape): 11 """Returns the last saved fission matrix as a scipy.sparse.csr _ matrix""" 12 with h5py.File(runtape, "r") as handle: 13 # Check runtape version 14 version _ file = handle["config _ control"].attrs["version _ file"] 15 if any(SUPPORTED _ RUNTAPE != version _ file): 16 print("Possibly incompatible runtape detected.") 17 18 fmat = handle["results/fission _ matrix"] 19 20 n = fmat["n"][()] 21 indices = fmat["indices"][:] 22 indptr = fmat["indptr"][:] 23 data = fmat["data"][:] 24 25 n _ xyz = fmat["n _ xyz"][:] 26 delta _ xyz = fmat["delta _ xyz"][:] 27 origin = fmat["origin"][:] 28 29 return sparse.csr _ matrix((data, indices, indptr), shape=(n, n)), n _ xyz, delta _ xyz, origin
```

Listing D.12: Fission Matrix HDF5 Reader

The remaining variables in the group are used for converting the
eigenvectors into a representation that has meaning in 3D. The
eigenvectors, as computed from the fission matrix, are unrolled in a
column-major way with x changing first. As NumPy [349] is row major by
default, the easiest way to generate a 3D array indexed by [ x, y, z ]
is to use the approach in Listing D.13. The origin variable is the
bottom-left-rear coordinate of the mesh, and delta \_ xyz is the spacing
of the mesh in x , y , and z , in units of centimeters.

```
31 mat, n _ xyz, delta _ xyz, origin = extract _ fmat("runtape.h5") 32 33 eigenvalues, eigenvectors = sla.eigs(mat) 34 35 # Reshape first eigenvector into 3D object 36 eigenvector = eigenvectors[:, 0].reshape(n _ xyz[2], n _ xyz[1], n _ xyz[0]).transpose()
```

Listing D.13: Eigenvector to 3D Mesh

Finally, the eigenfunctions can be scaled by arbitrary coefficients.
While it is common to interpret the fundamental eigenvector as
everywhere-positive, some solvers may return an eigenvector that is
everywherenegative. It is safe to negate this eigenvector to make it
positive. For more discussion on the interpretation of the results, see
[350, 351].
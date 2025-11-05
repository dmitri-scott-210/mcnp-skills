---
title: "Appendix A - Mesh-Based WWINP, WWOUT, and WWONE File Format"
chapter: "A"
source_pdf: "mcnp631_theory_user-manual/appendecies/A_Mesh-Based_WWINP,_WWOUT,_and_WWONE_File_Format.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## Appendix A

## Mesh-Based WWINP, WWOUT, and WWONE File Format

The mesh-based weight-window input file WWINP and the mesh-based weight-
window output files WWOUT and WWONE are ASCII files with a common
format. The files consist of three blocks:

1. Block 1 contains the header information, energy and time group numbers, and basic mesh information.
2. Block 2 contains the mesh geometry.
3. Block 3 contains the energy and time group boundaries and lower weight-window bounds.

The three-dimensional array of fine mesh cells is stored by assigning an
index number to each cell. The three dimensions are ( x, y, z ) for
rectangular meshes, ( r, z, θ ) for cylindrical meshes, and ( r, ϕ, θ )
for spherical meshes. These may be indexed as [ i, j, k ] with a total
of I , J , K meshes in each coordinate direction. The assignment of mesh
cells is illustrated in Fig. A.1 for an ( x, y, z ) mesh. The cell index
number is related to the fine mesh number in each coordinate direction
through the formula

<!-- formula-not-decoded -->

Figure A.1: Superimposed mesh cell indexing.

<!-- image -->

Table A.1 presents the file format using generic variables. Table A.2
describes the variables and gives the equivalent variables from the
WWINP, WWOUT, and WWONE files. A description of the variables follows.

Table A.1: Format of the Mesh-Based WWINP, WWOUT and WWONE Files

|   Block | Format         | Variable List                                    |
|---------|----------------|--------------------------------------------------|
|       1 | 4i10, 20x, a19 | if iv ni nr probid                               |
|       1 | 7i10           | nt(1) ... nt(ni) [if iv=2]                       |
|       1 | 7i10           | ne(1) ... ne(ni)                                 |
|       1 | 6g13.5         | nfx nfy nfz x0 y0 z0                             |
|       1 | 6g13.5         | ncx ncy ncz nwg [if nr=10]                       |
|       1 | 6g13.5         | ncx ncy ncz x1 y1 z1 [if nr=16]                  |
|       1 | 6g13.5         | x2 y2 z2 nwg [if nr=16]                          |
|       2 | 6g13.5         | x0 (qx(i), px(i), sx(i), i=1,ncx)                |
|       2 | 6g13.5         | y0 (qy(i), py(i), sy(i), i=1,ncy)                |
|       2 | 6g13.5         | z0 (qz(i), pz(i), sz(i), i=1,ncz)                |
|       3 | 6g13.5         | t(i,1) ... t(i,nt(i)) [if nt(i)>1]               |
|       3 | 6g13.5         | e(i,1) ... e(i,ne(i))                            |
|       3 | 6g13.5         | (((w(i,j,k,l,1) j=1,nft), k=1,ne(i)), l=1,nt(i)) |

Table A.2: Correspondence of Variable Names

| WWINP                         | WWOUT / WWONE                 | DESCRIPTION                           |
|-------------------------------|-------------------------------|---------------------------------------|
| ip                            | ip                            | Particle type                         |
| ic                            | ic                            | Mesh cell index                       |
| ie                            | ie                            | Energy index                          |
| it                            | it                            | Time index                            |
| ia                            | ia                            | Angle index (multigroup calculations) |
| im                            | im                            | Multitasking index                    |
| NWGM                          | NWGMA                         | Length of WGM/WGMA                    |
| NWWM                          | NWWMA                         | Total number of fine meshes           |
| MWWTF( ip )                   | MWWTG( ip )                   | Time bins                             |
| NWW( ip )                     | NGWW( ip )                    | Energy bins                           |
| WWM(26)                       | WWMA(26)                      | Geometry description                  |
| WGM( i )                      | WGMA( i )                     | Geometry boundaries, fine meshes      |
| WWE1( ip , ie )               | WWGE( ip , ie )               | Energy bounds                         |
| WWT1( ip , it )               | WWGT( ip , it )               | Time bounds                           |
| WWF( ip , ic , ie , it , ia ) | WWFA( ip , ic , ie , it , im) | Weight-window lower bounds            |

| if                | File type. Only 1 is supported. Unused. (MCNP name: if )                                                                                                                                    |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| iv                | Time-dependent windows flag (1 / 2 = no / yes) (MCNP name: iv )                                                                                                                             |
| ni                | Number of particle types (MCNP name: NI )                                                                                                                                                   |
| nr                | = 10 / 16 / 16 for rectangular / cylindrical / spherical (MCNP name: NR ) = number of words to describe mesh                                                                                |
| probid            | Problem identification description (MCNP name: probid )                                                                                                                                     |
| i                 | Particle type (MCNP name: KP )                                                                                                                                                              |
| nt(i)             | Number of time bins for particle type i (MCNP name: NWW(KP) )                                                                                                                               |
| ne(i)             | Number of energy bins for particle type i (MCNP name: NGWW(KP) )                                                                                                                            |
| nfx,nfy,nfz       | Total number of fine ( x, y, z ) , ( r, z, θ ) , or ( r, ϕ, θ ) mesh bins (MCNP name: WWM(1:3) )                                                                                            |
| x0,y0,z0          | Corner of ( x, y, z ) Cartesian geometry, bottom center of ( r, z, θ ) cylindrical geometry, or center of ( r, ϕ, θ ) spherical geometry (MCNP name: WWM(4:6) )                             |
| ncx,ncy,ncz       | Number of coarse ( x, y, z ) , ( r, z, θ ) , or ( r, ϕ, θ ) mesh bins (MCNP name: WWM(7:9) )                                                                                                |
| x1,y1,z1          | Vector from ( x 0 , y 0 , z 0 ) to ( x 1 , y 1 , z 1 ) defines ( r, z, θ ) cylinder or ( r, ϕ, θ ) polar axis (MCNP name: WWN(10:12) )                                                      |
| x2,y2,z2          | Vector from ( x 0 , y 0 , z 0 ) to ( x 2 , y 2 , z 2 ) defines ( r, z, θ ) cylinder or ( r, ϕ, θ ) azimuthal axis (MCNP name: WWN(13:15) )                                                  |
| nwg               | Geometry type 1, 2, 3 = ( x, y, z ) , ( r, z, θ ) , ( r, ϕ, θ ) (MCNP name: WWM(NR) )                                                                                                       |
| px(i),py(i),pz(i) | Coarse mesh coordinates for ( x, y, z ) , ( r, z, θ ) , or ( r, ϕ, θ ) (MCNP name: WGM(k) )                                                                                                 |
| qx(i),qy(i),qz(i) | Fine mesh ratio (presently = 1 always) in each coarse mesh for ( x, y, z ) , ( r, z, θ ) , or ( r, ϕ, θ ) (MCNP name: WGM(k) )                                                              |
| sx(i),sy(i),sz(i) | Number of fine meshes in each coarse mesh for ( x, y, z ) , ( r, z, θ ) , or ( r, ϕ, θ ) (MCNP name: WGM(k) )                                                                               |
| t(i,j)            | Upper time bounds for particle i , bin j (given only if nt(i) > 1 ) (MCNP name: WWT1(KP,j) )                                                                                                |
| e(i,j)            | Upper energy bounds for particle i , bin j (MCNP name: WWE1(KP,j) )                                                                                                                         |
| nft               | Total number of fine meshes ( nfx × nfy × nfz ) (MCNP name: NWWM )                                                                                                                          |
| w(i,j,k,l,1)      | Weight-window lower bounds. These are written in blocks of j = 1 : NWWMA geometry meshes for each energy k = 1 , NGWW(KP) and for each time l = 1 , MWWTG(KP) (MCNP name: WWF(KP,j,k,l,1) ) |

## A.1 Example Mesh Description and Files

Input file mesh description:

```
1 mesh geom=rzt ref= -4.2419 4.2419 -2 2 origin 0 0 -9.0001 3 imesh 3.02 6.0001 4 iints 3 5 5 jmesh 8.008 14.002 6 jints 4 3 7 kmesh .25 .50 .75 1 8 kints 2 1 2 3
```

Resultant WWINP, WWOUT and WWONE file:

<!-- image -->

| 1       | 1      | 1       | 16      |         |         |
|---------|--------|---------|---------|---------|---------|
| 1       |        |         |         |         |         |
| 6.0000  | 7.0000 | 8.0000  | 0.0000  | 0.0000  | -9.0001 |
| 2.0000  | 2.0000 | 4.0000  | 0.0000  | 0.0000  | 5.0001  |
| 6.0001  | 0.0000 | -9.0001 | 2.0000  |         |         |
| 0.0000  | 3.0000 | 3.0200  | 1.0000  | 5.0000  | 6.0001  |
| 1.0000  |        |         |         |         |         |
| 0.0000  | 4.0000 | 8.0080  | 1.0000  | 3.0000  | 14.002  |
| 1.0000  |        |         |         |         |         |
| 0.0000  | 2.0000 | 0.25000 | 1.0000  | 1.0000  | 0.50000 |
| 1.0000  | 2.0000 | 0.75000 | 1.0000  | 3.0000  | 1.0000  |
| 1.0000  |        |         |         |         |         |
| 100.00  |        |         |         |         |         |
| 0.0000  | 0.0000 | 1.1924  | 0.48566 | 0.60746 | 1.0653  |
| 0.10454 | 0.9993 | 0.11065 | 0.16738 | 0.37556 | 0.94980 |
| ...     |        |         |         |         |         |

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
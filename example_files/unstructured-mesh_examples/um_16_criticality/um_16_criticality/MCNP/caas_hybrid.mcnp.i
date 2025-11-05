caas_hybrid
c
c Attila calculation "caas_hybrid"
c Calculation for CAAS MCNP Hybrid CSG-UM
c       
c -------------------------- Input Information ------------------------------ 80
c Attila GUI created MCNP6 Input
c Attila Version 10.2.0.5512-oem1
c Input File Creation Date: Tue Sep 21 10:31:29 2021
c RxMesher version          : 1.0.0
c Simmetrix MeshSim version : 14.0-200321
c Global mesh size          : 2.5 m
c Generated                 : 2021-09-21T10:29:14-06:00
c Solid Geometry :
c   Filename     : caas_hybrid.x_t
c   Last changed : 2021-09-21T10:26:54-06:00
c   MD5 checksum : aacc11bc6299dc6d43ba345b87f87206
c Note: RTT Mesh has added cell flags for MCNP Abaqus part and pseudo-cell.
c Associated Abaqus Unstructured Mesh :
c   Filename     : caas_hybrid.abaq
c   Generated    : 2021-09-21T10:31:29
c   MD5 checksum : ce8b9d4a20dae86ac42d2d49e03e40d9
c n_points = 1118
c n_sides  = 2198
c n_cells  = 2775
c Mesh Bounding Box (cm):
c  x: -1300.000 - 1900.000
c  y: -1900.000 -  250.000
c  z:  -50.000 -  310.000
c
c Number of Attila Regions                 : 9
c Number of Abaqus Parts/MCNP Pseudo-Cells : 9
c Number of Materials                      : 2
c
c  Mesh Region/Pseudo-Cell Information
c   Attila Region #    : 1
c   Attila Region Name : "walls"
c   Abaqus Part #      : 1
c   Abaqus Part Name   : "walls"
c   MCNP Pseudo-cell # : 1
c   Material           : "concrete_1"
c    MCNP Material     : m1
c    Density           : 0.0764 atoms/b-cm
c   Mesh Data
c     Meshed Volume    : 5.015e+08 cm**3
c     # Cells          : 1477
c     % of Total Cells : 53.23% 
c
c   Attila Region #    : 2
c   Attila Region Name : "labwall"
c   Abaqus Part #      : 2
c   Abaqus Part Name   : "labwall"
c   MCNP Pseudo-cell # : 2
c   Material           : "concrete_1"
c    MCNP Material     : m1
c    Density           : 0.0764 atoms/b-cm
c   Mesh Data
c     Meshed Volume    : 1.35e+07 cm**3
c     # Cells          : 42
c     % of Total Cells : 1.51% 
c
c   Attila Region #    : 3
c   Attila Region Name : "wall1"
c   Abaqus Part #      : 3
c   Abaqus Part Name   : "wall1"
c   MCNP Pseudo-cell # : 3
c   Material           : "concrete_1"
c    MCNP Material     : m1
c    Density           : 0.0764 atoms/b-cm
c   Mesh Data
c     Meshed Volume    : 1.575e+07 cm**3
c     # Cells          : 59
c     % of Total Cells : 2.13% 
c
c   Attila Region #    : 4
c   Attila Region Name : "wall2"
c   Abaqus Part #      : 4
c   Abaqus Part Name   : "wall2"
c   MCNP Pseudo-cell # : 4
c   Material           : "concrete_1"
c    MCNP Material     : m1
c    Density           : 0.0764 atoms/b-cm
c   Mesh Data
c     Meshed Volume    : 1.35e+07 cm**3
c     # Cells          : 42
c     % of Total Cells : 1.51% 
c
c   Attila Region #    : 5
c   Attila Region Name : "wall3"
c   Abaqus Part #      : 5
c   Abaqus Part Name   : "wall3"
c   MCNP Pseudo-cell # : 5
c   Material           : "concrete_1"
c    MCNP Material     : m1
c    Density           : 0.0764 atoms/b-cm
c   Mesh Data
c     Meshed Volume    : 1.35e+07 cm**3
c     # Cells          : 42
c     % of Total Cells : 1.51% 
c
c   Attila Region #    : 6
c   Attila Region Name : "wall4"
c   Abaqus Part #      : 6
c   Abaqus Part Name   : "wall4"
c   MCNP Pseudo-cell # : 6
c   Material           : "concrete_1"
c    MCNP Material     : m1
c    Density           : 0.0764 atoms/b-cm
c   Mesh Data
c     Meshed Volume    : 1.35e+07 cm**3
c     # Cells          : 42
c     % of Total Cells : 1.51% 
c
c   Attila Region #    : 7
c   Attila Region Name : "wall5"
c   Abaqus Part #      : 7
c   Abaqus Part Name   : "wall5"
c   MCNP Pseudo-cell # : 7
c   Material           : "concrete_1"
c    MCNP Material     : m1
c    Density           : 0.0764 atoms/b-cm
c   Mesh Data
c     Meshed Volume    : 2.775e+07 cm**3
c     # Cells          : 90
c     % of Total Cells : 3.24% 
c
c   Attila Region #    : 8
c   Attila Region Name : "wall6"
c   Abaqus Part #      : 8
c   Abaqus Part Name   : "wall6"
c   MCNP Pseudo-cell # : 8
c   Material           : "concrete_1"
c    MCNP Material     : m1
c    Density           : 0.0764 atoms/b-cm
c   Mesh Data
c     Meshed Volume    : 1.35e+07 cm**3
c     # Cells          : 42
c     % of Total Cells : 1.51% 
c
c   Attila Region #    : 9
c   Attila Region Name : "ceiling"
c   Abaqus Part #      : 9
c   Abaqus Part Name   : "ceiling"
c   MCNP Pseudo-cell # : 9
c   Material           : "concrete_1"
c    MCNP Material     : m1
c    Density           : 0.0764 atoms/b-cm
c   Mesh Data
c     Meshed Volume    : 6.88e+07 cm**3
c     # Cells          : 939
c     % of Total Cells : 33.84% 
c
c ------------------------ End Input Information ---------------------------- 80
c
c ----------------------------- Cell Cards ---------------------------------- 80
1     1     0.0764       0                               u=1
2     1     0.0764       0                               u=1
3     1     0.0764       0                               u=1
4     1     0.0764       0                               u=1
5     1     0.0764       0                               u=1
6     1     0.0764       0                               u=1
7     1     0.0764       0                               u=1
8     1     0.0764       0                               u=1
9     1     0.0764       0                               u=1
10    2     4.8333e-05   0                               u=1 $ background
11    2     4.8333e-05   100 -101 102 -103 104 -105   fill=1 $ fill cell
12    0                  (-100:101:-102:103:-104:105)
c --------------------------- End Cell Cards -------------------------------- 80

c ---------------------------- Surface Cards -------------------------------- 80
c
100 px -1300.5
101 px 1900.5
102 py -1900.5
103 py 250.5
104 pz -50.5
105 pz 310.5
c -------------------------- End Surface Cards ------------------------------ 80

c ----------------------------- Data Cards ---------------------------------- 80
c Embedded Geometry Specification
embed1 meshgeo=abaqus mgeoin=caas_hybrid.abaq
       meeout=caas_hybrid.mcnp.eeout
       filetype=ascii
       background=10
       matcell= 1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9
c
c Materials
c
c  Material 1: "concrete_1"
c  Constituents (atom %):
c H-1001 (0.00842) O-8016 (0.04423) Al-13027 (0.00252) Si-14028 (0.014691)
c Si-14029 (0.000718176) Si-14030 (0.000460866) Na-11023 (0.00105)
c Ca-20040 (0.00284037) Ca-20042 (1.89571e-05) Ca-20043 (3.9555e-06)
c Ca-20044 (6.11198e-05) Ca-20046 (1.172e-07) Ca-20048 (5.4791e-06)
c Fe-26054 (4.1788e-05) Fe-26056 (0.000632003) Fe-26057 (1.4347e-05)
c Fe-26058 (1.862e-06) K-19039 (0.000643481) K-19040 (8.073e-08)
c K-19041 (4.64384e-05)
m1  1001 0.00842 8016 0.04423 13027 0.00252 14028 0.014691 14029 &
0.000718176 14030 0.000460866 11023 0.00105 20040 0.00284037 20042 &
1.89571e-05 20043 3.9555e-06 20044 6.11198e-05 20046 1.172e-07 20048 &
5.4791e-06 26054 4.1788e-05 26056 0.000632003 26057 1.4347e-05 26058 &
1.862e-06 19039 0.000643481 19040 8.073e-08 19041 4.64384e-05 
c
c  Material 2: "air_2"
c  Constituents (atom %):
c H-1001 (1.7404e-10) H-1002 (1.3065e-14) He-2003 (8.354e-16)
c He-2004 (4.5549e-10) C-6000 (1.11008e-08) N-7014 (3.8981e-05)
c N-7015 (1.3515e-07) O-8016 (9.1205e-06) O-8017 (3.4348e-09)
c Ar-18036 (3.0439e-10) Ar-18038 (5.3915e-11) Ar-18040 (8.0974e-08)
c Kr-36078 (1.7811e-14) Kr-36080 (1.1164e-13) Kr-36082 (5.6154e-13)
c Kr-36083 (5.49985e-13) Kr-36084 (2.69359e-12) Kr-36086 (7.98498e-13)
c Xe-54124 (2.30549e-13)
m2  1001 1.7404e-10 1002 1.3065e-14 2003 8.354e-16 2004 4.5549e-10 6000 &
1.11008e-08 7014 3.8981e-05 7015 1.3515e-07 8016 9.1205e-06 8017 &
3.4348e-09 18036 3.0439e-10 18038 5.3915e-11 18040 8.0974e-08 36078 &
1.7811e-14 36080 1.1164e-13 36082 5.6154e-13 36083 5.49985e-13 36084 &
2.69359e-12 36086 7.98498e-13 54124 2.30549e-13 
c
c Mode (Only n and/or p Currently Accepted)
mode n
c
c Cell Importances
imp:n 1 1 1 1 1 1 1 1 1 1 1 0
c
c Source Definition
sdef [UD]
c
c Histories (or Computer Time Cutoff)
nps 1
c ctme 1
c
c
c Tallies or embee cards
c [UD]
c
c L'Ecuyer 63-bit random number generator (period=9.2E18)
rand gen=2
c
print -85 -86 -87 -98
c
c --------------------------- End Data Cards -------------------------------- 80
c End MCNP Input

Nested Lattice Template - Multi-Level Hierarchy
c =================================================================
c Template for nested lattices (pin → assembly → core)
c Demonstrates 3-level hierarchy
c User must fill in: dimensions, materials, fill patterns
c =================================================================

c =================================================================
c BLOCK 1: Cell Cards
c =================================================================
c --- LEVEL 1: Pin Cell (Universe 1) ---
1    <mat#>  <density>  -1     U=1  IMP:N=1  VOL=<calc>  $ Pin core
2    <mat#>  <density>   1     U=1  IMP:N=1  VOL=<calc>  $ Pin background

c --- LEVEL 2: Assembly Lattice (Universe 10) ---
c    NxN pin lattice
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1
c    Replace FILL=1 with array if multiple pin types

c --- LEVEL 3: Core Lattice (Universe 100) ---
c    MxM assembly lattice
1000 0  -100 101 -102 103 -104 105  U=100  LAT=1  FILL=10  IMP:N=1
c    Replace FILL=10 with array for flux-based grouping:
c    FILL=0:M-1 0:M-1 0:0
c         <list assembly universes by flux zone>

c --- LEVEL 0: Real World ---
10000 0  -10000  FILL=100  IMP:N=1         $ Core
10001 <mat#>  <dens>  10000 -10001  IMP:N=1   $ Reflector
10002 0  10001  IMP:N=0

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
c --- Pin Surfaces (Level 1) ---
1    CZ   <pin_radius>

c --- Assembly Lattice Element (Level 2) ---
10   PX   0.0
11   PX   <N*pin_pitch>
12   PY   0.0
13   PY   <N*pin_pitch>
14   PZ   0.0
15   PZ   <height>

c --- Core Lattice Element (Level 3) ---
100  PX   0.0
101  PX   <M*assembly_pitch>
102  PY   0.0
103  PY   <M*assembly_pitch>
104  PZ   <zmin>
105  PZ   <zmax>

c --- Real World Boundaries ---
10000 RPP  <bounds>  or  RCC  <params>
10001 RPP  <bounds>  or  RCC  <params>

c =================================================================
c BLOCK 3: Data Cards
c =================================================================
MODE  N
M<#>  ...
c KCODE  ...  $ Criticality for reactor cores
c KSRC  <x> <y> <z>
F4:N  (1 < 100 < 1000[0:M-1 0:M-1 0:0])  $ All fuel pins
NPS   <#>  or controlled by KCODE
PRINT

c Hierarchy documentation:
c U=0 → U=100 (core) → U=10 (assembly) → U=1 (pin)

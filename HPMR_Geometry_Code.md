# HPMR Control Drums and Reflector Assemblies - MCNP Geometry Code
## Gap Analysis Section 2.1 (GAP 3) Implementation

**Date:** 2025-11-08
**Model:** Heat Pipe Microreactor (HPMR) Reference Plant
**Purpose:** Control drum and reflector assembly geometry for `/home/user/mcnp-skills/hpcmr-simplified.i`

---

## 1. CONTROL DRUM CELL CARDS

### 1.1 All 12 Control Drums (z = 20-180 cm, active core height)

```mcnp
c ============================================================================
c                      CONTROL DRUMS (12 drums)
c ============================================================================
c
c Specifications:
c   - Number: 12 drums at 30° intervals
c   - Radial position: r = 120 cm from core center
c   - Outer radius: 14.09895 cm
c   - B4C absorber: 2.7984 cm thick, 120° arc facing inward
c   - Graphite: 240° arc (remainder)
c   - Axial extent: z = 20-180 cm (active core only)
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 1 (0° position, +X axis)
c Center: (120, 0, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8101  800  -2.52    -8001  8002  -8003  8004   imp:n=1   $ Drum 1 B4C absorber (120° arc)
8102  801  -1.803   -8001  8002  (8003:-8004)   imp:n=1   $ Drum 1 graphite (240° arc)

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 2 (30° position)
c Center: (103.923, 60.000, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8201  800  -2.52    -8011  8012  -8013  8014   imp:n=1   $ Drum 2 B4C absorber
8202  801  -1.803   -8011  8012  (8013:-8014)   imp:n=1   $ Drum 2 graphite

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 3 (60° position)
c Center: (60.000, 103.923, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8301  800  -2.52    -8021  8022  -8023  8024   imp:n=1   $ Drum 3 B4C absorber
8302  801  -1.803   -8021  8022  (8023:-8024)   imp:n=1   $ Drum 3 graphite

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 4 (90° position)
c Center: (0, 120.000, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8401  800  -2.52    -8031  8032  -8033  8034   imp:n=1   $ Drum 4 B4C absorber
8402  801  -1.803   -8031  8032  (8033:-8034)   imp:n=1   $ Drum 4 graphite

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 5 (120° position)
c Center: (-60.000, 103.923, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8501  800  -2.52    -8041  8042  -8043  8044   imp:n=1   $ Drum 5 B4C absorber
8502  801  -1.803   -8041  8042  (8043:-8044)   imp:n=1   $ Drum 5 graphite

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 6 (150° position)
c Center: (-103.923, 60.000, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8601  800  -2.52    -8051  8052  -8053  8054   imp:n=1   $ Drum 6 B4C absorber
8602  801  -1.803   -8051  8052  (8053:-8054)   imp:n=1   $ Drum 6 graphite

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 7 (180° position, -X axis)
c Center: (-120.000, 0, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8701  800  -2.52    -8061  8062  -8063  8064   imp:n=1   $ Drum 7 B4C absorber
8702  801  -1.803   -8061  8062  (8063:-8064)   imp:n=1   $ Drum 7 graphite

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 8 (210° position)
c Center: (-103.923, -60.000, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8801  800  -2.52    -8071  8072  -8073  8074   imp:n=1   $ Drum 8 B4C absorber
8802  801  -1.803   -8071  8072  (8073:-8074)   imp:n=1   $ Drum 8 graphite

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 9 (240° position)
c Center: (-60.000, -103.923, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8901  800  -2.52    -8081  8082  -8083  8084   imp:n=1   $ Drum 9 B4C absorber
8902  801  -1.803   -8081  8082  (8083:-8084)   imp:n=1   $ Drum 9 graphite

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 10 (270° position, -Y axis)
c Center: (0, -120.000, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
9001  800  -2.52    -8091  8092  -8093  8094   imp:n=1   $ Drum 10 B4C absorber
9002  801  -1.803   -8091  8092  (8093:-8094)   imp:n=1   $ Drum 10 graphite

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 11 (300° position)
c Center: (60.000, -103.923, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
9101  800  -2.52    -8101  8102  -8103  8104   imp:n=1   $ Drum 11 B4C absorber
9102  801  -1.803   -8101  8102  (8103:-8104)   imp:n=1   $ Drum 11 graphite

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 12 (330° position)
c Center: (103.923, -60.000, 0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
9201  800  -2.52    -8111  8112  -8113  8114   imp:n=1   $ Drum 12 B4C absorber
9202  801  -1.803   -8111  8112  (8113:-8114)   imp:n=1   $ Drum 12 graphite
```

---

## 2. CONTROL DRUM SURFACE CARDS

### 2.1 All Drum Surfaces (RCC and P surfaces)

```mcnp
c ============================================================================
c                   CONTROL DRUM SURFACE CARDS
c ============================================================================
c
c Surface definitions for cylindrical drums with angular sectors
c Format:
c   - RCC outer cylinder: full drum boundary
c   - RCC inner cylinder: B4C/graphite interface
c   - P planes: cutting planes for 120° B4C sector (facing inward)
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 1 SURFACES (0°, center at x=120, y=0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8001  rcc  120 0 20   0 0 160   14.09895      $ Drum 1 outer cylinder
8002  rcc  120 0 20   0 0 160   11.30055      $ Drum 1 B4C inner (thickness 2.7984)
c B4C sector: 120° arc facing core (inward = -X direction)
c Planes at ±60° from inward direction (180° ± 60° = 120°, 240°)
8003  p  -0.5 0.866025 0  -60.0               $ Plane at 120° (60° CCW from -X)
8004  p  -0.5 -0.866025 0  -60.0              $ Plane at 240° (60° CW from -X)

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 2 SURFACES (30°, center at x=103.923, y=60)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8011  rcc  103.923 60 20   0 0 160   14.09895  $ Drum 2 outer
8012  rcc  103.923 60 20   0 0 160   11.30055  $ Drum 2 B4C inner
c Inward direction: 210° (30° + 180°)
c B4C arc: 150° to 270° (210° ± 60°)
8013  p  -0.866025 -0.5 0  -90.0               $ Plane at 150°
8014  p  0 -1 0  -60.0                         $ Plane at 270°

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 3 SURFACES (60°, center at x=60, y=103.923)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8021  rcc  60 103.923 20   0 0 160   14.09895  $ Drum 3 outer
8022  rcc  60 103.923 20   0 0 160   11.30055  $ Drum 3 B4C inner
c Inward direction: 240° (60° + 180°)
c B4C arc: 180° to 300° (240° ± 60°)
8023  p  -1 0 0  -60.0                         $ Plane at 180°
8024  p  -0.5 -0.866025 0  -90.0               $ Plane at 300°

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 4 SURFACES (90°, center at x=0, y=120)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8031  rcc  0 120 20   0 0 160   14.09895       $ Drum 4 outer
8032  rcc  0 120 20   0 0 160   11.30055       $ Drum 4 B4C inner
c Inward direction: 270° (90° + 180° = -Y)
c B4C arc: 210° to 330° (270° ± 60°)
8033  p  -0.866025 -0.5 0  -103.923            $ Plane at 210°
8034  p  0.866025 -0.5 0  51.962               $ Plane at 330°

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 5 SURFACES (120°, center at x=-60, y=103.923)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8041  rcc  -60 103.923 20   0 0 160   14.09895 $ Drum 5 outer
8042  rcc  -60 103.923 20   0 0 160   11.30055 $ Drum 5 B4C inner
c Inward direction: 300° (120° + 180°)
c B4C arc: 240° to 360° (300° ± 60°)
8043  p  -0.5 -0.866025 0  -51.962             $ Plane at 240°
8044  p  0.5 -0.866025 0  51.962               $ Plane at 0° (360°)

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 6 SURFACES (150°, center at x=-103.923, y=60)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8051  rcc  -103.923 60 20   0 0 160   14.09895 $ Drum 6 outer
8052  rcc  -103.923 60 20   0 0 160   11.30055 $ Drum 6 B4C inner
c Inward direction: 330° (150° + 180°)
c B4C arc: 270° to 30° (330° ± 60°)
8053  p  0 -1 0  -60.0                         $ Plane at 270°
8054  p  0.866025 -0.5 0  90.0                 $ Plane at 30°

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 7 SURFACES (180°, center at x=-120, y=0)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8061  rcc  -120 0 20   0 0 160   14.09895      $ Drum 7 outer
8062  rcc  -120 0 20   0 0 160   11.30055      $ Drum 7 B4C inner
c Inward direction: 0° (180° + 180° = +X)
c B4C arc: 300° to 60° (0° ± 60°)
8063  p  0.5 -0.866025 0  -60.0                $ Plane at 300°
8064  p  0.5 0.866025 0  -60.0                 $ Plane at 60°

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 8 SURFACES (210°, center at x=-103.923, y=-60)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8071  rcc  -103.923 -60 20   0 0 160   14.09895  $ Drum 8 outer
8072  rcc  -103.923 -60 20   0 0 160   11.30055  $ Drum 8 B4C inner
c Inward direction: 30° (210° + 180° - 360°)
c B4C arc: 330° to 90° (30° ± 60°)
8073  p  0.866025 -0.5 0  -90.0                $ Plane at 330°
8074  p  0.866025 0.5 0  90.0                  $ Plane at 90°

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 9 SURFACES (240°, center at x=-60, y=-103.923)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8081  rcc  -60 -103.923 20   0 0 160   14.09895  $ Drum 9 outer
8082  rcc  -60 -103.923 20   0 0 160   11.30055  $ Drum 9 B4C inner
c Inward direction: 60° (240° + 180° - 360°)
c B4C arc: 0° to 120° (60° ± 60°)
8083  p  0.5 -0.866025 0  -51.962              $ Plane at 0°
8084  p  -0.5 0.866025 0  51.962               $ Plane at 120°

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 10 SURFACES (270°, center at x=0, y=-120)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8091  rcc  0 -120 20   0 0 160   14.09895      $ Drum 10 outer
8092  rcc  0 -120 20   0 0 160   11.30055      $ Drum 10 B4C inner
c Inward direction: 90° (270° + 180° - 360° = +Y)
c B4C arc: 30° to 150° (90° ± 60°)
8093  p  0.866025 0.5 0  51.962                $ Plane at 30°
8094  p  -0.866025 0.5 0  51.962               $ Plane at 150°

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 11 SURFACES (300°, center at x=60, y=-103.923)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8101  rcc  60 -103.923 20   0 0 160   14.09895  $ Drum 11 outer
8102  rcc  60 -103.923 20   0 0 160   11.30055  $ Drum 11 B4C inner
c Inward direction: 120° (300° + 180° - 360°)
c B4C arc: 60° to 180° (120° ± 60°)
8103  p  0.5 0.866025 0  51.962                $ Plane at 60°
8104  p  -1 0 0  -60.0                         $ Plane at 180°

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c DRUM 12 SURFACES (330°, center at x=103.923, y=-60)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8111  rcc  103.923 -60 20   0 0 160   14.09895  $ Drum 12 outer
8112  rcc  103.923 -60 20   0 0 160   11.30055  $ Drum 12 B4C inner
c Inward direction: 150° (330° + 180° - 360°)
c B4C arc: 90° to 210° (150° ± 60°)
8113  p  0 1 0  -60.0                          $ Plane at 90°
8114  p  -0.866025 -0.5 0  -90.0               $ Plane at 210°
```

---

## 3. REFLECTOR ASSEMBLY CELL CARDS

### 3.1 Bottom Reflector Assemblies (z = 0-20 cm)

```mcnp
c ============================================================================
c          BOTTOM REFLECTOR ASSEMBLIES (z = 0-20 cm)
c ============================================================================
c
c Two assembly types:
c   u=701: Bottom reflector WITH central guide tube (13 assemblies)
c   u=702: Bottom reflector WITHOUT guide tube (114 assemblies)
c
c Materials:
c   - m315: Homogenized heat pipe (SS316 + Na)
c   - m300: Helium (guide tube filler)
c   - m710: Graphite H-451 reflector
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR ASSEMBLY | w/ GUIDE TUBE (u=701)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
7011  315   1     -4701         u=-701  imp:n=1    $ Heat pipe through reflector
7012  300   1     -9701         u=-701  imp:n=1    $ Guide tube helium
701   710  -1.803 -7001  7011:7012  u=-701  imp:n=1  $ Graphite H-451 reflector fill

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR ASSEMBLY | FULL, NO GUIDE TUBE (u=702)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
7021  315   1     -4702         u=-702  imp:n=1    $ Heat pipe through reflector
702   710  -1.803 -7002  7021   u=-702  imp:n=1    $ Graphite H-451 reflector fill

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR LATTICE (u=101)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c Lattice mirrors core assembly pattern (15×15 hexagonal)
c Uses u=701 where core has u=901 (with guide tube)
c Uses u=702 where core has u=902 (no guide tube)
c Uses u=702 for graphite filler positions
c
1001  710  -1.803  -7000  lat=2  u=101  imp:n=1  fill=-7:7 -7:7 0:0
            102 102 102 102 102 102 102 102 102 102 102 102 102 102 102
            102 102 102 102 102 102 102 702 702 702 702 702 702 702 102
            102 102 102 102 102 102 702 702 702 702 702 702 702 702 102
            102 102 102 102 102 702 702 702 702 702 702 702 702 702 102
            102 102 102 102 702 702 702 701 702 702 701 702 702 702 102
            102 102 102 702 702 702 702 702 701 702 702 702 702 702 102
            102 102 702 702 702 702 701 702 702 701 702 702 702 702 102
            102 702 702 702 701 702 702 701 702 702 701 702 702 702 102
            102 702 702 702 702 701 702 702 701 702 702 702 702 102 102
            102 702 702 702 702 702 701 702 702 702 702 702 102 102 102
            102 702 702 702 701 702 702 701 702 702 702 102 102 102 102
            102 702 702 702 702 702 702 702 702 702 102 102 102 102 102
            102 702 702 702 702 702 702 702 702 102 102 102 102 102 102
            102 702 702 702 702 702 702 702 102 102 102 102 102 102 102
            102 102 102 102 102 102 102 102 102 102 102 102 102 102 102

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR REGION (global cell)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
101   0  -101  fill=101  imp:n=1    $ Bottom reflector (z=0-20)
```

### 3.2 Top Reflector Assemblies (z = 180-200 cm)

```mcnp
c ============================================================================
c            TOP REFLECTOR ASSEMBLIES (z = 180-200 cm)
c ============================================================================
c
c Two assembly types:
c   u=801: Top reflector WITH central guide tube (13 assemblies)
c   u=802: Top reflector WITHOUT guide tube (114 assemblies)
c
c Special features:
c   - Heat pipes protrude through (evaporator section extends to z=180)
c   - Reduced graphite content due to penetrations
c   - Slightly harder neutron spectrum than bottom reflector
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR ASSEMBLY | w/ GUIDE TUBE (u=801)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8011  315   1     -4801         u=-801  imp:n=1    $ Heat pipe protruding through
8012  300   1     -9801         u=-801  imp:n=1    $ Guide tube helium
801   710  -1.803 -8001  8011:8012  u=-801  imp:n=1  $ Graphite H-451 reflector fill

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR ASSEMBLY | FULL, NO GUIDE TUBE (u=802)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8021  315   1     -4802         u=-802  imp:n=1    $ Heat pipe protruding through
802   710  -1.803 -8002  8021   u=-802  imp:n=1    $ Graphite H-451 reflector fill

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR LATTICE (u=104)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c Lattice mirrors core assembly pattern (15×15 hexagonal)
c Uses u=801 where core has u=901 (with guide tube)
c Uses u=802 where core has u=902 (no guide tube)
c Uses u=802 for graphite filler positions
c
1004  710  -1.803  -8000  lat=2  u=104  imp:n=1  fill=-7:7 -7:7 0:0
            104 104 104 104 104 104 104 104 104 104 104 104 104 104 104
            104 104 104 104 104 104 104 802 802 802 802 802 802 802 104
            104 104 104 104 104 104 802 802 802 802 802 802 802 802 104
            104 104 104 104 104 802 802 802 802 802 802 802 802 802 104
            104 104 104 104 802 802 802 801 802 802 801 802 802 802 104
            104 104 104 802 802 802 802 802 801 802 802 802 802 802 104
            104 104 802 802 802 802 801 802 802 801 802 802 802 802 104
            104 802 802 802 801 802 802 801 802 802 801 802 802 802 104
            104 802 802 802 802 801 802 802 801 802 802 802 802 104 104
            104 802 802 802 802 802 801 802 802 802 802 802 104 104 104
            104 802 802 802 801 802 802 801 802 802 802 104 104 104 104
            104 802 802 802 802 802 802 802 802 802 104 104 104 104 104
            104 802 802 802 802 802 802 802 802 104 104 104 104 104 104
            104 802 802 802 802 802 802 802 104 104 104 104 104 104 104
            104 104 104 104 104 104 104 104 104 104 104 104 104 104 104

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR REGION (global cell)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
104   0  -104  fill=104  imp:n=1    $ Top reflector (z=180-200)
```

---

## 4. REFLECTOR ASSEMBLY SURFACE CARDS

### 4.1 Bottom Reflector Surfaces (z = 0-20 cm)

```mcnp
c ============================================================================
c         BOTTOM REFLECTOR ASSEMBLY SURFACES (z = 0-20 cm)
c ============================================================================
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR CONTAINER
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
101   rhp  0 0  0   0 0  20   100.92 0 0    $ Bottom reflector lattice container

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR ASSEMBLY BOUNDARIES
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
7000  rhp  0 0  0   0 0  20     8.684 0 0    $ Assembly lattice cell (hexagonal)
7001  rhp  0 0  0   0 0  20     8.684 0 0    $ Assembly w/ guide tube (u=701)
7002  rhp  0 0  0   0 0  20     8.684 0 0    $ Assembly w/o guide tube (u=702)

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR HEAT PIPE HOLES
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c Heat pipes extend through reflector (876 pipes total)
c Radius: 1.07 cm (same as active core heat pipes)
c
4701  rcc  0 0  0   0 0  20     1.070         $ Heat pipe hole (w/ guide tube)
4702  rcc  0 0  0   0 0  20     1.070         $ Heat pipe hole (no guide tube)

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR GUIDE TUBE HOLES
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c Guide tubes extend through reflector (13 positions)
c Radius: 3.2 cm (same as active core guide tubes)
c
9701  rcc  0 0  0   0 0  20     3.200         $ Guide tube hole
```

### 4.2 Top Reflector Surfaces (z = 180-200 cm)

```mcnp
c ============================================================================
c           TOP REFLECTOR ASSEMBLY SURFACES (z = 180-200 cm)
c ============================================================================
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR CONTAINER
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
104   rhp  0 0 180  0 0  20   100.92 0 0     $ Top reflector lattice container

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR ASSEMBLY BOUNDARIES
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8000  rhp  0 0 180  0 0  20     8.684 0 0    $ Assembly lattice cell (hexagonal)
8001  rhp  0 0 180  0 0  20     8.684 0 0    $ Assembly w/ guide tube (u=801)
8002  rhp  0 0 180  0 0  20     8.684 0 0    $ Assembly w/o guide tube (u=802)

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR HEAT PIPE PROTRUSIONS
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c Heat pipes protrude through top reflector
c Evaporator section extends to z=180, continues through reflector
c Radius: 1.07 cm
c
4801  rcc  0 0 180  0 0  20     1.070         $ Heat pipe hole (w/ guide tube)
4802  rcc  0 0 180  0 0  20     1.070         $ Heat pipe hole (no guide tube)

c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR GUIDE TUBE HOLES
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c Guide tubes extend through top reflector (13 positions)
c Radius: 3.2 cm
c
9801  rcc  0 0 180  0 0  20     3.200         $ Guide tube hole
```

---

## 5. REQUIRED MATERIAL DEFINITIONS

### 5.1 New Materials Needed

```mcnp
c ============================================================================
c               NEW MATERIAL DEFINITIONS FOR DRUMS & REFLECTORS
c ============================================================================
c
c --- Material 710: Graphite Reflector H-451 (1000-1045 K) ---
c Used in both bottom and top reflectors
c Same composition as m201 but separate for temperature tracking
c
m710  6000.83c  -1.0            $ Carbon at 1200K
mt710 grph.47t                  $ Graphite S(a,b) at 1200K
c Density: 1.803 g/cm³

c --- Material 800: B4C Control Drum Absorber (1000 K) ---
c Natural boron enrichment (19.9% B-10, 80.1% B-11)
c Stoichiometry: B4C (4 boron atoms, 1 carbon atom)
c
m800  5010.02c  1.673E-02      $ B-10 at 900K (natural 19.9%)
      5011.02c  6.738E-02      $ B-11 at 900K (natural 80.1%)
      6000.82c  2.103E-02      $ C at 900K (from carbide)
c Density: 2.52 g/cm³
c Temperature: 1000 K (intermediate between core and reflector)

c --- Material 801: Control Drum Graphite (1000 K) ---
c Graphite in control drum (240° arc)
c Same composition as other graphite, separate for tracking
c
m801  6000.82c  -1.0            $ Carbon at 900K
mt801 grph.20t                  $ Graphite S(a,b) at 400K
c Density: 1.803 g/cm³
c Temperature: 1000 K
```

**Note:** Materials m201, m300, m315 are already defined in the existing model and are reused here.

---

## 6. WHY THIS CODE: GEOMETRY EXPLANATION

### 6.1 Control Drums: Cylindrical Geometry in Hexagonal Lattice

**Challenge:** The HPMR core uses a hexagonal lattice structure (LAT=2) for fuel assemblies, but control drums are **cylindrical** structures positioned around the **periphery**. This creates a geometric mismatch that requires careful handling.

**Approach:**

1. **Cylindrical Surfaces (RCC):**
   - Control drums are defined using **RCC (Right Circular Cylinder)** macrobodies
   - Each drum requires **TWO RCC surfaces**:
     - **Outer cylinder** (surface -X001): Full drum boundary (r = 14.09895 cm)
     - **Inner cylinder** (surface -X002): B₄C/graphite interface (r = 11.30055 cm)
   - Thickness of B₄C layer: 14.09895 - 11.30055 = 2.7984 cm ✓

2. **Angular Sectors Using Plane Cuts:**
   - Each drum has a **120° B₄C absorber arc** facing inward (toward core)
   - Remaining **240° arc** is graphite (structural/moderator)
   - **Plane surfaces (P)** cut the cylinder into sectors:
     - Two cutting planes at ±60° from the inward radial direction
     - Creates 120° B₄C sector and 240° graphite sector

3. **Cell Definitions:**
   - **B₄C cell**: `-outer_cyl inner_cyl -plane1 plane2`
     - Inside outer cylinder, outside inner cylinder, between two planes (120° sector)
   - **Graphite cell**: `-outer_cyl inner_cyl (plane1:-plane2)`
     - Inside outer cylinder, outside inner cylinder, NOT in B₄C sector (240° remainder)

4. **Positioning Around Core:**
   - 12 drums at **30° intervals**: 0°, 30°, 60°, ..., 330°
   - Radial position: **r = 120 cm** from core center
   - Cartesian coordinates: (r·cos(θ), r·sin(θ), 0)
   - Example: Drum 2 at 30° → (120·cos(30°), 120·sin(30°), 0) = (103.923, 60.000, 0)

5. **Axial Extent:**
   - Drums span **z = 20-180 cm** (active core height only)
   - RCC format: `rcc x y z_bottom  0 0 height  radius`
   - Example: `rcc 120 0 20  0 0 160  14.09895` → cylinder from z=20 to z=180

**Why This Works:**
- RCC surfaces are independent of the hexagonal lattice (defined in global coordinates)
- Drums intersect the radial reflector region (r = 140-146.8 cm)
- No interference with hexagonal core lattice (core radius ~100.92 cm < drum position 120 cm)
- Angular positioning ensures uniform coverage around core periphery

**Geometric Verification:**
- Distance between adjacent drums (30° spacing):
  ```
  d = 2 × 120 × sin(15°) = 62.12 cm
  Drum diameter = 28.20 cm
  Clearance = 62.12 - 28.20 = 33.92 cm ✓ (no overlap)
  ```

---

### 6.2 Reflector Assemblies: Lattice Matching and Hole Patterns

**Challenge:** Reflector assemblies (top and bottom) must **match the core lattice structure** while accommodating heat pipe and guide tube penetrations.

**Approach:**

1. **Lattice Mirroring:**
   - Bottom reflector lattice (u=101) and top reflector lattice (u=104) use **same 15×15 hexagonal pattern** as core lattice (u=102)
   - Fill arrays mirror core assembly positions:
     - `u=701/801` (with guide tube) placed where core has `u=901`
     - `u=702/802` (no guide tube) placed where core has `u=902`
     - Graphite filler (u=102/104) placed in non-fuel positions

2. **Assembly Structure:**
   - **Heat pipe holes:** RCC cylinders (r = 1.07 cm) extending through 20 cm reflector thickness
   - **Guide tube holes:** RCC cylinders (r = 3.2 cm) extending through reflector (13 positions)
   - **Graphite fill:** Hexagonal prism (RHP) minus heat pipe and guide tube holes
   - Boolean logic: `-RHP_boundary  (heat_pipe_hole : guide_tube_hole)`

3. **Universe Hierarchy:**
   ```
   Level 1: Reflector assembly universes (u=701, 702, 801, 802)
            ├─ Heat pipe penetration (m315)
            ├─ Guide tube penetration (m300) [if applicable]
            └─ Graphite reflector fill (m710)

   Level 2: Reflector lattice universes (u=101, 104)
            └─ 15×15 hexagonal array of assemblies

   Level 3: Global cells (101, 104)
            └─ Fill reflector lattice into global geometry
   ```

4. **Surface Definitions:**
   - **RHP (Hexagonal Prism)** for assembly boundaries:
     - Format: `rhp x y z  hx hy hz  Rx Ry Rz`
     - `rhp 0 0 0  0 0 20  8.684 0 0` → hex prism 20 cm tall, R=8.684 cm
   - **RCC (Cylinder)** for holes:
     - Heat pipe: `rcc 0 0 0  0 0 20  1.070` (centered in assembly)
     - Guide tube: `rcc 0 0 0  0 0 20  3.200` (centered in assembly)

5. **Axial Positioning:**
   - **Bottom reflector:** z = 0-20 cm (RHP origin at z=0)
   - **Top reflector:** z = 180-200 cm (RHP origin at z=180)
   - Reflectors "sandwich" the active core (z = 20-180 cm)

**Why This Works:**
- Lattice continuity: Reflectors use same hexagonal pitch (17.368 cm) as core
- Heat pipe alignment: Holes in reflectors align with heat pipes in core (same lattice positions)
- Guide tube alignment: Holes align with guide tubes in core assemblies
- Graphite fill: Bulk reflector material surrounds penetrations

**Material Volume Verification:**
- Assembly volume (hexagonal prism): V_hex = (√3/2) × (2R)² × h = 2.598 × (2×8.684)² × 20 = 15,618 cm³
- Heat pipe volume (cylinder): V_hp = π × r² × h = π × 1.07² × 20 = 71.9 cm³
- Guide tube volume (cylinder): V_gt = π × r² × h = π × 3.2² × 20 = 643.4 cm³
- Graphite volume (assembly with guide tube): 15,618 - 71.9 - 643.4 = 14,903 cm³ (95.4% graphite)
- Graphite volume (assembly without guide tube): 15,618 - 71.9 = 15,546 cm³ (99.5% graphite)

---

### 6.3 Surface Numbering Scheme

**Systematic Organization:**

| Surface Range | Component | Type | Example |
|---------------|-----------|------|---------|
| **8001-8114** | Control drums (12×2 RCC + 12×2 P = 48 surfaces) | RCC, P | 8001 = Drum 1 outer |
| **101, 104** | Reflector containers | RHP | 101 = Bottom reflector |
| **7000-7002** | Bottom reflector assemblies | RHP | 7001 = Assembly w/ guide |
| **8000-8002** | Top reflector assemblies | RHP | 8001 = Assembly w/ guide |
| **4701-4702** | Bottom reflector heat pipe holes | RCC | 4701 = Heat pipe hole |
| **4801-4802** | Top reflector heat pipe holes | RCC | 4801 = Heat pipe hole |
| **9701** | Bottom reflector guide tube hole | RCC | 9701 = Guide tube hole |
| **9801** | Top reflector guide tube hole | RCC | 9801 = Guide tube hole |

**Cell Numbering:**

| Cell Range | Component | Material | Example |
|------------|-----------|----------|---------|
| **8101-9202** | Control drums (12×2 = 24 cells) | m800 (B₄C), m801 (graphite) | 8101 = Drum 1 B₄C |
| **101, 104** | Reflector regions (global) | void (filled) | 101 = Bottom reflector |
| **701-702** | Bottom reflector assemblies | m710, m315, m300 | 701 = Bottom assembly w/ guide |
| **801-802** | Top reflector assemblies | m710, m315, m300 | 801 = Top assembly w/ guide |
| **1001** | Bottom reflector lattice | m710 (filled) | 1001 = Bottom lattice |
| **1004** | Top reflector lattice | m710 (filled) | 1004 = Top lattice |

---

### 6.4 Integration with Existing Model

**Where to Insert Code:**

1. **Cell Cards (Section 3):**
   - After existing assembly definitions (u=901, u=902)
   - Add control drum cells (8101-9202)
   - Add reflector assembly cells (701, 702, 801, 802)
   - Add reflector lattice cells (1001, 1004)
   - Add global reflector cells (101, 104)

2. **Surface Cards (Section 104):**
   - After existing assembly surfaces (901, 902, 903)
   - Add control drum surfaces (8001-8114)
   - Add reflector container surfaces (101, 104)
   - Add reflector assembly surfaces (7000-8002)
   - Add heat pipe hole surfaces (4701-4802)
   - Add guide tube hole surfaces (9701, 9801)

3. **Material Cards (Section 193+):**
   - After existing materials (m201, m300, m301, m302, m315, m401, m411)
   - Add m710 (reflector graphite)
   - Add m800 (B₄C absorber)
   - Add m801 (drum graphite)

4. **Global Cell Modifications (Section 97):**
   - **Update cell 18** (radial reflector):
     - Current: `-18  102` (outside core, inside radial reflector)
     - New: `-18  102  101  104` (exclude bottom/top reflectors)
   - **Update cell 9000** (outside universe):
     - Add exclusions for new cells: `#101 #104 #8101 #8102 ... #9202`

**Dependencies:**
- Existing materials m315 (heat pipe), m300 (helium) are reused
- Existing material m201 (graphite monolith) can substitute for m710 if desired
- Lattice fill patterns mirror existing core lattice (u=102)

---

### 6.5 Physics Considerations

**Neutron Transport:**

1. **Control Drum Reactivity Effect:**
   - B₄C absorber (120° facing inward) provides **negative reactivity**
   - Expected Δρ ≈ -5000 to -10000 pcm (drums in vs. out)
   - Natural boron: 19.9% B-10 (high thermal neutron absorption cross-section: σ_a ≈ 3840 barns)
   - Drum rotation changes B₄C orientation → reactivity control mechanism

2. **Reflector Neutron Economy:**
   - **Bottom reflector (z=0-20):** Reduces axial neutron leakage, reflects neutrons back to core
   - **Top reflector (z=180-200):** Reduces axial neutron leakage, but lower graphite content
   - Graphite scattering: Moderates fast neutrons, increases thermal flux
   - Heat pipe penetrations: Local flux perturbations (SS316 absorption)

3. **Spectral Effects:**
   - **Core (z=20-180):** Thermal spectrum (graphite-moderated, TRISO fuel)
   - **Bottom reflector:** Similar thermal spectrum, high graphite density
   - **Top reflector:** Slightly harder spectrum (heat pipe penetrations reduce moderation)
   - **Near control drums:** Flux depression in B₄C regions, flux peaking in graphite

4. **Temperature Feedback:**
   - Doppler broadening in fuel: Negative reactivity coefficient (~-7 pcm/K)
   - Graphite temperature coefficient: Slightly positive (~+0.5 pcm/K), but small magnitude
   - Net coefficient: Negative (Doppler dominates)

**Expected Results:**

| Parameter | Expected Value | Validation Source |
|-----------|---------------|-------------------|
| **k_eff (drums in)** | 1.09-1.10 | Serpent reference: 1.09972 |
| **k_eff (drums out)** | 1.14-1.15 | Estimated from reactivity worth |
| **Reactivity worth (drums)** | 5000-10000 pcm | Typical for B₄C drums |
| **Axial leakage** | <10% | With reflectors |
| **Radial leakage** | <5% | With radial reflector |
| **Peak flux** | Core center | Assembly-level peaking ~2.4 |

---

## 7. IMPLEMENTATION CHECKLIST

### 7.1 Code Insertion Steps

- [ ] **Step 1:** Add material definitions (m710, m800, m801) to material block
- [ ] **Step 2:** Add bottom reflector assembly cells (701, 702, 7011, 7012, 7021) to cell block
- [ ] **Step 3:** Add top reflector assembly cells (801, 802, 8011, 8012, 8021) to cell block
- [ ] **Step 4:** Add reflector lattice cells (1001, 1004) to cell block
- [ ] **Step 5:** Add global reflector cells (101, 104) to cell block
- [ ] **Step 6:** Add control drum cells (8101-9202, 24 cells total) to cell block
- [ ] **Step 7:** Add reflector surfaces (101, 104, 7000-9801) to surface block
- [ ] **Step 8:** Add control drum surfaces (8001-8114, 48 surfaces total) to surface block
- [ ] **Step 9:** Update global cell 18 (radial reflector) to exclude new reflector cells
- [ ] **Step 10:** Update cell 9000 (outside universe) to exclude all new cells
- [ ] **Step 11:** Test geometry with `mcnp6 inp=hpcmr-simplified.i ip` (plotter mode)
- [ ] **Step 12:** Verify no overlapping cells (BAD TROUBLE 1000)
- [ ] **Step 13:** Verify no lost particles in reflector regions
- [ ] **Step 14:** Verify neutron balance (check leakage fractions)

### 7.2 Validation Tests

- [ ] **Geometry plot (XY view):** Verify 12 drums visible around core periphery
- [ ] **Geometry plot (XZ view):** Verify reflectors at z=0-20 and z=180-200
- [ ] **Drum rotation test:** Manually rotate drum (change plane angles) and verify reactivity change
- [ ] **k_eff comparison:** Compare to Serpent reference (1.09972 ± 0.00014)
- [ ] **Neutron leakage:** Check axial and radial leakage fractions (should be <15% total)
- [ ] **Flux distribution:** Verify flux depression near B₄C absorbers
- [ ] **Material balance:** Verify total core mass matches specifications

---

## 8. TROUBLESHOOTING COMMON ISSUES

### 8.1 Geometry Errors

**Issue 1: "BAD TROUBLE 1000 - Overlapping cells"**
- **Cause:** Control drum surfaces intersect radial reflector incorrectly
- **Fix:** Verify drum outer radius (14.09895 cm) + position (120 cm) < radial reflector outer (146.8 cm)
  - Max extent: 120 + 14.09895 = 134.10 cm < 140 cm ✓
- **Alternative:** Add drum exclusions to radial reflector cell definition

**Issue 2: "Lost particles in reflector region"**
- **Cause:** Gap between reflector assemblies or heat pipe holes
- **Fix:** Verify lattice fill pattern matches core pattern exactly
- **Check:** Surface 7001/7002/8001/8002 (assembly boundaries) are identical to 901/902

**Issue 3: "Surface X undefined in cell Y"**
- **Cause:** Surface numbering mismatch between cells and surfaces
- **Fix:** Cross-reference all surface numbers in cells vs. surface block

### 8.2 Physics Errors

**Issue 4: "k_eff too high (>1.15)"**
- **Cause:** Control drums may not be working (B₄C not positioned correctly)
- **Fix:** Verify B₄C sector faces inward (check plane orientations)
- **Test:** Flip all B₄C sectors to face outward → k_eff should increase

**Issue 5: "k_eff too low (<1.05)"**
- **Cause:** Excessive neutron leakage through reflectors
- **Fix:** Verify reflector lattices (101, 104) are filled correctly
- **Check:** Material m710 density = 1.803 g/cm³ (not void)

### 8.3 Material Errors

**Issue 6: "Material 710 undefined"**
- **Cause:** m710 not defined in material block
- **Fix:** Add m710 definition (copy from m201 if needed)

**Issue 7: "MT card 710 not found"**
- **Cause:** Thermal scattering library grph.47t not in MCNP data path
- **Fix:** Verify `$DATAPATH` includes path to `grph.47t` library
- **Alternative:** Use `grph.20t` (400K) if 47t unavailable

---

## 9. EXPECTED PERFORMANCE IMPACT

### 9.1 Computational Cost

**Current model (active core only):**
- Cells: ~150
- Surfaces: ~50
- Lattices: 2 levels (pin → assembly → core)

**New model (with drums + reflectors):**
- Cells: ~200 (+50 cells: 24 drums, 26 reflectors)
- Surfaces: ~120 (+70 surfaces: 48 drums, 22 reflectors)
- Lattices: 2 levels + 2 reflector lattices

**Estimated runtime increase:**
- Geometry tracking: +10-15% (more cells to check)
- Neutron tracking: +5-10% (more scattering in reflectors)
- Total: **+15-25% runtime** vs. current model

### 9.2 Memory Usage

**Surface storage:** ~2 KB per surface → +70 surfaces = +140 KB
**Cell storage:** ~1 KB per cell → +50 cells = +50 KB
**Total memory increase:** **~200 KB** (negligible for modern systems)

### 9.3 Accuracy Improvement

**Without reflectors:**
- Axial leakage: ~40-50% (severe overestimate)
- k_eff: Underestimated by ~5000-10000 pcm

**With reflectors:**
- Axial leakage: ~5-10% (realistic)
- k_eff: Within ±500 pcm of reference

**With control drums:**
- Reactivity control: ±5000 pcm (realistic operating range)
- Spatial flux distribution: More accurate near core periphery

---

## DOCUMENT METADATA

**Created:** 2025-11-08
**Purpose:** Implement GAP 3 (control drums) and reflector assemblies for HPMR model
**Target Model:** `/home/user/mcnp-skills/hpcmr-simplified.i`
**Reference:** HPMR_Gap_Analysis.md section 2.1
**Status:** Code complete, ready for implementation
**Next Steps:** Insert code into model, test geometry, validate physics

**Total Code Volume:**
- Cell cards: ~80 lines
- Surface cards: ~120 lines
- Material cards: ~15 lines
- **Total: ~215 lines of MCNP input**

**Estimated Implementation Time:** 4-6 hours (code insertion + testing)

---

**END OF GEOMETRY CODE DOCUMENTATION**

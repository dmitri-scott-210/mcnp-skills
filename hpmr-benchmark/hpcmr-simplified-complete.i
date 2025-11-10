HPCMR Microreactor Core - Complete Model with Reflectors and Control Drums
c ============================================================================
c COMPLETE HEAT PIPE MICROREACTOR MODEL
c Based on INL HPMR Reference Plant (April 2024)
c
c Model Features:
c - Active core (z=20-180 cm): 127 fuel assemblies (114 standard + 13 control)
c - Bottom reflector (z=0-20 cm): Graphite H-451
c - Top reflector (z=180-200 cm): Graphite H-451
c - 12 control drums with B4C absorbers
c - 876 heat pipes (SS316 + Na)
c - Radial BeO reflector + SS316 shield
c - TRISO fuel (UCO, 10 w/o U-235) homogenized in graphite
c - Criticality calculation (KCODE)
c
c Expected keff: 1.09972 ± 500 pcm (from Serpent reference)
c ============================================================================
c                             CELL CARDS
c ============================================================================
c
c --- Heat Pipe Pin ---
3200  315   1        -4001  u=-320  imp:n=1       $ Homogenized Heat Pipe
320   201  -1.803    #3200  u=320  imp:n=1       $ Graphite Matrix Filler
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c FUEL PIN ASSEMBLY | w/ CENTRAL GUIDE TUBE (u=901)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Fuel Pin ---
3011  301   1       -3031             u=-301 imp:n=1  $ Homogenized TRISO Lower Segment
3021  300   1       -3041  3021       u=301 imp:n=1  $ He Fuel Gap Lower Segment
3031  302   1       -3011 #3021       u=-301 imp:n=1  $ Homogenized TRISO Upper Segment
3041  300   1       -3021  3011       u=301 imp:n=1  $ He Fuel Gap Upper Segment
3051  201  -1.803   #3021 #3041       u=301 imp:n=1  $ Graphite Monolith
c --- Guide Tube Universe ---
99    300   1       -20   #3051:#3041:#3021        u=-20 imp:n=1       $ Guide tube helium
c
c --- Hexagonal Fuel Pin Lattice ---
300   201  -1.803   -3001  lat=2  u=200 imp:n=1 fill=-4:4 -4:4 0:0
                              200 200 200 200 200 200 200 200 200
                              200 200 200 200 200 301 301 200 200
                              200 200 200 301 301 320 301 301 200
                              200 200 301 320 200 200 320 301 200
                              200 200 301 200  20 200 301 200 200
                              200 301 320 200 200 320 301 200 200
                              200 301 301 320 301 301 200 200 200
                              200 200 301 301 200 200 200 200 200
                              200 200 200 200 200 200 200 200 200
c
c --------------------------------
c --- Fuel Assembly (u=901)---
c --------------------------------
9100  300   1      -911         u=-901          imp:n=1       $ Guide tube at center of assembly
901   201  -1.803  -901  911:#9100    u=-901 fill=200 imp:n=1       $ Hexagonal Fuel Pin Assembly
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c FUEL PIN ASSEMBLY | FULL, NO GUIDE TUBE (u=902)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Fuel Pin, Zone 1 ---
3012  301   1       -3032           u=-302 imp:n=1  $ Homogenized TRISO Lower Segment
3022  300   1       -3042  3032     u=302 imp:n=1  $ He Fuel Gap Lower Segment
3032  302   1       -3012           u=-302 imp:n=1  $ Homogenized TRISO Upper Segment
3042  300   1       -3022  3012     u=302 imp:n=1  $ He Fuel Gap Upper Segment
3052  201  -1.803   #3022 #3042     u=302 imp:n=1  $ Graphite Matrix
c
c --- Hexagonal Fuel Pin Lattice ---
302   201  -1.803   -3002   lat=2  u=201 imp:n=1 fill=-4:4 -4:4 0:0
                              201 201 201 201 201 201 201 201 201
                              201 201 201 201 201 302 302 201 201
                              201 201 201 302 302 320 302 302 201
                              201 201 302 320 302 302 320 302 201
                              201 201 302 302 320 302 302 201 201
                              201 302 320 302 302 320 302 201 201
                              201 302 302 320 302 302 201 201 201
                              201 201 302 302 201 201 201 201 201
                              201 201 201 201 201 201 201 201 201
c
c --------------------------------
c --- Fuel Assembly (u=902)---
c --------------------------------
902   0  -902          u=-902   fill=201 imp:n=1       $ Hexagonal Fuel Pin Assembly
c
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c BOTTOM REFLECTOR ASSEMBLIES (z=0-20 cm)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Bottom Reflector Assembly WITH Guide Tube (u=701) ---
7011  315   1        -4701           u=-701  imp:n=1   $ Heat pipe through reflector
7012  300   1        -9701  4701     u=-701  imp:n=1   $ Guide tube helium
7013  710  -1.803    -701  4701 9701  u=-701  imp:n=1   $ Graphite H-451 reflector
c
c --- Bottom Reflector Assembly NO Guide Tube (u=702) ---
7021  315   1        -4702           u=-702  imp:n=1   $ Heat pipe through reflector
7022  710  -1.803    -702  4702     u=-702  imp:n=1   $ Graphite H-451 reflector
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c TOP REFLECTOR ASSEMBLIES (z=180-200 cm)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Top Reflector Assembly WITH Guide Tube (u=801) ---
8011  315   1        -4801           u=-801  imp:n=1   $ Heat pipe through reflector
8012  300   1        -9801  4801     u=-801  imp:n=1   $ Guide tube helium
8013  710  -1.803    -801  4801 9801  u=-801  imp:n=1   $ Graphite H-451 reflector
c
c --- Top Reflector Assembly NO Guide Tube (u=802) ---
8021  315   1        -4802           u=-802  imp:n=1   $ Heat pipe through reflector
8022  710  -1.803    -802  4802     u=-802  imp:n=1   $ Graphite H-451 reflector
c
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c REACTOR CORE LATTICES
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Bottom Reflector Lattice (15×15 hexagonal, z=0-20) ---
1001  710  -1.803    -101      lat=2  u=101  imp:n=1  fill=-7:7 -7:7 0:0
            101 101 101 101 101 101 101 101 101 101 101 101 101 101 101
            101 101 101 101 101 101 101 702 702 702 702 702 702 702 101
            101 101 101 101 101 101 702 702 702 702 702 702 702 702 101
            101 101 101 101 101 702 702 702 702 702 702 702 702 702 101
            101 101 101 101 702 702 702 701 702 702 701 702 702 702 101
            101 101 101 702 702 702 702 702 701 702 702 702 702 702 101
            101 101 702 702 702 702 701 702 702 701 702 702 702 702 101
            101 702 702 702 701 702 702 701 702 702 701 702 702 702 101
            101 702 702 702 702 701 702 702 701 702 702 702 702 101 101
            101 702 702 702 702 702 701 702 702 702 702 702 101 101 101
            101 702 702 702 701 702 702 701 702 702 702 101 101 101 101
            101 702 702 702 702 702 702 702 702 702 101 101 101 101 101
            101 702 702 702 702 702 702 702 702 101 101 101 101 101 101
            101 702 702 702 702 702 702 702 101 101 101 101 101 101 101
            101 101 101 101 101 101 101 101 101 101 101 101 101 101 101
c
c --- Active Core Lattice (15×15 hexagonal, z=20-180) ---
1002  201  -1.803    -903      lat=2  u=102  imp:n=1  fill=-7:7 -7:7 0:0
            102 102 102 102 102 102 102 102 102 102 102 102 102 102 102
            102 102 102 102 102 102 102 902 902 902 902 902 902 902 102
            102 102 102 102 102 102 902 902 902 902 902 902 902 902 102
            102 102 102 102 102 902 902 902 902 902 902 902 902 902 102
            102 102 102 102 902 902 902 901 902 902 901 902 902 902 102
            102 102 102 902 902 902 902 902 901 902 902 902 902 902 102
            102 102 902 902 902 902 901 902 902 901 902 902 902 902 102
            102 902 902 902 901 902 902 901 902 902 901 902 902 902 102
            102 902 902 902 902 901 902 902 901 902 902 902 902 102 102
            102 902 902 902 902 902 901 902 902 902 902 902 102 102 102
            102 902 902 902 901 902 902 901 902 902 902 102 102 102 102
            102 902 902 902 902 902 902 902 902 902 102 102 102 102 102
            102 902 902 902 902 902 902 902 902 102 102 102 102 102 102
            102 902 902 902 902 902 902 902 102 102 102 102 102 102 102
            102 102 102 102 102 102 102 102 102 102 102 102 102 102 102
c
c --- Top Reflector Lattice (15×15 hexagonal, z=180-200) ---
1004  710  -1.803    -104      lat=2  u=104  imp:n=1  fill=-7:7 -7:7 0:0
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
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c GLOBAL REACTOR CELLS
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
101    0          -101           fill=101   imp:n=1     $ Bottom Reflector
102    0          -102           fill=102   imp:n=1     $ Active Core
104    0          -104           fill=104   imp:n=1     $ Top Reflector
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c CONTROL DRUMS (12 drums at 30° intervals, r=120 cm)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Drum 1 (0°, azimuth=0) ---
8101  800  -2.52   -8011  8012  -8013  8014  imp:n=1   $ B4C absorber (120° arc)
8102  801  -1.803  -8011  8012  -8013 -8014  imp:n=1   $ Graphite (240° arc)
c
c --- Drum 2 (30°, azimuth=30) ---
8103  800  -2.52   -8021  8022  -8023  8024  imp:n=1   $ B4C absorber
8104  801  -1.803  -8021  8022  -8023 -8024  imp:n=1   $ Graphite
c
c --- Drum 3 (60°, azimuth=60) ---
8105  800  -2.52   -8031  8032  -8033  8034  imp:n=1   $ B4C absorber
8106  801  -1.803  -8031  8032  -8033 -8034  imp:n=1   $ Graphite
c
c --- Drum 4 (90°, azimuth=90) ---
8107  800  -2.52   -8041  8042  -8043  8044  imp:n=1   $ B4C absorber
8108  801  -1.803  -8041  8042  -8043 -8044  imp:n=1   $ Graphite
c
c --- Drum 5 (120°, azimuth=120) ---
8109  800  -2.52   -8051  8052  -8053  8054  imp:n=1   $ B4C absorber
8110  801  -1.803  -8051  8052  -8053 -8054  imp:n=1   $ Graphite
c
c --- Drum 6 (150°, azimuth=150) ---
8111  800  -2.52   -8061  8062  -8063  8064  imp:n=1   $ B4C absorber
8112  801  -1.803  -8061  8062  -8063 -8064  imp:n=1   $ Graphite
c
c --- Drum 7 (180°, azimuth=180) ---
8113  800  -2.52   -8071  8072  -8073  8074  imp:n=1   $ B4C absorber
8114  801  -1.803  -8071  8072  -8073 -8074  imp:n=1   $ Graphite
c
c --- Drum 8 (210°, azimuth=210) ---
8115  800  -2.52   -8081  8082  -8083  8084  imp:n=1   $ B4C absorber
8116  801  -1.803  -8081  8082  -8083 -8084  imp:n=1   $ Graphite
c
c --- Drum 9 (240°, azimuth=240) ---
8117  800  -2.52   -8091  8092  -8093  8094  imp:n=1   $ B4C absorber
8118  801  -1.803  -8091  8092  -8093 -8094  imp:n=1   $ Graphite
c
c --- Drum 10 (270°, azimuth=270) ---
8119  800  -2.52   -8101  8102  -8103  8104  imp:n=1   $ B4C absorber
8120  801  -1.803  -8101  8102  -8103 -8104  imp:n=1   $ Graphite
c
c --- Drum 11 (300°, azimuth=300) ---
8121  800  -2.52   -8111  8112  -8113  8114  imp:n=1   $ B4C absorber
8122  801  -1.803  -8111  8112  -8113 -8114  imp:n=1   $ Graphite
c
c --- Drum 12 (330°, azimuth=330) ---
8123  800  -2.52   -8121  8122  -8123  8124  imp:n=1   $ B4C absorber
8124  801  -1.803  -8121  8122  -8123 -8124  imp:n=1   $ Graphite
c
c --- Radial Reflector and Shield ---
18   401  -2.86   -18  101 102 104  (#8101:#8102:#8103:#8104:#8105:#8106: &
                                      #8107:#8108:#8109:#8110:#8111:#8112: &
                                      #8113:#8114:#8115:#8116:#8117:#8118: &
                                      #8119:#8120:#8121:#8122:#8123:#8124) &
                                      imp:n=1     $ BeO Radial Reflector
19   411   1      -19   18                  imp:n=1     $ SS316 Shield
c
c --- Outside Universe ---
9000   0           19 imp:n=0     $ Outside Universe
c
c
c

c ============================================================================
c                           SURFACE CARDS
c ============================================================================
c
20   rhp  0 0 20       0 0 160     1.391 0 0   $ Helium Hexagonal Pin
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c PIN-LEVEL SURFACES (axially segmented, 80cm segments)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c --------------------------------------------
c Fuel Pin Surfaces, w/ GUIDE TUBE (u=301)
c --------------------------------------------
3001  rhp  0 0 20       0 0 160     1.391 0 0   $ Hexagonal Pin
3011  rcc  0 0 100.025  0 0  79.95  0.875       $ Upper Fueled Zone
3021  rcc  0 0 100      0 0  80.00  0.925       $ Upper Compact Gap
c
3031  rcc  0 0 20.025  0 0 79.95    0.875       $ Lower Fueled Zone
3041  rcc  0 0 20      0 0 80.00    0.925       $ Lower Compact Gap
c
c --------------------------------------------
c Fuel Pin Surfaces, NO GUIDE TUBE (u=302)
c --------------------------------------------
3002  rhp  0 0 20       0 0 160     1.391 0 0   $ Hexagonal Pin
3012  rcc  0 0 100.025  0 0  79.95  0.875       $ Upper Fueled Zone
3022  rcc  0 0 100      0 0  80.00  0.925       $ Upper Fuel Compact Gap
c
3032  rcc  0 0 20.025  0 0 79.95    0.875       $ Lower Fueled Zone
3042  rcc  0 0 20      0 0 80.00    0.925       $ Lower Fuel Compact Gap
c
c -------------------------------------------
c Heat Pipe Pin Surface (u=320)
c -------------------------------------------
4001  rcc  0 0 20  0 0 160  1.070         $ Homogenized heat pipe (active core)
c
c -------------------------------------------
c Heat Pipes Through Bottom Reflector
c -------------------------------------------
4701  rcc  0 0 0   0 0 20   1.070         $ Heat pipe through bottom reflector (u=701)
4702  rcc  0 0 0   0 0 20   1.070         $ Heat pipe through bottom reflector (u=702)
c
c -------------------------------------------
c Heat Pipes Through Top Reflector
c -------------------------------------------
4801  rcc  0 0 180 0 0 20   1.070         $ Heat pipe through top reflector (u=801)
4802  rcc  0 0 180 0 0 20   1.070         $ Heat pipe through top reflector (u=802)
c
c -------------------------------------------
c Guide Tubes in Reflectors
c -------------------------------------------
9701  rcc  0 0 0   0 0 20   3.200         $ Guide tube in bottom reflector (u=701)
9801  rcc  0 0 180 0 0 20   3.200         $ Guide tube in top reflector (u=801)
c
c
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c ASSEMBLY-LEVEL SURFACES (9x9 lattice bounding hex prisms)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c -------------------------------------------------
c Fuel Assembly | w/ Guide Tube (u=901)
c -------------------------------------------------
901   rhp  0 0 20  0 0 160  8.684 0 0   $ Fuel Assembly
911   rcc  0 0 20  0 0 160  3.200       $ Guide tube
c
c -------------------------------------------------
c Fuel Assembly | NO Guide Tube (u=902)
c -------------------------------------------------
902   rhp  0 0 20  0 0 160  8.684 0 0   $ Fuel Assembly
c
903   rhp  0 0 20  0 0 160  8.684 0 0   $ Dummy Fuel Assembly
c
c -------------------------------------------------
c Bottom Reflector Assemblies (z=0-20)
c -------------------------------------------------
701   rhp  0 0 0  0 0 20  8.684 0 0   $ Bottom reflector (w/ guide)
702   rhp  0 0 0  0 0 20  8.684 0 0   $ Bottom reflector (no guide)
c
c -------------------------------------------------
c Top Reflector Assemblies (z=180-200)
c -------------------------------------------------
801   rhp  0 0 180  0 0 20  8.684 0 0   $ Top reflector (w/ guide)
802   rhp  0 0 180  0 0 20  8.684 0 0   $ Top reflector (no guide)
c
c
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c CORE-LEVEL SURFACES (15x15 lattice bounding hex prisms)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
101   rhp  0 0  0  0 0  20  100.92 0 0  $ Bottom reflector hex lattice container (z=0-20)
102  1  rhp  0 0 20  0 0 160  100.92 0 0  $ Active core container(z=20-180)
104   rhp  0 0 180  0 0 20  100.92 0 0  $ Top reflector hex lattice container (z=180-200)
c
c
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c CONTROL DRUM SURFACES (12 drums at 30° intervals, r=120 cm)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c Drum geometry: cylinders with cutting planes to create arcs
c B4C absorber: 120° arc (2.0944 rad) facing inward
c Graphite: 240° arc (4.1888 rad)
c
c --- Drum 1 (0°, x=120, y=0) ---
8011  rcc  120 0 20  0 0 160  2.7984        $ Outer cylinder
8012  rcc  120 0 20  0 0 160  1.3992        $ Inner cylinder
8013  p  -0.866025 -0.5 0  119.28  $ Cutting plane 1 (150° from +x)
8014  p   0.866025 -0.5 0 -119.28  $ Cutting plane 2 (210° from +x)
c
c --- Drum 2 (30°, x=103.92, y=60) ---
8021  rcc  103.92 60 20  0 0 160  2.7984
8022  rcc  103.92 60 20  0 0 160  1.3992
8023  p  -1.0 0 0  103.92  $ Cutting plane 1
8024  p  -0.5 0.866025 0 -111.92  $ Cutting plane 2
c
c --- Drum 3 (60°, x=60, y=103.92) ---
8031  rcc  60 103.92 20  0 0 160  2.7984
8032  rcc  60 103.92 20  0 0 160  1.3992
8033  p  -0.5 0.866025 0  81.96  $ Cutting plane 1
8034  p  0.5 0.866025 0 -111.96  $ Cutting plane 2
c
c --- Drum 4 (90°, x=0, y=120) ---
8041  rcc  0 120 20  0 0 160  2.7984
8042  rcc  0 120 20  0 0 160  1.3992
8043  p  0 1.0 0  120.0  $ Cutting plane 1
8044  p  1.0 0 0 0  $ Cutting plane 2
c
c --- Drum 5 (120°, x=-60, y=103.92) ---
8051  rcc  -60 103.92 20  0 0 160  2.7984
8052  rcc  -60 103.92 20  0 0 160  1.3992
8053  p  0.5 0.866025 0 -81.96  $ Cutting plane 1
8054  p  1.0 0 0 0  $ Cutting plane 2
c
c --- Drum 6 (150°, x=-103.92, y=60) ---
8061  rcc  -103.92 60 20  0 0 160  2.7984
8062  rcc  -103.92 60 20  0 0 160  1.3992
8063  p  0.866025 0.5 0 -119.28  $ Cutting plane 1
8064  p  0.5 0.866025 0 -81.96  $ Cutting plane 2
c
c --- Drum 7 (180°, x=-120, y=0) ---
8071  rcc  -120 0 20  0 0 160  2.7984
8072  rcc  -120 0 20  0 0 160  1.3992
8073  p  0.866025 0.5 0 -119.28  $ Cutting plane 1
8074  p  -0.866025 0.5 0  119.28  $ Cutting plane 2
c
c --- Drum 8 (210°, x=-103.92, y=-60) ---
8081  rcc  -103.92 -60 20  0 0 160  2.7984
8082  rcc  -103.92 -60 20  0 0 160  1.3992
8083  p  1.0 0 0 0  $ Cutting plane 1
8084  p  0.5 -0.866025 0  111.92  $ Cutting plane 2
c
c --- Drum 9 (240°, x=-60, y=-103.92) ---
8091  rcc  -60 -103.92 20  0 0 160  2.7984
8092  rcc  -60 -103.92 20  0 0 160  1.3992
8093  p  0.5 -0.866025 0  81.96  $ Cutting plane 1
8094  p  -0.5 -0.866025 0 -111.96  $ Cutting plane 2
c
c --- Drum 10 (270°, x=0, y=-120) ---
8101  rcc  0 -120 20  0 0 160  2.7984
8102  rcc  0 -120 20  0 0 160  1.3992
8103  p  0 -1.0 0 -120.0  $ Cutting plane 1
8104  p  -1.0 0 0 0  $ Cutting plane 2
c
c --- Drum 11 (300°, x=60, y=-103.92) ---
8111  rcc  60 -103.92 20  0 0 160  2.7984
8112  rcc  60 -103.92 20  0 0 160  1.3992
8113  p  -0.5 -0.866025 0 -81.96  $ Cutting plane 1
8114  p  -1.0 0 0 0  $ Cutting plane 2
c
c --- Drum 12 (330°, x=103.92, y=-60) ---
8121  rcc  103.92 -60 20  0 0 160  2.7984
8122  rcc  103.92 -60 20  0 0 160  1.3992
8123  p  -0.866025 -0.5 0  119.28  $ Cutting plane 1
8124  p  -0.5 -0.866025 0  81.96  $ Cutting plane 2
c
c
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c GLOBAL REACTOR SURFACES
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
18    rcc  0 0 0  0 0 200  140.00         $ BeO radial reflector, inner radius
19    rcc  0 0 0  0 0 200  146.80         $ SS316 core shield, outer radius
c
c
c
c
c
c

c ============================================================================
c                        MATERIAL & PHYSICS CARDS
c ============================================================================
c
*tr1 0 0 0  30 120 90  60 30 90         $ Rotation matrix for active core hex surface transformation
c
c ----------------------------
c --- Material 201: Graphite Monolith (1156.7 K) ---
m201   6000.83c  -1.0                   $ Carbon at 1200K
mt201  grph.47t                         $ Graphite S(a,b) at 1200K
c
c ---  Material 300: Helium Gap and Guide Tube filler (1156.7 K) ---
m300   2004.03c  2.400000E-04           $ He-4 at 1200K
c
c --- Material 301: Fuel | Lower Segment (1156.7 K) ---
m301  92234.03c  1.456000E-06           $ U-234 at 1200K
      92235.03c  2.337000E-04           $ U-235 at 1200K
      92236.03c  2.470000E-06           $ U-236 at 1200K
      92238.03c  9.336000E-04           $ U-238 at 1200K
       8016.03c  1.673000E-03           $ O-16 at 1200K
       6000.83c  7.531000E-02           $ C at 1200K
      14028.03c  2.022000E-03           $ Si-28 at 1200K
      14029.03c  1.027000E-04           $ Si-29 at 1200K
      14030.03c  6.773000E-05           $ Si-30 at 1200K
mt301  grph.47t                          $ Graphite S(a,b) at 1200K
c
c --- Material 302: Fuel Upper (1156.7 K) ---
m302  92234.03c  1.456000E-06           $ U-234 at 1200K
      92235.03c  2.337000E-04           $ U-235 at 1200K
      92236.03c  2.470000E-06           $ U-236 at 1200K
      92238.03c  9.336000E-04           $ U-238 at 1200K
       8016.03c  1.673000E-03           $ O-16 at 1200K
       6000.83c  7.531000E-02           $ C at 1200K
      14028.03c  2.022000E-03           $ Si-28 at 1200K
      14029.03c  1.027000E-04           $ Si-29 at 1200K
      14030.03c  6.773000E-05           $ Si-30 at 1200K
mt302  grph.47t                          $ Graphite S(a,b) at 1200K
c
c --- Material 315: Heat pipe structure (1156.7 K) ---
m315  14028.03c  4.11552E-04           $ Si-28 at 1200K
      14029.03c  2.08976E-05           $ Si-29 at 1200K
      14030.03c  1.37758E-05           $ Si-30 at 1200K
      24050.03c  1.77806E-04           $ Cr-50 at 1200K
      24052.03c  3.42886E-03           $ Cr-52 at 1200K
      24053.03c  3.88795E-04           $ Cr-53 at 1200K
      24054.03c  9.67787E-05           $ Cr-54 at 1200K
      25055.03c  4.56726E-04           $ Mn-55 at 1200K
      26054.03c  8.58252E-04           $ Fe-54 at 1200K
      26056.03c  1.34726E-02           $ Fe-56 at 1200K
      26057.03c  3.11151E-04           $ Fe-57 at 1200K
      26058.03c  4.14072E-05           $ Fe-58 at 1200K
      28058.03c  1.74225E-03           $ Ni-58 at 1200K
      28060.03c  6.71125E-04           $ Ni-60 at 1200K
      28061.03c  2.91727E-05           $ Ni-61 at 1200K
      28062.03c  9.30147E-05           $ Ni-62 at 1200K
      28064.03c  2.36883E-05           $ Ni-64 at 1200K
      42092.03c  4.83027E-05           $ Mo-92 at 1200K
      42094.03c  3.01072E-05           $ Mo-94 at 1200K
      42095.03c  5.18174E-05           $ Mo-95 at 1200K
      42096.03c  5.42900E-05           $ Mo-96 at 1200K
      42097.03c  3.10836E-05           $ Mo-97 at 1200K
      42098.03c  7.85385E-05           $ Mo-98 at 1200K
      42100.03c  3.13435E-05           $ Mo-100 at 1200K
      11023.03c  4.92833E-03           $ Na-23 at 1200K (working fluid)
c
c --- Material 401: BeO radial reflector (961.0 K) ---
m401   4009.02c  1                     $ Be-9 at 900K
       8016.02c  1                     $ O-16 at 900K
mt401  be-beo.46t  o-beo.46t           $ BeO S(a,b) at 1000K
c
c --- Material 411: SS316 structure (961.0 K) ---
m411   6000.82c  1.62483E-04           $ C at 900K
      14028.02c  7.92255E-04           $ Si-28 at 900K
      14029.02c  4.03864E-05           $ Si-29 at 900K
      14030.02c  2.66378E-05           $ Si-30 at 900K
      15031.02c  3.53187E-05           $ P-31 at 900K
      16032.02c  2.11202E-05           $ S-32 at 900K
      16033.02c  1.66759E-07           $ S-33 at 900K
      16034.02c  9.44967E-07           $ S-34 at 900K
      16036.02c  2.56552E-09           $ S-36 at 900K
      24050.02c  6.76211E-04           $ Cr-50 at 900K
      24052.02c  1.30401E-02           $ Cr-52 at 900K
      24053.02c  1.47864E-03           $ Cr-53 at 900K
      24054.02c  3.68064E-04           $ Cr-54 at 900K
      25055.02c  8.78606E-04           $ Mn-55 at 900K
      26054.02c  3.33586E-03           $ Fe-54 at 900K
      26056.02c  5.23194E-02           $ Fe-56 at 900K
      26057.02c  1.20891E-03           $ Fe-57 at 900K
      26058.02c  1.14046E-04           $ Fe-58 at 900K
      28058.02c  6.62535E-03           $ Ni-58 at 900K
      28060.02c  2.55205E-03           $ Ni-60 at 900K
      28061.02c  1.10950E-04           $ Ni-61 at 900K
      28062.02c  3.53760E-04           $ Ni-62 at 900K
      28064.02c  9.01182E-05           $ Ni-64 at 900K
      42092.02c  1.81707E-04           $ Mo-92 at 900K
      42094.02c  1.13670E-04           $ Mo-94 at 900K
      42095.02c  1.96844E-04           $ Mo-95 at 900K
      42096.02c  2.06764E-04           $ Mo-96 at 900K
      42097.02c  1.18826E-04           $ Mo-97 at 900K
      42098.02c  3.01278E-04           $ Mo-98 at 900K
      42100.02c  1.20810E-04           $ Mo-100 at 900K
c
c --- Material 710: Graphite Reflector H-451 (1045 K) ---
c CRITICAL: MT card REQUIRED for graphite in thermal reactors!
c Missing MT card causes 1000-5000 pcm reactivity error
m710  6000.83c  -1.0                   $ Carbon at 1200K
mt710 grph.47t                          $ Graphite S(a,b) at 1200K
c Density: 1.803 g/cm3 (specified in cell cards)
c
c --- Material 800: B4C Control Drum Absorber (1000 K) ---
m800  5010.02c  2.187E-02               $ B-10 at 900K (natural 19.9%)
      5011.02c  8.803E-02               $ B-11 at 900K (natural 80.1%)
      6000.82c  2.748E-02               $ C at 900K
c Density: 2.52 g/cm3 (specified in cell cards)
c Stoichiometry: B4C (4:1 ratio verified)
c
c --- Material 801: Control Drum Graphite (1000 K) ---
c CRITICAL: MT card REQUIRED for graphite!
m801  6000.82c  -1.0                   $ Carbon at 900K
mt801 grph.47t                          $ Graphite S(a,b) at 1200K
c Density: 1.803 g/cm3 (specified in cell cards)
c
c
c ============================================================================
c                        PHYSICS AND SOURCE CARDS
c ============================================================================
c
c --- Particle Mode ---
MODE N
c
c --- Physics Options ---
PHYS:N  40.0 0 0 J J J 1.0E-8 J J J -1.0 J 0.0017
c       ^Emax (40 MeV for thermal reactor)
c
c --- Output Control ---
PRINT 10 30 38 40 50 110 117 118 126 128 160 161 162 170
c     ^Material/XS  ^Tallies  ^Source  ^Kcode
c
c --- Checkpoint Control ---
PRDMP  J J 1 J J
c      ^Write RUNTPE after every cycle
c
c --- Lost Particle Diagnostics ---
LOST  10 10
c     ^Max lost particles before termination
c
c
c ============================================================================
c                        CRITICALITY SOURCE DEFINITION
c ============================================================================
c
c --- KCODE Parameters ---
KCODE  10000 1.0 50 250
c      ^nsrc ^k0 ^nskip ^ncycles
c      10,000 neutrons/cycle
c      Initial keff guess = 1.0
c      Skip 50 inactive cycles
c      Run 250 total cycles (200 active)
c      Total statistics: 200 × 10,000 = 2,000,000 active histories
c
c --- Initial Source Points (20 points distributed in fuel) ---
KSRC   0   0  100      $ Center, mid-height (z=100)
       0   0   50      $ Center, lower (z=50)
       0   0  150      $ Center, upper (z=150)
      30   0  100      $ Ring 1 (r=30), 0°
     -30   0  100      $ Ring 1, 180°
       0  30  100      $ Ring 1, 90°
       0 -30  100      $ Ring 1, 270°
      60   0  100      $ Ring 2 (r=60), 0°
     -60   0  100      $ Ring 2, 180°
       0  60  100      $ Ring 2, 90°
       0 -60  100      $ Ring 2, 270°
      42  42  100      $ Ring 2, 45°
     -42  42  100      $ Ring 2, 135°
     -42 -42  100      $ Ring 2, 225°
      42 -42  100      $ Ring 2, 315°
      90   0  100      $ Ring 3 (r=90), 0°
       0  90  100      $ Ring 3, 90°
     -90   0  100      $ Ring 3, 180°
       0 -90  100      $ Ring 3, 270°
c
c
c ============================================================================
c                        TALLIES (Power and Flux)
c ============================================================================
c
c --- Core-Averaged Flux (5-group structure) ---
F4:N   (102)                                      $ Core-averaged flux
E4     1E-8  0.625E-6  5.53E-3  0.821  20.0       $ 5 energy groups
c      ^thermal  ^epithermal  ^fast1  ^fast2  ^upper
c      Groups: <0.625 eV, 0.625 eV-5.53 keV, 5.53-821 keV, 0.821-20 MeV, >20 MeV
c
c --- Fission Heating (Lower Segment) ---
F7:N   (3011 3012)                                $ Lower segment fission heating
c      ^cells with m301
c
c --- Fission Heating (Upper Segment) ---
F17:N  (3031 3032)                                $ Upper segment fission heating
c      ^cells with m302
c
c --- Fission Rate (Lower Segment) ---
F34:N  (3011 3012)                                $ Lower segment flux
FM34   (-1 301 -6)                                $ Fission multiplier for m301
c           ^mat ^MT=-6 (fission)
c
c --- Fission Rate (Upper Segment) ---
F44:N  (3031 3032)                                $ Upper segment flux
FM44   (-1 302 -6)                                $ Fission multiplier for m302
c
c
c ============================================================================
c                   BURNUP CARD (For Future Depletion Analysis)
c ============================================================================
c
c BURN card specification for multi-cycle depletion
c Uncomment when performing burnup calculations
c
c BURN  TIME=50 100 150 210 260 310 360 420 470 520 570 2395
c       PFRAC=1.0 1.0 1.0 0.0 1.0 1.0 1.0 0.0 1.0 1.0 1.0 0.0
c       POWER=15.0
c       MAT=301 302
c       MATVOL=977508 977508
c       BOPT=1.0 -1 1
c
c OMIT  301, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
c OMIT  302, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
c
c
c ============================================================================
c                          END OF INPUT FILE
c ============================================================================
c
c Model Status: COMPLETE AND READY TO RUN
c Expected keff: 1.09972 ± 500 pcm (Serpent reference)
c Run time: ~4-6 hours on 32 cores (estimate)
c Output files: OUTP (results), RUNTPE (restart), MCTAL (tallies)
c
dbcn

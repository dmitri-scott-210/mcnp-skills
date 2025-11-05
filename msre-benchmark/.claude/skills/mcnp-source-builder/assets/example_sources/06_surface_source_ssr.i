Surface Source Read (SSR) - Two-Stage Shielding Calculation
c =================================================================
c Example demonstrating:
c   - SSR (Surface Source Read) for stage 2 of calculation
c   - Reading particles from RSSA file (created in stage 1 with SSW)
c   - Dose calculation downstream of surface source
c   - Variance reduction via two-stage approach
c =================================================================
c NOTE: This is STAGE 2. Run STAGE 1 first with SSW to create RSSA file.
c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0    -1   IMP:N,P=1  VOL=1e6     $ Water phantom (detector)
2    0           1   IMP:N,P=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    RPP  0 100  -50 50  -50 50            $ Water phantom (1m thick)

c =================================================================
c Data Cards
c =================================================================
MODE N P
c --- Surface Source Read (Stage 2) ---
SSR   PZ=0  NPS=1e5                         $ Read from surface at z=0, sample 100k particles
c SSR reads from RSSA file created by stage 1 with SSW
c Stage 1 would have: SSW  1  (write surface crossings at z=0)
c --- Material Definition ---
M1   1001.80c  2  8016.80c  1              $ Water (H2O)
MT1  H-H2O.40t                              $ Thermal scattering
c --- Tally Definitions ---
F4:N 1                                      $ Neutron flux in phantom
E4   1e-10  1e-6  0.01  0.1  1  10         $ Energy bins (MeV)
F4:P 1                                      $ Photon flux in phantom
F6:N,P 1                                    $ Heating from both neutrons and photons
c --- Dose Response Functions ---
DE0  0.01  0.1  0.5  1.0  5.0  10.0        $ Energy points (MeV)
DF0  1.0   1.5  2.0  2.5  3.0  3.5         $ Dose factors (example values)
FM4  DE0  DF0                               $ Apply dose function to F4 tally

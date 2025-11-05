Point Detector Dose - F5 with DE/DF Dose Conversion
c
c Example demonstrating:
c   - F5 point detector tally (next-event estimator)
c   - DE/DF dose conversion factors (ICRP-74 neutron flux-to-dose)
c   - Detector at distance from source
c   - Void geometry for unobstructed path
c
c =================================================================
c Cell Cards
c =================================================================
1    0         -1        IMP:N=1                  $ Problem void
2    0          1        IMP:N=0                  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   200.0          $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
MODE N
c Source - Watt fission spectrum at origin
SDEF  POS=0 0 0  ERG=D1
SI1  -3  0.965  2.29                               $ Watt spectrum parameters
c Point detector at x=100 cm
F5:N  100 0 0  0.5                                 $ Detector location, R=0.5 cm
c Dose conversion using ANSI/ANS-6.1.1-1977 flux-to-dose factors
DE5   1E-10 1E-8 1E-7 1E-6 1E-5 1E-4 1E-3         $ Energy bins (MeV)
      0.01 0.1 0.5 1.0 2.0 5.0 10.0 14.0 20.0
DF5   3.67E-6 3.67E-6 4.46E-6 4.54E-6 4.18E-6     $ Flux-to-dose (rem/h per n/cm^2/s)
      3.76E-6 3.56E-6 2.17E-5 9.26E-5 1.32E-4
      1.43E-4 1.42E-4 1.27E-4 1.03E-4 9.24E-5
c Termination
NPS   10000000

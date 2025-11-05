CSEWG: ORNL-6  1.0253 g/l Unreflected 27.24" Sphere; U233-SOL-THERM-001 #2
 1 1 0.10016 -1     $ Spherical Solution U(NO3)2-H2O
 2 2 0.060275 1 -2  $ Spherical Shell of Al-1100
 3 0 2
 
 1 so 34.595    $ Inner Radius of Al-1100 Sphell
 2 so 34.915    $ Outer RAdius of Al-1100 Sphell

mode n
imp:n 1 1 0
kcode 10000 1. 100 600
sdef pos 0.0 0.0 0.0 rad d1
sc1 Spherical Source
si1 34.595
read file=m-cards-endf71
totnu
c  print
prdmp  999999  999999  1  1  999999

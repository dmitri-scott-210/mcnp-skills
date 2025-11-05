 PU-MET-FAST-008  case 2  THOR  Plutonium sphere reflected by thorium
1         1        0.039454        -1        $ Pu Sphere
2         2        0.030054         1   -2   $ Cylindrical Th Reflector
3         0                         2
 
1         sph     0.0   0.0   0.0    5.31
2         rcc     0.0   0.0 -26.67   0.0  0.0  53.34   26.67
 
kcode    10000    1.0   100   600
imp:n     1.0    1.0    0.0
totnu
sdef   cel=1  erg=d1
sp1    -3
vol        627.15 118565.35      0.0
area       354.32      0.0    8938.32   2234.58    2234.58
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999

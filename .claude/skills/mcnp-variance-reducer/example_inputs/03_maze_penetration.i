Case Study: photons in a maze environment
c
c ***** CELLS *****
c
 1  0        102 -103  203 -204  302 -303      $ far door (exit)
 2  0        103 -104  203 -206  302 -303      $ room center
 3  0        104 -105  205 -206  302 -303      $ near door (entrance)
c
 4  1  -2.3  104 -105  203 -205  302 -303
 5  1  -2.3  102 -105  202 -203  302 -303
 6  1  -2.3  102 -103  204 -206  302 -303
 7  1  -2.3  102 -105  206 -207  302 -303
c
11  0        101 -102  203 -204  302 -303      $ far door (exit outer)
13  0        105 -106  205 -206  302 -303      $ near door (entrance outer)
c
c --------------------------------------------------------------------
c  Use next for thick walls
 14  2  -2.3  105 -106  202 -205  302 -303
 15  2  -2.3  101 -106  201 -202  302 -303
 16  2  -2.3  101 -102  202 -203  302 -303
 17  2  -2.3  101 -102  204 -207  302 -303
 18  2  -2.3  101 -106  207 -208  302 -303
 19  2  -2.3  105 -106  206 -207  302 -303
c
31  2  -2.3  101 -106  201 -208  306 -302      $ floor
32  2  -2.3  101 -106  201 -208  303 -305      $ roof
c
90  0       -400 (-101:106:-201:208:-306:305)  $ outside room
91  0        400                               $ outside world
c
c --------------------------------------------------------------------
c  Use next for NO thick walls
c 14  0        105 -106  202 -205  302 -303
c 15  0        101 -106  201 -202  302 -303
c 16  0        101 -102  202 -203  302 -303
c 17  0        101 -102  204 -207  302 -303
c 18  0        101 -106  207 -208  302 -303
c 19  0        105 -106  206 -207  302 -303
c
c 31  1  -2.3  101 -106  201 -208  301 -302      $ floor
c 32  1  -2.3  101 -106  201 -208  303 -304      $ roof
c
c 90  0       -400 (-101:106:-201:208:-301:304)  $ outside room
c 91  0        400                               $ outside world
c
c ***** END CELLS *****

c ***** SURFACES *****
c
101  px -160
102  px -105
103  px -100
104  px  100
105  px  105
106  px  160
c
201  py -410
202  py -355
203  py -350
204  py -250
205  py  -50
206  py   50
207  py   55
208  py  110
c
211  py   15   $ tally segmenting surface
212  py  -15   $ tally segmenting surface
213  py -315   $ tally segmenting surface
214  py -285   $ tally segmenting surface
c
301  pz   -5
302  pz    0
303  pz  250
304  pz  255
305  pz  310
306  pz  -60
c
311  pz   50   $ tally segmenting surface
312  pz  100   $ tally segmenting surface
c
400  s  0  -175  127  500
c
c ***** END SURFACES *****

c ***** DATA CARDS *****
c
mode p
phys:p  0.01    1  1          $ 
cut:p   J    0.01  0          $ 10 keV cutoff; analog capture
imp:p   1 17R 0
c
c Materials
c
c ANSI/ANS 6.6.1-1987 Concrete Composition
m1    1000 7.86e+21  
      8000 4.38e+22
     11000 1.05e+21
     12000 1.40e+20
     13000 2.39e+21
     14000 1.58e+22
     19000 6.90e+20
     20000 2.92e+21
     26000 3.10e+20
c
c ANSI/ANS 6.6.1-1987 Concrete Composition
m2    1000 7.86e+21  
      8000 4.38e+22
     11000 1.05e+21
     12000 1.40e+20
     13000 2.39e+21
     14000 1.58e+22
     19000 6.90e+20
     20000 2.92e+21
     26000 3.10e+20
c
c Dry Air
m3    7000 -0.755
      8000 -0.232
     18000 -0.013
c
sdef  par=2 pos=130 0 100  erg=0.6616  dir=d1  vec= -1 0 0
si1   h -1 0 1
sp1   d  0  0.5  0.5
sb1   d  0   1    10
c
f4:p   1
fs4    -213 214 -311 312 T
sd4     4.375e+4  4.375e+4  7.5e+3  2.25e+4  7.5e+3  1.25e+5
fm4     8.639e+4  2  -5  -6  $ multiplier for CS-137 R/hr per Curie
fc4     R/hr per Curie at maze exit
tf4   3J 5
c
f14:p  3
fs14   -212 211 -311 312 T
sd14    4.375e+4  4.375e+4  7.5e+3  2.25e+4  7.5e+3  1.25e+5
fm14    8.639e+4  2  -5  -6  $ multiplier for CS-137 R/hr per Curie
fc14    R/hr per Curie at maze entrance
tf14  3J 5
c
nps 10000000
prdmp 1e+9  1e+9
c
print
  






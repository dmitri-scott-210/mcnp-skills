<!-- image -->

American NuclearSociety

ISSN: 0029-5639 (Print) 1943-748X (Online) Journal homepage: www.tandfonline.com/journals/unse20

## Reactor Physics Benchmark of the First Criticality in the Molten Salt Reactor Experiment

Dan Shen, Germina Ilas, Jeffrey J. Powers &amp; Massimiliano Fratoni

To cite this article: Dan Shen, Germina Ilas, Jeffrey J. Powers &amp; Massimiliano Fratoni (2021) Reactor Physics Benchmark of the First Criticality in the Molten Salt Reactor Experiment, Nuclear Science and Engineering, 195:8, 825-837, DOI: 10.1080/00295639.2021.1880850

To link to this article:

https://doi.org/10.1080/00295639.2021.1880850

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

© 2021 The Author(s). Published with license by Taylor &amp; Francis Group, LLC.

- [x] Published online: 31 Mar 2021. 曲

Submit your article to this journal

Article views: 3385

View related articles

View Crossmark data

Citing articles: 8 View citing articles

CrossMark

## Nuclear Science and Engineering

<!-- image -->

<!-- image -->

## Reactor Physics Benchmark of the First Criticality in the Molten Salt Reactor Experiment

Dan Shen, a Germina Ilas, b Jeffrey J. Powers, b and Massimiliano Fratoni a *

a University of California, Berkeley, California

b Oak Ridge National Laboratory, Oak Ridge, Tennessee

Received December 6, 2020

Accepted for Publication January 20, 2021

Abstract -The deployment of molten salt reactors requires validation of the computational tools used to support the licensing process. The Molten Salt Reactor Experiment (MSRE), built and operated in the 1960s, offers a unique inventory of experimental data for reactor physics benchmarks. The first benchmark based on the  MSRE  appeared  in  'The  2019  Edition  of  the  IRPhEP  [International  Reactor  Physics  Experiment Evaluation  Project]  Handbook.'  The  benchmark  refers  to  the  first  criticality  experiment  at  zero  power, stationary salt, and uniform temperature with 235 U fuel. Simulations carried out for the developed benchmark model with the Monte Carlo code Serpent and ENDF/B-VII.1 cross-section library found that the calculated neutron  multiplication  is  1.02132  (±3  pcm)  and  that  the  combined  bias  of  the  model  and  experimental uncertainty is below 500 pcm. Such discrepancy between the experimental and calculated keff is not uncommon in  benchmarks  for  graphite-moderated  systems.  The  model  created  through  this  effort  paves  the  way  to additional benchmarks targeting reactor physics quantities of interest beyond multiplication factor.

Keywords -Molten salt reactor, criticality, benchmark.

Note -Some figures may be in color only in the electronic version.

## I. INTRODUCTION

In  recent  years  molten  salt  reactors  (MSRs)  have received worldwide attention from private and public entities seeking to commercialize such reactor concepts. A crucial step toward commercialization is to build confidence in the computational tools that are used not only to design  these  systems  but  also  to  prove  their  safety  case. Benchmarks  for  validation  of  reactor  physics  codes  are, arguably, the most challenging as they require critical facilities that are lengthy and costly to build. In this regard, the Molten Salt Reactor Experiment (MSRE), built and

*E-mail: maxfratoni@berkeley.edu

This  is  an  Open  Access  article  distributed  under  the  terms  of  the Creative Commons Attribution-NonCommercial-NoDerivatives License  (http://creativecommons.org/licenses/by-nc-nd/4.0/),  which permits  non-commercial  re-use,  distribution,  and  reproduction  in any  medium,  provided  the  original  work  is  properly  cited,  and  is not altered, transformed, or built upon in any way.

operated at the Oak Ridge National Laboratory (ORNL) in the 1960s, offers a unique inventory of experimental data. 1 Although researchers have used data from the MSRE in the past to assess results from simulations, up to this time, no official benchmark was available in 'The 2019 Edition of the  IRPhEP  Handbook' 2 (hereinafter  referred  to  as  the IRPhEP Handbook). The scope of the International Reactor Physics Experiment Evaluation Project (IRPhEP) is  to  collect  standardized  reactor  physics  benchmark  data sets of the highest quality as certified by a group of international experts that peer-reviews each set. In order to fill the  gap  in  the  IRPhEP,  the  University  of  California, Berkeley (UC Berkeley), and ORNL have joined forces to retrieve information from the MSRE and to create the first MSR-related  benchmark  that  appeared  in  the  IRPhEP Handbook.

This  paper  documents  the  steps  and  the  assumptions made in the process of creating a benchmark model of the MSRE first criticality experiment with 235 U fuel, conducted in June 1965 (Ref. 3). A description of the MSRE and the

<!-- image -->

procedure that was followed to achieve criticality are provided in Secs. II and III, respectively. Section IV describes the  benchmark  model,  and  Sec.  V  reports  the  results obtained from numerical simulations of the model.

## II. MSRE DESCRIPTION

The MSRE was a molten salt liquid fuel critical facility  operated  at  ORNL  from  1965  to  1969.  As  the  first large-scale, long-term, high-temperature testing performed for a fluid fuel salt, a graphite moderator, and a then-new nickel-based alloy  (named INOR-8) in a reactor environment, the MSRE purpose was to demonstrate key features of  the  molten  salt  liquid  fuel  concept  and  to  prove  the practicality of the MSR technology. 1 The MSRE primary system included a reactor vessel, a fuel circulating pump, a fuel heat exchanger, and an interconnecting piping. Fuelbearing  salt  circulated  through  these  components  at  an average nominal rate of 4.54 m 3 /min achieving criticality and heating up in the reactor core. The primary system was housed in a carbon steel vessel named the reactor cell. The reactor vessel was further confined within a thermal shield structure.  This  section  provides  a  brief  description  of  the geometry,  dimensions,  and  materials  of  the  reactor  core, vessel, and thermal shield (more detailed information can be  found  in  Ref.  1).  Components  outside  of  the  thermal shield were believed to have no impact on the benchmark and were not considered.

## II.A. Reactor Vessel

A  cutaway  drawing  of  the  MSRE  reactor  vessel  is shown in Fig. 1. The reactor vessel has an inner diameter of  147.32  cm  and  a  height  of  233.90  cm.  The  fuel  salt enters the flow distributor through the fuel inlet, arranged tangentially to the top of the vessel. The flow distributor is  half-circular  in  cross  section  with  an  inside  radius  of 10.16 cm. The fuel is distributed evenly around the circumference of the vessel while passing the flow distributor and then flows turbulently downward in a spiral path through a 2.54-cm-wide annulus between the vessel wall and the  core  can.  The  salt  loses  its  rotational  motion  in the 48 straightening vanes in the lower plenum and flows upward through the graphite matrix in the core can. The vessel has two torispherical domes with 147.32-cm inner diameter and 2.54-cm thickness as the upper plenum and lower plenum. The core can inside the vessel has an inner diameter of 140.97 cm and a thickness of 0.635 cm. The core can is supported-and also held down when salt is in the reactor-by a ring at the top that is bolted to 36 lugs

<!-- image -->

Fig. 1.  MSRE reactor vessel. 1

<!-- image -->

welded to the inside wall of the reactor vessel. The can, in turn, supports the graphite in the reactor. 1

## II.B. Reactor Core

The reactor core structure is an assembly of vertical graphite stringers with a 5.08 × 5.08-cm cross section as shown  in  Fig.  2.  Fissioning  occurs  when  the  fuel  salt flows  through  the  channels  formed  by  grooves  in  the four sides on the stringers. These channels are 1.016 × 3.048 cm with round corners of radius 5.08 cm. The  graphite stringers are  170.03  cm  long  and  are mounted in a vertical close-packed array. There is a  total  of  1140  equivalent  full-size  passages,  counting fractional  sizes.  The  dimensions  of  the  flow  channel provide  a  large  enough  passage  to  avoid  blockage  by small pieces of graphite and correspond to a nearly optimum fuel-to-graphite ratio in the core.

The MSRE graphite has an average density of 1.86 g/ cm 3 ,  which  is  lighter  than  the  salt  density,  which  is approximately  2.3275  g/cm 3 .  When  not  buoyed  up  by being  immersed  in  the  fuel  salt,  the  vertical  graphite stringers rest on a lattice of graphite blocks, with a 2.54 × 4.1275-cm cross section, that is laid horizontally in  two  layers  at  right  angles  to  each  other.  Holes  in  the

Fig.  2.  Graphite  stringers  and  their  arrangement  in  the MSRE core. 1

<!-- image -->

lattice  blocks  (2.642-cm  diameter)  house  the  2.54-cmdiameter doweled section at the lower end of each stringer. The upper horizontal surface of the vertical graphite stringers  is  tapered  to  ensure  that  no  salt  remains  on  it after drainage (Fig. 2).

## II.C. Control Rod and Sample Basket

Four channels, three hosting control rod thimbles and one  hosting  baskets  containing  graphite  and  INOR-8 samples,  are  arranged  equidistantly  near  the  center  of the  core  in  place  of four graphite  stringers,  as  shown  in Fig. 3. One of the objectives of the MSRE was to investigate  the  behavior of  bare graphite in the reactor environment.  Thus,  the  reactor  was  designed  for  periodic removal of graphite  specimens  from  the  sample  baskets near  the  center  of  the  core.  There  are  three  identical sample baskets mounted vertically, and each basket features  a  0.079-cm-thick  INOR-8  plate  and  0.238-cmdiameter  holes  and  contains  four  samples  (0.635  cm  in diameter  and  167.64  cm  in  length)  of  INOR-8  and  five samples of graphite (0.635 × 1.1938 cm with a length of 167.64 cm).

The control rod thimbles have a wall tubing of 5.08cm outer diameter and 0.1651-cm thickness. The control rods are segmented (see Fig. 4) to provide the flexibility needed  to  pass  through  the  bends  in  the  control  rod thimbles.  The  poison  material  is  in  the  form  of  thin-

Fig.  3.  Control  rod  and  sample  basket  layout  at  the center of the core. 1

<!-- image -->

Fig. 4.  Cutaway of an MSRE control element. 1

<!-- image -->

walled,  ceramic  cylinders,  and  the  ceramic  cylinder  is a  mixture  of  70  wt%  Gd2O3 and  30  wt%  Al2O3.  Each control element contains three ceramic cylinders, canned in  an  Inconel  shell.  Each  control  rod  is  made  of  38 elements  for  a  total  length  of  the  poison  section  of 150.774  cm.  The  segments  are  threaded,  beadlike,  on a  1.905-cm  outer  diameter  ×  1.5875-cm  inner  diameter helically wound, flexible stainless steel. Two 0.3175-cmdiameter braided Inconel cables run through this hose to restrain it from stretching when dropped in free fall. This hose passes upward through the thimble to the positioning chain on the control rod drive mechanism. The reference  system  used  to  determine  control  rod  position  is shown  in  Fig.  5.  In  this  system,  zero  corresponds  to a fully inserted rod when driven in whereas a fully withdrawn rod is positioned at 51 in.

AUGUST 2021

<!-- image -->

Fig.  5.  Elevations  of  core  components  and  control  rod position reference system. 3

<!-- image -->

## II.D. Thermal Shield

The reactor vessel is installed in a Type 304 stainless steel thermal shield that supports the vessel and forms the outer  wall  of  the  reactor  furnace.  The  shield  has  an approximate  outer  diameter  of  317.5  cm,  an  inner  diameter  of  236.22  cm,  and  a  height  of  383.54  cm.  The inside  of  the  thermal  shield  is  lined  with  15.24  cm  of high-temperature  insulation  (vermiculite).  The  reactor vessel is supported from the top removable cover of the thermal shield.

## III. FIRST CRITICALITY EXPERIMENT

In 1965, a first criticality experiment was conducted at the MSRE with the purpose of establishing the critical concentration of 235 U under the simplest possible conditions,  that  is,  isothermal  core,  stationary  fuel  salt,  and fully withdrawn control rods. To start, carrier salt (65LiF-30BeF2-5ZrF4)  and  depleted uranium  eutectic (73LiF-27UF4) were loaded in the drain tanks and circulated in the primary loop for 10 days. Then, increments of enriched uranium concentrate (93% 235 U) were

<!-- image -->

progressively  added  to  the  salt,  and  the  approach  to critical  concentration  was  monitored  by  measuring  neutron source multiplication. At first, kilogram quantities of 235 U were added to the salt in the drain tanks. Then, the salt  was  transferred  to  the  core,  and  the  neutron  multiplication was measured. This process was repeated until the  salt  contained  approximately  98%  in  weight  of  the anticipated critical mass. The remainder 235 U was added in  85-g  batches  through  the  sampler-enricher.  Four  neutron counting channels were used during the experiment: two  fission  chambers  in  the  instrument  shaft,  a  BF3 chamber in the instrument shaft, and another BF3  chamber in the thermal shield.

On  June  1,  1965,  at  approximately  6:00  p.m.,  the reactor reached the critical point with fuel salt stationary, two rods at fully withdrawn position (51 in.) and the other rod inserted at 3% of its integral worth (46.6 in.) (Ref. 3). Criticality was verified by leveling the power at a  successively  higher  level  with  the  same  rod  position. The actual system power was approximately 10 W. The corrected value of the book mass fraction of 235 U in the fuel salt was (1.408 ± 0.007) wt% considering the small amount of dilution of the fuel salt from residues of flush salt  left  in  freeze  valves  and  drain  tank  heels  when  the fuel salt was charged. The core temperature at the time of criticality was 911 K (1181°F) instead of 922 K (1200°F) as initially estimated. The fuel salt density was 2.3275 ± 0.0160 g/cm 3 , and its composition was 64.88 mol % LiF, 29.27 mol % BeF2, 5.06 mol % ZrF4, and 0.79 mol % UF4.

## IV. BENCHMARK MODEL

A high-fidelity benchmark model of the MSRE was created with the ultimate purpose of validating computational tools. Figures 6 and 7 provide an overview of the model, including axial location with respect to the bottom of  the  horizontal  graphite  lattice  and  radial  dimensions. The arrangement of the graphite stringers is disrupted in the center by three control rods and the sample baskets as shown in Fig.  8.  Additional  disruption  to  the  pattern  of the stringers occurs at the outer edge where partial stringers and partial channels are used and in the center of the core  where  stringers  are  shorter.  For  brevity,  these  and other details are not reported here, and readers interested in recreating the benchmark model should refer to Ref. 2 or Ref. 4 for a complete description.

The dimensions and materials for the horizontal and vertical  graphite  lattices,  control  rod  thimbles,  sample baskets, reactor vessel shell, flow distributor, and thermal

Fig.  6.  Horizontal  cross  section  of  the  MSRE  model  at 911  K.  The  cross  section  is  located  at  the  centerline  of the  flow  distributor  ( z =  145.396  cm  in  Fig.  7).  Image credit: David R. Sharp, Idaho National Laboratory.

<!-- image -->

Fig.  7.  Vertical  cross  section  of  the  MSRE  model  at 911 K. The cross section is offset by 5.08339 cm from the center of the graphite stinger lattice in order to show control rods. Location z = 0 corresponds to the bottom of the horizontal graphite lattice. Image credit: David R. Sharp, Idaho National Laboratory.

<!-- image -->

shield are those obtained from design data and blueprints as reported in Sec. II. The fuel inlet pipe, fuel outlet pipe, fuel outlet strainer, reactor access port, external loop outside  the  thermal  shield,  and  base  for  the  thermal  shield

Fig.  8.  Horizontal  cross  section  of  the  core  center  with control  rods  and  sample  baskets.  Image  credit:  David R. Sharp, Idaho National Laboratory.

<!-- image -->

were  neglected.  The  bias  from  neglecting  these  components in the benchmark was evaluated by creating a fully detailed  model  (Fig.  9)  that  contains  the  fuel  inlet  pipe, fuel outlet pipe, fuel outlet strainer, reactor access port, and thermal shield base, and the bias on keff was calculated to be (-22 ± 5) pcm.

There are other simplifications in the MSRE benchmark model that are believed to have no significant effect on keff . The lower head of the reactor vessel is simplified as a homogeneous mixture of fuel salt and INOR-8 with a volume ratio of 90.8:9.2 according to Ref. 5. The upper head  of  the  reactor  vessel  is  simplified  as  a  pure  salt region.  The  insulation  layer  and  thermal  shield  are  also simplified as a homogeneous mixture.

The  dimensions  reported  in  the  design  documents and in the blueprints are as built, thus at room temperature.  During  the  critical  experiment  the  registered  temperature  was  911  K;  therefore,  dimensional  changes  to graphite  and  metallic  components  in  the  reactor  vessel were applied assuming a thermal expansion coefficient of 1.5  ×  10 -6 ºF -1 for  graphite  and  of  7.8  ×  10 -6 ºF -1 for metallic  components. 6 It  was  assumed  that  the  reactor vessel freely expanded downward starting from the interface  between  the  outlet  pipe  and  the  upper  insulation layer.  The  horizontal  graphite  lattice  was  connected  to the vessel at its bottom ( z = 0 in Fig. 7), and the vertical graphite  stringers  were  held  by  the  horizontal  graphite lattice;  therefore,  to  account  for  thermal  expansion,  the horizontal graphite lattice was first moved together with

AUGUST 2021

<!-- image -->

Fig. 9.  (a) Horizontal cross section at z = 145.396 cm and (b) vertical cross section of the core offset by 5.08339 cm from the center of the fully detailed MSRE model.

<!-- image -->

the vessel and then thermally expanded upward. Finally, the thermally expanded vertical graphite stringers were placed above the horizontal graphite lattice. Table I reports hot and cold dimensions.

## V. RESULTS

The  benchmark  model  was  simulated using the Monte  Carlo  neutron  transport  code  Serpent  2  version 2.1.30  (Ref.  7)  with  the  ENDF/B-VII.1  cross-section library.  The  temperature  for  cross  sections  was  set  at 900 K, and it was preprocessed for Doppler broadening to  911  K  by  Serpent  2.  Thermal  scattering  laws  were applied  to  carbon  in  graphite  (with  a  temperature  of 911 K in the core and 305 K in the thermal shield) and hydrogen  in  water  (with  a  temperature  of  305  K  in  the thermal shield). For the thermal scattering laws, Serpent 2 interpolates  between  the  two  closest  available  temperature libraries.

The experimental keff is 1.0, and the assessed bias of the  benchmark  model  from  simplifications  is  -22  pcm; thus, the  expected keff for  the  benchmark  model  is 0.99978,  ±420  pcm  uncertainty  as  reported  below.  The keff calculated by Serpent is 1.02132 ± 0.00003, which is 2.154% larger than the experimental and the benchmark model values. The complexity of the model and the fact that  it  was  reconstructed  more  than  50  years  after  the experiment  based  on  the  publicly  available  documents make it difficult to identify the source(s) of such discrepancy. It can be noticed that keff is particularly sensitive, as expected, to the main core components, which are salt

TABLE I As-Built Cold Dimensions and Thermally Expanded Hot Dimensions

| Dimension                                                                                                                                                                                                                                                                                                                                | Cold (293 K)                                                                | Hot (911 K)                                                                 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Graphite lattice radius (cm) Core can inner radius (cm) Core can outer radius (cm) Reactor vessel inner radius (cm) Reactor vessel outer radius (cm) Graphite stringer width (cm) Fuel channel width (cm) Fuel channel length (cm) Graphite stringer height (cm) Total height of the vessel (cm) Length of the control rod inserted (cm) | 70.168 70.485 71.120 73.660 76.200 5.075 1.016 3.048 170.027 269.771 76.414 | 70.285 71.097 71.737 74.299 76.862 5.084 1.018 3.053 170.311 272.113 77.077 |

<!-- image -->

and graphite. The salt composition is particularly challenging  to  determine  as  obtained  by  successive  additions  of different  compositions,  and  changes  in  salt  composition would  largely  impact keff (further  details  are  discussed later in this section). At the time the benchmark was prepared, thermal scattering kernel data for salt were not available, although the impact of that is likely to be much smaller than the observed difference.

The impact of the nuclear data was evaluated comparing the ENDF/B-VII.1 and JENDL-4.0 cross-section libraries.  The  difference  in keff between  the  two  is (71  ±  5)  pcm  (Table  II).  In  addition,  the  eigenvalue for the MSRE core calculated using the ENDF/B-VII.1 data  is  (178  ±  5)  pcm  lower  if  only  the  carbon  cross section  is  replaced  with  JENDL-4.0  data.  The  difference in keff between the two is (71 ± 5) pcm (Table II). In  addition,  the  eigenvalue  for  the  MSRE  core  calculated using ENDF/B-VII.1 data is (178 ± 5) pcm lower if only the carbon cross section is replaced with JENDL-4.0 data.

It is also observed that other benchmarks of graphitemoderated  systems  currently  included  in  the  IRPhEP

Handbook  report  calculated keff 1%  to  2%  larger  than the  experimental value  as  shown  in  Table  III.  Such  discrepancy is possibly due to uncertainties in the impurity content  of  graphite  or  to  the  accuracy  of  the  neutron capture cross section of carbon.

## V.A. Experimental and Data Uncertainties

All input data to the benchmark model are characterized by their own uncertainty that propagates to the multiplication factor. In order to assess this uncertainty, keff was calculated perturbing each parameter i within its uncertainty range, in both positive and negative directions, and the corresponding Δ ki was determined as follows:

<!-- formula-not-decoded -->

where ui is  the  standard uncertainty of parameter i and ð k δ i GLYPH<0> kref Þ is  the  change  in keff induced  by  change  δ xi on  parameter i .  When  there  was  a  difference  between the  absolute  values  of  Δ ki calculated  from  the  positive

TABLE II Expected and Calculated Benchmark Model keff Values

| Case                                               | k eff                                                 | 100 (C-E)/E a   |
|----------------------------------------------------|-------------------------------------------------------|-----------------|
| Benchmark SERPENT, ENDF/B-VII.1 SERPENT, JENDL-4.0 | 0.99978 ± 0.00420 1.02132 ± 0.00003 1.02061 ± 0.00003 | - 2.154 2.083   |

a C = calculated value. E = experimental value.

TABLE III Difference Between Calculated and Expected keff for Selected Full-Core Benchmarks of Carbon-Moderated Systems Included in the IRPhEP Handbook*

| Benchmark Model                                                       | Code Library                                                         | Expected k eff              | Calculated k eff                                                        | 100 (C-E)/E a       |
|-----------------------------------------------------------------------|----------------------------------------------------------------------|-----------------------------|-------------------------------------------------------------------------|---------------------|
| HTR10 high-fidelity HTR10 simplified HTTR fully loaded PROTEUS Core 3 | MCNP5 ENDF/B-VI MCNP5 ENDF/B-VI MCNP5 END/B-VII.0 MCNP5 ENDF/B-VII.0 | 1.0000 1.0131 1.0025 0.9999 | 1.01190 ± 0.00021 1.02500 ± 0.00021 1.02310 ± 0.00010 1.00888 ± 0.00007 | 1.19 1.18 2.03 0.90 |

*Reference 2.

a C = calculated value. E = experimental value.

AUGUST 2021

<!-- image -->

TABLE IV Individual and Total Uncertainties on keff

| Item                                   | Nominal and Bounding Values                                                        |   ∆ k i (pcm) |
|----------------------------------------|------------------------------------------------------------------------------------|---------------|
| Graphite density                       | 1.86, 1.83 to 1.87 g/cm 3                                                          |         334   |
| Fuel salt density                      | (2.3275 ± 0.0160) g/cm 3                                                           |         103   |
| Be mass in carrier salt                | (309.62 ± 5.00) kg                                                                 |           8   |
| Zr mass in carrier salt                | (541.36 ± 5.00) kg                                                                 |          12   |
| 235U mass fraction in the salt         | (1.409 ± 0.007) wt%                                                                |          81   |
| 234U mass fraction in the salt         | (0.014 ± 0.007) wt%                                                                |          74   |
| 236U mass fraction in the salt         | (0.006 ± 0.006) wt%                                                                |          17   |
| INOR-8 density                         | (8.7745 ± 0.0200) g/cm 3                                                           |           3   |
| Graphite core height                   | (166.724 ± 1.000) cm                                                               |          21   |
| Graphite core radius                   | (70.285 ± 0.200) cm                                                                |           4   |
| Fuel channel width                     | (1.0160 ± 0.0127) cm                                                               |          51   |
| Fuel channel length                    | (3.0480 ± 0.0127) cm                                                               |          23   |
| 6Li enrichment                         | (0.005 ± 0.001) at. %                                                              |         172   |
| Boron concentration in graphite        | (0.000 080 ± 0.000 008) wt%                                                        |          17   |
| Temperature of thermal shield          | 305 K, 600 K                                                                       |           2   |
| Temperature of fuel salt               | (911 ± 1) K                                                                        |           6   |
| Temperature of graphite                | (911 ± 1) K                                                                        |           1   |
| Height vertical section of bottom head | (6.475 ± 1.000) cm                                                                 |           9   |
| Outlet pipe thickness                  | (2.511 ± 0.250) cm                                                                 |           3   |
| Outlet pipe height                     | (36.180 ± 1.000) cm                                                                |           4   |
| Distributor thickness                  | (0.826 ± 0.080) cm                                                                 |           3   |
| Sample basket outer diameter           | (5.4287 ± 0.0127) cm                                                               |           0   |
| Sample basket gap                      | 0, 0.0127 cm                                                                       |           5   |
| Cell atmosphere gas composition        | Mass fraction versus atom fraction                                                 |           0   |
| INOR-8 composition (C mass fraction)   | 0.06%, 0.08%                                                                       |           5   |
| Mo mass fraction in INOR-8             | (17.0 ± 0.5) wt%                                                                   |          12   |
| Cr mass fraction in INOR-8             | (7.0 ± 0.5) wt%                                                                    |           5   |
| Fe mass fraction in INOR-8             | (5.0 ± 0.5) wt%                                                                    |           4   |
| Impurities in salt                     | Fe: 162 ± 65 ppm, Cr: 28 ± 7 ppm                                                   |          12   |
| Helium void in salt                    | Ni: 30 ± 20 ppm, O: 490 ± 49 ppm 0, 0.076 vol %                                    |           5   |
| Salt absorption in graphite            | 0, 0.0010 vol %                                                                    |           2   |
| Hf in Zr                               | 50 ppm, 0 ppm                                                                      |          12   |
| Impurities in graphite                 | Ash: (0.00050 ± 0.00005) wt% V: (0.00090 ± 0.00009) wt% S: (0.00050 ± 0.00005) wt% |           4   |
| Graphite stringer width                | 5 : 07492 þ 0 : 0000 GLYPH<0> 0 : 0127 GLYPH<0> � cm                               |          13   |
| Poison density                         | (5.873 ± 0.020) g/cm 3                                                             |           0.5 |
| Gd 2 O 3 mass fraction                 | (70 ± 1) wt%                                                                       |           0.6 |
| Control rod position                   | (118.364 ± 0.127) cm                                                               |           0.7 |
| Regulating rod                         | Rod 1, rod 2, or rod                                                               |           0   |
| Graphite thermal expansion coefficient | 3 (1.5 ± 0.2) × 10 -6 ◦ F -1                                                       |          18   |
| INOR-8 thermal expansion coefficient   | (7.8 ± 0.2) × 10 -6 ◦ F -1                                                         |          17   |
| Measurement uncertainty in k eff       | -                                                                                  |          10   |
| Total (root-mean-square)               | -                                                                                  |         420   |

and  negative  perturbations  of  a  parameter,  the  larger one  was  selected  and  shown  in  Table  IV.  For  this evaluation, all the parameters were considered uncorrelated,  and  the  total  standard  uncertainty  of keff was calculated  as  the  root-mean-square  of  all  Δ ki .

<!-- image -->

The  (1σ)  uncertainty of the  experimental keff is 420  pcm,  as  shown  in  Table  IV.  Graphite  density,  fuel salt density, and 6 Li enrichment are the main contributors.

The effect of the temperature of the thermal scattering data was evaluated as shown in Table V. It was found

TABLE V Comparison of keff with Various Thermal Scattering Cross-Section Temperatures

| Carbon in Graphite   | Carbon in Thermal Shield   | Hydrogen in Thermal Shield   | k eff                                                 | Difference (pcm)   |
|----------------------|----------------------------|------------------------------|-------------------------------------------------------|--------------------|
| 800 K 911 K a 1000 K | 296 K 305 K a 400 K        | 293.6 K 305 K a 350 K        | 1.02723 ± 0.00010 1.02132 ± 0.00003 1.01640 ± 0.00010 | 591 0 -492         |

a Thermal scattering cross section interpolated by Serpent based on available data at 800 K and 1000 K.

that  a  100  K  change  in  the  temperature  of  the  thermal scattering  data  of  carbon  in  graphite  results  in  more  than 500 pcm difference in keff ; therefore, the use of an accurate temperature library is recommended.

The salt composition used in the benchmark model, reported  in  Ref.  8,  was  obtained  recording  the  amount and the composition of each salt addition into the primary loop and was checked and corrected by the experimenters to  be  self-consistent.  Nevertheless,  Ref.  8  reports  two additional salt compositions. One was obtained from chemical  and  mass  spectroscopy  analysis  at  the  time  of criticality, and the other was the anticipated composition with no correction. The effect on keff of these alternative compositions was evaluated keeping throughout the same enrichment  of  all  uranium  isotopes,  the  same  impurity concentration, and the same total salt density (Table VI). It was found that the results from chemical analysis show bias  in  the  determination  of  lithium  and  beryllium  concentrations.  Such  measurement  bias  from  the  chemical analysis  was  noticed  on  the  flush  salt. 8 Flush  salt  was used initially to flush the system before loading fuel salt and  later  on  before  and  after  maintenance  periods.  The nominal composition of the flush salt was LiF-BeF2  (66 to  34  mol  %);  however,  the  composition  determined  by chemical analysis was LiF-BeF2  (63.560 ± 0.005) mol % to (36.440 ± 0.005) mol %. The anticipated composition is very similar to the one selected for the benchmark, but the  latter  provides  the  best  agreement  with  the  recorded 235 U  mass  fraction:  1.409%  versus  (1.408  ±  0.007)% recorded. 3 Such  metric  is  considered  the  most  reliable as the overall scope of the experiment was to determine the critical amount of 235 U.

Sensitivity  coefficients  of keff to  uncertainties  in  the nuclear data (Table VII) were calculated using Serpent 2 (Ref.  9),  and  the  uncertainty  on keff due  to  the  crosssection  data  was  estimated  combining  the  sensitivity coefficients  with  covariance  data  [56-group  covariance matrices  were  obtained  from  SCALE  6.2  (Ref.  10)] through the so-called sandwich rule. The total uncertainty was  estimated  to  be  664  pcm,  and  the  most  important uncertainty contributors are listed in Table VIII.

## V.B. Simplified Model

Given the complexity of the MSRE model, it might be  challenging  for  some  reactor  physics  codes  to  reproduce  the  benchmark  model  in  full  details;  therefore, reference keff values  were  also  computed  for  models with various simplifications:

1. The half-torus flow distributor, located at the top of the vessel connecting the fuel salt inlet, was removed (Fig. 10).

TABLE VI Comparison of keff with Different Fuel Salt Compositions*

| Salt Composition   |   Lithium (wt%) |   Beryllium (wt)% |   Zirconium (wt%) |   Uranium (wt%) |   Fluorine (wt%) | k eff             |
|--------------------|-----------------|-------------------|-------------------|-----------------|------------------|-------------------|
| Benchmark          |          10.957 |             6.349 |            11.101 |           4.495 |           67.027 | 1.02132 ± 0.00003 |
| Chemical analysis  |          10.327 |             6.695 |            11.016 |           4.44  |           67.451 | 1.02248 ± 0.00010 |
| Anticipated        |          10.97  |             6.324 |            10.972 |           4.641 |           67.023 | 1.02595 ± 0.00010 |

*0.071 wt% impurities in all cases.

AUGUST 2021

<!-- image -->

TABLE VII Sensitivity Coefficients for keff from Cross-Section Data Uncertainties

| Nuclide                                                                  | Total ð× 10 GLYPH<0> 5 Þ                                        | Elastic Scattering ð× 10 GLYPH<0> 5 Þ                | Neutron Capture a ð× 10 GLYPH<0> 5 Þ                                  | Fission ð× 10 GLYPH<0> 5 Þ      |
|--------------------------------------------------------------------------|-----------------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------------------------|---------------------------------|
| 6 Li 7 Li 9 Be 90 Zr 91 Zr 92 Zr 94 Zr 96 Zr 19 F nat C 10 B 235 U 238 U | -1430 770 2920 3 -520 -16 -36 -86 8410 51 400 -650 22 990 -8470 | 0.04 2010 3250 50 150 130 5 2 8080 39 210 0.2 47 610 | -1430 -1380 -340 -64 -670 -160 -54 -89 -1070 -1760 -650 -14 080 -9170 | - - - - - - - - - - - 37 020 63 |

a As defined in Serpent includes all reactions with no neutron yield.

TABLE VIII Uncertainties on keff due to Cross-Section Data Uncertainties

| Reaction                                                                                                                        | Uncertainties (pcm)                   |
|---------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| 235 U, v Carbon, elastic 235 U, χ 7 Li( n ,γ) 235 U( n ,γ) 19 F elastic × 235 U( n,γ ) 235 U( n,f ) 58 Ni( n ,γ) 19 F inelastic | 373 264 257 197 172 150 128 120 97 96 |

2. The top and bottom heads of the reactor vessel  were assumed flat rather than torispherical domes, and  the total height of  the  vessel  was  conserved (Fig.  11).
3. The sample baskets were removed, and the housing channel was filled with graphite (Fig. 12b).
4. Materials  in  the  sample  basket  were  homogenized  while  the  basket  outer  radius  and  the  channel shape were kept unchanged (Fig. 12c).
5. Salt channels in between stringers were modeled as circular with 0.957-cm radius in order to maintain the same cross-sectional area as the reference channels (Fig. 13b).
6. Salt channels in between stringers were modeled as  rectangular  channels  (Fig.  13c)  with  the  long  side equal  to  the  length  of  the  long  side  of  the  reference

<!-- image -->

Fig. 10.  Vertical cross section of the MSRE model without the distributor (at y = 0).

<!-- image -->

Fig. 11.  Vertical cross section of the MSRE model with flat top and bottom sections (at y = 0).

<!-- image -->

channels (3.048 cm) and the half-length of the short side (0.472 cm)  adjusted to preserve the channel crosssectional area.

7. The  thermal  shield  and  insulation  layer  were removed from the model (see Fig. 14).

Table IX reports the calculated keff for the simplified models illustrated above.

## VI. CONCLUSIONS

This paper documents the effort of developing a  high-quality reactor physics benchmark for the MSRE that  has  been  reviewed  and  approved  by  the  IRPhEP committee  to  be  included  in  the  IRPhEP  Handbook. A  highly  detailed  benchmark  model  of  the  MSRE  was created collecting data from publicly available documents written both before and after the facility was operated. In particular,  the  benchmark  aimed  at  reproducing  the  first criticality  experiment  with 235 U  fuel,  conducted  at  zero power  with  stationary  salt  and  uniform  temperature. Blueprints and design documents provided an abundance of information to build a model; nevertheless, it was not possible  to  establish  if  any  change  was  made  during

Fig. 12.  Comparison of models for the sample basket.

<!-- image -->

Fig. 13.  Comparison of models for the fuel channel.

<!-- image -->

AUGUST 2021

<!-- image -->

Fig. 14.  Vertical cross section of the MSRE model without thermal shield and insulation layer (at y = 0).

<!-- image -->

TABLE IX Calculated keff with Various Model Simplifications

| Case                                   | k eff             |   100( k eff - k ref )/ k ref a |
|----------------------------------------|-------------------|---------------------------------|
| No distributor                         | 1.02032 ± 0.00004 |                          -0.098 |
| Flat top and bottom heads              | 1.02380 ± 0.00004 |                           0.243 |
| Sample baskets replaced with graphite  | 1.03790 ± 0.00004 |                           1.623 |
| Homogeneous sample baskets             | 1.02094 ± 0.00003 |                          -0.037 |
| Circular fuel channels                 | 1.02450 ± 0.00003 |                           0.311 |
| Rectangular fuel channel               | 1.02151 ± 0.00004 |                           0.019 |
| No thermal shield and insulation layer | 1.01228 ± 0.00003 |                          -0.885 |

a kref ¼ 1 : 02132 × 0 : 00003.

actual construction. Furthermore, the documented dimensions are 'as built' that is at room temperature, but at the moment  of  criticality,  a  uniform  temperature  of  911  K

<!-- image -->

was  recorded.  In  the  benchmark  model,  the  best  effort was made to account for thermal expansion. Salt composition  is  largely  documented,  and  some  discrepancies exist and are even noted in documents of the time. Such a parameter is of the greatest impact on reactor physics, and  once  again,  the  best  effort  was  made  to  reconstruct the salt composition guided by the fact that the 235 U concentration was expected to be accurately reported as the main target of the criticality experiment.

The  benchmark  model  was  simulated  using  the Monte  Carlo  code  Serpent  2  with  the  nuclear  data library  ENDF/B-VII.1 in order to calculate the neutron multiplication  factor  as  well  as  bias  and  uncertainties related  to  the  model.  It  was  estimated  that  the  benchmark bias on keff , the error due to approximations in the model, is as little as (-22 ± 5) pcm whereas the uncertainty  due  to  uncertainties  in  the  input  parameters,  i.e., tolerance,  is  420  pcm.  The  computed  multiplication factor  is  2.154%  higher  than  the  experimental  one, which is a 5σ difference. The reason for such difference was difficulty in tracking; nevertheless, it was observed that similar large differences are reported in other benchmarks for graphite-moderated systems that appear in  the  IRPhEP  Handbook.  This  might  indicate  that further investigation is needed into graphite composition and carbon nuclear data.

This  benchmark  model  provides  the  foundation  to extend  MSRE  benchmarks  beyond  multiplication  factor and to include other quantities of interest such as reactivity  coefficients,  control  rod  worth,  reactivity  impact  of salt  motion,  etc.  An  effort  in  this  direction  is  already ongoing based on the experiments that followed the first criticality.  Future  work should extend benchmark efforts beyond zero-power operation and potentially to 233 U-bearing  salt.  All  such  experiments  have  been  conducted at the MSRE, although the accuracy and the level of details reported in publicly available documents remain to be assessed.

## Acknowledgments

The  authors  express  the  deepest  gratitude  to  those  who greatly  contributed to improve the quality of this benchmark, in particular, the IRPhEP external reviewers Luka Snoj (Jozef Stefan Institute) and Aslak Stubsgaard (Copenhagen Atomics), the chair of the IRPhEP expert group John Bess (Idaho National Laboratory), and all the members of IRPhEP. This research used the  Savio  computational  cluster  resource  provided  by  the Berkeley Research Computing  program  at UC  Berkeley

(supported  by  the  UC  Berkeley  Chancellor,  Vice  Chancellor for  Research,  and  Chief  Information  Officer).  This  research was performed using funding received from the U.S. Department  of  Energy  Office  of  Nuclear  Energy's  Nuclear Energy University Programs.

## ORCID

Massimiliano Fratoni http://orcid.org/0000-0003-04520508

## References

1. R.  C.  ROBERTSON,  'MSRE  Design  and  Operations Report Part I: Description of Reactor Design,' ORNL-TM -0728,' Oak Ridge National Laboratory (1965).
2. J.  D.  BESS  et  al.,  'The  2019  Edition  of  the  IRPhEP Handbook,'  INL/CON-19-53745-Rev000,  Idaho  National Laboratory (Oct. 2019).
3. B. E. PRINCE et al., 'Zero-Power Physics Experiments on the  Molten-Salt  Reactor  Experiment,'  ORNL-4233,'  Oak Ridge National Laboratory (1968).
4. M.  FRATONI  et  al.,  'Molten  Salt  Reactor  Experiment Benchmark  Evaluation,'  DOE-UCB-8542,  University  of California, Berkeley (Mar. 2020).
5. P. N. HAUBENREICH  et al., 'MSRE  Design and Operations Report Part III: Nuclear Analysis,' ORNL-TM -730,' Oak Ridge National Laboratory (1964).
6. R.  C.  ROBERTSON,  'MSRE  Design  and  Operations Report Part I: Description of Reactor Design,' ORNL-TM -728, Oak Ridge National Laboratory (1965).
7. J.  LEPPANEN  et  al.,  'The  Serpent  Monte  Carlo  Code: Status,  Development  and  Applications  in  2013,' Ann. Nucl.  Energy , 82 ,  142  (2015);  https://doi.org/10.1016/j. anucene.2014.08.024.
8. R. E. THOMA, 'Chemical Aspects of MSRE Operation,' ORNL-4658, Oak Ridge National Laboratory (1971).
9. M. AUFIERO et al., 'A Collision History-Based Approach to  Sensitivity/Perturbation  Calculations  in  the  Continuous Energy Monte Carlo Code Serpent,' Ann. Nucl. Energy , 85 , 245 (2015); https://doi.org/10.1016/j.anucene.2015.05.008.
10. W. A. WIESELQUIST, R. A. LEFEBVRE, and M. A. JESSEE, 'SCALE Code System,' ORNL/TM-2005/ 39, Version 6.2.4, Oak Ridge National Laboratory (2020).

AUGUST 2021

<!-- image -->

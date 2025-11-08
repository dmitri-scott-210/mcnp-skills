## 2.3 MSRE

The configuration selected for the graphite-moderated molten salt reactor (MSR) is the Molten Salt Reactor Experiment (MSRE). The MSRE was built at ORNL and operated between 1965 and 1969. Its purpose was to demonstrate key features of the molten-salt liquid-fuel reactor concept and to prove the practicality of the MSR technology. This was the first large-scale, long-term, high-temperature testing performed for a fluid fuel salt, graphite moderator, and new nickel-based alloys in a reactor environment. The circulating fuel was a mixture of lithium, beryllium, and zirconium fluoride salts that contained uranium fluorides. Reactor heat was transferred from the fuel salt to a coolant salt and was then dissipated to the atmosphere. The MSRE was designed to provide a thermal output of 10 MWth. The MSRE reached criticality for the first time in June 1965; the corresponding zero-power first critical experiment with 235 U was recently included in the IRPhEP handbook (Shen et al., 2019). Table 5 presents an overview of the key characteristics of the MSRE, and Figure 5 and Figure 6 are illustrations of the  horizontal and vertical cross sections of the reactor core, respectively.

The MSRE core consisted of a graphite structure within a cylindrical reactor vessel. The fuel salt entered the flow distributor at the top of the vessel through the fuel inlet, was then distributed evenly around the circumference of the vessel, and then flowed downward through a ~2.54 cm annulus between the vessel wall and the core can. The salt was then pumped upward through the graphite structure. This graphite structure was a lattice of vertical stringers with a side length of 5.08 cm and an axial length of 170.03 cm. The salt could flow through in more than 1,000 channels, each ~1 cm thick, that were formed by grooves in the sides on the stringers. In the center of the core, three graphite sample baskets were mounted to allow investigation of the behavior of the graphite moderator in the reactor environment through periodic removals of graphite specimens.

The salt served the dual purpose of carrying the fuel and cooling the core. It was composed of (1) the carrier salt, containing the beryllium, zirconium, and most of the lithium fluorides, (2) depleted uranium eutectic (73LiF-27UF4), and (3) highly enriched uranium eutectic (73LiF-27UF4). The reactor vessel consisted of INOR-8, a nickel-based alloy. The core was surrounded by an insulator, simplified in the benchmark specification as a homogeneous mixture (O, Fe, Al, H, Si, Ca), and a steel thermal shield.

The temperature specified for the thermal shield and insulation is 305 K; the temperature specified for all other materials in the benchmark is 911 K.

The IRPhEP handbook provides an experimental eigenvalue along with the corresponding experimental uncertainty. The benchmark also provides a calculated eigenvalue obtained with the Serpent code and documents a first assessment of the influence of nuclear data uncertainties on the eigenvalue, as also summarized in a previous conference paper (Shen et al., 2018).

Table 5. Key characteristics of the MSRE (Shen, 2019).

| Reactor power (MWth)                                                                  | 10                                                                    |
|---------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Fuel and coolant                                                                      | 64.88LiF-29.27BeF 2 -5.06ZrF 4 -0.79UF 4 (expressed as molar percent) |
| Fuel salt density (g/cm 3 )                                                           | 2.3275                                                                |
| Graphite density (g/cm 3 )                                                            | 1.8507                                                                |
| Graphite lattice radius (cm)                                                          | 70.285                                                                |
| Core can radius (cm) Inner Outer                                                      | 71.097 71.737                                                         |
| Reactor vessel Inner radius (cm) Inner                                                | 74.299                                                                |
| Reactor vessel Outer radius (in active region)                                        | 75.741                                                                |
| Graphite stringer width (cm)                                                          | 5.084                                                                 |
| Fuel channel width (cm)                                                               | 1.018                                                                 |
| Fuel channel thickness (cm)                                                           | 3.053                                                                 |
| Graphite stringer height (cm)                                                         | 170.311                                                               |
| Height of the core can (cm)                                                           | 174.219                                                               |
| Total height of the vessel (from the bottom of vessel to the top of outlet pipe) (cm) | 272.113                                                               |
|                                                                                       |                                                                       | 

Figure 5. Horizontal cross section of the MSRE benchmark (Shen et al., 2019). Molten salt - light blue; graphite lattice - pink; reactor vessel, INOR (Ni-based alloy) - gray; void - dark blue; insulation, homogeneous mixture (O, Fe, Al, H, Si, Ca) - orange; stainless steel shells - green; mainly steel thermal shield - gray.

<!-- image -->

Figure 6. Vertical cross section of the MSRE benchmark (Shen et al., 2019). Molten salt - light blue; graphite lattice - pink; reactor vessel, INOR (Ni-based alloy) - gray; void - dark blue; insulation, homogeneous mixture (O, Fe, Al, H, Si, Ca) - orange; stainless steel shells - green; mainly steel thermal shield - gray;

<!-- image -->

## 2.4 MEGAPOWER

Heat pipe-cooled reactors with limited power output were first developed at Los Alamos National Laboratory (LANL) during the 1960s. Originally designed for space applications, the Kilopower heat pipe concept was scaled up to the low megawatt electric (MWe) range and is now known as the Megapower reactor (McClure et al., 2015; Figure 7). This concept was further expanded upon by Idaho National Laboratory (INL), and two alternative core designs were proposed (Sterbentz et al., 2018). From these INL designs, Design A was selected for the analysis of heat pipe reactors.

INL Design A includes fuel elements with a solid fuel region and heat pipes containing a potassium (K) coolant. The heat carried away from the core via the heat pipe is converted to power using an open-air Brayton cycle. The core is surrounded with 12 radial control drums and has Al2O3 and BeO reflectors on all sides (Figure 8). While the original LANL design (Figure 7) is oriented horizontally, INL Design A is oriented vertically. Design A consists of hexagonal fuel elements that contain a heat pipe (Figure 9). The original INL Design A specifications include 19.75% 235 U enriched UO2. However, in this project, a slightly modified version with metallic fuel consisting of 18.1% 235 U enriched uranium with a 10% weight fraction of zirconium (U-10Zr) will be studied (Hu, G. et al., 2019). Other key design characteristics are shown in Table 6.

A limited number of neutronics analyses performed with MCNP and Serpent provide calculated values for eigenvalue, reactivities, and reactor power for all concepts (Sterbentz et al., 2018; Lee et al., 2019; Hu,

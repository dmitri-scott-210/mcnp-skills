# The Monolithic Heat Pipe Microreactor Reference Plant Model 

Javier Ortensi ${ }^{1}$, Mustafa K. Jaradat ${ }^{1}$, Joshua Hansel ${ }^{2}$, and Stefano Terlizzi ${ }^{1}$<br>${ }^{1}$ Reactor Physics Methods and Analysis<br>${ }^{2}$ Computational Frameworks

## DISCLAIMER

This information was prepared as an account of work sponsored by an agency of the U.S. Government. Neither the U.S. Government nor any agency thereof, nor any of their employees, makes any warranty, expressed or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness, of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. References herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise, does not necessarily constitute or imply its endorsement, recommendation, or favoring by the U.S. Government or any agency thereof. The views and opinions of authors expressed herein do not necessarily state or reflect those of the U.S. Nuclear Regulatory Commission.

# The Monolithic Heat Pipe Microreactor Reference Plant Model 

Javier Ortensi ${ }^{\mathbf{1}}$, Mustafa K. Jaradat ${ }^{\mathbf{1}}$, Joshua Hansel ${ }^{\mathbf{2}}$, and Stefano Terlizzi ${ }^{\mathbf{1}}$<br>${ }^{1}$ Reactor Physics Methods and Analysis<br>${ }^{2}$ Computational Frameworks

April 2024

Idaho National Laboratory<br>Nuclear Science and Technology<br>Idaho Falls, Idaho 83415

http://www.inl.gov

Prepared for the
Office of Nuclear Regulatory Research
U. S. Nuclear Regulatory Commission

Washington, D. C. 20555
Task Order No.: 31310019F0015

Page intentionally left blank

## SUMMARY

This work introduces a reference plant model for a generic monolithic heat-pipe-cooled microreactor. The model will serve as a springboard to develop future evaluation models in the licensing process of similar microreactor designs at the U.S. Nuclear Regulatory Commission. This model has been developed with the Comprehensive Reactor Analysis Bundle and its specifications are based on open literature publications for the eVinci ${ }^{I M}$ design. BlueCRAB is the U.S. Nuclear Regulatory Commission non-light-water reactor analysis system based on the Multiphysics Object-Oriented Simulation Environment framework, which can couple the Griffin, BISON, and Sockeye applications to resolve the various physics that are essential for the safety analysis of this type of reactor system. The core specifications includes tristructural isotropic fuel, graphite monolith, graphite reflectors, and drums composed of graphite and $\mathrm{B}_{4} \mathrm{C}$. No moderator or burnable poison pins are used in the design. The fuel enrichment is reduced to control excess reactivity in the core. This core design is not optimized and only serves for testing purposes, since the primary objective of this work is to exercise the multiphysics coupling for this type of reactor system. A three dimensional (3D) core heterogeneous Griffin discrete ordinates (SN) transport model allows the precise calculation of the flux distribution and pin powers. Griffin transfers the power density distribution and obtains a temperature distribution to and from BISON. The BISON model computes the 3D core temperature distribution and is coupled to 876 Sockeye subapplications running a heat pipe model. This 3D conduction model is coupled to the various heat pipes via heat flux boundary conditions. The model includes a small gap between the heat pipe and the monolith. Convective heat transfer boundaries with either ambient temperature or condenser temperature as heat sinks are imposed at the model boundaries. The 2D Sockeye heat pipe model uses a vaporonly methodology, which provides the needed resolution for transient calculations and allows the determination of various heat pipe limits. This approach is superior to the superconductor model traditionally used in steady-state calculations. BlueCRAB computes steady-state power and temperature distributions that serve as the initial condition for a loss-of-heat-sink transient simulation. The steady-state results show significant peaking due to the position of the control drum, but this is a characteristic of the particular design used, which is not optimized at this stage. The transient results show the reactor power slowly stabilizing towards a $3 \%$ power level after the partial loss of secondary heat removal. Several recriticalities are observed due to cooling through the secondary system but the reactor is self-stabilizing and behaves as expected.

## ACKNOWLEDGEMENTS

The authors are grateful for the meshing support from Olin Calvin, Idaho National Laboratory, and Yinbin Miao and Yeon Sang Jung, Argonne National Laboratory. The authors also like to acknowledge the contribution of Guillaume Giudicelli, Idaho National Laboratory, for his assistance with troubleshooting issues in the MultiApps.

Specific contributions from the various authors:

1. Javier Ortensi-Conceptualization, development of Serpent, Griffin, and core thermal models; multiphysics coupling and analysis; supervision; writing, review and editing; project administration.
2. Mustafa K. Jaradat-Multiphysics coupling and analysis.
3. Josh Hansel-Heat pipe modeling, coupling of multiphysics models.
4. Stefano Terlizzi-Development of technical specifications for the model.

This research made use of Idaho National Laboratory's High Performance Computing systems located at the Collaborative Computing Center and supported by the Office of Nuclear Energy of the U.S. Department of Energy and the Nuclear Science User Facilities under Contract No. DE-AC07-05ID14517.

Page intentionally left blank

## CONTENTS

SUMMARY ..... iii
ACKNOWLEDGMENT ..... iv
1 INTRODUCTION ..... 1
2 SPECIFICATIONS ..... 2
3 ANALYSIS METHODS ..... 4
3.1 Modeling Assumptions and Limitations ..... 4
3.2 Reactor Physics ..... 5
3.2.1 Cross-Section Model ..... 5
3.2.2 Reactor Dynamics Model ..... 10
3.3 Thermal Model ..... 10
3.4 Multiphysics Coupling ..... 13
4 RESULTS. ..... 15
4.1 Steady State ..... 15
4.2 Loss-of-Heat-Sink Event ..... 17
5 CONCLUSIONS ..... 20
REFERENCES ..... 21

## FIGURES

Figure 1. Fuel assemblies for the gHPMR. ..... 3
Figure 2. Layout of the Serpent|gHPMR|model. ..... 6
Figure 3. Fuel spectral zoning for the gHPMR|model. ..... 7
Figure 4. Griffin mesh. ..... 11
Figure 5. Griffin mesh detail. ..... 11
Figure 6. Core conduction model for the gHPMR| No control rods or heat pipes are in- cluded in the domain. ..... 12
Figure 7. Multiphysics setup for the gHPMR|model. ..... 14
Figure 8. Coupled steady-state solutions for power and temperature. ..... 16
Figure 9. Coupled steady-state solutions for scalar flux. ..... 17
Figure 10. Power and heat rate evolution during the LHS transient. ..... 18
Figure 11. Core temperature evolution during the LHS transient. ..... 18
Figure 12. Temperature distribution at beginning (left) and end (right) of LHS transient. ..... 19

## TABLES

Table 1. List of deliverables ..... 1
Table 2. General specifications for the gHPMR [1]. ..... 2
Table 3. Heat pipe specifications [2]. ..... 3
Table 4. Compact and|TRISO|specifications [3]. ..... 4
Table 5. Axial zoning of cross sections. ..... 7
Table 6. Infinite multiplication factors for a 2D assembly calculation. ..... 8
Table 7. Multiplication factors and reaction rates for a 3D assembly calculation with nine energy groups. ..... 8
Table 8. Broad group structure from General Atomics [4]. ..... 8
Table 9. Cross-section tabulation state points. ..... 9
Table 10. Cross-section tabulation state point results (control drums facing in). ..... 9
Table 11. Doppler temperature coefficient of reactivity. ..... 10
Table 12. Graphite temperature coefficient of reactivity. ..... 10
Table 13. Boundary conditions for the thermal model. ..... 12
Table 14. Material specification for the thermal model. ..... 12
Table 15. Initial and boundary conditions for the heat pipe model. ..... 13
Table 16. Spatial discretization of the heat pipe model. ..... 13
Table 17. Calculation setup for the various multiapps. ..... 14
Table 18. Sequence of events for the loss-of-heat-sink design basis accident. ..... 15
Table 19. Coupled Solution Key Parameter Values ..... 16

Page intentionally left blank

## 1. INTRODUCTION

This report details the progress and activities of Idaho National Laboratory (INL) in regard to the U.S. Nuclear Regulatory Commission (NRC) project entitled "Development and Modeling Support for Advanced Non-Light Water Reactors."

Table 1 summarizes the tasks completed between 05/01/2023 and 03/15/2024 (i.e., the tasks documented in this report). It lists the deliverable numbers and statement-of-work tasks and offers a brief description of the deliverables.

Table 1: List of deliverables.
| Deliverable Number | Statement of Work Task | Description |
| :--- | :--- | :--- |
| 12 | 12 | Support the development of a <br> Griffin/SAM reference plant model for analysis of monolith-type heat-pipe-cooled microreactor. <br> Note: Instead of SAM, we choose to deploy the Sockeye vapor-only model. |
| 18 | 18 | Documentation of the work performed under Task 12 partly fulfills Deliverable 18. |


The previously completed tasks documented in this report are Task 12. Reference plant model for a monolithic heat-pipe-cooled microreactor:

1. Development of a reference plant model for a monolith-type microreactor
2. Support for improvements to the plant model for a fuel element type microreactor
3. Support for development of macroscopic cross sections and the potential use of equivalence theory for microreactors including modeling of control drums
4. Support for NRC analyses of Single Primary Heat Extraction and Removal Emulator and Microreactor Agile Non-Nuclear Experimental Test Bed facilities.

## 2. SPECIFICATIONS

The nuclear reactor design specifications used in this work are based on open literature information for the Westinghouse eVinci ${ }^{T M}$ design and includes significant approximations in dimensions, fuel enrichment, and materials. The reactor will be referenced henceforth as the generic Heat Pipe Microreactor (gHPMR) design.

The main core specifications for the gHPMR design are included in Table 2. Core dimensions were approximated from an International Conference on Nuclear Engineering publication [1]. The fuel enrichment was chosen to reduce the excess reactivity. Although the active core region is comprised of a monolithic graphite block, we refer to specific configurations of fuel and heat pipes as "assemblies." The two types of fuel assemblies are shown in Figure 1

Table 2: General specifications for the gHPMR [1].
| Parameter | Value |
| :--- | :--- |
| Core Power [ MWth ] | 15 |
| Core Height [m] | 1.8 |
| Core Height (Active) [m] | 1.6 |
| Reflector Height [m] | 0.2 |
| Core Radius [m] | 1.4 |
| Canister Radius [m] | 1.468 |
| Fuel Enrichment | $10 \mathrm{w} / \mathrm{o}$ |
| Number of Heat Pipes | 876 |
| Number of Fuel Assemblies Types | 2 |
| Number of Standard Fuel Assemblies | 114 |
| Number of Control Rod Fuel Assemblies | 13 |
| Number of Control Drums | 12 |
| Fuel Assembly Pitch [cm] | 17.368 |
| Pin Pitch [cm] | 2.782 |
| Fuel Compact Hole Radius [cm] | 0.95 |
| Heat Pipe Hole Radius [cm] | 1.07 |
| Number of Drums | 12 |
| Control Drum Diameter [cm] | 28.1979 |
| Control Drum $B_{4} C$ Layer Thickness [ cm ] | 2.7984 |
| Control Drum $B_{4} C$ Angular Extension [degrees] | 120 |


![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-14.jpg?height=730&width=1332&top_left_y=241&top_left_x=395)
Figure 1: Fuel assemblies for the gHPMR.

The specifications for the heat pipe are in Table 3, which are adopted from the Argonne National Laboratory report [2]. The "evaporator length" here includes not just the 1.6 m active core length (length of fuel pins) but also the 0.2 m reflector section that is coupled to the heat pipe.

Table 3: Heat pipe specifications [2].
| Parameter | Value |
| :--- | :--- |
| Working Fluid | Sodium |
| Wick Material | SS 316 |
| Cladding Material | SS 316 |
| Evaporator Length [m] | 1.8 |
| Adiabatic Length [m] | 0.4 |
| Condenser Length [m] | 1.8 |
| Outer Cladding Radius [m] | 0.0105 |
| Inner Cladding Radius [m] | 0.0097 |
| Outer Wick Radius [m] | 0.0090 |
| Inner Wick Radius [m] | 0.0080 |
| Wick Porosity | 0.7 |
| Wick Permeability [ $m^{2}$ ] | 2E-9 |
| Pore Radius [m] | $1 \mathrm{E}-8$ |
| Wick Fill | 10\% overfill by volume at 500 K |


The compact and tristructural isotropic specifications are based on Advanced Gas Reactor 2 [3] and shown in Table 4.

Table 4: Compact and TRISO specifications [3].
| Parameter | Value |
| :--- | :---: |
| Compact Fueled Zone Radius [cm] | 0.875 |
| Compact Non-Fueled Zone Radius [cm] | 0.9 |
| Compact Packing Fraction [\%] | 40 |
| UCO Kernel Radius [cm] | 0.02125 |
| Buffer Radius [cm] | 0.03125 |
| Inner PyC Radius [cm] | 0.03525 |
| SiC Radius [cm] | 0.03875 |
| Outer PyC Radius [cm] | 0.04275 |


## 3. ANALYSIS METHODS

The multiphysics model of the gHPMR relies on three Multiphysics Object-Oriented Simulation Environment based applications: Griffin, BISON, and Sockeye. All mesh files developed in this work use the MOOSE reactor module [5]. Although the meshing inputs and outputs are not optimal at this point, it is much easier for the user to have an integrated system to perform all necessary tasks. Therefore the meshing is entirely MOOSE-based to adopt future improvements in the reactor module. The reactor physics model is described in Section 3.2 and includes a discussion of the Serpent cross-section preparation as well as the Griffin dynamics model. The thermal model is discussed in Section 3.3 with details on the coupling between the core and the heat pipes. Finally, the multiphysics model is presented in Section 3.4 with a discussion on application coupling.

Although the physical core orientation is horizontal, we choose to present the models and results as a vertical core and will refer to the region of the core that is closer to the condenser as the "top."

### 3.1 Modeling Assumptions and Limitations

The following assumptions and limitations are applied to different physics.

## Reactor Physics

1. The fuel and fuel gap are homogenized together
2. The heat pipe core, clad, and gap are homogenized together
3. The spatial resolution of cross sections is sufficient but might need to be further researched
4. We assume that the nine-group structure selected is sufficient to resolve the core-wide physics. Future work should include core-wide group structure studies
5. No depletion studies have been conducted, and the buildup of fission product neutron poisons ( ${ }^{135} \mathrm{Xe}$ and ${ }^{149} \mathrm{Sm}$ ) is currently not taken into account
6. The current decay heat is a good approximation but needs to be improved in future work by adding a decay heat standard.

## Core Conduction

1. There is no fuel gap between the fuel and monolith
2. The fuel kernels and other TRISO constituent materials are at isothermal conditions with the compact matrix
3. The compact effective conductivity model in GraphiteMatrixThermal BISON material needs to be studied further to ensure accuracy for specific fuel types
4. The gap size between the heat pipes and monolith is assumed to be fixed with a constant heat transfer coefficient
5. Thermophysical properties need to be revisited when vendor-specific data is available
6. An adiabatic condition is imposed on the the control rod hole
7. Use a single value for the temperature and heat transfer coefficient for the heat sink (no spatial distribution of the external sink).

## Heat Pipe

1. Internal heat pipe specifications, such as wick properties, were unknown
2. The pore radius was chosen to be very small to avoid reaching the capillary limit in these analyses
3. The effects of any noncondensable gases present in the heat pipe were neglected
4. The heat pipe is assumed to be perfectly insulated between the core and heat exchanger
5. The heat exchanger is modeled with by a convection condition with a user-specified reference temperature and heat transfer coefficient.

### 3.2 Reactor Physics

### 3.2.1 Cross-Section Model

A Serpent [6] Monte Carlo model was developed to prepare the cross sections and provide reference solutions based on the specification provided in Section 2. Serpent is chosen as a highfidelity solution since it does not include significant approximations with regard to energy, angular, or spacial dependence. In addition, Serpent relies on a Woodcock delta-tracking algorithm [7] that renders very high performance for TRISO-based fuel forms compared to other Monte Carlo codes.

The core is comprised of standard and control rod assemblies in the arrangement shown in Figure 2. It is noteworthy that the top reflector includes protruding heat pipes and control rod holes, thus leading to lower graphite content in that region and a slightly harder spectrum than near the bottom of the core. The poisoned portion of the drums spans the height of the active core region.

The target Griffin model relies on a heterogeneous representation of the core with the CMFD accelerated SN transport solver. This implies that the Serpent-based macroscopic cross sections are required for each material and the fuel in the active core must be subdivided into spectral zones (i.e., zones with an assumed constant neutron spectrum). The cross-section spectral zoning in the radial direction is shown in Figure 3(a) with the standard assembly (F1) spanning four radial zones. The control rod assembly (F3) spans a single radial zone since it is positioned at the center of the core. In the axial direction, the fuel has three spectral zones with the spectrum transition zones

![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-17.jpg?height=1185&width=1388&top_left_y=241&top_left_x=363)
Figure 2: Layout of the Serpent gHPMR model.

20 cm from the bottom and top reflectors, as shown in Figure3(b). The cross-section identification numbers are included in Table 5 with three axial sets for the fuel regions and four axial sets for the heat pipes (including the upper reflector zone). In this model, the fuel compact and gap are homogenized together. In a similar way, the heat pipe core, clad, and gap are also homogenized.

![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-18.jpg?height=722&width=1313&top_left_y=246&top_left_x=417)
Figure 3: Fuel spectral zoning for the gHPMR model.

Table 5: Axial zoning of cross sections.
| Material Zone | Cross-Section identification |
| :--- | :--- |
| Fuel1 R0 | 100101102 |
| Fuel1 R1 | 110111112 |
| Fuel1 R2 | 120121122 |
| Fuel1 R3 | 130131132 |
| Fuel3 R0 | 300301302 |
| Heat Pipe R0 | 500501502503 |
| Heat Pipe R1 | 510511512513 |
| Heat Pipe R2 | 520521522523 |
| Heat Pipe R3 | 530531532533 |
| Heat Pipe R0 | 540541542543 |
| Monolith | 600 |
| Helium | 705 |
| Reflector | 710 |
| Stainless Steel | 715 |
| Control Drum Absorber | 800 |


Initial Serpent and Griffin calculations on a two dimensional (2D) assembly geometry showed reasonable agreement in terms of $k_{\infty}$ and reaction rates with $k_{\infty}$ differences in the 150 pcm range. Results with various broad group structures are included in Table 6, where the Serpent result is based on a continuous neutron energy (CE) calculation. Results for the 3D standard assembly are shown in Table 7 with a nine energy group structure. Note that the granularity of the group structure can affect the leakage fraction. Additional studies will be necessary to improve these results in terms of fuel homogenization as well as the core-wide energy group structure.

Table 6: Infinite multiplication factors for a 2D assembly calculation.
| Code | Number of Groups | $k_{\infty}$ | Difference [pcm] |
| :--- | :---: | :---: | :---: |
| Serpent | CE | $1.37478 \pm 29$ | - |
| Griffin SN | 9 | 1.37591 | 112.9 |
|  | 10 | 1.37610 | 132.3 |
|  | 13 | 1.37634 | 155.9 |
|  | 16 | 1.37637 | 158.5 |
|  | 26 | 1.37612 | 134.4 |


Table 7: Multiplication factors and reaction rates for a 3D assembly calculation with nine energy groups.
| Code | keff | Production | Absorption | Leakage |
| :--- | :---: | :---: | :---: | :---: |
| Serpent | $1.36914 \pm 1.7$ | $7.50 \mathrm{E}+10$ | $5.365 \mathrm{E}+10$ | $1.12 \mathrm{E}+09$ |
| Griffin SN | 1.37224 | $7.50 \mathrm{E}+10$ | $5.359 \mathrm{E}+10$ | $1.06 \mathrm{E}+09$ |
| Difference | 310 pcm | $0.00 \%$ | $-0.11 \%$ | $-5.51 \%$ |


The nine broad energy group structure is based on the General Atomics structure used for the Next Generation Nuclear Plant project [4] and is included in Table 8.

Table 8: Broad group structure from General Atomics [4].
| Energy <br> Group | Upper Energy <br> $[\mathrm{MeV}]$ |
| :--- | :---: |
| 1 | $4.0000 \mathrm{E}+01$ |
| 2 | $1.8316 \mathrm{E}-01$ |
| 3 | $9.6100 \mathrm{E}-04$ |
| 4 | $1.7610 \mathrm{E}-05$ |
| 5 | $3.9279 \mathrm{E}-06$ |
| 6 | $2.3800 \mathrm{E}-06$ |
| 7 | $1.2750 \mathrm{E}-06$ |
| 8 | $8.2500 \mathrm{E}-07$ |
| 9 | $1.3000 \mathrm{E}-07$ |


The case matrix used in preparing the cross-section tabulations is shown in Table 9. and the corresponding full core calculation results are included in Table 10. There is a significant bias ( 450 pcm), which is higher than observed for the 3D assembly, but the presence of control drums facing towards the active core region could exacerbate the difference. This bias can be further studied when the final design information is available.

Table 9: Cross-section tabulation state points.
| $T_{\text {fuel }}$ |  |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $T_{\text {mod }}$ | 600 | 800 | 1,000 | 1,200 | 1,400 |
| 600 | P | P | P | P | P |
| 800 | N | P | P | P | P |
| 1,000 | U | N | P | P | P |
| 1,200 | U | U | N | P | P |
| 1,400 | U | U | U | N | P |
| $\mathrm{P}=$ Physical, $\mathrm{N}=$ unphysical needed, $\mathrm{U}=$ not needed |  |  |  |  |  |


Table 10: Cross-section tabulation state point results (control drums facing in).
| Tfuel | Tmod | Serpent $k_{e f f}$ | Griffin SN $k_{e f f}$ | pcm diff |
| :--- | :--- | :--- | :--- | :--- |
| 600.0 | 600.0 | $1.09972 \pm 1.4$ | 1.10469 | 452.2 |
| 800.0 | 600.0 | $1.07883 \pm 1.4$ | 1.08390 | 470.0 |
| 1000.0 | 600.0 | $1.06154 \pm 1.5$ | 1.06665 | 481.6 |
| 1200.0 | 600.0 | $1.04609 \pm 1.5$ | 1.05145 | 512.3 |
| 1400.0 | 600.0 | $1.03249 \pm 1.5$ | 1.03785 | 518.8 |
| 800.0 | 800.0 | $1.0803 \pm 1.4$ | 1.08516 | 449.4 |
| 1000.0 | 800.0 | $1.06307 \pm 1.5$ | 1.06795 | 458.6 |
| 1200.0 | 800.0 | $1.04761 \pm 1.5$ | 1.05268 | 483.6 |
| 1400.0 | 800.0 | $1.03394 \pm 1.5$ | 1.03914 | 503.0 |
| 1000.0 | 1000.0 | $1.06461 \pm 1.4$ | 1.06944 | 453.3 |
| 1200.0 | 1000.0 | $1.04919 \pm 1.5$ | 1.05421 | 478.9 |
| 1400.0 | 1000.0 | $1.03534 \pm 1.5$ | 1.04021 | 470.7 |
| 1200.0 | 1200.0 | $1.05023 \pm 1.5$ | 1.05506 | 460.0 |
| 1400.0 | 1200.0 | $1.03639 \pm 1.5$ | 1.04130 | 473.5 |
| 1400.0 | 1400.0 | $1.03733 \pm 1.5$ | 1.04206 | 455.9 |


Tables 11 and 12 show the temperature coefficients of reactivity for the fuel and graphite for various temperature ranges. The fuel Doppler feedback is negative and much larger in magnitude than the graphite feedback, but it is worth noting that the graphite feedback is positive, although very small in magnitude.

Table 11: Doppler temperature coefficient of reactivity.
| $T_{\text {fuel }}$ <br> $[K]$ | $T_{\text {mod }}$ <br> $[K]$ | Temperature Coefficient <br> $[\mathrm{pcm} / K]$ |
| :--- | :---: | :---: |
| $600-800$ | 600 | -8.7 |
| $1200-1400$ | 600 | -6.2 |
| $800-1000$ | 800 | -7.4 |
| $1200-1400$ | 800 | -6.2 |
| $1000-1200$ | 1000 | -6.8 |
| $1200-1400$ | 1000 | -6.4 |


Table 12: Graphite temperature coefficient of reactivity.
| $T_{\text {graphite }}$ <br> $[K]$ | $T_{\text {fuel }}$ <br> $[K]$ | Temperature Coefficient <br> $[p \mathrm{~cm} / K]$ |
| :--- | :---: | :---: |
| $600-800$ | 800 | 0.5 |
| $600-800$ | 1400 | 0.6 |
| $800-1000$ | 1000 | 0.7 |
| $1000-1200$ | 1200 | 0.4 |


### 3.2.2 Reactor Dynamics Model

The mesh used in the neutronics calculations is shown in Figure 4. The radial mesh is finer than needed, as shown in 5. due to the current limitations in the assembly meshing for hexagonal pitch and of the Delaunay triangulation in the MOOSE reactor module, but will be improved in the future. Note that the aspect ratio of the elements is large since we choose 10 cm axial regions. Axial refinement studies can be later pursued to ensure proper convergence of the model. From a multiphysics perspective, this approximation is acceptable since the axial temperature profile does not exhibit significant temperature gradients due to the presence of the heat pipes.

Griffin solves the steady-state and time-dependent neutron transport equation with the CMFDaccelerated SN method. Griffin employs a Gauss-Chebyshev angular quadrature with two polar and three azimuthal angles with linear anisotropic scattering. This approximation results in 48 directions in the 3D representation of the angular flux. We use a multiplicative prolongation for the CMFD acceleration. The boundary conditions for this model are vacuum boundaries on all sides of the domain.

A decay heat model is manually added using the auxiliary system in MOOSE. In the future, a depletion calculation will be necessary to enable the use of the American Nuclear Society decay heat standard in Griffin, which can be deployed when using macroscopic cross sections for the model. Currently, the model assumes that the fuel and the monolith are in thermal equilibrium locally (element-wise). Additionally, the resolution can be obtained by including a TRISO model for each compact to compute a fuel temperature. The rotation of control drums has not been studied in detail at this point.

### 3.3 Thermal Model

The thermal model includes two levels: the core conduction and the heat pipe model. The core conduction model uses a domain and mesh that is very similar to the neutronics model, with

![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-22.jpg?height=781&width=1611&top_left_y=241&top_left_x=243)
Figure 4: Griffin mesh.

![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-22.jpg?height=611&width=1659&top_left_y=1116&top_left_x=233)
Figure 5: Griffin mesh detail.

the exception that is does not contain explicit control rods or heat pipes as shown in Figure 6 . The core thermal model entails solving the time-dependent energy equation for the heterogeneous core model. The thermal model includes the boundary conditions included in Figure 6 and Table 13 The core model assumes an adiabatic (Neumann) boundary condition in the control rod holes and convective (Robin) boundary conditions in all external boundaries. The top external boundary is coupled to the condenser temperature as its sink, whereas the other external surfaces use a fixed sink temperature of 300 K .

The thermophysical properties used in the core conduction model are shown in Table 14. The fuel compact assumes a TRISO packing fraction of 0.359 , with a thermal conductivity of $4.13 \mathrm{~W} / \mathrm{m}-$ K and a specific heat of $748.72 \mathrm{~J} / \mathrm{kg}-\mathrm{K}$.

![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-23.jpg?height=1031&width=1109&top_left_y=262&top_left_x=504)
Figure 6: Core conduction model for the gHPMR. No control rods or heat pipes are included in the domain.

Table 13: Boundary conditions for the thermal model.
| Surface | Boundary Condition Type | Value |
| :--- | :---: | :---: |
| Control Rod Hole | Neumann | 0 |
| Heat Pipe Hole | Robin | $3,877 \mathrm{~W} / \mathrm{m}^{2} / \mathrm{K}$ |
| Core Top | Robin | 300 K and $5 \mathrm{~W} / \mathrm{m}^{2} / \mathrm{K}$ |
| Core Outer Side and Bottom | Robin | 300 K and $5 \mathrm{~W} / \mathrm{m}^{2} / \mathrm{K}$ |


Table 14: Material specification for the thermal model.
| Material | BISON Model | Base Data | Density $\left[\mathrm{kg} / \mathrm{m}^{3}\right]$ |
| :--- | :---: | :---: | :---: |
| Fuel Compact | GraphiteMatrixThermal | IG_110 | 4912.0 |
| Monolith | GraphiteMatrixThermal | H_451 | 1806.0 |
| Reflectors | GraphiteMatrixThermal | H_451 | 1806.0 |
| Stainless steel | SS316Thermal | - | 7954.0 |


The initial and boundary conditions for the heat pipe model are shown in Table 15. Each of the heat pipes holes is coupled with a heat pipe model with a convective heat transfer boundary condition; thus the full core model uses 876 Sockeye subapplications (one for each heat pipe). Each of these models uses Sockeye's "vapor-only" (VO) heat pipe model, which consists of a 1D,
single-phase, compressible flow model for the vapor core of the heat pipe, coupled with 2D heat conduction in the heat pipe wick, annular gap, and cladding regions.

Table 15: Initial and boundary conditions for the heat pipe model.
| Parameter | Value |
| :--- | :---: |
| Initial Temperature $[\mathrm{K}]$ | 1073.15 |
| Evaporator BC | Neumann |
| Condenser BC | Robin |
| Condenser Convection Temperature $[\mathrm{K}]$ | 523.15 |
| Condenser Convection heat transfer coefficient $\left[\mathrm{W} /\left(\mathrm{m}^{2}-\mathrm{K}\right)\right]$ | 312.4 |


The condenser convection heat transfer coefficient was chosen to correspond to a heat pipe operating with its core temperature at 1073.15 K , removing 20 kW , considering approximate thermal resistances in the liquid and cladding.

The spatial discretization parameters used in the heat pipe are included in Table 16.

Table 16: Spatial discretization of the heat pipe model.
| Parameter | Value |
| :--- | :---: |
| Number of Axial Elements in Evaporator Section | 18 |
| Number of Axial Elements in Adiabatic Section | 4 |
| Number of Axial Elements in Condenser Section | 18 |
| Number of Radial Elements in Wick Region | 2 |
| Number of Radial Elements in Annular Gap Region | 2 |
| Number of Radial Elements in Cladding Region | 2 |


The axial discretization in the evaporator region is chosen to align with the axial discretization in the main thermal model, which is necessary to guarantee energy conservation between the main thermal model and the heat pipe models.

### 3.4 Multiphysics Coupling

A schematic of the structure of the coupling between the various MOOSE-based applications is shown in Figure 7. The Griffin full core neutronics calculation is the main application that interfaces with the BISON full core calculation. To ensure consistency between the Griffin and BISON solutions, the same mesh file was used in both models. To be precise, the heat pipes and heat pipe holes are removed from the BISON model. Griffin transfers the pin power density and obtains the heterogeneous temperature distribution from BISON. The BISON application calls 876 Sockeye subapplications that solve the heat pipe thermal fluids problem. The BISON model transfers the azimuthally averaged heat flux at various axial positions in the evaporator section, which are calculated at the boundary of the heat pipe hole. The Sockeye subapps transfer the outer cladding temperature of the evaporator section back to the BISON model. This cladding temperature is used to compute the heat flux across the heat pipe hole gap.

The type of multiapps in use for the steady-state and transient calculations is shown in Table 17. A Picard iteration scheme is used between Griffin and BISON, but we deploy loose coupling

![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-25.jpg?height=893&width=893&top_left_y=243&top_left_x=596)
Figure 7: Multiphysics setup for the gHPMR model.

for Sockeye since the convergence is currently quite difficult. Layered side averages compute the average cladding temperature in each heat pipe, and this is transferred to a 'CONST MONOMIAL' variable in the main thermal application. A heat flux is computed at each quadrature point on the heat pipe hole surfaces and applied as boundary conditions in the main thermal application. Then layered averages are computed for these heat fluxes and then transferred into a 'CONST MONOMIAL' variable in each Sockeye subapplication, where they are applied as boundary conditions. The discrete perimeter of each of the heat pipe holes (all equal by design, due to mesh generation) is transferred to Sockeye for heat flux normalization, which guarantees exact energy conservation across the transfer. In all cases, the layer averages are computed with the layers corresponding to the axial divisions, which match on each side.

Table 17: Calculation setup for the various multiapps.
| Application | Multiapp Type for <br> Steady \| Transient | Picard | Time integration |
| :--- | :---: | :---: | :---: |
| Griffin | Eigenvalue \| TransientMultiApp | Yes | 1st order Backward Euler |
| Core Conduction | FullSolveMultiApp \| TransientMultiApp | No | bdf2 |
| Heat Pipes | TransientMultiApp \| TransientMultiApp | - | bdf2 |


The Loss of Heat Sink (LHS) is a design basis accident in which the secondary system loses the ability to remove heat from the primary system. In graphite-moderated systems with strong temperature feedback, this leads to the increase in core temperatures and decrease in the power level where the reactor tends to stabilize through conduction cooldown. The accident sequence is shown in Table 18. The values of the condenser temperature and the heat transfer coefficient are assumed.

Table 18: Sequence of events for the loss-of-heat-sink design basis accident.
| Time [s] | Event(s) |
| :--- | :--- |
| $\leq 0$ | Initial equilibrium conditions are established |
| 0-10 | Null transient; maintain steady conditions |
| 10-60 | Linearly reduce the condenser heat transfer coefficient from $312.4 \rightarrow 5\left[W /\left(m^{2} K\right)\right]$ Linearly increase the condenser temperature from $523.15 \rightarrow 623.15 \mathrm{~K}$ |
| 60-11,800 | No change in input parameters |
| 11,800 | Simulation end time |


## 4. RESULTS

The results from this work are separated into two sections, with the calculation of the steadystate condition followed by the Loss of Heat Sink transient. The steady-state calculation uses the coupled system to achieve the equilibrium condition between the neutronics and thermal fluids with the heat pipes coupled to the secondary system at nominal conditions. These results are included in Section 4.1. The results from the steady-state calculation constitute the initial condition for the model used in the transient calculations. The loss-of-heat-sink transient is documented in Section 4.2

### 4.1 Steady State

The key parameter values for the steady-state solution of the coupled system are provided in Table 19. The current coupled fundamental model multiplication factor is significantly higher ( $\sim 5,000 \mathrm{pcm}$ ) than the critical value of 1.0 , but the buildup of fission product neutron poisons ( ${ }^{135} \mathrm{Xe}$ and ${ }^{149} \mathrm{Sm}$ ) is currently not taken into account. The reactivity value of these poisons is on the order of thousands of pcm. The power peaking is high in this configuration since the control drums are facing into the core; thus, the radial power shape is pushed towards the center of the core. This configuration leads to a severe power distribution and high peak temperatures but offers the opportunity to have a transient that tests some limiting conditions for this gHPMR design. The steady-state power and temperature distributions are included in Figure 8 and clearly show the peak temperature locations near the periphery of the assemblies away from the heat pipes. The average and maximum temperatures are provide in Table 19. Interestingly, the average fuel temperature is lower than the average monolith temperature, which is due to several factors, including this assembly periphery heating, the omission of the fuel gap, and the assumption that the fuel kernel and compact are at the same temperature. Although the average fuel and moderator temperature values are unusual, the maximum fuel temperature is always above the maximum monolith temperature, which is physically intuitive, due to the presence of the heat source in the fuel. For reflector zones, we observe that the radial reflector is at the lowest average temperature, which is consistent with the fact that it has the largest external surface area, and thus has a higher heat rejection rate. We note that the upper reflector is at a lower temperature due to the presence of heat pipes.

Table 19: Coupled Solution Key Parameter Values
| Parameter | Value |
| :--- | :---: |
| Eigenvalue | 1.04819 |
| Decay Heat Fraction | 0.063 |
| Power Peaking | 2.44 |
| Temperature [K] | Average \| Maximum |
| Fuel | $1155.6 \mid 1570.0$ |
| Monolith | $1156.7 \mid 1567.0$ |
| Radial Reflector | $961.0 \mid 1025.8$ |
| Bottom Reflector | $1045.6 \mid 1340.1$ |
| Top Reflector | $1002.0 \mid 1320.4$ |


![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-27.jpg?height=736&width=1563&top_left_y=926&top_left_x=308)
Figure 8: Coupled steady-state solutions for power and temperature.

The Group 1 (fast) and Group 9 (thermal) flux distribution are included in Figure 9. We observe some heterogeneity of the thermal flux solution due to the enhanced thermalization in the monolith regions between fuel assemblies.

![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-28.jpg?height=706&width=1567&top_left_y=243&top_left_x=290)
Figure 9: Coupled steady-state solutions for scalar flux.

### 4.2 Loss-of-Heat-Sink Event

The LHS transient was simulated for the gHPMR with the coupled multiphysics system. Figures 10 and 11 show the evolution of the power and temperatures during the event. The loss of the secondary system quickly increases the monolith temperature. The power in Figure 10(a) slightly increases initially due to the monolith's positive temperature coefficient of reactivity. The increase in the monolith temperature in Figure 11(a) and in the power level subsequently increase the fuel temperature. This increase in fuel temperature leads to a strong negative Doppler feedback, producing a sharp decrease in the power level and making the reactor subcritical. Since the secondary side is still removing heat, we observe a decrease in the fuel temperature 400 seconds into the transient, which results in the first recriticality event. These oscillations continue between fuel temperature and core power. We observe that the maximum fuel temperature is outside the tabulated temperature range, $600-1400.0 \mathrm{~K}$, and could slightly affect the transient results. We note that the average fuel temperature is more important and that the magnitude of the Doppler feedback quickly diminishes at high temperatures.

In time, the fuel and monolith trend towards the thermal equilibrium, and energy is transferred to the reflectors, the heat pipes, and the core boundary. In Figure 11, the decrease in the fuel and monolith temperatures leads to a net positive reactivity insertion that increases the power again, and this feedback cycle continues, although decreasing in magnitude. These oscillations dampen as the transient progresses, and the core will reach a thermal equilibrium at a stable power level.

The temperature distribution at the beginning and end point of the transient is shown in Figure 12. As the transient evolves the temperature distribution in the active core region becomes more homogeneous. We also observe the effect of the heat pipes on the reflectors, which move energy from the core center to the upper reflector zone.

![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-29.jpg?height=695&width=1630&top_left_y=422&top_left_x=246)
Figure 10: Power and heat rate evolution during the LHS transient.

![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-29.jpg?height=681&width=1621&top_left_y=1566&top_left_x=252)
Figure 11: Core temperature evolution during the LHS transient.

![](https://cdn.mathpix.com/cropped/2025_10_05_0adc9925f803ed71fae8g-30.jpg?height=945&width=1639&top_left_y=880&top_left_x=243)
Figure 12: Temperature distribution at beginning (left) and end (right) of LHS transient.

## 5. CONCLUSIONS

A high-fidelity model of agHPMR has been developed with the Comprehensive Reactor Analysis Bundle. This model is based on open literature publications for the eVinci ${ }^{T M}$ design. BlueCRAB is the U.S. NRC non-light-water reactor analysis system based on the MOOSE framework, which can coupled the Griffin, BISON, and Sockeye applications to resolve the various physics that are essential for the safety analysis of this type of reactor system. A 3D core heterogeneous Griffin SN transport model allows the precise calculation of the flux distribution and pin powers. Griffin transfers the power density distribution and obtains a temperature distribution to and from BISON. The BISON model computes the 3D core temperature distribution and is coupled to 876 Sockeye subapplications running a heat pipe model. This 3D conduction model is coupled to the various heat pipes via heat flux boundary conditions. The model includes a small gap between the heat pipe and the monolith. Convective heat transfer boundaries with either ambient temperature or condenser temperature as heat sinks are imposed at the model boundaries. The 2D Sockeye heat pipe model uses a vapor-only methodology, which allows the calculation of various heat pipe limits. BlueCRAB computes steady-state power and temperature distributions that serve as the initial condition for a loss-of-heat-sink transient simulation. The steady-state results show significant peaking due to the position of the control drum. The transient results show the reactor power slowly stabilizing towards a $3 \%$ power level after the partial loss of secondary heat removal. Several recriticalities are observed due to cooling through the secondary system but the reactor is self-stabilizing and behaves as expected. Several areas of improvement were identified:

1. Adjust the mesh generation to allow a flat-top lattice pincell within a flat-top assembly lattice and incorporate adaptive meshing for the reflector zone
2. increase the fuel temperature tabulation to 1600 K
3. Perform more core-wide spectral zone optimization
4. Perform a core-wide neutron energy group study to improve eigenvalue bias
5. Perform a depletion calculation to enable the use of the American Nuclear Society standard decay heat model
6. Explicitly model the gap between the fuel and the monolith
7. Explicitly model ${ }^{135} \mathrm{Xe}$ and ${ }^{149} \mathrm{Sm}$
8. Improve control drum modeling (cross-section dependence)
9. Explicitly compute the heat transfer coefficient for the various gaps
10. Add a shutdown control rod model
11. Improve the convergence behavior between the 3D conduction and Sockeye heat pipe and enable a Picard iteration between the two models.
12. Add TRISO fuel kernel temperature calculations for each compact
13. Determine flow conditions in the control rod hole from design information.

## REFERENCES

[1] Westinghouse eVinci ${ }^{\mathrm{TM}}$ Heat Pipe Micro Reactor Technology Development, vol. Volume 1: Operating Plant Challenges, Successes, and Lessons Learned; Nuclear Plant Engineering; Advanced Reactors and Fusion; Small Modular and Micro-Reactors Technologies and Applications of International Conference on Nuclear Engineering, 082021.
[2] N. Stauff, K. Mo, Y. Cao, J. Thomas, Y. Miao, L. Zou, D. Nunez, E. Shemon, B. Feng, and K. Ni, "Detailed analyses of a triso-fueled microreactor: Modeling of a micro-reactor system using neams tools," 92021.
[3] C. Marciulescu and A. Sowder, "Uranium oxycarbide (UCO) tristructural isotropic (TRISO)coated particle fuel performance," Tech. Rep. EPRI-AR-1(NP)-A, 3002019978, Electric Power Research Institute, November 2020.
[4] C. Ellis, A. Baxter, and D. Hanson, "Final report - ngnp core performance analysis, phase 1," NGNP Technical Report 911160, General Atomics, March 2009.
[5] E. Shemon, Y. Miao, S. Kumar, K. Mo, Y. S. Jung, A. Oaks, S. Richards, G. Giudicelli, L. Harbour, and R. Stogner, "Moose reactor module: An open-source capability for meshing nuclear reactor geometries," Nuclear Science and Engineering, vol. 0, no. 0, pp. 1-25, 2023.
[6] J. Leppänen, M. Pusa, T. Viitanen, V. Valtavirta, and T. Kaltiaisenaho, "The Serpent Monte Carlo code: Status, development and applications in 2013," Annals of Nuclear Energy, vol. 82, no. Supplement C, pp. 142-150, 2015. Joint International Conference on Supercomputing in Nuclear Applications and Monte Carlo 2013, SNA + MC 2013. Pluri- and Trans-disciplinarity, Towards New Modeling and Numerical Simulation Paradigms.
[7] E. Woodcock, T. Murphy, P. Hemmings, and T. Longworth, "Techniques used in the gem code for monte carlo neutronics calculations in reactors and other systems of complex geometry," Tech. Rep. ANL-7050, Argonne National Laboratory, 1965.


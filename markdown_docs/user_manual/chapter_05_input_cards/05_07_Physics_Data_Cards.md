---
title: "Chapter 5.7 - Physics-focused Data Cards"
chapter: "5.7"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.7_Physics-focused_Data_Cards.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

All discrete reaction libraries are based on a 262-energy-group
structure. Groups below 1 eV make the discrete treatment appropriate for
thermal neutron problems near room temperature. All discrete reaction
libraries have photon production data given in expanded format.

```
Data-card Form: DRXS z1 z2 . . . zK zk is a target identifier [§1.2.2]. All target formats are allowed.
```

Default: Continuous-energy cross-section treatment if DRXS is absent. If
the DRXS card is present but has no entries after the mnemonic, discrete
cross sections will be used for every nuclide, if available.

Use: Discouraged. Applies only to neutron cross sections. It is not
recommended that this card be used unless you are transporting neutrons
in an energy region where resonances and hence self-shielding are of
little importance. If the problem under consideration meets this
criterion, using the DRXS card can reduce computer storage requirements
and enhance timesharing.

## Details:

- 1 Use of these discrete cross sections will not result in the calculation being what is commonly referred to as a multigroup Monte Carlo calculation because the only change is that the cross sections are represented in a histogram form rather than a continuous-energy form. The angular treatment used for scattering, energy sampling after scattering, etc., is performed using identical procedures and data as in the continuousenergy treatment. The user wanting to make a truly multigroup Monte Carlo calculation should use the MGOPT card multigroup capability.

## 5.7 Physics-focused Data Cards

The data provided in this section describe the physics options that can
be selected.

## 5.7.1 MODE: Problem Type

The MODE card is used to specify the list of all particles that will be
transported. The selection of valid particle-identifier values can be
found in the 'Symbol' column of Table 4.3, with the exception of
positrons ( f ), which are invalid on the MODE card. The listed
individual particle identifiers must be space-delimited. The ordering of
particles listed does not matter.

In addition to the particle designators in Table 4.3, anti-particles may
be designated by placing a ' -' in front of the particle identifier. For
example, MODE h -h , MODE h g , and MODE g -g are all valid ways to
specify both proton ( h ) and anti-proton ( g ).

<!-- image -->

Default: If the MODE card is omitted, MODE n is assumed.

Use: Optional for neutron-only simulations. Required for any other non-
neutron or mixed-particle simulations.

## Details:

- 1 The # symbol represents all possible heavy ions. Although the # is generic to all heavy ions, the identities of different heavy ions are tracked by their appropriate Z (charge) and A (mass number). The user cannot choose to transport any particular heavy ion; however, the user may specify individual ions as source particles (see par keyword on the SDEF card) and may request tallies for specific ions (see res option on the FT special treatment tally card, §5.9.18.12).
- 2 If heavy ions ( # ) are specified on the MODE card, any residuals produced from any model physics will be transported even if the source particle is not a heavy ion.

## 5.7.2 PHYS: Particle Physics Options

## 5.7.2.1 Neutrons (PHYS:n)

## /warning\_sign Caution

The PHYS : n data card entries are different for MCNP6 than they were
for MCNP5 or MCNPX. In particular, the MCNPX PHYS : n 5th entry ( tabl )
has been replaced with the MCNP6 8th entry ( cutn ); the fission
multiplicity setting on the PHYS : n card ( fism for MCNPX and fisnu for
MCNP5) has been moved to the FMULT card.

| Data-card Form:   | PHYS : n emax emcnf iunr J J J coilf cutn ngam J J i _ int _ model i _ els _ model                                                                                                                                                                                     |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| emax              | Upper limit for neutron energy and memory reduction control (DEFAULT: emax = 100 MeV). If emax < cutn , all model physics is eliminated, thus reducing memory requirements ( 1 , 2 , 3 ).                                                                              |
| emcnf             | Analog energy limit (DEFAULT: emcnf = 0 MeV). If E is the energy of the neutron and                                                                                                                                                                                    |
| emcnf             | E < emcnf , then perform analog capture.                                                                                                                                                                                                                               |
| emcnf             | E > emcnf , then perform implicit capture.                                                                                                                                                                                                                             |
| iunr              | Controls unresolved resonance range probability table treatment when data tables are available. If                                                                                                                                                                     |
| iunr              | iunr = 0 , then probability table treatment is on (DEFAULT).                                                                                                                                                                                                           |
| iunr              | iunr = 1 , then probability table treatment is off.                                                                                                                                                                                                                    |
| J                 | Unused placeholder. Be sure to put the J in the keyword string ( 4 ).                                                                                                                                                                                                  |
| J                 | Unused; fatal error if a value appears. Be sure to put the J in the keyword string. In the MCNPX code, the 5th parameter of the PHYS : n card is tabl . As of MCNP6, tabl has been moved to the 8th entry and is now cutn .                                            |
| J                 | Unused; fatal error if a value appears. Be sure to put the J in the keyword string. In the MCNP5 code, the 5th entry on the PHYS : n card is fisnu and the MCNPX code's 6th entry on the PHYS : n card is fism . As of MCNP6, these have been moved to the FMULT card. |

| coilf = n.m   | Light-ion and heavy-ion recoil and Neutron Capture Ion Algorithm (NCIA) control (see §5.7.2.2). In this format, n is an integer and m is a specified fractional value. If                                                                                                                       |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|               | n = 0 , 1 , 2 , 4 and 0 < m ≤ 1 ,                                                                                                                                                                                                                                                               |
|               | n = 3 , 5 , then m = 0 and light-ion recoil is turned off.                                                                                                                                                                                                                                      |
|               | n = 2 , 3 , then NCIA is active only when the production of NCIA ions, shown in Table 5.8, is not modeled with the nuclear data tables.                                                                                                                                                         |
|               | n = 4 , 5 , then NCIA is active and the nuclear data tables for production of NCIA ions are not used.                                                                                                                                                                                           |
|               | Using the above set of criteria, valid coilf entries include:                                                                                                                                                                                                                                   |
|               | 0 . 001 < coilf < 1 . 001 then light-ion recoil makes coilf ions from elastic scatter.                                                                                                                                                                                                          |
|               | 1 . 001 < coilf < 2 . 001 then light-ion recoil makes coilf - 1 ions from elastic scatter; NCIA ions from neutron capture.                                                                                                                                                                      |
|               | Table data ion production will be used if possible. coilf = 3 then light-ion recoil is off; NCIA ions from neutron                                                                                                                                                                              |
|               | 3 . 001 < coilf < 4 . 001 then light-ion recoil makes coilf - 3 ions from elastic scatter; NCIA ions from neutron capture. NCIA will be used even if table data are available. coilf = 5 then light-ion recoil is off; NCIA ions from neutron capture. NCIA will be used even if table data are |
|               | available.                                                                                                                                                                                                                                                                                      |
| cutn          | Controls table-based physics cutoff and memory reduction. If cutn ≥ 0 , use physics models for energies above cutn and                                                                                                                                                                          |
|               | = - 1 , then mix and match. When tables are available, use them up to their upper limit for each nuclide, then use the physics models above that limit. See                                                                                                                                     |
|               | cutn                                                                                                                                                                                                                                                                                            |

|                 |                                                                 | MX card for mixing and matching isotopic-specific data table and model physics usage (DEFAULT).   |
|-----------------|-----------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
|                 | cutn > emax ,                                                   | save memory by eliminating all model physics arrays.                                              |
| ngam            | Controls secondary photon production ( 5 ). If                  | Controls secondary photon production ( 5 ). If                                                    |
|                 | ngam = 0 ,                                                      | no photons are produced.                                                                          |
|                 | ngam = 1 ,                                                      | photons are produced using the ACE nuclear data tables (DEFAULT).                                 |
|                 | ngam = 2 ,                                                      | photons are produced using the Cascading Gamma Multiplicity (CGM) model [235].                    |
| J               | Unused placeholder. Be sure to put the J in the keyword string. | Unused placeholder. Be sure to put the J in the keyword string.                                   |
| J               | Unused placeholder. Be sure to put the J in the keyword string. | Unused placeholder. Be sure to put the J in the keyword string.                                   |
| i _ int _ model | Controls treatment of nuclear interactions. If                  | Controls treatment of nuclear interactions. If                                                    |
|                 | i _ int _ model = - 1 ,                                         | no interactions. Equivalent to setting the inelastic cross section to zero.                       |
|                 | i _ int _ model = 0 ,                                           | process all interactions (DEFAULT).                                                               |
|                 | i _ int _ model = 1 ,                                           | no secondaries, inelastic collisions treated as weight reduction.                                 |
|                 | i _ int _ model = 2 ,                                           | no secondaries, inelastic collisions treated as removal.                                          |
| i _ els _ model | Controls treatment of nuclear elastic scattering ( 6 ). If      | Controls treatment of nuclear elastic scattering ( 6 ). If                                        |
|                 | i _ els _ model = - 1 ,                                         | no elastic scattering (i.e., treat as pseudo collision)                                           |
|                 | i _ els _ model = 0 ,                                           | elastic scattering by the Prael/Liu/Striganov model [236] (DEFAULT).                              |

PHYS n 100 0 0 J J J 0 -1 J J J 0 0

Default: :

Use: Optional to modify default neutron table and model physics
treatments. Additional neutron fission multiplicity options available on
the FMULT card.

Limitations: Restarted calculations are not supported for delayed-
neutron calculations that use model physics.

## Details:

- 1 Memory allocation can be reduced significantly for MODE n p e problems that do not invoke the photonuclear ( PHYS : p ispn = 0 ) option. By setting the neutron table/model cutoff energy, cutn , greater than the maximum neutron energy, emax , physics models are disabled, storage requirements for secondary particles are greatly reduced, and, consequently, the amount of memory that must be allocated to several MCNP6 arrays is decreased. The reduction of memory usage is helpful particularly for burnup problems. Use of this memory reduction option (i.e., setting emax &lt; cutn ) is confirmed by the following MCNP output file message: 'Memory reduction option specified, physics models disabled.'.
- 2 The parameter emax must be higher than the highest energy in the problem or the physics is wrong. For problems with energies above 100 MeV, emax should be chosen carefully; the default is appropriate for problems with energies below 100 MeV.

1

phys:n 100 100 0 3J 1

## 5.7.2.2 Light Ion Recoil Physics and the Neutron Capture Ion Algorithm (NCIA) Discussion

Light ion recoil physics accounts for the ionization potential and uses
the proper two-body kinematics (with neutron free-gas thermal treatment
if appropriate) to bank recoil particles with the proper energy and
angle. The input card MODE n h d t s a is required to produce and
transport the proton ( h ), deuteron ( d ), triton ( t ), helion ( s ),
and alpha ( a ) light ions. Heavy-ion recoils are produced if # is on
the MODE card. The particle-specific low-energy cutoff can be set with
the 2nd option, e , on the CUT : P card. For the P ions given on the
MODE card, it is recommended to adjust the low-energy cutoff such that
recoil ions produced are not killed by energy cutoff. See Table 4.3 for
the default low-energy cutoffs for each particle type.

If activated by the 7th entry, coilf , on the PHYS : n card, the
optional NCIA performs neutron capture in 3 He, 6 Li, and 10 B to
produce protons, tritons, deuterons, and/or alphas according to Table
5.8.

The diagnostic indicating that NCIA has been used appears in PRINT Table
100.

Unlike most secondary particle production in the table physics region,
NCIA particles are correlated. However, if 0 . 001 &lt; coilf &lt; 1 . 001 ,
then one light ion is created by the data library and the other by NCIA;
the correlation between the two particles is lost. If both particles are
produced by the library, no correlation exists, either. Thus, 3 . 001 &lt;
coilf &lt; 5 is recommended so that when NCIA data are available, table
data are not used.

Table 5.8: NCIA Reactions

| Isotope        | Reaction(s)                                            |
|----------------|--------------------------------------------------------|
| 3 He 6 Li 10 B | 3 He(n,h)t; n( 3 He,d)d n( 6 Li,t) α n( 10 B, α ) 7 Li |

- 3 Neutron data above emax are expunged, as are neutron data below the lower energy cutoff, which is entered via the 2nd entry on the CUT : n card. If a neutron is born at an energy greater than emax , that neutron is rejected and the event (such as fission) is resampled until an energy below emax is obtained.
- 4 The dnb parameter for delayed neutron biasing, which previously held this position, has been removed. The ACT card can be used to set delayed neutron parameters.
- 5 Correlated neutron and gamma emission is provided by CGM (unlike use of the ACE libraries) [235], although execution times will increase. CGM/CGMF currently treats neutron interactions with targets of Z &gt; 9 , except elastic scatter which continues to be treated by ACE libraries.
- 6 Elastic scattering will be ignored if nuclear interactions are turned off.

## 5.7.2.1.1 Example: 1

The configuration shown in Listing 5.21 forces all neutrons transported
to perform analog capture and a recoil ion will be created at each
elastic scatter event.

Listing 5.21: example\_phys\_cut\_nh.mcnp.inp.txt

When performing heating calculations, the user must exercise caution.
Because neutron energy deposition is physically mediated in most cases
by the secondary particle emission, NCIA may be inconsistent for heating
calculations. Neutron heating is done with kerma factors (heating
numbers), whereas heating from the charged secondaries is done at
collisions. For +F6 tallies and type 3 TMESH mesh tallies, the charged-
ion heating is subtracted from the neutron heating and thus is counted
only once. For F6 : n and F6 : h , d , t , a tallies, the heating is
counted once for each particle type. If heating tallies are done in
cells where charged ions are produced, energy may be double-counted in
F6 : P tallies. See §2.5.3 for further details.

## 5.7.2.3 Photons (PHYS:P)

## /warning\_sign Caution

Former MCNPX users need to be aware that the default behavior of the
PHYS : p nodop option has changed. Photon Doppler broadening is now on
by default ( nodop = 0 ).

| Data-card Form:   | PHYS : p emcpf ides nocoh ispn nodop J fism Upper energy limit for detailed photon physics treatment; photons with                                                                                                                                              | PHYS : p emcpf ides nocoh ispn nodop J fism Upper energy limit for detailed photon physics treatment; photons with                                                                                                                                              |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ides              | energy greater than emcpf will be tracked using the simple physics treatment (DEFAULT: emcpf = 100 MeV) ( 1 ). Controls generation of electrons by photons in MODE p e problems or, in photon-only problems, controls generation of bremsstrahlung photons with | energy greater than emcpf will be tracked using the simple physics treatment (DEFAULT: emcpf = 100 MeV) ( 1 ). Controls generation of electrons by photons in MODE p e problems or, in photon-only problems, controls generation of bremsstrahlung photons with |
|                   | the thick-target bremsstrahlung model ( 2 ). If                                                                                                                                                                                                                 | the thick-target bremsstrahlung model ( 2 ). If                                                                                                                                                                                                                 |
|                   | ides = 0 ,                                                                                                                                                                                                                                                      | then generation is on (DEFAULT).                                                                                                                                                                                                                                |
|                   | ides = 1 ,                                                                                                                                                                                                                                                      | then generation is off.                                                                                                                                                                                                                                         |
| nocoh             | Controls coherent (Thomson) scattering. If                                                                                                                                                                                                                      | Controls coherent (Thomson) scattering. If                                                                                                                                                                                                                      |
| nocoh             | nocoh = 0 ,                                                                                                                                                                                                                                                     | then coherent scattering is turned on (DEFAULT).                                                                                                                                                                                                                |
| nocoh             | nocoh = 1 ,                                                                                                                                                                                                                                                     | then coherent scattering is turned off ( 3 ).                                                                                                                                                                                                                   |
| ispn              | Controls photonuclear particle production ( 4 ). If                                                                                                                                                                                                             | Controls photonuclear particle production ( 4 ). If                                                                                                                                                                                                             |
| ispn              | ispn = - 1 ,                                                                                                                                                                                                                                                    | then photonuclear particle production is analog. One photon interaction per collision is sampled.                                                                                                                                                               |
| ispn              | ispn = 0 ,                                                                                                                                                                                                                                                      | then photonuclear particle production is turned off (DEFAULT).                                                                                                                                                                                                  |
| ispn              | ispn = 1 ,                                                                                                                                                                                                                                                      | then photonuclear particle production is biased. The bias causes a photonuclear event at each photoatomic event.                                                                                                                                                |
| nodop             | Controls photon Doppler energy broadening ( 5 ). If                                                                                                                                                                                                             | Controls photon Doppler energy broadening ( 5 ). If                                                                                                                                                                                                             |
| nodop             | nodop = 0 ,                                                                                                                                                                                                                                                     | then Doppler energy broadening is turned on (DEFAULT).                                                                                                                                                                                                          |
| nodop             | nodop = 1 ,                                                                                                                                                                                                                                                     | then Doppler energy broadening is turned off.                                                                                                                                                                                                                   |
| J                 | Unused. Be sure to put the J in the keyword string. ( 6 )                                                                                                                                                                                                       | Unused. Be sure to put the J in the keyword string. ( 6 )                                                                                                                                                                                                       |
| fism              | Controls selection of photo-fission method ( 7 ). If                                                                                                                                                                                                            | Controls selection of photo-fission method ( 7 ). If                                                                                                                                                                                                            |
| fism              | fism = 0 ,                                                                                                                                                                                                                                                      | sample photo-fission from ACE libraries (no photo-fission prompt gammas) (DEFAULT).                                                                                                                                                                             |

fism = 1 ,

Default:

PHYS : p 100 0 0 0 0 J 0

Use: Optional.

Limitations: Restarted calculations are not supported for delayed-gamma
calculations.

## Details:

- 1 If emax on the PHYS : e card is less than emcpf on the PHYS : p card, MCNP6 will internally reset empcf to be equal to emax .
- If wc1 = 0 on the CUT : p card, analog capture is used in the energy region above emcpf . Otherwise capture is simulated by weight reduction with Russian roulette handling low-weight particles. Photons with energy less than emcpf will be treated with the more detailed physics that always includes analog capture. For a detailed discussion of the simple and detailed photon physics treatments, see §2.4.4.1 and §2.4.4.2, respectively.
- The simple physics treatment, intended primarily for higher energy photons, considers the following physical processes: photoelectric effect without fluorescence, Compton scattering, and pair production. The highly forward peaked coherent Thomson scattering is ignored. In the detailed physics treatment, photoelectric absorption can result in fluorescent emission, the Thomson and Klein-Nishina differential cross sections are modified by appropriate form factors [238] and Compton profiles taking electron binding effects into account, and coherent scattering is included.
- 2 To turn off the production of secondary electrons generated by photons, the switch ides can be set, either on the PHYS : p or on the PHYS : e card. If either of these cards sets ides = 1 , photons will not produce electrons, even if ides = 0 is set on the other. In a photon-only problem, turning off secondary electrons causes the thick-target bremsstrahlung model to be bypassed. This option should be exercised only with great care because it alters the physics of the electron-photon cascade and will give erroneously low photon results when bremsstrahlung and electron transport are significant.
- 3 When nocoh = 1 , the cross section for coherent scattering will be set to zero. This approximation can be useful in problems with bad point detector variances.
- 4 Photonuclear physics models enable ( γ, n ) and other photonuclear reactions when photonuclear data tables are unavailable. When some photonuclear data tables are available, MCNP6 will mix and match, using tables when available and physics models when no tables are available. Consider using an MX : p card to override this default behavior.
- 5 When photon Doppler broadening is turned on ( nodop = 0 ), there is no effect unless photon Doppler broadening momentum profile data are available in the photon library. These data are available in the MCPLIB03 and later photon libraries.
- 6 The dgb parameter for delayed photon biasing, which previously held this position, has been removed. The ACT card can be used to set delayed gamma parameters.

glyph[negationslash]

- 7 When fism = 1 , photo-fission secondaries are sampled only when a photo-fission event occurs (unlike fism = 0 ). This enables coincidence counting of photo-fission secondaries. The LLNL fission library for photo-fission is the only way to produce prompt photo-fission gammas; these gammas are correlated with the photo-fission neutrons with appropriate multiplicities. When fism = 1 on the PHYS : p card, photonuclear physics must be turned on ( ispn = 0 ) and the LLNL fission library should be used also for neutrons ( method = 5 on the FMULT card).

sample photo-fission from the LLNL fission library [237]. Requires
photonuclear physics ( ispn = 0 ).

glyph[negationslash]

## 5.7.2.4 Electrons (PHYS:E)

Electron-specific physics settings are controlled with this card.
However, because of the close relationship between photons and electrons
during transport, also consider using the PHYS : p card in case adequate
control is unavailable on the PHYS : e card alone.

| Data-card Form: PHYS : e emax ides iphot ibad istrg bnum xnum rnok enum numb i _ mcs _ model mode _ electron _ elastic J efac electron _ method _ boundary ckvnum   | Data-card Form: PHYS : e emax ides iphot ibad istrg bnum xnum rnok enum numb i _ mcs _ model mode _ electron _ elastic J efac electron _ method _ boundary ckvnum                                                                                       | Data-card Form: PHYS : e emax ides iphot ibad istrg bnum xnum rnok enum numb i _ mcs _ model mode _ electron _ elastic J efac electron _ method _ boundary ckvnum                                                                                       |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| emax                                                                                                                                                                | Upper limit for electron energy (DEFAULT: emax on PHYS : n card or 100 MeV if no PHYS : n card) ( 1 ).                                                                                                                                                  | Upper limit for electron energy (DEFAULT: emax on PHYS : n card or 100 MeV if no PHYS : n card) ( 1 ).                                                                                                                                                  |
| ides                                                                                                                                                                | Controls production of electrons by photons in MODE e problems or, in photon-only problems, controls generation of bremsstrahlung photons with the thick-target bremsstrahlung model. If                                                                | Controls production of electrons by photons in MODE e problems or, in photon-only problems, controls generation of bremsstrahlung photons with the thick-target bremsstrahlung model. If                                                                |
|                                                                                                                                                                     | ides = 0 ,                                                                                                                                                                                                                                              | then electron production by photons is turned on (DEFAULT).                                                                                                                                                                                             |
|                                                                                                                                                                     | ides = 1 ,                                                                                                                                                                                                                                              | then electron production by photons is turned off.                                                                                                                                                                                                      |
| iphot                                                                                                                                                               | Controls production of photons by electrons. If                                                                                                                                                                                                         | Controls production of photons by electrons. If                                                                                                                                                                                                         |
|                                                                                                                                                                     | iphot = 0 ,                                                                                                                                                                                                                                             | then photon production by electrons is turned on (DEFAULT).                                                                                                                                                                                             |
|                                                                                                                                                                     | iphot = 1 ,                                                                                                                                                                                                                                             | then photon production by electrons is turn off.                                                                                                                                                                                                        |
| ibad                                                                                                                                                                | Controls bremsstrahlung angular distribution method. If                                                                                                                                                                                                 | Controls bremsstrahlung angular distribution method. If                                                                                                                                                                                                 |
|                                                                                                                                                                     | ibad = 0 ,                                                                                                                                                                                                                                              | perform full bremsstrahlung tabular angular distribution (DEFAULT).                                                                                                                                                                                     |
|                                                                                                                                                                     | ibad = 1 ,                                                                                                                                                                                                                                              | perform simple bremsstrahlung angular distribution approximation ( 2 ).                                                                                                                                                                                 |
| istrg                                                                                                                                                               | Controls electron continuous-energy slowing down ('straggling') treatment. If                                                                                                                                                                           | Controls electron continuous-energy slowing down ('straggling') treatment. If                                                                                                                                                                           |
|                                                                                                                                                                     | istrg = 0 ,                                                                                                                                                                                                                                             | use sampled value straggling method to compute electron energy loss at each collision (DEFAULT).                                                                                                                                                        |
|                                                                                                                                                                     | istrg = 1 ,                                                                                                                                                                                                                                             | use expected-value straggling method to compute electron energy loss at each collision.                                                                                                                                                                 |
| bnum                                                                                                                                                                | Controls production of bremsstrahlung photons created along electron sub steps. If                                                                                                                                                                      | Controls production of bremsstrahlung photons created along electron sub steps. If                                                                                                                                                                      |
|                                                                                                                                                                     | bnum = 0 ,                                                                                                                                                                                                                                              | bremsstrahlung photons will not be produced.                                                                                                                                                                                                            |
|                                                                                                                                                                     | bnum > 0 ,                                                                                                                                                                                                                                              | produce bnum times the analog number of bremsstrahlung photons. Radiative energy loss uses the bremsstrahlung energy of the first sampled photon (DEFAULT: bnum = 1 ).                                                                                  |
|                                                                                                                                                                     | The specification bnum < 0 is only applicable is using the EL03 electron-transport cross section library. Produce | bnum | times the number of analog photons. Radiative energy loss uses the average energy of all the bremsstrahlung photons sampled. | The specification bnum < 0 is only applicable is using the EL03 electron-transport cross section library. Produce | bnum | times the number of analog photons. Radiative energy loss uses the average energy of all the bremsstrahlung photons sampled. |
| xnum                                                                                                                                                                | Controls sampling of electron-induced x-rays produced along electron sub steps. If                                                                                                                                                                      | Controls sampling of electron-induced x-rays produced along electron sub steps. If                                                                                                                                                                      |

```
xnum = 0 , x-ray photons will not be produced by electrons. xnum > 0 , produce xnum times the analog number of electron-induced x-rays (DEFAULT: xnum = 1 ). rnok Controls creation of knock-on electrons produced in electron interactions. If rnok = 0 , knock-on electrons will not be produced. rnok > 0 , produce rnok times the analog number of knock-on electrons (DEFAULT: rnok = 1 ). e _ bias _ num Controls generation of photon-induced secondary electrons ( 3 ). If e _ bias _ num = 0 , photon-induced secondary electrons will not be produced. e _ bias _ num > 0 , produce e _ bias _ num times the analog number of photon-induced secondary electrons (DEFAULT: e _ bias _ num = 1 ). numb Controls bremsstrahlung production on each electron sub step ( 4 ). If numb = 0 , analog bremsstrahlung production (DEFAULT). numb > 0 , produce bremsstrahlung on each sub step. i _ mcs _ model Controls the choice of Coulomb scattering model. If i _ mcs _ model = -1 , turn off angular deflection. i _ mcs _ model = 0 , select the standard Goudsmit-Saunderson angular deflection method (DEFAULT). mode _ electron _ elastic Controls choice of electron elastic cross section. Single-event transport only. If mode _ electron _ elastic = 0 , large-angle elastic scattering is used (cosine > 10 -6 ) (DEFAULT). mode _ electron _ elastic = 2 , total elastic cross section (large-angle + in-peak) is used. J Unused placeholder. Be sure to put the J in the keyword string. efac Controls stopping power energy spacing ( 5 ). Restriction: 0 . 8 ≤ efac ≤ 0 . 99 (DEFAULT: efac = 0 . 917 ). electron _ method _ boundary Controls the start of single-event transport ( 6 , 7 ). electron _ method _ boundary is the energy (in MeV) above which MCNP6 transports electrons by the condensed-history algorithms and below which the single-event method is used (DEFAULT: electron _ method _ boundary = 10 -3 ). ckvnum Scales Cerenkov photon emission from a particular particle by a fractional amount with the photons emitted at higher weight ( 8 ). Allowed values are 0 ≤ ckvnum < 1 ); values of 10 -3 -10 -2 are recommended. ckvnum = 0 turns off Cerenkov emission (DEFAULT: 0).
```

## Default:

PHYS : e 100 0 0 0 0 1 1 1 1 0 0 0 J 0.917 0.001 0

Use: Optional.

## /warning\_sign Caution

The use of the switches (or of zero values for the biasing parameters)
to turn off various processes goes beyond biasing and actually changes
the physics of the simulation. Therefore such actions should be taken
with extreme care. These options are provided primarily for purposes of
debugging, code development, and special-purpose studies of the cascade
transport process.

## Details:

- 1 The parameter emax should be set to the highest electron energy encountered in your problem.
- 2 Point detectors and DXTRAN spheres use the simple bremsstrahlung angular distribution approximation. Always use ( ibad = 1 ).
- 3 The specification enum = 0 differs from ides = 1 . If enum = 0 , pair production is totally turned off. If ides = 1 , the pair production-produced annihilation photons are still produced.
- 4 Only a real event, i.e., one that has been sampled to have a bremsstrahlung interaction, causes energy loss. The weights of the bremsstrahlung photons are multiplied by the probability of interaction in a substep. If two or more photons are produced in a real event, the weight of the second or more photons is the unadjusted value because there is no Poisson sampling, except for real events.
- 5 When efac is specified, the energy spacing for multiple-scattering tables (stopping power, range, etc.) is determined by

where E 1 is the highest energy and where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

This means that on average, the energy of the particle will decrease by
a factor of two in D energy steps and that a larger value of efac
results in more points in the multiple-scattering tables. The default
value, efac = 0 . 917 , leads to the traditional choice of eight energy
steps for a factor-of-two energy loss.

- 6 To invoke the single-event electron-transport method, the problem must have access to photon data, even if the user is not interested in the photon transport. Therefore, the MODE card must included the specification for both photons ( p ) and electrons ( e ). Access to the EPRDATA14 library data is required to transport electrons below 1 keV. This library, which is denoted by the cross-section identifier '.14p,' is not the default in the xsdir \_ mcnp6.3 cross-section directory file provided with the MCNP code, version 6.3; therefore the EPRDATA14 library may need to be requested on the material cards explicitly. This low-energy ( &lt; 1 keV) data are only for zero-temperature atomic targets, so temperature, condensed state, and molecular effects are not yet treated for electrons in this regime.
- 7 The energy boundary that defines the switch to single-event transport should never be lower than 1 keV, because condensed-history methods rapidly collapse below this traditional lower limit.
- 8 Cerenkov photon production requires that a refractive index is specified on the M card.

1

## 5.7.2.4.0.1 Example 1

The configuration shown in Listing 5.22 causes the energy-boundary
switch to the single-event electrontransport method to occur at 10 keV.

Listing 5.22: example\_phys\_e.mcnp.inp.txt

| 100. 13j 0.01   |
|-----------------|

## 5.7.2.5 Protons (PHYS:H)

Proton-specific physics settings are controlled with this card.

| Data-card Form: PHYS : h emax ean tabl J istrg J recl J J J i _ mcs _ model i _ int _ model i _ els _ model efac J ckvnum drp   | Data-card Form: PHYS : h emax ean tabl J istrg J recl J J J i _ mcs _ model i _ int _ model i _ els _ model efac J ckvnum drp   | Data-card Form: PHYS : h emax ean tabl J istrg J recl J J J i _ mcs _ model i _ int _ model i _ els _ model efac J ckvnum drp                                                                                                                             |
|---------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| emax                                                                                                                            | Upper proton energy limit (DEFAULT: emax on PHYS : n card or 100 MeV if no PHYS : n card) ( 1 ).                                | Upper proton energy limit (DEFAULT: emax on PHYS : n card or 100 MeV if no PHYS : n card) ( 1 ).                                                                                                                                                          |
| ean                                                                                                                             | Analog energy limit (DEFAULT: ean = 0 MeV). If E is the energy of the proton and                                                | Analog energy limit (DEFAULT: ean = 0 MeV). If E is the energy of the proton and                                                                                                                                                                          |
| ean                                                                                                                             | E < ean ,                                                                                                                       | then perform analog capture.                                                                                                                                                                                                                              |
| ean                                                                                                                             | E > ean ,                                                                                                                       | then perform implicit capture.                                                                                                                                                                                                                            |
| tabl                                                                                                                            | Table-based physics cutoff. If                                                                                                  | Table-based physics cutoff. If                                                                                                                                                                                                                            |
| tabl                                                                                                                            | tabl = - 1 ,                                                                                                                    | then mix and match. When tables are available, use them up to their upper limit for each nuclide, then use the physics models above this limit (DEFAULT).                                                                                                 |
| tabl                                                                                                                            | tabl ≥ 0 ,                                                                                                                      | use physics models for energies E > tabl ) and data tables otherwise, if available (otherwise use models).                                                                                                                                                |
| J                                                                                                                               | Unused placeholder. Be sure to put the J in the keyword string.                                                                 | Unused placeholder. Be sure to put the J in the keyword string.                                                                                                                                                                                           |
| istrg                                                                                                                           | Controls charged-particle straggling. If                                                                                        | Controls charged-particle straggling. If                                                                                                                                                                                                                  |
| istrg                                                                                                                           | istrg = 0 ,                                                                                                                     | use Vavilov model for charged-particle straggling (DEFAULT).                                                                                                                                                                                              |
| istrg                                                                                                                           | istrg = 1 ,                                                                                                                     | use continuous slowing-down approximation for charged-particle straggling.                                                                                                                                                                                |
| J                                                                                                                               | Unused placeholder. Be sure to put the J in the keyword string.                                                                 | Unused placeholder. Be sure to put the J in the keyword string.                                                                                                                                                                                           |
| recl                                                                                                                            | Recoil production control for light-ion tabular physics ( 2 ). If                                                               | Recoil production control for light-ion tabular physics ( 2 ). If                                                                                                                                                                                         |
| recl                                                                                                                            | recl = 0 ,                                                                                                                      | then no recoil ions are produced in tabular physics (DEFAULT).                                                                                                                                                                                            |
| recl                                                                                                                            | 0 < recl ≤ 1 ,                                                                                                                  | recl is the number of recoil ions to be created at each light-ion elastic scatter event in tabular physics regimes. Recoil production can include protons, deuterons, tritons, 3 He, alphas, and heavy ions if they are present on the MODE card. Outside |

|                 |                                                                                                                                                                                                                                                                         | of the tabular physics regime, recoil production is performed by the model physics and is not affected by this setting. Note that this option enables the feature for all light-ion projectiles, regardless of whether protons are on the MODE card or not. See coilf on PHYS : n for the option to enable this for neutron projectiles.   |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| J               | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                                                        | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                                                                                                                           |
| J               | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                                                        | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                                                                                                                           |
| J               | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                                                        | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                                                                                                                           |
| i _ mcs _ model | Controls the choice of Coulomb scattering model. If                                                                                                                                                                                                                     | Controls the choice of Coulomb scattering model. If                                                                                                                                                                                                                                                                                        |
|                 | i _ mcs _ model = - 1                                                                                                                                                                                                                                                   | turn off angular deflection.                                                                                                                                                                                                                                                                                                               |
|                 | i _ mcs _ model = 0 ,                                                                                                                                                                                                                                                   | use FermiLab angular deflection model with Vavilov straggling (DEFAULT).                                                                                                                                                                                                                                                                   |
|                 | i _ mcs _ model = 1 ,                                                                                                                                                                                                                                                   | use Gaussian angular deflection model with Vavilov straggling.                                                                                                                                                                                                                                                                             |
|                 | i _ mcs _ model = 2 ,                                                                                                                                                                                                                                                   | use FermiLab coupled energy/angle MCS model.                                                                                                                                                                                                                                                                                               |
| i _ int _ model | Controls treatment of nuclear interactions. If                                                                                                                                                                                                                          | Controls treatment of nuclear interactions. If                                                                                                                                                                                                                                                                                             |
|                 | i _ int _ model = - 1                                                                                                                                                                                                                                                   | no interactions. This is equivalent to setting the inelastic cross section to zero.                                                                                                                                                                                                                                                        |
|                 | i _ int _ model = 0 ,                                                                                                                                                                                                                                                   | process all interactions (DEFAULT).                                                                                                                                                                                                                                                                                                        |
|                 | i _ int _ model = 1 ,                                                                                                                                                                                                                                                   | no secondaries, inelastic collisions treated as weight reduction.                                                                                                                                                                                                                                                                          |
|                 | i _ int _ model = 2 ,                                                                                                                                                                                                                                                   | no secondaries, inelastic collisions treated as removal.                                                                                                                                                                                                                                                                                   |
| i _ els _ model | Controls treatment of nuclear elastic scattering ( 3 ). If                                                                                                                                                                                                              | Controls treatment of nuclear elastic scattering ( 3 ). If                                                                                                                                                                                                                                                                                 |
|                 | i _ els _ model = - 1                                                                                                                                                                                                                                                   | no elastic scattering (i.e., treat as pseudo collision).                                                                                                                                                                                                                                                                                   |
|                 | i _ els _ model = 0 ,                                                                                                                                                                                                                                                   | elastic scattering by Prael/Liu/Striganov model[236] (DEFAULT).                                                                                                                                                                                                                                                                            |
| efac            | Controls stopping power energy spacing ( 4 ). Restriction: 0 . 8 ≤ efac ≤ 0 . 99 (DEFAULT: efac = 0 . 917 )                                                                                                                                                             | .                                                                                                                                                                                                                                                                                                                                          |
| J               | Unused placeholder. Be sure to put the J in the keyword string.                                                                                                                                                                                                         | Unused placeholder. Be sure to put the J in the keyword string.                                                                                                                                                                                                                                                                            |
| ckvnum          | Scales Cerenkov photon emission from a particular particle by a fractional amount with the photons emitted at higher weight ( 6 ). Allowed values are 0 ≤ ckvnum < 1 ); values of 10 - 3 - 10 - 2 are recommended. ckvnum = 0 turns off Cerenkov emission (DEFAULT: 0). | Scales Cerenkov photon emission from a particular particle by a fractional amount with the photons emitted at higher weight ( 6 ). Allowed values are 0 ≤ ckvnum < 1 ); values of 10 - 3 - 10 - 2 are recommended. ckvnum = 0 turns off Cerenkov emission (DEFAULT: 0).                                                                    |
| drp             | Lower energy delta-ray cutoff ( 5 ) If                                                                                                                                                                                                                                  | Lower energy delta-ray cutoff ( 5 ) If                                                                                                                                                                                                                                                                                                     |
|                 | drp = - 1 ,                                                                                                                                                                                                                                                             | turn on delta-ray production and use the default energy cutoff (0.020 MeV).                                                                                                                                                                                                                                                                |
|                 | drp = 0 ,                                                                                                                                                                                                                                                               | turn off delta-ray production (DEFAULT).                                                                                                                                                                                                                                                                                                   |
|                 | drp > 0 ,                                                                                                                                                                                                                                                               | turn on delta-ray production and set the cutoff to drp MeV, valid for charged particles only.                                                                                                                                                                                                                                              |

1

Default:

PHYS : h 100 0 -1 J 0 J 0 J J J 0 0 0 0.917 0 0

Use: Optional

## Details:

- 1 If emax on the PHYS : e card is less than emax on the PHYS : h card, the MCNP code will internally set the PHYS : h emax to the PHYS : e emax . The parameter emax must be higher than the highest energy in the problem or the physics is wrong. For problems with energies above 100 MeV, emax should be chosen carefully; the default is appropriate for problems with energies below 100 MeV.
- 2 Light ion recoil physics accounts for the ionization potential and uses the proper two-body kinematics (with neutron free-gas thermal treatment if appropriate) to bank recoil particles with the proper energy and angle. The particle-specific low-energy cutoff can be set with the 2nd option, e , on the CUT : P card. For the P ions given on the MODE card, it is recommended to adjust the low-energy cutoff such that recoil ions produced are not killed by energy cutoff. See Table 4.3 for the default low-energy cutoffs for each particle type. Note that protons colliding with hydrogen to produce more protons can produce an overwhelming number of protons. Therefore, caution is required, and recl &lt; 1 may be needed. This capability is the same for incident neutrons as controlled by the coilf keyword on the PHYS : h card.
- 3 Elastic scattering will be ignored if nuclear interactions are turned off.
- 4 When efac is specified, the energy spacing for multiple-scattering tables (stopping power, range, etc.) is determined by

where E 1 is the highest energy and where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

This means that on average, the energy of the particle will decrease by
a factor of two in D energy steps and that a larger value of efac
results in more points in the multiple-scattering tables. The default
value, efac = 0 . 917 , leads to the traditional choice of eight energy
steps for a factor-of-two energy loss.

<!-- formula-not-decoded -->

- 5 Delta-ray production is according to the formulation by B. Rossi [239]. The E -2 differential spectrum is truncated by the drp parameter, which should be greater than 1 keV, with a default value of 20 keV and a maximum of 1.022 MeV. To increase execution speed, this parameter should be set as large as possible, while retaining important effects to tallies of interest.
- 6 Cerenkov photon production requires that a refractive index is specified on the M card.

## 5.7.2.5.1 Example 1

The configuration shown in Listing 5.23 forces all protons transported
to perform analog capture and a recoil ion to be created at each elastic
scatter event.

Listing 5.23: example\_phys\_cut\_nh.mcnp.inp.txt

phys:h 100 100 -1 3J 1

## 5.7.2.6 Other Particles (PHYS: P )

Physics settings for all other particle types are controlled with this
card.

<!-- image -->

| Data-card Form: PHYS i _ els _ model efac J   | : P emax J J J istrg J xmunum ckvnum drp                                                                                                                                                                                            | xmugam J J i _ mcs _ model i _ int _ model                                                                                                                                                                                          |
|-----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| emax                                          | Particles designators other than n , p , e , and h ( 1 ).                                                                                                                                                                           | Particles designators other than n , p , e , and h ( 1 ).                                                                                                                                                                           |
|                                               | Upper energy limit (DEFAULT: emax on PHYS : n card or 100 MeV if no PHYS : n card) ( 2 ).                                                                                                                                           | Upper energy limit (DEFAULT: emax on PHYS : n card or 100 MeV if no PHYS : n card) ( 2 ).                                                                                                                                           |
| J                                             | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                    | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                    |
| J                                             | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                    | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                    |
| J                                             | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                    | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                    |
| istrg                                         | Controls charged-particle straggling. If                                                                                                                                                                                            | Controls charged-particle straggling. If                                                                                                                                                                                            |
| istrg                                         | istrg = 0 ,                                                                                                                                                                                                                         | use Vavilov model with an energy correction addressing stopping powers (DEFAULT).                                                                                                                                                   |
| istrg                                         | istrg = 1 ,                                                                                                                                                                                                                         | use continuous slowing-down ionization model.                                                                                                                                                                                       |
| J                                             | Unused placeholder. Be sure to put the J in the keyword string.                                                                                                                                                                     | Unused placeholder. Be sure to put the J in the keyword string.                                                                                                                                                                     |
| xmunum                                        | Controls the selection of muonic x-ray data. Restriction: Only valid for muons ( PHYS : | ). This PHYS card 7th entry has other meanings for P = n , p e , and h and is ignored for other particles. If                             | Controls the selection of muonic x-ray data. Restriction: Only valid for muons ( PHYS : | ). This PHYS card 7th entry has other meanings for P = n , p e , and h and is ignored for other particles. If                             |
| xmunum                                        | xmunum = - 1 ,                                                                                                                                                                                                                      | use only x-ray literature data. emit all x-rays including data from literature from the MUON/RURP code package [240]                                                                                                                |
| xmunum                                        | xmunum = 1 ,                                                                                                                                                                                                                        | and (DEFAULT).                                                                                                                                                                                                                      |
| xmugam                                        | Probability for emitting k-shell photon (DEFAULT: xmugam = 0 . 65 ). Restriction: Only valid for muons ( PHYS : | card) . This PHYS card 8th entry has other meanings for P = n , p , e , and h and is ignored for other particles. | Probability for emitting k-shell photon (DEFAULT: xmugam = 0 . 65 ). Restriction: Only valid for muons ( PHYS : | card) . This PHYS card 8th entry has other meanings for P = n , p , e , and h and is ignored for other particles. |
| J                                             | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                    | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                    |
| J                                             | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                    | Unused placeholders. Be sure to put the J in the keyword string.                                                                                                                                                                    |
| i _ mcs _ model                               | Controls the choice of Coulomb scattering model. Restriction: Valid for charged particles only. If                                                                                                                                  | Controls the choice of Coulomb scattering model. Restriction: Valid for charged particles only. If                                                                                                                                  |
| i _ mcs _ model                               | i _ mcs _ model = - 1 ,                                                                                                                                                                                                             | turn off angular deflection.                                                                                                                                                                                                        |
| i _ mcs _ model                               | i _ mcs _ model = 0 ,                                                                                                                                                                                                               | use FermiLab angular deflection model with Vavilov straggling (DEFAULT).                                                                                                                                                            |
| i _ mcs _ model                               | i _ mcs _ model = 1 ,                                                                                                                                                                                                               | use Gaussian angular deflection model with Vavilov straggling.                                                                                                                                                                      |
| i _ mcs _ model                               | i _ mcs _ model = 2 ,                                                                                                                                                                                                               | use FermiLab coupled energy/angle MCS model.                                                                                                                                                                                        |
| i _ int _ model                               | Controls treatment of nuclear interactions. If                                                                                                                                                                                      | Controls treatment of nuclear interactions. If                                                                                                                                                                                      |
| i _ int _ model                               | i _ int _ model = - 1 ,                                                                                                                                                                                                             | no interactions. This is equivalent to setting the inelastic cross section to zero.                                                                                                                                                 |

```
i _ int _ model = 0 , process all interactions (DEFAULT). i _ int _ model = 1 , no secondaries, inelastic collisions treated as weight reduction. i _ int _ model = 2 , no secondaries, inelastic collisions treated as removal. i _ els _ model Controls treatment of nuclear elastic scattering ( 3 ) If i _ els _ model = -1 , no elastic scattering (i.e., treat as pseudo collision). i _ els _ model = 0 , elastic scattering by Prael/Liu/Striganov model [236] (DEFAULT). efac Controls stopping power energy spacing ( 4 ). Restriction: 0 . 8 ≤ efac ≤ 0 . 99 ; valid for charged particles only (DEFAULT: efac = 0 . 917 ). J Unused placeholder. Be sure to put the J in the keyword string. ckvnum Scales Cerenkov photon emission from a particular particle by a fractional amount with the photons emitted at higher weight ( 6 ). Allowed values are 0 ≤ ckvnum < 1 ); values of 10 -3 -10 -2 are recommended. ckvnum = 0 turns off Cerenkov emission (DEFAULT: 0). drp Lower energy delta-ray cutoff ( 5 ) If drp = -1 , turn on delta-ray production and use the default energy cutoff (0.020 MeV). drp = 0 , turn off delta-ray production (DEFAULT). drp > 0 , turn on delta-ray production and set the cutoff to drp MeV. Valid for charged particles only.
```

Default:

PHYS : P 100 3J 0 5J 0 0 0 0.917 J 0 0

Default:

PHYS : | 100 3J 0 J 1 0.65 2J 0 0 0 0.917 J 0 0

Use: Optional.

## Details:

- 1 If emax on the PHYS : e card is less than emax on the PHYS : P card, MCNP6 will internally set the PHYS : P emax to the PHYS : e emax . Although heavy ions ( # ) may be designated, there is no heavy ion recoil for proton elastic scattering events.
- 2 The parameter emax must be higher than the highest energy in the problem or the physics is wrong. For problems with energies above 100 MeV, emax should be chosen carefully; the default is appropriate for problems with energies below 100 MeV.
- 3 Elastic scattering will be ignored if nuclear interactions are turned off.
- 4 When efac is specified, the energy spacing for multiple-scattering tables (stopping power, range, etc.) is determined by

<!-- formula-not-decoded -->

where E 1 is the highest energy and where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

This means that on average, the energy of the particle will decrease by
a factor of two in D energy steps and that a larger value of efac
results in more points in the multiple-scattering tables. The default
value, efac = 0 . 917 , leads to the traditional choice of eight energy
steps for a factor-of-two energy loss.

- 5 Delta-ray production is according to the formulation by B. Rossi [239]. The E -2 differential spectrum is truncated by the drp parameter, which should be greater than 1 keV, with a default value of 20 keV and a maximum of 1.022 MeV. To increase execution speed, this parameter should be set as large as possible, while retaining important effects to tallies of interest.
- 6 Cerenkov photon production requires that a refractive index is specified on the M card.

## 5.7.3 ACT: Activation Control Card

Available delayed particles are: neutrons, gammas, betas, alphas, and
positrons. Delayed-neutron emission can be calculated using library ( dn
= library ) or model ( dn = model ) treatments. The library treatment
uses ACE data and produces delayed neutrons only for fission. The model
treatment uses data from the delay \_ library \_ v5.dat library and
produces delayed neutrons for fission and, if requested, activation.
Delayed-gamma emission is calculated by line emission data ( dg = lines
), from ENDF/B-VII.1 data contained in cindergl.dat and augmented by
model data contained in delay \_ library \_ v5.dat , or only model data (
dg = mg ). Delayed betas, alphas, and positrons are sampled solely from
delay \_ library \_ v5.dat data.

The delay \_ library \_ v5.dat delayed-particle library provides unique
delayed neutron, gamma, beta, alpha, and positron spectra to be sampled
for each radionuclide. Delayed neutron spectra are sampled from 750 bins
ranging from 0-7.5 MeV for 298 nuclides. Delayed gamma spectra are
sampled from 500 bins ranging from 0-10 MeV for 1865 nuclides ( 3 , 4 ).
Delayed beta spectra are sampled from 100 bins ranging from 0-10 MeV for
1891 nuclides. Delayed positron spectra are sampled from 100 bins
ranging from 0-10 MeV for 531 nuclides. Delayed alpha spectra are
sampled from 100 bins ranging from 0-10 MeV for 248 nuclides. A warning
is issued when no delayed particle data is available and a nuclide with
a non-zero delayed-particle probability is sampled.

Delayed-gamma emission is limited to fixed source ( SDEF ) problems.

## Data-card Form: ACT KEYWORD = value(s)

fission

Type of delayed particle(s) to be produced from residuals created by
fission. If fission = none ,

fission = n , p , e , f , a , create no delayed particles from fission
events.

create delayed neutrons ( n ), delayed gammas ( p ), delayed beta
particles ( e ), delayed positron particles ( f ), and/or delayed alphas
( a ) from fission events. Only those listed will be created (DEFAULT:
fission = n ).

|                       | fission = all ,                                                                                                                                                                                                                                                                                                                        | create all delayed particles from fission events.                                                                                                                                                                                                                                                                                      |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| nonfiss               | Type of delayed particle(s) to be produced by simple multi-particle reaction activation (i.e., non-fission) events. If                                                                                                                                                                                                                 | Type of delayed particle(s) to be produced by simple multi-particle reaction activation (i.e., non-fission) events. If                                                                                                                                                                                                                 |
|                       | nonfiss = none ,                                                                                                                                                                                                                                                                                                                       | create no delayed particles from non-fission events (DEFAULT).                                                                                                                                                                                                                                                                         |
|                       | nonfiss = n , p , e , f , a                                                                                                                                                                                                                                                                                                            | , create delayed neutrons ( n ), delayed gammas ( p ), delayed beta particles ( e ), delayed positron particles ( f ), and/or delayed alphas ( a ) from non-fission events. Only those listed will be created.                                                                                                                         |
|                       | nonfiss = all ,                                                                                                                                                                                                                                                                                                                        | create all delayed particles from non-fission events.                                                                                                                                                                                                                                                                                  |
| dn                    | Delayed neutron data source. If                                                                                                                                                                                                                                                                                                        | Delayed neutron data source. If                                                                                                                                                                                                                                                                                                        |
|                       | dn = model ,                                                                                                                                                                                                                                                                                                                           | production of delayed neutrons uses models only ( 1 ).                                                                                                                                                                                                                                                                                 |
|                       | dn = library ,                                                                                                                                                                                                                                                                                                                         | production of delayed neutrons uses libraries only (DEFAULT).                                                                                                                                                                                                                                                                          |
|                       | dn = both ,                                                                                                                                                                                                                                                                                                                            | production of delayed neutrons uses models when libraries are missing.                                                                                                                                                                                                                                                                 |
|                       | dn = prompt ,                                                                                                                                                                                                                                                                                                                          | treat prompt and delayed neutrons as prompt.                                                                                                                                                                                                                                                                                           |
| dg                    | Delayed gamma data source ( 2 ). If                                                                                                                                                                                                                                                                                                    | Delayed gamma data source ( 2 ). If                                                                                                                                                                                                                                                                                                    |
|                       | dg = lines ,                                                                                                                                                                                                                                                                                                                           | sample delayed gammas using models based on line-emission data contained in cindergl.dat , augmented by data in the latest delay _ library _ v[n].dat .                                                                                                                                                                                |
|                       | dg = mg ,                                                                                                                                                                                                                                                                                                                              | sample delayed gammas using models based on 25-group emission data ( 3 ).                                                                                                                                                                                                                                                              |
|                       | dg = none ,                                                                                                                                                                                                                                                                                                                            | do not create delayed gammas (DEFAULT).                                                                                                                                                                                                                                                                                                |
| thresh = f            | The fraction of highest-amplitude discrete delayed-gamma lines, f , that will be retained ( 4 ) (DEFAULT: = 0 . 95 ).                                                                                                                                                                                                                  | The fraction of highest-amplitude discrete delayed-gamma lines, f , that will be retained ( 4 ) (DEFAULT: = 0 . 95 ).                                                                                                                                                                                                                  |
| dnbias = n            | Produce up to n delayed neutrons per interaction (DEFAULT: analog calculation). Restriction: 1 ≤ n ≤ 10 ; dnbias is disallowed in calculations.                                                                                                                                                                                        | Produce up to n delayed neutrons per interaction (DEFAULT: analog calculation). Restriction: 1 ≤ n ≤ 10 ; dnbias is disallowed in calculations.                                                                                                                                                                                        |
| nap = m               | The integer number m of activation products for which cumulative distribution functions will be calculated once and stored for reuse. The m most frequently accessed distribution functions are dynamically updated during execution. The nap keyword is applicable to ACT nonfiss problems using line data only (DEFAULT: nap = 10 ). | The integer number m of activation products for which cumulative distribution functions will be calculated once and stored for reuse. The m most frequently accessed distribution functions are dynamically updated during execution. The nap keyword is applicable to ACT nonfiss problems using line data only (DEFAULT: nap = 10 ). |
| dneb = w1 , e1 , w2 , | . . , wK , eK Delayed neutron                                                                                                                                                                                                                                                                                                          | . . , wK , eK Delayed neutron                                                                                                                                                                                                                                                                                                          |
|                       | wk                                                                                                                                                                                                                                                                                                                                     | energy biasing parameters where is the weight for the k th energy bin, and                                                                                                                                                                                                                                                             |
|                       | ek                                                                                                                                                                                                                                                                                                                                     | is the upper energy for the k th energy bin (initial lower bin bound of 0 assumed).                                                                                                                                                                                                                                                    |
|                       | Energies within a bin are sampled evenly; probability of sampling from within a bin is based upon wk ( 5 ).                                                                                                                                                                                                                            | Energies within a bin are sampled evenly; probability of sampling from within a bin is based upon wk ( 5 ).                                                                                                                                                                                                                            |

dgeb = w1 , e1 , w2 , e2 , . . . , wK , eK Delayed photon energy biasing
where wk is the weight for the k th energy bin, and ek is the upper
energy for the k th energy bin (initial lower bin bound of 0 assumed).
Energies within a bin are sampled evenly; probability of sampling from
within a bin is based upon wk ( 5 ). pecut = e Delayed-gamma energy
cutoff (MeV). Gamma lines below pecut will be expunged (DEFAULT: pecut =
0 ). hlcut = t Spontaneous-decay half-life threshold (seconds). Decay
chains are truncated when a daughter half-life exceeds hlcut . Delayed-
particle production from this and subsequent daughters is omitted
(DEFAULT: hlcut = 0 , i.e., no truncation of decay chains). sample Flag
for correlated or uncorrelated. If sample = correlate , treat as
correlated. sample = nonfiss \_ cor , treat as uncorrelated.

## Details:

- 1 Delayed-particle emission is currently integrated over 10 10 seconds with 99 time steps; however, the user should consider increasing the stability half-life parameter (10th entry on the DBCN card) when emission from long-lived radionuclides is important. Increasing this parameter results in an increase in the time integration to 10 19 seconds with 234 time steps.
- 2 The fission keyword enables delayed-particle emission from the decay of radioactive fission products created by neutron- or photon-induced fission treated by ACE libraries or any fission event treated by model physics. The nonfiss keyword enables delayed-particle emission from the decay of radioactive residuals created by neutron and photon interactions treated by ACE libraries or any nuclear interaction treated by model physics. Most neutron ACE libraries contain the necessary secondary-production cross sections needed to determine radioactive residuals, however few ACE photonuclear libraries currently contain this data. Thus, users should consider the use of photonuclear model physics (see the MX card) or obtain updated ACE photonuclear libraries in which secondary reactions are not lumped into MT = 5 . Proton ACE library interactions also suffer from this issue.
- 3 Bin-wise emission ( dg = mg ) is preferred when individual line-amplitude detail is not important. This option is significantly faster and the emission spectra will converge more quickly than line emission mode (i.e., dg = lines ). Line emission augmented with bin-wise emission ( dg = lines ) is useful for studies that require high fidelity, detailed-amplitude emission spectra. This option is significantly slower and can require the execution of large numbers of histories to suitably converge low probability delayed-gamma emission lines.
- 4 Set thresh = 1 . 0 to retain all lines in the cindergl.dat file.

## /warning\_sign Caution

For some problems (e.g., fission), the calculation with thresh = 1 . 0
will either run slowly or exceed memory limits and fail.

- 5 A weight of zero should not be set for any of the energy bins with dgeb or dneb . Instead, a small value (e.g., 0.001) is recommended [241].

## 5.7.4 Physics Cutoffs

## 5.7.4.1 CUT: Time, Energy, and Weight Cutoffs

<!-- image -->

| Data-card Form: CUT : P t e wc1 wc2 swtm   | Data-card Form: CUT : P t e wc1 wc2 swtm                                                                                                                                                                                                       |
|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P                                          | Particle designator.                                                                                                                                                                                                                           |
| t                                          | Time cutoff in shakes, 1 shake = 10 - 8 s ( 1 , 2 ).                                                                                                                                                                                           |
| e                                          | Lower energy cutoff in MeV ( 1 , 3 ).                                                                                                                                                                                                          |
| wc1 , wc2                                  | Weight cutoffs. If weight goes below wc2 roulette is played to restore weight to wc1 . Negative entries scale weight cutoff relative to the minimum source weight of a particle ( 4 ). Setting wc1 = wc2 = 0 invokes analog capture ( 5 , 6 ). |
| swtm                                       | Minimum source weight ( 7 , 8 ).                                                                                                                                                                                                               |

Neutron default: t is very large, e = 0 . 0 MeV, wc1 = -0 . 50 , wc2 =
-0 . 25 , swtm is the minimum source weight if the general source is
used.

Photon default: t is the neutron cutoff time, e = 0 . 001 MeV, wc1 = -0
. 50 , wc2 = -0 . 25 , swtm is the minimum source weight if the general
source is used; if there are pulse-height tallies, wc1 = wc2 = 0 ,
unless forced collisions are also used; if pulse-height tallies exist
with forced collisions, the default values are wc1 = -0 . 50 and wc2 =
-0 . 25 .

Electron default: t is the neutron cutoff time, e = 0 . 001 MeV, wc1 = 0
, wc2 = 0 , swtm is the minimum source weight if the general source is
used; if there are pulse-height tallies, wc1 = wc2 = 0 , unless forced
collisions are also used; if pulse-height tallies exist with forced
collisions, the default values are wc1 = -0 . 50 and wc2 = -0 . 25 .

With the exception of photon energy and electron/positron energy (see
§5.7.4.2 and §5.7.4.3), the default energy cutoff values for all
particles appear in Table 4.3. All other particle time and weight
default cutoffs are the same as for electrons.

Use: Optional, as needed. Analog capture is highly recommended when
using weight windows and for many other applications.

## Details:

- 1 If a particle's time exceeds the t specified for that particle, it is killed. Although MCNP6 is time dependent, particle decay is not considered. Any particle with energy lower than the e specified for that particle is killed.
- 2 The default (and maximum) emission time for delayed particle emission is 10 10 s. By using the CUT card(s), the maximum emission time becomes (1) the particle's time cutoff if time cutoff is specified or (2) the minimum of time cutoff if multiple time cutoffs are provided.

- 3 For adjoint ( MGOPT ) problems, e is the upper energy cutoff, not the lower energy cutoff.
- 4 For non-analog capture, if a particle's weight w falls below wc2 times the ratio R of the source cell importance to the current cell importance, then with probability

<!-- formula-not-decoded -->

the particle survives and is assigned w = wc1 × R . If negative values
are entered for the weight cutoffs, the values | wc1 | w s and | wc2 | w
s will be used for wc1 and wc2 , respectively, where w s is the minimum
starting weight assigned to a source particle from an MCNP6 general
source. Scaling the weight cutoff to the minimum source weight of a
particle prevents source particles from being immediately killed by
falling below the cutoff. These negative entries are recommended over
positive entries for most problems. If only wc1 is specified, then wc2 =
0 . 5 wc1 .

- 5 If wc1 is set to zero, capture is treated explicitly by analog rather than implicitly by reducing the particles' weight according to the capture probability. If ean or emcnf = emax on the PHYS : P card (i.e., applies to neutrons or protons), analog capture is used regardless of the value of wc1 except for particles leaving a DXTRAN sphere.
- 6 To generate delayed particles from non-fissioning isotopes, wc1 must be set to zero on both the photon and neutron CUT : P cards so that analog capture is invoked.
- 7 When the source is biased in any way, there will be a fluctuation in starting source weights. By playing the weight cutoff game relative to the minimum source weight, the weight cutoff in each cell is the same regardless of starting source weight. Note that if the source weight can go to zero, the minimum source weight is set to 10 -10 times the value of the wgt parameter on the SDEF card.
- 8 The parameter swtm can be used to make the weight cutoffs relative to the minimum starting weight of a source particle for a user source, as is done automatically for the general source. The entry will, in general, be the minimum starting weight of all source particles, including the effects of energy and direction biasing. The entry is also effective for the general source. Then swtm is multiplied by the wgt entry on the SDEF card, but is unaffected by any directional or energy biasing. This entry is ignored for a KCODE calculation.

## 5.7.4.2 Additional Photon Cutoff Notes

The CUT : p weight cutoffs are analogous to those on the CUT : n card
except that they are used only for energies above the emcpf entry on the
PHYS : p card. If wc1 = 0 , analog capture is specified for photons of
energy greater than emcpf . For energies below emcpf , analog capture is
the only choice with one exception: photons leaving a DXTRAN sphere.
Their weight is always checked against the CUT : p weight cutoff upon
exiting. If only wc1 is specified, then wc2 = 0 . 5 wc1 .

In a coupled neutron/photon problem, the photon weight cutoffs are the
same as the neutron weight cutoffs unless overridden by a CUT : p card.

In a coupled neutron/photon problem, photons are generated before the
neutron weight cutoff game is played.

Although the default photon energy cutoff is 1 keV, a user may
explicitly specify a lower cutoff down to 1 eV. The required photoatomic
cross sections from ENDF/B-VI, release 8, are included in the data
library EPRDATA14 (Electron-Photon-Relaxation DATA). The tables in this
library are presented in a newly developed ACE format specifically
designed for use with MCNP6. They cannot be used correctly with the
earlier codes MCNP5 or MCNPX. The proper tables can be requested on
material cards using the library identifier '.14p'. Users are cautioned
that at very low energies, molecular and other effects become important
for scattering and absorption, and these more complex effects are not
yet included in the photon transport methods. Also,

note that although electron transport has been extended down to 10 eV,
electron energies have not been extended as low as photon energies.

MCNP6 allows only analog capture below 0.001 MeV. Because the
photoelectric cross section is virtually 100% of the total cross section
below that energy for all isotopes, tracks will be quickly captured and
terminated.

## 5.7.4.3 Additional Electron/Positron Cutoff Notes

Positron physics in MCNP6 is identical to electron physics, except for
tracking directions in magnetic fields and consideration of positron
annihilation. Whereas electrons below the energy cutoff are terminated,
positrons below the energy cutoff produce annihilation photons. The
positrons have a positive charge and may be tallied using the FT card
elc option [§5.9.18.8]. Electron transport, which has a default cutoff
of 1 keV, may be explicitly specified down to 10 eV.

To transport electrons at energies below 1 keV, the EPRDATA14 library is
required. As with low-energy photon transport, the proper tables can be
requested with the library identifier '.14p'. Also as with photons, the
same cautions regarding temperature, molecular, solid-state, and other
low-energy phenomena apply to low-energy electrons.

For very low-energy electrons, a physics-based practical difficulty can
arise: the lack of energy-loss-inducing processes. Although
bremsstrahlung is still present, it is completely dominated by electron
elastic scattering, which results in no energy loss. Electro-ionization,
an important energy-loss channel, vanishes below the binding energy of
the least-bound shell given in the data. Whether that event occurs above
or below 10 eV is element-dependent. Excitation, another energy-loss
process, also can vanish at some energy above 10 eV, depending on the
element. Consequently, there can be a small energy range just above 10
eV in which the electron can no longer lose energy and only experiences
a large number of elastic scatterings. Coupled with the very short step
sizes that characterize electron transport at low energies, the effect
is that the transport suddenly grinds nearly to a halt because an
electron has become trapped, taking a huge number of small steps with
little or no opportunity to lose energy. Such an electron is very close
to the energy cutoff, but cannot get there because it is spending all
its time in elastic scatter. Preliminary practical experience indicates
that setting the electron cutoff no lower than about 12 eV may be
sufficient to avoid this occasional effect. Again note that the low-
energy cross-section data are only for cold atomic targets, and that
potential future treatments of molecular and other low-energy physics
will significantly alter this discussion.

## 5.7.4.4 Example 1

The configuration shown in Listing 5.24 causes the neutron energy cutoff
to be increased from zero to 0.99999 eV, the proton energy cutoff to be
lowered to zero, and the weight cutoff roulette parameters set to zero
to force analog proton capture. Note that increasing the neutron energy
cutoff should only be done in circumstances where fissile material is
not involved in the simulation. In general, it is not recommended.

```
1 cut:n J 0.99999e-6 2 cut:h J 0 0 0
```

Listing 5.24: example\_phys\_cut\_nh.mcnp.inp.txt

## 5.7.4.5 Example 2

The configuration shown in Listing 5.25 lowers the photon and electron
energy cutoffs to 1 eV and 10 eV, respectively. This allows for the
single event electron treatment to be used for the electron transport
from the electron \_ method \_ boundary energy specified on the PHYS : e
card down to 10 eV.

1

2

cut:p j 1e-6

cut:e j

```
1e-5
```

## 5.7.4.6 ELPT: Cell-by-Cell Energy Cutoff

| Cell-card Form: ELPT : P x or Data-card Form: ELPT : P x1 x2 . . . xJ   | Cell-card Form: ELPT : P x or Data-card Form: ELPT : P x1 x2 . . . xJ                           |
|-------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| P                                                                       | Particle designator.                                                                            |
| x                                                                       | Lower energy cutoff of cell.                                                                    |
| xj                                                                      | Lower energy cutoff of cell j . Number of entries, J , equals number of cells in problem ( 1 ). |

Default: Use cutoff parameters from CUT : P

Use: Optional. For cell-dependent energy cutoff.

## Details:

- 1 A separate lower energy cutoff can be specified for each cell in the problem. The higher of either the value on the ELPT : P card or the global value e on the CUT : P card applies.

## 5.7.5 TMP: Free-Gas Thermal Temperature

The TMP cards provide the MCNP code with the time-dependent thermal cell
temperatures that are necessary for the free-gas thermal treatment of
low-energy neutron transport. This treatment becomes important when the
neutron energy is less than about four times the temperature of heavy
nuclei or less than about 400 times the temperature of light nuclei.
Thus, the TMP cards should be used when parts of the problem are not at
room temperature and neutrons are transported with energies within a
factor of 400 from the thermal temperature.

The TMP card has two effects. The first is that the value of TMP is used
during neutron collision kinematics to properly compute the outgoing
energy spectrum due to a free-gas moving target. A simple constant
cross-section approximation is used in normal operation. Using the DBRC
card will additionally remove this constant approximation and is
recommended if the necessary 0 K libraries are available.

The second involves an adjustment to the neutron elastic scattering
cross section itself. If the cell card temperatures all match and are
the same as the nuclear data temperature, no adjustment is made. If the
cell card temperatures all match but do not match the nuclear data
temperature, the elastic scattering cross section is re-broadened using
an approximate method to the cell temperatures. If the cell card
temperatures do not match, the elastic cross section is un-broadened to
0 K and broadened on-the-fly to the cell temperature using this same
approximation.

The approximation used makes two assumptions: the elastic scattering
cross section at 0 K is constant and all other cross sections at 0 K are
proportional to 1 /v . From this, the elastic scattering cross section
is divided

Listing 5.25: example\_phys\_e.mcnp.inp.txt

Figure 5.5: Application of TMP card on 900 K 238 U data to adjust temperature to 293.6 K.

<!-- image -->

by the broadened constant value at the old temperature and multiplied by
the broadened constant value at the new temperature. Because nuclear
data follows these assumptions at the asymptotic 0 eV limit, this is
generally accurate at energies below the influence of the lowest-energy
resonance. However, this assumption does not handle resonances
whatsoever. The effect of this algorithm on 900 K 238 U data can be seen
in Fig. 5.5. On the left, the de-broadened 900 K data closely follows
the 293.6 K value at low energies. On the right, however, the 6.67 eV
resonance is unchanged and still follows the 900 K value.

For maximum accuracy, whenever the entire geometry is not room
temperature, it is recommended to set the TMP card on all cells that
contain a nuclear data library to the temperature of that nuclear data
library. Without TMP cards, the scattering cross section will be
adjusted to room temperature using the approximation mentioned above.

```
Cell-card Form: TMPn t or Data-card Form: TMP n tn1 tn2 . . . tnJ or Data-card Form: TMP t1 t2 . . . tJ n Index of time on the thermal time ( THTME ) card. Restriction: n ≤ 99 . t Temperature of cell at time index n , in MeV ( 1 , 2 ). tnj Temperature of cell j at time index n , in MeV. Number of entries equals number of cells in the problem ( 1 , 2 ). tj Temperature of cell j at all times, in MeV. Number of entries equals number
```

of cells in the problem (no THTME is card is present; 2 ).

Default: tnj = 2 . 53 × 10 -8 MeV, room temperature, for all cells of
the problem.

Use: Optional. Required when THTME card is used. Needed for low-energy
neutron transport at other than room temperature. A fatal error occurs
if a zero temperature is specified for a non-void cell.

## Details:

- 1 Cell thermal temperatures at times between two entries are determined by linear interpolation. Times before the first time value or after the last time value use the thermal temperature(s) at the nearest time entry.
- 2 The thermal temperature of a cell is denoted by kT in units of MeV. The conversions in Table 5.9 may be convenient.

## 5.7.6 THTME: Thermal Times

The THTME card specifies the times at which the thermal temperatures on
the TMP n cards are provided. For example, the temperatures on the TMP1
card are at t 1 on the THTME card; the temperatures on the TMP2 card are
at time t 2 on the THTME card, etc. The times must be monotonically
increasing. For each entry on the THTME card, there must be a TMP n
card.

## Data-card Form: THTME t1 t2 . . . tj

tj

Time in shakes ( 10 -8 s) at which thermal temperatures are specified on
the TMP j card(s). Number of entries is equal to the total number of
thermal times specified. Restriction: j ≤ 99 .

Default: Zero; temperature is not time dependent.

Use: Optional. Use with TMP card(s).

## 5.7.7 DBRC: Doppler Broadening Resonance Correction

A Doppler broadening resonance correction (DBRC) treatment is
implemented to address known deficiencies in the free-gas scattering
model [242, 243]. Modifications to the free-gas scattering treatment
that account for non-constant scattering cross sections have been
proposed and tested in previous versions of the MCNP

Table 5.9: Temperature Conversion Factors

| Unit of T   | kT (MeV)                           |
|-------------|------------------------------------|
| K           | T × 8 . 617 × 10 - 11              |
| ◦ C         | ( T +273 . 15) × 8 . 617 × 10 - 11 |
| ◦ R         | T × 4 . 787 × 10 - 11              |
| ◦ F         | ( T +459 . 67) 4 . 787 10 - 11     |

×

×

1

2

code [244-246]. With availability of 0-K nuclear cross sections that are
needed to apply the DBRC treatment, the previously tested treatments are
available through the DBRC data card.

To use the DBRC treatment, data tables with preprocessed energy and
scattering cross section pairs at 0 K are prepared using the dbrc \_ make
\_ lib code (see §E.1). This code is included in the MCNP6 distribution
in the MCNP \_ CODE/Utilities/DBRC \_ LIB directory. Both the DBRC \_
endf71.txt and DBRC \_ endf80.txt files distributed are installed within
the MCNP \_ DATA directory are products of the dbrc \_ make \_ lib code
based on the 0-K scattering data from the ENDF/B-VII.1 or ENDF/B-VIII.0
nuclear data libraries, respectively. Further information on the DBRC
code, data files, implementation and testing is available in a separate
report [247].

The DBRC input card provides user control over the DBRC treatment. If
the DBRC card is not present among the data cards, then the traditional
free-gas scattering treatment is used, with free-gas scattering for 1 H
at all energies and free-gas scattering at energies below 400 kT (10.12
eV at room temperature) for all other nuclides (for energies higher than
the range of S ( α, β ) [§2.3.6] data if used for a nuclide).

If the DBRC card is present among the data cards, then the following
keyword-value options are available:

## Data-card Form: DBRC KEYWORD = values(s)

endf = nn emax = eee

isos

=

iso \_ list library identifier for selecting scattering data at 0 K.

- Default data available include nn = 71 or nn = 80 , representing ENDF/B-VII.1 or ENDF/B-VIII.0 scattering data, respectively.
- The DBRC \_ endf nn .txt file in the DATAPATH contains all of the preprocessed 0-K scattering data for a given library.
- This entry is required if one or more nuclides are listed in the iso \_ list .
- Note that 0-K data cannot be mixed between libraries.

the upper energy limit for applying DBRC for all nuclides except 1 H, in
units of MeV.

- The default is 2 . 1 × 10 -4 MeV.
- If eee is specified and the iso \_ list is not present, then conventional free-gas scattering is performed for all nuclides up to eee , rather than the traditional 400 kT limit.
- eee must be less than or equal to the DBRC \_ endf nn .txt datafile upper limit, currently 2 . 5 × 10 -4 MeV.

list of one or more target identifiers [§1.2.2]. All target formats are
allowed.

- The DBRC treatment applies to every isotope listed in all materials.

Default: Use traditional free-gas scattering treatment.

Use: Optional.

## 5.7.7.1 Example 1

The data card in Listing 5.26 will apply the DBRC treatment to 238 U,
using the ENDF/B-VII.1 0-K scattering cross sections, and a default
energy cutoff of 2 . 1 × 10 -4 MeV.

```
dbrc endf=71 emax=2.10e-4 isos=U-238 m1 U-238.83c 1
```

Listing 5.26: example\_dbrc\_1.mcnp.inp.txt

1

2

3

4

5

6

7

8

9

## 5.7.7.2 Example 2

The data card in Listing 5.27 will apply the DBRC treatment to 234 U,
235 U, 236 U, and 238 U, using the ENDF/B-VIII.0 0-K scattering cross
sections, and an energy cutoff of 2 . 3 × 10 -4 MeV.

Listing 5.27: example\_dbrc\_2.mcnp.inp.txt

| dbrc   | endf=80   | emax=2.3e-4   |
|--------|-----------|---------------|
| m1     | U-234.00c | 0.011150      |
|        | U-235.00c | 0.97694       |
|        | U-236.00c | 0.0019919     |
|        | U-238.00c | 0.0099250     |
| m2     | H-1.00c   | 0.66667       |
|        | O-16.00c  | 0.33320       |
|        | O-17.00c  | 1.3333e-4     |
| mt2    | h-h2o     |               |

## 5.7.8 Model Physics and Physics Models

## 5.7.8.1 MPHYS: Model Physics Control

The use of physics models is controlled with the MPHYS card. When
isotopes that are missing cross-section libraries in a problem or when
reactions exceed a library's maximum energy, MCNP6's behavior can change
whether physics models are being used or not.

| Data-card Form: MPHYS toggle   | Data-card Form: MPHYS toggle                                                       |
|--------------------------------|------------------------------------------------------------------------------------|
| toggle                         | Control to enable or disable model physics. If the value of toggle is              |
| toggle                         | on , then model physics are enabled (default for particles other than n , p , e ). |
| toggle                         | off , indicates that model physics are disabled (default for n , p , e ).          |

Default: All MODE n p e problems (and subsets) run with physics models
off ( MPHYS off ) by default. Any particle on the MODE card other than n
, p , or e will automatically activate the use of physics models ( MPHYS
on ).

Use: To disable the use of physics models, set MPHYS off . To enable the
use of physics models, set MPHYS on or include the MPHYS card with no
entries.

## 5.7.8.2 Physics Models Options

Five cards ( LCA , LCB , LCC , LEA , and LEB ) control physics
parameters for the Bertini [248, 249], ISABEL [250, 251], CEM03.03 and
LAQGSM03.03 [200-216], and INCL4 [252] with ABLA [253, 254] options. All
of the input values on the five cards have defaults, which will be taken
in the absence of the cards, or with the use of the J input option.

These MCNP6 input cards provide the user control of physics options. A
summary of the cards follows. The options controlling the Bertini and
ISABEL physics modules are taken from [255]. The user is referred to
that document for further information.

Table 5.10: Permissible Model Physics Combinations

|                 | LCA   | 3rd entry ( iexisa )   |   LCA | entry ( icem )   | 7th entry ( ievap )   |
|-----------------|-------|------------------------|-------|------------------|-----------------------|
| Bertini/Dresner | 1     |                        |     0 |                  |                       |
| ISABEL/Dresner  | 2     |                        |     0 |                  |                       |
| Bertini/ABLA    | 1     |                        |     0 |                  |                       |
| ISABEL/ABLA     | 2     |                        |     0 |                  |                       |
| CEM03.03        | N/A   |                        |     1 |                  | N/A                   |
| INCL4/Dresner   | 0     |                        |     2 |                  |                       |
| INCL4/ABLA      | 0     |                        |     2 |                  |                       |

Table 5.10 shows how different combinations of physics models are
possible using the 3rd and 9th entries on the LCA card, iexisa and icem
, and the 7th entry on the LEA card, ievap . The CEM03.03 model contains
an intranuclear cascade model and evaporation/fission models; therefore,
the iexisa and ievap options are not applicable when icem = 1 .

## /warning\_sign Caution

Combinations of options for the physics models should be chosen with
careful consideration. Although many combinations are allowed,
inappropriate choices can lead to incorrect results.

## 5.7.8.2.1 LCA

The LCA card is used to select the Bertini, ISABEL, CEM03.03, or INCL4
model, as well as to set certain parameters used in Bertini and ISABEL.
CEM03.03 is a self-contained package with no user-adjustable options
presently defined.

glyph[negationslash]

<!-- image -->

|       | Controls elastic scattering. If                                       | Controls elastic scattering. If                                                                                                                                                                          |
|-------|-----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|       | ielas = 0 ,                                                           | then no nucleon elastic scattering.                                                                                                                                                                      |
|       | ielas = 1 ,                                                           | then elastic scattering for neutrons only.                                                                                                                                                               |
|       | ielas = 2 ,                                                           | then elastic scattering for neutrons and protons (DEFAULT).                                                                                                                                              |
| ipreq | Controls pre-equilibrium model [256] for Bertini and ISABEL ( 1 ). If | Controls pre-equilibrium model [256] for Bertini and ISABEL ( 1 ). If                                                                                                                                    |
| ipreq | ipreq = 0 ,                                                           | no pre-equilibrium model will be used.                                                                                                                                                                   |
| ipreq | ipreq = 1 ,                                                           | use pre-equilibrium model after intranuclear cascade (DEFAULT).                                                                                                                                          |
| ipreq | ipreq = 2 and iexisa = 0 ,                                            | ipreq = 2 and iexisa = 0 ,                                                                                                                                                                               |
| ipreq |                                                                       | select ipreq = 1 and ipreq = 3 randomly, with an energy-dependent probability that goes to ipreq = 3 at low energies and to ipreq = 1 at high incident energies. If iexisa = 0 , defaults to ipreq = 1 . |
| ipreq | ipreq = 3 and iexisa = 0 ,                                            | ipreq = 3 and iexisa = 0 ,                                                                                                                                                                               |
| ipreq |                                                                       | use pre-equilibrium model instead of the intranuclear cascade. If iexisa = 0 , defaults to ipreq = 1 .                                                                                                   |

glyph[negationslash]

| iexisa   | Controls model choice ( 2 , 3 ). If                                                                 | Controls model choice ( 2 , 3 ). If                                                                                                                                                                 |
|----------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|          | iexisa = 0 ,                                                                                        | do not use ISABEL intranuclear cascade (INC) model for any particle (DEFAULT if icem = 2 , which specifies the INCL4 model).                                                                        |
|          | iexisa = 1 ,                                                                                        | use Bertini model for nucleons and pions and ISABEL model for other particle types (DEFAULT).                                                                                                       |
|          | iexisa = 2 ,                                                                                        | use ISABEL model for all incident particle types.                                                                                                                                                   |
| ichoic   | Four integers ( ijkl ) that control ISABEL intranuclear cascade model (DEFAULT: ichoic = 0023 ). If | Four integers ( ijkl ) that control ISABEL intranuclear cascade model (DEFAULT: ichoic = 0023 ). If                                                                                                 |
|          | i = 0 ,                                                                                             | use partial Pauli blocking (DEFAULT).                                                                                                                                                               |
|          | i = 1 ,                                                                                             | use total Pauli blocking.                                                                                                                                                                           |
|          | i = - 2 ,                                                                                           | do not use Pauli blocking (not recommended).                                                                                                                                                        |
|          | j = 0 ,                                                                                             | no interaction between particles already excited above the Fermi sea (DEFAULT).                                                                                                                     |
|          | j > 0 ,                                                                                             | j is the number of time steps to elapse between such 'CAS-CAS' interactions.                                                                                                                        |
|          | k = 0 ,                                                                                             | use Meyer's density prescription with 8 steps.                                                                                                                                                      |
|          | k = 1 ,                                                                                             | use original (isobar) density prescription with 8 steps.                                                                                                                                            |
|          | k = 2 ,                                                                                             | use Krappe's folded-Yukawa prescription for radial density in 16 steps, with a local density approximation to the Thomas-Fermi distribution for the (sharp cutoff) momentum distribution (DEFAULT). |
|          | k = 3 ,                                                                                             | the choice is the same as k = 0 but using the larger nuclear radius of the Bertini model.                                                                                                           |
|          | k = 4 ,                                                                                             | the choice is the same as k = 1 but using the larger nuclear radius of the Bertini model.                                                                                                           |
|          | k = 5 ,                                                                                             | the choice is the same as k = 2 but using the larger nuclear radius of the Bertini model.                                                                                                           |
|          | l = 1 ,                                                                                             | perform reflection and refraction at the nuclear surface, but no escape cutoff for isobars.                                                                                                         |
|          | l = 2 ,                                                                                             | perform reflection and refraction at the nuclear surface, with escape cutoff for isobars.                                                                                                           |
|          | l = 3 ,                                                                                             | perform no reflection or refraction, with escape cutoff for isobars (DEFAULT).                                                                                                                      |
|          | l = 4 ,                                                                                             | the choice is the same as l = 1 but using a 25 -MeV potential well for pions.                                                                                                                       |
|          | l = 5 ,                                                                                             | the choice is the same as l = 2 but using a 25 -MeV potential well for pions.                                                                                                                       |
|          | l = 6 ,                                                                                             | the choice is the same as l = 3 but using a 25 -MeV potential well for pions.                                                                                                                       |
| jcoul    | Controls Coulomb barrier for incident charged particles. If                                         | Controls Coulomb barrier for incident charged particles. If                                                                                                                                         |

<!-- image -->

|         | jcoul = 1 ,                                                                                                                                                                                                         | the Coulomb barrier is on (DEFAULT).                                                                                                                                                                                                                                                                                            |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|         | jcoul = 0 ,                                                                                                                                                                                                         | the Coulomb barrier is off.                                                                                                                                                                                                                                                                                                     |
| nexite  | Subtract nuclear recoil energy to get excitation energy. If                                                                                                                                                         | Subtract nuclear recoil energy to get excitation energy. If                                                                                                                                                                                                                                                                     |
|         | nexite = 1 ,                                                                                                                                                                                                        | this feature is on (DEFAULT).                                                                                                                                                                                                                                                                                                   |
|         | nexite = 0 ,                                                                                                                                                                                                        | this feature is off.                                                                                                                                                                                                                                                                                                            |
| npidk   | Controls pion termination treatment. If                                                                                                                                                                             | Controls pion termination treatment. If                                                                                                                                                                                                                                                                                         |
|         | npidk = 0 ,                                                                                                                                                                                                         | force π - to interact by nuclear capture (INC) when cutoff is reached (DEFAULT).                                                                                                                                                                                                                                                |
|         | npidk = 1 ,                                                                                                                                                                                                         | force π - to terminate by decay at the pion cutoff energy ( 4 ).                                                                                                                                                                                                                                                                |
| noact   | Particle transport options. If                                                                                                                                                                                      | Particle transport options. If                                                                                                                                                                                                                                                                                                  |
|         | noact = - 2 ,                                                                                                                                                                                                       | source particles immediately collide; all progeny escape. In other words, all secondary particles produced are transported with no interactions and no decay. Used to compute and tally double-differential cross sections and residual nuclei with an F1 or F8 tally in conjunction with the FT res option ( 5 ).              |
|         | noact = - 1 ,                                                                                                                                                                                                       | nuclear interactions of source particles only; transport and slowing down are off.                                                                                                                                                                                                                                              |
|         | noact = 0 ,                                                                                                                                                                                                         | turn off all non-elastic reactions.                                                                                                                                                                                                                                                                                             |
|         | noact = 1 ,                                                                                                                                                                                                         | perform normal transport (DEFAULT).                                                                                                                                                                                                                                                                                             |
|         | noact = 2 ,                                                                                                                                                                                                         | attenuation mode; transport primary source particles without non-elastic reactions.                                                                                                                                                                                                                                             |
| icem    | Choose alternative physics model. If                                                                                                                                                                                | Choose alternative physics model. If                                                                                                                                                                                                                                                                                            |
|         | icem = 0 ,                                                                                                                                                                                                          | use the Bertini or ISABEL model determined by the iexisa parameter.                                                                                                                                                                                                                                                             |
|         | icem = 1 ,                                                                                                                                                                                                          | use the CEM03.03 model (DEFAULT) ( 6 ).                                                                                                                                                                                                                                                                                         |
|         | icem = 2 ,                                                                                                                                                                                                          | use INCL4 model ( 7 ). Default evaporation model is ABLA; see ievap on LEA card.                                                                                                                                                                                                                                                |
| ilaq    | Choose light ion and nucleon physics modules ( 7 ). If                                                                                                                                                              | Choose light ion and nucleon physics modules ( 7 ). If                                                                                                                                                                                                                                                                          |
|         | ilaq = 0 ,                                                                                                                                                                                                          | use LAQGSM03.03 to handle all heavy-ion interactions as well as all light-ion interactions above 940 MeV/nucleon. ISABEL will handle light-ion interactions below this energy. Use LAQGSM03.03 for proton and neutron interactions above the energy cutoff specified by parameters flenb1 and flenb2 on the LCB card (DEFAULT). |
|         | ilaq = 1 ,                                                                                                                                                                                                          | use LAQGSM03.03 to handle all heavy-ion interactions as well as all light-ion interactions.                                                                                                                                                                                                                                     |
| nevtype | Choose number of evaporation particles modeled by GEM2 (DEFAULT: nevtype = 66 ). If nevtype = N , evaporation modeling is limited to the lightest N particles. nevtype has a minimum value of 6 , which includes n, | Choose number of evaporation particles modeled by GEM2 (DEFAULT: nevtype = 66 ). If nevtype = N , evaporation modeling is limited to the lightest N particles. nevtype has a minimum value of 6 , which includes n,                                                                                                             |

Use: CEM03.03 and LAQGSM03.03 are highly recommended ( LCA 8J 1 1 );
noact is very useful for examining single reactions, i.e., interactions
with nuclei without transport.

## Details:

- 1 CEM03.03 and LAQGSM03.03 use their own pre-equilibrium model [200, 204, 216] all the time. INCL uses no pre-equilibrium model.
- 2 The antinucleons and kaons are unaffected by the choice of physics models. They always choose ISABEL below the flenb5 energy and LAQGSM03.03 above the flenb6 energy (see LCB card). At energies intermediate to these two, a weighted random choice is made between the two models.
- 3 The ISABEL INC model requires a much greater execution time. In addition, incident particle energies must be less than 1 GeV per nucleon for light ions (at higher energies, the LAQGSM03.03 model is automatically invoked).
- 4 The capture probability for any isotope in a material is proportional to the product of the number fraction and the charge of the isotope. However, capture on 1 H leads to decay rather than interaction.
- 5 If noact = -2 on the LCA card, table physics will be used whenever possible to get the differential data actually used in a given problem. To get the differential data with models only, table data can be turned off by setting the cutn parameter on the PHYS : n card and the tabl parameter on the PHYS : h card.
- 6 CEM03.03 allows neutrons, protons, pions, and photons to initiate nuclear reactions. We recommend when possible using CEM03.03 for target-nuclei energies up to about 5 GeV for reactions induced by nucleons and pions on heavy nuclei-targets, up to about 1 . 2 GeV for photonuclear reactions, and up to about 1 GeV for reactions on light nuclei-targets.
- Although results from CEM03.03 are expected to be more reliable in these energy regions, CEM03.03 is expected also to work quite reliably for all target-nuclei at energies up to about 5 GeV. CEM03.03 consists of an IntraNuclear Cascade (INC) model [216, 257, 258], followed by its own pre-equilibrium model [200, 204, 216] and an evaporation model (see details in [216] and references therein).
- Possible fission events are initiated in the equilibrium stage for compound nuclei with a charge number Z &gt; 65 . The evaporation/fission is handled by a modification of the Generalized Evaporation/Fission Model (GEM2) [259], which is an extension to an earlier evaporation model [260] and fission model [261] as described in [262]. Fission fragments undergo an evaporation stage that depends on their excitation energy. When the mass number of excited nuclei produced after INC, as well as after and during the pre-equilibrium and evaporation/fission stages of reactions, A &lt; 13 , CEM03.03 uses the Fermi break-up model to calculate the following de-excitation, instead of using the pre-equilibrium and/or the evaporation/fission models. After the last stage of a reaction calculated by CEM03.03 (usually, the evaporation), a de-excitation of the residual nucleus follows in MCNP6 (but not in CEM03.03 when used as a stand-alone code [216]), generating gammas with the PHT code adopted from LAHET [255].
- 7 By default, light ions (d, t, 3 He, 4 He) are handled by ISABEL below 940 MeV/nucleon and LAQGSM03.03 above 940 MeV/nucleon. Specifying ilaq = 1 will send them to LAQGSM03.03 at all energies. Specifying icem = 2 will instead send them to INCL for all energies.
- 8 By default, GEM2 models the evaporation of 66 types of particles (up to 28 Mg). As heavier nuclei often have negligible fission/evaporation probabilities, specifying nevtype = N , limits evaporation modeling to the lightest N particles. A minimum number of 6 particle types (n, p, d, t, 3 He, and 4 He) is needed, and will default to 6 when nevtype &lt; 6 . It is recommended that users of CEM03.03 and LAQGSM03.01 use a nevtype value of 66 only when evaporation of fragments heavier than 4 He are desired; otherwise the value of 6 is recommended to save computational performance.

## 5.7.8.2.2 LCB

The LCB card controls which physics module is used for particle
interactions depending on the kinetic energy of the particle.

| Data-card Form: LCB flenb1 flenb2 flenb3 flenb4 flenb5 flenb6 ctofe flim0   | Data-card Form: LCB flenb1 flenb2 flenb3 flenb4 flenb5 flenb6 ctofe flim0                                                                                                                                                                                                  | Data-card Form: LCB flenb1 flenb2 flenb3 flenb4 flenb5 flenb6 ctofe flim0                                                                                                                                                                                                                          |
|-----------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| flenb1                                                                      | Kinetic energy (DEFAULT: flenb1 = 3500 MeV). For nucleons, the CEM/Bertini/INCL INC model will be used below this value ( 1 , 2 ). See the LCA icem parameter for choice of INC model.                                                                                     | Kinetic energy (DEFAULT: flenb1 = 3500 MeV). For nucleons, the CEM/Bertini/INCL INC model will be used below this value ( 1 , 2 ). See the LCA icem parameter for choice of INC model.                                                                                                             |
| flenb2                                                                      | Kinetic energy (DEFAULT: flenb2 = 3500 MeV). For nucleons, the LAQGSM03.03 high-energy generator will be used above this value ( 1 , 2 ). See the LCA ilaq parameter for choice of high-energy model.                                                                      | Kinetic energy (DEFAULT: flenb2 = 3500 MeV). For nucleons, the LAQGSM03.03 high-energy generator will be used above this value ( 1 , 2 ). See the LCA ilaq parameter for choice of high-energy model.                                                                                              |
| flenb3                                                                      | Kinetic energy (DEFAULT: flenb3 = 2500 MeV). For pions, the CEM/Bertini/INCL INC model will be used below this value ( 2 , 3 ). See the LCA icem parameter for choice of INC model.                                                                                        | Kinetic energy (DEFAULT: flenb3 = 2500 MeV). For pions, the CEM/Bertini/INCL INC model will be used below this value ( 2 , 3 ). See the LCA icem parameter for choice of INC model.                                                                                                                |
| flenb4                                                                      | Kinetic energy (DEFAULT: flenb4 = 2500 MeV). For pions, the LAQGSM03.03 high-energy generator will be used above this value ( 2 , 3 See the LCA ilaq parameter for choice of high-energy model.                                                                            | Kinetic energy (DEFAULT: flenb4 = 2500 MeV). For pions, the LAQGSM03.03 high-energy generator will be used above this value ( 2 , 3 See the LCA ilaq parameter for choice of high-energy model.                                                                                                    |
| flenb5                                                                      | Kinetic energy (DEFAULT: flenb5 = 800 MeV). The ISABEL INC model will be used below this value ( 2 ).                                                                                                                                                                      | Kinetic energy (DEFAULT: flenb5 = 800 MeV). The ISABEL INC model will be used below this value ( 2 ).                                                                                                                                                                                              |
| flenb6                                                                      | Kinetic energy (DEFAULT: flenb6 = 800 MeV). An appropriate model will be used above this value ( 2 ). For                                                                                                                                                                  | Kinetic energy (DEFAULT: flenb6 = 800 MeV). An appropriate model will be used above this value ( 2 ). For                                                                                                                                                                                          |
|                                                                             | iexisa = 2 ,                                                                                                                                                                                                                                                               | flenb5 and flenb6 apply to all particle types.                                                                                                                                                                                                                                                     |
|                                                                             | iexisa = 1 ,                                                                                                                                                                                                                                                               | flenb5 and flenb6 apply to all particles except nucleons and pions.                                                                                                                                                                                                                                |
|                                                                             | iexisa = 0 ,                                                                                                                                                                                                                                                               | flenb5 and flenb6 are immaterial.                                                                                                                                                                                                                                                                  |
|                                                                             | See §5.7.8.2.2.1 for further explanation.                                                                                                                                                                                                                                  | See §5.7.8.2.2.1 for further explanation.                                                                                                                                                                                                                                                          |
| ctofe                                                                       | The cutoff kinetic energy (MeV) for particle escape during the INC when using the Bertini model. The cutoff energy prevents low-energy nucleons from escaping the nucleus during the INC; for protons, the actual cutoff is the maximum of ctofe and a Coulomb barrier. If | The cutoff kinetic energy (MeV) for particle escape during the INC when using the Bertini model. The cutoff energy prevents low-energy nucleons from escaping the nucleus during the INC; for protons, the actual cutoff is the maximum of ctofe and a Coulomb barrier. If                         |
|                                                                             | ctofe ≥ 0 ,                                                                                                                                                                                                                                                                | ctofe will be used as the cutoff energy.                                                                                                                                                                                                                                                           |
|                                                                             | ctofe < 0 ,                                                                                                                                                                                                                                                                | a random cutoff energy, uniformly distributed from zero to twice the mean binding energy of a nucleon will be sampled for each projectile-target interaction and separately for neutrons and protons. In this case the Coulomb barrier for protons is also randomized (DEFAULT: ctofe = - 1 . 0 ). |
|                                                                             | For the ISABEL INC, the randomized cutoff energy is always used.                                                                                                                                                                                                           | For the ISABEL INC, the randomized cutoff energy is always used.                                                                                                                                                                                                                                   |
| flim0                                                                       | The maximum correction allowed for mass-energy balancing in the cascade stage, used with nobalc = 1 on the LEA card. If                                                                                                                                                    | The maximum correction allowed for mass-energy balancing in the cascade stage, used with nobalc = 1 on the LEA card. If                                                                                                                                                                            |

| flim0 > 0 ,   | kinetic energies of secondary particles will be reduced by no more than a fraction of flim0 in attempting to obtain a non-negative excitation of the residual nucleus and a consistent mass-energy balance. A cascade will be resampled if the correction exceeds flim0 .   |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| flim0 = 0 ,   | no correction will be attempted and a cascade will be resampled if a negative excitation is produced.                                                                                                                                                                       |
| flim0 < 0 ,   | for incident energy, E , the maximum correction is 0 . 02 for E > 250 MeV, 0 . 05 for E < 100 MeV, and is set equal to 5 /E between those limits (DEFAULT: flim0 = - 1 . 0 ).                                                                                               |

## Details:

- 1 For nucleons, the Bertini model switches to a scaling procedure above 3 . 495 GeV, wherein results are scaled from an interaction at 3 . 495 GeV. Although both models will execute to arbitrarily high energies, a plausible upper limit for the Bertini scaling law is 10 GeV.
- 2 The interaction model selected is sampled uniformly, but weighted by proximity to the energy bound, between flenb1 and flenb2 , flenb3 and flenb4 , or flenb5 and flenb6 , as appropriate.
- 3 For pions, the Bertini model switches to the scaling law method above 2 . 495 GeV.

## 5.7.8.2.2.1 Example 1

The configuration shown on the LCB card in Listing 5.28 changes the
default energy-boundary switches and the ranges for stochastic model
selection sampling for all nucleon and pion interactions.

Listing 5.28: example\_mphys\_lcab.mcnp.inp.txt

| lca   | 2j 2 4j -2 0   |
|-------|----------------|
| lcb   | 3000 3000 2000 |

For iexisa = 1 , the default model on the LCA card, nucleons will switch
to the Bertini model from the LAQGSM03.03 model below flenb1 = 3 GeV,
and pions will switch below flenb3 = 2 GeV. Kaons and anti-nucleons will
switch to the ISABEL model from the LAQGSM03.03 model below 1 GeV. Muons
have no nuclear interactions.

For iexisa = 2 , selected by the 3rd entry on the LCA card in Listing
5.28, nucleons and pions will switch to the ISABEL model below flenb5 =
1 GeV. Note that the upper energy threshold in the ISABEL version used
by MCNP6 is 1 GeV/nucleon. No interactions are allowed at energies
greater than this value.

## 5.7.8.2.3 LCC

The LCC card specifies control parameters for the INCL4 model and the
ABLA fission-evaporation model. INCL4 is invoked by setting the 9th LCA
card entry, icem = 2 , and ABLA is invoked by setting the 7th LEA card
entry, ievap = 2 .

| Data-card Form: LCC stincl v0incl xfoisaincl npaulincl nosurfincl J J ecutincl ebankincl ebankabla   | Data-card Form: LCC stincl v0incl xfoisaincl npaulincl nosurfincl J J ecutincl ebankincl ebankabla                                                                                        | Data-card Form: LCC stincl v0incl xfoisaincl npaulincl nosurfincl J J ecutincl ebankincl ebankabla                                                                                        |
|------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| stincl                                                                                               | Rescaling factor of the cascade duration (DEFAULT: stincl = 1 . 0 ).                                                                                                                      | Rescaling factor of the cascade duration (DEFAULT: stincl = 1 . 0 ).                                                                                                                      |
| v0incl                                                                                               | Potential depth (DEFAULT: v0incl = 45 MeV).                                                                                                                                               | Potential depth (DEFAULT: v0incl = 45 MeV).                                                                                                                                               |
| xfoisaincl                                                                                           | Controls the maximum impact parameter for Pauli blocking, rmaxws = r 0 + xfoisaincl × a , where r 0 is the radius of the nucleus and a is the diffuseness (DEFAULT: xfoisaincl = 8 . 0 ). | Controls the maximum impact parameter for Pauli blocking, rmaxws = r 0 + xfoisaincl × a , where r 0 is the radius of the nucleus and a is the diffuseness (DEFAULT: xfoisaincl = 8 . 0 ). |
| npaulincl                                                                                            | Controls the Pauli blocking parameter. If                                                                                                                                                 | Controls the Pauli blocking parameter. If                                                                                                                                                 |
| npaulincl                                                                                            | npaulincl = 1 ,                                                                                                                                                                           | use Pauli strict blocking.                                                                                                                                                                |
| npaulincl                                                                                            | npaulincl = 0 ,                                                                                                                                                                           | use Pauli statistic blocking (DEFAULT).                                                                                                                                                   |
| npaulincl                                                                                            | npaulincl = - 1 ,                                                                                                                                                                         | no Pauli blocking.                                                                                                                                                                        |
| nosurfincl                                                                                           | Controls the diffuse nuclear surface based on Wood-Saxon density. If                                                                                                                      | Controls the diffuse nuclear surface based on Wood-Saxon density. If                                                                                                                      |
| nosurfincl                                                                                           | nosurfincl = - 2 ,                                                                                                                                                                        | use Wood-Saxon density and INCL4 stopping time (DEFAULT).                                                                                                                                 |
| nosurfincl                                                                                           | nosurfincl = - 1 ,                                                                                                                                                                        | use Wood-Saxon density and stopping time with impact dependence.                                                                                                                          |
| nosurfincl                                                                                           | nosurfincl = 0 ,                                                                                                                                                                          | use Wood-Saxon density and stopping time without impact dependence.                                                                                                                       |
| nosurfincl                                                                                           | nosurfincl = 1 ,                                                                                                                                                                          | use sharp surface.                                                                                                                                                                        |
| J                                                                                                    | Unused placeholder. Be sure to put the J in the keyword string.                                                                                                                           | Unused placeholder. Be sure to put the J in the keyword string.                                                                                                                           |
| J                                                                                                    | Unused placeholder. Be sure to put the J in the keyword string.                                                                                                                           | Unused placeholder. Be sure to put the J in the keyword string.                                                                                                                           |
| ecutincl                                                                                             | Use Bertini model below this energy (DEFAULT: ecutincl = 0 ).                                                                                                                             | Use Bertini model below this energy (DEFAULT: ecutincl = 0 ).                                                                                                                             |
| ebankincl                                                                                            | Write no INCL bank particles below this energy (DEFAULT: ebankincl = 0 ).                                                                                                                 | Write no INCL bank particles below this energy (DEFAULT: ebankincl = 0 ).                                                                                                                 |
| ebankabla                                                                                            | Write no ABLA bank particles below this energy (DEFAULT: ebankabla = 0 ).                                                                                                                 | Write no ABLA bank particles below this energy (DEFAULT: ebankabla = 0 ).                                                                                                                 |

## 5.7.8.2.4 LEA

The LEA card controls evaporation, Fermi-breakup, level-density
parameters, and fission models. These are external to the particular
intranuclear cascade/pre-equilibrium model chosen (Bertini, ISABEL, or
INCL), and may be used with any of these choices (except CEM03.03 and
LAQGSM03.03).

| Data-card Form: LEA ipht icc nobalc nobale ifbrk ilvden ievap nofis   | Data-card Form: LEA ipht icc nobalc nobale ifbrk ilvden ievap nofis     |
|-----------------------------------------------------------------------|-------------------------------------------------------------------------|
| ipht                                                                  | Control generation of de-excitation photons. If                         |
|                                                                       | ipht = 0 , generation of de-excitation photons is off.                  |
|                                                                       | ipht = 1 , generation of de-excitation photons is on (DEFAULT).         |
| icc                                                                   | Defines the level of physics to be applied for the LAHET-PHT [255, 263] |

|        | photon physics. If                                                                                                                                                                                                                                                                         |                                                                                                                                                                                                                                                                                            |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|        | icc = 0 ,                                                                                                                                                                                                                                                                                  | use the continuum model.                                                                                                                                                                                                                                                                   |
|        | icc = 1 ,                                                                                                                                                                                                                                                                                  | use the Troubetzkoy (E1) model.                                                                                                                                                                                                                                                            |
|        | icc = 2 ,                                                                                                                                                                                                                                                                                  | use the intermediate model (hybrid between icc = 1 and icc = 2 ).                                                                                                                                                                                                                          |
|        | icc = 3 ,                                                                                                                                                                                                                                                                                  | use the spin-dependent model.                                                                                                                                                                                                                                                              |
|        | icc = 4 ,                                                                                                                                                                                                                                                                                  | use the full model with experimental branching ratios (DEFAULT).                                                                                                                                                                                                                           |
| nobalc | Controls mass-energy balancing in the cascade stage (see [255] for historical information). A forced energy balance may distort the intent of any intranuclear cascade model. Energy balancing for the intranuclear cascade is controlled by the input parameter flim0 on the LCB card. If | Controls mass-energy balancing in the cascade stage (see [255] for historical information). A forced energy balance may distort the intent of any intranuclear cascade model. Energy balancing for the intranuclear cascade is controlled by the input parameter flim0 on the LCB card. If |
|        | nobalc = 0 ,                                                                                                                                                                                                                                                                               | use mass-energy balancing in the cascade phase.                                                                                                                                                                                                                                            |
|        | nobalc = 1 ,                                                                                                                                                                                                                                                                               | turn off mass-energy balancing in the cascade phase (DEFAULT).                                                                                                                                                                                                                             |
| nobale | Controls mass-energy balancing in evaporation stage (see [255] for historical information). If                                                                                                                                                                                             | Controls mass-energy balancing in evaporation stage (see [255] for historical information). If                                                                                                                                                                                             |
|        | nobale = 0 ,                                                                                                                                                                                                                                                                               | use mass-energy balancing in the evaporation stage (DEFAULT).                                                                                                                                                                                                                              |
|        | nobale = 1 ,                                                                                                                                                                                                                                                                               | turn off mass-energy balancing in the evaporation stage.                                                                                                                                                                                                                                   |
| ifbrk  | Controls Fermi-breakup model nuclide range. If                                                                                                                                                                                                                                             | Controls Fermi-breakup model nuclide range. If                                                                                                                                                                                                                                             |
|        | ifbrk = 1 ,                                                                                                                                                                                                                                                                                | use Fermi-breakup model for atomic mass number A ≤ 13 and for 14 ≤ A ≤ 20 with excitation below 44 MeV (DEFAULT).                                                                                                                                                                          |
|        | ifbrk = 0 ,                                                                                                                                                                                                                                                                                | use Fermi-breakup model only for atomic mass number A ≤ 5 .                                                                                                                                                                                                                                |
| ilvden | Controls level-density model. If                                                                                                                                                                                                                                                           | Controls level-density model. If                                                                                                                                                                                                                                                           |
|        | ilvden = - 1 ,                                                                                                                                                                                                                                                                             | use original HETC level-density formulation. See the LEB card for details on parameter inputs.                                                                                                                                                                                             |
|        | ilvden = 0 ,                                                                                                                                                                                                                                                                               | use Gilbert-Cameron-Cook-Ignatyuk level-density model [256] (DEFAULT).                                                                                                                                                                                                                     |
|        | ilvden = 1 ,                                                                                                                                                                                                                                                                               | use the Julich level-density parameterization as a function of mass number [264].                                                                                                                                                                                                          |
| ievap  | Controls evaporation and fission models ( 1 ). If                                                                                                                                                                                                                                          | Controls evaporation and fission models ( 1 ). If                                                                                                                                                                                                                                          |
|        | ievap = 0 ,                                                                                                                                                                                                                                                                                | use the RAL fission model [265].                                                                                                                                                                                                                                                           |
|        | ievap = - 1 ,                                                                                                                                                                                                                                                                              | use the ABLA evaporation model with its built-in fission model when icem = 2 , and use the RAL fission model [265] for all other cases (see icem on the LCA card) (DEFAULT).                                                                                                               |
|        | ievap = 1 ,                                                                                                                                                                                                                                                                                | use the ORNL fission model [266]. The ORNL model allows fission only for isotopes with atomic number Z ≥ 91 .                                                                                                                                                                              |

|       | ievap = 2 ,          | use the ABLA evaporation model with its built-in fission model.   |
|-------|----------------------|-------------------------------------------------------------------|
| nofis | Controls fission. If |                                                                   |
|       | nofis = 1 ,          | allow fission (DEFAULT).                                          |
|       | nofis = 0 ,          | suppress fission.                                                 |

## Details:

- 1 Bertini and ISABEL invoke the Dresner evaporation model with Rutherford Appleton Laboratory (RAL) fission by default. The fission model can be switched to the ORNL model using the ievap option on the LEA card. The evaporation model can be switched from Dresner to ABLA (with its built-in fission model) by setting ievap = 2 .

## 5.7.8.2.5 LEB

The LEB card controls level-density input options for the original HETC
implementation, ilvden = -1 on the LEA card.

|       | Data-card Form: LEB yzere                                                                                                                                                                                                              | Data-card Form: LEB yzere                                                                                                                                                                                                              |
|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|       |                                                                                                                                                                                                                                        | Z ≤ 70 , Z ≥ 71 ,                                                                                                                                                                                                                      |
| bzere | The B 0 parameter level-density formula for atomic number Z ≤ 70 (DEFAULT: bzere = 8 . 0 ). Zero or negative is an error condition; see yzere above.                                                                                   | The B 0 parameter level-density formula for atomic number Z ≤ 70 (DEFAULT: bzere = 8 . 0 ). Zero or negative is an error condition; see yzere above.                                                                                   |
| yzero | The Y 0 parameter in the level-density formula for atomic number Z ≥ 71 and all fission fragments (DEFAULT: yzero = 1 . 5 ). Zero or negative is an error condition; See yzere above.                                                  | The Y 0 parameter in the level-density formula for atomic number Z ≥ 71 and all fission fragments (DEFAULT: yzero = 1 . 5 ). Zero or negative is an error condition; See yzere above.                                                  |
| bzero | The B 0 parameter in the level-density formula for atomic number Z ≥ 71 and all fission fragments (DEFAULT: bzero = 10 . 0 for ievap = 0 and for ievap = 1 on the LEA card). Zero and negative is an error condition; see yzere above. | The B 0 parameter in the level-density formula for atomic number Z ≥ 71 and all fission fragments (DEFAULT: bzero = 10 . 0 for ievap = 0 and for ievap = 1 on the LEA card). Zero and negative is an error condition; see yzere above. |

## 5.7.9 FMULT: Fission Multiplicity Constants and Physics Models

For neutron-induced fission, the average value of neutron multiplicity,
ν , is available in nuclear data libraries and is a function of the
incident neutron energy. Historically, the neutron-induced fission
multiplicity probability distribution, P ( ν ) , is unavailable in
nuclear data libraries. Additionally, the nuclear data libraries that
contain the projectile-target reaction data for neutron-induced fission
reactions do not include spontaneous fission decay data. To simulate the
individual neutron emissions from a spontaneous fission source, the
combination of the par = sf particle type on the SDEF card and the
multiplicity constants and physics model options on the FMULT card are
needed. Additionally, when using the FMULT card, the neutron-induced
fission multiplicity is simulated regardless of whether a spontaneous
fission source is present.

| Data-card Form: FMULT target _ identifier KEYWORD = value(s)   | Data-card Form: FMULT target _ identifier KEYWORD = value(s)                                                                                                                                                                                 | Data-card Form: FMULT target _ identifier KEYWORD = value(s)                                                                                                                                                                                                                                                                       |
|----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| target _ identifier                                            | Target identifier [§1.2.2] ( 1 ). All formats supported. At this time, any values set for non-metastable nuclides also apply to the corresponding metastable nuclide, and a metastable input is converted to a non-metastable input.         | Target identifier [§1.2.2] ( 1 ). All formats supported. At this time, any values set for non-metastable nuclides also apply to the corresponding metastable nuclide, and a metastable input is converted to a non-metastable input.                                                                                               |
| sfnu                                                           | If                                                                                                                                                                                                                                           | If                                                                                                                                                                                                                                                                                                                                 |
|                                                                | sfnu = x ,                                                                                                                                                                                                                                   | where x is a single value, then x is the average neutron multiplicity, ν , used for sampling spontaneous fission multiplicity from a Gaussian distribution with width w ( 2 ).                                                                                                                                                     |
|                                                                | sfnu = x 0 x 1 . . . x N                                                                                                                                                                                                                     | , where multiple values are provided, then the x N values form the ordinates of a discrete cumulative probability distribution of spontaneous fission multiplicity, P ( ν = n ) for n = 0 ...N ( 2 ). A maximum of ten values may be specified, simulating between 0 and 9 neutrons emitted in a single spontaneous fission event. |
| width = w                                                      | Gaussian width full-width at half maximum (FWHM) for sampling P ( ν ) for both spontaneous and neutron-induced fission. This value is ignored for spontaneous fission when sfnu is specified as a cumulative probability distribution ( 2 ). | Gaussian width full-width at half maximum (FWHM) for sampling P ( ν ) for both spontaneous and neutron-induced fission. This value is ignored for spontaneous fission when sfnu is specified as a cumulative probability distribution ( 2 ).                                                                                       |
| sfyield = y                                                    | Spontaneous fission yield (n/s-g). Required for selecting the spontaneously fissioning nuclide when more than one is present in a material ( 2 ).                                                                                            | Spontaneous fission yield (n/s-g). Required for selecting the spontaneously fissioning nuclide when more than one is present in a material ( 2 ).                                                                                                                                                                                  |
| watt = a b                                                     | Watt energy spectrum parameters a and b (see Eq. (5.27)) for spontaneous fission neutron energy sampling ( 2 ).                                                                                                                              | Watt energy spectrum parameters a and b (see Eq. (5.27)) for spontaneous fission neutron energy sampling ( 2 ).                                                                                                                                                                                                                    |
| method = m                                                     | Use to select the Gaussian sampling algorithm method or model physics option ( 3 ). If                                                                                                                                                       | Use to select the Gaussian sampling algorithm method or model physics option ( 3 ). If                                                                                                                                                                                                                                             |
|                                                                | method = 0 ,                                                                                                                                                                                                                                 | use the MCNP5 sine/cosine sampling method (DEFAULT, see Table 5.11).                                                                                                                                                                                                                                                               |
|                                                                | method = 1 ,                                                                                                                                                                                                                                 | use the Lestone moment-fitting method [73]; this is MCNPX polar sampling with 0.5 added to the result.                                                                                                                                                                                                                             |
|                                                                | method = 3 ,                                                                                                                                                                                                                                 | use the Ensslin/Santi/Beddingfield/Mayo method [267, 268]; this is MCNPX polar sampling with a random number between 0 and 1 added to the result.                                                                                                                                                                                  |

glyph[negationslash]

|           | method = 5 ,                                                                               | use the LLNL fission library for neutron-induced, spontaneous, and photonuclear (if ispn = 0 and fism = 1 on the PHYS : p card) fission [237] ( 4 , 5 ). Restriction: method = 5 cannot be used with delayed neutron biasing ( dnbias on ACT card).   |
|-----------|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|           | method = 6 ,                                                                               | use the FREYA fission model for neutron-induced and spontaneous fission [269] ( 4 , 5 , 6 ). Restriction: method = 6 cannot be used with delayed neutron biasing ( dnbias on ACT card).                                                               |
|           | method = 7 ,                                                                               | use the CGMF fission model for neutron-induced and spontaneous fission [270] ( 4 , 5 , 6 ). Restriction: method = 7 cannot be used with delayed neutron biasing ( dnbias on ACT card).                                                                |
|           | Note: All other values for m are unused.                                                   | Note: All other values for m are unused.                                                                                                                                                                                                              |
| data = d  | Use to select data for isotope multiplicities ( 3 ). If                                    | Use to select data for isotope multiplicities ( 3 ). If                                                                                                                                                                                               |
|           | data = 0 ,                                                                                 | use bounded integer fission sampling (DEFAULT).                                                                                                                                                                                                       |
|           | data = 1 ,                                                                                 | use Lestone re-evaluated Gaussian width by isotope for multiplicities.                                                                                                                                                                                |
|           | data = 2 ,                                                                                 | use original Terrell Gaussian widths by isotope for multiplicities [72].                                                                                                                                                                              |
|           | data = 3 ,                                                                                 | use Ensslin/Santi/Beddingfield/Mayo.                                                                                                                                                                                                                  |
| shift = s | Designate method to modify the sampled ν to preserve the average multiplicity, ν ( 3 ). If | Designate method to modify the sampled ν to preserve the average multiplicity, ν ( 3 ). If                                                                                                                                                            |
|           | shift = 0 ,                                                                                | use the MCNP5 treatment, which assumes an integer number of neutrons per fission. For example, if ν = 2 . 7 , then the number of neutrons will be two 30% of the time and three 70% of the time (DEFAULT).                                            |
|           | shift = 1 ,                                                                                | use the MCNPX-style adjustment method that uses a re-evaluated Gaussian width to sample fission neutron multiplicities for all fissionable isotopes.                                                                                                  |
|           | shift = 2 ,                                                                                | sample the Gaussian distribution and preserve the average multiplicity by increasing the ν threshold.                                                                                                                                                 |
|           | shift = 3 ,                                                                                | sample the Gaussian distribution without correction. This will overpredict ν .                                                                                                                                                                        |
|           | shift = 4 ,                                                                                | use the MCNP4C integer sampling method in the presence of spontaneous fission.                                                                                                                                                                        |

Defaults shown correspond to the condition that no method , data , or
shift keywords are specified. If any of these keywords appear, the code
will automatically assign values for the unspecified keywords. The
default assignments otherwise are method = 3 , data = 3 , and shift = 1
.

Use: Optional. Enables users to override or add additional fission
multiplicity data.

Table 5.11: Mapping from MCNP5 and MCNPX PHYS : n Options to MCNP6 FMULT Options ( 3 )

| MCNPX PHYS : n    | MCNP6   | MCNP6   | FMULT   |
|-------------------|---------|---------|---------|
| fism (6th entry)  | method  | data    | shift   |
| 0                 | 0       | 0       | 0       |
| -1, 1             | 3       | 3       | 1       |
| 2                 | 3       | 3       | 2       |
| 3                 | 3       | 3       | 3       |
| 4                 | 3       | 3       | 4       |
| 5                 | 5       | N/A     | N/A     |
| MCNP5 PHYS : n    | MCNP6   | MCNP6   | FMULT   |
| fisnu (5th entry) | method  | data    | shift   |
| 0                 | 0       | 0       | 0       |
| 1                 | 0       | 1       | 0       |
| 2                 | 0       | 2       | 0       |

## Details:

- 1 When overriding the default values for the sfnu , width , sfyield or watt keywords, the target \_ identifier option must be specified. Defaults exist for the most common fissioning nuclei; these defaults are provided in PRINT Table 38 of the MCNP output [267, 271-279]. To have a spontaneous fission source for nuclides without default values (zero values in PRINT Table 38), a FMULT data card is required. Without a target \_ identifier option specified, only the fissioning nuclei that are missing default values will inherit the specified keyword values. method , shift , and data keywords are not isotope specific while the rest of the FMULT keywords are isotope specific; therefore, target \_ identifier is optional.
- 2 The sfnu , sfyield , and watt keywords are only applicable to spontaneous fission isotopes. For neutroninduced fission, the average fission neutron multiplicity, ν , and the fission spectrum, χ , come from the nuclear data libraries at the energy of the incident neutron causing fission. The width keyword value is required for the neutron-induced fission isotope even if a cumulative distribution on the sfnu keyword is specified for spontaneous fission. The spontaneous fission yield ( sfyield ) must be specified if more than one spontaneous fission source nuclide occurs.
- 3 The specific method , shift , and data parameter combinations listed in Table 5.11 are the only ones assured to work correctly. Other combinations are possible but have not been tested. While the method , shift , and data keywords may be specified on multiple FMULT cards in the input deck, only the last instance of each keyword determines the algorithms and data used for multiplicity sampling. When specifying method = 5 , 6 , or 7 , both shift and data keywords are not applicable and should not be used.
- 4 The LLNL fission library, the FREYA fission model, and the CGMF fission model are the only ways in MCNP6 to produce correlated prompt fission photons with multiplicities for spontaneous fission and low-energy neutron-induced fission events. For all other method values, no spontaneous fission photons are produced, and the neutron-induced photon production comes from the nuclear data libraries where fission and non-fission photons produced at a collision may not be distinguishable depending on the incident energy of the neutron and the library in use. Delayed fission photons are independent of the selected method and are controlled by the ACT card.
- 5 If the LLNL fission library, the FREYA fission model, or the CGMF fission model is used, then only the spontaneous fission yield ( sfyield ) is used for nuclides in the respective model. For fissioning nuclides not in the LLNL fission library, the FMULT parameters are used.
- 6 If either the FREYA or CGMF fission model is used, and the fission nuclide is unavailable, the LLNL fission library is used to emit correlated neutrons and photons.

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

1

## 5.7.9.1 Multiplicity Parameters Default Values

The spontaneous fission multiplicity constants in PRINT Table 38, shown
in Listing 5.29, are the default values [272] of the multiplicity
parameters in MCNP6. These constants are printed with three digits of
precision, but they are represented in the MCNP source code with seven
digits of precision.

Data actually used within the simulation are denoted by an * , shown in
Listing 5.29. If any data are overridden by FMULT user input, the user
data replaces the default data shown in PRINT Table 38. If the LLNL
fission library, FREYA, or CGMF methods are selected, additional
informational messages can be seen in the output file below PRINT Table
38.

Fission Watt spectra parameters and fission yields are not available for
the following nuclides: 246 Pu, 246 Cm, 248 Cm, 246 Cf, 250 Cf, 254 Cf,
257 Fm, and 252 No.

Listing 5.29: Default Fission Multiplicity Constants in Print Table 38

<!-- image -->

## 5.7.9.2 Example 1

fmult method=0 data=1 shift=0

This input card only specifies the method , data , and shift keywords,
relying on the default values for the fission multiplicity and spectrum
constants given in PRINT Table 38 in Listing 5.29.

## 5.7.9.3 Example 2

Listing 5.30: example\_fmult\_1.mcnp.inp.txt

1

2

3

4

```
sdef par=sf fmult Pu-239 width=1.16 watt=0.885247 3.8026 sfyield=0.0218 sfnu=2.1 fmult Cf-252 width=1.207 watt=1.18 1.03419 sfyield=2.34e12 sfnu=0.002 0.028 0.155 0.428 0.732 0.917 0.983 0.998 1.0
```

Listing 5.31: example\_fmult\_2.mcnp.inp.txt

These input cards specify a spontaneous fission source on the SDEF card
and user-specified values for the width , watt , sfnu , and sfyield
keywords. PRINT Table 38 includes all of the user-specified constants
given on the FMULT cards and the remaining default values not overridden
by the user input. PRINT Tables 117 and 115 in the output file include
information about the spontaneous and/or induced fission multiplicity
sampling that occurred in the simulation, including the moments of the
sampled ν values, and a summary of all fission neutron multiplicity,
respectively.

## 5.7.9.4 Example 3

```
1 m123 Fm-257 1 2 awtab Fm-257 254.88653438 3 mx123:n Cf-252 4 c 5 sdef par=sf 6 fmult Fm-257 watt=1.4 2.0 sfyield=5E11
```

Listing 5.32: example\_fmult\_3.mcnp.inp.txt

Nuclear cross-section tables for transporting 246 Cf, 254 Cf, 257 Fm,
and 252 No are not generally available. To model spontaneous fission
from these nuclides, it is necessary to do the transport either with
model physics or by substituting cross sections. Physics models are not
recommended at low energies. To make a nuclide substitution, the AWTAB
and MX cards must be used. The AWTAB card provides the atomic weight
ratio for 257 Fm, which may not be available depending on the available
data libraries installed. The MX123 : n card in this example substitutes
252 Cf, for which there are neutron cross-section data, for the
corresponding nuclide 257 Fm on the M123 material card.

## 5.7.10 TROPT: Transport Options

The TROPT card allows the user to modify the default options for
modeling how particle interactions occur. Typically these options are
useful for diagnosing the importance of certain physical processes, and
for generating tabulated double-differential cross sections when using
physics models. The PHYS card parameters for electrons and positrons are
not set or modified by the TROPT card entries.

| Data-card Form:   | TROPT KEYWORD = value(s)                                                                                                                                                                               | TROPT KEYWORD = value(s)                                                                                                                                                                               |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| mcscat            | Controls multiple Coulomb scattering. If                                                                                                                                                               | Controls multiple Coulomb scattering. If                                                                                                                                                               |
| mcscat            | mcscat = off ,                                                                                                                                                                                         | multiple coulomb scattering is disabled; no angular deflection occurs.                                                                                                                                 |
| mcscat            | mcscat = fnal1 ,                                                                                                                                                                                       | (DEFAULT).                                                                                                                                                                                             |
| mcscat            | mcscat = gaussian                                                                                                                                                                                      | mcscat = gaussian                                                                                                                                                                                      |
| mcscat            | mcscat = fnal2 ,                                                                                                                                                                                       | then treats eloss = strag1 as eloss = csda (recommended).                                                                                                                                              |
| eloss             | Controls slowing down energy losses. If                                                                                                                                                                | Controls slowing down energy losses. If                                                                                                                                                                |
| eloss             | eloss = off ,                                                                                                                                                                                          | no energy loss occurs during slowing down.                                                                                                                                                             |
| eloss             | eloss = strag1 ,                                                                                                                                                                                       | CSDA is used with straggling (DEFAULT).                                                                                                                                                                |
| eloss             | eloss = csda ,                                                                                                                                                                                         | Energy loss modeled using only CSDA.                                                                                                                                                                   |
| nreact            | Controls nuclear reactions. If                                                                                                                                                                         | Controls nuclear reactions. If                                                                                                                                                                         |
| nreact            | nreact = off ,                                                                                                                                                                                         | no nuclear reactions occur.                                                                                                                                                                            |
| nreact            | nreact = on ,                                                                                                                                                                                          | nuclear reactions allowed (DEFAULT).                                                                                                                                                                   |
| nreact            | nreact = atten ,                                                                                                                                                                                       | attenuation is turned on and absorption weighting occurs at collision.                                                                                                                                 |
| nreact            | nreact = remove ,                                                                                                                                                                                      | the incident particle is killed.                                                                                                                                                                       |
| nescat            | Controls nuclear elastic scattering. This keyword has no effect if nreact = off . If                                                                                                                   | Controls nuclear elastic scattering. This keyword has no effect if nreact = off . If                                                                                                                   |
| nescat            | nescat = off ,                                                                                                                                                                                         | acts as a delta-scatter for the elastic process in a transport calculation. For a genxs calculation, sets the elastic scattering cross section to zero.                                                |
| nescat            | nescat = on ,                                                                                                                                                                                          | (DEFAULT).                                                                                                                                                                                             |
| genxs             | Enables the generation of double-differential particle production cross sections and residual nucleus production cross sections from the high-energy nuclear interaction models. See §5.7.10.1. If the | Enables the generation of double-differential particle production cross sections and residual nucleus production cross sections from the high-energy nuclear interaction models. See §5.7.10.1. If the |
| genxs             | genxs                                                                                                                                                                                                  | keyword is absent, standard transport occurs.                                                                                                                                                          |
| genxs             | genxs = filename                                                                                                                                                                                       | is present, but no filename is specified, read the edit input from a file named inxc . If filename is specified, read the edit input from a file named filename .                                      |

## 5.7.10.1 Application of the genxs Option

The genxs option allows the application of high-energy nuclear
interaction models in a cross-section generation mode without particle
transport. A source may be specified inside a medium; each history will
consist only of the interaction of the source particle at the source
energy with the components of the medium. The tallied outcome from the
event consists of the energies and direction cosines of the secondary
particles and the recoil nuclei. In typical applications, the material
composition will be a single isotope; however, averaged results may be
obtained for a natural multi-isotopic element or a complex composition.
A genxs calculation is independent of the material density
specification.

The genxs option requires two input files: the standard MCNP6 input file
and an accompanying auxiliary inxc file. To invoke the genxs cross-
section-generating option, specify genxs or genxs = filename on the
TROPT card. The content and format of the edited output are determined
by the content of the auxiliary input file associated with the genxs
option. If genxs is specified on the TROPT card without a user-provided
file name, by default the output tally edit information will be read
from a file named inxc . If a file name is provided with the genxs
keyword, the output tally edit information will be read from the user-
specified filename. In either case, the absence of the required file
will produce a fatal error. A description of the inxc file structure can
be found in §D.9 with examples in §5.7.10.1.1 and §5.7.10.1.2.

To calculate inelastic secondary particle production only, turn off the
elastic scattering by setting nescat = off on the TROPT card. Isotopic
elastic scattering cross sections will be set to zero and the total
cross section will equal the nonelastic cross section. All histories
will sample the nonelastic interaction model. Note that this applies
only to the genxs option; in a transport calculation, nescat = off
implies a delta-scatter for the elastic process.

To examine only elastic scattering, use nreact = atten on the TROPT
card. All histories will sample the elastic scattering model and produce
results for the scattered projectile and the recoil nucleus.

In the output data for a multi-isotopic composition, quoted cross
sections are a weighted average of the isotopic cross sections, weighted
by the input atom fractions. Thus, the cross-section output represents
average cross sections per atom in the composition. Results will reflect
the variance introduced by sampling for the target isotope.

Energy- and angle-integrated results are provided as yield as well as
cross section. The term 'yield' might be better defined as
'multiplicity'. The nonelastic yield for a given particle type is the
number of secondary particles of that type produced per nonelastic
event. The elastic yield is per elastic event and is always unity. The
iyield input option in the inxc file (see §D.9) allows single- and
double-differential results to be provided as yield rather than cross
section, with the above normalization.

## 5.7.10.1.1 Example 1

In the cross-section generation ( genxs ) calculation shown in Listing
5.33, 23.08-GeV protons impinge upon natural tungsten.

```
1 Test problem: RECOIL2 2 1 1 -16.654 -1 2 -3 3 2 0 -4 (1:-2:3) 4 3 0 4 5 6 1 cz 4.0 7 2 pz -1.0
```

Listing 5.33: example\_genxs\_1.mcnp.inp.txt

```
8 3 pz 1.0 9 4 so 50.0 10 11 m1 74180 0.001300 74182 0.263000 74183 0.143000 12 74184 0.306700 74186 0.286000 13 sdef erg = 23080 par = h dir = 1 pos = 0 0 0 vec 0 0 1 14 imp:h 1 1 0 15 phys:h 23080 16 mode h 17 print 40 110 95 18 nps 10000000 19 prdmp 2j -1 20 tropt genxs nreact atten
```

Note that the genxs keyword of the TROPT card of the MCNP6 input file
does not specify a user-supplied file name; therefore, MCNP6 expects an
auxiliary input file named inxc (Listing 5.34) to be available.

```
1 Test problem: RECOIL2 2 5,1,1/ 3 Elastic scattering edit 4 0,-200,1/ 5 2.0/ ! 200 bin boundaries, 2 deg to 0 deg 6 -1/ ! elastic scattered projectile 7 Elastic scattering energy edit 8 125,0,1/ 9 23079,23079.01/ ! 125 10-keV bins above 23.079 GeV 10 -1/ ! elastic scattered projectile 11 Elastic recoil angle edit 12 0,102,1/ 13 0.0,0.02/ ! 101 boundaries mu=0 to 0.02&1.0 14 -2/ ! elastic recoil nucleus 15 Elastic recoil energy edit 16 125,0,1/ 17 0.01/ ! 125 10-keV bins below 1.25 MeV 18 -2/ ! elastic recoil nucleus 19 Elastic recoil momentum edit 20 150,0,1,,1/ 21 5/ ! 150 5-MeV/c bins below 750 MeV/c 22 -2/ ! elastic recoil nucleus
```

Listing 5.34: example\_genxs\_1.inxc.inp.txt

Five cross-section edit cases plus the residual nucleus edit are
specified. A mctal file is written for plotting. Because only elastic
scattering occurs, all the cases are chosen to be single-differential
cross sections only (i.e., nerg = 0 or nang = 0 in the incx input file):

1. d σ/ dΩ for the projectile, binned by degrees;
2. d σ/ d E for the projectile, binned by energy;
3. d σ/ dΩ for the recoil nuclei, binned by cosine;
4. d σ/ d E for the recoil nuclei, binned by energy; and
5. d σ/ d p for the recoil nucleus, binned by momentum.

Listing 5.35: Resultant MCNP6 Output File Excerpt

<!-- image -->

Because the computation is for only elastic scattering from a
composition (natural element), the cross section shown for production of
a particular residual nucleus is just f i σ e i per atom in the element
and the cross section for any residual with charge number Z = 74 is

<!-- formula-not-decoded -->

i.e., the average elastic cross section per atom in the composition.
Because the attenuation weighting option ( nreact = atten ) was used and
every event is an elastic event, the quantity 'mean weight of residual
nuclei per event' equals the ratio of the mean elastic cross section to
the mean total cross section for the element.

## 5.7.10.1.2 Example 2

In this example, the yields (i.e., production cross sections) of
products from a thin 238 U target bombarded by 1 -GeV protons are
calculated. The SDEF card of the MCNP input file (Listing 5.36) defines
a 1000 -MeV proton beam source pointed in the direction of the z axis.

Listing 5.36: example\_genxs\_2.mcnp.inp.txt

<!-- image -->

| MCNP6 test: p + U238 by   |    | CEM03.03   |
|---------------------------|----|------------|
| 1 1 1.0                   | -1 | 2 -3       |
| 2 0                       | -4 | (1:-2:3)   |
| 3 0                       | 4  |            |
| 1                         | cz | 4.0        |
| 2                         | pz | -1.0       |
| 3                         | pz | 1.0        |
| 4                         | so | 50.0       |

1

2

3

4

5

6

7

8

9

```
10 11 sdef erg=1000 par=H dir=1 pos=0 0 0 vec 0 0 1 12 imp:h 1 1 0 13 phys:h 1000 14 m1 92238 1.0 15 mode h 16 LCA 8j 1 $ use CEM03.03 17 tropt genxs inxc01 nreact on nescat off 18 print 40 110 95 19 nps 1000000 20 prdmp 2j -1
```

This beam bombards 238 U, which fills a cylinder with a 4 -cm radius
oriented on the z axis from z = -1 to z = 1 cm. The provided LCA card
parameters select the CEM03.03 event generator for this calculation. The
card indicates a genxs problem with an auxiliary input file named inxc01
(Listing 5.37).

```
1 MCNP6 test: p + U238 at 1 GeV for TR applications 2 1 1 1 / 3 Cross Section Edit 4 56 0 9 / 5 5. 10. 15. 20. 25. 30. 35. 40. 45. 50. 55. 60. 65. 70. 75. 80. 6 85. 90. 95. 100. 120. / 7 1 5 6 7 8 21 22 23 24 /
```

Listing 5.37: example\_genxs\_2.inxc.inp.txt

We will calculate only inelastic secondary particle production ( nreact
= on ) and we turn off the elastic scattering ( nescat = off ).

The input parameters of the inxc file indicate that one double-
differential cross-section edit is requested, the results are to be
written to the mctal file, and a residual nuclei edit is desired. The
fourth card of the input file specifies angle-integrated energy spectra
with 56 energy bin boundaries for nine particle types. The 56 energy bin
boundaries are defined on the 5th card (on multiple lines) using a
combination of user-provided values (the first 21 values) and code-
generated values (the final 25 values). The nine particle types to tally
are defined on the final card of the incx input file using flag values
to specify neutron, proton, π + , π -, π 0 , deuteron, triton, 3 He, and
4 He.

Listing 5.38: Resulting MCNP6 Output File Excerpt

<!-- image -->

10

11

12

13

14

15

16

17

18

19

<!-- image -->

Of particular interest is the production of 87 Br and 88 Br, primary
delayed neutron emitters with relatively long half-lives of 55 . 60 and
16 . 29 s, respectively. From this portion of the output, we see that
the cross section for the production of 87 Br is equal to 2 . 05096 × 10
-03 b ( ± 3.16%) and that of 88 Br is 1 . 10421 × 10 -03 b ( ± 4.30%).
We also see in the output file four isotopes of lithium, including 9 Li,
and cross sections for the production of 17 N and 16 C. These three
isotopes are also important delayed neutron emitters, although their
half-lives are only 0 . 178 , 4 . 173 , and 0 . 747 s, respectively.

## 5.7.11 UNC: Uncollided Secondaries

The historical definition of an uncollided particle in MCNP6 is any
particle that has not undergone a collision since its creation, whether
as a source particle or as a secondary particle. This definition, in
which secondary particles are created as uncollided particles, makes
separation of the contribution to a tally from the direct source and
contribution from secondary particles difficult. Identification of the
uncollided components is particularly useful for users who employ track-
length tallies in radiography applications instead of next-event
estimators.

The UNC card allows the user to control if secondaries are born as
uncollided or collided particles. When created as collided particles,
secondaries inherit the number of collisions of their parent particle.
If a particle inherits the number of collisions of the parent, then the
number of collisions is always greater than or equal to one.

<!-- image -->

| Cell-card Form: UNC : P u or Data-card Form: UNC : P u1 u2 . . . uJ   | Cell-card Form: UNC : P u or Data-card Form: UNC : P u1 u2 . . . uJ   | Cell-card Form: UNC : P u or Data-card Form: UNC : P u1 u2 . . . uJ   |
|-----------------------------------------------------------------------|-----------------------------------------------------------------------|-----------------------------------------------------------------------|
| P                                                                     | Particle designator.                                                  | Particle designator.                                                  |
| u                                                                     | If                                                                    | If                                                                    |
|                                                                       | u = 0 ,                                                               | then secondaries are considered to be collided for the cell.          |
|                                                                       | u = 1 ,                                                               | then secondaries are considered uncollided for the cell (DEFAULT).    |
| uj                                                                    | Number of entries equals number of cells in the problem, J . If       | Number of entries equals number of cells in the problem, J . If       |
|                                                                       | uj = 0 ,                                                              | then secondaries are considered to be collided for the cell.          |
|                                                                       | uj = 1 ,                                                              | then secondaries are considered uncollided for the cell (DEFAULT).    |

Default: uj = 1 , secondaries are considered uncollided for cell j .

Use: Optional. Useful for separating the contribution resulting from
uncollided source particles from that of secondaries that do not collide
after their creation.

## 5.7.12 Magnetic Field Tracking

MCNP6 provides two methods to simulate magnetic field effects on charged
particles [280, 281]. The first method utilizes transfer maps produced
by the beam dynamics simulation and analysis code COSY INFINITY [282].
This method is fast and accurate; however, its use is limited to void
cells only (i.e., in a vacuum) and to ensembles of particles with a
fairly small energy spread. The second method, magnetic field particle
ray tracing, is based on an algorithm adopted from the MARS [283-285]
transport code. This method can be applied to both void and material
cells and is valid over a very large range of particle energies. In
addition, for the magnetic field ray tracing method, MCNP6 includes an
option that simulates third-order aberrations for quadrupole magnets
caused by fringe-field effects by providing edge kicks for particles
entering and exiting the magnet faces. This latter feature is especially
important for proper particle transport through proton radiography beam
lines and magnetic lenses.

## 5.7.12.1 Magnetic Field Transfer Map

COSY INFINITY is a beam optics code that utilizes numerical integration
and differential algebraic techniques to generate transfer maps based on
a Taylor series expansion of a particle's canonical variables [286].
These transfer maps represent the functional relation between the phase-
space coordinates of a particle that has passed through a region with a
magnetic field and its phase-space coordinates before entering the field
region. In the transfer map approach to particle transport, the actual
trajectories that the particles follow through the field region do not
appear explicitly; in applying precomputed maps, charged particles are
transported from an initial location to a final location in one step by
applying the transfer maps to the initial phase space coordinates.

Although the COSY map method provides a fast and accurate method for
transporting charged particles in magnetic fields, the transfer map
method has several limitations:

1. Map methods can only be used in void regions.
2. The COSY maps are limited to only one particle type.
3. The Taylor expansions used in applying the maps have a finite volume of convergence in phase space. The convergence volume has a very complicated shape in five dimensions ( x, y, d x, d y, p ) , requiring that the shape of the phase-space volume and the order of the Taylor series needed in order to get a given accuracy in final particle position is not easily predicted in practice and can be checked only by particle tracking.

For example, a map to fifth order in energy deviation might be applied
with good accuracy to particles with energies within 10% of the
reference energy, but not to those with a 50% deviation. In other words,
COSY maps are specific to particle momentum; therefore, a particle with
significantly different energy or mass than what was used to create the
map will not be transported correctly.

## 5.7.12.1.1 COSYP: Magnetic Field Transfer Map Parameters

The COSYP card is used to define the parameters associated with external
COSY map files and how they may be generally applied within a problem.
No information about the magnetic fields is written to the output file.

| prefix   | The COSY map file prefix number is required. The map files must reside in the current working directory.                        | The COSY map file prefix number is required. The map files must reside in the current working directory.                        |
|----------|---------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| axsh     | Horizontal axis orientation. If                                                                                                 | Horizontal axis orientation. If                                                                                                 |
| axsh     | axsh = 1 ,                                                                                                                      | the x axis is the horizontal axis (DEFAULT).                                                                                    |
| axsh     | axsh = 2 ,                                                                                                                      | the y axis is the horizontal axis.                                                                                              |
| axsh     | axsh = 3 ,                                                                                                                      | the z axis is the horizontal axis.                                                                                              |
| axsv     | Vertical axis orientation. If                                                                                                   | Vertical axis orientation. If                                                                                                   |
| axsv     | axsv = 1 ,                                                                                                                      | the x axis is the vertical axis.                                                                                                |
| axsv     | axsv = 2 ,                                                                                                                      | the y axis is the vertical axis (DEFAULT).                                                                                      |
| axsv     | axsv = 3 ,                                                                                                                      | the z axis is the vertical axis.                                                                                                |
| emapk    | Set emapk = e k , where e k is the operating beam energy of the k th map assigned (DEFAULT is the energy of the k th COSY map). | Set emapk = e k , where e k is the operating beam energy of the k th map assigned (DEFAULT is the energy of the k th COSY map). |

Use: Optional. Use with COSY maps.

## 5.7.12.1.2 COSY: Magnetic Field Assignments

The COSY card is used with the COSYP card to assign the COSY maps to
specific cells in the problem geometry.

```
Cell-card Form: COSY = m or Data-card Form: COSY m1 m2 . . . mJ m Assign COSY map m to the current cell. mj Set cell j to COSY map mj .
```

Use: Use with COSY maps.

Default:

No map is assigned to the cell.

## 5.7.12.1.3 COSYP and COSY Example 1

```
1 cosyp 57 2 1 23070 11r 2 cosy 3j 1 j 2 j 3 j 4 10j 5 j 5 j 6 j 6
```

In this example, the COSYP card defines the COSY map file parameters.
Each COSY map file name is prefixed with 57 . The horizontal axis is the
y axis, and the vertical axis is the x axis. The operating energy for
all twelve maps assigned is 23 , 070 MeV. Field maps are assigned to
twelve cells specified on the COSY card. Table 5.12 lists the map
assignments. The COSY map files 571 , 572 , 573 , 574 , 575 , and 576
must be in the working directory.

## 5.7.12.2 Magnetic Field Particle Ray Tracing

To overcome the limitations of transfer maps, MCNP6 has implemented
direct magnetic field tracking utilizing numerical integration methods.
These routines were adopted from the MARS high-energy particle transport
code. Tracking in a void and material is performed by a higher-order
numerical integration algorithm, with a maximum step size controlled by
the user. Within a step, the trajectory is approximated by a segment of
the helical trajectory corresponding to a constant field equal to the
field at the midpoint of the step, i.e., the field variation within the
step is neglected. A solution of a 3-D equation of trajectory in such a
field provides the new direction cosines and new particle coordinates at
the end of the step. With appropriate parameters, this algorithm
provides extremely high accuracy of tracking.

Table 5.12: Example COSY Map Assignment

|   Map Number |   COSY Map File Name | Cell Numbers   |
|--------------|----------------------|----------------|
|            1 |                  571 | 4              |
|            2 |                  572 | 6              |
|            3 |                  573 | 8              |
|            4 |                  574 | 10             |
|            5 |                  575 | 21 and 23      |
|            6 |                  576 | 25 and 27      |

For quadrupole fields, MCNP6 includes a model to include the effect of
the magnet fringe fields. This can be approximated by applying hard-edge
kicks to the particle as it enters and leaves the magnetic field cell.
An option for edge kicks has been implemented for the quadrupole
magnetic field model. For a particle traveling along the z axis, the
following equations describe the position and momentum jumps applied to
a particle as it enters the upstream fringe field of a quadrupole [287]:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

In these equations, t x and t y are the direction cosines of the
momentum vector. The quantity G is the quadrupole gradient (in T/m) and
p/q is the particle rigidity (in T-m). In order to conserve energy, t z
is also recalculated using the formula

For particles passing through the downstream fringe field of a
quadrupole, the equations are the same, except that Gp/q is replaced
everywhere by -Gp/q .

<!-- formula-not-decoded -->

Summary of known limitations of the magnetic field particle ray tracing
method:

1. A particle can get lost, especially for complicated geometries and lattice cells.
2. In rare cases, MCNP6 could hang in an infinite loop.

## 5.7.12.2.1 BFLD: Magnetic Field Definition

The magnetic field tracking option is accessed by use of the magnetic
field definition card, BFLD . The MCNP code can model dipole and
quadrupole fields such as those shown in Fig. 5.6, where the quadrupole
fields can also include fringe-field edge kicks.

## Data-card Form: BFLDn type KEYWORD = value(s)

n

type field

The magnetic field identification number.

The magnetic field polarity is required. If type = const , magnetic
field is a dipole field.

type = quad , magnetic field is a quadrupole field.

type quadff

= , magnetic field is a quadrupole field with fringe-field edge kicks.

= f Required for each of the type s. If type = const , f = B , the
magnetic field strength (Tesla). type = quad or type = quadff , f = B/l
, the magnetic field gradient (Tesla/cm).

<!-- image -->

Figure 5.6: Supported magnetic field types with the associated vec and
axs vectors necessary to represent the field shown. The symbol ⊗
represents a vector (i.e., a particle) traveling into the page, B the
magnetic field, and F the force on the particle.

```
vec = ( u f , v f , w f ) Optional for each of the type s (DEFAULT: vec = 1 , 0 , 0 ). If type = const , ( u f , v f , w f ) is the direction of the magnetic field. type = quad or type = quadff , ( u f , v f , w f ) is the direction of a focusing quadrupole. axs = ( u q , v q , w q ) , The direction cosines of the quadrupole beam axis, which do not need to be normalized. Only applies to quadrupole fields (DEFAULT: axs = 0 , 0 , 1 ). refpnt = ( x, y, z ) , A point anywhere on the quadrupole beam axis. Only applies to quadrupole fields (DEFAULT: refpnt = 0 , 0 , 0 ). mxdeflc = a , Maximum deflection angle per step size (mrad) (DEFAULT: mxdeflc = 10 ). maxstep = ss , Maximum step size (cm) (DEFAULT: maxstep = 100 ). ffedges = s 1 s 2 . . . s J , List of surface numbers that fringe-field edge kicks are to be applied. Only applies to quadrupole fields with fringe-field kicks ( type = quadff ).
```

Use: Optional. If the type parameter of the BFLD card is not provided, a
fatal error occurs.

## 5.7.12.2.2 BFLCL: Magnetic Field Cell Assignment

The BFLCL card is used with the BFLD card(s) to assign the magnetic
fields to specific cells in the problem geometry.

1

2

1

2

3

4

5

6

```
Cell-card Form: BFLCL = m or Data-card Form: BFLCL m1 m2 . . . mJ m Assign magnetic field m to the current cell. mj Set cell j to magnetic field mj .
```

Default:

No magnetic field is assigned to the cell.

## 5.7.12.2.3 BFLD and BFLCL Example 1

```
bfld1 CONST FIELD .03 VEC 0 1 0 bflcl 2j 1
```

A constant magnetic field of strength 0.03 Tesla is applied to cell 3.
The field is in the + y direction.

## 5.7.12.2.4 BFLD and BFLCL Example 2

```
1 bfld2 QUADFF FIELD 0.195 FFEDGES = 31 2i 34 2 bflcl 31j 2 0 2
```

A quadruple magnet field of gradient 0.195 T/cm is assigned to cells 32
and 34. Fringe-field edge kicks are applied to surfaces 31, 32, 33, and
34.

## 5.7.12.2.5 BFLD and BFLCL Example 3

| bfld3   | QUAD FIELD 0.116     |
|---------|----------------------|
|         | VEC 0.5 0.5 0.707    |
|         | AXS 0.85 -0.14 -0.5  |
|         | REFPNT 40 30 100     |
|         | MXDEFLC 10 MAXSTEP=1 |
| bflcl   | 101j 3 0 3 7j 3 0 3  |

A quadrupole magnetic field of gradient 0.116 T/cm is assigned to cells
102, 104, 112, and 114. The axis of the quadrupole is along the vector
(0 . 85 , -0 . 14 , -0 . 5) , and the focusing direction is along the
vector (0 . 5 , 0 . 5 , 0 . 707) . The maximum step size is 1 cm, and
the maximum angular deflection is 10 mrads.
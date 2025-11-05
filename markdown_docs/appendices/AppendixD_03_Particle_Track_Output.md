---
title: "Appendix D.3 - Particle Track Output File Format"
chapter: "D.3"
source_pdf: "mcnp631_theory_user-manual/appendecies/D.3_Particle_Track_Output_File_Format.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## D.3 Particle Track Output File Format

This section details the current layout of the HDF5-formatted particle
track output file. Examples of how to process and interpret the data in
the particle track file using the Python programming language and
MCNPTools can be found in [346].

Note that the deprecated ASCII and unformatted binary particle track
output file formats [DEP-53382] are unchanged from the description of
them given in [2, Appendix D], which is what should be used as the
format reference for these output files.

All datasets in the HDF5-formatted particle track output file are
composed of compound datatypes, and the datasets may be of length zero.
Event types (and other uniquely identifiable fields, e.g., bank types)
are stored as enumerations in HDF5. An enumeration is a numerical value
with a corresponding unique string that describes the value. The
enumeration mapping is written to the file as part of the meta data for
the corresponding dataset. In the future, some compound data types may
be extended and some fields with no value to users may be removed or
replaced. However, the MCNPTools capability to parse the current HDF5
format will be maintained to provide users a stable interface [307].

## D.3.1 Main Layout

The following sections detail the layout of the HDF5-formatted particle
track output file. The h5dump utility provided with HDF5 distributions
is a convenient way to inspect the numerical representation and
available data fields of each compound data type in a human readable
format.

The groups and datasets are organized as follows:

<!-- image -->

## D.3.2 Configuration Control

See §D.2.2 for more information on the contents of this group.

## D.3.3 Problem Information

See §D.2.5 for more information on the contents of this group.

## D.3.4 RecordLog

Table D.1 describes the record log compound data type. The record log
dataset in the ptrack group provides information on the order that
events occurred during the simulation, for all histories. Each entry in
this dataset corresponds to a particular event and contains the NPS
number, event type (described in Table D.2), and the zero-based index
into the corresponding event array, where index zero corresponds to the
first entry in the corresponding event array. The NPS number uniquely
identifies a history and may be unordered in the record log for
simulations that used multiple threads. Record log entries also include
the node number. The node number is just a placeholder for a future
feature to identify relations between events and should not be depended
upon in use of the record log.

The record log dataset only needs to be processed if the order of events
during a history is necessary for the particular analysis being
performed. Otherwise, the events in each of the individual event arrays
can be processed independently.

## D.3.4.1 Interpreting the Record Log with Secondary Particles

When secondary particles are involved, from the occurrence of physical
particle production or variance reduction, the data in the record log
will not appear in the chronological order of the particle simulation;
the order in the table is governed by how MCNP processes secondary
particles that have been added to the bank. Secondary particles are
added and removed from the bank throughout the simulation as a stack,
where the particle added last to the bank is removed and processed
first. All of the events of the primary track are processed and added to
the record log in order through termination, and then particles in the
bank are fully processed with their events added to the log in order.
The banked particles are processed in order of last added until the bank
is emptied, noting that more secondary particles can be added to the
bank during the processing of a banked particle. If reconstructing the
branching of tracks within a history is required, the location and time
of collision, surface crossing, and bank events can typically be used,
but the process is not always straight forward. There are some cases,
e.g., DXTRAN-related bank events, where it is not possible to explicitly
reconstruct the history branching.

As an example of how to interpret the record log, consider the tabular
representation of example entries given in Table D.3. This data
represents the events for two histories, identified by NPS 10 and 11.
Remember that the values in the event \_ array \_ index dataset use zero-
based indices.

For the history with NPS 10, a particle is created with a source event
and then terminates. The description of the source event is given by
index 8 in the Source dataset. The termination event is given in index
13 of

Table D.1: RecordLog compound data type fields

| Field                           | Description                                                                                                               |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| nps node event_array_index type | History identifier for this event (placeholder) zero-based index of event in corresponding array enumerated type of event |

Table D.2: Event type HDF5 enumeration

| Event type       |   Number |
|------------------|----------|
| source           |     1000 |
| bank             |     2000 |
| surface_crossing |     3000 |
| collision        |     4000 |
| termination      |     5000 |

Table D.3: Example entries of the RecordLog. Each row in the table represents the data for a single instance of the compound datatype in the RecordLog dataset. The value of node for the entries is omitted here.

|   nps |   event _ array _ index | type        |
|-------|-------------------------|-------------|
|    10 |                       8 | source      |
|    10 |                      13 | termination |
|    11 |                       9 | source      |
|    11 |                      23 | collision   |
|    11 |                      24 | collision   |
|    11 |                      14 | termination |
|    11 |                       5 | bank        |
|    11 |                      25 | collision   |
|    11 |                      15 | termination |

the Termination dataset. For the history with NPS 11, a secondary
particle track has been created, assumed here to be from a collision
during the primary track. The primary track consisted of a source event
with index 9, two collisions with indices 23 and 24, and a termination
event with index 14. The secondary particle track is created with
details given by the bank event with index 5. The secondary track then
consisted of a collision with index 25 and termination with index 15. To
determine which event created the secondary track, it would be necessary
to look at the bank type enumeration given for the index 5 bank event
and match it to the collision type of index 23 or 24. If the bank type
does not uniquely identify the collision, then the bank event's particle
location or time may be matched to the index 23 or 24 collision event
that created the particle.

Table D.4: Particle type HDF5 enumeration

| Particle type   | Number   |
|-----------------|----------|
| HEAVY_ION       | 37       |
| K_MINUS         | 36       |
| PI_MINUS        | 35       |
| ALPHA           | 34       |
| HELION          | 33       |
| TRITON          | 32       |
| DEUTERON        | 31       |
| AOMEGA_MINUS    | 30       |
| XI_PLUS         | 29       |
| AXI0            | 28       |
| ASIGMA_MINUS    | 27       |
| ASIGMA_PLUS     | 26       |
| ALAMBDA0        | 25       |
| K0_LONG         | 24       |
| K0_SHORT        | 23       |
| K_PLUS          | 22       |
| PI_ZERO         | 21       |
| PI_PLUS         | 20       |
| APROTON         | 19       |
| ANU_M           | 18       |
| ANU_E           | 17       |
| MU_PLUS         | 16       |
| SIGMA_ZERO      | - 1      |
| OMEGA_MINUS     | 15       |
| ASIGMA_ZERO     | - 2      |
| XI_MINUS        | 14       |
| PIDROGEN        | - 3      |
| XI0             | 13       |
| SIGMA_MINUS     | 12       |
| SIGMA_PLUS      | 11       |
| LAMBDA0         | 10       |
| PROTON          | 9        |
| POSITRON        | 8        |
| NU_M            | 7        |
| NU_E            | 6        |
| ANEUTRON        | 5        |
| MU_MINUS        | 4        |
| ELECTRON        | 3        |
| PHOTON          | 2        |
| NEUTRON         | 1        |

## D.3.5 Bank

Bank events represent the removal of a particle from the particle bank
during transport, i.e., the birth of a secondary particle track. For
bank events not created by a collision, e.g., a DXTRAN particle created
from a source, the reaction\_type and zaid entries will be zero.

Table D.5: Bank event compound data type fields

| Data Field                                                                                                                        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-----------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x y z u v w energy weight time nps node material_id cell_id num_collisions_this_branch reaction_type bank_type zaid particle_type | x coordinate of the particle position y coordinate of the particle position z coordinate of the particle position Particle direction cosine relative to + x axis Particle direction cosine relative to + y axis Particle direction cosine relative to + z axis Particle energy Particle weight Time at particle position History identifier Number of nodes in track from source to here Program material ID of the cell containing event Problem number of the cell containing event Count of collisions per track Number identifying the bank reaction type that created banked particle Bank type enumeration ZZZAAA for reaction isotope, following the ZAID format [§1.2.2] Particle type enumeration |

Table D.6: Reaction types that caused creation of banked particle for associated bank event. N.B.: for the specific reactions listed below, the reaction type number is different for bank events than the reaction type number for the corresponding collision event.

| Number           | Description                         |
|------------------|-------------------------------------|
| Incident neutron | Incident neutron                    |
| 1                | Inelastic S ( α,β )                 |
| 2                | Elastic S ( α,β )                   |
| - 99             | Elastic scatter / Inelastic Scatter |
| > 5              | ENDF Reaction ID (MT number)        |
| Incident photon  | Incident photon                     |
| 1                | Incoherent scatter                  |
| 2                | Coherent scatter                    |
| 3                | Fluorescence / Single Fluorescence  |
| 4                | Double Fluorescence                 |
| 5                | Pair production                     |

Table D.7: Bank type HDF5 enumeration

| bank_type            |   Number | Description                                                                   |
|----------------------|----------|-------------------------------------------------------------------------------|
| BANK_DXT_TRACK       |        1 | DXTRAN track                                                                  |
| BANK_ERG_TME_SPLIT   |        2 | Energy or time split                                                          |
| BANK_WWS_SPLIT       |        3 | Weight-window surface split                                                   |
| BANK_WWC_SPLIT       |        4 | Weight-window collision split                                                 |
| BANK_UNC_TRACK       |        5 | Forced collision-uncollided particle                                          |
| BANK_IMP_SPLIT       |        6 | Importance split                                                              |
| BANK_N_XN_F          |        7 | Neutron from ( n,xn ) or ( n, f ) and secondary particle from library protons |
| BANK_N_XG            |        8 | Photon from Neutron                                                           |
| BANK_FLUORESCENCE    |        9 | Photon from double fluorescence                                               |
| BANK_ANNIHILATION    |       10 | Photon from annihilation                                                      |
| BANK_PHOTO_ELECTRON  |       11 | Electron from photo-electric effect                                           |
| BANK_COMPT_ELECTRON  |       12 | Electron from Compton scatter                                                 |
| BANK_PAIR_ELECTRON   |       13 | Electron from pair production                                                 |
| BANK_AUGER_ELECTRON  |       14 | Auger electron from photon/x-ray                                              |
| BANK_PAIR_POSITRON   |       15 | Positron from pair production                                                 |
| BANK_BREMSSTRAHLUNG  |       16 | Bremsstrahlung from electron                                                  |
| BANK_KNOCK_ON        |       17 | Knock-on electron                                                             |
| BANK_K_X_RAY         |       18 | X-rays from electron                                                          |
| BANK_N_XG_MG         |       19 | Photon from multigroup neutron ( n, p ) reaction                              |
| BANK_N_XF_MG         |       20 | Multigroup neutron ( n, f ) reaction                                          |
| BANK_N_XN_MG         |       21 | Multigroup neutron ( n,xn ) reaction                                          |
| BANK_G_XG_MG         |       22 | Multigroup ( p,xp ) (multiplying) reaction                                    |
| BANK_ADJ_SPLIT       |       23 | Adjoint weight split - multigroup                                             |
| BANK_WWT_SPLIT       |       24 | Weight-window pseudo-collision split                                          |
| BANK_PHOTONUCLEAR    |       25 | Secondary particles from photonuclear                                         |
| BANK_DECAY           |       26 | Secondary emission from a decay                                               |
| BANK_NUCLEAR_INT     |       27 | Nuclear interaction                                                           |
| BANK_RECOIL          |       28 | Recoil particle                                                               |
| BANK_DXTRAN_ANNIHIL  |       29 | DXTRAN annihilation photon from pulse-height tally variance reduction         |
| BANK_N_CHARGED_PART  |       30 | Light ions from neutrons                                                      |
| BANK_H_CHARGED_PART  |       31 | Light ions from protons                                                       |
| BANK_N_TO_TABULAR    |       32 | Library neutrons from model neutrons                                          |
| BANK_MODEL_UPDAT1    |       33 | Secondary particles from inelastic nuclear interactions                       |
| BANK_MODEL_UPDATE    |       34 | Secondary particles from elastic nuclear interactions                         |
| BANK_DELAYED_NEUTRON |       35 | Delayed neutron                                                               |
| BANK_DELAYED_PHOTON  |       36 | Delayed photon                                                                |
| BANK_DELAYED_BETA    |       37 | Delayed electron                                                              |
| BANK_DELAYED_ALPHA   |       38 | Delayed alpha                                                                 |
| BANK_DELAYED_POSITRN |       39 | Delayed positron                                                              |
| BANK_SPON_FISS       |       40 | Spontaneous fission source particle                                           |
| BANK_SURF_SRC        |       41 | Surface Source Read (SSR) source particle                                     |

## D.3.6 Collision

Table D.8 describes the compound data type representing a particle
collision event.

Table D.8: Collision event compound data type fields

| Data Field                                                                                                              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x y z u v w energy weight time nps node material_id cell_id num_collisions_this_branch reaction_type zaid particle_type | x coordinate of the particle position y coordinate of the particle position z coordinate of the particle position Particle direction cosine relative to + x axis Particle direction cosine relative to + y axis Particle direction cosine relative to + z axis Particle energy Particle weight Time at particle position History identifier Number of nodes in track from source to here Program material ID of the cell containing event Problem number of the cell containing event Count of collisions per track Number identifying the reaction type ZZZAAA for reaction isotope, following the ZAID format [§1.2.2] particle type enumeration |

Table D.9: Reaction types for collision events.

| Number           | Description                  |
|------------------|------------------------------|
| Incident neutron | Incident neutron             |
| 4                | Inelastic S ( α,β )          |
| - 2              | Elastic S ( α,β )            |
| > 0              | ENDF Reaction ID (MT number) |
| Incident photon  | Incident photon              |
| - 1              | Incoherent scatter           |
| - 2              | Coherent scatter             |
| - 3              | Fluorescence                 |
| 4                | Pair production              |

-

Table D.10: Source event compound data type fields

| Data Field                                                                                                       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x y z u v w energy weight time nps node material_id cell_id num_collisions_this_branch source_type particle_type | x coordinate of the particle position y coordinate of the particle position z coordinate of the particle position Particle direction cosine relative to + x axis Particle direction cosine relative to + y axis Particle direction cosine relative to + z axis Particle energy Particle weight Time at particle position History identifier Number of nodes in track from source to here Program material ID of the cell containing event Problem number of the cell containing event Count of collisions per track Number identifying the source type (See nsr in MCNP5 Vol. III manual [312]) Particle type enumeration |

## D.3.7 Source

Table D.10 describes source events, which represent the creation of a
particle at the beginning of a history.

Table D.11: Surface crossing event compound data type fields

| Data Field                                                                                                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|---------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x y z u v w energy weight time nps node material_id cell_id num_collisions_this_branch surface_id surface_normal_cosine particle_type | x coordinate of the particle position y coordinate of the particle position z coordinate of the particle position Particle direction cosine relative to + x axis Particle direction cosine relative to + y axis Particle direction cosine relative to + z axis Particle energy Particle weight Time at particle position History identifier Number of nodes in track from source to here Program material ID of the cell containing event Problem number of the cell containing event Count of collisions per track Problem number of surface crossed Cosine between surface normal and particle direction Particle type enumeration |

## D.3.8 SurfaceCrossing

Table D.11 describes the surface crossing event compound data type. Note
that the ID of the surface being crossed is a floating-point value
rather than an integer value to represent both conventional surfaces
(where an integer would be adequate) and macrobody facets (which are
represented as floating-point values).

Table D.12: Termination event compound data type fields

| Data Field                                                                                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|-----------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x y z u v w energy weight time nps node material_id cell_id num_collisions_this_branch termination_type particle_type | x coordinate of the particle position y coordinate of the particle position z coordinate of the particle position Particle direction cosine relative to + x axis Particle direction cosine relative to + y axis Particle direction cosine relative to + z axis Particle energy Particle weight Time at termination History identifier Number of nodes in track from source to here Program material ID of the cell containing event Problem number of the cell containing event Count of collisions per track Number identifying the termination type Particle type enumeration |

## D.3.9 Termination

Termination events represent the end of a track within a history.

Table D.13: Particle termination type values for different particle types

| Number                  | termination_type                | Description                   |
|-------------------------|---------------------------------|-------------------------------|
| All Particle Types      | All Particle Types              | All Particle Types            |
| 1                       | ALL_PARS_LOSS_ESCAPE            | Escape                        |
| 2                       | ALL_PARS_LOSS_ENERGY_CUTOFF     | Energy cutoff                 |
| 3                       | ALL_PARS_LOSS_TIME_CUTOFF       | Time cutoff                   |
| 4                       | ALL_PARS_LOSS_WEIGHT_WINDOW     | Weight-window roulette        |
| 5                       | ALL_PARS_LOSS_CELL_IMPORTANCE   | Cell importance               |
| 6                       | ALL_PARS_LOSS_WEIGHT_CUTOFF     | Weight cutoff                 |
| 7                       | ALL_PARS_LOSS_E_OR_T_IMPORTANCE | Energy/time importance        |
| 8                       | ALL_PARS_LOSS_DXTRAN            | Attempted DXTRAN region entry |
| 9                       | ALL_PARS_LOSS_FORCED_COLLISIONS | Forced collisions             |
| 10                      | ALL_PARS_LOSS_EXP_TRANSFORM     | Exponential transform         |
| Neutrons                | Neutrons                        | Neutrons                      |
| 11                      | NEUTRON_LOSS_DOWNSCATTERING     | Loss to down scatter          |
| 12                      | NEUTRON_LOSS_CAPTURE            | Capture                       |
| 13                      | NEUTRON_LOSS_LOSS_TO_N_XN       | Loss to (n,xn)                |
| 14                      | NEUTRON_LOSS_LOSS_TO_FISSION    | Loss to fission               |
| 15                      | NEUTRON_LOSS_NUCL_INTERACTION   | Nuclear interaction           |
| 16                      | NEUTRON_LOSS_PARTICLE_DECAY     | Particle decay                |
| 17                      | NEUTRON_LOSS_TABULAR_BOUNDARY   | Tabular boundary              |
| 18                      | NEUTRON_LOSS_ELASTIC_SCATTER    | Elastic scatter               |
| Photons                 | Photons                         | Photons                       |
| 11                      | PHOTON_LOSS_COMPTON_SCATTER     | Compton scatter               |
| 12                      | PHOTON_LOSS_CAPTURE             | Capture                       |
| 13                      | PHOTON_LOSS_PAIR_PRODUCTION     | Pair production               |
| 14                      | PHOTON_LOSS_PHOTONUCLEAR_ABS    | Photonuclear absorption       |
| 15                      | PHOTON_LOSS_PHOTOFISSION        | Loss to photofission          |
| Electrons               | Electrons                       | Electrons                     |
| 11                      | ELECTRON_LOSS_SCATTERING        | Scattering loss               |
| 12                      | ELECTRON_LOSS_BREMSSTRAHLUNG    | Bremsstrahlung loss           |
| 13                      | ELECTRON_LOSS_P_ANNIHILATION    | Positron annihiliation        |
| 14                      | ELECTRON_LOSS_EXCITATION        | Excitation event              |
| 16                      | ELECTRON_LOSS_IONIZATION        | Ionization event              |
| 17                      | ELECTRON_LOSS_ERG_REJECTION     | Energy rejection > emax       |
| Other neutral particles | Other neutral particles         | Other neutral particles       |
| 11                      | NEUTRAL_LOSS_NUCL_INTERACTION   | Nuclear interaction           |
| 12                      | NEUTRAL_LOSS_ELASTIC_SCATTER    | Elastic scatter               |
| 13                      | NEUTRAL_LOSS_PARTICLE_DECAY     | Particle decay                |
| Other charged particles | Other charged particles         | Other charged particles       |
| 11                      | CHARGED_LOSS_COLL_ENERGY_LOSS   | Collisional energy loss       |
| 13                      | CHARGED_LOSS_NUCL_INTERACTION   | Nuclear interaction           |
| 14                      | CHARGED_LOSS_ELASTIC_SCATTER    | Elastic scatter               |
| 15                      | CHARGED_LOSS_PARTICLE_DECAY     | Particle decay                |
| 16                      | CHARGED_LOSS_CAPTURE            | Capture                       |
| 17                      | CHARGED_LOSS_TABULAR_SAMPLING   | Tabular sampling              |
| 18                      | CHARGED_LOSS_COSY_APERTURE_HIT  | Cosy aperture hit             |
| 19                      | CHARGED_LOSS_COSY_FAULTS        | Cosy faults                   |
| 20                      | CHARGED_LOSS_ERG_REJECTION      | Energy rejection > emax       |
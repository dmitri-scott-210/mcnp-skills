# MCNP Template Catalog

## Shielding Templates

### shielding_sphere.i
**Purpose**: Point source in spherical shield
**Geometry**: 2 cells (shield + void)
**Source**: Point isotropic
**Tallies**: F2 (surface current), F4 (flux)
**Parameters**: Shield radius, material, source strength

### shielding_slab.i
**Purpose**: Plane source through slab
**Geometry**: 3-layer slab
**Source**: Planar
**Tallies**: F2 (transmission)
**Parameters**: Slab thickness, layers, materials

## Criticality Templates

### criticality_bare.i
**Purpose**: Bare fissile sphere keff
**Geometry**: Single sphere
**Source**: KSRC at center
**Tallies**: F4 (flux), F7 (fission)
**Parameters**: Core radius, material density

### criticality_reflected.i
**Purpose**: Reflected sphere keff
**Geometry**: Core + reflector
**Source**: KSRC distributed
**Tallies**: Detailed flux/fission profiles
**Parameters**: Core/reflector radii, materials

## Dose Templates

### dose_ambient.i
**Purpose**: Ambient dose equivalent H*(10)
**Geometry**: Void with detector sphere
**Source**: Point source
**Tallies**: F4+FM (flux to dose conversion)
**Parameters**: Distance, source energy, DE/DF factors

### dose_effective.i
**Purpose**: Effective dose
**Geometry**: Phantom with organs
**Source**: External field
**Tallies**: Organ doses
**Parameters**: Phantom dimensions, ICRP coefficients

## Activation Templates

### activation_simple.i
**Purpose**: Basic activation calculation
**Geometry**: Target volume
**Source**: Neutron flux
**Tallies**: F4 (flux), F6 (heating)
**Parameters**: Target material, irradiation time, BURN card

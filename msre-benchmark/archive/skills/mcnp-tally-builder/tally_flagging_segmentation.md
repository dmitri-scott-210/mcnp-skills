# Tally Flagging and Segmentation

## Overview

MCNP provides powerful features to track particle histories and subdivide tallies without additional geometry complexity through cell/surface flagging (CF/SF) and tally segmentation (FS/SD).

## Cell Flagging (CF Card)

### Purpose

The CF card flags particles when they leave designated cells, allowing separate tallies of flagged contributions.

### Syntax

```
CFn c1 c2 c3 ... cK
```

- `n` - Tally number
- `ck` - Cell number to flag upon exit

### Flagging Behavior

**Basic Flagging:**
```
F4:n 10 20
CF4 5
```
- Flag turns ON when particle exits cell 5
- Tally in cells 10 and 20 separately shows:
  1. Total contributions (all particles)
  2. Flagged contributions (particles that left cell 5)

**Negative Cell Numbers:**
```
CF4 -5
```
- Requires collision in cell 5 before flagging
- Exit alone does not set flag
- Use case: Particles that interacted in specific region

### Multiple Cells

```
CF4 3 4 5
```
- Flag set if particle exits ANY listed cell (OR logic)
- Once flagged, remains flagged for that particle and progeny

### Progeny Flagging

**Critical Feature:**
- If neutron is flagged, all secondary particles (photons, etc.) inherit flag
- Photon from flagged neutron will be tallied as flagged
- Tracks entire particle tree ancestry

**Example:**
```
F4:p 10          $ Photon flux in cell 10
CF4 5            $ Flag if exited cell 5
```
Result: Tallies photons from neutrons that passed through cell 5

## Surface Flagging (SF Card)

### Purpose

The SF card flags particles when they cross designated surfaces.

### Syntax

```
SFn s1 s2 s3 ... sK
```

- `n` - Tally number
- `sk` - Surface number to flag upon crossing

### Flagging Behavior

**Immediate Flagging:**
- Flag set upon any crossing of surface
- Direction (entering/leaving) does not matter
- No collision requirement

**Example:**
```
F4:n 15 20
SF4 100
```
Separate tally of particles that crossed surface 100

### Particle Killed on Surface

**Important Caution:**
- Particle killed on surface: Surface flag SET, cell flag NOT set
- Use SF rather than CF for surface-terminated particles

## Combined CF and SF Usage

### Syntax

Both cards can be used for same tally:

```
F4:n 10
CF4 3 4
SF4 50 60
```

### Combined Logic

- Flag set if particle exits cells 3 OR 4 OR crosses surfaces 50 OR 60
- Any condition triggers flagging
- Only ONE flagged output produced (not separate for CF vs SF)

### Use Cases

**Shielding Analysis:**
```
F4:n 100              $ Detector cell
CF4 -10               $ Collided in shield
SF4 20                $ Crossed outer boundary
```
Tracks particles that both interacted in shield AND crossed boundary

## Tally Segmentation (FS Card)

### Purpose

Subdivide cells or surfaces for tallying without additional geometry complexity.

### Syntax

```
FSn s1 s2 ... sK [T]
```

- `n` - Tally number
- `sk` - Segmenting surface with sense
- `T` - Optional: Provide total across all segments

### Segmentation Rules

**K Surfaces Create K+1 Bins:**

```
FS4 -10 20
```
Creates 3 bins:
1. Negative sense to surface 10
2. Positive sense to surface 20 (excluding bin 1)
3. Everything else (neither bin 1 nor 2)

**Order and Sense Matter:**
- Bins processed in order listed
- Each bin excludes regions already assigned
- Sign on surface determines included sense

### Example: Subdividing Cell

**Geometry:**
Cell 5 is large volume, subdivide into regions without creating new cells

**Setup:**
```
F4:n 5                $ Tally in cell 5
FS4 -10 11 T          $ Subdivide with surfaces 10 and 11
```

**Result:** 4 tally bins
1. Part of cell 5 with negative sense to surface 10
2. Part of cell 5 with positive sense to surface 11 (not already in bin 1)
3. Rest of cell 5 (everything else)
4. Total over entire cell 5

### Example: Subdividing Surface

**Geometry:**
Surface 1 is detector, want flux in different regions

**Setup:**
```
F2:n 1                $ Flux across surface 1
FS2 -20 -30           $ Subdivide surface
```

**Result:** 3 flux bins across different portions of surface 1

### Everything Else Bin

**Important Feature:**
- Bin K+1 contains all regions not covered by previous K bins
- Can be empty if surfaces completely partition region
- Useful for validation (should sum to total if T present)

### Zero Scores in Bins

**Possible Issues:**
- Surfaces don't actually intersect tally region
- Sense incorrectly specified
- Surfaces partition incorrectly

**Debugging:**
- Check geometry with MCNP plotter
- Verify surface senses in cell definitions
- Test with T option to ensure bins sum correctly

## Segment Divisor (SD Card)

### Purpose

Provide volumes, areas, or masses for segmented tallies when MCNP cannot calculate automatically.

### Syntax

```
SDn (d11 d12 ... d1M) (d21 d22 ... d2M) ...
```

- `n` - Tally number
- `K` - Number of cells/surfaces on F card
- `M` - Number of segment bins (K+1 from FS, or K+2 if FS has T)
- `dkm` - Divisor for k-th cell/surface, m-th segment

### Divisor Hierarchy

**For Non-Segmented Tallies (F2, F4, F6, F7):**
1. Non-zero entry on SD card
2. Non-zero entry on VOL or AREA card
3. Volume/area/mass calculated by MCNP
4. Fatal error if none available

**For Segmented Tallies (with FS card):**
1. Non-zero entry on SD card
2. Volume/area/mass calculated by MCNP (if possible)
3. Fatal error if neither available

**For F1 Tallies:**
1. Non-zero entry on SD card
2. No divisor (current not divided)

### SD for F1 Custom Divisor

**Use Case:** Surface current density (current per unit area)

```
F1:n 10
SD1 100.5        $ Divide by area to get current density
```

MCNP normally does not divide F1, but SD allows custom normalization

### SD for Repeated Structures

**Two Distinct Options:**

1. **Volumes for lattice elements not in problem:**
```
SD4 1            $ Each lattice element divided by 1 cm³
```

2. **Cell filling universe has volume:**
```
SD4 5.23         $ Use volume 5.23 cm³ for each lattice element
```

Consult Chapter 5.09 Section 5.9.15 for detailed repeated structure usage

### Parentheses Usage

Optional for grouping:
```
SD4 1.0 2.5 3.7   $ Without parentheses (single cell on F card)
SD4 (1.0 2.5) (3.5 4.1 5.2)  $ With parentheses (multiple cells)
```

### Example: Segmented Cell with SD

**Problem:** Cell 10 subdivided by planes 20 and 30, but MCNP cannot calculate segment volumes

**Setup:**
```
F4:n 10
FS4 -20 30 T
SD4 50.0 30.0 20.0 100.0    $ Segment 1: 50 cm³, segment 2: 30, segment 3: 20, total: 100
```

Manually calculated volumes for 3 segments plus total

## Practical Applications

### Application 1: Shielding Penetration Analysis

**Objective:** Determine flux contributions from particles that passed through specific shielding layers

```
F4:n 100          $ Detector cell
CF4 10 11 12      $ Shield layers
```

**Result:**
- Total flux in detector
- Flux from particles that transited shield layers

### Application 2: Regional Dose without Extra Cells

**Objective:** Dose in different regions of organ without complex geometry

```
F6:n 50           $ Organ cell
FS6 -10 11 -12 T  $ Surfaces defining anatomical regions
SD6 100 80 60 50 290  $ Masses of each region (g)
```

**Result:** Dose (MeV/g) in 4 sub-regions of organ

### Application 3: Detector Position Study

**Objective:** Compare detector response at multiple positions using single geometry

```
F5:n 0 0 10 0.1   $ Point detector
FS5 -20 30        $ Surfaces defining position bins
```

**Result:** Detector response as function of position

### Application 4: Streaming Path Identification

**Objective:** Identify which penetrations contribute to dose

```
F4:n 1000         $ Room
CF4 -10 -11 -12   $ Penetration 1, 2, 3 (with collision)
```

**Result:** Separate tally of particles that collided in each penetration

### Application 5: Time-Dependent Shield Effectiveness

**Objective:** Track buildup of activated shielding contributions

```
F4:n 200          $ Beyond shield
CF4 15            $ Shield activation region
T4 0 1e3 1e6 1e9  $ Time bins
```

**Result:** Time-dependent flux from activated particles

## Best Practices

1. **Use MCNP plotter** - Visualize segmenting surfaces before running
2. **Test with T option** - Verify segments sum to total
3. **Check everything else bin** - Unexpected scores indicate geometry error
4. **Combine CF and SF sparingly** - Complex logic can be hard to interpret
5. **Document flag purpose** - Comment cards explaining flagging strategy
6. **Verify SD hierarchy** - Ensure MCNP uses intended volumes/areas/masses
7. **Use negative cells for physics** - CF with negative numbers for collision tracking
8. **Consider progeny flags** - Remember secondary particles inherit flags
9. **Avoid over-segmentation** - Too many bins reduce statistics per bin
10. **Validate with simpler case** - Test flagging logic on known geometry

## Limitations and Considerations

### Not Compatible With

- Detector (F5) tallies - Use FT ICD keyword instead
- DXTRAN spheres
- Pulse-height (F8) tallies (for CF/SF)

### Performance Impacts

- Flagging: Minimal overhead, just sets particle attribute
- Segmentation: More bins = more memory, more output, same runtime
- SD card: No performance impact, just normalization

### Statistical Considerations

- Flagged tallies typically have higher uncertainty (subset of particles)
- Segmented tallies split scores across bins (variance per bin increases)
- Ensure adequate NPS for acceptable statistics in all bins

## See Also

- **SKILL.md** - Main tally workflow
- **advanced_tally_types.md** - Radiography uses FS for pixel grids
- **repeated_structures_tallies.md** - SD card for lattice volumes
- **dose_and_special_tallies.md** - FT ICD as alternative to CF/SF for detectors
- **Chapter 5.09 Sections 5.9.12-5.9.15** - MCNP Manual CF/SF/FS/SD details

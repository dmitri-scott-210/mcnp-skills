# Advanced Tally Types - Radiography Tallies

## Overview

MCNP provides specialized tally types for radiography applications that extend beyond the standard F1-F8 tallies. These tallies enable imaging capabilities for non-destructive testing, inspection, and visualization of internal structures.

## Radiography Tally Types

### FIP: Pinhole Image Tally

The FIP tally simulates a pinhole camera by treating a point detector as a pinhole projection.

**Syntax:**
```
FIPn:p x y z R
```

**Parameters:**
- `n` - Tally number
- `x y z` - Pinhole location (detector position)
- `R` - Pinhole radius (cm)

**Image Formation:**
- Creates 2D projection from 3D geometry
- Uses FS card to define pixel grid
- Records particles passing through pinhole radius R
- Image plane perpendicular to viewing direction

**Grid Definition:**
```
FIP4:n 0 0 50 0.1          $ Pinhole at z=50, radius 0.1 cm
FS4 -10 10                 $ Grid surfaces for x and y bins
C4 ...                     $ Optional angular bins for pixels
```

### FIR: Planar Radiograph Tally

The FIR tally creates a transmitted radiograph on a rectangular detector plane.

**Syntax:**
```
FIRn:p x y z i j k
```

**Parameters:**
- `x y z` - Reference point on detector plane
- `i j k` - Normal vector to detector plane

**Characteristics:**
- Records particles reaching detector plane
- Uses FS card for pixel grid (rows and columns)
- Transmitted intensity image (attenuation-based)
- Suitable for parallel beam or broad source geometries

**Example:**
```
FIR14:p 0 0 100 0 0 1      $ Detector at z=100, normal in +z
FS14 -20 -10 10 20         $ 4 surfaces creating 5×5 pixel grid
```

### FIC: Cylindrical Radiograph Tally

The FIC tally creates a radiograph on a cylindrical detector surface.

**Syntax:**
```
FICn:p x y z i j k R
```

**Parameters:**
- `x y z` - Cylinder axis reference point
- `i j k` - Cylinder axis direction vector
- `R` - Cylinder radius

**Applications:**
- Circumferential inspection
- Pipe/tube radiography
- 360° imaging around axis

**Grid Setup:**
```
FIC24:n 0 0 0 0 0 1 50     $ Cylinder axis along z, radius 50 cm
FS24 -30 30                $ Axial and angular bins
C24 ...                    $ Angular bins around cylinder
```

## Image Grid Configuration

### Using FS Card for Pixel Bins

The FS (segment) card divides the image plane into pixel bins:

**For FIP (pinhole):**
```
FIP4:p 0 0 50 0.1
FS4 -10 -5 0 5 10 -20 -10 0 10 20  $ 5×5 grid
```
Creates 25 pixels (5 horizontal × 5 vertical bins)

**For FIR (planar):**
```
FIR14:p 0 0 100 0 0 1
FS14 (-25 -15 -5 5 15 25) (-30 -10 10 30)  $ 6×4 grid
```
Creates 24 pixels arranged in rows and columns

### Using C Card for Angular Resolution

For cylindrical or angular binning:

```
FIC24:n 0 0 0 0 0 1 50
C24 -1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1  $ 10 angular bins
```

## Direct-Only Contributions

### NOTRN Card Integration

For clearer radiographs, limit to uncollided (direct) particles:

```
NOTRN 1 0 0         $ Track only primaries (no secondaries)
FIR14:p 0 0 100 0 0 1
NPS 1e8 1e7         $ 10^8 total, limit direct to 10^7
```

**Second NPS Entry:**
- First value: Total particle histories
- Second value: Maximum direct contributions
- Prevents excessive direct particle tracking
- Balances between direct signal and scattered background

**Effect:**
- Sharper images (reduced scatter blur)
- Lower statistics in scattered regions
- Faster convergence for transmission imaging
- May miss important scattered contributions

## Image Resolution and Sampling

### Pixel Size Considerations

**Spatial Resolution:**
- Smaller pixels = higher resolution, more bins, longer runtime
- Pixel size should match detector capabilities
- Consider source collimation and geometry magnification

**Typical Grid Sizes:**
- Low resolution: 10×10 to 25×25 pixels
- Medium resolution: 50×50 to 100×100 pixels
- High resolution: 200×200 to 500×500 pixels (expensive)

**Example 100×100 Grid:**
```
FIR14:p 0 0 100 0 0 1
c Create 100 surfaces in x direction
FS14 -50 -49 -48 ... -1 0 1 ... 48 49 50  $ (101 values for 100 bins)
     -50 -49 -48 ... -1 0 1 ... 48 49 50  $ Both x and y
```

### Statistical Considerations

**Variance per Pixel:**
- Each pixel is independent tally bin
- Requires sufficient particle crossings per pixel
- Edge pixels typically have lower statistics

**Recommended NPS:**
- Low resolution (25×25): 10^6 - 10^7 particles
- Medium resolution (100×100): 10^7 - 10^8 particles
- High resolution (500×500): 10^8 - 10^9 particles

## Output and Visualization

### MCNP Output Format

Radiography tallies produce:
- Array of pixel values (tally results)
- Statistical uncertainties per pixel
- Can be output to MCTAL file for processing

### Post-Processing Tools

**gridconv Utility:**
- Converts MCTAL radiography data to image formats
- Supports various output formats (ASCII, binary)
- Can generate viewable image files

**MCNP Tally Plotter:**
- Built-in visualization (if available)
- Displays 2D radiograph images
- Color mapping for intensity values

**External Tools:**
- Python with matplotlib or PIL
- MATLAB image processing
- ImageJ or other scientific imaging software

### Example Post-Processing Workflow

1. Run MCNP with radiography tally
2. Extract pixel data from MCTAL file
3. Reshape data to 2D grid (rows × columns)
4. Apply normalization/scaling
5. Display as grayscale or false-color image
6. Overlay geometry outlines if needed

## Integration with Other Features

### Variance Reduction for Radiography

**Weight Windows:**
- Focus importance on direct path to detector
- Reduce scattered particle contribution
- Speeds convergence for transmission images

**Example:**
```
WWP:p 5 5 5 0 0 -1        $ Weight window setup
WWGE:p 0.7                $ Energy for weight windows
FIR14:p 0 0 100 0 0 1     $ Detector plane
```

### Source Considerations

**Broad Source:**
- Uniform illumination over object
- Parallel beam approximation if far from object

**Point Source:**
- Creates magnification (cone beam geometry)
- Geometric blurring considerations
- Penumbra effects from finite source size

### Detector Response

**DE/DF Cards:**
- Model energy-dependent detector efficiency
- Account for detector material attenuation
- Realistic image intensity

```
FIR14:p 0 0 100 0 0 1
DE14 0.01 0.1 1.0 10.0    $ Energy bins (MeV)
DF14 0.5 0.8 0.95 0.98    $ Detection efficiency
```

## Common Applications

### Non-Destructive Testing

- Weld inspection
- Defect detection in castings
- Crack identification
- Corrosion mapping

### Cargo Scanning

- Container inspection
- Vehicle scanning
- Large object radiography

### Medical Imaging Simulation

- X-ray simulation
- CT geometry validation
- Dose assessment

### Industrial Radiography

- Pipeline inspection
- Component verification
- Quality assurance imaging

## Best Practices

1. **Start with coarse grid** - Test setup with low resolution, then refine
2. **Use NOTRN judiciously** - Direct-only may miss important physics
3. **Optimize source position** - Consider magnification and coverage
4. **Validate geometry** - Use MCNP plotter before running expensive radiograph
5. **Check detector distance** - Ensure particles reach detector plane
6. **Monitor edge effects** - Pixels at grid edges may have poor statistics
7. **Use appropriate particle type** - Photons for X-ray, neutrons for neutron radiography
8. **Consider energy bins** - Energy-resolved radiography shows contrast mechanisms
9. **Parallel computations** - High-resolution radiography benefits from parallel runs
10. **Archive MCTAL files** - Save for reprocessing with different visualization parameters

## See Also

- **SKILL.md** - Main tally-builder workflow
- **tally_flagging_segmentation.md** - FS card details for grid setup
- **dose_and_special_tallies.md** - FT card special features
- **Chapter 5.09 Section 5.9.1.3** - MCNP Manual radiography tallies

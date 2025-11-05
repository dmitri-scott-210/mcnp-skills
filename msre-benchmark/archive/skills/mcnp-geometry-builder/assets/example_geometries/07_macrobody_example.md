# Example 7: Macrobody Usage

## Purpose
Demonstrates macrobody shortcuts for common geometries.

## Macrobodies Used
- **RPP**: Rectangular parallelepiped (box)
  - Format: `RPP xmin xmax ymin ymax zmin zmax`
- **RCC**: Right circular cylinder
  - Format: `RCC x y z vx vy vz R` (base point, axis vector, radius)

## Advantages
- Fewer surface cards needed
- Clearer intent in geometry
- Common shapes defined quickly

## Limitations
- Cannot reference facets with SSR/SSW/SF/PTRAC/MCTAL
- Less flexible than primitive surfaces
- Debugging harder (can't plot individual facets easily)

## Usage
```bash
mcnp6 inp=07_macrobody_example.i
```

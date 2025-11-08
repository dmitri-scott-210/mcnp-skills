# Example 6: Transformed Geometry

## Purpose
Demonstrates surface transformations using *TR cards for rotated geometry.

## Concepts
- **Asterisk prefix** on surface (*1, *2) indicates transformation
- **TR cards** define rotation matrices and translation
- **Direction cosines** specify new coordinate system

## Geometry
- Cylinder 1: Rotated to lie along X-axis (TR1)
- Cylinder 2: Rotated to lie along Y-axis (TR2)
- Cylinder 3: Along Z-axis (no transformation needed)

## Transformation Matrices
- **TR1**: Rotates CZ (Z-axis cylinder) to X-axis
  - Direction cosines: (0,0,1), (0,1,0), (1,0,0)
- **TR2**: Rotates CZ to Y-axis
  - Direction cosines: (0,1,0), (1,0,0), (0,0,1)

## Usage
```bash
mcnp6 inp=06_transformed_geometry.i
```

## Learning Points
1. Asterisk (*) on surface number activates transformation
2. TR card has 12 numbers: 3 translation + 9 rotation matrix
3. Direction cosines must be orthonormal
4. Asterisk on TR card indicates surface (vs cell) transformation

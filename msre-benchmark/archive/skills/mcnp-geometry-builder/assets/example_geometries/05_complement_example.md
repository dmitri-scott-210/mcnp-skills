# Example 5: Box with Cylindrical Hole (Complement Operator)

## Purpose
Demonstrates complement operator (#) for creating void regions and cutouts.

## Concepts Illustrated
- **Complement operator (#n)** - All space NOT in cell n
- **Complex Boolean**: Intersection AND complement = cutout pattern
- **Cell reference**: Cell 10 defines hole, cell 1 excludes it
- **Union in graveyard**: (outside OR outside OR ...)

## Geometry
- **Cell 1**: Iron box (20×20×40 cm) with cylindrical hole through center
  - Geometry: `-1 2 -3 4 -5 6 #10` = Box AND (NOT cell 10)
- **Cell 2**: Void inside cylinder (dummy cell, r < 3 cm)
- **Cell 10**: Defines cylindrical region to be excluded from cell 1
- **Cell 3**: Graveyard (union of 6 outer regions)

## Materials
- M1: Iron at 10.0 g/cm³

## Complement Operator Usage
**Cell 1** uses `#10` to exclude cell 10's geometry:
- Without #10: Solid box fills entire region
- With #10: Box has cylindrical hole where cell 10 exists

**Cell 10** defines the exclusion region but could have any material (here it's void).

## Learning Points
1. **#n operator**: Excludes all space occupied by cell n
2. **Order matters**: Cell n must be defined before using #n
3. **Void cutouts**: Cell 10 is void, but #10 works with any material
4. **Multiple complements**: Can use #10 #20 #30 for multiple holes

## Usage
```bash
mcnp6 inp=05_complement_example.i
```

## Modifications to Try
- Add multiple cylinders (#10 #20 #30)
- Use sphere instead of cylinder for spherical void
- Make cell 10 a different material (water-filled tube)
- Try nested complements

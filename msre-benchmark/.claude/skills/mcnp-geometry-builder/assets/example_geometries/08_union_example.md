# Example 8: Union Operator

## Purpose
Demonstrates union operator (:) for combining overlapping regions.

## Geometry
- Two spheres at (-5,0,0) and (5,0,0), both R=8 cm
- They overlap in center region
- Cell 1 fills UNION of both spheres: `-1 : -2` = inside 1 OR inside 2

## Learning Points
- Union (:) evaluated LAST in Boolean precedence
- Overlap region belongs to cell 1 (not an error)
- Graveyard is outside BOTH: `1 2` (outside 1 AND outside 2)

## Usage
```bash
mcnp6 inp=08_union_example.i
```

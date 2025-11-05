# Valid Cubic Lattice (LAT=1)

**Purpose**: Demonstrate correct cubic lattice specification with proper fill array dimensions.

**Key Features**:
- Cell 100: LAT=1 (cubic lattice) with u=10
- Fill array: `-1:1 -1:1 0:0` = 3×3×1 = 9 values
- Array contains: 9 values (correct match)
- Lattice cell is void (material 0) - required
- Boundary: RPP macrobody (rectangular box) - optimal for LAT=1
- Universes 1 and 2 properly defined

**Validation Checks**:
- ✓ LAT=1 valid lattice type
- ✓ FILL parameter present
- ✓ Lattice cell is void (m=0)
- ✓ Fill array dimensions match: 3×3×1 = 9 values
- ✓ All referenced universes defined (u=1, u=2)
- ✓ Appropriate boundary surfaces (RPP)

**Expected Results**:
```
Lattice validation: PASS
  Cell 100: LAT=1 (cubic), 9 values expected, 9 found
  Universe 1: defined
  Universe 2: defined
  Boundary: RPP (optimal for cubic lattice)
```

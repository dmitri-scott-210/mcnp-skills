# Valid Simple Universe Fill

**Purpose**: Demonstrate correct universe definition and fill reference.

**Key Features**:
- Cell 1: Real world cell with `fill=1`
- Cell 100: Universe 1 definition with `u=1`
- All universe references are valid
- No circular dependencies

**Validation Checks**:
- ✓ Universe 1 defined (cell 100)
- ✓ Universe 1 used in fill= (cell 1)
- ✓ No undefined references
- ✓ No circular references
- ✓ Single-level hierarchy (depth=1)

**Expected Results**:
```
Universe validation: PASS
  Defined: [1]
  Used: [1]
  Undefined: []
  Hierarchy depth: 1
```

# Universe Reference Map

**Input File:** `_______________________`
**Date:** `_______________________`
**Created by:** `_______________________`

---

## Overview

This document maps the universe hierarchy for the MCNP input file, showing all universe definitions, their relationships, and purposes.

### Summary Statistics

- **Total universes:** `_______`
- **Maximum nesting depth:** `_______` levels
- **Lattice cells:** `_______`
- **Fill arrays:** `_______`

---

## Universe Hierarchy

### Level 0: Real World (u=0 - implicit)

**Purpose:** `[Describe what level 0 represents - e.g., "Reactor vessel and surrounding environment"]`

**Cells:**
- Cell `___`: `[Description]`
- Cell `___`: `[Description]`
- Cell `___`: `[Description]`

**Fills:**
- Fills universe `___` (to level 1)
- Fills universe `___` (to level 1)

**Notes:**
```
[Add any special notes about real world geometry]
```

---

### Level 1: `[Level Name - e.g., "Core Region"]`

#### Universe 1

**Purpose:** `[Describe what this universe represents]`

**Filled by:** Universe `___` (from level `___`)

**Cells:**
- Cell `___`: `[Description - material, geometry]`
- Cell `___`: `[Description]`

**Fills:**
- Fills universe `___` (to level 2)
- Fills universe `___` (to level 2)

**Cell Type:**
- ☐ Standard cell
- ☐ Lattice cell (LAT=`___`)
- ☐ Fill cell (simple fill)

**Notes:**
```
[Add notes about this universe - special features, design choices, etc.]
```

---

#### Universe 2

**Purpose:** `[Description]`

**Filled by:** Universe `___` (from level `___`)

**Cells:**
- Cell `___`: `[Description]`

**Fills:**
- Fills universe `___` (to level 2)

**Cell Type:**
- ☐ Standard cell
- ☐ Lattice cell (LAT=`___`)
- ☐ Fill cell (simple fill)

**Notes:**
```
[Add notes]
```

---

### Level 2: `[Level Name]`

#### Universe 10

**Purpose:** `[Description]`

**Filled by:** Universe `___` (from level `___`)

**Cells:**
- Cell `___`: `[Description]`

**Fills:**
- Fills universe `___` (to level 3)
- ☐ Terminal universe (no fills)

**Cell Type:**
- ☐ Standard cell
- ☐ Lattice cell (LAT=`___`)
- ☐ Fill cell (simple fill)

**If Lattice:**
- Lattice type: LAT=`___` (☐ cubic ☐ hexagonal)
- Array dimensions: `___ × ___ × ___`
- Fill array size: `___` values
- Universes used: `[list]`

**Notes:**
```
[Add notes]
```

---

### Level 3: `[Level Name]`

#### Universe 100

**Purpose:** `[Description]`

**Filled by:** Universe `___` (from level `___`)

**Cells:**
- Cell `___`: `[Description - include material and density]`

**Fills:**
- ☐ Terminal universe (has material, no fills)
- ☐ Fills universe `___`

**Cell Type:**
- ☐ Standard cell with material
- ☐ Lattice cell (LAT=`___`)
- ☐ Fill cell

**Notes:**
```
[Add notes about this terminal universe - materials, physics, etc.]
```

---

## Lattice Details

### Lattice Cell `[number]` (Universe `[u_num]`)

**Type:** LAT=`___` (☐ cubic ☐ hexagonal)

**Declaration:**
```
fill= i1:i2 j1:j2 k1:k2
```

**Dimensions:**
- i-direction: `___` to `___` (`___` elements)
- j-direction: `___` to `___` (`___` elements)
- k-direction: `___` to `___` (`___` elements)
- Total array size: `___ × ___ × ___ = ___` values

**Universe Composition:**
| Universe | Description | Count | Percentage |
|----------|-------------|-------|------------|
| `___`    | `[desc]`    | `___` | `___%`     |
| `___`    | `[desc]`    | `___` | `___%`     |

**Layout:**
```
[Describe the spatial arrangement - e.g., "Central control rod surrounded by fuel assemblies"]
```

---

## Terminal Universes

List all terminal universes (those that don't fill other universes):

| Universe | Level | Description | Material | Filled By |
|----------|-------|-------------|----------|-----------|
| `___`    | `___` | `[desc]`    | `___`    | u=`___`   |
| `___`    | `___` | `[desc]`    | `___`    | u=`___`   |

---

## Performance Optimization

### Negative Universe Candidates

Universes that could use negative numbers for optimization (`u=-N`):

| Universe | Current | Recommended | Level | Reason |
|----------|---------|-------------|-------|--------|
| `___`    | u=`___` | u=-`___`    | `___` | `[fully enclosed]` |
| `___`    | u=`___` | u=-`___`    | `___` | `[fully enclosed]` |

**Notes:**
- Only use negative universes if cells are FULLY enclosed
- Test with positive first, then switch to negative and verify results match

---

## Dependency Graph

```
u=0 (real world)
├── u=1 (level 1)
│   ├── u=10 (level 2)
│   │   └── u=100 (level 3 - terminal)
│   └── u=20 (level 2 - terminal)
└── u=2 (level 1)
    └── u=30 (level 2 - terminal)
```

---

## Validation Status

- [ ] All universes documented
- [ ] No circular references
- [ ] All fills have corresponding definitions
- [ ] Nesting depth acceptable
- [ ] Terminal universes identified
- [ ] Optimization opportunities noted

**Validated by:** `_______________________`
**Date:** `_______________________`

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| `___` | 1.0 | Initial creation | `___` |
| `___` | `___` | `[changes]` | `___` |

---

**END OF UNIVERSE REFERENCE MAP**
